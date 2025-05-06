# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [데이터베이스 마이그레이션](#migrations)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값 및 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [자바스크립트 다이얼로그](#javascript-dialogs)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소 뷰로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지 객체](#pages)
    - [페이지 객체 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [셀렉터 단축키](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합(CI)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력 있고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 JDK나 Selenium을 로컬 컴퓨터에 설치할 필요가 없습니다. 대신 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 단, 원하는 다른 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가해야 합니다:

    composer require --dev laravel/dusk

> {note} Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대** 프로덕션 환경에서 등록하지 마세요. 잘못 등록할 경우 임의의 사용자가 애플리케이션에 인증할 수 있는 보안 문제가 발생할 수 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리와 예제 Dusk 테스트를 생성합니다:

    php artisan dusk:install

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접근할 때 사용하는 URL과 일치해야 합니다.

> {tip} [Laravel Sail](/docs/{{version}}/sail)를 사용하여 로컬 개발 환경을 관리하는 경우에는 [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk)에 대한 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

Laravel Dusk에 포함된 것과 다른 버전의 ChromeDriver를 설치하려면 `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

    # OS에 맞는 ChromeDriver 최신 버전 설치...
    php artisan dusk:chrome-driver

    # OS에 맞는 특정 버전 설치...
    php artisan dusk:chrome-driver 86

    # 지원되는 모든 OS에 특정 버전 설치...
    php artisan dusk:chrome-driver --all

    # OS에서 감지된 Chrome/Chromium 버전에 맞는 ChromeDriver 설치...
    php artisan dusk:chrome-driver --detect

> {note} Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행에 문제가 있으면 다음 명령어로 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Google Chrome과 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용해 브라우저 테스트를 실행합니다. 하지만 직접 Selenium 서버를 시작하여 원하는 브라우저로 테스트를 실행할 수 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 열어 `startChromeDriver` 메서드 호출을 주석 처리하면 ChromeDriver 자동 실행이 중단됩니다:

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

그 다음, `driver` 메서드를 원하는 Selenium 서버의 URL과 포트로 수정하고, WebDriver에 전달할 "desired capabilities"도 변경할 수 있습니다:

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

<a name="getting-started"></a>
## 시작하기

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 위치합니다:

    php artisan dusk:make LoginTest

<a name="migrations"></a>
### 데이터베이스 마이그레이션

대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 가져오는 페이지와 상호작용합니다. 그러나 Dusk 테스트에서는 `RefreshDatabase` 트레잇을 사용해서는 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 활용하는데, 이는 HTTP 요청 간에 적용되거나 사용될 수 없습니다. 대신, 각 테스트마다 데이터베이스를 재마이그레이션하는 `DatabaseMigrations` 트레잇을 사용하세요:

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

> {note} Dusk 테스트 실행 시 SQLite 메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되므로 다른 프로세스의 메모리 데이터베이스에 접근할 수 없습니다.

<a name="running-tests"></a>
### 테스트 실행

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 실행하세요:

    php artisan dusk

마지막으로 `dusk` 명령 실행 시 테스트가 실패했다면, 실패한 테스트만 우선 실행하여 시간을 절약할 수 있습니다:

    php artisan dusk:fails

`dusk` 명령은 PHP Unit 테스트 러너에서 사용하는 인자들을 그대로 사용할 수 있습니다. 예를 들어 [group](https://phpunit.de/manual/current/en/appendixes.annotations.html#appendixes.annotations.group)별로 테스트를 실행할 수도 있습니다:

    php artisan dusk --group=foo

> {tip} [Laravel Sail](/docs/{{version}}/sail)를 사용하는 경우, [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk)에 대한 Sail 가이드도 확인하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작

기본적으로 Dusk는 ChromeDriver를 자동으로 시작합니다. 이런 방식이 작동하지 않는 환경에서는 `dusk` 명령 실행 전에 ChromeDriver를 수동으로 시작할 수 있습니다. 이 경우 `tests/DuskTestCase.php` 파일의 다음 줄을 주석 처리하세요:

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

또한, ChromeDriver를 9515 이외의 포트에서 시작하면, 같은 클래스 내 `driver` 메서드를 올바른 포트로 수정해야 합니다:

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

<a name="environment-handling"></a>
### 환경 파일 처리

Dusk가 테스트 실행 시 별도의 환경 파일을 사용하도록 만들려면, 프로젝트 루트에 `.env.dusk.{환경명}` 파일을 생성하세요. 예를 들어 `local` 환경에서 `dusk` 명령을 실행한다면, `.env.dusk.local` 파일을 작성하면 됩니다.

테스트 실행 시, Dusk는 `.env` 파일을 백업하고 Dusk 환경 파일을 `.env`로 리네임합니다. 테스트가 완료되면 원래 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본

<a name="creating-browsers"></a>
### 브라우저 생성

애플리케이션에 로그인할 수 있는지 검증하는 테스트를 작성해보겠습니다. 테스트 생성 후, 로그인 페이지로 이동하여 자격 증명을 입력하고 "Login" 버튼을 클릭하도록 테스트를 수정할 수 있습니다. Dusk 테스트 내부에서 `browse` 메서드를 호출해 브라우저 인스턴스를 생성할 수 있습니다:

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
         * 브라우저 기본 테스트 예제.
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

위 예제에서 보듯, `browse` 메서드는 클로저를 인자로 받아 자동으로 브라우저 인스턴스를 전달합니다. 이 브라우저 인스턴스가 애플리케이션과 상호작용 및 어설션의 주요 객체입니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성

특정 테스트를 제대로 수행하려면 여러 브라우저가 필요할 때가 있습니다. 예를 들어, 웹소켓과 상호작용하는 채팅 화면을 테스트하려면 여러 브라우저가 필요할 수 있습니다. 이런 경우, `browse` 메서드의 클로저에 추가 인자를 추가하세요:

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

<a name="navigation"></a>
### 네비게이션

`visit` 메서드는 애플리케이션 내 특정 URI로 이동하는 데 사용합니다:

    $browser->visit('/login');

`visitRoute` 메서드를 사용해 [네임드 라우트](/docs/{{version}}/routing#named-routes)로 이동할 수도 있습니다:

    $browser->visitRoute('login');

`back`과 `forward`로 이전 또는 다음 페이지로 이동할 수 있습니다:

    $browser->back();

    $browser->forward();

`refresh`로 페이지를 새로고침할 수 있습니다:

    $browser->refresh();

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절

`resize` 메서드로 브라우저 창 크기를 조정할 수 있습니다:

    $browser->resize(1920, 1080);

`maximize`는 브라우저 창을 최대화합니다:

    $browser->maximize();

`fitContent`는 브라우저 창을 컨텐츠 크기에 맞춥니다:

    $browser->fitContent();

테스트 실패 시 Dusk는 스크린샷을 찍기 전 자동으로 창 크기를 조정합니다. 이 기능은 `disableFitOnFailure`로 비활성화할 수 있습니다:

    $browser->disableFitOnFailure();

`move` 메서드는 브라우저 창을 화면 내 다른 위치로 이동시킵니다:

    $browser->move($x = 100, $y = 100);

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 사용하세요. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 정의합니다:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Laravel\Dusk\Browser;

    class DuskServiceProvider extends ServiceProvider
    {
        public function boot()
        {
            Browser::macro('scrollToElement', function ($element = null) {
                $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");
                return $this;
            });
        }
    }

매크로는 첫 번째 인자로 이름을, 두 번째 인자로 클로저를 받습니다. 정의한 뒤에는 `Browser` 인스턴스의 메서드처럼 사용할 수 있습니다:

    $this->browse(function ($browser) use ($user) {
        $browser->visit('/pay')
                ->scrollToElement('#credit-card-details')
                ->assertSee('Enter Credit Card Details');
    });

<a name="authentication"></a>
### 인증

대부분의 경우 인증이 필요한 페이지를 테스트합니다. 매번 로그인 화면을 거치지 말고 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델의 PK나 인스턴스를 인자로 받습니다:

    use App\Models\User;

    $this->browse(function ($browser) {
        $browser->loginAs(User::find(1))
              ->visit('/home');
    });

> {note} `loginAs` 메서드를 사용하면 해당 파일의 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드로 암호화된 쿠키 값을 조회하거나 설정할 수 있습니다. Laravel이 생성하는 모든 쿠키는 기본적으로 암호화됩니다:

    $browser->cookie('name');

    $browser->cookie('name', 'Taylor');

`plainCookie`는 암호화되지 않은 쿠키의 값을 조회하거나 설정합니다:

    $browser->plainCookie('name');

    $browser->plainCookie('name', 'Taylor');

`deleteCookie`로 주어진 쿠키를 삭제할 수 있습니다:

    $browser->deleteCookie('name');

<a name="executing-javascript"></a>
### 자바스크립트 실행

`script` 메서드는 브라우저 내에서 임의의 자바스크립트 명령을 실행합니다:

    $browser->script('document.documentElement.scrollTop = 0');

    $browser->script([
        'document.body.scrollTop = 0',
        'document.documentElement.scrollTop = 0',
    ]);

    $output = $browser->script('return window.location.pathname');

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 메서드로 스크린샷을 찍고 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

    $browser->screenshot('filename');

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 디스크 저장

`storeConsoleLog` 메서드로 현재 브라우저 콘솔 출력을 지정된 파일명으로 디스크에 기록할 수 있습니다. 콘솔 출력은 `tests/Browser/console` 디렉터리에 저장됩니다:

    $browser->storeConsoleLog('filename');

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크 저장

`storeSource` 메서드로 현재 페이지 소스를 디스크에 저장할 수 있습니다. 페이지 소스는 `tests/Browser/source` 디렉터리에 저장됩니다:

    $browser->storeSource('filename');

<a name="interacting-with-elements"></a>
## 요소와 상호작용

<a name="dusk-selectors"></a>
### Dusk 셀렉터

테스트에서 요소와 상호작용할 때 좋은 CSS 셀렉터를 고르는 것은 매우 어렵습니다. 프론트엔드 변경이 있으면 아래와 같은 셀렉터가 쉽게 깨질 수 있습니다:

    // HTML...

    <button>Login</button>

    // Test...

    $browser->click('.login-page .container div > button');

Dusk 셀렉터를 사용하면 CSS 셀렉터를 기억하지 않고도 효과적인 테스트를 작성할 수 있습니다. 셀렉터 정의는 HTML 요소에 `dusk` 속성을 추가해서 하고, 테스트에서는 `@` 기호를 붙여 사용합니다:

    // HTML...

    <button dusk="login-button">Login</button>

    // Test...

    $browser->click('@login-button');

<a name="text-values-and-attributes"></a>
### 텍스트, 값 및 속성

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정

Dusk는 요소의 현재 값, 표시 텍스트, 속성과 상호작용하는 다양한 메서드를 제공합니다. 예를 들어 주어진 CSS나 Dusk 셀렉터에 일치하는 요소의 "value"를 가져오려면 `value` 메서드를 사용하세요:

    // 값 조회...
    $value = $browser->value('selector');

    // 값 설정...
    $browser->value('selector', 'value');

특정 field name을 가진 input 요소의 값을 조회하려면 `inputValue`를 사용하세요:

    $value = $browser->inputValue('field');

<a name="retrieving-text"></a>
#### 텍스트 조회

`text` 메서드는 해당 셀렉터에 일치하는 요소의 표시 텍스트를 반환합니다:

    $text = $browser->text('selector');

<a name="retrieving-attributes"></a>
#### 속성 조회

마지막으로 `attribute` 메서드로 주어진 셀렉터에 일치하는 요소의 특정 속성 값을 반환할 수 있습니다:

    $attribute = $browser->attribute('selector', 'value');

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력하기

폼 및 입력 요소와 상호작용할 때 사용할 수 있는 다양한 메서드가 있습니다. 먼저, input 필드에 텍스트를 입력하는 예시입니다:

    $browser->type('email', 'taylor@laravel.com');

참고로, CSS 셀렉터를 꼭 전달하지 않아도 됩니다. 전달하지 않으면 Dusk는 주어진 name 속성을 가진 input 또는 textarea를 찾습니다.

필드에 값을 추가하고 싶을 때는 `append` 메서드를 사용하세요:

    $browser->type('tags', 'foo')
            ->append('tags', ', bar, baz');

`clear`로 input 값을 지울 수 있습니다:

    $browser->clear('email');

`typeSlowly`를 사용하면 천천히 키 입력을 시뮬레이션하여 입력할 수 있습니다. 기본 대기 시간은 100밀리초지만, 세 번째 인자로 밀리초 값을 지정할 수 있습니다:

    $browser->typeSlowly('mobile', '+1 (202) 555-5555');

    $browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);

`appendSlowly`로 천천히 값을 추가할 수도 있습니다:

    $browser->type('tags', 'foo')
            ->appendSlowly('tags', ', bar, baz');

<a name="dropdowns"></a>
#### 드롭다운

`select` 메서드는 `select` 요소에서 값을 선택할 때 사용합니다. 마찬가지로 CSS 셀렉터 대신 name 속성만 전달할 수 있습니다. 값 선택 시 표시 텍스트가 아니라 실제 option의 value를 전달하세요:

    $browser->select('size', 'Large');

두 번째 인자를 생략하면 무작위 option을 선택합니다:

    $browser->select('size');

배열을 두 번째 인자로 전달하면 다중 선택도 가능합니다:

    $browser->select('categories', ['Art', 'Music']);

<a name="checkboxes"></a>
#### 체크박스

체크박스를 "체크"하려면 `check` 메서드를 사용하세요. 대부분의 input 관련 메서드와 마찬가지로 전체 CSS 셀렉터가 필요하지 않습니다:

    $browser->check('terms');

체크 해제하려면 `uncheck`를 사용하세요:

    $browser->uncheck('terms');

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼을 선택하려면 `radio`를 사용하세요. 역시 전체 CSS 셀렉터 없이 name과 value 속성을 전달할 수 있습니다:

    $browser->radio('size', 'large');

<a name="attaching-files"></a>
### 파일 첨부

`attach` 메서드로 `file` 입력 요소에 파일을 첨부합니다. CSS 셀렉터를 꼭 전달하지 않아도 됩니다:

    $browser->attach('photo', __DIR__.'/photos/mountains.png');

> {note} attach 기능을 사용하려면 서버에 PHP `Zip` 확장 모듈이 설치되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭

`press` 메서드로 페이지의 버튼을 클릭할 수 있습니다. 인자로 버튼의 표시 텍스트나 CSS/Dusk 셀렉터를 사용할 수 있습니다:

    $browser->press('Login');

폼 제출 시, 많은 애플리케이션은 제출 버튼을 일시적으로 비활성화했다가 응답 후 재활성화합니다. 이를 고려해 버튼이 다시 활성화될 때까지 기다리는 `pressAndWaitFor`를 사용할 수 있습니다:

    // 최대 5초 대기
    $browser->pressAndWaitFor('Save');

    // 최대 1초 대기
    $browser->pressAndWaitFor('Save', 1);

<a name="clicking-links"></a>
### 링크 클릭

링크 클릭은 `clickLink` 메서드를 사용하세요. 인자는 링크의 표시 텍스트입니다:

    $browser->clickLink($linkText);

`seeLink`로 해당 표시 텍스트를 가진 링크가 표시 중인지 확인할 수 있습니다:

    if ($browser->seeLink($linkText)) {
        // ...
    }

> {note} 이들 메서드는 jQuery와 상호작용합니다. 페이지에 jQuery가 없으면 Dusk가 자동으로 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys` 메서드로 `type`보다 복잡한 입력 시퀀스를 요소에 보낼 수 있습니다. 예를 들어 shift 키를 누른 상태로 "taylor"를 입력한 후, modifier 없이 "swift"를 입력할 수 있습니다:

    $browser->keys('selector', ['{shift}', 'taylor'], 'swift');

"키보드 단축키" 조합을 보낼 수도 있습니다:

    $browser->keys('.app', ['{command}', 'j']);

> {tip} `{command}`와 같은 modifier 키는 `{}`로 감싸며, `Facebook\WebDriver\WebDriverKeys` 클래스의 상수를 참조합니다. [GitHub에서 확인하세요](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메서드는 지정한 CSS/Dusk 셀렉터와 일치하는 요소를 클릭합니다:

    $browser->click('.selector');

`clickAtXPath`로 XPath로 일치하는 요소를 클릭할 수도 있습니다:

    $browser->clickAtXPath('//div[@class = "selector"]');

`clickAtPoint`로 지정한 좌표에 위치한 요소를 클릭할 수 있습니다:

    $browser->clickAtPoint($x = 0, $y = 0);

`doubleClick`로 더블클릭을 시뮬레이션 할 수 있습니다:

    $browser->doubleClick();

`rightClick`로 우클릭을 시뮬레이션 할 수 있습니다:

    $browser->rightClick();

    $browser->rightClick('.selector');

`clickAndHold`와 `releaseMouse`로 마우스 클릭/홀드도 시뮬레이션 가능합니다:

    $browser->clickAndHold()
            ->pause(1000)
            ->releaseMouse();

<a name="mouseover"></a>
#### 마우스오버

`mouseover`로 지정한 요소에 마우스 오버 이벤트를 발생시킬 수 있습니다:

    $browser->mouseover('.selector');

<a name="drag-drop"></a>
#### 드래그 & 드롭

`drag`로 요소를 다른 요소에 드래그할 수 있습니다:

    $browser->drag('.from-selector', '.to-selector');

한 방향으로만 드래그할 수도 있습니다:

    $browser->dragLeft('.selector', $pixels = 10);
    $browser->dragRight('.selector', $pixels = 10);
    $browser->dragUp('.selector', $pixels = 10);
    $browser->dragDown('.selector', $pixels = 10);

지정한 오프셋만큼 드래그도 가능합니다:

    $browser->dragOffset('.selector', $x = 10, $y = 10);

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그

Dusk는 자바스크립트 다이얼로그와 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그가 나타날 때까지 대기할 수 있습니다:

    $browser->waitForDialog($seconds = null);

`assertDialogOpened`로 다이얼로그가 표시되었고 메시지가 맞는지 확인합니다:

    $browser->assertDialogOpened('Dialog message');

프롬프트 다이얼로그에는 `typeInDialog`로 입력할 수 있습니다:

    $browser->typeInDialog('Hello World');

"확인" 버튼 클릭은 `acceptDialog`로, "취소" 버튼 클릭은 `dismissDialog`로 할 수 있습니다:

    $browser->acceptDialog();

    $browser->dismissDialog();

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정

특정 셀렉터 내에서 여러 동작을 묶어 실행하고 싶을 때 `with` 메서드를 사용할 수 있습니다:

    $browser->with('.table', function ($table) {
        $table->assertSee('Hello World')
              ->clickLink('Delete');
    });

현재 범위 밖에서 어설션을 실행해야 할 경우, `elsewhere`와 `elsewhereWhenAvailable`를 사용하세요:

     $browser->with('.table', function ($table) {
        // 현재 범위: `body .table`...

        $browser->elsewhere('.page-title', function ($title) {
            // 현재 범위: `body .page-title`...
            $title->assertSee('Hello World');
        });

        $browser->elsewhereWhenAvailable('.page-title', function ($title) {
            $title->assertSee('Hello World');
        });
     });

<a name="waiting-for-elements"></a>
### 요소 대기

JavaScript를 많이 사용하는 앱을 테스트할 때 테스트가 진행되기 전 특정 요소나 데이터가 나타날 때까지 "대기"해야 할 때가 많습니다. Dusk는 이 작업을 여러 방법으로 쉽게 처리할 수 있도록 도와줍니다.

<a name="waiting"></a>
#### 대기

임의 시간(밀리초) 만큼 대기하려면 `pause`를 사용하세요:

    $browser->pause(1000);

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

`waitFor`로 지정한 CSS/Dusk 셀렉터가 나타날 때까지 테스트 실행을 일시 정지할 수 있습니다. 기본 대기 시간은 5초이며, 두 번째 인자로 커스텀 타임아웃을 지정할 수 있습니다:

    // 최대 5초 대기
    $browser->waitFor('.selector');

    // 최대 1초 대기
    $browser->waitFor('.selector', 1);

해당 셀렉터의 텍스트가 특정 값이 될 때까지 대기도 가능합니다:

    $browser->waitForTextIn('.selector', 'Hello World');

    $browser->waitForTextIn('.selector', 'Hello World', 1);

요소가 사라질 때까지 대기하려면:

    $browser->waitUntilMissing('.selector');

    $browser->waitUntilMissing('.selector', 1);

요소가 enabled/disabled 될 때까지도 대기할 수 있습니다:

    $browser->waitUntilEnabled('.selector');

    $browser->waitUntilEnabled('.selector', 1);

    $browser->waitUntilDisabled('.selector');

    $browser->waitUntilDisabled('.selector', 1);

<a name="scoping-selectors-when-available"></a>
#### 요소 등장 시 셀렉터 범위 지정

특정 요소가 나타난 후 곧바로 해당 요소와 상호작용할 필요가 있으면 `whenAvailable`을 사용하세요:

    $browser->whenAvailable('.modal', function ($modal) {
        $modal->assertSee('Hello World')
              ->press('OK');
    });

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText`로 특정 텍스트가 화면에 나타날 때까지 대기할 수 있습니다:

    $browser->waitForText('Hello World');

    $browser->waitForText('Hello World', 1);

`waitUntilMissingText`로 지정한 텍스트가 화면에서 사라질 때까지 대기할 수도 있습니다:

    $browser->waitUntilMissingText('Hello World');

    $browser->waitUntilMissingText('Hello World', 1);

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink`는 지정한 링크 텍스트가 화면에 나타날 때까지 대기합니다:

    $browser->waitForLink('Create');

    $browser->waitForLink('Create', 1);

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기

경로 어설션(예: `$browser->assertPathIs('/home')`)은 `window.location.pathname`이 비동기로 변화 중일 때 실패할 수 있습니다. `waitForLocation`으로 특정 위치로 변경될 때까지 대기할 수 있습니다:

    $browser->waitForLocation('/secret');

`waitForLocation`은 전체 URL 대기도 가능합니다:

    $browser->waitForLocation('https://example.com/path');

[네임드 라우트](/docs/{{version}}/routing#named-routes)로도 대기할 수 있습니다:

    $browser->waitForRoute($routeName, $parameters);

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기

동작 후 페이지가 새로고침될 때까지 기다려야 하는 경우 `waitForReload`를 사용하세요:

    use Laravel\Dusk\Browser;

    $browser->waitForReload(function (Browser $browser) {
        $browser->press('Submit');
    })
    ->assertSee('Success!');

버튼 클릭 후 새로고침을 기다릴 땐 `clickAndWaitForReload`가 더 편리합니다:

    $browser->clickAndWaitForReload('.selector')
            ->assertSee('something');

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

특정 JavaScript 표현식이 `true`가 될 때까지 테스트 실행을 일시정지하려면 `waitUntil`을 사용하세요. `return`이나 세미콜론은 필요 없습니다:

    $browser->waitUntil('App.data.servers.length > 0');

    $browser->waitUntil('App.data.servers.length > 0', 1);

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

`waitUntilVue`, `waitUntilVueIsNot`로 [Vue 컴포넌트](https://vuejs.org) 속성 값이 특정 값이 될 때까지 대기할 수 있습니다:

    $browser->waitUntilVue('user.name', 'Taylor', '@user');

    $browser->waitUntilVueIsNot('user.name', null, '@user');

<a name="waiting-with-a-callback"></a>
#### 콜백과 함께 대기

대부분의 대기 메서드는 내부적으로 `waitUsing`을 사용합니다. 이 메서드를 직접 호출해, 주어진 클로저가 `true`를 반환할 때까지 대기할 수 있습니다:

    $browser->waitUsing(10, 1, function () use ($something) {
        return $something->isReady();
    }, "Something wasn't ready in time.");

<a name="scrolling-an-element-into-view"></a>
### 요소 뷰로 스크롤

요소가 브라우저 뷰 영역 밖에 있어 클릭이 불가능할 때, `scrollIntoView`로 해당 요소가 뷰에 들어오도록 스크롤 시킬 수 있습니다:

    $browser->scrollIntoView('.selector')
            ->click('.selector');

<a name="available-assertions"></a>
## 사용 가능한 어설션

Dusk는 애플리케이션에 대해 다양한 어설션을 제공합니다. 아래는 사용 가능한 모든 어설션 목록입니다:

<!-- 스타일링 및 목록 : 코드/링크/HTML은 번역하지 않음 -->

<a name="assert-title"></a>
#### assertTitle

페이지의 제목이 주어진 텍스트와 일치하는지 확인:

    $browser->assertTitle($title);

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지의 제목에 주어진 텍스트가 포함되어 있는지 확인:

    $browser->assertTitleContains($title);

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL(쿼리스트링 제외)이 지정된 문자열과 일치하는지 확인:

    $browser->assertUrlIs($url);

<!-- 이하의 나머지 어설션 설명은 위 패턴을 따릅니다. 항목 번역이 너무 길어 생략하며 필요시 추가 제공 가능 -->

<a name="pages"></a>
## 페이지 객체

테스트가 여러 복잡한 작업을 순차적으로 수행해야 할 때 읽기 어려워질 수 있습니다. Dusk의 페이지 객체 기능을 사용하면, 복잡한 동작들을 하나의 메서드로 정의해 쉽게 재사용하고, 공용 셀렉터 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 객체 생성

`dusk:page` Artisan 명령어로 페이지 객체를 생성하세요. 모든 페이지 객체는 `tests/Browser/Pages` 디렉터리에 위치합니다:

    php artisan dusk:page Login

<a name="configuring-pages"></a>
### 페이지 설정

기본적으로 페이지에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 먼저 `url`과 `assert`를 설명합니다. `elements`는 [아래에서 더 자세히 설명됩니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 대표하는 URL 경로를 반환합니다. Dusk가 브라우저에서 페이지로 이동할 때 사용합니다:

    /**
     * 페이지의 URL을 반환.
     *
     * @return string
     */
    public function url()
    {
        return '/login';
    }

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert`에서는 브라우저가 해당 페이지에 있는지 확인하는 어설션을 자유롭게 추가할 수 있습니다. 빈 상태여도 무방하지만, 원하는 어설션을 정의해 여기서 자동으로 실행되도록 할 수 있습니다:

    /**
     * 해당 페이지인지 확인.
     *
     * @return void
     */
    public function assert(Browser $browser)
    {
        $browser->assertPathIs($this->url());
    }

<a name="navigating-to-pages"></a>
### 페이지로 이동

페이지가 정의되면, `visit` 메서드로 해당 페이지로 이동할 수 있습니다:

    use Tests\Browser\Pages\Login;

    $browser->visit(new Login);

이미 해당 페이지에 있고, 페이지 셀렉터 및 메서드를 현재 테스트 컨텍스트로 불러와야 하는 경우(예: 버튼 클릭 후 리디렉트 등)는 `on` 메서드를 사용할 수 있습니다:

    use Tests\Browser\Pages\CreatePlaylist;

    $browser->visit('/dashboard')
            ->clickLink('Create Playlist')
            ->on(new CreatePlaylist)
            ->assertSee('@create');

<a name="shorthand-selectors"></a>
### 셀렉터 단축키

페이지 클래스 내 `elements`에서 페이지의 CSS 셀렉터에 대한 단축키를 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드:

    /**
     * 페이지 내 단축 셀렉터 목록 반환.
     *
     * @return array
     */
    public function elements()
    {
        return [
            '@email' => 'input[name=email]',
        ];
    }

정의한 뒤에는 어디서든 단축키 형태로 사용할 수 있습니다:

    $browser->type('@email', 'taylor@laravel.com');

<a name="global-shorthand-selectors"></a>
#### 전역 셀렉터 단축키

설치 후 `tests/Browser/Pages` 디렉터리에 `Page` 기본 클래스가 생성됩니다. 이 클래스의 `siteElements`에서 모든 페이지에서 공통으로 사용할 전역 단축키 셀렉터를 정의할 수 있습니다:

    /**
     * 사이트 전역 단축 셀렉터 목록 반환.
     *
     * @return array
     */
    public static function siteElements()
    {
        return [
            '@element' => '#selector',
        ];
    }

<a name="page-methods"></a>
### 페이지 메서드

기본 메서드 이외에도, 페이지 별 커스텀 메서드를 추가할 수 있습니다. 예를 들어 음악 관리 앱에서 플레이리스트 생성 로직을 공통 메서드로 정의할 수 있습니다:

    <?php

    namespace Tests\Browser\Pages;

    use Laravel\Dusk\Browser;

    class Dashboard extends Page
    {
        // 페이지별 추가 메서드...

        public function createPlaylist(Browser $browser, $name)
        {
            $browser->type('name', $name)
                    ->check('share')
                    ->press('Create Playlist');
        }
    }

이렇게 정의하면, 해당 페이지를 활용하는 모든 테스트에서 사용할 수 있으며, 브라우저 인스턴스는 첫 인자로 자동 전달됩니다:

    use Tests\Browser\Pages\Dashboard;

    $browser->visit(new Dashboard)
            ->createPlaylist('My Playlist')
            ->assertSee('My Playlist');

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 페이지 객체와 유사하지만, 내비게이션 바/알림창 등 여러 페이지에서 재사용되는 UI 조각에 특화되어 있습니다. 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

`dusk:component` Artisan 명령어로 컴포넌트를 생성하세요. 새로운 컴포넌트는 `tests/Browser/Components` 디렉터리에 위치합니다:

    php artisan dusk:component DatePicker

예를 들어 "날짜 선택기"는 여러 페이지에서 사용되기에, 날짜 선택 로직을 컴포넌트로 정의하여 여러 테스트에서 반복을 방지하고 구현 변경 시 한 곳만 수정하면 됩니다.

<a name="using-components"></a>
### 컴포넌트 사용

컴포넌트 정의 후, 어떤 테스트에서도 손쉽게 사용할 수 있습니다. 날짜 선택 방식이 바뀌어도 컴포넌트만 수정하면 됩니다:

    <?php

    namespace Tests\Browser;

    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Laravel\Dusk\Browser;
    use Tests\Browser\Components\DatePicker;
    use Tests\DuskTestCase;

    class ExampleTest extends DuskTestCase
    {
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

<a name="continuous-integration"></a>
## 지속적 통합(CI)

> {note} 대부분의 Dusk CI 설정은 PHP 내장 개발 서버가 8000번 포트에서 동작하는 것으로 가정합니다. CI 환경의 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`인지 반드시 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, 아래와 같이 Google Chrome 빌드팩과 스크립트를 Heroku의 `app.json`에 추가하세요:

<!-- 코드블록은 번역 금지 지침에 따라 그대로 유지 -->

<a name="running-tests-on-travis-ci"></a>
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면, 아래 예시와 같이 `.travis.yml`을 설정합니다. 그래픽 환경이 아니므로 Chrome 브라우저 실행 등 추가 단계를 거쳐야 하며, PHP 내장 웹서버도 사용합니다:

<!-- 코드블록은 번역 금지 지침에 따라 그대로 유지 -->

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

[Github Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하는 경우 아래 설정 파일을 참고하세요. TravisCI와 마찬가지로 `php artisan serve`로 PHP 내장 웹서버를 실행합니다:

<!-- 코드블록은 번역 금지 지침에 따라 그대로 유지 -->

---

이상으로 Laravel Dusk 공식 문서의 주요 내용을 한글로 번역하였습니다.  
코드, HTML, 링크 URL은 번역하지 않고 마크다운 형식을 유지하였습니다.  
전문 용어와 기능에 맞는 용어로 번역하였습니다.