# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [빠른 시작](#quickstart)
- [서버 측 설치](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 측 설치](#client-side-installation)
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
    - [브로드캐스팅과 DB 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인가(Authorization)](#authorizing-channels)
    - [인가 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스트](#broadcasting-events)
    - [자신 이외 사용자만 전송](#only-to-others)
    - [커넥션 지정 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 복구(Rescue)](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React, Vue에서 사용하기](#using-react-or-vue)
- [프레즌스 채널(Presence Channels)](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notifications)](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대 웹 애플리케이션에서는 WebSocket을 활용하여 실시간으로 UI를 즉시 갱신하는 경우가 많습니다. 서버에서 데이터가 변경되면, 이 사실을 WebSocket 연결을 통해 클라이언트로 전달하여 처리합니다. WebSocket은 주기적으로 서버에 변경사항을 계속해서 요청하는 방식보다 효율적입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내 이메일로 보내는 기능이 있다고 가정해 봅시다. 그런데 CSV 생성이 몇 분 걸리므로, [큐 작업](/docs/master/queues)에서 생성 및 전송을 처리합니다. CSV 파일의 생성 및 메일 전송이 완료되면 `App\Events\UserDataExported` 이벤트를 브로드캐스트하여, 자바스크립트에서 이 이벤트를 즉시 받고, 사용자가 새로고침 없이 "메일이 도착했다"는 메시지를 확인할 수 있습니다.

이처럼 실시간 UI 기능을 쉽게 만들 수 있도록, Laravel에서는 서버 측 [이벤트](/docs/master/events)를 WebSocket을 통해 브라우저로 "브로드캐스트"하는 기능을 제공합니다. 이렇게 하면 서버와 클라이언트 양쪽에서 같은 이벤트 이름과 데이터를 사용할 수 있습니다.

브로드캐스팅의 핵심 개념은 단순합니다. 프론트엔드 클라이언트가 이름이 지정된 채널에 접속하고, 백엔드 Laravel 애플리케이션이 이 채널에 이벤트를 브로드캐스트합니다. 이때 이벤트에 원하는 데이터를 실어 프론트엔드로 전달할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

Laravel에서는 기본적으로 세 가지 서버 사이드 브로드캐스팅 드라이버를 지원합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전, 반드시 [이벤트 & 리스너](/docs/master/events) 문서를 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

Laravel 신규 애플리케이션에서는 브로드캐스팅이 기본적으로 비활성화되어 있습니다. 다음 Artisan 명령어로 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령을 실행하면 사용할 브로드캐스트 서비스를 선택하게 됩니다. 또한, `config/broadcasting.php` 설정 파일과 브로드캐스트 인가 라우트 및 콜백을 등록할 수 있는 `routes/channels.php` 파일이 생성됩니다.

Laravel은 여러 브로드캐스트 드라이버를 기본적으로 지원합니다: [Laravel Reverb](/docs/master/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한, 테스트 중 브로드캐스팅을 완전히 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버의 설정 예시는 `config/broadcasting.php`에 샘플로 포함되어 있습니다.

애플리케이션의 모든 브로드캐스트 설정은 `config/broadcasting.php` 파일에 저장됩니다. 이 파일이 없다면, `install:broadcasting` 명령 실행 시 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면 [브로드캐스트 이벤트 정의](#defining-broadcast-events) 및 [이벤트 리스닝](#listening-for-events)에 대해 더 자세히 학습할 준비가 되었습니다. React 또는 Vue용 [스타터 키트](/docs/master/starter-kits)를 사용하는 경우, Echo의 [useEcho hook](#using-react-or-vue)을 활용하여 이벤트를 쉽게 리스닝할 수 있습니다.

> [!NOTE]
> 이벤트 브로드캐스트를 사용하기 전에는 반드시 [큐 워커](/docs/master/queues) 설정 및 실행을 먼저 해야 합니다. 이벤트 브로드캐스팅은 모두 큐 작업으로 처리되어, 브로드캐스트로 인해 애플리케이션 응답속도가 지연되지 않게 보장합니다.

<a name="server-side-installation"></a>
## 서버 측 설치 (Server Side Installation)

Laravel에서 이벤트 브로드캐스트를 사용하려면, 애플리케이션 내에서 약간의 설정과 필요한 패키지 설치가 필요합니다.

브로드캐스팅은 서버 측 브로드캐스트 드라이버가 Laravel 이벤트를 처리·전송하고, JavaScript 라이브러리인 Laravel Echo가 이를 브라우저에서 수신하는 방식으로 동작합니다. 아래 단계별로 모든 설치 과정을 안내합니다.

<a name="reverb"></a>
### Reverb

Reverb를 브로드캐스터로 사용할 때 Laravel의 브로드캐스트 기능을 빠르게 활성화하려면 `--reverb` 옵션을 붙여 `install:broadcasting` 명령을 실행하세요. 이 명령어는 Reverb의 Composer·NPM 패키지 설치 및 환경설정 변수를 `.env`에 자동 추가합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 실행 시 [Laravel Reverb](/docs/master/reverb) 설치를 선택할 수 있습니다. 물론, Composer로 Reverb 패키지를 직접 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지를 설치했다면, 다음 명령으로 Reverb의 설정 파일을 배포하고, 필요한 환경 변수도 자동으로 추가하며, 이벤트 브로드캐스팅도 활성화할 수 있습니다.

```shell
php artisan reverb:install
```

자세한 설치·사용법은 [Reverb 공식 문서](/docs/master/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 브로드캐스터로 사용할 때 Laravel의 브로드캐스트 기능을 빠르게 활성화하려면 `--pusher` 옵션을 붙여 `install:broadcasting` 명령을 실행하세요. 이 명령은 Pusher 인증 정보를 입력하고, Pusher PHP 및 JavaScript SDK를 설치하며, `.env` 파일을 적절히 설정합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher를 수동으로 설정하려면, Composer로 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 설정 파일에서 Pusher 인증 정보를 입력하세요. 샘플 Pusher 설정서는 이미 들어 있으니, 키, 시크릿, 앱 ID만 바꿔주면 됩니다. 보통 인증 정보는 `.env`에 작성합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php`의 `pusher` 설정에는 클러스터 등 추가 옵션도 지정할 수 있습니다.

그리고 `.env` 파일의 `BROADCAST_CONNECTION` 값을 `pusher`로 설정하세요.

```ini
BROADCAST_CONNECTION=pusher
```

이후 [Laravel Echo](#client-side-installation)를 설치·설정하면 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래의 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법입니다. 그러나 Ably 팀에서는 Ably의 고유 기능을 최대한 활용할 수 있는 공식 드라이버와 Echo 클라이언트를 제공하니, 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 브로드캐스터로 사용할 때, `--ably` 옵션을 붙여 `install:broadcasting` Artisan 명령을 실행하세요. 이 명령은 Ably 인증 정보를 입력받고, Ably PHP 및 JavaScript SDK를 설치하며, 환경 변수를 자동으로 설정합니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, Ably 대시보드에서 반드시 "Pusher Protocol Support" 기능을 활성화해야 합니다(Ably 앱 설정의 Protocol Adapter Settings에서 설정).**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 추가하려면 Composer로 Ably PHP SDK를 설치하세요.

```shell
composer require ably/ably-php
```

그리고 `config/broadcasting.php`에 Ably 키를 지정하세요. 샘플 설정이 이미 들어 있으며, 보통 키 값은 `.env`의 `ABLY_KEY`로 지정합니다.

```ini
ABLY_KEY=your-ably-key
```

`.env`의 `BROADCAST_CONNECTION` 값도 `ably`로 설정합니다.

```ini
BROADCAST_CONNECTION=ably
```

그 뒤 [Laravel Echo](#client-side-installation)를 설치·설정하면 클라이언트에서 이벤트를 받을 수 있습니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 브로드캐스트한 이벤트를 JavaScript에서 간편하게 구독·수신할 수 있게 해주는 라이브러리입니다.

`install:broadcasting` 명령으로 Reverb 설치 시, Echo 설정과 구성이 자동으로 애플리케이션에 반영됩니다. 수동으로 Echo를 구성하려면 다음의 절차를 따르세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Echo를 수동 설정하려면, `pusher-js` 패키지를 설치해야 합니다. Reverb는 WebSocket 연결·채널·메시지에 Pusher 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치가 완료되면, Echo 인스턴스를 새로 생성합니다. 보통 `resources/js/bootstrap.js`의 하단에 설정합니다.

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

React 또는 Vue에서는 다음과 같이 설정할 수 있습니다.

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

이후 자바스크립트 에셋을 빌드합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0+ 버전이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 JavaScript에서 서버 브로드캐스트 이벤트를 쉽게 구독·수신할 수 있도록 도와주는 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령으로 설치할 경우, Pusher 및 Echo 구성은 자동으로 적용됩니다. 수동 설정하려면 아래 절차를 따라주세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

Echo를 수동 구성하려면 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다. 이들은 Pusher 프로토콜 기반으로 WebSocket 연결을 처리합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치 후 `resources/js/bootstrap.js`에서 Echo 인스턴스를 생성합니다.

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

React, Vue 설정 예시는 아래와 같습니다.

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

`.env` 파일에 다음과 같이 Pusher 환경 변수를 추가합니다(없으면 새로 추가).

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

에코 설정이 끝나면 에셋을 빌드하세요.

```shell
npm run build
```

> [!NOTE]
> 자바스크립트 에셋 컴파일 관련 자세한 내용은 [Vite](/docs/master/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

미리 구성된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo에 `client` 옵션으로 전달할 수 있습니다.

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
> 아래 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법입니다. Ably 공식 드라이버를 활용하면 Ably만의 고유 기능을 쓸 수 있습니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버에서 브로드캐스트한 이벤트를 쉽게 구독·수신할 수 있게 해주는 JavaScript 라이브러리입니다.

`install:broadcasting --ably` Artisan 명령으로 설치 시, Ably와 Echo의 구성은 자동 반영됩니다. 수동 설정하려면 아래 절차를 따르세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

Echo를 수동 구성하려면 `laravel-echo`와 `pusher-js` 패키지를 설치해야 하며, Ably도 이들 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**설정 전에, Ably 앱 대시보드에서 "Pusher Protocol Support"를 반드시 활성화해야 합니다.**

설치 후, `resources/js/bootstrap.js`에서 Echo 인스턴스를 만듭니다.

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

React 또는 Vue 예시는 다음과 같습니다.

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

Ably Echo 설정에서 `VITE_ABLY_PUBLIC_KEY` 환경 변수를 참고하는 점을 알 수 있습니다. 이 값은 Ably 키에서 `:` 앞에 오는 부분(퍼블릭 키)을 입력해야 합니다.

설정 완료 후 에셋을 빌드합니다.

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 에셋 컴파일에 관한 더 자세한 내용은 [Vite](/docs/master/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel의 이벤트 브로드캐스팅 기능은 서버-클라이언트를 WebSocket 기반으로 연결하는 드라이버 방식을 사용합니다. 현재 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 등 다양한 드라이버를 공식 지원합니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) JavaScript 패키지를 사용해 쉽게 이벤트를 소비할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트됩니다. 채널은 공개(public) 또는 비공개(private)로 지정할 수 있습니다. 공개 채널은 인증이나 인가 없이 누구나 구독이 가능하지만, 비공개 채널은 인증 및 권한이 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 활용

각 구성요소를 자세히 보기 전, 이커머스 스토어를 예시로 하여 브로드캐스팅 과정을 큰 흐름으로 살펴봅시다.

예를 들어, 사용자 주문의 배송 상태를 보여주는 페이지가 있습니다. 배송 상태가 변경되면 `OrderShipmentStatusUpdated` 이벤트를 애플리케이션에서 발생시키는 식입니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

주문 상세페이지를 보고 있는 사용자가 페이지를 새로고침하지 않아도 실시간으로 상태를 볼 수 있도록, `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스를 붙이면 이벤트가 발생할 때마다 자동으로 브로드캐스팅이 처리됩니다.

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

`ShouldBroadcast` 인터페이스를 구현하면, `broadcastOn` 메서드를 반드시 정의해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널(또는 채널 배열)을 반환합니다. 예를 들어 주문 생성자만 배송 상태를 듣게 하려면 아래처럼 비공개 채널을 사용합니다.

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

이벤트를 여러 채널에 브로드캐스트해야 한다면 배열로 반환하면 됩니다.

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

비공개 채널은 반드시 사용자가 해당 채널을 구독할 권한이 있는지 인증·인가가 필요합니다. `routes/channels.php` 파일에 아래처럼 인가 규칙을 정의합니다. 예를 들어 `orders.1` 채널에 접속하려는 사용자가 해당 주문의 생성자인지 확인하면 됩니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름, 콜백(인가 여부를 true/false로 반환)을 받으며, 콜백에는 인증 사용자와 와일드카드 값이 순서대로 전달됩니다. 여기서 `{orderId}`는 채널 이름의 와일드카드입니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 리스닝

이제 JavaScript 애플리케이션에서 이벤트를 리스닝하면 됩니다. [Laravel Echo](#client-side-installation)를 활용하세요. React, Vue용 Hook을 쓰면 편리하게 사용할 수 있으며, 이벤트의 public 속성들은 브로드캐스트 데이터로 자동 포함됩니다.

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

이벤트가 브로드캐스트되어야 함을 Laravel에 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 Laravel에서 생성하는 기본 이벤트 클래스에 이미 import되어 있으므로 손쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 반드시 하나의 메서드, 즉 `broadcastOn`을 구현해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널(`Channel`·`PrivateChannel`·`PresenceChannel`) 또는 그 배열을 반환해야 합니다. `Channel`은 누구나 구독 가능한 공개 채널, `PrivateChannel`과 `PresenceChannel`은 인가가 필요한 비공개 채널입니다.

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

`ShouldBroadcast` 인터페이스를 구현했다면, [이벤트를 발생](/docs/master/events)시키는 것만으로 지정된 드라이버·큐를 통해 자동으로 브로드캐스트가 처리됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름 (Broadcast Name)

Laravel은 기본적으로 이벤트 클래스 이름을 브로드캐스트 이름으로 사용합니다. 하지만 `broadcastAs` 메서드를 구현하여 브로드캐스트 이름을 커스터마이즈할 수 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`로 이름을 커스터마이즈하면, Echo에서 리스닝할 때 앞에 `.`(dot) 문자를 반드시 붙여야 네임스페이스가 자동으로 붙지 않습니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터 (Broadcast Data)

이벤트가 브로드캐스트될 때, 이벤트 클래스의 모든 `public` 속성은 자동으로 직렬화되어 payload로 전달됩니다. 예를 들어 `$user` 속성에 Eloquent 모델이 있다면, payload는 다음과 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

브로드캐스트 payload를 세밀하게 커스터마이즈하고 싶다면, 이벤트 클래스에 `broadcastWith` 메서드를 구현하세요. 이 메서드는 브로드캐스트 payload로 보낼 데이터를 배열로 반환합니다.

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
### 브로드캐스트 큐 (Broadcast Queue)

브로드캐스트 이벤트는 기본적으로 `queue.php`에 정의된 기본 연결·큐에 들어갑니다. 이벤트 클래스에 `connection`, `queue` 속성을 정의하여 브로드캐스터가 사용할 큐 연결 이름 또는 큐 이름을 지정할 수 있습니다.

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

혹은 `broadcastQueue` 메서드로도 큐 이름만 지정할 수 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

브로드캐스트를 기본 큐 드라이버가 아닌, 즉시 동기(synchronous)로 처리하려면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하세요.

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
### 브로드캐스트 조건 (Broadcast Conditions)

특정 조건에 따라 이벤트를 브로드캐스트하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하세요.

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
#### 브로드캐스팅과 DB 트랜잭션

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내부에서 발생하면, 큐가 트랜잭션이 커밋되기 전에 작업을 처리할 수 있습니다. 이때, 트랜잭션 내에서 갱신한 모델이나 레코드가 아직 DB에 반영되지 않은 상태일 수 있고, 그로 인해 브로드캐스트 작업 처리 시 예상치 못한 오류가 생길 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 때도, 해당 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 모든 트랜잭션 커밋 후에 작업이 실행됨을 보장할 수 있습니다.

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
> 이 문제를 법적으로 회피하는 방법을 더 알고 싶다면 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인가(Authorization) (Authorizing Channels)

비공개 채널은 반드시 현재 인증 사용자에게 채널 수신 권한이 있는지 확인해야 합니다. 이 판단은 브라우저에서 채널 이름을 포함한 HTTP 요청을 받아 애플리케이션에서 처리합니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 이 HTTP 요청은 자동으로 전송됩니다.

브로드캐스트를 설치하면, Laravel이 `/broadcasting/auth` 라우트를 자동으로 등록합니다. 만약 자동 등록에 실패했다면, `/bootstrap/app.php` 파일에서 수동 등록할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의

이제 실제로 인증된 사용자가 해당 채널에 들어갈 수 있는지 결정하는 로직을 `routes/channels.php`에 정의해야 합니다. `Broadcast::channel` 메서드를 사용해 등록합니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

채널 인가는 콜백을 통해 true/false 판단값을, 첫 번째 인수로 인증 사용자, 그 외 와일드카드 값을 추가로 받습니다. 여기서 `{orderId}`는 URL 라우터의 와일드카드와 동일한 역할을 합니다.

아래 Artisan 명령으로 등록된 인가 콜백 목록을 볼 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 콜백에서 모델 바인딩

HTTP 라우트처럼, 채널 라우트에서도 암묵적·명시적 [모델 바인딩](/docs/master/routing#route-model-binding)이 가능합니다. 예를 들어 `orders.{order}` 형태로 등록하면 아래처럼 직접 모델 인스턴스를 받을 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과는 달리, 채널 라우트 모델 바인딩은 [암묵적 바인딩 스코프](/docs/master/routing#implicit-model-binding-scoping)를 지원하지 않습니다. 하지만, 대부분 단일 모델의 기본키로 스코프가 충분하므로 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 콜백에서 인증 가드 지정

비공개·프레즌스 채널의 인증은 애플리케이션의 기본 인증 가드로 처리됩니다. 인증되지 않은 사용자는 자동으로 인가가 거부되고, 콜백이 실행되지 않습니다. 필요한 경우, 여러 커스텀 인증 가드를 지정할 수도 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션에서 많은 채널을 쓰면 `routes/channels.php`가 복잡해질 수 있습니다. 이때 클로저 대신별도의 채널 클래스를 만들어 사용할 수 있습니다. `make:channel` 명령어로 생성하세요. 클래스는 `App/Broadcasting` 디렉토리에 위치합니다.

```shell
php artisan make:channel OrderChannel
```

이제 `routes/channels.php`에 아래처럼 등록합니다.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

실제 인가 로직은 채널 클래스의 `join` 메서드에 작성합니다. 여기서도 모델 바인딩이 가능합니다.

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
> 다른 많은 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/master/container)에 의해 자동으로 의존성 주입이 처리됩니다. 생성자에서 필요한 의존성을 타입힌트할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스트 (Broadcasting Events)

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 붙였다면, 이벤트의 dispatch 메서드로 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 해당 이벤트에 ShouldBroadcast가 있음을 인식하고 이벤트를 브로드캐스트 큐에 넣습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 자신 이외 사용자만 전송 (Only to Others)

특정 채널의 구독자 중에서 현재 사용자만 제외하고 브로드캐스팅해야 할 때가 있습니다. 이럴 때는 `broadcast` 헬퍼에 `toOthers` 메서드를 체이닝하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어, 작업(Task) 리스트 애플리케이션에서 새 작업을 POST로 생성하는데, 이 작업이 브로드캐스트되고, 또 API 응답으로도 작업 리스트가 추가된다면, 브로드캐스트까지 받아 중복이 생길 수 있습니다. 이때 `toOthers`를 이용하면 자신에겐 전송되지 않으니 중복 없이 처리할 수 있습니다.

> [!WARNING]
> `toOthers`를 사용하려면 이벤트 클래스에 반드시 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 적용되어 있어야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정 방법

Echo 인스턴스가 초기화되면 socket ID가 연결에 할당됩니다. Axios 등의 글로벌 인스턴스를 쓸 경우, 모든 HTTP 요청 헤더에 `X-Socket-ID`가 자동으로 포함됩니다. 이 socket ID를 기반으로 `toOthers`가 브로드캐스트 대상에서 자신을 제외합니다.

글로벌 Axios를 사용하지 않는다면, 반드시 모든 요청에 `X-Socket-ID` 헤더를 추가해야 하며, Echo 인스턴스의 `socketId()`를 통해 값을 얻을 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 지정 커스터마이징 (Customizing the Connection)

여러 브로드캐스트 커넥션을 사용할 때, 기본 커넥션 이외의 브로드캐스터에 이벤트를 push하려면 `via` 메서드로 드라이버를 지정하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 클래스에서 `InteractsWithBroadcasting` 트레이트를 사용하고, 생성자에서 `broadcastVia` 메서드를 호출해 커넥션을 지정할 수 있습니다.

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
### 익명 이벤트 (Anonymous Events)

별도의 이벤트 클래스를 만들지 않고, 애플리케이션에서 단순히 브로드캐스트만 하고 싶을 때는 `Broadcast` 파사드에서 "익명 이벤트"를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 코드가 브로드캐스트하는 예시는 다음과 같습니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`와 `with` 메서드를 이용해 이벤트 이름과 데이터를 커스터마이즈할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

결과 예시는 아래와 같습니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

익명 이벤트로 비공개, 프레즌스 채널도 활용할 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send`는 작업을 [큐](/docs/master/queues)에 넣어 처리하며, 즉시 처리하고 싶으면 `sendNow`를 사용합니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증 사용자를 제외하려면 `toOthers` 메서드를 사용 가능합니다.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 복구(Rescuing Broadcasts)

큐 서버가 다운되어 있거나 브로드캐스트 중 오류가 발생하면 예외가 발생하고, 사용자는 애플리케이션 오류 메시지를 볼 수 있습니다. 브로드캐스트가 핵심 기능이 아니라면, 이러한 예외로 사용자 경험이 저해되지 않도록 `ShouldRescue` 인터페이스를 이벤트에 구현할 수 있습니다.

이 인터페이스를 구현하면 Laravel의 [rescue 헬퍼함수](/docs/master/helpers#method-rescue)가 자동 적용되어, 예외를 로깅만 하고 애플리케이션 실행은 정상적으로 계속됩니다.

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
### 이벤트 리스닝 (Listening for Events)

[Laravel Echo](#client-side-installation)를 설치·초기화했다면, 이제 Laravel에서 브로드캐스트된 이벤트를 리스닝할 수 있습니다. `channel` 메서드로 채널 인스턴스를 받아, `listen`으로 이벤트를 리스닝합니다.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 경우 `private` 메서드를 쓰세요. 한 채널에 여러 이벤트를 리스닝할 수도 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 리스닝 중지

특정 이벤트에 대한 리스닝만 중지하고 싶을 때(채널을 아예 나가지 않고), `stopListening` 메서드를 사용합니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널에서 나가려면 Echo 인스턴스에서 `leaveChannel`을 호출합니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 그에 연결된 비공개·프레즌스 채널 전체에서 나가려면 `leave` 메서드를 사용하세요.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스

예시 코드에서는 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않는 것을 볼 수 있습니다. Echo는 기본적으로 이벤트가 `App\Events`에 있다고 가정합니다. 만약 다른 네임스페이스를 사용할 경우, Echo 인스턴스 생성 시 `namespace` 옵션으로 지정 가능합니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 이벤트 이름 앞에 `.`을 붙여 완전한 클래스 이름을 지정할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React, Vue에서 사용하기 (Using React or Vue)

Laravel Echo는 React, Vue Hook을 제공해 좀 더 쉽게 브로드캐스트 이벤트를 리스닝할 수 있습니다. `useEcho` Hook을 호출하면, 프라이빗 채널 이벤트를 리스닝할 수 있고, 컴포넌트가 unmount되면 채널을 자동으로 떠납니다.

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

여러 이벤트를 동시에 등록할 수도 있습니다.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트 payload의 타입을 지정하면 타입 안정성과 코드 편집이 더 쉬워집니다.

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

`useEcho` Hook은 컴포넌트가 unmount될 때 자동으로 채널을 떠나지만, 반환되는 함수를 사용해 직접 리스닝 시작/중지, 채널 떠나기를 제어할 수 있습니다.

```js
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 리스닝만 중단하기...
stopListening();

// 리스닝 재개...
listen();

// 채널 떠나기...
leaveChannel();

// 채널과 관련 프라이빗·프레즌스 채널 전부 떠나기...
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

// 리스닝만 중단...
stopListening();

// 리스닝 재시작...
listen();

// 채널 떠나기...
leaveChannel();

// 채널(+관련 채널) 전체 떠나기...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### 공개채널 연결

공개 채널에 접속하려면 `useEchoPublic` Hook을 사용합니다.

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
#### 프레즌스 채널 연결

프레즌스 채널에 연결하려면 `useEchoPresence` Hook을 사용합니다.

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

<a name="react-vue-connection-status"></a>
#### 연결 상태 확인

현재 WebSocket 연결 상태는 `useConnectionStatus` Hook으로 받을 수 있습니다. 이 값은 연결 상태가 바뀌면 자동으로 갱신됩니다.

```js
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

가능한 상태 값은:

- `connected` - WebSocket 서버와 정상적으로 연결됨
- `connecting` - 최초 연결 시도 중
- `reconnecting` - 연결 끊긴 후 재접속 시도 중
- `disconnected` - 연결되어 있지 않으며 재접속 시도도 안 함
- `failed` - 연결 실패, 재시도하지 않음

<a name="presence-channels"></a>
## 프레즌스 채널 (Presence Channels)

프레즌스 채널은 프라이빗 채널의 보안성을 바탕으로, 채널에 누가 접속해 있는지 알 수 있게 해줍니다. 예를 들어, 채팅방 인원 목록, 페이지 동시 접속자 표시 등 협업 기능 구현에 적합합니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인가

프레즌스 채널 역시 프라이빗 채널이므로 [채널 인가](#authorizing-channels)가 필요합니다. 단, 인가 콜백에서 true/false가 아니라 사용자 정보를 담은 배열을 반환해야 합니다. 이 배열은 자바스크립트로 모두 전송되고, 리스너들이 사용 가능합니다.

인가 실패 시에는 false 또는 null을 반환하세요.

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

프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용하세요. 반환되는 객체에서 `here`, `joining`, `leaving`, `error` 등 다양한 이벤트를 구독할 수 있습니다.

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

`here`는 채널 참여 직후, 접속 중인 모든 사용자의 정보 배열을 받습니다. `joining`은 새 사용자가 들어올 때, `leaving`은 사용자가 나갈 때 각각 호출됩니다. `error`는 인증 서버 응답이 200이 아니거나 JSON 파싱 오류일 때 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널 브로드캐스트

프레즌스 채널도 공개/프라이빗 채널처럼 이벤트를 받을 수 있습니다. 예를 들어, 채팅방에서 `NewMessage` 이벤트를 프레즌스 채널로 보내고 싶다면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel`을 반환하세요.

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

일반 이벤트처럼 `broadcast`, `toOthers`를 함께 사용할 수 있습니다.

```php
broadcast(new NewMessage($message));
broadcast(new NewMessage($message))->toOthers();
```

클라이언트에서는 Echo의 `listen` 메서드로 이벤트를 받을 수 있습니다.

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
> 모델 브로드캐스팅에 앞서 Laravel의 모델 브로드캐스트 컨셉과, 수동으로 브로드캐스트 이벤트를 작성·리스닝하는 방법을 숙지하세요.

애플리케이션의 [Eloquent 모델](/docs/master/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 경우가 많습니다. 이를 위해 직접 [커스텀 이벤트를 만들어](/docs/master/eloquent#events) `ShouldBroadcast`를 붙여 처리할 수도 있습니다.

하지만, 오직 브로드캐스트만을 위해 일일이 이벤트 클래스를 만드는 것은 번거로운 일입니다. Laravel에서는 Eloquent 모델이 자체적으로 상태변화 이벤트를 자동 브로드캐스트할 수 있도록 지원합니다.

시작하려면 Eloquent 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용하세요. 이와 함께 `broadcastOn` 메서드를 구현하여 방송할 채널(배열)을 반환합니다.

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

이렇게 설정하면 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동, 복구될 때 자동으로 이벤트가 브로드캐스트됩니다.

추가로, `broadcastOn` 메서드는 발생한 이벤트 종류(`created`, `updated`, `deleted`, `trashed`, `restored`)를 `$event` 인수로 받습니다. 이 변수로 상황에 따라 브로드캐스트 채널을 다르게 지정할 수 있습니다.

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

모델 브로드캐스트 이벤트 생성 과정을 커스터마이즈하고 싶다면, 모델에 `newBroadcastableEvent` 메서드를 정의해 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환할 수 있습니다.

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
#### 채널 이름 규칙

위 예제에서 `broadcastOn`이 `Channel` 인스턴스 대신 모델을 직접 반환하는 것을 볼 수 있습니다. 이 경우 Laravel은 모델 클래스명과 기본키를 조합해 자동으로 프라이빗 채널 인스턴스를 만듭니다(`App.Models.User.1` 등). 물론 직접 채널 인스턴스를 반환하여 전체 채널 이름을 지정하는 것도 가능합니다.

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

채널 생성자에 모델 인스턴스를 직접 넘겨도, 위 규칙에 따라 자동으로 채널명이 변환됩니다.

```php
return [new Channel($this->user)];
```

모델의 채널 이름을 직접 확인하려면 `broadcastChannel` 메서드를 호출하세요. 예를 들어 사용자 ID가 1이라면, `App.Models.User.1`이 반환됩니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 이름·페이로드 규칙

모델 브로드캐스트 이벤트는 별도의 이벤트 클래스가 아니므로, 이름과 페이로드는 관례에 따라 자동으로 생성됩니다. 즉, 모델 클래스(네임스페이스 제외)와 트리거된 이벤트 이름의 조합을 씁니다.

예를 들어, `App\Models\Post`가 업데이트되면, `PostUpdated` 이벤트 이름으로 아래와 같이 브로드캐스트됩니다.

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

`App\Models\User`가 삭제되면 `UserDeleted` 이벤트로 브로드캐스트됩니다.

커스텀 이벤트 이름·데이터가 필요하다면, 모델에 `broadcastAs`, `broadcastWith` 메서드를 구현할 수 있습니다. 각 메서드는 발생 이벤트명을 인수로 받아 케이스별로 결과를 다르게 지정합니다. `broadcastAs`에서 null을 반환하면 위 기본 규칙이 적용됩니다.

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
### 모델 브로드캐스트 리스닝 (Listening for Model Broadcasts)

`BroadcastsEvents` 트레이트를 추가하고 모델의 `broadcastOn` 메서드를 정의했다면, 이제 클라이언트에서 모델 이벤트를 리스닝할 수 있습니다. 기본적으로 [이벤트 리스닝](#listening-for-events) 문서를 먼저 읽어보세요.

우선 `private` 메서드로 채널 인스턴스를 가져오고, `listen`으로 이벤트를 구독합니다. 채널 이름은 [모델 브로드캐스트 네이밍 규칙](#model-broadcasting-conventions)에 맞춰야 합니다.

이벤트 이름은 반드시 `.`(dot)으로 시작해야 네임스페이스가 붙지 않고, payload에는 항상 `model` 프로퍼티가 포함됩니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React, Vue에서 모델 브로드캐스트 사용

React, Vue에서는 `useEchoModel` Hook을 통해 쉽게 모델 브로드캐스트를 리스닝할 수 있습니다.

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

payload 타입도 지정 가능하여, 타입 안정성과 IDE 자동완성이 편리해집니다.

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
> [Pusher Channels](https://pusher.com/channels) 사용 시, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 보낼 수 있습니다.

가끔 라라벨 서버에 요청하지 않고, 브라우저들끼리만 이벤트를 브로드캐스트하고 싶을 때가 있습니다(예: "입력중..." 표시 등). 이런 경우 Echo의 `whisper` 메서드를 활용합니다.

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

React, Vue Hook 사용 예시:

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

클라이언트 이벤트는 `listenForWhisper`로 수신할 수 있습니다.

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

React, Vue에서도 동일하게 사용할 수 있습니다.

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

이벤트 브로드캐스트와 [알림 기능](/docs/master/notifications)을 결합하면, 자바스크립트 앱에서 새 알림이 실시간으로 도착하는 것을 즉시 받을 수 있습니다(페이지 새로고침 불필요). 시작 전, 반드시 [브로드캐스트 알림 채널](/docs/master/notifications#broadcast-notifications) 문서를 확인하세요.

브로드캐스트 채널로 알림을 전송하도록 구성했다면, Echo의 `notification` 메서드로 실시간 수신이 가능합니다. 채널 이름은 알림을 받는 엔티티의 클래스 명칭과 동일해야 합니다.

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

React, Vue Hook을 사용하는 경우:

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

이 방식으로 `App\Models\User` 인스턴스에 전송되는 모든 `broadcast` 채널 알림이 콜백으로 전달됩니다. 해당 채널에 맞는 인가 콜백이 `routes/channels.php`에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 리스닝 중지

알림 리스닝을 중지하고 싶다면(채널 자체에서 나가지는 않고), `stopListeningForNotification` 메서드를 사용하세요.

```js
const callback = (notification) => {
    console.log(notification.type);
}

// 리스닝 시작
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// 리스닝 중지 (콜백은 동일해야 함)
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
