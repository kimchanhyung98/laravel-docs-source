# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성하기](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행하기](#running-tests)
    - [환경 설정 처리하기](#environment-handling)
- [브라우저 기초](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
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
    - [자바스크립트 대화상자](#javascript-dialogs)
    - [인라인 프레임과 상호작용하기](#interacting-with-iframes)
    - [셀이터 범위 지정하기](#scoping-selectors)
    - [요소 대기하기](#waiting-for-elements)
    - [요소를 뷰로 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 어설션(검증)](#available-assertions)
- [페이지](#pages)
    - [페이지 생성하기](#generating-pages)
    - [페이지 구성하기](#configuring-pages)
    - [페이지로 이동하기](#navigating-to-pages)
    - [단축 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성하기](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [지속적 통합](#continuous-integration)
    - [Heroku CI에서 테스트 실행하기](#running-tests-on-heroku-ci)
    - [Travis CI에서 테스트 실행하기](#running-tests-on-travis-ci)
    - [GitHub Actions에서 테스트 실행하기](#running-tests-on-github-actions)
    - [Chipper CI에서 테스트 실행하기](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 뛰어나고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신 Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 하지만, 필요에 따라 다른 Selenium 호환 드라이버를 사용할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고, 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]  
> Dusk 서비스 프로바이더를 수동으로 등록하는 경우, 절대로 프로덕션 환경에서는 등록하면 안 됩니다. 그렇게 할 경우 임의 사용자가 애플리케이션 인증을 할 수 있는 보안 문제가 발생할 수 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉토리, 예제 Dusk 테스트, 그리고 운영체제에 맞는 ChromeDriver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

그 다음, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 URL은 브라우저에서 애플리케이션에 접속할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]  
> 로컬 개발 환경 관리를 위해 [Laravel Sail](/docs/10.x/sail)를 사용 중이라면, Sail 문서의 [Dusk 테스트 설정 및 실행](/docs/10.x/sail#laravel-dusk) 부분도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령으로 설치되는 ChromeDriver 버전 대신 다른 버전을 설치하고 싶다면, `dusk:chrome-driver` 명령어를 사용하세요:

```shell
# 운영체제에 맞는 최신 ChromeDriver를 설치
php artisan dusk:chrome-driver

# 운영체제에 맞는 특정 버전 ChromeDriver 설치 예: 86 버전
php artisan dusk:chrome-driver 86

# 모든 지원 운영체제에 버전 설치
php artisan dusk:chrome-driver --all

# 운영체제에서 감지된 Chrome/Chromium 버전에 맞는 ChromeDriver 자동 설치
php artisan dusk:chrome-driver --detect
```

> [!WARNING]  
> Dusk는 `chromedriver` 바이너리가 실행 권한을 가져야 합니다. Dusk 실행 문제가 발생한다면 다음 명령어로 실행 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용해 브라우저 테스트를 실행합니다. 하지만 원한다면 직접 Selenium 서버를 띄워서 원하는 브라우저에서 테스트를 실행할 수도 있습니다.

시작하려면 `tests/DuskTestCase.php` 파일을 열고 `startChromeDriver` 호출 부분을 주석 처리하면 됩니다. 이렇게 하면 Dusk가 자동으로 ChromeDriver를 시작하지 않습니다:

```php
/**
 * Dusk 테스트 실행 준비.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

그 다음, `driver` 메서드를 수정해 원하는 URL과 포트로 Selenium에 연결하도록 하세요. 또한 WebDriver에 전달할 "desired capabilities"를 변경할 수 있습니다:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * RemoteWebDriver 인스턴스 생성
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
### 테스트 생성하기 (Generating Tests)

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉토리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 조회하는 페이지와 상호작용합니다. 하지만 Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 활용하는데, 이는 HTTP 요청 간에 적합하지 않습니다. 대신 `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트 중 하나를 사용하세요.

<a name="reset-migrations"></a>
#### 마이그레이션 사용하기 (Using Database Migrations)

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 매번 데이터베이스 테이블을 삭제하고 새로 만드는 것은 테이블을 잘라내는 것보다 느립니다:

```php
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;
}
```

> [!WARNING]  
> SQLite 인메모리 데이터베이스는 Dusk 테스트 실행 중에 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되므로 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 테이블 자르기 사용하기 (Using Database Truncation)

`DatabaseTruncation` 트레이트를 사용하려면 먼저 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다:

```shell
composer require --dev doctrine/dbal
```

`DatabaseTruncation` 트레이트는 첫 테스트에서 데이터베이스 마이그레이션을 실행해 테이블이 제대로 생성됐는지 확인합니다. 이후 테스트부터는 데이터베이스 테이블을 자르기(truncate)만 해, 마이그레이션을 다시 수행하는 것보다 속도가 빠릅니다:

```php
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;
}
```

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 자릅니다. 자를 테이블을 직접 지정하고 싶다면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

```php
/**
 * 자를 테이블 목록
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

반대로 자르지 않을 테이블을 지정하려면 `$exceptTables` 속성을 정의할 수 있습니다:

```php
/**
 * 자르기 제외할 테이블 목록
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

자르기 대상 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 사용하세요:

```php
/**
 * 자르기 대상 데이터베이스 연결 이름 목록
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 자르기 전후에 실행할 코드를 추가하고 싶다면 테스트 클래스에 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의하세요:

```php
/**
 * 데이터베이스 자르기 전에 실행되는 작업
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * 데이터베이스 자르기 후에 실행되는 작업
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행하기 (Running Tests)

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 실행하세요:

```shell
php artisan dusk
```

이전에 테스트가 실패했다면, 실패한 테스트만 먼저 실행해 시간을 아낄 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 PHPUnit 테스트 러너가 일반적으로 받는 모든 인수를 사용할 수 있습니다. 예를 들어 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)의 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]  
> 로컬 개발 환경을 [Laravel Sail](/docs/10.x/sail)로 관리하는 경우, Sail 문서 내 [Dusk 테스트 설정 및 실행](/docs/10.x/sail#laravel-dusk) 부분을 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작하기 (Manually Starting ChromeDriver)

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려고 시도합니다. 시스템 환경에 따라 자동 시작이 안 될 경우, 수동으로 ChromeDriver를 실행 후 `dusk` 명령을 사용하세요. 이때 `tests/DuskTestCase.php` 파일 내 `startChromeDriver` 호출 부분을 주석 처리해야 합니다:

```php
/**
 * Dusk 테스트 실행 준비.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

또한, ChromeDriver를 기본 9515 포트가 아닌 다른 포트에서 실행한다면, 같은 클래스의 `driver` 메서드에도 포트 번호를 반영해야 합니다:

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * RemoteWebDriver 인스턴스 생성
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### 환경 설정 처리하기 (Environment Handling)

Dusk 테스트 실행 시 별도의 환경 파일을 사용하고 싶다면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어 `local` 환경에서 실행한다면 `.env.dusk.local` 파일을 생성합니다.

테스트 실행 시 Dusk는 원본 `.env` 파일을 백업한 후 `.env.dusk.*` 파일을 `.env`로 복사하여 사용합니다. 테스트가 완료되면 기존 `.env`를 복원합니다.

<a name="browser-basics"></a>
## 브라우저 기초 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성하기 (Creating Browsers)

로그인 기능을 확인하는 기본 테스트를 작성해 봅시다. 테스트를 생성한 후, 로그인 페이지 이동, 로그인 정보 입력, "Login" 버튼 클릭 동작을 추가합니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 호출해 생성할 수 있습니다:

```php
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * 기본 브라우저 테스트 예제
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

위 예제에서 보듯 `browse` 메서드는 클로저를 인자로 받으며, Dusk가 자동으로 브라우저 인스턴스를 클로저에 전달합니다. 이 인스턴스를 통해 애플리케이션과 상호작용하고 검증을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성하기 (Creating Multiple Browsers)

때로는 복수 브라우저 인스턴스가 필요할 수 있습니다. 예를 들어, 웹소켓으로 연동되는 채팅 화면 테스트 구현 시 여러 브라우저를 사용해야 합니다. `browse` 메서드 클로저의 매개변수를 여러 개 추가하면 됩니다:

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

이름이 지정된 [라우트](/docs/10.x/routing#named-routes)로 이동할 때는 `visitRoute` 메서드를 사용하세요:

```php
$browser->visitRoute('login');
```

브라우저에서 "뒤로 가기"와 "앞으로 가기"는 각각 `back`과 `forward` 메서드를 사용합니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드로 현재 페이지를 새로고침할 수 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

브라우저 창 크기는 `resize` 메서드로 조절 가능합니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 콘텐츠 크기에 맞게 창 크기를 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 스크린샷 촬영 전에 자동으로 창 크기를 조절합니다. 이 동작을 비활성화하려면 테스트 내에서 `disableFitOnFailure`를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드는 브라우저 창 위치를 조절합니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

테스트 여러 곳에서 재사용할 수 있는 맞춤 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 사용하세요. 보통 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드에서 정의합니다:

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

`macro` 함수는 첫번째 인자로 매크로 이름을, 두번째 인자로 실행할 클로저를 받습니다. 이렇게 정의된 매크로는 `Browser` 인스턴스에서 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
            ->scrollToElement('#credit-card-details')
            ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

로그인 페이지를 매번 거치지 않고 인증된 상태로 테스트하려면 `loginAs` 메서드를 사용하세요. 이 메서드는 인증 가능한 모델의 기본 키 또는 모델 인스턴스를 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
          ->visit('/home');
});
```

> [!WARNING]  
> `loginAs` 메서드 사용 후에는 파일 내 모든 테스트에 걸쳐 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

암호화된 쿠키 값을 가져오거나 설정하려면 `cookie` 메서드를 사용하세요:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키는 `plainCookie` 메서드로 다룹니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키 삭제는 `deleteCookie` 메서드를 사용합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행 (Executing JavaScript)

브라우저 내에서 임의의 자바스크립트 코드를 실행하려면 `script` 메서드를 사용하세요:

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

`위치`와 이름으로 스크린샷을 찍고 저장하려면 `screenshot` 메서드를 호출하세요. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드를 사용하면 여러 반응형 크기에서 스크린샷을 한 번에 촬영할 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장하기 (Storing Console Output to Disk)

현재 브라우저의 콘솔 출력을 파일로 저장하려면 `storeConsoleLog` 메서드를 사용하세요. 콘솔 로그는 `tests/Browser/console` 디렉토리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장하기 (Storing Page Source to Disk)

현재 페이지의 HTML 소스 코드를 저장하려면 `storeSource` 메서드를 사용하세요. 소스는 `tests/Browser/source` 디렉토리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

효과적인 CSS 셀렉터를 고르는 일은 Dusk 테스트 작성에서 가장 어려운 부분 중 하나입니다. 프론트엔드가 변경되면 다음 같은 셀렉터가 쉽게 깨질 수 있습니다:

```html
<!-- HTML... -->

<button>Login</button>
```

```php
// 테스트...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터는 CSS 셀렉터 대신 HTML 요소에 `dusk` 속성을 추가하고, 테스트 내에서 `@` 접두사를 붙여 사용합니다:

```html
<!-- HTML... -->

<button dusk="login-button">Login</button>
```

```php
// 테스트...

$browser->click('@login-button');
```

원한다면 `selectorHtmlAttribute` 메서드를 사용해 Dusk 셀렉터가 참조하는 HTML 속성을 변경할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기

Dusk는 페이지 요소의 현재 값, 표시 텍스트, 속성을 조작할 수 있는 여러 메서드를 제공합니다. 예를 들어 특정 CSS 또는 Dusk 셀렉터에 해당하는 요소 값을 가져오려면 `value` 메서드를 사용합니다:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 이름으로 입력 필드의 값을 얻습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드는 특정 셀렉터에 매칭되는 요소의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

`attribute` 메서드는 요소의 특정 속성 값을 가져옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기 (Interacting With Forms)

<a name="typing-values"></a>
#### 텍스트 입력하기

Dusk는 폼 입력 요소와 상호작용할 다양한 메서드를 제공합니다. 예를 들면, 다음은 입력 필드에 텍스트를 입력하는 예제입니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

이때 필요한 경우 CSS 셀렉터를 넣을 수 있으나, 보통은 입력 필드의 `name` 속성으로 자동 검색하여 입력합니다.

기존 텍스트를 지우지 않고 덧붙이려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
        ->append('tags', ', bar, baz');
```

입력 필드 값을 지우려면 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드는 글자 입력 속도를 느리게 할 수 있는데, 기본 100밀리초 간격으로 타이핑합니다. 세 번째 인자로 밀리초 단위 속도를 조절할 수 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

덧붙임 텍스트도 느리게 입력하려면 `appendSlowly` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
        ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운 선택

`select` 메서드로 `select` 요소에서 값을 선택할 수 있습니다. `select` 메서드는 전체 CSS 셀렉터를 요구하지 않고, 값으로는 옵션의 실제 값(value)을 전달해야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤 옵션을 선택합니다:

```php
$browser->select('size');
```

두 번째 인자로 배열을 제공하면 여러 옵션을 선택할 수도 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스를 선택하려면 `check` 메서드를 사용하세요. CSS 셀렉터를 꼭 지정하지 않아도 되고, `name` 속성과 일치하는 체크박스를 찾아 체크합니다:

```php
$browser->check('terms');
```

체크 상태를 해제하려면 `uncheck` 메서드를 사용합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼 선택 시 `radio` 메서드를 사용하세요. CSS 셀렉터가 없으면 `name`과 `value` 속성으로 일치하는 라디오 입력을 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기 (Attaching Files)

`attach` 메서드는 파일 입력 필드에 파일을 첨부할 때 씁니다. CSS 셀렉터 없이 `name` 속성으로도 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]  
> `attach` 기능을 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치되어 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

페이지 내 버튼을 누르려면 `press` 메서드를 사용하세요. 인자는 버튼 표시 텍스트나 CSS/Dusk 셀렉터를 넘길 수 있습니다:

```php
$browser->press('Login');
```

여러 애플리케이션은 폼 제출 버튼을 누른 직후 비활성화 시키고, 제출이 완료되면 다시 활성화합니다. 버튼을 누르고 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 쓰는데, 두 번째 인수로 최대 대기 시간을 초 단위로 지정할 수 있습니다:

```php
// 최대 5초 대기
$browser->pressAndWaitFor('Save');

// 최대 1초 대기
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 이용하세요. 인자로 링크 텍스트를 받습니다:

```php
$browser->clickLink($linkText);
```

링크가 보이는지 확인하려면 `seeLink`를 사용하세요:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]  
> 이 메서드들은 jQuery와 상호작용합니다. 만약 페이지에 jQuery가 없으면 Dusk가 테스트 실행 기간 동안 자동으로 jQuery를 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기 (Using the Keyboard)

`keys` 메서드를 사용하면 일반 타이핑 외에도 조합키 입력이 가능합니다. 예를 들어, `shift` 키를 누른 상태로 `taylor` 입력 후 `swift`를 입력하는 예:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또한, 앱 내 기본 CSS 셀렉터에 "키보드 단축키"를 전송할 때 유용합니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]  
> `{command}` 등 조합키는 중괄호 `{}`로 감싸며, `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수와 일치합니다. [GitHub 링크](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php) 참고.

<a name="fluent-keyboard-interactions"></a>
#### 유연한 키보드 조작 (Fluent Keyboard Interactions)

`withKeyboard` 메서드를 이용해 `Laravel\Dusk\Keyboard` 클래스를 사용, 더 복잡한 키 입력을 유창하게 수행할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다:

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

테스트 전체에서 재사용 가능한 키보드 동작을 만들려면 `Keyboard` 클래스의 `macro` 메서드를 사용합니다. 보통 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드에서 정의합니다:

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

`macro` 함수는 첫 번째 인자로 매크로 이름을, 두 번째 인자로 클로저를 받습니다. 클로저는 해당 매크로가 `Keyboard` 인스턴스 메서드로 호출될 때 실행됩니다:

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

주어진 CSS나 Dusk 셀렉터에 매칭되는 요소를 클릭하려면 `click` 메서드를 사용하세요:

```php
$browser->click('.selector');
```

XPath 표현식으로 요소를 클릭하려면 `clickAtXPath`를 사용합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

브라우저 화면 내 특정 좌표에서 클릭하려면 `clickAtPoint`를 이용합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

더블 클릭과 우클릭 시뮬레이션은 각각 `doubleClick`, `rightClick` 메서드를 사용합니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');

$browser->rightClick();

$browser->rightClick('.selector');
```

버튼 클릭 후 누르고 있기 시뮬레이션은 `clickAndHold`를, 클릭 해제는 `releaseMouse`를 사용합니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
        ->pause(1000)
        ->releaseMouse();
```

`ctrl+클릭` 이벤트는 `controlClick` 메서드를 씁니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

특정 요소 위로 마우스를 이동하려면 `mouseover` 메서드를 사용하세요:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

요소를 다른 요소로 드래그할 때는 `drag` 메서드를 씁니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

한 방향으로 드래그를 하려면 다음 메서드를 사용하세요:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋으로 드래그하려면 `dragOffset`을 이용합니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 대화상자 (JavaScript Dialogs)

Dusk는 자바스크립트 대화상자와 상호작용할 수 있는 다양한 메서드를 제공합니다.

예를 들어 대화상자가 나타날 때까지 기다리려면 `waitForDialog`를 사용합니다. 인수로 최대 대기 시간을 초 단위로 줄 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

대화상자가 열려 있고 특정 메시지를 포함하는지 검증하려면 `assertDialogOpened`를 사용하세요:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 포함된 대화상자에 입력하려면 `typeInDialog`를 씁니다:

```php
$browser->typeInDialog('Hello World');
```

대화상자 "확인" 클릭은 `acceptDialog`로 실행합니다:

```php
$browser->acceptDialog();
```

"취소" 클릭은 `dismissDialog`로 합니다:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용하기 (Interacting With Inline Frames)

iframe 내 요소와 상호작용하려면 `withinFrame` 메서드를 사용하세요. 이 메서드는 클로저 내의 모든 상호작용을 지정한 iframe 범위로 한정합니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '12/24')
        ->type('input[name="cvc"]', '123');
    })->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정하기 (Scoping Selectors)

특정 셀렉터 아래에서 여러 작업을 실행할 때는 `with` 메서드를 사용하세요. 클로저 내 모든 조작과 검증이 지정된 셀렉터로 한정됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
          ->clickLink('Delete');
});
```

범위 밖에서 검증해야 할 경우 `elsewhere` 또는 `elsewhereWhenAvailable` 메서드를 사용할 수 있습니다:

```php
 $browser->with('.table', function (Browser $table) {
    // 현재 범위는 `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 범위는 `body .page-title`
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 범위는 `body .page-title`
        $title->assertSee('Hello World');
    });
 });
```

<a name="waiting-for-elements"></a>
### 요소 대기하기 (Waiting for Elements)

자바스크립트를 많이 사용하는 애플리케이션 테스트 시 특정 요소나 데이터가 나타날 때까지 기다리는 경우가 많습니다. Dusk는 이를 쉽게 도와줍니다.

<a name="waiting"></a>
#### 대기하기 (Waiting)

단순히 일정 시간 밀리초 단위로 대기하려면 `pause` 메서드를 사용하세요:

```php
$browser->pause(1000);
```

조건이 참일 경우에만 대기하려면 `pauseIf`, 거짓일 경우에만 대기하려면 `pauseUnless`를 씁니다:

```php
$browser->pauseIf(App::environment('production'), 1000);

$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기하기 (Waiting for Selectors)

`waitFor` 메서드는 페이지에 주어진 CSS 또는 Dusk 셀렉터가 표시될 때까지 최대 5초(기본) 동안 테스트 실행을 멈춥니다. 타임아웃 조정도 가능합니다:

```php
// 최대 5초 대기
$browser->waitFor('.selector');

// 최대 1초 대기
$browser->waitFor('.selector', 1);
```

특정 요소가 텍스트를 포함할 때까지 기다리려면 `waitForTextIn`을 사용하세요:

```php
// 최대 5초 대기
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

요소가 사라질 때까지 기다리려면 `waitUntilMissing`을 이용합니다:

```php
// 최대 5초 대기
$browser->waitUntilMissing('.selector');

// 최대 1초 대기
$browser->waitUntilMissing('.selector', 1);
```

요소가 활성화 또는 비활성화 될 때까지 기다릴 수도 있습니다:

```php
// 최대 5초 대기 (활성화)
$browser->waitUntilEnabled('.selector');

// 최대 1초 대기 (활성화)
$browser->waitUntilEnabled('.selector', 1);

// 최대 5초 대기 (비활성화)
$browser->waitUntilDisabled('.selector');

// 최대 1초 대기 (비활성화)
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 나타날 때 범위 지정 (Scoping Selectors When Available)

예를 들어, 모달 창이 나타날 때까지 기다렸다가 모달 내 "OK" 버튼을 누르려면 `whenAvailable` 메서드를 사용하세요. 클로저 안의 동작은 지정한 셀렉터 범위 내에서 실행됩니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
          ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기하기 (Waiting for Text)

특정 텍스트가 페이지에 나타날 때까지 기다리려면 `waitForText`를 사용하세요:

```php
// 최대 5초 대기
$browser->waitForText('Hello World');

// 최대 1초 대기
$browser->waitForText('Hello World', 1);
```

반대로 텍스트가 사라질 때까지 기다리려면 `waitUntilMissingText`를 사용합니다:

```php
// 최대 5초 대기
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기하기 (Waiting for Links)

특정 링크 텍스트가 나타날 때까지 기다리려면 `waitForLink`를 사용하세요:

```php
// 최대 5초 대기
$browser->waitForLink('Create');

// 최대 1초 대기
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기하기 (Waiting for Inputs)

특정 입력 필드가 나타날 때까지 기다릴 경우 `waitForInput`을 사용하세요:

```php
// 최대 5초 대기
$browser->waitForInput($field);

// 최대 1초 대기
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기하기 (Waiting on the Page Location)

`$browser->assertPathIs('/home')` 같은 경로 검증은 `window.location.pathname`이 비동기 업데이트 되는 경우 실패할 수 있습니다. 이때는 `waitForLocation`으로 특정 위치가 될 때까지 기다리세요:

```php
$browser->waitForLocation('/secret');
```

전체 URL 대기도 가능합니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[이름 있는 라우트](/docs/10.x/routing#named-routes) 대기도 지원합니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기하기 (Waiting for Page Reloads)

페이지 리로드가 필요한 경우 `waitForReload` 메서드를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 리로드 대기를 할 때는 좀 더 편리하게 `clickAndWaitForReload` 메서드를 사용할 수 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
        ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기하기 (Waiting on JavaScript Expressions)

테스트 실행을 자바스크립트 표현식이 `true`가 될 때까지 기다리려면 `waitUntil`을 사용합니다. `return`이나 세미콜론은 생략해도 됩니다:

```php
// 최대 5초 대기
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초 대기
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기하기 (Waiting on Vue Expressions)

Vue 컴포넌트의 데이터가 특정 값이 될 때까지 기다리려면 `waitUntilVue`와 `waitUntilVueIsNot` 메서드를 사용하세요:

```php
// 특정 컴포넌트 속성이 값과 일치할 때까지 대기
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 특정 컴포넌트 속성이 값과 일치하지 않을 때까지 대기
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기하기 (Waiting for JavaScript Events)

특정 자바스크립트 이벤트가 발생할 때까지 기다리려면 `waitForEvent`를 사용하세요:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 현재 범위(`body` 엘리먼트)에 붙습니다. 셀렉터 범위 안에서 대기할 수도 있습니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe 내 load 이벤트 대기
    $iframe->waitForEvent('load');
});
```

특정 요소에 이벤트 리스너를 붙이려면 두 번째 인자에 셀렉터를 지정하세요:

```php
$browser->waitForEvent('load', '.selector');
```

`document`나 `window` 객체에 이벤트를 붙일 수도 있습니다:

```php
// 문서 스크롤 이벤트 대기
$browser->waitForEvent('scroll', 'document');

// 최대 5초 대기, 윈도우 리사이즈 이벤트 대기
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백과 함께 대기하기 (Waiting With a Callback)

많은 "대기" 메서드들은 기본적으로 `waitUsing` 메서드를 호출합니다. 직접 사용해 보려면, 최대 대기 시간, 반복 간격, 클로저, 실패 메시지를 지정할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 뷰로 스크롤하기 (Scrolling an Element Into View)

뷰에서 벗어난 요소 때문에 클릭이 안 될 때는 `scrollIntoView`로 해당 요소가 화면에 보이도록 스크롤하세요:

```php
$browser->scrollIntoView('.selector')
        ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션(검증) (Available Assertions)

Dusk는 애플리케이션 상태에 대해 다양한 어설션을 지원합니다. 주요 어설션 목록은 아래와 같습니다:

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

현재 URL(쿼리 스트링 제외)이 주어진 문자열과 일치하는지 검증합니다:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴(프로토콜)이 주어진 값과 일치하는지 검증합니다:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 주어진 값과 일치하지 않는지 검증합니다:

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

현재 URL 호스트가 주어진 값과 일치하지 않는지 검증합니다:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 주어진 값과 일치하는지 검증합니다:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 주어진 값과 일치하지 않는지 검증합니다:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로가 주어진 경로로 시작하는지 검증합니다:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 URL 경로가 주어진 경로와 정확히 일치하는지 검증합니다:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 URL 경로가 주어진 경로와 일치하지 않는지 검증합니다:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 주어진 [이름 있는 라우트](/docs/10.x/routing#named-routes)와 매칭되는지 검증합니다:

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

주어진 쿼리 스트링 파라미터가 존재하는지 검증합니다:

```php
$browser->assertQueryStringHas($name);
```

값 일치 여부도 검증할 수 있습니다:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

주어진 쿼리 스트링 파라미터가 존재하지 않는지 검증합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

현재 URL의 해시 프래그먼트가 주어진 값과 일치하는지 검증합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

현재 URL 해시 프래그먼트가 주어진 값으로 시작하는지 검증합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

현재 URL 해시 프래그먼트가 주어진 값과 일치하지 않는지 검증합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

주어진 암호화된 쿠키가 있는지 검증합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

주어진 비암호화 쿠키가 있는지 검증합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

주어진 암호화 쿠키가 없는지 검증합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

주어진 비암호화 쿠키가 없는지 검증합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키가 특정 값을 갖는지 검증합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

비암호화된 쿠키가 특정 값을 갖는지 검증합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

페이지에 특정 텍스트가 존재하는지 검증합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

페이지에 특정 텍스트가 존재하지 않는지 검증합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

특정 셀렉터 영역에 특정 텍스트가 있는지 검증합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

특정 셀렉터 영역에 특정 텍스트가 없는지 검증합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

특정 셀렉터 영역에 아무 텍스트라도 있는지 검증합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

특정 셀렉터 영역에 텍스트가 없는지 검증합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
#### assertScript

자바스크립트 표현식이 특정 값과 일치하는지 검증합니다:

```php
$browser->assertScript('window.isLoaded')
        ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지 소스에 특정 코드가 포함되어 있는지 검증합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지 소스에 특정 코드가 포함되어 있지 않은지 검증합니다:

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

페이지에 특정 링크가 존재하지 않는지 검증합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

입력 필드가 특정 값을 가지고 있는지 검증합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

입력 필드가 특정 값이 아닌지 검증합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

체크박스가 선택되어 있는지 검증합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

체크박스가 선택되어 있지 않은지 검증합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

체크박스가 불확정 상태인지 검증합니다:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

라디오 버튼이 선택되어 있는지 검증합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

라디오 버튼이 선택되어 있지 않은지 검증합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

드롭다운이 특정 값을 선택하고 있는지 검증합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

드롭다운이 특정 값을 선택하고 있지 않은지 검증합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

드롭다운에 특정 옵션 배열이 있는지 검증합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

드롭다운에 특정 옵션 배열이 없는지 검증합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

드롭다운에 특정 옵션이 있는지 검증합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

드롭다운에 특정 옵션이 없는지 검증합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

특정 셀렉터 요소가 특정 값을 가지고 있는지 검증합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

특정 셀렉터 요소가 특정 값을 가지고 있지 않은지 검증합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

특정 셀렉터 요소의 지정한 속성이 특정 값을 가지고 있는지 검증합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

특정 셀렉터 요소의 지정한 속성이 특정 값을 포함하는지 검증합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

특정 셀렉터 요소의 지정한 속성이 특정 값을 포함하지 않는지 검증합니다:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

특정 셀렉터 요소의 ARIA 속성이 특정 값을 가지고 있는지 검증합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>`라면 다음과 같이 검증할 수 있습니다:

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

특정 셀렉터 요소의 데이터 속성이 특정 값을 가지고 있는지 검증합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들면 `<tr id="row-1" data-content="attendees"></tr>`의 경우:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

특정 셀렉터 요소가 화면에 보여지는지 검증합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

특정 셀렉터 요소가 HTML 소스에 존재하는지 검증합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

특정 셀렉터 요소가 소스에 존재하지 않는지 검증합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

특정 셀렉터 요소가 화면에 표시되지 않는지 검증합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

입력 이름이 주어진 필드가 존재하는지 검증합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

주어진 이름의 입력 필드가 소스에 없는지 검증합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

특정 메시지를 가진 자바스크립트 대화상자가 열렸는지 검증합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

지정된 필드가 활성 상태인지 검증합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

지정된 필드가 비활성 상태인지 검증합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

지정한 버튼이 활성 상태인지 검증합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

지정한 버튼이 비활성 상태인지 검증합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

지정한 필드에 포커스가 있는지 검증합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

지정한 필드에 포커스가 없는지 검증합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태인지 검증합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태인지 검증합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

사용자가 특정 사용자로 인증되어 있는지 검증합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 Vue 컴포넌트 데이터 상태에 대한 어설션도 지원합니다. 예를 들어 애플리케이션에 다음 Vue 컴포넌트가 있다고 가정합니다:

```html
<!-- HTML -->

<profile dusk="profile-component"></profile>
```

```js
// 컴포넌트 정의

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

다음과 같이 Vue 데이터 상태를 검증할 수 있습니다:

```php
/**
 * 기본 Vue 테스트 예제
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

특정 Vue 컴포넌트 데이터 속성이 주어진 값이 아닌지 검증합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트 데이터가 배열이며 특정 값을 포함하는지 검증합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

Vue 컴포넌트 데이터가 배열이며 특정 값을 포함하지 않는지 검증합니다:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

복잡한 테스트에서 여러 동작을 연속 수행해야 하면 테스트가 복잡해지고 가독성이 떨어지기 쉽습니다. Dusk 페이지는 특정 페이지에 대한 동작과 자주 쓰는 셀렉터 단축키를 정의해 테스트를 더 쉽게 만들 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 사용하세요. 페이지 클래스는 `tests/Browser/Pages` 디렉토리에 생성됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성하기 (Configuring Pages)

기본적으로 페이지에는 `url`, `assert`, `elements` 세 메서드가 있습니다. 여기서는 `url`과 `assert`를 설명합니다. `elements`는 [단축 셀렉터](#shorthand-selectors) 부분에서 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지의 URL 경로를 반환해야 합니다. Dusk가 이 URL로 페이지 이동 시 사용합니다:

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

`assert` 메서드는 현재 브라우저가 페이지에 도달했는지 검증합니다. 내용은 필수는 아니지만, 원하는 검증을 작성할 수 있습니다. 페이지 방문 시 자동 실행됩니다:

```php
/**
 * 브라우저가 페이지에 있는지 검증
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동하기 (Navigating to Pages)

페이지 클래스가 정의되면, `visit` 메서드로 해당 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 있고 페이지 셀렉터와 메서드만 불러오려면 `on` 메서드를 사용하세요. 예를 들어 버튼 클릭 후 리다이렉트가 발생했을 때 사용할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
        ->clickLink('Create Playlist')
        ->on(new CreatePlaylist)
        ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드에서 페이지 내 셀렉터에 대한 짧은 이름 별칭을 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드 별칭을 등록합니다:

```php
/**
 * 페이지 내 단축 셀렉터 배열 반환
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

한번 등록된 단축 셀렉터는 일반 CSS 셀렉터 대신 어디서든 쓸 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 셀렉터 (Global Shorthand Selectors)

Dusk 설치 시 `tests/Browser/Pages` 내 베이스 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에서 전체 애플리케이션에 공통으로 적용할 글로벌 단축 셀렉터를 정의할 수 있습니다:

```php
/**
 * 애플리케이션 전체에서 공통으로 쓸 단축 셀렉터 반환
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

페이지 내 기본 메서드 외에 테스트에서 공통으로 쓸 추가 메서드를 정의할 수 있습니다. 예를 들어 음악 관리 애플리케이션에서 재생목록 생성 동작을 페이지 메서드에 작성할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;

class Dashboard extends Page
{
    // 다른 페이지 메서드...

    /**
     * 새 재생목록 생성
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
                ->check('share')
                ->press('Create Playlist');
    }
}
```

이후 테스트 코드에서는 페이지 메서드를 직접 호출해 로직 재사용이 가능합니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
        ->createPlaylist('My Playlist')
        ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 페이지 객체와 비슷하지만, 내비게이션 바나 알림창처럼 여러 페이지에서 공통으로 반복 사용하는 UI/기능을 위한 추상화입니다. 따라서 URL에 묶이지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기 (Generating Components)

컴포넌트를 생성하려면 `dusk:component` Artisan 명령어를 실행하세요. 생성된 컴포넌트는 `tests/Browser/Components` 디렉토리에 위치합니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어, 여러 테스트에서 날짜 선택 동작을 직접 작성하기 번거로우면, 날짜 선택기를 컴포넌트로 만들고 해당 로직을 캡슐화할 수 있습니다:

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
     * 컴포넌트가 페이지 내에 존재하는지 검증
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 내 단축 셀렉터 배열 반환
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
     * 특정 날짜 선택
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
### 컴포넌트 사용하기 (Using Components)

작성한 컴포넌트를 이용해 테스트에서 쉽게 날짜를 선택할 수 있고, 날짜 선택 로직이 바뀌면 컴포넌트만 수정하면 됩니다:

```php
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    /**
     * 기본 컴포넌트 테스트 예제
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
> 대부분의 Dusk CI 환경은 Laravel 애플리케이션이 내장 PHP 개발 서버로 포트 8000에서 구동된다고 가정합니다. 따라서 CI 환경에 `APP_URL` 환경 변수를 `http://127.0.0.1:8000`로 설정해야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행하기 (Heroku CI)

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, `app.json` 파일에 아래 Google Chrome 빌드팩과 스크립트를 추가하세요:

```json
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-google-chrome" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
### Travis CI에서 테스트 실행하기 (Travis CI)

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면, 그래픽 인터페이스가 없기 때문에 Chrome 브라우저 실행을 위한 여러 설정을 해야 합니다. 또한 `php artisan serve`로 웹서버를 띄웁니다:

```yaml
language: php

php:
  - 7.3

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
### GitHub Actions에서 테스트 실행하기 (GitHub Actions)

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행할 때 사용할 수 있는 예시 구성 파일입니다. Travis CI와 유사하게 `php artisan serve`를 통해 PHP 내장 서버를 띄웁니다:

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
        run: ./vendor/laravel/dusk/bin/chromedriver-linux &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: console
          path: tests/Browser/console
```

<a name="running-tests-on-chipper-ci"></a>
### Chipper CI에서 테스트 실행하기 (Chipper CI)

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행할 때 참고할 수 있는 설정입니다. Laravel은 PHP 내장 서버로 띄우고, 빌드 환경에 Chrome을 포함합니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Chrome 포함 서비스
services:
  - dusk

# 모든 커밋에서 빌드 실행
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate
      
      # dusk 환경 파일 복사 및 BUILD_HOST 기반 APP_URL 설정
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

Chipper CI에서 Dusk 테스트와 데이터베이스 사용법 등 자세한 내용은 [공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.