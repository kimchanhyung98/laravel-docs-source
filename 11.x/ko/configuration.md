# 설정

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 제공되어 있으므로, 해당 파일들을 살펴보고 사용할 수 있는 옵션들에 익숙해지시기 바랍니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 URL, 암호화 키 등 다양한 핵심 설정 값을 구성할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 등의 개요를 보여줍니다.

```shell
php artisan about
```

애플리케이션 개요 출력에서 특정 섹션만 확인하고 싶다면 `--only` 옵션으로 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 탐색하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 서로 다른 설정값을 사용하는 것이 도움이 될 때가 많습니다. 예를 들어, 로컬 환경과 프로덕션 서버에서 서로 다른 캐시 드라이버를 쓸 수 있습니다.

이를 간편하게 할 수 있도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새 Laravel 설치 시, 애플리케이션 루트 디렉터리에는 여러 일반적인 환경 변수를 정의하는 `.env.example` 파일이 포함되어 있습니다. Laravel 설치 과정 중에 이 파일이 `.env`로 자동 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬 환경과 프로덕션 웹 서버에서 다를 수 있는 일반적인 설정 값들이 포함되어 있습니다. 이 값들은 설정 파일에서 Laravel의 `env` 함수를 통해 읽힙니다.

팀과 함께 개발 중이라면, `.env.example` 파일을 계속 포함시키고 업데이트하는 것이 좋습니다. 예시 설정 파일에 기본값을 기입해 두면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수를 명확히 확인할 수 있습니다.

> [!NOTE]  
> `.env` 파일 내의 변수는 서버 레벨이나 시스템 환경 변수 등 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 애플리케이션 소스 컨트롤에 커밋하지 않아야 합니다. 각 개발자/서버마다 서로 다른 환경 구성이 필요할 수 있기 때문입니다. 또한 공격자가 소스 저장소에 접근할 경우, 민감한 인증 정보가 노출될 수 있으므로 보안에 취약합니다.

하지만, Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 통해 환경 파일을 암호화한 뒤 소스 컨트롤에 안전하게 저장할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션 환경 변수를 로드하기 전에, Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지 또는 `--env` CLI 인자가 지정되었는지 확인합니다. 해당되는 경우, Laravel은 `.env.[APP_ENV]` 파일이 존재하면 이를 로드합니다. 존재하지 않을 경우 기본 `.env` 파일을 사용합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 일반적으로 문자열로 해석되지만, `env()` 함수로 더 다양한 타입을 반환할 수 있도록 예약된 값들이 있습니다:

<div class="overflow-auto">

| `.env` 값   | `env()` 반환값     |
| ----------- | ----------------- |
| true        | (bool) true       |
| (true)      | (bool) true       |
| false       | (bool) false      |
| (false)     | (bool) false      |
| empty       | (string) ''       |
| (empty)     | (string) ''       |
| null        | (null) null       |
| (null)      | (null) null       |

</div>

값에 공백이 포함되는 환경 변수를 정의하려면 큰따옴표로 감싸서 사용할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정값 가져오기

`.env` 파일에 있는 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼 글로벌에 로드됩니다. 설정 파일에서는 `env` 함수를 사용해 이러한 변수 값을 가져올 수 있습니다. 실제로 Laravel의 설정 파일을 들여다보면 많은 옵션에서 이 함수를 사용하는 것을 볼 수 있습니다:

    'debug' => env('APP_DEBUG', false),

`env` 함수에 두 번째 인자로 전달된 값은 "기본값"입니다. 주어진 키에 해당하는 환경 변수가 없다면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드를 통해 접근할 수 있습니다.

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

`environment` 메서드에 인자를 전달하여 환경이 특정 값과 일치하는지 확인할 수 있습니다. 환경이 주어진 값들 중 하나와 일치하면 `true`를 반환합니다.

    if (App::environment('local')) {
        // 환경이 local입니다.
    }

    if (App::environment(['local', 'staging'])) {
        // 환경이 local 또는 staging입니다.
    }

> [!NOTE]  
> 현재 애플리케이션 환경 감지는 서버 레벨에서 `APP_ENV` 환경 변수를 정의함으로써 오버라이드할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일을 소스 컨트롤에 보관해서는 안 됩니다. 그러나, Laravel을 이용해 환경 파일을 암호화하여 애플리케이션의 다른 파일들과 마찬가지로 안전하게 소스 컨트롤에 추가할 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하면 됩니다:

```shell
php artisan env:encrypt
```

