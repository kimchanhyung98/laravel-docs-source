# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [서버 측 설치](#server-side-installation)
    - [설정](#configuration)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [오픈 소스 대안](#open-source-alternatives)
- [클라이언트 측 설치](#client-side-installation)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여](#authorizing-channels)
    - [권한 부여 라우트 정의](#defining-authorization-routes)
    - [권한 부여 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [자신을 제외한 사용자에게만](#only-to-others)
    - [연결 커스터마이징](#customizing-the-connection)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 청취](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 권한 부여](#authorizing-presence-channels)
    - [프레즌스 채널 참가](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 청취](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

현대 웹 애플리케이션에서 실시간으로 화면을 업데이트하는 인터페이스를 구현할 때 WebSocket을 많이 사용합니다. 서버 쪽에서 데이터가 업데이트되면, 보통 WebSocket 연결을 통해 클라이언트로 메시지를 전송합니다. WebSocket은 UI의 데이터 변경을 반영하기 위해 애플리케이션 서버에 계속 폴링하는 것보다 훨씬 효율적인 대안입니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고 이메일로 전송할 수 있다고 가정해봅시다. 하지만 CSV 파일을 생성하는 데 몇 분이 걸리기 때문에, 이 작업을 [큐 처리 작업](/docs/9.x/queues)으로 만들어 처리합니다. CSV가 만들어지고 이메일로 전송되면, `App\Events\UserDataExported` 이벤트를 브로드캐스팅하여 애플리케이션의 자바스크립트가 이를 수신할 수 있습니다. 이벤트가 수신되면 사용자가 페이지를 새로고침하지 않아도 CSV가 이메일로 전송되었다는 메시지를 표시할 수 있습니다.

이러한 기능 구현을 돕기 위해 Laravel은 서버 측 Laravel [이벤트](/docs/9.x/events)를 WebSocket 연결을 통해 쉽게 "브로드캐스팅"할 수 있도록 지원합니다. Laravel 이벤트를 브로드캐스팅하면 서버 측 Laravel 애플리케이션과 클라이언트 측 자바스크립트 애플리케이션 간에 같은 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트가 프론트엔드에서 명명된 채널에 연결하고, 백엔드인 Laravel 애플리케이션이 이 채널들에 이벤트를 브로드캐스팅합니다. 이 이벤트에는 프론트엔드에 제공할 추가 데이터를 담을 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 두 가지 서버 측 브로드캐스팅 드라이버를 제공합니다: [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com). 하지만 커뮤니티에서 개발한 [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction)나 [soketi](https://docs.soketi.app/) 같은 패키지는 상업용 브로드캐스팅 제공업체 없이도 브로드캐스팅 드라이버를 추가로 제공합니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 Laravel의 [이벤트와 리스너](/docs/9.x/events) 문서를 반드시 읽어보세요.

<a name="server-side-installation"></a>
## 서버 측 설치

Laravel 이벤트 브로드캐스팅 사용을 시작하려면, Laravel 애플리케이션 내에서 몇 가지 설정을 하고 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스팅 드라이버를 통해 이루어지며, 이는 Laravel 이벤트를 브로드캐스팅해서 브라우저 클라이언트에서 Laravel Echo(자바스크립트 라이브러리)가 이를 수신할 수 있도록 합니다. 걱정하지 마세요. 설치 과정의 각 단계를 차근차근 살펴보겠습니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 설정 파일에 저장됩니다. Laravel은 기본으로 [Pusher Channels](https://pusher.com/channels), [Redis](/docs/9.x/redis), 그리고 로컬 개발과 디버깅용 `log` 드라이버를 지원합니다. 또한, 테스트 시 브로드캐스팅을 완전히 비활성화하는 `null` 드라이버도 포함되어 있습니다. 각 드라이버별 예제 설정은 `config/broadcasting.php` 파일에 미리 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### Broadcast 서비스 프로바이더

이벤트를 브로드캐스팅하기 전에 먼저 `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 새로운 Laravel 애플리케이션에서는 `config/app.php` 설정 파일의 `providers` 배열에서 이 프로바이더의 주석을 해제하는 것만으로 충분합니다. 이 `BroadcastServiceProvider`는 브로드캐스트 권한 부여 라우트와 콜백을 등록하는 데 필요한 코드를 포함합니다.

<a name="queue-configuration"></a>
#### 큐 설정

또한 [큐 워커](/docs/9.x/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐에 등록된 잡(job)을 통해 수행되므로, 이벤트 브로드캐스팅이 애플리케이션의 응답 시간을 심각하게 저하시켜서는 안 됩니다.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)로 이벤트를 브로드캐스팅할 계획이라면, Composer 패키지 관리자를 통해 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

다음으로, `config/broadcasting.php` 설정 파일에서 Pusher Channels 자격 증명을 구성합니다. 이 파일에는 key, secret, application ID를 빠르게 지정할 수 있도록 이미 Pusher Channels 예제가 포함되어 있습니다. 보통 이 값들은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/9.x/configuration#environment-configuration)를 통해 설정합니다:

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

`config/broadcasting.php`의 `pusher` 설정에서는 클러스터 등 Pusher Channels에서 지원하는 추가 `options`도 지정할 수 있습니다.

마지막으로, `.env` 파일에서 브로드캐스트 드라이버를 `pusher`로 변경합니다:

```ini
BROADCAST_DRIVER=pusher
```

이후 [Laravel Echo](#client-side-installation)를 설치하고 구성하면 클라이언트 측에서 브로드캐스트 이벤트를 수신할 준비가 완료됩니다.

<a name="pusher-compatible-open-source-alternatives"></a>
#### 오픈 소스 Pusher 대안

[laravel-websockets](https://github.com/beyondcode/laravel-websockets)와 [soketi](https://docs.soketi.app/) 패키지는 Laravel용 Pusher 호환 WebSocket 서버를 제공합니다. 이 패키지들을 사용하면 상업용 WebSocket 제공업체 없이도 Laravel 브로드캐스팅의 모든 기능을 활용할 수 있습니다. 설치 및 사용법은 [오픈 소스 대안](#open-source-alternatives) 문서를 참고하세요.

<a name="ably"></a>
### Ably

[Ably](https://ably.com)로 이벤트를 브로드캐스팅할 경우에는 Composer 패키지 관리자를 이용해 Ably PHP SDK를 설치하세요:

```shell
composer require ably/ably-php
```

이어 `config/broadcasting.php` 설정 파일에 Ably 자격 증명을 구성합니다. 이 파일에는 key를 빠르게 지정할 수 있도록 Ably 예제가 포함되어 있습니다. 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/9.x/configuration#environment-configuration)를 통해 지정합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 브로드캐스트 드라이버를 `ably`로 변경합니다:

```ini
BROADCAST_DRIVER=ably
```

마지막으로, [Laravel Echo](#client-side-installation)를 설치하고 구성하여 클라이언트 측에서 브로드캐스트 이벤트를 수신할 준비를 합니다.

<a name="open-source-alternatives"></a>
### 오픈 소스 대안

<a name="open-source-alternatives-php"></a>
#### PHP

[laravel-websockets](https://github.com/beyondcode/laravel-websockets) 패키지는 Laravel용 순수 PHP Pusher 호환 WebSocket 패키지입니다. 이 패키지를 사용하면 상업용 WebSocket 제공업체 없이도 Laravel 브로드캐스팅을 완벽히 활용할 수 있습니다. 자세한 설치 및 사용법은 [공식 문서](https://beyondco.de/docs/laravel-websockets)를 참고하세요.

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반의 Pusher 호환 WebSocket 서버로, 내부적으로 매우 확장성 높고 빠른 µWebSockets.js를 사용합니다. 이 패키지는 역시 상업용 WebSocket 제공업체 없이도 Laravel 브로드캐스팅을 완벽히 활용할 수 있습니다. 자세한 설치 및 사용법은 [공식 문서](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스팅 드라이버를 통해 브로드캐스트되는 이벤트에 채널 구독 및 이벤트 청취를 쉽게 할 수 있도록 도와주는 자바스크립트 라이브러리입니다. NPM 패키지 관리자를 통해 Echo를 설치할 수 있습니다. 여기서는 Pusher Channels 브로드캐스터를 사용하므로 `pusher-js` 패키지도 함께 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면 애플리케이션 자바스크립트에서 새 Echo 인스턴스를 생성할 준비가 된 것입니다. 일반적으로 Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단에서 생성하는 것이 좋습니다. 기본적으로 이 파일에는 Echo 설정 예제가 주석 상태로 포함되어 있으니, 주석을 해제하고 필요에 따라 수정하세요:

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

설정을 완료했으면 애플리케이션 자산을 컴파일합니다:

```shell
npm run dev
```

> [!NOTE]
> 애플리케이션 자바스크립트 자산 컴파일에 관해서는 [Vite](/docs/9.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 구성된 Pusher Channels 클라이언트 인스턴스를 Echo가 활용하게 하려면, Echo 인스턴스 생성 시 `client` 옵션으로 전달할 수 있습니다:

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

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스팅 드라이버에서 브로드캐스트하는 이벤트에 채널 구독 및 이벤트 청취를 쉽게 할 수 있도록 돕는 자바스크립트 라이브러리입니다. NPM 패키지 관리자를 통해 Echo를 설치할 수 있습니다. 여기서도 `pusher-js` 패키지를 같이 설치합니다.

Ably를 브로드캐스트에 사용하지만 `pusher-js` 자바스크립트 라이브러리를 설치하는 이유는, Ably가 Pusher 프로토콜 호환 모드를 제공하여 클라이언트 측에서 Pusher 프로토콜을 사용할 수 있도록 지원하기 때문입니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 대시보드 내 "Protocol Adapter Settings"에서 설정할 수 있습니다.**

Echo 설치 이후 `resources/js/bootstrap.js` 파일 하단에서 새 Echo 인스턴스를 생성할 준비가 되었습니다. 기본 파일 내 구성은 Pusher용이므로, 아래 예시를 참조하여 Ably용으로 변경하세요:

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

이때 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키를 가리키며, 이는 Ably 키에서 `:` 문자 앞부분입니다.

설정을 마친 후 애플리케이션 자산을 컴파일합니다:

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 자산 컴파일에 관해서는 [Vite](/docs/9.x/vite) 문서를 참조하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel 이벤트 브로드캐스팅은 서버 측 Laravel 이벤트를 드라이버 기반 WebSocket 방식을 통해 클라이언트 측 자바스크립트 애플리케이션에 브로드캐스트할 수 있도록 합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com) 드라이버를 제공합니다. 클라이언트 측에서는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 사용해 쉽게 이벤트를 수신하고 처리할 수 있습니다.

이벤트는 "채널" 위에서 브로드캐스트되며, 공개(public) 또는 비공개(private) 채널로 지정할 수 있습니다. 공개 채널은 인증이나 권한 없이 누구나 구독할 수 있지만, 비공개 채널은 해당 채널을 청취할 수 있는 권한이 있는 인증된 사용자만 구독할 수 있습니다.

> [!NOTE]
> Pusher의 오픈 소스 대안을 탐색하고 싶다면 [오픈 소스 대안](#open-source-alternatives)을 참고하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

각 브로드캐스팅 구성요소를 자세히 살펴보기에 앞서, 전자상거래 매장을 예로 들어 개략적인 흐름을 살펴보겠습니다.

예를 들어 사용자가 주문한 상품의 배송 상태를 볼 수 있는 페이지가 있다고 합시다. 주문 배송 상태가 업데이트되면 `OrderShipmentStatusUpdated` 이벤트가 발생한다고 가정합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 상태를 확인할 때마다 새로고침하지 않도록, 업데이트가 생성되는 즉시 브로드캐스팅으로 변경 사항을 알려야 합니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해서 해당 이벤트가 발생하면 브로드캐스팅되도록 합니다:

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
     * 주문 인스턴스입니다.
     *
     * @var \App\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스를 구현하면 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트가 브로드캐스팅될 채널을 반환하는 역할을 하며, 생성된 이벤트 클래스에 이미 빈 메서드 형태로 포함되어 있으니 내용을 채우면 됩니다. 오직 주문 생성자만 상태 업데이트를 볼 수 있도록 주문별로 연동된 비공개 채널에서 이벤트를 브로드캐스팅하도록 합니다:

```
/**
 * 이벤트가 브로드캐스팅될 채널을 반환합니다.
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

비공개 채널은 권한이 있어야 청취할 수 있으므로, `routes/channels.php`에서 채널 권한 부여 규칙을 정의합니다. 여기서는 `orders.1` 비공개 채널을 청취하려는 사용자가 실제로 해당 주문 생성자인지 확인하는 예시입니다:

```
use App\Models\Order;

Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인수를 받는데, 첫 번째는 채널 이름, 두 번째는 사용자 권한 청취 여부를 `true` 또는 `false`로 반환하는 콜백입니다.

모든 권한 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고, 추가적으로 와일드카드 매개변수를 받습니다. 여기서는 `{orderId}` 자리 표시자가 채널 이름의 "ID" 부분을 나타내는 와일드카드입니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 청취

클라이언트 자바스크립트에서 이벤트를 청취하려면 [Laravel Echo](#client-side-installation)를 사용합니다. 먼저 `private` 메서드로 비공개 채널을 구독하고, `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 청취합니다. 기본적으로 이벤트의 모든 public 속성은 브로드캐스트 페이로드에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

Laravel에게 특정 이벤트를 브로드캐스트하도록 알리려면, 이벤트 클래스에서 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. Laravel은 프레임워크에서 생성한 모든 이벤트 클래스에 기본적으로 이 인터페이스를 import하므로 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 한 가지 메서드 `broadcastOn`을 요구합니다. 이 메서드는 이벤트가 브로드캐스팅될 단일 채널 또는 채널 배열을 반환해야 하며, `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스를 반환해야 합니다. `Channel`은 공개 채널로 모든 사용자가 구독할 수 있고, `PrivateChannel`과 `PresenceChannel`은 [채널 권한 부여](#authorizing-channels)가 필요한 비공개 채널입니다:

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
     * 이벤트 인스턴스 생성자.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * 이벤트가 브로드캐스팅될 채널을 반환.
     *
     * @return Channel|array
     */
    public function broadcastOn()
    {
        return new PrivateChannel('user.'.$this->user->id);
    }
}
```

`ShouldBroadcast`를 구현하면 평소처럼 [이벤트를 발생](/docs/9.x/events)시키기만 하면 됩니다. 이벤트가 발생하면 [큐에 등록된 작업](/docs/9.x/queues)이 자동으로 지정된 브로드캐스트 드라이버를 이용해 이벤트를 브로드캐스팅합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스 이름을 브로드캐스트 이벤트 이름으로 사용합니다. 하지만 `broadcastAs` 메서드를 정의해 브로드캐스트 이름을 커스터마이징할 수 있습니다:

```
/**
 * 이벤트 브로드캐스트 이름.
 *
 * @return string
 */
public function broadcastAs()
{
    return 'server.created';
}
```

`broadcastAs`로 이름을 변경하면, Echo에서는 앞에 `.` 문자를 붙여서 리스너를 등록해야 네임스페이스가 붙지 않습니다:

```
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 해당 이벤트 클래스의 모든 `public` 속성이 자동으로 직렬화되어 이벤트 페이로드에 포함되므로 자바스크립트에서 이 데이터를 사용할 수 있습니다. 예를 들어, `public $user` 속성이 있는 이벤트라면 브로드캐스트 페이로드 예시는 다음과 같습니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

필요하다면, `broadcastWith` 메서드를 추가해 브로드캐스트할 배열 데이터를 직접 제어할 수도 있습니다:

```
/**
 * 브로드캐스트할 데이터를 반환.
 *
 * @return array
 */
public function broadcastWith()
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
### 브로드캐스트 큐

기본적으로, 각 브로드캐스트 이벤트는 `queue.php` 설정에 지정된 기본 큐 연결의 기본 큐에 추가됩니다. 이벤트 클래스에 `connection`과 `queue`라는 속성을 정의하여 큐 연결과 큐 이름을 사용자 지정할 수 있습니다:

```
/**
 * 브로드캐스트 시 사용할 큐 연결 이름.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스팅 작업을 등록할 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드를 정의하여 큐 이름을 지정할 수도 있습니다:

```
/**
 * 브로드캐스팅 작업을 등록할 큐 이름을 반환.
 *
 * @return string
 */
public function broadcastQueue()
{
    return 'default';
}
```

기본 큐 드라이버 대신 `sync` 큐를 사용해 즉시 브로드캐스트하려면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요:

```
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    //
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건이 true일 때만 이벤트를 브로드캐스트하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 정의하세요:

```
/**
 * 이벤트를 브로드캐스트할지 여부 결정.
 *
 * @return bool
 */
public function broadcastWhen()
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 브로드캐스트 이벤트를 발생시키면, 큐 작업이 해당 트랜잭션이 커밋되기 전에 실행될 수 있습니다. 이 경우 트랜잭션 중에 적용한 모델이나 DB 레코드의 변경사항이 데이터베이스에 반영되지 않았을 수도 있고, 생성된 모델이나 레코드가 DB에 없을 수도 있습니다. 이런 의존성이 있는 경우, 큐 작업 실행 중 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`라면, 이벤트 클래스에 `$afterCommit` 속성을 `true`로 정의해 트랜잭션 커밋 후에 브로드캐스트되도록 명시할 수 있습니다:

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

> [!NOTE]
> 이런 문제에 대한 자세한 해결책은 [큐 작업과 데이터베이스 트랜잭션](/docs/9.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여

비공개 채널은 현재 인증된 사용자가 해당 채널을 청취할 권한이 있는지 확인해야 합니다. 이는 Laravel 애플리케이션에 채널명을 포함한 HTTP 요청을 보내서 사용자의 권한 여부를 판단하는 방식입니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 비공개 채널 구독 권한 확인 요청은 자동으로 보내집니다. 다만 요청을 처리할 라우트를 반드시 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 권한 부여 라우트 정의

Laravel은 채널 권한 부여 요청에 응답하는 라우트를 쉽게 정의할 수 있도록 합니다. `App\Providers\BroadcastServiceProvider`에서 `Broadcast::routes` 메서드를 호출하는 부분이 보일 것입니다. 이 메서드는 `/broadcasting/auth` 경로를 등록하여 권한 부여 요청을 처리합니다:

```
Broadcast::routes();
```

`Broadcast::routes` 메서드는 기본적으로 경로를 `web` 미들웨어 그룹에 등록하지만, 인수로 라우트 속성 배열을 넘겨 속성을 커스터마이징할 수도 있습니다:

```
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>
#### 권한 부여 엔드포인트 커스터마이징

기본적으로 Echo는 `/broadcasting/auth` 엔드포인트에서 채널 접근 권한을 체크합니다. 하지만 Echo 인스턴스를 생성할 때 `authEndpoint` 옵션을 지정해서 자신만의 엔드포인트를 지정할 수도 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 권한 부여 요청 커스터마이징

Laravel Echo가 권한 부여 요청을 어떻게 수행할지 직접 정의하려면 Echo 초기화 시 `authorizer` 옵션으로 커스텀 인증자를 전달할 수 있습니다:

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

실제로 현재 인증된 사용자가 특정 채널을 청취할 권한이 있는지 판단하는 로직은 `routes/channels.php` 파일에 작성합니다. 여기서 `Broadcast::channel` 메서드를 사용하여 권한 부여 콜백을 등록합니다:

```
Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 인수를 받으며, 첫째는 채널 이름, 둘째는 `true` 혹은 `false`를 반환하는 권한 콜백입니다.

권한 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고, 와일드카드 매개변수를 추가 인수로 받습니다. 위 예제에서는 `{orderId}`가 와일드카드입니다.

<a name="authorization-callback-model-binding"></a>
#### 권한 콜백 모델 바인딩

HTTP 라우트처럼 채널 라우트도 암묵적 또는 명시적 [라우트 모델 바인딩](/docs/9.x/routing#route-model-binding)을 사용할 수 있습니다. 예를 들어 문자열이나 숫자 ID 대신 실제 `Order` 모델 인스턴스를 받을 수도 있습니다:

```
use App\Models\Order;

Broadcast::channel('orders.{order}', function ($user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리 채널 모델 바인딩은 자동 [암묵적 모델 바인딩 스코핑](/docs/9.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 그러나 대부분의 경우 문제되지 않으며, 대부분의 채널은 고유한 기본키를 기준으로 스코핑 가능합니다.

<a name="authorization-callback-authentication"></a>
#### 권한 콜백 인증

비공개 및 프레즌스 채널은 애플리케이션의 기본 인증 가드를 사용해서 현재 사용자를 인증합니다. 인증되지 않으면 권한이 자동으로 거부되고 권한 콜백도 실행되지 않습니다. 필요한 경우 여러 개의 커스텀 가드를 지정할 수도 있습니다:

```
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션에서 많은 채널을 관리한다면, `routes/channels.php` 파일 내 클로저가 다소 방대해질 수 있습니다. 이때 권한 부여 로직을 클로저 대신 채널 클래스로 정의할 수 있습니다. `make:channel` Artisan 명령어를 사용하여 채널 클래스를 생성하세요. 클래스를 `App/Broadcasting` 디렉토리에 생성합니다:

```shell
php artisan make:channel OrderChannel
```

`routes/channels.php`에 생성한 클래스를 등록합니다:

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스의 `join` 메서드에 권한 부여 로직을 작성합니다. 이 메서드는 보통 권한 부여 클로저에 놓던 로직과 동일하며, 채널 모델 바인딩도 활용할 수 있습니다:

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
     * 사용자의 채널 접근 인증 처리.
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

> [!NOTE]
> Laravel의 다른 클래스들과 마찬가지로 채널 클래스도 [서비스 컨테이너](/docs/9.x/container)에 의해 자동으로 의존성 주입되어 생성되므로, 필요한 의존성을 생성자에 타입힌트할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현하면, 이벤트의 dispatch 메서드를 호출하기만 하면 됩니다. 이벤트 디스패처는 이벤트에 `ShouldBroadcast`가 구현된 것을 감지하여 브로드캐스팅 큐 작업을 등록합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 자신을 제외한 사용자에게만 브로드캐스트하기

이벤트 브로드캐스팅을 활용하는 애플리케이션에서, 가끔 현재 사용자 자신을 제외한 채널 구독자에게만 이벤트를 보내고 싶을 때가 있습니다. 그런 경우 `broadcast` 헬퍼와 `toOthers` 메서드를 사용합니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어 할 일 목록 앱에서 사용자가 새 작업을 생성하면, `/task` URL에 POST 요청을 보내 작업 생성 이벤트를 브로드캐스트하고, JSON 형태의 새 작업 데이터를 반환할 수 있습니다. 자바스크립트는 응답을 받아 리스트에 직접 작업을 추가합니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만 작업 생성 이벤트도 브로드캐스트하기 때문에, 이 이벤트를 청취하는 경우 중복된 작업이 목록에 나타납니다: 요청 응답과 브로드캐스트 두 곳에서 작업이 추가되기 때문입니다. `toOthers` 메서드를 사용하면 현재 접속자는 이벤트를 받지 않도록 할 수 있습니다.

> [!WARNING]
> `toOthers` 메서드를 호출하려면, 이벤트 클래스에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 구성

Laravel Echo 인스턴스를 초기화하면 각 연결에 소켓 ID가 할당됩니다. 글로벌 [Axios](https://github.com/mzabriskie/axios) 인스턴스로 HTTP 요청하면, `X-Socket-ID` 헤더에 소켓 ID가 자동으로 포함됩니다. `toOthers`를 호출하면 Laravel은 이 헤더에서 소켓 ID를 추출해 동일 소켓 ID를 가진 연결에는 브로드캐스트하지 않도록 통신합니다.

글로벌 Axios가 아니면 직접 소켓 ID를 HTTP 요청 헤더에 추가해야 하며, 소켓 ID는 `Echo.socketId()` 메서드로 얻을 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 커스터마이징

애플리케이션에서 여러 브로드캐스트 연결을 사용하는 경우, 기본 연결 이외의 다른 브로드캐스터를 지정해 이벤트를 보낼 수 있습니다. `via` 메서드를 사용하세요:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또한 이벤트 클래스 내에서 `InteractsWithBroadcasting` 트레이트를 사용하고, 생성자에서 `broadcastVia` 메서드를 호출해 연동할 브로드캐스트 연결을 지정할 수도 있습니다:

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
     * 이벤트 인스턴스 생성자.
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
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 청취

[Laravel Echo를 설치하고 인스턴스를 생성](#client-side-installation)했다면, 이제 Laravel 애플리케이션에서 브로드캐스트하는 이벤트를 청취할 준비가 된 것입니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻고, `listen` 메서드로 특정 이벤트를 청취합니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널 이벤트를 듣고 싶으면 `private` 메서드를 사용합니다. 여러 이벤트를 하나의 채널에서 청취하려면 `listen` 메서드를 연속으로 연결할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 청취 멈추기

채널을 [나가지](#leaving-a-channel) 않고 특정 이벤트 청취만 중단하고 싶으면 `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널 구독을 종료하려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

비공개 및 프레즌스 채널까지 모두 떠나려면 `leave` 메서드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

앞의 코드 예제에서 이벤트 클래스의 전체 `App\Events` 네임스페이스를 명시하지 않았는데, Echo는 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 가정하기 때문입니다. Echo 인스턴스 생성 시 `namespace` 설정 옵션으로 루트 네임스페이스를 변경할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 이벤트 클래스 앞에 `.`을 붙여 완전한 클래스 네임스페이스를 항상 명시할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        //
    });
```

<a name="presence-channels"></a>
## 프레즌스 채널

프레즌스 채널은 비공개 채널의 보안을 기반으로, 채널 내에 누가 구독 중인지 알 수 있는 기능을 추가로 제공합니다. 이를 통해 같은 페이지를 보고 있는 사용자가 누구인지 알려주거나, 채팅방 참가자 목록을 노출하는 등 강력한 협업 기능을 쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 권한 부여

프레즌스 채널도 비공개 채널이므로 [접근 권한 부여](#authorizing-channels)가 필요합니다. 하지만 권한 콜백에서 사용자가 채널에 참가할 수 있을 경우 `true`가 아닌, 사용자에 대한 배열 데이터를 반환해야 합니다.

이 배열 데이터는 자바스크립트에서 프레즌스 채널 이벤트 리스너가 접근할 수 있습니다. 권한이 없으면 `false`나 `null`을 반환해야 합니다:

```
Broadcast::channel('chat.{roomId}', function ($user, $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참가

Echo의 `join` 메서드는 프레즌스 채널에 참가하며, 이 메서드는 `PresenceChannel` 구현체를 반환합니다. `PresenceChannel`은 `listen` 메서드 외에도 `here`, `joining`, `leaving` 이벤트 구독을 지원합니다:

```js
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

- `here`: 채널에 성공적으로 참가한 직후 실행되며 현재 구독 중인 모든 사용자 정보 배열을 받습니다.
- `joining`: 새 사용자가 채널에 참가할 때 실행됩니다.
- `leaving`: 사용자가 채널을 떠날 때 실행됩니다.
- `error`: 인증 엔드포인트가 200번 이외 HTTP 상태 코드를 반환하거나, 반환된 JSON 파싱에 문제가 발생하면 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅

프레즌스 채널도 공개나 비공개 채널처럼 이벤트를 받을 수 있습니다. 예를 들어 채팅방 `NewMessage` 이벤트를 프레즌스 채널에 브로드캐스팅하려면, 이벤트 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다:

```
/**
 * 이벤트가 브로드캐스팅될 채널을 반환.
 *
 * @return Channel|array
 */
public function broadcastOn()
{
    return new PresenceChannel('room.'.$this->message->room_id);
}
```

다른 이벤트처럼 `broadcast` 헬퍼와 `toOthers` 메서드를 사용해 현재 사용자 제외 브로드캐스트도 가능합니다:

```
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

클라이언트는 Echo의 `listen` 메서드로 프레즌스 채널 이벤트를 받을 수 있습니다:

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        //
    });
```

<a name="model-broadcasting"></a>
## 모델 브로드캐스팅

> [!WARNING]
> 모델 브로드캐스팅 문서를 읽기 전에 Laravel 모델 브로드캐스팅 전반 개념과 수동으로 이벤트 정의 및 청취하는 법을 이해했는지 확인하세요.

애플리케이션에서 [Eloquent 모델](/docs/9.x/eloquent)이 생성, 업데이트, 삭제될 때 이벤트를 브로드캐스팅하는 경우가 많습니다. 물론 이는 수동으로 커스텀 이벤트를 정의하고 `ShouldBroadcast`를 구현하여 쉽게 할 수 있습니다.

하지만 모델 상태 변경 이벤트를 브로드캐스팅 용도로만 사용한다면 이벤트 클래스를 별도로 만드는 것이 번거로울 수 있습니다. 이때 Laravel은 Eloquent 모델에 자동으로 상태 변경 이벤트를 브로드캐스팅하도록 할 수 있게 지원합니다.

우선 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용하도록 하고, `broadcastOn` 메서드를 정의해 모델 이벤트를 브로드캐스팅할 채널 배열을 반환해야 합니다:

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
     * 이 포스트가 속한 사용자 반환.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트될 채널을 반환.
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

이후 해당 모델에서 인스턴스가 생성, 업데이트, 삭제, 휴지통 처리, 복구될 때마다 자동으로 이벤트가 브로드캐스팅됩니다.

`broadcastOn` 메서드는 `$event`라는 발생한 이벤트 유형 문자열을 인수로 받으며, 값은 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이를 조건문에서 확인해 특정 이벤트에 대해 채널을 다르게 지정할 수 있습니다:

```php
/**
 * 모델 이벤트가 브로드캐스트될 채널을 반환.
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

가끔 Laravel이 생성하는 모델 브로드캐스팅 이벤트를 커스터마이징하고 싶을 수 있습니다. 이 경우 모델에 `newBroadcastableEvent` 메서드를 정의하면 되고, `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델용 새 브로드캐스터블 이벤트 생성.
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

앞서 예제의 `broadcastOn` 메서드는 `Channel` 인스턴스가 아니라 Eloquent 모델 인스턴스를 반환했습니다. 만약 `broadcastOn`이 Eloquent 모델 인스턴스를 반환하거나 배열에 포함하면, Laravel은 모델 클래스명과 기본키 식별자를 조합한 이름으로 비공개 채널 인스턴스를 자동 생성합니다.

예를 들어, `App\Models\User` 모델 ID `1`은 `App.Models.User.1`이라는 이름의 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환됩니다. 물론 완전한 채널 인스턴스를 반환해 모델 채널 이름을 완전히 제어할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트될 채널을 반환.
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return [new PrivateChannel('user.'.$this->id)];
}
```

만약 `broadcastOn`에 채널 인스턴스 대신 모델을 넘기면, Laravel은 모델 채널 규칙에 따라 이를 채널 이름 문자열로 변환합니다:

```php
return [new Channel($this->user)];
```

특정 모델 인스턴스의 채널 이름을 알고 싶으면, `broadcastChannel` 메서드를 호출하세요. 예를 들어 `App\Models\User` 모델 인스턴스는 `App.Models.User.1` 같은 문자열을 반환합니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스팅 이벤트는 애플리케이션 `App\Events` 디렉터리 내 실제 이벤트와는 별도로 규칙에 따라 이름과 페이로드를 갖습니다. Laravel에서는 네임스페이스를 제외한 모델 클래스명과 발생한 모델 이벤트 명을 결합해 이벤트 이름으로 사용합니다.

예를 들어 `App\Models\Post` 모델의 업데이트는 클라이언트에 `PostUpdated` 이벤트와 아래 페이로드로 브로드캐스트됩니다:

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

사용자 모델이 삭제되는 경우 `UserDeleted` 이벤트가 브로드캐스트됩니다.

필요하면 `broadcastAs`와 `broadcastWith` 메서드를 모델에 정의해, 각 모델 이벤트에 따라 브로드캐스트 이름과 페이로드를 커스터마이징할 수 있습니다. `broadcastAs`가 `null`을 반환하면 기본 모델 브로드캐스팅 규칙이 적용됩니다:

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
 * 모델 브로드캐스트 시 사용할 데이터.
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
### 모델 브로드캐스트 청취

`BroadcastsEvents` 트레이트를 모델에 추가하고 `broadcastOn` 메서드를 정의했다면, 클라이언트 측에서 모델 이벤트를 청취할 준비가 된 것입니다. 먼저 [이벤트 청취](#listening-for-events) 문서를 참고하세요.

`private` 메서드에 채널 이름을 전달해 채널 인스턴스를 얻고, `listen` 메서드로 원하는 이벤트를 청취합니다. 채널 이름은 Laravel 모델 브로드캐스팅 규칙에 맞춰 지정해야 합니다.

모델 브로드캐스트 이벤트는 실제 `App\Events` 디렉터리 내 이벤트가 아니므로, [이벤트 이름](#model-broadcasting-event-conventions) 앞에 접두사 `.`를 붙여 네임스페이스가 없음을 명시해야 합니다. 각 이벤트는 `model` 속성에 모델의 브로드캐스트 가능한 모든 데이터를 포함합니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, 클라이언트 이벤트를 보내기 위해서는 [대시보드](https://dashboard.pusher.com/) 내 "앱 설정" 섹션에서 "Client Events" 옵션을 활성화해야 합니다.

클라이언트 간에 Laravel 서버를 경유하지 않고 직접 이벤트를 브로드캐스트하고 싶을 수 있습니다. 예를 들어 "타이핑 중" 상태 알림과 같이, 다른 사용자가 메시지를 작성 중임을 실시간 알리고 싶을 때 유용합니다.

Echo의 `whisper` 메서드를 사용해 클라이언트 이벤트를 브로드캐스트할 수 있습니다:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트를 청취하려면 `listenForWhisper` 메서드를 사용하세요:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅과 [알림](/docs/9.x/notifications)을 결합하면, 자바스크립트 애플리케이션이 새 알림을 페이지 새로고침 없이 실시간으로 수신할 수 있습니다. 시작하기 전에, [브로드캐스트 알림 채널](/docs/9.x/notifications#broadcast-notifications) 문서를 꼭 읽어보세요.

알림이 브로드캐스트 채널을 사용하도록 설정한 후, Echo의 `notification` 메서드로 브로드캐스트 이벤트를 청취할 수 있습니다. 채널 이름은 알림을 받을 엔티티 클래스명과 일치해야 합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

예를 들어, `App\Models\User` 인스턴스에 보내진 모든 브로드캐스트 알림은 콜백으로 수신됩니다. 기본 Laravel 프레임워크에 포함된 `BroadcastServiceProvider`에는 `App.Models.User.{id}` 채널에 대한 권한 부여 콜백이 미리 포함되어 있습니다.