# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션은 주석으로 문서화되어 있으니, 파일들을 살펴보고 사용 가능한 옵션들에 익숙해지길 권장합니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 타임존, 암호화 키 같은 다양한 핵심 설정 값을 구성하는 데 사용됩니다.

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 로컬 개발 환경에서는 한 가지 캐시 드라이버를 사용하고, 실제 운영 서버에서는 다른 드라이버를 사용하고자 할 수 있습니다.

이를 쉽게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 이용합니다. Laravel을 새로 설치하면 애플리케이션 루트 디렉터리에 `.env.example` 파일이 있으며, 이 파일에는 일반적인 환경 변수들이 정의되어 있습니다. 설치 과정 중 이 파일은 자동으로 `.env` 파일로 복사됩니다.

Laravel 기본 `.env` 파일에는 운영 환경과 로컬 환경에서 다를 수 있는 공통 설정 값들이 들어 있습니다. 이 값들은 Laravel의 `env` 함수를 써서 `config` 디렉터리 내 다양한 설정 파일에서 읽어옵니다.

팀 단위로 개발한다면 `.env.example` 파일을 계속 포함하는 것이 좋습니다. 이렇게 하면 예제 설정 파일에 플레이스홀더 값들이 있어 팀 내 다른 개발자들이 어떤 환경 변수가 필요한지 명확히 알 수 있습니다.

> [!TIP]
> `.env` 파일 내 어떤 변수든 서버 레벨이나 시스템 레벨 환경 변수 같은 외부 환경 변수에 의해 덮어쓰여질 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 애플리케이션마다, 서버마다 서로 다른 환경 구성이 필요하므로 소스 컨트롤에 커밋하지 않는 것이 좋습니다. 또한, 소스 컨트롤 리포지토리에 침입자가 접근했을 때 민감한 인증 정보가 노출되는 위험을 방지할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 불러오기 전에 Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었거나 CLI 인자로 `--env`가 지정되었는지 확인합니다. 만약 존재하면 `.env.[APP_ENV]` 파일이 있으면 이를 로드하려 시도합니다. 없으면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일 내 모든 변수는 기본적으로 문자열로 파싱됩니다. 하지만 `env()` 함수에서 더 다양한 타입을 지원하기 위해 예약된 값들이 있습니다:

`.env` 값   | `env()` 함수 반환 값
-----------|--------------------
true | (bool) true
(true) | (bool) true
false | (bool) false
(false) | (bool) false
empty | (string) ''
(empty) | (string) ''
null | (null) null
(null) | (null) null

값에 공백이 포함되어야 한다면, 큰 따옴표로 감싸서 정의할 수 있습니다:

```
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

이 파일에 나열된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌로 로드됩니다. 그러나 설정 파일에서는 `env` 헬퍼 함수를 통해 값을 가져올 수 있습니다. 실제로 Laravel 설정 파일에서도 많은 옵션에 이 헬퍼가 쓰이고 있음을 볼 수 있습니다:

```
'debug' => env('APP_DEBUG', false),
```

`env` 함수에 두 번째로 전달된 값은 "기본값"으로, 해당 키에 환경 변수가 없을 때 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 정해집니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드로 접근할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한 `environment` 메서드에 인수를 전달해, 현재 환경이 특정 값과 일치하는지 판단할 수 있습니다. 하나라도 일치하면 `true`를 반환합니다:

```
if (App::environment('local')) {
    // 현재 환경이 local 일 때
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 또는 staging 중 하나일 때
}
```

> [!TIP]
> 현재 애플리케이션 환경은 서버 레벨에서 정의된 `APP_ENV` 환경 변수를 갖고 덮어쓸 수 있습니다.

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기

애플리케이션 어디서든 전역 헬퍼 함수인 `config`를 통해 설정 값에 쉽게 접근할 수 있습니다. 설정 값은 점(dot) 구문을 사용하며, 파일 이름과 옵션 이름을 포함합니다. 기본값도 지정할 수 있으며, 설정 값이 없을 때 반환됩니다:

```
$value = config('app.timezone');

// 설정 값이 없을 경우 기본값 반환
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중 설정 값을 변경하고 싶으면, 배열을 `config` 헬퍼에 전달하면 됩니다:

