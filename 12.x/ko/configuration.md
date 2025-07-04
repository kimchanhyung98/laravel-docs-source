# 환경설정 (Configuration)

- [소개](#introduction)
- [환경설정 파일 관리](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경설정 값 조회](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 파일 배포](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션들은 문서화가 잘 되어 있으므로, 파일들을 살펴보며 사용 가능한 옵션에 익숙해지면 좋습니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보, 그리고 애플리케이션 URL, 암호화 키와 같은 다양한 주요 설정 값을 쉽게 지정할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

라라벨은 `about` 아티즌 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 정보의 개요를 표시해줍니다.

```shell
php artisan about
```

애플리케이션 개요 출력 중 특정 섹션만 확인하고 싶다면 `--only` 옵션을 이용해 해당 섹션만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 확인하고 싶다면 `config:show` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경설정 파일 관리

애플리케이션이 실행되는 환경에 따라 서로 다른 설정값을 사용하면 매우 편리합니다. 예를 들어, 로컬 환경과 운영 서버에서는 서로 다른 캐시 드라이버를 사용하고 싶을 수 있습니다.

이를 손쉽게 해결하려고, 라라벨은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 라라벨을 새로 설치하면, 애플리케이션의 루트 경로에 `.env.example` 파일이 포함되어 여러 공통 환경 변수를 정의합니다. 라라벨 설치 과정에서 이 파일은 자동으로 `.env` 파일로 복사됩니다.

라라벨의 기본 `.env` 파일에는 로컬 환경/운영 서버 등 환경에 따라 달라질 수 있는 일반적인 설정값이 들어 있습니다. 이 값들은 라라벨의 `env` 함수를 통해 `config` 디렉터리의 설정 파일에서 읽어들입니다.

팀 단위로 개발할 때는 `.env.example` 파일을 애플리케이션에 포함하고 지속적으로 업데이트하는 것이 좋습니다. 예시 환경설정 파일에 기본값(플레이스홀더)을 지정해 두면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수 목록을 쉽게 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일의 모든 변수는 서버나 시스템 레벨 환경 변수 등 외부 환경 변수에 의해 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버 환경마다 서로 다른 설정이 필요하기 때문에, 애플리케이션의 소스 컨트롤(버전 관리)에 커밋하면 안 됩니다. 만약 누군가 소스 저장소 접근 권한을 획득한다면, 민감한 인증 정보가 노출될 수 있으므로 보안상 위험이 크기 때문입니다.

하지만, 라라벨의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 통해 환경 파일을 암호화할 수 있습니다. 암호화된 환경 파일은 안전하게 소스 컨트롤에 올릴 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

라라벨은 애플리케이션의 환경 변수를 로드하기 전에 `APP_ENV` 환경 변수가 외부에서 지정되어 있거나, CLI 명령어에 `--env` 인자가 전달되었는지 확인합니다. 이 경우, 라라벨은 `.env.[APP_ENV]` 파일이 존재하면 그것을 로드합니다. 파일이 없다면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일 내의 모든 변수는 기본적으로 문자열로 처리됩니다. 하지만, `env()` 함수로 더 다양한 타입을 반환할 수 있도록 여러 예약어 값을 지원합니다.

<div class="overflow-auto">

| `.env` 값    | `env()` 결과 값      |
| ------------ | -------------------- |
| true         | (bool) true          |
| (true)       | (bool) true          |
| false        | (bool) false         |
| (false)      | (bool) false         |
| empty        | (string) ''          |
| (empty)      | (string) ''          |
| null         | (null) null          |
| (null)       | (null) null          |

</div>

공백이 포함된 환경 변수 값을 정의하려면 값 전체를 큰따옴표로 감싸면 됩니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경설정 값 조회

`.env` 파일에 정의된 모든 변수들은 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 하지만 설정 파일에서는 라라벨의 `env` 함수를 통해 이 값을 불러올 수 있습니다. 실제로 라라벨의 다양한 설정 파일에서 이 함수가 자주 사용되는 것을 확인할 수 있습니다.

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인자는 "기본값"으로, 해당 키에 대한 환경 변수가 없으면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

애플리케이션의 현재 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값을 `App` [파사드](/docs/12.x/facades)의 `environment` 메서드를 통해 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, `environment` 메서드에 값을 전달하면 현재 환경이 해당 값과 일치하는지 확인할 수 있습니다. 일치하면 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // 현재 환경이 local입니다.
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 또는 staging입니다...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 레벨의 `APP_ENV` 환경 변수로 재정의할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 소스 컨트롤에 보관해서는 안 됩니다. 하지만, 라라벨은 환경 파일을 안전하게 암호화해서 소스 컨트롤에 포함할 수 있도록 해줍니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하면 됩니다.

```shell
php artisan env:encrypt
```

이 명령어로 `.env` 파일이 암호화되어 `.env.encrypted` 파일에 저장됩니다. 복호화 키는 명령어 실행 결과로 표시되며, 반드시 보안성이 높은 패스워드 관리 도구에 저장해야 합니다. 직접 암호화 키를 지정하고 싶다면 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키 길이는 선택한 암호화 알고리즘의 요구사항을 충족해야 합니다. 기본적으로 라라벨은 32자 키가 필요한 `AES-256-CBC` 암호화 방식을 사용합니다. `--cipher` 옵션을 통해 라라벨에서 지원하는 [암호화 방식](/docs/12.x/encryption) 중 원하는 것을 고를 수 있습니다.

`.env` 또는 `.env.staging` 등 여러 환경 파일이 있다면, `--env` 옵션에 환경 이름을 지정하여 암호화 대상 파일을 선택할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키를 필요로 하며, 라라벨은 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 복호화 키를 가져옵니다.

```shell
php artisan env:decrypt
```

혹은, `--key` 옵션으로 복호화 키를 직접 명령어에 전달할 수 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어를 실행하면 `.env.encrypted` 파일의 내용을 복호화해 `.env` 파일에 저장합니다.

`--cipher` 옵션을 함께 사용하면 원하는 암호화 방식을 지정할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

`.env`나 `.env.staging` 등 여러 환경 파일이 있다면, `--env` 옵션에 원하는 환경 이름을 전달하면 해당 파일을 복호화합니다.

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰고 싶을 경우 `--force` 옵션을 추가합니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정값 접근하기

애플리케이션 어디에서나 `Config` 파사드나 전역 `config` 함수를 사용해 설정값을 손쉽게 가져올 수 있습니다. 값은 파일 이름과 옵션명 조합의 "dot(점) 표기법"으로 접근하며, 기본값을 두 번째 인자로 지정하면 해당 옵션이 없을 때 그 값이 반환됩니다.

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정값이 존재하지 않을 때 기본값을 반환...
$value = config('app.timezone', 'Asia/Seoul');
```

런타임에 설정값을 변경하려면 `Config` 파사드의 `set` 메서드를 호출하거나, `config` 함수에 배열을 전달할 수 있습니다.

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석을 지원하기 위해, `Config` 파사드는 타입별로 값을 가져오는 메서드도 제공합니다. 만약 얻어온 설정값의 타입이 기대와 다를 경우 예외가 발생합니다.

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션의 성능을 높이려면 `config:cache` 아티즌 명령어로 모든 설정 파일을 하나로 캐싱하는 것이 좋습니다. 이 명령어는 애플리케이션의 모든 설정 옵션을 하나의 파일로 합쳐서, 프레임워크가 빠르게 불러올 수 있도록 합니다.

일반적으로 이 명령어는 운영 환경 배포 과정에서 실행해야 하며, 로컬 개발 중에는 설정 변경이 자주 발생하므로 사용하지 않는 것이 좋습니다.

설정이 캐싱되면, 애플리케이션의 `.env` 파일은 프레임워크에서 더 이상 로드되지 않습니다. 따라서 `env` 함수는 외부 시스템 환경 변수만 반환합니다.

이러한 이유로, 반드시 애플리케이션 설정 파일(`config` 디렉터리) 내부에서만 `env` 함수를 호출해야 합니다. 실제로 라라벨의 기본 설정 파일을 확인해 보면 많은 예시를 볼 수 있습니다. 그 외의 코드에서는 [위에서 설명한](#accessing-configuration-values) `config` 함수를 통해 어디서든 설정에 접근할 수 있습니다.

캐싱된 설정을 삭제하려면 `config:clear` 명령어를 사용하면 됩니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, 반드시 애플리케이션 설정 파일 내부에서만 `env` 함수를 호출해야 합니다. 설정이 캐싱되면 `.env` 파일이 더 이상 로드되지 않으므로, `env` 함수는 오직 외부 시스템 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 파일 배포

라라벨의 대부분 설정 파일은 이미 애플리케이션의 `config` 디렉터리에 배포되어 있습니다. 하지만 `cors.php`, `view.php` 등 일부 설정 파일은 거의 수정할 일이 없어 기본적으로 배포되지 않습니다.

이런 설정 파일이 필요하다면, 언제든 `config:publish` 아티즌 명령어를 통해 추가로 배포할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 에러가 사용자에게 얼마나 자세히 표시될지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG`를 반드시 `true`로 설정해야 합니다. **운영(프로덕션) 환경에서는 이 값을 항상 `false`로 유지해야 하며, 만약 `true`로 설정하면 민감한 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

애플리케이션이 점검(유지보수) 모드에 들어가면, 모든 요청에서 사용자 정의 뷰가 표시됩니다. 업데이트나 시스템 점검 시 애플리케이션을 "잠시 중단"하기에도 매우 편리합니다. 점검 모드 체크는 기본 미들웨어 스택에 포함되어 있으며, 점검 중이면 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 503 상태 코드와 함께 발생합니다.

점검 모드를 활성화하려면 `down` 아티즌 명령어를 실행합니다.

```shell
php artisan down
```

모든 점검 모드 응답에 `Refresh` HTTP 헤더를 보내고 싶다면, `down` 명령어에 `refresh` 옵션을 추가하세요. 이 헤더는 브라우저가 지정한 시간(초) 이후 페이지를 자동으로 새로 고치도록 안내합니다.

```shell
php artisan down --refresh=15
```

`down` 명령어의 `retry` 옵션을 사용하면, `Retry-After` HTTP 헤더 값을 지정할 수도 있습니다. 하지만 대부분의 브라우저는 이 헤더를 무시합니다.

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회하기

비밀 토큰을 사용해서 점검 모드를 우회하도록 하려면, `secret` 옵션에 우회 토큰을 지정하면 됩니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

점검 모드를 활성화한 후, 이 토큰과 일치하는 애플리케이션 URL로 접속하면 라라벨이 브라우저에 점검 모드 우회 쿠키를 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

비밀 토큰을 라라벨이 자동 생성하도록 하고 싶다면, `with-secret` 옵션을 사용하면 됩니다. 비밀 토큰은 점검 모드로 들어간 후 화면에 표시됩니다.

```shell
php artisan down --with-secret
```

이 숨겨진 경로로 접근하면 `/` 경로로 리다이렉트됩니다. 쿠키가 정상적으로 발급되면, 점검 모드 상태임에도 평소처럼 애플리케이션을 이용할 수 있게 됩니다.

> [!NOTE]
> 점검 모드 우회용 비밀 토큰에는 알파벳, 숫자, 대시(-)만 사용하는 것이 좋으며, URL에서 특별한 의미가 있는 `?`, `&` 등의 문자는 피하는 것이 안전합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버에서 점검 모드 적용

기본적으로 라라벨은 파일 기반 시스템으로 점검 모드 여부를 판단합니다. 즉, 여러 대의 서버에서 모두 `php artisan down` 명령을 실행해야 점검 모드가 적용됩니다.

대신, 캐시 기반 방식으로 점검 모드를 관리할 수도 있습니다. 이 방법은 한 대의 서버에서만 `php artisan down` 명령을 실행하면 됩니다. 먼저 애플리케이션의 `.env`에서 점검 모드 설정 변수를 아래와 같이 지정하세요. 모든 서버에서 접근 가능한 캐시 `store`를 선택하면 점검 모드 상태가 여러 서버 간에 똑같이 적용됩니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 뷰 사전 렌더링

배포 도중 `php artisan down` 명령어를 사용할 때, 사용자가 딱 그 타이밍에 애플리케이션에 접속하면 Composer 의존성이나 인프라가 업데이트되는 사이 에러가 날 수 있습니다. 이는 라라벨 프레임워크가 점검 모드 여부를 판단해 점검 페이지를 표시할 때 일부 의존성 부트 과정이 필요하기 때문입니다.

이를 방지하려고, 라라벨은 요청 처리 초입에서 곧바로 반환할 수 있는 점검 모드 뷰를 미리 렌더링해둘 수 있도록 지원합니다. `down` 명령어의 `render` 옵션으로 원하는 템플릿을 사전 렌더링할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리다이렉트

점검 모드 동안은 어떤 URL로 접근해도 점검 모드 뷰가 표시됩니다. 대신, 원한다면 모든 요청을 특정 URL로 리다이렉트하도록 할 수 있습니다. 예를 들어 모든 요청을 `/`로 리다이렉트하는 방식입니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 해제

점검(유지보수) 모드를 해제하려면 `up` 명령어를 사용하세요.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿을 직접 커스텀하려면 `resources/views/errors/503.blade.php`에 원하는 파일을 생성하시면 됩니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐 작업

애플리케이션이 점검 모드일 때는 [큐 작업](/docs/12.x/queues)이 처리되지 않습니다. 점검 모드가 해제되면 큐가 다시 정상적으로 동작합니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드는 수 초간의 다운타임이 필요하기 때문에, 만약 무중단 배포가 필요하다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 플랫폼에서 애플리케이션을 실행할 것을 고려해 볼 수 있습니다.