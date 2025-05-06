# 브로드캐스팅

- [소개](#introduction)
- [서버 사이드 설치](#server-side-installation)
    - [설정](#configuration)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [오픈소스 대안](#open-source-alternatives)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅 & 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인증](#authorizing-channels)
    - [인증 라우트 정의](#defining-authorization-routes)
    - [인증 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스트](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프리즌스 채널(Presence Channels)](#presence-channels)
    - [프리즌스 채널 인증](#authorizing-presence-channels)
    - [프리즌스 채널 가입](#joining-presence-channels)
    - [프리즌스 채널 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

많은 현대 웹 애플리케이션에서는 WebSocket을 이용해 실시간 라이브 UI를 구현합니다. 서버에서 데이터가 업데이트되면, 일반적으로 메시지가 WebSocket을 통해 클라이언트로 전송되어 처리됩니다. WebSocket은 UI에 반영할 데이터의 변경을 지속적으로 폴링하는 것보다 효율적인 대안을 제공합니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내어 이메일로 전송하는 기능이 있다고 가정해봅시다. CSV 파일 생성에는 몇 분이 걸릴 수 있으므로, [큐 작업](/docs/{{version}}/queues)에서 파일을 생성하여 메일로 전송하기로 결정할 수 있습니다. CSV 파일이 생성되어 사용자에게 메일로 전송되면, `App\Events\UserDataExported` 이벤트를 브로드캐스팅하여 애플리케이션의 JavaScript가 이벤트를 수신할 수 있습니다. 이벤트가 수신되면, 사용자는 새로고침 없이도 "CSV가 메일로 전송되었다"는 메시지를 볼 수 있습니다.

이러한 기능 구축을 돕기 위해 Laravel은 서버 사이드 이벤트([이벤트](/docs/{{version}}/events))를 WebSocket을 통해 쉽게 "브로드캐스트"할 수 있게 해줍니다. Laravel 이벤트를 브로드캐스트하면, 서버 사이드와 클라이언트 사이드(JavaScript) 애플리케이션에서 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 단순합니다. 클라이언트는 프론트엔드의 이름이 지정된 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에 제공하고 싶은 모든 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 두 가지 서버 사이드 브로드캐스트 드라이버를 제공합니다: [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.io). 또한, [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction), [soketi](https://docs.soketi.app/)와 같은 커뮤니티 패키지를 통해 상용 브로드캐스트 제공자가 필요하지 않은 추가 드라이버를 사용할 수 있습니다.

> {tip} 이벤트 브로드캐스팅을 시작하기 전에 반드시 [이벤트와 리스너](/docs/{{version}}/events) 문서를 먼저 읽으세요.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel의 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션에서 일부 설정을 하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스트 드라이버를 사용하여 Laravel 이벤트를 브라우저의 Laravel Echo(JavaScript 라이브러리)가 수신할 수 있도록 브로드캐스트합니다. 걱정하지 마세요. 설치 과정을 단계적으로 안내합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스트 설정은 `config/broadcasting.php` 파일에 저장되어 있습니다. Laravel은 기본적으로 [Pusher Channels](https://pusher.com/channels), [Redis](/docs/{{version}}/redis), 그리고 로컬 개발/디버깅을 위한 `log` 드라이버를 지원합니다. 또한, 테스트 중 브로드캐스팅을 완전히 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버에 대한 설정 예제가 `config/broadcasting.php` 파일에 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### 브로드캐스트 서비스 프로바이더

이벤트를 브로드캐스트하기 전에, 먼저 `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 새로운 Laravel 애플리케이션에서는 `config/app.php` 파일의 `providers` 배열에서 이 프로바이더의 주석만 해제하면 됩니다. 이 서비스 프로바이더는 브로드캐스트 인증 라우트와 콜백을 등록하는 데 필요한 코드가 포함되어 있습니다.

<a name="queue-configuration"></a>
#### 큐 설정

[큐 워커](/docs/{{version}}/queues)도 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업으로 처리되므로, 브로드캐스트로 인해 애플리케이션의 응답 속도가 크게 영향을 받지 않습니다.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 통해 이벤트를 브로드캐스트하려면 Composer 패키지 관리자를 사용하여 Pusher Channels PHP SDK를 설치해야 합니다:

    composer require pusher/pusher-php-server

그 다음, `config/broadcasting.php` 파일에서 Pusher Channels 인증 정보를 설정하면 됩니다. 이 파일에는 이미 Pusher Channels 설정 예제가 포함되어 있으므로 키, 시크릿, 앱 ID만 빠르게 지정하면 됩니다. 일반적으로 이 값들은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 설정합니다:

    PUSHER_APP_ID=your-pusher-app-id
    PUSHER_APP_KEY=your-pusher-key
    PUSHER_APP_SECRET=your-pusher-secret
    PUSHER_APP_CLUSTER=mt1

`config/broadcasting.php`의 `pusher` 설정에서는 클러스터 등 Channels에서 지원하는 추가 `options`도 지정할 수 있습니다.

다음으로, `.env` 파일에서 브로드캐스트 드라이버를 `pusher`로 변경하세요:

    BROADCAST_DRIVER=pusher

이제 [Laravel Echo](#client-side-installation)를 설치 및 설정하면 클라이언트에서 브로드캐스트 이벤트를 수신할 준비가 됩니다.

<a name="pusher-compatible-open-source-alternatives"></a>
#### 오픈소스 Pusher 대안

[laravel-websockets](https://github.com/beyondcode/laravel-websockets)와 [soketi](https://docs.soketi.app/) 패키지는 Laravel을 위한 Pusher 호환 WebSocket 서버를 제공합니다. 이 패키지들을 이용하면 상용 WebSocket 제공자 없이도 Laravel 브로드캐스팅의 모든 기능을 활용할 수 있습니다. 설치 및 사용에 대한 자세한 정보는 [오픈소스 대안](#open-source-alternatives) 문서를 참고하세요.

<a name="ably"></a>
### Ably

[Ably](https://ably.io)를 통해 이벤트를 브로드캐스트하려면 Composer로 Ably PHP SDK를 설치하세요:

    composer require ably/ably-php

그 다음, `config/broadcasting.php`에서 Ably 인증 정보를 설정합니다. 이 파일에는 Ably 설정 예제도 포함되어 있으므로 키만 지정하면 됩니다. 보통 이 값은 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 설정합니다:

    ABLY_KEY=your-ably-key

이제 `.env` 파일에서 브로드캐스트 드라이버를 `ably`로 변경하세요:

    BROADCAST_DRIVER=ably

[Laravel Echo](#client-side-installation)를 설치 및 설정하여 클라이언트에서 브로드캐스트 이벤트를 수신하세요.

<a name="open-source-alternatives"></a>
### 오픈소스 대안

<a name="open-source-alternatives-php"></a>
#### PHP

[laravel-websockets](https://github.com/beyondcode/laravel-websockets) 패키지는 Laravel을 위한 순수 PHP 기반의 Pusher 호환 WebSocket 패키지입니다. 이 패키지를 사용하면 상용 WebSocket 제공자 없이도 브로드캐스팅 기능을 모두 사용할 수 있습니다. 설치 및 사용에 관한 자세한 내용은 [공식 문서](https://beyondco.de/docs/laravel-websockets)를 참조하세요.

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반의 Laravel용 Pusher 호환 WebSocket 서버입니다. 내부적으로 Soketi는 고성능과 확장성을 위해 µWebSockets.js를 사용합니다. 이 패키지는 상용 WebSocket 제공자 없이도 Laravel 브로드캐스팅 기능을 이용할 수 있게 해줍니다. 설치 및 사용법은 [공식 문서](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트하는 채널에 구독하고 이벤트를 듣는 것을 쉽게 해주는 JavaScript 라이브러리입니다. Echo는 NPM 패키지 관리자로 설치할 수 있습니다. 이 예제에서는 Pusher Channels 브로드캐스터를 사용할 것이므로 `pusher-js` 패키지도 함께 설치합니다:

```bash
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 완료되면, 애플리케이션 JavaScript에서 새로운 Echo 인스턴스를 만들 준비가 끝납니다. 좋은 위치는 Laravel 프레임워크에 기본 포함된 `resources/js/bootstrap.js` 파일의 하단입니다. 기본적으로 이 파일에는 Echo 설정 예제가 포함되어 있으며, 주석 처리를 해제해서 사용하면 됩니다:

```js
import Echo from 'laravel-echo';

window.Pusher = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: process.env.MIX_PUSHER_APP_KEY,
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

설정을 본인 상황에 맞게 수정한 후, 애플리케이션의 에셋을 컴파일하세요:

    npm run dev

> {tip} 애플리케이션의 JavaScript 에셋을 컴파일하는 방법은 [Laravel Mix](/docs/{{version}}/mix) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

미리 구성된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo의 `client` 옵션을 통해 사용할 수 있습니다:

```js
import Echo from 'laravel-echo';

const client = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: 'your-pusher-channels-key',
    client: client
});
```

<a name="client-ably"></a>
### Ably

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트하는 이벤트를 듣고 채널에 구독하는 것을 손쉽게 해주는 JavaScript 라이브러리입니다. Echo는 NPM 패키지로 설치할 수 있으며, 이 예제에서도 `pusher-js` 패키지를 함께 설치합니다.

Ably로 브로드캐스트하더라도 `pusher-js` JavaScript 라이브러리를 설치하는 이유가 궁금할 수 있습니다. Ably는 Pusher 프로토콜 호환 모드를 제공하므로, 클라이언트 앱에서 이벤트를 들을 때 Pusher 프로토콜을 사용할 수 있습니다:

```bash
npm install --save-dev laravel-echo pusher-js
```

**계속 진행하기 전, Ably 앱 설정 대시보드의 'Protocol Adapter Settings' 섹션에서 Pusher 프로토콜 지원을 활성화해야 합니다.**

Echo를 설치 완료하면, 새 Echo 인스턴스를 애플리케이션의 JavaScript에서 생성하세요. 추천 위치는 Laravel 프레임워크의 `resources/js/bootstrap.js` 파일 하단입니다. 이 파일에는 이미 Echo 설정 예제가 포함되어 있으나, 기본 설정은 Pusher용입니다. 아래 설정 예제로 Ably로 전환할 수 있습니다:

```js
import Echo from 'laravel-echo';

window.Pusher = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: process.env.MIX_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

Ably Echo 설정의 `MIX_ABLY_PUBLIC_KEY` 환경 변수는 Ably 퍼블릭 키여야 합니다. 퍼블릭 키는 Ably 키에서 `:` 앞 부분입니다.

설정을 적용하고 저장한 뒤, 애플리케이션의 에셋을 컴파일하세요:

    npm run dev

> {tip} 애플리케이션의 JavaScript 에셋 빌드 방법은 [Laravel Mix](/docs/{{version}}/mix) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel의 이벤트 브로드캐스팅은 드라이버 기반 WebSocket 접근 방식으로 서버 사이드 이벤트를 클라이언트 사이드 JavaScript에 브로드캐스트할 수 있게 해줍니다. 현재, Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.io) 드라이버를 지원합니다. 이벤트는 [Laravel Echo](#client-side-installation) JavaScript 패키지로 클라이언트에서 간편하게 수신할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트 됩니다. 이 채널은 공개 또는 비공개로 지정할 수 있습니다. 애플리케이션의 모든 방문자는 인증/인가 없이 공개 채널을 구독할 수 있지만, 비공개 채널을 구독하려면 해당 채널을 수신할 권한이 있어야 합니다.

> {tip} Pusher의 오픈소스 대안을 탐색하고 싶다면 [오픈소스 대안](#open-source-alternatives) 문서를 확인하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

이벤트 브로드캐스팅의 각 컴포넌트로 들어가기 전에, 전반적인 흐름을 전자상거래 스토어 예시로 개략적으로 살펴봅시다.

애플리케이션에 사용자가 자신 주문의 배송 상태를 볼 수 있는 페이지가 있다고 가정합시다. 또한, 배송 상태가 업데이트되면 `OrderShipmentStatusUpdated` 이벤트가 발생합니다:

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 자신 주문을 볼 때, 상태 업데이트를 확인하려고 새로고침하지 않도록, 업데이트 발생 시 애플리케이션에 직접 전달하고 싶습니다. 그러려면 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 그러면 이벤트가 발생할 때마다 Laravel이 브로드캐스트하게 됩니다:

    <?php

    namespace App\Events;

    use App\Models\Order;
    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\InteractsWithSockets;
    use Illuminate\Broadcasting\PresenceChannel;
    use Illuminate\Broadcasting\PrivateChannel;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Queue\SerializesModels;

    class OrderShipmentStatusUpdated implements ShouldBroadcast
    {
        /**
         * 주문 객체 인스턴스.
         *
         * @var \App\Order
         */
        public $order;
    }

`ShouldBroadcast` 인터페이스는 이벤트에 `broadcastOn` 메소드 정의를 요구합니다. 이 메소드는 이벤트가 브로드캐스트될 채널을 반환하는 역할을 합니다. 이 메소드의 빈 스텁은 자동 생성된 이벤트 클래스에 이미 포함되어 있으므로, 상세 구현만 넣으면 됩니다. 주문을 생성한 사용자만 상태를 볼 수 있으면 좋으니, 주문에 연결된 비공개 채널에 브로드캐스트합니다:

    /**
     * 이벤트가 브로드캐스트될 채널 반환
     *
     * @return \Illuminate\Broadcasting\PrivateChannel
     */
    public function broadcastOn()
    {
        return new PrivateChannel('orders.'.$this->order->id);
    }

<a name="example-application-authorizing-channels"></a>
#### 채널 인증

비공개 채널을 듣기 위해서는 사용자의 인증이 필요합니다. 애플리케이션의 `routes/channels.php` 파일에 인증 로직을 정의할 수 있습니다. 예제에서는 비공개 `orders.1` 채널을 구독하려는 사용자가 실제로 그 주문의 생성자인지 확인합니다:

    use App\Models\Order;

    Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

`channel` 메소드는 두 개의 인자를 받습니다: 채널명, 그리고 사용자가 구독 권한이 있는지 true/false를 반환하는 콜백 함수입니다.

모든 인증 콜백은 현재 인증된 사용자가 첫 번째 파라미터로, 와일드카드 파라미터가 두 번째부터 전달됩니다. 이 예제에서는 `{orderId}` 플레이스홀더를 사용해 채널명 일부가 와일드카드임을 표시합니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신

마지막으로, JavaScript 애플리케이션에서 이벤트를 수신만 하면 됩니다. [Laravel Echo](#client-side-installation)를 사용하여 다음과 같이 구현할 수 있습니다. 먼저 `private` 메소드로 비공개 채널에 구독한 후, `listen` 메소드로 `OrderShipmentStatusUpdated` 이벤트를 감지합니다. 이벤트의 모든 public 속성은 브로드캐스트 페이로드로 자동 포함됩니다.

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

Laravel에 특정 이벤트를 브로드캐스트해야 한다고 알리려면 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 이미 import되어 있어, 쉽게 사용할 수 있습니다.

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메소드 하나만 구현하면 됩니다. 이 메소드는 이벤트가 브로드캐스트될 하나 또는 여러 채널을 반환해야 하고, 채널은 `Channel`, `PrivateChannel`, `PresenceChannel`의 인스턴스여야 합니다. `Channel`은 모든 사용자가 구독 가능한 공개 채널, `PrivateChannel`과 `PresenceChannel`은 인증이 필요한 비공개 채널입니다.

    <?php

    namespace App\Events;

    use App\Models\User;
    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\InteractsWithSockets;
    use Illuminate\Broadcasting\PresenceChannel;
    use Illuminate\Broadcasting\PrivateChannel;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Queue\SerializesModels;

    class ServerCreated implements ShouldBroadcast
    {
        use SerializesModels;

        /**
         * 서버를 생성한 사용자
         *
         * @var \App\Models\User
         */
        public $user;

        /**
         * 새 이벤트 인스턴스 생성
         *
         * @param  \App\Models\User  $user
         * @return void
         */
        public function __construct(User $user)
        {
            $this->user = $user;
        }

        /**
         * 이벤트가 브로드캐스트될 채널 반환
         *
         * @return Channel|array
         */
        public function broadcastOn()
        {
            return new PrivateChannel('user.'.$this->user->id);
        }
    }

이제 `ShouldBroadcast` 인터페이스를 구현했다면, [이벤트를 발생시키는](/docs/{{version}}/events) 것만으로 브로드캐스트가 동작합니다. 이벤트가 발생하면, [큐 작업](/docs/{{version}}/queues)을 통해 지정한 드라이버로 브로드캐스트됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스명의 이름으로 브로드캐스트합니다. 하지만, `broadcastAs` 메소드를 정의해서 이름을 커스터마이징 할 수 있습니다:

    /**
     * 이벤트의 브로드캐스트 이름
     *
     * @return string
     */
    public function broadcastAs()
    {
        return 'server.created';
    }

이 경우, 리스너를 등록할 때 이벤트 이름 앞에 `.`을 붙여야 Echo가 애플리케이션 네임스페이스를 붙이지 않도록 합니다:

    .listen('.server.created', function (e) {
        ....
    });

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 모든 `public` 속성은 자동으로 직렬화되어 페이로드에 포함되어 JavaScript 애플리케이션에서 사용할 수 있습니다. 예를 들어, `$user` 속성이 포함된 이벤트라면 페이로드는 다음과 같습니다:

    {
        "user": {
            "id": 1,
            "name": "Patrick Stewart"
            ...
        }
    }

브로드캐스트 페이로드를 세밀하게 제어하고 싶으면, `broadcastWith` 메소드를 추가하고 반환 값을 배열로 지정하면 됩니다:

    /**
     * 브로드캐스팅할 데이터 반환
     *
     * @return array
     */
    public function broadcastWith()
    {
        return ['id' => $this->user->id];
    }

<a name="broadcast-queue"></a>
### 브로드캐스트 큐

각 브로드캐스트 이벤트는 기본적으로 `queue.php` 설정 파일의 기본 큐 및 커넥션에 배치됩니다. 이벤트 클래스에 `connection` 및 `queue` 속성을 정의하면, 사용할 큐 커넥션과 큐명을 직접 지정할 수 있습니다:

    /**
     * 브로드캐스트 시 사용할 큐 커넥션 이름
     *
     * @var string
     */
    public $connection = 'redis';

    /**
     * 브로드캐스트 작업이 할당될 큐 이름
     *
     * @var string
     */
    public $queue = 'default';

아니면, `broadcastQueue` 메소드를 정의해 큐명을 직접 반환할 수도 있습니다:

    /**
     * 브로드캐스트 작업의 큐 이름 반환
     *
     * @return string
     */
    public function broadcastQueue()
    {
        return 'default';
    }

`ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면, 기본적으로 `sync` 큐로 이벤트를 브로드캐스트합니다:

    <?php

    use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

    class OrderShipmentStatusUpdated implements ShouldBroadcastNow
    {
        //
    }

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건이 true일 때만 이벤트를 브로드캐스트하고 싶을 때는, 이벤트 클래스에 `broadcastWhen` 메소드를 추가하세요:

    /**
     * 이 이벤트를 브로드캐스트할지 결정
     *
     * @return bool
     */
    public function broadcastWhen()
    {
        return $this->order->value > 100;
    }

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅 & 데이터베이스 트랜잭션

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐가 DB 트랜잭션 커밋 전에 작업을 처리할 수 있습니다. 이 경우, 트랜잭션 중 변경된 모델/레코드가 아직 DB에 반영되지 않았을 수 있습니다. 이벤트가 이런 모델에 의존한다면, 예상치 못한 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`라면, 이벤트 클래스에 `$afterCommit` 속성을 `true`로 정의하여 모든 열려있는 DB 트랜잭션 커밋 이후에 이벤트가 디스패치되게 할 수 있습니다:

    <?php

    namespace App\Events;

    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Queue\SerializesModels;

    class ServerCreated implements ShouldBroadcast
    {
        use SerializesModels;

        public $afterCommit = true;
    }

> {tip} 이 문제의 우회 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인증

비공개 채널은, 현재 인증된 사용자가 해당 채널을 들을 수 있는지 인증해야 합니다. 이는 채널 이름을 포함한 HTTP 요청을 Laravel 애플리케이션으로 보내고, Laravel이 요청 사용자가 채널을 수신할 수 있는지 판단하여 처리합니다. [Laravel Echo](#client-side-installation)를 사용할 때는 자동으로 인증 요청을 보내지만, 응답할 적절한 라우트는 직접 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 인증 라우트 정의

Laravel은 인증 요청에 응답할 라우트를 쉽게 정의할 수 있도록 해줍니다. Laravel에 기본 포함된 `App\Providers\BroadcastServiceProvider`에는 `Broadcast::routes` 메소드가 호출되어 있으며, 이는 `/broadcasting/auth` 엔드포인트 라우트를 자동 등록합니다:

    Broadcast::routes();

`Broadcast::routes`는 기본적으로 라우트를 `web` 미들웨어 그룹에 넣지만, 배열 형태로 라우트 속성을 전달해 커스터마이징할 수 있습니다:

    Broadcast::routes($attributes);

<a name="customizing-the-authorization-endpoint"></a>
#### 인증 엔드포인트 커스터마이징

기본적으로 Echo는 `/broadcasting/auth` 엔드포인트로 채널 인증을 요청합니다. 하지만 Echo 인스턴스의 `authEndpoint` 설정 옵션을 사용하면 원하는 엔드포인트를 사용할 수 있습니다:

    window.Echo = new Echo({
        broadcaster: 'pusher',
        // ...
        authEndpoint: '/custom/endpoint/auth'
    });

<a name="customizing-the-authorization-request"></a>
#### 인증 요청 커스터마이징

Echo를 초기화할 때 `authorizer` 옵션을 제공해서 인증 요청 방식을 직접 지정할 수도 있습니다:

    window.Echo = new Echo({
        // ...
        authorizer: (channel, options) => {
            return {
                authorize: (socketId, callback) => {
                    axios.post('/api/broadcasting/auth', {
                        socket_id: socketId,
                        channel_name: channel.name
                    })
                    .then(response => {
                        callback(false, response.data);
                    })
                    .catch(error => {
                        callback(true, error);
                    });
                }
            };
        },
    })

<a name="defining-authorization-callbacks"></a>
### 인증 콜백 정의

이제 실제로 인증된 사용자가 주어진 채널을 들을 수 있는지 판단하는 로직을 정의해야 합니다. 이 로직은 기본적으로 포함된 `routes/channels.php` 파일에 정의합니다. 여기서 `Broadcast::channel` 메소드를 통해 채널 인증 콜백을 등록할 수 있습니다:

    Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

모든 인증 콜백은 현재 인증된 사용자와 추가 와일드카드 파라미터를 받습니다. 예제에서는 `{orderId}`를 사용하여 채널 명에 와일드카드를 사용하는 것을 볼 수 있습니다.

<a name="authorization-callback-model-binding"></a>
#### 인증 콜백 모델 바인딩

HTTP 라우트와 마찬가지로, 채널 라우트도 암시적/명시적 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어 문자열이 아닌 실제 `Order` 모델 인스턴스를 받을 수 있습니다:

    use App\Models\Order;

    Broadcast::channel('orders.{order}', function ($user, Order $order) {
        return $user->id === $order->user_id;
    });

> {note} HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 [자동 암시적 스코핑](/docs/{{version}}/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 그러나 대부분의 경우 단일 모델의 primary key로 스코프 하면 충분합니다.

<a name="authorization-callback-authentication"></a>
#### 인증 콜백에서의 인증

비공개/프리즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드로 현재 사용자를 인증합니다. 인증되지 않은 경우, 인증 콜백이 실행되지 않고 인증은 자동 거부됩니다. 필요하다면 여러 개의 커스텀 가드를 지정해서 인증 요청을 허용할 수 있습니다:

    Broadcast::channel('channel', function () {
        // ...
    }, ['guards' => ['web', 'admin']]);

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

여러 채널을 사용하는 경우 `routes/channels.php` 파일이 커질 수 있습니다. 이때 클로저 대신 채널 클래스를 생성해서 인증 로직을 분리 운영할 수 있습니다. `make:channel` 아티즌 명령어로 채널 클래스를 만들 수 있습니다. 이 클래스는 `App/Broadcasting` 디렉터리에 생성됩니다.

    php artisan make:channel OrderChannel

이제 `routes/channels.php` 파일에서 채널을 클래스에 연결하세요:

    use App\Broadcasting\OrderChannel;

    Broadcast::channel('orders.{order}', OrderChannel::class);

채널 클래스의 `join` 메소드에서 인증 로직을 구현하면 됩니다. 이 메소드 안에서도 모델 바인딩을 사용할 수 있습니다:

    <?php

    namespace App\Broadcasting;

    use App\Models\Order;
    use App\Models\User;

    class OrderChannel
    {
        public function __construct()
        {
            //
        }

        /**
         * 사용자의 채널 접근을 인증합니다.
         *
         * @param  \App\Models\User  $user
         * @param  \App\Models\Order  $order
         * @return array|bool
         */
        public function join(User $user, Order $order)
        {
            return $user->id === $order->user_id;
        }
    }

> {tip} Laravel의 많은 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)에서 자동 해결됩니다. 따라서 생성자에 필요한 의존성은 타입힌트로 명시하면 됩니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현했다면, 이벤트의 dispatch 메소드를 사용해 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처가 이 인터페이스가 구현된 이벤트임을 인식하고, 브로드캐스트 큐로 자동 등록합니다:

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스트

브로드캐스팅을 활용할 때, 현재 사용자 자신을 제외한 구독자들에게만 이벤트를 브로드캐스트할 필요가 있을 수 있습니다. `broadcast` 헬퍼와 `toOthers` 메소드를 사용하여 이를 구현할 수 있습니다:

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->toOthers();

예를 들어, 할 일 목록 애플리케이션을 가정해 봅시다. 사용자가 새 할 일을 추가하면, `/task` 엔드포인트에 요청해서 할 일이 생성됐다면 JSON을 바로 tasks 배열에 푸시할 수 있습니다:

    axios.post('/task', task)
        .then((response) => {
            this.tasks.push(response.data);
        });

하지만 이벤트도 브로드캐스트하기 때문에, 리스닝할 때 tasks 배열에 같은 할 일이 반복 추가될 수 있습니다. 이럴 때 `toOthers` 메소드를 사용해 브로드캐스트가 본인에게는 발생하지 않게 설정합니다.

> {note} `toOthers` 메소드 사용을 위해서는 이벤트에서 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스가 초기화되면 소켓 ID가 커넥션에 할당됩니다. 전역 [Axios](https://github.com/mzabriskie/axios)를 사용하면 요청마다 자동으로 `X-Socket-ID` 헤더가 포함됩니다. `toOthers` 메소드를 호출하면 Laravel이 해당 헤더에서 소켓 ID를 읽어, 브로드캐스트 받을 수신자를 제한할 수 있습니다.

전역 Axios를 사용하지 않는 경우, JS 애플리케이션에서 모든 요청 헤더에 `X-Socket-ID`를 수동으로 추가해야 합니다. 소켓 ID는 `Echo.socketId()`로 가져올 수 있습니다:

    var socketId = Echo.socketId();

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

한 애플리케이션에서 여러 브로드캐스트 커넥션을 사용할 때, 기본 커넥션이 아닌 다른 커넥션을 통해 이벤트를 브로드캐스트하고 싶다면, `via` 메소드를 사용해 어떤 커넥션을 사용할지 지정할 수 있습니다:

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');

이벤트 생성자에서 `broadcastVia` 메소드를 호출해 이벤트의 브로드캐스트 커넥션을 직접 지정할 수도 있습니다. 이때는 이벤트 클래스가 `InteractsWithBroadcasting` 트레이트를 사용해야 합니다:

    <?php

    namespace App\Events;

    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\InteractsWithBroadcasting;
    use Illuminate\Broadcasting\InteractsWithSockets;
    use Illuminate\Broadcasting\PresenceChannel;
    use Illuminate\Broadcasting\PrivateChannel;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Queue\SerializesModels;

    class OrderShipmentStatusUpdated implements ShouldBroadcast
    {
        use InteractsWithBroadcasting;

        public function __construct()
        {
            $this->broadcastVia('pusher');
        }
    }

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo 설치 및 인스턴스화](#client-side-installation)를 끝냈다면, 이제 Laravel에서 브로드캐스트한 이벤트를 수신할 준비가 된 것입니다. 먼저 `channel` 메소드로 채널 인스턴스를 얻고, `listen` 메소드로 특정 이벤트를 감지합니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 이벤트를 감지하려면 `private` 메소드를 사용하세요. 하나의 채널에서 여러 이벤트를 연속해서 감지하려면 `listen` 메소드를 체이닝할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(...)
    .listen(...)
    .listen(...);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중지

채널에서 [아예 나가지 않아도](#leaving-a-channel) 특정 이벤트만 리스닝을 중지하고 싶다면, `stopListening` 메소드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 나가려면 Echo 인스턴스의 `leaveChannel` 메소드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 연관된 비공개/프리즌스 채널 모두 떠나고 싶다면 `leave` 메소드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위의 예시에서 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않은 것을 눈치챘을 것입니다. 이는 Echo가 기본적으로 이벤트가 `App\Events`에 있다고 가정하기 때문입니다. Echo를 인스턴스화하면서 `namespace` 설정 옵션으로 루트 네임스페이스를 조정할 수도 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 이벤트 클래스 앞에 `.`을 붙여 Echo로 구독할 때마다 완전한 네임스페이스명을 명시할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        //
    });
```

<a name="presence-channels"></a>
## 프리즌스 채널(Presence Channels)

프리즌스 채널은 비공개 채널의 보안성을 유지하면서, 누가 채널에 구독 중인지도 알 수 있게 해줍니다. 이를 통해 특정 사용자가 같은 페이지를 보고 있다거나, 채팅방 참여자 목록 등 강력한 협업형 기능을 만들 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프리즌스 채널 인증

프리즌스 채널은 비공개 채널과 동일하게 [인증](#authorizing-channels)이 필요합니다. 다만, 사용자가 인증에 성공한 경우 `true`를 반환하는 대신, 사용자의 정보를 담은 배열을 반환해야 합니다.

이렇게 반환된 데이터는 JavaScript 애플리케이션에서 프리즌스 채널 이벤트 리스너가 사용할 수 있습니다. 인증에 실패하면 `false` 또는 `null`을 반환하세요:

    Broadcast::channel('chat.{roomId}', function ($user, $roomId) {
        if ($user->canJoinRoom($roomId)) {
            return ['id' => $user->id, 'name' => $user->name];
        }
    });

<a name="joining-presence-channels"></a>
### 프리즌스 채널 가입

Presence 채널에 가입하려면 Echo의 `join` 메소드를 사용합니다. 이 메소드는 `here`, `joining`, `leaving` 이벤트에 대응하며, 채널을 성공적으로 구독하면 `here` 콜백이 즉시 실행되고 현재 구독 중인 사용자의 정보를 배열로 제공합니다. `joining`은 새 사용자가 채널에 입장할 때, `leaving`은 사용자가 떠날 때, `error`는 인증 실패나 JSON 파싱 문제 시 실행됩니다.

    Echo.join(`chat.${roomId}`)
        .here((users) => {
            //
        })
        .joining((user) => {
            console.log(user.name);
        })
        .leaving((user) => {
            console.log(user.name);
        })
        .error((error) => {
            console.error(error);
        });

<a name="broadcasting-to-presence-channels"></a>
### 프리즌스 채널 브로드캐스팅

프리즌스 채널도 공개/비공개 채널처럼 이벤트를 받을 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 프리즌스 채널로 브로드캐스트하려면, 이벤트의 `broadcastOn` 메소드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다:

    /**
     * 이벤트가 브로드캐스트될 채널 반환
     *
     * @return Channel|array
     */
    public function broadcastOn()
    {
        return new PresenceChannel('room.'.$this->message->room_id);
    }

다른 이벤트와 마찬가지로, `broadcast` 헬퍼와 `toOthers` 메소드를 활용해 본인에겐 브로드캐스트되지 않도록 할 수 있습니다:

    broadcast(new NewMessage($message));

    broadcast(new NewMessage($message))->toOthers();

또한, Echo의 `listen` 메소드로 프리즌스 채널의 이벤트를 감지할 수 있습니다:

    Echo.join(`chat.${roomId}`)
        .here(...)
        .joining(...)
        .leaving(...)
        .listen('NewMessage', (e) => {
            //
        });

<a name="model-broadcasting"></a>
## 모델 브로드캐스팅

> {note} 모델 브로드캐스팅에 대해 읽기 전에, Laravel의 모델 브로드캐스팅 서비스 일반 개념과 수동 이벤트 생성, 브로드캐스트에 익숙해지시길 권장합니다.

애플리케이션의 [Eloquent 모델](/docs/{{version}}/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 것은 흔한 일입니다. 물론, 상태 변화 시마다 직접 커스텀 이벤트 클래스를 만들어 `ShouldBroadcast` 인터페이스를 구현해도 됩니다.

하지만, 이런 이벤트를 다른 용도로 사용하지 않는다면 단순 브로드캐스트만을 위해 이벤트 클래스를 만드는 것은 번거로울 수 있습니다. 이 문제를 해결하기 위해, Laravel은 Eloquent 모델이 상태 변경 시 자동으로 브로드캐스트되도록 지원합니다.

시작하려면, 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하고, 브로드캐스트할 채널을 반환하는 `broadcastsOn` 메소드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * 이 포스트가 소속된 유저를 반환합니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트될 채널을 반환합니다.
     *
     * @param  string  $event
     * @return \Illuminate\Broadcasting\Channel|array
     */
    public function broadcastOn($event)
    {
        return [$this, $this->user];
    }
}
```

이 트레이트를 추가하고 채널을 정의하면, 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동, 복구될 때마다 자동으로 이벤트가 브로드캐스트됩니다.

또한, `broadcastOn` 메소드는 `$event`라는 문자열 매개변수를 받습니다. 이 값은 모델에서 발생한 이벤트 유형이고, `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이를 검사해 특정 이벤트에서만 브로드캐스트할 채널을 지정할 수 있습니다:

```php
/**
 * 모델 이벤트가 브로드캐스트될 채널을 반환합니다.
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>
#### 모델 브로드캐스트 이벤트 생성 커스터마이징

Laravel에서 기본적으로 생성되는 모델 브로드캐스트 이벤트를 커스터마이징하고 싶을 경우, Eloquent 모델에 `newBroadcastableEvent` 메소드를 정의하면 됩니다. 이 메소드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred

/**
 * 모델용 새 브로드캐스트 이벤트 생성
 *
 * @param  string  $event
 * @return \Illuminate\Database\Eloquent\BroadcastableModelEventOccurred
 */
protected function newBroadcastableEvent($event)
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### 모델 브로드캐스팅 규칙

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 규칙

모델 예제의 `broadcastOn` 메소드가 `Channel` 인스턴스를 반환하지 않고, Eloquent 모델 인스턴스를 직접 반환한 것을 볼 수 있습니다. 만약 모델 인스턴스가 반환되면, Laravel은 모델의 클래스명과 primary key로 `PrivateChannel` 인스턴스를 자동 생성합니다.

예를 들면, `App\Models\User` 모델의 `id`가 1이면 채널명은 `App.Models.User.1`입니다. 물론 완전한 제어가 필요하면 `broadcastOn` 메소드에서 `Channel` 인스턴스를 직접 반환할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트될 채널 반환
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return [new PrivateChannel('user.'.$this->id)];
}
```

채널 생성자에 모델 인스턴스를 직접 넘겨도, 위에서 설명한 채널명 규칙이 적용됩니다:

```php
return [new Channel($this->user)];
```

모델의 채널명을 직접 확인하려면 인스턴스에서 `broadcastChannel` 메소드를 호출하세요. 예를 들어, `App\Models\User` 모델에 `id`가 1이면 `App.Models.User.1`을 반환합니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 `App\Events` 디렉터리 내의 실제 이벤트와 연관되어 있지 않기 때문에, 이름과 페이로드는 규칙에 따라 자동 지정됩니다. Laravel은 모델의 클래스명(네임스페이스 제외)과 해당 모델 이벤트명으로 이벤트를 브로드캐스트합니다.

예를 들어 `App\Models\Post` 모델이 업데이트되면, 클라이언트에서는 `PostUpdated`라는 이름의 이벤트가 다음과 같은 페이로드로 수신됩니다:

    {
        "model": {
            "id": 1,
            "title": "My first post"
            ...
        },
        ...
        "socket": "someSocketId",
    }

`App\Models\User` 모델 삭제는 `UserDeleted` 이벤트명으로 브로드캐스트 됩니다.

직접 커스텀 브로드캐스트 이름/페이로드가 필요하다면, 모델에 `broadcastAs`/`broadcastWith` 메소드를 추가할 수 있습니다. 두 메소드 모두 모델 이벤트명을 파라미터로 받아 상황에 맞게 이름과 페이로드를 커스터마이징할 수 있습니다. 만약 `broadcastAs`에서 null을 반환하면, 위의 규칙이 적용됩니다:

```php
/**
 * 모델 이벤트 브로드캐스트 이름 반환
 *
 * @param  string  $event
 * @return string|null
 */
public function broadcastAs($event)
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델 브로드캐스트 데이터 반환
 *
 * @param  string  $event
 * @return array
 */
public function broadcastWith($event)
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
### 모델 브로드캐스트 리스닝

`BroadcastsEvents` 트레이트를 모델에 추가하고 `broadcastOn` 메소드를 정의했다면, 이제 클라이언트에서 브로드캐스트된 모델 이벤트를 수신할 수 있습니다. 시작 전에 [이벤트 수신 방법](#listening-for-events) 전체 문서를 참고하세요.

먼저 `private` 메소드로 채널 인스턴스를 얻고, `listen`으로 이벤트를 수신하면 됩니다. 일반적으로 채널명은 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)을 따릅니다.

이벤트는 `App\Events` 네임스페이스와 별개로 동작하므로, [이벤트명](#model-broadcasting-event-conventions) 앞에는 `.`을 붙여 네임스페이스가 없음을 표시해야 합니다. 각 모델 브로드캐스트 이벤트의 페이로드에는 `model` 속성이 포함되어 있습니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> {tip} [Pusher Channels](https://pusher.com/channels)를 사용할 때는 [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

종종, Laravel 애플리케이션으로 요청을 보내지 않고도 다른 연결된 클라이언트에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이는, 예를 들어 사용자가 "입력 중"임을 알릴 때 유용합니다(입력 중 알림 등).

클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메소드를 사용하세요:

    Echo.private(`chat.${roomId}`)
        .whisper('typing', {
            name: this.user.name
        });

클라이언트 이벤트 리스닝은 `listenForWhisper` 메소드를 사용합니다:

    Echo.private(`chat.${roomId}`)
        .listenForWhisper('typing', (e) => {
            console.log(e.name);
        });

<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅과 [알림](/docs/{{version}}/notifications)을 결합하면, JavaScript 애플리케이션이 페이지 새로고침 없이 실시간으로 새 알림을 받을 수 있습니다. 시작 전 [브로드캐스트 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 사용법을 꼭 읽어보세요.

브로드캐스트 채널로 알림을 설정했다면, Echo의 `notification` 메소드로 브로드캐스트 이벤트를 수신할 수 있습니다. 이때 채널명은 알림을 받는 엔터티의 클래스명과 일치해야 합니다:

    Echo.private(`App.Models.User.${userId}`)
        .notification((notification) => {
            console.log(notification.type);
        });

이 예제처럼, `App\Models\User` 인스턴스에 브로드캐스트 채널로 전송된 모든 알림은 콜백에서 수신됩니다. `App.Models.User.{id}` 채널에 대한 인증 콜백은 Laravel 프레임워크에 기본 포함된 `BroadcastServiceProvider`에 정의되어 있습니다.