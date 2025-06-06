# 라라벨 Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행하기](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크에 저장하기](#storing-console-output-to-disk)
    - [페이지 소스 디스크에 저장하기](#storing-page-source-to-disk)
- [엘리먼트와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 활용](#using-the-keyboard)
    - [마우스 활용](#using-the-mouse)
    - [자바스크립트 대화상자](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기](#waiting-for-elements)
    - [엘리먼트로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 assertion](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지 이동](#navigating-to-pages)
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

[Laravel Dusk](https://github.com/laravel/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. Dusk는 별도의 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 이용하기 때문입니다. 하지만 원하는 경우 다른 Selenium 호환 드라이버도 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 [Google Chrome](https://www.google.com/chrome)을 설치한 후, 프로젝트에 `laravel/dusk` Composer 의존성을 추가해야 합니다:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록할 경우, 반드시 프로덕션 환경에서는 등록하지 않아야 합니다. 등록하면 임의의 사용자가 애플리케이션에 인증하여 접근할 수 있는 보안 위험이 생길 수 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` 아티즌 명령어를 실행합니다. 이 명령어는 `tests/Browser` 디렉터리, Dusk 테스트 예제, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 생성하고 설치해줍니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정합니다. 이 값은 브라우저에서 실제로 애플리케이션에 접속하는 URL과 동일해야 합니다.

> [!NOTE]
> 로컬 개발 환경 관리에 [Laravel Sail](/docs/12.x/sail)을 사용하고 있다면, Dusk 테스트의 [설정 및 실행에 관한 Sail 문서](/docs/12.x/sail#laravel-dusk)도 참고하시기 바랍니다.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령어로 라라벨 Dusk가 기본 설치하는 ChromeDriver가 아니라, 다른 버전의 ChromeDriver를 설치하고 싶다면 `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# 현재 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 운영체제에 특정 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# Chrome / Chromium의 버전에 맞는 ChromeDriver 자동 탐지 및 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk를 사용하려면 `chromedriver` 바이너리 실행 권한이 필요합니다. Dusk 실행에 문제가 있다면, 다음 명령어로 바이너리의 실행 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

Dusk는 기본적으로 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용하여 브라우저 테스트를 실행합니다. 그러나 원한다면 직접 Selenium 서버를 구동하고 원하는 브라우저에서 테스트를 진행할 수 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출 부분을 제거하면, Dusk가 ChromeDriver를 자동으로 시작하지 않도록 할 수 있습니다:

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

그런 다음, `driver` 메서드를 수정하여 원하는 URL과 포트로 연결하도록 설정할 수 있습니다. 또한, WebDriver에 전달해야 하는 "desired capabilities(원하는 기능 설정)"도 함께 변경할 수 있습니다:

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
## 시작하기

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 새로 생성하려면, `dusk:make` 아티즌 명령어를 사용하면 됩니다. 생성된 테스트 파일은 `tests/Browser` 디렉터리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 불러오는 페이지와 상호작용하게 됩니다. 다만, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. `RefreshDatabase` 트레이트는 데이터베이스 트랜잭션에 의존하는데, HTTP 요청 간에는 이러한 트랜잭션이 적합하지 않거나 사용할 수 없습니다. 이를 대신해 `DatabaseMigrations` 트레이트나 `DatabaseTruncation` 트레이트 두 가지 방법을 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 마이그레이션을 이용한 초기화

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 수행합니다. 하지만, 테스트마다 데이터베이스 테이블을 삭제하고 다시 생성하므로, 테이블을 단순히 비우는 것보다 속도가 느릴 수 있습니다:

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
> Dusk 테스트 실행 시 SQLite 인메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 독립적인 프로세스에서 동작하기 때문에, 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### Truncation을 이용한 초기화

`DatabaseTruncation` 트레이트를 사용하면 첫 번째 테스트에서 데이터베이스를 마이그레이션하여 테이블이 제대로 생성되었는지 확인합니다. 그리고 그 이후 테스트부터는 테이블을 단순히 비우기(truncation)만 하므로, 매번 모든 마이그레이션을 반복하는 것보다 훨씬 빠릅니다:

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

기본적으로, 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 비웁니다. 비우고자 하는 테이블 목록을 직접 지정하고 싶다면, 테스트 클래스에서 `$tablesToTruncate` 프로퍼티를 정의할 수 있습니다:

> [!NOTE]
> Pest를 사용 중이라면, 변수를 정의할 때는 기본 `DuskTestCase`나 테스트 파일이 상속하는 클래스에 속성 또는 메서드를 추가해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

반대로, 비우지 않을 테이블을 명시하고 싶다면 `$exceptTables` 프로퍼티를 사용할 수 있습니다:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

여러 데이터베이스 연결에서 테이블을 비우고자 한다면, `$connectionsToTruncate` 프로퍼티를 정의하면 됩니다:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

테이블 비우기 작업 전후로 코드를 실행하고 싶을 때는 테스트 클래스에서 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의할 수 있습니다:

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
### 테스트 실행하기

브라우저 테스트를 실행하려면 `dusk` 아티즌 명령어를 사용하세요:

```shell
php artisan dusk
```

마지막으로 `dusk` 명령어 실행 시 실패한 테스트가 있다면, `dusk:fails` 명령어로 이전 실패 테스트만 먼저 실행해 시간을 아낄 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest/PHPUnit 테스트 러너가 일반적으로 지원하는 모든 인수를 전달할 수 있습니다. 예를 들어, 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)만 실행하도록 지시할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 로컬 개발 환경을 관리한다면, [Dusk 테스트 설정 및 실행법](/docs/12.x/sail#laravel-dusk)도 꼭 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려 시도합니다. 하지만 환경에 따라 자동 실행이 동작하지 않을 수도 있기 때문에, 이 경우에는 테스트 실행 전 직접 ChromeDriver를 수동으로 띄울 수 있습니다. 직접 ChromeDriver를 실행한다면, `tests/DuskTestCase.php` 파일에서 다음 라인을 주석 처리해야 합니다:

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

또한, ChromeDriver를 9515가 아닌 다른 포트에서 실행한다면, 해당 클래스의 `driver` 메서드에서 포트 번호 또한 변경해주어야 합니다:

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
### 환경 파일 처리

Dusk가 테스트 실행 시 별도의 환경 파일을 사용하도록 강제하려면, 프로젝트 루트 디렉터리에 `.env.dusk.{환경명}` 형식의 파일을 생성하면 됩니다. 예를 들어, `local` 환경에서 `dusk` 명령어를 실행한다면, `.env.dusk.local` 파일을 만들어야 합니다.

테스트 실행 시, Dusk는 기존의 `.env` 파일을 백업하고 Dusk 환경 파일명을 `.env`로 변경합니다. 테스트가 완료되면 원래의 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성

우선, 애플리케이션에 로그인할 수 있는지 확인하는 테스트를 작성해보겠습니다. 테스트를 생성한 후, 로그인 페이지로 이동하여 인증 정보를 입력하고 "Login" 버튼을 클릭하는 동작을 추가할 수 있습니다. 브라우저 인스턴스를 생성하려면, Dusk 테스트에서 `browse` 메서드를 호출하면 됩니다:

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

위 예시에서 볼 수 있듯, `browse` 메서드는 클로저(익명 함수)를 받으며, 이 클로저로 브라우저 인스턴스가 자동으로 전달됩니다. 이 브라우저 인스턴스를 통해 실제 애플리케이션과 상호작용하고 assertion(검증)을 수행할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 인스턴스 생성하기

특정 테스트에서는 여러 브라우저가 필요할 수도 있습니다. 예를 들어, 웹소켓이 연동된 채팅 화면 등은 여러 브라우저 인스턴스에서의 상호작용이 필요할 수 있습니다. 이럴 땐, `browse` 메서드에 전달하는 클로저의 인자에 브라우저 인스턴스를 여러 개 선언하면 됩니다:

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
### 네비게이션

`visit` 메서드를 사용해 애플리케이션 내 특정 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

또한, `visitRoute` 메서드를 통해 [네임드 라우트](/docs/12.x/routing#named-routes)로 이동할 수도 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

`back` 및 `forward` 메서드를 이용해 브라우저의 뒤/앞 페이지로 이동할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드를 이용해 현재 페이지를 새로고침 할 수도 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메서드로 브라우저 창의 크기를 변경할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드를 사용하면 브라우저 창이 전체 화면으로 최대화됩니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 콘텐츠에 맞게 창 크기를 자동으로 조정합니다:

```php
$browser->fitContent();
```

테스트가 실패할 경우, Dusk는 자동으로 스크린샷을 찍기 전 브라우저를 콘텐츠 크기에 맞게 조정합니다. 이런 기능을 꺼두고 싶다면 테스트 내에서 `disableFitOnFailure` 메서드를 호출하면 됩니다:

```php
$browser->disableFitOnFailure();
```

`move` 메서드를 사용해 브라우저 창을 원하는 위치로 이동시킬 수도 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 커스텀 브라우저 메서드가 필요하다면, `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통은 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 메서드를 호출합니다:

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 이렇게 등록한 매크로는 `Browser` 인스턴스에서 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증

인증이 필요한 페이지를 테스트하는 경우가 많습니다. 이럴 때마다 로그인 화면을 거치지 않기 위해 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. `loginAs`는 인증 가능한 모델의 기본키 또는 모델 인스턴스를 받아 처리합니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용한 이후에는 해당 파일 내의 모든 테스트에서 사용자의 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드를 이용해 암호화된 쿠키 값을 조회하거나 설정할 수 있습니다. 라라벨이 생성하는 모든 쿠키는 기본적으로 암호화 처리되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값을 다루고 싶다면 `plainCookie` 메서드를 사용할 수 있습니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

지정한 쿠키를 삭제하려면 `deleteCookie` 메서드를 사용하세요:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>

### 자바스크립트 실행

브라우저 내에서 임의의 JavaScript 구문을 실행하려면 `script` 메서드를 사용할 수 있습니다.

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 메서드를 사용하여 스크린샷을 촬영하고, 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다.

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드를 사용하면 여러 반응형 구간(breakpoints)에서 연속으로 스크린샷을 촬영할 수도 있습니다.

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드를 활용하면 특정 요소만 스크린샷으로 저장할 수 있습니다.

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 내용을 디스크에 저장하기

`storeConsoleLog` 메서드를 사용하면 현재 브라우저의 콘솔 출력을 지정한 파일명으로 디스크에 저장할 수 있습니다. 콘솔 출력은 `tests/Browser/console` 디렉터리에 저장됩니다.

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크에 저장하기

현재 페이지의 소스 코드를 디스크에 저장하려면 `storeSource` 메서드를 사용할 수 있습니다. 저장된 소스 파일은 `tests/Browser/source` 디렉터리에 위치합니다.

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기

<a name="dusk-selectors"></a>
### Dusk 셀렉터(Dusk Selectors)

효과적으로 Dusk 테스트를 작성할 때 가장 어려운 부분 중 하나는 요소와 상호작용할 적절한 CSS 셀렉터를 선택하는 일입니다. 프론트엔드가 시간이 지나면서 변경되면, 아래와 같은 CSS 셀렉터가 테스트를 깨뜨릴 수 있습니다.

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터를 외우지 않고도 효과적인 테스트 작성에 집중할 수 있습니다. 셀렉터를 정의하려면, HTML 요소에 `dusk` 속성을 추가하세요. 그리고 테스트에서 해당 셀렉터를 사용할 때는 `@` 기호를 접두사로 붙여 사용하면 됩니다.

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원한다면 Dusk 셀렉터가 참조하는 HTML 속성을 `selectorHtmlAttribute` 메서드로 커스터마이징할 수도 있습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기

Dusk는 페이지 내 요소의 현재 값이나 표시 텍스트, 속성(attribute)과 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, 특정 CSS 또는 Dusk 셀렉터와 일치하는 요소의 "값"을 가져오려면 `value` 메서드를 사용합니다.

```php
// 값 조회...
$value = $browser->value('selector');

// 값 설정...
$browser->value('selector', 'value');
```

특정 필드명을 가진 input 요소의 "값"을 가져오려면 `inputValue` 메서드를 사용하면 됩니다.

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드는 지정된 셀렉터와 일치하는 요소의 표시 텍스트를 가져오는 데 사용할 수 있습니다.

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

마지막으로, `attribute` 메서드는 지정된 셀렉터와 일치하는 요소의 특정 속성 값을 가져올 수 있습니다.

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력하기

Dusk는 폼과 input 요소와 상호작용하기 위한 다양한 메서드를 제공합니다. 가장 기본적으로, 입력 필드에 텍스트를 입력하는 예시는 다음과 같습니다.

```php
$browser->type('email', 'taylor@laravel.com');
```

이 메서드는 필요하다면 CSS 셀렉터도 받을 수 있지만, 필수는 아닙니다. CSS 셀렉터를 전달하지 않으면 Dusk는 주어진 `name` 속성을 가진 `input` 또는 `textarea` 필드를 찾습니다.

필드의 기존 내용을 지우지 않고 텍스트를 추가하고 싶다면 `append` 메서드를 사용할 수 있습니다.

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

`clear` 메서드를 사용하여 입력값을 지울 수도 있습니다.

```php
$browser->clear('email');
```

Dusk로 천천히 타이핑하게 하려면 `typeSlowly` 메서드를 사용하세요. 기본적으로 Dusk는 키를 한 번 누를 때마다 100 밀리초씩 대기합니다. 대기 시간을 조정하려면 세 번째 인수로 밀리초 값을 전달하면 됩니다.

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드를 사용하면 텍스트를 천천히 추가할 수도 있습니다.

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운(Dropdowns)

`select` 요소에서 특정 값을 선택하려면 `select` 메서드를 사용하세요. 이 메서드 역시 `type` 메서드처럼 풀 CSS 셀렉터가 필요하지 않습니다. 값을 전달할 때는 표시 텍스트가 아니라 실제 option의 값을 넘겨야 합니다.

```php
$browser->select('size', 'Large');
```

두 번째 인자를 생략하면 무작위로 옵션을 하나 선택할 수 있습니다.

```php
$browser->select('size');
```

두 번째 인자로 배열을 전달하면 여러 옵션을 한 번에 선택할 수도 있습니다.

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스(Checkboxes)

체크박스 input을 "체크"하려면 `check` 메서드를 사용합니다. 다른 input 관련 메서드와 마찬가지로, CSS 셀렉터가 꼭 필요하지는 않습니다. 만약 CSS 셀렉터로 찾을 수 없으면 Dusk는 동일한 `name` 속성을 가진 체크박스를 검색하게 됩니다.

```php
$browser->check('terms');
```

체크박스를 "체크 해제"하려면 `uncheck` 메서드를 사용합니다.

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼(Radio Buttons)

`radio` input 옵션을 "선택"하려면 `radio` 메서드를 사용합니다. 이것 역시 다른 input 메서드와 같이 CSS 셀렉터가 필수는 아닙니다. 일치하는 CSS 셀렉터가 없을 경우, Dusk는 `name`과 `value` 속성이 일치하는 radio input을 검색합니다.

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부

`attach` 메서드는 `file` input 요소에 파일을 첨부할 때 사용할 수 있습니다. 이 역시 풀 CSS 셀렉터가 필요하지 않으며, 일치하는 셀렉터가 없을 경우 주어진 `name` 속성에 해당하는 input 요소를 찾아줍니다.

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능을 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치되어 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭하기

`press` 메서드를 사용해 페이지 내 버튼 요소를 클릭할 수 있습니다. 인수로 전달하는 값은 버튼의 표시 텍스트, 혹은 CSS / Dusk 셀렉터일 수 있습니다.

```php
$browser->press('Login');
```

폼 제출 시 많은 애플리케이션에서는 버튼이 눌린 후 HTTP 요청이 완료될 때까지 버튼을 비활성화한 뒤, 요청 완료 시 다시 활성화하는 패턴을 사용합니다. 버튼 클릭 후 버튼이 다시 활성화될 때까지 기다리고 싶다면, `pressAndWaitFor` 메서드를 사용할 수 있습니다.

```php
// 버튼을 클릭하고 최대 5초 동안 버튼이 활성화될 때까지 대기합니다...
$browser->pressAndWaitFor('Save');

// 버튼을 클릭하고 최대 1초 동안 버튼이 활성화될 때까지 대기합니다...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기

링크를 클릭하려면 브라우저 인스턴스의 `clickLink` 메서드를 사용하세요. 이 메서드는 주어진 표시 텍스트를 가진 링크를 클릭합니다.

```php
$browser->clickLink($linkText);
```

특정 표시 텍스트를 가진 링크가 페이지에 나타나 있는지 판별하려면 `seeLink` 메서드를 사용할 수도 있습니다.

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이러한 메서드는 jQuery와 상호작용합니다. 페이지에 jQuery가 없다면, Dusk가 테스트를 수행하는 동안 자동으로 jQuery를 삽입하여 사용할 수 있게 만듭니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기

`keys` 메서드를 이용하면 단순한 `type` 메서드보다 더 복잡한 키 입력을 요소에 전달할 수 있습니다. 예를 들어, 입력하는 동안 modifier 키를 누르는 등의 동작이 가능합니다. 아래 예시에서는 `shift` 키를 누른 상태로 `taylor`를 입력한 후, modifier 없이 `swift`를 입력합니다.

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

다른 활용 예로, 애플리케이션의 주요 CSS 셀렉터에 "키보드 단축키" 조합을 전달할 수 있습니다.

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 modifier 키는 모두 `{}`로 감싸서 표기해야 하며, `Facebook\WebDriver\WebDriverKeys` 클래스에서 정의된 상수와 일치합니다. (상세 내용은 [GitHub에서 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)할 수 있습니다.)

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk는 `Laravel\Dusk\Keyboard` 클래스를 통해 복잡한 키보드 상호작용을 간편하게 할 수 있도록 `withKeyboard` 메서드도 제공합니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 등 다양한 메서드를 제공하며, 예시는 다음과 같습니다.

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

테스트 전체에서 재사용할 수 있도록 커스텀 키보드 상호작용을 정의하려면, `Keyboard` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에 작성하는 것이 일반적입니다.

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받습니다. 이 매크로는 `Keyboard` 인스턴스에서 메서드로 호출할 때 실행됩니다.

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용하기

<a name="clicking-on-elements"></a>
#### 요소 클릭하기

`click` 메서드를 사용하여 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소를 클릭할 수 있습니다.

```php
$browser->click('.selector');
```

주어진 XPath와 일치하는 요소를 클릭하려면 `clickAtXPath` 메서드를 사용합니다.

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드를 사용하면 브라우저 화면의 기준 좌표에서 가장 위에 놓인 요소를 클릭할 수 있습니다.

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 마우스 더블 클릭을, `rightClick` 메서드는 마우스 오른쪽 클릭을 시뮬레이션합니다.

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드는 마우스 버튼을 누른 채로 유지하는 동작을 시뮬레이션합니다. 이후 `releaseMouse` 메서드를 호출하면 마우스 버튼이 해제됩니다.

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` 메서드는 브라우저 내에서 `ctrl+클릭` 이벤트를 시뮬레이션합니다.

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스오버(Mouseover)

`mouseover` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소 위로 마우스를 이동하는 동작을 수행합니다.

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭(Drag and Drop)

`drag` 메서드는 지정한 셀렉터의 요소를 다른 요소로 드래그할 때 사용합니다.

```php
$browser->drag('.from-selector', '.to-selector');
```

또는, 한 방향으로만 요소를 드래그할 수도 있습니다.

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 요소를 드래그하려면 아래처럼 사용합니다.

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그(JavaScript Dialogs)

Dusk는 자바스크립트 다이얼로그와 상호작용할 수 있도록 여러 메서드를 제공합니다. 예를 들어, `waitForDialog` 메서드를 사용하면 자바스크립트 다이얼로그가 표시될 때까지 기다릴 수 있습니다. 이 메서드는 다이얼로그가 표시될 때까지 대기할 최대 초 단위 시간을 인수로 받을 수 있습니다.

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 다이얼로그가 표시되었고, 특정 메시지를 담고 있는지 확인하는 데 사용할 수 있습니다.

```php
$browser->assertDialogOpened('Dialog message');
```

자바스크립트 다이얼로그에 프롬프트가 있다면, `typeInDialog` 메서드로 값을 입력할 수 있습니다.

```php
$browser->typeInDialog('Hello World');
```

"OK" 버튼을 클릭하여 열린 자바스크립트 다이얼로그를 닫으려면 `acceptDialog` 메서드를 호출하면 됩니다.

```php
$browser->acceptDialog();
```

"Cancel" 버튼을 클릭하여 다이얼로그를 닫으려면 `dismissDialog` 메서드를 사용하세요.

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용

iframe 내부 요소와 상호작용할 필요가 있을 때는 `withinFrame` 메서드를 사용할 수 있습니다. 이 메서드에 전달하는 클로저 내에서 이루어지는 모든 요소 상호작용은 지정한 iframe의 컨텍스트 내에서만 수행됩니다.

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정

특정 셀렉터 안에서 여러 동작을 묶어서 실행하고 싶은 경우가 종종 있습니다. 예를 들어, 어떤 텍스트가 특정 테이블 내부에만 존재하는지 확인한 뒤, 같은 테이블 내의 버튼을 클릭하고 싶을 수 있습니다. 이럴 때 `with` 메서드를 사용하면 됩니다. 이 메서드에 전달한 클로저 안에서 수행되는 모든 작업은 원래 지정한 셀렉터의 범위로 한정됩니다.

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때로는 현재 스코프(범위) 외부에서 assertion을 실행해야 할 필요가 생길 수도 있습니다. 이럴 땐 `elsewhere`나 `elsewhereWhenAvailable` 메서드를 사용할 수 있습니다.

```php
$browser->with('.table', function (Browser $table) {
    // 현재 스코프는 `body .table`입니다...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`입니다...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`입니다...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기(Waiting for Elements)

자바스크립트가 많이 사용되는 애플리케이션을 테스트할 때는, 테스트 진행 전에 특정 요소나 데이터가 준비될 때까지 "대기"하는 작업이 자주 필요하게 됩니다. Dusk는 이를 매우 간편하게 처리할 수 있도록 다양한 대기 메서드를 제공합니다. 이를 활용해, 특정 요소가 페이지에 표시될 때까지 혹은 주어진 자바스크립트 표현식이 `true`가 될 때까지 대기할 수 있습니다.

<a name="waiting"></a>
#### 대기하기

테스트를 지정한 밀리초(ms) 동안 단순히 일시정지하고 싶다면 `pause` 메서드를 사용하세요.

```php
$browser->pause(1000);
```

특정 조건이 `true`일 때만 일시정지하려면 `pauseIf` 메서드를 사용합니다.

```php
$browser->pauseIf(App::environment('production'), 1000);
```

반대로, 특정 조건이 `true`가 아닐 때만 일시정지하려면 `pauseUnless` 메서드를 쓸 수 있습니다.

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기(Waiting for Selectors)

`waitFor` 메서드는, 지정한 CSS 또는 Dusk 셀렉터와 일치하는 요소가 페이지에 표시될 때까지 테스트 실행을 일시정지합니다. 기본적으로 최대 5초까지 대기 후, 해당 요소가 없으면 예외가 발생합니다. 필요하다면 두 번째 인수로 타임아웃(초 단위)을 지정할 수 있습니다.

```php
// 최대 5초 동안 해당 셀렉터가 표시될 때까지 대기...
$browser->waitFor('.selector');

// 최대 1초 동안 해당 셀렉터가 표시될 때까지 대기...
$browser->waitFor('.selector', 1);
```

또한, 지정한 셀렉터와 일치하는 요소에 특정 텍스트가 나타날 때까지 대기할 수도 있습니다.

```php
// 최대 5초 동안 지정 텍스트가 나타날 때까지 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 동안 지정 텍스트가 나타날 때까지 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

반대로, 지정한 셀렉터와 일치하는 요소가 페이지에서 사라질 때까지 대기할 수도 있습니다.

```php
// 최대 5초 동안 해당 셀렉터가 사라질 때까지 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 동안 해당 셀렉터가 사라질 때까지 대기...
$browser->waitUntilMissing('.selector', 1);
```

또는, 해당 셀렉터의 요소가 활성화/비활성화될 때까지 대기할 수도 있습니다.

```php
// 최대 5초 동안 요소가 활성화될 때까지 대기...
$browser->waitUntilEnabled('.selector');

// 최대 1초 동안 요소가 활성화될 때까지 대기...
$browser->waitUntilEnabled('.selector', 1);

// 최대 5초 동안 요소가 비활성화될 때까지 대기...
$browser->waitUntilDisabled('.selector');

// 최대 1초 동안 요소가 비활성화될 때까지 대기...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>

#### 사용할 수 있을 때 셀렉터 범위 지정하기

때때로, 특정 셀렉터와 일치하는 요소가 나타날 때까지 기다렸다가 해당 요소에 상호작용하고 싶을 때가 있습니다. 예를 들어, 모달 창이 표시될 때까지 기다렸다가 그 모달 안의 "OK" 버튼을 클릭하고 싶은 경우가 있을 수 있습니다. 이럴 때는 `whenAvailable` 메서드를 사용할 수 있습니다. 전달한 클로저 내부에서 실행되는 모든 요소 동작은 원래의 셀렉터 범위로 한정됩니다.

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트가 나타날 때까지 대기하기

`waitForText` 메서드를 사용하면, 지정한 텍스트가 페이지에 표시될 때까지 대기할 수 있습니다.

```php
// 텍스트가 표시될 때까지 최대 5초 동안 기다립니다...
$browser->waitForText('Hello World');

// 텍스트가 표시될 때까지 최대 1초 동안 기다립니다...
$browser->waitForText('Hello World', 1);
```

페이지에서 위치한 텍스트가 사라질 때까지 기다려야 하는 경우에는 `waitUntilMissingText` 메서드를 사용할 수 있습니다.

```php
// 텍스트가 사라질 때까지 최대 5초 동안 기다립니다...
$browser->waitUntilMissingText('Hello World');

// 텍스트가 사라질 때까지 최대 1초 동안 기다립니다...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크가 표시될 때까지 대기하기

`waitForLink` 메서드를 사용하면, 지정한 링크 텍스트가 페이지에 표시될 때까지 대기할 수 있습니다.

```php
// 링크가 표시될 때까지 최대 5초 동안 기다립니다...
$browser->waitForLink('Create');

// 링크가 표시될 때까지 최대 1초 동안 기다립니다...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드가 표시될 때까지 대기하기

`waitForInput` 메서드를 사용하면, 지정한 입력 필드가 페이지에 표시될 때까지 대기할 수 있습니다.

```php
// 입력 필드가 표시될 때까지 최대 5초 동안 기다립니다...
$browser->waitForInput($field);

// 입력 필드가 표시될 때까지 최대 1초 동안 기다립니다...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 변화 대기하기

`$browser->assertPathIs('/home')`와 같은 경로(assertion) 검증을 할 때, `window.location.pathname`이 비동기로 갱신되면 검증에 실패할 수 있습니다. 이런 경우에는 `waitForLocation` 메서드를 사용해 원하는 위치가 될 때까지 대기할 수 있습니다.

```php
$browser->waitForLocation('/secret');
```

`waitForLocation` 메서드는 현재 창의 위치가 전체 URL로 변경될 때까지 대기하는 데도 사용할 수 있습니다.

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/12.x/routing#named-routes)의 위치를 대상으로 대기할 수도 있습니다.

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기하기

어떤 동작을 수행한 후 페이지가 리로드될 때까지 기다려야 한다면, `waitForReload` 메서드를 사용하면 됩니다.

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

보통 버튼을 클릭한 직후에 페이지 리로드를 기다리는 경우가 많으므로, 조금 더 간편하게 `clickAndWaitForReload` 메서드를 사용할 수도 있습니다.

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기하기

때때로, 테스트 실행을 특정 JavaScript 표현식의 값이 `true`가 될 때까지 잠시 멈추고 싶을 때가 있습니다. 이럴 때는 `waitUntil` 메서드를 쉽게 사용할 수 있습니다. 이 메서드에 표현식을 전달할 때는 `return` 키워드나 끝의 세미콜론을 포함하지 않아도 됩니다.

```php
// 해당 표현식이 true가 될 때까지 최대 5초 동안 기다립니다...
$browser->waitUntil('App.data.servers.length > 0');

// 해당 표현식이 true가 될 때까지 최대 1초 동안 기다립니다...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기하기

`waitUntilVue`, `waitUntilVueIsNot` 메서드는 [Vue 컴포넌트](https://vuejs.org)의 속성 값이 원하는 값이 될 때까지 대기할 수 있게 해줍니다.

```php
// 컴포넌트 속성이 지정한 값을 가지게 될 때까지 대기합니다...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 컴포넌트 속성이 지정한 값을 가지지 않게 될 때까지 대기합니다...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기하기

`waitForEvent` 메서드는 JavaScript 이벤트가 발생할 때까지 테스트 실행을 일시 중단하는 데 사용할 수 있습니다.

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 현재 스코프, 즉 기본적으로 `body` 요소에 연결됩니다. 선택자를 범위로 지정해서 사용할 경우에는 해당 요소에 이벤트 리스너가 연결됩니다.

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트를 기다립니다...
    $iframe->waitForEvent('load');
});
```

`waitForEvent` 메서드의 두 번째 인수로 셀렉터를 지정하여 이벤트 리스너를 특정 요소에 연결할 수도 있습니다.

```php
$browser->waitForEvent('load', '.selector');
```

또한 `document`나 `window` 객체에서 발생하는 이벤트도 기다릴 수 있습니다.

```php
// document가 스크롤될 때까지 기다립니다...
$browser->waitForEvent('scroll', 'document');

// window가 리사이즈될 때까지 최대 5초 동안 기다립니다...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 함수로 대기하기

Dusk의 다양한 "wait" 관련 메서드는 내부적으로 `waitUsing` 메서드를 기반으로 동작합니다. 직접 이 메서드를 사용하여, 주어진 클로저가 `true`를 반환할 때까지 대기할 수 있습니다. `waitUsing` 메서드는 최대 대기 시간(초), 클로저 호출 간격, 클로저 자체, 그리고 실패 시 표시할 메시지(선택 사항)를 인수로 받습니다.

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 화면에 스크롤하여 보이게 만들기

때로는 클릭하고자 하는 요소가 브라우저의 화면 밖에 있어서 클릭이 불가능한 경우가 있습니다. `scrollIntoView` 메서드는 지정한 셀렉터의 요소가 브라우저의 화면 안에 올 때까지 자동으로 스크롤을 이동시켜 줍니다.

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 Assertion

Dusk는 여러분이 애플리케이션에 대해 사용할 수 있는 다양한 assertion(검증) 메서드를 제공합니다. 아래 목록에서 모든 지원하는 assertion을 확인할 수 있습니다.

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

<a name="assert-title"></a>
#### assertTitle

페이지의 제목이 주어진 텍스트와 일치하는지 확인합니다.

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지의 제목에 주어진 텍스트가 포함되어 있는지 확인합니다.

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 스트링 제외)이 주어진 문자열과 일치하는지 확인합니다.

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL의 스킴(scheme)이 주어진 스킴과 일치하는지 확인합니다.

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL의 스킴이 주어진 스킴과 일치하지 않는지 확인합니다.

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL의 호스트(host)가 주어진 호스트와 일치하는지 확인합니다.

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL의 호스트가 주어진 호스트와 일치하지 않는지 확인합니다.

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL의 포트(port)가 주어진 포트와 일치하는지 확인합니다.

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL의 포트가 주어진 포트와 일치하지 않는지 확인합니다.

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로(path)가 주어진 경로로 시작하는지 확인합니다.

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

현재 URL 경로가 주어진 경로로 끝나는지 확인합니다.

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

현재 URL 경로에 주어진 경로가 포함되어 있는지 확인합니다.

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 주어진 경로와 일치하는지 확인합니다.

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 주어진 경로와 일치하지 않는지 확인합니다.

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 지정한 [네임드 라우트](/docs/12.x/routing#named-routes)의 URL과 일치하는지 확인합니다.

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

지정한 쿼리 스트링 파라미터가 존재하는지 확인합니다.

```php
$browser->assertQueryStringHas($name);
```

지정한 쿼리 스트링 파라미터가 존재하고, 그 값이 아래와 같이 전달한 값과 일치하는지 확인합니다.

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

지정한 쿼리 스트링 파라미터가 없는지 확인합니다.

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

URL의 현재 해시 프래그먼트(fragment)가 주어진 값과 일치하는지 확인합니다.

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

URL의 현재 해시 프래그먼트가 주어진 값으로 시작하는지 확인합니다.

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

URL의 현재 해시 프래그먼트가 주어진 값과 일치하지 않는지 확인합니다.

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

지정한 암호화된 쿠키가 존재하는지 확인합니다.

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

지정한 암호화되지 않은 쿠키가 존재하는지 확인합니다.

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

지정한 암호화된 쿠키가 존재하지 않는지 확인합니다.

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

지정한 암호화되지 않은 쿠키가 존재하지 않는지 확인합니다.

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키의 값이 주어진 값과 일치하는지 확인합니다.

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키의 값이 주어진 값과 일치하는지 확인합니다.

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

지정한 텍스트가 페이지에 존재하는지 확인합니다.

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

지정한 텍스트가 페이지에 존재하지 않는지 확인합니다.

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

해당 셀렉터 내부에 지정한 텍스트가 존재하는지 확인합니다.

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

해당 셀렉터 내부에 지정한 텍스트가 존재하지 않는지 확인합니다.

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

해당 셀렉터 내부에 어떤 텍스트든 존재하는지 확인합니다.

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>

#### assertSeeNothingIn

지정한 셀렉터에 아무 텍스트도 존재하지 않는지 확인합니다.

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### assertCount

주어진 셀렉터와 일치하는 요소가 지정한 횟수만큼 나타나는지 확인합니다.

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### assertScript

지정한 JavaScript 표현식이 특정 값으로 평가되는지 확인합니다.

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

주어진 소스 코드가 페이지에 존재하는지 확인합니다.

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

주어진 소스 코드가 페이지에 존재하지 않는지 확인합니다.

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

주어진 링크가 페이지에 존재하는지 확인합니다.

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

주어진 링크가 페이지에 존재하지 않는지 확인합니다.

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

지정한 입력 필드가 주어진 값을 가지고 있는지 확인합니다.

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

지정한 입력 필드의 값이 특정 값이 아님을 확인합니다.

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

주어진 체크박스가 선택되어 있는지 확인합니다.

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

주어진 체크박스가 선택되어 있지 않은지 확인합니다.

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

주어진 체크박스가 '불확정(indeterminate)' 상태인지 확인합니다.

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

주어진 라디오 필드에서 특정 값이 선택되어 있는지 확인합니다.

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

주어진 라디오 필드에서 특정 값이 선택되어 있지 않은지 확인합니다.

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

주어진 드롭다운 필드에서 지정한 값이 선택되어 있는지 확인합니다.

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

주어진 드롭다운 필드에서 특정 값이 선택되어 있지 않은지 확인합니다.

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

주어진 값의 배열이 선택 옵션으로 존재하는지 확인합니다.

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

주어진 값의 배열이 선택 옵션으로 존재하지 않는지 확인합니다.

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

지정한 필드에서 특정 값이 선택 옵션으로 존재하는지 확인합니다.

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

특정 값이 선택 옵션으로 존재하지 않는지 확인합니다.

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

주어진 셀렉터와 일치하는 요소가 특정 값을 가지고 있는지 확인합니다.

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

주어진 셀렉터와 일치하는 요소가 특정 값을 가지고 있지 않은지 확인합니다.

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

주어진 셀렉터와 일치하는 요소가, 특정 속성(attribute)에 지정한 값을 가지고 있는지 확인합니다.

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

주어진 셀렉터와 일치하는 요소에, 특정 속성(attribute)이 존재하지 않는지 확인합니다.

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

주어진 셀렉터와 일치하는 요소의 특정 속성(attribute)이 지정한 값을 포함하는지 확인합니다.

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

주어진 셀렉터와 일치하는 요소의 특정 속성(attribute)이 지정한 값을 포함하지 않는지 확인합니다.

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

주어진 셀렉터와 일치하는 요소의 aria 속성에 지정한 값이 존재하는지 확인합니다.

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어, `<button aria-label="Add"></button>` 마크업이 있을 때, `aria-label` 속성을 아래와 같이 검증할 수 있습니다.

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

주어진 셀렉터와 일치하는 요소의 data 속성에 지정된 값이 존재하는지 확인합니다.

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어, `<tr id="row-1" data-content="attendees"></tr>` 마크업이 있을 때, `data-label` 속성을 아래와 같이 검증할 수 있습니다.

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

주어진 셀렉터와 일치하는 요소가 화면에 보이는지(visible) 확인합니다.

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

주어진 셀렉터와 일치하는 요소가 소스에 존재하는지 확인합니다.

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

주어진 셀렉터와 일치하는 요소가 소스에 존재하지 않는지 확인합니다.

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

주어진 셀렉터와 일치하는 요소가 화면에 보이지 않는지 확인합니다.

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

지정한 이름을 가진 input 태그가 존재하는지 확인합니다.

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

지정한 이름의 input 태그가 소스코드에 존재하지 않는지 확인합니다.

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

지정한 메시지를 가진 JavaScript 다이얼로그가 열렸는지 확인합니다.

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

해당 필드가 활성화되어 있는지 확인합니다.

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

해당 필드가 비활성화(disabled) 상태인지 확인합니다.

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

주어진 버튼이 활성화되어 있는지 확인합니다.

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

주어진 버튼이 비활성화되어 있는지 확인합니다.

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

해당 필드에 포커스(focus)가 되어 있는지 확인합니다.

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

해당 필드에 포커스가 되어 있지 않은지 확인합니다.

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태인지 확인합니다.

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태(게스트)인지 확인합니다.

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

사용자가 주어진 사용자로 인증되었는지 확인합니다.

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 [Vue 컴포넌트](https://vuejs.org) 데이터의 상태도 검증할 수 있습니다. 예를 들어, 애플리케이션에 아래와 같은 Vue 컴포넌트가 있다고 가정해보겠습니다.

```
// HTML...

<profile dusk="profile-component"></profile>

// Component Definition...

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

아래와 같이 Vue 컴포넌트의 상태를 검증할 수 있습니다.

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
 * A basic Vue test example.
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

지정한 Vue 컴포넌트의 데이터 속성이 특정 값과 일치하지 않는지 확인합니다.

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

지정한 Vue 컴포넌트 데이터 속성이 배열이고, 해당 값이 포함되어 있는지 확인합니다.

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

지정한 Vue 컴포넌트 데이터 속성이 배열이고, 해당 값이 포함되어 있지 않은지 확인합니다.

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지(Pages)

테스트를 진행하다 보면 복잡한 작업을 여러 번 순차적으로 실행해야 할 때가 있습니다. 이런 경우 테스트가 읽기 어렵고 복잡해질 수 있습니다. Dusk 페이지(Pages) 기능을 사용하면, 특정 페이지에서 수행해야 하는 작업을 메서드 하나로 간결하게 정의할 수 있습니다. 또한, 애플리케이션 전체 혹은 단일 페이지에서 자주 사용하게 될 셀렉터 단축키를 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기

페이지 객체(Page Object)를 생성하려면 `dusk:page` Artisan 명령어를 실행하세요. 모든 페이지 객체는 애플리케이션의 `tests/Browser/Pages` 디렉터리에 생성됩니다.

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정하기

기본적으로 페이지 클래스에는 `url`, `assert`, `elements` 세 가지 메서드가 포함되어 있습니다. 지금은 `url`과 `assert` 메서드에 대해 설명합니다. `elements` 메서드는 아래 [단축 셀렉터(Shorthand Selectors) 항목](#shorthand-selectors)에서 더 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 대표하는 URL 경로를 반환해야 합니다. Dusk는 브라우저에서 해당 페이지로 이동할 때 이 URL을 사용합니다.

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

`assert` 메서드는 브라우저가 실제로 해당 페이지에 있는지 확인하는데 필요한 검증 로직을 작성할 수 있습니다. 이 메서드는 반드시 내용을 작성해야 하는 것은 아니지만, 필요하다면 자유롭게 원하는 검증을 구현할 수 있습니다. 이 검증은 페이지로 이동할 때 자동으로 실행됩니다.

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
### 페이지로 이동하기

페이지가 정의되었다면, `visit` 메서드를 사용해 해당 페이지로 이동할 수 있습니다.

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

때로는 이미 어떤 페이지에 있는 상태에서, 그 페이지의 셀렉터와 메서드만 현재 테스트 컨텍스트로 불러오고 싶을 때가 있습니다. 예를 들어 버튼을 클릭해서 명시적으로 경로 변경 없이 특정 페이지로 리다이렉트될 때 자주 사용됩니다. 이런 경우 `on` 메서드를 사용하여 페이지 정보를 불러올 수 있습니다.

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터(Shorthand Selectors)

페이지 클래스 내부의 `elements` 메서드를 사용하면, 자주 쓰는 CSS 셀렉터에 대해 간편하고 기억하기 쉬운 단축키를 지정할 수 있습니다. 예를 들어, 로그인 페이지의 "email" 입력 필드에 대한 단축 셀렉터를 정의해 보겠습니다.

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

단축 셀렉터가 정의되어 있으면, 일반적인 CSS 셀렉터를 사용할 때와 동일하게, 어떤 메서드에서든 이 단축 셀렉터를 사용할 수 있습니다.

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>

#### 전역 약식 셀렉터(Global Shorthand Selectors)

Dusk를 설치하면, 기본 `Page` 클래스가 `tests/Browser/Pages` 디렉터리에 생성됩니다. 이 클래스에는 `siteElements` 메서드가 포함되어 있는데, 애플리케이션의 모든 페이지에서 공통적으로 사용할 수 있는 전역 약식 셀렉터를 정의하는 데 사용할 수 있습니다.

```php
/**
 * 사이트의 전역 요소 단축키를 반환합니다.
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
### 페이지 메서드

페이지에 기본적으로 정의되어 있는 메서드 외에도, 테스트 전반에서 사용할 수 있는 추가적인 메서드를 직접 정의할 수 있습니다. 예를 들어, 음악 관리 애플리케이션을 만든다고 가정해 봅시다. 특정 페이지에서 자주 수행하는 작업이 플레이리스트 생성이라면, 각 테스트마다 플레이리스트를 생성하는 로직을 반복해서 작성하는 대신, 페이지 클래스에 `createPlaylist` 메서드를 정의할 수 있습니다.

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 다른 페이지 메서드...

    /**
     * 새로운 플레이리스트를 생성합니다.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

이 메서드를 정의한 후에는 해당 페이지를 사용하는 모든 테스트에서 손쉽게 사용할 수 있습니다. 커스텀 페이지 메서드에는 브라우저 인스턴스가 첫 번째 인수로 자동 전달됩니다.

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트(Components)

컴포넌트는 Dusk의 "페이지 객체(page objects)"와 비슷하지만, 내비게이션 바나 알림 창 처럼 애플리케이션 전반에서 여러 번 재사용되는 UI 및 기능 부분을 위해 만들어진다는 점이 다릅니다. 따라서 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기

컴포넌트를 생성하려면 `dusk:component` 아티즌 명령어를 실행합니다. 새로 생성된 컴포넌트는 `tests/Browser/Components` 디렉터리에 저장됩니다.

```shell
php artisan dusk:component DatePicker
```

위와 같이 "날짜 선택기(date picker)"는 여러 페이지에서 반복적으로 사용할 수 있는 컴포넌트의 예입니다. 테스트 코드 곳곳에서 날짜를 선택하는 자동화 로직을 매번 직접 작성하는 일은 번거로울 수 있습니다. 대신 Dusk 컴포넌트를 통해 날짜 선택기를 하나의 클래스로 정의하면, 그 로직을 컴포넌트에 캡슐화할 수 있습니다.

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * 컴포넌트의 루트 셀렉터를 반환합니다.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * 페이지에 해당 컴포넌트가 포함되어 있는지 확인합니다.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트의 요소 단축키를 반환합니다.
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
     * 지정한 날짜를 선택합니다.
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
### 컴포넌트 사용하기

컴포넌트를 정의하였다면, 이제 어떤 테스트에서도 쉽게 날짜 선택기를 통해 날짜를 선택할 수 있습니다. 날짜 선택 로직이 변경되더라도 컴포넌트만 수정하면 되기 때문에 유지보수도 손쉽게 할 수 있습니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

uses(DatabaseMigrations::class);

test('기본 예제', function () {
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
     * 기본 컴포넌트 테스트 예제입니다.
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

`component` 메서드를 사용하면 지정한 컴포넌트 범위에 제한된 브라우저 인스턴스를 가져올 수도 있습니다.

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(Continuous Integration)

> [!WARNING]
> 대부분의 Dusk 지속적 통합(CI) 설정은 라라벨 애플리케이션이 내장 PHP 개발 서버를 사용하여 8000번 포트에서 서비스된다고 가정합니다. 따라서 진행하기 전에, CI 환경에서 `APP_URL` 환경 변수의 값이 `http://127.0.0.1:8000`으로 설정되어 있는지 반드시 확인해야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행하기

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, Heroku `app.json` 파일에 아래와 같이 Google Chrome 빌드팩과 스크립트를 추가해야 합니다.

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
### Travis CI에서 테스트 실행하기

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면, 아래와 같은 `.travis.yml` 설정을 사용할 수 있습니다. Travis CI는 GUI 환경이 아니기 때문에 Chrome 브라우저를 실행하려면 몇 가지 추가 설정이 필요합니다. 또한 PHP의 내장 웹 서버를 구동하기 위해 `php artisan serve`를 사용합니다.

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
### GitHub Actions에서 테스트 실행하기

[GitHub Actions](https://github.com/features/actions)를 이용해 Dusk 테스트를 실행하는 경우, 아래 설정 파일을 참고하여 시작할 수 있습니다. Travis CI와 마찬가지로 `php artisan serve` 명령어를 사용하여 PHP 내장 웹 서버를 실행합니다.

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
### Chipper CI에서 테스트 실행하기

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면, 아래의 설정 파일 예제처럼 시작할 수 있습니다. 라라벨을 구동하기 위해 PHP의 내장 서버를 사용할 것이므로 요청을 수신할 수 있습니다.

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# 빌드 환경에 Chrome 포함
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

      # 새 dusk 환경 파일 생성 및 APP_URL에 BUILD_HOST 적용
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

Chipper CI에서 Dusk 테스트 실행 방법 및 데이터베이스 사용 방법 등 더 자세한 내용은 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하시기 바랍니다.