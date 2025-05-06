# 설정(Configuration)

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
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에는 설명이 붙어 있으니, 파일들을 살펴보며 사용 가능한 옵션에 익숙해지시기 바랍니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 URL, 암호화 키 등 다양한 핵심 설정 값들을 구성할 수 있도록 해줍니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요를 표시할 수 있습니다.

```shell
php artisan about
```

특정 섹션의 개요만 보고 싶을 경우 `--only` 옵션을 사용하여 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 확인하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 다른 설정 값을 사용하는 것이 도움이 될 때가 많습니다. 예를 들어, 로컬 환경에서는 프로덕션 서버와 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

이를 간편하게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새로운 Laravel 설치에서는 애플리케이션의 루트 디렉토리에 `.env.example` 파일이 있으며, 여러 일반 환경 변수를 정의합니다. Laravel 설치 과정에서 이 파일이 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬 또는 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있는 공통 설정 값들이 포함되어 있습니다. 이러한 값들은 `config` 디렉토리 내의 설정 파일에서 Laravel의 `env` 함수를 통해 읽어 들입니다.

여러 명의 개발자가 협업하는 경우, `.env.example` 파일을 계속해서 포함시키고 업데이트하는 것이 좋습니다. 예제 설정 파일에 예시 값을 넣어두면, 팀원의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수를 명확히 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일의 변수는 서버나 시스템 레벨의 외부 환경 변수로 덮어쓰기(overriding)될 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버마다 다른 환경 구성이 필요할 수 있으므로 소스 컨트롤에 커밋하지 않아야 합니다. 또한 누군가가 소스 저장소에 침입할 경우, 민감한 자격 정보가 노출될 위험이 있기 때문입니다.

하지만, Laravel의 내장된 [환경 파일 암호화](#encrypting-environment-files) 기능을 통해 환경 파일을 암호화하여 안전하게 소스 컨트롤에 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로드하기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 또는 CLI에서 `--env` 인자가 지정되었는지 확인합니다. 만약 지정되었다면, `.env.[APP_ENV]` 파일을 찾고 존재할 경우 이를 로드합니다. 파일이 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 일반적으로 문자열로 파싱됩니다. 하지만, `env()` 함수에서 더 다양한 타입을 반환받을 수 있도록 하기 위해 예약된 값들이 있습니다:

<div class="overflow-auto">

| `.env` 값  | `env()` 값     |
| ---------- | ------------- |
| true       | (bool) true   |
| (true)     | (bool) true   |
| false      | (bool) false  |
| (false)    | (bool) false  |
| empty      | (string) ''   |
| (empty)    | (string) ''   |
| null       | (null) null   |
| (null)     | (null) null   |

</div>

값에 공백이 포함되어야 할 경우, 큰따옴표로 값을 둘러싸서 정의할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 나열된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 하지만, 설정 파일에서는 `env` 함수를 사용하여 이러한 변수의 값을 손쉽게 가져올 수 있습니다. 실제로 Laravel 설정 파일 대부분이 이 함수를 사용하고 있음을 알 수 있습니다:

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수에 전달되는 두 번째 값은 "기본 값"입니다. 해당 키의 환경 변수가 없으면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/{{version}}/facades)의 `environment` 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

`environment` 메서드에 인수를 넘겨, 현재 환경이 지정한 값과 일치하는지 확인할 수도 있습니다. 이 메서드는 주어진 값 중 하나라도 일치하면 `true`를 반환합니다:

```php
if (App::environment('local')) {
    // 현재 환경이 local
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 이거나 staging인 경우...
}
```

> [!NOTE]
> 서버 레벨의 `APP_ENV` 환경 변수를 지정하여 현재 애플리케이션 환경 감지가 덮어써질 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 절대 소스 컨트롤에 저장해서는 안 됩니다. 그러나, Laravel에서는 환경 파일을 암호화하여 애플리케이션의 나머지와 함께 안전하게 소스 컨트롤에 포함시킬 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면, `env:encrypt` 명령어를 사용할 수 있습니다:

```shell
php artisan env:encrypt
```

