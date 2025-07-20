# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정값 접근](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 파일 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검(유지보수) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 설정 옵션에는 설명이 포함되어 있으니, 파일을 직접 열어 다양한 옵션을 살펴보고 익숙해지시기 바랍니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션 URL, 암호화 키 등 다양한 핵심 설정값을 지정할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

라라벨은 `about` 아티즌 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 등에 대한 개요 정보를 표시할 수 있습니다.

```shell
php artisan about
```

애플리케이션 개요 출력 중 특정 섹션만 보고 싶다면 `--only` 옵션을 사용해 해당 부분만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

또한, 특정 설정 파일의 내용을 자세히 확인하려면 `config:show` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 서로 다른 설정값을 사용하는 것이 여러 상황에서 유용할 수 있습니다. 예를 들어, 로컬 환경에서는 운영 서버와는 다른 캐시 드라이버를 사용하고 싶을 때가 있습니다.

이런 요구를 간편하게 처리하기 위해 라라벨은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 라라벨을 새로 설치하면 애플리케이션의 루트 디렉터리에 `.env.example` 파일이 포함되는데, 이 파일에는 자주 사용하는 환경변수들이 정의되어 있습니다. 라라벨 설치 과정에서 이 파일은 자동으로 `.env` 파일로 복사됩니다.

라라벨의 기본 `.env` 파일에는 애플리케이션이 로컬 환경에서 실행되는지, 운영 서버에서 실행되는지에 따라 다를 수 있는 다양한 설정값이 들어 있습니다. 이런 값들은 `config` 디렉터리 내 설정 파일에서 라라벨의 `env` 함수를 통해 읽어올 수 있습니다.

팀 단위로 개발할 때는 `.env.example` 파일을 계속해서 포함시키고 업데이트하는 것이 좋습니다. 예시 설정 파일에 자리를 표시하는 값(placeholder)를 넣어두면, 팀 내 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수 목록을 쉽게 파악할 수 있습니다.

> [!NOTE]
> `.env` 파일에 정의된 어떤 변수도 서버 또는 시스템 레벨 환경 변수와 같은 외부 환경 변수로 언제든지 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버마다 서로 다른 환경 구성이 필요하기 때문에 소스 제어에 커밋해서는 안 됩니다. 또한, 만약 악의적인 침입자가 소스 코드 저장소에 접근하게 된다면 민감한 정보가 노출될 수 있어서 보안상 위험합니다.

하지만, 라라벨의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 이용하면 환경 파일의 암호화를 할 수 있습니다. 암호화된 환경 파일은 비교적 안전하게 소스 제어에 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로드하기 전에, 라라벨은 `APP_ENV` 환경 변수가 외부에서 제공되었는지, 또는 CLI 인자로 `--env` 옵션이 지정되었는지 먼저 확인합니다. 해당하는 경우, `.env.[APP_ENV]` 형식의 파일이 있으면 이를 우선 불러옵니다. 만약 해당 파일이 없으면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일에 정의된 모든 변수들은 기본적으로 문자열로 파싱됩니다. 하지만, `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 예약값들이 만들어져 있습니다.

<div class="overflow-auto">

| `.env` 값    | `env()` 값        |
| ------------ | -------------    |
| true         | (bool) true      |
| (true)       | (bool) true      |
| false        | (bool) false     |
| (false)      | (bool) false     |
| empty        | (string) ''      |
| (empty)      | (string) ''      |
| null         | (null) null      |
| (null)       | (null) null      |

</div>

공백이 포함된 값을 환경 변수에 정의해야 할 때는 값을 큰따옴표로 감싸서 지정할 수 있습니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정값 가져오기

`.env` 파일에 나열된 모든 변수들은 애플리케이션이 요청을 받으면 PHP의 `$_ENV` 슈퍼글로벌(전역 변수)에 자동으로 로드됩니다. 이 변수들의 값은 설정 파일에서 `env` 함수를 사용해 가져올 수 있습니다. 실제로 라라벨의 기본 설정 파일을 보면 다양한 옵션에서 이미 이 함수를 사용하고 있습니다.

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인자는 "기본값"이며, 지정한 키에 대한 환경 변수가 존재하지 않을 경우 해당 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/12.x/facades)의 `environment` 메서드를 통해 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

이 메서드에 인자를 전달하면 현재 환경이 주어진 값과 일치하는지 확인할 수도 있습니다. 해당 환경 중 하나와 맞으면 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // 환경이 local일 때
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 또는 staging일 때...
}
```

> [!NOTE]
> 현재 애플리케이션 환경값은 서버 레벨의 `APP_ENV` 환경 변수로 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 절대 소스 제어에 저장해서는 안 됩니다. 그러나 라라벨에서는 환경 파일을 암호화해서 애플리케이션과 함께 안전하게 소스 제어에 추가할 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용합니다.