`env:encrypt` 명령어를 실행하면 `.env` 파일을 암호화하여 `.env.encrypted` 파일에 저장합니다. 복호화 키가 명령어 출력에 표시되며, 이 키는 반드시 안전한 비밀번호 관리자에 저장하시기 바랍니다. 직접 암호화 키를 지정하고 싶다면, 명령어 실행 시 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]  
> 제공하는 키 길이는 사용 중인 암호화 알고리즘에 요구되는 길이와 맞아야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 암호화 방식을 사용합니다. 명령어에 `--cipher` 옵션을 전달해 Laravel의 [암호화기](/docs/{{version}}/encryption)가 지원하는 임의의 암호 알고리즘을 사용할 수 있습니다.

애플리케이션에 여러 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션으로 암호화할 환경 파일명을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 찾습니다:

```shell
php artisan env:decrypt
```

또는, `--key` 옵션을 통해 키를 직접 전달할 수 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면, Laravel은 `.env.encrypted` 파일을 복호화하여 `.env` 파일에 결과를 저장합니다.

`env:decrypt` 명령어에 `--cipher` 옵션을 주어 사용자 정의 암호화 알고리즘을 사용할 수도 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일이 있을 경우, `--env` 옵션으로 복호화할 환경 파일명을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가합니다:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기

애플리케이션 어디에서든 `Config` 파사드나 전역 `config` 함수를 이용해 손쉽게 설정 값을 가져올 수 있습니다. 설정 값은 점(`.`) 표기법(파일명.옵션명)으로 접근할 수 있으며, 존재하지 않을 경우 반환할 기본값을 지정할 수도 있습니다:

    use Illuminate\Support\Facades\Config;

    $value = Config::get('app.timezone');

    $value = config('app.timezone');

    // 설정 값이 없으면 기본값을 가져옴
    $value = config('app.timezone', 'Asia/Seoul');

런타임에 설정 값을 변경하려면 `Config` 파사드의 `set` 메서드나 배열을 `config` 함수에 전달할 수 있습니다:

    Config::set('app.timezone', 'America/Chicago');

    config(['app.timezone' => 'America/Chicago']);

정적 분석을 돕기 위해, `Config` 파사드는 타입 안전한 설정 가져오기 메서드도 제공합니다. 반환값이 기대하는 타입과 일치하지 않으면 예외가 발생합니다:

    Config::string('config-key');
    Config::integer('config-key');
    Config::float('config-key');
    Config::boolean('config-key');
    Config::array('config-key');

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션 성능을 높이기 위해 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` Artisan 명령어를 사용하세요. 이 명령어는 애플리케이션의 모든 설정 옵션을 하나의 파일에 통합하여 프레임워크가 빠르게 로드할 수 있도록 합니다.

보통 프로덕션 배포 과정의 일부로 `php artisan config:cache` 명령어를 실행해야 합니다. 로컬 개발 중에는 애플리케이션 설정을 자주 변경하므로 이 명령어를 실행하지 않는 것이 좋습니다.

설정이 캐시되면, 애플리케이션의 `.env` 파일은 요청이나 Artisan 명령어 실행 시 프레임워크에 의해 로드되지 않습니다. 따라서, `env` 함수는 외부(시스템 레벨) 환경 변수만 반환합니다.

이러한 이유로, 애플리케이션의 설정(`config`) 파일 내에서만 `env` 함수를 호출해야 합니다. 기본 설정 파일을 참고하면 많은 예제를 확인할 수 있습니다. 설정 값은 위에서 설명한 `config` 함수를 통해 어디서나 접근할 수 있습니다.

`config:clear` 명령어를 사용하면 캐시된 설정을 삭제할 수 있습니다:

```shell
php artisan config:clear
```

> [!WARNING]  
> 배포 과정에서 `config:cache` 명령어를 실행할 경우, 오직 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 한 번 설정이 캐시되면 `.env` 파일은 로드되지 않으므로, `env` 함수는 외부 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 퍼블리싱

대부분의 Laravel 설정 파일은 애플리케이션의 `config` 디렉터리에 이미 퍼블리시되어 있습니다. 하지만, `cors.php`나 `view.php` 등 일부 설정 파일은 기본적으로 퍼블리시되지 않습니다(대부분의 애플리케이션이 수정할 필요가 없기 때문입니다).

필요하다면, `config:publish` Artisan 명령어를 사용해 기본적으로 퍼블리싱 되지 않은 설정 파일을 퍼블리싱할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 오류 발생 시 사용자에게 얼마나 많은 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 `false`로 설정해야 하며, 만약 프로덕션에 `true`로 되어 있다면, 애플리케이션의 민감한 설정 값이 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

애플리케이션이 점검(유지보수) 모드일 때는, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 업데이트나 유지보수 중 애플리케이션을 쉽게 "비활성화"할 수 있습니다. 점검 모드 확인 로직은 기본 미들웨어 스택에 포함되어 있습니다. 애플리케이션이 점검 모드이면, `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태코드와 함께 발생합니다.

