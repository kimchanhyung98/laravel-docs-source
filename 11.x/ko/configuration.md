# 설정 (Configuration)

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
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장되어 있습니다. 각 옵션은 문서화되어 있으니, 설정 파일을 살펴보면서 어떤 옵션들이 제공되는지 익히는 것을 권장합니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보 등 다양한 핵심 설정 값을 구성할 수 있으며, 애플리케이션 URL이나 암호화 키 같은 공통 설정도 포함됩니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요를 보여줄 수 있습니다.

```shell
php artisan about
```

특정 부분만 보고 싶다면 `--only` 옵션을 사용해 필터링할 수 있습니다:

```shell
php artisan about --only=environment
```

또는 특정 설정 파일의 값을 자세히 살펴보고 싶을 때는 `config:show` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 로컬 환경에서는 캐시 드라이버를 다르게 설정하고, 프로덕션 서버에서는 또 다른 드라이버를 사용할 수 있습니다.

이를 간편하게 하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 사용합니다. Laravel을 새로 설치하면, 애플리케이션 루트 디렉터리에 `.env.example` 파일이 포함되어 있으며, 이 파일에는 자주 사용하는 환경 변수가 정의되어 있습니다. 설치 과정 중에 이 파일은 자동으로 `.env` 파일로 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬 환경과 프로덕션 웹 서버 환경에 따라 달라질 수 있는 일반적인 설정 값들이 포함되어 있습니다. 이 값들은 Laravel의 `env` 함수로 `config` 디렉터리 내 설정 파일들이 읽어들입니다.

협업 개발 시에는 `.env.example` 파일을 계속 포함하고 업데이트하는 것이 좋습니다. 예시 설정 파일에 플레이스홀더 값을 넣음으로써 팀원들이 어떤 환경 변수가 필요한지 명확하게 알 수 있기 때문입니다.

> [!NOTE]  
> `.env` 파일에 있는 모든 변수는 서버 레벨 또는 시스템 레벨 환경 변수와 같은 외부 환경 변수에 의해 덮어씌워질 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

`.env` 파일은 애플리케이션 소스 컨트롤에 포함해서는 안 됩니다. 각 개발자나 서버는 서로 다른 환경 구성이 필요하기 때문입니다. 또한 소스 컨트롤 저장소에 접근한 공격자가 민감한 자격 증명을 볼 위험도 있습니다.

하지만 Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files)를 이용하면 환경 파일을 암호화하여 안전하게 소스 컨트롤에 보관할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션 환경 변수를 불러오기 전에, Laravel은 외부에서 제공된 `APP_ENV` 환경 변수나 `--env` CLI 인수가 있는지 확인합니다. 만약 있다면, `.env.[APP_ENV]` 파일이 존재하는 경우 이 파일을 우선 로드하며, 없으면 기본 `.env` 파일을 로드합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입 (Environment Variable Types)

`.env` 파일의 모든 변수는 기본적으로 문자열로 파싱됩니다. 하지만 `env()` 함수에서 더 다양한 타입의 값을 반환할 수 있도록 예약된 몇 가지 값들이 정의되어 있습니다:

<div class="overflow-auto">

| `.env` 값   | `env()` 반환 값  |
| ----------- | --------------- |
| true        | (bool) true     |
| (true)      | (bool) true     |
| false       | (bool) false    |
| (false)     | (bool) false    |
| empty       | (string) ''     |
| (empty)     | (string) ''     |
| null        | (null) null     |
| (null)      | (null) null     |

</div>

공백이 포함된 값을 환경 변수로 정의하려면, 값을 큰따옴표로 감싸면 됩니다:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기 (Retrieving Environment Configuration)

`.env` 파일에 적힌 모든 변수는 애플리케이션 요청 시 PHP의 `$_ENV` 슈퍼 글로벌에 로드됩니다. 설정 파일에서는 `env` 함수를 사용해 환경 변수 값을 가져올 수 있습니다. Laravel 기본 설정 파일을 보면 많은 옵션이 이미 이 함수를 사용 중인 것을 확인할 수 있습니다:

