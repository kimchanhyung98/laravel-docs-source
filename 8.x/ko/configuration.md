# 설정(Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
- [설정값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [디버그 모드](#debug-mode)
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일들은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에 대한 설명이 문서화되어 있으므로, 파일을 살펴보며 사용 가능한 옵션에 익숙해지시기 바랍니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 타임존, 암호화 키 등과 같은 다양한 핵심 설정값을 구성할 수 있습니다.

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 다른 설정값을 사용하는 것이 도움이 될 때가 많습니다. 예를 들어, 로컬에서는 프로덕션 서버와는 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

이 과정을 간단하게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 신규로 설치한 Laravel에는 루트 디렉터리에 여러 일반적인 환경 변수를 정의한 `.env.example` 파일이 포함되어 있습니다. 설치 과정 중에 이 파일은 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬 또는 프로덕션 웹 서버에서 실행 중인지에 따라 다를 수 있는 몇 가지 일반적인 설정값이 들어 있습니다. 이 값들은 Laravel의 `env` 함수를 사용해 `config` 디렉터리에 위치한 다양한 설정 파일에서 불러와집니다.

여러 명이 함께 개발을 하고 있다면, `.env.example` 파일을 계속 애플리케이션과 함께 포함시키는 것이 좋습니다. 예시 설정 파일에 플레이스홀더 값을 명확하게 넣어두면, 팀의 다른 개발자들이 애플리케이션 실행에 필요한 환경 변수가 무엇인지 쉽게 알 수 있습니다.

> {tip} `.env` 파일의 모든 변수는 서버나 시스템 레벨의 환경 변수 등 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 소스 컨트롤에 커밋해서는 안 됩니다. 애플리케이션을 사용하는 각 개발자나 서버가 서로 다른 환경 설정을 필요로 할 수 있기 때문입니다. 또한, 소스 저장소에 불법 침입자가 접근하게 될 경우 민감한 자격 증명이 노출될 수 있으므로 보안상 위험합니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 불러오기 전에, Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지 혹은 `--env` CLI 인자가 지정되었는지 확인합니다. 만약 그렇다면, Laravel은 `.env.[APP_ENV]` 파일이 존재하면 이를 불러오려고 시도합니다. 해당 파일이 없다면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 기본적으로 문자열로 파싱되지만, `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 일부 예약어 값이 정의되어 있습니다:

`.env` 값       | `env()` 반환값
--------------- | --------------
true            | (bool) true
(true)          | (bool) true
false           | (bool) false
(false)         | (bool) false
empty           | (string) ''
(empty)         | (string) ''
null            | (null) null
(null)          | (null) null

공백이 포함된 값을 환경 변수로 지정해야 한다면, 값을 큰따옴표로 감싸서 작성할 수 있습니다:

    APP_NAME="My Application"

<a name="retrieving-environment-configuration"></a>
### 환경 설정값 가져오기

이 파일에 정의된 모든 변수는 애플리케이션에 요청이 들어올 때 `$_ENV` PHP 슈퍼 글로벌에 로드됩니다. 하지만 설정 파일에서 `env` 헬퍼 함수를 이용해 이러한 변수값을 가져올 수 있습니다. 실제로 Laravel 설정 파일을 살펴보면 많은 옵션이 이 헬퍼를 이미 사용하고 있음을 알 수 있습니다:

    'debug' => env('APP_DEBUG', false),

`env` 함수에 전달되는 두 번째 인자는 "기본값"입니다. 지정한 키에 해당하는 환경 변수가 없을 경우 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드를 통해 접근할 수 있습니다:

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

또한, `environment` 메서드에 인자를 전달하여 현재 환경이 특정 값과 일치하는지 확인할 수 있습니다. 환경이 전달한 값 중 하나와 일치하면 메서드는 `true`를 반환합니다:

    if (App::environment('local')) {
        // 현재 환경이 local일 때
    }

    if (App::environment(['local', 'staging'])) {
        // 현재 환경이 local이거나 staging일 때...
    }

> {tip} 서버 레벨의 `APP_ENV` 환경 변수를 정의하면 애플리케이션 환경 감지가 이를 통해 덮어쓰기 됩니다.

<a name="accessing-configuration-values"></a>
## 설정값 접근하기

애플리케이션 어디서든 전역 `config` 헬퍼 함수를 이용해 설정값에 쉽게 접근할 수 있습니다. 파일명과 옵션명을 포함한 "닷(dot) 표기법"으로 접근할 수 있습니다. 설정 옵션이 존재하지 않을 때 반환될 기본값도 지정할 수 있습니다:

    $value = config('app.timezone');

    // 설정값이 없으면 기본값을 가져옵니다...
    $value = config('app.timezone', 'Asia/Seoul');

실행 중에 설정값을 변경하려면, `config` 헬퍼에 배열을 전달하세요:

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션의 성능을 높이기 위해 `config:cache` Artisan 명령어를 사용하여 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이 명령은 애플리케이션의 모든 설정 옵션을 하나의 파일로 합쳐 프레임워크가 빠르게 불러올 수 있도록 도와줍니다.

일반적으로 프로덕션 배포 과정에서 `php artisan config:cache` 명령어를 실행해야 합니다. 개발 중에는 설정 옵션을 자주 바꿔야 하므로 이 명령을 실행하지 않는 것이 좋습니다.

> {note} 배포 과정에서 `config:cache` 명령을 실행할 경우, `env` 함수를 오직 설정 파일 내에서만 사용했는지 반드시 확인해야 합니다. 설정이 캐싱되면 `.env` 파일은 더 이상 불러오지 않으므로, `env` 함수는 외부 시스템 환경 변수만 반환합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생시 사용자에게 얼마나 많은 정보를 노출할지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 시에는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 프로덕션에서 `true`로 설정되어 있다면, 민감한 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

점검 모드에서는 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 업데이트나 유지보수 작업 동안 애플리케이션을 간편하게 “비활성화”할 수 있습니다. 기본 미들웨어 스택에 이러한 점검 모드 체크가 포함되어 있습니다. 점검 모드일 때는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태 코드와 함께 발생합니다.

점검 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

    php artisan down

점검 모드 응답과 함께 `Refresh` HTTP 헤더를 보내고 싶다면, `down` 명령어 실행 시 `refresh` 옵션을 추가할 수 있습니다. `Refresh` 헤더는 브라우저가 지정한 초 이후 자동으로 페이지를 새로고침하게 만듭니다:

    php artisan down --refresh=15

또한, `down` 명령에 `retry` 옵션을 제공하면 이 값이 `Retry-After` HTTP 헤더에 설정됩니다. (대부분의 브라우저는 이 헤더를 무시함에 유의):

    php artisan down --retry=60

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

점검 모드 상태에서도, `secret` 옵션을 사용하여 점검 모드를 우회할 수 있는 토큰을 지정할 수 있습니다:

    php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"

애플리케이션을 점검 모드로 전환한 후, 이 토큰이 포함된 애플리케이션 URL로 접속하면 Laravel이 브라우저에 점검 모드 우회 쿠키를 발급합니다:

    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

이 숨겨진 경로로 접근하면 `/` 경로로 리디렉션됩니다. 쿠키가 발급된 후에는 점검 모드가 아닌 것처럼 애플리케이션을 정상적으로 이용할 수 있습니다.

> {tip} 점검 모드 시크릿은 일반적으로 영문자, 숫자, 선택적으로 대시(-) 문자로 구성하는 것이 좋습니다. `?` 또는 `&`와 같이 URL에서 특별한 의미를 지니는 문자는 피하세요.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 미리 렌더링하기

배포 시 `php artisan down` 명령을 사용한다면, 사용자가 Composer 의존성이나 인프라 컴포넌트를 업데이트하는 동안 애플리케이션에 접근하면 오류가 발생할 수 있습니다. 이는 Laravel 프레임워크의 상당 부분이 부팅되어야 점검 모드인지 확인하고 템플릿 엔진을 통해 유지보수 뷰를 렌더링하기 때문입니다.

이러한 이유로, Laravel에서는 요청 처리 주기의 맨 앞에서 반환할 점검 모드 뷰를 미리 렌더링할 수 있습니다. 이 뷰는 애플리케이션의 의존성이 로드되기 이전에 렌더링됩니다. `down` 명령의 `render` 옵션을 사용해 원하는 템플릿을 미리 렌더링할 수 있습니다:

    php artisan down --render="errors::503"

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리디렉션

점검 모드에서 사용자가 어떤 경로에 접근하든 유지보수 뷰가 표시됩니다. 모든 요청을 특정 URL로 리디렉션하고 싶으면, `redirect` 옵션을 사용할 수 있습니다. 예를 들어 모든 요청을 `/` URI로 리디렉션 하려면:

    php artisan down --redirect=/

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 비활성화

점검 모드를 비활성화하려면 `up` 명령을 사용합니다:

    php artisan up

> {tip} 기본 점검 모드 템플릿을 커스터마이징하려면 `resources/views/errors/503.blade.php`에 직접 템플릿을 정의하면 됩니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드 & 큐

애플리케이션이 점검 모드에서는 [큐에 등록된 작업](/docs/{{version}}/queues)이 처리되지 않습니다. 점검 모드가 종료되면 작업 처리가 정상적으로 재개됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드는 수 초간의 다운타임이 필요하므로, [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io)와 같은 무중단 배포(deployment) 도구를 활용하는 것도 고려해보세요.