# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수의 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 파일 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에는 상세한 문서가 작성되어 있으니, 파일들을 살펴보면서 어떤 옵션들이 있는지 익숙해지시기 바랍니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보, 애플리케이션 URL, 암호화 키 등 애플리케이션의 핵심 설정 값을 구성할 수 있게 도와줍니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요 정보를 표시할 수 있습니다.

```shell
php artisan about
```

특정 섹션에만 관심이 있다면, `--only` 옵션으로 해당 부분만 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 탐색하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 갖는 것이 유용한 경우가 많습니다. 예를 들어, 로컬 환경과 프로덕션 서버에서 서로 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

이런 과정이 쉬워지도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로 설치된 Laravel에서는 애플리케이션의 루트 디렉터리에 많은 공통 환경 변수들이 정의된 `.env.example` 파일이 포함되어 있습니다. Laravel 설치 과정에서 이 파일이 `.env` 파일로 자동 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬에서 실행 중인지, 프로덕션 웹 서버에서 실행 중인지에 따라 달라질 수 있는 여러 설정 값이 들어 있습니다. 이 값들은 `config` 디렉터리 내의 설정 파일에서 Laravel의 `env` 함수를 통해 읽어들입니다.

팀 프로젝트를 개발 중이라면, `.env.example` 파일을 계속 포함시키고 업데이트하면서 사용하는 것이 좋습니다. 예제 파일에 플레이스홀더 값을 넣어두면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수가 무엇인지 쉽게 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일에 있는 어떤 변수든, 서버 혹은 시스템 레벨의 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버마다 서로 다른 환경 구성이 필요할 수 있으므로 소스 컨트롤에 커밋해서는 안 됩니다. 또한 누군가 소스 컨트롤 저장소에 접근할 경우, 민감한 자격 증명이 노출될 수 있어 보안상 위험합니다.

하지만, Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 사용하면 환경 파일을 안전하게 암호화한 뒤 소스 컨트롤에 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 불러오기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었거나 `--env` CLI 옵션이 지정되었는지 확인합니다. 만약 그렇다면, Laravel은 해당 이름의 `.env.[APP_ENV]` 파일이 있을 경우 먼저 그것을 불러오려 시도합니다. 파일이 없을 경우에는 기본 `.env` 파일을 불러옵니다.

<a name="environment-variable-types"></a>
### 환경 변수의 타입

`.env` 파일의 모든 변수는 기본적으로 문자열로 파싱됩니다. 하지만 `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 아래와 같이 예약된 값들이 마련되어 있습니다:

<div class="overflow-auto">

| `.env` 값    | `env()` 반환 값    |
| ------------ | ------------------ |
| true         | (bool) true        |
| (true)       | (bool) true        |
| false        | (bool) false       |
| (false)      | (bool) false       |
| empty        | (string) ''        |
| (empty)      | (string) ''        |
| null         | (null) null        |
| (null)       | (null) null        |

</div>

값에 공백이 포함되어야 한다면, 큰따옴표로 값을 감싸서 정의할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 나열된 모든 변수는, 애플리케이션이 요청을 수신할 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 하지만 설정 파일 내에서는 `env` 함수를 사용하여 해당 변수 값을 불러올 수 있습니다. 실제로 Laravel의 설정 파일을 살펴보면, 많은 옵션이 이미 이 함수를 사용하고 있음을 볼 수 있습니다:

```php
'debug' => (bool) env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인수는 "기본값"으로, 해당 키에 대한 환경 변수가 존재하지 않을 때 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인

현재 애플리케이션 환경은 `.env` 파일 내의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/12.x/facades)의 `environment` 메서드를 통해 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

`environment` 메서드에 인수를 전달하여, 현재 환경이 해당 값과 일치하는지 확인할 수도 있습니다. 이때, 일치한다면 `true`를 반환합니다:

```php
if (App::environment('local')) {
    // 환경이 local입니다.
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 또는 staging입니다...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 레벨에서 `APP_ENV` 환경 변수를 정의하여 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 절대 소스 컨트롤에 저장해서는 안 됩니다. 하지만, Laravel에서는 환경 파일을 암호화하여, 애플리케이션의 다른 소스와 함께 소스 컨트롤에 안전하게 추가할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하면 됩니다:

```shell
php artisan env:encrypt
```

`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화 키는 명령어 실행 결과로 출력되며, 반드시 안전한 비밀번호 관리 도구에 저장해야 합니다. 직접 암호화 키를 지정하려면 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키의 길이는 사용 중인 암호화 알고리즘(cipher)의 요구사항을 만족해야 합니다. 기본적으로 Laravel은 `AES-256-CBC` cipher를 사용하며, 32자 길이의 키가 필요합니다. `--cipher` 옵션을 사용하면 Laravel의 [encrypter](/docs/12.x/encryption)에서 지원하는 어떤 cipher도 사용할 수 있습니다.

