# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성하기](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행하기](#running-tests)
    - [환경 설정 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증 처리](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 저장하기](#storing-console-output-to-disk)
    - [페이지 소스 저장하기](#storing-page-source-to-disk)
- [엘리먼트와 상호작용하기](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼 요소와 상호작용](#interacting-with-forms)
    - [파일 첨부하기](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭하기](#clicking-links)
    - [키보드 사용하기](#using-the-keyboard)
    - [마우스 사용하기](#using-the-mouse)
    - [자바스크립트 다이얼로그](#javascript-dialogs)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트 대기하기](#waiting-for-elements)
    - [엘리먼트를 뷰로 스크롤 하기](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성하기](#generating-pages)
    - [페이지 설정하기](#configuring-pages)
    - [페이지로 이동하기](#navigating-to-pages)
    - [단축 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성하기](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [지속적 통합(Continuous Integration)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치본을 사용합니다. 하지만 원하는 경우 다른 Selenium 호환 드라이버도 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require --dev laravel/dusk
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, 프로덕션 환경에서는 **절대** 등록하지 마세요. 그렇지 않으면 임의의 사용자가 애플리케이션 인증을 할 수 있는 보안 위험이 발생할 수 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령은 `tests/Browser` 디렉토리를 생성하고, Dusk 예제 테스트 및 운영체제에 맞는 ChromeDriver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수에 브라우저에서 접속하는 URL 값을 정확히 설정하세요.

> [!NOTE]
> [Laravel Sail](/docs/9.x/sail)로 로컬 개발 환경을 관리한다면, Sail 문서의 [Dusk 테스트 구성 및 실행](/docs/9.x/sail#laravel-dusk)도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령으로 설치된 ChromeDriver 버전 대신 다른 버전을 사용하고 싶다면 `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# OS에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# OS에 맞는 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원하는 모든 OS용 특정 버전 설치...
php artisan dusk:chrome-driver --all

# 현재 OS의 Chrome/Chromium 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리 파일이 실행 가능해야 합니다. Dusk 실행 중 문제가 있다면 다음 명령어로 실행 권한을 확인해주세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치본을 사용합니다. 그러나 자체 Selenium 서버를 기동하여 원하는 브라우저에서 테스트를 실행할 수도 있습니다.

시작하려면 `tests/DuskTestCase.php` 파일을 열어 `startChromeDriver` 호출 부분을 주석 처리하세요. 그러면 Dusk가 ChromeDriver를 자동으로 실행하지 않습니다:

```
/**
 * Dusk 테스트 실행 준비.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

그리고 `driver` 메서드를 원하는 WebDriver URL과 포트에 맞게 수정할 수 있습니다. 또한 WebDriver에 전달할 "desired capabilities"도 변경할 수 있습니다:

```
/**
 * RemoteWebDriver 인스턴스 생성.
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

`dusk:make` Artisan 명령어로 Dusk 테스트를 생성할 수 있습니다. 생성된 테스트는 `tests/Browser` 디렉토리에 위치합니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting The Database After Each Test)

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 조회하지만, Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 활용하는데, HTTP 요청 간에는 적용되지 않기 때문입니다. 대신 다음 두 가지 트레이트를 사용하세요: `DatabaseMigrations`와 `DatabaseTruncation`.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용하기 (Using Database Migrations)

`DatabaseMigrations` 트레이트는 각 테스트 실행 전에 마이그레이션을 실행하지만, 각 테스트마다 테이블을 삭제하고 다시 생성하기 때문에 일반적으로 테이블 내용만 지우는 것보다 느립니다:

```
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
> SQLite 메모리 내 데이터베이스는 Dusk 테스트 실행 시 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되므로, 다른 프로세스의 메모리 내 데이터베이스에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 내용 삭제 사용하기 (Using Database Truncation)

`DatabaseTruncation` 트레이트를 사용하려면 먼저 `doctrine/dbal` 패키지를 Composer로 설치해야 합니다:

```shell
composer require --dev doctrine/dbal
```

이 트레이트는 첫 번째 테스트에서 데이터베이스를 마이그레이션하여 테이블이 생성되었는지 확인하며, 이후 테스트에서는 모든 테이블의 데이터를 삭제(truncate)하여 마이그레이션을 재실행하는 것보다 빠릅니다:

```
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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 삭제합니다. 삭제할 테이블을 직접 지정하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

```
/**
 * 삭제할 테이블 목록.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

삭제에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 정의하세요:

```
/**
 * 삭제에서 제외할 테이블 목록.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

삭제할 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 정의할 수 있습니다:

```
/**
 * 삭제할 데이터베이스 연결 목록.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

<a name="running-tests"></a>
### 테스트 실행하기 (Running Tests)

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

만약 이전에 테스트 실패가 있었다면, 실패한 테스트만 먼저 실행하여 시간을 절약할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령은 PHPUnit 테스팅 러너에 전달되는 인수를 모두 받아들입니다. 예를 들어 특정 [그룹](https://phpunit.readthedocs.io/en/9.5/annotations.html#group)의 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/9.x/sail) 로컬 개발 환경을 사용한다면, Sail 문서의 [Dusk 테스트 구성 및 실행](/docs/9.x/sail#laravel-dusk)을 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행 (Manually Starting ChromeDriver)

기본적으로 Dusk는 ChromeDriver를 자동으로 실행하려 시도합니다. 만약 시스템에서 정상 동작하지 않는 경우, `dusk` 명령 실행 전 직접 ChromeDriver를 시작할 수 있습니다. 이 경우 `tests/DuskTestCase.php` 파일에서 다음 줄을 주석 처리하세요:

```
/**
 * Dusk 테스트 실행 준비.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

또한, ChromeDriver를 기본 포트(9515)가 아닌 다른 포트에서 실행한다면, `driver` 메서드에서 포트를 변경해야 합니다:

```
/**
 * RemoteWebDriver 인스턴스 생성.
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

테스트 실행 시 Dusk가 별도의 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하세요. 예를 들어 `local` 환경에서 테스트한다면 `.env.dusk.local` 파일을 만드는 식입니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업해 두었다가 `.env.dusk.{environment}` 파일을 `.env`로 임시 교체합니다. 테스트 완료 후 원래 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성하기 (Creating Browsers)

애플리케이션 로그인 기능이 작동하는지 확인하는 기본 테스트를 작성해 보겠습니다. 테스트를 생성한 후 로그인 페이지로 이동해서 인증 정보를 입력하고 "Login" 버튼을 눌러 홈 페이지에 도달하는지 확인합니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 호출해 생성할 수 있습니다:

```
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
     * 기본적인 브라우저 테스트 예제.
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

위 예제에서 보듯, `browse` 메서드는 클로저를 받습니다. 이 클로저에 Dusk가 자동으로 브라우저 인스턴스를 전달하며, 이를 통해 애플리케이션에 상호작용하고 어설션을 만들 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성하기

때로는 테스트를 위해 여러 브라우저 인스턴스가 필요할 수 있습니다. 예컨대, 웹소켓과 상호작용하는 채팅 화면 테스트가 그렇습니다. 이때는 클로저의 인자를 추가해 여러 브라우저 인스턴스를 생성하세요:

```
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
### 네비게이션 (Navigation)

`visit` 메서드로 애플리케이션 내 특정 URI로 이동할 수 있습니다:

```
$browser->visit('/login');
```

`visitRoute` 메서드는 [이름이 지정된 라우트](/docs/9.x/routing#named-routes)로 이동합니다:

```
$browser->visitRoute('login');
```

`back`과 `forward` 메서드로 브라우저 뒤로가기와 앞으로가기도 할 수 있습니다:

```
$browser->back();

$browser->forward();
```

`refresh` 메서드로 페이지 새로고침도 가능합니다:

```
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정 (Resizing Browser Windows)

`resize` 메서드는 브라우저 창 크기를 지정한 가로, 세로 픽셀로 조절합니다:

```
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```
$browser->maximize();
```

`fitContent` 메서드는 창 크기를 브라우저 콘텐츠 크기와 맞춥니다:

```
$browser->fitContent();
```

테스트 실패 시, Dusk는 자동으로 `fitContent`를 호출해 화면을 맞춘 뒤 스크린샷을 찍습니다. 이를 비활성화하려면 테스트 내에서 `disableFitOnFailure` 메서드를 호출하세요:

```
$browser->disableFitOnFailure();
```

`move` 메서드로 화면 내에서 브라우저 창 위치를 이동할 수 있습니다:

```
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재활용 가능한 커스텀 브라우저 메서드를 정의하고 싶다면, `Browser` 클래스의 `macro` 메서드를 사용하세요. 보통 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드 안에서 호출합니다:

```
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

`macro` 메서드는 첫 번째 인자로 메서드 이름, 두 번째 인자로 클로저를 받으며, 이 클로저가 실제 매크로 동작을 정의합니다. 브라우저 인스턴스에서 호출할 수 있습니다:

```
$this->browse(function ($browser) use ($user) {
    $browser->visit('/pay')
            ->scrollToElement('#credit-card-details')
            ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 처리 (Authentication)

자주 인증이 필요한 페이지를 테스트할 때, 매번 로그인 페이지를 거칠 필요 없이 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델 인스턴스나 해당 모델의 기본키를 받아 처리합니다:

```
use App\Models\User;

$this->browse(function ($browser) {
    $browser->loginAs(User::find(1))
          ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용하면, 해당 파일 내 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

암호화된 쿠키 값을 가져오거나 설정할 때 `cookie` 메서드를 사용합니다. Laravel에서 생성되는 모든 쿠키는 기본적으로 암호화되어 있습니다:

```
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키 값은 `plainCookie` 메서드로 다룰 수 있습니다:

```
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

특정 쿠키를 삭제하려면 `deleteCookie` 메서드를 사용하세요:

```
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행 (Executing JavaScript)

`script` 메서드를 통해 브라우저 내에서 자바스크립트 문장을 실행할 수 있습니다:

```
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기 (Taking A Screenshot)

`screenshot` 메서드로 스크린샷을 찍고 지정한 파일명으로 저장합니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 여러 해상도별로 연속적인 스크린샷을 찍습니다:

```
$browser->responsiveScreenshots('filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장하기 (Storing Console Output To Disk)

`storeConsoleLog` 메서드로 현재 브라우저의 콘솔 출력을 지정한 파일명으로 저장할 수 있습니다. 기록은 `tests/Browser/console` 폴더에 저장됩니다:

```
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장하기 (Storing Page Source To Disk)

`storeSource` 메서드로 현재 페이지의 HTML 소스를 지정한 파일명으로 저장할 수 있습니다. 저장 위치는 `tests/Browser/source` 폴더입니다:

```
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

효과적인 CSS 셀렉터 선택은 Dusk 테스트 작성에서 가장 어려운 부분입니다. 프론트엔드 변경사항이 다음과 같은 CSS 셀렉터를 깨뜨릴 수 있기 때문입니다:

```
// HTML...

<button>Login</button>

// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터는 테스트 작성에 집중할 수 있게 CSS 셀렉터 기억을 덜어줍니다. HTML 엘리먼트에 `dusk` 속성을 추가하고, 브라우저 명령어에서 `@`를 접두사로 붙여 셀렉터를 사용하세요:

```
// HTML...

<button dusk="login-button">Login</button>

// Test...

$browser->click('@login-button');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, & Attributes)

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정 (Retrieving & Setting Values)

Dusk는 페이지 내 엘리먼트의 현재 값, 표시되는 텍스트 및 속성에 대한 여러 메서드를 제공합니다. 예를 들어, CSS 또는 Dusk 셀렉터에 일치하는 엘리먼트의 `"value"` 속성을 가져오려면 `value` 메서드를 사용하세요:

```
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 주어진 필드 이름을 가진 입력 엘리먼트의 값을 가져옵니다:

```
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 조회 (Retrieving Text)

`text` 메서드는 주어진 셀렉터에 해당하는 엘리먼트의 표시 텍스트를 가져옵니다:

```
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 조회 (Retrieving Attributes)

`attribute` 메서드는 주어진 셀렉터 엘리먼트의 특정 속성 값을 조회합니다:

```
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼 요소와 상호작용하기 (Interacting With Forms)

<a name="typing-values"></a>
#### 입력값 타이핑하기 (Typing Values)

폼과 입력 요소에 타이핑하는 다양한 메서드를 제공합니다. 다음은 입력 필드에 텍스트를 입력하는 예제입니다:

```
$browser->type('email', 'taylor@laravel.com');
```

`type` 메서드는 필요한 경우 CSS 셀렉터를 받지만, 지정하지 않아도 `name` 속성과 일치하는 `input` 또는 `textarea` 엘리먼트를 자동 탐색합니다.

기존 내용에 추가로 텍스트를 덧붙이려면 `append` 메서드를 사용하세요:

```
$browser->type('tags', 'foo')
        ->append('tags', ', bar, baz');
```

`clear` 메서드로 입력값을 비울 수도 있습니다:

```
$browser->clear('email');
```

느린 타이핑도 가능합니다. `typeSlowly` 메서드는 기본적으로 키 입력 사이를 100 밀리초 간격으로 둡니다. 간격은 세 번째 인자로 조절할 수 있습니다:

```
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드로 느리게 텍스트를 덧붙일 수도 있습니다:

```
$browser->type('tags', 'foo')
        ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운 (Dropdowns)

`select` 메서드는 `select` 엘리먼트에서 값을 선택합니다. `type`과 마찬가지로 풀 CSS 셀렉터가 필요하지 않습니다. 대상 값을 선택할 때는 표시되는 텍스트가 아닌 옵션의 실제 값을 전달해야 합니다:

```
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 무작위 옵션을 선택합니다:

```
$browser->select('size');
```

배열을 넘기면 여러 옵션을 선택할 수도 있습니다:

```
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스 (Checkboxes)

`check` 메서드로 체크박스를 선택할 수 있습니다. CSS 셀렉터를 지정하지 않으면 `name` 속성과 일치하는 체크박스를 찾습니다:

```
$browser->check('terms');
```

체크를 해제하려면 `uncheck`를 사용하세요:

```
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼 (Radio Buttons)

`radio` 메서드로 라디오 버튼을 선택할 수 있습니다. CSS 셀렉터를 지정하지 않으면 `name`과 `value` 속성이 일치하는 라디오 입력을 찾습니다:

```
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기 (Attaching Files)

`attach` 메서드는 `file` 입력 요소에 파일을 첨부합니다. CSS 셀렉터를 지정하지 않으면 `name` 속성이 일치하는 파일 입력을 찾습니다:

```
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> `attach` 기능은 서버에 `Zip` PHP 확장 모듈이 설치되고 활성화되어 있어야 작동합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드는 페이지 내 버튼을 클릭합니다. 인자로는 버튼 텍스트, 또는 CSS/Dusk 셀렉터를 사용할 수 있습니다:

```
$browser->press('Login');
```

많은 앱은 폼 제출 후 버튼을 비활성화했다가 응답 완료 시 다시 활성화합니다. 버튼을 누르고 재활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용하세요:

```
// 최대 5초 동안 버튼이 활성화되기를 기다림...
$browser->pressAndWaitFor('Save');

// 최대 1초 동안 버튼이 활성화되기를 기다림...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 주어진 표시 텍스트를 가진 링크를 클릭합니다:

```
$browser->clickLink($linkText);
```

`seeLink` 메서드는 주어진 텍스트를 가진 링크가 페이지에 보이는지 확인합니다:

```
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드는 jQuery에 의존합니다. 페이지에 jQuery가 없으면 Dusk가 자동으로 테스트 기간 동안 페이지에 삽입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기 (Using The Keyboard)

`keys` 메서드는 `type` 메서드보다 더 복잡한 입력 시퀀스를 지정할 때 사용합니다. 예를 들어, 수정 키를 누른 채로 값을 입력할 수 있습니다. 아래 예제는 셀렉터에 대해 `shift` 키를 누른 채로 `taylor`를 타이핑하고, 수정키 없이 `swift`를 입력합니다:

```
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

키보드 단축키 조합을 보낼 때도 유용합니다:

```
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` 같은 모든 수정 키는 중괄호 `{}` 안에 써야 하며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스의 상수와 매칭됩니다. [GitHub 링크](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="using-the-mouse"></a>
### 마우스 사용하기 (Using The Mouse)

<a name="clicking-on-elements"></a>
#### 엘리먼트 클릭하기 (Clicking On Elements)

`click` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 엘리먼트를 클릭합니다:

```
$browser->click('.selector');
```

`clickAtXPath` 메서드는 주어진 XPath 식과 일치하는 엘리먼트를 클릭합니다:

```
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저 화면상의 지정 좌표 클릭을 수행합니다:

```
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick`은 더블클릭, `rightClick`은 우클릭 동작을 시뮬레이션합니다:

```
$browser->doubleClick();

$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`는 클릭 후 마우스를 누르고 있는 상태를 시뮬레이션하며, 이후 `releaseMouse`로 해제합니다:

```
$browser->clickAndHold()
        ->pause(1000)
        ->releaseMouse();
```

<a name="mouseover"></a>
#### 마우스 오버 (Mouseover)

`mouseover` 메서드는 마우스를 지정한 셀렉터 위로 이동시킵니다:

```
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 & 드롭 (Drag & Drop)

`drag` 메서드는 특정 엘리먼트를 지정한 다른 엘리먼트로 끌어다 놓습니다:

```
$browser->drag('.from-selector', '.to-selector');
```

또는 한 방향으로만 끌 수도 있습니다:

```
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 끌 수도 있습니다:

```
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그 (JavaScript Dialogs)

Dusk는 자바스크립트 알림창과 상호작용하는 다양한 메서드를 제공합니다.

예를 들어, 다이얼로그가 나타날 때까지 기다리려면 `waitForDialog`를 사용하세요. 옵션으로 최대 대기 시간을 초 단위로 지정할 수 있습니다:

```
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 특정 메시지를 포함하는 다이얼로그가 열렸는지 어설션합니다:

```
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 포함된 다이얼로그가 있을 때는 `typeInDialog` 메서드로 값을 입력합니다:

```
$browser->typeInDialog('Hello World');
```

"확인" 버튼을 눌러 다이얼로그를 닫으려면 `acceptDialog`를, "취소" 버튼으로 닫으려면 `dismissDialog`를 호출하세요:

```
$browser->acceptDialog();

$browser->dismissDialog();
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정 (Scoping Selectors)

특정 셀렉터 범위 내에서 여러 작업을 수행해야 할 때가 있습니다. 예를 들어, 테이블 내부에서만 특정 텍스트가 있는지 확인한 뒤, 그 안 버튼을 클릭하고 싶을 때 `with` 메서드를 사용합니다. 클로저 내부에서 이 셀렉터 범위로 모든 동작이 제한됩니다:

```
$browser->with('.table', function ($table) {
    $table->assertSee('Hello World')
          ->clickLink('Delete');
});
```

가끔 현재 범위 밖에서 어설션을 실행해야 하는 경우도 있습니다. 이때 `elsewhere`나 `elsewhereWhenAvailable` 메서드를 사용하세요:

```
$browser->with('.table', function ($table) {
    // 현재 범위는 `body .table`...

    $browser->elsewhere('.page-title', function ($title) {
        // 현재 범위는 `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function ($title) {
        // 현재 범위는 `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 엘리먼트 대기하기 (Waiting For Elements)

JavaScript가 많이 사용되는 앱을 테스트할 때, 특정 엘리먼트가 나타나거나 데이터가 준비될 때까지 기다려야 할 때가 많습니다. Dusk는 다양한 대기 메서드를 제공해 이 과정을 편리하게 만들어 줍니다.

<a name="waiting"></a>
#### 단순 대기 (Waiting)

테스트 실행을 지정한 밀리초만큼 멈추려면 `pause` 메서드를 사용하세요:

```
$browser->pause(1000);
```

특정 조건이 참일 때만 일시 정지하려면 `pauseIf`를 쓰세요:

```
$browser->pauseIf(App::environment('production'), 1000);
```

특정 조건이 거짓일 때만 멈추려면 `pauseUnless`를 사용합니다:

```
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기 (Waiting For Selectors)

`waitFor` 메서드는 특정 CSS 또는 Dusk 셀렉터를 가진 엘리먼트가 페이지에 표시될 때까지 기다립니다. 기본 최대 대기 시간은 5초이며, 필요하면 두 번째 인자로 조정할 수 있습니다:

```
// 최대 5초 대기...
$browser->waitFor('.selector');

// 최대 1초 대기...
$browser->waitFor('.selector', 1);
```

특정 텍스트가 셀렉터 안에 포함될 때까지 기다리려면 `waitForTextIn`을 사용합니다:

```
// 최대 5초 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

해당 셀렉터가 페이지에서 사라질 때까지 기다리려면 `waitUntilMissing`을 사용하세요:

```
// 최대 5초 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 대기...
$browser->waitUntilMissing('.selector', 1);
```

특정 셀렉터가 활성화되거나 비활성화될 때까지도 대기할 수 있습니다:

```
// 최대 5초 대기 (활성화)...
$browser->waitUntilEnabled('.selector');

// 최대 1초 대기 (활성화)...
$browser->waitUntilEnabled('.selector', 1);

// 최대 5초 대기 (비활성화)...
$browser->waitUntilDisabled('.selector');

// 최대 1초 대기 (비활성화)...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 엘리먼트가 준비될 때 범위 지정 (Scoping Selectors When Available)

모달과 같이 특정 엘리먼트가 나타난 후에 작업해야 할 때가 있습니다. `whenAvailable` 메서드를 사용하면 해당 셀렉터에 범위 한정된 동작을 실행할 수 있습니다:

```
$browser->whenAvailable('.modal', function ($modal) {
    $modal->assertSee('Hello World')
          ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기 (Waiting For Text)

`waitForText` 메서드로 페이지 내 특정 텍스트가 나타날 때까지 대기합니다:

```
// 최대 5초 대기...
$browser->waitForText('Hello World');

// 최대 1초 대기...
$browser->waitForText('Hello World', 1);
```

텍스트가 사라질 때까지 기다리려면 `waitUntilMissingText`를 사용하세요:

```
// 최대 5초 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기 (Waiting For Links)

특정 링크 텍스트가 나타날 때까지 기다리려면 `waitForLink`을 사용하세요:

```
// 최대 5초 대기...
$browser->waitForLink('Create');

// 최대 1초 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기 (Waiting For Inputs)

특정 입력 필드가 보일 때까지 대기하려면 `waitForInput`을 사용합니다:

```
// 최대 5초 대기...
$browser->waitForInput($field);

// 최대 1초 대기...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기 (Waiting On The Page Location)

`$browser->assertPathIs('/home')` 같은 경로 어설션은 `window.location.pathname`이 비동기로 업데이트될 때 실패할 수 있습니다. `waitForLocation` 메서드를 써서 위치가 정확해질 때까지 기다릴 수 있습니다:

```
$browser->waitForLocation('/secret');
```

전체 URL도 기다릴 수 있습니다:

```
$browser->waitForLocation('https://example.com/path');
```

[이름이 지정된 라우트](/docs/9.x/routing#named-routes)의 경로를 기다릴 수도 있습니다:

```
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기 (Waiting For Page Reloads)

어떤 동작 후 페이지 리로드를 기다려야 하면 `waitForReload` 메서드를 사용하세요:

```
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 리로드를 기다리는 작업이 많으므로, `clickAndWaitForReload` 메서드도 제공됩니다:

```
$browser->clickAndWaitForReload('.selector')
        ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기 (Waiting On JavaScript Expressions)

특정 자바스크립트 표현식이 `true`가 될 때까지 기다리려면 `waitUntil` 메서드를 사용하세요. `return` 키워드나 세미콜론을 빼고 표현식을 전달합니다:

```
// 최대 5초 대기...
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기 (Waiting On Vue Expressions)

`waitUntilVue`와 `waitUntilVueIsNot` 메서드는 [Vue 컴포넌트](https://vuejs.org)의 속성 값에 따라 대기할 수 있습니다:

```
// 해당 속성 값이 일치할 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 해당 속성 값이 일치하지 않을 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기 (Waiting For JavaScript Events)

`waitForEvent` 메서드로 자바스크립트 이벤트 발생을 대기할 수 있습니다:

```
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 현재 범위(기본 `body`)에 붙습니다. 범위 지정 셀렉터 내부에서 사용해도 동일하게 동작합니다:

```
$browser->with('iframe', function ($iframe) {
    // iframe의 load 이벤트 대기...
    $iframe->waitForEvent('load');
});
```

두 번째 인자로 셀렉터를 전달하여 특정 엘리먼트에 이벤트를 대기할 수도 있습니다:

```
$browser->waitForEvent('load', '.selector');
```

`document`와 `window` 객체의 이벤트도 대기 가능합니다:

```
// 문서 스크롤 대기...
$browser->waitForEvent('scroll', 'document');

// 최대 5초 동안 창 크기 조정 이벤트 대기...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 함수로 대기 (Waiting With A Callback)

`waitUsing` 메서드는 주어진 클로저가 `true`를 반환할 때까지 지정한 시간, 간격마다 실행하며 기다립니다. 실패 시 메시지를 지정할 수도 있습니다:

```
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트를 뷰로 스크롤 하기 (Scrolling An Element Into View)

뷰 영역 밖에 있어 클릭할 수 없는 엘리먼트는 `scrollIntoView`로 스크롤하여 뷰에 포함시킬 수 있습니다:

```
$browser->scrollIntoView('.selector')
        ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk가 지원하는 어설션은 매우 다양합니다. 아래 목록에서 주요한 어설션 메서드를 확인할 수 있습니다:

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

페이지 타이틀이 지정한 텍스트와 일치하는지 어설션합니다:

```
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 타이틀에 특정 텍스트가 포함되어 있는지 확인합니다:

```
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 스트링 제외)이 지정한 문자열과 일치하는지 확인합니다:

```
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 지정한 스킴과 일치하는지 확인합니다:

```
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 지정한 스킴과 일치하지 않는지 확인합니다:

```
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트가 지정한 호스트와 일치하는지 확인합니다:

```
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트가 지정한 호스트와 일치하지 않는지 확인합니다:

```
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 지정한 포트와 일치하는지 확인합니다:

```
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 지정한 포트와 일치하지 않는지 확인합니다:

```
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

URL 경로가 지정한 경로로 시작하는지 확인합니다:

```
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 지정한 경로와 정확히 일치하는지 확인합니다:

```
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 지정한 경로와 일치하지 않는지 확인합니다:

```
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 지정한 [이름 있는 라우트](/docs/9.x/routing#named-routes)에 해당하는지 확인합니다:

```
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

쿼리 스트링에 지정한 파라미터가 존재하는지 확인합니다:

```
$browser->assertQueryStringHas($name);
```

값까지 검사하려면 두 번째 인자로 지정할 수 있습니다:

```
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

쿼리 스트링에 지정한 파라미터가 없는지 확인합니다:

```
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

URL 해시 조각(fragment)이 지정한 값과 일치하는지 확인합니다:

```
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

URL 해시 조각이 지정한 값으로 시작하는지 확인합니다:

```
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

URL 해시 조각이 지정한 값과 일치하지 않는지 확인합니다:

```
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

암호화된 쿠키가 존재하는지 확인합니다:

```
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

암호화되지 않은 쿠키가 존재하는지 확인합니다:

```
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

암호화된 쿠키가 존재하지 않는지 확인합니다:

```
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

암호화되지 않은 쿠키가 존재하지 않는지 확인합니다:

```
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키의 값이 지정한 값인지 확인합니다:

```
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키의 값이 지정한 값인지 확인합니다:

```
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

지정한 텍스트가 페이지에 존재하는지 확인합니다:

```
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

지정한 텍스트가 페이지에 존재하지 않는지 확인합니다:

```
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

특정 셀렉터 안에 지정한 텍스트가 있는지 확인합니다:

```
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

특정 셀렉터 안에 지정한 텍스트가 없는지 확인합니다:

```
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

특정 셀렉터 내에 텍스트가 존재하는지 확인합니다:

```
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

특정 셀렉터 내에 어느 텍스트도 존재하지 않는지 확인합니다:

```
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
#### assertScript

자바스크립트 표현식이 특정 값과 일치하는지 확인합니다:

```
$browser->assertScript('window.isLoaded')
        ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지 소스 내에 특정 코드가 포함되어 있는지 확인합니다:

```
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지 소스 내에 특정 코드가 없는지 확인합니다:

```
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

페이지 내에 특정 링크 텍스트가 포함되어 있는지 확인합니다:

```
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

페이지 내에 특정 링크 텍스트가 포함되어 있지 않은지 확인합니다:

```
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

지정한 입력 필드 값이 기대하는 값과 일치하는지 확인합니다:

```
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

입력 필드 값이 특정 값과 일치하지 않는지 확인합니다:

```
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

체크박스가 선택되어 있는지 확인합니다:

```
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

체크박스가 선택되어 있지 않은지 확인합니다:

```
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

체크박스가 불확정 상태인지 확인합니다:

```
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

라디오 버튼이 선택되어 있는지 확인합니다:

```
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

라디오 버튼이 선택되어 있지 않은지 확인합니다:

```
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

드롭다운이 지정한 값을 선택하고 있는지 확인합니다:

```
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

드롭다운이 지정한 값을 선택하고 있지 않은지 확인합니다:

```
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

드롭다운이 지정한 여러 값을 옵션으로 가지고 있는지 확인합니다:

```
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

드롭다운이 지정한 여러 값을 옵션으로 가지고 있지 않은지 확인합니다:

```
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

드롭다운에 특정 값이 옵션으로 존재하는지 확인합니다:

```
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

드롭다운에 특정 값이 옵션으로 존재하지 않는지 확인합니다:

```
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

주어진 셀렉터에 해당하는 엘리먼트가 지정한 값을 가지고 있는지 확인합니다:

```
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

주어진 셀렉터에 해당하는 엘리먼트가 지정한 값을 가지고 있지 않은지 확인합니다:

```
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

주어진 셀렉터 엘리먼트가 지정한 속성을 특정 값으로 가지고 있는지 확인합니다:

```
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

주어진 셀렉터 엘리먼트의 특정 속성값에 지정한 값이 포함되어 있는지 확인합니다:

```
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

주어진 셀렉터 엘리먼트가 지정한 ARIA 속성을 특정 값으로 가지고 있는지 확인합니다:

```
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 환경이라면 다음과 같이 검사할 수 있습니다:

```
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

주어진 셀렉터 엘리먼트가 지정한 데이터 속성 값을 특정 값으로 가지고 있는지 확인합니다:

```
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 환경이라면 다음과 같이 검사합니다:

```
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

주어진 셀렉터 엘리먼트가 화면에 표시되고 있는지 확인합니다:

```
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

주어진 셀렉터 엘리먼트가 페이지 소스에 존재하는지 확인합니다:

```
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

주어진 셀렉터 엘리먼트가 페이지 소스에 존재하지 않는지 확인합니다:

```
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

주어진 셀렉터 엘리먼트가 화면에 표시되지 않는지 확인합니다:

```
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

지정한 이름의 입력 필드가 존재하는지 확인합니다:

```
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

지정한 이름의 입력 필드가 페이지 소스에 존재하지 않는지 확인합니다:

```
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

지정한 메시지를 가진 자바스크립트 다이얼로그가 열린 상태인지 확인합니다:

```
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

지정한 입력 필드가 활성화되어 있는지 확인합니다:

```
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

지정한 입력 필드가 비활성화되어 있는지 확인합니다:

```
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

지정한 버튼이 활성화되어 있는지 확인합니다:

```
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

지정한 버튼이 비활성화되어 있는지 확인합니다:

```
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

지정한 입력 필드에 포커스가 위치하고 있는지 확인합니다:

```
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

지정한 입력 필드에 포커스가 위치하지 않은지 확인합니다:

```
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태인지 확인합니다:

```
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태(게스트)인지 확인합니다:

```
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자로 인증된 상태인지 확인합니다:

```
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk는 [Vue 컴포넌트](https://vuejs.org) 데이터 상태에 대해서도 어설션할 수 있습니다. 예를 들어, 다음과 같은 Vue 컴포넌트가 있다고 가정하세요:

```
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

Vue 컴포넌트 상태에 대한 어설션은 다음과 같이 합니다:

```
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

지정한 Vue 컴포넌트 데이터 속성이 특정 값과 일치하지 않는지 확인합니다:

```
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트 데이터 속성이 배열이며 특정 값을 포함하는지 확인합니다:

```
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-does-not-contain"></a>
#### assertVueDoesNotContain

Vue 컴포넌트 데이터 속성이 배열이며 특정 값을 포함하지 않는지 확인합니다:

```
$browser->assertVueDoesNotContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

복잡한 테스트에서 여러 동작을 순차적으로 수행해야 할 때, 테스트가 읽기 어려워질 수 있습니다. Dusk의 페이지 객체는 특정 페이지에서 자주 수행하는 동작을 표현력 있게 정의하고, 한 메서드 호출로 실행할 수 있게 해줍니다. 또한 페이지 내 공통 셀렉터 단축도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기 (Generating Pages)

`dusk:page` Artisan 명령어로 페이지 객체를 생성하세요. 페이지 클래스는 `tests/Browser/Pages` 디렉토리에 생성됩니다:

```
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정하기 (Configuring Pages)

페이지 기본 메서드는 `url`, `assert`, `elements` 세 가지입니다. 여기서는 `url`과 `assert`부터 설명합니다. `elements`는 [단축 셀렉터](#shorthand-selectors)에서 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

페이지가 나타내는 URL 경로를 반환해야 합니다. Dusk는 이 경로를 이용해 브라우저 내 페이지로 이동합니다:

```
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

브라우저가 해당 페이지에 실제로 있는지 확인하는 어설션을 만들 수 있습니다. 꼭 메서드 내용을 작성하지 않아도 좋지만, 필요한 검증을 여기에 구현할 수 있습니다. 페이지로 이동할 때 자동 호출됩니다:

```
/**
 * 브라우저가 페이지에 있는지 어설션.
 *
 * @return void
 */
public function assert(Browser $browser)
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지 이동하기 (Navigating To Pages)

페이지가 정의되면 `visit` 메서드에 페이지 객체를 전달해 원하는 페이지로 이동할 수 있습니다:

```
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 페이지에 있는데, 그 페이지에 정의된 셀렉터와 메서드를 현재 테스트 컨텍스트에 로드하고 싶을 때 `on` 메서드를 사용합니다. 버튼을 누른 후 명시적 이동 없이 리다이렉트 되는 상황에서 유용합니다:

```
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
        ->clickLink('Create Playlist')
        ->on(new CreatePlaylist)
        ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드 내에서 페이지 내 CSS 셀렉터에 대한 짧고 기억하기 쉬운 별칭을 정의할 수 있습니다. 예를 들어 로그인 페이지에서 이메일 입력란 셀렉터 별칭은 다음과 같이 정의합니다:

```
/**
 * 페이지 내 셀렉터 단축키 정의.
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

이후 테스트에서 언제든 별칭을 풀 셀렉터 대신 쓸 수 있습니다:

```
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 셀렉터 (Global Shorthand Selectors)

Dusk 설치 시 기본 `Page` 클래스가 `tests/Browser/Pages`에 생성되며, 이 클래스의 `siteElements` 메서드에서 애플리케이션 전역에서 사용하는 공통 단축 셀렉터를 등록할 수 있습니다:

```
/**
 * 사이트 전역 셀렉터 단축 정의.
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

기본 메서드 외에 페이지 클래스는 추가 메서드를 정의할 수 있습니다. 예를 들어 플레이리스트 생성 액션을 공통 메서드로 만들면 테스트마다 중복 코드를 줄일 수 있습니다:

```
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

정의한 후에는 페이지 인스턴스에서 자동으로 브라우저 인자를 전달받아 사용할 수 있습니다:

```
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
        ->createPlaylist('My Playlist')
        ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 페이지 객체와 비슷하지만, 내비게이션 바, 알림창 등 애플리케이션 내 여러 페이지에서 반복 사용하는 UI 조각과 기능에 쓰입니다. 따라서 컴포넌트는 특정 URL에 묶여 있지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기 (Generating Components)

`dusk:component` Artisan 명령어로 컴포넌트를 생성합니다. 컴포넌트 클래스는 `tests/Browser/Components` 디렉토리에 생성됩니다:

```
php artisan dusk:component DatePicker
```

예를 들어 날짜 선택 컴포넌트는 여러 페이지에서 반복 사용되므로, 직접 각 테스트마다 선택 로직을 구현하지 말고 컴포넌트로 캡슐화할 수 있습니다:

```
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
     * 브라우저 페이지에 컴포넌트가 있는지 어설션.
     *
     * @param  Browser  $browser
     * @return void
     */
    public function assert(Browser $browser)
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 내 단축 셀렉터 정의.
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
     * 주어진 날짜 선택.
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

정의된 컴포넌트는 어느 테스트에서나 쉽게 불러와 사용할 수 있습니다. 날짜 선택 로직이 변경돼도 컴포넌트 클래스만 수정하면 됩니다:

```
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

> [!WARNING]
> 대부분의 Dusk CI 환경 구성은 Laravel 애플리케이션을 내장 PHP 개발 서버를 사용해 포트 8000에서 실행하는 것을 전제로 합니다. 따라서 CI 환경의 `APP_URL` 환경 변수는 `http://127.0.0.1:8000`으로 설정되어 있어야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 `app.json`에 다음과 같이 Google Chrome 빌드팩과 스크립트를 추가하세요:

```
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
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 설정을 사용하세요. Travis는 그래픽 환경이 아니므로 Chrome 브라우저를 실행하려면 추가 설정이 필요합니다. `php artisan serve`로 PHP 내장 서버를 구동합니다:

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
### GitHub Actions

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 수행하려면 다음 예시 구성파일을 참고하세요. Travis CI처럼 내장 웹서버를 사용합니다:

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
      - uses: actions/checkout@v3
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