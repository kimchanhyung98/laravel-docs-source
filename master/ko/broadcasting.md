# 브로드캐스팅

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
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인증](#authorizing-channels)
    - [인증 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 보내기](#only-to-others)
    - [연결 커스터마이즈하기](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신하기](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 인증](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스트하기](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 관례](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

많은 현대 웹 애플리케이션에서는 실시간, 라이브 UI 업데이트를 구현하기 위해 WebSocket을 사용합니다. 서버에서 데이터가 변경되면 일반적으로 메시지가 WebSocket 연결을 통해 클라이언트로 전송되어 처리됩니다. WebSocket은 UI에서 데이터 변경을 감지하기 위해 서버를 반복적으로 폴링하는 것보다 훨씬 효율적인 대안을 제공합니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고, 이메일로 전송할 수 있다고 가정해 보겠습니다. 이 CSV 파일을 만드는 데 몇 분이 걸린다면, [큐 작업](/docs/{{version}}/queues)으로 생성하고 전송하도록 하시겠죠. CSV 생성과 이메일 발송이 끝나면, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션의 자바스크립트가 이 이벤트를 수신할 수 있습니다. 이벤트가 수신되면, 사용자는 페이지 새로고침 없이 CSV가 이메일로 전송되었음을 알 수 있게 됩니다.

이런 기능을 손쉽게 구현할 수 있도록, Laravel은 서버 사이드 [이벤트](/docs/{{version}}/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 방법을 제공합니다. 이벤트 브로드캐스팅을 사용하면 서버 사이드 Laravel 애플리케이션과 클라이언트 사이드 자바스크립트 애플리케이션이 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 아주 간단합니다: 클라이언트는 프론트엔드에서 명명된 채널에 연결하고, 라라벨 애플리케이션은 백엔드에서 이 채널에 이벤트를 브로드캐스트합니다. 이벤트에는 프론트엔드에서 사용할 수 있도록 원하는 추가 데이터를 담을 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

기본적으로 Laravel은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 자세히 알아보기 전에, 라라벨의 [이벤트와 리스너](/docs/{{version}}/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel의 이벤트 브로드캐스팅을 사용하려면 애플리케이션 내에서 몇 가지 설정을 하고, 별도의 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스팅 드라이버에 의해 이루어지며, 이 드라이버가 Laravel 이벤트를 브라우저 클라이언트에서 Laravel Echo(자바스크립트 라이브러리)가 수신할 수 있도록 전송합니다. 걱정하지 마세요! 설치 과정을 하나씩 안내해 드립니다.

<a name="configuration"></a>
### 설정

애플리케이션의 이벤트 브로드캐스팅 설정은 모두 `config/broadcasting.php` 설정 파일에 저장됩니다. 이 디렉토리가 없다면, `install:broadcasting` 아티즌 명령어 실행 시 자동으로 생성됩니다.

라라벨은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅용 `log` 드라이버, 테스트 시 브로드캐스팅을 비활성화하는 `null` 드라이버가 있습니다. 각각의 드라이버에 대한 예제 설정이 `config/broadcasting.php` 파일에 포함되어 있습니다.

<a name="installation"></a>
#### 설치

기본적으로, 새로운 라라벨 애플리케이션에서는 브로드캐스팅이 비활성화되어 있습니다. `install:broadcasting` 아티즌 명령어로 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 `config/broadcasting.php` 설정 파일을 생성합니다. 또한, 애플리케이션의 브로드캐스트 인증 라우트와 콜백을 등록할 수 있는 `routes/channels.php` 파일도 함께 생성합니다.

<a name="queue-configuration"></a>
#### 큐 설정

이벤트를 브로드캐스트하기 전에, [큐 워커](/docs/{{version}}/queues)를 먼저 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스트는 큐 작업을 통해 처리되어, 애플리케이션의 응답 속도가 이벤트 브로드캐스트 때문에 크게 느려지지 않게 됩니다.

<a name="reverb"></a>
### Reverb

`install:broadcasting` 명령어를 실행하면, [Laravel Reverb](/docs/{{version}}/reverb)를 설치할 것인지 묻는 안내가 표시됩니다. 물론 Composer 패키지 매니저를 직접 사용하여 수동 설치하는 것도 가능합니다.

```shell
composer require laravel/reverb
```

패키지 설치가 완료되면, Reverb의 설치 명령어를 실행하여 설정을 퍼블리시하고, 필요한 환경 변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan reverb:install
```

자세한 설치 및 사용 방법은 [Reverb 문서](/docs/{{version}}/reverb)를 참고해주세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)을 통해 이벤트를 브로드캐스트하려면, Composer 패키지 매니저를 사용해 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 설정 파일에 Pusher Channels 인증 정보를 입력합니다. 이 파일에는 이미 예제 설정이 포함되어 있으므로, key, secret, application ID만 빠르게 지정할 수 있습니다. 일반적으로 `.env` 파일에서 인증 정보를 관리합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에는 클러스터 등 Channels에서 지원하는 추가 옵션(`options`)도 지정할 수 있습니다.

마지막으로, 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다:

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo 설치 및 설정](#client-side-installation)을 진행하면, 클라이언트 사이드에서 브로드캐스트 이벤트를 수신할 수 있습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 "Pusher 호환" 모드로 Ably를 사용하는 방법을 안내합니다. 그러나 Ably팀에서는 Ably 고유의 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트도 제공합니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 통해 이벤트를 브로드캐스트하려면, Composer 패키지 매니저로 Ably PHP SDK를 설치합니다:

```shell
composer require ably/ably-php
```

그리고 `config/broadcasting.php` 파일에 Ably 인증 정보를 입력합니다. 이미 포함되어 있는 예제 설정을 사용해 key를 빠르게 지정할 수 있습니다. 이 값은 보통 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)를 사용해 설정합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정하세요:

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo 설치 및 설정](#client-side-installation)을 통해 클라이언트 사이드에서 브로드캐스트 이벤트를 수신할 수 있습니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 클라이언트에서 채널 구독 및 리스닝할 수 있도록 해주는 자바스크립트 라이브러리입니다. Echo는 NPM 패키지 매니저로 설치할 수 있습니다. 이 예제에서는 WebSocket 구독, 채널, 메시지를 지원하기 위해 `pusher-js` 패키지도 함께 설치합니다(Reverb는 Pusher 프로토콜을 사용):

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후엔, 애플리케이션의 자바스크립트에서 새로운 Echo 인스턴스를 만듭니다. 이 작업은 `resources/js/bootstrap.js` 파일 하단에서 하면 좋습니다. 기본적으로 이 파일에 Echo 설정 예제가 포함되어 있으므로, 주석 처리된 부분을 해제하고 `broadcaster` 옵션을 `reverb`로 바꿔주세요:

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

이후 애플리케이션의 자산을 컴파일하세요:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo `reverb` 브로드캐스터는 laravel-echo v1.16.0+ 버전이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트한 이벤트를 채널에 구독하고 리스닝할 수 있게 해주는 자바스크립트 라이브러리입니다. Echo는 WebSocket 구독, 채널, 메시지를 위해 `pusher-js` NPM 패키지도 활용합니다.

`install:broadcasting` 아티즌 명령어는 `laravel-echo`와 `pusher-js` 패키지를 자동으로 설치합니다. 수동으로 설치하려면 아래처럼 하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면 자바스크립트 내에서 새 Echo 인스턴스를 생성하세요. `install:broadcasting` 명령어로 생성된 `resources/js/echo.js`의 기본 설정은 Reverb 용이므로, 아래의 설정을 참고하여 Pusher로 전환할 수 있습니다:

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

`.env` 파일에 Pusher 관련 환경변수를 적절하게 입력하세요. 만약 변수들이 없다면 추가해야 합니다:

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

설정을 마쳤다면 애플리케이션의 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]
> 자바스크립트 자산 컴파일에 대한 자세한 내용은 [Vite 문서](/docs/{{version}}/vite)를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 설정된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo의 `client` 옵션을 통해 전달할 수 있습니다:

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
> 아래 문서는 "Pusher 호환" 모드를 통한 Ably 사용법을 안내합니다. Ably팀이 권장하는 드라이버 및 Echo 클라이언트는 더 다양한 Ably의 고유 기능을 활용할 수 있습니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버의 이벤트를 자바스크립트에서 간편하게 구독·리스닝할 수 있게 해줍니다. 또한 WebSocket 구독 등을 위해 `pusher-js` NPM 패키지를 활용합니다.

`install:broadcasting` 아티즌 명령어를 사용하면, `laravel-echo`와 `pusher-js`를 자동으로 설치해주지만, 필요하다면 NPM으로 직접 설치도 가능합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속 진행하기 전에, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화하세요. 이는 Ably 애플리케이션의 "프로토콜 어댑터 설정"에서 변경할 수 있습니다.**

Echo가 설치된 후, 애플리케이션 자바스크립트에서 새 Echo 인스턴스를 생성하세요. `install:broadcasting` 명령어로 생성된 `resources/js/echo.js`의 기본 설정은 Reverb 용이므로, 아래 설정을 참고해 Ably로 전환하세요:

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

설정에 등장하는 `VITE_ABLY_PUBLIC_KEY` 환경변수에는 Ably public key를 입력해야 합니다. 이 값은 Ably 키에서 첫 번째 `:` 앞에 오는 부분입니다.

설정을 마친 뒤 자산을 컴파일하세요:

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 자산 컴파일에 대한 자세한 내용은 [Vite 문서](/docs/{{version}}/vite)를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

라라벨의 이벤트 브로드캐스팅은 WebSocket 기반의 드라이버 접근 방식을 통해, 서버 사이드 Laravel 이벤트를 클라이언트 자바스크립트 애플리케이션으로 손쉽게 전송할 수 있도록 해줍니다. 현재 라라벨은 [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 제공합니다. 이벤트는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지로 클라이언트에서 쉽게 사용할 수 있습니다.

이벤트는 "채널"을 매개로 브로드캐스트되며, 채널은 공개 또는 비공개로 지정할 수 있습니다. 공개 채널은 애플리케이션 방문자라면 누구나 인증이나 인가 없이 구독할 수 있습니다. 하지만 비공개 채널을 구독하려면 반드시 해당 채널을 청취할 수 있도록 사용자 인증 및 인가가 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

이벤트 브로드캐스팅의 각 구성 요소를 살펴보기 전에, 이커머스 스토어 예제를 통해 전체적인 흐름을 먼저 살펴봅시다.

사용자가 자신의 주문 배송 상태를 확인할 수 있는 웹 페이지가 있다고 가정합시다. 그리고, 주문의 배송 상태가 업데이트되면 `OrderShipmentStatusUpdated` 이벤트가 발생합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

주문을 보고 있는 사용자가 새로고침하지 않아도 상태 변경을 실시간으로 확인할 수 있습니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 붙여, 이벤트가 발생할 때 브로드캐스트되도록 해야 합니다.

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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스는 반드시 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환합니다. 생성된 이벤트 클래스에는 빈 스텁이 이미 정의되어 있으니, 세부 내용만 넣으면 됩니다. 주문 생성자만 배송 상태를 볼 수 있도록, 주문별 프라이빗(비공개) 채널에 브로드캐스트합니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트 될 채널을 반환합니다.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 이벤트를 브로드캐스트 하려면, 배열로 반환할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트 될 채널 목록을 반환합니다.
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
#### 채널 인증

사용자가 프라이빗 채널을 듣기 위해서는 인증이 필요합니다. 애플리케이션의 `routes/channels.php` 파일에서 채널 인증 규칙을 정의할 수 있습니다. 아래 예제에서는 `orders.1`과 같은 프라이빗 채널을 들으려는 사용자가 실제 주문의 생성자인지 확인합니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과, 사용자가 채널을 청취할 권한이 있는지 true/false를 반환하는 콜백을 받습니다.

모든 인증 콜백은 현재 인증된 사용자를 첫 번째 인자로 받고, 이름이 와일드카드인 나머지 파라미터들은 그 뒤로 전달받습니다. `{orderId}`를 사용하면 채널 이름의 "ID" 부분이 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>
#### 브로드캐스트 이벤트 리스닝

이제 남은 것은 자바스크립트 애플리케이션에서 이벤트를 리스닝하는 것입니다. [Laravel Echo](#client-side-installation)를 사용하면 아래처럼 간단하게 작성할 수 있습니다. 먼저, `private` 메서드로 프라이빗 채널을 구독하고, `listen`으로 `OrderShipmentStatusUpdated` 이벤트를 수신합니다. 기본적으로 이벤트의 모든 public 프로퍼티가 브로드캐스트 페이로드에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

---

**아래 내용부터는 원문의 마크다운 구조·코드·링크를 그대로 유지하면서, 위와 같은 번역 스타일로 계속 번역 바랍니다. 한 번에 길지 않게, 말씀해주시면 이어서 완성까지 계속 번역해드릴 수 있습니다.**