애플리케이션에 여러 환경 파일이 있는 경우(예: `.env`, `.env.staging` 등), `--env` 옵션으로 암호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 가져옵니다:

```shell
php artisan env:decrypt
```

또는, `--key` 옵션을 사용하여 키를 직접 명령어에 전달할 수 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면 Laravel은 `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장합니다.

커스텀 암호화 알고리즘을 사용하려면, `env:decrypt` 명령어에 `--cipher` 옵션을 추가할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일이 있다면, 복호화할 환경 파일을 `--env` 옵션으로 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면, `--force` 옵션을 추가해 실행하면 됩니다:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근 (Accessing Configuration Values)

애플리케이션 어디에서나 `Config` 파사드 또는 전역 `config` 함수를 사용해 손쉽게 설정 값에 접근할 수 있습니다. 접근할 때는 "점(dot) 표기법"을 사용하는데, 여기에는 파일명과 옵션명이 포함됩니다. 또한, 설정 값이 없을 경우 반환할 기본값도 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없을 때 기본 값 반환...
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중에 설정 값을 변경하려면, `Config` 파사드의 `set` 메서드를 호출하거나, 배열을 `config` 함수에 전달할 수 있습니다:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석 도구의 활용을 돕기 위해, `Config` 파사드는 타입을 명시하는 설정 값 반환 메서드도 제공합니다. 기대하는 타입과 설정 값이 일치하지 않으면 예외가 발생합니다:

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

애플리케이션의 속도를 높이기 위해 `config:cache` Artisan 명령어를 사용해 모든 설정 파일을 하나의 파일로 캐시할 수 있습니다. 이 명령어는 애플리케이션의 모든 설정 옵션을 한 파일에 모아, 프레임워크가 빠르게 로드할 수 있도록 해줍니다.

일반적으로 프로덕션 배포 과정에서 `php artisan config:cache` 명령어를 실행해야 합니다. 로컬 개발 중에는 설정이 자주 바뀌므로 이 명령어를 실행하지 않아야 합니다.

설정이 캐시되고 나면, 요청이나 Artisan 명령어 실행 시 프레임워크에서 더 이상 `.env` 파일을 로드하지 않습니다. 따라서 `env` 함수는 외부, 즉 시스템 레벨의 환경 변수만 반환하게 됩니다.

이런 이유로, 반드시 `env` 함수는 애플리케이션 설정(`config`) 파일 내에서만 호출해야 합니다. Laravel의 기본 설정 파일을 참고하면 이러한 사용 사례를 많이 볼 수 있습니다. 설정 값은 애플리케이션 어디에서든 [위에서 설명한](#accessing-configuration-values) `config` 함수를 사용해 접근할 수 있습니다.

캐시된 설정을 삭제하려면 `config:clear` 명령어를 사용하면 됩니다:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행할 때는, 반드시 `env` 함수를 설정 파일 내에서만 사용하도록 해야 합니다. 설정이 캐시되면 더 이상 `.env` 파일이 로드되지 않으므로, `env` 함수는 시스템 레벨 환경 변수만 반환하게 됩니다.

<a name="configuration-publishing"></a>
## 설정 파일 퍼블리싱 (Configuration Publishing)

Laravel의 대부분 설정 파일은 이미 애플리케이션의 `config` 디렉터리에 퍼블리시되어 있습니다. 하지만 `cors.php`, `view.php`와 같은 일부 설정 파일은 대부분의 애플리케이션에서 수정이 필요하지 않으므로 기본적으로 퍼블리싱되어 있지 않습니다.

하지만, `config:publish` Artisan 명령어를 사용하면 기본적으로 퍼블리시되지 않은 설정 파일도 퍼블리시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일에 있는 `debug` 옵션은 사용자에게 실제로 얼마나 많은 오류 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 시에는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 프로덕션에서 `true`로 두면, 민감한 설정 값이 사용자에게 노출될 수 있으니 주의하십시오.**

<a name="maintenance-mode"></a>
## 점검 모드 (Maintenance Mode)

애플리케이션이 점검 모드에 들어가면, 사용자가 모든 요청을 보낼 때 커스텀 뷰가 표시됩니다. 이를 통해 애플리케이션을 쉽게 "비활성화"시켜, 업데이트 또는 점검 작업을 수행하는 동안 사용자 접근을 차단할 수 있습니다. 애플리케이션의 기본 미들웨어 스택에는 점검 모드 체크가 포함되어 있습니다. 점검 모드일 경우, `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태 코드로 발생합니다.