`env:encrypt` 명령어를 실행하면 `.env` 파일을 암호화하여, 암호화된 내용을 `.env.encrypted` 파일에 저장합니다. 복호화 키는 명령어 실행 결과로 출력되며, 안전한 비밀번호 관리 프로그램에 저장해야 합니다. 직접 암호화 키를 제공하고 싶다면 명령어 실행시 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공한 키의 길이는 사용 중인 암호화 알고리즘이 요구하는 키 길이와 일치해야 합니다. 기본적으로 Laravel은 32자 길이 키가 필요한 `AES-256-CBC` 알고리즘을 사용합니다. `--cipher` 옵션을 사용하여 Laravel의 [encrypter](/docs/{{version}}/encryption)가 지원하는 다른 알고리즘을 활용할 수도 있습니다.

애플리케이션에 `.env`, `.env.staging` 등 여러 환경 파일이 있을 경우 `--env` 옵션으로 암호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령은 복호화 키가 필요하며, Laravel은 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 이 키를 가져옵니다:

```shell
php artisan env:decrypt
```

또는, `--key` 옵션을 통해 키를 직접 명령어에 넘길 수 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면 `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 씁니다.

`--cipher` 옵션을 `env:decrypt` 명령에 제공하여 커스텀 암호화 알고리즘을 사용할 수도 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

애플리케이션에 여러 환경 파일이 있는 경우 `--env` 옵션으로 복호화할 파일을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `env:decrypt` 명령에 `--force` 옵션을 추가하세요:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기

애플리케이션 어디에서나 `Config` 파사드 또는 전역 `config` 함수를 사용해 손쉽게 설정 값에 접근할 수 있습니다. 설정 값은 "도트(dot) 표기법"으로 접근할 수 있으며, 파일명과 옵션명을 포함합니다. 기본 값을 지정할 수도 있으며, 설정 옵션이 존재하지 않을 경우 이 값이 반환됩니다:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없을 경우 기본값을 가져오기...
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중(co-runtime)에 설정 값을 변경하려면, `Config` 파사드의 `set` 메서드나 `config` 함수에 배열을 전달할 수 있습니다:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석을 지원하기 위해, `Config` 파사드는 타입이 지정된 설정 값 조회 메서드도 제공합니다. 조회된 값이 기대한 타입과 일치하지 않으면 예외가 발생합니다:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션의 성능을 높이기 위해, `config:cache` Artisan 명령어를 사용하여 모든 설정 파일을 하나의 파일로 캐싱하는 것이 좋습니다. 이 명령어는 모든 설정 옵션을 하나의 파일로 결합해 프레임워크가 빠르게 로드할 수 있게 합니다.

일반적으로 `php artisan config:cache` 명령은 프로덕션 배포 과정의 일부로 실행해야 합니다. 로컬 개발 단계에서는 설정 값을 자주 변경하게 되므로, 이 명령어를 실행하지 않는 것이 좋습니다.

설정이 캐싱되면 요청이나 Artisan 명령어 실행 시 프레임워크가 `.env` 파일을 로드하지 않습니다. 따라서 `env` 함수는 외부, 시스템 레벨의 환경 변수만 반환하게 됩니다.

이러한 이유로, 애플리케이션의 설정(`config`) 파일 내에서만 `env` 함수를 호출해야 합니다. Laravel의 기본 설정 파일들을 참고하면 많은 예시를 확인할 수 있습니다. 설정 값은 [위에서 설명한 대로](#accessing-configuration-values) 어디서든지 `config` 함수로 읽을 수 있습니다.

캐시된 설정을 지우려면 `config:clear` 명령어를 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령을 실행했다면 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐싱되면 `.env` 파일은 더 이상 로드되지 않으며, 결과적으로 `env` 함수는 외부, 시스템 레벨의 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 게시

대부분의 Laravel 설정 파일들은 이미 애플리케이션의 `config` 디렉토리에 게시되어 있습니다. 그러나 `cors.php`, `view.php` 등 일부 설정 파일은 기본적으로 게시되지 않으며, 대부분의 애플리케이션에서는 수정할 필요가 없기 때문입니다.

하지만, `config:publish` Artisan 명령어를 사용하여 기본적으로 게시되지 않은 설정 파일도 게시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 파일의 `debug` 옵션은 오류 발생 시 사용자에게 얼마나 많은 정보가 표시되는지 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정하세요. 프로덕션에서 `true`로 설정하면 민감한 설정 값이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

애플리케이션이 점검(유지보수) 모드에 들어가면, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 애플리케이션 업데이트 중이나 유지보수 중에 애플리케이션을 "비활성화"하기가 쉬워집니다. 점검 모드 체크는 기본 미들웨어 스택에도 포함되어 있습니다. 만약 애플리케이션이 유지보수 모드라면, `Symfony\Component\HttpKernel\Exception\HttpException`이 503 상태코드와 함께 발생합니다.

점검(유지보수) 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

```shell
php artisan down
```

모든 점검 모드 응답에 `Refresh` HTTP 헤더를 같이 보내고 싶다면, `down` 명령어에 `refresh` 옵션을 줄 수 있습니다. 이 헤더는 브라우저에게 주어진 초 이후 페이지를 자동 새로고침 하도록 지시합니다:

```shell
php artisan down --refresh=15
```

`down` 명령에 `retry` 옵션을 전달하면, `Retry-After` HTTP 헤더의 값으로 설정됩니다. (브라우저는 이 헤더를 일반적으로 무시합니다.)

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검(유지보수) 모드 우회

비밀 토큰을 사용해 점검 모드 우회를 허용하려면, `secret` 옵션으로 우회 토큰을 지정할 수 있습니다:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 점검 모드로 전환한 후, 이 토큰이 포함된 URL로 접속하면 Laravel은 브라우저에 유지보수 모드 우회 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

비밀 토큰 생성을 Laravel에게 맡기고 싶다면, `with-secret` 옵션을 사용할 수 있습니다. 애플리케이션이 유지보수 모드에 들어가면 토큰이 표시됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로에 접근하면 `/` 경로로 리디렉션됩니다. 이 쿠키가 브라우저에 발급되면 애플리케이션을 유지보수 모드가 아닌 것처럼 정상적으로 이용할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰은 알파벳과 숫자, 그리고 필요한 경우 대시(-)를 사용하는 것이 일반적입니다. URL에서 의미 있는 문자(예: `?`, `&`)는 피하세요.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버에서의 점검(유지보수) 모드

Laravel은 기본적으로 파일 기반 시스템으로 점검 모드 여부를 판단합니다. 즉, 각 서버마다 `php artisan down` 명령어를 실행해야 유지보수 모드가 활성화됩니다.

대신, Laravel은 캐시 기반 점검 모드 방법도 제공합니다. 이 방법은 단 한 대의 서버에서만 `php artisan down` 명령을 실행하면 됩니다. 사용을 원한다면 애플리케이션의 `.env` 파일에서 유지보수 모드 변수들을 수정하세요. 모든 서버에서 접근 가능한 캐시 `store`를 선택해야 하며, 이를 통해 각 서버의 점검 모드 상태가 일관되게 유지됩니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 사전 렌더링

배포 중에 `php artisan down` 명령을 사용하는 경우, Composer 의존성 또는 인프라 구성 요소가 갱신되는 도중 사용자가 접속하면 간혹 오류가 발생할 수 있습니다. 이는 Laravel 프레임워크의 상당 부분이 애플리케이션이 점검 모드인지 확인하고 뷰 엔진으로 점검(유지보수) 모드 뷰를 렌더링하기 위해 부팅되어야 하기 때문입니다.

그래서 Laravel은 요청 사이클이 시작되자마자 반환되는 유지보수 모드 뷰를 미리 렌더링할 수 있도록 지원합니다. 이 뷰는 애플리케이션의 종속성이 로드되기 전에 렌더링됩니다. `down` 명령어의 `render` 옵션을 사용하여 원하는 템플릿을 미리 렌더링할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검(유지보수) 모드 요청 리디렉션

점검 모드에서는 사용자가 애플리케이션의 어떤 URL에 접속해도 해당 뷰가 표시됩니다. 모든 요청을 특정 URL로 리디렉션 하고 싶다면, `redirect` 옵션을 사용할 수 있습니다. 예를 들어, 모든 요청을 `/` URI로 리디렉션 할 수 있습니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검(유지보수) 모드 해제

점검(유지보수) 모드를 해제하려면 `up` 명령어를 사용하세요:

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php`에 직접 정의하여 커스터마이즈할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 점검(유지보수) 모드와 큐

애플리케이션이 점검 모드일 때는 [큐 작업](/docs/{{version}}/queues)이 처리되지 않습니다. 점검 모드 해제 시 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검(유지보수) 모드 대안

점검 모드는 애플리케이션이 몇 초간 중단되어야 한다는 단점이 있습니다. 무중단 배포(zero-downtime deploy)를 원한다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 플랫폼을 사용하는 것도 고려할 수 있습니다.