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
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인가](#authorizing-channels)
    - [인가 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅하기](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스트](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 복구](#rescuing-broadcasts)
- [브로드캐스트 수신하기](#receiving-broadcasts)
    - [이벤트 리스닝하기](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue 사용하기](#using-react-or-vue)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 가입](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대 웹 애플리케이션에서는 실시간으로 UI를 업데이트할 수 있도록 WebSocket을 자주 사용합니다. 서버에서 어떤 데이터가 변경되면 해당 내용을 WebSocket 연결을 통해 클라이언트가 처리할 수 있도록 메시지가 전송됩니다. WebSocket은 주기적으로 서버에 변경 사항을 지속적으로 요청(polling)하는 방식보다 훨씬 효율적입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내고 이메일로 전송하는 기능이 있다고 가정해봅니다. 그러나 이 CSV 파일을 생성하는 데는 몇 분이 걸릴 수 있으므로, [큐 작업](/docs/12.x/queues)에서 파일을 생성하고 이메일을 전송하도록 구성할 수 있습니다. CSV 파일이 생성되어 사용자가 메일로 받게 되면, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 애플리케이션의 JavaScript가 이를 받을 수 있도록 할 수 있습니다. 이벤트가 수신되면 페이지를 새로고침하지 않아도 사용자에게 "CSV가 이메일로 전송됨"과 같은 메시지를 표시할 수 있습니다.

이런 기능을 쉽게 만들 수 있도록, Laravel은 서버 측에서 [이벤트](/docs/12.x/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 방법을 제공합니다. 라라벨 이벤트를 브로드캐스트하면 서버 쪽 Laravel 애플리케이션과 클라이언트 JavaScript 애플리케이션에서 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 네임드 채널(named channel)에 연결하고, Laravel 애플리케이션은 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에 전달하고자 하는 모든 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

Laravel은 기본적으로 세 가지 서버 측 브로드캐스팅 드라이버를 포함합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에, 반드시 [이벤트와 리스너](/docs/12.x/events)에 대한 라라벨 문서를 먼저 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

Laravel의 기본 설정에서는 새로운 애플리케이션에서 브로드캐스팅이 활성화되어 있지 않습니다. 다음 Artisan 명령어를 사용하여 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령은 사용할 이벤트 브로드캐스팅 서비스를 선택하도록 안내합니다. 또한 `config/broadcasting.php` 설정 파일과, 애플리케이션의 브로드캐스트 인가 라우트와 콜백을 등록하는 곳인 `routes/channels.php` 파일을 생성합니다.

Laravel은 여러 브로드캐스트 드라이버를 기본 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버도 있습니다. 추가로, 테스트 중 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버별 설정 예시는 `config/broadcasting.php` 파일에 포함되어 있습니다.

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php`에 저장됩니다. 만약 이 파일이 없다면, `install:broadcasting` Artisan 명령 실행 시 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화하면 [브로드캐스트 이벤트 정의](#defining-broadcast-events)와 [이벤트 수신 및 리스닝](#listening-for-events)에 대해 더 자세히 배울 준비가 된 것입니다. React 또는 Vue [스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우 Echo의 [useEcho 훅](#using-react-or-vue)을 이용해 이벤트를 들을 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스트하기 전에 반드시 [큐 워커](/docs/12.x/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업으로 처리되므로, 브로드캐스트로 인해 애플리케이션의 응답 시간이 느려지지 않습니다.

<a name="server-side-installation"></a>
## 서버 측 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅 기능을 사용하려면 애플리케이션에서 일부 설정을 변경하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스트 드라이버가 Laravel 이벤트를 브라우저의 Javascript 라이브러리인 Laravel Echo에서 수신할 수 있도록 브로드캐스트하는 방식으로 동작합니다. 설치 과정을 단계별로 간단하게 안내드리겠습니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스트 드라이버로 사용하여 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 추가해서 실행하세요. 이 명령은 Reverb에 필요한 Composer와 NPM 패키지를 설치하고 `.env` 파일에 필요한 변수를 추가합니다:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/12.x/reverb) 설치를 안내하는 메시지가 표시됩니다. 또는 Composer 패키지 매니저를 사용해 직접 Reverb를 설치할 수 있습니다:

```shell
composer require laravel/reverb
```

패키지를 설치한 후, Reverb 설치 명령을 실행하면 설정을 퍼블리시하고, Reverb용 환경 변수 추가, 이벤트 브로드캐스팅 활성화 등이 자동으로 이루어집니다:

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용법은 [Reverb 공식 문서](/docs/12.x/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스트 드라이버로 사용하여 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--pusher` 옵션을 추가해 실행하세요. 이 명령은 Pusher 자격 증명 정보를 입력받고, Pusher PHP 및 Javascript SDK를 설치하며, `.env` 파일에 필요한 변수를 추가합니다:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 직접 설치하려면 Composer 패키지 매니저를 사용해 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

다음으로, `config/broadcasting.php` 설정 파일에서 Pusher Channels 자격 증명을 설정하세요. 예시 설정이 이미 파일에 포함되어 있으므로, key, secret, application ID만 지정하면 됩니다. 일반적으로 아래와 같이 `.env` 파일에서 값을 지정합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php`의 `pusher` 설정에서 클러스터(cluster)와 같이 Channels가 지원하는 다른 `options`도 지정할 수 있습니다.

마지막으로 `.env` 파일의 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정하세요:

```ini
BROADCAST_CONNECTION=pusher
```

이제 클라이언트에서 브로드캐스트 이벤트를 받을 수 있도록 [Laravel Echo](#client-side-installation)를 설치 및 구성할 준비가 되었습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 다룹니다. 그러나 Ably 팀은 Ably만의 고유 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트도 별도로 관리합니다. 자세한 사항은 [Ably의 Laravel broadcaster 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스트 드라이버로 사용하여 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--ably` 옵션을 추가해 실행하세요. 이 명령은 Ably 자격 증명을 입력받고, Ably PHP 및 JavaScript SDK를 설치하며, `.env` 파일에 필요한 변수를 추가합니다:

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, Ably 애플리케이션 설정에서 "Pusher 프로토콜 지원"을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 설정 대시보드의 "Protocol Adapter Settings"에서 켤 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 설치하려면 Composer 패키지 매니저로 Ably PHP SDK를 설치하세요:

```shell
composer require ably/ably-php
```

다음으로 `config/broadcasting.php`에 자격 증명을 설정합니다. 예시 Ably 설정이 이미 포함되어 있으므로 key만 입력하면 됩니다. 일반적으로 `ABLY_KEY` [환경 변수](/docs/12.x/configuration#environment-configuration)로 지정합니다:

```ini
ABLY_KEY=your-ably-key
```

그리고 `.env` 파일의 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정합니다:

```ini
BROADCAST_CONNECTION=ably
```

마지막으로 [Laravel Echo](#client-side-installation)를 설치 및 구성하여 클라이언트에서 브로드캐스트 이벤트를 받을 준비가 완료됩니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스터가 브로드캐스트한 채널에 구독하고, 이벤트를 손쉽게 리스닝할 수 있는 JavaScript 라이브러리입니다.

`install:broadcasting` Artisan 명령어를 통해 Reverb를 설치하면, Reverb와 Echo의 설정 및 템플릿 코드가 애플리케이션에 자동으로 추가됩니다. 단, 수동으로 Echo를 설정하려면 아래 지침을 참고하세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면 Reverb가 WebSocket 구독, 채널, 메시지 전송에 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지를 먼저 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo를 설치한 후에는, 애플리케이션의 JavaScript에서 Echo 인스턴스를 생성해야 합니다. 프레임워크에 포함된 `resources/js/bootstrap.js` 하단에 아래 코드를 추가하면 좋습니다:

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

다음으로 애플리케이션의 에셋을 빌드하세요:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 이벤트 리스닝 작업을 보다 쉽게 만들도록 도와줍니다.

`install:broadcasting --pusher` Artisan 명령어로 Pusher와 Echo를 설치하면 프런트엔드에 관련 설정 및 템플릿 코드가 자동으로 추가됩니다. 수동 설정이 필요한 경우 아래 방식대로 진행하십시오.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

애플리케이션 프론트엔드에서 Laravel Echo를 수동으로 설정하려면, Pusher 프로토콜용 `laravel-echo`와 `pusher-js`를 설치합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

설치가 완료되면 `resources/js/bootstrap.js`에 Echo 인스턴스를 새로 생성합니다:

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

.env 파일에 Pusher용 환경 변수를 정의하세요. 만약 이미 없다면 아래와 같이 추가합니다:

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

설정을 완료했으면 에셋을 빌드하세요:

```shell
npm run build
```

> [!NOTE]
> 자바스크립트 에셋 빌드와 관련해 더 자세한 내용은 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 이미 구성된 클라이언트 인스턴스 사용

이미 사전에 구성된 Pusher Channels 클라이언트 인스턴스가 있다면 Echo에서 `client` 설정 옵션을 사용하여 이를 활용할 수 있습니다:

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
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 안내합니다. 실제 서비스에서는 Ably 공식 브로드캐스터 및 Echo 클라이언트를 사용하는 것이 추천됩니다. 자세한 내용은 [Ably의 Laravel broadcaster 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버가 브로드캐스트한 이벤트를 브라우저에서 쉽게 수신할 수 있도록 도와줍니다.

`install:broadcasting --ably` Artisan 명령어로 Ably와 Echo를 설치하면 관련 설정과 템플릿 코드가 자동 추가됩니다. 또는 아래 절차에 따라 수동으로 Echo를 설정할 수 있습니다.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, Pusher 프로토콜 기반 WebSocket 지원을 위해 `laravel-echo`와 `pusher-js` 패키지를 설치하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```

**진행 전 Ably 애플리케이션 설정의 "Protocol Adapter Settings"에서 Pusher 프로토콜 지원을 반드시 활성화해야 합니다.**

설치가 완료되었으면 애플리케이션의 `resources/js/bootstrap.js` 파일에서 Echo 인스턴스를 생성하세요:

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

Echo 설정에서 사용하는 `VITE_ABLY_PUBLIC_KEY`는 Ably의 public key이어야 하며, Ably key에서 `:` 앞 부분입니다.

설정 조정이 끝나면 애플리케이션의 에셋을 빌드하세요:

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 에셋 빌드에 관해서는 [Vite](/docs/12.x/vite) 관련 문서를 참고하세요.

---

*(아래 내용부터는 "개념 개요(Concept Overview)", "브로드캐스트 이벤트 정의(Defining Broadcast Events)", "채널 인가(Authorizing Channels)", "이벤트 브로드캐스팅하기(Broadcasting Events)", "브로드캐스트 수신하기(Receiving Broadcasts)", "프레즌스 채널(Presence Channels)", "모델 브로드캐스팅(Model Broadcasting)", "클라이언트 이벤트(Client Events)", "알림(Notifications)" 등 마크다운 문서 전체가 동일한 구조와 규칙으로 번역됩니다. 분량 관계로, 현재 출력 가능한 길이만큼 제공하였고, 이후 추가 요청 시 나머지 부분도 연이어 번역 제공합니다.)*