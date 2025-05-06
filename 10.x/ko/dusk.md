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
- [브라우저 기본](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 로그 디스크 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [Dusk 선택자](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [자바스크립트 다이얼로그](#javascript-dialogs)
    - [iFrame과 상호작용](#interacting-with-iframes)
    - [선택자 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어서션 목록](#available-assertions)
- [페이지 객체](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [축약 선택자](#shorthand-selectors)
    - [페이지 메소드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적인 통합(CI)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개

[Laravel Dusk](https://github.com/laravel/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요 없이 사용할 수 있습니다. 대신 독립형 [ChromeDriver](https://sites.google.com/chromium.org/driver)가 사용됩니다. 물론 원한다면 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 [Google Chrome](https://www.google.com/chrome)을 설치하고, 프로젝트에 `laravel/dusk` Composer 의존성을 추가하세요:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]  
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대** 프로덕션 환경에 등록하지 마세요. 등록 시 임의의 사용자가 애플리케이션에 인증할 수 있는 위험이 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령을 실행합니다. 이 명령은 `tests/Browser` 디렉터리와 예시 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 생성합니다:

```shell
php artisan dusk:install
```

그 다음, 애플리케이션 `.env` 파일에서 `APP_URL` 환경변수를 설정합니다. 이 값은 브라우저에서 접속하는 URL과 일치해야 합니다.

> [!NOTE]  
> [Laravel Sail](/docs/{{version}}/sail)을 사용하여 로컬 개발 환경을 관리한다면, [Dusk 테스트 설정 및 실행에 대해]( /docs/{{version}}/sail#laravel-dusk ) Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

Laravel Dusk에서 `dusk:install` 명령으로 설치된 ChromeDriver와 다른 버전을 사용하려면 `dusk:chrome-driver` 명령을 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 설치
php artisan dusk:chrome-driver

# 특정 버전 설치
php artisan dusk:chrome-driver 86

# 모든 운영체제에 지원되는 버전 설치
php artisan dusk:chrome-driver --all

# Chrome/Chromium 버전에 맞는 ChromeDriver를 자동 감지하여 설치
php artisan dusk:chrome-driver --detect
```

> [!WARNING]  
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. 실행 중 문제가 있다면, 다음 명령어로 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 Chrome과 ChromeDriver를 사용하지만, 직접 Selenium 서버를 실행하고 원하는 브라우저로 테스트를 실행할 수 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스 파일인 `tests/DuskTestCase.php`를 엽니다. 이 파일에서 `startChromeDriver` 메소드 호출을 주석 처리하여 Dusk가 ChromeDriver를 자동으로 시작하지 않도록 할 수 있습니다:

    /**
     * Dusk 테스트 실행 준비.
     *
     * @beforeClass
     */
    public static function prepare(): void
    {
        // static::startChromeDriver();
    }

다음으로, 원하는 URL과 포트에 연결하고자 `driver` 메소드도 수정할 수 있습니다. 그리고 WebDriver로 전달될 "기대 속성(desired capabilities)"도 변경할 수 있습니다:

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
### 테스트 생성하기

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령을 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 불러오는 페이지와 상호작용하게 됩니다. 그러나 Dusk 테스트는 `RefreshDatabase` 트레이트를 사용해서는 안 됩니다. `RefreshDatabase`는 데이터베이스 트랜잭션을 이용하는데, 이는 HTTP 요청 간에 적용되거나 사용 불가할 수 있습니다. 대신 `DatabaseMigrations` 트레이트 또는 `DatabaseTruncation` 트레이트를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 그러나 각 테스트마다 테이블을 드롭하고 재생성하는 것은 단순히 테이블을 비우는 것(truncate)보다 더 느릴 수 있습니다.

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

> [!WARNING]  
> Dusk 테스트 실행 시 SQLite 메모리 데이터베이스 사용은 불가합니다. 브라우저가 별도의 프로세스에서 실행되므로 다른 프로세스의 메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 Truncation 사용

`DatabaseTruncation` 트레이트를 사용하기 전에, Composer로 `doctrine/dbal` 패키지를 설치해야 합니다:

```shell
composer require --dev doctrine/dbal
```

`DatabaseTruncation` 트레이트는 최초 테스트에서 데이터베이스를 마이그레이션하여 테이블이 준비됐는지 확인합니다. 그 다음 테스트부터는 단순히 테이블을 truncate하여 속도가 향상됩니다.

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 truncate합니다. truncate할 테이블을 커스터마이징하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

    /**
     * truncate할 테이블
     *
     * @var array
     */
    protected $tablesToTruncate = ['users'];

반대로, 제외할 테이블이 있다면 `$exceptTables` 속성을 명시하세요:

    /**
     * truncate에서 제외할 테이블
     *
     * @var array
     */
    protected $exceptTables = ['users'];

truncate할 데이터베이스 커넥션을 명시하려면 `$connectionsToTruncate` 속성을 사용할 수 있습니다:

    /**
     * truncate할 커넥션
     *
     * @var array
     */
    protected $connectionsToTruncate = ['mysql'];

또한 truncate 전후에 코드를 실행하려면 `beforeTruncatingDatabase`, `afterTruncatingDatabase` 메소드를 정의하면 됩니다:

    /**
     * truncate 전에 실행할 작업
     */
    protected function beforeTruncatingDatabase(): void
    {
        //
    }

    /**
     * truncate 후에 실행할 작업
     */
    protected function afterTruncatingDatabase(): void
    {
        //
    }

<a name="running-tests"></a>
### 테스트 실행하기

브라우저 테스트를 실행하려면 `dusk` Artisan 명령을 사용하세요:

```shell
php artisan dusk
```

마지막 테스트 실행 시 실패한 테스트만 우선 재실행하려면 `dusk:fails` 명령을 사용하세요:

```shell
php artisan dusk:fails
```

`dusk` 명령은 PHPUnit 테스트 러너가 지원하는 모든 인수를 사용할 수 있습니다. 예를 들어 특정 [group](https://docs.phpunit.de/en/10.5/annotations.html#group)만 실행할 수도 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]  
> [Laravel Sail](/docs/{{version}}/sail) 사용 시, [Dusk 테스트 설정과 실행에 대해]( /docs/{{version}}/sail#laravel-dusk ) Sail 문서를 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하지만, 시스템별로 자동 실행이 되지 않을 경우 수동으로 ChromeDriver를 먼저 실행해야 합니다. 이때는 `tests/DuskTestCase.php` 파일의 다음 라인을 주석 처리하세요:

    /**
     * Dusk 테스트 실행 준비
     *
     * @beforeClass
     */
    public static function prepare(): void
    {
        // static::startChromeDriver();
    }

또한 ChromeDriver를 9515 이외의 포트에서 시작했다면, 동일 클래스의 `driver` 메소드의 포트 번호도 맞춰서 수정해야 합니다:

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

Dusk 테스트 실행 시 별도의 환경 파일을 사용하려면 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어 `local` 환경에서 테스트한다면 `.env.dusk.local` 파일을 만듭니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고 Dusk 환경 파일을 `.env`로 변경합니다. 테스트 완료 후에는 원래 `.env` 파일이 복구됩니다.

<a name="browser-basics"></a>
## 브라우저 기본

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성

애플리케이션에 로그인할 수 있는지 확인하는 테스트를 예시로 살펴보겠습니다. 테스트를 생성한 뒤, 로그인 페이지로 이동하고, 자격 증명을 입력하고, "Login" 버튼을 누르도록 수정할 수 있습니다. Dusk 테스트에서 `browse` 메소드를 호출해 브라우저 인스턴스를 생성할 수 있습니다:

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
         * 기본 브라우저 테스트 예시.
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

위 예시에서 알 수 있듯, `browse` 메소드는 클로저를 인수로 받으며, 해당 클로저에는 Dusk가 브라우저 인스턴스를 자동으로 넘겨줍니다. 이 인스턴스를 통해 애플리케이션을 제어하고 어서션을 수행하게 됩니다.

<a name="creating-multiple-browsers"></a>
#### 다중 브라우저 생성

웹소켓과 상호작용하는 채팅 화면 등 일부 테스트에는 복수의 브라우저가 필요할 수 있습니다. 이 경우, `browse` 메소드 클로저의 시그니처에 브라우저 인수를 추가하면 됩니다:

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

`visit` 메소드로 애플리케이션 내 특정 URI로 이동할 수 있습니다:

    $browser->visit('/login');

[named route](/docs/{{version}}/routing#named-routes)로 이동하려면 `visitRoute` 메소드를 사용하세요:

    $browser->visitRoute('login');

`back`과 `forward` 메소드를 통해 뒤로, 앞으로 이동 가능합니다:

    $browser->back();

    $browser->forward();

`refresh` 메소드로 페이지 새로고침도 가능합니다:

    $browser->refresh();

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메소드로 브라우저 창의 크기를 원하는 값으로 조정할 수 있습니다:

    $browser->resize(1920, 1080);

`maximize` 메소드로 브라우저를 최대화할 수 있습니다:

    $browser->maximize();

`fitContent` 메소드는 창을 콘텐츠 크기에 맞게 조정합니다:

    $browser->fitContent();

테스트 실패 시, Dusk는 스크린샷을 찍기 전에 자동으로 콘텐츠에 맞게 창 크기를 조정합니다. 이 기능을 끄려면 `disableFitOnFailure`를 호출하세요:

    $browser->disableFitOnFailure();

`move` 메소드로 창 위치를 옮길 수 있습니다:

    $browser->move($x = 100, $y = 100);

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 커스텀 브라우저 메소드를 만들고 싶다면 `Browser` 클래스의 `macro` 메소드를 사용할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메소드에서 호출합니다:

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

매크로는 이름(첫 번째 인수)과 클로저(두 번째 인수)를 받습니다. 등록 후에는 브라우저 인스턴스에서 메소드처럼 호출할 수 있습니다:

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/pay')
                ->scrollToElement('#credit-card-details')
                ->assertSee('Enter Credit Card Details');
    });

<a name="authentication"></a>
### 인증

테스트 시 인증이 필요한 페이지가 많을 수 있습니다. 로그인 페이지로 매번 이동하지 않고 `loginAs` 메소드를 사용해 인증된 상태를 간편히 유지할 수 있습니다. 이 메소드는 기본키 또는 인증 가능한 모델 인스턴스를 인수로 받습니다:

    use App\Models\User;
    use Laravel\Dusk\Browser;

    $this->browse(function (Browser $browser) {
        $browser->loginAs(User::find(1))
              ->visit('/home');
    });

> [!WARNING]  
> `loginAs` 메소드 사용 후, 파일 내 전체 테스트에서 해당 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메소드로 암호화된 쿠키의 값을 가져오거나 저장할 수 있습니다(Laravel에서 생성한 쿠키는 기본 암호화됨):

    $browser->cookie('name');

    $browser->cookie('name', 'Taylor');

`plainCookie` 메소드로 암호화되지 않은 쿠키의 값을 사용할 수 있습니다:

    $browser->plainCookie('name');

    $browser->plainCookie('name', 'Taylor');

`deleteCookie`로 쿠키를 삭제할 수 있습니다:

    $browser->deleteCookie('name');

<a name="executing-javascript"></a>
### 자바스크립트 실행

`script` 메소드로 임의의 자바스크립트 문을 실행할 수 있습니다:

    $browser->script('document.documentElement.scrollTop = 0');

    $browser->script([
        'document.body.scrollTop = 0',
        'document.documentElement.scrollTop = 0',
    ]);

    $output = $browser->script('return window.location.pathname');

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 메소드로 스크린샷을 찍어 `tests/Browser/screenshots` 디렉터리에 저장합니다:

    $browser->screenshot('filename');

`responsiveScreenshots` 메소드는 여러 반응형 브레이크포인트에서 스크린샷을 찍습니다:

    $browser->responsiveScreenshots('filename');

<a name="storing-console-output-to-disk"></a>
### 콘솔 로그 디스크 저장

`storeConsoleLog` 메소드로 브라우저의 콘솔 로그를 `tests/Browser/console` 디렉터리의 파일에 저장합니다:

    $browser->storeConsoleLog('filename');

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 디스크 저장

`storeSource` 메소드로 현재 페이지 소스를 `tests/Browser/source` 디렉터리의 파일로 저장합니다:

    $browser->storeSource('filename');

<a name="interacting-with-elements"></a>
## 요소와 상호작용

<a name="dusk-selectors"></a>
### Dusk 선택자

테스트용 요소 탐색에 좋은 CSS 선택자를 유지하는 것은 매우 어렵습니다. 프론트엔드가 바뀌면 아래와 같은 CSS 선택자로 인한 테스트 오류가 잦습니다:

    // HTML...

    <button>Login</button>

    // 테스트...

    $browser->click('.login-page .container div > button');

Dusk 선택자를 이용하면 CSS 선택자에 신경쓰지 않고 테스트 로직에 집중할 수 있습니다. `dusk` 속성을 요소에 부여하고, 테스트 코드에서 `@`를 붙인 선택자로 조작할 수 있습니다:

    // HTML...

    <button dusk="login-button">Login</button>

    // 테스트...

    $browser->click('@login-button');

필요하다면 Dusk에서 사용하는 HTML 속성을 `selectorHtmlAttribute` 메소드로 변경할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메소드에서 호출합니다:

    use Laravel\Dusk\Dusk;

    Dusk::selectorHtmlAttribute('data-dusk');

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기/설정하기

Dusk는 페이지 요소의 현재 값, 표시 텍스트, 속성 등과 상호작용할 다양한 메소드를 제공합니다. 특정 CSS 또는 Dusk 선택자에 일치하는 요소의 "value"를 얻으려면 `value` 메소드를 사용하세요:

    // 값 조회...
    $value = $browser->value('selector');

    // 값 설정...
    $browser->value('selector', 'value');

특정 필드명(input)의 값이 필요할 땐 `inputValue`를 사용할 수 있습니다:

    $value = $browser->inputValue('field');

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메소드는 주어진 선택자에 일치하는 요소의 표시 텍스트를 가져옵니다:

    $text = $browser->text('selector');

<a name="retrieving-attributes"></a>
#### 속성 가져오기

결국, `attribute` 메소드로 선택자에 일치하는 요소의 속성 값을 가져올 수 있습니다:

    $attribute = $browser->attribute('selector', 'value');

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력

Dusk는 폼 또는 입력 요소와의 상호작용을 위한 다양한 메소드를 제공합니다. 예를 들어 input에 텍스트를 입력하려면:

    $browser->type('email', 'taylor@laravel.com');

선택자를 반드시 전달할 필요 없이, 주어진 name 속성을 가진 input 혹은 textarea 필드를 자동으로 찾습니다.

필드에 기존 값을 지우지 않고 텍스트를 추가하려면 `append` 메소드를 사용하세요:

    $browser->type('tags', 'foo')
            ->append('tags', ', bar, baz');

input의 값을 비우려면 `clear` 메소드를 사용하세요:

    $browser->clear('email');

`typeSlowly` 메소드로 느리게 입력할 수도 있습니다. 기본은 키 입력 간 100ms 딜레이가 있습니다. 딜레이(ms)는 세 번째 인수로 조정 가능합니다:

    $browser->typeSlowly('mobile', '+1 (202) 555-5555');

    $browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);

`appendSlowly` 메소드로 느리게 추가 타이핑을 할 수 있습니다:

    $browser->type('tags', 'foo')
            ->appendSlowly('tags', ', bar, baz');

<a name="dropdowns"></a>
#### 드롭다운

`select` 메소드로 select 박스 옵션을 선택할 수 있습니다. 옵션의 표시 텍스트가 아닌 value를 인수로 전달해야 합니다:

    $browser->select('size', 'Large');

두 번째 인수 없이 호출하면 임의의 옵션을 선택합니다:

    $browser->select('size');

여러 값을 넣으면 복수 선택이 가능합니다:

    $browser->select('categories', ['Art', 'Music']);

<a name="checkboxes"></a>
#### 체크박스

체크박스를 체크하려면 `check` 메소드를 사용하세요. CSS 선택자 대신 name 속성도 자동 인식합니다:

    $browser->check('terms');

`uncheck` 메소드로 체크 해제됩니다:

    $browser->uncheck('terms');

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼을 선택하려면 `radio` 메소드를 사용하세요. name과 value가 일치하는 라디오 input을 자동 검색합니다:

    $browser->radio('size', 'large');

<a name="attaching-files"></a>
### 파일 첨부

`attach` 메소드로 파일 input에 파일을 첨부할 수 있습니다. CSS 선택자 대신 name도 인식:

    $browser->attach('photo', __DIR__.'/photos/mountains.png');

> [!WARNING]  
> attach 기능은 PHP `Zip` 확장 모듈이 설치/활성화되어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭

`press` 메소드로 페이지 버튼을 클릭할 수 있습니다. 인수로 버튼의 표시 텍스트나 CSS/Dusk 선택자를 사용합니다:

    $browser->press('Login');

폼 제출 시 버튼이 잠시 비활성화된 뒤 재활성화되는 경우가 있습니다. `pressAndWaitFor` 메소드는 버튼이 활성화되기를 기다립니다:

    // 5초 대기
    $browser->pressAndWaitFor('Save');

    // 1초 대기
    $browser->pressAndWaitFor('Save', 1);

<a name="clicking-links"></a>
### 링크 클릭

브라우저 인스턴스의 `clickLink`로 특정 표시 텍스트의 링크를 클릭할 수 있습니다:

    $browser->clickLink($linkText);

`seeLink`로 해당 링크가 노출되는지 확인할 수 있습니다:

    if ($browser->seeLink($linkText)) {
        // ...
    }

> [!WARNING]  
> 이 메소드들은 jQuery와 상호작용합니다. 페이지에 jQuery가 없으면 Dusk가 자동으로 jQuery를 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys` 메소드는 `type` 메소드보다 복잡한 입력 시퀀스를 제공합니다. 예를 들어, modifier 키를 눌러 입력할 수 있습니다. 아래 예시는 shift 키를 눌러 "taylor" 입력 후, 일반 입력으로 "swift"를 입력합니다:

    $browser->keys('selector', ['{shift}', 'taylor'], 'swift');

애플리케이션의 대표 CSS 선택자에 "키보드 단축키"를 보낼 수도 있습니다:

    $browser->keys('.app', ['{command}', 'j']);

> [!NOTE]  
> `{command}` 등 모든 modifier 키는 `{}`로 감싸야 하며, `Facebook\WebDriver\WebDriverKeys` 의 상수와 일치합니다. [GitHub에서 전체 목록 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk의 `withKeyboard` 메소드로 `Laravel\Dusk\Keyboard`의 `press`, `release`, `type`, `pause` 등 복합적인 키보드 상호작용을 플루언트하게 제어할 수 있습니다:

    use Laravel\Dusk\Keyboard;

    $browser->withKeyboard(function (Keyboard $keyboard) {
        $keyboard->press('c')
            ->pause(1000)
            ->release('c')
            ->type(['c', 'e', 'o']);
    });

<a name="keyboard-macros"></a>
#### 키보드 매크로

테스트 내에서 쉽게 재사용할 키보드 상호작용을 정의하려면 `Keyboard` 클래스의 `macro` 메소드를 사용할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot`에서 작성합니다:

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

매크로는 이름과 클로저를 인수로 받고, 키보드 인스턴스에 메소드처럼 사용할 수 있습니다:

    $browser->click('@textarea')
        ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
        ->click('@another-textarea')
        ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메소드로 CSS/Dusk 선택자에 일치하는 요소를 클릭합니다:

    $browser->click('.selector');

`clickAtXPath`로 XPath 표현식에 일치하는 요소를 클릭할 수 있습니다:

    $browser->clickAtXPath('//div[@class = "selector"]');

`clickAtPoint`로 브라우저 화면 내 주어진 좌표에 존재하는 최상단 요소를 클릭합니다:

    $browser->clickAtPoint($x = 0, $y = 0);

`doubleClick`으로 마우스 더블 클릭 시뮬레이션:

    $browser->doubleClick();

    $browser->doubleClick('.selector');

`rightClick`으로 우클릭 시뮬레이션:

    $browser->rightClick();

    $browser->rightClick('.selector');

`clickAndHold`로 클릭을 누르고 있는 상태를 만들고, `releaseMouse`로 해제할 수 있습니다:

    $browser->clickAndHold('.selector');

    $browser->clickAndHold()
            ->pause(1000)
            ->releaseMouse();

`controlClick`으로 `ctrl+클릭` 이벤트를 시뮬레이션합니다:

    $browser->controlClick();

    $browser->controlClick('.selector');

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메소드는 CSS/Dusk 선택자에 일치하는 요소 위로 마우스를 이동시킵니다:

    $browser->mouseover('.selector');

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag`로 한 요소를 다른 요소로 드래그할 수 있습니다:

    $browser->drag('.from-selector', '.to-selector');

한 방향으로만 드래그하려면:

    $browser->dragLeft('.selector', $pixels = 10);
    $browser->dragRight('.selector', $pixels = 10);
    $browser->dragUp('.selector', $pixels = 10);
    $browser->dragDown('.selector', $pixels = 10);

특정 오프셋만큼 이동하려면:

    $browser->dragOffset('.selector', $x = 10, $y = 10);

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그

Dusk는 자바스크립트 다이얼로그와 상호작용하는 다양한 메소드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그 등장까지 대기할 수 있습니다(초 단위 대기 시간 지정 가능):

    $browser->waitForDialog($seconds = null);

`assertDialogOpened`로 다이얼로그가 나타나고 메시지가 맞는지 어서션할 수 있습니다:

    $browser->assertDialogOpened('Dialog message');

프롬프트 타입 다이얼로그에 텍스트 입력 시 `typeInDialog` 사용:

    $browser->typeInDialog('Hello World');

"확인" 버튼 클릭으로 닫으려면 `acceptDialog`를, "취소" 버튼 클릭으로 닫으려면 `dismissDialog`를 사용합니다:

    $browser->acceptDialog();

    $browser->dismissDialog();

<a name="interacting-with-iframes"></a>
### iFrame과 상호작용

iframe 내부의 요소와 상호작용해야 할 때는 `withinFrame` 메소드로 클로저 내 조작 범위를 지정할 수 있습니다:

    $browser->withinFrame('#credit-card-details', function ($browser) {
        $browser->type('input[name="cardnumber"]', '4242424242424242')
            ->type('input[name="exp-date"]', '12/24')
            ->type('input[name="cvc"]', '123');
        })->press('Pay');
    });

<a name="scoping-selectors"></a>
### 선택자 범위 지정

여러 연산을 특정 선택자 범위 내에서만 실행하고 싶다면 `with` 메소드를 사용합니다:

    $browser->with('.table', function (Browser $table) {
        $table->assertSee('Hello World')
              ->clickLink('Delete');
    });

범위 밖에서 어서션을 할 필요가 있다면 `elsewhere`, `elsewhereWhenAvailable`를 사용할 수도 있습니다:

     $browser->with('.table', function (Browser $table) {
        // 현재 범위: `body .table`

        $browser->elsewhere('.page-title', function (Browser $title) {
            // 현재 범위: `body .page-title`
            $title->assertSee('Hello World');
        });

        $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
            $title->assertSee('Hello World');
        });
     });

<a name="waiting-for-elements"></a>
### 요소 대기

JavaScript를 많이 쓰는 애플리케이션에서는 테스트 진행 전에 특정 요소나 데이터가 준비될 때까지 "대기"해야 할 때가 많습니다. Dusk는 다양한 대기 메소드를 제공합니다.

<a name="waiting"></a>
#### 대기

지정한 시간(ms)만큼 일시 정지하려면 `pause`를 사용하세요:

    $browser->pause(1000);

특정 조건이 `true`일 때만 일시 정지하려면 `pauseIf`:

    $browser->pauseIf(App::environment('production'), 1000);

반대로 조건이 `true`가 아닐 때만 일시 정지하려면 `pauseUnless`:

    $browser->pauseUnless(App::environment('testing'), 1000);

<a name="waiting-for-selectors"></a>
#### 선택자 대기

`waitFor`는 지정한 선택자가 페이지에 보일 때까지 대기합니다. 기본 최대 대기 시간은 5초이며, 두 번째 인수로 시간(초) 조절 가능:

    // 최대 5초 대기
    $browser->waitFor('.selector');

    // 최대 1초 대기
    $browser->waitFor('.selector', 1);

특정 선택자에 특정 텍스트가 포함될 때까지 대기하려면:

    $browser->waitForTextIn('.selector', 'Hello World');

    $browser->waitForTextIn('.selector', 'Hello World', 1);

지정 선택자가 페이지에서 사라질 때까지 대기하려면:

    $browser->waitUntilMissing('.selector');

    $browser->waitUntilMissing('.selector', 1);

선택자가 활성화(또는 비활성화) 될 때까지 대기할 수도 있습니다:

    $browser->waitUntilEnabled('.selector');
    $browser->waitUntilEnabled('.selector', 1);

    $browser->waitUntilDisabled('.selector');
    $browser->waitUntilDisabled('.selector', 1);

<a name="scoping-selectors-when-available"></a>
#### 선택자 등장 후 범위 지정

특정 요소가 등장할 때까지 기다렸다가 해당 요소와 상호작용할 경우가 있습니다. 예를 들어 모달이 뜨고 나서 버튼 클릭 등. 이럴 땐 `whenAvailable`이 유용합니다:

    $browser->whenAvailable('.modal', function (Browser $modal) {
        $modal->assertSee('Hello World')
              ->press('OK');
    });

<a name="waiting-for-text"></a>
#### 텍스트 대기

특정 텍스트가 페이지에 표시될 때까지 대기하려면:

    $browser->waitForText('Hello World');

    $browser->waitForText('Hello World', 1);

표시된 텍스트가 사라질 때까지 대기하려면:

    $browser->waitUntilMissingText('Hello World');
    $browser->waitUntilMissingText('Hello World', 1);

<a name="waiting-for-links"></a>
#### 링크 대기

특정 링크 텍스트가 보일 때까지 대기:

    $browser->waitForLink('Create');
    $browser->waitForLink('Create', 1);

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

특정 input 필드가 보일 때까지 대기:

    $browser->waitForInput($field);
    $browser->waitForInput($field, 1);

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기

페이지 경로가 비동기적으로 변경된다면 `$browser->assertPathIs('/home')` 어서션이 실패할 수 있습니다. 위치가 지정 값이 될 때까지 기다리려면:

    $browser->waitForLocation('/secret');

전체 URL 대기도 가능합니다:

    $browser->waitForLocation('https://example.com/path');

[named route](/docs/{{version}}/routing#named-routes)로 대기하려면:

    $browser->waitForRoute($routeName, $parameters);

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

액션 후 페이지가 새로고침될 때, `waitForReload`를 사용할 수 있습니다:

    use Laravel\Dusk\Browser;

    $browser->waitForReload(function (Browser $browser) {
        $browser->press('Submit');
    })
    ->assertSee('Success!');

보통 버튼 클릭 후 리로드가 필요하다면 `clickAndWaitForReload` 메소드도 사용할 수 있습니다:

    $browser->clickAndWaitForReload('.selector')
            ->assertSee('something');

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기

특정 JS 표현식이 `true`가 될 때까지 테스트 실행을 멈추고 싶을 땐 `waitUntil` 사용:

    $browser->waitUntil('App.data.servers.length > 0');

    $browser->waitUntil('App.data.servers.length > 0', 1);

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기

`waitUntilVue`, `waitUntilVueIsNot`는 [Vue 컴포넌트](https://vuejs.org) 속성의 값이 특정 상태가 될 때까지 대기합니다:

    $browser->waitUntilVue('user.name', 'Taylor', '@user');
    $browser->waitUntilVueIsNot('user.name', null, '@user');

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기

`waitForEvent`로 JS 이벤트 발생을 대기할 수 있습니다:

    $browser->waitForEvent('load');

기본은 body 요소이며, 범위 지정 시 해당 요소에 이벤트 리스너가 걸립니다:

    $browser->with('iframe', function (Browser $iframe) {
        $iframe->waitForEvent('load');
    });

두 번째 인수로 특정 요소에 리스너 지정도 가능합니다:

    $browser->waitForEvent('load', '.selector');

document, window 객체의 이벤트도 대기 가능합니다:

    $browser->waitForEvent('scroll', 'document');
    $browser->waitForEvent('resize', 'window', 5);

<a name="waiting-with-a-callback"></a>
#### 콜백으로 대기

많은 "대기" 메소드가 내부적으로 사용하는 `waitUsing` 메소드를 직접 사용할 수 있습니다. 지정 초, 평가 주기, 클로저, 실패 메시지를 인수로 받습니다:

    $browser->waitUsing(10, 1, function () use ($something) {
        return $something->isReady();
    }, "Something wasn't ready in time.");

<a name="scrolling-an-element-into-view"></a>
### 요소로 스크롤

뷰포트 밖 요소를 클릭해야 할 때, `scrollIntoView`로 스크롤 후 클릭합니다:

    $browser->scrollIntoView('.selector')
            ->click('.selector');

<a name="available-assertions"></a>
## 사용 가능한 어서션 목록

Dusk는 애플리케이션에 대해 다양한 어서션을 제공합니다. 전체 목록은 아래와 같습니다:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

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

(※ 이하 각 어서션 메소드 설명은 생략합니다. 위 설명을 동일하게 한국어로 옮기세요.)

<a name="pages"></a>
## 페이지 객체

복잡한 동작을 여러 번 반복 수행해야 하는 테스트는 읽기 어렵습니다. Dusk의 페이지 객체는 단일 메소드로 여러 동작을 표현적으로 수행할 수 있게 하여, 코드 가독성과 재사용성을 높입니다. 페이지 객체에서는 애플리케이션 및 각 페이지에 대한 공통 선택자 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

페이지 객체를 생성하려면 `dusk:page` Artisan 명령을 실행하세요. 페이지 객체는 `tests/Browser/Pages` 폴더에 저장됩니다:

    php artisan dusk:page Login

<a name="configuring-pages"></a>
### 페이지 설정

페이지 객체는 기본적으로 `url`, `assert`, `elements` 세 가지 메소드를 갖습니다. 지금은 `url`과 `assert`를 설명합니다. `elements`는 [아래에서 자세히 설명](#shorthand-selectors)합니다.

<a name="the-url-method"></a>
#### `url` 메소드

`url` 메소드는 해당 페이지의 경로를 반환해야 합니다. Dusk가 해당 페이지로 이동 시 이 경로를 사용합니다:

    /**
     * 페이지의 URL 반환.
     */
    public function url(): string
    {
        return '/login';
    }

<a name="the-assert-method"></a>
#### `assert` 메소드

`assert` 메소드에서는 브라우저가 실제로 올바른 페이지에 있는지 확인하는 어서션을 실어줄 수 있습니다. 필수적인 것은 아니지만, 자동 실행됩니다:

    /**
     * 브라우저가 페이지에 있는지 어서트.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertPathIs($this->url());
    }

<a name="navigating-to-pages"></a>
### 페이지로 이동

페이지 정의 후, `visit` 메소드로 해당 페이지로 이동할 수 있습니다:

    use Tests\Browser\Pages\Login;

    $browser->visit(new Login);

이미 특정 페이지에 있고, 해당 페이지의 selector/method를 "로드"해야 한다면 `on` 메소드로 가능합니다:

    use Tests\Browser\Pages\CreatePlaylist;

    $browser->visit('/dashboard')
            ->clickLink('Create Playlist')
            ->on(new CreatePlaylist)
            ->assertSee('@create');

<a name="shorthand-selectors"></a>
### 축약 선택자

페이지 클래스의 `elements` 메소드에서 모든 CSS 선택자에 대한 빠르고 쉬운 단축키를 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" input 필드에 대한 단축키:

    /**
     * 페이지 element 단축키 반환.
     *
     * @return array<string, string>
     */
    public function elements(): array
    {
        return [
            '@email' => 'input[name=email]',
        ];
    }

정의 후에는 일반적인 CSS 선택자 대신 단축키 사용이 가능합니다:

    $browser->type('@email', 'taylor@laravel.com');

<a name="global-shorthand-selectors"></a>
#### 전역 축약 선택자

Dusk 설치 후, `tests/Browser/Pages`에 기본 Page 클래스가 생깁니다. 이 클래스의 `siteElements` 메소드에서 모든 페이지에서 사용 가능한 전역 단축키를 정의할 수 있습니다:

    /**
     * 사이트 전역 element 단축키 반환.
     *
     * @return array<string, string>
     */
    public static function siteElements(): array
    {
        return [
            '@element' => '#selector',
        ];
    }

<a name="page-methods"></a>
### 페이지 메소드

페이지에서는 추가 커스텀 메소드를 정의해서 테스트에서 재사용할 수 있습니다. 예를 들어, 음악 관리 앱에서 플레이리스트를 만드는 동작을 페이지 메소드로 분리할 수 있습니다:

    <?php

    namespace Tests\Browser\Pages;

    use Laravel\Dusk\Browser;

    class Dashboard extends Page
    {
        // 기타 페이지 메소드...

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

정의 후, 이 메소드는 해당 페이지를 사용하는 테스트 어디서든 쓸 수 있습니다:

    use Tests\Browser\Pages\Dashboard;

    $browser->visit(new Dashboard)
            ->createPlaylist('My Playlist')
            ->assertSee('My Playlist');

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 "페이지 객체"와 비슷하지만, 주로 네비게이션 바, 알림창처럼 여러 페이지에서 재사용되는 UI 조각과 기능에 적합합니다. 컴포넌트는 특정 URL에 묶이지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

컴포넌트는 `dusk:component` Artisan 명령으로 생성합니다. 새 컴포넌트는 `tests/Browser/Components` 폴더에 만들어집니다:

    php artisan dusk:component DatePicker

예를 들어, 날짜 선택기는 애플리케이션 여러 페이지에서 쓰일 수 있으니 하나의 Dusk 컴포넌트로 로직을 캡슐화할 수 있습니다:

    <?php

    namespace Tests\Browser\Components;

    use Laravel\Dusk\Browser;
    use Laravel\Dusk\Component as BaseComponent;

    class DatePicker extends BaseComponent
    {
        /**
         * 컴포넌트의 루트 선택자 반환.
         */
        public function selector(): string
        {
            return '.date-picker';
        }

        /**
         * 브라우저 페이지에 컴포넌트가 노출됐는지 어서트.
         */
        public function assert(Browser $browser): void
        {
            $browser->assertVisible($this->selector());
        }

        /**
         * 컴포넌트 element 단축키 반환.
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
         * 주어진 날짜 선택.
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

<a name="using-components"></a>
### 컴포넌트 사용

정의한 컴포넌트는 어느 테스트에서나 쉽게 사용할 수 있습니다. 날짜 선택 로직이 바뀌면 컴포넌트만 수정하면 됩니다:

    <?php

    namespace Tests\Browser;

    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Laravel\Dusk\Browser;
    use Tests\Browser\Components\DatePicker;
    use Tests\DuskTestCase;

    class ExampleTest extends DuskTestCase
    {
        /**
         * 컴포넌트 테스트 예시.
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

<a name="continuous-integration"></a>
## 지속적인 통합(CI)

> [!WARNING]  
> 대부분의 Dusk CI 환경은 Laravel 앱이 내장 PHP 개발 서버의 8000포트에서 서비스 된다고 전제합니다. 반드시 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`인지 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, 다음과 같이 Google Chrome 빌드팩과 스크립트를 Heroku `app.json`에 추가하세요:

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

<a name="running-tests-on-travis-ci"></a>
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 설정을 참고하세요. Travis는 GUI 환경이 아니므로 Chrome 실행에 약간의 추가 설정이 필요합니다:

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

[GitHub Actions](https://github.com/features/actions)로 Dusk 테스트를 실행하려면 아래의 워크플로우 예시를 참고하세요:

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
### Chipper CI

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면 아래 설정 파일을 참고하세요. PHP 빌트인 서버로 Laravel을 구동합니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Build 환경에 Chrome 포함
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
      
      # APP_URL에 BUILD_HOST 적용된 Dusk env 파일 생성
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

Chipper CI에서 Dusk 테스트 실행 및 데이터베이스 사용 등에 대한 자세한 내용은 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.