# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 설정 관리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 촬영](#taking-a-screenshot)
    - [콘솔 출력 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [엘리먼트와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [자바스크립트 대화상자](#javascript-dialogs)
    - [인라인 프레임 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기](#waiting-for-elements)
    - [엘리먼트 스크롤하여 보기](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 구성](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [축약 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 쉽게 사용할 수 있는 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK 또는 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 물론, 원한다면 다른 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]  
> Dusk 서비스 프로바이더를 수동으로 등록하는 경우, 절대 프로덕션 환경에서 등록해서는 안 됩니다. 이렇게 하면 임의 사용자가 애플리케이션에 인증할 수 있는 보안 문제가 발생할 수 있습니다.

Dusk 패키지를 설치한 후에는 `dusk:install` Artisan 명령어를 실행하세요. 이 명령은 `tests/Browser` 디렉토리와 Dusk 테스트 예제, 그리고 사용 중인 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근하는 URL과 일치해야 합니다.

> [!NOTE]  
> 만약 [Laravel Sail](/docs/11.x/sail)을 로컬 개발 환경 관리에 사용하고 있다면, Sail 문서의 [Dusk 테스트 설정 및 실행](/docs/11.x/sail#laravel-dusk)도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어로 설치되는 ChromeDriver와 다른 버전을 설치하려면 `dusk:chrome-driver` 명령을 사용할 수 있습니다:

```shell
# OS에 맞는 최신 버전 설치...
php artisan dusk:chrome-driver

# 특정 버전 설치 (예: 86)...
php artisan dusk:chrome-driver 86

# 지원하는 모든 OS용 특정 버전 설치...
php artisan dusk:chrome-driver --all

# OS에서 감지된 Chrome/Chromium 버전에 맞는 버전 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]  
> Dusk는 `chromedriver` 바이너리가 실행 권한을 가지고 있어야 합니다. Dusk 실행에 문제가 있다면, 아래 명령어로 권한을 확인하고 설정하세요:  
> `chmod -R 0755 vendor/laravel/dusk/bin/`

<a name="using-other-browsers"></a>
### 다른 브라우저 사용 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용해 브라우저 테스트를 수행합니다. 하지만 원하는 경우 Selenium 서버를 직접 띄워 다른 브라우저에 대해 테스트할 수도 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 열고, `startChromeDriver` 호출을 제거하세요. 이렇게 하면 Dusk가 자동으로 ChromeDriver를 시작하지 않습니다:

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

그리고 `driver` 메서드를 수정해 원하는 URL과 포트에 연결하도록 하며, WebDriver에 전달할 "desired capabilities"도 조정할 수 있습니다:

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

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용합니다. 생성된 테스트는 `tests/Browser` 디렉토리에 놓입니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 가져오는 페이지와 상호작용하므로, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. 이 트레이트는 데이터베이스 트랜잭션을 활용하지만, HTTP 요청 간에는 적용되지 않기 때문입니다. 대신 두 가지 옵션이 있습니다: `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용하기

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 테스트마다 테이블을 삭제하고 재생성하는 것은 일반적으로 테이블 내용을 비우는 것보다 느릴 수 있습니다:

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
> SQLite 인-메모리 데이터베이스는 Dusk 테스트 실행 시 사용할 수 없습니다. 브라우저는 별도의 프로세스에서 실행되므로, 다른 프로세스의 인-메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 내용 비우기 사용하기

`DatabaseTruncation` 트레이트는 첫 번째 테스트 때 데이터베이스를 마이그레이션해서 테이블이 생성되도록 하고, 이후 테스트에서는 테이블 내용을 비워 속도를 향상시킵니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 비웁니다. 비울 테이블을 지정하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

> [!NOTE]  
> Pest를 사용하는 경우, 이 속성은 기본 `DuskTestCase` 클래스 또는 테스트가 확장하는 클래스에 정의해야 합니다.

```php
/**
 * 비울 테이블 지정
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는, 비우지 않을 테이블을 지정하는 `$exceptTables` 속성을 정의할 수도 있습니다:

```php
/**
 * 비우지 않을 테이블 지정
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

비울 데이터베이스 커넥션을 지정하려면 `$connectionsToTruncate` 속성을 정의하세요:

```php
/**
 * 테이블 내용을 비울 커넥션 지정
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 테이블 내용 비우기 전후에 실행할 코드를 넣으려면 각각 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의하세요:

```php
/**
 * 데이터베이스 테이블 내용 비우기 전 수행할 작업
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * 데이터베이스 테이블 내용 비우기 후 수행할 작업
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

이전에 `dusk` 명령어 실행 시 실패한 테스트가 있다면, 먼저 실패한 테스트만 다시 실행해 시간을 절약할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 러너에서 허용하는 인수를 모두 받아들입니다. 예를 들어 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group) 테스트만 실행하도록 할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]  
> [Laravel Sail](/docs/11.x/sail)로 로컬 개발 환경을 관리하는 경우, Sail 문서 내 [Dusk 테스트 설정 및 실행](/docs/11.x/sail#laravel-dusk)을 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려 시도합니다. 만약 환경에 맞지 않는다면, `dusk` 명령 실행 전에 ChromeDriver를 수동으로 시작할 수 있습니다. 수동으로 시작한다면 `tests/DuskTestCase.php` 파일에서 다음 코드를 주석 처리하세요:

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

만약 ChromeDriver를 9515 이외 포트에서 시작했다면, 같은 클래스 내 `driver` 메서드를 수정해 포트를 맞춰줘야 합니다:

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
### 환경 설정 관리 (Environment Handling)

Dusk가 테스트 실행 시 별도의 환경 파일을 사용하도록 강제하려면 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하세요. 예를 들어 로컬 환경에서 `dusk` 명령을 실행한다면 `.env.dusk.local` 파일을 만들어야 합니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고 `.env.dusk.*` 파일을 `.env`로 이름을 바꿉니다. 테스트가 끝나면 원래 `.env` 파일로 복원합니다.

<a name="browser-basics"></a>
## 브라우저 기본 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성 (Creating Browsers)

간단한 로그인 기능 테스트를 작성해 봅시다. 테스트 생성 후 로그인 페이지로 이동해 자격증명을 입력하고 "Login" 버튼을 누르는 동작을 추가할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내에서 `browse` 메서드를 호출하세요:

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
     * 기본적인 브라우저 테스트 예제.
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

위 예제에서 볼 수 있듯, `browse` 메서드는 클로저를 전달받아 Dusk가 자동으로 브라우저 인스턴스를 넘깁니다. 이 브라우저 객체를 사용해 애플리케이션과 상호작용하거나 어설션을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성하기

특정 테스트에서는 여러 브라우저 인스턴스가 필요할 수 있습니다. 예를 들어 웹소켓이 연결된 채팅 화면 테스트 시 유용합니다. 이러한 경우 `browse` 메서드에 전달하는 클로저의 시그니처에 추가로 브라우저 인수를 넣으면 됩니다:

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

`visit` 메서드를 사용하면 주어진 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

`visitRoute` 메서드를 활용하면 [이름있는 라우트](/docs/11.x/routing#named-routes)로 이동할 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

뒤로 가기와 앞으로 가기는 각각 `back`과 `forward` 메서드를 사용하세요:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드로 페이지를 새로 고침할 수 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

브라우저 창 크기를 바꾸려면 `resize` 메서드를 사용하세요:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 크기를 내용에 맞게 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 크기를 내용에 맞게 조정한 뒤 스크린샷을 찍습니다. 이 기능을 끄려면 테스트 중 `disableFitOnFailure` 메서드를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 브라우저 창 위치를 이동할 수도 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 이용하세요. 보통은 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Dusk 브라우저 매크로 등록
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

`macro`의 첫 번째 인자는 메서드 이름이고, 두 번째는 실행할 클로저입니다. 이후 `Browser` 인스턴스에서 해당 이름의 메서드를 사용할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

로그인해야 하는 페이지 테스트 시 매번 로그인 화면과 상호작용할 필요가 없도록, Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델의 기본 키나 모델 인스턴스를 인수로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]  
> `loginAs` 메서드를 사용하면, 사용자 세션이 테스트 파일 내 모든 테스트에서 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드로 암호화된 쿠키 값을 가져오거나 설정할 수 있습니다. 기본적으로 Laravel이 만드는 쿠키는 모두 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` 메서드는 암호화되지 않은 쿠키 값을 다룹니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메서드로 지정한 쿠키를 제거할 수 있습니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행 (Executing JavaScript)

`script` 메서드를 이용하면 브라우저 내에서 임의의 JavaScript 코드를 실행할 수 있습니다:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 촬영 (Taking a Screenshot)

`screenshot` 메서드로 스크린샷을 찍고 지정한 파일명으로 저장합니다. 스크린샷은 모두 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 브레이크포인트에서 일련의 스크린샷을 찍습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드는 페이지 내 특정 엘리먼트의 스크린샷을 찍습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장 (Storing Console Output to Disk)

현재 브라우저의 콘솔 출력을 파일로 저장하려면 `storeConsoleLog` 메서드를 사용합니다. 콘솔 출력은 `tests/Browser/console` 디렉토리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장 (Storing Page Source to Disk)

`storeSource` 메서드를 사용하면 현재 페이지의 소스 코드를 파일로 저장할 수 있습니다. 저장 위치는 `tests/Browser/source` 디렉토리입니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

엘리먼트와 상호작용하기 위한 적절한 CSS 셀렉터 선택은 어려운 작업입니다. 프론트엔드 코드가 변경되면 다음과 같은 복잡한 셀렉터가 깨질 수 있습니다:

```html
<!-- HTML... -->

<button>Login</button>
```

```php
// 테스트...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터 대신 명확한 이름으로 엘리먼트를 지정할 수 있어 테스트 유지보수가 쉬워집니다. 엘리먼트에 `dusk` 속성을 추가하고, 테스트에서는 `@`를 붙여 셀렉터로 사용하세요:

```html
<!-- HTML... -->

<button dusk="login-button">Login</button>
```

```php
// 테스트...

$browser->click('@login-button');
```

필요하다면, `selectorHtmlAttribute` 메서드로 Dusk가 사용하는 HTML 속성을 변경할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정

Dusk는 페이지 내 엘리먼트의 현재 값, 표시 텍스트, 속성을 쉽게 다룰 수 있도록 여러 메서드를 제공합니다. 예를 들어, 지정한 CSS 또는 Dusk 셀렉터에 해당하는 엘리먼트의 `value` 값을 가져오려면 `value` 메서드를 사용하세요:

```php
// 값 조회...
$value = $browser->value('selector');

// 값 설정...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 이름이 지정된 입력 필드의 값을 가져옵니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 조회

`text` 메서드는 지정한 셀렉터에 해당하는 엘리먼트의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 조회

`attribute` 메서드는 셀렉터에 해당하는 엘리먼트의 특정 속성 값을 가져옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력

Dusk는 폼 요소와 입력을 조작하는 다양한 메서드를 제공합니다. 간단한 입력 필드에 텍스트를 타이핑하는 예제입니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

`type` 메서드는 CSS 셀렉터를 받을 수 있으나 반드시 필요하지 않습니다. 셀렉터가 없으면, `name` 속성이 일치하는 `input` 또는 `textarea` 를 자동으로 찾습니다.

기존 내용에 덧붙여 입력하려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력 값을 비우려면 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드를 사용하면 키 입력 사이에 딜레이를 넣어 천천히 입력할 수 있습니다. 기본 딜레이는 100 밀리초이며, 세 번째 인수로 조절할 수 있습니다:

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
#### 드롭다운 선택

`select` 메서드를 사용하여 `select` 요소 내 옵션을 선택할 수 있습니다. `type` 메서드와 마찬가지로 전체 CSS 셀렉터는 필요하지 않습니다. 전달하는 값은 옵션의 표시 텍스트가 아니라 내부 값이어야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인자를 생략하면 무작위 옵션을 선택합니다:

```php
$browser->select('size');
```

두 번째 인자로 배열을 넘겨 여러 옵션을 선택할 수도 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

`check` 메서드는 체크박스를 선택합니다. CSS 셀렉터가 없으면 `name` 속성이 일치하는 체크박스를 찾습니다:

```php
$browser->check('terms');
```

`uncheck` 메서드는 체크를 해제합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

`radio` 메서드는 라디오 버튼을 선택합니다. CSS 셀렉터가 없으면 `name` 및 `value` 속성이 일치하는 라디오 버튼을 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

`attach` 메서드를 사용하면 파일 입력 필드에 파일을 첨부할 수 있습니다. CSS 셀렉터가 없으면 `name` 속성이 일치하는 `file` 입력 요소를 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]  
> `attach` 함수 사용 시 서버에 `Zip` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드는 페이지 내 버튼을 클릭합니다. 인자로는 버튼의 표시 텍스트나 CSS / Dusk 셀렉터를 사용할 수 있습니다:

```php
$browser->press('Login');
```

폼 제출 시 버튼을 누른 뒤 비활성화 되었다가 다시 활성화 될 때까지 기다려야 한다면, `pressAndWaitFor` 메서드를 사용하세요:

```php
// 최대 5초 동안 버튼이 활성화되길 기다림...
$browser->pressAndWaitFor('Save');

// 최대 1초 동안 버튼이 활성화되길 기다림...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 표시 텍스트가 일치하는 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

링크가 페이지에 보이는지 확인하려면 `seeLink` 메서드를 사용합니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]  
> 이 메서드들은 jQuery와 상호작용합니다. 페이지 내 jQuery가 없으면, Dusk가 자동으로 테스트 실행 동안 jQuery를 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용 (Using the Keyboard)

`keys` 메서드는 `type` 메서드보다 복잡한 키 입력을 할 수 있습니다. 예를 들어 modifier 키를 누른 상태로 타이핑할 수 있습니다. 아래 예제는 `shift` 키를 누른 채 `taylor`를 입력한 뒤, modifier 없이 `swift`를 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또한, 특정 CSS 셀렉터에 "키보드 단축키" 조합을 보낼 수도 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]  
> `{command}` 같은 modifier 키는 `{}`로 감싸며, `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수 이름과 일치합니다. ([GitHub 링크](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php))

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk는 `withKeyboard` 메서드로 `Laravel\Dusk\Keyboard` 클래스를 사용해 복잡한 키보드 이벤트를 유창하게 작성할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다:

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
#### 키보드 매크로

키보드 상호작용을 재사용 가능한 커스텀 메서드로 정의하려면 `Keyboard` 클래스가 제공하는 `macro` 메서드를 사용하세요. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
     * Dusk 키보드 매크로 등록
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

첫 번째 인자에 이름, 두 번째 인자에 클로저를 전달하며, 키보드 인스턴스에서 해당 이름의 메서드로 실행됩니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 엘리먼트 클릭

`click` 메서드는 CSS 또는 Dusk 셀렉터에 해당하는 엘리먼트를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식에 해당하는 엘리먼트를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저에서 보이는 영역 좌표를 기준으로 특정 위치의 가장 상단 엘리먼트를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드로 마우스 더블 클릭을 시뮬레이션할 수 있습니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` 메서드는 마우스 우클릭을 시뮬레이션합니다:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드는 마우스 클릭 상태를 유지합니다. 이후 `releaseMouse` 호출로 클릭을 해제합니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` 메서드는 `ctrl+클릭` 이벤트를 시뮬레이션합니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메서드를 사용해 마우스를 특정 엘리먼트 위로 이동시킬 수 있습니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 한 엘리먼트를 다른 엘리먼트로 드래그합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

다음과 같이 한 방향으로 드래그할 수도 있습니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

또는 오프셋을 기준으로 드래그하려면 `dragOffset` 메서드를 사용합니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 대화상자 (JavaScript Dialogs)

Dusk는 자바스크립트 대화상자와 상호작용할 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog` 메서드로 대화상자가 나타날 때까지 대기할 수 있으며, 인수로 최대 대기 시간을 초 단위로 지정할 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 대화상자가 뜨면서 특정 메시지가 포함된 것을 검증합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트 입력이 있는 대화상자라면 `typeInDialog` 메서드로 값을 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

열려 있는 대화상자를 "확인" 버튼을 눌러 닫으려면 `acceptDialog` 메서드를 호출하세요:

```php
$browser->acceptDialog();
```

"취소" 버튼을 눌러 닫으려면 `dismissDialog` 메서드를 호출합니다:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임 상호작용 (Interacting With Inline Frames)

iframe 내 엘리먼트와 상호작용해야 할 경우 `withinFrame` 메서드를 사용하세요. 이 메서드에 전달하는 클로저 내 모든 엘리먼트 조작은 지정한 iframe 컨텍스트 내에서 이루어집니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정 (Scoping Selectors)

특정 셀렉터 내에서 여러 작업을 수행해야 할 때는 `with` 메서드를 사용하세요. 클로저 내부 모든 작업은 원래 셀렉터 범위 내에서 이뤄집니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때로는 현재 범위 밖에서 어설션을 실행해야 할 수 있습니다. 이럴 때는 `elsewhere` 및 `elsewhereWhenAvailable` 메서드를 사용합니다:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 범위: body .table

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 범위: body .page-title
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 범위: body .page-title
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 엘리먼트 대기 (Waiting for Elements)

JavaScript를 많이 사용하는 앱에서는 특정 엘리먼트나 데이터가 나타날 때까지 기다려야 할 때가 많습니다. Dusk는 아래 다양한 메서드를 제공해 쉽게 대기할 수 있습니다.

<a name="waiting"></a>
#### 대기

특정 밀리초 동안 테스트를 잠시 멈추려면 `pause` 메서드를 사용하세요:

```php
$browser->pause(1000);
```

조건이 참일 때만 일시정지하려면 `pauseIf`를, 조건이 거짓일 때만 일시정지하려면 `pauseUnless`를 사용합니다:

```php
$browser->pauseIf(App::environment('production'), 1000);

$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor` 메서드를 사용하면 특정 CSS 또는 Dusk 셀렉터가 페이지에 표시될 때까지 대기할 수 있습니다. 기본 최대 시간은 5초이며, 두 번째 인수로 변경할 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitFor('.selector');

// 최대 1초 대기...
$browser->waitFor('.selector', 1);
```

특정 텍스트가 셀렉터 내에 나타날 때까지 기다리려면 `waitForTextIn`을 사용하세요:

```php
// 최대 5초 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

페이지에서 해당 셀렉터가 사라질 때까지 기다리려면 `waitUntilMissing`을 사용합니다:

```php
// 최대 5초 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 대기...
$browser->waitUntilMissing('.selector', 1);
```

셀렉터가 활성화 또는 비활성화 상태가 될 때까지도 기다릴 수 있습니다:

```php
// 활성화될 때까지 대기...
$browser->waitUntilEnabled('.selector');

// 비활성화될 때까지 대기...
$browser->waitUntilDisabled('.selector');
```

<a name="scoping-selectors-when-available"></a>
#### 사용 가능할 때 범위 지정

특정 셀렉터와 일치하는 엘리먼트가 나타날 때까지 기다렸다가 작업해야 할 경우 `whenAvailable` 메서드를 사용합니다. 클로저 내에서 수행하는 모든 작업은 해당 범위에 한정됩니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

특정 텍스트가 페이지에 나타날 때까지 기다리려면 `waitForText` 메서드를 사용하세요:

```php
// 최대 5초 대기...
$browser->waitForText('Hello World');

// 최대 1초 대기...
$browser->waitForText('Hello World', 1);
```

텍스트가 페이지에서 사라질 때까지 기다리려면 `waitUntilMissingText` 메서드를 사용합니다:

```php
// 최대 5초 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

특정 링크 텍스트가 나타날 때까지 기다리려면 `waitForLink`를 사용하세요:

```php
// 최대 5초 대기...
$browser->waitForLink('Create');

// 최대 1초 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

특정 입력 필드가 보일 때까지 기다리려면 `waitForInput`을 사용합니다:

```php
// 최대 5초 대기...
$browser->waitForInput($field);

// 최대 1초 대기...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기

`$browser->assertPathIs('/home')` 같은 경로 어설션은 `window.location.pathname`이 비동기 업데이트 될 경우 실패할 수 있습니다. 이럴 때 `waitForLocation` 메서드로 위치가 특정 값이 될 때까지 기다릴 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

완전한 URL도 대기할 수 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[이름 있는 라우트](`named route`)의 위치도 기다릴 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

액션 수행 후 페이지가 리로드 될 때까지 기다리려면 `waitForReload` 메서드를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 리로드 대기를 간편하게 하려면 `clickAndWaitForReload` 메서드를 쓰세요:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

테스트 실행을 일시 중지하고 특정 자바스크립트 표현식이 `true`가 될 때까지 대기하려면 `waitUntil` 메서드를 사용하세요. 표현식에 `return`이나 세미콜론은 포함하지 마세요:

```php
// 최대 5초 대기...
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

`waitUntilVue`와 `waitUntilVueIsNot` 메서드로 [Vue 컴포넌트](https://vuejs.org)의 속성 값이 특정 값이 되거나 안 될 때까지 대기할 수 있습니다:

```php
// 특정 값이 될 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 특정 값이 아닐 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기

`waitForEvent` 메서드는 지정한 자바스크립트 이벤트가 발생할 때까지 테스트를 일시 중지합니다:

```php
$browser->waitForEvent('load');
```

기본 이벤트 리스너는 스코프 범위의 `body` 엘리먼트에 붙습니다. 스코프 셀렉터가 지정된 경우 매칭되는 엘리먼트에 붙습니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe 로드 이벤트 대기...
    $iframe->waitForEvent('load');
});
```

두 번째 인자로 특정 셀렉터를 지정할 수도 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window` 객체 이벤트도 대기 가능합니다:

```php
// 문서 스크롤 대기...
$browser->waitForEvent('scroll', 'document');

// 최대 5초 동안 창 크기 변경 대기...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백과 대기

여러 Dusk "wait" 메서드는 내부적으로 `waitUsing` 메서드를 사용합니다. 직접 호출해 주어진 클로저가 `true`를 반환할 때까지 대기할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트 스크롤하여 보기 (Scrolling an Element Into View)

엘리먼트가 화면 보이는 영역 밖이라 클릭할 수 없을 때, `scrollIntoView` 메서드는 해당 엘리먼트가 화면에 보일 때까지 스크롤합니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk가 제공하는 다양한 어설션 메서드를 활용해 애플리케이션 상태를 검증할 수 있습니다. 주요 어설션 목록은 아래와 같습니다.

<!-- 이 부분 아래는 리스트로 구성되어 있으며 번역 유지 --> 

<div class="collection-method-list" markdown="1">

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

</div>

<a name="assert-title"></a>
#### assertTitle

페이지 제목이 주어진 텍스트와 일치하는지 검증합니다:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 제목에 주어진 텍스트가 포함되어 있는지 검증합니다:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 문자열 제외)이 주어진 문자열과 일치하는지 검증합니다:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 주어진 스킴과 일치하는지 검증합니다:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 주어진 스킴과 다름을 검증합니다:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트가 주어진 값과 일치하는지 검증합니다:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트가 주어진 값과 다른지 검증합니다:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 주어진 포트와 일치하는지 검증합니다:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 주어진 포트와 다름을 검증합니다:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 경로가 주어진 경로로 시작하는지 검증합니다:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

현재 경로가 주어진 경로로 끝나는지 검증합니다:

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

현재 경로에 주어진 경로가 포함되어 있는지 검증합니다:

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 주어진 경로와 일치하는지 검증합니다:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 주어진 경로와 다른지 검증합니다:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 주어진 [이름 있는 라우트](/docs/11.x/routing#named-routes) URL과 일치하는지 검증합니다:

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

주어진 쿼리 문자열 파라미터가 존재하는지 검증합니다:

```php
$browser->assertQueryStringHas($name);
```

주어진 파라미터가 특정 값인지도 검증할 수 있습니다:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

주어진 쿼리 문자열 파라미터가 없음을 검증합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

URL의 해시(fragment)가 주어진 값과 일치하는지 검증합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

URL 해시가 주어진 값으로 시작하는지 검증합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

URL 해시가 주어진 값과 다름을 검증합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

주어진 암호화된 쿠키가 존재하는지 검증합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

주어진 암호화되지 않은 쿠키가 존재하는지 검증합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

주어진 암호화된 쿠키가 없음을 검증합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

주어진 암호화되지 않은 쿠키가 없음을 검증합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키가 특정 값을 가지는지 검증합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키가 특정 값을 가지는지 검증합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

페이지에 주어진 텍스트가 존재하는지 검증합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

페이지에 주어진 텍스트가 없음을 검증합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

주어진 셀렉터 안에 텍스트가 존재하는지 검증합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

주어진 셀렉터 안에 텍스트가 없음을 검증합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

주어진 셀렉터 안에 어떤 텍스트든 존재하는지 검증합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

주어진 셀렉터 안에 텍스트가 전혀 없음을 검증합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
#### assertScript

주어진 자바스크립트 표현식이 특정 값을 반환하는지 검증합니다:

```php
$browser->assertScript('window.isLoaded')
        ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지 소스에 특정 코드가 존재하는지 검증합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지 소스에 특정 코드가 없음을 검증합니다:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

페이지에 특정 링크가 존재하는지 검증합니다:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

페이지에 특정 링크가 없음을 검증합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

주어진 입력 필드가 특정 값인지 검증합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

주어진 입력 필드가 특정 값이 아님을 검증합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

주어진 체크박스가 체크되어 있는지 검증합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

주어진 체크박스가 체크되어 있지 않음을 검증합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

주어진 체크박스가 중간 상태인지 검증합니다:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

주어진 라디오 버튼이 선택되었는지 검증합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

주어진 라디오 버튼이 선택되지 않았음을 검증합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

주어진 드롭다운이 특정 값으로 선택되었는지 검증합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

주어진 드롭다운이 특정 값으로 선택되지 않았음을 검증합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

주어진 값 목록이 선택 옵션으로 존재하는지 검증합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

주어진 값 목록이 선택 옵션에 없음을 검증합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

주어진 값이 선택 옵션에 존재하는지 검증합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

주어진 값이 선택 옵션에 없음을 검증합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

주어진 셀렉터가 특정 값을 가지는지 검증합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

주어진 셀렉터가 특정 값을 가지지 않음을 검증합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

주어진 셀렉터가 특정 속성에 특정 값을 가지는지 검증합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

주어진 셀렉터가 특정 속성을 가지지 않음을 검증합니다:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

주어진 셀렉터의 특정 속성 값에 특정 값이 포함되어 있는지 검증합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

주어진 셀렉터의 특정 속성 값에 특정 값이 포함되어 있지 않음을 검증합니다:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

주어진 셀렉터의 특정 aria 속성이 특정 값을 가지는지 검증합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 의 경우 다음과 같이 검증할 수 있습니다:

```php
$browser->assertAriaAttribute('button', 'label', 'Add');
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

주어진 셀렉터가 특정 data-* 속성에 특정 값을 가지는지 검증합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 의 경우 다음과 같이 검증할 수 있습니다:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees');
```

<a name="assert-visible"></a>
#### assertVisible

주어진 셀렉터가 화면에 보이는지 검증합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

주어진 셀렉터가 페이지 소스 내 존재하는지 검증합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

주어진 셀렉터가 페이지 소스 내 존재하지 않음을 검증합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

주어진 셀렉터가 화면에 보이지 않음을 검증합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

주어진 이름을 가진 입력 필드가 존재하는지 검증합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

주어진 이름을 가진 입력 필드가 소스 내 존재하지 않음을 검증합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

특정 메시지를 가진 자바스크립트 대화상자가 열린 상태인지 검증합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

주어진 필드가 활성화된 상태인지 검증합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

주어진 필드가 비활성화된 상태인지 검증합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

주어진 버튼이 활성화된 상태인지 검증합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

주어진 버튼이 비활성화된 상태인지 검증합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

주어진 필드가 포커스된 상태인지 검증합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

주어진 필드가 포커스되지 않은 상태인지 검증합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

현재 사용자가 인증된 상태인지 검증합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

현재 사용자가 인증되지 않은 상태인지 검증합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

현재 사용자가 특정 사용자로 인증되었는지 검증합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 [Vue 컴포넌트](https://vuejs.org)의 데이터 상태에 대해서도 어설션을 지원합니다. 예를 들어 다음과 같은 Vue 컴포넌트가 있다면:

```html
<!-- HTML -->

<profile dusk="profile-component"></profile>
```

```js
// Vue 컴포넌트 정의

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

다음과 같이 Vue 컴포넌트 상태를 테스트할 수 있습니다:

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
 * 기본적인 Vue 테스트 예제.
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

Vue 컴포넌트 데이터가 주어진 값과 다름을 검증합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트 데이터가 배열이고 특정 값을 포함하는지 검증합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

Vue 컴포넌트 데이터가 배열이고 특정 값을 포함하지 않음을 검증합니다:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

복잡한 연속 액션이 필요한 테스트가 많아질 경우, 테스트가 읽기 어렵고 이해하기 어려워질 수 있습니다. Dusk 페이지 객체는 표현력 있는 액션을 정의해, 하나의 메서드 호출로 페이지에서 수행할 수 있습니다. 또한 페이지 내 자주 쓰이는 셀렉터에 대한 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 사용하세요. 생성된 페이지 객체는 `tests/Browser/Pages` 디렉토리에 위치합니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성 (Configuring Pages)

기본적으로 페이지는 `url`, `assert`, `elements` 세 메서드를 가집니다. 여기서는 `url`과 `assert` 메서드를 설명합니다. `elements`는 아래에서 [축약 셀렉터](#shorthand-selectors) 부분에서 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 페이지를 나타내는 경로를 문자열로 반환합니다. Dusk는 이 값을 사용해 해당 페이지로 이동합니다:

```php
/**
 * 페이지 URL 반환
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert` 메서드에서는 브라우저가 현재 페이지에 있는지 검증하기 위한 어설션을 수행할 수 있습니다. 반드시 구현할 필요는 없으나, 구현 시 페이지로 이동 시 자동 실행됩니다:

```php
/**
 * 브라우저가 페이지에 있음을 검증
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동 (Navigating to Pages)

페이지 클래스가 정의되면 `visit` 메서드로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 있으면서 페이지 내 셀렉터와 메서드를 현재 테스트 컨텍스트에 불러오려면 `on` 메서드를 사용합니다. 예를 들면 버튼 클릭 후 리다이렉트가 발생할 때 유용합니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
        ->clickLink('Create Playlist')
        ->on(new CreatePlaylist)
        ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 축약 셀렉터 (Shorthand Selectors)

페이지 클래스 내 `elements` 메서드에서는 페이지 내 특정 CSS 셀렉터에 대해 축약키를 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드 단축키를 정의하면:

```php
/**
 * 페이지 내 엘리먼트 단축키 배열 반환
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

정의 후에는 일반 CSS 셀렉터 대신 단축키를 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 축약 셀렉터

Dusk 설치 시 기본 `Page` 클래스가 `tests/Browser/Pages`에 생성됩니다. 이 클래스의 `siteElements` 메서드에서 앱 전체에 적용할 전역 축약 셀렉터를 정의할 수 있습니다:

```php
/**
 * 사이트 전체에서 사용하는 전역 엘리먼트 단축키 배열 반환
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

기본 메서드 외 원하는 메서드를 페이지 클래스에 추가할 수 있습니다. 예를 들어 음악 관리 앱에서 플레이리스트 생성 로직을 중복 없이 페이지 메서드로 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 기타 페이지 메서드...

    /**
     * 새 플레이리스트 생성
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

정의한 메서드는 테스트 내에서 페이지 방문 후 바로 사용할 수 있으며, 브라우저 인스턴스는 첫 번째 인자로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
        ->createPlaylist('My Playlist')
        ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 페이지 객체와 유사하지만, 내비게이션 바나 알림창처럼 애플리케이션 전반에서 재사용되는 UI 조각이나 기능에 적합합니다. 컴포넌트는 특정 URL에 묶이지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트를 생성하려면 `dusk:component` Artisan 명령을 사용하세요. 컴포넌트는 `tests/Browser/Components` 디렉토리에 생성됩니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어 "날짜 선택기" 컴포넌트는 여러 페이지에서 쓰일 수 있는 UI입니다. 여러 테스트에서 매번 날짜 선택 로직을 작성하는 대신 컴포넌트로 정의해 코드 중복을 줄입니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * 컴포넌트 루트 셀렉터 반환
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * 브라우저 페이지에 컴포넌트가 표시되는지 검증
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 단축 엘리먼트 배열 반환
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
     * 주어진 날짜 선택
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
### 컴포넌트 사용 (Using Components)

컴포넌트가 정의된 후에는 어떤 테스트에서든 Dusk의 `within` 메서드로 컴포넌트를 포함한 영역 내 동작을 캡슐화 할 수 있습니다. 만약 날짜 선택 로직이 변경되면 컴포넌트만 수정하면 되어 유지보수가 용이합니다:

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

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

> [!WARNING]  
> 대부분의 Dusk CI 설정은 Laravel 앱을 내장 PHP 개발 서버를 사용해 포트 8000에서 서비스한다고 가정합니다. 따라서 CI 환경에 `APP_URL` 환경 변수가 `http://127.0.0.1:8000` 으로 설정되어 있는지 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행 (Running Tests on Heroku CI)

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 `app.json` 파일에 다음 빌드팩과 스크립트를 추가하세요:

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
### Travis CI에서 테스트 실행 (Running Tests on Travis CI)

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행할 때는 그래픽 환경이 없기 때문에 Chrome 브라우저 실행을 위해 추가 설정이 필요합니다. PHP 내장 웹서버도 `php artisan serve` 명령으로 실행합니다:

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
### GitHub Actions에서 테스트 실행 (Running Tests on GitHub Actions)

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트 실행을 위해 다음과 같은 작업 흐름 설정을 시작점으로 사용할 수 있습니다. Travis CI와 비슷하게 `php artisan serve` 명령을 사용해 PHP 내장 서버를 실행합니다:

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
### Chipper CI에서 테스트 실행 (Running Tests on Chipper CI)

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행할 경우, PHP 내장 서버로 Laravel 앱을 실행하고 다음과 같은 `.chipperci.yml` 설정을 사용할 수 있습니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Chrome을 빌드 환경에 포함
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

      # dusk 환경 파일 만들기 (APP_URL에 BUILD_HOST 적용)
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

Chipper CI에서 Dusk 및 데이터베이스 설정 관련 자세한 내용은 [공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.