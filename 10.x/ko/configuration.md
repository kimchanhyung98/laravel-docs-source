# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션에 대한 문서가 포함되어 있으니, 파일들을 살펴보며 어떤 옵션들이 있는지 익히는 것을 추천합니다.

이 설정 파일을 통해 데이터베이스 연결 정보, 메일 서버 정보뿐만 아니라 애플리케이션 타임존, 암호화 키 등 다양한 핵심 설정 값을 구성할 수 있습니다.

<a name="application-overview"></a>
#### 애플리케이션 개요

급히 설정 정보를 확인하고 싶다면, `about` Artisan 명령어를 사용해 애플리케이션의 설정, 드라이버, 환경에 대한 빠른 개요를 확인할 수 있습니다:

```shell
php artisan about
```

출력된 애플리케이션 개요 중 특정 섹션만 보고 싶다면 `--only` 옵션으로 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는 특정 구성 파일의 값을 자세히 살펴보려면 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 로컬에서는 다른 캐시 드라이버를 사용하고, 프로덕션 서버에서는 또 다른 드라이버를 사용할 수 있습니다.

이를 쉽게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. 새롭게 Laravel을 설치하면, 애플리케이션 루트 디렉터리에 `.env.example` 파일이 포함되어 있으며, 여기에는 흔히 사용하는 환경 변수들이 정의되어 있습니다. 설치 과정에서 이 파일은 자동으로 `.env`로 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있는 공통 설정 값들이 포함되어 있습니다. 이러한 값들은 Laravel의 `env` 함수를 통해 `config` 디렉터리 내 여러 설정 파일에서 읽혀집니다.

팀으로 개발할 경우, `.env.example` 파일을 애플리케이션에 포함하는 것이 좋습니다. 예제 설정 파일에 플레이스홀더로 값을 넣어두면, 다른 개발자들이 애플리케이션 실행에 필요한 환경 변수를 쉽게 파악할 수 있습니다.

> [!NOTE]  
> `.env` 파일 내 변수들은 서버 레벨 또는 시스템 레벨 환경 변수와 같은 외부 환경 변수에 의해 덮어씌워질 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 각 개발자나 서버별로 환경 구성이 다를 수 있으므로, 애플리케이션의 소스 코드 관리 저장소에 커밋해서는 안 됩니다. 또한, 만약 외부 침입자가 저장소에 접근했다면, 민감한 자격증명이 노출될 위험이 있습니다.

하지만 Laravel 내장 [환경 암호화 기능](#encrypting-environment-files)을 이용하면 `.env` 파일을 암호화하여, 안전하게 소스 코드 저장소에 포함시킬 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션이 환경 변수들을 로드하기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었거나 CLI `--env` 인수가 지정되었는지 확인합니다. 만약 존재하면 Laravel은 해당 환경 이름에 맞는 `.env.[APP_ENV]` 파일을 불러오려고 시도합니다. 해당 파일이 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입 (Environment Variable Types)

`.env` 파일 내의 모든 변수는 기본적으로 문자열로 해석됩니다. 하지만 Laravel에서는 `env()` 함수로 좀 더 다양한 타입을 반환하기 위해 예약된 값을 사용할 수 있도록 했습니다:

| `.env` 값  | `env()` 반환값     |
|------------|--------------------|
| true       | (bool) true        |
| (true)     | (bool) true        |
| false      | (bool) false       |
| (false)    | (bool) false       |
| empty      | (string) ''        |
| (empty)    | (string) ''        |
| null       | (null) null        |
| (null)     | (null) null        |

값에 공백이 포함될 경우, 값 전체를 큰따옴표로 감싸서 정의할 수 있습니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기 (Retrieving Environment Configuration)

`.env` 파일에 적힌 모든 변수는 애플리케이션이 요청을 받을 때 PHP의 `$_ENV` 슈퍼 글로벌에 로드됩니다. 하지만 설정 파일 내에서는 `env` 함수를 사용해 환경 변수 값을 불러오는 것이 일반적입니다. 기본 Laravel 설정 파일을 보면 많은 옵션들이 이미 이 함수를 통해 값을 받고 있습니다:

```
'debug' => env('APP_DEBUG', false),
```

`env` 함수는 두 번째 인자로 기본값을 받을 수 있으며, 해당 키의 환경 변수가 없을 경우 기본값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기 (Determining the Current Environment)

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/10.x/facades)의 `environment` 메서드를 통해 확인할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

