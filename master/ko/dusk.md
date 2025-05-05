# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성하기](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행하기](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본 사용법](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증(Authentication)](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 로그 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [엘리먼트와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [자바스크립트 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기](#waiting-for-elements)
    - [엘리먼트 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지 객체](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 구성](#configuring-pages)
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

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신 Dusk는 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 물론 원하는 경우 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> 만약 Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, 이를 **프로덕션 환경에서는 절대 등록하지 마십시오.** 등록하면 누구나 애플리케이션에 인증 없이 접근할 수 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` Artisan 명령을 실행합니다. 이 명령은 `tests/Browser` 디렉토리와 예제 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저로 애플리케이션에 접근할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]
> [Laravel Sail](/docs/{{version}}/sail)로 로컬 개발 환경을 관리한다면 [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk) 관련 Sail 문서를 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령으로 설치되는 ChromeDriver가 아닌 다른 버전을 설치하려면, `dusk:chrome-driver` Artisan 명령을 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 운영체제에 특정 버전 설치...
php artisan dusk:chrome-driver --all

# 크롬/크로미엄의 감지된 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리 파일의 실행 권한을 필요로 합니다. 문제가 있다면 다음 명령으로 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)로 브라우저 테스트를 실행합니다. 그러나 직접 Selenium 서버를 실행해서 원하는 브라우저로 테스트를 진행할 수도 있습니다.

`tests/DuskTestCase.php` 파일을 열고, `startChromeDriver` 메소드 호출을 주석 처리합니다. 이로써 Dusk가 ChromeDriver를 자동으로 시작하지 않게 됩니다:

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

이제 `driver` 메서드를 원하는 URL과 포트로 연결하도록 수정하고, WebDriver에 전달할 "desired capabilities"도 바꿀 수 있습니다:

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
### 테스트 생성하기

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령을 사용하세요. 생성된 테스트는 `tests/Browser` 디렉토리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션 DB에서 데이터를 가져오는 페이지와 상호작용할 것입니다. Dusk 테스트에서는 `RefreshDatabase` 트레이트를 **절대** 사용하지 마십시오. 그 이유는 이 트레이트가 HTTP 요청 간에 적용되지 않는 데이터베이스 트랜잭션에 의존하기 때문입니다. 대신 `DatabaseMigrations` 트레이트 또는 `DatabaseTruncation` 트레이트 중 하나를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 모든 테스트마다 테이블을 삭제 및 재생성하는 것은 테이블만 잘라내는(truncate) 것보다 느립니다.

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
> Dusk 테스트 실행 시에는 SQLite 메모리 데이터베이스를 사용할 수 없습니다. 브라우저가 별도의 프로세스로 실행되어, 메모리 DB에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 테이블 Truncation 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 마이그레이션을 실행하여 테이블이 준비되도록 합니다. 이후 테스트에서는 단순히 테이블을 truncate(비우기)하여 마이그레이션을 재실행하지 않아 속도가 향상됩니다.

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 truncate합니다. Truncate할 테이블을 직접 지정하려면, 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

> [!NOTE]
> Pest에서 사용하는 경우, 속성이나 메소드는 base `DuskTestCase` 클래스나 테스트 파일이 상속하는 클래스에 정의하세요.

```php
/**
 * Truncate할 테이블 지정
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

반대로, truncate에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 사용할 수 있습니다:

```php
/**
 * Truncate에서 제외할 테이블 지정
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

Truncate 적용할 데이터베이스 연결명을 지정할 수도 있습니다:

```php
/**
 * 테이블을 truncate할 연결명
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

Truncate 전/후 실행할 코드를 정의하려면 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 사용할 수 있습니다:

```php
/**
 * Truncate 시작 전 실행 코드
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Truncate 완료 후 실행 코드
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행하기

브라우저 테스트를 실행하려면 `dusk` Artisan 명령을 실행하세요:

```shell
php artisan dusk
```

이전 테스트에서 실패한 항목만 먼저 다시 실행하려면 `dusk:fails` 명령을 사용할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령은 Pest / PHPUnit에서 허용되는 모든 인자를 받을 수 있습니다. 예로, 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)의 테스트만 실행:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/{{version}}/sail) 환경에서 사용하는 경우, [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk) 관련 Sail 문서를 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

Dusk는 기본적으로 ChromeDriver를 자동으로 실행합니다. 자동 실행이 제대로 동작하지 않으면, 직접 ChromeDriver를 먼저 실행해야 합니다. 이 경우 `tests/DuskTestCase.php` 파일에서 다음 라인을 주석 처리합니다:

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

만약 9515 외의 포트로 ChromeDriver를 실행한다면, 아래처럼 `driver` 메서드의 포트도 바꿔주십시오:

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

테스트 실행 시 Dusk만의 환경 파일을 사용하게 하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어 `local` 환경에서 `dusk` 명령을 실행하려면 `.env.dusk.local` 파일이 필요합니다.

테스트를 실행하면 Dusk는 기존 `.env` 파일을 백업하고, Dusk 환경 파일을 `.env`로 바꿉니다. 테스트 완료 후에는 원래 `.env`로 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사용법

<a name="creating-browsers"></a>
### 브라우저 생성

로그인 기능이 잘 동작하는지 확인하는 테스트를 만들어 보겠습니다. 테스트를 생성한 후, 로그인 페이지로 이동해 자격 증명을 입력 후 "Login" 버튼을 클릭하도록 수정할 수 있습니다. Dusk 테스트 내에서 `browse` 메서드로 브라우저 인스턴스를 생성하여 사용합니다:

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

위 예제에서 `browse` 메서드는 클로저를 받습니다. Dusk는 클로저에 브라우저 인스턴스를 자동으로 전달하며, 이 인스턴스를 사용해 애플리케이션과 상호작용 및 어설션을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 여러개의 브라우저 생성

두 명 이상의 사용자가 필요한(예: 웹소켓 기반 채팅) 테스트에서는 클로저 인자에 브라우저 인스턴스를 추가해서 동시에 여러 브라우저를 사용할 수 있습니다:

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

`visit` 메서드로 주어진 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[네임드 라우트](/docs/{{version}}/routing#named-routes)로 이동할 때는 `visitRoute` 메서드를 사용할 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

`back` 및 `forward` 메서드로 브라우저 뒤로가기/앞으로가기 이동도 지원합니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드로 페이지 새로고침도 가능합니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메서드로 브라우저 창의 크기를 지정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize`로 브라우저 창을 최대화할 수 있습니다:

```php
$browser->maximize();
```

`fitContent`로 브라우저 창을 콘텐츠 크기에 맞출 수 있습니다:

```php
$browser->fitContent();
```

테스트가 실패할 때 Dusk는 자동으로 컨텐츠에 맞게 창을 조정한 뒤 스크린샷을 찍습니다. 이 기능을 끄려면 `disableFitOnFailure` 메서드를 호출하면 됩니다.

```php
$browser->disableFitOnFailure();
```

`move`로 브라우저 창을 원하는 위치로 이동할 수 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 반복적으로 사용할 브라우저 메소드를 정의하려면, `Browser` 클래스의 `macro` 메서드를 통해 매크로를 등록할 수 있습니다. 일반적으로 이 코드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록합니다:

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

이렇게 등록한 매크로는 브라우저 인스턴스에서 일반 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증(Authentication)

로그인이 필요한 페이지를 매번 브라우저에서 사용자 정보를 입력하지 않고 테스트하려면, Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 모델의 주키 또는 모델 인스턴스를 인자로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드 사용 후에는 파일 내 모든 테스트에서 해당 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드로 암호화된 쿠키의 값을 가져오거나 설정할 수 있습니다. Laravel에서 생성된 쿠키는 기본적으로 암호화됩니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` 메서드로 암호화되지 않은 쿠키의 값을 다룰 수 있습니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie`로 특정 쿠키를 삭제할 수 있습니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행

`script` 메서드로 브라우저 내에서 임의 자바스크립트 문을 실행할 수 있습니다:

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

`screenshot` 메서드로 스크린샷을 찍어 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots`에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드로 다양한 브레이크포인트에서 연속적으로 스크린샷을 얻을 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement`로 특정 엘리먼트만 스크린샷을 찍을 수 있습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 로그 저장

`storeConsoleLog` 메서드로 현재 브라우저의 콘솔 로그를 파일로 저장할 수 있습니다. 콘솔 로그는 `tests/Browser/console` 폴더에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장

`storeSource` 메서드로 현재 페이지의 소스 코드를 파일로 저장할 수 있습니다. `tests/Browser/source` 폴더에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용

<a name="dusk-selectors"></a>
### Dusk 셀렉터

테스트에서 엘리먼트와 상호작용하기 위한 좋은 CSS 셀렉터를 고르는 것은 어렵습니다. 프런트엔드의 변화로 인해 기존 CSS 셀렉터로 테스트가 깨질 수 있습니다. Dusk 셀렉터는 효과적인 테스트 작성에 집중할 수 있도록 도와줍니다. HTML 태그에 `dusk` 속성을 부여하고, 테스트 코드에서는 `@` 접두사를 붙여 사용할 수 있습니다:

```html
<button dusk="login-button">Login</button>
```

```php
$browser->click('@login-button');
```

원한다면 Dusk 셀렉터가 사용할 HTML 속성을 `selectorHtmlAttribute` 메소드로 변경할 수 있습니다. 보통 앱의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기/설정하기

엘리먼트의 값, 표시 텍스트, 속성에 대한 다양한 메서드를 제공합니다. 예를 들어, 셀렉터와 일치하는 엘리먼트의 "value"를 얻으려면:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

특정 input 요소의 값을 얻으려면 `inputValue`를 사용하세요:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드는 셀렉터에 일치하는 엘리먼트의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

`attribute` 메서드는 특정 셀렉터의 엘리먼트에서 속성 값을 조회합니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력하기

폼과 인풋 엘리먼트와 상호작용할 수 있는 다양한 메서드가 있습니다. 예를 들어, input 필드에 값을 입력할 때:

```php
$browser->type('email', 'taylor@laravel.com');
```

`type`은 CSS 셀렉터를 생략할 수 있고, 이 경우 `name` 속성이 일치하는 `input` 또는 `textarea`를 찾습니다. 추가로 `append`로 기존 값을 유지하면서 텍스트를 입력할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

`clear`로 인풋 값을 비울 수도 있습니다:

```php
$browser->clear('email');
```

`typeSlowly`로 키 입력 간 딜레이를 줄 수 있습니다(기본 100ms):

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly`로 천천히 추가 입력도 가능합니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운(Select)

`select`로 select 엘리먼트의 옵션 값을 선택할 수 있습니다. 두 번째 인자가 없으면 랜덤옵션을 선택합니다:

```php
$browser->select('size', 'Large');
$browser->select('size');
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

`check`로 체크박스를 체크, `uncheck`로 체크 해제할 수 있습니다:

```php
$browser->check('terms');
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼 선택은 `radio` 메서드를 사용합니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부

`attach`로 file input 엘리먼트에 파일을 첨부할 수 있습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 첨부 기능은 서버에 PHP `Zip` 확장 모듈이 활성화되어야 사용 가능합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭

`press` 메서드로 버튼을 클릭할 수 있습니다. 인자로 버튼 텍스트나 셀렉터를 사용할 수 있습니다:

```php
$browser->press('Login');
```

폼 제출 후 버튼이 비활성화됐다가 재활성화될 때까지 기다리려면 `pressAndWaitFor`을 사용합니다:

```php
$browser->pressAndWaitFor('Save');
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭

`clickLink`로 특정 텍스트를 가진 링크를 클릭할 수 있습니다:

```php
$browser->clickLink($linkText);
```

`seeLink`로 특정 텍스트를 가진 링크가 페이지에 보이는지도 확인할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드들은 jQuery에 의존합니다. 페이지에 jQuery가 없다면 Dusk가 자동으로 삽입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys` 메서드로 복잡한 키 입력 시퀀스를 제공할 수 있습니다. 예를 들어, modifier 키 조합이나 단축키도 입력 가능합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` 같은 modifier 키들은 `{}`로 감싸서 사용합니다. 이 값은 `Facebook\WebDriver\WebDriverKeys` 클래스 상수와 일치합니다.

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

`withKeyboard` 메서드로 `Laravel\Dusk\Keyboard` 클래스를 통해 플루언트하게 복잡한 키보드 인터랙션을 조합할 수 있습니다:

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

키보드 상호작용도 매크로로 등록해서 사용할 수 있습니다. 주로 [서비스 프로바이더](/docs/{{version}}/providers)에서 등록합니다:

```php
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
```

등록한 매크로는 다음처럼 사용할 수 있습니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 엘리먼트 클릭

`click` 메서드로 셀렉터에 해당하는 엘리먼트를 클릭할 수 있습니다:

```php
$browser->click('.selector');
```

`clickAtXPath`로 XPath 표현식으로도 클릭 가능합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint`로 지정한 좌표값에 위치한 최상단 엘리먼트를 클릭할 수 있습니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

더블클릭, 우클릭, 클릭후 홀드 등 다양한 마우스 액션도 지원합니다:

```php
$browser->doubleClick();
$browser->doubleClick('.selector');
$browser->rightClick();
$browser->rightClick('.selector');
$browser->clickAndHold('.selector');
$browser->clickAndHold()->pause(1000)->releaseMouse();
$browser->controlClick();
$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스오버

`mouseover`로 해당 엘리먼트 위에 마우스를 올릴 수 있습니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag`로 한 엘리먼트를 다른 위치로 드래그할 수 있습니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

방향, 오프셋에 따라 이동도 지원합니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그

JavaScript 다이얼로그와 다양한 상호작용이 가능합니다. 예를 들어, 다이얼로그가 나타날 때까지 기다리거나, 특정 메시지가 포함되어 있는지 어설션할 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
$browser->assertDialogOpened('Dialog message');
$browser->typeInDialog('Hello World');
$browser->acceptDialog();
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용

iframe 내부 엘리먼트와 상호작용하려면 `withinFrame` 메서드를 사용할 수 있습니다:

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

여러 작업을 특정 셀렉터 영역 안에서만 하고 싶다면 `with` 메서드를 사용합니다. 안에서는 그 영역만 범위로 인식합니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

스코프 밖에서 어설션이 필요할 경우 `elsewhere`, `elsewhereWhenAvailable`를 이용하세요:

```php
$browser->with('.table', function (Browser $table) {
    $browser->elsewhere('.page-title', function (Browser $title) {
        $title->assertSee('Hello World');
    });
    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 엘리먼트 대기

JavaScript를 많이 사용하는 앱을 테스트할 때는 특정 엘리먼트나 데이터가 준비될 때까지 기다릴 필요가 있습니다. Dusk는 이런 대기를 쉽게 할 수 있도록 다양한 메서드를 제공합니다.

#### 대기

테스트를 잠시 멈추고 싶으면 `pause`를 쓰세요:

```php
$browser->pause(1000);
```

조건이 참일 때만 대기하려면 `pauseIf`, 아닐 때만 대기하려면 `pauseUnless`를 사용하세요:

```php
$browser->pauseIf(App::environment('production'), 1000);
$browser->pauseUnless(App::environment('testing'), 1000);
```

#### 셀렉터 대기

`waitFor`는 주어진 셀렉터가 나타날 때까지(기본 5초, 타임아웃 지정 가능) 기다립니다:

```php
$browser->waitFor('.selector');
$browser->waitFor('.selector', 1);
```

셀렉터 안에 특정 텍스트가 들어갈 때까지 기다릴 수도 있습니다:

```php
$browser->waitForTextIn('.selector', 'Hello World');
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

셀렉터가 없어질 때까지:

```php
$browser->waitUntilMissing('.selector');
$browser->waitUntilMissing('.selector', 1);
```

활성화/비활성화 등 다양한 조건 대기:

```php
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);
$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

#### 셀렉터 등장 시 범위 지정

특정 셀렉터가 등장하면 내부에서 작업을 실행하려면 `whenAvailable`을 사용합니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

#### 텍스트 대기

`waitForText`로 특정 텍스트가 등장/사라질 때까지 대기할 수 있습니다:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

#### 링크 대기

텍스트가 포함된 링크가 보일 때까지 기다립니다:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

#### 인풋 대기

input 필드가 보일 때까지:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

#### 페이지 위치(주소) 대기

주소가 비동기로 변경될 때 대기할 수 있습니다:

```php
$browser->waitForLocation('/secret');
$browser->waitForLocation('https://example.com/path');
$browser->waitForRoute($routeName, $parameters);
```

#### 페이지 리로드 대기

버튼 등 액션 후 리로드될 때:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');

$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

#### 자바스크립트 식 대기

JS 식이 true가 될 때까지 대기:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

#### Vue 표현식 대기

[Vue 컴포넌트](https://vuejs.org)의 데이터 속성이 특정 값이 될 때까지 대기:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

#### 자바스크립트 이벤트 대기

특정 이벤트가 발생할 때까지 대기:

```php
$browser->waitForEvent('load');
$browser->with('iframe', function (Browser $iframe) {
    $iframe->waitForEvent('load');
});
$browser->waitForEvent('load', '.selector');
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

#### 콜백과 함께 대기

`waitUsing`은 직접 클로저가 true를 반환할 때까지 기다립니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트 스크롤

뷰포트 밖의 엘리먼트도 `scrollIntoView`로 뷰 영역으로 가져와 클릭할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션

Dusk에서는 다양한 어설션 메서드를 제공합니다. 아래 목록을 참고하세요:

<!-- 어설션 목록(생략, 본문 참조. 여기에선 구조 유지만) -->

<a name="pages"></a>
## 페이지 객체

복잡한 일련의 동작이 필요한 테스트의 경우, Page 오브젝트를 통해 테스트 로직을 간결하게 만들 수 있습니다. 페이지 객체에 공통 셀렉터 단축키 및 표현력 있는 동작 메서드를 정의하여 재사용할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

페이지 객체를 만들려면 `dusk:page` Artisan 명령을 실행합니다. 이 객체는 `tests/Browser/Pages`에 저장됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성

기본적으로 페이지에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다.

#### `url` 메서드

이 페이지가 나타내는 URL을 반환합니다:

```php
public function url(): string
{
    return '/login';
}
```

#### `assert` 메서드

브라우저가 올바른 페이지에 있는지 판별하는 어설션입니다. 선택 사항이며, 원하는 경우 작성합니다. 페이지로 이동하면 자동 실행됩니다:

```php
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동

정의된 페이지로는 다음과 같이 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

리다이렉트되어 페이지로 오게 될 경우 `on` 메서드로 페이지의 셀렉터 및 메서드를 현재 컨텍스트로 로드할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터

페이지 클래스의 `elements` 메서드는 CSS 셀렉터의 별칭을 정의할 수 있습니다:

```php
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

이렇게 하면 페이지 코드 내에서 언제든 별칭으로 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

#### 전역 단축 셀렉터

설치 후 `tests/Browser/Pages` 디렉터리 내의 base `Page` 클래스의 `siteElements` 메소드에서 전역 별칭을 정의할 수 있습니다:

```php
public static function siteElements(): array
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### 페이지 메서드

페이지에 커스텀 메서드를 정의해서 다수의 테스트에서 재사용할 수 있습니다. 예를 들어, Playlist 생성 기능 로직을 하나의 메소드로 캡슐화:

```php
public function createPlaylist(Browser $browser, string $name): void
{
    $browser->type('name', $name)
        ->check('share')
        ->press('Create Playlist');
}
```

이제 이 메서드는 해당 페이지 객체를 사용하는 모든 테스트에서 쉽게 호출할 수 있습니다:

```php
$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 페이지 객체와 비슷하지만, 사이트 내 여러 페이지에 반복 사용되는 UI 조각(네비게이션 바, 알림창 등) 용입니다. URL과는 연관 없습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

`dusk:component` Artisan 명령으로 컴포넌트를 생성합니다. 결과는 `tests/Browser/Components` 경로에 저장됩니다:

```shell
php artisan dusk:component DatePicker
```

예시 컴포넌트 (`DatePicker`):

```php
class DatePicker extends BaseComponent
{
    public function selector(): string
    {
        return '.date-picker';
    }

    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    public function elements(): array
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

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
### 컴포넌트 사용

작성된 컴포넌트는 모든 테스트에서 쉽게 재사용할 수 있고, 내부 로직이 변경되더라도 해당 컴포넌트만 수정하면 됩니다:

```php tab=Pest
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
class ExampleTest extends DuskTestCase
{
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
## 지속적 통합(CI)

> [!WARNING]
> 대부분의 Dusk CI 구성은 Laravel 앱이 포트 8000에서 PHP 내장 개발 서버로 서비스되고 있다고 가정합니다. CI 환경의 `APP_URL`을 `http://127.0.0.1:8000`으로 설정하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk를 실행하려면, 다음과 같이 app.json 파일에 Chrome buildpack과 스크립트를 추가하세요:

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

[Travis CI](https://travis-ci.org)에서 테스트하려면 다음 `.travis.yml` 설정을 사용할 수 있습니다:

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

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하려는 경우, 아래 구성 예시를 참고하세요:

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

[Chipper CI](https://chipperci.com)를 사용할 경우, PHP 내장 서버로 요청을 받을 수 있도록 다음 설정 예시를 사용할 수 있습니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

services:
  - dusk

on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate
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

Chipper CI에서 데이터베이스 활용 등 더 자세한 내용은 [공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.