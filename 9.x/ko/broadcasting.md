# 브로드캐스팅

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
    - [브로드캐스팅 & 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인증](#authorizing-channels)
    - [인증 라우트 정의](#defining-authorization-routes)
    - [인증 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스팅](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [Presence 채널](#presence-channels)
    - [Presence 채널 인증](#authorizing-presence-channels)
    - [Presence 채널 가입](#joining-presence-channels)
    - [Presence 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 컨벤션](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notifications)](#notifications)

<a name="introduction"></a>
## 소개

최근의 많은 웹 애플리케이션에서는 WebSocket을 활용해 실시간, 라이브 UI 업데이트를 구현합니다. 서버에서 데이터가 변경되었을 때, 메시지가 WebSocket 커넥션을 통해 전송되며 클라이언트에서 처리됩니다. WebSocket은 UI에 반영해야 할 데이터 변화를 서버에 지속적으로 폴링하는 것보다 훨씬 효율적인 방법입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내고 이메일로 발송하는 기능을 생각해 볼 수 있습니다. 하지만 CSV 파일 생성 시간이 오래 걸린다면, [큐 처리된 작업](/docs/{{version}}/queues) 내에서 CSV를 생성하고 메일로 발송하도록 구현할 수 있습니다. CSV 파일이 생성되고 이메일 전송까지 완료되면, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션의 자바스크립트가 수신할 수 있게 할 수 있습니다. 이렇게 하면 페이지를 새로고침하지 않아도 사용자에게 CSV가 메일로 발송되었다는 메시지를 보여줄 수 있습니다.

이 기능을 쉽게 구축할 수 있도록, Laravel은 서버 사이드 [이벤트](/docs/{{version}}/events)를 WebSocket 커넥션을 통해 "브로드캐스트"할 수 있도록 지원합니다. 이벤트 브로드캐스팅을 사용하면 서버(라라벨)와 클라이언트(자바스크립트)에서 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 기본 개념은 단순합니다: 클라이언트는 프론트엔드에서 이름이 지정된 채널로 연결하고, 백엔드의 Laravel 애플리케이션은 이 채널에 이벤트를 브로드캐스트합니다. 이 이벤트는 프론트엔드로 전달하고자 하는 데이터를 자유롭게 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

기본적으로 Laravel은 서버 측 브로드캐스팅 드라이버로 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com)를 제공합니다. 또한 [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction)와 [soketi](https://docs.soketi.app/) 등 커뮤니티 주도의 패키지로 상업용 브로드캐스팅 제공업체 없이도 사용 가능한 드라이버를 추가할 수 있습니다.

> **참고**  
> 이벤트 브로드캐스팅을 학습하기 전에, [이벤트와 리스너](/docs/{{version}}/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 측 설치

Laravel의 이벤트 브로드캐스팅을 사용하려면 Laravel 애플리케이션에서 몇 가지 설정과 패키지 설치가 필요합니다.

이벤트 브로드캐스팅은 서버에서 Laravel 이벤트를 브로드캐스팅하여, 브라우저(클라이언트) 내에서는 Laravel Echo(자바스크립트 라이브러리)가 이를 수신하는 방식으로 동작합니다. 아래에서 각 설치 과정을 차근차근 설명합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 파일에 저장됩니다. Laravel은 기본적으로 여러 드라이버를 지원합니다: [Pusher Channels](https://pusher.com/channels), [Redis](/docs/{{version}}/redis), 로컬 개발/디버깅을 위한 `log` 드라이버. 또한 브로드캐스팅을 완전히 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버에 대한 예시 설정이 `config/broadcasting.php`에 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### 브로드캐스트 서비스 프로바이더

이벤트를 브로드캐스트하기 전에, `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 최신 Laravel 애플리케이션에서는 `config/app.php` 파일의 `providers` 배열에서 이 프로바이더의 주석을 해제하면 됩니다. 이 프로바이더는 브로드캐스트 인증 라우트와 콜백을 등록하는 데 필요한 코드를 포함합니다.

<a name="queue-configuration"></a>
#### 큐 설정

[큐 워커](/docs/{{version}}/queues)도 설정 및 실행해야 합니다. 이벤트 브로드캐스팅은 큐 작업을 통해 처리되기 때문에, 이벤트 브로드캐스트로 인해 애플리케이션의 응답 시간이 저하되지 않습니다.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 통해 이벤트를 브로드캐스트할 계획이라면, Composer로 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 파일에서 Pusher Channels 자격 증명을 설정합니다. 예시 설정이 이미 파일에 포함되어 있으므로, 여기에 키, 시크릿, 앱 ID 정보를 빠르게 입력할 수 있습니다. 일반적으로 이러한 값은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 지정해야 합니다:

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

`config/broadcasting.php`의 `pusher` 설정에서는 cluster 등 추가 옵션도 지정 가능합니다.

이제 `.env` 파일에서 브로드캐스트 드라이버를 `pusher`로 변경합니다:

```ini
BROADCAST_DRIVER=pusher
```

마지막으로, 클라이언트 측에서 브로드캐스트 이벤트를 수신할 수 있도록 [Laravel Echo](#client-side-installation)를 설치 및 설정하면 됩니다.

<a name="pusher-compatible-open-source-alternatives"></a>
#### 오픈 소스 Pusher 대안

[laravel-websockets](https://github.com/beyondcode/laravel-websockets)와 [soketi](https://docs.soketi.app/) 패키지는 Pusher와 호환되는 WebSocket 서버를 제공합니다. 상업용 WebSocket 서비스 없이도 Laravel 브로드캐스팅의 모든 기능을 사용할 수 있게 지원합니다. 설치 및 사용법의 자세한 내용은 [오픈 소스 대안](#open-source-alternatives) 문서를 참고하세요.

<a name="ably"></a>
### Ably

[Ably](https://ably.com)로 이벤트를 브로드캐스팅할 계획이라면, Composer를 사용하여 Ably PHP SDK를 설치하세요:

```shell
composer require ably/ably-php
```

그 다음, `config/broadcasting.php` 파일에서 Ably 자격 증명을 설정합니다. 예시 설정도 이미 포함되어 있습니다. 일반적으로 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)로 값이 지정되어야 합니다:

```ini
ABLY_KEY=your-ably-key
```

그리고 `.env` 파일에서 브로드캐스트 드라이버를 `ably`로 변경하세요:

```ini
BROADCAST_DRIVER=ably
```

마지막으로, 클라이언트 측에서 브로드캐스트 이벤트를 수신할 수 있도록 [Laravel Echo](#client-side-installation)를 설치 및 설정하면 됩니다.

<a name="open-source-alternatives"></a>
### 오픈 소스 대안

<a name="open-source-alternatives-php"></a>
#### PHP

[laravel-websockets](https://github.com/beyondcode/laravel-websockets) 패키지는 순수 PHP로 구현된, Pusher와 호환되는 WebSocket 서버입니다. 상업용 WebSocket 서비스 없이도 Laravel 브로드캐스팅을 사용할 수 있습니다. 자세한 설치 및 사용법은 [공식 문서](https://beyondco.de/docs/laravel-websockets)를 참조하세요.

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반의, Pusher와 호환되는 WebSocket 서버입니다. 내부적으로 µWebSockets.js를 통해 매우 뛰어난 확장성과 속도를 자랑합니다. 이 패키지를 활용해 상업용 WebSocket 서비스 없이도 Laravel 브로드캐스팅을 사용할 수 있습니다. 자세한 내용은 [공식 문서](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스트 드라이버로부터 브로드캐스트되는 이벤트에 채널 구독 및 리스닝을 쉽게 할 수 있도록 도와주는 자바스크립트 라이브러리입니다. Echo는 NPM으로 설치할 수 있습니다. 아래 예시에서는 `pusher-js`도 함께 설치하는데, 이는 Pusher Channels 브로드캐스터 사용을 위한 것입니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo를 설치한 후, `resources/js/bootstrap.js` 파일 하단에 Echo 인스턴스를 새로 생성하세요. 기본적으로 이 파일에는 Echo 예제 설정이 주석 처리되어 있습니다. 주석을 해제해서 사용하면 됩니다:

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

설정을 주석 해제 및 필요에 따라 수정한 후, 애플리케이션의 자바스크립트 에셋을 컴파일합니다:

```shell
npm run dev
```

> **참고**  
> 자바스크립트 에셋 컴파일에 대한 더 자세한 정보는 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 사전 구성된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo에 `client` 옵션으로 전달할 수 있습니다:

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

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스트 드라이버로부터 이벤트를 구독하고 리스닝할 수 있는 자바스크립트 라이브러리입니다. Echo는 NPM으로 설치할 수 있으며, 이 예제 역시 `pusher-js`를 같이 설치하게 됩니다.

비록 Ably를 사용하더라도, Ably가 Pusher 호환 모드를 지원하기 때문에 `pusher-js` 패키지를 사용하여 클라이언트에서 동일한 방식으로 이벤트를 수신할 수 있습니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**이전에, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 반드시 활성화해야 합니다. 이는 Ably 애플리케이션 대시보드의 'Protocol Adapter Settings'에서 설정할 수 있습니다.**

Echo가 설치되었다면, 라라벨 프레임워크에서 제공하는 `resources/js/bootstrap.js` 파일 하단에 Echo 인스턴스를 생성하세요. 아래는 Ably에 맞춘 설정 예시입니다:

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

여기서 `VITE_ABLY_PUBLIC_KEY` 환경 변수 값은 Ably의 public key로, 콜론(`:`) 앞의 부분만 사용해야 합니다.

설정을 주석 해제 및 필요에 따라 수정한 후, 애플리케이션의 자바스크립트 에셋을 컴파일합니다:

```shell
npm run dev
```

> **참고**  
> 자바스크립트 에셋 컴파일에 대한 더 자세한 정보는 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel의 이벤트 브로드캐스팅은 드라이버 방식의 WebSocket을 사용해 서버 측의 Laravel 이벤트를 클라이언트(자바스크립트) 애플리케이션으로 전송할 수 있게 합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 지원합니다. 이 이벤트들은 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 이용해 쉽게 클라이언트에서 처리할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트 되며, 공개 채널 또는 비공개 채널로 지정할 수 있습니다. 공개 채널은 누구나 인증/권한 없이 구독할 수 있지만, 비공개 채널은 인증/권한 승인이 필요합니다.

> **참고**  
> Pusher의 오픈 소스 대안을 원한다면, [오픈 소스 대안](#open-source-alternatives)을 참고하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

각 컴포넌트 설명에 앞서, 전자상거래 스토어 예제를 통해 브로드캐스팅 흐름을 간단히 살펴보겠습니다.

예를 들어, 사용자가 자신의 주문 배송 상태를 확인할 수 있는 페이지가 있다고 가정합시다. 배송 상태가 변경될 때 `OrderShipmentStatusUpdated` 이벤트가 발생합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문을 보고 있을 때, 상태 업데이트를 확인하기 위해 페이지 새로고침을 하게 하고 싶지 않습니다. 새로운 상태가 생성될 때마다 자동으로 갱신되게 하려면, `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 그러면 이벤트가 발생할 때 자동으로 브로드캐스트됩니다.

```php
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
     * 주문 인스턴스
     *
     * @var \App\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스를 구현하면 반드시 `broadcastOn` 메서드를 구현해야 합니다. 이 메서드는 이벤트가 브로드캐스트될 채널(들)을 반환합니다. 이 예시에서는 주문의 소유자만 상태 업데이트를 볼 수 있어야 하므로, 해당 주문에 연결된 비공개 채널로 브로드캐스트합니다.

```php
/**
 * 이 이벤트가 브로드캐스트될 채널을 반환합니다.
 *
 * @return \Illuminate\Broadcasting\PrivateChannel
 */
public function broadcastOn()
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

<a name="example-application-authorizing-channels"></a>
#### 채널 인증

비공개 채널은 사용자가 채널을 수신할 권한이 있는지 인증이 필요합니다. 인증 로직은 `routes/channels.php` 파일에서 정의할 수 있습니다. 예를 들어, `orders.1` 같은 비공개 채널에 접근하려는 사용자가 실제로 해당 주문의 소유자인지 확인합니다:

```php
use App\Models\Order;

Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인자를 받습니다: 채널 이름과, 사용자가 채널을 구독할 수 있는지 `true` 또는 `false`를 반환하는 콜백입니다.

모든 인증 콜백은 첫 번째 인수로 현재 인증된 사용자 객체를 받고, 이후 와일드카드 파라미터들을 순서대로 받습니다. 이 예시에서 `{orderId}`는 채널 이름의 ID 부분이 와일드카드임을 의미합니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스팅 수신

마지막 단계는 자바스크립트 애플리케이션에서 이벤트를 수신하는 것입니다. [Laravel Echo](#client-side-installation)를 이용해 `private` 메서드로 비공개 채널에 구독하고, `listen` 메서드로 이벤트를 수신합니다. 이벤트의 public 프로퍼티가 모두 브로드캐스트 데이터에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

특정 이벤트를 브로드캐스트하려면, 이벤트 클래스에서 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 `broadcastOn` 메서드 하나만 구현하면 됩니다. 이 메서드는 이벤트가 브로드캐스트될 채널(배열)을 반환해야 합니다. 채널 객체는 `Channel`, `PrivateChannel`, `PresenceChannel` 중 하나로 인스턴스화됩니다.

```php
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
     * 이 이벤트가 브로드캐스트될 채널을 반환합니다.
     *
     * @return Channel|array
     */
    public function broadcastOn()
    {
        return new PrivateChannel('user.'.$this->user->id);
    }
}
```

이제 이벤트를 일반적으로 [발행](/docs/{{version}}/events)만 하면, [큐 작업](/docs/{{version}}/queues)로 지정한 브로드캐스트 드라이버를 통해 자동으로 브로드캐스트됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스명을 브로드캐스트 이름으로 사용합니다. 브로드캐스트 이름을 커스터마이징하려면 `broadcastAs` 메서드를 정의하면 됩니다.

```php
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

`broadcastAs`로 커스텀 이름을 설정했다면, 이벤트 리스너에 반드시 앞에 `.`을 붙여서 등록해야 Echo가 네임스페이스를 덧붙이지 않습니다:

```js
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트되면 이벤트의 `public` 프로퍼티가 모두 자동으로 직렬화되어 페이로드로 전송됩니다. 예를 들어, public `$user` 프로퍼티가 Eloquent 모델이라면, 브로드캐스트 페이로드는 다음과 같습니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

브로드캐스트 페이로드를 더욱 세밀하게 제어하려면, `broadcastWith` 메서드를 이벤트에 추가하여 직접 데이터 배열을 반환할 수 있습니다:

```php
/**
 * 브로드캐스트할 데이터 반환
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

브로드캐스트 이벤트는 기본적으로 `queue.php` 설정 파일의 기본 커넥션 및 기본 큐에 할당됩니다. 이벤트 클래스에서 `connection` 및 `queue` 프로퍼티를 정의하여 커넥션 및 큐를 변경할 수 있습니다:

```php
/**
 * 브로드캐스트 시 사용할 큐 커넥션 이름
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스트 작업을 할당할 큐 이름
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드로 큐 이름만 커스터마이징할 수 있습니다:

```php
/**
 * 브로드캐스트 작업을 할당할 큐 이름
 *
 * @return string
 */
public function broadcastQueue()
{
    return 'default';
}
```

이벤트를 기본 드라이버 대신 `sync` 큐로 브로드캐스트하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다:

```php
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    //
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건에서만 이벤트를 브로드캐스트하고자 한다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하면 됩니다:

```php
/**
 * 이벤트가 브로드캐스트될지 결정
 *
 * @return bool
 */
public function broadcastWhen()
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅 & 데이터베이스 트랜잭션

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내부에서 디스패치될 경우, 큐가 트랜잭션 커밋 전에 해당 작업을 처리할 수 있습니다. 이 경우 데이터베이스 트랜잭션 내의 모델 변경사항이 아직 DB에 반영되지 않았거나, 모델이 실제로 DB에 존재하지 않을 수 있어서 문제가 생길 수 있습니다.

큐 커넥션의 `after_commit` 옵션이 `false`라면, 이벤트 클래스에 `$afterCommit` 프로퍼티를 추가해 트랜잭션이 모두 완료된 뒤 발행되도록 할 수 있습니다:

```php
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

> **참고**  
> 이러한 문제의 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인증

비공개 채널은 현재 인증된 사용자가 해당 채널을 수신할 권한이 있는지 검증해야 합니다. 채널 이름과 함께 HTTP 요청을 Laravel 애플리케이션에 보내고, 애플리케이션이 사용자의 수신 권한을 판별합니다. [Laravel Echo](#client-side-installation)를 사용하면, 이 HTTP 요청은 자동으로 이루어집니다. 하지만 인증 요청을 처리할 올바른 라우트는 반드시 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 인증 라우트 정의

Laravel에서는 채널 인증 요청을 처리하는 라우트 정의가 매우 쉽습니다. `App\Providers\BroadcastServiceProvider`에서 `Broadcast::routes` 메서드를 볼 수 있습니다. 이 메서드는 `/broadcasting/auth` 라우트를 등록하여 인증 요청을 처리합니다.

```php
Broadcast::routes();
```

`Broadcast::routes`는 자동으로 `web` 미들웨어 그룹에 라우트를 추가합니다. 필요하면 배열로 원하는 라우트 속성을 넘겨서 커스터마이징할 수도 있습니다:

```php
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>
#### 인증 엔드포인트 커스터마이징

기본적으로 Echo는 `/broadcasting/auth` 엔드포인트를 통해 채널 접근 인증을 진행합니다. 직접 엔드포인트 경로를 지정하려면 Echo 생성 시 `authEndpoint` 옵션을 사용하세요:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 인증 요청 커스터마이징

Laravel Echo의 인증 요청 개인화가 필요하다면, Echo 생성 시 커스텀 authorizer를 제공할 수 있습니다:

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
### 인증 콜백 정의

인증된 사용자가 특정 채널을 들을 수 있는지 실제로 판별하는 로직을 작성해야 합니다. 이 로직은 애플리케이션의 `routes/channels.php` 파일에 정의합니다. `Broadcast::channel` 메서드로 인증 콜백을 등록합니다:

```php
Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

각 인증 콜백의 첫 번째 인자는 현재 인증된 사용자 객체이고, 나머지 인자는 와일드카드로 받은 파라미터들입니다. 예를 들어 `{orderId}`는 채널 이름에 따라 변하는 부분입니다.

<a name="authorization-callback-model-binding"></a>
#### 인증 콜백 모델 바인딩

HTTP 라우트처럼, 채널 라우트도 암시적/명시적 [모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어, 문자열/숫자 대신 실제 `Order` 모델 인스턴스를 받을 수 있습니다:

```php
use App\Models\Order;

Broadcast::channel('orders.{order}', function ($user, Order $order) {
    return $user->id === $order->user_id;
});
```

> **경고**  
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [암시적 모델 바인딩 범위지정](/docs/{{version}}/routing#implicit-model-binding-scoping)를 지원하지 않습니다. 대부분의 경우 단일 모델의 고유 기본키로 충분하므로 문제되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 인증 콜백의 인증

비공개 및 presence 브로드캐스트 채널은 애플리케이션의 기본 인증 가드로 사용자를 인증합니다. 인증이 안 된 사용자는 콜백이 실행되지 않고, 채널 구독이 거부됩니다. 필요하다면 여러 개의 커스텀 가드를 지정할 수도 있습니다:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션에서 채널이 많아지면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 이럴 경우 클로저 대신 채널 클래스를 사용할 수 있습니다. `make:channel` Artisan 명령어로 클래스를 생성할 수 있으며, `App/Broadcasting` 디렉터리에 생성됩니다.

```shell
php artisan make:channel OrderChannel
```

생성한 채널 클래스를 `routes/channels.php`에서 등록하세요:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스를 사용해 인증 로직은 `join` 메서드에서 구현하며, 채널 모델 바인딩도 활용 가능합니다:

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * 새 채널 인스턴스 생성
     */
    public function __construct()
    {
        //
    }

    /**
     * 사용자의 채널 접근 인증
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

> **참고**  
> Laravel의 다른 클래스들처럼, 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)에서 자동으로 주입됩니다. 생성자에서 필요한 의존성을 타입힌트로 받을 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현했다면, 평소처럼 이벤트의 dispatch 메서드를 호출하면 됩니다. 이벤트 dispatcher가 `ShouldBroadcast` 인터페이스를 감지하고 자동으로 해당 드라이버를 통해 브로드캐스트 작업을 큐에 넣습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스팅

간혹, 현재 사용자 외 모든 구독자에게만 이벤트를 브로드캐스트해야 할 수 있습니다. 이때는 `broadcast` 헬퍼와 `toOthers` 메서드를 사용할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어 할 일 목록 앱에서, 사용자가 새 할 일을 작성하면 `/task` URL로 요청을 보내고 생성된 태스크 정보를 JSON으로 받아온 뒤 클라이언트에서 목록에 직접 추가할 수 있습니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

동시에 할 일 생성 시 이벤트도 브로드캐스트한다면, 이벤트를 수신하는 클라이언트가 중복으로 항목을 추가할 수 있습니다. 이 경우 `toOthers`를 활용해 현재 사용자에게는 브로드캐스트하지 않도록 할 수 있습니다.

> **경고**  
> `toOthers` 메서드를 사용하려면, 이벤트 클래스에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 포함되어 있어야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스가 초기화되면 소켓 ID가 연결에 할당됩니다. Axios와 같이 글로벌 HTTP 클라이언트를 사용하면 소켓 ID가 자동으로 `X-Socket-ID` 헤더로 모든 요청에 첨부됩니다. `toOthers` 호출 시 Laravel은 이 헤더의 소켓 ID를 추출해 해당 소켓 ID로는 브로드캐스트하지 않습니다.

글로벌 Axios를 사용하지 않는 경우, 자바스크립트 애플리케이션에서 수동으로 `X-Socket-ID` 헤더를 모든 요청에 추가해야 합니다. 소켓 ID는 `Echo.socketId()`에서 가져올 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 브로드캐스트 커넥션 커스터마이징

여러 브로드캐스트 커넥션을 사용하는 애플리케이션에서, 기본 커넥션이 아닌 특정 브로드캐스터로 이벤트를 보낼 때 `via` 메서드를 사용할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 생성자에서 `broadcastVia` 메서드로 커넥션을 직접 지정할 수 있습니다. 그 전에, 클래스에 `InteractsWithBroadcasting` 트레이트가 포함되어야 합니다:

```php
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
     * 새 이벤트 인스턴스 생성
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
### 이벤트 리스닝

[Laravel Echo 설치 및 인스턴스 생성](#client-side-installation)이 완료되었다면, 채널 인스턴스를 받아 `listen` 메서드로 특정 이벤트를 수신할 수 있습니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널에서 이벤트를 수신하려면 `private` 메서드를 사용하십시오. 하나의 채널에서 여러 이벤트를 리스닝하기 위해 `listen` 메서드를 연이어 호출할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중단

채널을 [나가지 않고](#leaving-a-channel) 특정 이벤트 수신만 중단하려면 `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 나가려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널 뿐만 아니라 관련된 private/presence 채널도 모두 나가려면 `leave` 메서드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예시처럼 이벤트 클래스의 전체 네임스페이스를 지정하지 않아도 됩니다. Echo가 기본적으로 `App\Events` 네임스페이스를 사용하기 때문입니다. Echo 인스턴스를 생성할 때 `namespace` 옵션으로 루트 네임스페이스를 직접 지정할 수도 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 `.이벤트전체접근경로`와 같이 앞에 점(`.`)을 붙여 Echo에서 구독할 때 명시해도 됩니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        //
    });
```

<a name="presence-channels"></a>
## Presence 채널

Presence 채널은 비공개 채널의 보안성 위에, 채널에 접속 중인 사용자가 누군지를 추가로 파악할 수 있는 기능을 제공합니다. 이를 활용해 예를 들어 채팅방의 접속자 리스트 노출, 여러 사용자가 같은 페이지를 실시간으로 보고 있다는 알림 등, 강력하고 협업적인 기능을 손쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### Presence 채널 인증

Presence 채널은 비공개 채널이므로 [인증이 필요합니다](#authorizing-channels). 단, 해당 채널 인증 콜백에서 사용자 데이터 배열을 반환해야 하며, 그래야 자바스크립트에서 presence 채널의 리스너에서 사용자 정보를 활용할 수 있습니다. 사용자가 채널에 접속할 수 없는 경우에는 `false` 또는 `null`을 반환하세요.

```php
Broadcast::channel('chat.{roomId}', function ($user, $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### Presence 채널 가입

Presence 채널에 가입하려면 Echo의 `join` 메서드를 사용합니다. `join`은 `PresenceChannel` 인스턴스를 반환하며, `here`, `joining`, `leaving` 이벤트를 구독할 수 있습니다.

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

- `here` 콜백은 채널 가입 직후, 이미 참여 중인 모든 사용자의 정보를 배열로 전달합니다.
- `joining`은 새로운 사용자가 채널에 들어올 때 실행됩니다.
- `leaving`은 사용자가 채널을 떠날 때 실행됩니다.
- `error`는 인증 실패 등 오류 시에 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### Presence 채널로 브로드캐스팅

Presence 채널에도 일반 채널처럼 이벤트를 브로드캐스팅할 수 있습니다. 예를 들어, 채팅방에서 새 메시지(`NewMessage`) 이벤트를 presence 채널로 브로드캐스트하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다:

```php
/**
 * 이 이벤트가 브로드캐스트될 채널 반환
 *
 * @return Channel|array
 */
public function broadcastOn()
{
    return new PresenceChannel('room.'.$this->message->room_id);
}
```

역시나, 현재 사용자를 제외하고 브로드캐스트하려면 `broadcast` 헬퍼와 `toOthers` 메서드를 사용할 수 있습니다:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Presence 채널로 전송된 이벤트도 Echo의 `listen` 메서드로 수신할 수 있습니다:

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

> **경고**  
> 모델 브로드캐스팅 문서 읽기 전에, 라라벨의 일반적인 모델 브로드캐스팅 서비스와 수동 이벤트 브로드캐스트 및 리스닝 방식을 먼저 숙지하는 것이 좋습니다.

애플리케이션에서 [Eloquent 모델](/docs/{{version}}/eloquent)가 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스팅하는 것이 일반적입니다. 물론 각각의 상태 변화에 맞는 커스텀 이벤트를 만들어 `ShouldBroadcast`를 붙여 처리할 수도 있습니다.

하지만 별도의 다른 용도가 아닌 오직 브로드캐스팅만을 위해 이벤트 클래스를 만드는 것은 번거로울 수 있습니다. 이를 해결하기 위해, Laravel에서는 Eloquent 모델이 자체적으로 상태 변화를 자동으로 브로드캐스트하도록 할 수 있습니다.

시작하려면, 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용하세요. 그리고 브로드캐스트 대상 채널 배열을 반환하는 `broadcastOn` 메서드를 정의합니다:

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
     * 게시글에 속한 사용자
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트를 브로드캐스트할 채널 배열 반환.
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

이제 이 트레이트와 메서드를 추가하면, 해당 모델 인스턴스가 생성/수정/삭제/임시삭제/복구될 때마다 자동으로 브로드캐스팅됩니다.

직접 구현한 `broadcastOn` 메서드는 `$event` 인자를 받는데, 이 인자는 모델에 발생한 이벤트 타입(`created`, `updated`, `deleted`, `trashed`, `restored`)입니다. 조건에 따라 특정 이벤트만 브로드캐스트하도록 커스터마이징이 가능합니다:

```php
/**
 * 모델 이벤트를 브로드캐스트할 채널 반환
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

라라벨이 내부적으로 생성하는 모델 브로드캐스트 이벤트의 동작을 커스터마이징하고 싶다면, `newBroadcastableEvent` 메서드를 모델에 정의하세요. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델의 새 브로드캐스트 이벤트 생성
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
### 모델 브로드캐스팅 컨벤션

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 컨벤션

위 예시에서 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않고, Eloquent 모델 인스턴스 자체를 반환했습니다. 모델 인스턴스가 반환될 경우, Laravel은 해당 모델의 클래스명과 PK로 이름이 정해진 프라이빗 채널을 자동으로 생성합니다.

예를 들어, `App\Models\User` 모델의 `id`가 1이라면 채널 이름은 `App.Models.User.1`이 됩니다. 물론 원한다면 `broadcastOn`에서 직접 `Channel` 인스턴스를 반환하여 채널 이름을 완전히 제어할 수 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

public function broadcastOn($event)
{
    return [new PrivateChannel('user.'.$this->id)];
}
```

또는 채널 생성자에 모델 인스턴스를 넘겨도 자동 변환됩니다:

```php
return [new Channel($this->user)];
```

모델의 채널 이름을 알아내고 싶다면, 모델 인스턴스에서 `broadcastChannel` 메서드를 호출하면 됩니다. 예를 들어, `App\Models\User`의 `id`가 1이면 `App.Models.User.1`이 반환됩니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 컨벤션

모델 브로드캐스트 이벤트는 실제 애플리케이션 `App\Events` 디렉토리에 이벤트가 없으므로, 이름과 페이로드는 컨벤션에 따릅니다. 기본적으로 이벤트 이름은 모델 클래스명(네임스페이스 제외)과 발생한 모델 이벤트 이름이 조합됩니다.

따라서 `App\Models\Post` 모델의 업데이트는 `PostUpdated` 이벤트로 브로드캐스트되며, 페이로드는 다음과 같습니다:

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

마찬가지로, `App\Models\User` 모델 삭제는 `UserDeleted`라는 이벤트 이름으로 브로드캐스트됩니다.

필요하다면 모델에 `broadcastAs` 및 `broadcastWith` 메서드를 정의해 이벤트별 이름과 페이로드를 커스터마이징할 수 있습니다. `broadcastAs`에서 `null`을 반환하면, 앞서 설명한 컨벤션이 그대로 적용됩니다:

```php
/**
 * 모델 이벤트의 브로드캐스트 이름
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

모델에 `BroadcastsEvents` 트레이트와 `broadcastOn` 메서드를 추가했다면, 이제 클라이언트 애플리케이션에서 해당 모델 이벤트를 수신할 수 있습니다. 자세한 내용은 [이벤트 리스닝](#listening-for-events) 문서를 참고하시기 바랍니다.

우선, 채널 이름은 [모델 브로드캐스팅 컨벤션](#model-broadcasting-conventions)을 따라야 하므로, `private` 메서드로 채널을 가져옵니다. 그리고 `listen` 메서드로 특정 이벤트를 수신합니다. 이때, 실제 `App\Events` 아래에 이벤트 클래스가 없으므로, [이벤트 이름](#model-broadcasting-event-conventions) 앞에 `.`을 붙여 네임스페이스가 없음을 표시해야 합니다. 각 모델 브로드캐스트 이벤트의 페이로드는 해당 모델의 모든 브로드캐스트 데이터(`model`)를 포함합니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> **참고**  
> [Pusher Channels](https://pusher.com/channels) 사용 시, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

별도의 서버 통신 없이, 클라이언트 간에만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. "입력 중" 알림 등, 서버에 요청을 보내지 않아도 되는 실시간 상호작용에 유용합니다.

클라이언트 이벤트 브로드캐스트는 Echo의 `whisper` 메서드를 이용합니다:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트 수신은 `listenForWhisper` 메서드로 처리합니다:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림(Notifications)

이벤트 브로드캐스팅을 [알림](/docs/{{version}}/notifications)과 조합하면, 사용자가 페이지를 새로 고침하지 않아도 새로운 알림을 실시간으로 받을 수 있습니다. 먼저 [브로드캐스트 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 설정을 참고하세요.

알림을 broadcast 채널로 설정하면, Echo의 `notification` 메서드로 브로드캐스트 알림을 청취할 수 있습니다. 이때 채널 이름은 알림을 받는 엔티티의 클래스명과 일치해야 합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

이 예시에서는, `broadcast` 채널로 `App\Models\User` 인스턴스에게 전송된 모든 알림이 콜백으로 전달됩니다. `App.Models.User.{id}` 채널용 알림 인증 콜백이 기본 `BroadcastServiceProvider`에 포함되어 있습니다.