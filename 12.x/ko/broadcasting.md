# 브로드캐스팅(Broadcasting)

- [소개](#introduction)
- [서버 측 설치](#server-side-installation)
    - [설정](#configuration)
    - [리버브(Reverb)](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 측 설치](#client-side-installation)
    - [리버브](#client-reverb)
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
    - [권한 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스트](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널에서 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프리젠스 채널](#presence-channels)
    - [프리젠스 채널 권한 부여](#authorizing-presence-channels)
    - [프리젠스 채널 참여](#joining-presence-channels)
    - [프리젠스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notification)](#notifications)

<a name="introduction"></a>
## 소개

많은 현대 웹 애플리케이션에서는 실시간으로 UI를 업데이트하기 위해 WebSocket을 사용합니다. 서버의 데이터가 업데이트될 때, 보통 WebSocket 연결을 통해 메시지가 클라이언트로 전송되어, UI에 반영됩니다. WebSocket은 데이터 변경 시마다 서버에 폴링하는 것보다 훨씬 효율적인 방법을 제공합니다.

예를 들어, 여러분의 애플리케이션에서 사용자의 데이터를 CSV 파일로 내보내고 이메일로 발송한다고 가정해봅시다. 하지만 CSV 파일 생성에 수 분이 걸리기 때문에 이를 [큐 작업](/docs/{{version}}/queues)으로 처리할 수 있습니다. CSV가 생성되어 사용자의 이메일로 발송되면, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 자바스크립트에서 수신할 수 있습니다. 이벤트가 수신되면, 사용자가 페이지를 새로고침하지 않아도 CSV가 이메일로 발송되었음을 안내하는 메시지를 보여줄 수 있습니다.

이러한 기능 구현을 돕기 위해, 라라벨은 서버 사이드 [이벤트](/docs/{{version}}/events)를 WebSocket으로 쉽게 "브로드캐스트"할 수 있도록 지원합니다. 라라벨 이벤트를 브로드캐스트하면 동일한 이벤트 이름과 데이터를 서버와 클라이언트(자바스크립트) 모두에서 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 단순합니다. 클라이언트는 프론트엔드에서 네임드 채널에 연결하고, 라라벨 서버는 백엔드에서 이 채널들로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에서 사용할 수 있는 데이터도 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 라라벨은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에, [이벤트 및 리스너](/docs/{{version}}/events)에 관한 공식 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 측 설치

라라벨 이벤트 브로드캐스팅을 사용하려면 몇 가지 설정과 패키지 설치가 필요합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스트 드라이버가 라라벨 이벤트를 브라우저에서 라라벨 에코(Echo, 자바스크립트 라이브러리)로 수신할 수 있도록 브로드캐스트하는 방식으로 작동합니다. 걱정하지 마세요. 각 단계별로 설치 과정을 안내해드립니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 설정 파일에 저장됩니다. 만약 이 파일이 없다면, `install:broadcasting` 아티즌 명령어로 생성됩니다.

라라벨은 기본적으로 [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 로컬 개발 및 디버깅에 사용할 수 있는 `log` 드라이버, 그리고 테스트 시 브로드캐스트를 비활성화하는 `null` 드라이버를 지원합니다. 각 드라이버의 설정 예제는 `config/broadcasting.php` 파일에 포함되어 있습니다.

<a name="installation"></a>
#### 설치

신규 라라벨 애플리케이션에서는 브로드캐스팅이 기본적으로 비활성화되어 있습니다. 다음 아티즌 명령어로 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 `config/broadcasting.php` 설정 파일을 생성합니다. 또한, 애플리케이션의 브로드캐스트 권한(authorization) 라우트 및 콜백을 등록할 수 있는 `routes/channels.php` 파일도 생성됩니다.

<a name="queue-configuration"></a>
#### 큐 설정

이벤트를 브로드캐스트하기 전에, 먼저 [큐 워커](/docs/{{version}}/queues)를 설정 및 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업으로 처리되어, 브로드캐스팅으로 인해 애플리케이션의 응답 속도가 느려지지 않습니다.

<a name="reverb"></a>
### 리버브(Reverb)

`install:broadcasting` 명령어를 실행하면 [Laravel Reverb](/docs/{{version}}/reverb) 설치 여부를 묻는 메시지가 표시됩니다. Composer 패키지 관리자를 사용해 Reverb를 직접 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치 후 Reverb의 설치 명령어를 실행하여, 설정을 게시하고, 필요한 환경변수를 추가하며, 이벤트 브로드캐스팅을 활성화하세요.

```shell
php artisan reverb:install
```

자세한 설치 및 사용법은 [Reverb 문서](/docs/{{version}}/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)로 이벤트를 브로드캐스트하려면, 다음 Composer 명령어로 PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

이제 `config/broadcasting.php` 설정 파일에서 Pusher 인증 정보를 입력하세요. 예제 값이 파일에 미리 포함되어 있어, key, secret, app ID만 지정하면 됩니다. 일반적으로 .env 파일에서 아래처럼 설정합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에서는 클러스터와 같은 추가 옵션도 지정할 수 있습니다.

또한, `.env` 파일에서 `BROADCAST_CONNECTION` 환경변수를 `pusher`로 설정하세요.

```ini
BROADCAST_CONNECTION=pusher
```

마지막으로, [Laravel Echo](#client-side-installation)를 설치 및 설정하면, 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 Ably의 "Pusher 호환" 모드 사용 방법을 설명합니다. Ably 팀이 추천하는 공식 브로드캐스터 및 Echo 클라이언트가 별도로 있으니, [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)도 참고하세요.

[Ably](https://ably.com)로 이벤트를 브로드캐스트하려면 Composer로 Ably PHP SDK를 설치하세요.

```shell
composer require ably/ably-php
```

이어, `config/broadcasting.php` 파일에서 Ably 인증키를 설정합니다. 일반적으로 다음과 같이 `.env` 파일에 값을 지정합니다.

```ini
ABLY_KEY=your-ably-key
```

그리고 `.env`에서 `BROADCAST_CONNECTION` 환경변수를 `ably`로 설정하세요.

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo](#client-side-installation)를 설치 및 설정하면 클라이언트에서 브로드캐스트 이벤트를 수신할 준비가 됩니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-reverb"></a>
### 리버브

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 브로드캐스트하는 이벤트를 클라이언트(브라우저)에서 손쉽게 수신할 수 있도록 하는 자바스크립트 라이브러리입니다. NPM을 통해 Echo를 설치할 수 있습니다. Reverb는 WebSocket 구독 및 메시지 전송에 Pusher 프로토콜을 사용하므로, `pusher-js` 패키지도 함께 설치합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치가 완료되면, 애플리케이션의 JS 코드(예: `resources/js/bootstrap.js`)에서 Echo 인스턴스를 생성합니다. 기본적으로 예제 Echo 설정이 포함되어 있는데, 주석을 해제하고 `broadcaster` 옵션을 `reverb`로 변경하세요.

```js
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

그 다음, 애플리케이션 자산을 빌드합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터 사용 시, laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

Echo와 `pusher-js` 설치는 `install:broadcasting` 아티즌 명령어로 자동 설치됩니다. 직접 설치하려면 다음 NPM 명령어를 사용하세요.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치 뒤, JS에서 Echo 인스턴스를 생성합니다. 기본 생성된 `resources/js/echo.js`는 Reverb 설정입니다. 아래 설정으로 Pusher용으로 바꿀 수 있습니다.

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

`.env` 파일에 필요한 Pusher 환경변수를 정의하세요.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

설정이 끝나면 자산을 빌드하세요.

```shell
npm run build
```

> [!NOTE]
> 자바스크립트 자산 빌드에 대한 자세한 내용은 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

미리 구성된 Pusher Channels 클라이언트 인스턴스를 Echo가 사용하도록 하려면 `client` 옵션으로 전달할 수 있습니다.

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
> 아래 문서는 Ably의 "Pusher 호환" 모드 사용 방법을 설명합니다. Ably가 유지/관리하는 브로드캐스터 및 Echo 클라이언트 사용에 대한 안내는 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참조하세요.

Echo와 `pusher-js` 패키지는 명령어로 자동 설치됩니다. 직접 설치도 가능합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에, Ably 대시보드에서 "Protocol Adapter Settings"을 통해 Pusher 프로토콜 지원을 활성화해야 합니다.**

Echo 설치 후, JS에서 아래와 같이 Echo 인스턴스를 생성하여 Ably에 연결할 수 있습니다.

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

Ably Echo 설정에서 사용되는 `VITE_ABLY_PUBLIC_KEY`는 Ably의 공개키(키의 앞부분, 즉 ':' 앞의 부분)여야 합니다.

설정 후 자산을 빌드하세요.

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 자산 빌드에 대한 자세한 내용은 [Vite](/docs/{{version}}/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

라라벨의 이벤트 브로드캐스팅은 드라이버 기반으로 WebSocket을 통해 서버의 라라벨 이벤트를 프론트엔드 자바스크립트 애플리케이션으로 브로드캐스트합니다. 현재 라라벨은 [Pusher Channels](https://pusher.com/channels) 및 [Ably](https://ably.com) 드라이버를 내장하고 있으며, 클라이언트 측에서는 [Laravel Echo](#client-side-installation)로 쉽게 수신할 수 있습니다.

이벤트는 "채널"에서 브로드캐스트되며, 공개(public) 또는 프라이빗(private) 채널로 지정할 수 있습니다. 모든 방문자는 인증 및 권한 없이 공개 채널에 구독할 수 있지만, 프라이빗 채널을 구독하려면 해당 사용자가 인증되고 권한이 있어야 합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

각 컴포넌트 설명에 앞서, 전자상거래 스토어 예제에서의 흐름을 살펴봅시다.

사용자가 주문의 배송 상태를 볼 수 있는 페이지가 있다고 가정합시다. 주문 상태 업데이트가 처리되면 `OrderShipmentStatusUpdated` 이벤트가 발생합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 특정 주문을 보고 있을 때, 새로 고치지 않고도 상태 업데이트를 받을 수 있어야 합니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현하여, 이벤트가 발생할 때 자동으로 브로드캐스트되도록 합니다.

```php
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
```

`ShouldBroadcast` 인터페이스는 이벤트에 `broadcastOn` 메서드를 정의하도록 요구합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환해야 하며, 예제에서는 해당 주문의 작성자만 상태 업데이트를 볼 수 있도록 프라이빗 채널을 사용합니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트될 채널 반환
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

이벤트를 여러 채널로 브로드캐스트하려면 배열을 반환할 수 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트될 채널 반환
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
```

<a name="example-application-authorizing-channels"></a>
#### 채널 권한 부여

프라이빗 채널은 사용자가 해당 채널을 들을 수 있는지 권한을 검증해야 합니다. 아래는 `routes/channels.php` 파일에 권한 검증 규칙을 정의하는 예입니다. 예제에서는 `orders.1` 프라이빗 채널에 접근하려는 사용자가 해당 주문의 작성자인지 확인합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 가지 인자를 받습니다: 채널 이름과, 사용자의 권한을 반환하는 콜백(논리값).

모든 콜백은 현재 인증된 사용자, 그리고 와일드카드로 전달된 추가 인자를 받습니다. 예제에서는 `{orderId}` 플레이스홀더를 사용해 채널명 일부가 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 리스닝

브라우저 JS에서 이벤트를 리스닝하려면 [Laravel Echo](#client-side-installation)를 사용하면 됩니다. 먼저 프라이빗 채널에 `private` 메서드로 구독한 뒤, `listen`으로 해당 이벤트를 감지할 수 있습니다. 기본적으로 이벤트의 모든 public 프로퍼티가 브로드캐스트 페이로드에 포함됩니다.

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

라라벨이 특정 이벤트를 브로드캐스트하도록 하려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 자동으로 이벤트 클래스에 import되어 있어, 쉽게 사용할 수 있습니다.

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트를 브로드캐스트할 채널 또는 채널 배열을 반환해야 하며, 반환값은 `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스여야 합니다. `Channel`은 공개 채널, `PrivateChannel`과 `PresenceChannel`은 [채널 권한](#authorizing-channels)이 필요한 프라이빗 채널입니다.

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
     * 새로운 이벤트 인스턴스 생성
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 이벤트 브로드캐스트 채널 반환
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
```

`ShouldBroadcast` 인터페이스를 구현한 뒤에는, 이벤트를 [일반적인 방식](/docs/{{version}}/events)으로 발생시키면 됩니다. 이벤트가 발생되면, 자동으로 [큐 작업](/docs/{{version}}/queues)으로 처리되어 지정한 브로드캐스트 드라이버로 전송됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

라라벨은 기본적으로 이벤트 클래스명을 브로드캐스트 이름으로 사용합니다. 하지만 원하는 이름으로 변경하려면 이벤트에 `broadcastAs` 메서드를 추가하세요.

```php
/**
 * 이벤트의 브로드캐스트 이름 반환
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`로 브로드캐스트 이름을 커스터마이징할 경우, 리스너 등록 시 반드시 앞에 `.`(점) 문자를 붙여야 이름 앞에 네임스페이스가 붙지 않습니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, public 프로퍼티는 자동으로 직렬화되어 페이로드로 전송되므로, 자바스크립트에서 해당 데이터에 접근할 수 있습니다. 예를 들어, public `$user` 프로퍼티 하나만 있을 경우 다음과 같이 전달됩니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

더 정교하게 페이로드를 제어하길 원한다면 `broadcastWith` 메서드를 구현하세요.

```php
/**
 * 브로드캐스트할 데이터 반환
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
### 브로드캐스트 큐

기본적으로 각 브로드캐스트 이벤트는 `queue.php`에서 기본 큐 연결에 지정된 기본 큐에 할당됩니다. 이벤트 클래스에 `connection` 및 `queue` 프로퍼티를 정의해 큐 연결 및 이름을 커스터마이징 할 수 있습니다.

```php
/**
 * 브로드캐스트시 사용할 큐 연결명
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스터가 작업을 넣을 큐 이름
 *
 * @var string
 */
public $queue = 'default';
```

대신, `broadcastQueue` 메서드로 큐 이름만 커스터마이징할 수도 있습니다.

```php
/**
 * 브로드캐스트 작업 큐 이름 반환
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

이벤트를 기본 큐 드라이버 대신 `sync` 큐로 즉시 브로드캐스팅하고 싶으면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 사용하세요.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건이 성립할 때에만 이벤트를 브로드캐스트하고 싶을 때는 `broadcastWhen` 메서드를 활용할 수 있습니다.

```php
/**
 * 이 이벤트를 브로드캐스트할지 여부 반환
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 이벤트를 브로드캐스트할 때, 큐 작업이 데이터베이스 커밋 전에 실행될 수 있습니다. 이 경우 트랜잭션 내에서 생성·수정된 데이터가 아직 DB에 반영되지 않아, 브로드캐스트 시 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`이어도, 해당 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 모든 트랜잭션 커밋 후에 이벤트가 디스패치됩니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```

> [!NOTE]
> 이와 관련된 자세한 안내는 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여

프라이빗 채널은 인증된 사용자가 실제로 해당 채널을 들을 수 있는지 권한을 확인해야 합니다. 라라벨 애플리케이션에 HTTP 요청을 보내어 채널명에 대한 권한을 판단하며, [Laravel Echo](#client-side-installation)를 사용할 경우 이 과정을 자동으로 처리합니다.

브로드캐스팅 활성화 시, Laravel은 `/broadcasting/auth` 라우트를 자동으로 등록하고, 이 라우트는 `web` 미들웨어 그룹 내에 위치합니다.

<a name="defining-authorization-callbacks"></a>
### 권한 콜백 정의

현재 인증된 사용자가 채널을 들을 수 있는지 판단하는 로직은 `install:broadcasting` 명령어로 생성된 `routes/channels.php`에서 정의합니다. `Broadcast::channel` 메서드로 채널 권한 콜백을 등록하세요.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

모든 콜백은 현재 인증 사용자와 와일드카드 파라미터를 인자로 받습니다.

채널 권한 콜백 목록은 다음 명령어로 조회할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 권한 콜백 모델 바인딩

HTTP 라우트처럼 채널 라우트에서도 명시적·암시적 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)이 가능합니다. 아래처럼 사용하면, 일반 문자열이 아닌 `Order` 모델로 바인딩됩니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트와 다르게, 채널 모델 바인딩은 자동 [암시적 모델 바인딩 스코프](/docs/{{version}}/routing#implicit-model-binding-scoping)를 지원하지 않습니다. 그러나 대부분의 경우 단일 모델 기본키로 스코프를 정하므로 큰 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 권한 콜백 인증

프라이빗·프레즌스 채널은 기본 인증 가드로 사용자를 인증합니다. 인증에 실패한 경우 자동으로 권한이 거부되어 콜백이 실행되지 않습니다. 필요하다면 여러 가드로 인증 대상을 설정할 수도 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

다수의 채널을 사용하면 `routes/channels.php` 파일이 비대해질 수 있습니다. 이럴 때 콜백 대신 채널 클래스를 만들어 권한 부여를 할 수 있습니다. 다음 명령어로 클래스를 생성하세요.

```shell
php artisan make:channel OrderChannel
```

이후 `routes/channels.php`에서 채널을 등록합니다.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스의 `join` 메서드에 권한 로직을 작성합니다.

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * 채널 인스턴스 생성자
     */
    public function __construct() {}

    /**
     * 사용자의 채널 접근 인증
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> 다른 라라벨 클래스들처럼, 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)에서 자동으로 의존성 주입됩니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 마킹했다면, 이벤트를 디스패치하는 것만으로 브로드캐스터가 자동으로 큐에 해당 이벤트를 등록합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스트

한 채널의 모든 구독자 중 현재 사용자만 제외하고 메시지를 보낼 수도 있습니다. `broadcast` 헬퍼와 `toOthers` 메서드를 활용하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어 할 일 목록 앱에서 사용자가 작업을 등록하면 브로드캐스트와 동시에 바로 응답이 오므로, 클라이언트에서는 중복 작업이 추가될 수 있습니다. `toOthers`를 사용하면 이런 중복 문제를 방지할 수 있습니다.

> [!WARNING]
> 이벤트 클래스에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 포함되어 있어야 `toOthers` 메서드를 사용할 수 있습니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스가 초기화될 때 소켓 ID가 부여됩니다. 글로벌 [Axios](https://github.com/axios/axios) 인스턴스를 사용하는 경우 이 소켓 ID가 모든 요청 헤더(`X-Socket-ID`)에 자동으로 포함됩니다. `toOthers` 호출 시 이 소켓 ID를 기반으로 본인을 제외한 나머지 사용자에게만 이벤트를 브로드캐스트합니다.

글로벌 Axios를 사용하지 않는 경우, 모든 요청에 직접 `X-Socket-ID` 헤더를 추가해야 합니다. 소켓 ID는 다음으로 얻을 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

여러 브로드캐스트 커넥션을 사용할 때 특정 커넥션으로만 이벤트를 브로드캐스트하려면 `via` 메서드를 활용하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

이벤트 생성자 내부에서 `broadcastVia` 메서드로 지정할 수도 있습니다. 단, 이벤트 클래스에서 `InteractsWithBroadcasting` 트레이트를 사용해야 합니다.

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
     * 새로운 이벤트 인스턴스 생성
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### 익명 이벤트

별도의 이벤트 클래스를 만들지 않고 간단하게 이벤트를 프론트엔드에 브로드캐스트하려면 "익명 이벤트"를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 코드는 다음과 같은 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

이벤트 이름과 데이터는 `as`와 `with` 메서드로 커스터마이징할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

위 코드는 다음과 같이 브로드캐스트됩니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

프라이빗 또는 프리젠스 채널에서도 익명 이벤트를 보낼 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

익명 이벤트를 즉시 브로드캐스트하려면 `sendNow`를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증 사용자를 제외한 구독자에게만 브로드캐스트하려면 `toOthers`를 호출하세요.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo 설치 및 인스턴스 생성](#client-side-installation)을 마친 뒤, Echo로 브로드캐스트되는 이벤트를 리슨할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻고, 지정 이벤트명을 `listen`에 전달하세요.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

프라이빗 채널에서는 `private` 메서드를 사용하세요. `listen`을 체이닝하여 한 채널에서 여러 이벤트를 동시에 수신할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 특정 이벤트 리스닝 중지

채널을 떠나지 않고, 특정 이벤트 리스닝만 멈추려면 `stopListening` 메서드를 사용하세요.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널에서 나가기

채널을 떠나려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출합니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 관련된 프라이빗·프리젠스 채널도 모두 나가려면 `leave`를 사용하세요.

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예제들처럼 이벤트 클래스의 전체 네임스페이스를 지정하지 않아도 되는 이유는, Echo가 기본적으로 `App\Events`를 네임스페이스로 가정하기 때문입니다. 필요하다면 Echo 인스턴스 생성 시 `namespace` 옵션을 통해 변경할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 수신시 클래스 이름 앞에 `.`을 붙이면 항상 완전한 클래스 이름을 지정할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## 프리젠스 채널(Presence Channels)

프리젠스 채널은 프라이빗 채널의 보안성을 바탕으로, 해당 채널에 누가 구독중인지까지 알 수 있게 해줍니다. 이를 이용하면 같은 페이지를 보고 있는 사용자 안내, 채팅방 참여자 목록 등 강력한 협업 기능을 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프리젠스 채널 권한 부여

프리젠스 채널은 내부적으로 프라이빗 채널이므로 [프라이빗 채널 권한](#authorizing-channels) 검증이 필요합니다. 단, 이 경우 권한이 있으면 단순히 `true`를 반환하는 대신, 사용자 정보를 배열로 반환합니다.

콜백에서 반환한 정보는 자바스크립트에서 presence 채널 이벤트 리스너에 전달됩니다. 권한이 없으면 `false`나 `null`을 반환하세요.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프리젠스 채널 참여

Echo의 `join` 메서드로 프리젠스 채널에 참여할 수 있습니다. 이 메서드는 `PresenceChannel` 인스턴스를 반환하며, `listen` 외에도 `here`, `joining`, `leaving` 이벤트를 수신할 수 있습니다.

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

- `here` 콜백은 채널 참여 직후 한 번 실행되어 현재 구독중인 사용자 정보를 배열로 받습니다.
- `joining`은 새 사용자가 채널에 들어올 때,
- `leaving`은 사용자가 나갈 때 호출됩니다.
- `error`는 인증 endpoint에서 200 외의 HTTP 상태코드가 반환되거나 JSON 파싱 문제가 발생할 때 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프리젠스 채널로 브로드캐스팅

프리젠스 채널도 공개·프라이빗 채널처럼 이벤트를 수신할 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 presence 채널에 브로드캐스트 하려면, 이벤트의 `broadcastOn` 메서드에서 PresenceChannel을 반환하세요.

```php
/**
 * 이벤트 브로드캐스트 채널 반환
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```

다른 이벤트와 마찬가지로, `toOthers` 메서드로 본인에게는 이벤트를 브로드캐스트하지 않을 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Echo에서 presence 채널로 전송된 이벤트를 아래처럼 리슨할 수 있습니다.

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
## 모델 브로드캐스팅

> [!WARNING]
> 아래 문서를 읽기 전, 라라벨 모델 브로드캐스팅의 기본 개념 및 수동 이벤트/리스너 생성법을 숙지하시기 바랍니다.

보통 [Eloquent 모델](/docs/{{version}}/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하곤 합니다. 물론, 직접 [커스텀 이벤트](/docs/{{version}}/eloquent#events)를 정의하고 `ShouldBroadcast`로 마킹해 처리할 수 있습니다.

하지만 단순 브로드캐스트만 목적이라면, 별도의 이벤트 클래스 없이 모델 자체가 상태 변경을 자동으로 브로드캐스트하도록 지정할 수 있습니다.

Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하고, `broadcastOn` 메서드를 정의하면, 해당 모델의 이벤트가 방송됩니다.

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
     * 포스트 소유자 반환
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트 브로드캐스트 채널 반환
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이렇게 설정하면, 모델 인스턴스가 생성, 수정, 삭제, 트래시, 복원될 때 자동 브로드캐스트됩니다.

`broadcastOn`의 `$event` 인자는 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이를 참고해 이벤트별로 채널을 제어할 수 있습니다.

```php
/**
 * 모델 이벤트 브로드캐스트 채널 반환
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
#### 모델 브로드캐스팅 이벤트 생성 커스터마이징

간혹 라라벨이 생성하는 기본 모델 이벤트 대신, 맞춤 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이 경우 `newBroadcastableEvent` 메서드를 모델에 정의하여 반환값으로 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 리턴하면 됩니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 새로운 브로드캐스트 가능 모델 이벤트 생성
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### 모델 브로드캐스팅 규칙

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 명명 규칙

예제에서 보듯 `broadcastOn` 메서드는 Channel 인스턴스를 직접 반환하는 대신, Eloquent 모델 인스턴스를 반환할 수 있습니다. 라라벨은 모델의 클래스명과 기본키를 채널 이름으로 삼아 `PrivateChannel` 인스턴스를 만듭니다.

예를 들어, `App\Models\User`(id=1)은 `App.Models.User.1`이라는 채널명으로 변환됩니다. 물론 Channel 인스턴스를 직접 반환하여 채널 이름을 완전히 제어할 수도 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트 브로드캐스트 채널 반환
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

채널 생성자에 모델 인스턴스를 전달할 수도 있으며, 이 경우 채널명 규칙이 그대로 적용됩니다.

```php
return [new Channel($this->user)];
```

특정 모델의 채널명을 구하려면, `broadcastChannel` 메서드를 사용하세요.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 명명 규칙

모델 브로드캐스트 이벤트는 별도의 `App\Events` 내 클래스와 매핑되지 않으므로, conventio으로 이벤트 이름과 페이로드가 생성됩니다. 라라벨은 (1) 모델의 클래스명(네임스페이스 제외) (2) 발생 이벤트명을 결합해 방송합니다.

예를 들어, `App\Models\Post` 모델이 업데이트되면 `PostUpdated` 이벤트명이 되고, 페이로드는 다음과 같습니다.

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```

모델 삭제 시에는 `UserDeleted` 등으로 방송됩니다.

원한다면, `broadcastAs`와 `broadcastWith` 추가로 이벤트명과 페이로드를 커스터마이즈 할 수 있습니다. 두 메서드는 모델 이벤트 형태(예: 'created', 'updated')를 인자로 받습니다. `broadcastAs`에서 null을 반환하면 기본 규칙이 적용됩니다.

```php
/**
 * 모델 이벤트 브로드캐스트 이름
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델 브로드캐스트 데이터 반환
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
### 모델 브로드캐스트 리스닝

모델에 `BroadcastsEvents` 트레이트와 `broadcastOn` 메서드를 추가했다면, 클라이언트 측에서 바로 이벤트를 수신할 수 있습니다. 자세한 이벤트 리스닝 방법은 [리스닝 문서](#listening-for-events)를 참고하세요.

보통 Echo의 `private` 메서드로 채널 인스턴스를 얻고, `listen`으로 이벤트명을 등록합니다. 모델 브로드캐스트 이벤트는 별도의 이벤트 클래스가 없으므로, [이벤트명 표기 규칙](#model-broadcasting-event-conventions)에 따라 앞에 `.`을 붙여 네임스페이스에 종속되지 않음을 나타냅니다. 각 이벤트의 `model` 프로퍼티에는 방송 가능한 모델 정보가 포함되어 있습니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)을 사용할 경우, [대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 반드시 활성화해야 클라이언트 이벤트 송신이 가능합니다.

Laravel 애플리케이션을 거치지 않고, 연결된 클라이언트끼리 직접 이벤트를 송신할 때가 있습니다. 예를 들어, 채팅에서 "입력 중" 알림을 보내고 싶을 때, 클라이언트 이벤트를 사용할 수 있습니다.

Echo의 `whisper` 메서드로 클라이언트 이벤트를 보냅니다.

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트 리스닝은 `listenForWhisper`로 처리할 수 있습니다.

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림(Notification)

이벤트 브로드캐스팅을 [알림](/docs/{{version}}/notifications)과 결합하면, 사용자는 페이지를 새로 고침하지 않고도 실시간 알림을 받을 수 있습니다. 시작 전 [Broadcast 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 문서를 참고하세요.

알림이 브로드캐스트 채널을 사용하도록 설정했다면, Echo의 `notification` 메서드로 관련 이벤트를 수신할 수 있습니다. 여기서 채널명은 알림 수신 엔티티의 클래스명과 일치해야 합니다.

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

이 예시에서 브로드캐스트 채널을 통한 모든 `App\Models\User` 알림은 콜백에서 수신됩니다. 해당 채널에 대한 권한 콜백도 `routes/channels.php` 파일에 정의되어 있습니다.