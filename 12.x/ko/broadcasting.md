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
    - [예제 애플리케이션을 활용한 설명](#using-example-application)
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
    - [Others만 브로드캐스트](#only-to-others)
    - [커넥션 커스터마이즈](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 예외 처리](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스 활용](#namespaces)
    - [React 혹은 Vue로 사용하기](#using-react-or-vue)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notification)](#notifications)

<a name="introduction"></a>
## 소개

현대적인 웹 애플리케이션에서는 WebSocket을 활용해 실시간으로 사용자 인터페이스(UI)를 동적으로 업데이트하는 기능이 많이 사용되고 있습니다. 서버에서 데이터가 변경되면, 주로 WebSocket 연결을 통해 메시지가 클라이언트로 전송되고, 클라이언트는 이 메시지를 받아 UI를 갱신합니다. WebSocket을 활용하면 데이터 변경 사항을 감지하기 위해 계속 서버를 폴링하는 방식보다 훨씬 효율적으로 정보를 전달할 수 있습니다.

예를 들어, 여러분의 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내어 이메일로 전송하는 기능을 제공한다고 가정해 봅시다. 이 CSV 파일을 생성하는 데 시간이 몇 분 정도 소요된다면, [큐 작업(queued job)](/docs/12.x/queues)에서 이를 처리하고 사용자가 파일을 이메일로 받게 할 수도 있습니다. CSV 생성 및 발송이 완료되는 시점에 `App\Events\UserDataExported` 이벤트를 브로드캐스팅하면, 애플리케이션의 자바스크립트가 이 이벤트를 받아서 사용자의 화면에 "CSV가 이메일로 전송되었습니다"라는 메시지를 보여줄 수 있습니다. 이 과정에서 사용자는 페이지를 새로고침할 필요가 없습니다.

이처럼 실시간 기능을 손쉽게 구축할 수 있도록, 라라벨에서는 서버 사이드의 [이벤트](/docs/12.x/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 기능을 지원합니다. 라라벨의 이벤트 브로드캐스팅을 이용하면 여러분의 서버 사이드 라라벨 애플리케이션과 클라이언트 사이드 자바스크립트 애플리케이션이 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 매우 단순합니다: 클라이언트는 프론트엔드에서 특정 이름의 채널에 연결하고, 라라벨 애플리케이션은 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 이러한 이벤트에는 프론트엔드에서 활용할 수 있는 추가 데이터도 포함시킬 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

라라벨은 기본적으로 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), 그리고 [Ably](https://ably.com)입니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 [이벤트와 리스너](/docs/12.x/events) 관련 라라벨 공식 문서를 먼저 읽어주시는 것이 좋습니다.

<a name="quickstart"></a>
## 빠른 시작

기본적으로, 라라벨의 새로운 프로젝트에서는 브로드캐스팅이 비활성화되어 있습니다. `install:broadcasting` 아티즌 명령어를 실행하면 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어를 실행하면, 어떤 이벤트 브로드캐스팅 서비스를 사용할지 선택하라는 안내가 나오며, 동시에 `config/broadcasting.php` 설정 파일과 여러분의 애플리케이션 브로드캐스트 인가(authorization) 라우트와 콜백을 등록하는 `routes/channels.php` 파일도 생성됩니다.

라라벨은 몇 가지 브로드캐스트 드라이버를 기본적으로 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한 테스트 중에 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버별 설정 예시는 `config/broadcasting.php` 파일에 들어 있습니다.

여러분의 애플리케이션에서 사용하는 브로드캐스트 관련 모든 설정은 `config/broadcasting.php` 파일에 저장됩니다. 만약 이 파일이 아직 없다면 걱정하지 마세요. `install:broadcasting` 아티즌 명령어 실행 시 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅이 활성화되었다면, [브로드캐스트 이벤트 정의](#defining-broadcast-events)와 [이벤트 수신(리스닝)](#listening-for-events)에 대해 계속 학습할 준비가 된 것입니다. 만약 라라벨에서 제공하는 React 또는 Vue [스타터 킷](/docs/12.x/starter-kits)을 사용 중이라면, Echo의 [useEcho hook](#using-react-or-vue)을 통해 이벤트를 받을 수 있습니다.

> [!NOTE]
> 어떤 이벤트라도 브로드캐스트 하기에 앞서 [큐 워커](/docs/12.x/queues)를 반드시 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅 작업은 큐잉된 작업(queued jobs)을 통해 처리되므로, 브로드캐스트로 인해 애플리케이션의 응답 속도가 저하되는 것을 막을 수 있습니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치

라라벨의 이벤트 브로드캐스팅을 사용하기 위해서는 라라벨 애플리케이션 내부 설정을 일부 변경하고, 필요한 패키지를 추가로 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스팅 드라이버가 라라벨 이벤트를 브라우저 클라이언트의 Laravel Echo(자바스크립트 라이브러리)에서 수신할 수 있도록 브로드캐스트함으로써 동작합니다. 걱정하지 마세요! 설치 과정을 하나씩 차근차근 안내드릴 예정입니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스팅 드라이버로 이용하여 라라벨의 브로드캐스팅 기능을 신속하게 활성화하려면, `install:broadcasting` 아티즌 명령어에 `--reverb` 옵션을 추가해 실행하십시오. 이 명령어는 Reverb가 요구하는 Composer 및 NPM 패키지를 설치하고, 필요한 환경변수들도 `.env` 파일에 자동으로 추가합니다:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령어를 실행할 때 [Laravel Reverb](/docs/12.x/reverb) 설치 여부를 묻는 안내가 표시됩니다. 직접 Reverb를 설치하고 싶다면 Composer 패키지 매니저로 아래와 같이 설치할 수 있습니다:

```shell
composer require laravel/reverb
```

패키지 설치 후, Reverb의 설치 명령어를 실행하면 설정 파일을 배포(publish)하고, 필요한 환경변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅이 활성화됩니다:

```shell
php artisan reverb:install
```

Reverb의 상세한 설치 및 사용 방법은 [Reverb 공식 문서](/docs/12.x/reverb)에서 확인하시기 바랍니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스팅 드라이버로 이용하여 라라벨 브로드캐스팅을 신속하게 활성화하려면, `install:broadcasting` 아티즌 명령어에 `--pusher` 옵션을 추가해 실행하세요. 이 명령어는 Pusher 인증 정보를 입력받고, Pusher PHP 및 JavaScript SDK를 설치하며, 주요 환경 변수들도 `.env` 파일에 반영합니다:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 직접 추가하려면, 우선 Composer 패키지 매니저로 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```

그다음, `config/broadcasting.php` 설정 파일의 Pusher Channels 항목에 인증 정보를 입력합니다. 이 파일에는 이미 기본 Pusher Channels 설정 예제가 들어 있으므로, key, secret, application ID 값만 여러분의 것으로 지정하시면 됩니다. 일반적으로는 인증 정보를 애플리케이션의 `.env` 파일에 설정합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에서는, cluster 등 Channels에서 지원하는 추가 옵션들도 지정할 수 있습니다.

그리고, 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 지정하세요:

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo](#client-side-installation)를 설치하고 설정하면 클라이언트에서 브로드캐스트 이벤트를 수신할 수 있게 됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래의 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법을 안내합니다. 하지만 Ably 팀에서는 Ably의 기능을 최대한 활용할 수 있도록 직접 유지보수하는 브로드캐스터 및 Echo 클라이언트도 제공하고 있습니다. Ably 공식 드라이버를 활용하는 방법은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스팅 드라이버로 사용하여 라라벨의 브로드캐스팅 기능을 활성화하려면, 아래와 같이 `install:broadcasting` 아티즌 명령어에 `--ably` 옵션을 추가해 실행합니다. 이 명령어는 Ably 인증 정보를 입력받고, Ably PHP 및 JavaScript SDK를 설치하며, 필요한 환경 변수를 `.env` 파일에 추가합니다:

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, 반드시 Ably 애플리케이션 설정에서 "Pusher 프로토콜 지원"을 활성화해야 합니다. 이 기능은 애플리케이션의 설정 대시보드 내 "Protocol Adapter Settings"에서 켤 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 추가하려면 Composer 패키지 매니저로 Ably PHP SDK를 설치해야 합니다:

```shell
composer require ably/ably-php
```

그다음, `config/broadcasting.php` 설정 파일에 Ably 인증 정보를 입력합니다. 이 파일에는 이미 Ably 예제 설정이 들어 있으므로 key만 지정하시면 됩니다. 일반적으로, 이 값은 `ABLY_KEY` [환경 변수](/docs/12.x/configuration#environment-configuration)에 저장합니다:

```ini
ABLY_KEY=your-ably-key
```

그리고 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정하세요:

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo](#client-side-installation)를 설치하고 설정하면 클라이언트 측에서 브로드캐스트 이벤트를 수신할 준비가 완료됩니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 자바스크립트 라이브러리로, 서버 사이드 브로드캐스팅 드라이버에서 브로드캐스트한 이벤트를 쉽게 구독하고 수신할 수 있도록 도와줍니다.

`install:broadcasting` 아티즌 명령어로 Laravel Reverb를 설치하면, Reverb와 Echo 관련 스캐폴딩 및 설정이 애플리케이션에 자동으로 포함됩니다. 하지만, 직접 Laravel Echo를 설정하고 싶다면 아래의 설명을 따라 수동으로 구성할 수 있습니다.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, 먼저 Reverb가 WebSocket 구독/채널/메시지에 Pusher 프로토콜을 사용하므로 `pusher-js` 패키지를 함께 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 완료되면, 애플리케이션의 자바스크립트에서 새로운 Echo 인스턴스를 생성합니다. 이 예시는 라라벨 프레임워크에서 제공하는 `resources/js/bootstrap.js` 파일 하단에 추가하는 것이 좋은 위치입니다:

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

이제 애플리케이션 에셋을 컴파일해 줍니다:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터 기능을 사용하려면 laravel-echo 버전 v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 자바스크립트 라이브러리로, 서버 사이드 브로드캐스팅 드라이버에서 브로드캐스트한 이벤트를 쉽게 구독하고 수신할 수 있도록 도와줍니다.

`install:broadcasting --pusher` 아티즌 명령어로 브로드캐스팅 지원을 설치하면, Pusher와 Echo 관련 스캐폴딩 및 설정이 자동으로 애플리케이션에 추가됩니다. 하지만 직접 Laravel Echo를 설정하고 싶다면 아래 과정을 따라 수동으로 구성할 수 있습니다.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

프런트엔드에서 Laravel Echo를 직접 설정하려면, WebSocket 구독/채널/메시지에 Pusher 프로토콜을 활용하는 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 완료되면, 애플리케이션의 `resources/js/bootstrap.js` 파일에서 새로운 Echo 인스턴스를 생성하세요:

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

다음 단계로, `.env` 파일에서 Pusher 관련 환경 변수 값을 정의해야 합니다. 파일에 해당 값이 없다면 아래와 같이 추가하세요:

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

Echo 설정을 애플리케이션 요구에 맞게 조정한 후에는, 다음 명령어로 에셋을 빌드하면 됩니다:

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 자바스크립트 에셋 빌드에 대한 자세한 내용은 [Vite 공식 문서](/docs/12.x/vite)를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 활용

이미 미리 설정된 Pusher Channels 클라이언트 인스턴스가 있고 이것을 Echo에서 그대로 활용하고 싶다면, Echo 설정의 `client` 옵션을 통해 전달할 수 있습니다:

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
> 아래의 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법을 안내합니다. 하지만 Ably 팀에서는 Ably의 기능을 최대한 활용할 수 있도록 직접 유지보수하는 브로드캐스터 및 Echo 클라이언트도 제공하고 있습니다. 공식 드라이버 사용법은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 자바스크립트 라이브러리로, 서버 사이드 브로드캐스팅 드라이버에서 브로드캐스트한 이벤트를 쉽게 구독하고 수신할 수 있게 해줍니다.

`install:broadcasting --ably` 아티즌 명령어로 브로드캐스팅 지원을 설치하면, Ably와 Echo 관련 스캐폴딩 및 설정이 자동으로 포함됩니다. 직접 Laravel Echo를 설정하려면, 아래의 과정을 따라 수동으로 구성할 수 있습니다.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 직접 설정하려면, WebSocket 구독/채널/메시지에 Pusher 프로토콜을 사용하는 `laravel-echo`와 `pusher-js` 패키지를 먼저 설치해야 합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속 진행하기 전 반드시 Ably 애플리케이션 설정에서 "Pusher 프로토콜 지원"을 활성화해야 합니다. 이 기능은 애플리케이션의 설정 대시보드 내 "Protocol Adapter Settings"에서 켤 수 있습니다.**

Echo 설치가 완료되면, 애플리케이션의 `resources/js/bootstrap.js` 파일에서 새 Echo 인스턴스를 생성하세요:

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

여기서 Echo 설정에 언급된 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 여러분의 Ably 공개키(public key)값이어야 합니다. 공개키는 Ably 키의 `:` 문자 앞부분입니다.

Echo의 설정을 요구 사항에 맞게 조정했다면, 아래 명령어로 애플리케이션의 에셋을 빌드하세요:

```shell
npm run dev
```

> [!NOTE]
> 애플리케이션의 자바스크립트 에셋 빌드에 대한 자세한 내용은 [Vite 공식 문서](/docs/12.x/vite)를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

라라벨의 이벤트 브로드캐스팅은 서버 사이드의 라라벨 이벤트를 클라이언트 사이드 자바스크립트 애플리케이션으로 WebSocket(드라이버 기반) 방식으로 내보낼 수 있게 해줍니다. 현재 라라벨은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 지원합니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지를 이용해 이벤트를 수신할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트되며, 이 채널은 공개(public) 또는 비공개(private)로 지정할 수 있습니다. 애플리케이션 방문자는 인증 또는 인가 없이 공개 채널에 자유롭게 구독할 수 있지만, 비공개 채널을 구독하려면 반드시 인증 및 인가 절차를 통과해야 합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션을 활용한 설명

이벤트 브로드캐스팅의 각 컴포넌트에 대해 본격적으로 살펴보기 전에, 실제 전자상거래 스토어(쇼핑몰) 예시로 전체 흐름을 먼저 간단히 살펴보겠습니다.

우리 애플리케이션에는 주문의 배송 상태를 확인할 수 있는 페이지가 있다고 가정해 보겠습니다. 애플리케이션에서 주문의 배송 상태가 업데이트되면 `OrderShipmentStatusUpdated` 이벤트가 발생하게 됩니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 자신의 주문 상태를 보고 있을 때, 페이지를 새로고침하지 않고도 상태 업데이트 내용을 받아보기를 원할 것입니다. 이를 위해 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이렇게 하면 이벤트가 발생할 때 라라벨이 해당 이벤트를 자동으로 브로드캐스트하게 됩니다.

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

`ShouldBroadcast` 인터페이스를 구현한 이벤트 클래스는 반드시 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널을 반환하는 역할을 합니다. 자동 생성되는 이벤트 클래스에는 이미 이 메서드의 골격이 포함되어 있으니, 여러분은 세부 동작만 구현하시면 됩니다. 예를 들어, 주문 생성자(주문자)만 상태 업데이트를 확인할 수 있도록 주문에 연결된 비공개(private) 채널에서 브로드캐스트하도록 구현합니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 채널 반환
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

여러 채널에 이벤트를 동시에 브로드캐스트하고 싶다면, 배열(`array`)로 반환하면 됩니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 여러 채널 반환
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
#### 채널 인가(Authorization)

비공개 채널을 이용하려면 사용자는 반드시 해당 채널에 대해 인가되어야 합니다. 애플리케이션의 `routes/channels.php` 파일에 채널 인가 규칙을 정의할 수 있습니다. 아래와 같이 비공개 채널 `orders.1`에 접근하려는 사용자가 해당 주문의 생성자인지 여부를 확인하도록 구현할 수 있습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인수, 즉 채널 이름과 인가 판정을 반환하는 콜백을 받습니다. 콜백에서 `true`를 반환하면 사용자가 해당 채널을 구독할 수 있고, `false`면 거부됩니다.

모든 인가 콜백에는 현재 인증된 사용자가 첫 번째 인수로 전달되며, 추가 와일드카드 인자는 그 이후에 순서대로 전달됩니다. 위 예제에서는 채널 이름에 `{orderId}` 플레이스홀더를 사용하여, 채널 이름 중 "ID" 부분이 와일드카드임을 명시하고 있습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신

이제 마지막으로 JavaScript 애플리케이션에서 해당 이벤트를 수신하기만 하면 됩니다. 이 작업은 [Laravel Echo](#client-side-installation)를 이용해 쉽게 할 수 있습니다. Echo에서 제공하는 React, Vue 전용 훅을 사용하면 간단하게 시작할 수 있으며, 기본적으로 모든 public 속성이 브로드캐스트 이벤트에 포함됩니다:

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

## 브로드캐스트 이벤트 정의하기

특정 이벤트가 브로드캐스트되어야 함을 라라벨에 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 이미 import되어 있으므로, 필요한 이벤트에 손쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 한 가지 메서드, 즉 `broadcastOn` 메서드만 구현하도록 요구합니다. `broadcastOn` 메서드는 이벤트를 브로드캐스트할 채널 또는 채널 배열을 반환해야 합니다. 이 채널들은 `Channel`, `PrivateChannel`, `PresenceChannel`의 인스턴스여야 합니다. `Channel` 클래스의 인스턴스는 모든 사용자가 구독할 수 있는 공개 채널을 의미하며, `PrivateChannel`과 `PresenceChannel`은 [채널 인가](#authorizing-channels)가 필요한 비공개 채널을 나타냅니다.

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

`ShouldBroadcast` 인터페이스를 구현한 후에는, [이벤트를 발생시키는 것](/docs/12.x/events) 이외에 별다른 작업이 필요하지 않습니다. 이벤트를 발생시키면, [큐에 등록된 작업](/docs/12.x/queues)이 자동으로 지정한 브로드캐스트 드라이버를 이용해 이벤트를 브로드캐스트합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 라라벨은 이벤트의 클래스명을 사용해 이벤트를 브로드캐스트합니다. 하지만, 필요하다면 이벤트 클래스에 `broadcastAs` 메서드를 정의하여 브로드캐스트할 이름을 직접 지정할 수 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs` 메서드를 사용해 브로드캐스트 이름을 지정했다면, 반드시 앞에 점(`.`)을 붙여서 리스너를 등록해야 합니다. 이렇게 하면 Echo가 애플리케이션 네임스페이스를 이벤트 이름 앞에 자동으로 붙이지 않게 됩니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 해당 이벤트의 모든 `public` 속성은 자동으로 직렬화되어 이벤트의 페이로드(payload)로 전송됩니다. 따라서 자바스크립트 애플리케이션에서 공개 속성의 데이터를 그대로 사용할 수 있습니다. 예를 들어, 이벤트에 Eloquent 모델을 담은 `$user`라는 public 속성만 있다면, 브로드캐스트 페이로드는 아래와 같이 전송됩니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

좀 더 세밀하게 브로드캐스트 페이로드 데이터를 제어하고 싶다면, 이벤트 클래스에 `broadcastWith` 메서드를 추가하면 됩니다. 이 메서드는 브로드캐스트시 전송될 데이터를 배열로 반환해야 합니다.

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
### 브로드캐스트 큐 지정

기본적으로 각각의 브로드캐스트 이벤트는 `queue.php` 설정 파일에 지정된 기본 큐 커넥션의 기본 큐에 등록됩니다. 이벤트 클래스에 `connection` 및 `queue` 속성을 정의하면 브로드캐스터가 사용하는 큐 커넥션과 큐 이름을 원하는 대로 지정할 수 있습니다.

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

큐 이름만 간단히 변경하고 싶은 경우, 이벤트 클래스에 `broadcastQueue` 메서드를 추가할 수도 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

기본 큐 드라이버 대신 `sync` 큐를 사용하여 이벤트를 브로드캐스트하고 싶으면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다.

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

특정 조건이 만족될 때만 이벤트를 브로드캐스트하고 싶을 수도 있습니다. 이럴 때는 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 조건을 반환하면 됩니다.

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
#### 브로드캐스트와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 브로드캐스트 이벤트를 디스패치하면, 큐에서 이벤트를 처리할 때 데이터베이스 트랜잭션이 아직 완료되지 않았을 수 있습니다. 이 경우 트랜잭션 중에 변경한 모델이나 데이터베이스 레코드가 데이터베이스에 반영되지 않아 문제가 발생할 수 있습니다. 트랜잭션 내부에서 생성한 모델이나 레코드 역시 데이터베이스에 존재하지 않을 수 있습니다. 이런 상황에서 해당 모델에 의존하는 이벤트라면, 이벤트를 브로드캐스트하는 작업에서 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정 값이 `false`라면, 특정 브로드캐스트 이벤트만 트랜잭션 모두 커밋 후에 디스패치되도록 하려면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

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
> 이러한 문제의 해결 방법에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하시기 바랍니다.

<a name="authorizing-channels"></a>
## 채널 인가(Authorization) 처리

비공개 채널(Private Channel)을 사용하려면, 현재 인증된 사용자가 해당 채널을 실제로 수신할 수 있는지 인가 과정을 거쳐야 합니다. 이 작업은 채널 이름을 포함해 라라벨 애플리케이션에 HTTP 요청을 보내고, 애플리케이션이 사용자의 채널 접근 권한을 스스로 판단하는 방식으로 이루어집니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 비공개 채널 구독을 위한 이 HTTP 요청은 자동으로 처리됩니다.

브로드캐스팅이 활성화되면, 라라벨은 인증 요청 처리를 위한 `/broadcasting/auth` 라우트를 자동으로 등록합니다. `/broadcasting/auth` 라우트는 `web` 미들웨어 그룹에 포함되어 동작합니다.

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의하기

다음으로, 현재 인증된 사용자가 특정 채널에 접속할 수 있는지 여부를 판단하는 인가 로직을 정의해야 합니다. 이는 `install:broadcasting` Artisan 명령어 실행 시 생성된 `routes/channels.php` 파일에서 진행합니다. 해당 파일에서 `Broadcast::channel` 메서드를 이용해 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과 채널 접근 가능 여부를 `true` 또는 `false`로 반환하는 콜백을 두 개의 인수로 받습니다.

모든 인가 콜백은 첫 번째 인수로 현재 인증된 사용자 객체를, 그 이후 순서로는 와일드카드 파라미터를 전달받게 됩니다. 위 예시에서는 `orders.{orderId}`에서처럼 `{orderId}` 플레이스홀더를 사용해 채널 이름의 일부(예: ID)가 와일드카드임을 나타냅니다.

애플리케이션에 등록된 브로드캐스트 인가 콜백 목록은 `channel:list` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백의 모델 바인딩

HTTP 라우트와 마찬가지로, 채널 라우트 역시 암묵적 또는 명시적 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어, 단순히 문자열이나 숫자 ID 대신 실제 `Order` 모델 인스턴스를 요청할 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 [암묵적 모델 바인딩 범위 지정](/docs/12.x/routing#implicit-model-binding-scoping)을 자동으로 지원하지 않습니다. 하지만 보통 대부분의 채널은 단일 모델의 고유(프라이머리) 키로만 범위를 지정하면 되므로 실제로 문제가 되는 경우는 드뭅니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백의 인증 처리

비공개 채널(Private Channel)과 존재 채널(Presence Channel)은 애플리케이션의 기본 인증 가드(guard)를 통해 사용자 인증을 수행합니다. 사용자가 인증되지 않은 경우, 채널 인가는 자동으로 거부되고 인가 콜백이 실행되지 않습니다. 필요하다면, 요청이 여러 커스텀 가드를 통해 인증되도록 `guards` 옵션을 지정할 수 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션에서 사용하는 채널이 많아지면, `routes/channels.php` 파일이 복잡해질 수 있습니다. 이럴 때는 클로저 대신 채널 클래스를 활용할 수 있습니다. 채널 클래스는 `make:channel` Artisan 명령어로 생성할 수 있으며, 생성된 파일은 `App/Broadcasting` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:channel OrderChannel
```

그다음, `routes/channels.php` 파일에서 해당 채널을 등록합니다.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

최종적으로, 채널 클래스의 `join` 메서드에 채널 인가 로직을 구현하면 됩니다. 이 `join` 메서드는 기존에 클로저로 작성했던 인가 처리를 담당하며, 모델 바인딩도 그대로 활용할 수 있습니다.

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
> 라라벨의 다른 클래스들과 마찬가지로, 채널 클래스 역시 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 resolve됩니다. 즉, 채널 클래스의 생성자에 필요한 의존성을 타입 힌트로 지정하면 자동으로 주입됩니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스로 표시한 후에는, 해당 이벤트의 디스패치 메서드를 이용해 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처(dispatcher)는 이벤트가 `ShouldBroadcast` 인터페이스를 구현했음을 감지해, 브로드캐스트를 위한 큐에 이벤트를 자동 등록합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 현재 사용자 제외 브로드캐스트

이벤트 브로드캐스팅을 사용하는 애플리케이션을 개발하다 보면, 때로는 현재 사용자를 제외한 모든 구독자에게만 이벤트를 브로드캐스트해야 할 때가 있습니다. 이때는 `broadcast` 헬퍼와 `toOthers` 메서드를 함께 사용하면 됩니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

`toOthers` 메서드를 언제 써야 할지 이해하기 쉽도록, 할 일 목록 예시를 들어보겠습니다. 어떤 사용자가 작업(task) 이름을 입력해 새 할 일을 생성한다고 해 봅시다. 이때 애플리케이션은 `/task` URL로 요청을 보내 작업 생성 이벤트를 브로드캐스트하고, 새 작업의 JSON 데이터를 응답으로 돌려받습니다. 자바스크립트 애플리케이션은 이 응답을 받아 할 일 목록에 바로 추가할 수 있습니다.

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만, 작업의 생성 이벤트 역시 브로드캐스트되었다는 점을 유의해야 합니다. 만약 자바스크립트 애플리케이션이 이 이벤트를 수신해 할 일을 리스트에 추가한다면, 엔드포인트 응답과 브로드캐스트 이벤트 양쪽에서 할 일이 중복 추가되는 문제가 생깁니다. 이 문제는 `toOthers` 메서드를 사용해 현재 사용자에겐 이벤트를 브로드캐스트하지 않도록 하면 쉽게 해결할 수 있습니다.

> [!WARNING]
> `toOthers` 메서드를 호출하려면 이벤트에 반드시 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 포함되어 있어야 합니다.

<a name="only-to-others-configuration"></a>
#### 관련 설정

라라벨 Echo 인스턴스를 초기화할 때 연결에 고유한 socket ID가 할당됩니다. 만약 JavaScript에서 글로벌 [Axios](https://github.com/axios/axios) 인스턴스를 사용할 경우, socket ID는 `X-Socket-ID` 헤더를 통해 모든 HTTP 요청에 자동으로 포함됩니다. `toOthers` 메서드를 호출하면, 라라벨은 이 헤더에서 socket ID를 추출해 해당 ID와 일치하는 연결로는 절대 이벤트를 브로드캐스트하지 않습니다.

글로벌 Axios 인스턴스를 사용하지 않는 경우, JavaScript 애플리케이션에서 `X-Socket-ID` 헤더를 직접 모든 요청에 포함시켜야 합니다. Echo에서 socket ID는 `Echo.socketId` 메서드로 가져올 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 브로드캐스트 커넥션 지정하기

애플리케이션에서 여러 개의 브로드캐스트 커넥션을 운영하고 있고, 기본값이 아닌 특정 커넥션으로 이벤트를 브로드캐스트하고 싶다면, `via` 메서드로 커넥션 이름을 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는, 이벤트 클래스의 생성자에서 `broadcastVia` 메서드를 호출하는 방식도 가능합니다. 단, 이 방법을 사용하려면 이벤트 클래스에 `InteractsWithBroadcasting` 트레이트가 포함되어야 합니다.

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
### 익명 이벤트 브로드캐스트

애플리케이션 프론트엔드에 간단한 이벤트를 브로드캐스트하고 싶은데, 별도의 이벤트 클래스를 만들 필요가 없는 경우도 있습니다. 이런 상황을 위해 `Broadcast` 파사드는 "익명 이벤트" 브로드캐스트를 지원합니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예시는 아래와 같은 이벤트를 브로드캐스트하게 됩니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as` 및 `with` 메서드를 이용해 이벤트 이름과 데이터를 원하는 대로 커스터마이즈할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

위 코드는 아래와 같은 형태로 이벤트를 브로드캐스트합니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

프라이빗 채널이나 프레즌스 채널에 익명 이벤트를 브로드캐스트하려면 `private` 및 `presence` 메서드를 사용할 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드를 통해 익명 이벤트를 브로드캐스트하면 [큐](/docs/12.x/queues)를 통해 처리됩니다. 만약 이벤트를 즉시 브로드캐스트하고 싶다면, `sendNow` 메서드를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증된 사용자를 제외한 모든 구독자에게만 익명 이벤트를 브로드캐스트하려면 `toOthers` 메서드를 활용하세요.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 예외 처리

애플리케이션의 큐 서버가 중단되었거나, 이벤트 브로드캐스트 중에 라라벨에서 오류가 발생하면, 예외가 발생해 사용자에게 애플리케이션 오류가 표시될 수 있습니다. 이벤트 브로드캐스트는 애플리케이션의 핵심 기능이 아닌 경우가 많으므로, 이러한 오류로 인해 사용자 경험이 방해되지 않도록 하려면 이벤트에 `ShouldRescue` 인터페이스를 구현하면 됩니다.

`ShouldRescue` 인터페이스를 구현한 이벤트는 라라벨의 [rescue 헬퍼 함수](/docs/12.x/helpers#method-rescue)를 자동으로 활용합니다. 이 헬퍼는 발생한 예외를 잡아 애플리케이션의 예외 핸들러에 기록하도록 넘기고, 최종적으로 사용자 작업 흐름이 끊기지 않게 합니다.

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
## 브로드캐스트 수신하기

<a name="listening-for-events"></a>
### 이벤트 수신(Listen)하기

[라라벨 Echo를 설치 및 인스턴스화](#client-side-installation)했다면, 이제 라라벨 애플리케이션에서 브로드캐스트한 이벤트를 수신(Listen)할 준비가 되었습니다. 먼저 `channel` 메서드로 채널 인스턴스를 가져오고, `listen` 메서드로 특정 이벤트를 수신하세요.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널에서 이벤트를 수신하고 싶다면 `private` 메서드를 사용하면 됩니다. 한 채널에서 여러 이벤트를 동시에 수신할 수도 있으며, 이 때는 `listen` 호출을 체이닝하면 됩니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중단

특정 이벤트 수신만 중단하고 [채널에서 나가지 않고](#leaving-a-channel) 싶다면, `stopListening` 메서드를 사용하세요.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널에서 나가기

채널에서 나가려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출하세요.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 연결된 비공개 및 프레즌스 채널까지 모두 나가고 싶다면, `leave` 메서드를 사용할 수 있습니다.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스

위 예시에서 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않은 것을 눈치챘을 수도 있습니다. 이는 Echo가 이벤트가 `App\Events` 네임스페이스에 있다고 자동으로 가정하기 때문입니다. Echo 인스턴스 생성 시 `namespace` 옵션을 통해 네임스페이스를 직접 지정할 수도 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는, Echo로 구독할 때 이벤트 클래스 앞에 점(`.`)을 붙이면, 항상 전체 네임스페이스를 지정해서 사용할 수도 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue에서 사용하기

라라벨 Echo는 React, Vue에서 이벤트 수신을 쉽게 해주는 전용 hook을 제공합니다. 먼저 `useEcho` hook을 호출하면, 비공개 이벤트 수신이 매우 간단해집니다. 이 hook은 소비 컴포넌트가 언마운트될 때 자동으로 채널에서 나가게 처리되어 있습니다.

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

여러 이벤트를 동시에 수신하려면, 이벤트 배열을 `useEcho`에 넘기면 됩니다.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트 페이로드 데이터의 타입 구조를 직접 지정해서, 타입 안정성과 편집 편의성을 높일 수도 있습니다.

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

`useEcho` hook은 컴포넌트가 언마운트될 때 자동으로 채널에서 나가지만, 함수로 리턴되는 여러 기능들을 통해 필요에 따라 직접 수신 중단/재개, 채널 나가기 등을 수동으로 할 수도 있습니다.

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
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

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>

#### 공개 채널에 연결하기

공개 채널에 연결하려면 `useEchoPublic` 훅을 사용할 수 있습니다.

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
#### 프레즌스 채널에 연결하기

프레즌스(presence) 채널에 연결하려면 `useEchoPresence` 훅을 사용할 수 있습니다.

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
## 프레즌스 채널(Presence Channels)

프레즌스 채널은 프라이빗 채널의 보안을 기반으로 하면서, 현재 해당 채널에 누가 가입해 있는지 알 수 있는 기능을 추가로 제공합니다. 이를 통해 같은 페이지를 보고 있는 사용자를 인지하게 하거나, 채팅방에 누가 있는지 목록을 보여주는 등 강력한 협업 기능을 쉽게 구축할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인가

모든 프레즌스 채널은 프라이빗 채널이기도 하므로, 사용자는 [채널 접근 권한이 인가되어야 합니다](#authorizing-channels). 그러나 프레즌스 채널의 인가 콜백을 정의할 때는, 사용자가 채널에 들어갈 수 있도록 단순히 `true`를 반환하는 대신, 사용자에 대한 정보를 담은 배열을 반환해야 합니다.

인가 콜백에서 반환한 데이터는 자바스크립트 애플리케이션에서 프레즌스 채널 이벤트 리스너에서 사용할 수 있습니다. 만약 사용자가 채널에 가입할 자격이 없다면, `false`나 `null`을 반환하면 됩니다.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 가입하기

프레즌스 채널에 가입하려면 Echo의 `join` 메서드를 사용할 수 있습니다. `join` 메서드는 `PresenceChannel` 구현체를 반환하며, `listen` 메서드뿐만 아니라 `here`, `joining`, `leaving` 등의 이벤트에 구독할 수 있습니다.

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

`here` 콜백은 채널에 성공적으로 가입하자마자 즉시 실행되며, 현재 해당 채널에 가입해 있는 모든 사용자 정보를 배열로 전달받습니다. `joining` 메서드는 새로운 사용자가 채널에 들어올 때, `leaving` 메서드는 사용자가 나갈 때 각각 호출됩니다. `error` 메서드는 인증 엔드포인트가 200 이외의 HTTP 상태 코드를 반환하거나, 반환된 JSON 파싱에 문제가 있을 경우 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로의 브로드캐스트

프레즌스 채널 역시 공개/프라이빗 채널처럼 이벤트를 받을 수 있습니다. 예를 들어, 채팅방에 대해 `NewMessage` 이벤트를 프레즌스 채널로 브로드캐스트하고 싶다면 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다.

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

다른 이벤트와 마찬가지로, 현재 사용자를 이벤트 브로드캐스트에서 제외하려면 `broadcast` 헬퍼와 `toOthers` 메서드를 사용할 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

또한, 일반적인 이벤트와 마찬가지로, Echo의 `listen` 메서드로 프레즌스 채널에서 발생한 이벤트를 청취할 수 있습니다.

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
## 모델 브로드캐스팅(Model Broadcasting)

> [!WARNING]
> 아래 모델 브로드캐스팅과 관련된 문서를 읽기 전에, 라라벨의 모델 브로드캐스팅 서비스의 일반적인 개념과 브로드캐스트 이벤트를 직접 생성하고 수신하는 방법을 먼저 숙지하는 것이 좋습니다.

애플리케이션의 [Eloquent 모델](/docs/12.x/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하는 것이 일반적입니다. 당연히 이 작업은 [Eloquent 모델 상태 변경에 대한 커스텀 이벤트를 직접 정의하고](/docs/12.x/eloquent#events), 해당 이벤트에 `ShouldBroadcast` 인터페이스를 구현함으로써 쉽게 달성할 수 있습니다.

그러나 애플리케이션에서 다른 목적 없이 오직 브로드캐스트를 위해서만 이벤트 클래스를 만들어야 한다면, 상당히 번거로울 수 있습니다. 이를 개선하기 위해, 라라벨은 Eloquent 모델이 상태 변경을 자동으로 브로드캐스트하도록 지정하는 기능을 제공합니다.

시작하려면, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 적용해야 합니다. 그리고 모델에서 `broadcastOn` 메서드를 정의하여, 모델 이벤트가 브로드캐스트될 채널의 배열을 반환하도록 만들어야 합니다.

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

이처럼 모델에 트레이트를 적용하고 브로드캐스트 채널을 정의하면, 앞으로 해당 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동(trashed), 복원(restored)될 때마다 자동으로 브로드캐스트됩니다.

또한, `broadcastOn` 메서드가 문자열 `$event` 인자를 받는 것을 볼 수 있습니다. 이 인자에는 모델에서 발생한 이벤트의 타입이 전달되며, 값은 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나가 됩니다. 이를 활용하여 특정 이벤트에 대해 어떤 채널에 브로드캐스트할지(또는 하지 않을지)를 구분할 수 있습니다.

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

가끔은 라라벨이 내부적으로 생성하는 모델 브로드캐스트 이벤트를 커스터마이징하고 싶을 때도 있습니다. 이럴 때는 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

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
### 모델 브로드캐스팅 규칙(컨벤션)

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 컨벤션

앞서 본 예제에서 모델의 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않고, Eloquent 모델 인스턴스를 직접 반환하고 있습니다. 만약 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스를 반환하면(또는 반환되는 배열에 포함되어 있다면), 라라벨은 해당 모델의 클래스명과 기본 키(primary key)를 채널명으로 사용하는 프라이빗 채널을 자동으로 생성해줍니다.

예를 들어, `id`가 1인 `App\Models\User` 모델의 경우 라라벨은 이 객체를 `App.Models.User.1`라는 이름의 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환합니다. 물론 모델의 `broadcastOn`에서 직접 `Channel` 인스턴스를 반환하여 채널 이름을 완전히 제어하고 싶으면 그 방법도 사용할 수 있습니다.

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

`broadcastOn` 메서드에서 채널 인스턴스를 직접 반환할 때, 해당 채널의 생성자에 Eloquent 모델 객체를 인자로 넘길 수도 있습니다. 이 경우 앞서 언급한 모델 채널 네이밍 규칙을 따라 채널 이름 문자열로 변환됩니다.

```php
return [new Channel($this->user)];
```

모델의 채널 이름이 궁금하다면, 모델 인스턴스에서 `broadcastChannel` 메서드를 호출하면 됩니다. 예를 들어, `id`가 1인 `App\Models\User` 모델의 경우, 이 메서드는 `App.Models.User.1`이라는 문자열을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 컨벤션

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉토리에 있는 "실제" 이벤트 클래스와 연결되어 있지 않으므로, 이름과 페이로드(payload)는 규칙(컨벤션)에 의해 자동으로 지정됩니다. 라라벨에서는 모델의 클래스명(네임스페이스 제외)과 이벤트 명을 이용해 브로드캐스트 이벤트 이름을 정합니다.

예를 들어, `App\Models\Post` 모델이 업데이트되면, 클라이언트 쪽 애플리케이션에서 `PostUpdated`라는 이름으로 다음과 같은 페이로드가 전달됩니다.

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

`App\Models\User` 모델이 삭제될 경우에는 `UserDeleted`라는 이벤트 이름으로 브로드캐스트됩니다.

필요하다면, `broadcastAs`와 `broadcastWith` 메서드를 모델에 추가하여 커스텀 브로드캐스트 이름과 페이로드를 정의할 수도 있습니다. 이 메서드들은 해당 모델에서 발생한 이벤트/연산의 이름을 인자로 받아, 각 이벤트마다 이름과 데이터를 자유롭게 바꿀 수 있습니다. 만약 `broadcastAs`에서 `null`을 반환하면, 라라벨은 자동으로 위의 규칙을 따라 이름을 지정합니다.

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
### 모델 브로드캐스트 수신하기

이제 모델에 `BroadcastsEvents` 트레이트를 추가하고 `broadcastOn` 메서드를 정의했다면, 클라이언트 애플리케이션에서 브로드캐스트된 모델 이벤트를 수신할 준비가 끝났습니다. 본격적으로 시작하기 전에, [이벤트 청취 관련 전체 문서](#listening-for-events)를 참고하시는 것이 좋습니다.

우선 `private` 메서드를 통해 채널 인스턴스를 가져오고, `listen` 메서드를 호출해 원하는 이벤트를 청취하면 됩니다. 이때, 채널 이름은 라라벨의 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)에 맞게 지정해야 합니다.

채널 인스턴스를 가져온 후에는 `listen` 메서드를 호출하여 원하는 이벤트를 청취할 수 있습니다. 모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉토리 내 실제 이벤트와 매핑되어 있지 않으므로, [이벤트 이름](#model-broadcasting-event-conventions) 앞에 마침표(`.`)를 붙여 네임스페이스가 없음을 표시해야 합니다. 각 모델 브로드캐스트 이벤트에는 `model` 프로퍼티가 있으며, 해당 모델의 브로드캐스트 가능한 모든 속성이 담겨 있습니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React나 Vue에서 사용하기

React 또는 Vue를 사용할 경우, 라라벨 Echo에 포함된 `useEchoModel` 훅을 활용해 매우 간편하게 모델 브로드캐스트를 수신할 수 있습니다.

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

또한 모델 이벤트 페이로드 데이터의 구조(type)를 직접 지정해, 더 안전하게 타입 체킹 및 코드 작성을 할 수 있습니다.

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
## 클라이언트 이벤트(Client Events)

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings" 섹션에서 "Client Events" 옵션을 활성화해야 클라이언트 이벤트 전송이 가능합니다.

때때로 라라벨 애플리케이션의 서버를 거치지 않고, 다른 연결된 클라이언트로 직접 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어, 다른 사용자가 채팅 중 입력 중임을 알릴 수 있는 "입력 중" 알림과 같은 기능에 유용하게 사용할 수 있습니다.

클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용할 수 있습니다.

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

클라이언트 이벤트를 청취하려면, `listenForWhisper` 메서드를 사용하면 됩니다.

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

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
## 알림(Notifications)

이벤트 브로드캐스팅을 [알림](/docs/12.x/notifications)과 결합하면, 자바스크립트 애플리케이션이 새 알림을 실시간으로 받을 수 있으므로, 사용자가 페이지를 새로 고치지 않아도 됩니다. 먼저 [브로드캐스트 알림 채널 사용법](/docs/12.x/notifications#broadcast-notifications) 문서를 꼭 읽어보시기 바랍니다.

브로드캐스트 채널을 사용하도록 알림을 설정했다면, Echo의 `notification` 메서드를 통해 브로드캐스트 이벤트를 청취할 수 있습니다. 이때 채널 이름은 알림을 수신할 대상 엔티티의 클래스명 규칙을 따라야 합니다.

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

이 예제에서는, `broadcast` 채널을 통해 `App\Models\User` 인스턴스에 보낸 모든 알림이 콜백 함수로 전달되게 됩니다. `App.Models.User.{id}` 채널에 대한 채널 인가 콜백은 애플리케이션의 `routes/channels.php` 파일에 포함되어 있습니다.