```
config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션 속도 향상을 위해 모든 설정 파일을 하나의 파일로 캐시하는 것이 좋습니다. `config:cache` Artisan 명령어를 사용하면 설정 옵션을 한 파일로 합쳐 프레임워크가 빠르게 로드할 수 있습니다.

보통 이 명령어는 프로덕션 배포 과정에서 실행해야 하며, 로컬 개발 환경에서는 자주 변경되는 설정으로 인해 실행하지 않는 것이 좋습니다.

> [!NOTE]
> 배포 시 `config:cache`를 실행했다면, 설정 파일 내에서 `env` 함수를 호출할 때 오직 외부 시스템 환경 변수만 참조해야 합니다. `.env` 파일은 캐시 후에는 로드되지 않기 때문입니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일 내 `debug` 옵션은 오류 발생 시 사용자에게 얼마나 많은 정보를 보여줄지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 설정된 `APP_DEBUG` 환경 변수를 따라갑니다.

로컬 개발 환경에서는 `APP_DEBUG`를 `true`로 설정하는 것이 좋지만, **운영 환경에서는 반드시 `false`로 설정해야 합니다.** 만약 운영 환경에서 `true`로 설정하면 민감한 설정 값이 사용자에게 노출될 위험이 있습니다.

<a name="maintenance-mode"></a>
## 유지보수 모드

애플리케이션이 유지보수 모드일 때는 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 업데이트나 유지보수 작업 시 애플리케이션을 쉽게 "비활성화"할 수 있습니다. 유지보수 모드 체크는 기본 미들웨어 스택에 포함되어 있습니다. 유지보수 모드일 경우, HTTP 상태 코드 503인 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 다음 Artisan 명령어를 실행하세요:

```
php artisan down
```

`down` 명령 실행 시 `refresh` 옵션을 지정하면, 모든 유지보수 모드 응답에 `Refresh` HTTP 헤더가 포함되어 브라우저가 자동으로 지정한 초 뒤에 페이지를 새로고침하게 할 수 있습니다:

```
php artisan down --refresh=15
```

또한 `retry` 옵션으로 `Retry-After` HTTP 헤더 값을 지정할 수 있으나, 대부분의 브라우저는 이 헤더를 무시합니다:

```
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회하기

유지보수 모드 중이라도 `secret` 옵션으로 우회 토큰을 지정할 수 있습니다:

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드가 활성화된 후, 해당 토큰을 URL 경로로 접근하면 Laravel이 우회 쿠키를 브라우저에 발급합니다:

```
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

해당 숨겨진 경로에 접속하면 `/` 경로로 리다이렉트되며, 쿠키가 발급된 후에는 유지보수 모드가 아닌 것처럼 정상적으로 애플리케이션을 이용할 수 있습니다.

> [!TIP]
> 유지보수 모드 비밀 키는 보통 영숫자와 대시(-)를 사용하며, URL에서 특별한 의미를 가지는 `?`나 `&` 등 문자는 피하는 것이 좋습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링

`php artisan down` 명령을 배포 중 사용하면, Composer 종속성이나 다른 인프라가 업데이트되는 동안 사용자들이 잠깐씩 오류를 경험할 수도 있습니다. 이는 유지보수 모드임을 판단하고 뷰를 렌더링하기 위해 Laravel 프레임워크가 부팅되어야 하기 때문입니다.

이 문제를 줄이기 위해 사전 렌더링된 유지보수 모드 뷰를 요청 사이클 초기에 바로 반환할 수 있습니다. `down` 명령어의 `render` 옵션을 사용해 원하는 뷰 템플릿을 미리 렌더링하세요:

```
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리다이렉트

유지보수 모드에서는 사용자 요청에 대해 기본 유지보수 모드 뷰가 보여집니다. 원한다면 모든 요청을 특정 URL로 리다이렉트하도록 지정할 수도 있습니다. `redirect` 옵션을 사용해서 예를 들어 모든 요청을 `/` URI로 리다이렉트할 수 있습니다:

```
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 종료하기

유지보수 모드를 비활성화하려면 `up` 명령어를 사용하세요:

```
php artisan up
```

> [!TIP]
> 기본 유지보수 모드 템플릿을 커스터마이징하려면 `resources/views/errors/503.blade.php` 파일을 수정하세요.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐 작업

유지보수 모드에서는 [큐 작업](/docs/{{version}}/queues)이 처리되지 않습니다. 유지보수 모드 종료 후에는 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션 다운타임이 필요하므로, 무중단 배포가 가능한 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io) 같은 다른 방법도 고려해보세요.