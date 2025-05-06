# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성하기](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행하기](#running-tests)
    - [환경 파일 관리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [이동(네비게이션)](#navigation)
    - [브라우저 창 크기 조정하기](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증 처리](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행하기](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크에 저장하기](#storing-console-output-to-disk)
    - [페이지 소스 디스크에 저장하기](#storing-page-source-to-disk)
- [요소와 상호작용하기](#interacting-with-elements)
    - [Dusk 선택자](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭하기](#clicking-links)
    - [키보드 사용하기](#using-the-keyboard)
    - [마우스 사용하기](#using-the-mouse)
    - [JavaScript 대화상자](#javascript-dialogs)
    - [인라인 프레임과 상호작용하기](#interacting-with-iframes)
    - [선택자 범위 한정(스코핑)](#scoping-selectors)
    - [요소 대기(Waiting)](#waiting-for-elements)
    - [요소를 뷰로 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성하기](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동하기](#navigating-to-pages)
    - [약식 선택자(Shorthand Selectors)](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성하기](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [CI 연동](#continuous-integration)
    - [Heroku CI에서 테스트 실행](#running-tests-on-heroku-ci)
    - [Travis CI에서 테스트 실행](#running-tests-on-travis-ci)
    - [GitHub Actions에서 테스트 실행](#running-tests-on-github-actions)
    - [Chipper CI에서 테스트 실행](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고, 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 JDK나 Selenium을 로컬 컴퓨터에 설치할 필요가 없습니다. 대신 Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 단, 원한다면 원하는 Selenium 호환 드라이버를 사용할 수도 있습니다.

<a name="installation"></a>
## 설치

먼저, [Google Chrome](https://www.google.com/chrome)을 설치하고, 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk 서비스 프로바이더를 수동으로 등록하는 경우, 프로덕션 환경에는 **절대** 등록하지 마십시오. 프로덕션에 등록할 경우 임의의 사용자가 애플리케이션에 로그인할 수 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령은 `tests/Browser` 디렉토리, 예시 테스트, 그리고 운영체제에 맞는 ChromeDriver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 접근하는 애플리케이션의 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경 관리를 [Laravel Sail](/docs/{{version}}/sail)로 하는 경우, [Dusk 테스트 설정 및 실행](/docs/{{version}}/sail#laravel-dusk)에 관한 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령어로 설치되는 기본 ChromeDriver 버전이 아닌 다른 버전을 설치하려면, 아래 명령어를 사용할 수 있습니다:

```shell
# OS에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 지정한 버전 설치...
php artisan dusk:chrome-driver 86

# 모든 지원 OS에 대해 특정 버전 설치...
php artisan dusk:chrome-driver --all

# 설치된 Chrome/Chromium 버전에 맞는 ChromeDriver 자동 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk에서 사용하는 `chromedriver` 바이너리는 실행 가능해야 합니다. 권한 문제로 실행이 안 된다면, 다음 명령어로 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용해 브라우저 테스트를 수행합니다. 하지만, 원한다면 직접 Selenium 서버를 실행하여 원하는 브라우저로 테스트할 수도 있습니다.

`tests/DuskTestCase.php` 파일을 열어, `startChromeDriver` 메서드 호출을 제거합니다. 이렇게 하면 Dusk에서 ChromeDriver를 자동으로 시작하지 않습니다:

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

이후, `driver` 메서드를 수정하여 원하는 URL 및 포트에 연결하고, WebDriver에 전달할 "desired capabilities"도 직접 설정할 수 있습니다:

```php
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
```

<a name="getting-started"></a>
## 시작하기

<a name="generating-tests"></a>
### 테스트 생성하기

Dusk 테스트를 생성하려면, `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉토리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

대부분의 테스트는 데이터베이스와 상호작용하는 페이지를 테스트합니다. 그러나, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. 이 트레이트는 HTTP 요청 간에 적용되지 않는 데이터베이스 트랜잭션을 사용합니다. 대신 `DatabaseMigrations` 트레이트 또는 `DatabaseTruncation` 트레이트 중 하나를 사용하세요.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 전 데이터베이스 마이그레이션을 실행합니다. 하지만, 매번 테이블을 드랍/재생성하는 것은 단순 테이블 초기화보다 느릴 수 있습니다:

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
> SQLite 인메모리 데이터베이스는 Dusk 테스트에서 사용할 수 없습니다. 브라우저가 별도 프로세스에서 동작하므로, 다른 프로세스의 인메모리 DB에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 초기화 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 테이블 생성(migrate)을 수행한 뒤, 각 테스트 후 테이블을 단순히 비웁니다. 이 방식은 마이그레이션 전체를 반복 실행하는 것보다 빠릅니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 초기화합니다. 초기화할 테이블을 커스텀하려면, 테스트 클래스 내 `$tablesToTruncate` 프로퍼티를 정의하세요:

> [!NOTE]
> Pest를 사용할 경우, 프로퍼티나 메서드는 기본 `DuskTestCase` 클래스 또는 테스트 파일에서 확장한 클래스에 정의해야 합니다.

```php
/**
 * 초기화할 테이블 지정.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

혹은 `$exceptTables` 프로퍼티로 초기화에서 제외할 테이블을 명시할 수도 있습니다:

```php
/**
 * 초기화에서 제외할 테이블 지정.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

초기화할 데이터베이스 연결명을 지정하려면, `$connectionsToTruncate` 프로퍼티를 정의하세요:

```php
/**
 * 초기화할 연결명 지정.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

초기화 전/후에 실행할 코드를 정의하려면, `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 사용하세요:

```php
/**
 * DB 초기화 전 추가 작업.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * DB 초기화 후 추가 작업.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행하기

브라우저 테스트를 실행하려면 아래 명령어를 사용하세요:

```shell
php artisan dusk
```

마지막으로 실패한 테스트만 빠르게 재실행하려면 `dusk:fails` 명령어를 사용하세요:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit에서 사용하는 인자도 그대로 쓸 수 있습니다. 예를 들어, [group](https://docs.phpunit.de/en/10.5/annotations.html#group)별로 실행 가능합니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/{{version}}/sail)로 개발 환경을 관리 중이라면, [Dusk 테스트 환경 설정](/docs/{{version}}/sail#laravel-dusk)도 꼭 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 만약 시스템에서 자동 실행이 되지 않는다면, 테스트 명령 실행 전 수동으로 ChromeDriver를 실행해야 합니다. 이때는 `tests/DuskTestCase.php` 파일에서 다음 코드를 주석 처리하세요:

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

ChromeDriver를 9515 포트 외 다른 포트에서 실행했다면, 동일 클래스의 `driver` 메서드도 해당 포트에 맞게 수정하세요:

```php
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
```

<a name="environment-handling"></a>
### 환경 파일 관리

Dusk 실행 시 별도의 환경 파일을 강제로 사용하려면, 프로젝트 루트에 `.env.dusk.{환경}` 파일을 만드세요. 예를 들어, `local` 환경에서 명령을 시작할 경우 `.env.dusk.local` 파일을 생성합니다.

테스트 실행 시 Dusk는 현재 `.env`를 백업하고, Dusk용 환경 파일을 `.env`로 복사 및 이름을 바꿉니다. 테스트 완료 후 원래 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본

<a name="creating-browsers"></a>
### 브라우저 생성하기

애플리케이션 로그인이 가능한지 확인하는 간단한 테스트 예시를 만들어봅시다. 테스트를 생성한 뒤, 로그인 페이지로 이동해 자격 증명을 입력하고 "Login" 버튼을 누르도록 수정합니다. Dusk 테스트 내에서 `browse` 메서드로 브라우저 인스턴스를 사용할 수 있습니다:

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
     * 브라우저 테스트 예시
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

위 예시처럼, `browse` 메서드는 클로저를 인자로 받으며 브라우저 인스턴스가 자동 전달됩니다. 이 인스턴스를 사용해 애플리케이션과 상호작용하거나 어설션을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 멀티 브라우저 인스턴스 생성

여러 브라우저가 필요한 테스트(예: 웹소켓으로 채팅 화면 동시 테스트)에서는, 클로저에 인자를 추가하여 여러 브라우저 인스턴스를 만들 수 있습니다:

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
### 이동(네비게이션)

`visit` 메서드로 지정한 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[named route](/docs/{{version}}/routing#named-routes)로 이동하려면 `visitRoute`를 사용하세요:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`, `forward` 메서드로 앞/뒤 페이지로 이동할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh`로 현재 페이지를 새로고침합니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정하기

`resize` 메서드로 브라우저 창 크기를 변경할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드로 창 전체화면을 만들 수 있습니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창을 컨텐츠 크기에 맞춥니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 스크린샷 전에 fitContent를 실행합니다. 이 기능을 끄려면 `disableFitOnFailure`를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move`로 브라우저 창 위치를 이동할 수 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면, `Browser` 클래스의 `macro` 메서드를 사용합니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 설정합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * 브라우저 매크로 등록.
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

`macro`는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받습니다. 정의된 이름으로 브라우저 인스턴스에서 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 처리

로그인이 필요한 테스트에서는 매번 로그인 화면을 거칠 필요 없이 Dusk의 `loginAs` 메서드를 활용할 수 있습니다. 이 메서드는 인증 가능한 모델의 PK 혹은 인스턴스를 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 사용 후, 해당 파일 내의 모든 테스트는 같은 사용자 세션을 유지합니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드로 암호화된 쿠키의 값을 읽거나 설정할 수 있습니다. Laravel에서 생성하는 쿠키는 기본적으로 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` 메서드는 암호화되지 않은 쿠키의 값을 읽거나 설정합니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie`로 지정한 쿠키를 삭제합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행하기

`script` 메서드로 임의의 JavaScript 코드를 실행할 수 있습니다:

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

`screenshot` 메서드로 스크린샷을 찍어 지정한 파일명으로 저장합니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots`로 다양한 브레이크포인트에서 시리즈 스크린샷을 찍을 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement`는 특정 요소만 스크린샷으로 저장할 수 있습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 디스크에 저장하기

`storeConsoleLog` 메서드로 현재 브라우저의 콘솔 출력을 파일로 저장합니다. 위치는 `tests/Browser/console`입니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크에 저장하기

`storeSource` 메서드로 현재 페이지의 소스코드를 지정 파일명으로 저장합니다. 위치는 `tests/Browser/source`입니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기

<a name="dusk-selectors"></a>
### Dusk 선택자

효과적인 Dusk 테스트 작성을 위해 견고한 CSS 선택자를 정하는 것은 중요한 부분입니다. 프론트엔드 구조 변경에 따라 다음과 같은 CSS 선택자는 자주 깨질 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// 테스트...

$browser->click('.login-page .container div > button');
```

Dusk 선택자를 활용하면 CSS 선택자를 기억하지 않고도 효과적으로 테스트를 작성할 수 있습니다. HTML 요소에 `dusk` 속성을 추가하고, 테스트 내에서는 선택자 앞에 `@`를 붙여 해당 요소를 조작합니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// 테스트...

$browser->click('@login-button');
```

필요하다면 Dusk가 사용하는 HTML 속성명을 `selectorHtmlAttribute`로 커스텀할 수 있습니다. 보통 앱의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기

Dusk는 페이지 내 요소의 현재 값, 표시 텍스트, 속성 등을 상호작용하는 여러 메서드를 제공합니다. 예를 들어, 특정 CSS 또는 Dusk 선택자에 해당하는 요소의 값을 가져오려면 `value` 메서드를 사용합니다:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue`로 주어진 필드명에 해당하는 input 요소 값을 가져올 수 있습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 추출

`text` 메서드는 선택자에 해당하는 요소의 표시 텍스트를 반환합니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성값 추출

`attribute` 메서드는 선택자에 해당하는 요소의 특정 속성 값을 가져옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력하기 (typing)

입력 필드에 텍스트를 입력하려면:

```php
$browser->type('email', 'taylor@laravel.com');
```

선택자를 생략하면 Dusk가 해당 name 속성의 input이나 textarea를 자동으로 찾습니다.

내용을 지우지 않고 텍스트를 덧붙이고 싶으면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력값을 초기화하려면 `clear`를 사용:

```php
$browser->clear('email');
```

`typeSlowly`로 입력 속도를 조절할 수 있습니다(기본 100ms, 커스텀 가능):

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');
$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly`로 텍스트를 천천히 덧붙이기도 지원합니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 메서드는 select 요소의 옵션을 선택할 때 씁니다. 인자로 display text가 아닌 실제 option value를 사용해야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인자를 생략하면 랜덤 옵션이 선택됩니다:

```php
$browser->select('size');
```

배열을 넘기면 다중 옵션 선택 지원:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스에 체크/해제를 하려면 각각 `check`, `uncheck` 메서드를 사용합니다. name 속성으로 자동 검색됩니다:

```php
$browser->check('terms');
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼의 값을 고르려면:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부

`attach` 메서드로 파일 업로드를 처리할 수 있습니다. name 속성으로 자동 검색됩니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능은 서버에 PHP `Zip` 확장 모듈이 설치되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기

`press`는 버튼 요소를 클릭하도록 도와줍니다. display text 또는 selector가 가능합니다:

```php
$browser->press('Login');
```

폼 전송 시 버튼이 비활성화되었다가 다시 활성화될 때까지 기다려야 한다면 `pressAndWaitFor`를 사용하세요:

```php
$browser->pressAndWaitFor('Save');
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기

`clickLink` 메서드는 지정한 텍스트를 가진 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

`seeLink`로 해당 텍스트의 링크가 표시 중인지 확인할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드는 jQuery 의존성이 있습니다. 페이지에 jQuery가 없으면 Dusk가 자동으로 inject 합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기

`keys` 메서드는 Shift 등 복합키를 조합한 복잡한 입력 시퀀스를 지원합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> 모든 modifier 키는 `{}`로 감싸며, `Facebook\WebDriver\WebDriverKeys` 상수와 일치합니다. [GitHub 소스 참고](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="fluent-keyboard-interactions"></a>
#### 유창한 키보드 상호작용

Dusk는 `withKeyboard`로 `Laravel\Dusk\Keyboard` 클래스를 활용해 press/release/type/pause 등 복잡한 상호작용을 할 수 있습니다:

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

키보드 상호작용을 매크로로 정의해 반복 사용하려면 다음과 같이 작성할 수 있습니다:

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

정의된 매크로는 다음과 같이 쓸 수 있습니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용하기

<a name="clicking-on-elements"></a>
#### 요소 클릭

CSS/Dusk 선택자에 해당하는 요소를 클릭:

```php
$browser->click('.selector');
```

XPath로 클릭:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

좌표 기반 클릭:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

더블 클릭:

```php
$browser->doubleClick();
$browser->doubleClick('.selector');
```

우클릭:

```php
$browser->rightClick();
$browser->rightClick('.selector');
```

마우스 클릭 & 홀드, 이후 release:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

Ctrl+클릭 이벤트:

```php
$browser->controlClick();
$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

마우스를 요소 위로 이동:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 & 드롭

한 요소를 다른 요소로 드래그:

```php
$browser->drag('.from-selector', '.to-selector');
```

한 방향으로 지정 픽셀만큼 드래그:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 드래그:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 대화상자

`waitForDialog`로 대화상자가 나타날 때까지 대기:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`로 메시지가 포함된 대화상자가 표시됐는지 확인:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 있는 경우 입력값 전송:

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼 클릭(닫기):

```php
$browser->acceptDialog();
```

"취소" 버튼 클릭(닫기):

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용

iframe 내부 요소에 상호작용하려면 `withinFrame`을 사용하세요. 클로저 내 동작이 지정한 iframe 컨텍스트 내에서 동작합니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 선택자 범위 한정 (스코핑)

특정 selector 범위 내에서 여러 작업을 묶어 하고 싶으면 `with`를 사용하세요:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

스코프 외에서 어설션 등 수행이 필요하다면, `elsewhere`, `elsewhereWhenAvailable`를 사용할 수 있습니다:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 스코프: `body .table`

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 스코프: `body .page-title`
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 스코프: `body .page-title`
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기(Waiting)

JavaScript를 많이 사용하는 앱은 테스트 시 특정 데이터나 요소가 로딩될 때까지 대기해야 할 수 있습니다. Dusk는 다양한 대기 메서드를 제공합니다.

<a name="waiting"></a>
#### 일반 대기

지정 시간(ms)만큼 대기:

```php
$browser->pause(1000);
```

특정 조건이 true일 때만 대기:

```php
$browser->pauseIf(App::environment('production'), 1000);
```

조건이 true가 아닐 때만 대기:

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 선택자 대기

CSS/Dusk 선택자에 해당하는 요소가 표시될 때까지 최대 5초 대기(기본값). 두 번째 인자 사용시 커스텀 대기(초 단위):

```php
$browser->waitFor('.selector');
$browser->waitFor('.selector', 1);
```

요소가 특정 텍스트를 가질 때까지 대기:

```php
$browser->waitForTextIn('.selector', 'Hello World');
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

선택자가 사라질 때까지 대기:

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
#### 선택자 등장 시 스코핑

선택자가 등장하면 그 안에서 추가 작업을 하려면 `whenAvailable`을 사용하세요:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

특정 텍스트가 페이지에 보일 때까지 대기:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

텍스트가 사라질 때까지 대기:

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

특정 링크 텍스트가 페이지에 나타날 때까지 대기:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

input 필드가 나타날 때까지 대기:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 주소(location) 대기

예: 경로 어설션과 window.location.pathname 비동기 업데이트 충돌 방지

```php
$browser->waitForLocation('/secret');
$browser->waitForLocation('https://example.com/path');
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기

액션 후 페이지 리로드가 필요하면 `waitForReload` 또는 `clickAndWaitForReload` 사용:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기

지정 JS 표현식이 true가 될 때까지 대기:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

[Vue 컴포넌트](https://vuejs.org) 속성이 특정 값이 될 때 대기:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기

JS 이벤트가 발생할 때까지 대기:

```php
$browser->waitForEvent('load');
```

스코프 지정:

```php
$browser->with('iframe', function (Browser $iframe) {
    $iframe->waitForEvent('load');
});
```

특정 요소에 대해 이벤트 리스너:

```php
$browser->waitForEvent('load', '.selector');
```

document/window에 대해서도 사용 가능:

```php
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 기반 대기

Dusk 대부분의 대기 메서드는 `waitUsing`에 기반합니다. 최대 대기 시간, 호출 간격, 콜백, 실패 메시지 순으로 인자를 넘깁니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 뷰로 스크롤하기

뷰에 보이지 않는 위치의 요소를 클릭하기 위해선 `scrollIntoView`를 사용해 뷰로 스크롤한 후 클릭할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션

Dusk에서 사용할 수 있는 다양한 어설션 메서드는 아래와 같습니다:

<!-- HTML과 스타일, 링크 URL 번역하지 않음 -->
<!-- (아래 내용은 지침에 의해 번역하지 않음) -->

<a name="pages"></a>
## 페이지

테스트에서 복잡한 액션이 연속적으로 이어질 경우 가독성이 떨어집니다. Dusk 페이지 오브젝트를 활용하면 여러 액션을 하나의 expressive한 메서드로 묶어 쓸 수 있고, 애플리케이션 혹은 개별 페이지 공통 selector에 대한 약어도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기

`dusk:page` Artisan 명령어로 페이지 오브젝트를 생성할 수 있습니다. 생성된 파일은 `tests/Browser/Pages`에 저장됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정

기본적으로 페이지에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 여기선 `url`, `assert`를 설명합니다. `elements`는 [아래에서 설명](#shorthand-selectors)합니다.

<a name="the-url-method"></a>
#### `url` 메서드

페이지를 나타내는 URL 경로를 반환해야 합니다. Dusk가 해당 페이지로 이동시 이 값을 사용합니다:

```php
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

실제로 브라우저가 해당 페이지에 있는지 확인(어설션)을 넣을 수 있습니다. 생략 가능하지만, 넣으면 페이지 이동시 자동으로 실행됩니다:

```php
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동하기

정의한 페이지로 이동하려면 `visit` 사용:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 있고 Selector와 메서드만 현재 컨텍스트에 로드하고 싶을 때는 `on`을 호출하세요:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 약식 선택자(Shorthand Selectors)

페이지 클래스의 `elements` 메서드에 자주 쓰는 CSS selector에 대해 약어를 정의할 수 있습니다:

```php
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

정의된 약어는 CSS selector 대신 쓸 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 글로벌 약식 선택자

Dusk 설치 후 `tests/Browser/Pages`에 생성되는 기본 Page 클래스에는 `siteElements` 메서드로 모든 페이지에서 공통 사용할 약식을 지정할 수 있습니다:

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

페이지 클래스에 메서드를 추가 정의해서 아무 곳에서나 쓸 수도 있습니다. 예를 들어, 플레이리스트 생성 로직을 별도 메서드로 정의한 뒤 아래처럼 사용할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

이렇게 정의된 메서드는 다음처럼 사용할 수 있습니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트

컴포넌트란 네비게이션 바, 알림 등 사이트 전체에서 재사용되는 UI와 기능 조각에 대해 Dusk의 “페이지 오브젝트”와 유사하게 사용할 수 있게 만든 것입니다. 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기

`dusk:component` 명령어로 컴포넌트를 만들면, 새 파일이 `tests/Browser/Components`에 생성됩니다:

```shell
php artisan dusk:component DatePicker
```

예시처럼 "date picker"는 여러 페이지에서 반복 사용할 수 있는 컴포넌트입니다. 반복되는 브라우저 조작 코드를 컴포넌트로 모아두면, 이후 바뀌는 로직에 대한 유지보수도 쉬워집니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

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
### 컴포넌트 사용하기

컴포넌트를 정의한 뒤에는, 어떤 테스트에서나 손쉽게 사용할 수 있습니다. 내부 로직이 변경돼도 각 테스트는 수정 없어도 됩니다:

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
## CI 연동

> [!WARNING]
> 대부분의 Dusk CI 설정은 Laravel 앱을 내장 PHP 서버(8000번 포트)에서 서비스하길 기대합니다. 따라서, CI 환경에서 반드시 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`으로 설정되어있는지 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, 아래 Google Chrome buildpack 및 스크립트를 `app.json`에 추가하세요:

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
### Travis CI에서 테스트 실행

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면, 아래 `.travis.yml` 구성을 사용하세요. Travis CI는 GUI 환경이 아니므로 Chrome 브라우저 구동을 위한 추가 작업이 필요합니다:

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
### GitHub Actions에서 테스트 실행

[GitHub Actions](https://github.com/features/actions)로 Dusk 테스트 실행 시 아래와 같은 기본 config를 활용할 수 있습니다:

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
### Chipper CI에서 테스트 실행

[Chipper CI](https://chipperci.com)로 Dusk 테스트를 실행하려면 아래와 같은 config 파일을 참고하세요. PHP 내장서버로 Laravel을 실행하게 됩니다:

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

Chipper CI 환경에서 Dusk 테스트 실행과 DB 연동 등 자세한 내용은 [공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.