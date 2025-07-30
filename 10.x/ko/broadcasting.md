# 방송 (Broadcasting)

- [소개](#introduction)
- [서버 사이드 설치](#server-side-installation)
    - [설정](#configuration)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [오픈 소스 대안](#open-source-alternatives)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스트와 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인증](#authorizing-channels)
    - [인증 라우트 정의하기](#defining-authorization-routes)
    - [인증 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 방송하기](#broadcasting-events)
    - [현재 사용자를 제외한 나머지에게 방송하기](#only-to-others)
    - [연결 설정 맞춤화하기](#customizing-the-connection)
- [방송 수신하기](#receiving-broadcasts)
    - [이벤트 청취하기](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
- [프레즌스 채널 (Presence Channels)](#presence-channels)
    - [프레즌스 채널 인증](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 방송하기](#broadcasting-to-presence-channels)
- [모델 방송 (Model Broadcasting)](#model-broadcasting)
    - [모델 방송 규칙](#model-broadcasting-conventions)
    - [모델 방송 청취하기](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

현대 웹 애플리케이션에서는 사용자 인터페이스를 실시간으로 업데이트하기 위해 WebSocket을 많이 사용합니다. 서버에서 데이터가 변경되면 메시지가 WebSocket 연결을 통해 클라이언트로 전송되고 클라이언트에 의해 처리됩니다. WebSocket은 UI에 반영되어야 하는 데이터 변경 사항을 계속해서 서버에 요청하는 폴링 방식보다 훨씬 효율적인 대안입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내고 이를 이메일로 보내는 기능이 있다고 가정해봅시다. CSV 파일 생성에 몇 분이 걸리기 때문에 CSV 생성과 메일 발송을 [큐드 작업](/docs/10.x/queues)으로 처리합니다. CSV 생성과 메일 발송이 완료되면 `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션의 자바스크립트가 이를 수신하게 합니다. 이벤트가 수신되면 사용자는 페이지를 새로고침하지 않고도 CSV가 이메일로 전송되었다는 메시지를 볼 수 있습니다.

이러한 기능을 쉽게 구현할 수 있도록 Laravel은 서버 사이드 Laravel [이벤트](/docs/10.x/events)를 WebSocket 연결을 통해 "브로드캐스트"할 수 있는 편의 기능을 제공합니다. Laravel 이벤트를 브로드캐스트하면 서버 사이드 Laravel 애플리케이션과 클라이언트 사이드 자바스크립트 애플리케이션 간에 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 이름이 지정된 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 이 채널들로 이벤트를 브로드캐스트합니다. 이때 이벤트에 포함하고 싶은 추가 데이터를 담을 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 다음 세 개의 서버 사이드 방송 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]  
> 이벤트 브로드캐스팅을 시작하기 전, Laravel의 [이벤트와 리스너](/docs/10.x/events) 문서를 먼저 숙지하세요.

<a name="server-side-installation"></a>
## 서버 사이드 설치

Laravel 이벤트 브로드캐스팅을 시작하려면 Laravel 애플리케이션 내에서 설정 작업과 함께 몇 개의 패키지를 설치해야 합니다.

이벤트 방송은 서버 사이드 방송 드라이버가 담당하며, 이 드라이버는 Laravel 이벤트를 브로드캐스트하여 브라우저 클라이언트에서 Laravel Echo(자바스크립트 라이브러리)가 이를 수신할 수 있게 합니다. 걱정 마세요. 설치 과정 각 단계를 차근차근 설명합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 모든 이벤트 방송 설정은 `config/broadcasting.php` 파일에 저장되어 있습니다. Laravel은 기본적으로 여러 방송 드라이버를 지원합니다: [Pusher Channels](https://pusher.com/channels), [Redis](/docs/10.x/redis), 그리고 로컬 개발 및 디버깅용 `log` 드라이버가 있습니다. 또한 테스트 시 방송을 완전히 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 이 드라이버별 설정 예는 모두 `config/broadcasting.php`에 포함되어 있습니다.

<a name="broadcast-service-provider"></a>
#### Broadcast 서비스 프로바이더

브로드캐스트를 사용하기 위해서는 먼저 `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. Laravel의 새 애플리케이션에서는 `config/app.php` 파일의 `providers` 배열에서 이 프로바이더의 주석을 해제하는 것만으로 충분합니다. 이 `BroadcastServiceProvider`에는 브로드캐스트 인증 라우트와 콜백을 등록하는 코드가 포함되어 있습니다.

<a name="queue-configuration"></a>
#### 큐 설정

또한 [큐 워커](/docs/10.x/queues)를 구성하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐드 작업을 통해 이루어져야 애플리케이션 응답 속도가 이벤트 방송 때문에 심각하게 느려지지 않습니다.

<a name="reverb"></a>
### Reverb

Composer 패키지 매니저를 통해 Reverb를 설치할 수 있습니다:

```sh
composer require laravel/reverb
```

패키지를 설치한 후에는 Reverb의 설치 명령을 실행하여 설정 파일을 발행하고 애플리케이션의 방송 설정을 업데이트하며 Reverb의 필요한 환경 변수를 추가할 수 있습니다:

```sh
php artisan reverb:install
```

상세한 Reverb 설치 및 사용법은 [Reverb 문서](/docs/10.x/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels)를 사용하여 이벤트를 방송할 계획이라면 Composer를 통해 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 파일에서 Pusher Channel 인증 정보를 설정해야 합니다. 이 파일에는 이미 예제 설정이 포함되어 있어 키, 시크릿, 애플리케이션 ID를 빠르게 지정할 수 있습니다. 보통 이 값들은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID` [환경 변수](/docs/10.x/configuration#environment-configuration)로 설정합니다:

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

`config/broadcasting.php`의 `pusher` 설정에서는 클러스터 같은 Pusher Channels가 지원하는 추가 `options`도 지정할 수 있습니다.

그리고 `.env` 파일에서 방송 드라이버를 `pusher`로 변경하세요:

```ini
BROADCAST_DRIVER=pusher
```

마지막으로, 클라이언트 사이드에서 방송 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 되었습니다.

<a name="pusher-compatible-open-source-alternatives"></a>
#### Pusher 호환 오픈 소스 대안

[soketi](https://docs.soketi.app/)는 Laravel용으로 Pusher와 호환되는 WebSocket 서버를 제공합니다. 이를 사용하면 상업용 WebSocket 공급자 없이도 Laravel 브로드캐스팅 기능을 활용할 수 있습니다. 브로드캐스팅을 위한 오픈 소스 패키지 설치 및 사용법은 [오픈 소스 대안](#open-source-alternatives) 문서를 참조하세요.

<a name="ably"></a>
### Ably

> [!NOTE]  
> 아래 문서는 Ably를 "Pusher 호환" 모드로 사용하는 방법을 다룹니다. 하지만 Ably팀은 Ably 고유의 기능을 활용할 수 있는 별도의 브로드캐스터와 Echo 클라이언트도 관리하고 권장합니다. Ably가 관리하는 드라이버 사용법에 관한 자세한 내용은 [Ably Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 사용해 이벤트를 방송하려면 Composer를 통해 Ably PHP SDK를 설치해야 합니다:

```shell
composer require ably/ably-php
```

다음으로 `config/broadcasting.php` 설정 파일에서 Ably 인증 정보를 설정하세요. 이 파일에는 키를 쉽게 지정할 수 있는 예제 설정이 포함되어 있습니다. 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/10.x/configuration#environment-configuration)를 통해 설정합니다:

```ini
ABLY_KEY=your-ably-key
```

그 다음, `.env` 파일에서 방송 드라이버를 `ably`로 변경하세요:

```ini
BROADCAST_DRIVER=ably
```

마지막으로 [Laravel Echo](#client-side-installation)를 설치하고 설정하여 클라이언트 측에서 방송 이벤트를 받도록 준비하세요.

<a name="open-source-alternatives"></a>
### 오픈 소스 대안

<a name="open-source-alternatives-node"></a>
#### Node

[Soketi](https://github.com/soketi/soketi)는 Node 기반으로 Laravel용 Pusher 호환 WebSocket 서버를 제공합니다. 속도와 확장성 면에서 µWebSockets.js를 활용합니다. 이 패키지를 사용하면 상업용 WebSocket 공급자 없이 Laravel 브로드캐스팅을 자유롭게 사용할 수 있습니다. 설치 및 사용법은 공식 문서인 [Soketi 문서](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 방송 드라이버로부터 브로드캐스트된 이벤트를 구독하고 듣기 쉽게 만드는 자바스크립트 라이브러리입니다. NPM을 통해 Echo를 설치할 수 있습니다. 이 예제에서는 Reverb가 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지도 함께 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면 애플리케이션의 자바스크립트에 새로운 Echo 인스턴스를 생성할 준비가 된 것입니다. Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일 하단에 작성하는 것이 좋습니다. 기본적으로 이 파일에는 Echo 설정 예제가 주석 처리되어 있으니 주석을 해제하고 `broadcaster`를 `reverb`로 수정하세요:

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
> Laravel Echo의 `reverb` 방송기는 laravel-echo 버전 1.16.0 이상을 필요로 합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 방송 드라이버가 브로드캐스트한 이벤트를 구독하기 쉽게 만들어주는 자바스크립트 라이브러리입니다. NPM으로 Echo를 설치할 수 있습니다. 이 예에서는 Pusher Channels 방송기를 사용하기 때문에 `pusher-js`도 함께 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, Laravel에서 제공하는 `resources/js/bootstrap.js` 파일 하단에 새로운 Echo 인스턴스를 생성할 준비가 되었습니다. 기본 예제가 주석 처리되어 있으니 주석을 해제하세요:

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

필요에 맞게 Echo 설정을 수정하고 주석을 해제한 후, 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]  
> 애플리케이션의 자바스크립트 자산 컴파일에 대해 더 알고 싶다면 [Vite 문서](/docs/10.x/vite)를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 이미 구성된 클라이언트 인스턴스 사용

만약 Pusher Channels용으로 미리 구성된 클라이언트 인스턴스가 있다면, Echo 초기화 시 `client` 설정 옵션으로 전달할 수 있습니다:

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
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 설명합니다. 그러나 Ably팀은 Ably 고유 기능을 활용할 수 있는 별도의 브로드캐스터 및 Echo 클라이언트도 제공합니다. Ably 공식 Laravel 브로드캐스터 문서(https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 방송 드라이버가 브로드캐스트한 이벤트를 구독하기 쉽게 도와주는 자바스크립트 라이브러리입니다. NPM으로 Echo를 설치할 수 있으며, 이 예에서는 `pusher-js`도 함께 설치합니다.

Ably를 사용하지만 왜 `pusher-js`를 설치하냐고 의아할 수 있습니다. 다행히도 Ably는 Pusher 호환 모드를 제공하여, 클라이언트 애플리케이션에서 Pusher 프로토콜로 이벤트를 수신할 수 있게 해줍니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 설정은 Ably 애플리케이션 대시보드의 "Protocol Adapter Settings" 섹션에서 켤 수 있습니다.**

Echo가 설치되면 애플리케이션 자바스크립트에 새로운 Echo 인스턴스를 생성할 준비가 됩니다. Laravel에 포함된 `resources/js/bootstrap.js` 파일 하단에 추가하는 것이 좋습니다. 기본 `bootstrap.js` 파일 예제는 Pusher용 설정이므로, 아래 구성으로 복사하여 Ably용으로 전환하세요:

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

위 설정에서 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키 값이어야 합니다. Ably 키 중 `:` 앞부분이 공개 키입니다.

설정을 수정한 후 애플리케이션 자산을 컴파일하세요:

```shell
npm run dev
```

> [!NOTE]  
> 자바스크립트 자산 컴파일에 대해 더 배우고 싶다면 [Vite 문서](/docs/10.x/vite)를 참조하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel 이벤트 방송은 드라이버 기반 WebSocket 방식을 통해 서버 측 Laravel 이벤트를 클라이언트 측 자바스크립트 애플리케이션에 방송합니다. 현재 Laravel은 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.com) 드라이버를 제공합니다. 이벤트는 클라이언트에서 [Laravel Echo](#client-side-installation) 자바스크립트 패키지로 쉽게 수신할 수 있습니다.

이벤트는 "채널"을 통해 방송합니다. 채널은 공개(public) 또는 비공개(private)를 지정할 수 있습니다. 공개 채널은 인증 없이 누구나 구독할 수 있지만, 비공개 채널 구독을 위해서는 인증과 인가가 반드시 필요합니다.

> [!NOTE]  
> Pusher의 오픈 소스 대안을 살펴보고 싶다면 [오픈 소스 대안](#open-source-alternatives)을 참고하세요.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용

본격적으로 이벤트 브로드캐스팅 구성요소를 살펴보기 전에, 전자상거래 예시를 통해 간략히 개념을 살펴봅시다.

예를 들어 사용자가 주문의 배송 상태를 보는 페이지가 있다고 가정합니다. 배송 상태가 업데이트되면 `OrderShipmentStatusUpdated` 이벤트가 애플리케이션에서 발행됩니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문을 보는 도중 페이지 새로고침 없이 실시간으로 상태 업데이트를 보길 원합니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. Laravel에게 이 이벤트가 발행될 때 방송하도록 지시하는 역할을 합니다:

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

`ShouldBroadcast` 인터페이스는 이벤트 클래스에 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 방송될 채널을 반환해야 합니다. 생성된 이벤트 클래스에 빈 메서드 스텁이 이미 있으니 내용을 채워 넣으세요. 주문 생성자만 상태 업데이트를 볼 수 있게 하려면, 주문에 연결된 비공개 채널에 방송합니다:

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

이벤트를 여러 채널에 방송하려면 `array`로 반환할 수 있습니다:

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
#### 채널 인증

비공개 채널은 사용자 권한이 필요합니다. 애플리케이션의 `routes/channels.php` 파일에서 채널 권한 규칙을 정의할 수 있습니다. 아래 예는 `orders.{orderId}` 채널을 구독하려는 사용자가 실제 주문 생성자인지 확인합니다:

```
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인자를 받습니다: 채널 이름과 인증 여부를 반환하는 콜백 함수입니다.

모든 인증 콜백은 현재 인증된 사용자를 첫 인자로 받고, 채널 이름 내 와일드카드에 해당하는 추가 인자를 후속 인자로 받습니다. 위 예시에서는 `{orderId}`가 와일드카드 자리입니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 청취하기

다음으로, 자바스크립트 애플리케이션에서 이벤트를 듣기만 하면 됩니다. [Laravel Echo](#client-side-installation)를 사용해 비공개 채널을 구독하고, `listen` 메서드로 `OrderShipmentStatusUpdated` 이벤트를 청취하세요. 기본적으로 이벤트의 모든 공개 속성이 방송 페이로드에 포함됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의하기

Laravel에 특정 이벤트가 방송되어야 함을 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 Laravel의 이벤트 자동 생성 시 기본으로 포함되어 있어 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 `broadcastOn`이라는 단일 메서드 구현을 요구합니다. `broadcastOn` 메서드는 이벤트가 방송될 채널 또는 채널 배열을 반환해야 하며, 이 채널들은 `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스여야 합니다. `Channel` 인스턴스는 공개 채널을, `PrivateChannel` 및 `PresenceChannel`은 인증이 필요한 비공개 채널임을 나타냅니다:

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
     * 이벤트가 방송될 채널 반환.
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

`ShouldBroadcast` 인터페이스 구현 후에는 일반 이벤트처럼 [이벤트를 발행](/docs/10.x/events)하기만 하면 됩니다. 이벤트가 발행되면 [큐 작업](/docs/10.x/queues)이 자동으로 이벤트를 방송합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스명을 브로드캐스트 이벤트 이름으로 사용합니다. 하지만 이벤트 클래스에 `broadcastAs` 메서드를 정의해 이름을 변경할 수 있습니다:

```
/**
 * 브로드캐스트 이벤트 이름.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`로 이름을 변경하면, 이벤트 리스너 등록 시 이벤트 이름 앞에 `.` 문자를 붙여야 합니다. 이렇게 하면 Echo가 기본 애플리케이션 네임스페이스를 자동으로 붙이지 않습니다:

```
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 방송될 때, 모든 `public` 속성이 자동으로 직렬화되어 이벤트 페이로드로 포함됩니다. 이렇게 하여 자바스크립트 애플리케이션에서 공개 데이터를 접근할 수 있습니다. 예를 들어, 이벤트에 Eloquent 모델을 포함한 `$user` 공개 속성이 있으면 broadcast 페이로드는 다음과 같습니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

더 세밀하게 페이로드를 제어하고 싶다면, `broadcastWith` 메서드를 이벤트에 추가해 반환할 배열 형태의 데이터를 정의할 수 있습니다:

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

기본적으로 방송 이벤트는 `queue.php` 설정 파일에 명시된 기본 큐 연결과 큐 이름을 사용해 큐에 쌓입니다. 큐 연결 및 이름을 변경하려면 이벤트 클래스에 `connection`과 `queue` 속성을 정의하세요:

```
/**
 * 방송 시 사용할 큐 연결 이름.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 방송 작업을 넣을 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 이벤트에 `broadcastQueue` 메서드를 추가해 큐 이름을 반환할 수도 있습니다:

```
/**
 * 방송 작업을 넣을 큐 이름 반환.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

만약 기본 큐 대신 즉시 방송하려면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요:

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

특정 조건에서만 이벤트를 방송하고 싶으면, `broadcastWhen` 메서드를 정의하여 조건을 명시하세요:

```
/**
 * 이 이벤트를 방송할지 여부 결정.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 이벤트가 발행되면, 방송 작업이 트랜잭션 커밋 전에 큐에서 실행될 수 있습니다. 이 경우 트랜잭션 중 변경된 데이터가 DB에 아직 반영되어 있지 않거나 새로 생성된 모델이 DB에 존재하지 않을 수도 있습니다. 이로 인해 의도치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`라면, 특정 방송 이벤트에 대해 모든 데이터베이스 트랜잭션이 커밋된 뒤에 방송되도록 하려면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요:

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
> 큐 작업과 데이터베이스 트랜잭션 관련 문제 해결법은 [큐 작업과 데이터베이스 트랜잭션](/docs/10.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인증

비공개 채널에선 현재 인증된 사용자가 실제로 해당 채널을 구독할 권한이 있는지 인증해야 합니다. Laravel 앱에 채널 명과 함께 HTTP 요청을 보내 사용자 권한을 검증하는 방식입니다. [Laravel Echo](#client-side-installation)를 사용할 때 이 요청은 자동으로 처리되지만, 처리할 라우트를 정의해야 합니다.

<a name="defining-authorization-routes"></a>
### 인증 라우트 정의하기

다행히 Laravel은 채널 인증에 필요한 라우트를 쉽게 정의할 수 있습니다. 애플리케이션에 포함된 `App\Providers\BroadcastServiceProvider`에서 `Broadcast::routes` 메서드 호출을 찾을 수 있습니다. 이 메서드는 `/broadcasting/auth` 경로를 등록해 인증 요청을 처리합니다:

```
Broadcast::routes();
```

`Broadcast::routes`는 기본적으로 `web` 미들웨어 그룹 안에 라우트를 등록하지만, 원하는 경우 속성 배열을 넣어 커스터마이징할 수도 있습니다:

```
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>
#### 인증 엔드포인트 커스터마이징

기본적으로 Echo는 `/broadcasting/auth` 경로를 인증 엔드포인트로 사용합니다. 하지만 Echo 생성자에 `authEndpoint` 옵션을 넣어 인증 엔드포인트를 변경할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 인증 요청 커스터마이징

Echo가 인증 요청을 어떻게 수행할지 커스터마이징하려면 Echo 초기화 시 직접 authorizer를 정의할 수 있습니다:

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
### 인증 콜백 정의하기

이제 실제로 사용자가 특정 채널을 구독할 권한이 있는지 판단하는 로직을 정의해야 하는데, `routes/channels.php` 파일에서 `Broadcast::channel` 메서드를 사용해 채널 인증 콜백을 등록할 수 있습니다:

```
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과, 사용자가 권한이 있으면 `true`를, 없으면 `false`를 반환하는 콜백을 받습니다.

인증 콜백은 첫 번째 인자로 현재 인증된 사용자, 그 뒤 인자로는 채널 이름 와일드카드 패턴에 대응하는 추가 인자를 받습니다. 위 예제에서는 `{orderId}`가 와일드카드입니다.

`channel:list` Artisan 명령어로 애플리케이션에 등록된 방송 인증 콜백 목록을 볼 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인증 콜백 모델 바인딩

HTTP 라우트와 마찬가지로, 채널 라우트도 명시적 혹은 암묵적 [모델 바인딩](/docs/10.x/routing#route-model-binding)을 지원합니다. 예를 들어 문자열 ID 대신 실제 `Order` 모델 인스턴스를 인자로 받을 수 있습니다:

```
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]  
> HTTP 라우트에서 지원하는 암묵적 모델 바인딩 스코핑은 채널 바인딩에서는 자동 지원되지 않습니다. 대부분의 채널은 모델 고유 식별자 PK 기준으로 스코프가 가능하므로 보통 문제되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 인증 콜백 인증

비공개 채널과 프레즌스 채널은 앱 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않았다면 자동으로 권한 거부되며 콜백은 실행되지 않습니다. 여러 인증 가드를 지정할 수도 있습니다:

```
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션에서 여러 채널을 다룰 때 `routes/channels.php`에 인증 로직이 너무 많아질 수 있습니다. 이럴 때는 익명 함수 대신 채널 클래스를 사용하세요. 채널 클래스는 `make:channel` Artisan 명령어로 생성하며, `App/Broadcasting` 디렉토리에 배치됩니다:

```shell
php artisan make:channel OrderChannel
```

그 다음 `routes/channels.php`에 클래스를 등록합니다:

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스에 인증 논리는 `join` 메서드에 작성하며, 콜백에 했던 것과 같은 역할을 합니다. 모델 바인딩도 가능합니다:

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
    public function __construct()
    {
        // ...
    }

    /**
     * 채널 접근 인증 처리.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]  
> 채널 클래스도 Laravel [서비스 컨테이너](/docs/10.x/container)에 의해 자동으로 의존성 주입이 가능합니다. 필요한 의존성을 생성자에서 타입힌트하세요.

<a name="broadcasting-events"></a>
## 이벤트 방송하기

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현했으면, 일반적인 이벤트 발행 방식으로 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 `ShouldBroadcast`를 구현한 이벤트임을 인지하고 방송 큐 작업을 등록합니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 현재 사용자를 제외한 나머지에게만 방송하기

어떤 경우엔 현재 사용자를 제외한 동일 채널의 다른 사용자들에게만 이벤트를 방송하려 할 수 있습니다. 이럴 땐 `broadcast` 헬퍼와 `toOthers` 메서드를 사용합니다:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어, 할 일 목록 앱에서 사용자가 새 작업을 입력하면 `/task` 경로로 요청을 보내 작업을 생성하고, 생성된 작업 정보를 JSON으로 응답받아 클라이언트에서 즉시 화면에 추가합니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

한편, 작업 생성은 방송되기 때문에 클라이언트가 방송 이벤트도 듣고 있다면 작업 항목이 두 번 중복으로 추가될 수 있습니다. `toOthers`를 사용하면 현재 사용자에게는 방송하지 않도록 하여 이를 방지할 수 있습니다.

> [!WARNING]  
> 이벤트 클래스는 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 `toOthers` 메서드를 호출할 수 있습니다.

<a name="only-to-others-configuration"></a>
#### 구성

Echo 인스턴스가 초기화 될 때 소켓 ID가 지정됩니다. 만약 자바스크립트에서 글로벌 Axios 인스턴스를 사용해 HTTP 요청을 보내면, Axios는 자동으로 모든 요청에 `X-Socket-ID` 헤더를 추가합니다. 방송 시 `toOthers`를 호출하면 Laravel이 이 헤더에서 소켓 ID를 읽어 현재 사용자 연결에는 방송하지 않도록 합니다.

글로벌 Axios 인스턴스를 쓰지 않는다면, `Echo.socketId` 메서드로 소켓 ID를 직접 얻어 요청에 붙여야 합니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 설정 맞춤화하기

만약 애플리케이션이 여러 브로드캐스트 연결을 사용하면서 기본 방송기 이외의 다른 연결을 통해 이벤트를 방송하려면, `broadcast` 헬퍼의 `via` 메서드를 써서 연결 이름을 지정하세요:

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 클래스 내에서 `broadcastVia` 메서드를 호출해 방송 연결을 지정할 수 있습니다. 이때 이벤트 클래스에 `InteractsWithBroadcasting` 트레이트가 포함되어 있어야 합니다:

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

<a name="receiving-broadcasts"></a>
## 방송 수신하기

<a name="listening-for-events"></a>
### 이벤트 청취하기

[Laravel Echo 설치 및 초기화](#client-side-installation)를 마쳤으면, 이제 Laravel 애플리케이션에서 브로드캐스트된 이벤트를 청취할 준비가 된 것입니다. 채널 인스턴스를 얻으려면 `channel` 메서드를 사용하고, 특정 이벤트를 청취하려면 `listen` 메서드를 호출하세요:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 경우 `private` 메서드를 사용합니다. 하나의 채널에 대해 여러 이벤트를 듣고 싶다면 `listen` 메서드를 계속 체이닝해서 호출할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 특정 이벤트 청취 중지하기

만약 채널을 나가지 않고 특정 이벤트 청취만 중지하고 싶다면, `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 완전히 나가려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출하세요:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

비공개 및 프레즌스 채널을 포함해 채널과 관련된 모든 채널에서 나가려면 `leave` 메서드를 사용합니다:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

이전 예제를 보면 이벤트 클래스의 전체 네임스페이스인 `App\Events`를 지정하지 않았습니다. Echo는 기본적으로 `App\Events` 네임스페이스 하위에 이벤트가 있다고 가정하기 때문입니다. 만약 네임스페이스를 변경하고 싶다면 Echo 생성 시 `namespace` 설정 옵션을 추가하세요:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는, 이벤트 이름에 `.`를 붙여 항상 완전한 클래스명을 지정할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## 프레즌스 채널 (Presence Channels)

프레즌스 채널은 비공개 채널 보안 규칙을 기반으로 하면서도 현재 채널에 누가 구독 중인지 알려주는 기능을 추가합니다. 이를 통해 여러 사용자 간 동시에 페이지를 보고 있음을 알리거나, 채팅방 참여자 목록을 표시하는 등 협업 기능을 쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인증

프레즌스 채널 역시 비공개 채널이므로 [사용자 인증이 필요하며](#authorizing-channels) 권한을 검사하는 콜백을 정의해야 합니다. 다만 인증 콜백은 단순히 `true`를 반환하는 대신, 사용자의 추가 데이터를 배열로 반환해야 합니다.

이 데이터는 자바스크립트의 프레즌스 채널 이벤트 리스너에 전달됩니다. 허가되지 않았다면 `false`나 `null`을 반환하세요:

```
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여

Echo의 `join` 메서드를 사용해 프레즌스 채널에 참여할 수 있습니다. 이 메서드는 `PresenceChannel` 객체를 반환하며, `listen` 외에도 `here`, `joining`, `leaving` 이벤트를 구독할 수 있습니다:

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

- `here`: 채널 참가 시 즉시 호출되며, 현재 채널에 참여 중인 사용자 정보를 배열로 받음
- `joining`: 누군가 채널에 새로 들어왔을 때 호출
- `leaving`: 누군가 채널을 떠날 때 호출
- `error`: 인증 API가 200 이외의 응답을 할 때나 JSON 파싱 문제 발생 시 호출

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 방송하기

프레즌스 채널은 공개나 비공개 채널처럼 이벤트를 받을 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 방송하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하세요:

```
/**
 * 이벤트가 방송될 채널 반환.
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

`broadcast` 헬퍼와 `toOthers` 메서드를 사용하면 현재 사용자를 방송 대상에서 제외할 수 있습니다:

```
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Echo에서는 판단 채널의 `listen` 메서드로 프레즌스 채널 이벤트를 받을 수 있습니다:

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
## 모델 방송 (Model Broadcasting)

> [!WARNING]  
> 모델 방송 문서를 읽기 전에 Laravel 모델 방송 서비스 및 수동으로 이벤트를 생성하고 청취하는 방식을 익히는 것을 추천합니다.

애플리케이션에서 [Eloquent 모델](/docs/10.x/eloquent)이 생성, 수정, 삭제될 때 이벤트를 방송하는 것은 흔한 일입니다. 물론, 이 작업을 직접 [모델 상태 변경 이벤트](/docs/10.x/eloquent#events)로 정의하고, `ShouldBroadcast`를 구현해 방송할 수도 있습니다.

하지만 방송용 이벤트를 별도로 만드는 것이 번거롭다면, Laravel은 Eloquent 모델 자체가 상태 변경을 자동으로 방송하도록 설정할 수 있게 지원합니다.

시작하려면 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가해야 합니다. 또한 모델은 `broadcastOn` 메서드를 정의해야 하며, 이 메서드는 모델 이벤트가 방송될 채널 배열을 반환해야 합니다:

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
     * 게시물이 속한 사용자 모델 반환.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 방송될 채널 반환.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이제 모델에 이 트레이트와 `broadcastOn`이 정의되면, 생성, 수정, 삭제, 휴지통 처리, 복원 시 자동으로 방송 이벤트가 브로드캐스트됩니다.

또한 `broadcastOn` 메서드는 `$event`라는 문자열 인자를 받습니다. 이 인자는 발생한 모델 이벤트 종류로 ‘created’, ‘updated’, ‘deleted’, ‘trashed’, ‘restored’ 중 하나입니다. 이 값을 조건문에 활용하여 특정 이벤트에만 방송할 채널을 제어할 수 있습니다:

```php
/**
 * 모델 이벤트가 방송될 채널 반환.
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
#### 모델 방송 이벤트 생성 맞춤화

가끔 Laravel이 생성하는 방송 이벤트를 커스터마이징하고 싶을 경우, 모델에 `newBroadcastableEvent` 메서드를 정의해 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환할 수 있습니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델 브로드캐스트 이벤트 새로 생성.
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
#### 채널 규칙

예제 모델 `broadcastOn` 메서드에서 `Channel` 인스턴스 대신 Eloquent 모델을 직접 반환하는 것을 볼 수 있습니다. 만약 모델 인스턴스가 반환되면 Laravel은 모델 클래스명과 기본키를 이용해 자동으로 `PrivateChannel`을 생성합니다.

예를 들어, `App\Models\User` 중 `id`가 1인 모델은 `App.Models.User.1` 이름의 `PrivateChannel`로 변환됩니다. 물론 채널 이름을 완전히 제어하고자 하면 `broadcastOn`에서 명시적으로 `Channel` 인스턴스를 반환할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 방송될 채널 반환.
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

이때도 모델을 채널 생성자의 인자로 넣으면 위 모델 방송 규칙이 적용됩니다:

```php
return [new Channel($this->user)];
```

특정 모델의 방송 채널 이름을 알고 싶다면, `broadcastChannel` 메서드를 호출하세요. 예를 들어 `App\Models\User`의 경우 `App.Models.User.1` 문자열을 반환합니다:

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 방송 이벤트는 실제 애플리케이션 `App\Events` 디렉토리 내의 이벤트가 아니므로 이름과 페이로드가 규칙에 따라 할당됩니다. Laravel 규칙에 따르면, 모델 클래스명(네임스페이스 제외)과 모델 이벤트 이름을 조합하여 방송 이벤트명을 만듭니다.

예를 들어 `App\Models\Post` 모델이 수정되면 `PostUpdated` 이벤트가 방송되며, 페이로드는 다음과 같습니다:

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

`App\Models\User` 모델이 삭제되면 `UserDeleted` 이벤트가 방송됩니다.

원한다면 모델에 `broadcastAs`와 `broadcastWith` 메서드를 추가해 브로드캐스트 이름이나 페이로드를 직접 지정할 수 있습니다. 이 메서드들은 발생한 이벤트 이름을 인자로 받아, 각 작업별로 커스터마이징할 수 있습니다. `broadcastAs`가 `null`을 반환하면 기본 규칙 이름을 사용합니다:

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
 * 방송할 데이터 반환.
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
### 모델 방송 청취하기

모델에 `BroadcastsEvents` 트레이트를 포함시키고 `broadcastOn` 메서드를 정의했다면, 클라이언트에서 이 모델 방송 이벤트를 청취할 수 있습니다. 먼저 [이벤트 청취하기](#listening-for-events) 문서를 참고하세요.

`private` 메서드로 채널을 얻어 원하는 이벤트 이름을 `listen`으로 청취합니다. 모델 방송 이벤트 이름은 [모델 방송 규칙](#model-broadcasting-conventions)에 따라 네임스페이스 없이 이벤트명을 그대로 사용하고, 이름 앞에 `.`을 붙여 네임스페이스가 없음을 나타냅니다. 방송된 모델 데이터는 `model` 속성으로 전달됩니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]  
> [Pusher Channels](https://pusher.com/channels)를 사용할 때는 [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings" 섹션에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트 전송이 가능합니다.

때때로 서버에 요청하지 않고 연결된 다른 클라이언트에게 이벤트를 전송하고 싶을 수 있습니다. 예를 들어 누군가 채팅 입력란에서 타이핑 중임을 다른 사용자에게 알리는 경우입니다.

클라이언트 이벤트는 Echo의 `whisper` 메서드를 사용합니다:

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

클라이언트 이벤트 청취는 `listenForWhisper` 메서드로 할 수 있습니다:

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅과 [알림](/docs/10.x/notifications)을 조합하면, 자바스크립트 애플리케이션이 새 알림을 실시간으로 받고 페이지를 새로고침할 필요가 없습니다. 시작 전 [브로드캐스트 알림 채널](/docs/10.x/notifications#broadcast-notifications) 문서를 읽어보세요.

알림이 브로드캐스트 채널을 사용하도록 설정된 후, Echo의 `notification` 메서드로 방송된 알림을 수신할 수 있습니다. 채널 이름은 알림을 받는 엔티티 클래스 이름과 일치해야 합니다:

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

위 예시에서는 `App\Models\User` 인스턴스에 브로드캐스트 채널로 전달된 모든 알림을 콜백에서 처리합니다. 기본 `BroadcastServiceProvider`에 이미 `App.Models.User.{id}` 채널 권한 콜백도 포함되어 있습니다.