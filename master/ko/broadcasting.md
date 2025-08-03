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
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여하기](#authorizing-channels)
    - [권한 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [본인 제외하기](#only-to-others)
    - [연결 맞춤 설정하기](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 수신 대기](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 권한 부여](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 수신 대기](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

많은 현대 웹 애플리케이션에서는 WebSocket을 이용해 실시간 라이브 업데이트 UI를 구현합니다. 서버에서 데이터가 업데이트될 때, 보통 WebSocket 연결을 통해 클라이언트로 메시지가 전송되어 처리됩니다. WebSocket은 UI에 반영할 데이터 변경을 위해 애플리케이션 서버를 지속적으로 폴링하는 것보다 훨씬 효율적입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 추출해 이메일로 보내는 애플리케이션을 생각해보세요. CSV 파일 생성에 수 분이 소요되므로 작업을 [큐 잡](/docs/master/queues)으로 처리한다고 가정합시다. CSV 파일이 생성되어 사용자에게 이메일로 전송되면, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션 자바스크립트가 이를 수신하게 할 수 있습니다. 이벤트 수신 즉시 페이지를 새로 고침하지 않아도 CSV가 이메일로 전송되었음을 사용자에게 알릴 수 있습니다.

이러한 기능 개발을 돕기 위해, Laravel은 서버 측 Laravel [이벤트](/docs/master/events)를 WebSocket 연결을 통해 쉽게 "브로드캐스트"할 수 있도록 지원합니다. Laravel 이벤트 브로드캐스팅을 통해 서버와 클라이언트 자바스크립트 애플리케이션 간 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 이름 있는 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 해당 채널로 이벤트를 브로드캐스트합니다. 이벤트는 프론트엔드에 전달할 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 세 가지 서버 측 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 반드시 Laravel의 [이벤트 및 리스너](/docs/master/events) 문서를 먼저 읽어보세요.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel 이벤트 브로드캐스팅을 시작하려면 Laravel 애플리케이션 내에서 설정 작업과 몇몇 패키지 설치가 필요합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스팅 드라이버가 Laravel 이벤트를 브로드캐스트하여 Laravel Echo(자바스크립트 라이브러리)가 브라우저 클라이언트에서 이를 수신하게 하는 방식으로 동작합니다. 걱정하지 마세요 - 설치 과정을 단계별로 자세히 설명할 것입니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 파일에 저장됩니다. 애플리케이션에 해당 디렉터리가 없더라도 걱정하지 마세요. `install:broadcasting` Artisan 명령어를 실행하면 생성됩니다.

Laravel은 기본적으로 [Laravel Reverb](/docs/master/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com)와 로컬 개발 및 디버깅용 `log` 드라이버를 지원합니다. 또한 테스트 중 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. `config/broadcasting.php` 파일에는 각 드라이버별 예제 설정이 포함되어 있습니다.

<a name="installation"></a>
#### 설치

새 Laravel 애플리케이션에서는 기본적으로 브로드캐스팅이 활성화되어 있지 않습니다. 다음 Artisan 명령어를 사용해 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

이 명령어는 `config/broadcasting.php` 설정 파일을 생성합니다. 또한 애플리케이션의 브로드캐스트 권한 부여 라우트와 콜백을 등록할 수 있는 `routes/channels.php` 파일도 생성합니다.

<a name="queue-configuration"></a>
#### 큐 설정

이벤트를 브로드캐스트하기 전에 먼저 [큐 작업자](/docs/master/queues)를 구성하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐드 잡을 통해 처리되므로, 이벤트 브로드캐스트가 애플리케이션 응답 시간에 큰 영향을 주지 않습니다.

<a name="reverb"></a>
### Reverb

`install:broadcasting` 명령어를 실행하면 [Laravel Reverb](/docs/master/reverb)를 설치할지 묻습니다. 물론, Composer 패키지 관리자를 통해 직접 설치할 수도 있습니다:

```shell
composer require laravel/reverb
```

패키지가 설치되면, Reverb 설치 명령어를 실행하여 설정을 게시하고 필요한 환경 변수들을 추가 및 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용법은 [Reverb 문서](/docs/master/reverb)에서 확인하세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 이용해 이벤트를 브로드캐스트하려면 Composer를 통해 PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

그다음 `config/broadcasting.php` 설정 파일에서 Pusher Channels 자격 증명을 설정합니다. 이미 예제 설정이 포함되어 있어 빠르게 key, secret, application ID를 지정할 수 있습니다. 보통 `.env` 파일에 다음과 같이 설정합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일 내 `pusher` 설정은 클러스터 등 Channels가 지원하는 추가 `options` 항목도 지정할 수 있습니다.

그리고 `.env` 파일에 다음과 같이 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다:

```ini
BROADCAST_CONNECTION=pusher
```

이제 클라이언트 측에서 브로드캐스트 이벤트를 수신할 수 있도록 [Laravel Echo](#client-side-installation)를 설치 및 설정할 준비가 되었습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 Ably를 "Pusher 호환" 모드로 사용하는 방법을 설명합니다. 하지만 Ably 팀은 Ably의 고유 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트를 유지 관리합니다. Ably가 제공하는 드라이버를 사용하려면 [Ably Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참조하세요.

[Ably](https://ably.com)를 통해 이벤트를 브로드캐스트하려면 Composer로 PHP SDK를 설치해야 합니다:

```shell
composer require ably/ably-php
```

`config/broadcasting.php` 파일에서 Ably 자격증명을 설정합니다. 이미 key를 지정할 수 있는 예제 설정이 포함되어 있으며, 보통 `ABLY_KEY` [환경 변수](/docs/master/configuration#environment-configuration)로 설정합니다:

```ini
ABLY_KEY=your-ably-key
```

그리고 `.env` 파일에서 다음과 같이 `BROADCAST_CONNECTION`을 `ably`로 지정합니다:

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo](#client-side-installation)를 설치 및 설정하여 클라이언트에서 브로드캐스트를 수신할 수 있습니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스팅 드라이버에서 브로드캐스트되는 이벤트 채널 구독과 수신을 쉽게 해주는 자바스크립트 라이브러리입니다. NPM 패키지 관리자를 통해 Echo를 설치할 수 있습니다. Reverb는 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지도 함께 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo를 설치하면 애플리케이션 자바스크립트에서 fresh Echo 인스턴스를 생성할 준비가 된 것입니다. Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단이 적합한 위치입니다. 기본적으로 이 파일에 Echo 구성 예제가 주석 처리되어 포함돼 있으니, 주석을 해제하고 `broadcaster` 옵션을 `'reverb'`로 변경하세요:

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

그 후 애플리케이션 자산을 컴파일합니다:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버의 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 수신하기 쉽게 해주는 자바스크립트 라이브러리입니다. Pusher 프로토콜 지원을 위해 `pusher-js` NPM 패키지도 활용합니다.

`install:broadcasting` Artisan 명령어는 자동으로 `laravel-echo`와 `pusher-js`를 설치하지만, NPM을 통해 수동 설치도 가능합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, 애플리케이션 자바스크립트에서 새로운 Echo 인스턴스를 생성할 준비가 됩니다. `install:broadcasting` 명령어는 `resources/js/echo.js` 파일에 Echo 구성을 생성하는데, 이 기본 구성은 Laravel Reverb 용입니다. 아래 예제 구성을 복사해 Pusher용으로 변경할 수 있습니다:

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

그 다음 `.env` 파일에 Pusher 환경 변수를 설정합니다. 해당 변수가 없으면 새로 추가하세요:

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

Echo 구성을 애플리케이션 요구에 맞게 조정한 뒤, 다시 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]
> 애플리케이션 자바스크립트 자산 컴파일에 관해 더 알고 싶다면 [Vite 문서](/docs/master/vite)를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 사전에 구성된 Pusher 클라이언트 인스턴스가 있다면, Echo에 `client` 옵션을 전달하여 활용할 수 있습니다:

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
> 아래 문서는 Ably를 "Pusher 호환" 모드로 사용하는 방법을 설명합니다. Ably 팀은 Ably의 고유 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 별도로 유지 관리하며, 자세한 내용은 [Ably Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스팅 드라이버에서 브로드캐스트되는 이벤트 채널 구독과 수신을 간편하게 도와주는 자바스크립트 라이브러리입니다. Echo는 Pusher 프로토콜을 지원하기 위해 `pusher-js` NPM 패키지도 사용합니다.

`install:broadcasting` Artisan 명령어가 자동으로 `laravel-echo`와 `pusher-js`를 설치하지만, 직접 NPM으로 설치할 수도 있습니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**먼저, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. Ably 설정 대시보드의 "Protocol Adapter Settings" 영역에서 활성화할 수 있습니다.**

Echo를 설치한 후, 애플리케이션 자바스크립트에서 새로운 Echo 인스턴스를 생성할 준비가 되었습니다. `install:broadcasting` 명령어는 기본적으로 Reverb용 Echo 구성 파일을 `resources/js/echo.js`에 생성합니다. Ably로 전환할 때는 아래 예제를 참고해 구성을 변경하세요:

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

위 예제에서 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키이며, Ably 키에서 `:` 앞부분입니다.

Echo 구성을 조정한 후, 애플리케이션 자산을 컴파일합니다:

```shell
npm run dev
```

> [!NOTE]
> 애플리케이션 자바스크립트 자산 컴파일 관련 자세한 내용은 [Vite 문서](/docs/master/vite)를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel 이벤트 브로드캐스팅은 서버 측 Laravel 이벤트를 드라이버 기반 WebSocket 방식을 사용해 클라이언트 자바스크립트 앱으로 브로드캐스트합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com)를 기본 드라이버로 제공합니다. 클라이언트는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 사용해 쉽게 이벤트를 수신할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트되며, 공개(public) 또는 비공개(private)로 지정할 수 있습니다. 공개 채널은 누구나 인증 없이 구독할 수 있으나, 비공개 채널은 사용자 인증과 권한 부여를 거쳐야 구독할 수 있습니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

브로드캐스팅의 각 구성요소를 살펴보기 전에, 전자상거래 스토어 예제를 통해 전체 개념을 간단히 설명합니다.

우리 애플리케이션에는 사용자가 주문 배송 상태를 볼 수 있는 페이지가 있다고 가정합시다. 그리고 `OrderShipmentStatusUpdated` 이벤트가 배송 상태가 업데이트될 때 발생한다고 합시다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 페이지를 보면서 상태 업데이트를 위해 페이지를 새로고침하지 않도록, 업데이트가 생성되는 즉시 애플리케이션에 브로드캐스트하고자 합니다. 따라서 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현하여, 자동으로 이벤트가 발생할 때 브로드캐스트 되도록 합니다:

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

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트할 채널을 반환합니다. 생성된 이벤트 클래스에는 이미 빈 메서드가 있으므로 내용을 채우기만 하면 됩니다. 주문을 생성한 사용자만 상태 업데이트를 볼 수 있도록, 주문에 연동된 비공개 채널에서 이벤트를 브로드캐스트합니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트 할 채널을 반환합니다.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

다수 채널에 브로드캐스트하려면 `array`로 반환할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트할 채널들.
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

비공개 채널이므로 구독자는 권한 검증을 받아야 합니다. 권한 검사 로직은 `routes/channels.php` 파일에서 정의합니다. 이 예제에서는 `orders.{orderId}` 비공개 채널을 구독하려는 사용자가 실제 해당 주문 생성자인지 확인합니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 첫 번째 인자로 채널 이름, 두 번째 인자로 사용자가 채널을 구독할 권한이 있는지 `true` 또는 `false`를 반환하는 콜백을 받습니다.

권한 콜백은 현재 인증된 사용자를 첫 번째 인자로 받고, 와일드카드 매개변수를 추가 인자로 받습니다. 예제에서는 `{orderId}` 부분이 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신 대기

자바스크립트 애플리케이션에서 이벤트를 수신 대기만 하면 됩니다. Laravel Echo를 사용해 `private` 메서드로 비공개 채널을 구독하고, `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 청취합니다. 기본적으로 이벤트의 모든 public 속성이 브로드캐스트 페이로드에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의하기

Laravel에 이벤트를 브로드캐스트하라고 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 기본 포함되어 있으므로 간단히 추가할 수 있습니다.

`ShouldBroadcast`는 단일 메서드 `broadcastOn` 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트할 채널(`Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스) 또는 채널 배열을 반환해야 합니다. `Channel`은 누구나 구독할 수 있는 공개 채널, `PrivateChannel`과 `PresenceChannel`은 인증이 필요한 비공개 채널입니다.

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
     * 새 이벤트 인스턴스 생성.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 이벤트가 브로드캐스트할 채널 반환.
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

`ShouldBroadcast`를 구현한 후에는 평소처럼 [이벤트를 발동](/docs/master/events)하기만 하면 됩니다. 발동 시 [큐드 잡](/docs/master/queues)이 자동으로 이벤트를 브로드캐스트하도록 처리합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스 이름을 이벤트 이름으로 사용하지만, 이벤트클래스에 `broadcastAs` 메서드를 정의해 브로드캐스트 이름을 커스텀할 수 있습니다:

```php
/**
 * 이벤트의 브로드캐스트 이름 정의.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`를 사용해 이름을 변경했다면, Echo에서는 이벤트 이름 앞에 `.`을 붙여 리스너를 등록해야 합니다. 그러면 Echo가 네임스페이스를 자동으로 붙이지 않습니다:

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때 모든 `public` 속성이 자동 직렬화되어 이벤트 페이로드로 전달됩니다. 예를 들어 이벤트에 `$user`라는 단일 public 속성에 Eloquent 모델이 있다면 다음과 같은 JSON이 전송됩니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

보다 세밀하게 브로드캐스트 페이로드를 제어하려면 `broadcastWith` 메서드를 이벤트에 추가할 수 있습니다. 이 메서드는 브로드캐스트할 데이터를 배열로 반환해야 합니다:

```php
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

기본적으로 브로드캐스트 이벤트는 `queue.php` 설정 파일에 정의된 기본 큐 및 연결에서 실행됩니다. 이벤트 클래스에 `connection`과 `queue` 속성을 정의해 큐 연결과 이름을 지정할 수 있습니다:

```php
/**
 * 브로드캐스트 이벤트를 처리할 큐 연결명.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스팅 잡이 넣어질 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드로 큐 이름을 지정할 수도 있습니다:

```php
/**
 * 브로드캐스트 잡이 넣어질 큐 이름 반환.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

기본 큐 드라이버 대신 동기(sync) 큐를 사용하려면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요:

```php
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
### 브로드캐스트 조건

특정 조건이 충족될 때만 이벤트를 브로드캐스트하고 싶으면, 이벤트 클래스에 `broadcastWhen` 메서드를 정의할 수 있습니다:

```php
/**
 * 이벤트를 브로드캐스트할지 여부 결정.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내부에서 이벤트 브로드캐스트가 실행되면, 처리 큐 작업이 데이터베이스 커밋 전에 실행될 수 있습니다. 이런 경우 모델이나 데이터베이스 레코드 변경 내용이 데이터베이스에 반영되지 않았을 수 있고, 새로운 레코드는 존재하지 않을 수 있습니다. 이로 인해 브로드캐스트 작업 처리 시 예기치 않은 오류가 발생할 수 있습니다.

큐 연결 설정 중 `after_commit`이 `false`로 되어 있으면, 특별히 이 문제를 해결하기 위해 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현해 트랜잭션 커밋 후에만 이벤트가 브로드캐스트되도록 할 수 있습니다:

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
> 관련 문제 해결 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여하기

비공개 채널은 현재 인증된 사용자가 해당 채널을 구독할 권한이 있는지 확인해야 합니다. 애플리케이션에 HTTP 요청을 보내 채널 이름을 함께 전달하면, Laravel에서 권한 검사 후 허용 여부를 결정합니다. Laravel Echo를 사용하면, 비공개 채널 구독 권한 확인용 HTTP 요청을 자동으로 처리합니다.

브로드캐스팅이 활성화되면 Laravel은 `/broadcasting/auth` 라우트를 자동 등록하여 권한 요청을 처리합니다. 이 라우트는 `web` 미들웨어 그룹에 속합니다.

<a name="defining-authorization-callbacks"></a>
### 권한 콜백 정의하기

이제 실제로 인증된 사용자가 채널 구독 권한이 있는지 결정하는 로직을 작성해야 합니다. `install:broadcasting` 명령어가 만든 `routes/channels.php` 파일에서 `Broadcast::channel` 메서드로 권한 콜백을 등록합니다:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 권한 여부를 `true` 또는 `false`로 반환하는 콜백을 받습니다.

권한 콜백의 첫 번째 인자는 현재 인증된 사용자이며, 그 후에 와일드카드 값이 추가 인자로 전달됩니다. 위 예제에서 `{orderId}`는 와일드카드임을 나타냅니다.

애플리케이션의 모든 브로드캐스트 권한 콜백 목록은 Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 권한 콜백 모델 바인딩

HTTP 라우팅과 마찬가지로, 채널 라우트도 암묵적 및 명시적 [라우트 모델 바인딩](/docs/master/routing#route-model-binding)을 지원합니다. 예를 들어, 주문 ID 대신 실제 `Order` 모델 인스턴스를 받을 수도 있습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [암묵적 모델 바인딩 스코핑](/docs/master/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 그러나 대부분의 채널은 단일 모델의 고유 기본 키를 기준으로 스코핑하기 때문에 큰 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 권한 콜백 인증

비공개 및 프레즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 인증되지 않은 사용자에 대해선 권한이 자동 부여되지 않으며, 권한 콜백도 호출되지 않습니다. 필요하면 다중 맞춤 가드를 지정할 수도 있습니다:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

채널이 많아지면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 이때 클로저 대신 채널 클래스를 사용할 수 있습니다. `make:channel` Artisan 명령어를 이용해 채널 클래스를 생성하면 `App/Broadcasting` 디렉토리에 새로운 클래스를 만듭니다:

```shell
php artisan make:channel OrderChannel
```

생성한 채널 클래스를 `routes/channels.php`에 등록합니다:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스의 `join` 메서드에 권한 로직을 작성합니다. 이는 기존 클로저에 작성하던 코드와 동일한 역할을 하며, 모델 바인딩도 활용할 수 있습니다:

```php
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
     * 사용자의 채널 접속 권한 검사.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Laravel의 다른 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/master/container)에 의해 자동 해결되므로 생성자에 필요한 의존성을 타입힌트할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

`ShouldBroadcast` 인터페이스를 구현한 이벤트를 생성했다면, 단순히 이벤트의 `dispatch` 메서드를 호출해 이벤트를 발동하세요. 이벤트 디스패처가 인터페이스를 인지하고 자동으로 큐에 브로드캐스트 작업을 등록합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 본인 제외하기

가끔 동일 채널 구독자 중 현재 사용자 자신 제외하고 브로드캐스트하려는 경우가 있습니다. `broadcast` 헬퍼와 `toOthers` 메서드를 함께 사용할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어, 작업 리스트 애플리케이션에서 사용자가 새 작업을 생성하고 `/task` 경로에 POST 요청을 보냈다고 가정합시다. 이 요청은 작업 생성 후 작업 생성 이벤트를 브로드캐스트하고 새 작업을 JSON으로 응답합니다. 자바스크립트가 응답을 받아 바로 작업 리스트에 추가합니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만 작업 생성 이벤트가 별도로 broadcast되어 있다면, 자바스크립트는 동일 작업을 중복해서 두 번 추가하게 됩니다. 이 문제를 `toOthers` 메서드로 현재 사용자에게는 브로드캐스트하지 않도록 해결할 수 있습니다.

> [!WARNING]
> `toOthers` 메서드를 사용하려면 이벤트에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 포함되어 있어야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스 생성 시, 각 연결에 소켓 ID가 할당됩니다. Axios 같은 글로벌 HTTP 클라이언트 인스턴스를 사용하는 경우, 모든 HTTP 요청에 `X-Socket-ID` 헤더가 자동으로 추가됩니다. `toOthers`를 호출하면 Laravel이 이 헤더에서 소켓 ID를 추출하고 현재 클라이언트에게는 브로드캐스트하지 않도록 지시합니다.

글로벌 Axios 인스턴스를 사용하지 않는다면, 직접 HTTP 요청에 `X-Socket-ID` 헤더를 추가해야 하며, 소켓 ID는 다음과 같이 가져올 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 맞춤 설정하기

여러 브로드캐스트 연결을 사용하는 애플리케이션이라면 기본 브로드캐스트 연결 이외의 브로드캐스트 드라이버를 지정할 수 있습니다. `via` 메서드를 이용하세요:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 생성자 내부에서 `broadcastVia` 메서드를 호출하여 연결을 지정할 수 있습니다. 단, 이때는 이벤트 클래스가 `InteractsWithBroadcasting` 트레이트를 사용해야 합니다:

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

때로는 전용 이벤트 클래스를 만들지 않고 간단한 이벤트를 프론트엔드에 브로드캐스트할 수 있습니다. `Broadcast` 파사드를 사용해 "익명 이벤트"를 브로드캐스트할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예제는 다음과 같은 이벤트를 브로드캐스트합니다:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as` 및 `with` 메서드를 사용해 이벤트 이름과 데이터를 변경할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

다음은 브로드캐스트 예입니다:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

비공개 또는 프레즌스 채널에서 익명 이벤트를 브로드캐스트하려면 `private` 또는 `presence` 메서드를 사용하세요:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 이벤트를 큐에 넣어 비동기 처리하지만, 즉시 브로드캐스트하려면 `sendNow`를 사용합니다:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 사용자 제외하고 이벤트를 브로드캐스트하려면 `toOthers`를 호출합니다:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 수신 대기

[Laravel Echo 설치 및 인스턴스 생성](#client-side-installation)이 완료되면, Laravel에서 브로드캐스트하는 이벤트를 수신할 준비가 된 것입니다. `channel` 메서드로 채널 인스턴스를 얻고, `listen` 메서드로 특정 이벤트를 청취합니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 이벤트를 듣는다면 `private` 메서드를 대신 사용하세요. 한 채널에서 여러 이벤트를 중첩해 청취할 수도 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중지

특정 이벤트에 대해 수신을 멈추고 싶다면(채널은 그대로 구독), `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 완전히 나가려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출합니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 연관된 비공개 및 프레즌스 채널까지 모두 나가려면 `leave` 메서드를 사용하세요:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위 예시에서 이벤트 클래스의 완전한 `App\Events` 네임스페이스를 지정하지 않았습니다. Echo는 기본적으로 `App\Events` 네임스페이스를 가정해서입니다. Echo 인스턴스 생성 시 `namespace` 옵션으로 기본 네임스페이스를 설정할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

별도로 이벤트 클래스 이름 앞에 `.`을 붙여 구독하면 항상 전체 클래스명을 지정할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## 프레즌스 채널

프레즌스 채널은 비공개 채널의 보안성을 유지하면서 구독자 정보를 노출하는 기능을 더한 채널입니다. 같은 페이지를 동시에 보는 사용자 알림, 채팅방 사용자 목록 표시 등의 협업 기능 구현에 유용합니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 권한 부여

프레즌스 채널도 비공개 채널이므로 권한 부여가 필요하지만, 권한 콜백에선 `true` 대신 사용자 정보를 담은 배열을 반환해야 합니다. 반환된 정보는 자바스크립트 이벤트 리스너가 접근할 수 있습니다. 권한 없을 경우 `false` 또는 `null`을 반환하세요:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여

Echo의 `join` 메서드로 프레즌스 채널에 참가할 수 있으며, 반환값인 `PresenceChannel`은 `listen` 메서드 뿐 아니라 `here`, `joining`, `leaving` 이벤트 구독도 지원합니다:

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

- `here`: 채널 참여 즉시 호출되어 현재 구독 중인 사용자 배열을 전달
- `joining`: 새 사용자가 참여할 때 호출
- `leaving`: 사용자가 나갈 때 호출
- `error`: 인증 실패 등 오류 발생 시 호출

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅

프레즌스 채널도 공개 및 비공개 채널과 마찬가지로 이벤트를 받아 브로드캐스트할 수 있습니다. 예를 들어 채팅방의 `NewMessage` 이벤트는 `PresenceChannel` 인스턴스를 반환하는 `broadcastOn` 메서드로 채널에 전송합니다:

```php
/**
 * 이벤트가 브로드캐스트할 채널 반환.
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

예시와 마찬가지로 `broadcast` 헬퍼와 `toOthers`를 사용해 현재 사용자 제외 브로드캐스트도 가능합니다:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

프레즌스 채널에는 Echo의 `listen` 메서드로 이벤트를 수신할 수 있습니다:

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
> 모델 브로드캐스팅에 대한 아래 문서를 읽기 전에 Laravel 모델 브로드캐스팅 개념과 수동으로 브로드캐스트 이벤트를 생성·수신하는 방법을 숙지할 것을 권장합니다.

Eloquent 모델이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하는 일이 흔합니다. 물론 직접 관련 이벤트 클래스를 만들어 `ShouldBroadcast`를 구현해 처리할 수도 있습니다.

하지만 이벤트를 브로드캐스트용으로만 사용하는 경우 이벤트 클래스를 따로 만드는 것은 번거롭습니다. 이를 해결할 방법으로, Laravel은 Eloquent 모델이 상태가 변할 때 자동으로 브로드캐스트하도록 지정할 수 있습니다.

먼저 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 적용하고, `broadcastOn` 메서드를 정의해서 모델 이벤트가 브로드캐스트할 채널을 반환해야 합니다:

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
     * 게시글의 작성자 관계 정의.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트할 채널 반환.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

트레이트를 적용하고 `broadcastOn`을 정의하면, 모델 인스턴스가 생성, 수정, 삭제, 휴지통 처리, 복구될 때 자동으로 이벤트가 브로드캐스트됩니다.

`broadcastOn` 메서드는 문자열 `$event` 인자를 받으며, 이벤트 종류(`created`, `updated`, `deleted`, `trashed`, `restored`)가 전달됩니다. 이 값을 보고 특정 이벤트별로 채널을 달리 반환할 수도 있습니다:

```php
/**
 * 모델 이벤트가 브로드캐스트할 채널 반환.
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
#### 모델 브로드캐스팅 이벤트 생성 맞춤 설정

가끔 Laravel이 내부적으로 생성하는 모델 브로드캐스트 이벤트를 커스텀하고 싶다면, 모델에 `newBroadcastableEvent` 메서드를 정의해 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환할 수 있습니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델용 새로운 브로드캐스트 가능한 이벤트 생성.
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

위 모델 예제의 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않고 모델 인스턴스를 반환하는 것을 볼 수 있습니다. 이 경우, Laravel은 모델의 클래스명과 기본 키를 조합해 비공개 채널을 자동 생성합니다.

예컨대 `App\Models\User` 클래스의 `id`가 `1`인 모델은 `App.Models.User.1`이라는 이름의 `PrivateChannel` 인스턴스로 변환됩니다. `broadcastOn`에서 채널 인스턴스를 직접 반환하면 채널 이름을 완벽히 제어할 수 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트할 채널 반환.
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

채널 인스턴스 생성 시 모델 인스턴스를 매개변수로 전달하면 Laravel이 내부적으로 이름 규칙에 따라 채널명으로 변환합니다:

```php
return [new Channel($this->user)];
```

모델 채널 이름을 확인하려면 모델 인스턴스에서 `broadcastChannel` 메서드를 호출하면 됩니다. 예를 들어, ID가 1인 `App\Models\User` 모델의 채널명은 `App.Models.User.1`으로 반환됩니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 `App\Events` 디렉토리에 실제 이벤트가 없으므로 명명 규칙과 페이로드 형식을 적용합니다. Laravel은 모델 클래스 이름(네임스페이스 제외)과 모델 이벤트 이름을 조합해 이벤트 이름을 만듭니다.

예를 들어 `App\Models\Post` 모델 수정 시 클라이언트에 `PostUpdated` 이벤트가 보내지고, 페이로드는 다음과 유사합니다:

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

`App\Models\User` 모델 삭제는 `UserDeleted` 이벤트가 브로드캐스트됩니다.

필요하다면 `broadcastAs`, `broadcastWith` 메서드로 각 모델 이벤트별로 이름과 페이로드를 커스텀할 수 있습니다. `broadcastAs`가 `null`을 반환하면 기본 규칙을 따릅니다:

```php
/**
 * 모델 이벤트의 브로드캐스트 이름 지정.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델 브로드캐스트 페이로드 반환.
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
### 모델 브로드캐스트 수신 대기

모델에 `BroadcastsEvents` 트레이트와 `broadcastOn` 메서드를 추가했다면, 클라이언트에서 방송된 모델 이벤트를 청취할 준비가 된 것입니다. 먼저 [이벤트 수신 대기](#listening-for-events) 문서를 참고하세요.

`private` 메서드로 채널 인스턴스를 얻은 뒤, 모델 브로드캐스팅 규칙에 따라 채널명으로 지정한 뒤 특정 이벤트를 `listen`하세요. 모델 브로드캐스트 이벤트는 `App\Events` 네임스페이스에 실제 존재하지 않으므로 이벤트 이름 앞에 `.`을 붙여 네임스페이스 없음 표시를 해야 합니다. 각 이벤트에 `model` 속성이 포함되어 브로드캐스트 가능한 모델 데이터를 담고 있습니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels) 사용 시, [Pusher 대시보드](https://dashboard.pusher.com/)의 애플리케이션 설정에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트 전송이 가능합니다.

서버를 거치지 않고 연결된 다른 클라이언트에게 이벤트를 브로드캐스트하는 기능도 있습니다. 예를 들어 "입력 중" 알림과 같이 다른 사용자가 메시지 입력 중인 걸 알릴 때 유용합니다.

클라이언트 이벤트는 Echo의 `whisper` 메서드를 사용해 브로드캐스트합니다:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트 수신은 `listenForWhisper` 메서드를 이용합니다:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅과 [알림 시스템](/docs/master/notifications)을 결합하면, 페이지 새로고침 없이도 실시간으로 자바스크립트 애플리케이션에서 새 알림을 받을 수 있습니다. 시작 전에 [브로드캐스트 알림 채널](/docs/master/notifications#broadcast-notifications) 문서를 먼저 숙지하세요.

알림이 브로드캐스트 채널로 전송되도록 설정했다면, Echo의 `notification` 메서드로 수신할 수 있습니다. 채널 이름은 알림을 받는 엔티티 클래스 이름과 일치해야합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

예제에서는 `App\Models\User` 인스턴스에 방송 채널로 전송된 모든 알림을 콜백으로 받습니다. 이 채널에 대한 권한 부여 콜백은 `routes/channels.php` 파일에 포함되어 있습니다.