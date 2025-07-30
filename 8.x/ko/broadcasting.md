# 방송 (Broadcasting)

- [소개](#introduction)
- [서버 사이드 설치](#server-side-installation)
    - [설정](#configuration)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [오픈 소스 대안](#open-source-alternatives)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여](#authorizing-channels)
    - [권한 부여 라우트 정의](#defining-authorization-routes)
    - [권한 부여 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스트하기](#broadcasting-events)
    - [나를 제외한 다른 사용자에게만](#only-to-others)
    - [연결 사용자 지정하기](#customizing-the-connection)
- [브로드캐스트 수신하기](#receiving-broadcasts)
    - [이벤트 청취하기](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스(존재) 채널](#presence-channels)
    - [프레즌스 채널 권한 부여하기](#authorizing-presence-channels)
    - [프레즌스 채널 참여하기](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅하기](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 청취하기](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대적인 웹 애플리케이션에서는 보통 WebSocket을 사용하여 실시간, 라이브 업데이트되는 사용자 인터페이스를 구현합니다. 서버에서 데이터가 업데이트되면 일반적으로 WebSocket 연결을 통해 메시지가 클라이언트로 전송되어 처리됩니다. WebSocket은 UI에 반영되어야 할 데이터 변경 상태를 지속적으로 서버에 폴링하는 것보다 훨씬 효율적인 대안입니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내 이메일로 전송하는 기능이 있다고 가정해봅니다. CSV 파일 생성에 몇 분 정도 소요되기에, 이 작업을 [큐에 등록된 작업](/docs/{{version}}/queues) 내에서 생성하고 전송하도록 설계할 수 있습니다. 그리고 CSV 파일이 만들어지고 이메일로 발송되면, `App\Events\UserDataExported` 이벤트를 브로드캐스팅하여 애플리케이션의 자바스크립트에서 해당 이벤트를 수신할 수 있습니다. 이벤트를 수신하면 페이지를 새로 고침하지 않아도 사용자에게 이메일 전송 완료 메시지를 보여줄 수 있습니다.

이러한 기능을 쉽게 구현할 수 있도록 Laravel은 서버 측의 Laravel [이벤트](/docs/{{version}}/events)를 WebSocket 연결을 통해 "브로드캐스트" 할 수 있게 지원합니다. Laravel 이벤트를 브로드캐스트하면 서버 측 Laravel 애플리케이션과 클라이언트 측 자바스크립트 애플리케이션 간에 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스트의 핵심 개념은 단순합니다: 클라이언트는 프론트엔드에서 이름이 지정된 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 이러한 채널로 이벤트를 브로드캐스트합니다. 이 이벤트들은 프론트엔드에서 접근 가능하도록 추가적인 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

기본적으로 Laravel은 서버 측 브로드캐스트 드라이버로 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.io)를 제공합니다. 그러나 커뮤니티에서 만들어진 [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction), [soketi](https://docs.soketi.app/) 등의 패키지를 통해 상업용 브로드캐스팅 제공자가 없어도 작동하는 추가 드라이버를 사용할 수 있습니다.

> [!TIP]
> 이벤트 브로드캐스팅을 시작하기 전, Laravel의 [이벤트 및 리스너](/docs/{{version}}/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치 (Server Side Installation)

Laravel 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션 내에서 설정을 진행하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스트 드라이버가 담당하며, 이 드라이버는 Laravel 이벤트를 브로드캐스트하여 브라우저 클라이언트 내에서 Laravel Echo (자바스크립트 라이브러리)가 이를 수신할 수 있게 합니다. 걱정하지 마세요. 설치 과정을 단계별로 자세히 안내해 드립니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션 내 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 구성 파일에 저장됩니다. Laravel은 기본적으로 [Pusher Channels](https://pusher.com/channels), [Redis](/docs/{{version}}/redis), 개발 및 디버깅용 `log` 드라이버를 지원합니다. 또한 테스트 시 브로드캐스팅을 완전히 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버 예제 구성이 `config/broadcasting.php` 파일에 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### Broadcast 서비스 프로바이더

이벤트 브로드캐스트를 시작하기 전, `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 새 Laravel 애플리케이션에서는 `config/app.php` 구성 파일의 `providers` 배열에서 해당 프로바이더의 주석을 해제하기만 하면 됩니다. `BroadcastServiceProvider`는 브로드캐스트 권한 부여 라우트와 콜백을 등록하는 데 필요한 코드를 포함하고 있습니다.

<a name="queue-configuration"></a>
#### 큐 설정

또한 [큐 작업자](/docs/{{version}}/queues)를 구성하고 실행해야 합니다. 모든 이벤트 브로드캐스팅 작업은 큐 작업으로 처리되어 애플리케이션의 응답 속도가 브로드캐스트 이벤트 처리로 인해 심각하게 영향을 받지 않도록 합니다.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 사용해 이벤트를 브로드캐스트하려면, Composer를 사용해 Pusher Channels PHP SDK를 설치해야 합니다:

```
composer require pusher/pusher-php-server
```

그 다음, Pusher Channels 자격 증명을 `config/broadcasting.php`에 설정합니다. 이 파일에 이미 예제가 포함되어 있어 키, 시크릿, 애플리케이션 ID를 빠르게 지정할 수 있습니다. 일반적으로 이 값들은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 설정합니다:

```
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

`config/broadcasting.php`의 `pusher` 설정에서 클러스터와 같은 추가 `options`도 지정할 수 있습니다.

이제 `.env` 파일에서 브로드캐스트 드라이버를 `pusher`로 변경합니다:

```
BROADCAST_DRIVER=pusher
```

마지막으로 [Laravel Echo](#client-side-installation)를 설치하고 설정하여 클라이언트 측에서 브로드캐스트 이벤트를 수신할 준비를 합니다.

<a name="pusher-compatible-open-source-alternatives"></a>
#### 오픈 소스 Pusher 대안

[laravel-websockets](https://github.com/beyondcode/laravel-websockets), [soketi](https://docs.soketi.app/) 등 패키지는 Laravel용 Pusher 호환 WebSocket 서버를 제공합니다. 이 패키지들을 사용하면 상업용 WebSocket 제공자 없이도 Laravel 브로드캐스팅의 모든 기능을 활용할 수 있습니다. 자세한 설치 및 사용법은 [오픈 소스 대안](#open-source-alternatives) 문서를 참고하세요.

<a name="ably"></a>
### Ably

[Ably](https://ably.io)를 사용해 이벤트를 브로드캐스트하려면, Composer를 사용해 Ably PHP SDK를 설치해야 합니다:

```
composer require ably/ably-php
```

그 다음, Ably 자격 증명을 `config/broadcasting.php`에 설정합니다. 이 파일에 키를 간단히 지정할 수 있는 예제가 포함되어 있습니다. 키는 일반적으로 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 설정합니다:

```
ABLY_KEY=your-ably-key
```

이제 `.env` 파일에서 브로드캐스트 드라이버를 `ably`로 변경합니다:

```
BROADCAST_DRIVER=ably
```

마지막으로 [Laravel Echo](#client-side-installation)를 설치하고 설정하여 클라이언트 측에서 브로드캐스트 이벤트를 수신할 준비를 합니다.

<a name="open-source-alternatives"></a>
### 오픈 소스 대안 (Open Source Alternatives)

<a name="open-source-alternatives-php"></a>
#### PHP

[laravel-websockets](https://github.com/beyondcode/laravel-websockets) 패키지는 순수 PHP 기반의 Pusher 호환 WebSocket 패키지로, 상업용 WebSocket 제공자 없이 Laravel 브로드캐스팅을 이용할 수 있습니다. 자세한 설치 및 사용법은 [공식 문서](https://beyondco.de/docs/laravel-websockets)를 참고하십시오.

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반의 Pusher 호환 WebSocket 서버입니다. 내부적으로 µWebSockets.js를 사용해 성능과 확장성을 극대화합니다. 상업용 WebSocket 제공자 없이 Laravel 브로드캐스팅을 사용할 수 있습니다. 자세한 사항은 [공식 문서](https://docs.soketi.app/)를 참조하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치 (Client Side Installation)

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버 측 브로드캐스트 드라이버가 전송하는 이벤트 청취를 쉽게 하는 자바스크립트 라이브러리입니다. NPM을 사용해 Echo를 설치할 수 있습니다. 이 예제에서는 Pusher Channels 브로드캐스터를 사용하므로 `pusher-js` 패키지도 같이 설치합니다:

```bash
npm install --save-dev laravel-echo pusher-js
```

Echo를 설치하면 애플리케이션 자바스크립트에 새 Echo 인스턴스를 생성할 준비가 됩니다. Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단이 좋은 위치입니다. 기본적으로 이 파일에 Echo 사용 예제가 포함되어 있으므로 주석을 해제하면 됩니다:

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

필요에 맞게 Echo 설정을 조정한 뒤, 애플리케이션 자산을 컴파일합니다:

```
npm run dev
```

> [!TIP]
> 자바스크립트 자산 컴파일에 대해 더 알고 싶다면 [Laravel Mix](/docs/{{version}}/mix) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 Pusher Channels 클라이언트 인스턴스가 있다면, Echo 인스턴스 생성 시 `client` 옵션으로 전달할 수 있습니다:

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

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스트 드라이버가 송신한 이벤트를 손쉽게 구독할 수 있게 도와줍니다. NPM을 사용해 Echo를 설치할 수 있으며, 이 예제에서는 `pusher-js` 패키지도 같이 설치합니다.

왜 Ably를 사용하면서도 `pusher-js`를 설치하느냐고 의아해 할 수 있습니다. 다행히도 Ably는 Pusher 호환 모드를 포함하고 있어, 클라이언트 측에서 Pusher 프로토콜을 사용하여 이벤트를 수신할 수 있습니다:

```bash
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화하세요. 이 기능은 Ably 대시보드의 "Protocol Adapter Settings"에서 켤 수 있습니다.**

Echo가 설치되면, 애플리케이션 자바스크립트에 새 Echo 인스턴스를 생성할 준비가 됩니다. Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단이 좋은 위치입니다. 기본 설정 예제는 Pusher용이므로, 다음 예제로 복사하여 Ably로 전환할 수 있습니다:

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

Ably Echo 설정에서 참조하는 `MIX_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키여야 합니다. 공개 키는 Ably 키에서 `:` 문자 앞 부분입니다.

필요에 따라 Echo 설정을 조정하고, 애플리케이션 자산을 컴파일하세요:

```
npm run dev
```

> [!TIP]
> 자바스크립트 자산 컴파일에 대해 더 알고 싶다면 [Laravel Mix](/docs/{{version}}/mix) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel 이벤트 브로드캐스팅은 WebSocket 연결에 대한 드라이버 기반 접근 방식을 통해 서버 측 Laravel 이벤트를 클라이언트 측 자바스크립트 애플리케이션으로 브로드캐스트할 수 있습니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.io) 드라이버를 기본 제공합니다. 이벤트들은 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 통해 클라이언트에서 쉽게 구독할 수 있습니다.

이벤트는 "채널" 위에서 브로드캐스트되며, 채널은 public (공개) 또는 private (비공개)으로 지정할 수 있습니다. 공개 채널은 누구나 인증이나 권한 없이 구독할 수 있지만, 비공개 채널은 해당 채널에 대해 인증되고 권한이 부여된 사용자만 구독할 수 있습니다.

> [!TIP]
> Pusher의 오픈 소스 대안을 탐색하고 싶다면 [오픈 소스 대안](#open-source-alternatives)을 확인하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용 (Using An Example Application)

브로드캐스트 각 구성 요소를 살펴보기 전에, 전자상거래 매장 예제를 통해 큰 그림을 이해해봅니다.

애플리케이션에서 사용자가 주문의 배송 상태를 확인할 수 있는 페이지가 있다고 가정합니다. 그리고 주문 배송 상태가 업데이트될 때 `OrderShipmentStatusUpdated` 이벤트가 발생한다고 가정합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문을 보는 동안 페이지를 새로고침하지 않고 배송 상태를 실시간으로 업데이트 받도록 구현하고 싶습니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해 Laravel이 이벤트 발생 시 브로드캐스트하도록 지시합니다:

```
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
     * 주문 인스턴스.
     *
     * @var \App\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트할 채널을 반환합니다. 기본 생성된 이벤트 클래스에 빈 형태로 포함되어 있으니 내용을 채우기만 하면 됩니다. 주문 생성자만 배송 상태 업데이트를 볼 수 있도록 해당 주문에 연결된 비공개 채널에서 이벤트를 브로드캐스트합니다:

```
/**
 * 이벤트가 브로드캐스트할 채널을 반환합니다.
 *
 * @return \Illuminate\Broadcasting\PrivateChannel
 */
public function broadcastOn()
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

<a name="example-application-authorizing-channels"></a>
#### 채널 권한 부여

비공개 채널은 사용자가 청취하도록 권한이 있어야 함을 기억하세요. 애플리케이션의 `routes/channels.php` 파일에서 채널 권한 부여 규칙을 정의할 수 있습니다. 예를 들어, 비공개 `orders.1` 채널에 접속하려는 사용자가 실제 주문 생성자인지 확인하는 예제는 다음과 같습니다:

```
use App\Models\Order;

Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 인수를 받습니다: 채널 이름과 사용자가 청취 권한이 있는지 `true` 또는 `false`를 반환하는 콜백.

모든 권한 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고, 추가 와일드카드 매개변수는 이후 인수로 받습니다. 위 예제는 `{orderId}` 자리 표시에 ID가 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>
#### 브로드캐스트 이벤트 청취하기

이제 자바스크립트 애플리케이션에서 이벤트를 청취할 차례입니다. [Laravel Echo](#client-side-installation)를 사용합니다. `private` 메서드로 비공개 채널에 구독한 뒤 `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 청취합니다. 기본적으로 이벤트의 모든 public 속성이 브로드캐스트 페이로드에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의하기 (Defining Broadcast Events)

Laravel에게 특정 이벤트를 브로드캐스트 해야 한다고 알리려면, 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 이미 임포트되어 있어 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 한 개를 구현하도록 요구하며, 이 메서드는 이벤트가 브로드캐스트할 채널 또는 채널 배열을 반환해야 합니다. 채널은 `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스여야 하며, `Channel`은 모든 사용자가 구독할 수 있는 공개 채널을, `PrivateChannel`과 `PresenceChannel`은 권한 부여가 필요한 비공개 채널을 나타냅니다:

```
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
     * 서버를 생성한 사용자.
     *
     * @var \App\Models\User
     */
    public $user;

    /**
     * 새 이벤트 인스턴스 생성.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * 이벤트가 브로드캐스트할 채널 반환.
     *
     * @return Channel|array
     */
    public function broadcastOn()
    {
        return new PrivateChannel('user.'.$this->user->id);
    }
}
```

`ShouldBroadcast` 구현 후에는 평소처럼 [이벤트를 실행](/docs/{{version}}/events)하기만 하면 됩니다. 이벤트가 발생하면 [큐에 등록된 작업](/docs/{{version}}/queues)이 자동으로 해당 이벤트를 지정한 브로드캐스트 드라이버를 통해 방송합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름 (Broadcast Name)

기본적으로 Laravel은 이벤트의 클래스 이름을 브로드캐스트 이벤트 이름으로 사용합니다. 그러나 `broadcastAs` 메서드를 정의하여 브로드캐스트 이름을 사용자 정의할 수 있습니다:

```
/**
 * 이벤트의 브로드캐스트 이름.
 *
 * @return string
 */
public function broadcastAs()
{
    return 'server.created';
}
```

`broadcastAs`로 이름을 변경하면, 리스너 등록 시에도 이벤트 이름 앞에 점(`.`)을 붙여 등록해야 합니다. 이렇게 하면 Echo가 애플리케이션 네임스페이스를 이벤트에 자동으로 덧붙이지 않습니다:

```
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터 (Broadcast Data)

이벤트가 브로드캐스트될 때, 모든 `public` 속성이 자동으로 직렬화되어 이벤트 페이로드로 방송됩니다. 자바스크립트 애플리케이션에서 이런 공개 데이터에 접근할 수 있습니다. 예를 들어, 이벤트가 Eloquent 모델을 포함하는 `$user` 단일 public 속성을 가질 때 페이로드는 다음과 같이 됩니다:

```
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

페이로드를 더 정밀하게 제어하고 싶다면, 이벤트에 `broadcastWith` 메서드를 추가할 수 있습니다. 이 메서드는 브로드캐스트할 데이터 배열을 반환해야 합니다:

```
/**
 * 브로드캐스트할 데이터 반환.
 *
 * @return array
 */
public function broadcastWith()
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
### 브로드캐스트 큐 (Broadcast Queue)

기본적으로 각 브로드캐스트 이벤트는 `queue.php` 설정 파일의 기본 큐 연결과 큐 이름에 따라 큐에 등록됩니다. 이벤트 클래스에 `connection`과 `queue` 속성을 정의하여 큐 연결과 큐 이름을 지정할 수 있습니다:

```
/**
 * 브로드캐스트 이벤트 큐 연결 이름.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스트 작업을 배치할 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드를 정의해 큐 이름을 반환할 수도 있습니다:

```
/**
 * 브로드캐스트 작업을 배치할 큐 이름 반환.
 *
 * @return string
 */
public function broadcastQueue()
{
    return 'default';
}
```

기본 큐 드라이버 대신 동기(`sync`) 큐를 사용해 즉시 브로드캐스트하려면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요:

```
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    //
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건 (Broadcast Conditions)

때로는 특정 조건이 참일 때만 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 조건을 정의할 수 있습니다:

```
/**
 * 이벤트를 브로드캐스트할지 결정.
 *
 * @return bool
 */
public function broadcastWhen()
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션 (Broadcasting & Database Transactions)

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내에서 발생하면, 큐에 등록된 작업이 트랜잭션 커밋 전에 처리될 수 있습니다. 이 경우 트랜잭션 내에서 수정한 모델이나 데이터가 데이터베이스에 아직 반영되지 않았거나, 트랜잭션 내에서 생성한 모델이 존재하지 않을 수 있어, 이벤트가 의존하는 데이터가 불완전할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`일 경우, 이벤트 클래스에 `$afterCommit` 속성을 정의해 해당 브로드캐스트 이벤트가 모든 열린 데이터베이스 트랜잭션이 커밋된 뒤에 디스패치 되도록 할 수 있습니다:

```
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    public $afterCommit = true;
}
```

> [!TIP]
> 이 이슈에 대해 더 알아보려면 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여 (Authorizing Channels)

비공개 채널은 현재 인증된 사용자가 해당 채널의 청취 권한이 있는지 확인해야 합니다. 이것은 Laravel 애플리케이션에 채널 이름을 포함한 HTTP 요청을 보내, 사용자가 해당 채널에 청취할 수 있는지 판단하도록 합니다. [Laravel Echo](#client-side-installation)를 사용하면 이러한 권한 승인 요청은 자동으로 전송되지만, 애플리케이션에서는 이에 응답할 올바른 라우트를 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 권한 부여 라우트 정의 (Defining Authorization Routes)

다행히 Laravel은 채널 권한 승인을 처리할 라우트 정의를 쉽게 해줍니다. Laravel 애플리케이션에 포함된 `App\Providers\BroadcastServiceProvider` 내에는 `Broadcast::routes` 호출이 있습니다. 이 메서드는 권한 요청을 처리할 `/broadcasting/auth` 라우트를 등록합니다:

```
Broadcast::routes();
```

`Broadcast::routes`는 기본적으로 `web` 미들웨어 그룹에 라우트를 포함하지만, 라우트 속성 배열을 인수로 넘겨 속성을 커스터마이징할 수도 있습니다:

```
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>
#### 권한 부여 엔드포인트 커스터마이징

기본적으로 Echo는 채널 접근 권한 승인을 위해 `/broadcasting/auth` 엔드포인트를 사용합니다. 하지만 Echo 인스턴스 생성 시 `authEndpoint` 설정으로 별도의 권한 승인 엔드포인트를 지정할 수 있습니다:

```
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 권한 부여 요청 커스터마이징

Echo가 권한 승인 요청을 수행하는 방식을 변경하고 싶으면, 초기화 시 커스텀 authorizer를 직접 정의할 수 있습니다:

```
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
```

<a name="defining-authorization-callbacks"></a>
### 권한 부여 콜백 정의 (Defining Authorization Callbacks)

이제 실제로 현재 인증된 사용자가 특정 채널을 청취할 수 있는지 결정하는 로직을 정의해야 합니다. 이 작업은 애플리케이션의 `routes/channels.php` 파일에서 수행하며, `Broadcast::channel` 메서드를 사용해 채널 권한 승인 콜백을 등록합니다:

```
Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과, 사용자의 권한 여부를 `true` 또는 `false`로 반환하는 콜백 두 인수를 받습니다.

모든 권한 콜백은 현재 인증 사용자 인스턴스를 첫 번째 인수로 받고, 추가 와일드카드 파라미터는 이후 인수로 받습니다. 위 예제는 `{orderId}`가 와일드카드임을 나타냅니다.

<a name="authorization-callback-model-binding"></a>
#### 권한 부여 콜백 모델 바인딩

HTTP 라우트처럼, 채널 라우트도 명시적 또는 암묵적 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용할 수 있습니다. 즉, 문자열 ID 대신 실제 `Order` 모델 인스턴스를 받을 수 있습니다:

```
use App\Models\Order;

Broadcast::channel('orders.{order}', function ($user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!NOTE]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [암묵적 모델 바인딩 스코핑](/docs/{{version}}/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 하지만 채널 대부분은 단일 모델의 고유 주 키를 기준으로 스코프를 지정하기 때문에 일반적으로 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 권한 부여 콜백 인증

비공개 및 프레즌스 브로드캐스트 채널은 기본 인증 가드로 현재 사용자를 인증합니다. 인증되지 않은 사용자는 자동으로 채널 권한 승인이 거부되며 권한 부여 콜백이 실행되지 않습니다. 필요한 경우 여러 개의 커스텀 가드를 지정할 수도 있습니다:

```
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의 (Defining Channel Classes)

만약 애플리케이션이 많은 채널을 사용한다면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 권한 부여를 클로저 대신 채널 클래스를 사용해 처리할 수 있습니다. `make:channel` Artisan 명령어로 채널 클래스를 생성하세요. 이 클래스는 `App/Broadcasting` 디렉토리에 생성됩니다:

```
php artisan make:channel OrderChannel
```

이후, `routes/channels.php`에서 채널을 등록합니다:

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스의 `join` 메서드에 권한 부여 로직을 작성합니다. `join` 메서드는 기존에 클로저에서 처리하던 로직을 담당하며, 모델 바인딩도 활용할 수 있습니다:

```
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * 새 채널 인스턴스 생성.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * 사용자의 채널 접근 권한 인증.
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
```

> [!TIP]
> Laravel의 다른 클래스들처럼 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 인스턴스화됩니다. 생성자에서 필요한 의존성을 타입힌팅 할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스트하기 (Broadcasting Events)

이벤트를 정의하고 `ShouldBroadcast` 인터페이스로 표시한 후에는 이벤트 `dispatch` 메서드를 호출해 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 `ShouldBroadcast`가 구현된 이벤트임을 감지하고 해당 이벤트를 브로드캐스트할 큐 작업으로 등록합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 나를 제외한 다른 사용자에게만 (Only To Others)

가끔 같은 채널 구독자 중 현재 사용자 자신을 제외한 나머지 사용자들에게만 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이 경우 `broadcast` 헬퍼와 `toOthers` 메서드를 함께 사용합니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어 할 일 목록 애플리케이션에서 사용자가 새 태스크를 생성하는 경우를 상상해봅시다. `/task` 엔드포인트에 요청해 태스크를 생성하고 JSON 응답을 받아 태스크 목록에 직접 추가합니다:

```
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

동시에, 태스크 생성 이벤트를 브로드캐스트하기 때문에 자바스크립트 애플리케이션이 해당 이벤트 청취 중이면 할 일 목록에 중복된 태스크가 표시됩니다. 이 문제를 해결하려면 `toOthers`를 사용해 브로드캐스터가 현재 사용자에게 이벤트를 보내지 않도록 지시합니다.

> [!NOTE]
> `toOthers` 메서드를 사용하려면, 이벤트 클래스가 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 구성

Echo 인스턴스를 생성하면 소켓 ID가 연결에 할당됩니다. 자바스크립트 애플리케이션에서 전역 [Axios](https://github.com/mzabriskie/axios)를 사용하면 이 소켓 ID가 모든 HTTP 요청 헤더의 `X-Socket-ID`로 자동 첨부됩니다. 이렇게 하면 `toOthers` 메서드를 호출할 때 Laravel이 헤더에서 소켓 ID를 추출해 해당 소켓 ID가 할당된 연결 대상으로는 브로드캐스트하지 않습니다.

전역 Axios 인스턴스를 사용하지 않는다면, 자바스크립트 쪽에서 수동으로 모든 요청에 `X-Socket-ID` 헤더를 추가해야 합니다. 소켓 ID는 `Echo.socketId()` 메서드로 얻을 수 있습니다:

```
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 사용자 지정하기 (Customizing The Connection)

애플리케이션이 여러 브로드캐스트 연결을 다룰 때, 기본 브로드캐스트 드라이버가 아닌 다른 드라이버로 이벤트를 방송하려면 `via` 메서드에서 연결을 지정할 수 있습니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는, 이벤트 클래스가 `InteractsWithBroadcasting` 트레이트를 사용한다면, 이벤트 생성자 내에서 `broadcastVia` 메서드를 호출해 브로드캐스트 연결을 지정할 수 있습니다:

```
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
     * 새 이벤트 인스턴스 생성.
     *
     * @return void
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신하기 (Receiving Broadcasts)

<a name="listening-for-events"></a>
### 이벤트 청취하기 (Listening For Events)

[Laravel Echo 설치 및 인스턴스 생성](#client-side-installation) 후, Laravel에서 방송한 이벤트를 청취할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻은 뒤 `listen` 메서드로 원하는 이벤트를 청취하세요:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널을 청취할 땐 `private` 메서드를 대신 사용하면 됩니다. 단일 채널에서 여러 이벤트를 청취할 때는 `listen`을 연속으로 호출할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(...)
    .listen(...)
    .listen(...);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 청취 중지하기

채널을 떠나지 않고 특정 이벤트 청취만 중단하려면 `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 떠나기 (Leaving A Channel)

채널을 완전히 떠나려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

비공개 및 프레즌스 채널까지 모두 떠나려면 `leave` 메서드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스 (Namespaces)

위 예제들에서 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않은 이유는 Echo가 기본적으로 `App\Events` 네임스페이스를 가정하기 때문입니다. Echo 인스턴스 생성 시 `namespace` 설정 옵션으로 기본 네임스페이스를 변경할 수도 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 이벤트 구독 시 이벤트 이름 앞에 `.`를 붙여 완전한 클래스 이름을 지정할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        //
    });
```

<a name="presence-channels"></a>
## 프레즌스(존재) 채널 (Presence Channels)

프레즌스 채널은 비공개 채널의 보안을 기반으로 하면서 누가 해당 채널에 참가해 있는지 알 수 있는 추가 기능을 제공합니다. 이를 통해 같은 페이지를 보고 있는 사용자 알림이나 채팅방 인원 목록 같은 협업 기능을 쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 권한 부여하기 (Authorizing Presence Channels)

프레즌스 채널은 비공개 채널이므로 [권한 부여](#authorizing-channels)가 필요합니다. 그러나 프레즌스 채널 권한 콜백에서 사용자가 채널에 참여할 수 있으면 `true` 대신 사용자 정보를 담은 배열을 반환해야 합니다.

콜백에서 반환된 데이터는 자바스크립트 프레즌스 채널 리스너에서 사용됩니다. 접근 권한이 없으면 `false` 또는 `null`을 반환합니다:

```
Broadcast::channel('chat.{roomId}', function ($user, $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여하기 (Joining Presence Channels)

프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용하세요. `join`은 `PresenceChannel` 인스턴스를 반환하며, `listen` 메서드는 물론 `here`, `joining`, `leaving` 이벤트 구독도 지원합니다:

```
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
```

- `here` 콜백은 채널 참여 성공 시 즉시 실행되며, 현재 해당 채널에 구독 중인 모든 사용자 정보를 배열로 받습니다.
- `joining`은 새 사용자가 채널에 입장할 때 실행됩니다.
- `leaving`은 사용자가 채널을 떠날 때 실행됩니다.
- `error`는 권한 승인 엔드포인트가 200 이외 응답을 하거나 반환된 JSON 파싱 문제 발생 시 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅하기 (Broadcasting To Presence Channels)

프레즌스 채널도 공개 및 비공개 채널처럼 이벤트를 수신할 수 있습니다. 채팅방 예제로 `NewMessage` 이벤트를 방 프레즌스 채널로 브로드캐스트하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환합니다:

```
/**
 * 이벤트가 브로드캐스트할 채널 반환.
 *
 * @return Channel|array
 */
public function broadcastOn()
{
    return new PresenceChannel('room.'.$this->message->room_id);
}
```

다른 이벤트들과 마찬가지로, `broadcast` 헬퍼와 `toOthers` 메서드를 써서 현재 사용자를 제외할 수 있습니다:

```
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Echo로 프레즌스 채널에 보낸 이벤트를 청취하려면 `listen`를 사용하세요:

```
Echo.join(`chat.${roomId}`)
    .here(...)
    .joining(...)
    .leaving(...)
    .listen('NewMessage', (e) => {
        //
    });
```

<a name="model-broadcasting"></a>
## 모델 브로드캐스팅 (Model Broadcasting)

> [!NOTE]
> 다음 모델 브로드캐스팅 문서를 읽기 전, Laravel 모델 방송 서비스 및 브로드캐스트 이벤트를 수동 생성해 청취하는 일반 개념에 익숙해지는 것을 권장합니다.

보통 애플리케이션에서 [Eloquent 모델](/docs/{{version}}/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트합니다. 물론, 직접 [Eloquent 모델 상태 변경용 커스텀 이벤트](/docs/{{version}}/eloquent#events)를 정의하고 `ShouldBroadcast`를 구현해 쉽게 할 수 있습니다.

하지만 이 이벤트들을 브로드캐스트 목적 외에는 사용하지 않는다면, 단지 브로드캐스트 때문에 이벤트 클래스를 생성하는 건 번거로울 수 있습니다. 이를 해결하기 위해 Laravel은 Eloquent 모델 스스로 상태 변경 시 자동으로 이벤트를 브로드캐스트하도록 지정할 수 있게 합니다.

먼저, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용합니다. 또한 모델에 `broadcastsOn` 메서드를 정의해 모델 이벤트가 브로드캐스트할 채널 배열을 반환해야 합니다:

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
     * 게시글 작성자 관계 정의.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트할 채널 반환.
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

트레이트 추가와 브로드캐스트 채널 정의 후, 모델 생성, 수정, 삭제, 휴지통 처분, 복원 시 자동으로 이벤트가 브로드캐스트됩니다.

`broadcastOn` 메서드는 발생한 이벤트 종류를 나타내는 `$event` 문자열 인수를 받습니다. 값은 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이를 통해 어떤 이벤트에서 어떤 채널에 방송할지 결정할 수 있습니다:

```php
/**
 * 모델 이벤트가 브로드캐스트할 채널 반환.
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
#### 모델 브로드캐스팅 이벤트 생성 커스터마이징

가끔 Laravel이 만드는 기본 모델 브로드캐스팅 이벤트 생성 방식을 수정하고 싶을 수 있습니다. 이 경우 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의하세요. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred

/**
 * 모델용 새 브로드캐스트 이벤트 생성.
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
### 모델 브로드캐스팅 규칙 (Model Broadcasting Conventions)

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 규칙

위 모델 예제 `broadcastOn` 메서드가 `Channel` 인스턴스가 아닌 Eloquent 모델 인스턴스를 반환한 점에 주목하세요. 만약 Eloquent 모델 인스턴스가 `broadcastOn` 반환 값(또는 배열 내)에 있으면 Laravel은 모델 클래스명과 기본 키 식별자를 기반으로 이름 지정된 비공개 채널 인스턴스를 자동 생성합니다.

예를 들어, `App\Models\User` 클래스 인스턴스의 `id`가 `1`이라면, `Illuminate\Broadcasting\PrivateChannel` 인스턴스에 이름이 `App.Models.User.1`인 채널로 변환됩니다. 물론, 모델 인스턴스 대신 직접 `Channel` 인스턴스를 반환해 채널 이름을 완전하게 제어할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트할 채널 반환.
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return [new PrivateChannel('user.'.$this->id)];
}
```

모델 인스턴스를 채널 생성자에 전달하면 Laravel은 위 모델 채널 규칙에 따라 모델을 채널 이름 문자열로 변환합니다:

```php
return [new Channel($this->user)];
```

모델 채널 이름을 알고 싶으면 `broadcastChannel` 메서드를 호출하세요. 예를 들어, `App\Models\User` 인스턴스에서 `broadcastChannel`은 `App.Models.User.1` 문자열을 반환합니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 애플리케이션 `App\Events` 디렉토리 내의 "실제" 이벤트가 아니므로, 이름과 페이로드가 규칙에 따라 부여됩니다. Laravel 규칙은 모델 클래스명(네임스페이스 제외)과 발생한 모델 이벤트명으로 브로드캐스트 이름을 만듭니다.

예를 들어, `App\Models\Post` 모델을 수정하면 클라이언트 측에 `PostUpdated` 이벤트를 방송하며 페이로드는 다음처럼 모델 데이터를 포함합니다:

```
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

`App\Models\User` 모델 삭제 시엔 이름이 `UserDeleted`인 이벤트를 보냅니다.

원한다면 `broadcastAs`와 `broadcastWith` 메서드를 모델에 추가하여, 발생하는 각 모델 이벤트별 맞춤 이름과 페이로드를 설정할 수 있습니다. `broadcastAs`가 `null`을 반환하면 기본 규칙을 사용합니다:

```php
/**
 * 모델 이벤트 브로드캐스트 이름.
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
 * 브로드캐스트할 모델 데이터 반환.
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
### 모델 브로드캐스트 청취하기 (Listening For Model Broadcasts)

모델에 `BroadcastsEvents` 트레이트를 추가하고 `broadcastOn` 메서드를 정의했다면, 클라이언트 측에서 모델 브로드캐스트 이벤트를 청취할 준비가 된 겁니다. 시작 전에 [이벤트 청취](#listening-for-events) 문서를 참고하면 도움이 됩니다.

먼저 `private` 메서드에 모델 브로드캐스팅 규칙(#model-broadcasting-conventions)과 일치하는 채널 이름을 넣어 채널 인스턴스를 가져옵니다. 그리고 `listen` 메서드로 특정 이벤트를 청취합니다. 모델 브로드캐스트 이벤트는 애플리케이션 `App\Events` 네임스페이스에 속하지 않다는 표시로 이벤트 이름 앞에 반드시 `.`를 붙여야 합니다. 각 모델 이벤트에는 방송 가능한 모델 속성을 담은 `model` 프로퍼티가 있습니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트 (Client Events)

> [!TIP]
> [Pusher Channels](https://pusher.com/channels)를 사용할 땐, [대시보드](https://dashboard.pusher.com/)의 "앱 설정"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 보낼 수 있습니다.

서버를 거치지 않고 다른 연결된 클라이언트들에게 이벤트를 브로드캐스트해야 할 경우가 있습니다. 예를 들어, 사용자가 채팅 입력란에 타이핑 중임을 알리는 "입력 중" 알림은 서버에 요청하지 않고 클라이언트끼리 직접 방송하면 유용합니다.

클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용합니다:

```
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트를 청취하려면 `listenForWhisper`를 사용하세요:

```
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림 (Notifications)

이벤트 브로드캐스팅과 [알림 시스템](/docs/{{version}}/notifications)을 함께 사용하면, 자바스크립트 애플리케이션에서 새 알림이 발생할 때마다 페이지를 새로 고치지 않고 즉시 수신할 수 있습니다. 시작 전, [브로드캐스트 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 사용법을 꼭 읽어보세요.

알림이 브로드캐스트 채널을 사용하도록 구성되면, Echo의 `notification` 메서드로 브로드캐스트 알림 이벤트를 청취할 수 있습니다. 채널 이름은 알림을 받는 엔티티 클래스명과 일치해야 합니다:

```
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

위 예제는 `broadcast` 채널을 통해 `App\Models\User` 인스턴스에게 전송되는 모든 알림을 콜백에서 수신합니다. 기본 `BroadcastServiceProvider`에는 `App.Models.User.{id}` 채널 권한 부여 콜백이 포함되어 있어 연결이 원활합니다.