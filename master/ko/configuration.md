# 설정

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정값 조회](#retrieving-environment-configuration)
    - [현재 환경 확인](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정값 접근](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 파일 게시](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장됩니다. 각 옵션에 대한 문서가 포함되어 있으니, 파일을 둘러보고 사용 가능한 옵션을 익혀보시길 권장합니다.

이 설정 파일들을 이용해 데이터베이스 연결 정보, 메일 서버 정보, 어플리케이션 URL, 암호화 키 등 다양한 핵심 설정 값을 구성할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 개요를 보여줄 수 있습니다.

```shell
php artisan about
```

애플리케이션 개요에서 특정 섹션만 보고 싶다면 `--only` 옵션을 사용해 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또한, 특정 설정 파일의 값을 자세히 탐색하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 로컬에서는 운영 서버와 다른 캐시 드라이버를 쓰고 싶을 수 있습니다.

이를 간편하게 처리하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로운 Laravel 설치에서는 애플리케이션 루트 디렉토리에 여러 일반적인 환경 변수를 정의한 `.env.example` 파일이 포함되어 있습니다. Laravel 설치 과정에서 이 파일이 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬에서 실행되는지, 운영 서버에서 실행되는지에 따라 다를 수 있는 일반적인 환경 값들이 포함되어 있습니다. 이 값들은 설정 파일(`config` 디렉토리 내)에 Laravel의 `env` 함수를 통해 읽혀집니다.

여러 개발자가 함께 작업할 경우 `.env.example` 파일의 포맷을 유지·업데이트하는 것이 좋습니다. 예시 파일에 플레이스홀더 값을 넣어두면 팀 내 다른 개발자들은 애플리케이션 실행에 필요한 환경 변수를 명확하게 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일의 어떤 변수든 서버 레벨 또는 시스템 레벨 환경 변수와 같은 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 애플리케이션 소스 컨트롤에 커밋하지 말아야 합니다. 각 개발자 및 서버가 서로 다른 환경 구성을 필요로 할 수 있기 때문입니다. 또한, 소스 저장소가 해킹될 경우 민감한 자격 증명이 노출될 수 있어 보안상 위험합니다.

하지만 Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files)를 이용하면 환경 파일을 안전하게 암호화하여 소스 컨트롤에 저장할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 불러오기 전에, Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지 혹은 `--env` CLI 인자가 지정되었는지 확인합니다. 만약 그렇다면, Laravel은 `.env.[APP_ENV]` 파일이 존재하는지 확인 후 존재하면 해당 파일을, 없으면 기본 `.env` 파일을 불러옵니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 기본적으로 문자열로 해석되지만, `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 예약어를 사용할 수 있습니다:

<div class="overflow-auto">

| `.env` 값   | `env()` 반환값         |
| ----------- | --------------------- |
| true        | (bool) true           |
| (true)      | (bool) true           |
| false       | (bool) false          |
| (false)     | (bool) false          |
| empty       | (string) ''           |
| (empty)     | (string) ''           |
| null        | (null) null           |
| (null)      | (null) null           |

</div>

값에 띄어쓰기가 필요한 경우, 큰따옴표로 감싸서 정의할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정값 조회

`.env` 파일에 나열된 모든 변수는 애플리케이션이 요청을 받을 때 PHP의 `$_ENV` 슈퍼글로벌에 로드됩니다. 설정 파일 내에서 이 변수들의 값을 조회하려면 `env` 함수를 사용할 수 있습니다. 실제로 Laravel의 여러 설정 파일을 보면 많은 옵션들이 이미 이 함수를 사용하고 있습니다:

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인자는 "기본값"으로, 해당 키에 대한 환경 변수가 없는 경우 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인

현재 애플리케이션의 환경은 `.env` 파일 내의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드를 통해 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

`environment` 메서드에 인자를 넘겨 주어진 값과 환경이 일치하는지 확인할 수도 있습니다. 환경이 일치하면 `true`를 반환합니다:

```php
if (App::environment('local')) {
    // 환경이 local임
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 아니면 staging임...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 레벨의 `APP_ENV` 환경 변수 정의로 재정의될 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 소스 컨트롤에 저장하면 안 됩니다. 하지만 Laravel은 환경 파일을 안전하게 암호화하여 애플리케이션과 함께 소스 관리에 추가할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하면 됩니다:

```shell
php artisan env:encrypt
```

이 명령을 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일로 저장됩니다. 암호화 키는 명령 실행 결과에 출력되므로, 반드시 안전한 패스워드 매니저에 보관해야 합니다. 직접 암호화 키를 지정하고 싶다면 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 키의 길이는 사용하는 암호화 알고리즘에 맞아야 합니다. 기본적으로 Laravel은 32자의 키가 필요한 `AES-256-CBC` 알고리즘을 사용합니다. `--cipher` 옵션을 사용해 Laravel이 지원하는 [Encrypter](/docs/{{version}}/encryption)의 다른 암호화 방식도 선택할 수 있습니다.

애플리케이션에 `.env`, `.env.staging` 등 복수의 환경 파일이 있다면, `--env` 옵션으로 암호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령은 복호화 키가 필요하며, Laravel은 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 이 키를 가져옵니다:

```shell
php artisan env:decrypt
```

또는 키를 직접 `--key` 옵션으로 제공할 수도 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령이 실행되면 `.env.encrypted` 파일의 내용이 복호화되어 `.env` 파일로 저장됩니다.

`--cipher` 옵션으로 사용자 지정 암호화 방식을 지정할 수도 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일을 사용하는 경우, `--env` 옵션을 통해 복호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰고 싶다면 `--force` 옵션을 추가합니다:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정값 접근

애플리케이션 어디에서나 `Config` 파사드 또는 전역 `config` 함수를 통해 쉽게 설정값에 접근할 수 있습니다. 설정값은 "점(dot) 문법"을 사용하여 접근합니다(파일명.옵션명). 존재하지 않을 경우 반환할 기본값을 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정값이 없을 때 기본값 가져오기...
$value = config('app.timezone', 'Asia/Seoul');
```

런타임에서 설정값을 변경하려면 `Config` 파사드의 `set` 메서드나, 배열을 `config` 함수에 전달하세요:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석 지원을 위해 `Config` 파사드는 타입별 설정값 반환 메서드도 제공합니다. 반환값이 기대하는 타입과 다르면 예외가 발생합니다:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션 성능을 높이려면, `config:cache` Artisan 명령어로 모든 설정 파일을 하나의 파일로 캐시하세요. 이렇게 하면 모든 앱 설정 옵션이 하나의 파일로 합쳐져 프레임워크가 빠르게 로드할 수 있습니다.

보통 운영 배포 과정에서 `php artisan config:cache` 명령을 실행하세요. 개발 중에는 설정 변경이 잦으므로 이 명령을 실행해서는 안 됩니다.

설정이 캐시되면, 애플리케이션의 `.env` 파일은 요청이나 Artisan 명령에서 로드되지 않습니다. 따라서 `env` 함수는 오직 외부(시스템 레벨) 환경 변수만 반환하게 됩니다.

이유 때문에, `env` 함수는 반드시 애플리케이션의 설정 파일(`config`) 내에서만 호출해야 합니다. [위 설명](#accessing-configuration-values)처럼 어디서든 `config` 함수를 통해 설정값을 가져올 수 있습니다.

캐시된 설정 제거는 `config:clear` 명령을 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache`를 실행했다면, 반드시 `env` 함수를 설정 파일 안에서만 호출해야 합니다. 설정이 캐시된 후엔 `.env` 파일이 로드되지 않으므로, `env` 함수는 외부(시스템) 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 파일 게시

대부분의 Laravel 설정 파일은 이미 애플리케이션의 `config` 디렉토리에 게시되어 있지만, `cors.php`나 `view.php`와 같이 기본적으로 게시되지 않은 설정 파일도 있습니다(대부분의 앱에서 수정할 필요가 없는 파일).

이런 파일도 필요하다면 `config:publish` Artisan 명령어로 게시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 어느 정도의 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 개발 환경에서는 `APP_DEBUG` 환경 변수를 반드시 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 항상 `false`로 두세요. 운영 환경에서 `true`로 두면 민감한 설정 값이 엔드유저에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

애플리케이션이 점검 모드일 때는 모든 요청에 대해 사용자 정의 화면이 표시됩니다. 덕분에 업데이트나 유지보수 시 쉽게 "애플리케이션을 비활성화"할 수 있습니다. 점검 모드 체크는 기본 미들웨어 스택에 포함돼 있습니다. 점검 모드에 들어가면 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태코드와 함께 발생합니다.

점검 모드를 활성화하려면 `down` 명령을 실행하세요:

```shell
php artisan down
```

점검 모드 응답에 `Refresh` HTTP 헤더를 추가하려면, `down` 명령에 `refresh` 옵션을 사용하세요. 브라우저는 지정한 초 후 페이지를 자동 새로고침합니다:

```shell
php artisan down --refresh=15
```

또한, `down` 명령에 `retry` 옵션을 지정해 `Retry-After` HTTP 헤더 값을 설정할 수 있습니다(브라우저에서는 거의 무시됨):

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

비밀 토큰을 이용해 점검 모드를 우회할 수 있습니다. `secret` 옵션에 토큰을 지정하세요:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

이후 토큰이 포함된 애플리케이션 URL에 접속하면 Laravel이 점검 모드 우회 쿠키를 브라우저에 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 대신 생성하게 하려면 `with-secret` 옵션을 사용할 수 있습니다. 점검 모드 진입 시 토큰이 표시됩니다:

```shell
php artisan down --with-secret
```

이렇게 숨겨진 경로로 접근하면 `/` 경로로 리다이렉트됩니다. 쿠키가 발급된 이후에는 점검 모드여도 정상적으로 앱을 사용할 수 있습니다.

> [!NOTE]
> 점검 모드용 비밀 토큰은 보통 영문자, 숫자, 그리고 선택적으로 대시(-)만 사용하길 권장합니다. URL에서 의미가 있는 문자(예: `?`, `&`)는 피하세요.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버 점검 모드

기본적으로 Laravel은 파일 기반 시스템을 이용해 점검 모드 여부를 확인합니다. 따라서 애플리케이션을 호스팅하는 각 서버에서 `php artisan down` 명령을 실행해야 점검 모드가 활성화됩니다.

대신 캐시 기반 방법도 지원합니다. 이 방식에서는 한 서버에서만 `php artisan down` 명령을 실행하면 됩니다. 사용하려면 `.env` 파일에서 점검 모드 관련 변수를 수정하세요. 여러 서버에서 접근 가능한 캐시 `store`를 선택해야 합니다. 모든 서버에서 점검 모드 상태가 일관되게 유지됩니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 화면 미리 렌더링

배포 과정에서 `php artisan down` 명령을 사용하는 경우, Composer 의존성이나 인프라가 갱신되는 동안 사용자가 애플리케이션에 접근하면 에러가 발생할 수 있습니다. 이유는, 점검 모드 여부를 판별해 화면을 보여주기 위해 Laravel 프레임워크의 상당 부분이 부팅되어야 하기 때문입니다.

이 문제를 방지하려고 Laravel은 점검 모드 화면을 미리 렌더링할 수 있게 해줍니다. 모든 의존성 로드 전에 해당 화면이 반환됩니다. `down` 명령의 `render` 옵션을 사용해 원하는 템플릿을 미리 렌더하세요:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리디렉션

점검 모드일 때, 모든 애플리케이션 URL 접근 시 점검 모드 화면이 나타나지만, 모든 요청을 특정 URL로 리디렉션하도록 지정할 수 있습니다. 예를 들어 모든 요청을 `/` 경로로 리디렉션하려면:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 비활성화

점검 모드를 해제하려면 `up` 명령을 실행하세요:

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿은 `resources/views/errors/503.blade.php` 파일로 직접 커스터마이즈할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐

애플리케이션이 점검 모드일 때는 어떤 [대기열 작업](/docs/{{version}}/queues)도 처리되지 않습니다. 점검 모드가 해제되면 작업이 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드는 몇 초가량 서비스 중단이 필요하므로, 완전 무중단 배포가 가능한 [Laravel Cloud](https://cloud.laravel.com)와 같은 SaaS 플랫폼 이용을 고려하세요.