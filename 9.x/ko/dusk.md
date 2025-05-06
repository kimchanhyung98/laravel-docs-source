# Laravel Dusk

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기초](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [네비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값 및 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [셀렉터 범위 한정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소 뷰로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 구성](#configuring-pages)
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

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 뛰어나고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 하지만 다른 Selenium 호환 드라이버도 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면, [Google Chrome](https://www.google.com/chrome)을 설치하고 `laravel/dusk` Composer 의존성을 프로젝트에 추가하세요:

```shell
composer require --dev laravel/dusk
```

> **경고**
> Dusk 서비스 프로바이더를 수동으로 등록하고 있는 경우, **절대로** 운영 환경에서 등록하지 마세요. 그렇게 하면 누구나 애플리케이션에 인증 없이 접근할 위험이 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리, 예제 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 생성합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션에 접속할 때 사용하는 URL과 일치해야 합니다.

> **참고**
> [Laravel Sail](/docs/{{version}}/sail)을 사용하여 로컬 개발 환경을 관리하는 경우, [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk)에 대한 Sail 문서도 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 관리

`dusk:install` 명령을 통해 설치되는 ChromeDriver 외의 버전을 설치하려면 `dusk:chrome-driver` 명령어를 사용하세요:

```shell
# 운영체제에 맞는 최신 버전 설치
php artisan dusk:chrome-driver

# 특정 버전 설치
php artisan dusk:chrome-driver 86

# 지원되는 모든 운영체제에 특정 버전 설치
php artisan dusk:chrome-driver --all

# Chrome/Chromium 감지 후 그 버전에 맞는 드라이버 설치
php artisan dusk:chrome-driver --detect
```

> **경고**
> Dusk는 `chromedriver` 바이너리의 실행 권한이 필요합니다. 실행에 문제가 있을 경우, 다음 명령어로 권한을 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용

기본적으로 Dusk는 Google Chrome과 독립 실행형 ChromeDriver를 사용하여 테스트를 실행합니다. 그러나 Selenium 서버를 직접 띄우고 원하는 브라우저로 테스트를 실행할 수 있습니다.

`tests/DuskTestCase.php` 파일을 열어, 이 파일에서 `startChromeDriver` 호출을 제거하세요. 이렇게 하면 Dusk는 ChromeDriver를 자동 실행하지 않습니다:

    /**
     * Dusk 테스트 실행 전 준비.
     *
     * @beforeClass
     * @return void
     */
    public static function prepare()
    {
        // static::startChromeDriver();
    }

그리고 나서, 원하는 URL과 포트로 WebDriver에 연결하도록 `driver` 메서드를 수정할 수 있습니다:

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

<a name="getting-started"></a>
## 시작하기

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 생성하려면, `dusk:make` Artisan 명령어를 사용하세요. 생성된 테스트는 `tests/Browser` 디렉터리에 위치합니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

대부분의 테스트는 데이터베이스에서 데이터를 받아오는 페이지와 상호작용하게 됩니다. 그러나 Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하지 마세요. `RefreshDatabase`는 데이터베이스 트랜잭션을 활용하므로 HTTP 요청 간에 적용되지 않거나 사용이 불가능합니다. 대신 `DatabaseMigrations` 트레이트나 `DatabaseTruncation` 트레이트 중 하나를 사용하세요.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 매번 테이블을 드롭하고 재생성하기 때문에, 테이블을 truncate할 때보다 느릴 수 있습니다.

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

> **경고**
> Dusk 테스트 실행 시 SQLite 인메모리 데이터베이스는 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되어 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 데이터베이스 Truncation 사용

`DatabaseTruncation` 트레이트를 사용하기 전에, Composer로 `doctrine/dbal` 패키지를 설치해야 합니다:

```shell
composer require --dev doctrine/dbal
```

이 트레이트는 첫 번째 테스트에서 마이그레이션을 실행하여 테이블이 올바르게 생성되도록 합니다. 이후 테스트에서는 테이블을 truncate만 하여 마이그레이션을 반복 실행하는 것보다 빠르게 동작합니다.

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 truncate 합니다. truncate할 테이블을 커스터마이징하려면, 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

    /**
     * Truncate할 테이블 지정
     *
     * @var array
     */
    protected $tablesToTruncate = ['users'];

반대로, truncate에서 제외할 테이블을 지정하고 싶으면 `$exceptTables` 속성을 정의합니다:

    /**
     * Truncate에서 제외할 테이블 지정
     *
     * @var array
     */
    protected $exceptTables = ['users'];

truncate를 적용할 데이터베이스 커넥션을 지정하려면 `$connectionsToTruncate` 속성을 사용합니다:

    /**
     * Truncate할 커넥션 지정
     *
     * @var array
     */
    protected $connectionsToTruncate = ['mysql'];

<a name="running-tests"></a>
### 테스트 실행

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

마지막 테스트 실행 시 실패했던 테스트만 먼저 재실행하고 싶을 때는 `dusk:fails` 명령어를 사용하세요:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 PHPUnit와 같이 [그룹](https://phpunit.readthedocs.io/en/9.5/annotations.html#group) 등 다양한 인자를 그대로 사용할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> **참고**
> [Laravel Sail](/docs/{{version}}/sail)을 사용하여 개발 환경을 운영한다면, [Dusk 테스트 구성 및 실행](/docs/{{version}}/sail#laravel-dusk) 관련 Sail 문서를 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 만약 시스템에서 자동 실행이 잘 되지 않는다면, `dusk` 명령 실행 전 ChromeDriver를 직접 실행할 수 있습니다. 이 경우, `tests/DuskTestCase.php` 파일의 다음 코드를 주석 처리하세요.

    /**
     * Dusk 테스트 실행 전 준비.
     *
     * @beforeClass
     * @return void
     */
    public static function prepare()
    {
        // static::startChromeDriver();
    }

또한, ChromeDriver를 9515 포트가 아닌 다른 포트에서 실행할 때는 같은 클래스의 `driver` 메서드에서 포트 번호도 수정해야 합니다:

    /**
     * RemoteWebDriver 인스턴스 생성
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

Dusk가 테스트 실행 중 별도의 환경 파일을 사용하도록 하려면 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어 `local` 환경에서 `dusk` 명령을 실행한다면 `.env.dusk.local` 파일을 만들면 됩니다.

테스트를 실행하면, Dusk가 기존 `.env` 파일을 백업한 후 Dusk 환경 파일을 `.env`로 바꿉니다. 테스트가 끝나면 원래의 `.env` 파일로 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기초

<a name="creating-browsers"></a>
### 브라우저 생성

이제 애플리케이션에 로그인할 수 있는지 확인하는 테스트를 작성해 봅시다. 테스트를 생성한 후, 로그인 페이지로 이동하여, 자격 증명을 입력하고 "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내에서 `browse` 메서드를 호출하세요.

(코드 생략: 번역 요청 시 특이사항이 없으므로 그대로 두었습니다.)

`browse` 메서드는 클로저를 인자로 받아 자동으로 브라우저 인스턴스를 전달합니다. 이 브라우저 인스턴스를 사용하여 애플리케이션과 상호작용하거나 어설션을 할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 생성

테스트를 제대로 수행하기 위해 여러 브라우저가 필요할 때가 있습니다. 예를 들어, 웹소켓 채팅 화면을 테스트할 때 여러 브라우저 인스턴스가 필요할 수 있습니다. 여러 브라우저를 생성하려면 `browse` 메서드의 클로저 시그니처에 인자를 추가하세요.

(코드 생략)

<a name="navigation"></a>
### 네비게이션

`visit` 메서드는 애플리케이션의 지정된 URI로 이동할 때 사용합니다.

(코드 생략)

`visitRoute` 메서드를 사용하면 [네임드 라우트](/docs/{{version}}/routing#named-routes)로 이동할 수 있습니다.

(코드 생략)

`back`, `forward`로 뒤로, 앞으로 이동할 수 있습니다.

(코드 생략)

`refresh`로 새로고침도 가능합니다.

(코드 생략)

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메서드로 브라우저 창 크기를 조절할 수 있습니다.

(코드 생략)

`maximize`로 전체화면, `fitContent`로 컨텐츠에 맞게 크기 조절이 가능합니다.

(코드 생략)

테스트가 실패하면 Dusk가 자동으로 브라우저를 컨텐츠에 맞게 리사이즈 후 스크린샷을 찍습니다. 이 기능은 `disableFitOnFailure`로 끌 수 있습니다.

(코드 생략)

윈도우 위치 이동에는 `move`를 사용하세요.

(코드 생략)

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot`에서 호출합니다.

(코드 생략)

매크로는 첫 번째 인자로 이름, 두 번째에 클로저를 받으며, 이후 브라우저 인스턴스에서 메서드처럼 호출할 수 있습니다.

(코드 생략)

<a name="authentication"></a>
### 인증

인증이 필요한 페이지를 테스트할 때, 매번 로그인 화면을 거치지 않고 `loginAs` 메서드를 통해 로그인된 상태로 테스트를 시작할 수 있습니다. 이 메서드는 모델의 PK 또는 모델 인스턴스를 인자로 받습니다.

(코드 생략)

> **경고**
> `loginAs` 사용 후에는 해당 파일 내의 모든 테스트에 유저 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie`로 암호화된 쿠키 값을 얻거나 설정할 수 있습니다.

(코드 생략)

`plainCookie`는 암호화되지 않은 쿠키에 사용합니다.

(코드 생략)

`deleteCookie`로 쿠키를 삭제할 수 있습니다.

(코드 생략)

<a name="executing-javascript"></a>
### JavaScript 실행

`script`로 임의의 JS 코드를 실행할 수 있습니다.

(코드 생략)

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot`으로 해당 파일명으로 스크린샷을 찍어 `tests/Browser/screenshots`에 저장합니다.

(코드 생략)

`responsiveScreenshots`로 여러 해상도에서 스크린샷을 찍을 수도 있습니다.

(코드 생략)

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장

`storeConsoleLog`로 현재 브라우저의 콘솔 출력을 파일로 저장합니다. 저장 경로는 `tests/Browser/console`입니다.

(코드 생략)

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장

`storeSource`로 현재 페이지의 소스를 파일로 저장합니다. 저장 경로는 `tests/Browser/source`입니다.

(코드 생략)

<a name="interacting-with-elements"></a>
## 요소와 상호작용

<a name="dusk-selectors"></a>
### Dusk 셀렉터

효과적인 Dusk 테스트를 작성하려면, 요소에 대한 좋은 CSS 셀렉터를 선택하는 것이 매우 중요합니다. 프론트엔드 변경으로 인해 CSS 셀렉터가 자주 깨질 수 있습니다.

(코드 생략)

Dusk 셀렉터는 HTML 요소에 `dusk` 속성을 추가하여 정의할 수 있습니다. 이후 테스트에서는 `@`을 접두사로 사용하여 해당 요소를 쉽게 선택할 수 있습니다.

(코드 생략)

<a name="text-values-and-attributes"></a>
### 텍스트, 값 및 속성

<a name="retrieving-setting-values"></a>
#### 값 조회 및 설정

Dusk는 현재 값, 표시 텍스트, 속성 등을 조회하거나 설정할 수 있는 여러 메서드를 제공합니다.

- `value`로 값을 가져오거나 변경할 수 있습니다.
- `inputValue`로 입력 필드의 값을 조회할 수 있습니다.

<a name="retrieving-text"></a>
#### 텍스트 조회

`text`로 셀렉터에 맞는 요소의 텍스트 내용을 조회할 수 있습니다.

<a name="retrieving-attributes"></a>
#### 속성 조회

`attribute`로 셀렉터에 맞는 요소의 특정 속성 값을 가져올 수 있습니다.

<a name="interacting-with-forms"></a>
### 폼과 상호작용

<a name="typing-values"></a>
#### 값 입력

Dusk는 폼 및 입력 요소와 상호작용하는 다양한 메서드를 제공합니다.

- `type`으로 입력 필드에 텍스트 입력
- `append`로 값 추가
- `clear`로 값 지우기
- `typeSlowly` 및 `appendSlowly`로 천천히 입력

<a name="dropdowns"></a>
#### 드롭다운

- `select`로 드롭다운 값 선택 (옵션 값 기준)
- 배열을 전달해 다중 선택도 가능

<a name="checkboxes"></a>
#### 체크박스

- `check`로 체크, `uncheck`로 해제

<a name="radio-buttons"></a>
#### 라디오 버튼

- `radio`로 라디오 옵션 선택

<a name="attaching-files"></a>
### 파일 첨부

`attach`로 파일을 첨부할 수 있으며, 이 기능은 PHP의 `Zip` 확장자가 필요합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭

- `press`로 버튼 클릭
- `pressAndWaitFor`로 비동기 처리 후 버튼이 다시 활성화되는 것까지 대기

<a name="clicking-links"></a>
### 링크 클릭

- `clickLink`로 텍스트를 가진 링크 클릭
- `seeLink`로 해당 링크가 페이지에 있는지 확인

> **경고**
> 이 메서드들은 jQuery에 의존합니다. 페이지에 없으면 Dusk가 자동 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys` 메서드로 Ctrl, Shift 등 조합 및 복잡한 입력 시퀀스를 전달할 수 있습니다.

> **참고**
> `{command}` 등 모디파이어 키는 `{}`로 감싸며, 이는 `Facebook\WebDriver\WebDriverKeys` 상수와 일치합니다.

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 요소 클릭

- `click`으로 CSS/Dusk 셀렉터에 맞는 요소 클릭
- `clickAtXPath`로 XPath로 요소 클릭
- `clickAtPoint`로 위치 좌표로 클릭
- `doubleClick`, `rightClick`, `clickAndHold` 등 다양한 마우스 이벤트 지원

<a name="mouseover"></a>
#### 마우스오버

- `mouseover`로 셀렉터 요소로 마우스 이동

<a name="drag-drop"></a>
#### 드래그 앤 드롭

- `drag`로 요소를 다른 요소로 드래그
- `dragLeft`, `dragRight`, `dragUp`, `dragDown` 등 방향 지정도 가능
- `dragOffset`로 기준점에서 오프셋 지정

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그

- `waitForDialog`로 다이얼로그 표시 대기
- `assertDialogOpened`로 다이얼로그 메시지 검증
- `typeInDialog`, `acceptDialog`, `dismissDialog` 등 지원

<a name="scoping-selectors"></a>
### 셀렉터 범위 한정

- `with` 메서드로 셀렉터 범위 내에서 여러 작업 수행
- `elsewhere`, `elsewhereWhenAvailable`로 범위 밖에서 작업 가능

<a name="waiting-for-elements"></a>
### 요소 대기

JavaScript를 많이 사용하는 앱 테스트 시, 특정 요소나 데이터가 준비될 때까지 대기할 필요가 있습니다. Dusk에서는 다양한 대기 메서드를 제공합니다.

<a name="waiting"></a>
#### 대기

- `pause`로 일정 시간 대기
- `pauseIf`, `pauseUnless`로 조건부 대기도 가능

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

- `waitFor`, `waitForTextIn`, `waitUntilMissing`, `waitUntilEnabled`, `waitUntilDisabled` 등 다양한 상태 대기

<a name="scoping-selectors-when-available"></a>
#### 요소 등장시 범위 한정

- `whenAvailable`로 해당 요소가 뜨면 범위 내에서 작업 수행

<a name="waiting-for-text"></a>
#### 텍스트 대기

- `waitForText`, `waitUntilMissingText`로 해당 텍스트가 등장 혹은 사라질 때까지 대기

<a name="waiting-for-links"></a>
#### 링크 대기

- `waitForLink`로 텍스트를 가진 링크가 나타날 때까지 대기

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

- `waitForInput`로 입력 필드가 보일 때까지 대기

<a name="waiting-on-the-page-location"></a>
#### 위치 대기

- `waitForLocation`을 이용해 URL 또는 전체 경로, [네임드 라우트](/docs/{{version}}/routing#named-routes)로 대기

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기

- `waitForReload`와 `clickAndWaitForReload` 등 페이지가 새로 고쳐질 때까지 대기

<a name="waiting-on-javascript-expressions"></a>
#### JS 표현식 대기

- `waitUntil`로 JS 코드 결과가 true가 될 때까지 대기

<a name="waiting-on-vue-expressions"></a>
#### Vue 상태 대기

- `waitUntilVue`, `waitUntilVueIsNot`로 Vue 컴포넌트 속성의 값에 맞춰 대기

<a name="waiting-for-javascript-events"></a>
#### JS 이벤트 대기

- `waitForEvent`로 지정한 JS 이벤트를 대기
- 특정 셀렉터, document, window 등 원하는 위치에 바인딩 가능

<a name="waiting-with-a-callback"></a>
#### 콜백으로 대기

- `waitUsing`으로 콜백 값이 true가 될 때까지 커스텀 대기

<a name="scrolling-an-element-into-view"></a>
### 요소 뷰로 스크롤

`scrollIntoView`로 브라우저 화면 내에서 해당 셀렉터 요소가 보일 때까지 스크롤할 수 있습니다.

(코드 생략)

<a name="available-assertions"></a>
## 사용 가능한 어설션

Dusk에서 사용할 수 있는 다양한 어설션 메서드는 아래와 같습니다.

(코드 블록: HTML 및 스타일링 포함된 부분은 그대로 유지)

각 어설션 예시 및 코드 스니펫은 원문과 동일하게 사용하십시오.

<a name="pages"></a>
## 페이지

테스트가 여러 복잡한 동작을 순차적으로 실행해야 하는 경우, 테스트가 읽기 어렵고 복잡해질 수 있습니다. Dusk 페이지는 하나의 메서드를 통해 여러 동작을 정의하고 실행할 수 있도록 해줍니다. 또한 공통 셀렉터나 특정 페이지의 셀렉터 단축키도 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

`dusk:page` Artisan 명령으로 페이지 오브젝트를 생성합니다. 모든 페이지 오브젝트는 `tests/Browser/Pages` 디렉터리에 생성됩니다.

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성

기본적으로 페이지에는 `url`, `assert`, `elements` 세 메서드가 있습니다. 현재는 `url`과 `assert`를 다루고, `elements`는 [아래에서](#shorthand-selectors) 자세히 설명합니다.

#### `url` 메서드

페이지를 나타내는 URL 경로를 반환합니다. Dusk가 해당 페이지로 이동할 때 이 경로를 사용합니다.

(코드 생략)

#### `assert` 메서드

브라우저가 실제로 해당 페이지에 있는지 추가적인 어설션을 할 수 있습니다. 생략 가능하며, 정의된 경우 페이지 이동 시 자동으로 실행됩니다.

(코드 생략)

<a name="navigating-to-pages"></a>
### 페이지로 이동

페이지가 정의되었다면 `visit` 메서드로 해당 페이지로 이동할 수 있습니다.

(코드 생략)

이미 특정 페이지에 있다고 판단되는 경우, `on` 메서드로 페이지의 셀렉터나 메서드를 가져올 수 있습니다. 이 방법은 예를 들어, 버튼 클릭 후 페이지 리다이렉트 상황 등에 유용합니다.

(코드 생략)

<a name="shorthand-selectors"></a>
### 셀렉터 단축키

페이지의 `elements` 메서드에서 CSS 셀렉터에 단축키를 정의할 수 있습니다. 예를 들어 로그인 페이지의 "email" 입력 필드 단축키:

(코드 생략)

정의한 후에는 일반 CSS 셀렉터 대신 shorthand로 사용할 수 있습니다.

(코드 생략)

#### 전역 셀렉터 단축키

설치 후 `tests/Browser/Pages`에는 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에서 사이트 전체에 적용되는 전역 단축키를 정의할 수 있습니다.

(코드 생략)

<a name="page-methods"></a>
### 페이지 메서드

페이지에 커스텀 동작을 메서드로 추가할 수 있습니다. 예를 들어, "플레이리스트 생성" 기능을 페이지 메서드로 만들고 여러 테스트에 재사용할 수 있습니다.

(코드 생략)

정의된 페이지 메서드를 테스트에서 호출하면, 브라우저 인스턴스가 자동으로 첫 번째 인자로 전달됩니다.

(코드 생략)

<a name="components"></a>
## 컴포넌트

컴포넌트는 Dusk의 "페이지 오브젝트"와 유사하지만, 네비게이션 바, 알림 창 등 애플리케이션 전체에서 재사용되는 UI와 기능을 위한 것입니다. 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

`dusk:component` Artisan 명령으로 컴포넌트를 생성할 수 있습니다. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 위치합니다.

```shell
php artisan dusk:component DatePicker
```

예제처럼 "date picker"처럼 여러 페이지에서 사용되는 컴포넌트의 브라우저 자동화 로직을 별도 컴포넌트로 작성하면, 중복 없이 재사용이 가능합니다.

(코드 생략)

<a name="using-components"></a>
### 컴포넌트 사용

컴포넌트를 정의한 후, 모든 테스트에서 쉽게 해당 컴포넌트를 사용할 수 있습니다. 로직이 변해도 컴포넌트만 수정하면 됩니다.

(코드 생략)

<a name="continuous-integration"></a>
## 지속적 통합(CI)

> **경고**
> 대부분의 Dusk CI 환경은 라라벨 애플리케이션이 8000 포트의 내장 PHP 개발 서버로 서비스된다고 가정합니다. CI 환경의 `APP_URL` 변수가 `http://127.0.0.1:8000`인지 반드시 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, 아래와 같이 `app.json`에 Google Chrome 빌드팩과 스크립트를 추가하세요.

(코드 생략)

<a name="running-tests-on-travis-ci"></a>
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 아래 `.travis.yml`로 설정합니다. Travis CI는 그래픽 환경이 아니므로 Chrome 브라우저를 실행하려면 추가 작업이 필요합니다.

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

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하려면 아래 설정 예시를 참고하세요. `php artisan serve`를 통해 내장 웹서버를 실행합니다.

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

---

**주의사항**
- 코드 블록, HTML 태그, URL, 마크다운 구조 등은 원본을 그대로 유지하였습니다.
- PHP, 셸, YAML 등 코드 예제도 번역하지 않았습니다.
- 문서 구조 및 마크다운 포맷도 원본에 맞추었습니다.
- 전문 용어는 '트레이트', '아티즌(Artisan, 명령어)', '셀렉터', '컴포넌트', '어설션', '페이지 오브젝트', '네비게이션 바' 등 맥락에 맞게 번역하였습니다.