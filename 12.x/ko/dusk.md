# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 변수 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증 처리](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 저장하기](#storing-console-output-to-disk)
    - [페이지 소스 저장하기](#storing-page-source-to-disk)
- [요소와 상호작용하기](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용하기](#interacting-with-forms)
    - [파일 첨부하기](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭하기](#clicking-links)
    - [키보드 사용하기](#using-the-keyboard)
    - [마우스 사용하기](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용하기](#interacting-with-iframes)
    - [셀렉터 범위 지정하기](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소를 뷰로 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지 네비게이션](#navigating-to-pages)
    - [단축 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용법](#using-components)
- [CI 환경에서 사용하기](#continuous-integration)
    - [Heroku CI에서 테스트 실행](#running-tests-on-heroku-ci)
    - [Travis CI에서 테스트 실행](#running-tests-on-travis-ci)
    - [GitHub Actions에서 테스트 실행](#running-tests-on-github-actions)
    - [Chipper CI에서 테스트 실행](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로, Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 물론 Selenium 호환 드라이버를 자유롭게 사용할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> 만약 Dusk 서비스 프로바이더를 직접 등록하고 있다면, **절대** 운영 환경에서 등록하지 말아야 합니다. 운영 환경에서 등록 시 임의 사용자가 애플리케이션에 인증할 수 있는 보안 위험이 발생할 수 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리, 예제 Dusk 테스트, 그리고 운영 체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 URL은 브라우저에서 애플리케이션에 접근하는 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경 관리를 위해 [Laravel Sail](/docs/12.x/sail)을 사용한다면, Sail 문서의 [Dusk 테스트 구성과 실행](/docs/12.x/sail#laravel-dusk)도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

Laravel Dusk가 `dusk:install` 명령어를 통해 설치하는 ChromeDriver 버전과 다른 버전을 설치하고자 할 경우, `dusk:chrome-driver` 명령어를 사용하세요:

```shell
# OS용 ChromeDriver 최신 버전 설치...
php artisan dusk:chrome-driver

# 특정 버전 설치 (예: 86)...
php artisan dusk:chrome-driver 86

# 지원되는 모든 OS용 특정 버전 설치...
php artisan dusk:chrome-driver --all

# OS에서 사용 중인 Chrome/Chromium 버전을 감지하여 맞는 드라이버 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. 실행 문제 발생 시 다음 명령어로 실행 권한을 설정하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용하여 브라우저 테스트를 수행합니다. 그러나 직접 Selenium 서버를 띄워 원하는 브라우저와 테스트 할 수도 있습니다.

시작하려면, `tests/DuskTestCase.php` 파일을 열고 `startChromeDriver` 메서드 호출을 주석 처리하세요. 이렇게 하면 Dusk는 자동으로 ChromeDriver를 시작하지 않습니다:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

다음으로, `driver` 메서드를 수정하여 원하는 URL과 포트로 WebDriver에 연결하세요. 또한 WebDriver에 넘기는 "desired capabilities"도 변경할 수 있습니다:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a name="getting-started"></a>
## 시작하기 (Getting Started)

<a name="generating-tests"></a>
### 테스트 생성 (Generating Tests)

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 위치합니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

작성하는 대부분의 테스트는 애플리케이션 데이터베이스와 연결된 페이지와 상호작용하지만, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. 이는 `RefreshDatabase`가 데이터베이스 트랜잭션을 이용하는데, 이는 HTTP 요청을 넘어서서는 적용되지 않기 때문입니다.

대신, 두 가지 선택지가 있습니다: `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트입니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용하기

`DatabaseMigrations` 트레이트는 각 테스트 수행 전 데이터베이스 마이그레이션을 실행합니다. 하지만 모든 테이블을 매번 삭제 및 재생성하기 때문에 속도가 느릴 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

uses(DatabaseMigrations::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    //
}
```

> [!WARNING]
> Dusk 테스트에서는 SQLite 인메모리 데이터베이스를 사용할 수 없습니다. 브라우저가 별도 프로세스에서 실행되기 때문에, 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 초기화 사용하기

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 데이터베이스 마이그레이션을 실행해 테이블을 생성하고, 그 이후 테스트에서는 테이블 데이터를 단순히 초기화(트렁케이트)합니다. 이렇게 하면 마이그레이션을 반복하는 것보다 빠릅니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

uses(DatabaseTruncation::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;

    //
}
```

기본적으로, 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 초기화합니다. 초기화할 테이블을 사용자 정의하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

> [!NOTE]
> Pest를 사용한다면 속성이나 메서드는 기본 `DuskTestCase` 클래스나 테스트 파일이 상속하는 클래스에 정의해야 합니다.

```php
/**
 * 초기화할 테이블 목록.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는 `$exceptTables` 속성을 정의하여 초기화에서 제외할 테이블을 지정할 수 있습니다:

```php
/**
 * 초기화에서 제외할 테이블 목록.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

초기화할 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 정의하세요:

```php
/**
 * 테이블 초기화를 적용할 연결 목록.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

초기화 수행 전후에 코드를 실행하고 싶으면, 테스트 클래스에 `beforeTruncatingDatabase` 와 `afterTruncatingDatabase` 메서드를 정의하세요:

```php
/**
 * 데이터베이스 초기화 시작 전 실행할 작업.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * 데이터베이스 초기화 완료 후 실행할 작업.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행 (Running Tests)

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

이전에 실패한 테스트가 있다면, `dusk:fails` 명령어로 실패한 테스트부터 먼저 실행하여 시간을 절약할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest나 PHPUnit 테스트 러너가 일반적으로 받아들이는 모든 인수를 지원합니다. 예를 들어 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)에 속한 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> Laravel Sail로 로컬 개발 환경을 관리 중이라면, Sail 문서의 [Dusk 테스트 구성과 실행](/docs/12.x/sail#laravel-dusk)을 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작하기

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려 시도합니다. 만약 시스템에서 이 기능이 작동하지 않는다면, `dusk` 명령 실행 전에 ChromeDriver를 직접 시작할 수 있습니다. 이때 `tests/DuskTestCase.php` 파일에서 다음 코드를 주석 처리해야 합니다:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

만약 ChromeDriver를 기본 포트 9515가 아닌 다른 포트에서 시작한다면, 동일 클래스의 `driver` 메서드도 적절히 수정하세요:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### 환경 변수 처리 (Environment Handling)

테스트 실행 시 Dusk가 자신의 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어, `local` 환경에서 `dusk` 명령을 실행할 계획이라면 `.env.dusk.local` 파일을 생성하세요.

테스트 실행 중에 Dusk는 기존 `.env` 파일을 백업해 두고 `.env.dusk.{environment}` 파일을 `.env`로 바꿉니다. 테스트가 완료되면 원래 `.env` 파일을 복원합니다.

<a name="browser-basics"></a>
## 브라우저 기본 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성하기 (Creating Browsers)

간단한 예제로 애플리케이션에 로그인할 수 있는지 테스트를 작성해 봅시다. 테스트 생성 후 로그인 페이지로 이동하여 자격 증명을 입력하고 "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 호출하면 생성됩니다:

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

uses(DatabaseMigrations::class);

test('basic example', function () {
    $user = User::factory()->create([
        'email' => 'taylor@laravel.com',
    ]);

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/login')
            ->type('email', $user->email)
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * 기본 브라우저 테스트 예제.
     */
    public function test_basic_example(): void
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/home');
        });
    }
}
```

위 예시처럼, `browse` 메서드는 클로저(익명 함수)를 인자로 받으며, Dusk가 브라우저 인스턴스를 해당 클로저에 자동으로 전달합니다. 이 브라우저 인스턴스를 통해 애플리케이션과 상호작용하고 어설션을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 여러 개 브라우저 만들기 (Creating Multiple Browsers)

웹소켓 등으로 상호작용하는 채팅 화면 테스트처럼, 여러 브라우저 인스턴스가 필요할 때가 있습니다. `browse` 메서드 클로저에 추가로 브라우저 인수를 선언하면 됩니다:

```php
$this->browse(function (Browser $first, Browser $second) {
    $first->loginAs(User::find(1))
        ->visit('/home')
        ->waitForText('Message');

    $second->loginAs(User::find(2))
        ->visit('/home')
        ->waitForText('Message')
        ->type('message', 'Hey Taylor')
        ->press('Send');

    $first->waitForText('Hey Taylor')
        ->assertSee('Jeffrey Way');
});
```

<a name="navigation"></a>
### 네비게이션 (Navigation)

`visit` 메서드는 애플리케이션 내 특정 URI로 이동할 때 사용합니다:

```php
$browser->visit('/login');
```

`visitRoute` 메서드로 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)로 이동할 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`(뒤로가기), `forward`(앞으로가기) 메서드도 사용할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드는 페이지 새로고침을 수행합니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드를 사용해 브라우저 창 크기를 조절할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창 크기를 콘텐츠 크기에 맞게 조정합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 `fitContent`를 호출해 스크린샷 촬영 전에 창 크기를 맞춥니다. 이를 비활성화하려면 테스트 내에서 `disableFitOnFailure` 메서드를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 화면 내 브라우저 창 위치를 이동할 수도 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 이용할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Dusk 브라우저 매크로 등록.
     */
    public function boot(): void
    {
        Browser::macro('scrollToElement', function (string $element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

`macro`는 이름과 클로저를 받아, 해당 이름으로 호출 시 클로저가 실행됩니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 처리 (Authentication)

테스트 중 로그인을 반복하지 않기 위해 Dusk의 `loginAs` 메서드를 사용하여 인증할 수 있습니다. 이 메서드는 인증 가능한 모델의 기본 키나 모델 인스턴스를 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용하면 해당 테스트 파일 내 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

암호화된 쿠키 값을 가져오거나 설정하려면 `cookie` 메서드를 사용합니다. Laravel에서 생성한 쿠키는 기본적으로 모두 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값을 다루려면 `plainCookie` 메서드를 이용하세요:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키를 삭제할 때는 `deleteCookie` 메서드를 사용합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 (Executing JavaScript)

`script` 메서드를 통해 브라우저 내에서 임의의 JavaScript 코드를 실행할 수 있습니다:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기 (Taking a Screenshot)

`screenshot` 메서드를 사용하면 주어진 파일명으로 스크린샷을 저장합니다. 스크린샷은 모두 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드를 사용하면 다양한 화면 크기로 스크린샷 시리즈를 찍을 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

특정 요소만 스크린샷으로 찍으려면 `screenshotElement` 메서드를 사용하세요:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장하기 (Storing Console Output to Disk)

`storeConsoleLog` 메서드로 현재 브라우저의 콘솔 로그를 파일로 저장할 수 있습니다. 콘솔 로그는 `tests/Browser/console` 디렉터리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장하기 (Storing Page Source to Disk)

`storeSource` 메서드로 현재 페이지의 소스 코드를 파일로 저장할 수 있습니다. 파일은 `tests/Browser/source` 디렉터리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

좋은 CSS 셀렉터를 선택하는 것은 Dusk 테스트 작성의 어려운 부분 중 하나입니다. 프론트엔드 변경 시 다음처럼 기억했던 셀렉터가 깨질 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 선택자 대신 요소에 `dusk` 속성을 추가해 테스트에 집중할 수 있습니다. Dusk 브라우저에서는 `@` 기호를 붙여 해당 요소를 조작할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원한다면 Dusk 셀렉터가 사용할 HTML 속성을 `selectorHtmlAttribute` 메서드로 커스터마이징할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기 (Retrieving and Setting Values)

Dusk는 페이지 요소의 현재 값, 표시 텍스트, 속성을 조작할 수 있는 여러 메서드를 제공합니다. 예를 들어, 선택자에 부합하는 요소의 "value" 값을 얻으려면 `value` 메서드를 사용합니다:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 특정 이름을 가진 입력 필드의 값을 가져오는데 사용할 수 있습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기 (Retrieving Text)

`text` 메서드를 사용하면 선택자에 부합하는 요소의 표시 텍스트를 가져올 수 있습니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기 (Retrieving Attributes)

`attribute` 메서드는 선택자에 해당하는 요소의 특정 속성 값을 조회합니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기 (Typing Values)

Dusk는 폼과 입력 요소를 다룰 다양한 메서드를 제공합니다. 텍스트 입력 예시는 다음과 같습니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

`type` 메서드는 CSS 셀렉터를 지정할 수 있지만, 미지정 시 `name` 속성이 일치하는 `input` 또는 `textarea` 필드를 찾아 입력합니다.

기존 내용에 텍스트를 덧붙이려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력 값 초기화는 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

좀 더 느린 타이핑을 원한다면 `typeSlowly` 메서드를 사용하세요. 기본 딜레이는 키 입력 사이 100밀리초입니다. 세 번째 인자로 딜레이 밀리초를 직접 지정할 수 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

느리게 덧붙이려면 `appendSlowly` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운 (Dropdowns)

`select` 메서드로 `select` 요소에서 값을 선택할 수 있습니다. `type`과 마찬가지로 전체 CSS 선택자를 요구하지 않으며, 전달하는 값은 옵션의 실제 값이어야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤 옵션을 선택합니다:

```php
$browser->select('size');
```

배열을 두 번째 인수로 전달하면 여러 옵션을 선택할 수 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스 (Checkboxes)

`check` 메서드를 이용해 체크박스를 체크합니다. 전체 CSS 선택자 없이도 `name` 속성이 일치하는 체크박스를 찾습니다:

```php
$browser->check('terms');
```

`uncheck` 메서드는 체크 해제를 수행합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼 (Radio Buttons)

`radio` 메서드로 라디오 버튼을 선택할 수 있습니다. CSS 선택자 없이 `name`과 `value` 속성에 매칭되는 라디오 입력을 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기 (Attaching Files)

`attach` 메서드로 `file` 타입 입력 요소에 파일을 첨부할 수 있습니다. 역시 CSS 셀렉터 없이 `name` 속성으로 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> `attach` 메서드를 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드는 페이지 내 버튼을 클릭합니다. 인수는 버튼에 보이는 텍스트이거나 CSS/Dusk 셀렉터입니다:

```php
$browser->press('Login');
```

폼 제출 버튼은 클릭 시 비활성화되고, 제출 완료되면 다시 활성화되는 경우가 많습니다. 버튼을 클릭하고 버튼이 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용하세요:

```php
// 최대 5초 기다림...
$browser->pressAndWaitFor('Save');

// 최대 1초 기다림...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 주어진 표시 텍스트를 가진 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

페이지에 해당 텍스트 링크가 보이는지 확인하려면 `seeLink`를 사용하세요:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드들은 jQuery를 사용합니다. 페이지에 jQuery가 없으면 Dusk가 테스트 기간 동안 자동으로 페이지에 삽입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기 (Using the Keyboard)

`keys` 메서드는 기본 `type` 메서드보다 복잡한 입력을 허용합니다. 예를 들어, modifier 키를 누른 상태에서 값을 입력할 수 있습니다. 아래는 `shift` 키를 누른 상태로 `taylor` 입력 후, modifier 없이 `swift` 입력 예시입니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또는 키보드 단축키를 CSS 선택자에 보내려면:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> 모든 modifier 키는 중괄호 `{}`로 감싸며, Facebook\WebDriver\WebDriverKeys 클래스에서 상수로 정의되어 있습니다. (https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php 참고)

<a name="fluent-keyboard-interactions"></a>
#### 간편한 키보드 조작 (Fluent Keyboard Interactions)

Dusk는 `withKeyboard` 메서드를 제공해 `Laravel\Dusk\Keyboard`를 통해 복잡한 키보드 동작을 쉽게 처리할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 지원합니다:

```php
use Laravel\Dusk\Keyboard;

$browser->withKeyboard(function (Keyboard $keyboard) {
    $keyboard->press('c')
        ->pause(1000)
        ->release('c')
        ->type(['c', 'e', 'o']);
});
```

<a name="keyboard-macros"></a>
#### 키보드 매크로 (Keyboard Macros)

테스트 전반에서 재사용 가능한 키보드 동작을 커스텀 매크로로 정의하려면 `Keyboard` 클래스의 `macro` 메서드를 활용하세요. 보통 서비스 프로바이더 `boot` 메서드에서 정의합니다:

```php
<?php

namespace App\Providers;

use Facebook\WebDriver\WebDriverKeys;
use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Keyboard;
use Laravel\Dusk\OperatingSystem;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Dusk 키보드 매크로 등록.
     */
    public function boot(): void
    {
        Keyboard::macro('copy', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'c',
            ]);

            return $this;
        });

        Keyboard::macro('paste', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'v',
            ]);

            return $this;
        });
    }
}
```

매크로는 이름과 클로저를 받으며, 해당 이름으로 `Keyboard` 인스턴스에서 호출할 때 클로저가 실행됩니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용하기 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭하기

`click` 메서드로 CSS 또는 Dusk 셀렉터에 해당하는 요소를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식에 해당하는 요소를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint`는 브라우저에서 지정한 좌표 내 최상위 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick`은 더블 클릭을 시뮬레이션합니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick`은 우클릭을 시뮬레이션합니다:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`는 마우스 버튼을 눌러 누르고 있는 상태를 시뮬레이트하며, `releaseMouse` 호출로 해제할 수 있습니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 `ctrl`키와 클릭 이벤트를 시뮬레이션합니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메서드로 지정 요소 위에 마우스를 올립니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드로 한 요소를 다른 요소로 드래그할 수 있습니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

단일 방향으로 드래그하는 메서드도 있습니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 드래그하려면 `dragOffset` 메서드를 사용합니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그 (JavaScript Dialogs)

Dusk는 JavaScript 대화상자와 상호작용하기 위한 다양한 메서드를 제공합니다.

`waitForDialog` 메서드로 대화상자가 나타날 때까지 대기합니다. 인수로 최대 대기 시간을 줄 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`는 지정한 메시지를 포함한 대화상자가 나타났는지 단언합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 뜨면 `typeInDialog`로 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼 클릭으로 대화상자를 닫으려면 `acceptDialog` 를 호출합니다:

```php
$browser->acceptDialog();
```

"취소" 버튼 클릭은 `dismissDialog` 를 호출합니다:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용하기 (Interacting With Inline Frames)

iframe 내 요소를 조작하려면 `withinFrame` 메서드를 사용합니다. 클로저 내의 모든 조작은 지정한 iframe 내부로 한정됩니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정하기 (Scoping Selectors)

특정 셀렉터에 한정해 여러 동작을 해야 할 때, `with` 메서드를 사용하세요. 클로저 내 모든 동작이 주어진 셀렉터 범위로 한정됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때때로 범위를 벗어난 어설션을 해야 할 수 있습니다. 이때 `elsewhere` 와 `elsewhereWhenAvailable` 메서드를 사용하세요:

```php
$browser->with('.table', function (Browser $table) {
    // 범위: body .table

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 범위: body .page-title
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 범위: body .page-title
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기 (Waiting for Elements)

JavaScript가 많이 사용되는 애플리케이션 테스트 시, 특정 요소가 준비될 때까지 기다려야 하는 경우가 많습니다. Dusk에서는 다양한 대기 메서드를 제공합니다.

<a name="waiting"></a>
#### 대기 (Waiting)

특정 시간(ms) 동안 일시 정지하려면 `pause` 메서드를 사용합니다:

```php
$browser->pause(1000);
```

`pauseIf` 는 조건이 참일 때만 일시 정지합니다:

```php
$browser->pauseIf(App::environment('production'), 1000);
```

`pauseUnless` 는 조건이 거짓일 때만 일시 정지합니다:

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기 (Waiting for Selectors)

`waitFor` 메서드는 주어진 CSS 또는 Dusk 셀렉터가 페이지에 표시될 때까지 최대 5초(기본) 대기합니다. 두 번째 인자로 시간 제한을 변경할 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitFor('.selector');

// 최대 1초 대기...
$browser->waitFor('.selector', 1);
```

요소 안에 특정 텍스트가 표시될 때까지 대기하려면:

```php
// 최대 5초 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

특정 셀렉터가 사라질 때까지 기다릴 수도 있습니다:

```php
// 최대 5초 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 대기...
$browser->waitUntilMissing('.selector', 1);
```

또한 요소가 활성화(Enabled) 혹은 비활성화(Disabled)될 때까지도 대기 가능합니다:

```php
// 활성화될 때까지 최대 5초 대기...
$browser->waitUntilEnabled('.selector');

// 비활성화될 때까지 최대 5초 대기...
$browser->waitUntilDisabled('.selector');
```

<a name="scoping-selectors-when-available"></a>
#### 요소가 준비됐을 때 범위 지정해 대기하기

모달 창이 활성화될 때까지 기다려 버튼을 누르는 등, 요소가 준비된 후 특정 조작을 해야 할 때 `whenAvailable` 메서드를 활용하세요:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기 (Waiting for Text)

지정한 텍스트가 페이지에 표시될 때까지 기다리려면 `waitForText` 메서드를 사용합니다:

```php
// 최대 5초 대기...
$browser->waitForText('Hello World');

// 최대 1초 대기...
$browser->waitForText('Hello World', 1);
```

텍스트가 사라질 때까지 기다리려면 `waitUntilMissingText` 메서드를 사용하세요:

```php
// 최대 5초 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기 (Waiting for Links)

특정 링크 텍스트가 페이지에 표시될 때까지 기다리려면 `waitForLink` 메서드를 사용합니다:

```php
// 최대 5초 대기...
$browser->waitForLink('Create');

// 최대 1초 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기 (Waiting for Inputs)

입력 필드가 표시될 때까지 대기하려면 `waitForInput` 메서드를 사용합니다:

```php
// 최대 5초 대기...
$browser->waitForInput($field);

// 최대 1초 대기...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기 (Waiting on the Page Location)

`assertPathIs` 같은 경로 어설션 시, `window.location.pathname` 값이 비동기적으로 업데이트돼 실패할 수 있습니다. 이때 `waitForLocation`으로 위치가 변할 때까지 기다립니다:

```php
$browser->waitForLocation('/secret');
```

전체 URL로도 사용할 수 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[이름 있는 라우트](/docs/12.x/routing#named-routes)도 대기할 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기 (Waiting for Page Reloads)

액션 후 페이지가 리로드될 때까지 기다리려면 `waitForReload`을 사용합니다:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭+리로드는 편의를 위해 `clickAndWaitForReload`도 제공합니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기 (Waiting on JavaScript Expressions)

JavaScript 표현식이 `true`가 될 때까지 기다리려면 `waitUntil` 메서드를 사용하세요. `return` 문이나 세미콜론은 생략해도 됩니다:

```php
// 최대 5초 대기...
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기 (Waiting on Vue Expressions)

`waitUntilVue`와 `waitUntilVueIsNot` 메서드로 [Vue 컴포넌트](https://vuejs.org)의 데이터 속성 값이 지정한 상태가 될 때까지 대기할 수 있습니다:

```php
// 지정 값이 될 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 해당 값이 아닐 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기 (Waiting for JavaScript Events)

`waitForEvent` 메서드로 지정한 JavaScript 이벤트가 발생할 때까지 대기할 수 있습니다:

```php
$browser->waitForEvent('load');
```

기본 대기 범위는 `body` 요소지만, 스코프가 지정되면 해당 요소에 이벤트 리스너가 붙습니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    $iframe->waitForEvent('load');
});
```

특정 셀렉터에 직접 이벤트 리스너를 붙이고 싶다면 두 번째 인자로 지정하세요:

```php
$browser->waitForEvent('load', '.selector');
```

`document`나 `window` 객체의 이벤트도 기다릴 수 있습니다:

```php
// 문서 스크롤 이벤트 대기...
$browser->waitForEvent('scroll', 'document');

// 윈도우 리사이즈 이벤트 최대 5초 대기...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 함수와 함께 대기하기 (Waiting With a Callback)

많은 대기 메서드들은 내부적으로 `waitUsing` 메서드를 사용합니다. 직접 사용해도 되며, 클로저가 `true`를 반환할 때까지 최대 대기시간과 폴링 간격을 지정해 대기합니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 뷰로 스크롤하기 (Scrolling an Element Into View)

뷰 영역 밖에 있어 클릭할 수 없는 요소가 있을 수 있습니다. `scrollIntoView` 메서드는 해당 요소가 보이도록 스크롤합니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어설션을 제공합니다. 아래는 주요 어설션 목록입니다:

[assertTitle](#assert-title)  
[assertTitleContains](#assert-title-contains)  
[assertUrlIs](#assert-url-is)  
[assertSchemeIs](#assert-scheme-is)  
[assertSchemeIsNot](#assert-scheme-is-not)  
[assertHostIs](#assert-host-is)  
[assertHostIsNot](#assert-host-is-not)  
[assertPortIs](#assert-port-is)  
[assertPortIsNot](#assert-port-is-not)  
[assertPathBeginsWith](#assert-path-begins-with)  
[assertPathEndsWith](#assert-path-ends-with)  
[assertPathContains](#assert-path-contains)  
[assertPathIs](#assert-path-is)  
[assertPathIsNot](#assert-path-is-not)  
[assertRouteIs](#assert-route-is)  
[assertQueryStringHas](#assert-query-string-has)  
[assertQueryStringMissing](#assert-query-string-missing)  
[assertFragmentIs](#assert-fragment-is)  
[assertFragmentBeginsWith](#assert-fragment-begins-with)  
[assertFragmentIsNot](#assert-fragment-is-not)  
[assertHasCookie](#assert-has-cookie)  
[assertHasPlainCookie](#assert-has-plain-cookie)  
[assertCookieMissing](#assert-cookie-missing)  
[assertPlainCookieMissing](#assert-plain-cookie-missing)  
[assertCookieValue](#assert-cookie-value)  
[assertPlainCookieValue](#assert-plain-cookie-value)  
[assertSee](#assert-see)  
[assertDontSee](#assert-dont-see)  
[assertSeeIn](#assert-see-in)  
[assertDontSeeIn](#assert-dont-see-in)  
[assertSeeAnythingIn](#assert-see-anything-in)  
[assertSeeNothingIn](#assert-see-nothing-in)  
[assertCount](#assert-count)  
[assertScript](#assert-script)  
[assertSourceHas](#assert-source-has)  
[assertSourceMissing](#assert-source-missing)  
[assertSeeLink](#assert-see-link)  
[assertDontSeeLink](#assert-dont-see-link)  
[assertInputValue](#assert-input-value)  
[assertInputValueIsNot](#assert-input-value-is-not)  
[assertChecked](#assert-checked)  
[assertNotChecked](#assert-not-checked)  
[assertIndeterminate](#assert-indeterminate)  
[assertRadioSelected](#assert-radio-selected)  
[assertRadioNotSelected](#assert-radio-not-selected)  
[assertSelected](#assert-selected)  
[assertNotSelected](#assert-not-selected)  
[assertSelectHasOptions](#assert-select-has-options)  
[assertSelectMissingOptions](#assert-select-missing-options)  
[assertSelectHasOption](#assert-select-has-option)  
[assertSelectMissingOption](#assert-select-missing-option)  
[assertValue](#assert-value)  
[assertValueIsNot](#assert-value-is-not)  
[assertAttribute](#assert-attribute)  
[assertAttributeMissing](#assert-attribute-missing)  
[assertAttributeContains](#assert-attribute-contains)  
[assertAttributeDoesntContain](#assert-attribute-doesnt-contain)  
[assertAriaAttribute](#assert-aria-attribute)  
[assertDataAttribute](#assert-data-attribute)  
[assertVisible](#assert-visible)  
[assertPresent](#assert-present)  
[assertNotPresent](#assert-not-present)  
[assertMissing](#assert-missing)  
[assertInputPresent](#assert-input-present)  
[assertInputMissing](#assert-input-missing)  
[assertDialogOpened](#assert-dialog-opened)  
[assertEnabled](#assert-enabled)  
[assertDisabled](#assert-disabled)  
[assertButtonEnabled](#assert-button-enabled)  
[assertButtonDisabled](#assert-button-disabled)  
[assertFocused](#assert-focused)  
[assertNotFocused](#assert-not-focused)  
[assertAuthenticated](#assert-authenticated)  
[assertGuest](#assert-guest)  
[assertAuthenticatedAs](#assert-authenticated-as)  
[assertVue](#assert-vue)  
[assertVueIsNot](#assert-vue-is-not)  
[assertVueContains](#assert-vue-contains)  
[assertVueDoesntContain](#assert-vue-doesnt-contain)

<a name="assert-title"></a>
#### assertTitle

페이지 타이틀이 지정한 텍스트와 일치함을 단언합니다:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 타이틀에 지정한 텍스트가 포함됨을 단언합니다:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 문자열 제외)이 지정 문자열과 일치함을 단언합니다:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 지정한 스킴과 일치함을 단언합니다:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 지정한 스킴과 일치하지 않음을 단언합니다:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트가 지정한 호스트와 일치함을 단언합니다:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트가 지정한 호스트와 일치하지 않음을 단언합니다:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 지정한 포트와 일치함을 단언합니다:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 지정한 포트와 일치하지 않음을 단언합니다:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로가 지정 경로로 시작함을 단언합니다:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

현재 URL 경로가 지정 경로로 끝남을 단언합니다:

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

현재 URL 경로가 지정 경로를 포함함을 단언합니다:

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 지정 경로와 일치함을 단언합니다:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 지정 경로와 일치하지 않음을 단언합니다:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 지정한 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)와 일치함을 단언합니다:

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

쿼리 문자열에 지정 파라미터가 존재함을 단언합니다:

```php
$browser->assertQueryStringHas($name);
```

지정 파라미터가 특정 값임도 단언할 수 있습니다:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

쿼리 문자열에 지정 파라미터가 없음을 단언합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

현재 URL 해시 조각이 지정 조각과 일치함을 단언합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

현재 URL 해시 조각이 지정 조각으로 시작함을 단언합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

현재 URL 해시 조각이 지정 조각과 일치하지 않음을 단언합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

암호화된 쿠키가 존재함을 단언합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

암호화되지 않은 쿠키가 존재함을 단언합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

암호화된 쿠키가 없음을 단언합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

암호화되지 않은 쿠키가 없음을 단언합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키가 특정 값을 갖음을 단언합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키가 특정 값을 갖음을 단언합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

페이지에 지정한 텍스트가 보임을 단언합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

페이지에 지정한 텍스트가 보이지 않음을 단언합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

선택자 범위 내에 지정한 텍스트가 보임을 단언합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

선택자 범위 내에 지정한 텍스트가 없음을 단언합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

선택자 범위 내에 어떤 텍스트라도 존재함을 단언합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

선택자 범위 내에 텍스트가 전혀 없음을 단언합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### assertCount

선택자와 매칭되는 요소가 지정된 개수만큼 존재함을 단언합니다:

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### assertScript

지정한 JavaScript 표현식이 지정 값과 일치함을 단언합니다:

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지 소스 안에 특정 코드가 포함됨을 단언합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지 소스 안에 특정 코드가 없음을 단언합니다:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

페이지 내에 지정한 링크 텍스트가 존재함을 단언합니다:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

페이지 내에 지정한 링크 텍스트가 존재하지 않음을 단언합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

입력 필드가 지정한 값을 갖고 있음을 단언합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

입력 필드가 지정한 값을 갖고 있지 않음을 단언합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

지정한 체크박스가 체크되어 있음을 단언합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

지정한 체크박스가 체크되어 있지 않음을 단언합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

지정한 체크박스가 결정되지 않은(중간) 상태임을 단언합니다:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

지정한 라디오 버튼이 선택되어 있음을 단언합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

지정한 라디오 버튼이 선택되어 있지 않음을 단언합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

지정한 드롭다운이 특정 값을 선택하고 있음을 단언합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

지정한 드롭다운이 특정 값을 선택하고 있지 않음을 단언합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

드롭다운에 지정한 옵션 배열이 존재함을 단언합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

드롭다운에 지정한 옵션 배열이 없음을 단언합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

지정한 드롭다운에 특정 옵션이 존재함을 단언합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

지정한 드롭다운에 특정 옵션이 없음을 단언합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

주어진 선택자에 해당하는 요소가 특정 값을 갖고 있음을 단언합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

주어진 선택자에 해당하는 요소가 특정 값을 갖고 있지 않음을 단언합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

주어진 선택자에 해당하는 요소가 특정 속성에 지정한 값을 갖고 있음을 단언합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

주어진 선택자에 해당하는 요소가 특정 속성을 갖고 있지 않음을 단언합니다:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

주어진 선택자에 해당하는 요소가 특정 속성에 지정한 값을 포함함을 단언합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

주어진 선택자에 해당하는 요소가 특정 속성에 지정한 값을 포함하지 않음을 단언합니다:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

주어진 선택자에 해당하는 요소가 `aria` 속성에 지정한 값을 갖고 있음을 단언합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 마크업에 대해:

```php
$browser->assertAriaAttribute('button', 'label', 'Add');
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

주어진 선택자에 해당하는 요소가 `data` 속성에 지정한 값을 갖고 있음을 단언합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 마크업에 대해:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees');
```

<a name="assert-visible"></a>
#### assertVisible

선택자에 해당하는 요소가 화면에 표시됨을 단언합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

선택자에 해당하는 요소가 페이지 소스에 존재함을 단언합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

선택자에 해당하는 요소가 페이지 소스에 존재하지 않음을 단언합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

선택자에 해당하는 요소가 화면에 보이지 않음을 단언합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

이름이 지정된 입력 요소가 존재함을 단언합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

이름이 지정된 입력 요소가 페이지 소스에 없음을 단언합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

지정한 메시지를 가진 JavaScript 대화상자가 열렸음을 단언합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

지정한 필드가 활성화되어 있음을 단언합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

지정한 필드가 비활성화되어 있음을 단언합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

지정한 버튼이 활성화되어 있음을 단언합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

지정한 버튼이 비활성화되어 있음을 단언합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

지정한 필드가 포커스를 받고 있음을 단언합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

지정한 필드가 포커스를 받고 있지 않음을 단언합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태임을 단언합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태임을 단언합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

사용자가 지정한 사용자로 인증된 상태임을 단언합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 [Vue 컴포넌트](https://vuejs.org)의 상태 어설션도 지원합니다. 예를 들어 다음 Vue 컴포넌트가 있다고 가정합시다:

```
// HTML...

<profile dusk="profile-component"></profile>

// 컴포넌트 정의...

Vue.component('profile', {
    template: '<div>{{ user.name }}</div>',

    data: function () {
        return {
            user: {
                name: 'Taylor'
            }
        };
    }
});
```

다음과 같이 컴포넌트 상태를 어설션할 수 있습니다:

```php tab=Pest
test('vue', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
});
```

```php tab=PHPUnit
/**
 * 기본 Vue 테스트 예제.
 */
public function test_vue(): void
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
#### assertVueIsNot

Vue 컴포넌트의 데이터 속성이 특정 값이 아님을 단언합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트의 데이터가 배열이고, 지정 값이 포함됨을 단언합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

Vue 컴포넌트의 데이터가 배열이고, 지정 값이 포함되지 않음을 단언합니다:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

복잡한 테스트에서는 여러 동작을 순차적으로 실행하는 경우가 많아 테스트가 어렵게 읽힐 수 있습니다. Dusk의 페이지 객체 기능을 활용하면, 페이지별 행동을 별도 메서드로 정의하여 테스트를 더 깔끔하고 표현력 있게 만들 수 있습니다. 또한, 페이지에서 자주 사용되는 셀렉터 단축도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체는 `dusk:page` Artisan 명령어로 생성합니다. 생성된 페이지 클래스는 `tests/Browser/Pages` 디렉터리에 위치합니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

기본적으로 페이지에는 `url`, `assert`, `elements` 3가지 메서드가 있습니다. 여기서는 `url`과 `assert` 메서드를 설명합니다. `elements` 메서드는 [단축 셀렉터](#shorthand-selectors) 항목에서 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

페이지가 대표하는 URL 경로를 반환합니다. Dusk는 이 URL을 통해 해당 페이지로 네비게이션합니다:

```php
/**
 * 페이지 URL 반환.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

브라우저가 실제로 해당 페이지에 있음을 검증하기 위한 어설션을 수행합니다. 반드시 메서드 구현이 필요하진 않지만, 존재할 경우 `visit` 등으로 페이지에 접근 시 자동 실행됩니다:

```php
/**
 * 페이지 위치 검증.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지 네비게이션 (Navigating to Pages)

페이지 객체를 정의한 후, `visit` 메서드에 페이지 인스턴스를 전달해 바로 방문할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 특정 페이지에 있을 때 해당 페이지의 셀렉터와 메서드를 현재 테스트 컨텍스트에 불러오려면 `on` 메서드를 사용합니다. 예를 들어 버튼 클릭 후 리다이렉트되어 페이지 내비게이션이 명시적으로 호출되지 않은 경우 유용합니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터 (Shorthand Selectors)

페이지 클래스 내 `elements` 메서드에서 페이지 내 특정 CSS 셀렉터에 대한 별칭(별명)을 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드에 단축 셀렉터를 만들어 봅시다:

```php
/**
 * 페이지에서 사용할 셀렉터 별칭 반환.
 *
 * @return array<string, string>
 */
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

정의하면 이러한 별칭을 CSS 셀렉터 대신 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 셀렉터 (Global Shorthand Selectors)

Dusk 설치 시 `tests/Browser/Pages` 내 베이스 `Page` 클래스에 존재하는 `siteElements` 메서드를 이용해 애플리케이션 모든 페이지에서 공통으로 사용할 단축 셀렉터를 정의할 수 있습니다:

```php
/**
 * 사이트 전역에서 사용할 셀렉터 별칭 반환.
 *
 * @return array<string, string>
 */
public static function siteElements(): array
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### 페이지 메서드 (Page Methods)

기본 메서드 외에 페이지 클래스에 여러 메서드를 정의해 테스트에서 활용할 수 있습니다. 예를 들어 음악 관리 애플리케이션에서 플레이리스트 생성 로직을 한번만 작성하려면 다음처럼 메서드를 만듭니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 다른 페이지 메서드들...

    /**
     * 새로운 플레이리스트 생성.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

정의 후, 해당 페이지를 이용하는 테스트에서 메서드를 호출할 수 있습니다. 첫 번째 인자로 브라우저 인스턴스가 자동으로 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 페이지 객체와 비슷하지만, 네비게이션 URL과는 무관하게 애플리케이션 전반에서 반복 사용하는 UI나 기능 단위를 위한 것입니다. 예를 들어 내비게이션 바나 알림 창 등이 있습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트는 `dusk:component` Artisan 명령어로 생성합니다. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 위치합니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어 날짜 선택기 컴포넌트는 여러 테스트에서 날짜 선택 로직을 중복 작성하지 않도록 캡슐화할 수 있습니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * 컴포넌트 루트 셀렉터 반환.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * 페이지 내 컴포넌트 존재 여부 확인.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 내 요소 별칭 반환.
     *
     * @return array<string, string>
     */
    public function elements(): array
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

    /**
     * 지정 날짜 선택.
     */
    public function selectDate(Browser $browser, int $year, int $month, int $day): void
    {
        $browser->click('@date-field')
            ->within('@year-list', function (Browser $browser) use ($year) {
                $browser->click($year);
            })
            ->within('@month-list', function (Browser $browser) use ($month) {
                $browser->click($month);
            })
            ->within('@day-list', function (Browser $browser) use ($day) {
                $browser->click($day);
            });
    }
}
```

<a name="using-components"></a>
### 컴포넌트 사용법 (Using Components)

컴포넌트가 있으면 날짜 선택기 같은 UI 조작을 테스트에서 쉽게 재사용할 수 있습니다. 만약 날짜 선택 로직이 바뀌면 컴포넌트만 수정하면 됩니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

uses(DatabaseMigrations::class);

test('basic example', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->within(new DatePicker, function (Browser $browser) {
                $browser->selectDate(2019, 1, 30);
            })
            ->assertSee('January');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    /**
     * 기본 컴포넌트 테스트 예제.
     */
    public function test_basic_example(): void
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                ->within(new DatePicker, function (Browser $browser) {
                    $browser->selectDate(2019, 1, 30);
                })
                ->assertSee('January');
        });
    }
}
```

`component` 메서드로 지정 컴포넌트에 범위가 한정된 브라우저 인스턴스도 얻을 수 있습니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## CI 환경에서 사용하기 (Continuous Integration)

> [!WARNING]
> 대부분 Dusk CI 구성은 빌트인 PHP 개발 서버를 8000포트에서 실행하는 환경을 전제로 합니다. 따라서 CI 환경에 `APP_URL` 환경 변수를 `http://127.0.0.1:8000`으로 설정해야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행 (Heroku CI)

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, `app.json` 파일에 다음 Chrome 빌드팩과 스크립트를 추가하세요:

```json
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-chrome-for-testing" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux --port=9515 > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
### Travis CI에서 테스트 실행 (Travis CI)

Travis CI는 GUI 환경이 아니므로 Chrome 브라우저 실행을 위해 추가 구성이 필요합니다. PHP 내장 서버는 `php artisan serve`로 실행합니다. `.travis.yml` 예시는 다음과 같습니다:

```yaml
language: php

php:
  - 8.2

addons:
  chrome: stable

install:
  - cp .env.testing .env
  - travis_retry composer install --no-interaction --prefer-dist
  - php artisan key:generate
  - php artisan dusk:chrome-driver

before_script:
  - google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
  - php artisan serve --no-reload &

script:
  - php artisan dusk
```

<a name="running-tests-on-github-actions"></a>
### GitHub Actions에서 테스트 실행 (GitHub Actions)

[GitHub Actions](https://github.com/features/actions)에서도 `php artisan serve`로 PHP 내장 서버를 띄워 Dusk 테스트를 실행합니다. 기본 예시는 다음과 같습니다:

```yaml
name: CI
on: [push]
jobs:

  dusk-php:
    runs-on: ubuntu-latest
    env:
      APP_URL: "http://127.0.0.1:8000"
      DB_USERNAME: root
      DB_PASSWORD: root
      MAIL_MAILER: log
    steps:
      - uses: actions/checkout@v4
      - name: Prepare The Environment
        run: cp .env.example .env
      - name: Create Database
        run: |
          sudo systemctl start mysql
          mysql --user="root" --password="root" -e "CREATE DATABASE \`my-database\` character set UTF8mb4 collate utf8mb4_bin;"
      - name: Install Composer Dependencies
        run: composer install --no-progress --prefer-dist --optimize-autoloader
      - name: Generate Application Key
        run: php artisan key:generate
      - name: Upgrade Chrome Driver
        run: php artisan dusk:chrome-driver --detect
      - name: Start Chrome Driver
        run: ./vendor/laravel/dusk/bin/chromedriver-linux --port=9515 &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: console
          path: tests/Browser/console
```

<a name="running-tests-on-chipper-ci"></a>
### Chipper CI에서 테스트 실행 (Chipper CI)

[Chipper CI](https://chipperci.com)에서도 PHP 내장 서버를 이용해 Laravel을 실행하고 테스트할 수 있습니다. 기본 구성을 예시로 들면 다음과 같습니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Chrome 포함 환경 설정
services:
  - dusk

# 모든 커밋 빌드
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Dusk 환경 파일을 생성하고 APP_URL을 BUILD_HOST로 설정
      cp -v .env .env.dusk.ci
      sed -i "s@APP_URL=.*@APP_URL=http://$BUILD_HOST:8000@g" .env.dusk.ci

  - name: Compile Assets
    cmd: |
      npm ci --no-audit
      npm run build

  - name: Browser Tests
    cmd: |
      php -S [::0]:8000 -t public 2>server.log &
      sleep 2
      php artisan dusk:chrome-driver $CHROME_DRIVER
      php artisan dusk --env=ci
```

Chipper CI에서 Dusk를 실행하며 데이터베이스 등도 사용할 경우 공식 문서(https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.