```
'debug' => env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인수는 "기본값"이며, 해당 키에 환경 변수가 없을 때 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인하기 (Determining the Current Environment)

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [facade](/docs/11.x/facades)의 `environment` 메서드로 접근할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, `environment` 메서드에 인수를 전달하면 현재 환경이 인수 값과 일치하는지 확인할 수 있으며, 일치할 경우 `true`를 반환합니다:

```
if (App::environment('local')) {
    // 현재 환경이 local인 경우
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 또는 staging인 경우
}
```

> [!NOTE]  
> 현재 애플리케이션 환경은 서버 레벨의 `APP_ENV` 환경 변수를 정의함으로써 재정의할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화하기 (Encrypting Environment Files)

암호화되지 않은 환경 파일은 절대 소스 컨트롤에 저장해서는 안 됩니다. 하지만 Laravel은 환경 파일을 암호화해 애플리케이션과 함께 안심하고 소스 컨트롤에 추가할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화 (Encryption)

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용하세요:

```shell
php artisan env:encrypt
```

이 명령어는 `.env` 파일을 암호화하여 `.env.encrypted` 파일에 저장하며, 복호화 키를 명령어 출력으로 보여줍니다. 이 키는 안전한 비밀번호 관리자에 보관해야 합니다. 복호화 키를 직접 제공하려면 `--key` 옵션을 사용하면 됩니다:

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]  
> 제공하는 키 길이는 사용하는 암호화 알고리즘에 맞아야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 암호화를 사용합니다. 또한 `--cipher` 옵션을 이용해 Laravel이 지원하는 다른 암호화 알고리즘을 사용할 수 있습니다. 관련 내용은 [encrypter](/docs/11.x/encryption) 문서를 참고하세요.

복수의 환경 파일(예: `.env`, `.env.staging`)이 있을 경우 `--env` 옵션으로 암호화할 환경 파일을 지정할 수 있습니다:

```shell
php artisan env:encrypt --env=staging
```

<a name="decryption"></a>
#### 복호화 (Decryption)

암호화된 환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용합니다. 이 명령어는 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 복호화 키를 찾아 사용합니다:

```shell
php artisan env:decrypt
```

또는 `--key` 옵션으로 키를 직접 제공할 수도 있습니다:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

명령어 실행 시, `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장합니다.

사용할 커스텀 암호화 알고리즘을 지정하려면 `--cipher` 옵션을 함께 사용할 수 있습니다:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

복수 환경 파일 중 복호화할 파일을 지정하려면 `--env` 옵션을 사용하세요:

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가합니다:

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기 (Accessing Configuration Values)

애플리케이션 어디서든 `Config` facade나 전역 `config` 함수를 통해 설정 값에 쉽게 접근할 수 있습니다. 설정 값은 파일명과 옵션명을 점(`.`)으로 구분해 "dot" 구문을 사용해 불러옵니다. 기본값도 함께 지정 가능합니다. 만약 해당 설정이 없으면 기본값을 반환합니다:

```
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없으면 기본값 반환
$value = config('app.timezone', 'Asia/Seoul');
```

런타임에 설정 값을 변경하려면 `Config` facade의 `set` 메서드 혹은 `config` 함수에 배열을 전달할 수 있습니다:

```
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석 도구 지원을 위해 `Config` facade는 타입별 설정 값 조회 메서드도 제공합니다. 조회한 설정 값이 기대하는 타입과 다르면 예외가 발생합니다:

```
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

애플리케이션 속도를 높이려면 `config:cache` Artisan 명령어로 모든 설정 파일을 하나의 파일로 캐싱하는 것이 좋습니다. 이 명령어는 설정 옵션들을 하나로 합쳐 프레임워크가 빠르게 로드할 수 있게 합니다.

보통 프로덕션 배포 과정에서 `php artisan config:cache` 명령어를 실행해야 하며, 로컬 개발 중에는 자주 설정을 변경해야 하므로 이 명령어를 사용하지 않는 것이 좋습니다.

캐싱 후에는 애플리케이션 요청 시 `.env` 파일이 로드되지 않기 때문에, `env` 함수는 외부 시스템 환경 변수만 반환합니다.

