# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 게시](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에 주석으로 설명이 되어 있으니, 파일을 살펴보며 사용 가능한 설정 옵션에 익숙해지시기 바랍니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션 URL, 암호화 키와 같은 다양한 핵심 설정 값을 구성할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 정보 개요를 보여줄 수 있습니다.

```shell
php artisan about
```

특정 부분의 정보만 보고 싶다면, `--only` 옵션으로 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는 특정 설정 파일의 값을 자세히 확인하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 설정 값이 다르게 적용되는 것이 유용할 때가 많습니다. 예를 들어, 로컬에서는 다른 캐시 드라이버를 사용하고 프로덕션 서버에서는 또 다른 드라이버를 사용하는 것처럼 말입니다.

Laravel은 이를 쉽게 하기 위해 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 신규 Laravel 설치 시 애플리케이션 루트 디렉토리에 `.env.example` 파일이 존재하는데, 이 파일에는 일반적으로 필요한 환경 변수들이 정의되어 있습니다. 설치 과정에서 이 파일은 자동으로 `.env` 파일로 복사됩니다.

Laravel의 기본 `.env` 파일은 로컬과 프로덕션 웹 서버 등 환경에 따라 달라질 수 있는 공통 설정 값을 포함합니다. 이 값들은 `config` 디렉토리 내의 설정 파일들이 Laravel의 `env` 함수를 통해 읽습니다.

협업하는 경우, `.env.example` 파일을 계속 관리하며 업데이트하는 것이 좋습니다. 예시 설정 파일에 플레이스홀더 값을 넣으면 팀의 다른 개발자들이 어떤 환경 변수가 필요한지 명확히 알 수 있습니다.

> [!NOTE]
> `.env` 파일의 모든 변수는 서버 레벨 또는 시스템 레벨 환경 변수 같은 외부 환경 변수에 의해 덮어쓰여질 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버마다 환경 설정이 다를 수 있으므로 소스 관리에 커밋하면 안 됩니다. 또한 공격자가 소스 리포지토리를 탈취했을 때 중요한 자격 증명이 노출될 위험이 있습니다.

