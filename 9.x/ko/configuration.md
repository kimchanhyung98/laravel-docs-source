# 설정

- [소개](#소개)
- [환경 설정](#환경-설정)
    - [환경 변수 타입](#환경-변수-타입)
    - [환경 설정 값 가져오기](#환경-설정-값-가져오기)
    - [현재 환경 확인](#현재-환경-확인)
    - [환경 파일 암호화](#환경-파일-암호화)
- [설정 값 접근](#설정-값-접근)
- [설정 캐싱](#설정-캐싱)
- [디버그 모드](#디버그-모드)
- [유지보수 모드](#유지보수-모드)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션은 문서화되어 있으므로, 다양한 옵션을 직접 살펴보고 익숙해지시기 바랍니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션의 타임존, 암호화 키 등 다양한 핵심 설정 값을 구성할 수 있게 해줍니다.

<a name="application-overview"></a>
#### 애플리케이션 개요

빠르게 살펴보고 싶으신가요? `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요를 빠르게 확인할 수 있습니다.

```shell
php artisan about
```

특정 섹션의 출력만 보고 싶다면, `--only` 옵션을 사용해 해당 섹션만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
## 환경 설정

같은 애플리케이션이라도 실행되는 환경에 따라 서로 다른 설정 값이 필요할 수 있습니다. 예를 들어, 로컬 환경에서는 프로덕션 서버와 다른 캐시 드라이버를 사용할 수도 있습니다.

이를 쉽게 관리할 수 있도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새로 설치된 Laravel 애플리케이션의 루트 디렉터리에는 여러 공통 환경 변수가 정의된 `.env.example` 파일이 포함되어 있습니다. Laravel 설치 과정에서 이 파일은 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있는 주요 설정 값이 포함되어 있습니다. 이 값들은 Laravel의 `env` 함수를 통해 `config` 디렉터리 내 다양한 설정 파일에서 불러와 사용됩니다.

팀에서 개발 중이라면, `.env.example` 파일을 애플리케이션에 포함시키는 것이 좋습니다. 예시 설정 파일에 기본값(또는 플레이스홀더 값)을 넣어두면, 다른 팀원도 어떤 환경 변수가 필요한지 쉽게 확인할 수 있습니다.

> **참고**  
> `.env` 파일의 모든 변수는 서버 또는 시스템 레벨 환경 변수 등 외부 환경 변수로 재정의(overriding)될 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 개발자나 서버마다 환경 구성이 다를 수 있으므로 소스 컨트롤(버전 관리 시스템)에 커밋하지 않아야 합니다. 또한, 만약 소스 저장소에 침입자가 접근할 경우, 민감한 정보가 노출될 수 있어 보안 위험이 발생합니다.

하지만 Laravel의 내장 [환경 파일 암호화](#환경-파일-암호화) 기능을 사용해 환경 파일을 암호화할 수 있습니다. 암호화된 환경 파일은 안전하게 소스 컨트롤에 포함할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 불러오기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 또는 `--env` CLI 인자가 지정되었는지를 확인합니다. 해당 경우가 있으면, Laravel은 `.env.[APP_ENV]` 파일이 존재할 경우 이를 불러옵니다. 만약 존재하지 않으면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 기본적으로 문자열 타입으로 해석됩니다. 하지만, `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 몇 가지 예약어가 존재합니다.

| `.env` 값   | `env()` 반환값  |
|-------------|----------------|
| true        | (bool) true    |
| (true)      | (bool) true    |
| false       | (bool) false   |
| (false)     | (bool) false   |
| empty       | (string) ''    |
| (empty)     | (string) ''    |
| null        | (null) null    |
| (null)      | (null) null    |

공백이 포함된 값을 환경 변수에 지정하려면, 값을 큰따옴표로 감싸면 됩니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 나열된 모든 변수들은 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 설정 파일에서는 이 변수 값을 `env` 함수로 가져올 수 있습니다. 실제로 Laravel의 설정 파일을 살펴보면, 많은 옵션에서 이미 이 함수를 사용합니다.

    'debug' => env('APP_DEBUG', false),

`env` 함수에 전달하는 두 번째 값은 "기본값(default value)"입니다. 주어진 키에 해당하는 환경 변수가 없으면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드로 가져올 수 있습니다.

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

`environment` 메서드에 인자를 전달하면 현재 환경이 해당 값과 일치하는지 확인할 수 있습니다. 일치하는 값이 하나라도 있으면 이 메서드는 `true`를 반환합니다.

    if (App::environment('local')) {
        // 현재 환경은 local입니다.
    }

    if (App::environment(['local', 'staging'])) {
        // 현재 환경은 local 또는 staging입니다.
    }

> **참고**  
> 현재 애플리케이션 환경은 서버 레벨의 `APP_ENV` 환경 변수로 오버라이드할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 소스 컨트롤에 저장해서는 안 됩니다. 하지만, Laravel은 환경 파일을 암호화해서 안전하게 소스 컨트롤에 추가할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면, `env:encrypt` 명령어를 사용합니다.

```shell
php artisan env:encrypt
```

`env:encrypt` 명령을 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화(해독) 키는 명령 출력에 표시되며, 반드시 안전한 비밀번호 관리 프로그램에 보관해야 합니다. 직접 암호화 키를 지정하고 싶다면, 명령어에 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> **참고**  
> 제공하는 키의 길이는 사용하는 암호화 알고리즘이 요구하는 길이와 일치해야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 암호화를 사용합니다. 명령어에 `--cipher` 옵션을 추가해 Laravel [암호화기](/docs/{{version}}/encryption)가 지원하는 다른 알고리즘을 사용할 수도 있습니다.

`.env`나 `.env.staging` 등 복수의 환경 파일이 있는 경우, `--env` 옵션을 통해 특정 환경 파일을 암호화할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면, `env:decrypt` 명령어를 사용합니다. 이 명령어는 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 복호화 키를 불러옵니다.

```shell
php artisan env:decrypt
```

또는, `--key` 옵션으로 복호화 키를 직접 지정할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면, `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장합니다.

`env:decrypt` 명령어에 `--cipher` 옵션을 추가해 커스텀 암호화 알고리즘을 사용할 수도 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일(예: `.env`, `.env.staging`)이 있는 경우, `--env` 옵션을 통해 특정 환경 파일만 복호화할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면, `env:decrypt` 명령에 `--force` 옵션을 추가합니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근

애플리케이션 어디서든 글로벌 `config` 함수를 사용하여 설정 값을 쉽게 가져올 수 있습니다. 설정 값은 "점 표기법(dot syntax)"으로 접근하는데, 파일명과 접근하려는 옵션명을 포함합니다. 기본값도 지정할 수 있으며, 해당 옵션이 없을 때 반환됩니다.

    $value = config('app.timezone');

    // 설정 값이 없을 때 기본값 반환...
    $value = config('app.timezone', 'Asia/Seoul');

실행 중 설정 값을 변경하려면 `config` 함수에 배열을 전달하세요.

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션의 속도를 높이기 위해 모든 설정 파일을 하나의 파일로 캐싱하여 `config:cache` Artisan 명령어로 합칠 수 있습니다. 이 명령어는 애플리케이션의 모든 설정 옵션을 하나의 파일에 모아서, 프레임워크가 더욱 빠르게 로드할 수 있도록 해줍니다.

`php artisan config:cache` 명령은 프로덕션 배포 단계에서 실행하는 것이 일반적입니다. 개발 중에는 설정 값이 자주 변경되므로 실행하지 않는 것이 좋습니다.

캐시된 설정을 삭제하려면 `config:clear` 명령어를 사용하세요.

```shell
php artisan config:clear
```

> **경고**  
> 배포 과정에서 `config:cache` 명령어를 실행했다면, `env` 함수는 반드시 설정 파일 내에서만 호출해야 합니다. 설정이 캐싱된 이후에는 `.env` 파일이 로드되지 않으므로, `env` 함수는 외부 시스템 레벨 환경 변수만 반환합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 오류 발생 시 사용자에게 어느 정도의 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG`를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 하며, 만약 `true`로 설정되어 있다면 민감한 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지보수 모드

애플리케이션이 유지보수 모드일 때는 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이는 업데이트나 점검 중일 때 애플리케이션을 쉽게 "비활성화"할 수 있도록 해 줍니다. 유지보수 모드 체크는 기본 미들웨어 스택에 포함되어 있으며, 유지보수 모드일 때는 503 상태 코드와 함께 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령을 실행하세요.

```shell
php artisan down
```

모든 유지보수 응답에 `Refresh` HTTP 헤더를 보내고 싶다면, `down` 명령어에 `refresh` 옵션을 사용할 수 있습니다. `Refresh` 헤더는 지정한 초 후 브라우저가 자동으로 페이지를 새로고침하도록 지시합니다.

```shell
php artisan down --refresh=15
```

또한 `retry` 옵션을 사용하여 `Retry-After` HTTP 헤더 값을 설정할 수 있습니다.(대부분의 브라우저는 이 헤더를 무시합니다.)

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회

비밀 토큰을 이용해 유지보수 모드를 우회할 수 있도록 `secret` 옵션으로 토큰을 지정하세요.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 유지보수 모드로 전환한 후, 이 토큰이 포함된 URL로 이동하면 Laravel이 유지보수 모드 우회 쿠키를 브라우저에 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

이 숨겨진 경로로 접속하면, 애플리케이션의 `/` 경로로 리디렉션됩니다. 한 번 쿠키가 발급되면, 유지보수 모드가 아닌 것처럼 정상적으로 애플리케이션에 접속할 수 있습니다.

> **참고**  
> 유지보수 모드 비밀 토큰은 일반적으로 영문, 숫자, 하이픈(-)만 사용해야 하며, URL에서 특수 의미를 갖는 `?`나 `&` 등의 문자는 피해야 합니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 뷰 미리 렌더링

배포 시 `php artisan down` 명령어를 사용하면, 사용자가 Composer 의존성이나 기타 인프라가 업데이트되는 도중 애플리케이션에 접속할 경우 오류가 발생하기도 합니다. 이는 Laravel이 유지보수 모드임을 판단하고 템플릿 엔진을 사용해 뷰를 렌더링하기 위해 일정 부분 부팅을 먼저 진행하기 때문입니다.

이런 이유로, Laravel은 요청 사이클 시작 시점에 반환할 유지보수 모드 뷰를 미리 렌더링하는 기능을 제공합니다. 의존성이 로드되기 전에 이 뷰가 바로 반환됩니다. `down` 명령어의 `render` 옵션을 통해 원하는 템플릿을 미리 렌더링할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리디렉션

유지보수 모드에서는 사용자가 접근하는 모든 URL에 대해 유지보수 뷰가 표시됩니다. 필요하다면 모든 요청을 특정 URL로 리디렉션하도록 Laravel에 지시할 수 있습니다. 예를 들어, 모든 요청을 `/` URI로 리디렉션하려면 다음과 같이 합니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제

유지보수 모드를 해제하려면 `up` 명령어를 사용하세요.

```shell
php artisan up
```

> **참고**  
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php`에 직접 정의하여 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드 & 큐

애플리케이션이 유지보수 모드에 들어가 있는 동안에는 어떠한 [큐 작업](/docs/{{version}}/queues)도 처리되지 않습니다. 유지보수 모드 해제 시 다시 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션이 몇 초간 다운타임을 가질 수밖에 없으므로, [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io)와 같은 대안을 통해 무중단 배포(Zero-downtime deployment)를 고려해 보세요.