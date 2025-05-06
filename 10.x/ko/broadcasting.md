# 방송(Broadcasting)

- [소개](#introduction)
- [서버 사이드 설치](#server-side-installation)
    - [설정](#configuration)
    - [Reverb](#reverb)
    - [Pusher 채널](#pusher-channels)
    - [Ably](#ably)
    - [오픈소스 대안](#open-source-alternatives)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher 채널](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용하기](#using-example-application)
- [방송 이벤트 정의](#defining-broadcast-events)
    - [방송 이름](#broadcast-name)
    - [방송 데이터](#broadcast-data)
    - [방송 큐](#broadcast-queue)
    - [방송 조건](#broadcast-conditions)
    - [방송과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여](#authorizing-channels)
    - [권한 부여 라우트 정의](#defining-authorization-routes)
    - [권한 부여 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 방송](#broadcasting-events)
    - [다른 사용자에게만 방송하기](#only-to-others)
    - [연결 커스터마이징](#customizing-the-connection)
- [방송 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [Presence 채널](#presence-channels)
    - [Presence 채널 권한 부여](#authorizing-presence-channels)
    - [Presence 채널 참여](#joining-presence-channels)
    - [Presence 채널로 방송하기](#broadcasting-to-presence-channels)
- [모델 방송](#model-broadcasting)
    - [모델 방송 규칙](#model-broadcasting-conventions)
    - [모델 방송 수신](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notifications)](#notifications)

<a name="introduction"></a>
## 소개

최신 웹 애플리케이션에서는 WebSocket을 이용해 실시간(Realtime)의 라이브 UI를 구현하는 경우가 많습니다. 서버의 데이터가 변경되면, 보통 WebSocket 연결을 통해 메시지가 클라이언트로 전송되어 처리됩니다. WebSocket은 애플리케이션 UI에서 반영해야 할 데이터 변화를 위해 서버에 반복적으로 요청을 보내는 방법보다 훨씬 효율적입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내고 이메일로 전송하는 기능이 있다고 가정해봅시다. CSV 파일 생성에 몇 분이 걸린다면, 이를 [큐 작업](/docs/{{version}}/queues)으로 처리하는 것이 좋습니다. CSV가 생성되어 사용자가 이메일을 받은 뒤, 우리는 `App\Events\UserDataExported`라는 이벤트를 방송하여 자바스크립트(프론트엔드)에서 이를 수신할 수 있습니다. 이벤트가 수신되면, 사용자는 페이지를 새로고침할 필요 없이 이메일이 전송됐다는 메시지를 볼 수 있습니다.

이러한 기능을 쉽게 개발할 수 있도록, Laravel은 서버 사이드 이벤트를 WebSocket 연결을 통해 '방송'하는 기능을 제공합니다. Laravel 이벤트를 방송하면, 서버의 Laravel 애플리케이션과 클라이언트의 JavaScript 애플리케이션에서 같은 이벤트 이름과 데이터를 공유할 수 있습니다.

방송의 핵심 개념은 매우 간단합니다: 클라이언트는 프론트엔드에서 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 각 채널로 이벤트를 방송합니다. 이 이벤트는 프론트엔드에서 사용할 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

Laravel은 기본적으로 세 가지 서버 사이드 방송 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), 그리고 [Ably](https://ably.com).

> [!NOTE]  
> 이벤트 방송을 시작하기 전에, [이벤트와 리스너](/docs/{{version}}/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel의 이벤트 방송을 사용하기 위해서는 몇 가지 설정과 패키지 설치가 필요합니다.

이벤트 방송은 서버 사이드 방송 드라이버를 통하여 Laravel의 이벤트를 방송하고, 자바스크립트 라이브러리인 Laravel Echo가 이를 브라우저 클라이언트에서 수신하도록 합니다. 설치 과정을 단계별로 안내하니 걱정하지 않으셔도 됩니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 방송 설정은 `config/broadcasting.php` 파일에 저장됩니다. Laravel은 [Pusher Channels](https://pusher.com/channels), [Redis](/docs/{{version}}/redis), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버를 내장 지원합니다. 또한, 테스트 중에 방송을 완전히 비활성화할 수 있는 `null` 드라이버도 있습니다. 각 드라이버의 설정 예제가 `config/broadcasting.php` 파일에 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### 방송 서비스 프로바이더

이벤트를 방송하기 전에, 먼저 `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 새 Laravel 애플리케이션에서는 `config/app.php`의 `providers` 배열에서 이 프로바이더의 주석을 해제하기만 하면 됩니다. 이 프로바이더에는 방송 권한 인증 라우트와 콜백을 등록하는 데 필요한 코드가 포함되어 있습니다.

<a name="queue-configuration"></a>
#### 큐 설정

또한 [큐 워커](/docs/{{version}}/queues)를 구성하고 실행해야 합니다. 이벤트 방송은 모두 큐 작업으로 처리되어, 이벤트 방송이 애플리케이션의 응답 시간을 심각하게 저하시키지 않도록 보장합니다.

<a name="reverb"></a>
### Reverb

Composer 패키지 관리자를 이용해 Reverb를 설치할 수 있습니다:

```sh
composer require laravel/reverb
```

패키지 설치 후, Reverb의 설치 명령어를 실행해 설정파일을 게시하고, Broadcasting 설정을 갱신하며, Reverb에 필요한 환경변수를 추가하세요:

```sh
php artisan reverb:install
```

자세한 설치 및 사용법은 [Reverb 공식 문서](/docs/{{version}}/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher 채널

[Pusher Channels](https://pusher.com/channels)로 이벤트를 방송할 계획이라면, Composer를 이용해 Pusher Channels PHP SDK를 설치하세요:

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 설정 파일에서 Pusher 채널 자격 증명을 설정하세요. 이 파일에는 예시 설정이 포함되어 있으므로, 키, 시크릿, 앱 ID만 빠르게 지정할 수 있습니다. 일반적으로 이러한 값은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 지정합니다:

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

추가적으로, `config/broadcasting.php`의 `pusher` 설정에서는 클러스터와 같은 추가 `options`도 지정할 수 있습니다.

`BROADCAST_DRIVER`를 `.env` 파일에서 `pusher`로 변경하세요:

```ini
BROADCAST_DRIVER=pusher
```

마지막으로, [Laravel Echo](#client-side-installation)를 설치 및 구성하여, 클라이언트에서 방송 이벤트를 수신할 준비를 하세요.

<a name="pusher-compatible-open-source-alternatives"></a>
#### 오픈소스 Pusher 대안

[soketi](https://docs.soketi.app/)는 Pusher와 호환되는 WebSocket 서버로, 상용 WebSocket 제공자 없이도 Laravel 방송의 모든 기능을 활용할 수 있습니다. 더 자세한 오픈소스 방송 패키지 사용 방법은 [오픈소스 대안](#open-source-alternatives) 문서를 참고하세요.

<a name="ably"></a>
### Ably

> [!NOTE]  
> 아래 설명은 Ably의 "Pusher 호환 모드" 사용법에 대해 다룹니다. 그러나 Ably는 자체 드라이버와 Echo 클라이언트를 유지 관리하며, Ably만의 고유 기능을 활용할 수 있도록 권장합니다. 자세한 내용은 [Ably의 Laravel Broadcaster 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)로 이벤트를 방송할 계획이라면, Composer 패키지 관리자를 이용해 Ably PHP SDK를 설치하세요:

```shell
composer require ably/ably-php
```

그 다음, `config/broadcasting.php`에 Ably 자격 증명을 입력하세요. 예시 설정이 이미 파일에 포함되어 있으며, 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 지정합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 방송 드라이버를 `ably`로 변경하세요:

```ini
BROADCAST_DRIVER=ably
```

이제 [Laravel Echo](#client-side-installation) 설치 및 구성하면, 클라이언트에서 방송 이벤트를 수신할 수 있습니다.

<a name="open-source-alternatives"></a>
### 오픈소스 대안

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반, Pusher 프로토콜과 호환되는 WebSocket 서버입니다. Soketi는 내부적으로 µWebSockets.js를 사용하여 매우 우수한 확장성과 속도를 지원합니다. 이 패키지를 통해 상용 WebSocket 서비스 제공자 없이도 Laravel 방송을 최대한 활용할 수 있습니다. 설치 및 사용법은 [공식 문서](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 방송된 이벤트를 구독하고 리스닝하는 작업을 쉽게 해주는 자바스크립트 라이브러리입니다. NPM을 이용해 설치할 수 있습니다. Reverb는 Pusher 프로토콜을 사용하므로 이 예제에서는 `pusher-js` 패키지도 함께 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면, 애플리케이션의 JavaScript 내에서 새 Echo 인스턴스를 생성하면 됩니다. 보통은 Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단에서 이것을 수행합니다. 기본적으로 Echo 예시 설정이 포함되어 있으므로, 주석을 해제하고 `broadcaster` 옵션을 `reverb`로 변경하면 됩니다:

```js
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT,
    wssPort: import.meta.env.VITE_REVERB_PORT,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

그 다음, 애플리케이션의 자산을 컴파일하세요:

```shell
npm run build
```

> [!WARNING]  
> Laravel Echo의 `reverb` broadcaster는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher 채널

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 방송된 이벤트를 구독하고 리스닝하는 작업을 쉽게 해주는 자바스크립트 라이브러리입니다. NPM을 이용해 설치할 수 있습니다. Pusher Channels broadcaster를 사용할 예정이므로 `pusher-js` 패키지도 함께 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

설치 후에는 JavaScript에서 Echo 인스턴스를 새로 만듭니다. 역시 `resources/js/bootstrap.js` 파일 하단에서 설정하면 좋습니다. Echo의 예시 설정이 이미 파일에 포함되어 있으므로, 주석을 해제하고 필요에 따라 값을 맞추면 됩니다:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

주석을 해제하고, Echo 설정을 필요에 맞게 조정했다면, 애플리케이션의 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]  
> 자바스크립트 자산 컴파일에 대해 더 알고 싶다면 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

미리 설정된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo의 `client` 옵션을 통해 전달할 수 있습니다:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: 'your-pusher-channels-key'
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
### Ably

> [!NOTE]  
> 아래 설명은 Ably "Pusher 호환 모드" 사용법을 다루지만, Ably 팀에서는 자사 드라이버와 Echo 클라이언트를 사용하는 것을 권장합니다. 자세한 내용은 [Ably의 Laravel broadcaster 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 방송된 이벤트를 구독하고 리스닝하는 작업을 쉽게 해주는 자바스크립트 라이브러리입니다. 역시 NPM을 이용해 Echo와 `pusher-js`를 함께 설치하세요.

Ably로 방송하더라도 `pusher-js`를 설치하는 이유는, Ably가 제공하는 Pusher 프로토콜 호환 모드를 사용하기 때문입니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**진행 전, Ably 애플리케이션의 "Protocol Adapter Settings"에서 Pusher 프로토콜 지원을 반드시 활성화하세요.**

Echo 설치 후, 새 Echo 인스턴스를 JavaScript에서 생성합니다. 기본 설정 예시는 `bootstrap.js`에 존재하나, 아래와 같이 Ably로 변경할 수 있습니다:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

여기서 `VITE_ABLY_PUBLIC_KEY` 환경변수는 Ably 키에서 `:` 앞부분에 해당합니다.

설정 후 애플리케이션 자산을 컴파일하세요:

```shell
npm run dev
```

> [!NOTE]  
> 자바스크립트 자산 컴파일에 대해 더 알고 싶다면 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel 이벤트 방송 기능은 드라이버 기반 WebSocket 접근방식으로 서버 사이드 이벤트를 프론트엔드 JavaScript 애플리케이션으로 방송할 수 있게 합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 제공합니다. 방송 이벤트들은 [Laravel Echo](#client-side-installation)를 통해 손쉽게 수신할 수 있습니다.

이벤트는 '채널'을 통해 방송되며, 채널은 공개(public) 또는 비공개(private)로 구분될 수 있습니다. 애플리케이션의 모든 방문자는 인증 및 권한 없이 공개 채널을 구독할 수 있습니다. 하지만 비공개 채널에 구독하려면 사용자의 인증과 권한 부여가 필요합니다.

> [!NOTE]  
> Pusher의 오픈소스 대안이 궁금하다면 [오픈소스 대안](#open-source-alternatives) 섹션을 참고하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

이벤트 방송의 각 구성요소를 본격적으로 살펴보기 전에, 전자상거래(e-commerce) 스토어 예시를 통해 한 번에 큰 흐름을 이해해봅시다.

애플리케이션에 사용자가 자신의 주문 배송 상태를 볼 수 있는 페이지가 있다고 가정합니다. 배송 상태가 변경되면 `OrderShipmentStatusUpdated` 이벤트를 발생시킨다고 해봅시다:

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 상세 페이지를 보고 있을 때, 새로고침 없이 상태 업데이트를 보고싶을 것입니다. 그러므로 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해주어, 이벤트 발생 시 자동으로 방송되도록 해야 합니다:

    <?php

    namespace App\Events;

    use App\Models\Order;
    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\InteractsWithSockets;
    use Illuminate\Broadcasting\PresenceChannel;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Queue\SerializesModels;

    class OrderShipmentStatusUpdated implements ShouldBroadcast
    {
        /**
         * 주문 인스턴스
         *
         * @var \App\Models\Order
         */
        public $order;
    }

`ShouldBroadcast` 인터페이스를 구현하면, 이벤트에 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트가 방송될 채널(들)을 반환합니다. 기본 이벤트 클래스에는 이미 빈 스텁이 생성되어 있으니, 내부 내용만 작성해주면 됩니다. 우리는 주문 생성자가 상태를 볼 수 있게 하고 싶으니, 이벤트를 해당 주문 ID로 비공개 채널에 방송합니다:

    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\PrivateChannel;

    /**
     * 이벤트가 방송될 채널을 반환합니다.
     */
    public function broadcastOn(): Channel
    {
        return new PrivateChannel('orders.'.$this->order->id);
    }

여러 채널에 방송하려는 경우, 배열을 반환할 수도 있습니다:

    use Illuminate\Broadcasting\PrivateChannel;

    /**
     * 이벤트가 방송될 채널 목록을 반환합니다.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('orders.'.$this->order->id),
            // ...
        ];
    }

<a name="example-application-authorizing-channels"></a>
#### 채널 권한 부여

비공개 채널에 리스닝하려면 사용자 권한 인증이 필수입니다. `routes/channels.php` 파일에서 채널 권한 부여 규칙을 정의할 수 있습니다. 예를 들어, `orders.1` 비공개 채널에 리스닝을 시도하는 사용자가 실제 해당 주문의 생성자인지 확인해야 합니다:

    use App\Models\Order;
    use App\Models\User;

    Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

`channel` 메서드는 채널명과 ‘해당 사용자가 권한이 있는지’(true/false)를 반환하는 콜백 두 개를 인자로 받습니다. 모든 인증 콜백 함수는 로그인된 사용자를 첫 번째 인자로 받고, 이후 와일드카드 파라미터들을 그 다음 인자로 받습니다. 여기서는 `{orderId}` 플레이스홀더를 사용했습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 방송 리스닝

마지막으로, JavaScript 애플리케이션에서 이벤트를 리스닝하면 됩니다. [Laravel Echo](#client-side-installation)를 사용합니다. 먼저 `private` 메서드로 비공개 채널을 구독하고, `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 수신합니다. 기본적으로 이벤트의 퍼블릭 프로퍼티가 방송 데이터에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 방송 이벤트 정의

어떤 이벤트를 방송해야 한다고 Laravel에 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현하면 됩니다. 이 인터페이스는 이미 프레임워크가 생성한 모든 이벤트 클래스에 임포트되어 있어서 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 오직 하나의 메서드 `broadcastOn` 만 구현하면 됩니다. 이 메서드는 Channel, PrivateChannel, PresenceChannel 인스턴스 또는 그 배열을 반환해야 합니다. Channel은 공개 채널, PrivateChannel 및 PresenceChannel은 [채널 권한 부여](#authorizing-channels)가 필요한 비공개 채널입니다.

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
         * 새로운 이벤트 인스턴스를 생성합니다.
         */
        public function __construct(
            public User $user,
        ) {}

        /**
         * 이벤트가 방송될 채널을 반환합니다.
         *
         * @return array<int, \Illuminate\Broadcasting\Channel>
         */
        public function broadcastOn(): array
        {
            return [
                new PrivateChannel('user.'.$this->user->id),
            ];
        }
    }

이제 `ShouldBroadcast`를 구현했으므로, [이벤트를 발생](/docs/{{version}}/events)시 내부적으로 지정한 방송 드라이버를 통해 큐 작업으로 이벤트가 자동 방송됩니다.

<a name="broadcast-name"></a>
### 방송 이름

기본적으로 Laravel은 이벤트 클래스 이름을 그대로 방송 이름으로 사용합니다. 방송 이름을 커스터마이징하려면, `broadcastAs` 메서드를 정의할 수 있습니다:

    /**
     * 방송 이벤트 이름을 반환합니다.
     */
    public function broadcastAs(): string
    {
        return 'server.created';
    }

`broadcastAs`로 방송 이름을 변경한 경우, 리스너 등록 시 앞에 `.`을 반드시 붙여야 네임스페이스가 추가되지 않습니다:

    .listen('.server.created', function (e) {
        ....
    });

<a name="broadcast-data"></a>
### 방송 데이터

이벤트의 `public` 프로퍼티는 자동으로 시리얼라이즈되어 방송 페이로드로 포함되어, 자바스크립트에서 접근할 수 있습니다. 예를 들어, 이벤트에 퍼블릭 `$user` 프로퍼티가 있다면 방송 데이터는 다음과 같이 됩니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

더 세밀하게 방송 페이로드를 제어하려면, 이벤트에 `broadcastWith` 메서드를 추가하면 됩니다. 이 메서드는 방송할 데이터 배열을 반환합니다:

    /**
     * 방송할 데이터를 반환합니다.
     *
     * @return array<string, mixed>
     */
    public function broadcastWith(): array
    {
        return ['id' => $this->user->id];
    }

<a name="broadcast-queue"></a>
### 방송 큐

기본적으로, 방송 이벤트는 `queue.php` 설정 파일의 기본 큐 연결과 큐 이름에 할당됩니다. `connection`과 `queue` 프로퍼티를 이벤트 클래스에 정의하면, 방송시 사용할 큐 연결과 큐 이름을 별도로 지정할 수 있습니다:

    /**
     * 방송시 사용할 큐 연결명
     *
     * @var string
     */
    public $connection = 'redis';

    /**
     * 방송 작업이 제출될 큐 이름
     *
     * @var string
     */
    public $queue = 'default';

또는, `broadcastQueue` 메서드를 정의해 큐 이름만 별도로 지정할 수도 있습니다:

    /**
     * 방송 작업이 제출될 큐 이름
     */
    public function broadcastQueue(): string
    {
        return 'default';
    }

`sync` 큐 드라이버를 방송에 사용하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다:

    <?php

    use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

    class OrderShipmentStatusUpdated implements ShouldBroadcastNow
    {
        // ...
    }

<a name="broadcast-conditions"></a>
### 방송 조건

특정 조건일 때만 이벤트 방송이 필요하다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하면 됩니다:

    /**
     * 이 이벤트를 방송할지 여부를 반환합니다.
     */
    public function broadcastWhen(): bool
    {
        return $this->order->value > 100;
    }

<a name="broadcasting-and-database-transactions"></a>
#### 방송과 데이터베이스 트랜잭션

방송 이벤트가 데이터베이스 트랜잭션 내에서 디스패치되면, 큐가 트랜잭션이 커밋되기 전에 이벤트를 처리할 수도 있습니다. 이렇게 되면, 트랜잭션 도중 변경된 모델/레코드가 DB에 반영되지 않았거나, 생성된 데이터가 아직 존재하지 않을 수 있어 예기치 못한 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`여도, 해당 이벤트에 `ShouldDispatchAfterCommit` 인터페이스를 구현하여 모든 오픈된 DB 트랜잭션 커밋 후에만 이벤트가 디스패치되게 할 수 있습니다:

    <?php

    namespace App\Events;

    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
    use Illuminate\Queue\SerializesModels;

    class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
    {
        use SerializesModels;
    }

> [!NOTE]  
> 이와 관련된 자세한 사항은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여

비공개 채널은 현재 인증된 유저가 채널을 수신할 수 있는지 권한 인증을 필요로 합니다. 이는 채널명과 함께 애플리케이션으로 HTTP 요청을 보내고, 인증/권한을 판단하여 승낙/거부하는 방식입니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 비공개 채널 구독시 자동으로 이 요청이 발생하므로 별도로 HTTP 요청을 직접 보낼 필요는 없습니다. 하지만 올바른 라우트를 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 권한 부여 라우트 정의

Laravel은 채널 인증 요청에 대응하는 라우트를 쉽게 정의할 수 있도록 지원합니다. 애플리케이션의 `App\Providers\BroadcastServiceProvider`에서 `Broadcast::routes()`를 호출하면, `/broadcasting/auth` 엔드포인트가 자동으로 등록됩니다:

    Broadcast::routes();

이 메서드는 기본적으로 자신의 라우트를 `web` 미들웨어 그룹에 등록하지만, 라우트 속성 배열을 전달해 미들웨어 등 특성을 수정할 수 있습니다:

    Broadcast::routes($attributes);

<a name="customizing-the-authorization-endpoint"></a>
#### 인증 엔드포인트 커스터마이징

Echo는 기본적으로 `/broadcasting/auth` 엔드포인트로 인증 요청을 보냅니다. 지정한 엔드포인트를 사용하려면, Echo 설정에 `authEndpoint` 옵션을 추가하세요:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 인증 요청 커스터마이징

Echo를 초기화할 때 커스텀 authorizer를 지정해 인증 요청 방식도 바꿀 수 있습니다:

```js
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
                    callback(null, response.data);
                })
                .catch(error => {
                    callback(error);
                });
            }
        };
    },
})
```

<a name="defining-authorization-callbacks"></a>
### 권한 부여 콜백 정의

이제 현재 인증된 사용자가 특정 채널을 수신할 수 있는지 실제 판별 로직만 작성하면 됩니다. 이 부분은 기본 제공되는 `routes/channels.php` 파일에서 수행합니다. 이 파일에서 `Broadcast::channel` 함수를 사용해 채널 권한 콜백을 등록할 수 있습니다:

    use App\Models\User;

    Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

`channel`은 채널명과, true/false를 반환하는 콜백을 받습니다. 콜백의 첫 번째 인자는 인증된 사용자, 이후에는 와일드카드 파라미터입니다.

등록된 방송 채널 인증 콜백 목록은 `channel:list` 아티즌 명령어로 조회할 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인증 콜백 모델 바인딩

일반 HTTP 라우트처럼, 채널 라우트도 묵시적(implicit)·명시적(explicit) [모델 바인딩](/docs/{{version}}/routing#route-model-binding)이 가능합니다. 주문 숫자 ID 대신, 실제 Order 모델 인스턴스를 받도록 할 수 있습니다:

    use App\Models\Order;
    use App\Models\User;

    Broadcast::channel('orders.{order}', function (User $user, Order $order) {
        return $user->id === $order->user_id;
    });

> [!WARNING]  
> HTTP route model binding에서 지원하는 [묵시적 모델 바인딩 범위(scoping)](/docs/{{version}}/routing#implicit-model-binding-scoping)가 채널 라우트에선 작동하지 않습니다. 하지만 보통 각 채널은 단일 모델의 주요 키로 범위가 한정되기에 큰 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 인증 콜백에서의 인증

비공개 및 presence 방송 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않은 경우, 권한 콜백은 실행되지 않고 자동 거부됩니다. 필요하다면 여러 개의 커스텀 가드를 인증 과정에 추가할 수도 있습니다:

    Broadcast::channel('channel', function () {
        // ...
    }, ['guards' => ['web', 'admin']]);

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션에서 채널이 많아진다면 `routes/channels.php`가 복잡해질 수 있습니다. 익명 클로저 대신 채널 클래스를 사용하면 더 구조적으로 관리할 수 있습니다. `make:channel` 아티즌 명령어로 채널 클래스를 생성하세요. 클래스는 `App/Broadcasting` 디렉터리에 생성됩니다.

```shell
php artisan make:channel OrderChannel
```

`routes/channels.php`에 채널을 등록하세요:

    use App\Broadcasting\OrderChannel;

    Broadcast::channel('orders.{order}', OrderChannel::class);

권한 부여 로직은 채널 클래스의 `join` 메서드에 작성하면 됩니다. 이 메서드는 채널 인증 클로저에 작성하던 로직과 동일하며, 모델 바인딩도 지원됩니다.

    <?php

    namespace App\Broadcasting;

    use App\Models\Order;
    use App\Models\User;

    class OrderChannel
    {
        /**
         * 새 채널 인스턴스를 생성합니다.
         */
        public function __construct()
        {
            // ...
        }

        /**
         * 사용자의 채널 접근 권한을 인증합니다.
         */
        public function join(User $user, Order $order): array|bool
        {
            return $user->id === $order->user_id;
        }
    }

> [!NOTE]  
> Laravel의 다른 클래스들처럼 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)가 자동 주입합니다. 따라서 생성자에 필요한 의존성을 타입힌트로 명시할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 방송

이벤트에 `ShouldBroadcast`를 구현했다면, 이벤트의 dispatch 메서드를 통해 이벤트를 트리거하는 것 만으로 방송이 이루어집니다. 이벤트 디스패처가 `ShouldBroadcast` 인터페이스 여부를 감지해 이벤트를 방송 큐에 제출합니다:

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="only-to-others"></a>
### 다른 사용자에게만 방송하기

방송 이벤트를 사용할 때, 현재 사용자만 제외하고 다른 모든 구독자에게만 방송하고 싶을 때가 있습니다. 이때는 `broadcast` 헬퍼의 `toOthers` 메서드를 쓰세요:

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->toOthers();

이 기능이 필요한 대표적인 예시로, 고객이 태스크 목록을 관리할 때 `/task` 엔드포인트에 요청을 보내고, 응답으로 새로운 태스크를 리스트에 추가한다고 합시다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만 새로운 태스크 생성 이벤트도 방송하고 있다면, JavaScript에서 동일한 태스크가 두 번 추가될 수 있습니다(엔드포인트 응답 + 방송 이벤트). 이럴 때 `toOthers`를 써서 현재 사용자를 제외할 수 있습니다.

> [!WARNING]  
> `toOthers` 메서드를 사용하려면 이벤트 클래스에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 포함되어야 합니다.

<a name="only-to-others-configuration"></a>
#### 구성 방법

Laravel Echo 인스턴스가 초기화되면 고유의 socket ID가 연결에 할당됩니다. JavaScript에서 (예시로) Axios를 사용할 경우, 모든 HTTP 요청의 `X-Socket-ID` 헤더에 이 ID가 자동으로 첨부됩니다. `toOthers` 사용 시, Laravel은 이 헤더를 추출해 동일 ID를 가진 연결에는 방송하지 않도록 합니다.

Axios를 전역으로 쓰지 않는다면, `Echo.socketId()` 메서드로 직접 socket ID 값을 추출해 모든 요청에 `X-Socket-ID` 헤더로 전송해야 합니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 커스터마이징

여러 방송 연결을 사용하며, 특정 이벤트를 기본 방송자 외의 다른 브로드캐스터로 전송하고 싶다면, `via` 메서드를 사용하세요:

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');

또는, 이벤트 생성자 내에서 `broadcastVia` 메서드를 호출해 방송 연결을 지정할 수도 있습니다. 이때는 이벤트 클래스에 `InteractsWithBroadcasting` 트레이트가 포함되어야 합니다:

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

        /**
         * 새로운 이벤트 인스턴스 생성자
         */
        public function __construct()
        {
            $this->broadcastVia('pusher');
        }
    }

<a name="receiving-broadcasts"></a>
## 방송 수신

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo를 설치 및 인스턴스화](#client-side-installation)했다면, 이제 각 채널에 연결하고 이벤트를 수신할 수 있습니다. `channel`로 인스턴스를 가져오고, `listen`을 사용해 특정 이벤트를 구독하세요:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널에 리스닝하려면, `private` 메서드를 사용하세요. 한 채널에서 여러 이벤트를 리스닝하려면 메서드 체인도 가능합니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중단

특정 이벤트만 리스닝 중지하고 싶을 때는 `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널에서 나가고 싶다면, Echo 인스턴스의 `leaveChannel` 메서드를 사용하세요:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널 및 관련된 프라이빗·프레즌스 채널까지 모두 나가려면 `leave` 메서드를 쓰세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예제처럼 이벤트 클래스의 전체 네임스페이스(예: App\Events)를 명시하지 않은 것도 볼 수 있습니다. 이는 Echo가 기본적으로 이벤트가 `App\Events` 네임스페이스에 위치한다고 가정하기 때문입니다. Echo 인스턴스 생성 시, `namespace` 옵션으로 네임스페이스를 바꿀 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

대신, Echo 구독 시 `.이벤트명`처럼 접두사로 점을 붙여 항상 전체 네임스페이스를 지정할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## Presence 채널

Presence 채널은 비공개 채널 보안 위에, "누가 지금 이 채널에 있는지"까지 알 수 있도록 추가 기능을 제공합니다. 덕분에 같은 페이지를 누가 보는지 알림, 채팅방 참여자 목록 등 협업 기능을 간편하게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### Presence 채널 권한 부여

Presence 채널은 기본적으로 비공개 채널이므로, [권한 인증](#authorizing-channels)이 필요합니다. 다만 presence 채널에서는 인증 콜백에서 true 대신 사용자의 정보를 담은 배열을 반환해야 합니다. 이 데이터는 자바스크립트에서 presence 채널의 이벤트 리스너에서 활용됩니다. 인증 실패시에는 false 또는 null을 반환하세요:

    use App\Models\User;

    Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
        if ($user->canJoinRoom($roomId)) {
            return ['id' => $user->id, 'name' => $user->name];
        }
    });

<a name="joining-presence-channels"></a>
### Presence 채널 참여

Presence 채널에 참여하려면 Echo의 `join` 메서드를 사용하세요. 이 메서드는 `PresenceChannel` 구현체를 반환하며, `listen` 외에도 `here`, `joining`, `leaving` 이벤트를 구독할 수 있습니다:

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
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
```

`here` 콜백은 채널 참여 성공시 즉시 실행되며, 현재 채널에 연결된 모든 유저 정보 배열을 받습니다. `joining`은 누가 입장할 때, `leaving`은 퇴장할 때 실행되고, 문제가 생기거나 인증 엔드포인트가 HTTP 200 이외의 응답을 반환하면 `error`가 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### Presence 채널로 방송하기

Presence 채널도 public/private 채널처럼 이벤트를 수신합니다. 예를 들어 채팅방에서는 `NewMessage` 이벤트를 presence 채널로 방송할 수 있습니다. 이벤트의 `broadcastOn` 메서드에서 PresenceChannel을 반환하세요:

    /**
     * 이벤트가 방송될 채널을 반환
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PresenceChannel('chat.'.$this->message->room_id),
        ];
    }

다른 이벤트처럼 `broadcast` 헬퍼와 `toOthers` 메서드로 자기 자신은 제외할 수 있습니다:

    broadcast(new NewMessage($message));

    broadcast(new NewMessage($message))->toOthers();

Presence 채널에 대한 이벤트 리스닝도 Echo의 `listen` 메서드를 쓰면 됩니다:

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```

<a name="model-broadcasting"></a>
## 모델 방송

> [!WARNING]  
> 모델 브로드캐스팅에 대해 읽기 전에, Laravel의 일반적인 모델 방송 서비스와 직접 방송 이벤트를 생성·리스닝하는 방법을 숙지하는 것이 좋습니다.

Eloquent 모델이 생성·수정·삭제될 때 자동으로 이벤트를 방송하는 것이 일반적입니다. 물론, 상황별로 [커스텀 이벤트를 직접 정의](https://laravel.com/docs/{{version}}/eloquent#events)해 `ShouldBroadcast`를 붙일 수도 있습니다.

하지만, 별도 이벤트에 다른 용도가 없을 때, 단순 방송만 위해 이벤트 클래스를 생성하는 것은 번거로울 수 있습니다. 이럴 땐 모델의 자동 방송 기능을 사용할 수 있습니다.

시작을 위해, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하세요. 그리고 모델에 `broadcastOn` 메서드를 정의하면, 해당 모델의 이벤트가 방송될 채널들을 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * 이 게시글의 작성자
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 방송될 채널
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이 트레이트와 `broadcastOn` 메서드를 포함하면, 모델 인스턴스 생성, 수정, 삭제, 트래시 이동, 복원 시 자동으로 방송 이벤트가 발생합니다.

`broadcastOn` 메서드는 `$event` 매개변수로, 해당 모델 이벤트의 트리거 타입(`created`, `updated`, `deleted`, `trashed`, `restored`) 값을 받습니다. 이를 검사해서, 상황에 따라 방송 채널을 다르게 반환할 수 있습니다:

```php
/**
 * 모델 이벤트가 방송될 채널
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>
#### 모델 방송 이벤트 생성 커스터마이징

드물게, 모델의 방송 이벤트 인스턴스 생성 로직을 직접 제어하고 싶다면, `newBroadcastableEvent` 메서드를 모델에 추가하세요. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델의 새로운 방송 이벤트를 생성합니다.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### 모델 방송 규칙

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 명명 규칙

위의 예시에서는 `broadcastOn`이 Channel 인스턴스 대신 그냥 Eloquent 모델을 반환했습니다. 모델 인스턴스를 반환하는 경우, Laravel은 클래스명과 주키(primary key)를 조합해 자동으로 PrivateChannel 인스턴스를 생성합니다.

즉, `App\Models\User` 모델의 id가 1이라면, 채널명은 `App.Models.User.1`이 됩니다. 물론 직접 Channel 인스턴스를 반환하여 더 세밀하게 채널명을 지정할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 방송될 채널을 반환합니다.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```

모델을 Channel의 생성자에 직접 넘길 수도 있습니다:

```php
return [new Channel($this->user)];
```

모델의 채널명을 구해야 할 때는, 모델 인스턴스에서 `broadcastChannel()`을 호출하면 됩니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 명명 규칙

모델 브로드캐스트 이벤트는 `App\Events` 디렉터리의 '실제' 이벤트에 속하지 않기 때문에, 이름과 페이로드가 규칙에 따라 결정됩니다. 클래스명(네임스페이스 제외)과 모델 이벤트 종류로 이름이 정해지며, 예시로 `App\Models\Post`가 수정되면 브로드캐스트 이름은 `PostUpdated`가 됩니다:

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId",
}
```

`App\Models\User` 모델이 삭제되면, 이벤트명은 `UserDeleted`가 됩니다.

필요하다면 `broadcastAs`와 `broadcastWith` 메서드를 모델에 정의하여, 이벤트명과 페이로드를 직접 지정할 수 있습니다. 두 메서드는 각각 모델 이벤트 종류/연산명을 인자로 받습니다. `broadcastAs`가 null을 반환하면 기본 네이밍 규칙을 따릅니다:

```php
/**
 * 모델 이벤트 방송명 반환
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델 이벤트 방송 페이로드 반환
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
### 모델 방송 리스닝

모델에 `BroadcastsEvents` 트레이트와 `broadcastOn`을 추가했다면, 클라이언트에서 모델 방송을 곧장 수신할 수 있습니다. 시작 전, [이벤트 리스닝](#listening-for-events) 문서를 참고하세요.

채널 이름은 [모델 방송 규칙](#model-broadcasting-conventions)에 따라 결정되므로, `private`로 채널에 연결한 뒤, `listen`을 사용해 특정 이벤트명을(점 접두사) 명시해서 수신합니다. 모델 브로드캐스트 이벤트는 페이로드 내 `model` 프로퍼티에 시리얼라이즈된 모델 데이터가 포함됩니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]  
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, 앱 대시보드의 "App Settings"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

가끔은 Laravel 서버로 요청을 보내지 않고, 연결된 다른 클라이언트에게만 간단하게 이벤트를 방송하고 싶을 수 있습니다. 대표적인 경우가 타이핑 알림, 즉 누군가 글자를 입력 중임을 알려주는 상황입니다.

클라이언트 이벤트 방송에는 Echo의 `whisper` 메서드를 사용합니다:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트 수신은 `listenForWhisper` 메서드로 가능합니다:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림(Notifications)

이벤트 방송과 [알림](https://laravel.com/docs/{{version}}/notifications)을 결합하면, 사용자는 페이지를 새로 고침하지 않고도 실시간으로 새 알림을 받을 수 있습니다. 먼저 [방송 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 문서를 읽어보세요.

알림에 방송 채널을 설정했다면, Echo의 `notification` 메서드로 알림 방송 이벤트를 수신할 수 있습니다. 채널명은 알림을 수신하는 엔터티의 클래스명을 따라야 합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

이 예제에서는 `broadcast` 채널을 통해 `App\Models\User` 인스턴스에 전달된 모든 알림이 콜백으로 수신됩니다. `App.Models.User.{id}` 채널에 대한 권한 콜백도 기본 `BroadcastServiceProvider`에 포함되어 있습니다.