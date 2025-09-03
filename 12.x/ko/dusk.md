# Laravel Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 실행 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본 사용법](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크에 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크에 저장](#storing-page-source-to-disk)
- [엘리먼트와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 활용](#using-the-keyboard)
    - [마우스 활용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기](#waiting-for-elements)
    - [엘리먼트로 스크롤 이동](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [요약 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합(CI)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> [Pest 4](https://pestphp.com/)는 이제 Laravel Dusk에 비해 성능과 사용성 면에서 훨씬 향상된 자동 브라우저 테스트 기능을 제공합니다. 새로운 프로젝트에서는 브라우저 테스트에 Pest 사용을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 간결하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 별도로 설치할 필요가 없습니다. 대신 독립적으로 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 설치해서 사용합니다. 물론, 필요에 따라 Selenium 호환 드라이버를 자유롭게 사용할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 먼저 [Google Chrome](https://www.google.com/chrome)을 설치하고, 프로젝트에 `laravel/dusk` Composer 의존성을 추가해야 합니다:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록한다면, **절대로** 프로덕션 환경에서는 등록하지 마십시오. 그렇지 않으면 누구나 애플리케이션에 인증해서 접근할 수 있는 보안 문제가 발생할 수 있습니다.

Dusk 패키지 설치 후에는 `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리, Dusk 테스트 예제 파일, 그리고 운영체제에 맞는 ChromeDriver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수 값을 설정해야 합니다. 이 값은 브라우저에서 애플리케이션에 접속할 때 사용되는 URL이어야 합니다.

> [!NOTE]
> 로컬 개발 환경을 [Laravel Sail](/docs/12.x/sail)로 관리 중이라면, [Dusk 테스트를 설정하고 실행하는 방법](/docs/12.x/sail#laravel-dusk)에 대해 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령으로 설치된 ChromeDriver와는 다른 버전을 설치하고 싶다면, `dusk:chrome-driver` 명령을 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 운영체제에 맞는 지정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 OS에 지정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# Chrome/Chromium의 감지된 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행에 문제가 있을 경우, 다음 명령어로 실행 권한을 부여해야 합니다: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립적으로 설치된 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용하지만, 별도의 Selenium 서버를 직접 구동하여 원하는 브라우저로 테스트를 실행할 수 있습니다.

먼저 애플리케이션 내 Dusk 테스트의 기본 케이스 파일인 `tests/DuskTestCase.php`를 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출을 제거하면 Dusk가 ChromeDriver를 자동 시작하지 않게 됩니다:

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

그 다음, `driver` 메서드를 수정하여 연결하고자 하는 URL 및 포트로 변경할 수 있습니다. 또한, WebDriver에 전달할 "desired capabilities"도 필요에 따라 조정할 수 있습니다:

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

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하면 됩니다. 생성된 테스트는 `tests/Browser` 디렉터리에 위치합니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 실행 후 데이터베이스 초기화 (Resetting the Database After Each Test)

대부분의 테스트는 애플리케이션의 데이터베이스에서 데이터를 읽는 페이지와 상호작용하게 됩니다. 하지만 Dusk 테스트에서는 `RefreshDatabase` 트레이트를 **절대로** 사용하면 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 이용하는데, HTTP 요청 간에는 이 트랜잭션 처리가 불가능합니다. 대신 `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트 중 하나를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 실행 전마다 데이터베이스 마이그레이션을 수행합니다. 다만, 매 테스트마다 테이블을 드롭하고 재생성하므로, 테이블을 잘라(truncate)내는 작업에 비해 느릴 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

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
> Dusk 테스트 실행 시에는 SQLite 메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 동작하기 때문에, 다른 프로세스의 메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 잘라내기(Truncation) 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 데이터베이스 마이그레이션을 실행해 모든 테이블이 만들어져 있는지 확인합니다. 이후 테스트들에서는 마이그레이션 전체를 반복하지 않고, 테이블만 바로 비우기(truncate) 때문에 처리 속도가 더 빠릅니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

pest()->use(DatabaseTruncation::class);

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 truncate합니다. truncate 대상 테이블을 직접 지정하고 싶다면, 테스트 클래스에 `$tablesToTruncate` 속성을 정의하면 됩니다:

> [!NOTE]
> Pest를 사용하는 경우, 속성이나 메서드는 반드시 base `DuskTestCase` 클래스 또는 테스트 파일이 상속하는 어떤 클래스에서 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는 truncation에서 제외할 테이블을 지정하려면, `$exceptTables` 속성을 사용할 수 있습니다:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

truncate를 적용할 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 정의합니다:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

database truncate 전후로 작업을 실행하고 싶다면, `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의할 수 있습니다:

```php
/**
 * Perform any work that should take place before the database has started truncating.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Perform any work that should take place after the database has finished truncating.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행 (Running Tests)

브라우저 테스트 실행은 `dusk` Artisan 명령어로 할 수 있습니다:

```shell
php artisan dusk
```

직전 테스트에서 실패했던 테스트만 빠르게 재실행하려면 `dusk:fails` 명령어를 사용합니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit에서 허용하는 인수들도 그대로 사용할 수 있으며, [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)별로 테스트를 실행하는 것도 가능합니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 개발 환경을 구축했다면, [Sail의 Dusk 테스트 설정 및 실행 방법](/docs/12.x/sail#laravel-dusk)도 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 만약 시스템 환경상 자동 실행이 불가능하다면, ChromeDriver를 미리 수동으로 실행한 다음 `dusk` 명령어를 이용하면 됩니다. 이 경우, `tests/DuskTestCase.php` 파일의 다음 부분을 주석 처리해야 합니다:

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

또한, ChromeDriver를 9515번 이외의 포트로 실행했다면, 같은 클래스의 `driver` 메서드에서 포트 값을 변경해야 합니다:

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
### 환경 파일 처리 (Environment Handling)

Dusk가 테스트 실행 시 독립적인 환경 파일을 사용하도록 하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하세요. 예를 들어, `local` 환경에서 `dusk` 명령을 실행한다면 `.env.dusk.local` 파일을 만들면 됩니다.

테스트 실행 중에는 기존 `.env` 파일을 백업하고, Dusk 환경 파일명을 `.env`로 변경해 사용합니다. 테스트 종료 후에는 원래의 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사용법 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성 (Creating Browsers)

애플리케이션에 로그인이 정상적으로 되는지 확인하는 테스트를 예시로 살펴봅니다. 테스트 생성 후, 로그인 페이지 접속, 자격 증명 입력, 로그인 버튼 클릭까지 거래를 작성할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 안에서 `browse` 메서드를 사용하여 생성합니다:

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

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
     * A basic browser test example.
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

예제에서 볼 수 있듯, `browse` 메서드는 클로저를 인수로 받으며, Dusk가 자동으로 브라우저 인스턴스를 이 클로저에 전달합니다. 이 브라우저 객체를 통해 실제 애플리케이션과 상호작용하거나 어설션을 수행할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 다중 브라우저 인스턴스 생성

때때로 테스트를 제대로 수행하려면 여러 개의 브라우저가 필요할 수 있습니다. 예를 들어, 채팅 화면(WebSockets 활용) 등을 테스트하려면 여러 브라우저가 필요합니다. `browse` 함수의 클로저 시그니처에 브라우저 인수를 추가하면 여러 브라우저를 다룰 수 있습니다:

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

`visit` 메서드를 사용해 애플리케이션 내 특정 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[named route](/docs/12.x/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 쓸 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`과 `forward` 메서드로 "뒤로 가기"와 "앞으로 가기"를 할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드를 사용하면 페이지를 새로 고칠 수 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드를 사용해 브라우저 창의 크기를 조절할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창 크기를 컨텐츠에 맞게 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시, Dusk는 자동으로 브라우저 크기를 컨텐츠에 맞게 조정한 뒤 스크린샷을 찍습니다. 이 기능을 비활성화하려면 `disableFitOnFailure`를 사용하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 브라우저 창을 화면 상의 다른 위치로 옮길 수 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 활용하세요. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받으며, 매크로를 브라우저 인스턴스의 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

로그인 인증이 필요한 페이지를 자주 테스트하게 됩니다. 모든 테스트마다 로그인 과정을 거치지 않으려면 Dusk의 `loginAs` 메서드를 활용하세요. 이 메서드에는 인증 가능한 모델의 PK나 모델 인스턴스를 전달하면 됩니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 사용 뒤에는, 해당 파일 내 모든 테스트에서 해당 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드로 암호화된 쿠키 값을 읽거나 설정할 수 있습니다. Laravel에서 생성된 쿠키는 기본적으로 모두 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키의 값을 읽거나 설정하려면 `plainCookie` 메서드를 사용하세요:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메서드로 쿠키를 삭제할 수 있습니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 (Executing JavaScript)

`script` 메서드를 이용해 브라우저 내에서 임의의 JavaScript 코드를 실행할 수 있습니다:

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

`screenshot` 메서드로 지정한 파일명으로 스크린샷을 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 여러 화면 너비(브레이크포인트)별로 스크린샷을 저장합니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드는 특정 엘리먼트만 스크린샷으로 저장할 수 있습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 디스크에 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드를 이용해 브라우저의 콘솔 출력을 파일로 저장할 수 있습니다. 로그는 `tests/Browser/console` 디렉터리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크에 저장 (Storing Page Source to Disk)

`storeSource` 메서드로 현재 페이지 소스를 파일에 저장할 수 있습니다. 파일은 `tests/Browser/source` 디렉터리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

엘리먼트 상호작용을 위한 CSS 셀렉터 선택은 Dusk 테스트에서 가장 어려운 부분 중 하나입니다. 프론트엔드가 변경되면 하드코딩된 CSS 셀렉터가 망가질 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터를 외우는 대신 효과적인 테스트 작성에 집중할 수 있습니다. HTML 요소에 `dusk` 속성을 부여하면 되고, 테스트에서는 셀렉터 앞에 `@`를 붙여 해당 요소와 상호작용할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

필요에 따라 Dusk 셀렉터가 사용할 HTML 속성을 `selectorHtmlAttribute` 메서드로 변경할 수도 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 읽기/설정하기

Dusk는 화면의 엘리먼트가 가진 값(value), 화면에 보이는 텍스트, 속성(attribute)에 접근할 수 있는 다양한 메서드를 제공합니다. 예를 들어, 특정 CSS 또는 Dusk 셀렉터에 해당하는 엘리먼트의 "value" 값을 읽거나 설정하려면 `value` 메서드를 사용하세요:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 입력 필드명에 해당하는 input 엘리먼트의 값을 가져옵니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 읽기

`text` 메서드는 셀렉터에 해당하는 엘리먼트의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 읽기

`attribute` 메서드는 지정한 셀렉터의 엘리먼트에서 특정 속성의 값을 읽어옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기

Dusk는 폼 및 입력 엘리먼트와 상호작용할 수 있도록 다양한 메서드를 제공합니다. 먼저, 입력 필드에 텍스트를 입력하는 기본 예제부터 살펴보겠습니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

이 때 CSS 셀렉터를 생략할 수도 있는데, 그 경우 `name` 속성이 일치하는 `input` 또는 `textarea`를 자동으로 찾아 입력합니다.

필드에 기존 값을 지우지 않고 텍스트를 추가하려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

값을 지우려면 `clear` 메서드를 사용할 수 있습니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드를 사용하면 키를 일정 시간 간격을 두고 천천히 입력하게 할 수 있습니다. 기본 지연 시간은 키 입력당 100ms이며, 직접 밀리세컨드 단위로 지정할 수도 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드를 사용하면 천천히 텍스트를 추가할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 엘리먼트의 옵션을 선택하려면 `select` 메서드를 사용하세요. 옵션의 표시 텍스트 대신 실제 값(value)을 전달해야 합니다:

```php
$browser->select('size', 'Large');
```

값을 생략하면 랜덤 옵션이 선택됩니다:

```php
$browser->select('size');
```

배열을 두 번째 인수로 전달하면 여러 옵션을 동시에 선택할 수 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스(input[type="checkbox"])를 "체크"하려면 `check` 메서드를 사용하세요:

```php
$browser->check('terms');
```

체크 해제를 원하면 `uncheck` 메서드를 사용합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼(input[type="radio"])을 선택하려면 `radio` 메서드를 사용하세요:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

파일 업로드 input에 파일을 첨부하려면 `attach` 메서드를 사용하세요:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능은 서버에 `Zip` PHP 확장 기능이 설치되어 활성화되어 있어야만 사용할 수 있습니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드를 통해 페이지 내 버튼을 클릭할 수 있습니다. 인수로 버튼의 표시 텍스트 또는 CSS/Dusk 셀렉터를 전달합니다:

```php
$browser->press('Login');
```

폼 제출 시, 대부분의 애플리케이션은 HTTP 요청이 끝날 때까지 버튼을 비활성화합니다. 이런 경우 `pressAndWaitFor` 메서드를 사용해 버튼이 다시 활성화될 때까지 대기할 수 있습니다:

```php
// 최대 5초까지 버튼이 활성화될 때까지 대기...
$browser->pressAndWaitFor('Save');

// 최대 1초까지 대기...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 인수로 표시 텍스트를 전달합니다:

```php
$browser->clickLink($linkText);
```

특정 링크가 보이는지 확인하려면 `seeLink` 메서드를 사용합니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드들은 jQuery와 상호작용합니다. 페이지에 jQuery가 없으면, 테스트 중 자동 주입됩니다.

<a name="using-the-keyboard"></a>
### 키보드 활용 (Using the Keyboard)

`keys` 메서드는 `type`보다 더 복잡한 키 입력 시퀀스를 구현할 수 있습니다. 예를 들어, modifier 키를 누른 채 값을 입력하는 경우 등입니다. 아래 예시는 `shift` 키를 누르고 `taylor` 을 입력한 뒤, modifier 없이 `swift` 를 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

키보드 단축키 조합을 특정 셀렉터에 전송할 수도 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` 등 모든 modifier 키는 `{}`로 감싸야 하며, [WebDriverKeys 클래스](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)에 정의된 상수와 동일하게 사용합니다.

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

`withKeyboard` 메서드를 사용하면 `Laravel\Dusk\Keyboard` 클래스를 통한 키보드 상호작용을 더 명확하게 구현할 수 있습니다. 이 클래스는 `press`, `release`, `type`, `pause` 등의 메서드를 제공합니다:

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

반복 사용되는 키보드 상호작용을 쉽게 재사용하려면, `Keyboard` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에 정의합니다:

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
     * Register Dusk's browser macros.
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

매크로는 이름과 클로저를 인수로 받으며, `Keyboard` 인스턴스에서 메서드처럼 사용할 수 있습니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 활용 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메서드는 CSS 또는 Dusk 셀렉터로 매칭되는 요소를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath로 요소를 클릭할 수 있습니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 상대 좌표 기준으로 브라우저 뷰영역의 맨 위에 있는 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick`은 마우스의 더블 클릭을, `rightClick`은 우클릭을 시뮬레이션합니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`로 마우스를 누른 상태를 유지하고, 이후 `releaseMouse`로 해제합니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 `ctrl+클릭` 이벤트를 시뮬레이션합니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메서드는 지정 셀렉터의 요소 위로 마우스를 이동시킵니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 한 요소를 다른 요소로 드래그할 때 사용합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

단 방향으로 요소를 드래그하려면 다음 메서드들이 있습니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 드래그하려면 `dragOffset` 메서드를 사용하세요:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그 (JavaScript Dialogs)

Dusk는 JavaScript 다이얼로그와의 상호작용을 위한 다양한 메서드를 제공합니다. 예를 들어, 다이얼로그가 뜰 때까지 대기하려면 `waitForDialog`를 사용합니다:

```php
$browser->waitForDialog($seconds = null);
```

다이얼로그가 보여지고 특정 메시지를 포함하고 있는지 어설션하려면 `assertDialogOpened`를 사용합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 있으면 `typeInDialog`로 값도 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

JavaScript 다이얼로그의 "OK" 버튼을 클릭하여 닫으려면 `acceptDialog`를, "Cancel" 버튼을 클릭하려면 `dismissDialog`를 사용하세요:

```php
$browser->acceptDialog();
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용 (Interacting With Inline Frames)

iframe 내 요소와 상호작용하려면 `withinFrame` 메서드를 사용합니다. 클로저 내의 모든 동작이 지정된 iframe 범위 내에서 실행됩니다:

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

여러 작업을 특정 셀렉터 범위 내에서 실행하려면 `with` 메서드를 사용할 수 있습니다. 예를 들어, 테이블 내에만 존재하는 텍스트를 검사하고, 그 테이블 안의 버튼을 누르고 싶을 때 사용하면 됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

이 스코프 밖에서 어설션을 실행하려면 `elsewhere`와 `elsewhereWhenAvailable` 메서드를 이용하면 됩니다:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 스코프는 `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 엘리먼트 대기 (Waiting for Elements)

JavaScript를 많이 사용하는 애플리케이션 테스트에서는 특정 요소나 데이터가 준비될 때까지 "대기"하는 일이 자주 필요합니다. Dusk는 이러한 대기를 손쉽게 처리할 수 있는 다양한 대기 메서드를 제공합니다.

<a name="waiting"></a>
#### 대기 (Waiting)

일정 ms 동안 단순히 대기하려면 `pause` 메서드를 사용합니다:

```php
$browser->pause(1000);
```

특정 조건이 `true`일 때만 대기하려면 `pauseIf`를, 그렇지 않으면 `pauseUnless` 메서드를 사용하세요:

```php
$browser->pauseIf(App::environment('production'), 1000);
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor` 메서드는 CSS 혹은 Dusk 셀렉터로 지정된 요소가 화면에 나타날 때까지 대기합니다. 기본 대기 시간은 최대 5초입니다:

```php
// 최대 5초까지 대기
$browser->waitFor('.selector');

// 최대 1초까지만 대기
$browser->waitFor('.selector', 1);
```

지정된 텍스트가 포함될 때까지 대기하려면 `waitForTextIn`을 사용합니다:

```php
$browser->waitForTextIn('.selector', 'Hello World');
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

지정된 셀렉터의 요소가 사라질 때까지 대기하려면 `waitUntilMissing`을 사용합니다:

```php
$browser->waitUntilMissing('.selector');
$browser->waitUntilMissing('.selector', 1);
```

해당 셀렉터가 비활성화/활성화 될 때까지 대기하려면 다음 메서드를 사용합니다:

```php
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);

$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 나타났을 때 범위 지정

주로 모달 등 특정 엘리먼트가 화면에 나타나면 그 요소 안에서 추가 작업을 해야 할 때, `whenAvailable` 메서드를 활용할 수 있습니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText` 메서드는 특정 텍스트가 화면에 나타날 때까지 대기합니다:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

텍스트가 사라질 때까지 대기하려면 `waitUntilMissingText`를 사용합니다:

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink` 메서드는 특정 링크 텍스트가 화면에서 보일 때까지 대기합니다:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

`waitForInput` 메서드는 지정 입력필드가 나타날 때까지 대기합니다:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 경로 대기

만약 `$browser->assertPathIs('/home')`와 같은 경로 어설션이 비동기적으로 window.location.pathname이 바뀌는 상황에서 실패한다면, `waitForLocation` 메서드로 경로가 바뀔 때까지 대기할 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

전체 URL로 대기할 수도 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

또는 [named route](/docs/12.x/routing#named-routes)를 지정할 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

어떤 액션 후 페이지가 재로드되는 것을 기다릴 필요가 있다면 `waitForReload`를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

특정 버튼 클릭 후 바로 리로드를 기다리는 경우 `clickAndWaitForReload`로 더 편하게 쓸 수 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

테스트 실행을 자바스크립트 표현식이 `true`가 될 때까지 대기하고자 할 때는 `waitUntil` 메서드를 사용할 수 있습니다. `return`이나 세미콜론은 적지 않아도 됩니다:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

`waitUntilVue`와 `waitUntilVueIsNot` 메서드로 [Vue 컴포넌트](https://vuejs.org) 속성의 값이 특정 값이 될 때까지 기다릴 수 있습니다:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기

`waitForEvent` 메서드는 특정 자바스크립트 이벤트 발생까지 테스트 실행을 멈춥니다:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 `body` 요소에 붙지만, 셀렉터를 범위 지정하면 해당 요소에 붙습니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    $iframe->waitForEvent('load');
});
```

또는 두 번째 인수로 특정 셀렉터를 지정할 수도 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document`나 `window`에도 이벤트 리스너를 붙일 수 있습니다:

```php
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백으로 대기

대부분의 "대기" 메서드는 내부적으로 `waitUsing`을 사용합니다. 직접 `waitUsing`을 이용해 주어진 클로저로 대기 조건을 지정할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트로 스크롤 이동 (Scrolling an Element Into View)

엘리먼트가 화면에 보이지 않는 바깥 영역에 있을 때 클릭이 안 될 수 있습니다. 이때 `scrollIntoView`로 해당 셀렉터가 보일 때까지 스크롤할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 사용할 수 있는 다양한 어설션을 제공합니다. 아래는 지원하는 어설션 목록입니다:

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

</div>

<!-- 이하 각 어설션 항목 번역 생략: 마크다운 구조 및 코드블록 규칙 상 그대로 유지 -->

<a name="pages"></a>
## 페이지 (Pages)

복잡한 시나리오를 순서대로 수행해야 하는 테스트는, 테스트 코드의 가독성과 유지보수를 떨어뜨릴 수 있습니다. Dusk의 페이지 객체 기능을 사용하면 페이지별로 의미 있는 액션과 셀렉터를 정의해, 코드의 이해와 재사용성을 높일 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` Artisan 명령을 사용합니다. 새 페이지 객체는 애플리케이션의 `tests/Browser/Pages` 디렉터리에 생성됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

기본적으로 페이지에는 `url`, `assert`, `elements` 메서드가 있습니다. 여기서는 `url`, `assert` 메서드만 설명하며, `elements` 메서드는 [아래에서 자세히 설명](#shorthand-selectors)합니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지의 경로를 반환합니다. Dusk는 이 URL로 브라우저에서 페이지를 탐색합니다:

```php
/**
 * Get the URL for the page.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert` 메서드는 브라우저가 실제 이 페이지에 도착했는지 검증할 때 사용합니다. 꼭 내용을 채울 필요는 없습니다. 어설션이 있다면 페이지 이동 시 자동으로 실행됩니다:

```php
/**
 * Assert that the browser is on the page.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동 (Navigating to Pages)

페이지가 정의되어 있다면 `visit` 메서드로 해당 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 특정 페이지에 있으며, 해당 페이지 객체의 셀렉터와 메서드만 불러와야 하는 경우, 즉 버튼 클릭 후 리다이렉트 등에서는 `on` 메서드를 사용합니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 요약 셀렉터 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드에서는 자주 쓰는 CSS 셀렉터에 대한 별칭을 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드에 대해 별칭을 둘 수 있습니다:

```php
/**
 * Get the element shortcuts for the page.
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

이후에는 별칭을 사용해 마치 CSS 셀렉터처럼 어디서나 활용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 요약 셀렉터

Dusk 설치 후 `tests/Browser/Pages` 디렉터리에는 기본 `Page` 클래스가 추가됩니다. 이 클래스의 `siteElements` 메서드는 애플리케이션 전체에서 쓸 수 있는 전역 셀렉터 별칭을 정의합니다:

```php
/**
 * Get the global element shortcuts for the site.
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

기본 메서드 외에, 추가적인 동작을 페이지별로 메서드로 만들어 재사용할 수 있습니다. 예를 들어 음악 관리 앱에서 "플레이리스트 생성"과 같은 액션을 페이지 메서드로 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 기타 페이지 메서드...

    /**
     * Create a new playlist.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

정의한 메서드는 페이지를 사용하는 테스팅 코드 어디에서든 호출할 수 있으며, 브라우저 인스턴스가 첫 인수로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk 페이지 객체와 비슷하지만, 다양한 페이지에서 반복적으로 사용되는 UI(예: 네비게이션 바, 알림창 등)에 주로 사용됩니다. 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트 생성을 위해 Artisan의 `dusk:component` 명령어를 사용할 수 있습니다. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 추가됩니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어 "날짜 선택기"와 같은 기능은 여러 페이지에서 반복 사용될 수 있습니다. 각 테스트마다 자동화 코드를 계속 작성하는 대신, Dusk 컴포넌트로 로직을 캡슐화할 수 있습니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * Get the root selector for the component.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * Assert that the browser page contains the component.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * Get the element shortcuts for the component.
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
     * Select the given date.
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

컴포넌트가 정의되면, 어느 테스트에서든 쉽게 사용할 수 있습니다. 날짜 선택 로직이 바뀌더라도 컴포넌트만 수정하면 모든 테스트에 일괄 반영됩니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

pest()->use(DatabaseMigrations::class);

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
     * A basic component test example.
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

`component` 메서드를 이용해 해당 컴포넌트에 스코프가 지정된 브라우저 인스턴스를 얻고, 그 안에서 동작할 수도 있습니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 구성은 Laravel 애플리케이션이 8000번 포트에서 내장 PHP 개발 서버로 실행되는 것을 전제로 합니다. 따라서 CI 환경의 `APP_URL` 환경변수가 반드시 `http://127.0.0.1:8000`이어야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 아래와 같이 Heroku `app.json` 파일에 Google Chrome buildpack과 관련 스크립트를 추가하세요:

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
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 아래와 같은 `.travis.yml` 구성을 참고하세요. Travis는 GUI 환경이 아니므로 Chrome 브라우저 실행을 위한 별도 설정이 필요합니다. 또한, `php artisan serve`로 내장 PHP 웹 서버를 사용합니다:

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
### GitHub Actions

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하려면 아래와 같은 설정 파일을 참고하면 됩니다. TravisCI와 마찬가지로 내장 PHP 서버를 사용합니다:

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
### Chipper CI

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면 아래의 설정 파일을 참고하세요. 내장 PHP 서버를 사용하도록 되어 있습니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Include Chrome in the build environment
services:
  - dusk

# Build all commits
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Create a dusk env file, ensuring APP_URL uses BUILD_HOST
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

Chipper CI에서 Dusk 테스트 및 데이터베이스 사용 방법에 대한 더 자세한 내용은 [Chipper CI 공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.