하지만 Laravel 내장 환경 파일 암호화 기능([환경 파일 암호화](#encrypting-environment-files))을 사용하면 환경 파일을 암호화하여 소스 관리에 안전하게 포함할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션 환경 변수를 로드하기 전에 Laravel은 외부에서 제공된 `APP_ENV` 환경 변수 또는 `--env` CLI 인자가 있는지 확인합니다. 있으면 `.env.[APP_ENV]` 파일을 로드하려 시도하며, 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입 (Environment Variable Types)

`.env` 파일의 모든 변수는 기본적으로 문자열로 파싱되기 때문에 `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 예약된 값을 제공합니다:

<div class="overflow-auto">

| `.env` 값    | `env()` 반환 값  |
| ------------ | ---------------- |
| true         | (bool) true      |
| (true)       | (bool) true      |
| false        | (bool) false     |
| (false)      | (bool) false     |
| empty        | (string) ''      |
| (empty)      | (string) ''      |
| null         | (null) null      |
| (null)       | (null) null      |

</div>

공백이 포함된 문자열 값을 정의하려면 큰따옴표로 감싸서 작성할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기 (Retrieving Environment Configuration)

`.env` 파일에 있는 모든 변수는 요청 시 `$_ENV` PHP 슈퍼 글로벌에 로드됩니다. 하지만 설정 파일에서 이 변수들을 읽기 위해 `env` 함수를 사용합니다. Laravel 기본 설정 파일을 보면 많은 옵션 값이 이미 이 함수를 사용하고 있음을 확인할 수 있습니다:

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인수는 기본값으로, 해당 키가 존재하지 않으면 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기 (Determining the Current Environment)

애플리케이션 현재 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. `App` [파사드](/docs/12.x/facades)의 `environment` 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

`environment` 메서드에 인수를 전달해 환경이 특정 값과 일치하는지 확인할 수 있습니다. 인자가 배열이면, 환경이 해당 배열 중 하나와 일치할 경우 `true`를 반환합니다:

```php
if (App::environment('local')) {
    // 환경이 local인 경우
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 또는 staging인 경우
}
```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 레벨에서 정의된 `APP_ENV` 환경 변수에 의해 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화 (Encrypting Environment Files)

평문 환경 파일은 절대 소스 관리에 포함되어서는 안 됩니다. Laravel은 환경 파일을 암호화하여 애플리케이션과 함께 안전하게 소스 관리에 포함할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화

환경 파일 암호화는 `env:encrypt` 명령어를 사용합니다:

```shell
php artisan env:encrypt
```

이 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화 키는 명령어 실행 결과로 출력되며, 안전한 비밀번호 관리 도구에 보관해야 합니다. 직접 키를 제공하려면 `--key` 옵션을 사용합니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키 길이는 암호화에 사용하는 암호 방식에 맞춰져야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 암호화를 사용합니다. `--cipher` 옵션을 써서 원하는 암호 방식을 지정할 수도 있습니다. ([encrypter](/docs/12.x/encryption) 참고)

여러 환경 파일(`.env`, `.env.staging` 등)이 있다면 `--env` 옵션으로 암호화할 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일 복호화는 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키를 필요로 하며, 기본적으로 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수를 통해 가져옵니다:

```shell
php artisan env:decrypt
```

키를 직접 제공하려면 `--key` 옵션을 사용합니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

명령어 실행 시 `.env.encrypted` 파일을 복호화하여 `.env` 파일에 저장합니다.

커스텀 암호화를 사용하려면 `--cipher` 옵션도 제공할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

복수 환경 파일에도 마찬가지로 `--env` 옵션을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가하세요:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기 (Accessing Configuration Values)

애플리케이션 어디서나 `Config` 파사드 또는 전역 `config` 함수를 이용해 설정 값을 쉽게 가져올 수 있습니다. 설정 값은 파일명과 옵션명을 점(.) 구문으로 접근합니다. 설정 값이 없으면 기본값을 지정해서 받을 수도 있습니다:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없으면 기본값 사용...
$value = config('app.timezone', 'Asia/Seoul');
```

런타임 중 설정 값을 변경하려면 `Config` 파사드의 `set` 메서드를 호출하거나 `config` 함수에 배열로 전달할 수 있습니다:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석을 돕기 위해, `Config` 파사드는 타입별 설정 조회 메서드도 제공합니다. 반환 값이 예상 타입과 다르면 예외가 발생합니다:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

애플리케이션 속도 향상을 위해 `config:cache` Artisan 명령어를 사용하여 모든 설정 파일을 하나의 파일로 캐시할 수 있습니다. 이 명령은 모든 설정 옵션을 하나로 합쳐 빠르게 로드할 수 있게 합니다.

보통 `php artisan config:cache` 명령어는 프로덕션 배포 과정에서 실행합니다. 로컬 개발 중에는 자주 설정 변경이 필요하기 때문에 캐싱하지 않는 것이 좋습니다.

캐싱 후에는 프레임워크가 `.env` 파일을 요청이나 Artisan 명령어 실행 시 로드하지 않으므로, `env` 함수는 외부 시스템 환경 변수만 반환합니다.

따라서 `env` 함수 호출은 반드시 애플리케이션 설정 파일(`config` 디렉토리) 내에서만 이루어져야 합니다. Laravel 기본 설정 파일에서 이 부분을 확인할 수 있으며, 설정 값은 애플리케이션 어디서나 `config` 함수를 통해 접근할 수 있습니다.

캐시된 설정을 삭제하려면 `config:clear` 명령어를 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 시 `config:cache` 명령어를 실행한다면, `env` 함수 호출이 반드시 설정 파일 내에서만 이뤄지도록 주의해야 합니다. 캐시된 설정이 로드되는 동안 `.env` 파일은 무시되며, `env` 함수는 외부 시스템 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 게시 (Configuration Publishing)

대부분의 Laravel 설정 파일은 이미 애플리케이션의 `config` 디렉토리에 게시되어 있습니다. 하지만 `cors.php`, `view.php` 같은 일부 설정 파일은 기본적으로 게시되지 않는데, 대부분 애플리케이션에서는 수정할 필요가 없기 때문입니다.

필요하다면 `config:publish` Artisan 명령어로 게시되지 않은 설정 파일을 게시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 `debug` 옵션은 오류 발생 시 사용자에게 노출할 정보의 양을 결정합니다. 기본값은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수를 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정하세요. **프로덕션 환경에서는 항상 `false`로 설정해야 하며, `true`로 설정하면 애플리케이션 사용자에게 민감한 설정 값이 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지보수 모드 (Maintenance Mode)

애플리케이션이 유지보수 모드에 들어가면 모든 요청에 대해 사용자 지정 뷰가 표시됩니다. 이를 통해 업데이트 중이거나 점검 시 애플리케이션을 "사용 중지" 상태로 간편히 전환할 수 있습니다. 유지보수 모드 검사 미들웨어가 기본 미들웨어 스택에 포함되어 있습니다. 유지보수 모드이면 HTTP 상태 코드 503과 함께 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행합니다:

```shell
php artisan down
```

`down` 명령어에 `refresh` 옵션을 제공하면 모든 유지보수 모드 응답에 `Refresh` HTTP 헤더가 포함되어, 지정한 초 수 후에 브라우저가 자동으로 페이지를 새로고침합니다:

```shell
php artisan down --refresh=15
```

`retry` 옵션도 지정할 수 있으며, 이는 `Retry-After` HTTP 헤더로 설정됩니다. 다만 대부분 브라우저는 이 헤더를 무시합니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회하기

비밀 토큰을 통해 유지보수 모드를 우회하려면 `secret` 옵션을 써서 토큰을 지정하세요:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 진입 후, 비밀 토큰이 포함된 URL로 접속하면 Laravel이 우회 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 자동 생성하게 하려면 `with-secret` 옵션을 사용하세요. 유지보수 모드 활성화 시 생성된 비밀 토큰이 출력됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로에 접속하면 애플리케이션의 `/` 경로로 리다이렉트되며, 쿠키가 발급되면 유지보수 모드가 아닌 것처럼 정상적으로 애플리케이션을 사용할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰은 일반적으로 영문, 숫자 및 대시(-) 문자로 구성하며, URL 특수문자(`?`, `&` 등)는 피하는 것이 좋습니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 복수 서버 환경에서 유지보수 모드

기본적으로 Laravel은 파일 기반으로 유지보수 모드 여부를 확인합니다. 즉, 애플리케이션이 여러 서버에 배포되어 있으면 각 서버에서 `php artisan down` 명령어를 개별 실행해야 합니다.

대안으로, 캐시 기반 유지보수 모드 방식을 제공하며 이 경우 한 서버에서만 `php artisan down`을 실행하면 됩니다. 이를 사용하려면 애플리케이션 `.env` 파일에서 유지보수 모드 설정을 다음과 같이 수정하세요. 모든 서버가 접근할 수 있는 캐시 스토어를 지정해야 상태가 일관되게 유지됩니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링

배포 시 `php artisan down` 명령어를 사용할 때, 사용자들이 Composer 의존성 업데이트 등으로 인해 가끔 오류를 경험할 수도 있습니다. 이는 Laravel 프레임워크 일부가 부팅되어야 유지보수 모드임을 판단하고 템플릿 엔진으로 뷰를 렌더링하기 때문입니다.

이를 해결하려 Laravel은 요청 사이클 초기에 반환할 유지보수 모드를 미리 렌더링할 수 있는 기능을 제공합니다. 애플리케이션 종속성이 로딩되기 전에 렌더링된 뷰가 반환됩니다. 원하는 템플릿을 지정해서 사전 렌더링하려면 `down` 명령어의 `render` 옵션을 사용하세요:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리다이렉트

유지보수 모드 동안 Laravel은 모든 URL에 대해 유지보수 모드 뷰를 보여줍니다. 필요하면 모든 요청을 특정 URL로 리다이렉트하도록 지시할 수 있습니다. `redirect` 옵션을 사용해 예를 들어 모든 요청을 루트 URI로 리다이렉트할 수 있습니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제

유지보수 모드를 해제하려면 `up` 명령어를 실행하세요:

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php` 경로에 사용자 정의 템플릿을 만들어 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 유지보수 모드일 때는 [큐 작업](/docs/12.x/queues)이 처리되지 않습니다. 유지보수 모드가 해제된 후에는 정상적으로 큐 작업이 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션에 몇 초간의 다운타임이 발생합니다. 무중단 배포를 위해서는 [Laravel Cloud](https://cloud.laravel.com) 같은 완전관리형 플랫폼에서 애플리케이션을 운영하는 것을 고려해보세요.