```shell
php artisan env:encrypt
```

이 명령어를 실행하면 `.env` 파일이 암호화되어 그 결과가 `.env.encrypted` 파일로 저장됩니다. 복호화에 필요한 키는 명령어 실행 결과에 표시되며, 반드시 안전한 비밀번호 관리자에 보관해야 합니다. 만약 자체적으로 암호화 키를 지정하고 싶다면 명령어 실행 시 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키의 길이는 사용하는 암호화 알고리즘에서 요구하는 길이와 일치해야 합니다. 기본적으로 라라벨은 `AES-256-CBC` 알고리즘을 사용하므로 32자의 키가 필요합니다. 명령어 실행 시 `--cipher` 옵션을 통해 라라벨의 [encrypter](/docs/12.x/encryption)가 지원하는 다른 알고리즘을 사용할 수도 있습니다.

애플리케이션에 여러 환경 파일(예: `.env`, `.env.staging`)이 있다면, `--env` 옵션을 통해 암호화할 파일의 환경 이름을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 복호화 키가 필요한데, 라라벨은 기본적으로 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 키를 읽어옵니다.

```shell
php artisan env:decrypt
```

또는, 키를 명령어에 직접 `--key` 옵션으로 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면, `.env.encrypted` 파일의 내용이 복호화되어 `.env` 파일로 저장됩니다.

맞춤 암호화 알고리즘을 사용하려면 `env:decrypt` 명령어에 `--cipher` 옵션을 함께 사용할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일이 존재하는 경우, `--env` 옵션을 통해 복호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면, `env:decrypt` 명령어에 `--force` 옵션을 추가하면 됩니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정값 접근

애플리케이션 어디에서든 `Config` 파사드 또는 전역 함수 `config`를 사용해 각종 설정값을 쉽게 가져올 수 있습니다. 파일명과 옵션명을 점(`.`)으로 이어붙인 "dot" 문법을 통해 설정값에 접근할 수 있습니다. 특정 설정값이 없을 때 반환할 기본값도 지정 가능합니다.

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정값이 없을 경우 기본값 반환...
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중에 설정값을 변경하고 싶다면, `Config` 파사드의 `set` 메서드를 호출하거나, 배열을 전역 `config` 함수에 전달하면 됩니다.

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석(static analysis)에 도움을 주기 위해, `Config` 파사드에서는 타입이 지정된 설정값 반환 메서드도 제공합니다. 반환된 값의 타입이 예상 타입과 다를 경우 예외가 발생합니다.

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

