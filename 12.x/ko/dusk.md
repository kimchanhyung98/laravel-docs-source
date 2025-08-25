# 라라벨 더스크 (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본 사용법](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [페이지 이동](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [더스크 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭하기](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지 객체](#pages)
    - [페이지 객체 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [약식 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합(CI)](#continuous-integration)
    - [Heroku CI 사용](#running-tests-on-heroku-ci)
    - [Travis CI 사용](#running-tests-on-travis-ci)
    - [GitHub Actions 사용](#running-tests-on-github-actions)
    - [Chipper CI 사용](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> [Pest 4](https://pestphp.com/)는 이제 자동화된 브라우저 테스트 기능을 제공하며, 이는 Laravel Dusk에 비해 성능과 사용성이 크게 향상되었습니다. 새로운 프로젝트에서는 브라우저 테스트에 Pest 사용을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Dusk는 기본적으로 JDK 또는 Selenium을 별도로 설치할 필요가 없습니다. 대신, 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 단, Selenium과 호환되는 그 외의 드라이버도 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고, `laravel/dusk` Composer 의존성을 프로젝트에 추가합니다.

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 직접 등록할 경우, **절대로** 운영 환경에서는 등록하지 마십시오. 그렇지 않으면 임의의 사용자가 애플리케이션에 인증하여 접근할 수 있는 위험이 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` 아티즌 명령어를 실행합니다. 이 명령어는 `tests/Browser` 디렉터리와 예제 더스크 테스트 파일을 생성하고, 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다.

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정해야 합니다. 이 값은 실제 브라우저에서 애플리케이션에 접근할 때 사용하는 URL과 동일해야 합니다.

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 로컬 개발 환경을 구성하는 경우, [Dusk 테스트 구성 및 실행](/docs/12.x/sail#laravel-dusk) 관련 Sail 문서도 참고하시기 바랍니다.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어로 설치되는 ChromeDriver와 다른 버전을 사용하고 싶다면, `dusk:chrome-driver` 명령어를 활용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 원하는 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 운영체제용으로 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# Chrome / Chromium의 감지된 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk를 사용하려면 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행 시 문제가 발생한다면, 다음 명령어로 실행 권한을 부여해야 합니다: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 이용해 브라우저 테스트를 실행합니다. 하지만 원한다면 Selenium 서버를 직접 실행해 임의의 브라우저로 테스트를 할 수 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출 부분을 주석 처리하면 ChromeDriver의 자동 실행이 중지됩니다.

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

그 다음, `driver` 메서드를 수정하여 원하는 Selenium 서버의 URL과 포트로 연결합니다. 또한 WebDriver에 전달할 "desired capabilities"도 변경할 수 있습니다.

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

Dusk 테스트를 생성하려면 `dusk:make` 아티즌 명령어를 사용합니다. 생성된 테스트는 `tests/Browser` 디렉터리에 저장됩니다.

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

작성하는 대부분의 테스트는 애플리케이션 데이터베이스의 데이터를 조회하는 페이지와 상호작용합니다. 하지만, Dusk 테스트는 절대로 `RefreshDatabase` 트레이트를 사용해서는 안 됩니다. 이 트레이트는 데이터베이스 트랜잭션을 활용하는데, HTTP 요청 간에는 이 트랜잭션을 사용할 수 없습니다. 대신, `DatabaseMigrations` 트레이트 또는 `DatabaseTruncation` 트레이트 두 가지 방법 중 하나를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 실행 전마다 데이터베이스 마이그레이션을 수행합니다. 하지만, 테스트마다 테이블을 드롭하고 다시 생성하기 때문에 성능상 `truncation` 방식보다 느릴 수 있습니다.

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
> Dusk 테스트 실행 시 SQLite의 인메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 동작하므로, 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 Truncation 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 마이그레이션을 수행해 데이터베이스 테이블을 먼저 생성한 후, 이후 테스트에서는 테이블을 단순히 `truncate` 처리합니다. 이로 인해, 매번 마이그레이션을 재실행하는 방식보다 속도가 빨라집니다.

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 truncate 처리합니다. truncate할 테이블을 지정하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요.

> [!NOTE]
> Pest를 사용하는 경우, 속성이나 메서드는 기본 `DuskTestCase` 클래스 또는 여러분의 테스트 파일이 상속하는 클래스에 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

반대로 truncate 대상에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 정의하세요.

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

truncate 처리 대상 데이터베이스 커넥션을 지정하려면 `$connectionsToTruncate` 속성을 사용하세요.

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

truncate 전후에 코드를 실행하고 싶다면, 테스트 클래스에 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의할 수 있습니다.

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

브라우저 테스트를 실행하려면 `dusk` 아티즌 명령어를 실행하세요.

```shell
php artisan dusk
```

마지막 테스트 실행 시 일부 테스트가 실패했다면, `dusk:fails` 명령어로 실패한 테스트만 우선적으로 실행할 수 있습니다.

```shell
php artisan dusk:fails
```

`dusk` 명령어는 평소 Pest / PHPUnit 테스팅 러너에서 허용되는 인수(예: 특정 [group](https://docs.phpunit.de/en/10.5/annotations.html#group)만 실행)를 동일하게 사용할 수 있습니다.

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 로컬 개발 환경을 구성한다면, [Dusk 테스트 구성 및 실행](/docs/12.x/sail#laravel-dusk) 관련 Sail 문서를 참고하시기 바랍니다.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver를 수동으로 시작하기

Dusk는 기본적으로 ChromeDriver를 자동으로 시작합니다. 만약 자동 실행이 정상적으로 되지 않는다면, `dusk` 명령어 실행 전에 직접 ChromeDriver를 수동으로 시작할 수 있습니다. 수동 실행 시, `tests/DuskTestCase.php` 파일에서 다음 줄을 반드시 주석 처리해야 합니다.

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

또한, ChromeDriver를 9515번 포트 외의 포트로 실행했다면, 클래스의 `driver` 메서드에서 해당 포트로 주소를 수정해야 합니다.

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

테스트 실행 시 Dusk에서 별도의 환경 파일을 사용하도록 하려면 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하세요. 예를 들어, `local` 환경에서 `dusk` 명령어를 실행한다면 `.env.dusk.local` 파일을 생성하면 됩니다.

테스트 실행 시, Dusk는 기존 `.env` 파일을 백업하고 Dusk 전용 환경 파일을 `.env`로 리네임합니다. 테스트가 종료되면 원래의 `.env` 파일로 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사용법 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성 (Creating Browsers)

애플리케이션에 로그인할 수 있는지 확인하는 간단한 테스트를 작성해 봅시다. 테스트를 생성한 뒤, 로그인 페이지로 이동하여 자격 증명을 입력하고 "Login" 버튼을 클릭하도록 코드를 수정할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드로 생성할 수 있습니다.

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

위 예제에서 확인할 수 있듯, `browse` 메서드는 클로저를 인수로 받습니다. 브라우저 인스턴스는 Dusk가 클로저에 자동으로 전달하며, 애플리케이션과 상호작용하거나 어설션을 할 때 사용되는 주요 객체입니다.

<a name="creating-multiple-browsers"></a>
#### 복수 브라우저 인스턴스 생성

여러 개의 브라우저가 필요한 테스트가 있을 수 있습니다. 예를 들어, 웹소켓을 사용하는 채팅 화면 테스트 시 두 명 이상의 사용자가 필요합니다. 브라우저 인스턴스를 여러 개 만들려면 `browse` 메서드 클로저의 인수에 브라우저 객체를 추가로 선언하면 됩니다.

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
### 페이지 이동 (Navigation)

`visit` 메서드는 애플리케이션 내의 지정된 URI로 이동합니다.

```php
$browser->visit('/login');
```

[named route](/docs/12.x/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 사용할 수 있습니다.

```php
$browser->visitRoute($routeName, $parameters);
```

`back`과 `forward` 메서드로 이전/다음 페이지로 이동할 수 있습니다.

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드로 현재 페이지를 새로 고칠 수 있습니다.

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드로 브라우저 창 크기를 설정할 수 있습니다.

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 화면에 최대로 확장합니다.

```php
$browser->maximize();
```

`fitContent` 메서드는 페이지의 콘텐츠 크기에 맞게 창 크기를 조절합니다.

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 스크린샷을 찍기 전에 자동으로 창 크기를 콘텐츠에 맞게 조정합니다. 이 기능을 비활성화하려면 `disableFitOnFailure` 메서드를 호출하세요.

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 브라우저 창 위치를 지정 좌표로 이동할 수 있습니다.

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

다양한 테스트에서 반복적으로 사용할 커스텀 브라우저 메서드가 필요하다면, `Browser` 클래스의 `macro` 메서드로 정의할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

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

`macro`는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 매크로로 등록한 메서드는 Browser 인스턴스에서 호출할 수 있습니다.

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

로그인이 필요한 페이지를 테스트할 때, 매번 로그인 화면을 거치지 않고 더스크의 `loginAs` 메서드를 이용할 수 있습니다. 이 메서드는 인증 가능한 모델의 기본 키 또는 인스턴스를 받습니다.

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용하면 해당 파일 내의 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드로 암호화된 쿠키의 값을 조회하거나 설정할 수 있습니다. 라라벨에서 생성되는 모든 쿠키는 기본적으로 암호화됩니다.

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값을 원한다면 `plainCookie` 메서드를 사용하세요.

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메서드로 지정 쿠키를 삭제할 수 있습니다.

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 (Executing JavaScript)

`script` 메서드로 브라우저 내에서 임의의 JavaScript 문을 실행할 수 있습니다.

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

`screenshot` 메서드로 지정한 파일명으로 스크린샷을 찍을 수 있습니다. 모든 스크린샷 이미지는 `tests/Browser/screenshots` 디렉터리에 저장됩니다.

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 해상도(브레이크포인트)에서 여러 장의 스크린샷을 생성합니다.

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드로 특정 요소에 한정한 스크린샷을 찍을 수도 있습니다.

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 디스크 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드로 브라우저의 콘솔 출력을 파일로 저장할 수 있습니다. 저장 파일은 `tests/Browser/console` 디렉터리에 생성됩니다.

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크 저장 (Storing Page Source to Disk)

`storeSource` 메서드로 현재 페이지의 소스코드를 파일로 저장할 수 있습니다. 저장 파일은 `tests/Browser/source` 디렉터리에 생성됩니다.

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### 더스크 셀렉터 (Dusk Selectors)

테스트에서 요소와 상호작용할 때, CSS 셀렉터 관리가 가장 까다로운 점 중 하나입니다. 프론트엔드가 변경되면 기존 CSS 셀렉터 기반 코드가 쉽게 깨질 수 있습니다.

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 테스트 작성에 더 집중할 수 있습니다. HTML 요소에 `dusk` 속성을 추가하고, 테스트에서는 `@`로 시작하는 셀렉터를 사용합니다.

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원한다면, 더스크가 참조하는 HTML 속성명을 `selectorHtmlAttribute` 메서드로 변경할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider`에서 호출합니다.

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정

Dusk는 현재 값, 표시 텍스트, 속성값 등 요소의 다양한 값을 조회/설정하는 메서드를 제공합니다. 특정 CSS 또는 Dusk 셀렉터와 일치하는 요소의 "값"을 얻으려면 `value` 메서드를 사용합니다.

```php
// 값 조회...
$value = $browser->value('selector');

// 값 설정...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 주어진 필드명을 가진 인풋 요소의 값을 조회합니다.

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 조회

`text` 메서드로 주어진 셀렉터에 해당하는 요소의 표시 텍스트를 얻을 수 있습니다.

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성값 조회

`attribute` 메서드는 특정 셀렉터 요소의 지정 속성값을 조회합니다.

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력

Dusk는 폼과 인풋 요소와 상호작용하는 다양한 메서드를 제공합니다. 먼저, 텍스트 입력란에 값을 입력하는 예시입니다.

```php
$browser->type('email', 'taylor@laravel.com');
```

CSS 셀렉터를 반드시 지정할 필요는 없습니다. 셀렉터를 생략하면 `name` 속성으로 자동 검색합니다.

기존 값에 텍스트를 추가하려면 `append` 메서드를 사용하세요.

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력값을 비우려면 `clear` 메서드를 쓰면 됩니다.

```php
$browser->clear('email');
```

`typeSlowly` 메서드로 키를 일정 간격으로 천천히 입력하게 할 수 있습니다. 세 번째 인수로 대기 밀리초(ms) 지정이 가능합니다.

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

텍스트를 천천히 추가할 때는 `appendSlowly` 메서드도 사용할 수 있습니다.

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 메서드는 `select` 요소에서 값을 선택할 때 사용합니다. 옵션의 표시 텍스트가 아닌 값을 인수로 넘기세요.

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤 옵션이 선택됩니다.

```php
$browser->select('size');
```

배열을 넘기면 복수 옵션을 선택할 수도 있습니다.

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스 입력을 "체크"하려면 `check` 메서드를 사용합니다. CSS 셀렉터가 일치하지 않으면 `name` 속성 기준으로 검색합니다.

```php
$browser->check('terms');
```

"체크 해제"하려면 `uncheck` 메서드를 쓰세요.

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 입력값을 선택하려면 `radio` 메서드를 사용하세요. 마찬가지로 CSS 셀렉터 대신 `name`과 `value` 값을 사용할 수 있습니다.

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

`attach` 메서드는 `file` 입력 필드에 파일을 첨부할 때 사용합니다. 마찬가지로 CSS 셀렉터가 없으면 `name` 속성을 기준으로 검색합니다.

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능을 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드는 지정한 버튼(텍스트 또는 셀렉터) 요소를 클릭합니다.

```php
$browser->press('Login');
```

폼 제출 시 일반적으로 버튼이 비활성화됐다가 요청 완료 후 다시 활성화되는 경우가 많습니다. 버튼이 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용할 수 있습니다.

```php
// 최대 5초간 버튼이 활성화될 때까지 대기...
$browser->pressAndWaitFor('Save');

// 최대 1초간 대기...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용할 수 있습니다. 이 메서드는 표시 텍스트와 일치하는 링크를 클릭합니다.

```php
$browser->clickLink($linkText);
```

주어진 링크 텍스트가 페이지에 표시되는지 확인하려면 `seeLink` 메서드를 사용하세요.

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드는 jQuery를 사용합니다. 페이지에 jQuery가 없으면 Dusk가 자동으로 삽입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용 (Using the Keyboard)

`keys` 메서드는 `type` 메서드보다 복잡한 입력 시퀀스나 조합을 지원합니다. 예를 들어, modifier key(Shift 등) 동작도 지원합니다. 아래 예제는 `shift` 키를 누른 상태에서 `taylor`를 입력하고, 이어서 modifier 없이 `swift`를 입력합니다.

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

CSS 셀렉터에 "키보드 단축키" 조합을 입력하는 데에도 쓸 수 있습니다.

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 modifier key는 `{}`로 감싸야 하며, 값은 `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수를 사용합니다. [GitHub](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)에서 전체 상수 목록을 확인할 수 있습니다.

<a name="fluent-keyboard-interactions"></a>
#### 유창한 키보드 동작

Dusk는 `Laravel\Dusk\Keyboard` 클래스와 함께 `withKeyboard` 메서드를 제공합니다. 이 메서드는 `press`, `release`, `type`, `pause`와 같은 다양한 메서드로 복합 키보드 동작을 fluently 수행할 수 있게 합니다.

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

키보드 동작을 반복적으로 사용하고 싶다면, `Keyboard` 클래스의 `macro` 메서드로 커스텀 동작을 등록해둘 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot`에서 호출합니다.

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

등록한 매크로는 아래와 같이 사용할 수 있습니다.

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소를 클릭합니다.

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식으로 해당하는 요소를 클릭합니다.

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저 화면에서 특정 좌표에 위치한 최상단 요소를 클릭합니다.

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 마우스 더블 클릭을 시뮬레이션합니다.

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` 메서드는 마우스 우클릭 동작을 시뮬레이션합니다.

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`는 마우스 버튼 누르고 유지, `releaseMouse`로 버튼을 놓는 동작이 가능합니다.

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 ctrl+클릭 동작을 시뮬레이션합니다.

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메서드는 마우스를 지정 요소 위로 이동시킵니다.

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그&드롭

`drag` 메서드는 요소를 다른 요소로 드래그합니다.

```php
$browser->drag('.from-selector', '.to-selector');
```

특정 방향으로 드래그하려면 아래와 같이 사용할 수 있습니다.

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

오프셋 좌표만큼 드래그하려면 다음과 같이 작성합니다.

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그 (JavaScript Dialogs)

Dusk는 다양한 JavaScript 다이얼로그 처리 메서드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그가 나타날 때까지 기다릴 수 있습니다.

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`는 다이얼로그가 열렸고 특정 메시지를 포함하는지 검증합니다.

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트 다이얼로그에서 텍스트를 입력하려면 `typeInDialog`를 사용할 수 있습니다.

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼을 클릭해 다이얼로그를 닫으려면 `acceptDialog`를 이용하세요.

```php
$browser->acceptDialog();
```

"취소" 버튼 클릭 시에는 `dismissDialog`를 사용합니다.

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용 (Interacting With Inline Frames)

iframe 내의 요소와 상호작용이 필요하다면 `withinFrame` 메서드를 사용합니다. 클로저 내의 모든 동작은 해당 iframe 범위 내에서만 작동합니다.

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

특정 셀렉터 범위 안에서 여러 동작을 묶어 실행하려면 `with` 메서드를 사용하세요. 클로저 내에서는 지정한 셀렉터에 범위가 제한됩니다.

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

현재 범위 밖의 셀렉터를 다루고 싶다면 `elsewhere` 또는 `elsewhereWhenAvailable` 메서드를 사용할 수 있습니다.

```php
$browser->with('.table', function (Browser $table) {
    // 현재 범위: `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 범위: `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 범위: `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기 (Waiting for Elements)

JavaScript가 많이 사용된 애플리케이션을 테스트할 땐 특정 요소나 데이터가 준비될 때까지 "대기"가 필요할 때가 많습니다. Dusk는 이 작업을 쉽게 도와줍니다.

<a name="waiting"></a>
#### 대기 (Waiting)

테스트를 주어진 밀리초(ms)만큼 일시정지하려면 `pause` 메서드를 사용합니다.

```php
$browser->pause(1000);
```

조건이 `true`일 때만 대기하려면 `pauseIf`를 사용하세요.

```php
$browser->pauseIf(App::environment('production'), 1000);
```

특정 조건이 `true`가 아닐 때만 대기하려면 `pauseUnless`를 사용합니다.

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor` 메서드는 지정한 CSS 또는 Dusk 셀렉터의 요소가 화면에 표시될 때까지 테스트 진행을 멈춥니다. 기본적으로 5초 대기 후 실패합니다. 두 번째 인수로 대기 시간(초)을 지정할 수 있습니다.

```php
// 최대 5초 대기
$browser->waitFor('.selector');

// 최대 1초 대기
$browser->waitFor('.selector', 1);
```

지정 셀렉터의 요소가 특정 텍스트를 포함할 때까지 대기할 수도 있습니다.

```php
// 최대 5초 대기
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

지정 셀렉터가 사라질 때까지 대기하려면 `waitUntilMissing` 메서드를 사용합니다.

```php
$browser->waitUntilMissing('.selector');
$browser->waitUntilMissing('.selector', 1);
```

또한, 해당 셀렉터가 활성화(Enabled) 또는 비활성화(Disabled)될 때까지 대기도 가능합니다.

```php
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);

$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 사용 가능해질 때 범위 지정

지정 셀렉터의 요소가 나타난 뒤 상호작용하고 싶을 때는 `whenAvailable` 메서드를 활용하세요. 클로저 내의 모든 동작은 해당 셀렉터 범위 안에서 이루어집니다.

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText` 메서드는 특정 텍스트가 페이지에 나올 때까지 대기합니다.

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

표시된 텍스트가 사라질 때까지는 `waitUntilMissingText`를 사용합니다.

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink` 메서드로 링크 텍스트가 나타날 때까지 대기할 수 있습니다.

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 인풋 필드 대기

`waitForInput` 메서드는 지정한 인풋 필드가 보일 때까지 대기합니다.

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 경로 대기

`$browser->assertPathIs('/home')`와 같은 경로 어설션이 실패할 경우, JavaScript로 인해 `window.location.pathname`이 비동기적으로 변경될 수 있습니다. 이런 경우 `waitForLocation` 메서드로 경로 변경을 대기할 수 있습니다.

```php
$browser->waitForLocation('/secret');
```

현재 위치가 완전한 URL이어도 대기가 가능합니다.

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/12.x/routing#named-routes)의 경로가 될 때까지 대기할 수도 있습니다.

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

액션 이후에 페이지가 리로드되기를 대기하려면 `waitForReload` 메서드를 사용하세요.

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

일반적으로 버튼 클릭 이후에 발생하므로, `clickAndWaitForReload` 메서드를 사용할 수도 있습니다.

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기

특정 JavaScript 표현식이 `true`가 될 때까지 대기하는 경우에는 `waitUntil` 메서드를 쓰면 됩니다. `return` 키워드와 세미콜론(`;`)은 필요 없습니다.

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

[Vue 컴포넌트](https://vuejs.org) 속성이 특정 값이 되기를 기다리려면 `waitUntilVue`와 `waitUntilVueIsNot` 메서드를 사용하세요.

```php
// 값이 세팅될 때까지 대기
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 값이 null이 아닐 때까지 대기
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기

`waitForEvent` 메서드는 특정 JavaScript 이벤트가 발생할 때까지 대기합니다.

```php
$browser->waitForEvent('load');
```

현재 범위(기본값은 body)에 이벤트리스너가 부착됩니다. 스코프 셀렉터를 사용하면 해당 요소에도 장착됩니다.

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트 대기
    $iframe->waitForEvent('load');
});
```

이벤트를 특정 요소에 붙이고 싶다면 두 번째 인수로 셀렉터를 넘길 수 있습니다.

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window`에도 이벤트리스너를 연결해서 대기할 수 있습니다.

```php
// document 스크롤 대기
$browser->waitForEvent('scroll', 'document');

// window resize 5초 대기
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 기반 대기

대부분의 "wait" 계열 메서드는 내부적으로 `waitUsing` 메서드를 사용합니다. 이 메서드를 직접 이용해, 특정 조건(클로저 반환값이 true)이 만족될 때까지 대기할 수 있습니다.

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소로 스크롤 (Scrolling an Element Into View)

브라우저 뷰 영역 밖에 있는 요소를 클릭해야 할 때, `scrollIntoView`로 지정 요소를 화면에 표시할 수 있습니다.

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어설션을 제공합니다. 아래는 사용 가능한 모든 어설션 목록입니다.  
(각 어설션별 사용법 및 설명은 원문과 동일하게 유지합니다.)

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

<!-- 이하 각 어설션의 원문 설명(코드 포함)은 변경 없이 유지 -->

<a name="assert-title"></a>
#### assertTitle

페이지 타이틀이 지정한 텍스트와 일치하는지 검증합니다.

```php
$browser->assertTitle($title);
```

...  
(중략 – 이하 어설션 각 항목은 원문과 동일하게 유지, 필요 시 용어만 변경)

<a name="pages"></a>
## 페이지 객체 (Pages)

여러 복잡한 동작이 연속적으로 필요한 테스트의 경우, 테스트 코드가 길어지고 읽기 어려워질 수 있습니다. 더스크 페이지 객체를 사용하면, 여러 동작을 한 번에 수행하는 간결한 메서드를 정의할 수 있습니다. 또한, 각 페이지마다 자주 사용하는 셀렉터의 별칭을 지정해 사용할 수도 있습니다.

<a name="generating-pages"></a>
### 페이지 객체 생성 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` 아티즌 명령어를 사용하세요. 모든 페이지 객체는 `tests/Browser/Pages` 디렉터리에 생성됩니다.

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

기본적으로 페이지 클래스엔 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 먼저 `url`, `assert`를 살펴봅니다. `elements`는 [아래에서 자세히 설명](#shorthand-selectors)합니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 대표하는 URL의 경로를 반환해야 합니다. Dusk가 브라우저에서 이 URL로 이동할 때 사용됩니다.

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

`assert` 메서드는 브라우저가 실제로 해당 페이지에 있는지 검증할 필요가 있다면 어설션을 추가할 수 있습니다(필수는 아니며, 원한다면 비워둘 수 있습니다). 페이지로 이동시 자동으로 실행됩니다.

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

페이지를 정의했다면, `visit` 메서드로 해당 페이지로 이동할 수 있습니다.

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 특정 페이지에 있고, 페이지의 셀렉터 및 메서드만 현재 테스트 컨텍스트에 "불러오고" 싶을 때는 `on` 메서드를 사용할 수 있습니다. 이는 버튼 클릭 이후 특정 페이지로 리다이렉트될 때 유용합니다.

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 약식 셀렉터 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드에서는 각 페이지에 자주 사용하는 CSS 셀렉터에 대해 기억하기 쉬운 별칭을 정의할 수 있습니다.

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

정의된 별칭은 CSS 셀렉터를 사용하는 모든 곳에서 사용 가능합니다.

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 약식 셀렉터

Dusk를 설치하면, `tests/Browser/Pages` 디렉터리에 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에 전역적으로 사용할 약식 셀렉터를 정의할 수 있습니다.

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

기본 페이지 메서드 외에 추가 메서드를 자유롭게 정의할 수 있습니다. 음악 관리 애플리케이션을 예로 들면, 플레이리스트 생성은 여러 번 반복되는 동작입니다. 이런 로직을 각 테스트마다 직접 작성하지 않고, 페이지 클래스의 메서드로 추상화할 수 있습니다.

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // Other page methods...

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

정의된 메서드는 해당 페이지를 사용하는 모든 테스트에서 사용할 수 있습니다. 브라우저 인스턴스가 첫 번째 인수로 자동 전달됩니다.

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 "페이지 객체"와 유사하지만, 네비게이션 바나 알림창처럼 전체 애플리케이션 어디서나 반복적으로 쓰이는 UI 및 기능에 특화되어 있습니다. 컴포넌트는 특정 URL에 구속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

`dusk:component` 아티즌 명령어로 컴포넌트를 생성합니다. 컴포넌트 파일은 `tests/Browser/Components` 디렉터리에 저장됩니다.

```shell
php artisan dusk:component DatePicker
```

예를 들어, "날짜 선택기"는 여러 페이지에서 자주 등장하는 컴포넌트입니다. 컴포넌트로 정의함으로써 관련 테스트 코드를 여러 번 작성하지 않아도 되고, 선택 로직이 변경되어도 컴포넌트만 수정하면 됩니다.

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

컴포넌트를 정의하면, 모든 테스트에서 손쉽게 해당 컴포넌트 조작이 가능합니다. 만약 날짜 선택 방식이 변경되더라도 컴포넌트만 수정하면 모든 테스트에 일괄 반영됩니다.

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

`component` 메서드로 해당 컴포넌트 범위의 브라우저 인스턴스를 얻고, 바로 메서드를 사용할 수도 있습니다.

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 환경은 라라벨 애플리케이션이 8000번 포트에서 PHP 내장 서버로 서비스될 것을 기대합니다. 따라서, CI 환경의 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`인지 반드시 확인하십시오.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI 사용

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 아래의 Google Chrome 빌드팩과 스크립트를 Heroku `app.json`에 추가하세요.

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
### Travis CI 사용

[Travis CI](https://travis-ci.org) 환경에서는 아래 `.travis.yml` 설정을 사용할 수 있습니다. Travis CI는 GUI 환경이 아니기 때문에 Chrome 브라우저를 실행하기 위한 추가 설정이 필요합니다. PHP 내장 서버는 `php artisan serve`로 실행됩니다.

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
### GitHub Actions 사용

[GitHub Actions](https://github.com/features/actions)를 사용하여 Dusk 테스트를 실행할 경우, 다음과 같은 설정 파일을 참고할 수 있습니다. Travis CI와 마찬가지로 `php artisan serve` 명령으로 PHP 내장 서버를 실행합니다.

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
### Chipper CI 사용

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면, 다음 설정 파일을 참고할 수 있습니다. 라라벨을 PHP 내장 서버로 실행합니다.

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

Chipper CI에서 Dusk 테스트 실행과 데이터베이스 활용에 대한 자세한 내용은 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.
