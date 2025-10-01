# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [빠른 시작](#quickstart)
- [서버 사이드 설치](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
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
- [채널 인가](#authorizing-channels)
    - [인가 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스트하기](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 예외 처리](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 수신 대기](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스 활용](#namespaces)
    - [React 또는 Vue 사용](#using-react-or-vue)
- [프리젠스 채널](#presence-channels)
    - [프리젠스 채널 인가](#authorizing-presence-channels)
    - [프리젠스 채널 가입](#joining-presence-channels)
    - [프리젠스 채널로 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 수신 대기](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대 웹 애플리케이션에서는 WebSocket을 이용해 실시간으로 사용자에게 UI 변화를 즉시 반영하는 기능을 구현하는 경우가 많습니다. 서버의 데이터가 변경되면, 이 변경 메시지를 WebSocket 커넥션을 통해 클라이언트에 전송하여 처리합니다. WebSocket은 UI에 반영되어야 하는 데이터 변화가 있을 때마다 애플리케이션 서버를 계속 폴링하는 방식에 비해 훨씬 효율적입니다.

예를 들어, 사용자 데이터를 CSV 파일로 내보내고 이메일로 전송하는 기능을 생각해 보세요. CSV 파일 생성은 몇 분 정도 걸릴 수 있으므로, 이를 [큐 작업](/docs/12.x/queues)에서 처리하기로 합니다. CSV 파일이 생성되어 사용자의 이메일로 전송되면, 브로드캐스트 이벤트 기능을 이용해 `App\Events\UserDataExported` 이벤트를 발생시킬 수 있습니다. 이 이벤트를 애플리케이션의 JavaScript가 수신하면, 사용자는 페이지를 새로 고침하지 않고도 "CSV가 이메일로 전송됨" 등과 같은 알림을 바로 받을 수 있습니다.

이러한 기능 개발이 쉽도록, Laravel은 WebSocket을 통해 서버 사이드에서 발생한 [이벤트](/docs/12.x/events)를 "브로드캐스팅"할 수 있는 기능을 제공합니다. 이벤트 브로드캐스팅을 활용하면, 서버와 클라이언트 양쪽 모두에서 동일한 이벤트 이름과 데이터를 사용할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트(프론트엔드)는 네임드 채널에 연결되고, Laravel 애플리케이션(백엔드)은 이 채널로 이벤트를 브로드캐스트합니다. 이벤트에는 프론트엔드에서 사용할 추가 데이터를 자유롭게 포함시킬 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

Laravel은 기본적으로 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 바로 시작하기 전에, 우선 [이벤트와 리스너](/docs/12.x/events)에 대한 Laravel 공식 문서를 숙지하는 것이 좋습니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

기본적으로, 새로 생성된 Laravel 애플리케이션에서는 브로드캐스팅이 비활성화되어 있습니다. 브로드캐스팅을 활성화하려면 `install:broadcasting` Artisan 명령어를 실행하십시오.

```shell
php artisan install:broadcasting
```

이 명령은 사용하고자 하는 이벤트 브로드캐스팅 서비스를 묻는 프롬프트를 제공하며, `config/broadcasting.php` 설정 파일과 애플리케이션의 브로드캐스트 인가 관련 라우트 및 콜백을 등록하는 `routes/channels.php` 파일을 생성합니다.

Laravel은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅용 `log` 드라이버, 테스트 시 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 설정 파일에는 각 드라이버별 예제도 함께 제공됩니다.

애플리케이션의 모든 브로드캐스트 설정은 `config/broadcasting.php` 파일에 저장됩니다. 이 파일이 없다면 위 명령 실행 시 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, [브로드캐스트 이벤트 정의](#defining-broadcast-events)와 [이벤트 수신 대기](#listening-for-events) 문서를 참고하여 추가 학습을 이어가십시오. Laravel의 React, Vue [스타터 키트](/docs/12.x/starter-kits)를 사용한다면 Echo의 [useEcho 훅](#using-react-or-vue)으로 쉽게 이벤트를 수신할 수 있습니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 실제로 사용하기 전에, [큐 워커](/docs/12.x/queues)를 반드시 구성 및 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 처리되므로, 브로드캐스트 때문에 애플리케이션의 응답 속도가 급격히 느려지는 것을 방지할 수 있습니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션의 설정 몇 가지를 조정하고 몇 가지 패키지를 추가로 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드의 브로드캐스팅 드라이버가 Laravel 이벤트를 브라우저 클라이언트에서 Laravel Echo(JavaScript 라이브러리)로 전달하는 방식으로 이루어집니다. 걱정하지 마세요. 설치 절차를 단계별로 안내합니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스터로 사용하고자 한다면, `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 추가해서 지원을 빠르게 활성화할 수 있습니다. 이 명령은 Reverb에 필요한 Composer 및 NPM 패키지 설치, 그리고 `.env` 환경 변수 추가까지 자동으로 처리합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령 실행 시 [Laravel Reverb](/docs/12.x/reverb) 설치 여부를 묻는 프롬프트가 표시됩니다. 물론 Composer 패키지 매니저를 활용해 수동으로 Reverb를 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치 후, Reverb의 설치 명령어를 실행하여 설정 파일을 퍼블리싱하고, 환경 변수 등록 및 브로드캐스팅 기능을 활성화할 수 있습니다.

```shell
php artisan reverb:install
```

자세한 설치 및 사용 방법은 [Reverb 공식 문서](/docs/12.x/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 사용할 경우, `install:broadcasting` 명령어에 `--pusher` 옵션을 추가하면 빠르게 구성할 수 있습니다. 이 명령은 Pusher 인증 정보 입력을 유도하고, PHP 및 JavaScript용 Pusher SDK를 설치하며, `.env` 파일 환경 변수도 자동으로 추가합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

직접 수동으로 Pusher를 지원하려면 Composer로 Pusher Channels PHP SDK를 먼저 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

다음은 `config/broadcasting.php` 설정 파일에서 Pusher Channels credential을 설정합니다. 이 파일에는 이미 Pusher용 예제가 포함되어 있어, key/secret/app id만 빠르게 지정하면 됩니다. 일반적으로는 `.env` 파일에 아래와 같이 환경 변수를 지정하게 됩니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일 내 `pusher` 항목에는 클러스터(cluster)와 같은 추가 옵션도 지정할 수 있습니다.

그리고 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 지정해줍니다.

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo](#client-side-installation)를 설치하고 구성하면, 클라이언트 쪽에서 브로드캐스트 이벤트를 수신할 준비가 완료됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래의 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법에 대해 다룹니다. 그러나 Ably에서는 자체적으로 유지관리하는 드라이버 및 Echo 클라이언트가 별도로 있으니, 더 많은 기능을 활용하고 싶다면 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스터로 사용할 때는 `install:broadcasting` 명령어에 `--ably` 옵션을 추가하면 빠르게 환경을 구성할 수 있습니다. 이 명령은 Ably credential 입력, Ably PHP 및 JavaScript SDK 설치, 환경 변수 추가까지 자동 처리합니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, Ably 애플리케이션 설정의 "Protocol Adapter Settings"에서 Pusher Protocol Support 기능을 반드시 활성화하세요.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably를 수동으로 설치하려면 Composer로 Ably PHP SDK를 설치합니다.

```shell
composer require ably/ably-php
```

다음으로 `config/broadcasting.php` 설정 파일에서 Ably credential을 설정하세요. 보통 `ABLY_KEY` 환경 변수를 통해 이 값을 설정합니다.

```ini
ABLY_KEY=your-ably-key
```

그리고 `.env` 파일에서 `BROADCAST_CONNECTION`을 `ably`로 지정합니다.

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo](#client-side-installation)를 설치 및 구성하면, 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있습니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트한 채널을 구독하고 이벤트를 수신하는 작업을 간편하게 해주는 JavaScript 라이브러리입니다.

`install:broadcasting` Artisan 명령어로 Reverb를 설치하면 Echo와 Reverb의 환경이 자동으로 준비됩니다. 별도로 Echo를 직접 설정하려면 아래 방식대로 진행할 수 있습니다.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 직접 설정하려면, 먼저 `pusher-js` 패키지를 설치해야 합니다. Reverb는 Pusher 프로토콜을 이용해 WebSocket 구독과 채널, 메시지를 처리합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 끝났다면, 애플리케이션의 JavaScript(일반적으로 `resources/js/bootstrap.js`) 파일 하단에 새 Echo 인스턴스를 생성할 수 있습니다.

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

React, Vue의 경우에도 각각 다음과 같이 설정할 수 있습니다.

```js
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

설정이 끝나면 애플리케이션 에셋을 빌드하세요.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 채널을 구독하고 이벤트를 수신하는 작업을 간편하게 만들어 줍니다.

`install:broadcasting --pusher` 명령어로 Pusher 및 Echo 설정이 자동으로 완료되며, 수동으로 직접 구성하고 싶다면 아래 절차를 참고하세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 직접 설정하려면, 먼저 WebSocket 구독, 채널, 메시지를 처리하는 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 끝나면 `resources/js/bootstrap.js` 파일에 Echo 인스턴스를 생성하세요.

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

React, Vue 환경은 다음을 참고하세요.

```js
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

`.env` 파일에 Pusher용 환경 변수도 빠짐없이 지정해야 합니다. 없을 경우 아래와 같이 추가하세요.

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

Echo 구성을 마쳤으면 애플리케이션 에셋을 빌드하세요.

```shell
npm run build
```

> [!NOTE]
> JavaScript 에셋 빌드에 관한 더 많은 정보는 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

이미 사전 구성된 Pusher Channels 클라이언트 인스턴스를 사용하려면, Echo의 `client` 설정 옵션을 사용할 수 있습니다.

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
### Ably

> [!NOTE]
> 아래 내용은 Ably의 "Pusher 호환 모드" 사용에 대한 설명입니다. Ably가 독자적으로 유지관리하는 드라이버와 Echo 클라이언트를 사용하면 Ably 고유 기능도 이용할 수 있으니 [Ably Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 채널을 구독하고 이벤트를 손쉽게 받아올 수 있도록 해주는 JavaScript 라이브러리입니다.

`install:broadcasting --ably` 명령어로 Ably와 Echo 환경이 자동 설정됩니다. 수동으로 구성하려면 아래 설명을 참고하세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

Echo를 직접 설정하려면 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다. 이 패키지들은 Pusher 프로토콜을 사용해 WebSocket 구독, 채널, 메시지를 처리합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**진행 전, Ably 애플리케이션의 "Protocol Adapter Settings"에서 Pusher 프로토콜 지원을 활성화해야 합니다.**

Echo를 설치했다면, `resources/js/bootstrap.js` 파일에서 새 Echo 인스턴스를 생성합니다.

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

React, Vue 예시도 아래와 같습니다.

```js
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

여기서 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably의 public key를 의미합니다. Ably key에서 `:` 앞쪽 부분이 public key입니다.

Echo 구성을 맞췄다면 에셋을 빌드하세요.

```shell
npm run dev
```

> [!NOTE]
> JavaScript 에셋 빌드 방법은 [Vite](/docs/12.x/vite) 문서에서 자세히 확인하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel의 이벤트 브로드캐스팅은 서버 사이드의 Laravel 이벤트를 WebSocket 기반 드라이버로 클라이언트 사이드 JavaScript 애플리케이션과 공유할 수 있게 해줍니다. Laravel은 현재 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 기본 제공합니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) 패키지로 이벤트를 간편하게 사용할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스팅됩니다. 채널은 공개(퍼블릭) 또는 비공개(프라이빗)로 지정할 수 있습니다. 공개 채널은 누구나 인증 없이 구독할 수 있지만, 비공개 채널은 사용자 인증 및 인가가 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

각 컴포넌트 세부 설명에 앞서, 전반적인 사용 예제를 간단히 살펴보겠습니다. 예를 들어, 이커머스 스토어에서 사용자가 자신의 주문 배송 상태를 조회하는 페이지가 있다고 가정해봅니다. 이때 배송 상태가 업데이트되면, `OrderShipmentStatusUpdated` 이벤트가 발생합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 자신의 주문 정보를 보고 있을 때, 변경 사항을 확인하려고 직접 새로고침하지 않도록 하려면, 주문 상태가 업데이트될 때마다 이벤트를 브로드캐스트해야 합니다. 이를 위해서는 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 하며, 이로써 이벤트가 발생할 때 Laravel이 브로드캐스트하도록 할 수 있습니다.

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

`ShouldBroadcast` 인터페이스는 이벤트에서 `broadcastOn` 메서드 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환합니다. 이벤트 생성 시 이미 이 메서드의 기본 형태가 존재하므로, 세부 내용을 완성하면 됩니다. 이 예시에서는 주문 생성자만 배송 상태를 조회할 수 있도록 주문 ID와 연결된 프라이빗 채널로 브로드캐스트합니다.

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

여러 채널로 이벤트를 브로드캐스트하고 싶다면 배열로 반환하면 됩니다.

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

비공개 채널(프라이빗 채널)은 사용자가 구독 가능한지 인가(authorization) 절차가 필요합니다. 이 인가 규칙은 `routes/channels.php` 파일에서 정의할 수 있습니다. 아래는 예시로, 사용자가 `orders.1` 채널에 접속할 때 실제 주문 생성자인지를 확인합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 인가용 콜백을 인수로 받습니다. 콜백은 사용자가 채널을 구독할 수 있다면 `true`, 아니면 `false`를 반환해야 합니다.

인가 콜백에는 현재 인증된 사용자가 첫 번째 인수로 전달되고, 추가 와일드카드 파라미터가 그 뒤를 따릅니다. 위 예시에서는 채널명 일부에 `{orderId}` 와일드카드를 사용하여 주문 ID 부분을 동적으로 처리합니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신 대기

이제 남은 것은 JavaScript 애플리케이션에서 이벤트를 수신 대기하는 것입니다. 이때는 [Laravel Echo](#client-side-installation)를 사용합니다. Echo는 React, Vue용 기본 제공 훅이 있어 바로 시작할 수 있으며, 이벤트의 public 프로퍼티가 기본적으로 브로드캐스트됩니다.

```js
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<a name="defining-broadcast-events"></a>
## 브로드캐스트 이벤트 정의 (Defining Broadcast Events)

Laravel이 특정 이벤트를 브로드캐스트하도록 하려면, 해당 이벤트 클래스에서 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 Laravel 프레임워크가 생성하는 모든 이벤트 클래스에 이미 import되어 있으므로, 손쉽게 추가할 수 있습니다.

`ShouldBroadcast`는 `broadcastOn` 메서드 하나만 구현을 요구합니다. 이 메서드는 이벤트가 브로드캐스트될 하나 이상의 채널(혹은 채널 배열)을 반환해야 하며, 각 채널은 `Channel`, `PrivateChannel`, `PresenceChannel` 등 Laravel에서 제공하는 채널 인스턴스여야 합니다. `Channel`은 공개 채널, `PrivateChannel`과 `PresenceChannel`은 인가가 필요합니다.

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

`ShouldBroadcast` 인터페이스를 구현했다면, 평소대로 [이벤트를 디스패치](/docs/12.x/events)하기만 하면 브로드캐스트도 자동으로 처리됩니다. 이벤트가 발생하면 [큐 작업](/docs/12.x/queues)을 통해 브로드캐스트가 이루어집니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel 이벤트의 클래스 이름이 브로드캐스트 이름이 됩니다. 하지만, `broadcastAs` 메서드를 정의하여 브로드캐스트 이름을 커스터마이즈 할 수도 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

커스텀 이름을 사용할 경우, 리스너 등록 시에는 앞에 `.`을 붙이도록 합니다. 이렇게 하면 Echo가 애플리케이션의 네임스페이스를 이벤트 앞에 붙이지 않습니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 이벤트의 모든 `public` 프로퍼티가 자동으로 직렬화되어 페이로드로 전송됩니다. 즉, JavaScript에서 해당 public 데이터를 모두 접근할 수 있습니다. 예를 들어 public `$user` 프로퍼티에 Eloquent 모델이 담겨 있다면, 페이로드는 아래와 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

페이로드를 좀 더 상세히 제어하려면, `broadcastWith` 메서드를 이벤트에 추가하여 원하는 데이터 배열을 리턴하면 됩니다.

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

브로드캐스트되는 각 이벤트는 기본적으로 `queue.php` 설정 파일에 정의한 기본 큐 연결의 기본 큐에 저장됩니다. 이벤트 클래스에 `connection`과 `queue` 프로퍼티를 지정하면, 브로드캐스팅에 사용할 큐 커넥션과 이름을 직접 지정할 수 있습니다.

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

또는, `broadcastQueue` 메서드를 정의하여 큐 이름만 별도로 지정할 수도 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

이벤트를 기본 큐 드라이버가 아닌 `sync` 큐로 즉시 처리하고 싶다면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요.

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

특정 조건이 충족될 때만 이벤트를 브로드캐스트하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 사용하면 됩니다.

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

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 큐에서 이벤트를 처리할 때 아직 DB 트랜잭션이 커밋되지 않았을 수 있습니다. 이 경우, 트랜잭션 내에서 변경된 모델이나 레코드가 DB에 반영되지 않은 상태일 수도 있어 예상치 못한 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 옵션이 `false`라면, 특정 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하여 해당 브로드캐스트 이벤트가 모든 오픈된 트랜잭션이 커밋된 후에 디스패치되도록 할 수 있습니다.

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
> 이런 문제에 대한 더 자세한 정보는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인가 (Authorizing Channels)

프라이빗(비공개) 채널을 사용하려면, 현재 인증된 사용자가 해당 채널을 구독할 자격이 있는지 인가를 거쳐야 합니다. 이 인가는 브라우저에서 Laravel 애플리케이션에 채널 이름을 전송하여 이루어지며, 애플리케이션이 승인 여부를 판단합니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 프라이빗 채널 구독 시 이 인가 요청이 자동으로 전송됩니다.

브로드캐스팅이 활성화되면, Laravel이 자동으로 `/broadcasting/auth` 라우트를 등록하여 인가 요청을 처리합니다. 이 라우트는 `web` 미들웨어 그룹 내부에 위치합니다.

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의

이제 현재 인증 사용자가 특정 채널에 구독할 자격이 있는지 판단하는 로직을 구현해야 합니다. 이 작업은 `install:broadcasting` Artisan 명령어로 생성된 `routes/channels.php` 파일에서 처리합니다. 이 파일에서 `Broadcast::channel` 메서드를 사용해 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 인가용 콜백을 인수로 받습니다. 콜백은 사용자가 채널을 구독할 수 있으면 `true`, 아니면 `false`를 반환해야 합니다.

모든 인가 콜백은 현재 인증된 사용자, 그리고 전달받은 와일드카드 파라미터를 순서대로 받습니다.

애플리케이션의 브로드캐스트 인가 콜백을 확인하려면 `channel:list` Artisan 명령어를 사용하세요.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백 모델 바인딩

HTTP 라우트와 마찬가지로 채널 라우트에서도 암묵적/명시적 [모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용할 수 있습니다. 즉, 문자열이나 숫자 ID 대신 실제 Eloquent 모델 인스턴스를 직접 받을 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 [암묵적 모델 바인딩 범위 지정](/docs/12.x/routing#implicit-model-binding-scoping)은 지원하지 않습니다. 하지만, 대부분의 채널은 단일 모델의 기본 키로 범위 지정하므로 이로 인한 문제는 드뭅니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백 인증 방식

프라이빗 및 프리젠스 채널의 인가는 애플리케이션의 기본 인증 가드를 사용해 이뤄집니다. 사용자가 인증되지 않은 경우 자동으로 인가 거부되며, 콜백이 실행되지 않습니다. 필요하다면 여러 개의 커스텀 가드를 지정할 수도 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션에서 다양한 종류의 채널을 사용하다 보면 `routes/channels.php` 파일이 너무 커질 수 있습니다. 콜백 대신 채널 클래스로 인가 로직을 분리할 수 있습니다. 채널 클래스 생성은 `make:channel` Artisan 명령을 사용합니다. 클래스 파일은 `App/Broadcasting` 디렉터리에 생성됩니다.

```shell
php artisan make:channel OrderChannel
```

이후, 채널을 `routes/channels.php` 파일에 등록하세요.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 인가 로직은 채널 클래스의 `join` 메서드에서 구현할 수 있습니다. 여기서 모델 바인딩도 자유롭게 사용할 수 있습니다.

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
> Laravel의 다른 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/12.x/container)로 자동 해석됩니다. 따라서 채널 생성자에서 의존성 주입을 자유롭게 사용할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅 (Broadcasting Events)

이벤트 클래스를 정의하고 `ShouldBroadcast` 인터페이스를 구현했다면, 평소대로 이벤트를 디스패치만 하면 됩니다. 이벤트 디스패처는 `ShouldBroadcast`가 포함된 이벤트인지 확인하고, 해당 이벤트를 브로드캐스팅 큐에 추가합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스트하기

브로드캐스팅을 활용하다 보면, 현재 사용자를 제외하고 채널의 다른 구독자들에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이런 경우에는 `broadcast` 헬퍼와 `toOthers` 메서드를 조합하면 됩니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들면 할 일 리스트 앱에서 사용자가 작업을 생성하면, 클라이언트는 `/task`로 요청을 보내고, 서버는 새 작업 정보를 브로드캐스트한 뒤 JSON으로 응답하게 처리할 수 있습니다. 프론트엔드가 해당 엔드포인트 응답으로 새 작업을 리스트에 추가하고 동시에 새 작업 생성 이벤트도 수신 대기 중이라면, 중복된 작업이 리스트에 추가될 수 있습니다. 이런 중복을 막기 위해서 `toOthers`를 활용하여 현재 사용자 본인에게는 브로드캐스팅하지 않도록 설정할 수 있습니다.

> [!WARNING]
> 이벤트에서 `toOthers`를 사용하려면 반드시 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 포함해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스를 생성하면 소켓 ID가 자동으로 할당됩니다. 글로벌 [Axios](https://github.com/axios/axios) 인스턴스를 사용해 HTTP 요청을 보낼 경우, 모든 요청에 해당 소켓 ID(`X-Socket-ID` 헤더)가 자동 전송됩니다. 이후 서버의 `toOthers` 사용 시 Laravel이 이 헤더를 참고하여 해당 소켓 ID의 연결에는 브로드캐스트하지 않습니다.

글로벌 Axios 인스턴스를 사용하지 않는다면, JavaScript에서 `Echo.socketId()`로 객체의 소켓 ID를 수동으로 얻어서 모든 요청 헤더에 함께 전송하도록 직접 설정해야 합니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

여러 개의 브로드캐스트 커넥션을 활용하고 있을 때, 이벤트별로 지정한 브로드캐스터를 이용해 브로드캐스트할 수 있습니다. `broadcast` 헬퍼의 `via` 메서드를 사용하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 클래스 생성자에서 `broadcastVia` 메서드를 호출할 수 있습니다. 이때는 `InteractsWithBroadcasting` 트레이트를 반드시 사용해야 합니다.

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

가끔은 별도의 이벤트 클래스를 만들지 않고, 간단한 이벤트만 프론트엔드에 브로드캐스트하고 싶을 수 있습니다. Laravel의 `Broadcast` 파사드를 통해 익명 이벤트(anonymous event)를 전송할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예시는 다음과 같은 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`, `with` 메서드로 이벤트 이름과 데이터를 커스터마이징할 수도 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

이 경우 다음과 같은 이벤트가 생성됩니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

익명 이벤트를 프라이빗 또는 프리젠스 채널에 브로드캐스트하고 싶을 때는 `private`, `presence` 메서드를 사용하세요.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send`는 이벤트를 [큐](/docs/12.x/queues)를 통해 비동기 처리합니다. 즉시 브로드캐스트하고 싶다면 `sendNow`를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 사용자를 제외한 구독자에게만 보내고 싶다면 `toOthers`를 활용하세요.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 예외 처리 (Rescuing Broadcasts)

큐 서버가 동작하지 않거나 이벤트 브로드캐스트 도중 오류가 발생하면 예외가 발생하여, 이로 인해 사용자에게 서비스 전체 오류가 표시될 수도 있습니다. 브로드캐스트는 대개 필수 동작이 아니라 부가적 기능이므로, 이런 에러가 서비스 흐름을 망치지 않게 하려면 이벤트에 `ShouldRescue` 인터페이스를 구현하세요.

`ShouldRescue`를 구현한 이벤트는 Laravel의 [rescue 헬퍼 함수](/docs/12.x/helpers#method-rescue)를 통해 예외를 자동으로 캐치하고 로그로 남긴 후, 사용자 흐름에는 영향이 없게 처리합니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 수신 (Receiving Broadcasts)

<a name="listening-for-events"></a>
### 이벤트 수신 대기

[Laravel Echo](#client-side-installation)를 설치 및 인스턴스화 했다면, 이제 Laravel에서 브로드캐스트된 이벤트를 클라이언트에서 수신할 준비가 끝났습니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻고, `listen` 메서드로 특정 이벤트를 수신하면 됩니다.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

프라이빗 채널로 이벤트 수신 대기를 하려면 `private` 메서드를 사용하세요. 여러 이벤트를 동일 채널에서 수신하려면 listen 체이닝이 가능합니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중단

채널을 나가지 않고 특정 이벤트에 대한 수신만 중단하려면 `stopListening` 메서드를 이용하세요.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널에서 완전히 나가려면 `leaveChannel` 메서드를 사용하세요.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널뿐 아니라, 관련된 프라이빗, 프리젠스 채널까지 모두 나가려면 `leave` 메서드를 사용하면 됩니다.

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스 활용

이벤트 클래스 전체 네임스페이스를 생략해도 되는 이유는 Echo가 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 가정하기 때문입니다. Echo 인스턴스화 시 `namespace` 옵션으로 루트 네임스페이스를 바꿀 수도 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

혹은, 이벤트 클래스를 `.`으로 시작해서 네임스페이스 전체를 항상 명시할 수도 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue 사용

Laravel Echo는 React, Vue에서도 이벤트 수신을 매우 쉽게 할 수 있는 훅(hook)을 제공합니다. 시작하려면, 프라이빗 이벤트 수신에 사용하는 `useEcho` 훅을 적용하세요. 이 훅은 컴포넌트 언마운트 시 자동으로 채널에서 떠납니다.

```js
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

여러 이벤트를 동시에 수신하려면 이벤트 배열을 넘기면 됩니다.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트 페이로드 타입을 명확히 지정하고 싶다면 아래와 같이 하면 됩니다.

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```

`useEcho`는 채널에서 자동으로 나가지만, 반환된 메서드를 사용하면 프로그래밍적으로 수신 중단/재개/채널 나가기 등을 컨트롤할 수 있습니다.

```js
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 수신만 중단(채널은 유지)
stopListening();

// 수신 재개
listen();

// 채널 나가기
leaveChannel();

// 관련 프라이빗/프리젠스 채널 포함 모두 나가기
leave();
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 수신만 중단
stopListening();

// 수신 재개
listen();

// 채널 나가기
leaveChannel();

// 관련 채널 포함 모두 나가기
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### 퍼블릭 채널 연결

퍼블릭 채널을 연결하려면 `useEchoPublic` 훅을 사용하세요.

```js
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### 프리젠스 채널 연결

프리젠스 채널에 연결하려면 `useEchoPresence` 훅을 사용하세요.

```js
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="presence-channels"></a>
## 프리젠스 채널 (Presence Channels)

프리젠스 채널은 프라이빗 채널의 보안과 더불어, 채널 내에 누가 접속해 있는지 알 수 있는 "존재 인식" 기능까지 제공합니다. 이를 통해 채팅방의 참가자 리스트를 보여주거나, 같은 페이지를 보고 있는 사용자를 알려주는 협업 기능도 쉽게 만들 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프리젠스 채널 인가

프리젠스 채널도 프라이빗 채널이므로, [채널 인가](#authorizing-channels)가 필요합니다. 인가 콜백에서 인가를 허용하면 단순히 `true`를 반환하는 대신, 사용자 정보를 담은 배열을 리턴해야 합니다.

이렇게 반환한 데이터는 프리젠스 채널에 들어오는 JavaScript 이벤트 리스너에서 사용할 수 있습니다. 인가되지 않은 사용자는 `false` 또는 `null`을 반환하면 됩니다.

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

Echo의 `join` 메서드로 프리젠스 채널에 접속할 수 있습니다. 이 메서드는 `PresenceChannel` 인스턴스를 반환하는데, `listen`뿐 아니라 `here`, `joining`, `leaving` 등의 이벤트를 사용할 수 있게 합니다.

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

- `here`: 채널에 정상적으로 접속하면 즉시 실행되며, 현재 채널에 접속 중인 모든 사용자 정보를 배열로 받습니다.
- `joining`: 새로운 사용자가 채널에 접속했을 때 실행됩니다.
- `leaving`: 사용자가 채널을 떠날 때 실행됩니다.
- `error`: 인증 엔드포인트가 200이 아닌 HTTP 상태 코드를 반환하거나 JSON 파싱 문제가 있을 때 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프리젠스 채널로 브로드캐스트

프리젠스 채널 역시 퍼블릭, 프라이빗 채널과 마찬가지로 이벤트를 주고 받을 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 프리젠스 채널로 브로드캐스트하려면, 이벤트의 `broadcastOn`에서 `PresenceChannel`을 반환하면 됩니다.

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

프리젠스 채널도 `broadcast`와 `toOthers`로 현재 사용자를 제외한 다른 사용자에게만 보낼 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

이벤트 수신은 Echo의 `listen` 메서드를 이용해 위의 다른 예시와 같습니다.

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
## 모델 브로드캐스팅 (Model Broadcasting)

> [!WARNING]
> 이 문서의 내용을 읽기 전, 먼저 Laravel의 모델 브로드캐스팅 개념과 브로드캐스트 이벤트 생성/수신 일반 방법을 익혀두면 좋습니다.

애플리케이션에서 [Eloquent 모델](/docs/12.x/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 경우가 많습니다. 물론, 직접 이벤트 클래스를 만들어 `ShouldBroadcast`를 마킹해서 처리할 수도 있습니다.

하지만 오직 브로드캐스팅만을 위해 별도 이벤트 클래스를 만드는 것이 번거로울 때는, Laravel이 모델의 상태 변화에 따라 자동 브로드캐스트하도록 할 수 있습니다.

시작하려면, 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하세요. 그리고 `broadcastOn` 메서드에서 해당 모델 이벤트가 브로드캐스트될 채널 배열을 반환하면 됩니다.

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

이렇게 하면, 모델 인스턴스가 생성/수정/삭제/임시삭제/복구될 때마다 이벤트가 브로드캐스트됩니다.

`broadcastOn` 메서드는 이벤트의 종류(`created`, `updated`, `deleted`, `trashed`, `restored`)를 매개변수로 받아, 타입별로 브로드캐스트 대상 채널을 다르게 지정할 수도 있습니다.

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
#### 모델 브로드캐스팅 이벤트 생성 방식 커스터마이징

간혹 Laravel이 내부적으로 생성하는 모델 브로드캐스트 이벤트를 사용자가 직접 커스터마이즈하고 싶을 수 있습니다. 이럴 때는 모델에서 `newBroadcastableEvent` 메서드를 정의하고, `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환하면 됩니다.

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
### 모델 브로드캐스팅 규칙 (Model Broadcasting Conventions)

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 네이밍 규칙

위 예제의 `broadcastOn`에서는 `Channel` 인스턴스 대신 Eloquent 모델 인스턴스 자체를 반환했습니다. 모델 인스턴스를 반환하면, Laravel이 해당 모델의 클래스명과 기본 키를 이용해 자동으로 프라이빗 채널 인스턴스를 만들어줍니다.

예를 들어, `App\Models\User`의 id가 1인 경우, `App.Models.User.1` 이름의 `Illuminate\Broadcasting\PrivateChannel` 인스턴스가 자동 생성됩니다. 물론 필요한 경우 `Channel` 인스턴스를 직접 반환하여 채널명을 자유롭게 지정할 수도 있습니다.

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

직접 채널 인스턴스를 반환하면서 모델을 생성자에 전달하면, Laravel이 위에서 설명한 규칙대로 채널 이름을 문자열로 변환해줍니다.

```php
return [new Channel($this->user)];
```

특정 모델의 채널명을 확인하고 싶다면 `broadcastChannel` 메서드를 호출하면 됩니다. 예를 들어, id 1인 `App\Models\User`의 경우 `App.Models.User.1`을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 네이밍/페이로드 규칙

모델 브로드캐스트 이벤트는 `App\Events` 내 "실제" 이벤트와 달리, 이름과 페이로드가 규칙(컨벤션)으로 자동 생성됩니다. Laravel은 "모델 클래스명 + 모델 이벤트명(updated, created 등)" 형태로 이름을 정합니다.

예를 들어 `App\Models\Post` 모델에서 업데이트가 발생하면, 클라이언트에 `PostUpdated`라는 이름의 이벤트와 아래와 같은 페이로드가 전달됩니다.

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

`App\Models\User` 모델 삭제 시에는 `UserDeleted` 이벤트가 발송됩니다.

더 세분화하여 커스텀 이벤트 명과 페이로드를 지정하고 싶다면 모델에 `broadcastAs`, `broadcastWith` 메서드를 정의하면 됩니다. 각 메서드는 현재 수행 중인 모델 이벤트/작업명을 전달받습니다. `broadcastAs`에서 null을 반환하면, Laravel의 규칙대로 이름이 생성됩니다.

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
### 모델 브로드캐스트 수신 대기 (Listening for Model Broadcasts)

모델에 `BroadcastsEvents` 트레이트와 적절한 `broadcastOn` 메서드를 추가했다면, 이제 클라이언트에서 브로드캐스트된 모델 이벤트를 수신할 수 있습니다. 구체적인 수신 방식은 [이벤트 수신](#listening-for-events) 문서도 참고하면 좋습니다.

먼저 `private` 메서드로 채널을 가져오고, `listen` 메서드로 이벤트를 수신해야 합니다. 채널 명은 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)과 일치하도록 지정해야 합니다.

이벤트 이름에는 네임스페이스가 없으므로 앞에 `.`를 붙여 구분합니다. 각 모델 이벤트 페이로드에는 `model` 프로퍼티가 브로드캐스트됩니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React 또는 Vue에서 모델 브로드캐스트 수신

React/Vue 환경에서는 Laravel Echo의 `useEchoModel` 훅으로 모델 브로드캐스트 이벤트를 더 쉽게 수신할 수 있습니다.

```js
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

브로드캐스트 페이로드 타입을 명확히 해 타입 안정성과 개발 편의성을 높일 수도 있습니다.

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```

<a name="client-events"></a>
## 클라이언트 이벤트 (Client Events)

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용할 때는, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 활성화해야 합니다.

때로는 Laravel 애플리케이션 서버를 거치지 않고, 연결된 다른 클라이언트에 직접 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어 실시간 타이핑 알림처럼, 사용자가 입력 중임을 다른 사용자에게 즉시 알려주고 싶을 때 유용합니다.

이럴 때 Echo의 `whisper` 메서드를 사용할 수 있습니다.

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

React, Vue는 다음과 같이 처리합니다.

```js
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

클라이언트 이벤트 수신은 `listenForWhisper` 메서드를 사용하세요.

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

<a name="notifications"></a>
## 알림 (Notifications)

[알림](/docs/12.x/notifications) 시스템과 이벤트 브로드캐스팅을 연동하면, JavaScript 애플리케이션이 페이지를 새로 고침하지 않고도 새로운 알림을 실시간으로 받을 수 있습니다. 먼저, [브로드캐스트 알림 채널 사용법](/docs/12.x/notifications#broadcast-notifications)을 살펴보세요.

알림이 브로드캐스트 채널을 통해 전송되도록 설정했다면, Echo의 `notification` 메서드로 알림을 수신할 수 있습니다. 채널 이름은 알림을 받는 엔티티의 클래스명과 일치해야 합니다.

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

React, Vue 환경의 예시는 다음과 같습니다.

```js
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

위 예시에서는, `broadcast` 채널을 통해 `App\Models\User` 인스턴스에 보낸 모든 알림이 콜백으로 수신됩니다. `App.Models.User.{id}` 채널에 대한 채널 인가 콜백은 `routes/channels.php`에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 수신 중단

채널을 떠나지 않고 알림 수신만 중단하고 싶을 때는, `stopListeningForNotification` 메서드를 사용하세요.

```js
const callback = (notification) => {
    console.log(notification.type);
}

// 수신 시작...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// 수신 중단(콜백은 동일 참조여야 함)
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