`environment` 메서드에 인수를 전달하면 현재 환경이 인수들과 일치하는지 확인할 수도 있습니다. 일치하면 `true`를 반환합니다:

```
if (App::environment('local')) {
    // 현재 환경이 로컬
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 로컬 또는 스테이징 중 하나
}
```

> [!NOTE]  
> 현재 애플리케이션 환경은 서버 레벨에서 정의한 `APP_ENV` 환경 변수를 통해 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화 (Encrypting Environment Files)

암호화되지 않은 환경 파일은 절대 소스 코드 관리에 저장하지 말아야 합니다. 하지만, Laravel은 환경 파일을 암호화하여 안전하게 소스 코드에 포함시킬 수 있게 해줍니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하세요:

```shell
php artisan env:encrypt
```

이 명령어는 `.env` 파일을 암호화하여 `.env.encrypted` 파일로 저장합니다. 명령어 출력에 복호화 키가 표시되며, 이 키는 안전한 비밀번호 관리자에 보관해야 합니다. 직접키를 제공하고 싶다면 `--key` 옵션을 사용할 수 있습니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]  
> 키 길이는 사용하는 암호화 알고리즘에서 요구하는 값과 일치해야 합니다. 기본적으로 Laravel은 `AES-256-CBC`를 사용하며, 32글자 키가 필요합니다. `--cipher` 옵션을 사용하면 Laravel이 지원하는 다른 암호 방식을 선택할 수 있습니다.

여러 환경 파일(예: `.env`, `.env.staging`)이 있을 경우, `--env` 옵션으로 암호화를 원하는 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화

환경 파일 복호화는 `env:decrypt` 명령어를 사용합니다. 복호화 키는 기본적으로 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 가져옵니다:

```shell
php artisan env:decrypt
```

명령어에 직접 키를 전달하려면 `--key` 옵션을 사용하세요:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

복호화 시 `.env.encrypted` 파일이 `.env` 파일로 다시 생성됩니다.

`--cipher` 옵션으로 맞춤형 암호화 알고리즘을 지정할 수도 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일이 있는 경우, `--env` 옵션으로 복호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 붙이세요:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기 (Accessing Configuration Values)

애플리케이션 어디서든 `Config` facade 또는 글로벌 `config` 함수를 사용해 설정 값을 쉽게 불러올 수 있습니다. 설정 값은 "dot" 문법을 사용해 접근하며, 파일 이름과 옵션 이름을 포함합니다. 기본값을 지정할 수도 있으며, 설정 값이 없을 경우 기본값이 반환됩니다:

```
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 기본값 반환 예시
$value = config('app.timezone', 'Asia/Seoul');
```

런타임에 설정 값을 변경하려면 `Config` facade의 `set` 메서드를 호출하거나, `config` 함수에 배열을 넘겨주면 됩니다:

