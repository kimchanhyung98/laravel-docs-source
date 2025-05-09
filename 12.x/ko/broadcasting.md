# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [서버 사이드 설치](#server-side-installation)
    - [설정](#configuration)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 활용](#using-example-application)
- [브로드캐스트 이벤트 정의](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인가](#authorizing-channels)
    - [인가 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스트](#only-to-others)
    - [연결 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프리젠스 채널](#presence-channels)
    - [프리젠스 채널 인가](#authorizing-presence-channels)
    - [프리젠스 채널 가입](#joining-presence-channels)
    - [프리젠스 채널로 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notification)](#notifications)

<a name="introduction"></a>
## 소개

최신 웹 애플리케이션에서는 실시간으로 사용자 인터페이스를 업데이트하기 위해 WebSocket을 자주 활용합니다. 서버의 데이터가 변경될 때마다 메세지가 WebSocket 연결을 통해 클라이언트로 전송되어 브라우저에서 처리하게 됩니다. WebSocket은 UI에 반영할 데이터 변경을 확인하기 위해 서버에 반복적으로 요청을 보내는 것보다 훨씬 효율적인 대안입니다.

예를 들어, 애플리케이션에서 사용자의 데이터를 CSV 파일로 내보내고 이메일로 전송해주는 기능을 생각해봅시다. 하지만 이 CSV 파일을 생성하는 데 시간이 오래 걸리기 때문에, [큐 작업](/docs/{{version}}/queues)으로 파일을 생성하고 이메일로 발송하도록 처리할 수 있습니다. CSV 파일이 생성되어 사용자의 이메일로 발송되면, 서버에서 `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션의 JavaScript가 이를 수신할 수 있게 할 수 있습니다. 이렇게 하면 사용자는 페이지를 새로고침하지 않아도 CSV가 이메일로 전송되었음을 바로 알 수 있습니다.

이러한 기능을 쉽게 구현할 수 있도록, 라라벨에서는 서버 사이드의 [이벤트](/docs/{{version}}/events)를 WebSocket 연결을 통해 간편하게 "브로드캐스트"할 수 있게 해줍니다. 라라벨 이벤트를 브로드캐스트하면 서버와 클라이언트(JavaScript) 애플리케이션이 동일한 이벤트 이름과 데이터를 주고받을 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 명명된 채널에 연결하고, 라라벨 애플리케이션은 백엔드에서 해당 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에서 활용할 다양한 추가 데이터를 포함할 수도 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

라라벨은 기본적으로 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 본격적으로 시작하기 전에 [이벤트와 리스너](/docs/{{version}}/events)에 대한 라라벨 공식 문서를 먼저 읽어보시는 것이 좋습니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치

라라벨의 이벤트 브로드캐스팅을 사용하려면, 애플리케이션에서 약간의 설정과 몇 가지 패키지 설치가 필요합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스팅 드라이버가 담당합니다. 이 드라이버가 라라벨의 이벤트를 브라우저 내의 JavaScript 라이브러리인 Laravel Echo로 전달할 수 있도록 브로드캐스트합니다. 걱정하지 마세요. 아래에서 설치 과정을 단계별로 안내합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스트 관련 설정은 `config/broadcasting.php` 파일에 저장됩니다. 만약 이 파일이 없다면, `install:broadcasting` Artisan 명령어를 실행하면 자동으로 생성됩니다.

라라벨은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한, 테스트 중 브로드캐스트를 비활성화할 수 있는 `null` 드라이버도 제공됩니다. 각각의 예시 설정이 `config/broadcasting.php` 파일에 포함되어 있으니 참고하시면 됩니다.

<a name="installation"></a>
#### 설치

기본적으로 새로 생성된 라라벨 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. 다음 Artisan 명령어로 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 `config/broadcasting.php` 설정 파일을 생성해줍니다. 또한, 브로드캐스트 인가(authorization) 라우트와 콜백을 등록할 수 있는 `routes/channels.php` 파일도 같이 만들어집니다.

<a name="queue-configuration"></a>
#### 큐 설정

이벤트를 브로드캐스트하기 전에, 먼저 [큐 워커](/docs/{{version}}/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅 작업은 큐 작업으로 처리되어, 이벤트 브로드캐스트로 인해 애플리케이션 응답 속도가 느려지는 것을 방지합니다.

<a name="reverb"></a>
### Reverb

`install:broadcasting` 명령어를 실행하면 [Laravel Reverb](/docs/{{version}}/reverb) 설치 여부를 묻는 안내가 표시됩니다. 물론, Composer 패키지 관리자를 이용해 직접 Reverb를 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치 후에는 Reverb의 설치 명령어를 실행하여 설정 파일을 배포하고, 필요한 환경 변수 추가 및 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan reverb:install
```

자세한 설치 및 사용 방법은 [Reverb 공식 문서](/docs/{{version}}/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 이용해 이벤트를 브로드캐스트하려면, Composer 패키지 관리자로 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 설정 파일에 Pusher Channels 인증 정보를 입력해야 합니다. 이 파일에는 이미 예시 설정이 포함되어 있으니, key, secret, app id 등을 빠르게 지정할 수 있습니다. 보통 `.env` 파일을 통해 인증 정보를 설정하게 됩니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에서는 클러스터 등 Channels에서 지원하는 추가 `options`도 지정할 수 있습니다.

마지막으로, `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다.

```ini
BROADCAST_CONNECTION=pusher
```

이제, 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있도록 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 되었습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법입니다. 하지만 Ably 팀은 Ably의 고유한 기능을 활용할 수 있는 전용 브로드캐스터 및 Echo 클라이언트를 별도로 권장 및 유지보수하고 있습니다. 보다 자세한 설정 방법은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 통해 이벤트를 브로드캐스트하려면, Composer 패키지 관리자로 Ably PHP SDK를 설치해야 합니다.

```shell
composer require ably/ably-php
```

설치 후, `config/broadcasting.php` 설정 파일에 Ably 인증 정보를 입력합니다. 이 파일에는 이미 예시 설정이 포함되어 있어 key만 빠르게 지정하면 됩니다. 보통 이 값은 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)를 통해 지정합니다.

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 설정합니다.

```ini
BROADCAST_CONNECTION=ably
```

이제, 클라이언트에서 브로드캐스트 이벤트를 받을 수 있도록 [Laravel Echo](#client-side-installation)를 설치하고 설정하면 됩니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버에서 브로드캐스트되는 이벤트를 수신하는 과정을 매우 간단하게 만들어주는 JavaScript 라이브러리입니다. Echo는 NPM 패키지 매니저를 통해 설치할 수 있습니다. 이 예제에서는 Reverb가 WebSocket 구독, 채널, 메세지를 위해 Pusher 프로토콜을 사용하기 때문에 `pusher-js` 패키지도 함께 설치합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후에는 애플리케이션 JavaScript에서 Echo 인스턴스를 새로 만들 수 있습니다. 라라벨의 기본 프로젝트 구조에서는 `resources/js/bootstrap.js` 파일 하단에 설정하는 것이 좋습니다. 기본적으로 이 파일에는 Echo 설정 예제가 주석 처리된 채로 들어 있으니, 주석을 해제하고 `broadcaster` 옵션을 `reverb`로 변경하면 됩니다.

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

이제 애플리케이션의 에셋을 컴파일해야 합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` broadcaster는 laravel-echo v1.16.0 이상 버전이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드의 브로드캐스팅 드라이버가 전송하는 이벤트를 손쉽게 구독할 수 있도록 해줍니다. Echo는 WebSocket 구독, 채널, 메시지 처리를 위해 `pusher-js` NPM 패키지도 사용합니다.

`install:broadcasting` Artisan 명령어를 실행하면 `laravel-echo`와 `pusher-js` 패키지가 자동으로 설치되지만, 수동으로 설치할 수도 있습니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, 새 Echo 인스턴스를 JavaScript에서 생성할 수 있습니다. `install:broadcasting` 명령어를 통해 생성된 `resources/js/echo.js` 파일의 기본 설정은 Laravel Reverb용이므로, 아래와 같이 내용을 수정해 Pusher로 사용할 수 있습니다.

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

그 다음, `.env` 파일에 Pusher 관련 환경 변수 값을 입력합니다. 해당 변수들이 없으면 직접 추가해야 합니다.

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

설정이 완료되면 다음 명령어로 애플리케이션 에셋을 컴파일합니다.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 JavaScript 에셋 컴파일에 대해 더 알고 싶다면 [Vite 문서](/docs/{{version}}/vite)를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 활용

이미 사전에 설정된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo의 `client` 설정 옵션을 통해 직접 지정할 수 있습니다.

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
> 아래 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법입니다. 그러나 Ably 팀에서는 Ably 고유의 기능을 활용할 수 있는 공식 브로드캐스터와 Echo 클라이언트를 별도로 유지하고 있습니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 브로드캐스트되는 이벤트를 간편하게 수신할 수 있게 해주는 JavaScript 라이브러리입니다. Echo는 WebSocket 구독, 채널, 메시지 처리를 위해 `pusher-js` NPM 패키지를 함께 사용합니다.

`install:broadcasting` Artisan 명령어를 실행하면 `laravel-echo`와 `pusher-js` 패키지가 자동 설치되지만, 직접 NPM으로 수동 설치해도 무방합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**설정 전, Ably 앱의 대시보드에서 "Protocol Adapter Settings" 부분에서 Pusher 프로토콜 지원(Pusher protocol support)을 활성화해야 합니다.**

Echo 설치 후, 새 Echo 인스턴스를 JavaScript에서 생성합니다. 기본 설정은 Laravel Reverb용이므로, 아래와 같이 Ably용으로 수정해 사용할 수 있습니다.

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

이 설정에서는 `VITE_ABLY_PUBLIC_KEY` 환경 변수를 참조합니다. 이 값에는 Ably 키에서 `:` 문자 앞부분에 해당하는 public key를 넣어야 합니다.

설정을 마친 뒤에는 애플리케이션의 에셋을 컴파일합니다.

```shell
npm run dev
```

> [!NOTE]
> JavaScript 에셋 컴파일에 대한 더 자세한 내용은 [Vite 문서](/docs/{{version}}/vite)를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

라라벨의 이벤트 브로드캐스팅 기능을 사용하면 서버에서 발생한 라라벨 이벤트를 WebSocket 기반의 드라이버를 이용해 클라이언트(JavaScript 애플리케이션)로 브로드캐스트할 수 있습니다. 현재 라라벨은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 지원합니다. 이러한 이벤트들은 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 이용해 클라이언트에서 쉽게 소비할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트됩니다. 채널은 퍼블릭 또는 프라이빗으로 구분할 수 있습니다. 퍼블릭 채널은 인증이나 인가 없이 누구나 구독할 수 있지만, 프라이빗 채널은 사용자가 해당 채널에 대한 접근 권한이 있는지 인증, 인가가 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 활용

이벤트 브로드캐스팅의 각 구성 요소를 살펴보기 전에, 전자상거래 스토어를 예시로 전체 흐름을 간단히 살펴보겠습니다.

애플리케이션의 한 페이지에서 사용자가 자신의 주문 배송 상태를 확인할 수 있다고 가정합시다. 주문 상태가 처리되면 `OrderShipmentStatusUpdated` 이벤트가 발생합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 화면을 보고 있을 때, 상태를 확인하려고 매번 새로고침하지 않게 하려면, 이벤트가 발생한 즉시 화면에 상태 변화를 브로드캐스트 해야 합니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트 클래스에 `ShouldBroadcast` 인터페이스를 구현해주면 됩니다. 이 인터페이스는 이벤트가 발생할 때 자동으로 브로드캐스트하도록 라라벨에 지시합니다.

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
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환해야 하며, 기본적으로 자동 생성된 이벤트 클래스 템플릿에 빈 메서드가 포함되어 있으니 필요한 내용을 채워주면 됩니다. 주문의 작성자(해당 주문의 소유자)만 상태 업데이트를 볼 수 있도록, 주문마다 고유한 프라이빗 채널에 브로드캐스트하도록 할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 브로드캐스트하고 싶다면, 배열을 반환하면 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
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
#### 채널 인가

프라이빗 채널을 사용하려면 사용자가 채널을 구독(리스닝)할 자격이 있는지 인가해야 합니다. 이 인가 규칙은 `routes/channels.php` 파일에서 정의합니다. 예를 들어, 프라이빗 `orders.1` 채널에 구독하려는 사용자가 실제 해당 주문의 소유자인지 확인하는 코드는 다음과 같습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 인가를 검사하는 콜백을 받습니다. 콜백의 반환 값이 `true`면 접근이 허용되고, `false`면 거부됩니다.

모든 인가 콜백은 첫 번째 인자로 현재 인증된 사용자를, 그 이후로는 와일드카드(플레이스홀더) 파라미터 값을 받습니다. 위에서는 `{orderId}`를 사용해 "ID" 부분을 동적으로 처리합니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 리스닝

마지막으로, JavaScript 애플리케이션에서 이벤트를 수신하는 코드만 남습니다. [Laravel Echo](#client-side-installation)를 이용해 할 수 있습니다. 먼저, `private` 메서드로 프라이빗 채널에 구독하고, 그 후 `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 리스닝하면 됩니다. 기본적으로 이벤트의 모든 public 속성은 브로드캐스트 이벤트에 포함되어 전달됩니다.

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

특정 이벤트를 브로드캐스트하도록 지정하려면, 이벤트 클래스에서 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현하면 됩니다. 이 인터페이스는 라라벨에서 생성된 모든 이벤트 클래스에 이미 임포트되어 있으므로, 언제든 간단히 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 오직 하나의 메서드, `broadcastOn`의 구현만 요구합니다. `broadcastOn`은 이벤트가 브로드캐스트될 채널(혹은 채널 배열)을 반환해야 합니다. 채널 인스턴스는 `Channel`, `PrivateChannel`, `PresenceChannel` 중 하나여야 하며, `Channel`은 인증 필요 없는 퍼블릭 채널, `PrivateChannel`와 `PresenceChannel`은 [인가](#authorizing-channels)가 필요한 프라이빗 채널입니다.

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
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
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

`ShouldBroadcast` 인터페이스를 구현한 후에는 [이벤트 발생(디스패치)](/docs/{{version}}/events)만 하면 됩니다. 이벤트가 발생하면 [큐 작업](/docs/{{version}}/queues)으로 자동 브로드캐스팅됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 라라벨은 이벤트의 클래스명을 브로드캐스트 이름으로 사용합니다. 하지만, `broadcastAs` 메서드를 정의해 브로드캐스트 이름을 자유롭게 지정할 수도 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

이렇게 이름을 커스터마이징하면, 리스너 등록 시 이벤트 이름 앞에 `.`을 붙여 애플리케이션 네임스페이스가 자동으로 붙지 않도록 Echo에 알려야 합니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 이벤트의 모든 `public` 속성은 자동으로 직렬화되어 페이로드로 전송됩니다. 이를 통해 JavaScript에서 공개된 데이터를 쉽게 접근할 수 있습니다. 예를 들어, public `$user` 속성에 Eloquent 모델이 담겨 있다면 이벤트의 페이로드는 다음과 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

더 세밀하게 브로드캐스트할 데이터 목록을 지정하고 싶다면, `broadcastWith` 메서드를 추가해 반환값으로 원하는 데이터 배열을 지정할 수 있습니다.

```php
/**
 * Get the data to broadcast.
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

기본적으로 각 브로드캐스트 이벤트는 `queue.php` 설정 파일의 기본 큐와 기본 연결을 사용하여 처리됩니다. 이벤트 클래스에 `connection` 및 `queue` 속성을 정의해 브로드캐스트에서 사용할 큐 연결과 큐 이름을 커스터마이즈할 수 있습니다.

```php
/**
 * The name of the queue connection to use when broadcasting the event.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * The name of the queue on which to place the broadcasting job.
 *
 * @var string
 */
public $queue = 'default';
```

혹은, `broadcastQueue` 메서드를 구현해 큐 이름만 별도로 지정할 수도 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

이벤트 브로드캐스트를 기본 큐 드라이버 대신 `sync` 큐로 처리하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하시면 됩니다.

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

특정 조건이 맞을 때만 이벤트를 브로드캐스트하고 싶을 때는, 이벤트 클래스에 `broadcastWhen` 메서드를 추가할 수 있습니다.

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 브로드캐스트 이벤트가 디스패치되면, 이벤트 큐가 트랜잭션 커밋 전에 먼저 처리될 수 있습니다. 이럴 경우, 트랜잭션 내 데이터 변경 내용이 아직 데이터베이스에 반영되지 않아, 브로드캐스트 작업에서 예상치 못한 문제가 발생할 수 있습니다.

만약 큐 연결 설정의 `after_commit` 옵션이 `false`여도, 특정 브로드캐스트 이벤트를 오픈된 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치하고 싶다면, 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

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
> 이 이슈를 우회하는 방법에 대해 더 알고 싶으시다면 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고해주세요.

<a name="authorizing-channels"></a>
## 채널 인가

프라이빗 채널은 현재 인증된 사용자가 해당 채널을 구독할 자격이 있는지 반드시 인가(authorization) 과정을 거쳐야 합니다. 이를 위해 라라벨 애플리케이션에 채널 이름과 함께 HTTP 요청을 보내고, 라라벨이 사용자 인가를 직접 판단합니다. [Laravel Echo](#client-side-installation)를 사용하면 프라이빗 채널 구독 시 HTTP 인가 요청은 자동으로 처리됩니다.

브로드캐스팅이 활성화되면, 라라벨은 `/broadcasting/auth` 라우트를 자동 등록해 인가 요청을 처리합니다. 이 라우트는 자동으로 `web` 미들웨어 그룹에 포함됩니다.

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의

다음으로, 실제로 사용자가 해당 채널을 구독할 수 있는지 검증하는 로직을 정의해야 합니다. 이 내용은 `install:broadcasting` Artisan 명령어로 생성된 `routes/channels.php` 파일에서 작성합니다. 이 파일에서 `Broadcast::channel` 메서드로 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 인가 결과(`true` 또는 `false`)를 반환하는 콜백을 인자로 받습니다.

모든 인가 콜백은 첫 번째 인자로 현재 인증된 사용자를, 그 외 나머지 인자에는 와일드카드 파라미터 값을 전달받습니다. 위 예시처럼 `{orderId}`는 채널 이름의 일부가 동적으로 변할 때 사용합니다.

등록된 브로드캐스트 인가 콜백 목록은 다음 Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백에서 모델 바인딩 활용

HTTP 라우트와 마찬가지로, 채널 라우트에서도 암묵적 또는 명시적 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용할 수 있습니다. 예를 들어, 문자열이나 숫자가 아닌 실제 `Order` 모델 인스턴스를 인자로 받을 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP의 암묵적 모델 바인딩 스코프와 달리, 채널 모델 바인딩은 [암묵적 모델 바인딩 스코프](/docs/{{version}}/routing#implicit-model-binding-scoping)를 자동 지원하지 않습니다. 하지만 대부분의 채널이 단일 모델의 고유 기본 키로 충분히 스코프될 수 있으므로 실제로 문제되는 경우는 드뭅니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백에서 인증

프라이빗 및 프리젠스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드를 이용해 사용자를 인증합니다. 인증되지 않은 사용자는 인가는 무조건 거절되며, 콜백은 실행되지 않습니다. 하지만 요청에 대해 여러 커스텀 가드를 지정하고 싶다면 `guards` 옵션을 사용할 수 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

다양한 채널을 사용하는 애플리케이션의 경우, `routes/channels.php` 파일이 커질 수 있습니다. 이럴 때는 콜백 대신 채널 클래스를 활용할 수 있습니다. 채널 클래스를 생성하려면 `make:channel` Artisan 명령어를 사용합니다. 이 명령어는 `App/Broadcasting` 디렉터리에 새 채널 클래스를 생성해줍니다.

```shell
php artisan make:channel OrderChannel
```

그 이어서, `routes/channels.php`에서 채널을 등록합니다.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

이제 채널 클래스의 `join` 메서드에 인가 로직을 작성하면 됩니다. 이 메서드는 기존 콜백과 동일한 로직을 담을 수 있고, 모델 바인딩도 활용할 수 있습니다.

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> 라라벨의 다른 클래스들과 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 의존성 주입이 가능합니다. 따라서 생성자에 필요한 의존성을 타입힌트로 명시할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스로 마킹했다면, 해당 이벤트의 디스패치 메서드로 [이벤트를 발생]시키기만 하면 됩니다. 이벤트 디스패처는 자동으로 `ShouldBroadcast` 인터페이스가 붙은 이벤트를 감지해 큐에 등록해 브로드캐스트하게 됩니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스트

이벤트 브로드캐스팅을 사용하는 애플리케이션에서, 때로는 현재 사용자 자신을 제외한 채널 구독자 모두에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이럴 땐 `broadcast` 헬퍼의 `toOthers` 메서드를 활용하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

이 메서드가 필요한 이유는 다음과 같습니다. 예를 들어, 사용자가 새로운 작업(Task)을 추가할 때 `/task` 엔드포인트에 요청을 보내고, 서버는 작업 생성과 동시에 이벤트를 브로드캐스트합니다. 클라이언트는 엔드포인트 응답으로 받은 작업을 그대로 리스트에 추가할 수도 있고, 동시에 이벤트 브로드캐스트를 듣고 추가할 수도 있습니다. 하지만 이럴 경우 작업이 중복으로 나타날 수 있습니다. 이 때 `toOthers`를 사용하면 현재 사용자는 브로드캐스트 대상에서 제외되어, 리스트가 중복되지 않습니다.

> [!WARNING]
> `toOthers` 메서드를 사용하려면, 이벤트에서 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 반드시 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스가 초기화되면, 소켓 ID가 연결에 할당됩니다. 전역 [Axios](https://github.com/axios/axios) 인스턴스를 이용해 HTTP 요청을 보낸다면, 소켓 ID가 모든 요청의 `X-Socket-ID` 헤더에 자동으로 첨부됩니다. 그러면 서버에서 `toOthers`를 호출할 때 해당 소켓 ID를 보고 현재 사용자를 브로드캐스트 대상에서 제외해줍니다.

만약 전역 Axios 인스턴스를 사용하지 않는다면, JavaScript 애플리케이션에서 모든 요청에 `X-Socket-ID` 헤더를 수동으로 추가해주어야 합니다. 이 때는 `Echo.socketId` 메서드로 소켓 ID를 얻을 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 커스터마이징

여러 브로드캐스트 연결을 사용하고 있으며, 기본 연결이 아닌 다른 브로드캐스터를 통해 이벤트를 브로드캐스트하고 싶다면, 이벤트를 보낼 때 `via` 메서드로 원하는 연결을 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는, 이벤트 클래스의 생성자에서 `broadcastVia` 메서드를 호출해 브로드캐스트 연결을 지정할 수도 있습니다. 단, 이 경우 이벤트 클래스에서 `InteractsWithBroadcasting` 트레이트를 반드시 사용해야 합니다.

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
     * Create a new event instance.
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### 익명 이벤트

간단한 이벤트를 위해 전용 이벤트 클래스를 만들지 않고, 프론트엔드로 바로 이벤트를 브로드캐스트하고 싶을 때는 `Broadcast` 파사드를 통해 "익명 이벤트"를 보낼 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 코드는 아래와 같은 형태의 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`와 `with` 메서드를 이용해 이벤트의 이름과 데이터를 커스터마이징할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

이 경우, 브로드캐스트되는 이벤트는 다음과 같아집니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

익명 이벤트를 프라이빗 또는 프리젠스 채널로 브로드캐스트하고 싶다면, `private` 또는 `presence` 메서드를 사용하세요.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 익명 이벤트를 [큐](/docs/{{version}}/queues)로 보냅니다. 즉시 브로드캐스트하고 싶을 때는 `sendNow`를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증된 사용자를 제외한 모든 채널 구독자에게 브로드캐스트하려면, `toOthers` 메서드를 사용하세요.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo](#client-side-installation)를 설치하고 인스턴스를 생성했다면, 이제 서버에서 브로드캐스트되는 이벤트를 수신할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 구한 뒤, `listen` 메서드로 원하는 이벤트를 리스닝하세요.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

프라이빗 채널에서는 `private` 메서드를 사용하면 됩니다. 한 채널에서 여러 이벤트를 리스닝하려면 `listen`을 계속 체이닝할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중지

브로드캐스트 채널 자체를 [떠나지 않고](#leaving-a-channel), 특정 이벤트만 리스닝을 멈추고 싶다면, `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 떠나기

채널을 완전히 떠나려면 Echo 인스턴스의 `leaveChannel` 메서드를 사용하세요.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

만약 해당 채널과 연관된 프라이빗 및 프리젠스 채널까지 모두 떠나려면, `leave` 메서드를 사용할 수 있습니다.

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예제들을 보면, 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않았습니다. Echo는 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 간주합니다. Echo 인스턴스 생성 시 `namespace` 설정 옵션을 전달해 루트 네임스페이스를 변경할 수도 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 리스닝 시 이벤트 이름 앞에 항상 `.`을 붙이면, 전체 네임스페이스를 명시할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## 프리젠스 채널

프리젠스 채널은 프라이빗 채널의 보안성을 갖추면서, 누가 채널에 접속해 있는지도 알려주는 추가 기능을 제공합니다. 예를 들어, 다른 사용자가 같은 페이지를 보고 있거나, 채팅방에 누구누구가 입장해 있는지 실시간으로 알리는 협업 기능을 쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프리젠스 채널 인가

모든 프리젠스 채널은 프라이빗 채널이기도 하므로, [인가 절차](#authorizing-channels)가 필요합니다. 하지만 프리젠스 채널에 대한 인가 콜백에서는 단순히 `true`가 아니라, 사용자의 정보를 담은 배열을 반환해야 합니다.

이 콜백에서 반환한 데이터는 JavaScript에서 프리젠스 채널 리스너를 통해 사용할 수 있습니다. 인가되지 않은 사용자는 `false` 또는 `null`을 반환하면 됩니다.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프리젠스 채널 가입

프리젠스 채널에 가입하려면 Echo의 `join` 메서드를 사용하세요. 이 메서드는 `PresenceChannel` 인스턴스를 반환하며, 여기에 `listen`은 물론, `here`, `joining`, `leaving` 이벤트를 구독할 수 있습니다.

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

- `here` 콜백은 채널 가입 성공 시 즉시 실행되며, 현재 채널에 접속 중인 모든 사용자 정보를 배열로 전달합니다.
- `joining`은 새로운 사용자가 채널에 들어올 때,
- `leaving`은 사용자가 채널을 떠날 때 호출됩니다.
- `error`는 인증 엔드포인트가 200이 아닌 HTTP 코드나 JSON 파싱 문제 발생 시 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프리젠스 채널로 브로드캐스트

프리젠스 채널도 퍼블릭/프라이빗 채널과 동일하게 이벤트를 받을 수 있습니다. 예를 들어 채팅방에서 새로운 메세지가 들어오면 `NewMessage` 이벤트를 프리젠스 채널로 브로드캐스트할 수 있습니다. 이때, 이벤트의 `broadcastOn`에서 `PresenceChannel` 인스턴스를 반환하면 됩니다.

```php
/**
 * Get the channels the event should broadcast on.
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

항상 그렇듯, `broadcast` 헬퍼와 `toOthers` 메서드를 조합해 현재 사용자에게만 제외할 수도 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

클라이언트에서는 Echo의 `listen` 메서드를 통해 프리젠스 채널의 브로드캐스트 이벤트를 수신할 수 있습니다.

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
> 아래 모델 브로드캐스팅 기능을 읽기 전, 라라벨의 모델 브로드캐스팅 개념과 직접 이벤트를 정의/리스닝 하는 방법을 먼저 이해하고 계시는 것을 추천합니다.

라라벨 애플리케이션에서 [Eloquent 모델](/docs/{{version}}/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 경우가 많습니다. 물론, 각 상태 변화에 맞는 커스텀 이벤트를 생성해 `ShouldBroadcast` 인터페이스를 마킹하는 방식으로 처리할 수 있습니다.

하지만, 모델 상태 변화 이벤트를 오로지 브로드캐스트 목적으로만 정의하는 것이 번거롭다면, Eloquent 모델에 '자동 브로드캐스트' 기능을 사용할 수 있습니다.

우선 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용해야 합니다. 추가로, 모델에 `broadcastOn` 메서드를 정의하고, 해당 모델의 이벤트가 어떤 채널로 브로드캐스트될지 채널 인스턴스의 배열로 반환해야 합니다.

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
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

트레이트와 `broadcastOn` 메서드를 설정한 뒤에는, 모델 인스턴스가 생성, 수정, 삭제, 트래시, 복원될 때마다 자동으로 이벤트가 브로드캐스트됩니다.

이 때, `broadcastOn` 메서드의 매개변수인 `$event`에는 `created`, `updated`, `deleted`, `trashed`, `restored` 중 해당 모델 이벤트명이 전달됩니다. 이를 활용해, 특정 이벤트에서만 별도의 채널을 사용하도록 자유롭게 분기할 수 있습니다.

```php
/**
 * Get the channels that model events should broadcast on.
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
#### 모델 브로드캐스트 이벤트 생성 커스터마이징

때때로 라라벨이 생성하는 기본 모델 브로드캐스팅 이벤트 동작을 커스터마이징하고 싶을 수 있습니다. 이럴 때는 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의해주면 됩니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
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
#### 채널명 규칙

위의 `broadcastOn` 예제처럼, 반드시 `Channel` 인스턴스를 반환하지 않아도 됩니다. Eloquent 모델 인스턴스 그 자체를 반환할 수도 있습니다. 모델 인스턴스가 반환되면 라라벨이 자동으로 모델 클래스명과 기본 키를 조합해 프라이빗 채널 이름을 생성합니다.

예를 들어, `App\Models\User` 모델의 `id`가 `1`이라면, `App.Models.User.1`이라는 프라이빗 채널이 자동으로 생성됩니다. 물론, 원하는 경우 완전한 채널 인스턴스를 직접 반환해 원하는 채널 이름을 명시적으로 지정할 수 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
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

만약 채널 인스턴스 생성 시 Eloquent 모델을 전달하면, 자동으로 위와 같은 모델 이름 룰을 반영해 채널명이 지정됩니다.

```php
return [new Channel($this->user)];
```

특정 모델의 자동 채널명을 확인하고 싶다면 `broadcastChannel` 메서드를 사용하세요. 예를 들어, `App\Models\User` 모델의 `id`가 `1`이라면 이 메서드는 `App.Models.User.1`을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 `App\Events` 디렉터리 내 실제 이벤트 클래스에 연동되어 있지 않기 때문에, 이벤트 이름과 페이로드가 규칙에 따라 정해집니다. 라라벨은 모델 클래스명(네임스페이스 제외)과 트리거된 모델 이벤트명을 조합해 이벤트 이름을 지정합니다.

예를 들어, `App\Models\Post` 모델의 수정 시 `PostUpdated` 이벤트가 다음과 같은 페이로드와 함께 브로드캐스트됩니다.

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

`App\Models\User` 모델이 삭제될 경우 `UserDeleted`로 이벤트가 전송됩니다.

원한다면 모델에 `broadcastAs`(이벤트 브로드캐스트 이름)와 `broadcastWith`(이벤트 페이로드 데이터) 메서드를 추가해 규칙을 커스터마이징할 수 있습니다. 각 메서드는 발생 이벤트명/작업명을 받아, 이벤트 유형별로 이름과 페이로드를 다르게 지정할 수 있습니다. `broadcastAs`에서 `null`을 반환하면, 라라벨은 기본 규칙을 그대로 사용합니다.

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
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

모델에 `BroadcastsEvents` 트레이트를 추가하고 `broadcastOn` 메서드를 구현했다면, 이제 클라이언트 애플리케이션에서 브로드캐스팅된 모델 이벤트를 수신할 수 있습니다. 시작하기 전에 [이벤트 리스닝](#listening-for-events) 문서를 한 번 더 참고해 보세요.

채널 이름은 [모델 브로드캐스트 규칙](#model-broadcasting-conventions)에 따라 `private` 메서드에 전달하면 됩니다. 모델 브로드캐스트 이벤트는 별도의 실제 이벤트 클래스와 매핑되지 않기 때문에, [이벤트 이름](#model-broadcasting-event-conventions) 앞에 반드시 `.`을 붙여 특정 네임스페이스에 속하지 않는다는 점을 Echo에 알려야 합니다. 각각의 모델 브로드캐스트 이벤트에는 `model` 속성이 포함되어, 모든 모델 공개 속성 정보가 전달됩니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용할 때는 [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

때때로, 라라벨 서버를 거치지 않고 클라이언트들끼리 직접 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어, 입력 중("typing 중")인 상태를 다른 사용자에게 실시간으로 알려주는 경우가 대표적입니다.

클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용할 수 있습니다.

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트를 수신하려면 `listenForWhisper` 메서드를 사용하세요.

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림(Notification)

이벤트 브로드캐스팅을 [알림 시스템](/docs/{{version}}/notifications)과 결합하면, 사용자는 페이지를 새로고침하지 않아도 실시간으로 새 알림을 받을 수 있습니다. 시작하기 전 [브로드캐스트 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 관련 문서를 반드시 확인해 주세요.

알림이 브로드캐스트 채널을 사용하도록 설정하면, Echo의 `notification` 메서드로 브로드캐스트되는 알림을 수신할 수 있습니다. 이때 채널 이름은 알림 수신 대상 엔터티의 클래스명 규칙을 따라야 합니다.

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

이 예제에서는, `App\Models\User` 인스턴스에 `broadcast` 채널을 통해 알림이 전달되면, 콜백에서 해당 알림을 수신하게 됩니다. `App.Models.User.{id}` 채널에 대한 인가 콜백은 애플리케이션의 `routes/channels.php` 파일에 이미 포함되어 있습니다.