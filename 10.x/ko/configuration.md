# 설정(Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 유형](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [디버그 모드](#debug-mode)
- [유지 보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각각의 옵션은 문서화되어 있으므로, 파일을 살펴보며 사용 가능한 옵션에 익숙해지시기 바랍니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션의 타임존, 암호화 키와 같은 다양한 핵심 설정 값을 구성할 수 있습니다.

<a name="application-overview"></a>
#### 애플리케이션 개요

빠르게 살펴볼 필요가 있나요? `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 전체 개요를 확인할 수 있습니다:

```shell
php artisan about
```

애플리케이션 개요 출력에서 특정 섹션만 관심 있다면 `--only` 옵션으로 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 살펴보고 싶다면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 다른 설정 값을 사용하는 것이 도움이 되는 경우가 많습니다. 예를 들어, 로컬에서는 프로덕션 서버와 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

이를 쉽게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새로운 Laravel 설치 시, 애플리케이션의 루트 디렉터리에는 여러 일반적인 환경 변수를 정의하는 `.env.example` 파일이 포함되어 있습니다. 설치 과정 중 이 파일은 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬 또는 프로덕션 웹 서버에서 실행되는지에 따라 다를 수 있는 설정 값들이 포함돼 있습니다. 이 값들은 `config` 폴더 내의 여러 Laravel 설정 파일에서 Laravel의 `env` 함수를 통해 읽혀집니다.

여러 명이 함께 개발하는 경우 `.env.example` 파일을 계속 포함시키는 것이 좋습니다. 예시 설정 파일에 자리 표시자 값을 넣어두면, 다른 개발자들이 애플리케이션을 실행하는 데 필요한 환경 변수를 명확하게 확인할 수 있습니다.

> [!NOTE]  
> `.env` 파일의 어떤 변수든 서버 수준이나 시스템 수준의 외부 환경 변수를 통해 재정의될 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자 및 서버에 맞는 환경 구성이 필요하므로, 소스 컨트롤에 커밋해서는 안 됩니다. 또한, 침입자가 소스 컨트롤 저장소에 접근할 경우 민감한 자격 증명이 노출될 위험이 있습니다.

그러나 Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 사용하여 환경 파일을 암호화할 수 있으며, 암호화된 파일은 안전하게 소스 컨트롤에 추가할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로드하기 전에 Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 또는 CLI에서 `--env` 인자가 지정되었는지를 확인합니다. 해당하는 경우, Laravel은 `.env.[APP_ENV]` 파일이 존재하는지 확인하여 존재하면 이를 로드합니다. 존재하지 않으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 유형

`.env` 파일의 모든 변수는 기본적으로 문자열로 파싱되지만, `env()` 함수에서 다양한 타입을 반환할 수 있도록 몇 가지 예약 값이 마련되어 있습니다:

| `.env` 값  | `env()` 반환값      |
|------------|--------------------|
| true       | (bool) true        |
| (true)     | (bool) true        |
| false      | (bool) false       |
| (false)    | (bool) false       |
| empty      | (string) ''        |
| (empty)    | (string) ''        |
| null       | (null) null        |
| (null)     | (null) null        |

값에 공백이 포함된 환경 변수가 필요할 경우, 큰따옴표로 감싸서 정의하세요:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 나열된 모든 변수는 애플리케이션이 요청을 받을 때 PHP의 `$_ENV` 슈퍼 글로벌로 로드됩니다. 그러나 설정 파일에서는 `env` 함수를 사용해 이러한 변수의 값을 가져올 수 있습니다. 실제로 Laravel의 설정 파일을 살펴보면 많은 옵션들이 이미 이 함수를 사용하고 있음을 알 수 있습니다:

    'debug' => env('APP_DEBUG', false),

`env` 함수의 두 번째 인자는 "기본값"입니다. 지정된 키에 대한 환경 변수가 없을 경우 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드를 통해 접근할 수 있습니다:

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

또한 `environment` 메서드에 인자를 전달하여 환경이 주어진 값과 일치하는지 확인할 수 있습니다. 일치하는 값이 하나라도 있으면 `true`를 반환합니다:

    if (App::environment('local')) {
        // 환경이 local입니다.
    }

    if (App::environment(['local', 'staging'])) {
        // 환경이 local이거나 staging입니다...
    }

> [!NOTE]  
> 현재 애플리케이션 환경 감지는 서버 수준의 `APP_ENV` 환경 변수 정의로 재정의할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 절대로 소스 컨트롤에 저장해서는 안 됩니다. 그러나 Laravel은 환경 파일을 암호화할 수 있도록 하여, 애플리케이션의 나머지 부분과 함께 안전하게 소스 컨트롤에 추가할 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하세요:

```shell
php artisan env:encrypt
```

`env:encrypt` 명령을 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화 키는 명령 실행 결과로 출력되며, 안전한 비밀번호 관리 소프트웨어에 보관해야 합니다. 직접 암호화 키를 제공하려면 명령 실행 시 `--key` 옵션을 사용하세요:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]  
> 제공된 키의 길이는 사용 중인 암호화 암호에 필요한 길이와 일치해야 합니다. 기본적으로 Laravel은 `AES-256-CBC` 암호를 사용하며, 32자의 키를 필요로 합니다. 명령 실행 시 `--cipher` 옵션을 통해, Laravel의 [암호화기](/docs/{{version}}/encryption)에서 지원하는 어떠한 암호도 자유롭게 사용할 수 있습니다.

여러 환경 파일(예: `.env`, `.env.staging`)이 있는 경우, `--env` 옵션을 통해 암호화할 환경 파일의 이름을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용하세요. 이 명령은 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 가져옵니다:

```shell
php artisan env:decrypt
```

또는, 키를 명령어에 직접 `--key` 옵션으로 제공할 수 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령이 실행되면 `.env.encrypted` 파일의 내용이 복호화되어 `.env` 파일에 저장됩니다.

사용자 지정 암호화 암호를 사용하려면 `--cipher` 옵션도 제공할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일(예: `.env`, `.env.staging`)이 있는 경우, `--env` 옵션을 통해 복호화할 환경 파일의 이름을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `env:decrypt` 명령에 `--force` 옵션을 사용하세요:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근

애플리케이션 어디에서든 `Config` 파사드 또는 전역 `config` 함수를 사용해 설정 값을 간편하게 읽을 수 있습니다. 설정 값은 "점" 표기법(dot syntax, 예: 파일명.옵션)을 사용해 접근하며, 기본값도 지정할 수 있습니다. 설정 옵션이 없을 경우 기본값이 반환됩니다.

    use Illuminate\Support\Facades\Config;

    $value = Config::get('app.timezone');

    $value = config('app.timezone');

    // 설정 값이 없으면 기본값을 가져옴...
    $value = config('app.timezone', 'Asia/Seoul');

런타임에 설정 값을 변경하려면 `Config` 파사드의 `set` 메서드 또는 배열을 `config` 함수에 전달할 수 있습니다:

    Config::set('app.timezone', 'America/Chicago');

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션의 속도를 높이기 위해 모든 설정 파일을 하나의 파일로 캐시하려면 `config:cache` Artisan 명령어를 사용하세요. 이 명령은 모든 설정 옵션을 하나의 파일로 결합하여 프레임워크가 빠르게 로딩할 수 있게 합니다.

이 명령은 일반적으로 프로덕션 배포 과정의 일부로 실행되어야 합니다. 개발 단계에서는 설정 옵션을 자주 변경해야 하므로 로컬 개발 중에는 실행하지 않는 것이 좋습니다.

설정이 캐시된 후에는 애플리케이션의 `.env` 파일이 요청이나 Artisan 명령 도중 프레임워크에서 로드되지 않습니다. 따라서 `env` 함수는 외부(시스템 수준)의 환경 변수만 반환합니다.

이러한 이유로, 반드시 애플리케이션의 설정(`config`) 파일 내에서만 `env` 함수를 호출해야 합니다. Laravel 기본 설정 파일을 보면 이러한 예시를 많이 볼 수 있습니다. 설정 값은 [앞서 설명한 대로](#accessing-configuration-values) 어디서든 `config` 함수를 통해 읽을 수 있습니다.

캐시된 설정을 비우려면 `config:clear` 명령을 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]  
> 배포 과정 중 `config:cache` 명령을 실행한다면 반드시 `env` 함수 호출이 설정 파일 내에만 있는지 확인해야 합니다. 설정이 캐시되면 `.env` 파일이 로드되지 않으므로, `env` 함수는 외부(시스템 수준)의 환경 변수만 반환합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 실제로 얼마나 많은 오류 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> 로컬 개발에서는 `APP_DEBUG` 환경 변수를 `true`로 설정하세요. **프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 만약 프로덕션에서 이 변수가 `true`로 설정되어 있다면, 민감한 설정 값이 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지 보수 모드

애플리케이션이 유지 보수 모드에 들어가 있으면 모든 요청에 대해 사용자 정의 뷰가 표시됩니다. 이렇게 하면 업데이트 중이거나 점검 중에 애플리케이션을 "비활성화"하기 쉽습니다. 기본 미들웨어 스택에 유지 보수 모드 체크가 포함되어 있습니다. 유지 보수 모드일 경우 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태코드로 발생합니다.

유지 보수 모드를 활성화하려면 `down` Artisan 명령을 실행하세요:

```shell
php artisan down
```

모든 유지 보수 모드 응답에 `Refresh` HTTP 헤더를 포함시키려면, `down` 명령어에 `refresh` 옵션을 사용하세요. 브라우저는 지정된 초 이후 자동으로 페이지를 새로고침합니다:

```shell
php artisan down --refresh=15
```

또한, `down` 명령에 `retry` 옵션을 지정하여 `Retry-After` HTTP 헤더 값을 설정할 수 있습니다. (브라우저에서 이 헤더는 일반적으로 무시됩니다):

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지 보수 모드 우회

비밀 토큰을 사용해 유지 보수 모드를 우회할 수 있도록 하려면, `secret` 옵션으로 유지 보수 모드 우회 토큰을 지정하세요:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 유지 보수 모드로 전환한 후, 해당 토큰이 포함된 주소로 접근하면 Laravel은 브라우저에 유지 보수 모드 우회 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

비밀 토큰을 Laravel이 자동 생성하도록 하려면 `with-secret` 옵션을 사용하세요. 애플리케이션이 유지 보수 모드에 진입하면 비밀 토큰이 표시됩니다:

```shell
php artisan down --with-secret
```

이 숨김 경로로 접근하면, 이후 애플리케이션의 `/` 경로로 리다이렉트 됩니다. 쿠키가 브라우저에 발급되면, 유지 보수 모드가 아닌 것처럼 애플리케이션을 정상적으로 탐색할 수 있습니다.

> [!NOTE]  
> 유지 보수 모드 비밀 토큰은 일반적으로 영문, 숫자, 그리고 선택적으로 대시(-)를 조합해서 구성되어야 합니다. URL에서 특별한 의미를 가지는 `?`, `&` 등의 문자는 피해야 합니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지 보수 모드 뷰 미리 렌더링

배포 중 `php artisan down` 명령을 사용할 경우, 사용자들이 Composer 의존성이나 기타 인프라가 업데이트되는 동안 애플리케이션에 접근한다면 간헐적으로 오류를 만날 수 있습니다. 이는 Laravel 프레임워크의 상당 부분이 유지 보수 모드 상태를 판단하고 템플릿 엔진을 사용해 뷰를 렌더링하기 위해 부트되어야 하기 때문입니다.

이런 이유로, Laravel에서는 요청 사이클이 시작될 때 반환할 유지 보수 모드 뷰를 미리 렌더링할 수 있습니다. 이 뷰는 애플리케이션의 의존성이 로드되기 전 렌더링됩니다. 원하는 템플릿을 `down` 명령의 `render` 옵션으로 미리 렌더할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지 보수 모드 요청 리다이렉트

유지 보수 모드에서는 사용자가 접근하는 모든 URL에 대해 유지 보수 모드 뷰가 표시됩니다. 원하는 경우, 모든 요청을 특정 URL로 리다이렉트하도록 Laravel에 지시할 수 있습니다. 예를 들어, 모든 요청을 `/` URI로 리다이렉트하려면 다음과 같이 할 수 있습니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지 보수 모드 해제

유지 보수 모드를 해제하려면 `up` 명령을 사용하세요:

```shell
php artisan up
```

> [!NOTE]  
> 기본 유지 보수 모드 템플릿을 커스터마이즈하려면 `resources/views/errors/503.blade.php` 에 자신만의 템플릿을 정의할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지 보수 모드와 큐

애플리케이션이 유지 보수 모드인 동안에는 [큐 작업](/docs/{{version}}/queues)이 처리되지 않습니다. 유지 보수 모드 해제 후, 작업은 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지 보수 모드의 대안

유지 보수 모드는 애플리케이션에 몇 초간의 다운타임이 필요하므로, [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io)와 같이 Laravel의 무중단 배포(Zero-downtime deployment)를 지원하는 대안을 고려해 보세요.