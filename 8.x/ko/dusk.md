# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리하기](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성하기](#generating-tests)
    - [데이터베이스 마이그레이션](#migrations)
    - [테스트 실행하기](#running-tests)
    - [환경 설정 처리](#environment-handling)
- [브라우저 기초](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [탐색](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행하기](#executing-javascript)
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
    - [JavaScript 대화상자 다루기](#javascript-dialogs)
    - [셀렉터 범위 지정하기](#scoping-selectors)
    - [요소 대기하기](#waiting-for-elements)
    - [요소 스크롤하여 보기](#scrolling-an-element-into-view)
- [사용 가능한 Assertions](#available-assertions)
- [페이지](#pages)
    - [페이지 생성하기](#generating-pages)
    - [페이지 설정하기](#configuring-pages)
    - [페이지로 이동하기](#navigating-to-pages)
    - [단축 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성하기](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [지속적 통합](#continuous-integration)
    - [Heroku CI에서 테스트 실행](#running-tests-on-heroku-ci)
    - [Travis CI에서 테스트 실행](#running-tests-on-travis-ci)
    - [GitHub Actions에서 테스트 실행](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 JDK나 Selenium을 로컬 컴퓨터에 설치할 필요가 없습니다. 대신 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 물론, 원한다면 다른 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

사용을 시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```
composer require --dev laravel/dusk
```

> [!NOTE]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대** 프로덕션 환경에 등록하지 마세요. 프로덕션 환경에서 등록하면 임의의 사용자가 애플리케이션에 인증할 수 있는 위험이 있습니다.

Dusk 패키지를 설치한 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령은 `tests/Browser` 디렉토리와 예제 Dusk 테스트 파일을 생성합니다:

```
php artisan dusk:install
```

다음으로, 애플리케이션 `.env` 파일에서 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근하는 URL과 일치해야 합니다.

> [!TIP]
> [Laravel Sail](/docs/{{version}}/sail)로 로컬 개발 환경을 관리하는 경우, Sail 문서의 [Dusk 테스트 설정 및 실행](#laravel-dusk)도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리하기 (Managing ChromeDriver Installations)

Laravel Dusk에 포함된 버전과 다른 ChromeDriver를 설치하려면 `dusk:chrome-driver` 명령을 사용할 수 있습니다:

```
# OS에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원하는 모든 OS용 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# OS의 Chrome / Chromium 버전과 일치하는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!NOTE]
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행 문제 발생 시, 다음 명령어로 바이너리 실행 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용하여 브라우저 테스트를 실행합니다. 하지만 Selenium 서버를 직접 시작하고 원하는 브라우저에서 테스트를 실행할 수 있습니다.

먼저 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 열고, `startChromeDriver` 호출을 주석 처리하여 Dusk가 ChromeDriver를 자동 시작하지 않도록 하세요:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

그 다음, `driver` 메서드를 수정하여 원하는 URL과 포트로 연결하도록 조정할 수 있습니다. 또한 WebDriver에 전달할 "desired capabilities"도 변경할 수 있습니다:

```php
/**
 * Create the RemoteWebDriver instance.
 *
 * @return \Facebook\WebDriver\Remote\RemoteWebDriver
 */
protected function driver()
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

```
php artisan dusk:make LoginTest
```

<a name="migrations"></a>
### 데이터베이스 마이그레이션 (Database Migrations)

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 조회하는 페이지와 상호작용합니다. 하지만 Dusk 테스트에서는 `RefreshDatabase` trait를 사용하면 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 사용하며, 이는 HTTP 요청 간 사용 불가능합니다. 대신 `DatabaseMigrations` trait를 사용해 각 테스트마다 데이터베이스를 다시 마이그레이션하세요:

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

> [!NOTE]
> Dusk 테스트 실행 시 SQLite 인메모리 데이터베이스는 사용 불가합니다. 브라우저가 별도 프로세스에서 실행되므로 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="running-tests"></a>
### 테스트 실행하기 (Running Tests)

브라우저 테스트를 실행하려면 `dusk` Artisan 명령을 사용하세요:

```
php artisan dusk
```

이전에 테스트 실패가 있었다면, 실패했던 테스트만 먼저 실행해 시간 절약을 할 수 있습니다. `dusk:fails` 명령을 사용하세요:

```
php artisan dusk:fails
```

`dusk` 명령어는 PHPUnit 테스트 실행기에서 지원하는 모든 인수를 전달할 수 있습니다. 예를 들어 특정 [그룹](https://phpunit.de/manual/current/en/appendixes.annotations.html#appendixes.annotations.group) 테스트만 실행하려면:

```
php artisan dusk --group=foo
```

> [!TIP]
> [Laravel Sail](/docs/{{version}}/sail) 사용 시, Sail 문서의 [Dusk 테스트 설정 및 실행](#laravel-dusk) 부분을 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작하기 (Manually Starting ChromeDriver)

기본적으로 Dusk는 ChromeDriver를 자동 시작합니다. 만약 시스템에서 자동 시작이 잘 안 되는 경우, `dusk` 명령 실행 전에 ChromeDriver를 수동으로 시작할 수 있습니다. 이 경우 `tests/DuskTestCase.php` 파일에서 다음 줄을 주석 처리해야 합니다:

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

또한, ChromeDriver를 기본 포트(9515) 이외에서 시작했다면, 같은 클래스의 `driver` 메서드에서 포트 번호를 수정하세요:

```php
/**
 * Create the RemoteWebDriver instance.
 *
 * @return \Facebook\WebDriver\Remote\RemoteWebDriver
 */
protected function driver()
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### 환경 설정 처리 (Environment Handling)

테스트 실행 시 Dusk가 자체 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어 `local` 환경에서 `dusk` 명령을 실행한다면 `.env.dusk.local` 파일을 생성합니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고 이 파일을 `.env`로 교체해 사용합니다. 테스트 완료 후에는 원래 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기초 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성하기 (Creating Browsers)

시작하기 위해, 애플리케이션에 로그인을 할 수 있는지 검사하는 테스트를 작성해 보겠습니다. 테스트를 생성한 후 로그인 페이지로 이동하여 자격 증명을 입력하고 "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 호출하여 생성할 수 있습니다:

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

    /**
     * 기본 브라우저 테스트 예제.
     *
     * @return void
     */
    public function test_basic_example()
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function ($browser) use ($user) {
            $browser->visit('/login')
                    ->type('email', $user->email)
                    ->type('password', 'password')
                    ->press('Login')
                    ->assertPathIs('/home');
        });
    }
}
```

위 예제에서 볼 수 있듯, `browse` 메서드는 클로저를 인자로 받습니다. Dusk가 자동으로 브라우저 인스턴스를 클로저에 전달하며, 이 인스턴스를 통해 애플리케이션과 상호작용하고 어설션을 수행합니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성하기

때때로 여러 브라우저 인스턴스가 필요할 때가 있습니다. 예를 들어 WebSocket과 상호작용하는 채팅 화면 테스트 같은 경우입니다. 여러 브라우저가 필요하다면, `browse` 메서드에 전달하는 클로저의 인자 목록에 브라우저 인스턴스를 추가하면 됩니다:

```php
$this->browse(function ($first, $second) {
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
### 탐색 (Navigation)

`visit` 메서드를 사용하여 애플리케이션 내 특정 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

`visitRoute` 메서드는 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes)로 이동할 때 사용할 수 있습니다:

```php
$browser->visitRoute('login');
```

`back` 및 `forward` 메서드는 브라우저 "뒤로가기"와 "앞으로가기" 탐색을 수행합니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드는 현재 페이지를 새로 고칩니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드를 사용하여 브라우저 창 크기를 지정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창 크기를 콘텐츠 크기에 맞게 조정합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 창 크기를 콘텐츠에 맞추어 스크린샷을 찍습니다. 이 기능을 비활성화하려면, 테스트 내에서 `disableFitOnFailure` 메서드를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드는 브라우저 창을 화면 내 다른 위치로 이동합니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 수 있는 맞춤 브라우저 메서드를 정의하고 싶다면 `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Dusk 브라우저 매크로 등록.
     *
     * @return void
     */
    public function boot()
    {
        Browser::macro('scrollToElement', function ($element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

`macro` 함수는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받습니다. 매크로 클로저는 `Browser` 인스턴스에서 매크로를 메서드처럼 호출할 때 실행됩니다:

```php
$this->browse(function ($browser) use ($user) {
    $browser->visit('/pay')
            ->scrollToElement('#credit-card-details')
            ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

종종 인증이 필요한 페이지를 테스트할 때가 있습니다. 매 테스트마다 로그인 화면을 거치지 않도록, Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델 인스턴스나 해당 모델의 기본 키를 받습니다:

```php
use App\Models\User;

$this->browse(function ($browser) {
    $browser->loginAs(User::find(1))
          ->visit('/home');
});
```

> [!NOTE]
> `loginAs` 메서드를 사용하면, 사용자의 세션은 해당 파일 내의 모든 테스트 동안 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드를 사용하여 암호화된 쿠키 값을 읽거나 설정할 수 있습니다. 기본적으로 Laravel에서 생성된 모든 쿠키는 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값을 다룰 땐 `plainCookie` 메서드를 사용하세요:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

특정 쿠키를 삭제하려면 `deleteCookie` 메서드를 사용합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행하기 (Executing JavaScript)

`script` 메서드를 사용하여 브라우저 내부에서 임의의 JavaScript 코드를 실행할 수 있습니다:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기 (Taking A Screenshot)

`screenshot` 메서드를 사용해 스크린샷을 찍고, 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장하기 (Storing Console Output To Disk)

`storeConsoleLog` 메서드를 사용하면 현재 브라우저의 콘솔 출력을 파일로 저장할 수 있습니다. 콘솔 로그는 `tests/Browser/console` 디렉토리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장하기 (Storing Page Source To Disk)

`storeSource` 메서드를 사용하여 현재 페이지 소스를 파일로 저장할 수 있습니다. 저장된 페이지 소스는 `tests/Browser/source` 디렉토리에 위치합니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

적절한 CSS 셀렉터를 선택하는 것은 Dusk 테스트 작성 시 가장 어려운 부분 중 하나입니다. 시간이 지나면서 프론트엔드가 변경되면 아래와 같은 CSS 셀렉터가 테스트를 깨뜨릴 수 있습니다:

```html
// HTML...

<button>Login</button>

// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터를 기억하는 대신 효과적인 테스트 작성에 집중할 수 있습니다. 셀렉터를 정의하려면 HTML 요소에 `dusk` 속성을 추가하세요. 그런 다음 Dusk 브라우저에서 `@` 접두사를 붙여 해당 요소를 조작할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>

// Test...

$browser->click('@login-button');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, & Attributes)

<a name="retrieving-setting-values"></a>
#### 값 읽기 및 설정하기 (Retrieving & Setting Values)

Dusk는 페이지 내 요소의 현재 값, 표시 텍스트, 속성에 접근할 수 있는 다양한 메서드를 제공합니다. 예를 들어, 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소의 "value"를 가져오려면 `value` 메서드를 사용합니다:

```php
// 값 읽기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 특정 필드 이름을 가진 입력 요소의 값을 가져옵니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 읽기 (Retrieving Text)

`text` 메서드는 특정 셀렉터와 일치하는 요소의 표시 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 읽기 (Retrieving Attributes)

`attribute` 메서드는 특정 셀렉터와 일치하는 요소의 지정된 속성 값을 가져옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기 (Typing Values)

Dusk는 다양한 폼 및 입력 요소와 상호작용할 수 있는 여러 메서드를 제공합니다. 먼저, 입력 필드에 텍스트를 입력하는 예제를 살펴보겠습니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

`type` 메서드는 CSS 셀렉터를 전달할 필요 없이, 입력 필드나 텍스트 영역의 `name` 속성을 기준으로 필드를 찾아 자동으로 값을 입력합니다.

내용을 지우지 않고 텍스트를 덧붙이고 싶다면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
        ->append('tags', ', bar, baz');
```

입력 값을 지우려면 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

느리게 타이핑하고 싶다면 `typeSlowly` 메서드를 사용하세요. 기본적으로 키 입력 사이에 100밀리초 일시 정지합니다. 세 번째 인수에 밀리초 값을 전달해 간격을 조정할 수 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

느리게 텍스트를 덧붙이려면 `appendSlowly` 메서드를 사용합니다:

```php
$browser->type('tags', 'foo')
        ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운 (Dropdowns)

`select` 메서드를 이용해 `select` 요소에서 값을 선택할 수 있습니다. `type` 메서드와 같이 전체 CSS 셀렉터를 지정할 필요는 없습니다. `select` 메서드의 인자로는 옵션의 표시 텍스트가 아니라 실제 값(value)을 전달해야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인자를 생략하면 옵션 중 하나가 무작위로 선택됩니다:

```php
$browser->select('size');
```

두 번째 인자로 배열을 전달하면 여러 옵션을 선택할 수 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스 (Checkboxes)

체크박스 입력 요소를 체크하려면 `check` 메서드를 사용합니다. 전체 CSS 셀렉터가 없는 경우, `name` 속성으로 체크박스를 찾습니다:

```php
$browser->check('terms');
```

체크를 해제하려면 `uncheck` 메서드를 사용하세요:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼 (Radio Buttons)

라디오 버튼을 선택하려면 `radio` 메서드를 사용합니다. 전체 CSS 셀렉터가 없으면 `name`과 `value` 속성으로 라디오 버튼을 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기 (Attaching Files)

`attach` 메서드를 사용해 `file` 입력 요소에 파일을 첨부할 수 있습니다. 전체 CSS 셀렉터가 없으면 `name` 속성으로 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!NOTE]
> `attach` 함수는 PHP의 `Zip` 확장 모듈 설치 및 활성화가 필요합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드를 사용해 페이지 내 버튼 요소를 클릭할 수 있습니다. 첫 번째 인자는 버튼에 표시된 텍스트나 CSS / Dusk 셀렉터가 될 수 있습니다:

```php
$browser->press('Login');
```

많은 애플리케이션에서는 폼 제출 버튼을 누른 후 버튼을 비활성화하고, HTTP 요청이 완료되면 다시 활성화합니다. 버튼을 누른 후 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용하세요:

```php
// 최대 5초간 버튼이 활성화될 때까지 기다리기...
$browser->pressAndWaitFor('Save');

// 최대 1초간 기다리기...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기 (Clicking Links)

링크를 클릭할 때는 브라우저 인스턴스의 `clickLink` 메서드를 사용합니다. 지정한 표시 텍스트를 가진 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

페이지에 특정 표시 텍스트의 링크가 있는지 확인하려면 `seeLink` 메서드를 사용하세요:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!NOTE]
> 이들 메서드는 jQuery와 상호작용합니다. 만약 페이지에 jQuery가 없으면 Dusk가 테스트 기간 동안 자동으로 jQuery를 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기 (Using The Keyboard)

`keys` 메서드는 `type` 메서드보다 더 복잡한 키 입력 시퀀스를 특정 요소에 보낼 수 있습니다. 예를 들어, `shift` 키를 누른 상태에서 문자열을 입력하고 그 후 다시 일반 모드로 타이핑할 수 있습니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또한, 특정 CSS 셀렉터에 "키보드 단축키" 조합을 보낼 수 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!TIP]
> `{command}` 등 모든 수정키는 중괄호 `{}`로 감싸져 있으며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스 상수와 일치합니다. [GitHub에서 확인할 수 있습니다](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="using-the-mouse"></a>
### 마우스 사용하기 (Using The Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭하기 (Clicking On Elements)

`click` 메서드로 특정 CSS 또는 Dusk 셀렉터와 일치하는 요소를 클릭할 수 있습니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 XPath 표현식에 맞는 요소를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저 화면 내 특정 좌표에 있는 최상단 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 마우스 더블 클릭을 시뮬레이션합니다:

```php
$browser->doubleClick();
```

`rightClick` 메서드는 마우스 우클릭을 시뮬레이션합니다:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드는 마우스 버튼을 클릭한 상태로 누른 상태를 시뮬레이션합니다. 이어서 `releaseMouse` 메서드로 누른 상태를 해제합니다:

```php
$browser->clickAndHold()
        ->pause(1000)
        ->releaseMouse();
```

<a name="mouseover"></a>
#### 마우스 오버 (Mouseover)

`mouseover` 메서드는 마우스를 특정 CSS 또는 Dusk 셀렉터 요소 위로 이동할 때 사용합니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 & 드롭 (Drag & Drop)

`drag` 메서드는 특정 셀렉터 요소를 다른 요소로 드래그합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

또는, 한 방향으로 드래그할 수도 있습니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

지정된 오프셋만큼 드래그할 때는 `dragOffset`을 사용합니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 대화상자 다루기 (JavaScript Dialogs)

Dusk는 JavaScript 대화상자와 상호작용하는 다양한 메서드를 제공합니다. 예를 들어 `waitForDialog` 메서드는 JavaScript 대화상자가 나타날 때까지 대기합니다. 이 메서드는 대기할 최대 시간을 초 단위로 선택적으로 받을 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 대화상자가 열렸고 특정 메시지가 포함되어 있는지 검사합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 포함된 대화상자에는 `typeInDialog` 메서드로 값을 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

열린 대화상자를 "확인" 버튼으로 닫으려면 `acceptDialog`를 호출하세요:

```php
$browser->acceptDialog();
```

"취소" 버튼으로 닫으려면 `dismissDialog`를 호출합니다:

```php
$browser->dismissDialog();
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정하기 (Scoping Selectors)

때때로 특정 셀렉터 범위 내에서 여러 작업을 수행하고 싶을 때가 있습니다. 예를 들어 테이블 안에서만 텍스트 존재 여부를 검사하고 그 안의 버튼을 클릭하는 작업이 필요할 때 `with` 메서드를 사용할 수 있습니다. `with` 메서드에 전달된 클로저 내에서 수행하는 모든 작업은 지정한 셀렉터 영역 내에 한정됩니다:

```php
$browser->with('.table', function ($table) {
    $table->assertSee('Hello World')
          ->clickLink('Delete');
});
```

때때로 현재 범위 밖에서 어설션을 수행해야 할 때가 있습니다. `elsewhere` 및 `elsewhereWhenAvailable` 메서드를 사용합니다:

```php
 $browser->with('.table', function ($table) {
    // 현재 범위: `body .table`...

    $browser->elsewhere('.page-title', function ($title) {
        // 현재 범위: `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function ($title) {
        // 현재 범위: `body .page-title`...
        $title->assertSee('Hello World');
    });
 });
```

<a name="waiting-for-elements"></a>
### 요소 대기하기 (Waiting For Elements)

JavaScript가 많이 사용되는 애플리케이션의 경우 특정 요소나 데이터가 준비될 때까지 테스트를 "대기"하도록 해야 할 때가 많습니다. Dusk는 이를 매우 쉽게 지원합니다. 다양한 메서드를 통해 페이지 요소가 보일 때까지, 또는 특정 JavaScript 표현식이 `true`가 될 때까지 기다릴 수 있습니다.

<a name="waiting"></a>
#### 기다리기 (Waiting)

단순히 지정한 밀리초만큼 테스트를 일시 정지하려면 `pause` 메서드를 사용하세요:

```php
$browser->pause(1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기하기 (Waiting For Selectors)

`waitFor` 메서드는 지정한 CSS 또는 Dusk 셀렉터와 일치하는 요소가 페이지에 나타날 때까지 테스트 실행을 일시 정지합니다. 기본 대기 시간은 최대 5초이며, 두 번째 인자로 다른 시간(초)을 지정할 수 있습니다:

```php
// 최대 5초간 대기...
$browser->waitFor('.selector');

// 최대 1초간 대기...
$browser->waitFor('.selector', 1);
```

특정 셀렉터 안에 원하는 텍스트가 나타날 때까지 기다릴 수도 있습니다:

```php
// 최대 5초간 텍스트가 나타날 때까지 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초간 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

특정 셀렉터가 사라질 때까지 기다리려면 다음을 사용합니다:

```php
// 최대 5초간 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초간 대기...
$browser->waitUntilMissing('.selector', 1);
```

또한 셀렉터가 활성화/비활성화 될 때까지 기다릴 수도 있습니다:

```php
// 최대 5초간 활성화될 때까지 대기...
$browser->waitUntilEnabled('.selector');

// 최대 1초간 대기...
$browser->waitUntilEnabled('.selector', 1);

// 최대 5초간 비활성화될 때까지 대기...
$browser->waitUntilDisabled('.selector');

// 최대 1초간 대기...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 요소 사용 가능 시 범위 지정하기 (Scoping Selectors When Available)

모달 창 등 특정 요소가 나타날 때까지 기다렸다가 범위를 지정해 작업하려면 `whenAvailable` 메서드를 사용합니다. 클로저 내의 모든 작업은 지정된 셀렉터 범위 내에서 수행됩니다:

```php
$browser->whenAvailable('.modal', function ($modal) {
    $modal->assertSee('Hello World')
          ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기하기 (Waiting For Text)

`waitForText` 메서드는 특정 텍스트가 페이지에 보일 때까지 기다립니다:

```php
// 최대 5초간 대기...
$browser->waitForText('Hello World');

// 최대 1초간 대기...
$browser->waitForText('Hello World', 1);
```

표시된 텍스트가 사라질 때까지 기다릴 땐 `waitUntilMissingText`를 사용합니다:

```php
// 최대 5초간 텍스트 사라질 때까지 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초간 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기하기 (Waiting For Links)

특정 링크 텍스트가 보일 때까지 기다릴 때는 `waitForLink` 메서드를 사용하세요:

```php
// 최대 5초간 대기...
$browser->waitForLink('Create');

// 최대 1초간 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기하기 (Waiting On The Page Location)

`$browser->assertPathIs('/home')` 같은 경로 어설션은 `window.location.pathname`이 비동기로 업데이트되면 실패할 수 있습니다. 이때 `waitForLocation` 메서드로 특정 위치를 대기할 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

완전한 URL도 기다릴 수 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[이름이 지정된 라우트](/docs/{{version}}/routing#named-routes) 위치도 기다릴 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기하기 (Waiting for Page Reloads)

어떤 작업 후 페이지가 리로드될 때까지 기다려야 한다면 `waitForReload` 메서드를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 새로 고침을 기다릴 때는 간편한 `clickAndWaitForReload` 메서드를 사용할 수도 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
        ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 대기하기 (Waiting On JavaScript Expressions)

특정 JavaScript 표현식이 `true`가 될 때까지 대기하려면 `waitUntil` 메서드를 사용하세요. 전달할 때 `return` 키워드나 세미콜론(`;`)을 포함하지 않아도 됩니다:

```php
// 최대 5초간 표현식이 true가 될 때까지 대기...
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초간 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기하기 (Waiting On Vue Expressions)

`waitUntilVue` 및 `waitUntilVueIsNot` 메서드를 사용해 [Vue 컴포넌트](https://vuejs.org)의 속성 값 변화를 대기할 수 있습니다:

```php
// 컴포넌트 속성이 특정 값을 가질 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 컴포넌트 속성이 특정 값을 갖지 않을 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-with-a-callback"></a>
#### 콜백을 이용한 대기 (Waiting With A Callback)

많은 "wait" 메서드는 기본적으로 `waitUsing` 메서드를 이용합니다. 이 메서드는 클로저가 `true`를 반환할 때까지 지정한 시간과 간격으로 반복 대기합니다. 실패 시 출력할 메시지도 지정할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소 스크롤하여 보기 (Scrolling An Element Into View)

때때로 요소가 브라우저 화면 밖에 있어 클릭이 안 되는 경우가 있습니다. `scrollIntoView` 메서드는 지정한 셀렉터 위치까지 스크롤하여 요소를 화면에 보이게 합니다:

```php
$browser->scrollIntoView('.selector')
        ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 Assertions (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어설션을 제공합니다. 아래 목록에 있는 모든 어설션이 문서화되어 있습니다:



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
[assertVueDoesNotContain](#assert-vue-does-not-contain)

</div>

<a name="assert-title"></a>
#### assertTitle

페이지 제목이 주어진 텍스트와 일치하는지 어설션합니다:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 제목에 주어진 텍스트가 포함되어 있는지 어설션합니다:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 문자열 제외)이 주어진 문자열과 일치하는지 어설션합니다:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 주어진 스킴과 일치하는지 어설션합니다:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 주어진 스킴과 일치하지 않는지 어설션합니다:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트가 주어진 호스트와 일치하는지 어설션합니다:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트가 주어진 호스트와 일치하지 않는지 어설션합니다:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 주어진 포트와 일치하는지 어설션합니다:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 주어진 포트와 일치하지 않는지 어설션합니다:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로가 주어진 경로로 시작하는지 어설션합니다:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 주어진 경로와 일치하는지 어설션합니다:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 주어진 경로와 일치하지 않는지 어설션합니다:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 주어진 [이름이 지정된 라우트](/docs/{{version}}/routing#named-routes) URL과 일치하는지 어설션합니다:

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

주어진 쿼리 문자열 파라미터가 존재하는지 어설션합니다:

```php
$browser->assertQueryStringHas($name);
```

특정 값도 함께 가진 파라미터인지 확인할 수도 있습니다:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

주어진 쿼리 문자열 파라미터가 없는지 어설션합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

URL의 현재 해시 프래그먼트가 주어진 프래그먼트와 일치하는지 어설션합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

URL 해시 프래그먼트가 주어진 프래그먼트로 시작하는지 어설션합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

URL 해시 프래그먼트가 주어진 프래그먼트와 일치하지 않는지 어설션합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

주어진 암호화된 쿠키가 존재하는지 어설션합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

주어진 암호화되지 않은 쿠키가 존재하는지 어설션합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

주어진 암호화된 쿠키가 존재하지 않는지 어설션합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

주어진 암호화되지 않은 쿠키가 존재하지 않는지 어설션합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키 값이 특정 값인지 어설션합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키 값이 특정 값인지 어설션합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

페이지에 특정 텍스트가 존재하는지 어설션합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

페이지에 특정 텍스트가 존재하지 않는지 어설션합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

특정 셀렉터 내에 특정 텍스트가 존재하는지 어설션합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

특정 셀렉터 내에 특정 텍스트가 존재하지 않는지 어설션합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

특정 셀렉터 내에 어떤 텍스트라도 존재하는지 어설션합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

특정 셀렉터 내에 텍스트가 전혀 없음을 어설션합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
#### assertScript

주어진 JavaScript 표현식이 특정 값을 반환하는지 어설션합니다:

```php
$browser->assertScript('window.isLoaded')
        ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지에 지정된 소스 코드가 포함되어 있는지 어설션합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지에 지정된 소스 코드가 포함되어 있지 않은지 어설션합니다:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

페이지에 특정 링크가 존재하는지 어설션합니다:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

페이지에 특정 링크가 존재하지 않는지 어설션합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

입력 필드가 특정 값을 가지고 있는지 어설션합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

입력 필드가 특정 값을 가지지 않는지 어설션합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

체크박스가 체크되어 있는지 어설션합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

체크박스가 체크되어 있지 않은지 어설션합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

라디오 버튼이 선택되어 있는지 어설션합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

라디오 버튼이 선택되어 있지 않은지 어설션합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

드롭다운이 특정 값을 선택하고 있는지 어설션합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

드롭다운이 특정 값을 선택하고 있지 않은지 어설션합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

특정 값들의 배열이 선택 옵션에 존재하는지 어설션합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

특정 값들의 배열이 선택 옵션에 존재하지 않는지 어설션합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

특정 값이 선택 옵션에 존재하는지 어설션합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

특정 값이 선택 옵션에 존재하지 않는지 어설션합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

특정 셀렉터 요소가 특정 값을 가지고 있는지 어설션합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

특정 셀렉터 요소가 특정 값을 가지고 있지 않은지 어설션합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

특정 셀렉터 요소가 지정된 속성에 특정 값을 가지고 있는지 어설션합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

특정 셀렉터 요소가 지정된 속성에 특정 값을 포함하는지 어설션합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

특정 셀렉터 요소가 ARIA 속성에 특정 값을 가지고 있는지 어설션합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>`가 있으면 다음과 같이 검사할 수 있습니다:

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

특정 셀렉터 요소가 데이터 속성에 특정 값을 가지고 있는지 검사합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>`는 이렇게 검사:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

특정 셀렉터 요소가 화면에 보이는지 어설션합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

특정 셀렉터 요소가 페이지 소스에 존재하는지 어설션합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

특정 셀렉터 요소가 페이지 소스에 존재하지 않는지 어설션합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

특정 셀렉터 요소가 화면에 보이지 않는지 어설션합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

특정 이름을 가진 입력 요소가 존재하는지 어설션합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

특정 이름을 가진 입력 요소가 페이지 소스에 존재하지 않는지 어설션합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

특정 메시지를 가진 JavaScript 대화상자가 뜬 것을 어설션합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

특정 필드가 활성화되어 있는지 어설션합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

특정 필드가 비활성화되어 있는지 어설션합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

특정 버튼이 활성화되어 있는지 어설션합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

특정 버튼이 비활성화되어 있는지 어설션합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

특정 필드에 포커스가 들어가 있는지 어설션합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

특정 필드에 포커스가 들어가 있지 않은지 어설션합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태인지 어설션합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태인지 어설션합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자로 인증된 상태인지 어설션합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 [Vue 컴포넌트](https://vuejs.org)의 상태도 어설션할 수 있습니다. 예를 들어 애플리케이션에 다음 Vue 컴포넌트가 있다면:

```html
// HTML...

<profile dusk="profile-component"></profile>

// 컴포넌트 정의...

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

Vue 컴포넌트 상태를 다음과 같이 어설션할 수 있습니다:

```php
/**
 * 기본 Vue 테스트 예제.
 *
 * @return void
 */
public function testVue()
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
                ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
#### assertVueIsNot

Vue 컴포넌트 데이터 속성이 주어진 값과 다르다는 것을 어설션합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트 데이터 속성이 배열이며, 특정 값을 포함하는지 어설션합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-does-not-contain"></a>
#### assertVueDoesNotContain

Vue 컴포넌트 데이터 속성이 배열이며, 특정 값을 포함하지 않는지 어설션합니다:

```php
$browser->assertVueDoesNotContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

때로는 복잡한 동작을 순차적으로 수행해야 해서 테스트 코드가 어렵게 느껴집니다. Dusk의 페이지 객체를 사용하면 페이지 단위로 표현력 있는 액션을 정의하고, 한 메서드 호출로 여러 동작을 수행할 수 있습니다. 또한 공통 셀렉터의 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기 (Generating Pages)

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 실행하세요. 생성된 페이지 객체는 `tests/Browser/Pages` 디렉토리에 위치합니다:

```
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정하기 (Configuring Pages)

기본적으로 페이지는 세 가지 메서드 `url`, `assert`, `elements`를 가집니다. 여기서는 `url`과 `assert` 메서드를 설명합니다. `elements` 메서드는 [단축 셀렉터](#shorthand-selectors)에서 더 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 페이지를 나타내는 URL 경로를 반환해야 합니다. Dusk는 이 URL을 사용해 브라우저를 이동시킵니다:

```php
/**
 * 페이지 URL 반환.
 *
 * @return string
 */
public function url()
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

브라우저가 현재 해당 페이지에 있음을 검증하는 어설션을 수행합니다. 반드시 내용을 채울 필요는 없지만, 원하는 경우 어설션을 넣을 수 있습니다. 페이지로 이동할 때 자동으로 실행됩니다:

```php
/**
 * 브라우저가 페이지에 있다는 것을 어설션.
 *
 * @return void
 */
public function assert(Browser $browser)
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동하기 (Navigating To Pages)

페이지 객체를 정의한 후에는 `visit` 메서드를 사용해 해당 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 특정 페이지에 있고, 그 페이지의 셀렉터와 메서드를 현재 컨텍스트에 "로드"해야 할 때가 있습니다. 예를 들어 버튼 클릭 후 리다이렉션되어 명시적 이동 없이도 다음 페이지의 기능을 사용해야 할 때 `on` 메서드를 사용합니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
        ->clickLink('Create Playlist')
        ->on(new CreatePlaylist)
        ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터 (Shorthand Selectors)

페이지 클래스 내 `elements` 메서드를 사용하면 페이지의 CSS 셀렉터에 대한 쉽고 기억하기 좋은 단축키를 정의할 수 있습니다. 예를 들어, 로그인 페이지의 "email" 입력 필드를 다음과 같이 정의할 수 있습니다:

```php
/**
 * 페이지의 요소 단축키 반환.
 *
 * @return array
 */
public function elements()
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

단축키를 정의하면 CSS 셀렉터 대신 언제든지 단축키를 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 셀렉터 (Global Shorthand Selectors)

Dusk 설치 시 `tests/Browser/Pages` 디렉토리에 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에서 애플리케이션 전체에서 공통으로 사용할 전역 단축 셀렉터를 정의할 수 있습니다:

```php
/**
 * 사이트 전체 전역 요소 단축키 반환.
 *
 * @return array
 */
public static function siteElements()
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### 페이지 메서드 (Page Methods)

기본 메서드 외에 페이지 클래스에 추가 메서드를 정의할 수 있습니다. 예를 들어 음악 관리 애플리케이션에서 플레이리스트를 만드는 기능은 여러 테스트에 반복되니, 페이지 클래스에 `createPlaylist` 메서드로 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;

class Dashboard extends Page
{
    // 기타 페이지 메서드...

    /**
     * 새 플레이리스트 생성.
     *
     * @param  \Laravel\Dusk\Browser  $browser
     * @param  string  $name
     * @return void
     */
    public function createPlaylist(Browser $browser, $name)
    {
        $browser->type('name', $name)
                ->check('share')
                ->press('Create Playlist');
    }
}
```

정의 후에는 해당 페이지를 사용하는 모든 테스트에서 메서드를 호출할 수 있습니다. 브라우저 인스턴스는 첫 번째 인자로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
        ->createPlaylist('My Playlist')
        ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 페이지 객체와 비슷하지만, 네비게이션 바나 알림 창처럼 애플리케이션 여러 곳에서 재사용되는 UI 조각 및 기능을 나타냅니다. 컴포넌트는 특정 URL에 묶이지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기 (Generating Components)

컴포넌트를 생성하려면 `dusk:component` Artisan 명령을 실행하세요. 새 컴포넌트는 `tests/Browser/Components` 디렉토리에 생성됩니다:

```
php artisan dusk:component DatePicker
```

위 예제처럼 "date picker"는 애플리케이션 여러 페이지에 존재할 수 있습니다. 수십 개의 테스트에서 날짜 선택 로직을 일일이 작성하는 대신, 컴포넌트를 정의해 해당 로직을 캡슐화할 수 있습니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * 컴포넌트 루트 셀렉터 반환.
     *
     * @return string
     */
    public function selector()
    {
        return '.date-picker';
    }

    /**
     * 브라우저 페이지가 컴포넌트를 포함하는지 어설션.
     *
     * @param  Browser  $browser
     * @return void
     */
    public function assert(Browser $browser)
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 요소 단축키 반환.
     *
     * @return array
     */
    public function elements()
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

    /**
     * 지정한 날짜 선택.
     *
     * @param  \Laravel\Dusk\Browser  $browser
     * @param  int  $year
     * @param  int  $month
     * @param  int  $day
     * @return void
     */
    public function selectDate(Browser $browser, $year, $month, $day)
    {
        $browser->click('@date-field')
                ->within('@year-list', function ($browser) use ($year) {
                    $browser->click($year);
                })
                ->within('@month-list', function ($browser) use ($month) {
                    $browser->click($month);
                })
                ->within('@day-list', function ($browser) use ($day) {
                    $browser->click($day);
                });
    }
}
```

<a name="using-components"></a>
### 컴포넌트 사용하기 (Using Components)

컴포넌트를 정의하면 날짜 선택 로직이 변경되어도 컴포넌트만 수정하면 되므로, 테스트가 더욱 간결해집니다:

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
     * 기본 컴포넌트 테스트 예제.
     *
     * @return void
     */
    public function testBasicExample()
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                    ->within(new DatePicker, function ($browser) {
                        $browser->selectDate(2019, 1, 30);
                    })
                    ->assertSee('January');
        });
    }
}
```

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

> [!NOTE]
> 대부분 Dusk 지속적 통합(CI) 설정은 Laravel 애플리케이션을 내장 PHP 개발 서버로 포트 8000에서 실행하도록 요구합니다. 따라서 CI 환경에 `APP_URL` 환경 변수를 반드시 `http://127.0.0.1:8000` 으로 설정하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행 (Heroku CI)

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 `app.json` 파일에 다음 Google Chrome 빌드팩과 스크립트를 추가하세요:

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
### Travis CI에서 테스트 실행 (Travis CI)

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 아래 `.travis.yml` 구성을 사용하세요. Travis CI는 그래픽 환경이 아니므로 Chrome 브라우저 실행을 위해 추가 설정이 필요하며, PHP 내장 웹 서버를 `php artisan serve`로 실행합니다:

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
### GitHub Actions에서 테스트 실행 (GitHub Actions)

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하는 기본 구성 예시는 다음과 같습니다. Travis CI처럼 `php artisan serve`로 PHP 내장 웹 서버를 실행합니다:

```yaml
name: CI
on: [push]
jobs:

  dusk-php:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Prepare The Environment
        run: cp .env.example .env
      - name: Create Database
        run: |
          sudo systemctl start mysql
          mysql --user="root" --password="root" -e "CREATE DATABASE 'my-database' character set UTF8mb4 collate utf8mb4_bin;"
      - name: Install Composer Dependencies
        run: composer install --no-progress --prefer-dist --optimize-autoloader
      - name: Generate Application Key
        run: php artisan key:generate
      - name: Upgrade Chrome Driver
        run: php artisan dusk:chrome-driver `/opt/google/chrome/chrome --version | cut -d " " -f3 | cut -d "." -f1`
      - name: Start Chrome Driver
        run: ./vendor/laravel/dusk/bin/chromedriver-linux &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        env:
          APP_URL: "http://127.0.0.1:8000"
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