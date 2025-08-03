# 환경 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화하기](#encrypting-environment-files)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 환경 설정 파일은 `config` 디렉토리에 저장되어 있습니다. 각각의 옵션에는 문서가 포함되어 있으므로, 파일을 살펴보며 사용 가능한 옵션에 익숙해져도 좋습니다.

이 설정 파일들은 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션 URL, 암호화 키와 같은 여러 핵심 설정 값을 구성할 수 있게 해줍니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경 개요를 출력할 수 있습니다.

```shell
php artisan about
```

출력되는 애플리케이션 개요 중 특정 부분만 보고 싶다면 `--only` 옵션을 사용해 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는 특정 설정 파일의 값을 자세히 탐색하려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 종종 유용합니다. 예를 들어, 로컬 개발 환경에서는 프로덕션 서버와는 다른 캐시 드라이버를 사용하고자 할 수 있습니다.

이를 쉽게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로 설치한 Laravel 애플리케이션의 루트 디렉토리에는 `.env.example` 파일이 포함되어 있는데, 이 파일은 여러 공통 환경 변수를 정의합니다. Laravel 설치 과정에서 이 파일이 자동으로 `.env`로 복사됩니다.

Laravel 기본 `.env` 파일에는 로컬 또는 프로덕션 웹 서버에서 실행할 때 달라질 수 있는 여러 공통 설정 값이 포함되어 있습니다. 이 값들은 `config` 디렉토리 내 설정 파일에서 Laravel의 `env` 함수를 통해 읽혀집니다.

팀 개발 시에는 `.env.example` 파일을 계속 포함하여 업데이트하는 것이 좋습니다. 이 파일에 플레이스홀더 값을 넣으면, 팀원들이 애플리케이션 실행에 필요한 환경 변수를 명확히 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일 내 변수는 서버나 시스템 수준 외부 환경 변수로 언제든지 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자 및 서버마다 환경 구성이 달라지기 때문에 소스 제어에 커밋해서는 안 됩니다. 또한 만약 악의적인 사용자가 소스 제어 저장소에 접근하게 되면 중요한 인증 정보가 노출되는 보안 위험이 있습니다.