```
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

애플리케이션 속도를 높이기 위해, 모든 설정 파일을 하나의 파일로 합쳐 캐싱할 수 있습니다. `config:cache` Artisan 명령어를 사용하면, 모든 설정을 한 파일로 합쳐 프레임워크가 빠르게 로드할 수 있게 합니다.

일반적으로 이 명령어는 프로덕션 배포 과정에서 실행합니다. 로컬 개발 중에는 설정 값이 자주 변경되므로 실행하지 않는 것이 좋습니다.

설정을 캐시한 후에는, 요청이나 Artisan 명령어 실행 시 애플리케이션의 `.env` 파일은 로드되지 않습니다. 따라서 `env` 함수는 오직 외부의 시스템 레벨 환경 변수만 반환합니다.

이 때문에 `env` 함수는 애플리케이션의 설정(`config`) 파일 내에서만 사용하는 것이 권장됩니다. Laravel의 기본 설정 파일들을 보면 많은 예시를 확인할 수 있습니다. 설정 값은 애플리케이션 어디에서나 위에서 설명한 `config` 함수로 접근할 수 있습니다.

캐시된 설정을 삭제하려면 다음 명령어를 실행하세요:

```shell
php artisan config:clear
```

> [!WARNING]  
> 배포 과정에서 `config:cache`를 실행한다면, `env` 함수를 설정 파일 내에서만 호출하는지 반드시 확인해야 합니다. 한 번 캐싱하면 `.env` 파일은 로드되지 않고, `env` 함수는 오로지 외부 환경 변수만 반환하기 때문입니다.

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 얼마나 많은 정보를 보여줄지 결정합니다. 기본값은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]  
> 로컬 개발 환경에서는 `APP_DEBUG`를 `true`로 설정하세요. **반면 프로덕션 환경에서는 반드시 `false`로 설정해야 합니다.** 프로덕션에서 `true`로 설정하면 민감한 설정 값들이 최종 사용자에게 노출될 위험이 있습니다.

<a name="maintenance-mode"></a>
## 유지보수 모드 (Maintenance Mode)

애플리케이션이 유지보수 모드에 있을 때는, 사용자 모든 요청에 대해 커스텀 뷰가 표시됩니다. 이를 통해 업데이트나 점검 중에 애플리케이션을 "사용 불가" 상태로 만들 수 있습니다. 유지보수 모드 확인은 기본 미들웨어 스택에 포함되어 있으며, 모드가 활성화되어 있으면 상태 코드 503인 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

```shell
php artisan down
```

모든 유지보수 응답에 `Refresh` HTTP 헤더를 포함시키고 싶다면, `down` 명령어에 `--refresh` 옵션을 사용할 수 있습니다. `Refresh` 헤더는 브라우저가 지정된 시간 후 페이지를 자동 새로고침하게 만듭니다:

```shell
php artisan down --refresh=15
```

`down` 명령어에 `--retry` 옵션을 주어 `Retry-After` HTTP 헤더 값을 설정할 수도 있는데, 브라우저가 이 헤더를 무시하는 경우가 많습니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회하기

유지보수 모드를 비밀 토큰으로 우회하려면, `secret` 옵션으로 우회 토큰을 지정할 수 있습니다:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 진입 후, 토큰에 맞는 URL로 접속하면 Laravel이 우회 쿠키를 브라우저에 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel에 우회 토큰 생성을 맡기려면 `with-secret` 옵션을 사용하세요. 유지보수 모드 진입 시 비밀 토큰이 출력됩니다:

```shell
php artisan down --with-secret
```

이 숨겨진 경로를 방문하면 애플리케이션의 기본 `/` 경로로 리디렉션됩니다. 쿠키가 발급된 후에는 유지보수 모드가 아닌 것처럼 애플리케이션을 정상 이용할 수 있습니다.

> [!NOTE]  
> 유지보수 모드 비밀 토큰은 보통 알파벳과 숫자, 선택적으로 대시로 구성합니다. URL에서 특별한 의미가 있는 `?`, `&` 등의 문자는 피하는 것이 좋습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 미리 렌더링하기

`php artisan down` 명령어를 배포 시 사용하면 Composer 의존성이나 인프라 구성이 업데이트 되는 동안 사용자가 접근 시 간헐적으로 오류가 발생할 수 있습니다. 이는 Laravel이 유지보수 모드임을 판단하고 템플릿 엔진으로 뷰를 렌더링하기 위해 프레임워크 부팅이 먼저 필요하기 때문입니다.

이를 위해 Laravel은 어플리케이션 의존성이 로드되기 전에 요청 초반에 반환할 유지보수 모드 뷰를 미리 렌더링하는 기능을 제공합니다. 특정 뷰 템플릿을 미리 렌더링하려면 `down` 명령어의 `--render` 옵션을 사용하세요:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리디렉션

유지보수 모드 동안 사용자가 어떤 URL에 접근해도 유지보수 페이지가 뜨는데, 원하는 경우 모든 요청을 특정 URL로 리디렉션할 수 있습니다. `--redirect` 옵션을 사용하세요. 예를 들어 모든 요청을 `/` URI로 리디렉션하려면 다음과 같이 실행합니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 비활성화

유지보수 모드를 종료하려면 `up` 명령어를 실행하면 됩니다:

```shell
php artisan up
```

> [!NOTE]  
> 기본 유지보수 모드 템플릿을 커스터마이징하려면 `resources/views/errors/503.blade.php` 경로에 직접 템플릿을 정의하세요.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 유지보수 모드에 있으면 [큐 작업](/docs/10.x/queues)은 처리되지 않습니다. 유지보수 모드가 종료되면 정상적으로 작업이 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션의 다운타임이 몇 초 이상 발생할 수 있으므로, 무중단 배포를 원한다면 [Laravel Vapor](https://vapor.laravel.com), [Envoyer](https://envoyer.io) 같은 도구를 고려해 보세요.