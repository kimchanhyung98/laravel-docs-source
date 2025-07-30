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
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스트와 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 권한 부여](#authorizing-channels)
    - [권한 부여 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [자기 자신 제외하기](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 복구](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 수신](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue 사용하기](#using-react-or-vue)
- [프레즌스 채널 (Presence Channels)](#presence-channels)
    - [프레즌스 채널 권한 부여](#authorizing-presence-channels)
    - [프레즌스 채널 참가](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규약](#model-broadcasting-conventions)
    - [모델 브로드캐스트 수신](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림 (Notifications)](#notifications)

<a name="introduction"></a>
## 소개

현대 웹 애플리케이션에서는 WebSocket을 사용하여 실시간으로 UI를 업데이트하는 경우가 많습니다. 서버에서 데이터가 변경되면 일반적으로 WebSocket 연결을 통해 메시지를 보내며, 클라이언트가 이를 처리합니다. WebSocket은 애플리케이션 서버를 계속해서 반복적으로 조회(polling)하는 방식보다 훨씬 효율적인 대안입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내 이메일로 발송하는 기능이 있다고 가정해 봅시다. 이 CSV 파일 생성에 몇 분이 걸리므로, 이를 [큐 작업](/docs/12.x/queues)을 통해 처리하도록 선택할 수 있습니다. CSV가 완성되어 이메일로 전송되면, 이벤트 브로드캐스팅을 통해 `App\Events\UserDataExported` 이벤트를 발생시켜 자바스크립트에서 이를 수신할 수 있습니다. 이렇게 하면 사용자가 페이지를 새로 고침하지 않고도 CSV가 이메일로 전송되었다는 메시지를 표시할 수 있습니다.

Laravel은 이런 기능들을 쉽게 구축할 수 있도록, 서버 사이드 Laravel [이벤트들](/docs/12.x/events)을 WebSocket 연결을 통해 "브로드캐스트"할 수 있는 기능을 제공합니다. Laravel 이벤트를 브로드캐스트하면 서버 측 Laravel 애플리케이션과 클라이언트 측 자바스크립트 애플리케이션 간에 같은 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 이름이 지정된 채널에 접속하고, 서버 측 Laravel 애플리케이션은 백엔드에서 이 채널들에 이벤트를 브로드캐스팅 합니다. 이벤트에는 프론트엔드에서 사용할 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원하는 드라이버

기본적으로 Laravel은 세 가지 서버 사이드 브로드캐스팅 드라이버를 포함하고 있습니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), 그리고 [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 Laravel 문서의 [이벤트와 리스너](/docs/12.x/events)를 반드시 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 빠른 시작

기본적으로 새 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어로 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 어떤 이벤트 브로드캐스팅 서비스를 사용할지 묻고, `config/broadcasting.php` 구성 파일과 사용자의 브로드캐스트 권한 부여 라우트와 콜백을 등록할 `routes/channels.php` 파일을 생성합니다.

Laravel은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버. 또한, `null` 드라이버가 포함되어 테스트 중 브로드캐스팅을 비활성화할 수 있습니다. 이 드라이버들은 모두 `config/broadcasting.php` 파일에 설정 예제가 포함되어 있습니다.

애플리케이션의 모든 이벤트 브로드캐스팅 구성은 `config/broadcasting.php` 파일에 저장됩니다. 만약 이 파일이 없다면, Artisan `install:broadcasting` 명령어를 실행하면 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, 이제 [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)와 [이벤트 수신하기](#listening-for-events)를 학습할 준비가 된 것입니다. Laravel React 또는 Vue [스타터 킷](/docs/12.x/starter-kits)을 사용하는 경우, Echo의 [useEcho 훅](#using-react-or-vue)을 통해 이벤트를 쉽게 수신할 수 있습니다.

> [!NOTE]
> 어떤 이벤트도 브로드캐스팅 전에 반드시 [큐 워커](/docs/12.x/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 처리되어, 애플리케이션의 응답 속도가 이벤트 브로드캐스트로 인해 심각하게 느려지지 않도록 하기 때문입니다.

<a name="server-side-installation"></a>
## 서버 측 설치

Laravel 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션 내에서 몇 가지 설정을 하고 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스트 드라이버가 Laravel 이벤트를 브로드캐스트하여, 클라이언트 브라우저에서 Laravel Echo 자바스크립트 라이브러리가 이를 수신합니다. 각 설치 단계를 차근차근 안내하겠습니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스터로 사용할 경우, `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 붙여 빠르게 설치할 수 있습니다. 이 명령어는 Reverb에 필요한 Composer와 NPM 패키지를 설치하고, `.env` 파일에 관련 변수를 추가해 줍니다:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령어를 실행하면 Laravel Reverb 설치 여부를 묻습니다. 물론 직접 Composer를 이용해 수동으로도 Reverb를 설치할 수 있습니다:

```shell
composer require laravel/reverb
```

패키지를 설치한 뒤에는, 다음 명령어로 Reverb 설치를 진행해 설정 파일을 발행하고 환경변수도 추가하며, 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan reverb:install
```

자세한 설치 및 사용법은 [Reverb 문서](/docs/12.x/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 사용할 때는, `install:broadcasting` Artisan 명령어에 `--pusher` 옵션을 붙여 빠르게 설치하세요. 명령어 실행 시 Pusher 자격 증명 정보를 요청하며, Pusher PHP와 자바스크립트 SDK를 설치하고 `.env` 파일에 환경 변수를 추가합니다:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 직접 설정하려면 Composer로 Pusher 채널 PHP SDK를 설치합니다:

```shell
composer require pusher/pusher-php-server
```

다음으로 `config/broadcasting.php` 파일에서 Pusher 자격 증명을 설정하세요. 이 파일에는 이미 예시 설정이 포함되어 있습니다. 보통 `.env` 파일에서 다음과 같이 설정합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 내 `pusher` 설정은 클러스터 같은 추가 `options`도 지정할 수 있습니다.

마지막으로, `.env` 파일에서 기본 브로드캐스트 연결을 `pusher`로 설정하세요:

```ini
BROADCAST_CONNECTION=pusher
```

그 후, 클라이언트 측에서 브로드캐스트 이벤트를 받을 [Laravel Echo](#client-side-installation)를 설치 및 설정하면 됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서에서는 "Pusher 호환 모드"의 Ably 사용법을 설명합니다. 그러나 Ably 팀은 Ably 고유 기능을 활용하는 전용 브로드캐스터 및 Echo 클라이언트를 권장하며, 이를 위한 드라이버도 유지 관리하고 있습니다. Ably 드라이버 사용법은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

Ably를 이벤트 브로드캐스터로 사용하려면, `install:broadcasting` Artisan 명령어에 `--ably` 옵션을 붙여 실행하세요. 이 명령어는 Ably 자격 증명 정보를 묻고, Ably PHP와 JS SDK를 설치하며 `.env` 파일에 알맞은 환경 변수를 추가합니다:

```shell
php artisan install:broadcasting --ably
```

**계속하기 전, 반드시 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화하세요. 해당 설정은 Ably 대시보드의 "Protocol Adapter Settings"에서 할 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 직접 설정하려면 Composer로 Ably PHP SDK를 설치합니다:

```shell
composer require ably/ably-php
```

다음으로 `config/broadcasting.php` 파일 내 Ably 자격 증명을 설정하세요. 이 파일에 예시가 포함되어 있으며, 일반적으로 `ABLY_KEY` [환경 변수](/docs/12.x/configuration#environment-configuration)를 통해 지정합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 기본 브로드캐스트 연결을 `ably`로 설정하세요:

```ini
BROADCAST_CONNECTION=ably
```

이제 클라이언트 측에서 브로드캐스트 이벤트를 수신할 Laravel Echo를 설치하고 설정하면 됩니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버 측 브로드캐스터가 보낸 이벤트 수신을 간편하게 만드는 자바스크립트 라이브러리입니다.

`install:broadcasting` Artisan 명령어로 Laravel Reverb를 설치하면 Reverb와 Echo의 설정과 기본 코드가 자동으로 애플리케이션에 삽입됩니다. 수동으로 Echo를 설정하려면 아래 지침을 따라주세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

Laravel Echo를 수동으로 설정하려면, 우선 Reverb가 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지를 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

설치가 완료되면, `resources/js/bootstrap.js` 파일 아래쪽에 다음처럼 새 Echo 인스턴스를 생성하세요:

```js tab=JavaScript
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

React 환경에서는 다음과 같이 설정할 수 있습니다:

```js tab=React
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

Vue 환경에서는 다음과 같이 사용합니다:

```js tab=Vue
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

이후 애플리케이션 자산을 컴파일하세요:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo 버전 1.16.0 이상을 필요로 합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

Laravel Echo는 서버 측 브로드캐스트 드라이버로부터 브로드캐스트된 이벤트 구독을 간편하게 처리합니다.

`install:broadcasting --pusher` Artisan 명령어를 사용해 Pusher와 Echo를 자동으로 설정할 수 있지만, 수동 구성도 가능합니다.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

클라이언트에서 Echo를 수동으로 구성하려면 `laravel-echo`와 `pusher-js` 패키지를 설치하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```

그 다음 `resources/js/bootstrap.js` 파일에 다음과 같이 Echo 인스턴스를 만듭니다:

```js tab=JavaScript
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

React:

```js tab=React
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

Vue:

```js tab=Vue
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

`.env` 파일에 Pusher 환경 변수들을 설정하세요. 만약 없으면 직접 추가하면 됩니다:

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

설정이 끝나면 애플리케이션 자산을 컴파일하세요:

```shell
npm run build
```

> [!NOTE]
> 자바스크립트 자산 컴파일에 관해 자세히 알고 싶다면 [Vite 문서](/docs/12.x/vite)를 참조하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 Pusher 클라이언트 인스턴스를 따로 설정해 두었다면, Echo 생성 시 `client` 옵션을 통해 전달할 수도 있습니다:

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
> 아래 문서는 "Pusher 호환 모드"로 Ably를 사용하기 위한 예제입니다. Ably 팀에서 제공하는 고유 기능을 활용한 별도의 공식 브로드캐스터 및 Echo 클라이언트가 있으니, 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

Laravel Echo는 서버 측 브로드캐스트 드라이버가 보낸 이벤트를 쉽게 수신할 수 있도록 돕는 자바스크립트 라이브러리입니다.

`install:broadcasting --ably` Artisan 명령어를 사용하면 Ably와 Echo 설정이 자동으로 처리됩니다. 수동 설정을 원한다면 아래 절차를 따르세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

Echo를 수동으로 설정하려면, `laravel-echo`와 `pusher-js` 패키지를 설치하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```

**먼저, Ably 애플리케이션 설정에서 "Pusher 프로토콜 지원"을 활성화해야 합니다. 이 설정은 Ably 대시보드의 "Protocol Adapter Settings"에서 할 수 있습니다.**

설치가 완료되면 `resources/js/bootstrap.js` 파일에 다음과 같이 Echo 인스턴스를 만드세요:

```js tab=JavaScript
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

React:

```js tab=React
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

Vue:

```js tab=Vue
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

위 예제에서 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 Ably 공개 키 값으로, Ably 키에서 `:` 문자 이전 부분입니다.

마지막으로 애플리케이션 자산을 컴파일하세요:

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 자산 컴파일에 대해 알고 싶다면 [Vite 문서](/docs/12.x/vite)를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel 이벤트 브로드캐스팅은 서버 측 Laravel 이벤트를 드라이버 기반 WebSocket 방식을 통해 클라이언트 측 자바스크립트 애플리케이션으로 전송합니다. 현재 Laravel은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), 그리고 [Ably](https://ably.com) 드라이버를 제공합니다. 이 이벤트들은 클라이언트에서 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 통해 쉽게 소비할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트되며, 채널은 공개 또는 비공개로 지정할 수 있습니다. 공개 채널은 모든 방문자가 인증 없이 구독 가능하지만, 비공개 채널 구독은 인증 및 권한 부여가 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

각 브로드캐스트 구성 요소를 살펴보기 전에, 전자상거래 스토어 예제로 개념을 간단히 살펴봅시다.

애플리케이션에 사용자가 자신의 주문 배송 상태를 보는 페이지가 있다고 가정합니다. 주문 배송 상태 업데이트가 처리될 때 `OrderShipmentStatusUpdated` 이벤트가 발생합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 상태를 볼 때 페이지 새로 고침 없이 실시간 상태 업데이트를 받고 싶다면, `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이것으로 이벤트 발생 시 자동으로 브로드캐스트됩니다:

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
     * 주문 인스턴스입니다.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

`ShouldBroadcast` 인터페이스는 `broadcastOn` 메서드 구현을 요구하는데, 이벤트가 브로드캐스트될 채널을 반환해야 합니다. 생성된 이벤트 클래스에는 템플릿 메서드가 이미 있으므로, 세부 정보만 채우면 됩니다. 주문 생성자만 상태 업데이트를 보도록 하고 싶으므로, 주문에 연결된 비공개 채널에 브로드캐스트합니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트될 채널을 반환합니다.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 브로드캐스트하려면 배열을 반환할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트될 여러 채널을 반환합니다.
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

비공개 채널은 사용자가 구독 권한이 있어야 합니다. 권한 규칙은 애플리케이션의 `routes/channels.php` 파일에서 정의할 수 있습니다. 예를 들어, `orders.1` 비공개 채널에 접속하는 사용자가 실제 주문 생성자인지 확인하는 코드는 다음과 같습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과, 해당 채널 구독 권한 여부를 `true`/`false`로 반환하는 콜백을 인자로 받습니다.

권한 콜백의 첫 번째 인자는 인증된 사용자이며, 그 다음 인자들은 와일드카드 부분을 의미합니다. 위 예제에서는 `{orderId}`가 와일드카드입니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신하기

다음으로 자바스크립트 애플리케이션에서 이벤트를 수신합니다. [Laravel Echo](#client-side-installation)을 통해 쉽게 할 수 있으며, 기본적으로 이벤트의 모든 public 속성이 포함되어 전달됩니다:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
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
## 브로드캐스트 이벤트 정의하기

Laravel에게 특정 이벤트를 브로드캐스트할 것을 알리려면, 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 자동으로 생성하는 이벤트 클래스에 이미 포함되어 있어 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 단일 메서드 `broadcastOn` 구현을 요구하며, 이 메서드는 이벤트가 브로드캐스트될 채널이나 채널 배열을 반환해야 합니다. 반환 타입은 `Channel`, `PrivateChannel`, `PresenceChannel` 인스턴스여야 합니다. `Channel`은 아무나 구독 가능한 공개 채널이고, `PrivateChannel`과 `PresenceChannel`은 [채널 권한 부여](#authorizing-channels)가 필요한 비공개 채널입니다:

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
     * 이벤트가 브로드캐스트될 채널 반환.
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

`ShouldBroadcast`를 적용했다면, 평소처럼 [이벤트를 발생](/docs/12.x/events)시키기만 하면 됩니다. 발행된 이벤트는 자동으로 [큐 작업](/docs/12.x/queues)을 통해 지정한 브로드캐스트 드라이버로 브로드캐스트됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스를 이름으로 사용해 브로드캐스트합니다. 하지만 `broadcastAs` 메서드를 정의해 브로드캐스트용 이름을 사용자 정의할 수 있습니다:

```php
/**
 * 이벤트의 브로드캐스트 이름.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs`를 사용해 이름을 정의했다면, Echo에서 리스너 등록 시 이벤트 이름 앞에 `.`을 붙여 등록해야 합니다. 이렇게 하면 Echo가 앱 네임스페이스 접두어를 붙이지 않습니다:

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

브로드캐스트 시, 이벤트의 모든 `public` 속성은 자동으로 직렬화되어 페이로드로 보내집니다. 예를 들어 이벤트에 `$user`라는 public 속성이 Eloquent 모델이라면, 브로드캐스트 페이로드는 다음과 같습니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

브로드캐스트 페이로드를 더 세밀하게 제어하려면, `broadcastWith` 메서드를 이벤트에 추가할 수 있습니다. 이 메서드는 배열을 반환하며, 그 데이터가 이벤트 페이로드가 됩니다:

```php
/**
 * 브로드캐스트할 데이터를 반환.
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

기본적으로 각 브로드캐스트 이벤트는 `queue.php` 구성 파일의 기본 큐 연결과 큐 이름에 따라 대기열에 추가됩니다. 이벤트 클래스에 `connection`과 `queue` 속성을 정의해 큐 연결 및 이름을 직접 지정할 수 있습니다:

```php
/**
 * 브로드캐스트 시 사용할 큐 연결 이름.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스트 작업을 넣을 큐 이름.
 *
 * @var string
 */
public $queue = 'default';
```

또는 `broadcastQueue` 메서드를 정의해 큐 이름을 반환할 수도 있습니다:

```php
/**
 * 브로드캐스트 작업을 넣을 큐 이름.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

만약 동기(sync) 큐를 사용해 즉시 브로드캐스트하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다:

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

특정 조건이 참일 때만 이벤트를 브로드캐스트하고 싶으면, 이벤트에 `broadcastWhen` 메서드를 정의하세요:

```php
/**
 * 이벤트 브로드캐스트 여부를 결정합니다.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 브로드캐스트 이벤트를 발생시키면, 큐 작업이 트랜잭션 커밋 전에 처리될 수 있습니다. 이때 모델이나 레코드 변경 사항이 아직 DB에 반영되지 않으며, 트랜잭션 내 새로 생성된 모델이나 레코드가 존재하지 않을 수도 있습니다. 이런 상황에서 이벤트가 해당 모델이나 데이터를 참조하면 예기치 못한 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`라면, `ShouldDispatchAfterCommit` 인터페이스를 이벤트에 구현하여 해당 이벤트만 트랜잭션 커밋 후에 디스패치하도록 할 수 있습니다:

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
> 이 문제를 회피하는 방법에 대해서는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 권한 부여

비공개 채널은 현재 인증된 사용자가 채널을 구독할 권한이 있는지 확인해야 합니다. 이는 채널명과 함께 Laravel 애플리케이션에 HTTP 요청을 보내어, 애플리케이션이 사용자의 구독 권한을 판단하는 방식입니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 비공개 채널 구독 권한 요청은 자동으로 처리됩니다.

브로드캐스팅 활성화 시 Laravel은 `/broadcasting/auth` 라우트를 자동으로 등록하며, 이 라우트는 `web` 미들웨어 그룹에 포함됩니다.

<a name="defining-authorization-callbacks"></a>
### 권한 부여 콜백 정의하기

실제 현재 인증된 사용자가 특정 채널을 구독할 권한이 있는지 결정하는 로직을 `routes/channels.php` 파일에 정의합니다. `install:broadcasting` 명령어로 생성된 이 파일에 `Broadcast::channel` 메서드를 사용해 권한 부여 콜백을 등록하세요:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널명과, 구독 권한 여부(true/false)를 반환하는 콜백을 인자로 받습니다.

모든 권한 콜백은 첫 번째 인자로 현재 인증된 사용자 객체를 받으며, 다음 인자들은 와일드카드 매개변수로 전달됩니다. 위 예제에서는 `{orderId}`가 와일드카드입니다.

등록된 권한 부여 콜백 목록은 Artisan 명령어 `channel:list`로 확인할 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 권한 콜백 모델 바인딩

HTTP 라우트처럼, 채널 라우트도 암묵적 또는 명시적 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어 주문 ID 대신 실제 `Order` 모델 인스턴스를 받을 수 있습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과는 달리, 채널 모델 바인딩은 암묵적 [스코핑 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 하지만 이는 드문 문제이며, 대부분 채널은 단일 모델의 고유 기본 키를 기준으로 범위를 지정합니다.

<a name="authorization-callback-authentication"></a>
#### 권한 콜백 인증

비공개 및 프레즌스 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않으면 권한이 자동으로 거부되고 콜백은 호출되지 않습니다. 필요한 경우 여러 커스텀 가드를 지정할 수도 있습니다:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션이 많은 채널을 사용하면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 이 경우, 권한 부여에 클로저 대신 채널 클래스를 사용할 수 있습니다. `make:channel` Artisan 명령어로 `App/Broadcasting` 디렉토리에 새 채널 클래스를 생성할 수 있습니다:

```shell
php artisan make:channel OrderChannel
```

그 후 `routes/channels.php` 파일에 채널을 등록합니다:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

마지막으로 해당 채널 클래스의 `join` 메서드에 권한 부여 로직을 구현하세요. 이 메서드는 이전에 클로저에서 하던 권한 검사 역할을 합니다. 라우트 모델 바인딩도 사용할 수 있습니다:

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
     * 사용자의 채널 접근 권한 인증.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Laravel 서비스 컨테이너가 채널 클래스 인스턴스를 자동으로 생성하므로, 생성자에 필요한 의존성을 타입힌트로 선언하면 주입 받을 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현했다면, 이벤트 발생 시 해당 이벤트를 디스패치하기만 하면 브로드캐스트됩니다. 이벤트 디스패처는 이벤트가 `ShouldBroadcast`로 표시된 것을 감지해 브로드캐스트 큐 작업에 넣습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 자기 자신 제외하기 (Only to Others)

때론 현재 사용자를 제외한 채널 구독자 모두에게 이벤트를 브로드캐스트하고 싶을 때가 있습니다. `broadcast` 헬퍼와 `toOthers` 메서드를 사용하면 이를 구현할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

예를 들어, 할 일 목록 애플리케이션에서 사용자가 새 할 일을 만들면, 할 일 생성 API 요청에 대한 응답에서 즉시 목록에 추가하면서도, 브로드캐스트 이벤트로도 다른 사용자의 목록에 동기화합니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만 브로드캐스트 이벤트 리스너도 할 일을 추가한다면 중복이 발생합니다. `toOthers`를 통해 현재 사용자에게는 브로드캐스트하지 않도록 해 해결할 수 있습니다.

> [!WARNING]
> `toOthers` 메서드를 호출하려면 이벤트 클래스가 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Echo 인스턴스가 초기화되면 소켓 ID가 연결에 할당됩니다. Axios 글로벌 인스턴스를 사용하는 경우 이 소켓 ID가 자동으로 모든 요청 헤더에 `X-Socket-ID`로 포함됩니다. 그 후 `toOthers`를 호출하면, Laravel이 이 소켓 ID를 참조해 해당 연결을 제외합니다.

글로벌 Axios 인스턴스를 사용하지 않는다면, 수동으로 `X-Socket-ID` 헤더를 보내야 하며 Echo에서 소켓 ID를 다음과 같이 받을 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

여러 브로드캐스트 커넥션이 존재하고, 기본 연결이 아닌 다른 드라이버로 이벤트를 브로드캐스트하려면 `via` 메서드를 사용하세요:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또한, `InteractsWithBroadcasting` 트레이트를 이벤트 클래스에 적용한 후 생성자에서 `broadcastVia` 메서드를 호출해 기본 연결을 지정할 수도 있습니다:

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

간단한 이벤트를 별도의 클래스 없이 브로드캐스트하고 싶을 때 `Broadcast` 팩사드를 사용할 수 있습니다. 익명 이벤트를 이렇게 전송합니다:

```php
Broadcast::on('orders.'.$order->id)->send();
```

이렇게 하면 다음과 같은 이벤트가 브로드캐스트됩니다:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`와 `with` 메서드로 이름과 데이터를 커스터마이징할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

이 경우 브로드캐스트 이벤트는 다음과 같이 전송됩니다:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

비공개 혹은 프레즌스 채널에 익명 이벤트를 보내려면 `private`, `presence` 메서드를 사용하세요:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 이벤트를 큐 작업으로 디스패치합니다. 즉시 브로드캐스트하려면 `sendNow` 메서드를 사용하세요:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증 사용자를 제외하고 브로드캐스트하려면 `toOthers` 메서드를 체인하세요:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 복구 (Rescuing Broadcasts)

큐 서버가 오프라인이거나 브로드캐스트 도중 예외 발생 시, 기본적으로 사용자에게 에러가 표시됩니다. 브로드캐스팅이 애플리케이션 핵심 기능 보조용일 경우, 이런 예외가 사용자 경험을 방해하지 않도록 이벤트 클래스에 `ShouldRescue` 인터페이스를 구현하면 됩니다.

이 인터페이스가 적용된 이벤트는 Laravel의 [rescue 헬퍼 함수](/docs/12.x/helpers#method-rescue)를 통해 브로드캐스트 중 예외를 포착하고, 로그로 남기며 사용자 흐름을 중단하지 않습니다:

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
## 브로드캐스트 수신

<a name="listening-for-events"></a>
### 이벤트 수신하기

[Laravel Echo 설치 및 인스턴스화](#client-side-installation) 후, 이벤트 수신을 시작할 수 있습니다. 먼저 `channel` 메서드를 사용해 채널 인스턴스를 가져오고, 이어서 `listen` 메서드로 특정 이벤트를 구독합니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널 이벤트를 수신하려면 `private` 메서드를 쓰세요. 하나의 채널에 대해 여러 이벤트를 연속으로 구독할 수도 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중지하기

채널은 떠나지 않고 특정 이벤트만 수신을 중지하려면 `stopListening` 메서드를 호출하면 됩니다:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 완전히 탈퇴하려면 `leaveChannel` 메서드를 호출하세요:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 관련된 비공개, 프레즌스 채널 모두를 나가려면 `leave` 메서드를 사용합니다:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

Echo가 자동으로 이벤트 클래스가 `App\Events` 네임스페이스에 있다고 가정하기 때문에, 예시에서 전체 네임스페이스를 명시하지 않았던 것입니다. Echo 인스턴스를 만들 때 `namespace` 옵션을 넣어 루트 네임스페이스를 설정할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 이벤트 이름 앞에 `.`을 붙여 완전한 클래스명을 사용할 수도 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue 사용하기

Laravel Echo에는 React와 Vue용 훅이 포함되어 있어 이벤트 수신이 간편합니다. `useEcho` 훅을 호출하면 비공개 이벤트를 수신할 수 있습니다. 이 훅은 컴포넌트 언마운트 시 채널을 자동으로 나갑니다:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
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

여러 이벤트를 배열로 넣어 수신할 수도 있습니다:

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트 페이로드의 타입을 지정해 더 엄격하고 편한 편집도 가능합니다:

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

`useEcho` 훅은 자동으로 채널을 떠나지만, 반환된 함수들을 이용해 프로그램적으로 수신을 중지하거나 재개하고, 채널을 나갈 수도 있습니다:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 이벤트 수신만 중지...
stopListening();

// 다시 수신 시작...
listen();

// 채널 나가기...
leaveChannel();

// 채널과 관련된 비공개 및 프레즌스 채널 모두 나가기...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 이벤트 수신만 중지...
stopListening();

// 다시 수신 시작...
listen();

// 채널 나가기...
leaveChannel();

// 채널과 관련된 비공개 및 프레즌스 채널 모두 나가기...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### 공개 채널 연결하기

공개 채널에 연결하려면 `useEchoPublic` 훅을 사용합니다:

```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### 프레즌스 채널 연결하기

프레즌스 채널에 연결하려면 `useEchoPresence` 훅을 사용합니다:

```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="presence-channels"></a>
## 프레즌스 채널 (Presence Channels)

프레즌스 채널은 비공개 채널의 보안을 기반으로 하면서도, 누가 채널에 구독했는지를 알 수 있게 해 줍니다. 이를 통해 사용자가 동일한 페이지를 보고 있음을 알리는 기능이나 채팅방 사용자 목록 구현 등의 협업 기능을 쉽게 만들 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 권한 부여

프레즌스 채널도 비공개 채널이므로 사용자가 접근 권한이 있는지 인증해야 합니다. 그러나 권한 콜백에서 권한 허용 시 `true`를 반환하는 대신, 사용자에 관한 배열 데이터를 반환해야 합니다.

권한 콜백에서 반환한 데이터는 프론트엔드의 프레즌스 채널 이벤트 리스너에서 사용할 수 있습니다. 권한이 없으면 `false`나 `null`을 반환하세요:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참가

프레즌스 채널에 참가하려면 Echo의 `join` 메서드를 사용합니다. 이 메서드는 `PresenceChannel` 인스턴스를 반환하며, `listen` 메서드 외에 `here`, `joining`, `leaving` 이벤트도 구독할 수 있습니다:

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // 현재 채널에 구독 중인 사용자 목록
    })
    .joining((user) => {
        console.log(user.name); // 새로 참여한 사용자 정보
    })
    .leaving((user) => {
        console.log(user.name); // 채널 나간 사용자 정보
    })
    .error((error) => {
        console.error(error); // 인증 실패나 JSON 파싱 문제 처리
    });
```

`here` 콜백은 채널 입장 직후 호출되며, 현재 구독자 전체의 사용자 정보를 배열로 받습니다. `joining`과 `leaving`은 사용자가 채널에 접속하거나 나갈 때 각각 호출됩니다. `error`는 인증 요청이 200 이외 코드로 실패하거나 반환된 JSON 파싱에 문제가 있을 때 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅

프레즌스 채널은 공개 및 비공개 채널과 동일하게 이벤트를 받을 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 프레즌스 채널로 브로드캐스트하려면, 이벤트 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환합니다:

```php
/**
 * 이벤트가 브로드캐스트될 채널 반환.
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

위 예제처럼 이벤트를 브로드캐스트할 때 `broadcast` 헬퍼와 `toOthers` 메서드를 사용해 현재 사용자를 제외할 수 있습니다:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

클라이언트 측에서는 Echo의 `listen` 메서드로 프레즌스 채널 이벤트도 구독할 수 있습니다:

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
> 모델 브로드캐스팅을 읽기 전에 Laravel의 모델 브로드캐스팅과 Eloquent 모델 상태 변경 이벤트를 직접 정의하고 리스닝하는 방법을 먼저 이해하면 좋습니다.

일반적으로 Eloquent 모델이 생성, 업데이트, 삭제될 때 이벤트를 브로드캐스트합니다. 물론, 이를 위해 이벤트 클래스를 직접 정의하고 `ShouldBroadcast`를 구현할 수도 있습니다.

하지만 애플리케이션에서 별도로 사용하지 않는 경우라면, 방송만 위한 이벤트 클래스를 만드는 게 번거로울 수 있습니다. 이를 위해 Laravel은 Eloquent 모델 상태 변화를 자동으로 브로드캐스트하도록 할 수 있습니다.

시작하려면 Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 적용하고, `broadcastOn` 메서드를 정의해서 모델 이벤트가 브로드캐스트될 채널 배열을 반환하세요:

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
     * 게시글 소유자 사용자.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트될 채널 반환.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이렇게 하면 모델 인스턴스가 생성, 업데이트, 삭제, 휴지통 이동, 복원될 때 자동으로 이벤트를 브로드캐스트합니다.

또한 `broadcastOn` 메서드는 `$event` 인자로 발생한 모델 이벤트 종류(`created`, `updated`, `deleted`, `trashed`, `restored`) 문자열을 받습니다. 이 변수 값에 따라 브로드캐스트할 채널을 조정할 수도 있습니다:

```php
/**
 * 모델 이벤트가 브로드캐스트될 채널 반환.
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

Laravel이 모델 브로드캐싱 이벤트를 생성하는 방식을 바꾸려면 `newBroadcastableEvent` 메서드를 정의하세요. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 새 브로드캐스트 가능한 모델 이벤트 생성.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### 모델 브로드캐스팅 규약

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 규약

위 예제의 `broadcastOn` 메서드는 `Channel` 인스턴스가 아니라 Eloquent 모델을 반환했습니다. 이 경우 Laravel은 모델 클래스명과 기본 키를 조합한 채널 이름으로 `PrivateChannel` 인스턴스를 자동 생성합니다.

예를 들어 `App\Models\User` 모델에서 ID가 1인 경우, 채널 이름은 `App.Models.User.1`로 변환됩니다. 물론 직접 `Channel` 인스턴스를 반환해 세밀하게 제어할 수도 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트될 채널 반환.
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

채널 클래스 생성자에 모델을 전달할 경우 Laravel이 위 규칙에 따라 모델을 채널 이름 문자열로 변환합니다:

```php
return [new Channel($this->user)];
```

모델의 채널 이름을 확인하려면 `broadcastChannel` 메서드를 호출하세요. 예를 들어 `App\Models\User` 모델에서 ID가 1이면 다음을 반환합니다:

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규약

모델 브로드캐스트 이벤트는 실제 이벤트 클래스를 가지지 않으므로, Laravel은 모델 클래스 이름(네임스페이스 제외)과 발생한 모델 이벤트 타입을 조합해 이벤트 이름과 페이로드를 생성합니다.

예를 들어 `App\Models\Post` 모델이 업데이트되면, 클라이언트에서는 `PostUpdated` 이벤트를 수신하고 페이로드는 다음과 같습니다:

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

`App\Models\User` 모델이 삭제되면 `UserDeleted`라는 이벤트가 브로드캐스트됩니다.

원한다면, `broadcastAs`와 `broadcastWith` 메서드를 모델에 추가해 이름과 페이로드를 세부적으로 정의할 수 있습니다. 이 메서드들은 `$event` 인자를 받아 모델 이벤트 종류별로 다르게 조정할 수 있습니다. `broadcastAs`가 `null`을 반환하면 기본 규칙을 사용합니다:

```php
/**
 * 모델 이벤트 브로드캐스트 이름.
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
### 모델 브로드캐스트 수신

모델에 `BroadcastsEvents` 트레이트를 추가하고 `broadcastOn` 메서드를 정의했다면, 이제 클라이언트에서 모델 브로드캐스트 이벤트를 수신할 수 있습니다. 먼저 [이벤트 수신하기](#listening-for-events) 문서를 참고하세요.

주로 `private` 메서드에 Laravel 모델 브로드캐스팅 규약을 따른 채널 이름을 넣고, `listen`으로 이벤트를 수신합니다. 모델 브로드캐스트 이벤트는 실제 클래스를 갖지 않으므로 [이벤트 이름 앞에 `.`](#model-broadcasting-event-conventions)을 붙여 네임스페이스에서 제외시켜야 합니다.

각 브로드캐스트 이벤트에는 `model` 속성이 포함되어 방송된 모델의 모든 공개 속성을 포함합니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

React 또는 Vue를 사용한다면 Laravel Echo의 `useEchoModel` 훅으로 모델 브로드캐스트를 쉽게 구독할 수 있습니다:

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

모델 이벤트 페이로드 타입을 지정해 더욱 엄격한 타입 검증과 편집 편의를 얻을 수도 있습니다:

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
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용하는 경우, [대시보드](https://dashboard.pusher.com/)의 "앱 설정"에서 "클라이언트 이벤트" 옵션을 반드시 활성화해야 클라이언트 이벤트를 보낼 수 있습니다.

클라이언트가 Laravel 애플리케이션을 거치지 않고 직접 다른 연결된 클라이언트에 이벤트를 보내려는 경우가 있습니다. 예를 들어, 누군가 입력 중임을 다른 사용자에게 알리는 "타이핑 중" 알림 같은 경우입니다.

이때 Echo의 `whisper` 메서드를 사용합니다:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

React:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

Vue:

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

클라이언트 이벤트 수신은 `listenForWhisper` 메서드를 사용합니다:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

React:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

Vue:

```vue tab=Vue
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

이벤트 브로드캐스팅과 [알림](/docs/12.x/notifications)을 결합하면, 자바스크립트 애플리케이션이 새 알림을 받을 때 페이지 새로 고침 없이 실시간으로 알림을 처리할 수 있습니다. 시작하기 전에 [브로드캐스트 알림 채널](/docs/12.x/notifications#broadcast-notifications) 문서를 먼저 읽어보세요.

알림이 브로드캐스트 채널을 사용하도록 설정하면 Echo의 `notification` 메서드로 알림 이벤트를 구독할 수 있습니다. 채널명은 알림을 받는 엔터티(예: 사용자) 클래스명과 일치해야 합니다:

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

React:

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

Vue:

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

이 예제에서 `App\Models\User` 인스턴스에 방송된 모든 알림을 콜백이 받습니다. `routes/channels.php`에 `App.Models.User.{id}` 채널 권한 콜백이 등록되어 있습니다.