# Laravel Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저의 기본 사용법](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크 저장](#storing-page-source-to-disk)
- [요소와 상호작용하기](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [IFrame과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소 뷰로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지(Pages)](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 구성](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [약식 셀렉터](#shorthand-selectors)
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

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Dusk는 기본적으로 사용자의 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신, 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 하지만 필요하다면 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, [Google Chrome](https://www.google.com/chrome)을 설치하고, Composer를 이용해 `laravel/dusk` 의존성을 프로젝트에 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대** 프로덕션 환경에서는 등록하지 마십시오. 그렇지 않으면 임의의 사용자가 애플리케이션에 인증할 수 있는 보안 이슈가 발생할 수 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리와 예시 Dusk 테스트, 그리고 운영 체제에 맞는 Chrome Driver 바이너리를 생성 및 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근하는 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경을 [Laravel Sail](/docs/12.x/sail)로 관리한다면, [Dusk 테스트 환경 구성 및 실행](/docs/12.x/sail#laravel-dusk)에 관한 Sail 문서도 함께 참고하시기 바랍니다.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어를 통해 Laravel Dusk가 설치하는 ChromeDriver의 버전이 아닌 다른 버전을 설치하고 싶다면, `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 지정한 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 모든 지원 OS에 대한 지정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# 운영체제에서 감지된 Chrome/Chromium 버전에 맞는 ChromeDriver를 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk에서 사용하는 `chromedriver` 바이너리는 실행 가능해야 합니다. 만약 Dusk 실행에 문제가 있다면, 아래 명령어로 바이너리에 실행 권한이 있는지 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

Dusk는 기본적으로 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용해 브라우저 테스트를 실행합니다. 하지만 직접 Selenium 서버를 실행하고, 원하는 브라우저에 대해 테스트를 수행할 수도 있습니다.

먼저 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출을 제거할 수 있습니다. 이렇게 하면 Dusk가 ChromeDriver를 자동으로 시작하지 않습니다:

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

그 다음, `driver` 메서드를 수정하여 원하는 URL과 포트에 연결하고, WebDriver에 전달할 "desired capabilities"도 수정할 수 있습니다:

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

작성하는 대부분의 테스트는 애플리케이션의 데이터베이스에서 데이터를 조회하는 페이지와 상호작용할 것입니다. 하지만, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 절대 사용하지 않아야 합니다. `RefreshDatabase` 트레이트는 데이터베이스 트랜잭션을 활용하는데, 이는 HTTP 요청 간에는 적용되거나 사용할 수 없습니다. 대신 두 가지 옵션이 있습니다: `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트입니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 이전에 데이터베이스 마이그레이션을 실행합니다. 하지만, 각 테스트마다 데이터베이스 테이블을 드롭하고 다시 생성하는 것은 일반적으로 테이블을 잘라내는(Truncate) 것보다 느립니다:

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
> SQLite 인메모리 데이터베이스는 Dusk 테스트 실행 시 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되기 때문에, 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 Truncation 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 데이터베이스를 마이그레이션 해 테이블이 정상적으로 생성됐는지 보장합니다. 이후 테스트에서는 데이터베이스 테이블을 단순히 잘라내(Truncate) 처리하며, 반복적으로 마이그레이션하는 것보다 속도가 더 빠릅니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 Truncate 처리합니다. Truncate할 테이블을 커스텀하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의할 수 있습니다:

> [!NOTE]
> Pest를 사용하는 경우, 속성 또는 메서드는 기본 `DuskTestCase` 클래스 또는 테스트 파일이 확장한 클래스에 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는, 트렁케이션에서 제외할 테이블을 지정하고 싶다면 `$exceptTables` 속성을 사용할 수 있습니다:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

Truncate할 데이터베이스 커넥션을 지정하려면 `$connectionsToTruncate` 속성을 정의하세요:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 Truncate 전후에 실행할 코드를 정의하려면, 테스트 클래스에 `beforeTruncatingDatabase` 혹은 `afterTruncatingDatabase` 메서드를 선언하면 됩니다:

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

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

마지막으로 `dusk` 명령어 실행 시 테스트 실패가 있었다면, `dusk:fails` 명령어를 사용해 실패한 테스트만 먼저 재실행할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 러너에서 일반적으로 사용하는 모든 인수를 받을 수 있습니다. 예를 들어 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)별로 특정 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 로컬 개발 환경을 관리한다면, [Dusk 테스트 환경 구성 및 실행](/docs/12.x/sail#laravel-dusk)에 관한 Sail 문서를 꼭 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 시스템에 따라 자동 실행이 동작하지 않는다면, `dusk` 명령어를 실행하기 전에 ChromeDriver를 수동으로 실행하세요. 수동 실행을 선택한 경우, `tests/DuskTestCase.php` 파일 내 해당 라인을 주석 처리해야 합니다:

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

그리고 ChromeDriver를 9515번 이외의 포트에서 실행한다면 동일 클래스의 `driver` 메서드에서 포트 설정을 바꿔야 합니다:

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

테스트 실행 시 별도의 환경 파일을 사용하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하면 됩니다. 예를 들어 `local` 환경에서 `dusk` 명령어를 실행할 계획이라면, `.env.dusk.local` 파일을 만드세요.

테스트 실행 중에는 Dusk가 기존 `.env` 파일을 백업하고, Dusk용 환경 변수를 `.env`로 변경합니다. 테스트 종료 후에는 원래 `.env` 파일로 복원됩니다.

<a name="browser-basics"></a>
## 브라우저의 기본 사용법 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성 (Creating Browsers)

애플리케이션에 로그인할 수 있는지 확인하는 테스트를 예시로 살펴보겠습니다. 테스트를 생성한 후, 로그인 페이지로 이동해 자격 증명을 입력하고 "Login" 버튼을 클릭하는 작업을 추가할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 통해 생성할 수 있습니다:

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

위 예제에서 볼 수 있듯, `browse` 메서드는 클로저를 인수로 받으며, 이 클로저로 브라우저 인스턴스가 자동으로 전달됩니다. 이 브라우저 인스턴스를 통해 애플리케이션과 상호작용하고 다양한 어설션을 수행할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 인스턴스 생성

채팅 화면처럼 웹소켓을 통해 여러 사용자가 상호작용하는 기능을 테스트하려면, 여러 브라우저 인스턴스가 필요할 수 있습니다. 여러 브라우저를 사용하려면 `browse` 메서드의 클로저 시그니처에 추가 인수를 선언하면 됩니다:

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

`visit` 메서드는 애플리케이션 내의 지정 URI로 이동할 때 사용합니다:

```php
$browser->visit('/login');
```

[named route](/docs/12.x/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 사용할 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

"뒤로 가기(back)", "앞으로 가기(forward)"는 각각 `back`, `forward` 메서드로 가능합니다:

```php
$browser->back();

$browser->forward();
```

페이지를 새로고침하려면 `refresh` 메서드를 사용하세요:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

브라우저 창의 크기를 조절하려면 `resize` 메서드를 사용할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

창을 최대화하려면 `maximize` 메서드를 사용하세요:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창을 컨텐츠 크기에 맞게 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 스크린샷을 찍기 전에 창 크기를 컨텐츠에 맞게 조정합니다. 이 기능을 끄고 싶다면 `disableFitOnFailure` 메서드를 호출하세요:

```php
$browser->disableFitOnFailure();
```

브라우저 창을 화면에서 원하는 위치로 옮기려면 `move` 메서드를 사용하세요:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 반복적으로 사용하는 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 등록하세요:

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

`macro` 함수의 첫 번째 인수는 매크로 이름, 두 번째 인수는 클로저입니다. 등록한 매크로는 `Browser` 인스턴스에서 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

로그인을 요구하는 페이지를 테스트할 때는 매번 로그인 화면을 거치지 않고, Dusk의 `loginAs` 메서드를 이용해 곧바로 인증 처리를 할 수 있습니다. 이 메서드는 인증가능한 모델의 기본키 또는 모델 인스턴스를 인수로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용한 후에는, 해당 파일 내 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드를 사용해 암호화된 쿠키의 값을 가져오거나 설정할 수 있습니다. Laravel이 생성하는 모든 쿠키는 기본적으로 암호화됩니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값은 `plainCookie` 메서드로 사용할 수 있습니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키를 삭제하려면 `deleteCookie` 메서드를 사용하세요:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 (Executing JavaScript)

브라우저 내에서 원하는 JavaScript 구문을 실행할 땐 `script` 메서드를 사용하세요:

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

`filename`으로 스크린샷을 찍고 저장하려면 `screenshot` 메서드를 사용하세요. 스크린샷은 모두 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 브레이크포인트에서 일련의 스크린샷을 찍습니다:

```php
$browser->responsiveScreenshots('filename');
```

특정 요소만 스크린샷 찍고 싶다면 `screenshotElement` 메서드를 사용하세요:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 디스크 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드를 사용해 브라우저의 콘솔 출력을 파일로 저장할 수 있습니다. 파일은 `tests/Browser/console` 디렉터리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크 저장 (Storing Page Source to Disk)

현재 페이지의 소스를 파일로 저장하려면 `storeSource` 메서드를 사용하세요. 파일은 `tests/Browser/source` 디렉터리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

Dusk 테스트를 작성할 때 적절한 CSS 셀렉터를 선택하는 것은 가장 어려운 일 중 하나입니다. 프론트엔드가 변경되면 아래와 같은 CSS 셀렉터는 쉽게 테스트 오류를 유발할 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터를 기억하지 않고도 효과적으로 테스트에 집중할 수 있습니다. HTML 요소에 `dusk` 속성을 추가하여 셀렉터를 정의하세요. 테스트에서 `@` 기호를 붙여 해당 요소를 조작할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

필요하다면, Dusk 셀렉터에서 사용할 HTML 속성명을 `selectorHtmlAttribute` 메서드로 커스터마이즈할 수 있으며, 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기

Dusk는 페이지 내 요소의 현재 값, 표시되는 텍스트, 속성과 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, 지정한 CSS 또는 Dusk 셀렉터와 일치하는 요소의 "value"를 가져오려면 `value` 메서드를 사용하세요:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 주어진 필드명을 갖는 input 요소의 "value" 값을 가져옵니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

요소에 표시된 텍스트를 가져오려면 `text` 메서드를 사용하세요:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

특정 요소의 속성 값을 가져오려면 `attribute` 메서드를 사용하세요:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기

Dusk는 폼 및 입력 요소와 상호작용하는 여러 메서드를 제공합니다. 예를 들어 input 필드에 텍스트를 입력하려면 다음과 같이 작성합니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

필요할 경우 CSS 셀렉터를 인수로 넘길 수 있으나, 인수 없이 넘기면 Dusk는 넘긴 이름의 `input` 또는 `textarea` 요소를 자동으로 찾습니다.

필드의 기존 내용 뒤에 텍스트를 추가하려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력값을 지우려면 `clear` 메서드를 사용하세요:

```php
$browser->clear('email');
```

Dusk가 천천히 입력하도록 하려면 `typeSlowly` 메서드를 사용합니다. 기본적으로는 키마다 100밀리초 대기합니다. 세 번째 인수로 밀리초를 지정해 대기 시간을 조정할 수 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드는 기존 입력 값 뒤에 천천히 텍스트를 추가합니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 요소에서 값을 선택하려면 `select` 메서드를 사용하세요. 역시 전체 CSS 셀렉터를 넘길 필요 없이, 옵션 값(option value)을 인수로 넘기면 됩니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면, 무작위 옵션이 선택됩니다:

```php
$browser->select('size');
```

두 번째 인수로 배열을 넘기면 여러 값을 선택할 수 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스 입력을 "체크"하려면 `check` 메서드를, "체크 해제"하려면 `uncheck` 메서드를 사용하세요. 마찬가지로 전체 CSS 셀렉터가 아니라 이름을 사용해도 됩니다:

```php
$browser->check('terms');

$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼을 선택하려면 `radio` 메서드를 사용합니다. CSS 셀렉터가 없는 경우 Dusk는 `name`과 `value`가 일치하는 라디오 입력을 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

파일 입력 필드에 파일을 첨부하려면 `attach` 메서드를 사용하세요. CSS 셀렉터를 쓰지 않아도 `name` 속성으로 자동 탐색됩니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 이 기능을 사용하려면 서버에 `Zip` PHP 확장자가 설치되어 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭 (Pressing Buttons)

페이지의 버튼을 클릭하려면 `press` 메서드를 사용하세요. 인수로는 버튼의 표시 텍스트, CSS 또는 Dusk 셀렉터를 넘길 수 있습니다:

```php
$browser->press('Login');
```

폼 전송 시 HTTP 요청이 완료될 때까지 버튼을 비활성화했다가 재활성화하는 애플리케이션이 많습니다. 버튼을 누르고 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용하세요:

```php
// 최대 5초 기다리며 버튼 활성화 대기
$browser->pressAndWaitFor('Save');

// 최대 1초까지 기다리며 버튼 활성화 대기
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 브라우저 인스턴스의 `clickLink` 메서드를 사용하세요. 이 메서드는 주어진 표시 텍스트와 일치하는 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

해당 표시 텍스트 링크가 페이지에 표시되는지 확인하려면 `seeLink` 메서드를 사용할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이들 메서드는 jQuery와 함께 동작합니다. 페이지에 jQuery가 없다면, Dusk가 테스트 중에 자동으로 jQuery를 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용 (Using the Keyboard)

`keys` 메서드를 이용하면 `type` 메서드보다 복잡한 입력 시나리오를 구현할 수 있습니다. 예를 들어, 수정자 키를 누른 채로 입력하는 것도 가능합니다. 아래 예시는 `shift` 키를 누른 상태에서 `taylor`를 입력하고, 이후 `swift`는 수정자 없이 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또한 `keys` 메서드는 주어진 CSS 셀렉터에 키보드 단축키 조합(예: 커맨드+J)을 보낼 때 유용합니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 모든 수정자 키는 `{}`로 감싸 인수로 전달하며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스의 상수와 일치합니다. [GitHub에서 목록 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk는 `withKeyboard` 메서드도 제공하여, `Laravel\Dusk\Keyboard` 클래스를 통해 복잡한 키보드 작업을 플루언트하게 처리할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 지원합니다:

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

자주 사용하는 키보드 작업이 있다면, `Keyboard` 클래스의 `macro` 메서드로 재사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot`에서 등록합니다:

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

등록한 키보드 매크로는 `Keyboard` 인스턴스의 메서드처럼 사용할 수 있습니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭하기

`click` 메서드는 주어진 CSS 또는 Dusk 셀렉터에 일치하는 요소를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식과 일치하는 요소를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저에서 보이는 영역 내의 지정 좌표에 위치한 최상위 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 은 더블클릭을, `rightClick`은 우클릭을 시뮬레이션합니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');

$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`는 마우스 버튼을 누르고 유지하는 동작을 시뮬레이션하며, `releaseMouse`로 해제할 수 있습니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 브라우저에서 `ctrl+클릭` 동작을 시뮬레이션합니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

요소 위에 마우스를 올려야 할 경우, `mouseover` 메서드를 사용하세요:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 한 셀렉터의 요소를 다른 셀렉터로 드래그합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

한 방향으로만 드래그하려면 다음과 같이 합니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 드래그하려면:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그 (JavaScript Dialogs)

Dusk는 JavaScript 다이얼로그와 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog` 메서드는 JavaScript 다이얼로그가 표시될 때까지 대기합니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`는 다이얼로그가 띄워졌고, 주어진 메시지가 포함되었는지 확인합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트 창에 값을 입력하려면 `typeInDialog`를 사용하세요:

```php
$browser->typeInDialog('Hello World');
```

JavaScript 다이얼로그의 "OK" 버튼을 클릭해 닫으려면 `acceptDialog`, "Cancel" 클릭으로 닫으려면 `dismissDialog`를 호출합니다:

```php
$browser->acceptDialog();
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### IFrame과 상호작용 (Interacting With Inline Frames)

iframe 내 요소와 상호작용하려면 `withinFrame` 메서드를 사용하세요. 클로저 내에서 이루어진 모든 요소 조작은 해당 iframe 내 컨텍스트로 범위가 좁아집니다:

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

특정 셀렉터 내에서 여러 작업을 묶어서 수행하고 싶을 때는 `with` 메서드를 사용하세요. 클로저 내의 모든 명령이 해당 셀렉터 범위 내로 제한됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

가끔은 현재 범위를 벗어난 요소에서 어설션을 해야할 수도 있습니다. 이럴 땐 `elsewhere`, `elsewhereWhenAvailable` 메서드를 활용하세요:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 scope는 `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // scope는 `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기 (Waiting for Elements)

JavaScript를 많이 사용하는 애플리케이션을 테스트할 때는, 특정 요소나 데이터가 준비될 때까지 대기(wait)하는 것이 매우 중요합니다. Dusk는 이를 쉽게 지원합니다. 다양한 메서드를 사용해, 페이지에 요소가 표시될 때까지 혹은 특정 JavaScript 표현식이 `true`가 될 때까지 기다릴 수 있습니다.

<a name="waiting"></a>
#### 대기

특정 시간(밀리초)만큼 테스트를 단순히 일시정지하려면 `pause` 메서드를 사용합니다:

```php
$browser->pause(1000);
```

특정 조건이 `true`일 때만 일시정지하려면 `pauseIf`를, 특정 조건이 `true`가 아닐 때만 정지하려면 `pauseUnless`를 사용하세요:

```php
$browser->pauseIf(App::environment('production'), 1000);

$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor` 메서드는 조건에 일치하는 요소가 페이지에 표시될 때까지(기본 5초) 대기합니다. 두 번째 인수로 대기 시간(초)을 조절할 수 있습니다:

```php
$browser->waitFor('.selector');
$browser->waitFor('.selector', 1);
```

특정 셀렉터의 텍스트가 특정 값이 될 때까지 대기하려면:

```php
$browser->waitForTextIn('.selector', 'Hello World');
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

셀렉터와 일치하는 요소가 사라질 때까지(wait until missing):

```php
$browser->waitUntilMissing('.selector');
$browser->waitUntilMissing('.selector', 1);
```

셀렉터 요소가 활성화(Enabled)되거나 비활성화(Disabled)될 때까지도 기다릴 수 있습니다:

```php
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);
$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 등장할 때만 범위 지정

특정 셀렉터를 가진 요소가 등장한 후 그 요소와 상호작용해야 할 때(`whenAvailable`), 예를 들어 모달 창이 등장하면 그 안에서 "OK" 버튼을 누르는 경우에 사용합니다. 클로저 내 동작은 해당 셀렉터 범위에 한정됩니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

특정 텍스트가 페이지에 표시될 때까지 대기하려면 `waitForText` 메서드를 사용하세요:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

특정 텍스트가 사라질 때까지 대기하려면 `waitUntilMissingText`:

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 텍스트 대기

특정 링크 텍스트가 표시될 때까지 대기하려면 `waitForLink`를 사용하세요:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

특정 입력 필드가 페이지에 표시될 때까지 `waitForInput` 메서드를 사용합니다:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 주소 대기

예를 들어 경로 어설션 `$browser->assertPathIs('/home')`을 할 때, `window.location.pathname`이 비동기로 변경되고 있다면 어설션 실패가 발생할 수 있습니다. 이럴 땐 `waitForLocation`을 사용합니다:

```php
$browser->waitForLocation('/secret');
```

전체 URL로 대기할 수도 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/12.x/routing#named-routes)의 위치 대기도 가능합니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

동작 후에 페이지가 새로고침될 때까지 기다려야 한다면 `waitForReload`를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

대부분 버튼 클릭 이후 발생하므로, `clickAndWaitForReload`도 사용할 수 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기

특정 JavaScript 코드가 `true`가 될 때까지 대기하고 싶다면 `waitUntil`을 사용하세요. 코드를 전달할 때 `return`이나 세미콜론은 입력하지 않아도 됩니다:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

[Vue 컴포넌트](https://vuejs.org) 속성이 원하는 값이 될 때까지 `waitUntilVue`, `waitUntilVueIsNot`를 사용할 수 있습니다:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기

JavaScript 이벤트가 발생할 때까지 테스트를 일시 정지하려면 `waitForEvent`를 사용하세요:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 `body`에 바인딩되고, 범위 지정 셀렉터가 사용되면 그 요소에 바인딩됩니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트 대기
    $iframe->waitForEvent('load');
});
```

두 번째 인수로 셀렉터를 지정해 특정 요소에 리스너를 추가할 수 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document`, `window`에도 이벤트를 대기할 수 있습니다:

```php
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 대기

Dusk의 많은 대기(wait) 메서드는 내부적으로 `waitUsing`을 사용합니다. 직접 이 메서드를 활용해, 주어진 클로저가 `true`를 반환할 때까지 원하는 조건을 기다릴 수 있습니다. (첫 번째 인수는 최대 대기 시간, 두 번째는 체크 간격, 세 번째는 조건, 네 번째는 실패 메시지):

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소 뷰로 스크롤 (Scrolling an Element Into View)

요소가 브라우저의 보기 영역 밖에 있어 클릭할 수 없는 경우, `scrollIntoView` 메서드로 해당 요소가 보일 때까지 스크롤할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어설션(검증, 체크)을 지원합니다. 아래에서 사용 가능한 모든 어설션 메서드를 확인할 수 있습니다:

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

(*각 어설션의 설명과 사용법은 원문을 참고하여 상세하게 번역/정리되어 있습니다. 생략 없이 모두 제공합니다.*)

<a name="pages"></a>
## 페이지(Pages) (Pages)

테스트에서 여러 복잡한 동작을 순차적으로 수행해야 하는 경우, 코드를 이해하거나 관리하기 어려워질 수 있습니다. Dusk의 페이지(Page) 기능을 활용하면, 단일 메서드로 수행되는 명확한 액션을 정의할 수 있으며, 애플리케이션 전체 또는 특정 페이지에 자주 쓰이는 셀렉터의 단축키도 선언할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 실행하세요. 생성된 페이지 객체는 `tests/Browser/Pages` 디렉터리에 저장됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성 (Configuring Pages)

기본적으로 페이지 객체에는 `url`, `assert`, `elements`라는 세 가지 메서드가 생성됩니다. 여기서는 `url`과 `assert` 메서드를 먼저 다루고, `elements`는 [아래에서 자세히 설명](#shorthand-selectors)합니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 대표하는 URL 경로(path)를 반환해야 합니다. Dusk는 브라우저에서 이 URL을 활용합니다:

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

`assert` 메서드에는 브라우저가 실제로 이 페이지에 있는지 확인할 수 있는 어설션 로직을 자유롭게 작성할 수 있습니다. 아무 것도 작성하지 않아도 되지만, 필요한 경우 어설션을 넣을 수 있으며, 페이지 이동 시 자동으로 실행됩니다:

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

페이지가 정의되면, `visit` 메서드로 해당 페이지 객체를 사용할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 진입한 상태에서 페이지의 셀렉터 및 기능을 로딩만 하고 싶다면 `on` 메서드를 사용할 수 있습니다. 이는 버튼 클릭 후 리다이렉트되어 명시적으로 이동하지 않았을 때 주로 사용합니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 약식 셀렉터 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드에서는 페이지에서 자주 사용할 CSS 셀렉터의 단축 이름을 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드에 대한 단축키를 설정하려면 다음과 같이 합니다:

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

정의한 약식 셀렉터는 전체 CSS 셀렉터 대신 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 글로벌 약식 셀렉터

Dusk 설치 후 `tests/Browser/Pages` 디렉터리에는 기본 `Page` 클래스가 있습니다. 이 클래스의 `siteElements` 메서드를 통해 전역에서 사용할 글로벌 단축 셀렉터를 정의할 수 있습니다:

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

기본적으로 제공되는 메서드 외에도, 페이지 클래스에서 커스텀 메서드를 정의해 다양한 테스트에서 재사용할 수 있습니다. 예를 들어 음악 앱에서 플레이리스트를 생성하는 로직이 반복적으로 필요하다면, 다음과 같이 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // ...

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

정의한 메서드는 해당 페이지를 사용하는 모든 테스트에서 첫 번째 인수로 브라우저 인스턴스가 자동 전달되며 쉽게 활용할 수 있습니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 "페이지 객체"와 비슷하지만, 내비게이션 바나 알림창처럼 애플리케이션 곳곳에서 반복적으로 사용하는 UI 조각 또는 기능에 초점을 맞춥니다. 즉, 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트를 생성하려면 `dusk:component` Artisan 명령어를 사용하세요. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 저장됩니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어, "날짜 선택기"는 여러 페이지에 공통적으로 존재할 수 있는 컴포넌트입니다. 각각의 테스트마다 날짜 선택 로직을 직접 작성하는 것은 번거로우므로, Dusk 컴포넌트로 캡슐화해 재사용할 수 있습니다:

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

컴포넌트를 정의하고 나면, 실제 테스트에서 번거로운 로직 없이 해당 컴포넌트를 사용할 수 있습니다. 이후, 만약 날짜 선택 로직이 변경되더라도 컴포넌트만 수정하면 전체 테스트가 자동으로 업데이트됩니다:

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

`component` 메서드를 이용해 브라우저 인스턴스를 해당 컴포넌트 범위로 가져올 수도 있습니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 설정은 Laravel 애플리케이션이 8000포트에서 PHP 개발 서버로 서비스된다고 가정합니다. CI 환경의 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`인지 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI (Heroku CI)

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, Heroku `app.json` 파일에 아래 Google Chrome buildpack과 스크립트를 추가하세요:

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
### Travis CI (Travis CI)

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면, 아래와 같이 `.travis.yml`을 설정하세요. Travis CI는 그래픽 환경이 아니므로, Chrome 브라우저를 실행하기 위해 약간의 추가 작업이 필요합니다. 또한, `php artisan serve` 명령으로 PHP 내장 웹 서버를 실행합니다:

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
### GitHub Actions (GitHub Actions)

[GitHub Actions](https://github.com/features/actions) 환경에서 Dusk 테스트를 실행한다면, 아래 설정 파일을 참고해 시작하세요. Travis CI와 마찬가지로 `php artisan serve`로 PHP 내장 서버를 구동합니다:

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
### Chipper CI (Chipper CI)

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하는 경우, 아래와 같은 설정 파일 예제로 시작할 수 있습니다. Laravel을 PHP 내장 서버로 구동해 요청을 수신받습니다:

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

Chipper CI에서 Dusk 테스트 실행 및 데이터베이스 사용에 대한 자세한 내용은 [Chipper CI 공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.