점검 모드를 활성화하려면, 다음과 같이 `down` Artisan 명령어를 실행하면 됩니다:

```shell
php artisan down
```

모든 점검 모드 응답에 `Refresh` HTTP 헤더를 포함하고 싶다면, `down` 명령어 실행 시 `refresh` 옵션을 제공할 수 있습니다. `Refresh` 헤더는 지정한 초 후에 브라우저가 자동으로 페이지를 새로고침하도록 안내합니다:

```shell
php artisan down --refresh=15
```

`down` 명령어에 `retry` 옵션을 제공하면 `Retry-After` HTTP 헤더에 해당 값이 지정됩니다. 하지만, 대부분의 브라우저는 이 헤더를 무시합니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

비밀 토큰을 사용하여 점검 모드를 우회할 수 있도록 하려면, `secret` 옵션으로 우회용 토큰을 지정할 수 있습니다:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 점검 모드에 두고 이후 해당 토큰이 포함된 URL로 접근하면, Laravel이 브라우저에 점검 모드 우회 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 자동 생성하도록 하려면, `with-secret` 옵션을 사용하면 됩니다. 점검 모드가 활성화되면 토큰이 표시됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로로 접근하면, 이후 `/` 경로로 리다이렉트됩니다. 쿠키가 브라우저에 발급된 뒤에는 점검 모드가 아닌 것처럼 애플리케이션을 정상적으로 이용할 수 있습니다.

> [!NOTE]
> 점검 모드 비밀 토큰에는 일반적으로 영문/숫자 및 선택적으로 하이픈(-)을 사용하는 것이 좋습니다. URL에서 특수한 의미가 있는 `?`, `&` 등의 문자는 사용을 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 여러 서버에서의 점검 모드

기본적으로 Laravel은 파일 기반 방식으로 점검 모드 여부를 판단합니다. 이 방식에서는 애플리케이션을 호스팅하는 각 서버마다 `php artisan down` 명령어를 실행해야 합니다.

대안으로, Laravel은 캐시 기반 점검 모드 방법도 제공합니다. 이 방법에서는 한 서버에서만 `php artisan down` 명령어를 실행하면 됩니다. 이를 사용하려면, 애플리케이션의 `.env` 파일에서 점검 모드 관련 변수를 아래와 같이 수정합니다. 모든 서버가 접근할 수 있는 캐시 `store`를 선택해야 하며, 이를 통해 여러 서버에서 점검 모드 상태를 일관적으로 유지할 수 있습니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 미리 렌더링

배포(Deployment) 과정에서 `php artisan down` 명령어를 사용할 경우, 사용자들이 Composer 의존성이나 기타 인프라가 업데이트되는 중 애플리케이션에 접근하게 되면 가끔 오류를 마주할 수 있습니다. 이는 점검 모드임을 판단하고 점검 모드 뷰를 렌더링하기 위해 Laravel 프레임워크의 많은 부분이 부트되어야 하기 때문입니다.

이런 상황을 예방하기 위해, Laravel은 요청 사이클의 가장 초기에 반환되는 점검 모드 뷰를 미리 렌더링할 수 있습니다. 이 뷰는 애플리케이션의 의존성이 로드되기 전에 렌더링됩니다. `down` 명령어의 `render` 옵션을 사용해 원하는 템플릿을 미리 렌더링할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리다이렉트

점검 모드에서는 사용자가 접근하고자 하는 모든 애플리케이션 URL에 대해 점검 모드 뷰가 표시됩니다. 필요하다면 이 때 Laravel이 모든 요청을 특정 URL로 리다이렉트하도록 할 수도 있습니다. 이를 위해 `redirect` 옵션을 사용할 수 있습니다. 예를 들어 모든 요청을 `/` URI로 리다이렉트하려면 아래와 같이 실행합니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 해제

점검 모드를 해제하려면, `up` 명령어를 사용합니다:

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿을 커스텀하려면, `resources/views/errors/503.blade.php`에 직접 템플릿을 정의하면 됩니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐(Queue)

애플리케이션이 점검 모드일 때는, 어떤 [큐 작업](/docs/12.x/queues)도 처리되지 않습니다. 점검 모드를 빠져나오면 작업이 정상적으로 이어서 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드가 몇 초간의 다운타임을 수반한다는 점을 고려해, 완전관리형 플랫폼에서 애플리케이션을 운영하는 것도 한 방법입니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 이용하면, 다운타임 없이 배포(zero-downtime deployment)가 가능합니다.
