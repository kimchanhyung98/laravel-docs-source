# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기초](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 파일 저장](#storing-console-output-to-disk)
    - [페이지 소스 파일 저장](#storing-page-source-to-disk)
- [엘리먼트와 상호작용하기](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기](#waiting-for-elements)
    - [엘리먼트 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어서션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [단축 셀렉터](#shorthand-selectors)
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
## 소개

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK 또는 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치본을 사용합니다. 하지만 원하는 경우 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가해야 합니다:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]  
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, 절대 프로덕션 환경에서 등록해서는 안 됩니다. 그렇게 할 경우 임의의 사용자가 애플리케이션에 인증할 수 있기 때문입니다.

Dusk 패키지를 설치한 후, `dusk:install` Artisan 명령을 실행하세요. 이 명령은 `tests/Browser` 디렉터리와 예제 Dusk 테스트를 생성하고, OS에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접속할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]  
> [Laravel Sail](/docs/{{version}}/sail)를 이용해 로컬 개발 환경을 관리한다면, [Dusk 테스트 설정 및 실행](/docs/{{version}}/sail#laravel-dusk)에 관한 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령이 설치하는 ChromeDriver와 다른 버전을 사용하고 싶다면, `dusk:chrome-driver` 명령을 사용할 수 있습니다:

```shell
# OS용 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원하는 모든 OS용 특정 버전 설치...
php artisan dusk:chrome-driver --all

# 감지된 Chrome / Chromium 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]  
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행에 문제가 있다면 다음 명령어로 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치본으로 브라우저 테스트를 실행합니다. 하지만 직접 Selenium 서버를 시작하고, 원하는 브라우저로 테스트를 실행할 수도 있습니다.

시작하려면, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서는 `startChromeDriver` 메서드 호출을 제거할 수 있습니다. 이렇게 하면 Dusk가 ChromeDriver를 자동으로 시작하지 않게 됩니다.

    /**
     * Dusk 테스트 실행 준비.
     *
     * @beforeClass
     */
    public static function prepare(): void
    {
        // static::startChromeDriver();
    }

그 다음, 원하는 URL과 포트로 연결하도록 `driver` 메서드를 수정할 수 있습니다. 또한 WebDriver에 전달할 "원하는 기능(Desired Capabilities)" 값도 변경할 수 있습니다:

    use Facebook\WebDriver\Remote\RemoteWebDriver;

    /**
     * RemoteWebDriver 인스턴스 생성.
     */
    protected function driver(): RemoteWebDriver
    {
        return RemoteWebDriver::create(
            'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
        );
    }

<a name="getting-started"></a>
## 시작하기

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 생성하려면, `dusk:make` Artisan 명령을 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 가져오는 페이지와 상호작용하게 됩니다. 그러나 Dusk 테스트에서는 `RefreshDatabase` 트레잇을 **사용하지 않아야 합니다**. 이는 데이터베이스 트랜잭션을 활용하는데, HTTP 요청마다 적용되지 않거나 지원되지 않습니다. 대신, `DatabaseMigrations` 트레잇과 `DatabaseTruncation` 트레잇 중 하나를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레잇은 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 단, 각 테스트마다 테이블을 드롭하고 다시 생성하므로 속도가 느릴 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

uses(DatabaseMigrations::class);

// ...
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
> Dusk 테스트 실행 시 SQLite 인메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되므로, 다른 프로세스의 인메모리 데이터에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 잘라내기(Truncation) 사용

`DatabaseTruncation` 트레잇은 첫 번째 테스트에서 데이터를 마이그레이션하여 테이블이 제대로 생성되도록 보장합니다. 이후 테스트부터는 테이블을 단순히 잘라내기(Truncate)하여, 마이그레이션을 반복 실행하는 것보다 속도가 빠릅니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

uses(DatabaseTruncation::class);

// ...
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

기본적으로 이 트레잇은 `migrations` 테이블을 제외한 모든 테이블을 잘라냅니다. 잘라낼 테이블을 커스터마이즈하려면 테스트 클래스에서 `$tablesToTruncate` 속성을 지정할 수 있습니다:

> [!NOTE]  
> Pest를 사용하는 경우, 속성이나 메서드는 베이스 `DuskTestCase` 혹은 테스트 파일이 확장한 클래스에 정의하세요.

    /**
     * 잘라낼 테이블 지정.
     *
     * @var array
     */
    protected $tablesToTruncate = ['users'];

반대로 잘라내기에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 사용할 수 있습니다:

    /**
     * 잘라내기에서 제외할 테이블 지정.
     *
     * @var array
     */
    protected $exceptTables = ['users'];

잘라낼 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 사용할 수 있습니다:

    /**
     * 잘라낼 연결 지정.
     *
     * @var array
     */
    protected $connectionsToTruncate = ['mysql'];

잘라내기 전후에 코드를 실행하고 싶을 때는 `beforeTruncatingDatabase`, `afterTruncatingDatabase` 메서드를 구현하세요:

    /**
     * 잘라내기 전 실행할 작업.
     */
    protected function beforeTruncatingDatabase(): void
    {
        //
    }

    /**
     * 잘라내기 후 실행할 작업.
     */
    protected function afterTruncatingDatabase(): void
    {
        //
    }

<a name="running-tests"></a>
### 테스트 실행

브라우저 테스트를 실행하려면, `dusk` Artisan 명령을 실행하세요:

```shell
php artisan dusk
```

직전 테스트에서 실패한 테스트만 빠르게 다시 실행하고 싶다면 `dusk:fails` 명령을 사용하세요:

```shell
php artisan dusk:fails
```

`dusk` 명령은 Pest / PHPUnit 테스트 러너가 제공하는 모든 인자를 받아 테스트 그룹만 실행되는 등 다양한 옵션을 사용할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]  
> [Laravel Sail](/docs/{{version}}/sail)로 로컬 개발 환경을 관리 중이라면, Sail 문서의 [Dusk 테스트 설정 및 실행](/docs/{{version}}/sail#laravel-dusk) 부분도 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 시작합니다. 이 방법이 시스템과 맞지 않으면 테스트 실행 전에 직접 ChromeDriver를 실행할 수 있습니다. 이 경우 `tests/DuskTestCase.php`에서 ChromeDriver 자동 실행 부분을 주석 처리해야 합니다:

    /**
     * Dusk 테스트 실행 준비.
     *
     * @beforeClass
     */
    public static function prepare(): void
    {
        // static::startChromeDriver();
    }

또한, ChromeDriver를 9515번이 아닌 다른 포트에서 실행하는 경우 `driver` 메서드 내 포트 번호도 일치시켜야 합니다:

    use Facebook\WebDriver\Remote\RemoteWebDriver;

    /**
     * RemoteWebDriver 인스턴스 생성.
     */
    protected function driver(): RemoteWebDriver
    {
        return RemoteWebDriver::create(
            'http://localhost:9515', DesiredCapabilities::chrome()
        );
    }

<a name="environment-handling"></a>
### 환경 파일 처리

Dusk 테스트 실행 시 별도의 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{환경명}` 파일을 생성합니다. 예를 들어 `local` 환경에서 `dusk` 명령을 실행한다면, `.env.dusk.local` 파일을 만드세요.

테스트 실행 시, Dusk는 기존 `.env` 파일을 백업한 뒤 Dusk 환경 파일을 `.env`로 변경합니다. 테스트 종료 후 `.env` 파일이 복구됩니다.

<a name="browser-basics"></a>
## 브라우저 기초

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성

애플리케이션에 로그인할 수 있는지 확인하는 테스트 예제를 만들어봅시다. 테스트를 생성한 뒤, 로그인 페이지로 이동하여 인증 정보를 입력하고 "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내에서 `browse` 메서드를 호출합니다:

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

위 예제에서 보듯, `browse`에는 클로저가 전달되며, Dusk에서 자동으로 브라우저 인스턴스를 주입해줍니다. 이 인스턴스로 애플리케이션과 상호작용하거나 어서션을 진행할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 복수 브라우저 인스턴스 생성

때때로 테스트를 올바르게 수행하려면 복수 브라우저가 필요할 수 있습니다. 예를 들어, 웹소켓이 연동된 채팅화면 테스트 시 여러 브라우저가 유용합니다. 클로저의 인자에 브라우저를 더 추가하면 됩니다:

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

<a name="navigation"></a>
### 네비게이션

`visit` 메서드로 애플리케이션의 특정 URI로 이동할 수 있습니다:

    $browser->visit('/login');

[named route](/docs/{{version}}/routing#named-routes)로 이동하려면 `visitRoute`를 사용할 수 있습니다:

    $browser->visitRoute($routeName, $parameters);

뒤로가기와 앞으로가기는 각각 `back`, `forward` 메서드를 사용합니다:

    $browser->back();

    $browser->forward();

페이지 새로고침은 `refresh` 메서드로 할 수 있습니다:

    $browser->refresh();

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize`로 브라우저 창 크기를 조정할 수 있습니다:

    $browser->resize(1920, 1080);

창을 최대화하려면 `maximize`를 사용하세요:

    $browser->maximize();

`fitContent`는 창 크기를 내용에 맞게 자동 조정합니다:

    $browser->fitContent();

테스트 실패 시 Dusk는 스크린샷을 찍기 전에 자동으로 브라우저를 내용에 맞게 조정합니다. 이 기능을 끄려면 `disableFitOnFailure`를 호출하세요:

    $browser->disableFitOnFailure();

`move`로 브라우저 위치를 옮길 수도 있습니다:

    $browser->move($x = 100, $y = 100);

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 반복해서 사용할 사용자 정의 브라우저 메서드를 만들고 싶다면, `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 주로 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록합니다:

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

이렇게 등록한 매크로는 브라우저 인스턴스에서 메서드처럼 사용할 수 있습니다:

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/pay')
            ->scrollToElement('#credit-card-details')
            ->assertSee('Enter Credit Card Details');
    });

<a name="authentication"></a>
### 인증

인증이 필요한 페이지를 자주 테스트할 때마다 로그인 화면을 거치지 않으려면 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델의 기본키나 인스턴스를 받습니다:

    use App\Models\User;
    use Laravel\Dusk\Browser;

    $this->browse(function (Browser $browser) {
        $browser->loginAs(User::find(1))
            ->visit('/home');
    });

> [!WARNING]  
> `loginAs`를 사용하면 파일 내 모든 테스트에 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드로 암호화된 쿠키 값을 가져오거나 설정할 수 있습니다. Laravel이 생성하는 모든 쿠키는 기본적으로 암호화되어 있습니다:

    $browser->cookie('name');

    $browser->cookie('name', 'Taylor');

암호화되지 않은 쿠키 조작에는 `plainCookie`를 사용하세요:

    $browser->plainCookie('name');

    $browser->plainCookie('name', 'Taylor');

쿠키 삭제는 `deleteCookie`로 할 수 있습니다:

    $browser->deleteCookie('name');

<a name="executing-javascript"></a>
### JavaScript 실행

`script` 메서드로 브라우저 내 임의 JavaScript를 실행할 수 있습니다:

    $browser->script('document.documentElement.scrollTop = 0');

    $browser->script([
        'document.body.scrollTop = 0',
        'document.documentElement.scrollTop = 0',
    ]);

    $output = $browser->script('return window.location.pathname');

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 메서드로 스크린샷을 찍어 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots`에 저장됩니다:

    $browser->screenshot('filename');

`responsiveScreenshots`로 다양한 브레이크포인트에서 연속 스크린샷을 찍을 수 있습니다:

    $browser->responsiveScreenshots('filename');

`screenshotElement`는 페이지의 특정 엘리먼트만 스크린샷으로 찍을 때 사용합니다:

    $browser->screenshotElement('#selector', 'filename');

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 파일 저장

`storeConsoleLog`로 현재 브라우저의 콘솔 출력을 지정한 파일명으로 디스크에 저장할 수 있습니다. 출력물은 `tests/Browser/console`에 저장됩니다:

    $browser->storeConsoleLog('filename');

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 파일 저장

`storeSource`로 현재 페이지 소스를 파일로 저장할 수 있습니다. 소스는 `tests/Browser/source`에 저장됩니다:

    $browser->storeSource('filename');

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용하기

<a name="dusk-selectors"></a>
### Dusk 셀렉터

효과적인 Dusk 테스트를 위해서는 CSS 셀렉터를 잘 선택하는 것이 중요하지만, 프론트엔드가 바뀌면 아래와 같은 CSS 셀렉터가 쉽게 깨질 수 있습니다:

    // HTML...

    <button>Login</button>

    // 테스트...

    $browser->click('.login-page .container div > button');

Dusk 셀렉터는 CSS 셀렉터 대신 효율적으로 엘리먼트에 접근할 수 있도록 `dusk` 속성을 부여해줍니다. `@`로 프리픽스 하여 사용할 수 있습니다:

    // HTML...

    <button dusk="login-button">Login</button>

    // 테스트...

    $browser->click('@login-button');

필요하다면 Dusk 셀렉터가 사용하는 HTML 속성을 `selectorHtmlAttribute` 메서드로 변경할 수도 있습니다. 주로 `AppServiceProvider`의 `boot` 메서드에서 지정합니다:

    use Laravel\Dusk\Dusk;

    Dusk::selectorHtmlAttribute('data-dusk');

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기/설정

Dusk는 엘리먼트의 값, 화면 표시 텍스트, 속성에 상호작용할 수 있는 여러 메서드를 제공합니다. 값은 `value`로 얻거나 저장할 수 있습니다:

    // 값 가져오기...
    $value = $browser->value('selector');

    // 값 설정...
    $browser->value('selector', 'value');

`inputValue`로는 주어진 필드명을 가진 input 엘리먼트의 값을 가져옵니다:

    $value = $browser->inputValue('field');

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드로 특정 셀렉터의 화면 표시 텍스트를 가져올 수 있습니다:

    $text = $browser->text('selector');

<a name="retrieving-attributes"></a>
#### 속성 가져오기

`attribute` 메서드는 특정 셀렉터의 엘리먼트에서 속성 값을 가져옵니다:

    $attribute = $browser->attribute('selector', 'value');

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력

Dusk는 다양한 폼 및 input 요소를 위한 메서드를 제공합니다. 먼저 input 필드에 텍스트를 입력하는 예시입니다:

    $browser->type('email', 'taylor@laravel.com');

위 메서드는 CSS 셀렉터를 생략하면 name 속성으로 input이나 textarea를 자동 검색합니다.

내용을 지우지 않고 추가로 입력하려면 `append`를 사용하세요:

    $browser->type('tags', 'foo')
        ->append('tags', ', bar, baz');

input 내용을 클리어하려면 `clear`를 사용하세요:

    $browser->clear('email');

`typeSlowly`로 천천히 입력할 수 있습니다 (기본 100ms, ms 지정 인자도 제공):

    $browser->typeSlowly('mobile', '+1 (202) 555-5555');

    $browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);

`appendSlowly`로 천천히 이어 붙일 수도 있습니다:

    $browser->type('tags', 'foo')
        ->appendSlowly('tags', ', bar, baz');

<a name="dropdowns"></a>
#### 드롭다운

`select`로 select 엘리먼트의 값을 선택할 수 있습니다. 두 번째 인자로는 option의 텍스트가 아닌 value 값을 넘깁니다:

    $browser->select('size', 'Large');

두 번째 인자를 생략하면 랜덤 옵션을 선택합니다:

    $browser->select('size');

배열로 넘기면 멀티 옵션도 선택됩니다:

    $browser->select('categories', ['Art', 'Music']);

<a name="checkboxes"></a>
#### 체크박스

체크박스를 체크하려면 `check`를 사용하세요:

    $browser->check('terms');

체크 해제를 하려면 `uncheck`를 사용합니다:

    $browser->uncheck('terms');

<a name="radio-buttons"></a>
#### 라디오 버튼

`radio`로 라디오 타입의 값을 선택합니다. name, value 값을 인자로 줍니다:

    $browser->radio('size', 'large');

<a name="attaching-files"></a>
### 파일 첨부

`attach`로 파일 input 요소에 파일을 첨부할 수 있습니다. CSS 셀렉터 대신 name으로 탐색합니다:

    $browser->attach('photo', __DIR__.'/photos/mountains.png');

> [!WARNING]  
> 파일 첨부 기능을 사용하려면 PHP Zip 확장이 설치되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기

`press`로 버튼을 클릭할 수 있습니다. 인자로 버튼 display 텍스트나 CSS/Dusk 셀렉터를 사용할 수 있습니다:

    $browser->press('Login');

사용자 입력 중 버튼이 비활성/활성 상태로 전환되기를 기다려야 할 때 `pressAndWaitFor`를 사용하세요:

    // 5초 동안 대기
    $browser->pressAndWaitFor('Save');

    // 1초 동안 대기
    $browser->pressAndWaitFor('Save', 1);

<a name="clicking-links"></a>
### 링크 클릭

`clickLink`로 특정 텍스트를 가진 링크를 클릭할 수 있습니다:

    $browser->clickLink($linkText);

`seeLink`로 특정 텍스트를 가진 링크가 보이는지 확인할 수 있습니다:

    if ($browser->seeLink($linkText)) {
        // ...
    }

> [!WARNING]  
> 이 메서드들은 jQuery에 의존합니다. 해당 페이지에 jQuery가 없다면 Dusk가 자동으로 inject 해줍니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys`로 복잡한 입력 시퀀스를 사용할 수 있습니다. 예를 들어 modifier 키와 함께 입력하거나, 키보드 단축키를 시뮬레이션할 수 있습니다:

    $browser->keys('selector', ['{shift}', 'taylor'], 'swift');

    $browser->keys('.app', ['{command}', 'j']);

> [!NOTE]  
> `{command}` 등 modifier 키는 `{}`로 감싸며, 모두 [WebDriverKeys.php](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)에 정의되어 있습니다.

<a name="fluent-keyboard-interactions"></a>
#### 유연한 키보드 인터페이스

Dusk의 `withKeyboard`를 사용해 `Laravel\Dusk\Keyboard` 클래스를 통해 입력, 눌림, 릴리즈, 일시정지 등의 조합을 유연하게 할 수 있습니다:

    use Laravel\Dusk\Keyboard;

    $browser->withKeyboard(function (Keyboard $keyboard) {
        $keyboard->press('c')
            ->pause(1000)
            ->release('c')
            ->type(['c', 'e', 'o']);
    });

<a name="keyboard-macros"></a>
#### 키보드 매크로

키보드 상호작용도 매크로로 만들어 재사용할 수 있습니다. 역시 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot`에서 등록할 수 있습니다:

    <?php

    namespace App\Providers;

    use Facebook\WebDriver\WebDriverKeys;
    use Illuminate\Support\ServiceProvider;
    use Laravel\Dusk\Keyboard;
    use Laravel\Dusk\OperatingSystem;

    class DuskServiceProvider extends ServiceProvider
    {
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

매크로는 키보드 인스턴스에서 메서드처럼 사용할 수 있습니다:

    $browser->click('@textarea')
        ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
        ->click('@another-textarea')
        ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 클릭

`click`으로 셀렉터에 일치하는 엘리먼트를 클릭할 수 있습니다:

    $browser->click('.selector');

`clickAtXPath`로 XPath에 일치하는 엘리먼트를 클릭할 수 있습니다:

    $browser->clickAtXPath('//div[@class = "selector"]');

`clickAtPoint`로 좌표(x, y)에 가장 가까운 엘리먼트를 클릭합니다:

    $browser->clickAtPoint($x = 0, $y = 0);

`doubleClick`는 더블클릭 이벤트를 시뮬레이션합니다:

    $browser->doubleClick();

    $browser->doubleClick('.selector');

`rightClick`은 마우스 우클릭을 시뮬레이션합니다:

    $browser->rightClick();

    $browser->rightClick('.selector');

`clickAndHold`로 클릭 상태를 유지할 수 있고, `releaseMouse`로 해제합니다:

    $browser->clickAndHold('.selector');

    $browser->clickAndHold()
        ->pause(1000)
        ->releaseMouse();

`controlClick`은 ctrl+클릭 이벤트를 시뮬레이션합니다:

    $browser->controlClick();

    $browser->controlClick('.selector');

<a name="mouseover"></a>
#### 마우스오버

`mouseover` 메서드는 указ한 셀렉터에 마우스를 올려둡니다:

    $browser->mouseover('.selector');

<a name="drag-drop"></a>
#### 드래그&드롭

`drag`로 한 엘리먼트를 다른 엘리먼트로 드래그할 수 있습니다:

    $browser->drag('.from-selector', '.to-selector');

지정한 픽셀만큼 한 방향으로 드래그할 수도 있습니다:

    $browser->dragLeft('.selector', $pixels = 10);
    $browser->dragRight('.selector', $pixels = 10);
    $browser->dragUp('.selector', $pixels = 10);
    $browser->dragDown('.selector', $pixels = 10);

지정한 오프셋(x, y)만큼 드래그할 수도 있습니다:

    $browser->dragOffset('.selector', $x = 10, $y = 10);

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그

Dusk는 다양한 JavaScript 다이얼로그와 상호작용할 수 있는 메서드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그 표시를 대기할 수 있습니다:

    $browser->waitForDialog($seconds = null);

`assertDialogOpened`로 다이얼로그가 특정 메시지로 열린 것을 검증할 수 있습니다:

    $browser->assertDialogOpened('Dialog message');

프롬프트 입력이 필요한 경우 `typeInDialog`로 값 입력도 가능합니다:

    $browser->typeInDialog('Hello World');

"확인" 버튼 클릭으로 다이얼로그를 닫으려면 `acceptDialog`를 사용합니다:

    $browser->acceptDialog();

"취소" 버튼 클릭으로 닫으려면 `dismissDialog`를 사용합니다:

    $browser->dismissDialog();

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용

iframe 내부 엘리먼트와 상호작용할 때는 `withinFrame`을 사용합니다. 클로저 내부에서는 전달받은 $browser 객체의 범위가 해당 iframe으로 한정됩니다:

    $browser->withinFrame('#credit-card-details', function ($browser) {
        $browser->type('input[name="cardnumber"]', '4242424242424242')
            ->type('input[name="exp-date"]', '1224')
            ->type('input[name="cvc"]', '123')
            ->press('Pay');
    });

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정

특정 셀렉터 범위 내에서 여러 작업을 수행하고 싶을 때는 `with`를 사용합니다:

    $browser->with('.table', function (Browser $table) {
        $table->assertSee('Hello World')
            ->clickLink('Delete');
    });

범위를 일시적으로 벗어나서 어서션을 해야 할 때는 `elsewhere`, `elsewhereWhenAvailable`를 사용할 수 있습니다:

     $browser->with('.table', function (Browser $table) {
        // 현재 범위: `body .table` ...

        $browser->elsewhere('.page-title', function (Browser $title) {
            // 현재 범위: `body .page-title` ...
            $title->assertSee('Hello World');
        });

        $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
            // 현재 범위: `body .page-title` ...
            $title->assertSee('Hello World');
        });
     });

<a name="waiting-for-elements"></a>
### 엘리먼트 대기

JavaScript를 많이 사용하는 애플리케이션 테스트 시, 특정 엘리먼트나 데이터가 준비될 때까지 "대기"해야 할 필요가 많습니다. Dusk는 이런 상황을 다양한 메서드로 간단하게 처리할 수 있도록 도와줍니다.

<a name="waiting"></a>
#### 대기

단순히 일정 ms만 대기하려면 `pause`:

    $browser->pause(1000);

조건이 맞을 때만 대기하려면 `pauseIf`:

    $browser->pauseIf(App::environment('production'), 1000);

조건이 아닐 때만 대기하려면 `pauseUnless`:

    $browser->pauseUnless(App::environment('testing'), 1000);

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor`는 셀렉터가 보일 때까지 테스트 실행을 일시 중지합니다(기본 5초):

    // 5초 이내 대기
    $browser->waitFor('.selector');

    // 1초 이내 대기
    $browser->waitFor('.selector', 1);

지정한 셀렉터에 특정 텍스트가 나타날 때까지 기다릴 수도 있습니다:

    $browser->waitForTextIn('.selector', 'Hello World');
    $browser->waitForTextIn('.selector', 'Hello World', 1);

지정한 셀렉터가 사라질 때까지 기다릴 수도 있습니다:

    $browser->waitUntilMissing('.selector');
    $browser->waitUntilMissing('.selector', 1);

지정한 셀렉터가 활성/비활성화될 때까지 대기도 가능합니다:

    $browser->waitUntilEnabled('.selector');
    $browser->waitUntilEnabled('.selector', 1);
    $browser->waitUntilDisabled('.selector');
    $browser->waitUntilDisabled('.selector', 1);

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 준비됐을 때 범위 지정

특정 셀렉터가 나타났을 때 특정 작업을 수행하려면 `whenAvailable`을 사용할 수 있습니다:

    $browser->whenAvailable('.modal', function (Browser $modal) {
        $modal->assertSee('Hello World')
            ->press('OK');
    });

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText`로 특정 텍스트가 표시될 때까지 대기할 수 있습니다:

    $browser->waitForText('Hello World');
    $browser->waitForText('Hello World', 1);

`waitUntilMissingText`로 텍스트가 사라질 때까지 대기할 수 있습니다:

    $browser->waitUntilMissingText('Hello World');
    $browser->waitUntilMissingText('Hello World', 1);

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink`로 지정한 텍스트의 링크가 표시될 때까지 대기할 수 있습니다:

    $browser->waitForLink('Create');
    $browser->waitForLink('Create', 1);

<a name="waiting-for-inputs"></a>
#### 인풋 대기

`waitForInput`로 입력 필드가 보여질 때까지 대기할 수 있습니다:

    $browser->waitForInput($field);
    $browser->waitForInput($field, 1);

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기

`$browser->assertPathIs('/home')` 같이 경로 어서션 시, 비동기적으로 window.location.pathname이 변경되는 경우 실패할 수 있습니다. 이럴 때 `waitForLocation`을 사용할 수 있습니다:

    $browser->waitForLocation('/secret');

완전한 URL까지 기다릴 수도 있습니다:

    $browser->waitForLocation('https://example.com/path');

[named route](/docs/{{version}}/routing#named-routes)로도 대기 가능합니다:

    $browser->waitForRoute($routeName, $parameters);

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

액션 수행 후 페이지 리로드를 기다려야 한다면 `waitForReload`를 사용할 수 있습니다:

    use Laravel\Dusk\Browser;

    $browser->waitForReload(function (Browser $browser) {
        $browser->press('Submit');
    })
    ->assertSee('Success!');

보통 버튼 클릭 후에 자주 쓰이므로 `clickAndWaitForReload`도 제공됩니다:

    $browser->clickAndWaitForReload('.selector')
        ->assertSee('something');

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 조건 대기

특정 JavaScript 표현식이 true가 될 때까지 기다리려면 `waitUntil`을 사용하세요:

    $browser->waitUntil('App.data.servers.length > 0');
    $browser->waitUntil('App.data.servers.length > 0', 1);

<a name="waiting-on-vue-expressions"></a>
#### Vue 속성 대기

`waitUntilVue`, `waitUntilVueIsNot`로 [Vue 컴포넌트](https://vuejs.org) 속성이 특정 값이 될 때까지 대기할 수 있습니다:

    $browser->waitUntilVue('user.name', 'Taylor', '@user');
    $browser->waitUntilVueIsNot('user.name', null, '@user');

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기

`waitForEvent`로 JS 이벤트 발생까지 대기할 수 있습니다:

    $browser->waitForEvent('load');

기본적으로 body 엘리먼트 기준이지만, 범위 셀렉터를 넘길 수도 있습니다:

    $browser->with('iframe', function (Browser $iframe) {
        $iframe->waitForEvent('load');
    });

특정 엘리먼트로도 지정 가능:

    $browser->waitForEvent('load', '.selector');

`document`와 `window`에도 사용할 수 있습니다:

    $browser->waitForEvent('scroll', 'document');
    $browser->waitForEvent('resize', 'window', 5);

<a name="waiting-with-a-callback"></a>
#### 콜백으로 대기

대부분 "wait" 메서드는 내부적으로 `waitUsing`을 사용합니다. 직접 쓸 수도 있습니다:

    $browser->waitUsing(10, 1, function () use ($something) {
        return $something->isReady();
    }, "Something wasn't ready in time.");

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트 스크롤

클릭하려는 엘리먼트가 보이지 않을 때 `scrollIntoView`를 사용하면 엘리먼트가 보이는 위치로 스크롤합니다:

    $browser->scrollIntoView('.selector')
        ->click('.selector');

<a name="available-assertions"></a>
## 사용 가능한 어서션

Dusk는 다양한 어서션(검증) 메서드를 제공합니다. 모든 어서션은 아래와 같습니다:

<!-- 스타일 및 HTML 태그는 형식 유지를 위해 번역하지 않음 -->

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

<!-- 이하 각 어서션별 설명의 번역은 이해를 돕기 위해 생략합니다. (구체적 명령어 설명이므로 문법/코드는 번역 대상이 아닙니다.) -->

<a name="pages"></a>
## 페이지

테스트 중에 여러 복잡한 동작이 순차적으로 필요한 경우가 많습니다. 이런 경우 테스트 가독성이 떨어질 수 있는데, Dusk 페이지는 한 번에 실행할 수 있는 명확한 동작을 정의할 수 있도록 도와줍니다. 또한 단일 페이지용, 또는 전체 애플리케이션용 단축 셀렉터도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

페이지 오브젝트를 생성하려면 `dusk:page` Artisan 명령을 실행하세요. 모든 페이지 오브젝트는 `tests/Browser/Pages`에 위치합니다:

    php artisan dusk:page Login

<a name="configuring-pages"></a>
### 페이지 설정

기본적으로 페이지에는 `url`, `assert`, `elements`의 세 가지 메서드가 있습니다. 여기서는 `url`, `assert`에 대해 설명합니다. `elements`는 [아래서 더 다룹니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 대표하는 URL의 경로를 반환해야 합니다. Dusk는 브라우저가 페이지로 이동할 때 이 URL을 사용합니다:

    /**
     * 페이지 URL 반환.
     */
    public function url(): string
    {
        return '/login';
    }

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert` 메서드는 브라우저가 실제로 해당 페이지에 있는지 확인하는 데 필요한 어서션을 작성할 수 있습니다. 비워 둬도 되지만, 필요한 경우 원하는 어서션을 자유롭게 넣을 수 있습니다:

    /**
     * 브라우저가 해당 페이지에 있는지 어서트.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertPathIs($this->url());
    }

<a name="navigating-to-pages"></a>
### 페이지로 이동

페이지를 정의한 후에는 `visit`로 이동할 수 있습니다:

    use Tests\Browser\Pages\Login;

    $browser->visit(new Login);

현재 페이지에 이미 있고, 페이지 셀렉터 및 메서드를 로드해야 하는 경우가 있습니다. 예를 들어, 버튼을 눌러 리다이렉트된 다음, 특정 페이지의 기능을 사용하고 싶을 때는 `on` 메서드를 사용합니다:

    use Tests\Browser\Pages\CreatePlaylist;

    $browser->visit('/dashboard')
            ->clickLink('Create Playlist')
            ->on(new CreatePlaylist)
            ->assertSee('@create');

<a name="shorthand-selectors"></a>
### 단축 셀렉터

페이지 클래스의 `elements` 메서드를 통해 CSS 셀렉터에 별칭을 줄 수 있습니다. 예를 들어 로그인 페이지의 "email" 필드에 단축 별명을 줄 수 있습니다:

    public function elements(): array
    {
        return [
            '@email' => 'input[name=email]',
        ];
    }

이제 어느 곳에서든 단축 셀렉터를 사용할 수 있습니다:

    $browser->type('@email', 'taylor@laravel.com');

<a name="global-shorthand-selectors"></a>
#### 글로벌 단축 셀렉터

Dusk 설치 후 `tests/Browser/Pages`에 기본 `Page` 클래스가 있는데, 여기의 `siteElements` 메서드에 모든 페이지에서 사용할 글로벌 단축 셀렉터를 설정할 수 있습니다:

    public static function siteElements(): array
    {
        return [
            '@element' => '#selector',
        ];
    }

<a name="page-methods"></a>
### 페이지 메서드

기본 메서드 외에도, 반복적이거나 공통 동작을 메서드로 정의할 수 있습니다. 예를 들어 음악 관리 앱에서 플레이리스트를 생성하는 로직이 많다면 별도의 `createPlaylist` 메서드로 뽑을 수 있습니다:

    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }

이 메서드는 해당 페이지를 사용하는 모든 테스트에서 쉽게 재사용할 수 있습니다.

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 페이지 객체와 비슷하지만, 내비게이션 바나 알림창처럼 여러 페이지에서 반복적으로 등장하는 UI 및 기능을 위한 것입니다. 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

컴포넌트를 생성하려면 `dusk:component` Artisan 명령을 사용하세요. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 생성됩니다:

    php artisan dusk:component DatePicker

예시에는 "날짜 선택기" 컴포넌트가 있습니다. 여러 테스트에서 날짜를 설정하는 로직을 반복하지 않고, 아래 처럼 구현하면 됩니다:

<!-- 코드 생략, 원본과 동일 -->

<a name="using-components"></a>
### 컴포넌트 사용

이제 정의한 컴포넌트를 어떤 테스트에서든 재사용할 수 있습니다. 로직 수정이 필요할 땐 해당 컴포넌트만 변경하면 됩니다.

<!-- 코드 생략, 원본과 동일 -->

<a name="continuous-integration"></a>
## 지속적 통합(CI)

> [!WARNING]  
> 대부분의 Dusk CI 환경은 Laravel 애플리케이션을 8000번 포트에서 내장 PHP 개발 서버로 제공한다고 가정합니다. 따라서 CI 환경의 APP_URL 환경 변수는 반드시 `http://127.0.0.1:8000`으로 설정되어 있어야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 아래 Google Chrome 빌드팩과 스크립트를 `app.json`에 추가하세요.

<!-- JSON 및 코드 블록 생략, 원본과 동일 -->

<a name="running-tests-on-travis-ci"></a>
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 구성을 참고하세요. Travis CI는 GUI 환경이 아니므로, 크롬을 별도 실행하고, PHP 내장 서버를 띄워야 합니다.

<!-- YAML 및 코드 블록 생략, 원본과 동일 -->

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행할 때 사용할 수 있는 설정 예시는 아래와 같습니다.

<!-- YAML 및 코드 블록 생략, 원본과 동일 -->

<a name="running-tests-on-chipper-ci"></a>
### Chipper CI

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행할 때 사용할 수 있는 기본 설정입니다. 역시 PHP 내장 서버로 요청을 수신합니다.

<!-- YAML 및 코드 블록 생략, 원본과 동일 -->

Chipper CI에서의 Dusk 테스트 실행 및 데이터베이스 사용 등 자세한 내용은 [Chipper CI 공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.

---

*이 문서는 Laravel Dusk 공식 문서를 한국어로 번역한 것입니다. 최신 내용 및 상세 설명은 [공식 문서](https://laravel.com/docs/dusk)를 참고하세요.*