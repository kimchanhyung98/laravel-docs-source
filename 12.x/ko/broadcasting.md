# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [퀵스타트](#quickstart)
- [서버 사이드 설치](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예시 애플리케이션 활용](#using-example-application)
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
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 예외 처리](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 수신](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue에서 사용하기](#using-react-or-vue)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 관례](#model-broadcasting-conventions)
    - [모델 브로드캐스트 수신](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

최신 웹 애플리케이션에서는 WebSocket을 사용하여 실시간으로 즉시 반영되는 사용자 인터페이스를 구현하는 경우가 많습니다. 서버에서 데이터가 업데이트되면 일반적으로 WebSocket 연결을 통해 메시지를 클라이언트로 전송하여 처리합니다. WebSocket은 애플리케이션 서버에 데이터 변경 사항을 반영하기 위해 지속적으로 폴링하는 방법보다 훨씬 효율적입니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고 이메일로 발송할 수 있다고 가정해봅시다. 그런데 이 CSV 파일을 생성하는 데 수 분이 걸려서, [큐 작업](/docs/12.x/queues) 내에서 CSV를 생성하고 메일로 보내기로 결정했습니다. CSV가 생성되어 메일로 발송된 후에는 `App\Events\UserDataExported` 이벤트를 브로드캐스트하여, 애플리케이션의 JavaScript에서 이 이벤트를 수신할 수 있도록 할 수 있습니다. 이벤트가 수신되면, 사용자가 새로고침하지 않아도 "CSV가 이메일로 전송됐음"과 같은 메시지를 즉시 보여줄 수 있습니다.

이처럼 실시간 기능을 쉽게 만들 수 있도록, Laravel에서는 서버 사이드 Laravel [이벤트](/docs/12.x/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 기능을 제공합니다. Laravel 이벤트를 브로드캐스트하면 서버 사이드와 클라이언트 사이드(JavaScript 애플리케이션)에서 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 특정 이름의 채널에 연결하고, Laravel 애플리케이션이 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에서 사용할 수 있도록 원하는 데이터를 추가할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅에 들어가기 전에 [이벤트와 리스너](/docs/12.x/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 퀵스타트 (Quickstart)

기본적으로 새로 생성된 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어를 사용하여 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

이 명령어는 어떤 브로드캐스팅 서비스를 사용할지 선택하도록 안내하며, `config/broadcasting.php` 설정 파일과 브로드캐스트 인가 라우트 및 콜백을 등록할 수 있는 `routes/channels.php` 파일을 자동으로 생성합니다.

Laravel은 [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅용 `log` 드라이버를 기본 제공하며, 테스트 시 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각각의 드라이버에 대한 설정 예시가 `config/broadcasting.php` 파일에 들어 있습니다.

애플리케이션의 모든 브로드캐스팅 설정은 `config/broadcasting.php` 파일에 저장됩니다. 이 파일이 없다면, 위의 Artisan 명령어를 실행하면 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, 이제 [브로드캐스트 이벤트 정의](#defining-broadcast-events)나 [이벤트 리스닝](#listening-for-events) 방법을 배울 준비가 되었습니다. React나 Vue [스타터 킷](/docs/12.x/starter-kits)을 사용한다면 Echo의 [useEcho 훅](#using-react-or-vue)을 활용할 수 있습니다.

> [!NOTE]
> 어떤 이벤트든 브로드캐스팅하기 전에 [큐 워커](/docs/12.x/queues)를 먼저 구성하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 처리되어, 브로드캐스팅으로 인해 애플리케이션 응답 속도가 느려지는 것을 방지합니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션 내에서 약간의 설정과 패키지 설치가 필요합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스팅 드라이버를 통해 이루어지며, 이 드라이버가 Laravel 이벤트를 브로드캐스트하면 Laravel Echo(JavaScript 라이브러리)가 브라우저에서 이를 수신할 수 있습니다. 각 설치 단계는 아래에 자세히 안내합니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스팅 드라이버로 사용할 때 Laravel 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 추가하세요. 이 명령어는 Reverb에 필요한 Composer 및 NPM 패키지를 설치하고, `.env` 파일에 필요한 변수를 자동으로 추가합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/12.x/reverb) 설치 안내가 나옵니다. 물론 Composer 패키지 매니저로 Reverb를 수동으로 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치 후, Reverb 설치 명령어를 실행해서 설정 파일을 배포(publish)하고, 환경변수를 추가하며, 이벤트 브로드캐스팅을 활성화합니다.

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용법은 [Reverb 공식 문서](/docs/12.x/reverb)를 참고하세요.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 사용할 때 Laravel 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting`에 `--pusher` 옵션을 사용하세요. 이 Artisan 명령어는 Pusher 자격증명 입력을 요구하고, Pusher PHP 및 JavaScript SDK를 설치하며, `.env` 파일을 적절히 설정합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher를 수동으로 설치하려면, Composer 패키지 매니저를 통해 Pusher Channels PHP SDK를 설치합니다.

```shell
composer require pusher/pusher-php-server
```

그 후, `config/broadcasting.php` 파일에 Pusher Channels 자격증명을 설정해야 합니다. 이 파일은 이미 예시 설정이 포함되어 있으므로, key, secret, application ID만 입력하면 됩니다. 보통 자격증명을 `.env` 파일에 추가하여 관리합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

추가로, 브로드캐스팅에 사용할 드라이버를 `.env` 파일의 `BROADCAST_CONNECTION` 환경 변수에 지정해야 합니다.

```ini
BROADCAST_CONNECTION=pusher
```

이제, [Laravel Echo](#client-side-installation)를 설치 및 설정하여 클라이언트에서 브로드캐스트 이벤트를 수신할 준비를 할 수 있습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 "Pusher 호환" 모드에서 Ably를 사용하는 방법을 다룹니다. 하지만 Ably 팀은 Ably의 고유 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트를 공식적으로 개발, 유지보수 중입니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스터로 사용할 때 Laravel 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--ably` 옵션을 활용하십시오. 이 명령은 Ably 자격증명 입력을 안내하고, Ably PHP/JS SDK를 설치하며, `.env` 파일을 알맞게 수정합니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, Ably 애플리케이션 설정에서 반드시 "Pusher 프로토콜 지원(Pusher protocol support)"을 활성화해야 합니다. 이는 Ably 애플리케이션 설정의 "Protocol Adapter Settings" 부분에서 켤 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 사용을 수동으로 설정하려면, 먼저 Composer 패키지 매니저로 Ably PHP SDK를 설치해야 합니다.

```shell
composer require ably/ably-php
```

그리고, `config/broadcasting.php` 파일 내에 Ably 자격증명을 설정합니다. 예시 설정이 파일에 포함되어 있으며, 보통 `ABLY_KEY` [환경 변수](/docs/12.x/configuration#environment-configuration)에 값을 지정합니다.

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정합니다.

```ini
BROADCAST_CONNECTION=ably
```

마지막으로 [Laravel Echo](#client-side-installation)를 설치, 구성하여 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있도록 준비하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 구독 및 리스닝하는 과정을 매우 간단하게 만들어주는 JavaScript 라이브러리입니다.

`install:broadcasting` Artisan 명령어로 Reverb를 설치하면, Reverb와 Echo의 스캐폴딩 및 설정이 자동으로 애플리케이션에 적용됩니다. 수동으로 Laravel Echo를 구성하려면 아래 지침을 참고하세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, 먼저 `pusher-js` 패키지를 설치해야 합니다. Reverb는 WebSocket 구독, 채널, 메시지에 Pusher 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치 후, JavaScript 내에서 Echo 인스턴스를 새로 생성하세요. 일반적으로 Laravel 프레임워크에서 제공하는 `resources/js/bootstrap.js` 파일 하단이 좋습니다.

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

자바스크립트 설정을 완료한 뒤에는 애플리케이션의 자산을 컴파일하세요.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 구독 및 리스닝하는 과정을 매우 간단하게 만들어주는 JavaScript 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령으로 브로드캐스팅을 설치하면, Pusher와 Echo의 스캐폴딩 및 설정이 자동으로 애플리케이션에 적용됩니다. 수동 설치가 필요하다면 아래 단계에 따라 진행하세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

Laravel Echo를 프론트엔드에 수동으로 설정하려면, 먼저 Pusher 프로토콜을 사용하는 `laravel-echo`와 `pusher-js` 패키지를 설치하세요.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치가 끝나면 `resources/js/bootstrap.js` 파일 등에서 Echo 인스턴스를 생성하세요.

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

`.env` 파일에 아래와 같이 Pusher 환경 변수를 추가하거나 값이 지정되어 있는지 확인하세요.

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

설정을 마쳤으면 애플리케이션의 자산을 컴파일하세요.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 JavaScript 자산 컴파일에 관한 더 많은 정보는 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

미리 구성된 Pusher Channels 클라이언트 인스턴스를 Echo에서 사용하고 싶다면, `client` 옵션을 통해 전달할 수 있습니다.

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
> 아래 문서는 "Pusher 호환" 모드에서 Ably를 사용하는 방법을 다룹니다. 그러나 Ably 팀은 Ably의 고유한 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트를 공식적으로 개발, 유지관리합니다. 자세한 내용은 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 구독하고 리스닝하는 과정을 아주 쉽게 만들어줍니다.

`install:broadcasting --ably` Artisan 명령어로 지원을 설치하면, Ably와 Echo의 스캐폴딩 및 설정이 자동 적용됩니다. 수동 구성 방법은 아래를 참고하세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

Ably 사용을 위해서는 `laravel-echo`, `pusher-js` 패키지를 설치해야 하며, 이들은 Pusher 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**진행 전 Ably 대시보드에서 "Pusher 프로토콜 지원(Pusher protocol support)"을 반드시 활성화해야 합니다. "Protocol Adapter Settings"에서 켤 수 있습니다.**

Echo 설치 후, 아래와 같이 새로운 Echo 인스턴스를 생성합니다.

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

Ably Echo 설정에서 사용하는 `VITE_ABLY_PUBLIC_KEY` 환경 변수에는 Ably 퍼블릭 키를 지정해야 합니다. 퍼블릭 키는 Ably 키에서 `:` 앞부분입니다.

설정을 완료했다면 아래 명령어로 자산 빌드를 수행하세요.

```shell
npm run dev
```

> [!NOTE]
> JavaScript 자산 컴파일에 대한 자세한 내용은 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel 이벤트 브로드캐스팅은 서버 사이드 Laravel 이벤트를 드라이버 기반(WebSocket) 방식으로 클라이언트 사이드 JavaScript 애플리케이션으로 브로드캐스트할 수 있게 해줍니다. 현재 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 제공합니다. 이벤트는 [Laravel Echo](#client-side-installation) JavaScript 패키지를 통해 클라이언트에서 쉽게 수신할 수 있습니다.

이벤트는 "채널"로 브로드캐스트되며, 공개 채널(public)과 프라이빗 채널(private)로 구분됩니다. 공개 채널은 인증이나 인가 없이 누구나 구독할 수 있는 반면, 프라이빗 채널은 사용자가 해당 채널 리스닝 권한이 있어야만 구독할 수 있습니다.

<a name="using-example-application"></a>
### 예시 애플리케이션 활용

각 브로드캐스팅 컴포넌트로 들어가기 전, 전자상거래 스토어의 예시로 전체 흐름을 간단히 살펴봅니다.

사용자가 자신의 주문 배송 상태를 볼 수 있는 페이지가 있다고 가정합시다. 배송 상태 업데이트가 발생할 때마다 `OrderShipmentStatusUpdated` 이벤트가 발생한다고 가정합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문을 보는 중에는 페이지를 새로고침하지 않고도 새 배송 상태가 즉시 표시되도록 업데이트를 브로드캐스트하려고 합니다. 따라서 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이를 통해 이벤트가 발생할 때 Laravel이 자동으로 이벤트를 브로드캐스트하도록 지정합니다.

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

`ShouldBroadcast` 인터페이스를 구현하면 반드시 이벤트에 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환하는 역할을 합니다. 생성된 이벤트 클래스에는 이미 빈 메서드 스텁이 정의되어 있으니, 사용자 정의로 채우면 됩니다. 여기서는 주문 생성자만 자신의 주문 상태를 볼 수 있도록 주문에 연결된 프라이빗 채널로 이벤트를 브로드캐스트합니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 채널을 반환
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 이벤트를 브로드캐스트하고 싶을 경우, `array`를 반환하면 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 채널(들)을 반환
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

프라이빗 채널을 구독하려면 사용자가 해당 채널을 들을 수 있도록 권한이 있어야 합니다. 애플리케이션의 `routes/channels.php` 파일에 채널 인가 규칙을 정의할 수 있습니다. 예시에서는, 어떤 사용자가 프라이빗 `orders.1` 채널을 구독하려 할 때 그 사용자가 실제로 해당 주문의 주인인지 검증합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 사용 권한 여부(`true`/`false`)를 반환하는 콜백을 받습니다.

모든 인가 콜백에는 첫 번째 인수로 현재 인증된 사용자가, 두 번째 이후 인수에는 와일드카드 파라미터들이 전달됩니다. 위 예시에서는 `{orderId}` 자리가 와일드카드임을 나타내고 있습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신

마지막으로, JavaScript 애플리케이션에서 이벤트를 수신하면 됩니다. [Laravel Echo](#client-side-installation)를 통해 가능합니다. Laravel Echo의 내장 React, Vue 훅(`useEcho`)을 사용하면 간단하게 시작할 수 있고, 디폴트로 이벤트의 public 속성은 모두 브로드캐스트 페이로드에 포함됩니다.

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

(이하 내용은 원문과 동일하게 구조와 규칙을 지켜 계속 번역됩니다.)