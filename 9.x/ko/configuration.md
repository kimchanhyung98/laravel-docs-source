# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 조회](#retrieving-environment-configuration)
    - [현재 환경 확인](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근](#accessing-configuration-values)
- [설정 캐시](#configuration-caching)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에 대한 설명이 포함되어 있으니, 파일들을 살펴보면서 어떤 옵션들이 제공되는지 익혀두시기 바랍니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보 등과 같은 기본적인 설정뿐만 아니라 애플리케이션의 타임존, 암호화 키 같은 다양한 핵심 구성값을 설정할 수 있도록 해줍니다.

<a name="application-overview"></a>
#### 애플리케이션 개요 (Application Overview)

급하게 전체 설정 구성을 빠르게 보고 싶다면 `about` Artisan 명령어를 사용하세요:

```shell
php artisan about
```

특정 섹션만 보고 싶다면 `--only` 옵션을 사용하여 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 다른 설정 값을 사용하는 것이 종종 유용합니다. 예를 들어, 로컬 개발 환경과 실제 운영 서버에서 다른 캐시 드라이버를 사용하고자 할 수 있습니다.

이를 쉽게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. Laravel을 새로 설치하면, 애플리케이션 루트 디렉토리에 `.env.example` 파일이 있는데, 이 파일에는 흔히 쓰이는 환경 변수들이 정의되어 있습니다. Laravel 설치 과정에서 이 파일은 자동으로 `.env` 파일로 복사됩니다.

Laravel 기본 `.env` 파일은 로컬 환경인지 운영 서버인지에 따라 달라질 수 있는 몇 가지 공통 설정 값을 담고 있습니다. 이 값들은 Laravel의 `env` 함수를 통해 `config` 디렉토리 내 다양한 설정 파일에서 읽어옵니다.

팀 단위로 개발할 경우, `.env.example` 파일을 계속 포함시키는 것이 좋습니다. 예제 파일에 자리 표시자 값들을 넣어두면, 다른 개발자가 어떤 환경 변수가 필요한지 명확히 알 수 있습니다.

> [!NOTE]
> `.env` 파일에 정의된 모든 변수는 서버 또는 시스템 수준의 외부 환경 변수에 의해 덮어쓰여질 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안 (Environment File Security)

`.env` 파일은 각각의 개발자나 서버에 따라 다른 환경 설정이 필요하기 때문에 소스 코드 저장소에 커밋하지 않아야 합니다. 또한, 만약 외부 침입자가 저장소에 접근할 경우 중요한 자격 증명이 노출될 위험이 있습니다.

하지만 Laravel의 내장 [환경 암호화](#encrypting-environment-files) 기능을 이용하면 환경 파일을 암호화하여 소스 코드 저장소에 안전하게 보관할 수도 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일 (Additional Environment Files)

애플리케이션 환경 변수를 로드하기 전에, Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지, 또는 CLI 실행 시 `--env` 인수로 지정되었는지를 확인합니다. 만약 그렇다면, 해당 환경에 맞는 `.env.[APP_ENV]` 파일이 존재할 경우 그 파일을 먼저 로드하며, 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입 (Environment Variable Types)

`.env` 파일 내 변수들은 보통 문자열로 파싱됩니다. 하지만 `env()` 함수가 더 다양한 타입을 반환할 수 있도록 몇 가지 예약값이 정의되어 있습니다:

| `.env` 값  | `env()` 반환값       |
|------------|---------------------|
| true       | (bool) true         |
| (true)     | (bool) true         |
| false      | (bool) false        |
| (false)    | (bool) false        |
| empty      | (string) ''         |
| (empty)    | (string) ''         |
| null       | (null) null         |
| (null)     | (null) null         |

값에 공백이 포함돼야 하는 경우, 큰따옴표로 감싸서 정의할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 조회 (Retrieving Environment Configuration)

`.env`에 정의된 모든 변수는 애플리케이션 요청 시 `$_ENV` PHP 슈퍼글로벌로 로드됩니다. 또한, 설정 파일 내에서 `env` 함수를 사용해 이러한 값을 쉽게 조회할 수 있습니다. Laravel 설정 파일을 보면 여러 옵션들이 이미 이 함수를 사용하고 있음을 알 수 있습니다:

```
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인수는 기본값이며, 해당 환경 변수가 없을 경우 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인 (Determining The Current Environment)

현재 애플리케이션 환경은 `.env` 파일에 설정된 `APP_ENV` 변수로 결정됩니다. `App` [페이사드](/docs/9.x/facades)의 `environment` 메서드를 통해 이 값을 확인할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, 인수를 전달하여 특정 환경인지 확인할 수도 있습니다. 전달한 값 중 하나라도 현재 환경과 일치하면 `true`가 반환됩니다:

```
if (App::environment('local')) {
    // 현재 환경이 local 임
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 또는 staging 임
}
```

> [!NOTE]
> 서버 수준의 `APP_ENV` 환경 변수를 정의하면, 애플리케이션 환경 감지가 이를 우선하여 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화 (Encrypting Environment Files)

암호화되지 않은 환경 파일은 소스 코드 저장소에 절대 저장하지 않는 것이 좋습니다. 하지만 Laravel은 환경 파일을 암호화하여 애플리케이션의 다른 파일과 함께 안전하게 저장할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화 (Encryption)

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용할 수 있습니다:

```shell
php artisan env:encrypt
```

이 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일로 저장됩니다. 암호 해제 키는 명령어 출력에 표시되며, 안전한 비밀번호 관리자에 보관해야 합니다. 직접 키를 지정하려면 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 키 길이는 사용 중인 암호화 알고리즘에 맞춰야 하며, 기본적으로 Laravel은 32자리 키를 요구하는 `AES-256-CBC` 암호화를 사용합니다. `--cipher` 옵션으로 Laravel에서 지원하는 다른 암호화를 지정할 수도 있습니다.

여러 환경 파일 예를 들어 `.env`와 `.env.staging`이 있다면, `--env` 옵션으로 특정 환경 파일을 암호화할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화 (Decryption)

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키를 필요로 하며, 기본적으로 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 키를 가져옵니다:

```shell
php artisan env:decrypt
```

직접 키를 지정하려면 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어를 실행하면 `.env.encrypted` 파일이 복호화되어 `.env` 파일에 저장됩니다.

`--cipher` 옵션을 이용하면 커스텀 암호화 방식을 지정할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

앞서 말한 것처럼, 특정 환경 파일을 지정하려면 `--env` 옵션을 사용할 수도 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가하세요:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근 (Accessing Configuration Values)

애플리케이션 어디서든 전역 `config` 함수를 사용해 설정 값을 쉽게 조회할 수 있습니다. 설정 값은 점(dot) 표기법으로 불러오는데, 파일명과 옵션명으로 구성됩니다. 기본값도 지정할 수 있으며, 설정 값이 없으면 기본값이 반환됩니다:

```
$value = config('app.timezone');

// 설정 값이 없으면 기본값 반환
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중에 설정 값을 변경하려면 배열을 `config` 함수에 전달합니다:

```
config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
## 설정 캐시 (Configuration Caching)

애플리케이션 속도를 향상시키기 위해, 모든 설정 파일을 하나의 파일로 캐시할 수 있습니다. `config:cache` Artisan 명령어를 사용하면 모든 설정이 하나로 합쳐져 빠르게 로드됩니다.

보통 이 명령어는 배포 과정에서 실행해야 하며, 개발 중에는 자주 변경되는 설정 때문에 실행하지 않는 것이 좋습니다.

캐시된 설정을 지우려면 다음 명령어를 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 중에 `config:cache`를 실행한다면, 설정 파일 내에서는 반드시 `env` 함수만 호출해야 합니다. 캐시 후에는 `.env` 파일이 로드되지 않으므로, `env` 함수는 오직 시스템 수준 환경 변수만 반환합니다.

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일 내 `debug` 옵션은 오류 발생 시 사용자에게 보여줄 정보량을 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수를 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 값을 `true`로 설정하세요. **운영 환경에서는 반드시 `false`로 설정해야 하며, `true`로 설정하면 민감한 설정 값이 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지보수 모드 (Maintenance Mode)

유지보수 모드가 활성화되면, 모든 요청에 대해 사용자 정의 뷰가 표시됩니다. 변경 작업이나 점검 중인 애플리케이션을 "일시 중지"하는 데 유용합니다. 유지보수 모드 확인은 애플리케이션 기본 미들웨어 스택에 포함되어 있으며, 해당 모드인 경우 HTTP 상태 코드 503과 함께 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

```shell
php artisan down
```

모든 유지보수 모드 응답에 `Refresh` HTTP 헤더를 보내 자동 새로 고침을 원한다면, `--refresh` 옵션을 사용할 수 있습니다. 지정한 초 후에 브라우저가 페이지를 자동 새로 고침합니다:

```shell
php artisan down --refresh=15
```

또한, `--retry` 옵션으로 `Retry-After` HTTP 헤더 값을 설정할 수도 있지만, 대부분 브라우저는 이 헤더를 무시합니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회 (Bypassing Maintenance Mode)

비밀 토큰을 이용해 유지보수 모드를 우회하려면 `--secret` 옵션으로 토큰을 지정하세요:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 상태에서 토큰 URL에 접속하면 Laravel이 우회 쿠키를 브라우저에 발급하고, 이를 통해 유지보수 모드임에도 애플리케이션을 정상적으로 이용할 수 있습니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

해당 URL에 접속하면 `/` 라우트로 리다이렉트되며, 쿠키가 발급된 후에는 유지보수 모드가 아닌 것처럼 애플리케이션을 탐색할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰은 보통 영숫자 및 선택적으로 대시(-) 문자를 포함하며, URL에서 특별한 의미를 갖는 `?`, `&` 같은 문자는 피하세요.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링 (Pre-Rendering The Maintenance Mode View)

`php artisan down` 명령어 사용 시, Composer 의존성이나 인프라 업데이트 중에 사용자가 접속하면 일부 오류가 발생할 수 있습니다. 이는 유지보수 모드 여부를 확인하고 블레이드 템플릿으로 유지보수 페이지를 렌더링하려면 Laravel 프레임워크의 상당 부분이 부팅되어야 하기 때문입니다.

이를 방지하려 Laravel은 요청 초기 단계에서 바로 반환할 수 있는 유지보수 모드 뷰를 사전 렌더링하는 기능을 제공합니다. 원하는 템플릿 파일을 지정해 미리 렌더링할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리다이렉트 (Redirecting Maintenance Mode Requests)

유지보수 모드 중에는 애플리케이션 URL에 접근하면 유지보수 페이지가 표시됩니다. 필요한 경우 모든 요청을 특정 URL로 리다이렉트하도록 설정할 수 있습니다. 예를 들어 모든 요청을 `/` URI로 리다이렉트하려면 다음과 같이 합니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제 (Disabling Maintenance Mode)

유지보수 모드를 해제하려면 `up` 명령어를 사용하세요:

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php` 파일을 만들어 직접 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐 (Maintenance Mode & Queues)

유지보수 모드 상태에서는 [큐 작업](/docs/9.x/queues)이 처리되지 않습니다. 모드가 해제되면 큐 작업은 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안 (Alternatives To Maintenance Mode)

유지보수 모드는 애플리케이션에 몇 초간의 다운타임이 발생합니다. 무중단 배포가 필요한 경우 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io) 같은 도구를 활용하는 것을 고려해보세요.