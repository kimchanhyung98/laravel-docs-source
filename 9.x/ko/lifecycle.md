# 요청 라이프사이클 (Request Lifecycle)

- [소개](#introduction)
- [라이프사이클 개요](#lifecycle-overview)
    - [첫 단계](#first-steps)
    - [HTTP / 콘솔 커널](#http-console-kernels)
    - [서비스 프로바이더](#service-providers)
    - [라우팅](#routing)
    - [마무리 단계](#finishing-up)
- [서비스 프로바이더에 집중하기](#focus-on-service-providers)

<a name="introduction"></a>
## 소개

"실제 세계"에서 어떤 도구를 사용할 때, 그 도구의 작동 방식을 이해하면 더 자신감 있게 사용할 수 있습니다. 애플리케이션 개발도 마찬가지입니다. 개발 도구의 동작 원리를 이해하면 더욱 편안하고 자신 있게 활용할 수 있습니다.

이 문서의 목적은 라라벨 프레임워크가 어떻게 동작하는지 전체적인 흐름을 쉽고 명확하게 설명하는 데 있습니다. 프레임워크의 전체 구조를 이해하면 '마법 같아 보였던' 부분들이 훨씬 익숙해지고, 여러분도 애플리케이션을 더 자신 있게 개발할 수 있습니다. 만약 당장 모든 용어나 개념이 완벽하게 이해되지 않더라도 걱정하지 마세요! 대략적인 흐름만 먼저 파악하신 뒤, 다른 문서들을 살펴보면서 점차 지식을 쌓아가도 충분합니다.

<a name="lifecycle-overview"></a>
## 라이프사이클 개요

<a name="first-steps"></a>
### 첫 단계

라라벨 애플리케이션으로 들어오는 모든 요청의 진입점은 `public/index.php` 파일입니다. 웹 서버(Apache 또는 Nginx) 설정에 따라 모든 요청이 이 파일로 전달됩니다. 이 `index.php` 파일 자체에는 많은 코드가 들어 있지 않으며, 프레임워크의 나머지 부분을 불러오는 출발점 역할만 합니다.

`index.php`에서는 Composer로 생성된 오토로더(자동 로더)를 불러오고, 그 다음 `bootstrap/app.php` 파일로부터 라라벨 애플리케이션 인스턴스를 가져옵니다. 라라벨이 가장 먼저 하는 작업은 애플리케이션 인스턴스(즉, [서비스 컨테이너](/docs/9.x/container))를 생성하는 것입니다.

<a name="http-console-kernels"></a>
### HTTP / 콘솔 커널

그 다음, 들어온 요청이 어떤 종류인지에 따라 HTTP 커널 또는 콘솔 커널로 전달됩니다. 이 두 커널은 모든 요청이 반드시 거쳐 가는 중앙 허브 같은 역할을 합니다. 여기서는 HTTP 커널에 집중해서 살펴보겠습니다. HTTP 커널은 `app/Http/Kernel.php` 파일에 있습니다.

HTTP 커널은 `Illuminate\Foundation\Http\Kernel` 클래스를 확장하며, 이 클래스에는 요청 실행 전에 실행될 `bootstrappers` 배열이 정의되어 있습니다. 이 부트스트래퍼들은 에러 처리, 로깅 설정, [애플리케이션 환경 감지](/docs/9.x/configuration#environment-configuration) 등 요청을 실제로 처리하기 전에 필요한 여러 작업을 수행합니다. 보통 이 작업들은 내부적으로 라라벨이 자체 설정을 하는 부분이므로, 여러분이 직접 신경 쓸 필요는 거의 없습니다.

또한, HTTP 커널에는 애플리케이션으로 들어오는 모든 요청이 반드시 거쳐야 하는 HTTP [미들웨어](/docs/9.x/middleware) 목록이 정의되어 있습니다. 미들웨어는 [HTTP 세션](/docs/9.x/session) 읽기/쓰기, 애플리케이션이 유지보수 모드인지 확인, [CSRF 토큰 검증](/docs/9.x/csrf) 등 다양한 처리를 담당합니다. 미들웨어에 대해서는 곧 더 자세히 설명하겠습니다.

HTTP 커널의 `handle` 메서드는 매우 단순한 시그니처를 가지고 있습니다. `Request`를 받아서 `Response`를 반환합니다. 이 커널을 하나의 큰 블랙박스(검은 상자)로 생각해도 좋습니다. 이 안에 HTTP 요청을 넣으면, HTTP 응답이 나오는 구조입니다.

<a name="service-providers"></a>
### 서비스 프로바이더

커널 부트스트래핑 과정에서 가장 중요한 작업 중 하나가 바로, 애플리케이션의 [서비스 프로바이더](/docs/9.x/providers)를 로딩하는 일입니다. 서비스 프로바이더는 데이터베이스, 큐, 유효성 검증, 라우팅 등 프레임워크의 다양한 구성 요소를 초기화하고 준비하는 역할을 맡고 있습니다. 애플리케이션에서 사용할 서비스 프로바이더는 `config/app.php` 설정 파일의 `providers` 배열에 정의되어 있습니다.

라라벨은 이 배열에 들어 있는 각 프로바이더를 반복적으로 하나씩 인스턴스화합니다. 프로바이더가 인스턴스화된 후, 먼저 모든 프로바이더의 `register` 메서드가 호출됩니다. 그리고 모든 프로바이더의 등록이 끝나면, 그 다음 각 프로바이더의 `boot` 메서드가 호출됩니다. 이렇게 하는 이유는, 모든 서비스 컨테이너 바인딩이 등록 및 사용 가능한 상태에서 `boot` 메서드가 실행되도록 보장하기 위함입니다.

라라벨이 제공하는 거의 모든 주요 기능은 서비스 프로바이더를 통해 초기화되고 설정됩니다. 즉, 서비스 프로바이더는 프레임워크의 각종 기능을 준비하고 설정하는 중심에 있는 매우 중요한 요소입니다.

<a name="routing"></a>
### 라우팅

애플리케이션에서 가장 중요한 서비스 프로바이더 중 하나가 바로 `App\Providers\RouteServiceProvider`입니다. 이 프로바이더는 애플리케이션의 `routes` 디렉터리에 들어 있는 라우트 파일들을 불러옵니다. 시간이 된다면 직접 `RouteServiceProvider` 코드를 열어보고 어떻게 동작하는지 살펴보시기 바랍니다!

애플리케이션이 모두 초기화되고, 모든 서비스 프로바이더가 등록된 이후에는 요청이 라우터로 넘어가서 실제 라우팅 작업이 진행됩니다. 라우터는 요청을 알맞은 라우트 또는 컨트롤러로 전달하며, 해당 라우트에 지정된 미들웨어도 함께 실행합니다.

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 필터링하거나 검사하는 데 매우 편리한 수단을 제공합니다. 예를 들어, 라라벨에는 애플리케이션 사용자가 인증되어 있는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우, 이 미들웨어는 로그인 화면으로 리다이렉트합니다. 반면 인증된 사용자라면, 요청이 애플리케이션 내부로 계속 전달됩니다. 미들웨어는 애플리케이션의 모든 라우트에 공통으로 적용될 수도 있고(HTTP 커널의 `$middleware` 속성에 정의된 것처럼), 특정 라우트나 라우트 그룹에만 개별적으로 적용할 수도 있습니다. 미들웨어에 대한 자세한 내용은 [미들웨어 설명서](/docs/9.x/middleware)를 참고하세요.

요청이 해당 라우트의 모든 미들웨어를 통과하면, 라우트 또는 컨트롤러의 메서드가 실행되고, 해당 메서드가 반환하는 응답이 다시 라우트의 미들웨어 체인을 거쳐 나가게 됩니다.

<a name="finishing-up"></a>
### 마무리 단계

라우트 또는 컨트롤러의 메서드가 응답을 반환하면, 이 응답은 다시 한번 라우트의 미들웨어를 거치며 애플리케이션이 응답을 수정하거나 검사할 수 있는 기회를 얻게 됩니다.

마지막으로, 응답이 다시 미들웨어를 모두 통과하면 HTTP 커널의 `handle` 메서드가 응답 객체를 반환하고, `index.php` 파일에서 이 응답 객체의 `send` 메서드를 호출합니다. 이렇게 해서 응답 본문이 사용자의 웹 브라우저로 전송됩니다. 이로써 라라벨의 요청 라이프사이클 전체 여정을 마치게 됩니다!

<a name="focus-on-service-providers"></a>
## 서비스 프로바이더에 집중하기

서비스 프로바이더는 라라벨 애플리케이션을 부트스트랩하는 데 있어서 핵심적인 역할을 합니다. 애플리케이션 인스턴스가 생성되고, 서비스 프로바이더들이 등록된 뒤, 요청이 준비된 애플리케이션에 전달되는 구조입니다. 정말 단순하게 설명하면 이렇습니다!

서비스 프로바이더가 어떻게 라라벨 애플리케이션을 초기화하고 준비하는지 잘 이해하면 개발에 큰 도움이 됩니다. 여러분의 애플리케이션에서 기본적으로 제공되는 서비스 프로바이더들은 `app/Providers` 디렉터리에 위치합니다.

기본적으로 `AppServiceProvider`는 큰 역할을 담당하고 있지 않지만, 여러분이 직접 애플리케이션의 새로운 서비스 바인딩이나 부트스트랩 작업을 추가하는 좋은 공간입니다. 규모가 큰 애플리케이션이라면, 각 서비스별로 좀 더 세분화된 부트스트랩을 위해 여러 개의 서비스 프로바이더를 따로 생성하여 관리하는 것이 좋습니다.