점검 모드를 활성화하려면 `down` Artisan 명령어를 사용하세요:

```shell
php artisan down
```

모든 점검 모드 응답에 `Refresh` HTTP 헤더를 포함하려면, `down` 명령어 실행 시 `refresh` 옵션을 사용할 수 있습니다. 이 헤더는 지정된 초 이후 브라우저가 자동으로 페이지를 새로고침 하도록 지시합니다:

```shell
php artisan down --refresh=15
```

`down` 명령어에 `retry` 옵션을 추가하면, 해당 값이 `Retry-After` HTTP 헤더값으로 설정됩니다(주로 브라우저에서는 무시됨):

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

비밀 토큰을 통해 점검 모드를 우회하게 하고 싶다면, `secret` 옵션으로 점검 모드 우회 토큰을 지정할 수 있습니다:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션이 점검 모드에 들어간 후 토큰과 일치하는 URL로 접속하면, Laravel은 브라우저에 점검 모드 우회 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 토큰을 자동으로 생성하게 하려면 `with-secret` 옵션을 사용할 수 있습니다. 애플리케이션이 점검 모드에 들어가면 토큰이 표시됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로에 접근하면 애플리케이션의 `/` 경로로 리디렉션됩니다. 브라우저에 쿠키가 발급되면, 점검 모드가 아닌 상태처럼 애플리케이션을 정상적으로 이용할 수 있습니다.

> [!NOTE]  
> 점검 모드 비밀 토큰은 영숫자와(선택적으로) 대시로 구성하는 것이 일반적입니다. URL에서 특별한 의미를 갖는 문자(`?`, `&` 등)는 피하세요.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 복수 서버에서의 점검 모드

기본적으로 Laravel은 파일 기반 방식으로 점검 모드 상태를 관리합니다. 따라서 여러 서버에서 서비스 중이라면 각 서버에서 `php artisan down` 명령어를 실행해야 점검 모드가 활성화됩니다.

대신, Laravel은 캐시 기반 점검 모드 처리 방법도 제공합니다. 이 방법은 한 서버에서만 `php artisan down` 명령어를 실행하면 됩니다. 이를 위해, `.env` 파일의 점검 모드 관련 변수를 수정합니다. 모든 서버가 접근할 수 있는 캐시 `store`를 선택해야 점검 모드 상태가 여러 서버에 일관되게 적용됩니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 미리 렌더링

배포 과정 중 `php artisan down` 명령어를 사용할 경우, Composer 의존성이나 기타 인프라가 갱신되는 동안 사용자가 애플리케이션에 접근하면 간혹 오류 페이지를 만날 수 있습니다. 이는 점검 모드 여부와 뷰 렌더링을 판단하기 위해 Laravel 프레임워크의 많은 부분이 부팅되어야 하기 때문입니다.

이런 문제를 예방하기 위해, Laravel은 요청 처리 초기에 바로 반환할 수 있도록 점검 모드 뷰를 미리 렌더링할 수 있게 지원합니다. 이 뷰는 애플리케이션 의존성이 로드되기 전 렌더링됩니다. `down` 명령어의 `render` 옵션을 이용해 원하는 템플릿을 미리 렌더링할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리디렉션

점검 모드에서는, 사용자가 접근하는 모든 URL에 대해 점검 모드 뷰가 표시됩니다. 필요하다면, 모든 요청을 특정 URL로 리디렉트하도록 Laravel에 지시할 수 있습니다. 예를 들어 모든 요청을 `/`로 리디렉션하려면:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 비활성화

점검 모드를 해제하려면 `up` 명령어를 사용하세요:

```shell
php artisan up
```

> [!NOTE]  
> 기본 점검 모드 템플릿을 커스터마이징하고 싶다면, `resources/views/errors/503.blade.php` 경로에 직접 템플릿을 정의하면 됩니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐

애플리케이션이 점검 모드일 때는 [큐 작업](/docs/{{version}}/queues)이 처리되지 않습니다. 점검 모드가 해제되면 정상적으로 작업이 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드는 애플리케이션이 최장 수 초간 다운타임을 갖게 됩니다. 만약 무중단 배포를 원한다면 [Laravel Vapor](https://vapor.laravel.com) 나 [Envoyer](https://envoyer.io) 같은 도구로 대체할 수 있습니다.