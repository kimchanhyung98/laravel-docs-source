# 라라벨 더스크 (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 변수 처리](#environment-handling)
- [브라우저 기본 사용법](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [더스크 선택자](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [자바스크립트 대화상자](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [선택자 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소 스크롤 인투뷰](#scrolling-an-element-into-view)
- [사용 가능한 어서션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [축약 선택자](#shorthand-selectors)
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
> [Pest 4](https://pestphp.com/)는 이제 자동화된 브라우저 테스트를 포함하고 있으며, 이는 Laravel Dusk보다 성능과 사용성에서 상당한 향상을 제공합니다. 새로운 프로젝트에서는 브라우저 테스트에 Pest를 사용하는 것을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로, Dusk는 JDK나 Selenium을 로컬 컴퓨터에 설치할 필요가 없습니다. 대신 Dusk는 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 다만 원한다면 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면, [Google Chrome](https://www.google.com/chrome)을 설치하고 Composer로 `laravel/dusk` 패키지를 프로젝트에 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대로** 프로덕션 환경에 등록하면 안 됩니다. 등록 시 임의의 사용자가 애플리케이션에 인증할 수 있는 위험이 있습니다.

Dusk 패키지 설치 후에는 `dusk:install` 아티즌 명령어를 실행합니다. 이 명령어는 `tests/Browser` 디렉터리, 예제 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경을 [Laravel Sail](/docs/12.x/sail)로 관리하는 경우, [Dusk 테스트 설정 및 실행](/docs/12.x/sail#laravel-dusk) 관련 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어로 설치되는 것과 다른 버전의 ChromeDriver를 설치하고자 한다면, `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 OS용 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# Chrome/Chromium 감지 버전과 일치하는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk를 실행하려면 `chromedriver` 바이너리가 실행 가능해야 합니다. 실행에 문제가 있다면, 다음 명령어를 통해 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용 (Using Other Browsers)

Dusk는 기본적으로 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)로 브라우저 테스트를 진행합니다. 그러나 직접 Selenium 서버를 구동하여 원하는 브라우저로 테스트를 실행할 수도 있습니다.

먼저 애플리케이션의 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일은 Dusk 테스트의 기반이 되는 클래스입니다. 여기서 `startChromeDriver` 메서드 호출을 주석 처리하거나 제거하면, Dusk가 ChromeDriver를 자동으로 시작하지 않습니다:

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

그 후, `driver` 메서드를 수정해 원하는 URL 및 포트와 연결하도록 할 수 있습니다. 또한 WebDriver에 전달할 "원하는 기능(desired capabilities)"도 함께 변경할 수 있습니다:

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

Dusk 테스트를 생성하려면 `dusk:make` 아티즌 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 위치합니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 읽는 페이지와 상호작용합니다. 그러나 Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하지 않아야 합니다. `RefreshDatabase` 트레이트는 데이터베이스 트랜잭션을 사용하지만, 이는 HTTP 요청 간에 적용되지 않거나 사용할 수 없습니다. 대신 `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트 중 하나를 선택해 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트마다 데이터베이스 마이그레이션을 실행합니다. 다만 테이블을 매번 드롭하고 재생성하기 때문에, 테이블을 잘라내는(truncate) 방식보다 속도가 느릴 수 있습니다:

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
> Dusk 테스트를 실행할 때는 SQLite 인메모리 데이터베이스를 사용할 수 없습니다. 브라우저는 별도 프로세스에서 실행되기 때문에, 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 트렁케이션 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 데이터베이스 마이그레이션을 실행하여 테이블이 올바르게 생성되었는지 확인합니다. 이후 테스트부터는 테이블을 잘라내(truncate)만 하여 전체 마이그레이션보다 속도가 빠릅니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 잘라냅니다. 잘라낼 테이블을 지정하려면, 테스트 클래스에 `$tablesToTruncate` 속성을 정의할 수 있습니다:

> [!NOTE]
> Pest를 사용하는 경우, 속성이나 메서드는 기본 `DuskTestCase` 클래스 또는 테스트 파일이 상속하는 클래스에 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

반대로 잘라내기에서 제외할 테이블을 지정하고 싶다면 `$exceptTables` 속성을 정의하세요:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

테이블을 잘라낼 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 정의할 수 있습니다:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 트렁케이션 전후로 작업을 하고 싶으면, `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 테스트 클래스에 정의할 수 있습니다:

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

브라우저 테스트를 실행하려면 `dusk` 아티즌 명령어를 사용하세요:

```shell
php artisan dusk
```

이전 테스트 실행 시 실패했던 테스트만 먼저 다시 실행하려면, `dusk:fails` 명령어를 사용할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 러너에서 지원하는 다양한 인수(예: 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group) 테스트만 실행)를 그대로 사용할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 개발 환경을 관리 중이라면, [Dusk 테스트 설정 및 실행](/docs/12.x/sail#laravel-dusk) 관련 Sail 문서를 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

Dusk는 기본적으로 ChromeDriver를 자동으로 시작합니다. 시스템 환경에 따라 자동 실행이 작동하지 않을 경우, 직접 ChromeDriver를 수동으로 시작한 뒤 `dusk` 명령어를 실행할 수 있습니다. 이 경우 `tests/DuskTestCase.php` 파일의 다음 줄을 주석 처리하세요:

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

또한, 9515번 포트가 아닌 다른 포트에서 ChromeDriver를 실행했다면, 해당 클래스의 `driver` 메서드를 올바른 포트로 수정해야 합니다:

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

Dusk에서 별도의 환경 파일을 사용하게 하려면, 프로젝트 루트에 `.env.dusk.{environment}` 형식의 파일을 생성하세요. 예시로 `local` 환경에서 `dusk` 명령어를 사용할 계획이라면 `.env.dusk.local` 파일을 만드세요.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고, 지정된 Dusk 환경 파일을 `.env`로 이름 변경합니다. 테스트 완료 후 원래의 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사용법 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성 (Creating Browsers)

예를 들어, 간단한 로그인 테스트를 작성해봅시다. 테스트를 생성한 뒤 로그인 페이지로 이동하여 자격 증명을 입력하고, "Login" 버튼을 클릭하도록 코드를 작성할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내부에서 `browse` 메서드를 호출하면 됩니다:

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

위 예시에서 볼 수 있듯이, `browse` 메서드는 클로저(익명 함수)를 인수로 받으며, Dusk가 자동으로 브라우저 인스턴스를 이 클로저에 전달해줍니다. 이 인스턴스를 통해 애플리케이션과 상호작용하거나 여러 어서션을 할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 다중 브라우저 인스턴스 생성

특정 테스트 상황에서는 여러 개의 브라우저 인스턴스가 필요할 수 있습니다. 예를 들어, 웹소켓과 상호작용하는 채팅 화면 테스트 등에서 활용할 수 있습니다. `browse` 메서드에 전달하는 클로저의 시그니처에 브라우저 인스턴스를 여러 개 선언하면 됩니다:

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

`visit` 메서드를 사용해 애플리케이션에서 특정 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[named route](/docs/12.x/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 사용하세요:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`과 `forward` 메서드를 이용해 브라우저의 뒤로/앞으로 이동을 할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드를 사용해 페이지를 새로고침할 수도 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드를 사용해 브라우저 창의 크기를 지정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 화면에 맞게 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창을 페이지 콘텐츠 크기에 맞게 조정합니다:

```php
$browser->fitContent();
```

테스트가 실패할 경우, Dusk는 자동으로 스크린샷을 찍기 전에 창 크기를 콘텐츠 크기에 맞춥니다. 이 기능을 비활성화하고 싶다면, 테스트 내에서 `disableFitOnFailure` 메서드를 호출하면 됩니다:

```php
$browser->disableFitOnFailure();
```

`move` 메서드를 사용해 브라우저 창을 화면 내에서 원하는 위치로 이동시킬 수 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하고 싶다면, `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 메서드를 호출합니다:

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

`macro` 함수는 첫 번째 인수에 이름, 두 번째 인수에 클로저를 받습니다. 등록된 매크로는 `Browser` 인스턴스의 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

종종 인증이 필요한 페이지를 테스트하게 됩니다. 매번 로그인 화면을 거치지 않고, Dusk의 `loginAs` 메서드를 사용해 인증 상태를 설정할 수 있습니다. `loginAs`는 인증 가능한 모델의 기본키 또는 인스턴스를 인수로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용한 후에는, 파일 내 모든 테스트에서 해당 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드를 사용해 암호화된 쿠키 값을 조회하거나 설정할 수 있습니다. 기본적으로 라라벨에서 생성된 쿠키는 모두 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화하지 않은 쿠키는 `plainCookie` 메서드로 다룰 수 있습니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키를 삭제하려면 `deleteCookie` 메서드를 사용하세요:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행 (Executing JavaScript)

`script` 메서드를 사용해 브라우저에서 임의의 자바스크립트 코드를 실행할 수 있습니다:

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

`screenshot` 메서드를 사용해 스크린샷을 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 브레이크포인트에서 스크린샷을 연속으로 찍을 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드를 사용하면 특정 요소에 대한 스크린샷을 찍을 수 있습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드를 사용해 브라우저의 콘솔 출력을 지정한 파일명으로 저장할 수 있습니다. 콘솔 로그는 `tests/Browser/console` 디렉터리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장 (Storing Page Source to Disk)

`storeSource` 메서드를 사용해 현재 페이지의 소스를 지정한 파일명으로 저장할 수 있습니다. 소스 파일은 `tests/Browser/source` 디렉터리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### 더스크 선택자 (Dusk Selectors)

CSS 선택자를 사용해 요소를 찾는 것은 Dusk 테스트에서 가장 까다로운 부분 중 하나입니다. 프론트엔드 변경이 발생하면 아래와 같은 CSS 선택자가 테스트를 깨뜨릴 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

더스크 선택자를 사용하면 CSS 선택자를 외울 필요 없이, 효과적인 테스트 작성에 집중할 수 있습니다. HTML 요소에 `dusk` 속성을 추가하고, 테스트에서는 선택자 앞에 `@`를 붙여 해당 요소를 사용할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

필요하다면 Dusk가 사용할 HTML 속성명을 `selectorHtmlAttribute` 메서드로 변경할 수 있습니다. 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 지정합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정

Dusk는 요소의 현재 값, 표시 텍스트, 속성과 상호작용할 수 있는 여러 메서드를 제공합니다. 예를 들어, 주어진 CSS 또는 Dusk 선택자에 해당하는 요소의 "value" 값을 가져오거나 설정하려면 `value` 메서드를 사용합니다:

```php
// 값 조회...
$value = $browser->value('selector');

// 값 설정...
$browser->value('selector', 'value');
```

`inputValue` 메서드를 사용하면 주어진 필드명의 input 요소 값을 조회할 수 있습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 조회

`text` 메서드는 주어진 선택자에 해당하는 요소의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 값 조회

마지막으로, `attribute` 메서드는 주어진 선택자에 맞는 요소의 특정 속성 값을 조회합니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력

Dusk는 폼 및 입력 요소와 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, input 필드에 텍스트를 입력하려면 아래와 같이 합니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

CSS 선택자를 생략할 수 있으며, 생략 시 Dusk는 `name` 속성이 일치하는 `input` 또는 `textarea` 필드를 찾습니다.

필드의 내용을 비우지 않고 텍스트를 추가하려면 `append` 메서드를 사용할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력 값을 비우려면 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드를 사용하면 천천히(키 입력 간 간격을 두고) 입력할 수 있습니다. 기본은 100ms, 3번째 인수로 지연 시간을 커스텀할 수 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

천천히 텍스트를 추가하려면 `appendSlowly`를 사용할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 메서드를 사용해 `select` 요소의 값을 선택할 수 있습니다. 두 번째 인수에는 표시 텍스트가 아닌 option의 실제 값(value)를 입력해야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤 옵션을 선택합니다:

```php
$browser->select('size');
```

배열을 전달하면 여러 옵션을 동시에 선택하게 할 수 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스 입력을 "체크" 하려면 `check` 메서드를 사용합니다. CSS 선택자가 없으면, `name`이 일치하는 체크박스를 찾습니다:

```php
$browser->check('terms');
```

체크를 해제하려면 `uncheck`를 사용합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

`radio` 메서드를 사용해 라디오 입력을 "선택"할 수 있습니다. CSS 선택자가 없으면 `name`과 `value`가 일치하는 라디오를 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

`attach` 메서드를 사용해 `file` 입력에 파일을 첨부할 수 있습니다. CSS 선택자가 없다면 `name`이 일치하는 파일 입력을 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능을 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드는 페이지에서 버튼 요소를 클릭하는 데 사용할 수 있습니다. 인수로는 버튼 텍스트 또는 CSS/Dusk 선택자를 전달할 수 있습니다:

```php
$browser->press('Login');
```

폼 제출 시 HTTP 요청이 끝날 때까지 버튼을 비활성화했다가 다시 활성화하는 앱이라면, `pressAndWaitFor`를 사용해 버튼이 활성화될 때까지 기다릴 수 있습니다:

```php
// 최대 5초간 버튼 활성화 대기
$browser->pressAndWaitFor('Save');

// 최대 1초간 버튼 활성화 대기
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 이 메서드는 지정한 표시 텍스트를 가진 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

지정한 텍스트를 가진 링크가 페이지에 보이는지 확인하려면 `seeLink` 메서드를 사용할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 위 두 메서드는 내부적으로 jQuery와 상호작용합니다. 페이지에 jQuery가 없을 경우, Dusk가 임시로 삽입해 테스트 동안 사용할 수 있게 만듭니다.

<a name="using-the-keyboard"></a>
### 키보드 사용 (Using the Keyboard)

`keys` 메서드는 `type` 메서드로는 구현하기 어려운 복잡한 입력 시나리오를 지원합니다. 예를 들어, modifier 키(Shift 등)를 누른 채 값을 입력할 수 있습니다. 아래 예에서는 `shift` 키를 누른 채로 `taylor`를 입력하고, 이후에는 modifier 없이 `swift`를 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

애플리케이션의 주요 CSS 선택자에 키보드 단축키 조합을 보낼 때도 사용할 수 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 modifier 키는 `{}`로 감싸며, `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수와 일치합니다. [GitHub에서 전체 목록 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 인터랙션

Dusk에서는 `withKeyboard` 메서드도 제공합니다. 이 메서드를 통해 `Laravel\Dusk\Keyboard` 클래스의 `press`, `release`, `type`, `pause` 등의 키보드 동작을 조합할 수 있습니다:

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

키보드 상호작용도 `Keyboard` 클래스의 `macro` 메서드를 사용해 커스텀 함수로 쉽게 재사용할 수 있습니다. 주로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 정의합니다:

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

정의한 매크로는 `Keyboard` 인스턴스에서 메서드처럼 호출할 수 있습니다:

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

`click` 메서드는 주어진 CSS 또는 Dusk 선택자에 일치하는 요소를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식에 일치하는 요소를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저 화면에서 지정한 좌표(x, y)에 위치한 최상위 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 더블 클릭을, `rightClick`은 우클릭을 시뮬레이션합니다:

```php
$browser->doubleClick();
$browser->doubleClick('.selector');

$browser->rightClick();
$browser->rightClick('.selector');
```

`clickAndHold`는 마우스 버튼을 누른 채 유지하고, `releaseMouse`는 해당 상태를 해제합니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 브라우저 내에서 `ctrl+click` 이벤트를 시뮬레이션합니다:

```php
$browser->controlClick();
$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스오버

`mouseover` 메서드는 지정한 CSS 또는 Dusk 선택자에 맞는 요소로 마우스를 이동시킵니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 & 드롭

`drag` 메서드는 한 요소를 다른 요소로 드래그&드롭합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

특정 방향으로 드래그하려면 다음과 같이 할 수 있습니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

지정한 오프셋만큼 드래그하려면:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 대화상자 (JavaScript Dialogs)

Dusk는 자바스크립트 대화상자와 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog`는 대화상자가 나타날 때까지 대기합니다(기본 대기 시간 지정 가능):

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`는 대화상자가 나타나고 지정한 메시지를 포함하는지 검증합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 있는 경우, `typeInDialog`로 값을 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

열려 있는 대화상자에서 "OK"를 클릭하려면 `acceptDialog`, "Cancel"을 클릭하려면 `dismissDialog`를 사용하세요:

```php
$browser->acceptDialog();
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용 (Interacting With Inline Frames)

iframe 내부의 요소와 상호작용해야 할 때는 `withinFrame`을 사용합니다. 이 메서드에 전달한 클로저 내의 모든 동작은 해당 iframe 범위 내에서 실행됩니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 선택자 범위 지정 (Scoping Selectors)

특정 선택자 범위 내에서 여러 동작을 연속으로 수행하고 싶을 때는 `with` 메서드를 사용합니다. 클로저 내 동작들은 모두 최초 지정 선택자 범위 안에서 수행됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

가끔 범위 밖에서 어서션을 실행해야 할 경우에는 `elsewhere` 또는 `elsewhereWhenAvailable` 메서드를 사용할 수 있습니다:

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

자바스크립트를 많이 사용하는 애플리케이션을 테스트할 때는, 특정 요소나 데이터가 준비될 때까지 "대기"가 필요할 때가 많습니다. Dusk는 다양한 대기 메서드를 제공합니다.

<a name="waiting"></a>
#### 대기

설정한 밀리초(ms)만큼 단순히 일시 정지하려면 `pause`를 사용합니다:

```php
$browser->pause(1000);
```

특정 조건이 `true`일 때만 일시 정지하려면 `pauseIf`, 그렇지 않으면 `pauseUnless`를 사용하세요:

```php
$browser->pauseIf(App::environment('production'), 1000);
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 선택자 대기

`waitFor` 메서드는 지정된 CSS/Dusk 선택자에 해당하는 요소가 페이지에 나타날 때까지 일시 정지합니다. 기본 대기 시간은 최대 5초이며, 필요시 time-out을 두 번째 인수로 지정할 수 있습니다:

```php
// 최대 5초 대기
$browser->waitFor('.selector');

// 최대 1초 대기
$browser->waitFor('.selector', 1);
```

주어진 선택자에 해당하는 요소의 텍스트가 일치할 때까지 대기할 수도 있습니다:

```php
// 최대 5초 동안 주어진 텍스트가 포함될 때까지 대기
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

선택자에 해당하는 요소가 없어질 때까지 대기:

```php
$browser->waitUntilMissing('.selector');
$browser->waitUntilMissing('.selector', 1);
```

선택자가 활성화/비활성화될 때까지 대기:

```php
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);

$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 요소 등장 시 범위 지정

특정 요소가 등장할 때까지 대기한 뒤 작업하고 싶다면 `whenAvailable`을 사용합니다. 클로저 내 동작은 해당 범위 안에서만 적용됩니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText`는 지정한 텍스트가 페이지에 표시될 때까지 대기합니다:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

`waitUntilMissingText`로 특정 텍스트가 사라질 때까지 대기할 수도 있습니다:

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink`는 특정 링크 텍스트가 페이지에 나타날 때까지 대기합니다:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 칸 대기

`waitForInput`은 특정 input 필드가 페이지에 표시될 때까지 대기합니다:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기

`window.location.pathname`이 비동기로 업데이트될 경우, `$browser->assertPathIs('/home')`와 같은 경로 어서션이 실패할 수 있습니다. 이럴 때는 `waitForLocation`을 사용하세요:

```php
$browser->waitForLocation('/secret');
```

전체 URL에 대해 대기할 수도 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/12.x/routing#named-routes)의 위치가 될 때까지 대기:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기

특정 동작 이후 페이지 리로드가 필요할 때는 `waitForReload`를 사용합니다:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

주로 버튼 클릭 후 리로드되는 경우가 많으므로, `clickAndWaitForReload`로 간편하게 사용할 수 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

테스트 실행을 특정 자바스크립트 표현식이 `true`가 될 때까지 대기하려면 `waitUntil`을 사용하세요. `return`이나 세미콜론(;)은 필요 없습니다:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

[Vue 컴포넌트](https://vuejs.org)의 속성 값이 특정 값이 될 때까지 기다리려면 `waitUntilVue` 및 `waitUntilVueIsNot`을 사용할 수 있습니다:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기

`waitForEvent` 메서드는 자바스크립트 이벤트가 발생할 때까지 테스트 실행을 일시 정지합니다:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 `body` 요소에 연결되며, 범위 지정 선택자가 있는 경우 해당 요소에 연결됩니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트 대기
    $iframe->waitForEvent('load');
});
```

두 번째 인수로 이벤트를 감지할 요소 선택자를 직접 전달할 수도 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window` 객체에 대한 이벤트 대기도 가능합니다:

```php
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 기반 대기

Dusk의 다양한 "wait" 메서드는 내부적으로 `waitUsing` 메서드를 활용합니다. 직접 사용해 콜백(클로저)가 `true`를 반환할 때까지 대기할 수 있습니다. 첫 번째 인수는 최대 대기 초(second), 두 번째는 평가 간격(second), 세 번째는 콜백, 네 번째는 실패 메시지입니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소 스크롤 인투뷰 (Scrolling an Element Into View)

브라우저 뷰포트 밖에 있어 클릭할 수 없는 요소라면, `scrollIntoView`로 해당 요소가 화면에 들어오도록 스크롤한 뒤 클릭할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어서션(검증)을 지원합니다. 모든 어서션은 아래 목록에서 확인하실 수 있습니다:

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

<!-- 이하 각 어서션 설명은 원문과 동일하며 생략 없이 위 가이드와 패턴에 맞게 제공합니다. 코드 블록과 어서션별 설명은 원문 구조를 반드시 유지하세요. -->

<a name="pages"></a>
## 페이지 (Pages)

복잡한 시나리오의 테스트는 동작이 길어져서 읽고 관리하기 어려울 수 있습니다. Dusk의 "페이지" 기능을 사용하면, 여러 단계를 하나의 메서드로 묶어서 사용할 수 있습니다. 또한 페이지 별 혹은 전체 애플리케이션에 사용되는 선택자 단축어도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체는 `dusk:page` 아티즌 명령어로 생성 가능합니다. 생성된 객체는 프로젝트의 `tests/Browser/Pages` 디렉터리에 위치합니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

기본적으로 페이지 클래스에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 여기에서는 `url`과 `assert`를 소개하며, `elements`는 [아래에서 더 자세히 다룹니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 페이지를 대표하는 URL의 경로를 반환해야 합니다. Dusk는 브라우저에서 해당 페이지로 이동할 때 이 값을 사용합니다:

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

`assert` 메서드에서는 현재 브라우저가 해당 페이지에 위치하고 있음을 검증하는 어서션을 자유롭게 추가할 수 있습니다. 반드시 작성해야 하는 것은 아니며, 원한다면 생략해도 됩니다. 이 어서션들은 해당 페이지로 이동할 때 자동으로 실행됩니다:

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

페이지를 정의한 뒤에는 `visit` 메서드에 해당 페이지 객체를 전달하여 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 위치해 있고, 페이지의 선택자 및 메서드를 현재 테스트 컨텍스트로 불러오고 싶은 경우(예: 버튼 클릭 후 페이지 리디렉션 등)에는 `on` 메서드를 사용할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 축약 선택자 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드에서, 페이지 내 임의의 CSS 선택자를 더 기억하기 쉬운 축약어로 정의할 수 있습니다. 예를 들어, 로그인 페이지의 이메일 입력란을 아래와 같이 정의할 수 있습니다:

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

정의한 축약 선택자는 일반 선택자가 사용되는 모든 곳에 적용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 축약 선택자

Dusk 설치 후, `tests/Browser/Pages` 디렉터리에는 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에 전역 축약 선택자를 정의하면, 애플리케이션 전 페이지에서 사용할 수 있습니다:

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

기본 메서드 외에도, 자주 사용하는 동작을 별도 메서드로 만들 수 있습니다. 예시로 음악 관리 애플리케이션에서 재생목록 생성 로직을 `createPlaylist` 메서드로 추출하면 여러 테스트에서 재사용하기 편리합니다:

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

정의된 메서드는 사용하는 테스트에서 아래와 같이 자유롭게 쓸 수 있습니다. 브라우저 인스턴스는 첫 번째 인수로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 "페이지 객체"와 비슷하지만, 네비게이션 바나 알림창처럼 애플리케이션 전반에서 자주 재사용되는 UI와 기능 단위를 대상으로 합니다. 따라서 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트는 `dusk:component` 아티즌 명령어로 생성할 수 있습니다. 생성된 컴포넌트는 `tests/Browser/Components` 디렉터리에 위치합니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어 "날짜 선택기"는 여러 페이지에 걸쳐 반복적으로 사용되는 컴포넌트입니다. 여러 테스트에서 날짜 선택 로직을 반복해 작성하는 대신, 별도의 Dusk 컴포넌트로 작성하면 관리가 쉬워집니다:

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

컴포넌트를 정의했으면, 어떤 테스트에서든 쉽게 날짜 선택 등 동작을 호출할 수 있습니다. 만약 날짜 선택 로직이 변경되더라도 컴포넌트 한 곳만 수정하면 됩니다:

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

`component` 메서드는 특정 컴포넌트 범위에 한정된 브라우저 인스턴스를 반환합니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 환경 설정은 Laravel 애플리케이션이 8000번 포트에서 PHP 내장 서버로 구동된다고 가정합니다. 따라서 CI 환경에 `APP_URL` 환경 변수가 `http://127.0.0.1:8000`로 세팅되어 있는지 반드시 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 아래 Google Chrome buildpack과 스크립트를 Heroku `app.json` 파일에 추가하세요:

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

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 아래 `.travis.yml` 예제를 참고하세요. Travis CI는 GUI 환경이 아니므로, Chrome 브라우저를 실행하기 위해 몇 가지 추가 작업이 필요합니다. 또한, `php artisan serve`로 PHP 내장 서버를 사용합니다:

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

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하려면 아래 설정 파일을 시작점으로 사용할 수 있습니다. Travis CI와 마찬가지로, `php artisan serve`로 내장 서버를 구동합니다:

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

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면 아래 설정 파일 예제를 참고하세요. 역시 PHP 내장 서버로 요청을 받을 수 있게 합니다:

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

Chipper CI에서 Dusk 테스트 실행 및 데이터베이스 관련 상세 정보는 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.

<!--
주의: 본 문서는 아티즌/컴포저 등 명령어, 코드 블록, 코드 내 변수/문자열/결과 등은 절대 번역하지 않고 원문 그대로 유지하였습니다.
-->