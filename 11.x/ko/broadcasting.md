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
    - [예제 애플리케이션 사용](#using-example-application)
- [브로드캐스트 이벤트 정의](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여](#authorizing-channels)
    - [권한 부여 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [본인 제외하기](#only-to-others)
    - [연결 설정 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 듣기](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스(존재감) 채널](#presence-channels)
    - [프레즌스 채널 권한 부여](#authorizing-presence-channels)
    - [프레즌스 채널 합류](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 듣기](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

현대 웹 애플리케이션에서 WebSocket은 실시간으로 뷰가 업데이트되는 사용자 인터페이스를 구현하는 데 널리 사용됩니다. 서버에서 일부 데이터가 변경될 때, 보통 WebSocket 연결을 통해 메시지가 전송되어 클라이언트에서 처리됩니다. WebSocket은 사용자 인터페이스에 반영되어야 하는 데이터 변화를 지속적으로 서버에 폴링하는 것보다 더 효율적인 대안입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내 이메일로 보내는 기능을 생각해보세요. 이 CSV 파일 생성에 수분이 걸려, CSV 생성과 이메일 전송 작업을 [큐 작업](/docs/11.x/queues)으로 처리하기로 결정할 수 있습니다. CSV가 성공적으로 생성되어 사용자에게 메일로 전송되면, `App\Events\UserDataExported` 이벤트를 방송해 애플리케이션의 자바스크립트가 이를 수신하게 할 수 있습니다. 이벤트가 수신되면, 페이지를 새로고침하지 않아도 사용자에게 CSV가 메일로 전송되었다는 메시지를 보여줄 수 있습니다.

이와 같은 기능을 쉽게 구현할 수 있도록 Laravel은 서버 측 Laravel [이벤트](/docs/11.x/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 기능을 제공합니다. Laravel 이벤트를 브로드캐스트하면 서버 사이드 Laravel 애플리케이션과 클라이언트 사이드 자바스크립트 애플리케이션이 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 명명된 채널에 연결하고, 서버 측 Laravel 애플리케이션은 이 채널에 이벤트를 방송합니다. 이벤트는 프론트엔드에 공개하고 싶은 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

기본적으로 Laravel은 3개의 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), 그리고 [Ably](https://ably.com)입니다.

> [!NOTE]  
> 이벤트 브로드캐스팅을 배우기 전에 Laravel 문서의 [이벤트 및 리스너](/docs/11.x/events)를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel의 이벤트 브로드캐스팅을 시작하려면, Laravel 애플리케이션 내에서 설정을 수행하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스팅 드라이버에 의해 수행되며, 이 드라이버는 Laravel 이벤트를 브로드캐스트하여 Laravel Echo(자바스크립트 라이브러리)가 브라우저 클라이언트 내에서 이를 수신할 수 있도록 합니다. 걱정하지 마세요. 설치 과정의 각 단계를 차근차근 안내해 드립니다.

<a name="configuration"></a>
### 설정

애플리케이션의 이벤트 브로드캐스팅 설정은 모두 `config/broadcasting.php` 설정 파일에 저장됩니다. 해당 파일이 없다면, `install:broadcasting` Artisan 명령어를 실행하면 생성됩니다.

Laravel은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/11.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅용 `log` 드라이버. 또한, 테스트 시 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 이 모든 드라이버 설정 예시는 `config/broadcasting.php` 파일 내에 포함되어 있습니다.

<a name="installation"></a>
#### 설치

기본적으로 새 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어로 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

이 명령어는 `config/broadcasting.php` 설정 파일을 생성합니다. 또한, 애플리케이션의 브로드캐스트 권한 부여 라우트와 콜백을 등록할 수 있는 `routes/channels.php` 파일도 생성합니다.

<a name="queue-configuration"></a>
#### 큐 설정

어떤 이벤트든 브로드캐스트하기 전에, [큐 작업자](/docs/11.x/queues)를 설정하고 실행하는 것이 좋습니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 이루어지므로, 이벤트 브로드캐스트가 애플리케이션의 응답 시간을 심각하게 저하시킬 위험을 방지합니다.

<a name="reverb"></a>
### Reverb

`install:broadcasting` 명령어로 설치할 때 [Laravel Reverb](/docs/11.x/reverb) 설치 여부를 묻습니다. 물론, Composer 패키지 매니저로 직접 설치할 수도 있습니다.

```sh
composer require laravel/reverb
```

패키지를 설치한 후에는 Reverb 설치 명령어를 실행하여 설정 파일을 발행하고, 필요한 환경 변수도 추가하며, 애플리케이션 내에서 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```sh
php artisan reverb:install
```

Reverb 설치와 사용에 관한 자세한 내용은 [Reverb 문서](/docs/11.x/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 이용해 이벤트를 브로드캐스트할 계획이라면, Composer를 사용해 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

그 후, `config/broadcasting.php` 설정 파일에서 Pusher Channels 자격 증명을 설정해야 합니다. 이 파일에는 예시 설정이 포함되어 있어 키, 시크릿, 애플리케이션 ID를 빠르게 지정할 수 있습니다. 보통은 `.env` 파일 내에 다음과 같이 설정합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 내 `pusher` 설정에서는 클러스터 등 Channels가 지원하는 추가 `options`도 지정할 수 있습니다.

그리고 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 다음처럼 설정하세요:

```ini
BROADCAST_CONNECTION=pusher
```

마지막으로, 클라이언트 쪽에서 브로드캐스트 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 완료됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]  
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 설명합니다. 그러나 Ably 팀은 Ably 고유의 기능을 활용할 수 있는 자체 브로드캐스터와 Echo 클라이언트를 추천하고 유지 관리합니다. Ably가 제공하는 드라이버 사용법에 대해서는 [Ably의 Laravel broadcaster 문서](https://github.com/ably/laravel-broadcaster)를 참조하세요.

[Ably](https://ably.com)를 이용해 이벤트를 브로드캐스트할 계획이라면 Composer 패키지 매니저를 사용해 Ably PHP SDK를 설치해야 합니다:

```shell
composer require ably/ably-php
```

다음으로, `config/broadcasting.php` 설정에서 Ably 자격 증명을 구성하세요. 이 파일에는 키를 빠르게 지정할 수 있는 예시 설정이 포함되어 있습니다. 보통 이 값은 `ABLY_KEY` [환경 변수](/docs/11.x/configuration#environment-configuration)로 지정합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일 내에 `BROADCAST_CONNECTION` 환경 변수를 다음과 같이 설정하세요:

```ini
BROADCAST_CONNECTION=ably
```

마지막으로, 클라이언트 측에서 방송 이벤트를 수신할 수 있도록 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 완료됩니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스터가 송출하는 채널을 구독하고 이벤트를 듣기 쉽게 해주는 자바스크립트 라이브러리입니다. NPM을 통해 Echo를 설치할 수 있습니다. 이 예제에서는 Reverb가 WebSocket 구독, 채널, 메시지 전송에 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지도 같이 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, 애플리케이션의 자바스크립트 내에서 새 Echo 인스턴스를 생성할 준비가 됩니다. 좋은 위치는 Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 맨 아래입니다. 기본적으로 이 파일에는 예시 Echo 설정이 포함되어 있으므로, 주석을 해제하고 `broadcaster` 설정을 `reverb`로 변경하면 됩니다.

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

그 후, 애플리케이션 자산을 컴파일합니다:

```shell
npm run build
```

> [!WARNING]  
> Laravel Echo `reverb` 브로드캐스터는 laravel-echo 버전 1.16.0 이상을 필요로 합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 이벤트 청취를 쉽게 해주는 자바스크립트 라이브러리입니다. Echo는 또한 `pusher-js` NPM 패키지를 사용해 Pusher 프로토콜 기반 WebSocket 구독, 채널, 메시지 전송을 구현합니다.

`install:broadcasting` Artisan 명령어를 사용하면 `laravel-echo`와 `pusher-js` 패키지가 자동으로 설치되지만, 수동으로 NPM을 통해 설치할 수도 있습니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, 애플리케이션 자바스크립트 내에서 새 Echo 인스턴스를 생성할 준비가 됩니다. `install:broadcasting` 명령어는 `resources/js/echo.js`에 Echo 설정 파일을 생성하지만, 기본 설정은 Laravel Reverb 용입니다. 아래 설정 예시를 복사해 Pusher용 설정으로 바꿀 수 있습니다:

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

그리고 애플리케이션의 `.env` 파일에 필요한 Pusher 환경 변수를 정의하세요. `.env` 파일에 없으면 다음 값을 추가합니다:

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

필요에 맞게 Echo 설정을 조정한 후 애플리케이션 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]  
> 애플리케이션 자바스크립트 자산 컴파일에 관해 더 알고 싶으면 [Vite](/docs/11.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 Pusher Channels 클라이언트 인스턴스가 미리 설정되어 있으면, Echo를 생성할 때 `client` 옵션으로 전달하여 사용할 수 있습니다:

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
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 설명합니다. 그러나 Ably 팀은 Ably 고유의 기능을 활용할 수 있는 자체 브로드캐스터와 Echo 클라이언트를 추천하고 유지 관리합니다. Ably가 제공하는 드라이버 사용법에 대해서는 [Ably의 Laravel broadcaster 문서](https://github.com/ably/laravel-broadcaster)를 참조하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스터가 송출하는 채널을 구독하고 이벤트를 듣기 쉽게 해주는 자바스크립트 라이브러리입니다. Echo는 `pusher-js` NPM 패키지를 사용해 Pusher 프로토콜 기반 WebSocket 구독, 채널, 메시지 전송을 구현합니다.

`install:broadcasting` Artisan 명령어는 `laravel-echo`와 `pusher-js`를 자동으로 설치하지만, 직접 NPM으로 설치할 수도 있습니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. Ably 애플리케이션의 설정 대시보드 내 "Protocol Adapter Settings" 항목에서 이 기능을 활성화할 수 있습니다.**

Echo 설치 후, `resources/js/echo.js`에 기본적으로 Laravel Reverb용 설정이 생성됩니다. 아래 설정 예시를 참고해 Ably 용으로 변경할 수 있습니다:

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

설정 중 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키를 의미합니다. 공개 키는 Ably 키 문자열의 `:` 문자 앞부분입니다.

설정을 마쳤으면 애플리케이션 자산을 컴파일하세요:

```shell
npm run dev
```

> [!NOTE]  
> 애플리케이션 자바스크립트 자산 컴파일에 관해 더 알고 싶으면 [Vite](/docs/11.x/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel의 이벤트 브로드캐스팅은 드라이버 기반 접근법으로 서버 측 Laravel 이벤트를 클라이언트 사이드 자바스크립트 애플리케이션에 방송할 수 있도록 합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com) 드라이버를 기본 제공하며, 클라이언트 측에서는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 사용해 이벤트를 쉽게 수신할 수 있습니다.

이벤트는 "채널"을 통해 방송되며, 해당 채널은 퍼블릭(public) 또는 프라이빗(private)으로 지정할 수 있습니다. 퍼블릭 채널은 누구나 인증이나 권한 없이 구독할 수 있지만, 프라이빗 채널은 반드시 인증과 해당 채널에 대한 권한이 있어야 구독할 수 있습니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용

각 브로드캐스팅 구성요소를 보기 전에, 전자상거래 사이트를 예로 들어 전체 흐름을 간단히 살펴보겠습니다.

가령, 사용자가 주문 배송 상태를 확인할 수 있는 페이지가 있다고 합시다. 그리고 애플리케이션에서 배송 상태가 업데이트될 때마다 `OrderShipmentStatusUpdated` 이벤트가 발생한다 가정합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 상태를 보기 위해 매번 페이지를 새로고침할 필요를 없애려면, 배송 상태 업데이트가 처리될 때마다 이를 방송해야 합니다. 따라서 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현합니다. 그러면 Laravel은 이벤트가 발생할 때 이를 자동으로 방송합니다:

```
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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 방송될 채널을 반환하는 역할을 합니다. 기본적으로 이벤트 클래스 생성 시 이 메서드의 빈 코드가 포함되어 있으니, 내용을 채우면 됩니다. 주문 생성자만 상태 업데이트를 볼 수 있도록 주문과 연관된 프라이빗 채널에서 방송하겠습니다:

```
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 방송될 채널 반환.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 방송하려면 `array`를 반환할 수도 있습니다:

```
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 방송될 채널들 반환.
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
#### 채널 권한 부여하기

프라이빗 채널에 접속하려면 사용자가 권한이 있어야 합니다. 이를 위해 애플리케이션의 `routes/channels.php` 파일에 권한 부여 규칙을 정의할 수 있습니다. 예를 들어, `orders.1` 프라이빗 채널에 접속하는 사용자가 실제로 해당 주문의 생성자인지 확인해야 합니다:

```
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널명과 사용자 권한 유무를 반환하는 콜백을 두 인수로 받습니다.

권한 부여 콜백은 첫 번째 인수로 현재 인증된 유저를, 두 번째부터는 와일드카드 매개변수를 받습니다. 여기서는 `{orderId}`를 사용해 채널 이름에서 ID 부분이 와일드카드를 의미함을 나타내고 있습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 청취하기

마지막으로 애플리케이션 자바스크립트에서 [Laravel Echo](#client-side-installation)를 이용해 이벤트를 청취합니다. 먼저 `private` 메서드로 프라이빗 채널을 구독하고, `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트에 대해 청취합니다. 기본적으로 이벤트의 모든 public 속성이 전달됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의

Laravel에게 특정 이벤트를 브로드캐스트하도록 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 기본적으로 포함되어 있으므로 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 단일 메서드 `broadcastOn` 구현을 요구합니다. `broadcastOn` 메서드는 방송할 채널이나 채널 배열을 반환해야 하며, 채널은 `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스여야 합니다. `Channel` 인스턴스는 모든 사용자가 구독 가능한 퍼블릭 채널이며, `PrivateChannel`과 `PresenceChannel`은 [채널 권한 부여](#authorizing-channels)를 필요로 하는 프라이빗 채널을 나타냅니다.

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
     * 새 이벤트 인스턴스 생성.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 방송할 채널 반환.
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

`ShouldBroadcast`를 구현한 후에는 일반적인 방법대로 [이벤트를 발생시키기](/docs/11.x/events)만 하면 됩니다. 이벤트 발생 시, [큐 작업](/docs/11.x/queues)이 자동으로 브로드캐스트 작업을 처리를 담당합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스명을 브로드캐스트 이벤트 이름으로 사용합니다. 그러나 `broadcastAs` 메서드를 이벤트에 정의해 브로드캐스트 이름을 커스터마이징할 수 있습니다:

```
/**
 * 이벤트의 브로드캐스트 이름.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`를 사용해 이름을 변경했다면, Echo에서 앞에 `.` 문자를 붙여 이벤트를 등록하세요. 이렇게 하면 Echo가 애플리케이션 네임스페이스를 앞에 붙이지 않습니다:

```
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 방송될 때, 모든 `public` 속성은 자동으로 직렬화되어 이벤트의 페이로드(payload)로 전달되므로 자바스크립트 애플리케이션에서 이를 바로 사용할 수 있습니다. 예를 들어, public `$user` 속성이 Eloquent 모델로 정의되어 있다면, 브로드캐스트 페이로드는 다음과 같습니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

그러나 페이로드를 세밀하게 제어하려면 `broadcastWith` 메서드를 추가할 수 있으며, 이 메서드가 반환하는 배열이 이벤트 데이터로 방송됩니다:

```
/**
 * 브로드캐스트할 데이터 반환.
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

기본적으로 방송 이벤트는 `queue.php` 설정 파일 내 기본 큐 연결과 기본 큐에 할당됩니다. 브로드캐스터가 사용하는 큐 연결과 큐 이름을 이벤트 클래스의 `connection`과 `queue` 속성으로 커스터마이즈할 수 있습니다:

```
/**
 * 브로드캐스트 시 사용할 큐 연결 이름.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스트 작업을 할당할 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드를 통해 큐 이름을 정의할 수도 있습니다:

```
/**
 * 브로드캐스트 작업을 할당할 큐 이름 반환.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

만약 기본 큐 드라이버 대신 동기(sync) 큐를 사용해 즉시 브로드캐스트하려면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요:

```
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건이 참일 때만 이벤트를 방송하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가해 조건을 정의할 수 있습니다:

```
/**
 * 이벤트 방송 여부 결정.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

이벤트 닷치가 데이터베이스 트랜잭션 내에서 발생하면, 큐 작업은 트랜잭션 커밋 전에 실행될 수 있습니다. 이로 인해 트랜잭션 중에 변경한 데이터가 아직 데이터베이스에 반영되지 않았거나, 새로 생성한 레코드가 존재하지 않을 수 있습니다. 이 경우 모델에 의존하는 이벤트가 에러를 발생시킬 수 있습니다.

큐 연결 설정에서 `after_commit` 옵션이 `false`일 경우, 특정 브로드캐스트 이벤트가 모든 열린 트랜잭션이 커밋된 이후에 디스패치되도록 `ShouldDispatchAfterCommit` 인터페이스를 이벤트 클래스에 구현할 수 있습니다:

```
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
> 이 문제 해결에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/11.x/queues#jobs-and-database-transactions) 문서를 확인하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여

프라이빗 채널은 사용자가 현재 인증된 상태인지, 그리고 해당 채널에 접근 권한이 있는지 승인받아야 구독할 수 있습니다. 이는 채널 이름과 함께 HTTP 요청을 Laravel 애플리케이션에 보내서, 애플리케이션이 사용자의 권한 여부를 판단하도록 하는 방식입니다. [Laravel Echo](#client-side-installation)를 사용하는 경우, 프라이빗 채널 권한 부여에 필요한 HTTP 요청이 자동으로 이루어집니다.

브로드캐스팅이 활성화되면, Laravel은 `/broadcasting/auth` 라우트를 자동으로 등록하여 권한 부여 요청을 처리합니다. 이 경로는 기본적으로 `web` 미들웨어 그룹 내부에 위치합니다.

<a name="defining-authorization-callbacks"></a>
### 권한 부여 콜백 정의하기

이제 실제로 현재 인증된 사용자가 특정 채널을 구독할 권한이 있는지 판단하는 로직을 정의해야 합니다. 이는 `install:broadcasting` 명령어가 생성한 `routes/channels.php` 파일에서 합니다. 여기서 `Broadcast::channel` 메서드로 채널 권한 부여 콜백을 등록할 수 있습니다:

```
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널명과 권한 여부를 `true` 또는 `false`로 반환할 콜백을 받습니다.

모든 권한 부여 콜백은 첫 번째 인수로 현재 인증된 사용자, 이후 인수로는 와일드카드 매개변수를 받습니다. 위 예제에서 `{orderId}`는 채널명에서 ID 부분이 와일드카드임을 의미합니다.

등록한 권한 부여 콜백 목록은 `channel:list` Artisan 명령으로 확인할 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 권한 부여 콜백 모델 바인딩

HTTP 라우트처럼 채널 경로도 명시적 또는 암묵적 [라우트 모델 바인딩](/docs/11.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어, `orderId` 대신 실제 `Order` 모델 인스턴스를 받을 수도 있습니다:

```
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]  
> HTTP 라우트와 달리, 채널 모델 바인딩은 자동 [스코핑](/docs/11.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 그러나 대부분의 채널은 단일 모델 기본키로 충분히 스코핑되므로 큰 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 권한 부여 콜백 인증

프라이빗 및 프레즌스 브로드캐스트 채널은 요청에 대해 기본 인증 가드를 통해 사용자를 인증합니다. 인증되지 않은 사용자는 자동으로 권한 부여가 거절되어 콜백이 실행되지 않습니다. 다중 또는 커스텀 가드를 사용해야 할 경우 옵션으로 지정할 수 있습니다:

```
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션에서 여러 채널을 사용할 경우, `routes/channels.php` 파일이 너무 복잡해질 수 있습니다. 이 때, 권한 부여를 클로저 대신 채널 클래스로 분리할 수 있습니다. `make:channel` Artisan 명령어로 채널 클래스를 생성하세요. 이 클래스는 `App/Broadcasting` 디렉토리에 생성됩니다.

```shell
php artisan make:channel OrderChannel
```

생성 후, `routes/channels.php`에 채널을 등록합니다:

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

그리고 그 채널 클래스 내의 `join` 메서드에 권한 부여 로직을 구현하세요. 이 메서드는 채널 권한 부여 클로저와 같은 역할을 하며, 모델 바인딩도 사용할 수 있습니다:

```
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * 새 채널 인스턴스 생성.
     */
    public function __construct() {}

    /**
     * 채널 접근 권한 인증.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]  
> Laravel의 다른 클래스처럼, 채널 클래스도 [서비스 컨테이너](/docs/11.x/container)에 의해 자동으로 해석되므로, 의존성은 생성자 주입을 활용할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

`ShouldBroadcast` 인터페이스를 구현한 이벤트를 정의했다면, 이제 평소처럼 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 해당 이벤트가 `ShouldBroadcast`로 표시되었음을 감지하고 브로드캐스트 큐에 작업을 넣습니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 본인 제외하기

브로드캐스팅을 활용하는 애플리케이션에서는 가끔 현재 사용자를 제외한 다른 모든 구독자에게만 이벤트를 방송할 필요가 있습니다. 이는 `broadcast` 헬퍼 함수와 `toOthers` 메서드를 통해 구현할 수 있습니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어, 작업 목록 애플리케이션에서 사용자가 작업을 생성할 때, 서버에 `/task` 경로로 요청하면 작업이 생성되고 방금 생성된 작업의 JSON 데이터가 반환됩니다. 클라이언트 자바스크립트가 응답을 받아 작업 목록에 즉시 추가하죠:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

한편, 작업 생성 이벤트도 브로드캐스트됩니다. 자바스크립트가 이 이벤트를 듣고 작업을 추가한다면, 같은 작업이 두 번 목록에 나타납니다. 이를 막으려면 `toOthers` 메서드를 이용해 현재 사용자는 방송에서 제외시키세요.

> [!WARNING]  
> `toOthers` 메서드를 사용하려면, 이벤트에서 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 반드시 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 구성

Laravel Echo 인스턴스가 초기화될 때, 연결에 소켓 ID가 할당됩니다. Axios 전역 인스턴스를 사용하는 경우, 이 소켓 ID가 모든 HTTP 요청의 `X-Socket-ID` 헤더에 자동으로 포함됩니다. `toOthers`가 호출되면 이 헤더의 소켓 ID를 기준으로 현재 사용자의 연결을 방송에서 제외합니다.

만약 Axios 전역 인스턴스를 쓰지 않으면, 직접 모든 요청에 `X-Socket-ID` 헤더를 포함하도록 자바스크립트를 설정해야 합니다. 소켓 ID는 `Echo.socketId()` 메서드로 얻을 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 설정 커스터마이징

애플리케이션에서 여러 브로드캐스트 연결을 사용하고 있고, 기본 연결과 다른 드라이버로 이벤트를 방송하고 싶다면 `via` 메서드를 사용할 수 있습니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 클래스 내 생성자에서 `broadcastVia` 메서드를 호출해 방송 연결을 지정할 수도 있습니다. 이 때 `InteractsWithBroadcasting` 트레이트가 사용되어야 합니다:

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
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### 익명 이벤트

때때로, 별도의 이벤트 클래스를 만들지 않고 간단한 이벤트를 방송하고 싶을 수 있습니다. 이를 위해 `Broadcast` 파사드는 "익명 이벤트" 방송을 지원합니다:

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 코드는 다음과 같은 이벤트를 방송합니다:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`와 `with` 메서드로 이벤트 이름과 데이터를 커스터마이징할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

이벤트 이름이 `OrderPlaced`이고 다음과 유사한 데이터를 방송합니다:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

익명 이벤트를 프라이빗이나 프레즌스 채널에서 방송하려면 `private` 또는 `presence` 메서드를 이용하세요:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 이벤트를 큐에 넣어 처리하게 하지만, 즉시 브로드캐스트하려면 `sendNow` 메서드를 사용하세요:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 사용자를 제외한 모든 구독자에게 익명 이벤트를 방송하려면 `toOthers`를 호출하세요:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 듣기

[Laravel Echo 설치 및 인스턴스화](#client-side-installation)를 완료하면, Laravel 애플리케이션에서 브로드캐스트된 이벤트를 듣기 시작할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 가져온 후 `listen` 메서드로 특정 이벤트를 청취하세요:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

프라이빗 채널에 대해선 `private` 메서드를 사용하세요. 한 채널에서 여러 이벤트를 청취하기 위해 `listen`을 연속 호출할 수도 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 듣기 중단하기

특정 이벤트만 더 이상 듣고 싶다면, [채널을 떠나는 것과 별개로](#leaving-a-channel) `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 떠나기

채널을 떠나려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

해당 채널과 그에 연결된 프라이빗 및 프레즌스 채널까지 모두 떠나려면 `leave` 메서드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예제들에서 이벤트 클래스의 전체 `App\Events` 네임스페이스를 명시하지 않은 것을 보셨을 겁니다. 이는 Echo가 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 간주하기 때문입니다. Echo 생성 시 `namespace` 설정 옵션으로 기본 네임스페이스를 바꿀 수도 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

아니면, Echo에서 이벤트 이름 앞에 `.`를 붙여 네임스페이스를 명시하지 않고 전체 클래스명을 직접 지정할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## 프레즌스(존재감) 채널

프레즌스 채널은 프라이빗 채널의 보안 기능에 더해, 누가 해당 채널에 접속해 있는지 알 수 있게 해줍니다. 이를 통해 같은 페이지를 보는 사용자 알림, 채팅방 참가자 목록 표시 같은 강력한 협업 기능을 쉽게 만들 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 권한 부여

프레즌스 채널도 프라이빗 채널과 동일하게 접근 권한이 있어야 합니다. 권한 콜백을 정의할 때, 사용자가 채널에 접속 가능하면 단순히 `true`를 반환하는 것이 아니라 사용자 정보를 담은 배열을 반환해야 합니다.

권한 콜백이 반환한 데이터는 프레즌스 채널 Javascript 이벤트 리스너에서 사용할 수 있습니다. 권한이 없으면 `false` 또는 `null`을 반환해야 합니다:

```
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 합류

프레즌스 채널에 합류하려면 Echo의 `join` 메서드를 사용하세요. `join` 메서드는 `PresenceChannel` 객체를 반환하며, 이는 `listen` 메서드 뿐 아니라 `here`, `joining`, `leaving` 이벤트에도 구독할 수 있게 합니다:

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // 현재 채널에 있는 사용자 배열
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

- `here` 콜백은 채널 합류 성공 시 즉시 실행되며, 현재 접속중인 사용자 정보 배열을 받습니다.
- `joining` 메서드는 새 사용자가 합류할 때 호출됩니다.
- `leaving` 메서드는 사용자가 채널을 떠날 때 호출됩니다.
- `error` 메서드는 인증 엔드포인트에서 200 이외의 HTTP 상태가 응답되거나 반환된 JSON을 파싱하는 데 문제가 있을 때 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅

프레즌스 채널도 퍼블릭/프라이빗 채널처럼 이벤트를 받을 수 있습니다. 예를 들어 채팅채널에서 `NewMessage` 이벤트를 프레즌스 채널로 방송하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다:

```
/**
 * 이벤트가 방송할 채널 반환.
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

다른 이벤트와 마찬가지로 `broadcast` 헬퍼와 `toOthers` 메서드를 써서 현재 사용자를 제외할 수 있습니다:

```
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

클라이언트 측에서는 Echo의 `listen` 메서드로 프레즌스 채널 이벤트를 청취합니다:

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
> 모델 브로드캐스팅 문서를 읽기 전에 Laravel의 모델 브로드캐스팅 서비스 기본 개념과 직접 이벤트 클래스를 만들어 사용하는 방법에 익숙해지는 것을 추천합니다.

애플리케이션에서 Eloquent 모델이 생성, 갱신, 삭제될 때 종종 해당 상태 변화를 방송하는 경우가 있습니다. 물론, 이를 위해 모델 상태 변경용 커스텀 이벤트를 정의하고 `ShouldBroadcast`를 구현하는 전통적인 방법이 있습니다.

하지만 이 이벤트들을 다른 용도로 사용하지 않는다면, 단지 브로드캐스팅을 위해 이벤트 클래스를 만드는 것은 번거로울 수 있습니다. 이를 위해 Laravel은 Eloquent 모델이 상태 변경 시 자동으로 방송하도록 지정할 수 있는 기능을 제공합니다.

우선 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용해야 합니다. 또한 모델에 `broadcastOn` 메서드를 정의하여 모델 이벤트를 방송할 채널 배열을 반환하도록 합니다:

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
     * 포스트가 속한 사용자 반환.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트 방송 채널 반환.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이렇게 하면 모델 인스턴스가 생성, 갱신, 삭제, 휴지통에 등록(trashed), 복원(restored)될 때 자동으로 방송됩니다.

`broadcastOn` 메서드는 `$event`라는 이벤트 종류 문자열(`created`, `updated`, `deleted`, `trashed`, `restored`)을 인수로 받아 처리할 수 있습니다:

```php
/**
 * 모델 이벤트 방송 채널 반환.
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

Laravel이 내부적으로 모델 브로드캐스트 이벤트를 생성하는 방식을 수정하려면, 모델에 `newBroadcastableEvent` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 객체를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델에 대한 새 브로드캐스트 이벤트 생성.
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
#### 채널 규칙

`broadcastOn` 메서드가 `Channel` 인스턴스 대신 Eloquent 모델을 반환하는 것을 보셨을 겁니다. 이렇게 모델 인스턴스를 반환하면, Laravel은 자동으로 모델 클래스명과 기본키를 사용해 프라이빗 채널 이름을 만들어 줍니다.

예를 들어, `App\Models\User` 모델 인스턴스의 `id`가 `1`이라면, 이 모델은 `Illuminate\Broadcasting\PrivateChannel` 인스턴스(`App.Models.User.1` 이름)로 변환됩니다. 실제로 채널 인스턴스를 반환해 자유롭게 채널 이름을 지정할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트 방송 채널 반환.
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

또한, Eloquent 모델 인스턴스를 채널 생성자에 직접 넘기면, 위와 같은 규칙에 따라 채널 이름 문자열로 변환됩니다:

```php
return [new Channel($this->user)];
```

모델 인스턴스의 채널 이름을 확인하고 싶으면 `broadcastChannel` 메서드를 호출하세요. 예를 들어 `App\Models\User` 모델 인스턴스는 다음과 같습니다:

```php
$user->broadcastChannel()
```

`App.Models.User.1`와 같은 문자열을 반환합니다.

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉토리 내 실제 이벤트가 아니므로, Laravel의 규칙에 따라 이름과 페이로드가 결정됩니다. 규칙은 모델의 클래스명(네임스페이스 제외)과 발생한 모델 이벤트 이름을 결합한 형태입니다.

예를 들어 `App\Models\Post` 모델이 갱신되면, 클라이언트에 `PostUpdated` 이벤트가 방송되고 페이로드 예시는 다음과 같습니다:

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

`App\Models\User` 모델 삭제는 `UserDeleted` 이벤트를 방송합니다.

커스텀 이름과 페이로드를 정의하려면 모델에 `broadcastAs`와 `broadcastWith` 메서드를 추가하세요. 이들 메서드는 발생하는 모델 이벤트 이름을 인수로 받아 상황별로 다른 이름과 데이터를 반환할 수 있습니다. 만약 `broadcastAs`에서 `null`을 반환하면, 기본 규칙대로 이벤트 이름이 결정됩니다:

```php
/**
 * 모델 이벤트 방송 이름.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델 방송 데이터 반환.
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
### 모델 브로드캐스트 듣기

`BroadcastsEvents` 트레이트를 모델에 추가하고, `broadcastOn` 메서드를 정의한 상태라면 클라이언트 측에서 방송되는 모델 이벤트를 듣기 시작할 수 있습니다. [이벤트 듣기](#listening-for-events) 문서를 참고하세요.

우선 `private` 메서드로 Laravel 모델 브로드캐스팅 규칙에 맞는 채널을 구독하고, `listen` 메서드로 특정 이벤트를 청취하세요. 모델 브로드캐스트 이벤트는 애플리케이션 이벤트가 아니므로, 이벤트 이름 앞에 반드시 `.`를 붙여 네임스페이스 소속 아님을 나타내야 합니다. 각 모델 방송 이벤트 데이터는 `model` 프로퍼티에 모델의 모든 방송 가능한 속성이 포함됩니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]  
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, [Pusher 대시보드](https://dashboard.pusher.com/)의 "Client Events" 옵션을 앱 설정에서 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

클라이언트끼리 Laravel 애플리케이션에 요청하지 않고 이벤트를 방송할 때가 있습니다. 예를 들어 누군가 메시지를 입력하고 있다는 "타이핑 중" 알림 기능 등에서 유용합니다.

클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용하세요:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트는 `listenForWhisper`로 청취할 수 있습니다:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅과 [알림](/docs/11.x/notifications)을 연동하면, 자바스크립트 애플리케이션에서 페이지 새로고침 없이 실시간 새 알림을 받을 수 있습니다. 시작하기 전에 [브로드캐스트 알림 채널](/docs/11.x/notifications#broadcast-notifications) 문서를 먼저 읽어보세요.

알림을 브로드캐스트 채널에 설정한 후, Echo의 `notification` 메서드로 방송 이벤트를 청취할 수 있습니다. 채널명은 알림을 받을 객체 클래스명과 일치해야 합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

이 예제는 `App\Models\User` 인스턴스에 `broadcast` 채널을 통해 전송된 모든 알림을 콜백으로 수신합니다. `routes/channels.php` 파일에는 `App.Models.User.{id}` 채널에 대한 권한 부여 콜백이 기본 포함되어 있습니다.