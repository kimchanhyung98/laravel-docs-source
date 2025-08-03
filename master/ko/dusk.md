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
- [브라우저 기본사항](#browser-basics)
    - [브라우저 생성하기](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
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
    - [셀렉터 범위 지정하기](#scoping-selectors)
    - [요소 대기하기](#waiting-for-elements)
    - [요소를 뷰로 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 단언(Assertions)](#available-assertions)
- [페이지](#pages)
    - [페이지 생성하기](#generating-pages)
    - [페이지 설정하기](#configuring-pages)
    - [페이지로 네비게이션하기](#navigating-to-pages)
    - [별칭 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성하기](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [지속적 통합(CI)](#continuous-integration)
    - [Heroku CI에서 테스트 실행하기](#running-tests-on-heroku-ci)
    - [Travis CI에서 테스트 실행하기](#running-tests-on-travis-ci)
    - [GitHub Actions에서 테스트 실행하기](#running-tests-on-github-actions)
    - [Chipper CI에서 테스트 실행하기](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 하지만 원하실 경우 어떤 Selenium 호환 드라이버든 사용할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 `laravel/dusk` Composer 의존성을 프로젝트에 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> 만약 Dusk의 서비스 프로바이더를 수동으로 등록하고 있다면, 절대 프로덕션 환경에서는 등록하지 마세요. 이렇게 하면 임의의 사용자가 애플리케이션에 인증할 수 있게 되어 보안상 위험할 수 있습니다.

Dusk 패키지를 설치한 후 `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉토리와 예제 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

다음으로 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경 관리를 위해 [Laravel Sail](/docs/master/sail)을 사용한다면, [Dusk 테스트 구성 및 실행](/docs/master/sail#laravel-dusk) 관련 Sail 문서도 참조하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

Laravel Dusk의 `dusk:install` 명령어를 통해 설치된 ChromeDriver 버전과 다르게 설치하고 싶다면 `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 운영체제에 맞는 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 모든 지원 운영체제용 특정 버전 ChromeDriver 설치...
php artisan dusk:chrome-driver --all

# 운영체제에 설치된 Chrome / Chromium 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행에 문제가 있다면 다음 명령어로 바이너리 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용해 브라우저 테스트를 실행합니다. 하지만 직접 Selenium 서버를 시작하여 원하는 어떤 브라우저로도 테스트를 실행할 수 있습니다.

시작하려면 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 열고, `startChromeDriver` 메서드 호출 부분을 제거하세요. 이렇게 하면 Dusk가 자동으로 ChromeDriver를 시작하지 않습니다:

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

다음으로 `driver` 메서드를 수정해 원하는 URL과 포트에 연결하도록 하세요. 원하는 경우 WebDriver에 전달할 "desired capabilities"도 수정할 수 있습니다:

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

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉토리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 불러오는 페이지와 상호작용합니다. 하지만 Dusk 테스트에서는 절대 `RefreshDatabase` 트레이트를 사용하지 마세요. `RefreshDatabase` 트레이트는 데이터베이스 트랜잭션을 사용하는데, 이는 HTTP 요청 간에 적용되거나 사용될 수 없기 때문입니다. 대신 두 가지 옵션이 있습니다: `DatabaseMigrations` 트레이트와 `DatabaseTruncation` 트레이트.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용하기

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 각 테스트마다 테이블을 드롭했다가 다시 생성하는 것은 테이블을 단순히 초기화하는 것보다 일반적으로 느립니다:

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
> SQLite 인메모리 데이터베이스는 Dusk 테스트 실행 시 사용할 수 없습니다. 브라우저가 별도의 프로세스 내에서 실행되기 때문에 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 초기화 사용하기

`DatabaseTruncation` 트레이트는 첫 번째 테스트에서 마이그레이션을 실행하여 데이터베이스 테이블이 제대로 준비되었는지 확인합니다. 이후 진행하는 테스트에서는 테이블을 단순히 초기화(truncate)하여 모든 마이그레이션을 다시 실행하는 것보다 빠르게 처리합니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 초기화합니다. 초기화할 테이블을 직접 지정하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

> [!NOTE]
> Pest를 사용하는 경우, 기본 `DuskTestCase` 클래스나 테스트가 상속하는 클래스에 속성이나 메서드를 정의해야 합니다.

```php
/**
 * 초기화할 테이블 목록 지정.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는 초기화에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 정의하세요:

```php
/**
 * 초기화에서 제외할 테이블 목록 지정.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

초기화할 데이터베이스 연결을 지정하려면 `$connectionsToTruncate` 속성을 정의할 수 있습니다:

```php
/**
 * 테이블을 초기화할 데이터베이스 연결 목록 지정.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

초기화 작업 전후에 실행할 코드를 작성하려면 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 테스트 클래스에 정의하세요:

```php
/**
 * 데이터베이스 초기화 전에 실행할 작업.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * 데이터베이스 초기화 후에 실행할 작업.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행하기

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

지난번 테스트 실행 시 실패한 경우, 실패한 테스트부터 다시 실행하여 시간을 절약하려면 `dusk:fails` 명령어를 사용할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 실행기와 동일한 인수를 사용할 수 있습니다. 예를 들어 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)의 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> Laravel Sail로 로컬 개발 환경을 관리 중이라면, Sail 문서의 [Dusk 테스트 구성 및 실행](/docs/master/sail#laravel-dusk)도 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작하기

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려고 합니다. 자동 시작이 특정 환경에서 실패하면 직접 ChromeDriver를 실행한 후 `dusk` 명령을 실행하세요. 수동 시작 시 `tests/DuskTestCase.php` 파일에서 다음 줄을 주석 처리해야 합니다:

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

또한 ChromeDriver를 기본 포트 9515가 아닌 다른 포트에서 실행할 경우, 같은 클래스의 `driver` 메서드를 수정하여 올바른 포트를 반영해야 합니다:

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
### 환경 설정 처리

Dusk가 테스트 실행 시 자체 환경 파일을 사용하도록 하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 생성하세요. 예를 들어 `local` 환경에서 `dusk` 명령을 실행한다면 `.env.dusk.local` 파일을 만들어야 합니다.

테스트 실행 중 Dusk는 기존 `.env` 파일을 백업하고 `.env.dusk.{environment}` 파일을 `.env`로 임시 변경합니다. 테스트가 끝나면 원래 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본사항

<a name="creating-browsers"></a>
### 브라우저 생성하기

시작하기 위해 로그인할 수 있는지 확인하는 테스트를 작성해보겠습니다. 테스트를 생성한 후 로그인 페이지로 이동해 자격 증명을 입력하고 "Login" 버튼을 클릭하는 식으로 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내에서 `browse` 메서드를 호출하세요:

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

위 예시에서 보듯 `browse` 메서드는 클로저를 인수로 받습니다. Dusk는 이 클로저에 브라우저 인스턴스를 자동으로 전달하며, 해당 인스턴스를 통해 애플리케이션과 상호작용하고 단언할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성하기

때때로 테스트 수행을 위해 여러 브라우저 인스턴스가 필요할 수 있습니다. 예를 들어, WebSocket과 연동하는 채팅 화면을 테스트할 때 여러 브라우저 인스턴스가 필요합니다. `browse` 메서드에 클로저를 넘길 때, 브라우저 인자를 여러 개 추가하면 됩니다:

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

`visit` 메서드는 애플리케이션 내 특정 URI로 이동할 때 사용합니다:

```php
$browser->visit('/login');
```

`visitRoute` 메서드는 [이름이 지정된 라우트](/docs/master/routing#named-routes)로 이동할 때 사용합니다:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`과 `forward` 메서드를 사용해 브라우저 탐색기능인 뒤로, 앞으로 이동을 제어할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드는 페이지를 새로고침합니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메서드를 이용해 브라우저 창 크기를 조정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드는 브라우저 창을 최대화합니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창 크기를 페이지 콘텐츠 크기에 맞게 조정합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 스크린샷 전 창 크기를 콘텐츠에 맞게 조절합니다. 이 기능을 비활성화하려면 테스트 내에서 `disableFitOnFailure` 메서드를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드는 브라우저 창을 지정한 위치로 이동시킵니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

테스트 내 여러 곳에서 재사용 가능한 사용자 지정 브라우저 메서드를 정의하고 싶다면 `Browser` 클래스의 `macro` 메서드를 사용하세요. 보통 이는 애플리케이션의 [서비스 프로바이더](/docs/master/providers) `boot` 메서드에서 호출합니다:

```php
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
```

`macro` 메서드는 첫번째 인수로 이름, 두번째 인수로 클로저를 받습니다. 정의한 매크로는 `Browser` 인스턴스에서 해당 이름의 메서드를 호출할 때 실행됩니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증

로그인해야만 접근 가능한 페이지를 테스트할 때는 매번 로그인 화면을 거치는 대신 Dusk의 `loginAs` 메서드를 사용해 인증 과정을 생략할 수 있습니다. `loginAs`는 인증 가능한 모델의 기본 키 또는 모델 인스턴스를 인수로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용하면, 해당 테스트 파일 내 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드는 암호화된 쿠키의 값을 읽거나 설정할 수 있습니다. Laravel이 생성하는 쿠키는 기본적으로 암호화되어 있습니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` 메서드는 암호화하지 않은 쿠키 값을 읽거나 설정할 때 사용합니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메서드는 지정한 쿠키를 삭제합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행

`script` 메서드를 이용해 브라우저 내에서 임의의 자바스크립트를 실행할 수 있습니다:

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

`screenshot` 메서드는 스크린샷을 찍어 지정한 파일명으로 저장합니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 해상도별 브레이크포인트에서 여러 장의 스크린샷을 찍습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드는 특정 페이지 요소만 스크린샷으로 저장합니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장하기

`storeConsoleLog` 메서드는 현재 브라우저 콘솔 로그를 지정한 파일명으로 저장합니다. 저장 위치는 `tests/Browser/console` 디렉토리입니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장하기

`storeSource` 메서드는 현재 페이지의 HTML 소스 코드를 지정한 파일명으로 저장합니다. 저장 위치는 `tests/Browser/source` 디렉토리입니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기

<a name="dusk-selectors"></a>
### Dusk 셀렉터

효과적인 CSS 셀렉터를 선택해 요소를 조작하는 것은 Dusk 테스트 작성의 가장 어려운 부분 중 하나입니다. 프런트엔드 변경으로 인해 다음 같은 셀렉터가 깨질 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// 테스트...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면 CSS 셀렉터를 기억하는 대신 테스트 작성에 집중할 수 있습니다. HTML 요소에 `dusk` 속성을 추가해 셀렉터를 정의하세요. 그런 다음 Dusk 브라우저에서 이 셀렉터 앞에 `@`를 붙여 테스트 내에서 해당 요소를 다룰 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// 테스트...

$browser->click('@login-button');
```

필요 시, `selectorHtmlAttribute` 메서드로 Dusk 셀렉터가 사용하는 HTML 속성명을 변경할 수 있습니다. 일반적으로 애플리케이션의 `AppServiceProvider` `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 읽기와 설정

Dusk는 페이지 내 요소의 현재 값, 표시 텍스트, 속성 값을 다루기 위한 여러 메서드를 제공합니다. 예를 들어, 특정 CSS 또는 Dusk 셀렉터에 대응하는 요소의 "value"를 가져오려면 `value` 메서드를 사용하세요:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드는 이름이 지정된 입력 필드의 값을 쉽게 가져올 수 있습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드는 해당 셀렉터의 요소에서 표시되는 텍스트를 가져옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

`attribute` 메서드는 주어진 셀렉터 요소의 특정 속성 값을 가져옵니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기

<a name="typing-values"></a>
#### 값 입력하기

Dusk는 폼과 입력 요소와 상호작용하기 위한 다양한 메서드를 제공합니다. 예를 들어 텍스트 필드에 값을 입력하려면 `type` 메서드가 있습니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

`type` 메서드는 CSS 셀렉터를 꼭 필요로 하진 않습니다. 만약 CSS 셀렉터를 제공하지 않으면, Dusk는 `name` 속성이 일치하는 `input` 또는 `textarea` 필드를 검색합니다.

기존 내용을 지우지 않고 텍스트를 덧붙일 때는 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력 필드 값을 지우려면 `clear` 메서드를 사용합니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드는 천천히 타이핑하는 효과를 냅니다. 기본적으로 키 입력 사이에 100밀리초 대기합니다. 간격을 조절하려면 세 번째 인수로 밀리초 단위를 넘기면 됩니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드도 비슷하게 텍스트를 천천히 덧붙입니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 메서드는 `select` 요소에서 값을 선택할 때 사용합니다. `type`과 마찬가지로 전체 CSS 셀렉터가 필요하지 않습니다. 선택할 때는 표시 텍스트가 아니라 옵션의 실제 값을 전달해야 합니다:

```php
$browser->select('size', 'Large');
```

두번째 인수를 빼면 랜덤 옵션이 선택됩니다:

```php
$browser->select('size');
```

두번째 인수에 배열을 전달하면 여러 옵션을 선택할 수도 있습니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스를 체크하려면 `check` 메서드를 사용하세요. 전체 CSS 셀렉터가 없어도 됩니다. 셀렉터가 없으면 `name` 속성이 일치하는 체크박스를 찾습니다:

```php
$browser->check('terms');
```

체크를 해제할 때는 `uncheck` 메서드를 사용합니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 입력 옵션을 선택하려면 `radio` 메서드를 사용하세요. 마찬가지로 전체 CSS 셀렉터가 없어도 됩니다. 셀렉터가 없으면 `name`과 `value` 속성이 일치하는 라디오를 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기

`file` 입력 요소에 파일을 첨부하려면 `attach` 메서드를 사용하세요. 전체 CSS 셀렉터가 없어도 됩니다. 없으면 `name` 속성과 일치하는 `file` 입력을 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> `attach` 기능을 사용하려면 서버에 `Zip` PHP 확장 모듈이 설치되어 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기

`press` 메서드는 페이지 내 버튼 요소를 클릭합니다. 인수로는 버튼의 표시 텍스트 혹은 CSS/Dusk 셀렉터를 사용할 수 있습니다:

```php
$browser->press('Login');
```

폼 제출 버튼은 클릭 후 비활성화됐다가 HTTP 요청이 완료되면 다시 활성화하는 경우가 많습니다. 버튼이 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용하세요:

```php
// 최대 5초 동안 버튼이 활성화될 때까지 대기...
$browser->pressAndWaitFor('Save');

// 최대 1초 동안 버튼이 활성화될 때까지 대기...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기

`clickLink` 메서드는 표시 텍스트가 주어진 링크를 클릭합니다:

```php
$browser->clickLink($linkText);
```

`seeLink` 메서드는 링크가 페이지에 보이는지 확인합니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드들은 내부적으로 jQuery를 사용합니다. 페이지에 jQuery가 없으면, Dusk가 테스트 실행 동안 자동으로 삽입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기

`keys` 메서드를 사용하면 `type` 메서드보다 복잡한 입력 시퀀스를 지정할 수 있습니다. 예를 들어, `shift` 키를 누른 상태에서 텍스트를 입력할 수 있습니다. 아래 예시에서 `shift` 키를 누른 채로 `taylor`를 입력 후 키를 떼고 `swift`를 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

또한 앱의 주요 CSS 셀렉터에 대해 키보드 단축키 조합을 보낼 수도 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` 같은 모든 수정자 키는 중괄호 `{}`로 감싸며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스 상수와 일치합니다. [GitHub에서 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)할 수 있습니다.

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk는 `withKeyboard` 메서드를 제공해 `Laravel\Dusk\Keyboard` 클래스를 통해 복잡한 키보드 상호작용을 플루언트하게 수행할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다:

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

키보드 상호작용에 대한 맞춤 매크로를 정의해 테스트 전반에서 재사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/master/providers) `boot` 메서드에서 등록합니다:

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
     * Dusk 키보드 매크로 등록.
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

`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받으며, 매크로 클로저는 `Keyboard` 인스턴스의 메서드로 호출될 때 실행됩니다:

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

`click` 메서드는 주어진 CSS 또는 Dusk 셀렉터에 해당하는 요소를 클릭합니다:

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 주어진 XPath 표현식에 맞는 요소를 클릭합니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저 화면 뷰포트 내 주어진 좌표에서 가장 위에 있는 요소를 클릭합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 마우스 더블 클릭을 시뮬레이트합니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` 메서드는 마우스 우클릭을 시뮬레이트합니다:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드는 마우스 버튼을 누른 상태로 유지합니다. 이후 `releaseMouse` 메서드를 호출하면 해제됩니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` 메서드는 브라우저 내 `ctrl+click` 이벤트를 시뮬레이트합니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### mouseover

`mouseover` 메서드는 마우스를 지정한 CSS나 Dusk 셀렉터의 요소 위로 이동시킵니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 한 요소를 다른 요소로 드래그합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

한 방향으로 드래그도 가능합니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

주어진 좌표만큼 오프셋을 주어 드래그할 수도 있습니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 대화상자

Dusk는 자바스크립트 대화상자와 상호작용할 여러 메서드를 제공합니다. 예를 들어 `waitForDialog` 메서드는 대화상자가 나타날 때까지 기다립니다. 대기할 최대 초수를 인수로 받을 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 대화상자가 표시되었고 지정한 메시지를 포함하는지 단언합니다:

```php
$browser->assertDialogOpened('Dialog message');
```

대화상자가 프롬프트를 포함한다면, `typeInDialog` 메서드로 입력할 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

열린 대화상자를 "확인" 버튼 클릭으로 닫으려면 `acceptDialog` 메서드를 사용하세요:

```php
$browser->acceptDialog();
```

"취소" 버튼 클릭으로 닫으려면 `dismissDialog` 메서드를 사용하세요:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용하기

iframe 내부 요소와 상호작용하려면 `withinFrame` 메서드를 사용하세요. 클로저 내에서 이루어지는 모든 상호작용은 지정한 iframe 영역에 국한됩니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정하기

특정 셀렉터 내에서 여러 작업을 수행하고 싶을 때 `with` 메서드를 사용하세요. 클로저 내 모든 작업은 원래 셀렉터 범위 안에서 수행됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때로는 현재 범위 외부에서 단언을 해야 할 수도 있습니다. 이때 `elsewhere` 또는 `elsewhereWhenAvailable` 메서드를 사용하세요:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 범위: body .table...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 범위: body .page-title...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 범위: body .page-title...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기하기

자바스크립트를 많이 사용하는 애플리케이션 테스트 시 특정 요소나 데이터가 준비될 때까지 기다려야 할 때가 많습니다. Dusk의 여러 메서드를 통해 페이지에 요소가 보이거나 특정 자바스크립트 표현식이 `true`가 될 때까지 대기할 수 있습니다.

<a name="waiting"></a>
#### 대기하기

일정 시간(밀리초)동안 단순히 테스트를 멈추려면 `pause` 메서드를 사용하세요:

```php
$browser->pause(1000);
```

조건이 `true`일 때만 대기하려면 `pauseIf`를 사용하세요:

```php
$browser->pauseIf(App::environment('production'), 1000);
```

조건이 `true`가 아닐 때만 대기하려면 `pauseUnless`를 사용합니다:

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor` 메서드는 지정한 셀렉터에 부합하는 요소가 페이지에 표시될 때까지 테스트 실행을 일시 중지합니다. 기본 대기 시간은 5초이며, 두 번째 인수로 원하는 타임아웃을 설정할 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitFor('.selector');

// 최대 1초 대기...
$browser->waitFor('.selector', 1);
```

특정 텍스트가 셀렉터에 포함될 때까지 대기하려면 `waitForTextIn`을 사용합니다:

```php
// 최대 5초 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

페이지에서 셀렉터가 사라질 때까지 기다리려면 `waitUntilMissing` 메서드를 사용하세요:

```php
// 최대 5초 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 대기...
$browser->waitUntilMissing('.selector', 1);
```

셀렉터가 활성화(사용 가능) 또는 비활성화될 때까지 기다릴 수도 있습니다:

```php
// 최대 5초 대기 활성화까지...
$browser->waitUntilEnabled('.selector');

// 최대 1초 대기 활성화까지...
$browser->waitUntilEnabled('.selector', 1);

// 최대 5초 대기 비활성화까지...
$browser->waitUntilDisabled('.selector');

// 최대 1초 대기 비활성화까지...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 준비될 때 범위 지정하기

모달 창이 열리고 "OK" 버튼을 누르는 등 특정 셀렉터가 있으면 즉시 작동해야 하는 경우, `whenAvailable` 메서드를 사용해 해당 셀렉터가 나타날 때까지 기다릴 수 있습니다. 클로저 내 작업은 원래 셀렉터 범위 내에 적용됩니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기하기

`waitForText` 메서드는 지정한 텍스트가 페이지에 나타날 때까지 대기합니다:

```php
// 최대 5초 대기...
$browser->waitForText('Hello World');

// 최대 1초 대기...
$browser->waitForText('Hello World', 1);
```

표시된 텍스트가 없어질 때까지 기다리려면 `waitUntilMissingText` 메서드를 사용하세요:

```php
// 최대 5초 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기하기

`waitForLink` 메서드는 지정한 링크 텍스트가 나타날 때까지 대기합니다:

```php
// 최대 5초 대기...
$browser->waitForLink('Create');

// 최대 1초 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기하기

`waitForInput` 메서드는 지정한 필드가 페이지에 보일 때까지 대기합니다:

```php
// 최대 5초 대기...
$browser->waitForInput($field);

// 최대 1초 대기...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기하기

`assertPathIs('/home')` 같은 경로 단언은 `window.location.pathname`이 비동기적으로 바뀌면 실패할 수 있습니다. 이럴 때 `waitForLocation` 메서드로 특정 위치가 될 때까지 기다리세요:

```php
$browser->waitForLocation('/secret');
```

완전한 URL 위치도 대기 가능합니다:

```php
$browser->waitForLocation('https://example.com/path');
```

이름이 지정된 라우트 위치도 대기할 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기하기

어떤 동작 후 페이지가 새로고침된다면 `waitForReload` 메서드를 사용하세요:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 새로고침까지 기다리는 `clickAndWaitForReload` 메서드도 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

특정 자바스크립트 표현식이 `true`가 될 때까지 기다리고 싶다면 `waitUntil` 메서드를 사용하세요. `return` 키워드나 세미콜론은 생략해도 됩니다:

```php
// 최대 5초 대기...
$browser->waitUntil('App.data.servers.length > 0');

// 최대 1초 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

`waitUntilVue`와 `waitUntilVueIsNot` 메서드는 [Vue 컴포넌트](https://vuejs.org)의 속성 값이 특정 조건을 만족할 때까지 대기합니다:

```php
// 주어진 값이 될 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 주어진 값이 아닐 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기

`waitForEvent` 메서드는 특정 자바스크립트 이벤트가 발생할 때까지 기다립니다:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 현재 스코프인 `body` 요소에 붙습니다. 스코프가 지정된 경우 해당 요소에 붙습니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    $iframe->waitForEvent('load');
});
```

특정 셀렉터에 이벤트를 걸 수도 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document`나 `window` 객체에서 발생하는 이벤트도 대기할 수 있습니다:

```php
// 문서 스크롤 이벤트 대기...
$browser->waitForEvent('scroll', 'document');

// 윈도우 리사이즈 이벤트(최대 5초 대기)...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백과 함께 대기하기

많은 "wait" 메서드는 내부적으로 `waitUsing` 메서드를 사용합니다. 직접 호출해 최대 대기 시간, 폴링 간격, 검사할 클로저, 실패 시 메시지를 지정할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 뷰로 스크롤하기

뷰 영역 밖에 있어서 클릭할 수 없는 요소를 화면 안으로 스크롤하려면 `scrollIntoView` 메서드를 사용하세요:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 단언(Assertions)

Dusk는 애플리케이션에 대해 다양한 단언 메서드를 제공합니다. 아래 목록에서 모두 확인할 수 있습니다:

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

<a name="assert-title"></a>
#### assertTitle

페이지 제목이 지정한 텍스트와 일치하는지 단언합니다:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 제목이 지정한 텍스트를 포함하는지 단언합니다:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리 문자열 제외)이 지정한 문자열과 일치하는지 단언합니다:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 지정한 스킴과 일치하는지 단언합니다:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 지정한 스킴과 일치하지 않는지 단언합니다:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트명이 지정한 호스트와 일치하는지 단언합니다:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트명이 지정한 호스트와 일치하지 않는지 단언합니다:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 지정한 포트와 일치하는지 단언합니다:

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 지정한 포트와 일치하지 않는지 단언합니다:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로가 지정한 경로로 시작하는지 단언합니다:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

현재 URL 경로가 지정한 경로로 끝나는지 단언합니다:

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

현재 URL 경로에 지정한 경로가 포함되어 있는지 단언합니다:

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 지정한 경로와 일치하는지 단언합니다:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 지정한 경로와 일치하지 않는지 단언합니다:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 지정한 [이름이 있는 라우트](/docs/master/routing#named-routes)와 일치하는지 단언합니다:

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

지정한 쿼리 문자열 파라미터가 존재하는지 단언합니다:

```php
$browser->assertQueryStringHas($name);
```

값까지 검사하려면:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

지정한 쿼리 문자열 파라미터가 존재하지 않는지 단언합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

현재 URL의 해시 조각이 지정한 부분과 일치하는지 단언합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

현재 URL의 해시 조각이 지정한 부분으로 시작하는지 단언합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

현재 URL의 해시 조각이 지정한 부분과 일치하지 않는지 단언합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

지정한 암호화된 쿠키가 존재하는지 단언합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

지정한 비암호화 쿠키가 존재하는지 단언합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

지정한 암호화 쿠키가 존재하지 않는지 단언합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

지정한 비암호화 쿠키가 존재하지 않는지 단언합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키의 값이 지정한 값과 일치하는지 단언합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

비암호화 쿠키의 값이 지정한 값과 일치하는지 단언합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

페이지에 지정한 텍스트가 보이는지 단언합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

페이지에 지정한 텍스트가 보이지 않는지 단언합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

지정한 셀렉터 안에 특정 텍스트가 있는지 단언합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

지정한 셀렉터 안에 특정 텍스트가 없는지 단언합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

지정한 셀렉터 안에 어떤 텍스트라도 존재하는지 단언합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

지정한 셀렉터 안에 텍스트가 전혀 없는지 단언합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
#### assertScript

자바스크립트 표현식이 특정 값을 반환하는지 단언합니다:

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

페이지 소스코드에 특정 코드가 포함되어 있는지 단언합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

페이지 소스코드에 특정 코드가 없는지 단언합니다:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

페이지 내에 지정한 링크가 존재하는지 단언합니다:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

페이지 내에 지정한 링크가 존재하지 않는지 단언합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

입력 필드가 지정한 값을 가지는지 단언합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

입력 필드가 지정한 값을 가지지 않는지 단언합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

체크박스가 체크된 상태인지 단언합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

체크박스가 체크되지 않은 상태인지 단언합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

체크박스가 불확정(indeterminate) 상태인지 단언합니다:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

라디오 버튼이 선택된 상태인지 단언합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

라디오 버튼이 선택되지 않은 상태인지 단언합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

드롭다운이 지정한 값을 선택한 상태인지 단언합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

드롭다운이 지정한 값을 선택하지 않은 상태인지 단언합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

지정한 배열에 포함된 값들이 선택지로 존재하는지 단언합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

지정한 배열에 포함된 값들이 선택지에 없는지 단언합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

지정한 값이 선택지에 포함되는지 단언합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

지정한 값이 선택지에 포함되지 않는지 단언합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

셀렉터에 해당하는 요소가 지정한 값을 가지는지 단언합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

셀렉터에 해당하는 요소가 지정한 값을 가지지 않는지 단언합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

셀렉터에 해당하는 요소가 지정한 속성을 지정한 값으로 가지는지 단언합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

셀렉터에 해당하는 요소가 특정 속성을 가지지 않는지 단언합니다:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

셀렉터에 해당하는 요소의 지정 속성 값에 특정 값이 포함되는지 단언합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

셀렉터에 해당하는 요소의 지정 속성 값에 특정 값이 포함되지 않는지 단언합니다:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

셀렉터에 해당하는 요소가 지정한 aria 속성에 특정 값을 가지는지 단언합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 가 있다면 다음과 같이 단언합니다:

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

셀렉터에 해당하는 요소가 지정한 data 속성에 특정 값을 가지는지 단언합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 가 있다면 다음과 같이 단언합니다:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### assertVisible

셀렉터에 해당하는 요소가 화면에 보이는지 단언합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

셀렉터에 해당하는 요소가 소스 내에 존재하는지 단언합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

셀렉터에 해당하는 요소가 소스 내에 존재하지 않는지 단언합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

셀렉터에 해당하는 요소가 화면에 표시되지 않는지 단언합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

지정한 이름을 가진 입력 필드가 존재하는지 단언합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

지정한 이름을 가진 입력 필드가 소스에 존재하지 않는지 단언합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

지정한 메시지를 가진 자바스크립트 대화상자가 열렸는지 단언합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

지정한 필드가 활성화되어 있는지 단언합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

지정한 필드가 비활성화되어 있는지 단언합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

지정한 버튼이 활성화되어 있는지 단언합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

지정한 버튼이 비활성화되어 있는지 단언합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

지정한 필드에 포커스가 맞춰져 있는지 단언합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

지정한 필드에 포커스가 맞춰져 있지 않은지 단언합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증된 상태인지 단언합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않은 상태인지 단언합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

지정한 사용자로 인증된 상태인지 단언합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Vue 컴포넌트 상태에 대해 단언할 수 있습니다. 예를 들어, 애플리케이션에 아래와 같은 Vue 컴포넌트가 있다고 가정합니다:

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

Vue 컴포넌트 상태에 대해 다음과 같이 단언할 수 있습니다:

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
 * 기본 Vue 테스트 예제.
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

Vue 컴포넌트의 특정 데이터 속성이 지정한 값과 다를 때 단언합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

Vue 컴포넌트의 데이터 속성이 배열이며 지정한 값을 포함하는지 단언합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

Vue 컴포넌트의 데이터 속성이 배열이며 지정한 값을 포함하지 않는지 단언합니다:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지

복잡한 테스트는 여러 동작을 순차적으로 수행해야 하며, 이는 테스트를 읽고 이해하기 어렵게 만듭니다. Dusk 페이지를 사용하면 특정 페이지에 대한 표현적인 동작을 정의해 단일 메서드 호출로 실행할 수 있습니다. 또한 페이지 또는 애플리케이션 전체에서 공통 셀렉터에 대한 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성하기

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 실행하세요. 모든 페이지 객체는 `tests/Browser/Pages` 디렉토리에 저장됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정하기

기본적으로 페이지는 `url`, `assert`, `elements` 세 가지 메서드를 가집니다. 여기서는 `url`과 `assert` 메서드를 설명합니다. `elements` 메서드는 [별칭 셀렉터](#shorthand-selectors) 항목에서 더 자세히 다룹니다.

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 나타내는 URL 경로를 반환해야 합니다. Dusk는 이 URL을 사용해 브라우저에서 페이지로 이동합니다:

```php
/**
 * 페이지 URL 반환.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert` 메서드는 브라우저가 실제 해당 페이지에 있는지 확인하기 위한 단언을 수행할 수 있습니다. 실제로 비워 둘 수 있지만, 원한다면 단언을 자유롭게 작성할 수 있습니다. 이 단언은 페이지에 접근 시 자동으로 실행됩니다:

```php
/**
 * 브라우저가 해당 페이지임을 단언.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 네비게이션하기

페이지가 정의되면 `visit` 메서드를 사용해 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

때로는 이미 특정 페이지에 있고, 그 페이지의 셀렉터와 메서드를 현재 테스트 컨텍스트에 불러와야 할 때가 있습니다. 예를 들어 버튼 클릭 후 명시적 네비게이션 없이 리다이렉트되는 경우입니다. 이때 `on` 메서드를 사용하여 페이지 정보를 로드할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 별칭 셀렉터

페이지 클래스의 `elements` 메서드는 페이지 내 임의의 CSS 셀렉터에 대한 간단한 별칭을 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드 별칭을 다음과 같이 정의할 수 있습니다:

```php
/**
 * 페이지 내 요소 별칭 반환.
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

별칭을 정의한 뒤에는 전체 CSS 셀렉터 대신 이 별칭을 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 별칭 셀렉터

Dusk를 설치하면 `tests/Browser/Pages` 디렉토리에 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드로 애플리케이션 전체 페이지에서 공통으로 사용할 별칭 셀렉터를 정의할 수 있습니다:

```php
/**
 * 사이트 전역 별칭 셀렉터 반환.
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

페이지에 기본 메서드 외에도 테스트 전반에 걸쳐 사용할 추가 메서드를 정의할 수 있습니다. 예를 들어 음악 관리 애플리케이션에서 플레이리스트를 생성하는 기능을 생각해보세요. 각 테스트에 동일한 로직을 계속 쓰기보다 페이지 클래스에 `createPlaylist` 메서드를 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 기타 페이지 메서드...

    /**
     * 새 플레이리스트 생성.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

정의한 메서드는 해당 페이지를 사용하는 어떤 테스트에서도 사용할 수 있습니다. 브라우저 인스턴스는 첫 번째 인수로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 '페이지 객체'와 비슷하지만, 탐색할 특정 URL에 묶이지 않고 애플리케이션 전반에서 중복 사용하는 UI 또는 기능 단위(예: 네비게이션 바, 알림창 등)에 적합합니다.

<a name="generating-components"></a>
### 컴포넌트 생성하기

`dusk:component` Artisan 명령어로 컴포넌트를 생성할 수 있습니다. 생성된 컴포넌트는 `tests/Browser/Components` 디렉토리에 위치합니다:

```shell
php artisan dusk:component DatePicker
```

예를 들어, 달력 컴포넌트는 여러 페이지에 쓰여 여러 테스트에서 매번 날짜 선택 로직을 작성하는 것이 번거롭습니다. 컴포넌트로 정의해 관련 로직을 한 곳에 묶을 수 있습니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * 컴포넌트 루트 셀렉터 반환.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * 브라우저에 컴포넌트가 존재함을 단언.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * 컴포넌트 내 요소 별칭 반환.
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
     * 지정한 날짜 선택.
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

컴포넌트를 정의하면 테스트 어디서든 간단히 날짜를 선택할 수 있으며, 로직이 바뀌더라도 컴포넌트만 수정하면 됩니다:

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
    /**
     * 기본 컴포넌트 테스트 예제.
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
## 지속적 통합(CI)

> [!WARNING]
> 대부분 Dusk CI 환경에서는 Laravel 애플리케이션을 내장 PHP 개발 서버(포트 8000)로 서빙할 것을 기대합니다. 따라서 CI 환경에 `APP_URL` 환경 변수를 `http://127.0.0.1:8000`로 설정해두세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI에서 테스트 실행하기

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 `app.json` 파일에 다음과 같이 Google Chrome 빌드팩과 스크립트를 추가하세요:

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

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 파일 구성을 사용하세요. Travis는 그래픽 환경이 아니므로 Chrome 브라우저를 실행하는 추가 작업이 필요합니다. 또한 PHP 내장 서버를 실행합니다:

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

[GitHub Actions](https://github.com/features/actions)로 Dusk 테스트를 구동하려면 다음 구성 파일을 출발점으로 활용할 수 있습니다. Travis CI처럼 내장 PHP 서버를 실행합니다:

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

[Chipper CI](https://chipperci.com)로 Dusk 테스트를 실행할 때 사용할 수 있는 기본 구성은 다음과 같습니다. PHP 내장 서버를 실행해 Laravel을 서빙하고 요청을 수신합니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Chrome 포함 빌드 환경
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

      # dusk 환경 파일 생성, APP_URL에 BUILD_HOST 반영
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

Chipper CI에서 Dusk 테스트 실행 및 데이터베이스 사용법 등 자세한 내용은 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.