따라서 `env` 함수는 반드시 애플리케이션 설정 파일 안에서만 호출하는 것이 좋습니다. Laravel 기본 설정 파일들을 살펴보면 이를 확인할 수 있습니다. 설정 값을 애플리케이션 어디서든 `config` 함수를 통해 접근할 수 있습니다([위 설명 참조](#accessing-configuration-values)).

캐시된 설정을 삭제하려면 `config:clear` 명령어를 사용하세요:

```shell
php artisan config:clear
```

> [!WARNING]  
> 배포 과정 중 `config:cache` 명령어를 사용한다면, `env` 함수가 반드시 설정 파일 내에서만 호출되도록 해야 합니다. 캐싱 이후에는 `.env` 파일이 로드되지 않아, `env` 함수가 외부 시스템 환경 변수만 반환하기 때문입니다.

<a name="configuration-publishing"></a>
## 설정 퍼블리싱 (Configuration Publishing)

Laravel의 대부분 설정 파일은 이미 애플리케이션 `config` 디렉터리에 퍼블리시되어 있습니다. 다만 `cors.php`, `view.php`처럼 기본적으로 퍼블리시되지 않는 설정 파일들도 있습니다. 보통 이러한 파일을 수정할 필요가 없기 때문입니다.

하지만 필요에 따라 `config:publish` Artisan 명령어로 기본 퍼블리시되지 않은 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 `debug` 옵션은 애플리케이션 오류 시 사용자에게 보여줄 정보량을 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수를 따릅니다.

> [!WARNING]  
> 로컬 개발 중에는 `APP_DEBUG` 환경 변수를 `true`로 설정하세요. **하지만 프로덕션 환경에서는 반드시 `false`로 설정해야 합니다.** 그렇지 않으면 민감한 설정 값이 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.

<a name="maintenance-mode"></a>
## 유지보수 모드 (Maintenance Mode)

애플리케이션이 유지보수 모드에 들어가면, 모든 요청에 대해 맞춤 뷰가 표시됩니다. 이는 업데이트 중이거나 유지보수를 진행할 때 애플리케이션을 "일시 중지"하는 간편한 방법입니다. 유지보수 모드 확인은 기본 미들웨어 스택에 포함되어 있으며, 유지보수 모드 시 상태 코드 503과 함께 `Symfony\Component\HttpKernel\Exception\HttpException` 예외가 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행하세요:

```shell
php artisan down
```

유지보수 모드 응답에 `Refresh` HTTP 헤더를 포함하여, 지정한 초 후에 자동으로 페이지가 새로 고쳐지게 하려면 `--refresh` 옵션을 추가합니다:

```shell
php artisan down --refresh=15
```

`--retry` 옵션을 추가하면 `Retry-After` HTTP 헤더를 설정할 수 있지만, 대부분의 브라우저는 이를 무시합니다:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회하기

비밀 토큰을 사용해 유지보수 모드를 우회하려면 `secret` 옵션으로 토큰을 지정하세요:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 진입 후 이 토큰을 포함한 URL에 접속하면 Laravel이 브라우저에 유지보수 모드 우회용 쿠키를 발급합니다:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel에게 비밀 토큰을 자동 생성하게 하려면 `with-secret` 옵션을 사용하세요. 유지보수 모드 진입과 동시에 토큰이 출력됩니다:

```shell
php artisan down --with-secret
```

이 비밀 경로에 접속하면 사용자는 `/` 경로로 리다이렉션 되고, 쿠키 발급 후에는 유지보수 모드가 아니었던 것처럼 애플리케이션을 자유롭게 이용할 수 있습니다.

> [!NOTE]  
> 유지보수 모드 비밀 토큰은 일반적으로 영숫자와 대시(`-`)로 구성합니다. URL에서 특별한 의미가 있는 `?`나 `&` 같은 문자는 사용하지 않는 것이 좋습니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 여러 서버 환경에서의 유지보수 모드

기본적으로 Laravel은 파일 기반 시스템으로 유지보수 모드 여부를 판단하므로, 여러 서버가 있을 경우 각각에서 `php artisan down` 명령어를 실행해야 합니다.

대신 캐시 기반 방식을 사용할 수도 있으며, 이 경우 한 서버에서 `php artisan down`만 실행하면 됩니다. 캐시 방식을 사용하려면 `.env` 파일에서 유지보수 모드 관련 변수를 수정하고, 모든 서버가 접근 가능한 캐시 저장소를 선택해야 합니다:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링

배포 시 `php artisan down` 명령어를 사용할 경우, Composer 의존성이나 기타 인프라가 변경 중일 때 사용자가 간헐적으로 오류를 경험할 수 있습니다. 이는 Laravel 프레임워크가 작동 완료되어 유지보수 모드임을 확인하고 Blade 템플릿으로 뷰를 렌더링하는 데 시간이 걸리기 때문입니다.

이 문제를 해결하기 위해 Laravel은 요청 초기에 반환할 유지보수 모드 뷰를 미리 렌더링할 수 있는 기능을 제공합니다. 이 뷰는 애플리케이션 의존성이 로드되기 이전에 렌더링됩니다. 원하는 템플릿을 사용해 뷰를 사전 렌더링하려면 `down` 명령어에 `--render` 옵션을 지정하세요:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리다이렉트

유지보수 모드 중 모든 요청에 대해 특정 URL로 리다이렉트하고 싶다면 `--redirect` 옵션을 사용하세요. 예를 들어, 모든 요청을 `/` URI로 리다이렉트하려면 다음과 같이 명령어를 실행합니다:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제하기

유지보수 모드를 해제하려면 `up` 명령어를 사용하세요:

```shell
php artisan up
```

> [!NOTE]  
> 유지보수 모드 기본 템플릿은 `resources/views/errors/503.blade.php` 파일을 정의해 커스터마이즈할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

유지보수 모드 중에는 [대기열 작업](/docs/11.x/queues)이 처리되지 않습니다. 유지보수 모드 종료 후에 작업 처리가 정상적으로 다시 시작됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드 대안

유지보수 모드는 애플리케이션에 몇 초간의 다운타임이 필요하므로, 다운타임 없이 배포가 가능한 [Laravel Vapor](https://vapor.laravel.com)나 [Envoyer](https://envoyer.io) 같은 대안을 고려할 수 있습니다.