애플리케이션의 성능을 높이기 위해, 모든 설정 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` 아티즌 명령어를 사용합니다. 이 명령어는 모든 설정 옵션을 하나의 파일로 통합해 프레임워크가 빠르게 불러올 수 있도록 합니다.

운영 환경 배포 프로세스 중에 `php artisan config:cache` 명령어를 실행하는 것이 일반적입니다. 개발 환경에서는 애플리케이션을 개발하며 설정값을 자주 변경할 수 있기 때문에 이 명령어를 사용하지 않는 것이 좋습니다.

설정이 캐시되면, 애플리케이션의 `.env` 파일은 요청이나 아티즌 명령 실행 시 프레임워크에서 더 이상 로드되지 않습니다. 따라서 `env` 함수는 외부, 즉 시스템 레벨 환경 변수만 반환하게 됩니다.

이런 이유로, 반드시 애플리케이션의 설정(`config`) 파일 내에서만 `env` 함수를 호출해야 합니다. 실제 예는 라라벨 기본 설정 파일에서 확인할 수 있습니다. 그리고 애플리케이션 전체에서는 `config` 함수를 이용해 원하는 설정값에 접근할 수 있습니다. (자세한 방법은 위 [설정값 접근](#accessing-configuration-values) 참고)

설정 캐시를 삭제하려면 `config:clear` 명령어를 사용하면 됩니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 프로세스에서 `config:cache` 명령어를 사용한다면, 반드시 설정 파일(`config` 폴더) 외의 위치에서는 `env` 함수를 호출하지 않아야 합니다. 설정이 캐시되면 `.env` 파일은 로드되지 않으므로, `env` 함수는 오직 외부(시스템) 레벨 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 파일 퍼블리싱

라라벨의 대부분 설정 파일은 애플리케이션의 `config` 폴더에 이미 퍼블리시되어 있습니다. 하지만, `cors.php`, `view.php`와 같은 일부 설정 파일은 기본적으로 퍼블리시되지 않습니다. 대부분의 애플리케이션은 이 파일들을 수정할 필요가 없기 때문입니다.

필요한 경우, 퍼블리시되지 않은 설정 파일도 `config:publish` 아티즌 명령어로 손쉽게 추가(퍼블리싱)할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 어떤 정보까지 표시할지를 결정합니다. 기본적으로 이 값은 `.env` 파일의 `APP_DEBUG` 환경 변수값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 반드시 이 값을 `false`로 설정해야 하며, 그렇지 않을 경우 민감한 설정값이 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(유지보수) 모드

애플리케이션이 점검(유지보수) 모드일 때는, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 이용하면 앱을 업데이트하거나 유지보수 작업을 수행할 때 애플리케이션을 쉽게 "비활성화"할 수 있습니다. 애플리케이션의 기본 미들웨어 스택에는 점검 모드 체크가 포함되어 있습니다. 점검 모드에서는 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 503 상태코드로 발생합니다.

점검 모드를 활성화하려면 `down` 아티즌 명령어를 실행합니다.

```shell
php artisan down
```

모든 점검 모드 응답에 `Refresh` HTTP 헤더를 포함시키려면, `down` 명령어에 `refresh` 옵션을 지정할 수 있습니다. 이 헤더 값은 사용자의 브라우저에서 지정한 초(seconds)만큼 후에 자동으로 페이지를 새로고침하도록 안내합니다.

```shell
php artisan down --refresh=15
```

또한, `down` 명령어에 `retry` 옵션을 지정하면, `Retry-After` HTTP 헤더값이 설정됩니다(대부분의 브라우저는 이 헤더를 무시합니다).

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

비밀 토큰을 이용해 점검 모드를 우회하고 싶다면, `secret` 옵션으로 우회 토큰을 직접 설정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

점검 모드로 전환한 뒤, 해당 토큰이 포함된 URL로 접속하면 라라벨에서 브라우저에 점검 모드 우회 쿠키를 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

라라벨에서 직접 비밀 토큰을 생성해 주길 원한다면 `with-secret` 옵션을 사용할 수 있습니다. 애플리케이션이 점검 모드가 되면 비밀 토큰이 표시됩니다.

```shell
php artisan down --with-secret
```

이 숨겨진 경로로 접근하면 애플리케이션의 `/` 경로로 리디렉션됩니다. 쿠키가 발급되면 사용자는 점검 모드 중에도 애플리케이션을 평소처럼 이용할 수 있습니다.

> [!NOTE]
> 점검 모드 비밀번호(시크릿)는 일반적으로 영문자와 숫자, 그리고 선택적으로 대시(-)만 포함하는 것이 좋습니다. URL에서 특별한 의미를 가지는 문자(`?`, `&` 등)는 사용을 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버에서의 점검 모드

기본적으로, 라라벨은 파일 기반 방식으로 점검 모드 상태를 관리합니다. 즉, 각 서버마다 `php artisan down` 명령을 개별 실행해야 점검 모드가 활성화됩니다.

대신, 캐시 기반 방식을 사용하면 여러 서버에서 일관되게 점검 모드를 적용할 수 있습니다. 이 방법을 사용하려면 `.env` 파일에 점검 모드 관련 변수를 추가해주세요. 그리고 모든 서버에서 접근 가능한 캐시 `store`를 지정해야 각 서버가 점검 상태를 정확하게 공유할 수 있습니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 사전 렌더링

배포 작업 중 `php artisan down` 명령을 사용하면, 사용자가 Composer 의존성이나 인프라가 업데이트되는 시점에 애플리케이션에 접속할 경우 간헐적으로 에러가 발생할 수 있습니다. 이는 라라벨이 점검 모드 여부를 판단하고 뷰를 렌더링하기 위해 프레임워크 핵심을 부팅해야하기 때문입니다.

이런 문제를 방지하기 위해, 라라벨은 ‘요청 사이클의 가장 초반’에 반환되는 점검 모드 뷰를 사전 렌더링할 수 있게 지원합니다. 원하는 뷰 템플릿을 `down` 명령의 `render` 옵션으로 미리 렌더링할 수 있습니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리다이렉트

점검 모드 상태에서는 모든 경로에 대해 점검용 뷰가 렌더링됩니다. 만약 모든 요청을 특정 URL로 리다이렉트하고 싶다면 `redirect` 옵션을 사용할 수 있습니다. 예를 들어 모든 요청을 `/` URI로 리다이렉트하려면 다음 명령어를 실행합니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 해제

점검 모드를 해제하려면 `up` 명령어를 사용합니다.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿을 커스텀하고 싶다면 `resources/views/errors/503.blade.php` 경로에 직접 템플릿을 정의하면 됩니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐

애플리케이션이 점검 모드일 때는 [큐에 등록된 작업](/docs/12.x/queues)이 실행되지 않습니다. 점검 모드가 해제되면 작업 처리는 정상적으로 다시 진행됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드를 사용하면 애플리케이션에 수 초간의 다운타임이 발생할 수 있습니다. 만약 다운타임 없는 무중단 배포가 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 완전관리형 플랫폼에서 애플리케이션을 운영하는 것도 고려해볼 수 있습니다.