하지만 Laravel의 내장 [환경 암호화](#encrypting-environment-files) 기능을 이용하면 환경 파일을 암호화해서 소스 제어에 안전하게 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션이 환경 변수를 로드하기 전에, Laravel은 외부에서 제공된 `APP_ENV` 환경 변수나 `--env` CLI 인자가 있는지 확인합니다. 있다면 `.env.[APP_ENV]` 파일을 찾고, 존재하면 해당 파일을 로드합니다. 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일 안의 모든 변수는 기본적으로 문자열로 파싱됩니다. 하지만 `env()` 함수에서 좀 더 다양한 타입을 반환할 수 있도록 몇 가지 예약값이 정의되어 있습니다:

<div class="overflow-auto">

| `.env` 값  | `env()` 반환 값  |
| ---------- | --------------- |
| true       | (bool) true     |
| (true)     | (bool) true     |
| false      | (bool) false    |
| (false)    | (bool) false    |
| empty      | (string) ''     |
| (empty)    | (string) ''     |
| null       | (null) null     |
| (null)     | (null) null     |

</div>

만약 공백이 포함된 환경 변수를 정의하려면, 값 전체를 큰따옴표로 감싸면 됩니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 나열된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 하지만 설정 파일 내에서는 `env` 함수를 사용해 이 값을 가져올 수 있습니다. Laravel 기본 설정 파일을 보면 많은 옵션들이 이미 이 함수를 활용하고 있음을 알 수 있습니다:

```php
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인자는 "기본값"입니다. 지정한 환경 변수가 없으면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. `App` [퍼사드](/docs/master/facades)의 `environment` 메서드를 이용해 이 값을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, `environment` 메서드에 인수를 전달해 현재 환경이 주어진 값과 일치하는지 확인할 수 있습니다. 이 메서드는 전달받은 값 중 하나와 환경이 일치하면 `true`를 반환합니다:

```php
if (App::environment('local')) {
    // 환경이 local입니다.
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 또는 staging 중 하나입니다.
}
```

> [!NOTE]
> 서버 수준의 `APP_ENV` 환경 변수를 정의하면 현재 환경 감지를 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화하기

암호화되지 않은 환경 파일은 소스 제어에 저장해서는 안 됩니다. 하지만 Laravel에서는 환경 파일을 암호화해서 애플리케이션과 함께 안전하게 소스 제어에 포함할 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하세요:

```shell
php artisan env:encrypt
```

이 명령어는 `.env` 파일을 암호화하여 `.env.encrypted` 파일로 저장합니다. 복호화 키가 명령어 실행 결과에 출력되니, 안전한 비밀번호 관리자에 보관해야 합니다. 직접 암호화 키를 지정하려면 `--key` 옵션을 사용하세요:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 키 길이는 사용하는 암호화 방식에 맞춰야 합니다. 기본적으로 Laravel은 32자 길이 키가 필요한 `AES-256-CBC` 방식을 사용합니다. `--cipher` 옵션을 통해 Laravel에서 지원하는 다른 암호화 방식을 지정할 수도 있습니다.

만약 `.env` 외에 `.env.staging` 같은 여러 환경 파일이 있다면, `--env` 옵션을 통해 특정 환경 파일을 암호화할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일 복호화는 `env:decrypt` 명령어를 사용합니다. 이 명령어는 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 복호화 키를 가져옵니다:

```shell
php artisan env:decrypt
```

또는 `--key` 옵션으로 직접 키를 제공할 수도 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

실행 시 Laravel은 `.env.encrypted` 파일 내용을 복호화하여 `.env` 파일로 저장합니다.

사용자 지정 암호화 방식을 사용하려면 `--cipher` 옵션도 지정할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

멀티 환경 파일 중 복호화할 파일을 지정하려면 아래와 같이 `--env` 옵션을 사용하세요:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가하십시오:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기

애플리케이션 어디서나 `Config` 퍼사드 또는 전역 함수 `config`를 사용해 설정 값을 쉽게 가져올 수 있습니다. 설정 값은 "도트 표기법"으로 파일 이름과 옵션 이름을 점으로 구분하여 접근합니다. 기본값도 지정할 수 있으며, 설정 옵션이 없을 경우 이 기본값이 반환됩니다:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없으면 기본값 반환
$value = config('app.timezone', 'Asia/Seoul');
```

런타임 중에 설정 값을 변경하려면 `Config` 퍼사드의 `set` 메서드나 `config` 함수에 배열을 전달합니다:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석에 도움이 되도록, `Config` 퍼사드는 타입이 지정된 설정 조회 메서드도 제공합니다. 반환 값이 기대한 타입과 다르면 예외가 발생합니다:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱

애플리케이션 속도를 높이려면 `config:cache` Artisan 명령어를 이용해 모든 설정 파일을 하나의 파일로 캐싱하는 것이 좋습니다. 이 명령어는 앱의 설정 옵션들을 하나의 파일로 합쳐서 프레임워크가 빠르게 불러올 수 있게 만듭니다.

보통 `php artisan config:cache` 명령은 프로덕션 배포 과정에서 실행하는 것이 권장됩니다. 개발 중에는 설정 값을 자주 변경해야 하므로 실행하지 않는 것이 좋습니다.

캐싱 후에는 애플리케이션 요청이나 Artisan 명령 실행 시 `.env` 파일이 로드되지 않습니다. 따라서 `env` 함수는 외부 시스템 레벨 환경 변수만 반환합니다.

때문에 `env` 함수 호출은 반드시 애플리케이션의 설정 (`config`) 파일 내에서만 해야 합니다. Laravel의 기본 설정 파일을 보면 이 원리가 잘 적용되어 있습니다. 설정 값은 애플리케이션 어디서나 위에서 설명한 `config` 함수를 통해 얻을 수 있습니다.

캐시된 설정을 제거하려면 `config:clear` 명령어를 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행할 경우, `env` 함수가 반드시 설정 파일 내에서만 호출되고 있는지 확인해야 합니다. 캐싱 후에는 `.env` 파일이 로드되지 않아 `env` 함수는 외부 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 퍼블리싱

대부분의 Laravel 설정 파일은 이미 애플리케이션의 `config` 디렉토리에 퍼블리시되어 있습니다. 다만 `cors.php`, `view.php` 같은 몇몇 파일은 기본적으로 퍼블리시되지 않는데, 이는 대부분의 애플리케이션에서 수정할 필요가 없기 때문입니다.

필요한 경우 `config:publish` Artisan 명령어를 사용해 기본 퍼블리시되지 않은 설정 파일들을 퍼블리시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 설정 파일 내 `debug` 옵션은 에러에 관한 정보를 얼마나 사용자에게 보여줄지 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 값을 `true`로 설정해야 합니다. **하지만 프로덕션 환경에서는 반드시 `false`로 설정해야 하며, 만약 프로덕션 환경에서 `true`로 설정되어 있으면 중요한 설정 값이 외부 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지보수 모드

애플리케이션이 유지보수 모드에 들어가면, 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 애플리케이션을 임시로 "비활성화"하고 업데이트하거나 유지보수를 수행할 수 있습니다. 유지보수 모드 검사는 기본 미들웨어 스택에 포함되어 있으며, 모드 중일 때 `Symfony\Component\HttpKernel\Exception\HttpException` 상태 코드 503 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

```shell
php artisan down
```

모든 유지보수 응답에 `Refresh` HTTP 헤더를 보내서 지정된 초가 지나면 자동으로 페이지를 새로고침하도록 하려면, `down` 명령에 `--refresh` 옵션을 추가하세요:

```shell
php artisan down --refresh=15
```

또한 `retry` 옵션을 지정할 수 있는데, 이 값은 `Retry-After` HTTP 헤더로 설정되지만 보통 브라우저에서는 무시합니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회하기

비밀 토큰을 사용해 유지보수 모드를 우회하도록 하려면 `secret` 옵션을 사용해 우회 토큰을 지정할 수 있습니다:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 유지보수 모드로 전환한 뒤, 토큰과 일치하는 URL에 접속하면 Laravel은 브라우저에 유지보수 모드 우회 쿠키를 발행합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 생성하도록 하려면 `with-secret` 옵션을 사용하세요. 유지보수 모드 활성화 후 비밀 토큰이 화면에 출력됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로에 접근하면 자동으로 `/` 경로로 리디렉션됩니다. 일단 쿠키가 발행되면 유지보수 모드가 아닌 것처럼 애플리케이션을 정상적으로 탐색할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰은 보통 영숫자 및 대시(-) 문자로 구성하는 것이 좋습니다. `?`, `&` 같은 URL에서 특수한 의미를 갖는 문자는 피하는 것이 좋습니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버에서의 유지보수 모드

기본적으로 Laravel은 파일 기반 시스템을 사용해 애플리케이션 유지보수 모드를 판단합니다. 즉, 유지보수 모드를 활성화하려면 앱이 호스팅된 모든 서버에서 `php artisan down` 명령을 각각 실행해야 합니다.

대안으로 Laravel은 캐시 기반 유지보수 모드 방식을 제공합니다. 이 방식은 단 한 서버에서 `php artisan down` 명령만 실행하면 됩니다. 사용하려면 애플리케이션 `.env` 파일에서 유지보수 모드 관련 변수를 수정하세요. 모든 서버가 접근 가능한 캐시 `store`를 선택해야 유지보수 모드 상태가 모든 서버에 일관되게 적용됩니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링하기

`php artisan down` 명령어를 배포 과정에서 사용할 경우, 일부 사용자가 Composer 의존성이나 인프라 구성 요소가 업데이트되는 시점에 오류를 겪을 수 있습니다. 이유는 Laravel 프레임워크의 상당 부분이 유지보수 모드 여부를 판단하고 템플릿 엔진으로 뷰를 렌더링하기 위해 부팅되어야 하기 때문입니다.

이를 해결하기 위해 Laravel은 유지보수 모드 뷰를 요청 사이클 초기에 미리 렌더링할 수 있도록 지원합니다. 이 뷰는 애플리케이션 의존성이 로딩되기 전에 렌더링됩니다. 원하는 템플릿을 `down` 명령어의 `--render` 옵션으로 미리 렌더링할 수 있습니다:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리디렉션하기

유지보수 모드 중에는 Laravel이 사용자가 요청하는 모든 URL에 대해 유지보수 모드 뷰를 표시합니다. 만약 모든 요청을 특정 URL로 리디렉션하고 싶다면 `--redirect` 옵션을 사용하세요. 예를 들어 모든 요청을 `/` URI로 리디렉션할 수 있습니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제하기

유지보수 모드를 해제하려면 `up` 명령어를 실행하세요:

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php` 위치에 사용자 정의 템플릿을 만들어 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 유지보수 모드에 있을 때는 모든 [큐 작업](/docs/master/queues)이 처리되지 않습니다. 유지보수 모드가 해제되면 작업들이 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션이 몇 초간 다운되는 점 때문에, 다운타임 없는 배포를 원한다면 [Laravel Cloud](https://cloud.laravel.com) 같은 완전 관리형 플랫폼에서 애플리케이션을 운영하는 것을 고려해 보세요.