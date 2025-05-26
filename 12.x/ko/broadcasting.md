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
    - [예제 애플리케이션 활용하기](#using-example-application)
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
    - [타인에게만 브로드캐스트하기](#only-to-others)
    - [커스텀 커넥션 사용](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 수신 대기](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue 사용](#using-react-or-vue)
- [프레즌스 채널](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널로 브로드캐스트하기](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 수신](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

최근의 웹 애플리케이션에서는 실시간 갱신되는 사용자 인터페이스를 구현하기 위해 WebSocket이 자주 사용됩니다. 서버에서 데이터가 변경되면, WebSocket 연결을 통해 클라이언트로 메시지를 전송하게 됩니다. WebSocket을 사용하면 주기적으로 서버에 변경사항이 있는지 계속 요청(polling)하지 않아도 되기 때문에 더 효율적으로 UI를 갱신할 수 있습니다.

예를 들어, 여러분의 애플리케이션에서 사용자의 데이터를 CSV 파일로 내보내어 이메일로 전달하는 기능이 있다고 가정해 보겠습니다. 그러나 이 CSV 파일을 생성하는 데 몇 분이 걸릴 수 있어서, [큐 처리된 작업](/docs/12.x/queues)에서 파일 생성 및 이메일 발송을 처리하도록 구현한다고 가정합니다. CSV 파일이 생성되어 사용자가 이메일을 받은 시점에서, 브로드캐스팅 기능을 활용해 `App\Events\UserDataExported` 이벤트를 발행하고, 이는 애플리케이션의 자바스크립트 코드에서 바로 수신할 수 있습니다. 이를 통해 사용자는 페이지를 새로고침하지 않아도, CSV가 이메일로 전송되었다는 메시지를 실시간으로 확인할 수 있습니다.

이처럼 실시간 기능을 손쉽게 구현할 수 있도록, Laravel은 여러분이 서버에서 발생시키는 [이벤트](/docs/12.x/events)를 WebSocket 연결을 통해 효과적으로 브로드캐스트할 수 있는 방법을 제공합니다. 즉, Laravel의 이벤트를 브로드캐스트하면 서버에서 발생한 이벤트의 이름과 데이터가 클라이언트(JavaScript) 애플리케이션에서도 그대로 공유될 수 있습니다.

브로드캐스팅의 핵심 원리는 간단합니다. 클라이언트는 프론트엔드에서 특정 이름의 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 해당 채널로 이벤트를 브로드캐스트합니다. 이때 이벤트에는 프론트엔드에서 활용할 다양한 데이터도 함께 실을 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

기본적으로 Laravel은 서버 측 브로드캐스팅을 위한 3가지 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에, 먼저 [이벤트 및 리스너](/docs/12.x/events)에 대한 Laravel 공식 문서를 읽고 오시기를 권장합니다.

<a name="quickstart"></a>
## 빠른 시작

기본적으로 새로운 Laravel 애플리케이션에서는 브로드캐스팅 기능이 활성화되어 있지 않습니다. 브로드캐스팅을 사용하려면 `install:broadcasting` Artisan 명령어를 실행하여 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어를 실행하면, 사용하고자 하는 이벤트 브로드캐스팅 서비스를 어떤 것으로 할지 물어봅니다. 또한, 이 명령어는 `config/broadcasting.php` 설정 파일과, 애플리케이션의 브로드캐스트 인가 라우트 및 콜백을 등록할 `routes/channels.php` 파일을 생성합니다.

Laravel은 기본적으로 여러 가지 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버. 또한, 테스트 과정에서 브로드캐스팅을 비활성화하기 위한 `null` 드라이버도 포함되어 있습니다. 각 드라이버에 대한 설정 예시는 모두 `config/broadcasting.php` 파일에 포함되어 있습니다.

모든 브로드캐스팅에 관한 설정은 `config/broadcasting.php` 파일에 저장됩니다. 만약 이 파일이 아직 여러분의 애플리케이션에 없다면, `install:broadcasting` Artisan 명령어를 실행하면 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, 이제 [브로드캐스트 이벤트 정의](#defining-broadcast-events) 및 [이벤트 수신 대기](#listening-for-events)에 대해 보다 자세히 알아볼 준비가 되었습니다. 만약 Laravel의 React 또는 Vue [스타터 키트](/docs/12.x/starter-kits)를 사용한다면, Echo의 [useEcho 훅](#using-react-or-vue)을 이용해 편리하게 이벤트를 수신할 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스트하기 전에, 반드시 [큐 워커](/docs/12.x/queues)를 먼저 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅 작업은 큐에 올라가서 처리되므로, 브로드캐스트 작업 때문에 애플리케이션 응답 속도가 느려지는 일을 방지할 수 있습니다.

<a name="server-side-installation"></a>
## 서버 측 설치

Laravel의 이벤트 브로드캐스팅을 시작하려면, 애플리케이션 내에서 일부 설정을 하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅 기능은 서버 측의 브로드캐스팅 드라이버에 의해 처리되어, 여러분이 발생시키는 Laravel 이벤트를 브라우저 클라이언트의 Laravel Echo(자바스크립트 라이브러리)에서 수신할 수 있습니다. 걱정하지 마세요! 아래 단계별 안내를 따라가면 어렵지 않게 설정할 수 있습니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면, `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 붙여 실행합니다. 이 명령어는 Reverb와 관련된 Composer/NPM 패키지를 설치하고, 애플리케이션의 `.env` 파일에 필요한 변수들을 자동으로 추가해줍니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/12.x/reverb) 설치 여부를 질문합니다. 물론, 원한다면 Composer 패키지 매니저를 이용하여 직접 Reverb를 수동으로 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치가 끝나면, 다음 설치 명령어를 실행해서 Reverb의 설정 파일을 발행하고, 필요한 환경 변수를 등록하며, 이벤트 브로드캐스팅을 활성화하세요.

```shell
php artisan reverb:install
```

자세한 설치 및 사용법은 [Reverb 공식 문서](/docs/12.x/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 이용하여 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면, `install:broadcasting` Artisan 명령에 `--pusher` 옵션을 추가해 실행합니다. 이 명령은 Pusher 인증 정보를 입력받고, Pusher PHP/JavaScript SDK를 설치하며, `.env` 파일에 필요한 변수를 등록해줍니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher를 직접 수동으로 설정하기 위해서는 Composer 패키지 매니저로 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

그다음, `config/broadcasting.php` 설정 파일에서 Pusher Channels 인증 정보를 입력/수정해야 합니다. 이 파일에는 이미 Pusher Channels를 위한 예시 설정이 포함되어 있어서, 여러분의 키·시크릿·앱 ID만 바로 입력하면 됩니다. 보통은 `.env` 파일에 Pusher 인증 정보를 입력해놓고, 설정 파일에서는 이를 참조하는 방식을 사용합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

또한 `config/broadcasting.php` 파일의 `pusher` 설정에서, 클러스터(cluster) 등 Channels에서 지원하는 추가 `options`도 설정할 수 있습니다.

마지막으로, 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 지정해야 합니다.

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo](#client-side-installation) 패키지를 설치하고 설정하면, 클라이언트 측에서 브로드캐스트된 이벤트를 수신할 준비가 완료됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법에 대한 안내입니다. 하지만 Ably 팀에서는 Ably의 고유한 기능을 충분히 활용할 수 있는 자체 브로드캐스터 및 Echo 클라이언트 패키지를 공식적으로 제공하고 있습니다. Ably가 관리하는 드라이버를 사용하는 방법은 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)을(를) 브로드캐스터로 사용해서 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면, `install:broadcasting` Artisan 명령어에 `--ably` 옵션을 붙여 실행하세요. 이 명령은 Ably 인증 정보를 입력받고, Ably의 PHP/JavaScript SDK를 설치하며, `.env` 파일도 자동으로 업데이트합니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에, 반드시 Ably 애플리케이션의 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 대시보드의 'Protocol Adapter Settings' 메뉴에서 설정할 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 직접 수동으로 설정하려면, Composer로 Ably PHP SDK부터 설치해야 합니다.

```shell
composer require ably/ably-php
```

다음으로, `config/broadcasting.php` 설정 파일에 Ably 인증 정보를 입력해야 합니다. Ably 설정 예제가 파일에 포함되어 있으니, 여러분의 키만 추가하면 됩니다. 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/12.x/configuration#environment-configuration)를 이용해 지정합니다.

```ini
ABLY_KEY=your-ably-key
```

또한, 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정해야 합니다.

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo](#client-side-installation) 패키지를 설치하고 설정하면, 클라이언트 측에서 Ably를 통한 브로드캐스트 이벤트를 수신할 준비가 끝납니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버 측 드라이버에서 브로드캐스트한 이벤트 수신을 손쉽게 할 수 있도록 도와주는 자바스크립트 라이브러리입니다.

Reverb를 `install:broadcasting` Artisan 명령으로 설치하면, Reverb와 Echo의 초기 설정 및 구성이 자동으로 애플리케이션에 적용됩니다. 다만, Laravel Echo를 직접 수동으로 설정하고 싶다면 아래 안내를 참고하세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면 먼저 `pusher-js` 패키지를 설치해야 합니다. 이는 Reverb가 WebSocket 구독, 채널, 메시지 전송에 Pusher 프로토콜을 사용하기 때문입니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치가 끝나면, 애플리케이션의 자바스크립트에서 새로운 Echo 인스턴스를 만들어야 합니다. 보통 `resources/js/bootstrap.js` 파일 하단에 코드를 추가하는 것이 좋습니다.

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

이제 애플리케이션의 에셋을 빌드해야 합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터를 사용하려면 laravel-echo v1.16.0 이상 버전이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버 측 드라이버에서 브로드캐스트한 이벤트 수신을 손쉽게 할 수 있도록 도와주는 자바스크립트 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령어로 브로드캐스팅 지원을 설치하면, Pusher 및 Echo의 초기 구성과 파일이 애플리케이션에 자동으로 세팅됩니다. Echo를 직접 수동으로 설정하려면 아래 안내를 참고하세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, 우선 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다. 이 패키지들은 WebSocket 구독, 채널, 메시지 전송 등에 Pusher 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면, 애플리케이션 내 `resources/js/bootstrap.js` 파일에서 새로운 Echo 인스턴스를 만듭니다.

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

이제 애플리케이션의 `.env` 파일에 Pusher 환경 변수를 제대로 정의해야 합니다. 변수들이 없는 경우 직접 추가해 주세요.

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

Echo 설정을 마무리했다면 애플리케이션 에셋을 다시 빌드하세요.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 자바스크립트 에셋 빌드에 대해 더 자세히 알고 싶다면, [Vite](/docs/12.x/vite) 관련 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

미리 설정된 Pusher Channels 클라이언트 인스턴스를 Echo에서 그대로 사용하고 싶다면, `client` 설정 옵션으로 인스턴스를 전달할 수 있습니다.

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
> 아래 설명은 Ably를 "Pusher 호환 모드"로 사용하는 방법에 대한 안내입니다. 그러나 Ably 팀에서는 Ably에 특화되어 있는 드라이버 및 Echo 클라이언트도 공식 지원하고 있습니다. Ably가 제공하는 브로드캐스터와 클라이언트 사용법은 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 확인하세요.

[Laravel Echo](https://github.com/laravel/echo)는 채널 구독과 서버 측 드라이버에서 브로드캐스트한 이벤트 수신을 손쉽게 할 수 있도록 도와주는 자바스크립트 라이브러리입니다.

`install:broadcasting --ably` Artisan 명령어로 브로드캐스팅 지원을 설치하면, Ably와 Echo의 기본 설정 파일 및 구조가 여러분의 애플리케이션에 자동으로 적용됩니다. 수동으로 Echo를 설정하고 싶다면 아래 안내를 참고하세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 직접 설정하려면 먼저 `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다. 이 패키지들은 WebSocket 구독, 채널, 메시지 전송 등에 Pusher 프로토콜을 사용합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**설치하기 전에, 반드시 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 옵션은 Ably 대시보드의 "Protocol Adapter Settings" 부분에서 사용할 수 있습니다.**

Echo가 설치되면, `resources/js/bootstrap.js` 파일에서 새로운 Echo 인스턴스를 생성하세요.

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

여기서 Ably Echo 설정에 사용된 `VITE_ABLY_PUBLIC_KEY` 환경 변수는 여러분의 Ably 공개 키여야 합니다. 이 키는 Ably의 전체 키에서 `:` 문자 앞 부분이 공개 키입니다.

환경설정을 완료했다면 에셋을 빌드하세요.

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 에셋 빌드에 대한 자세한 안내는 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요

Laravel의 이벤트 브로드캐스팅은 여러분이 서버에서 발생시킨 이벤트를 드라이버 기반 방식(WebSocket)을 통해 클라이언트(JavaScript) 애플리케이션으로 실시간 전달할 수 있습니다. 현재 Laravel에서는 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 기본 제공하며, 클라이언트에서는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지로 쉽게 수신할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트됩니다. 각 채널은 공개(Public) 또는 비공개(Private)로 지정할 수 있습니다. 공개 채널은 인증이나 인가 없이 누구나 구독할 수 있으며, 비공개 채널은 인증 및 인가된 사용자만 구독할 수 있습니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 활용하기

각 브로드캐스팅 구성요소를 본격적으로 설명하기 전에, 전자상거래(e-commerce) 애플리케이션을 예시로 하여 전체 흐름을 먼저 살펴보겠습니다.

우리의 애플리케이션에는 사용자가 주문 배송 현황을 확인할 수 있는 페이지가 있다고 가정하겠습니다. 그리고 주문의 배송 상태가 갱신될 때마다 `OrderShipmentStatusUpdated` 이벤트가 발생됩니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 페이지를 보고 있을 때, 배송 상태가 변경될 때마다 자동으로 갱신되기를 원한다면 페이지를 새로고침할 필요 없이 브로드캐스트를 통해 실시간으로 갱신할 수 있습니다. 이를 위해서는 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이렇게 하면 이 이벤트가 발생할 때 자동으로 브로드캐스트됩니다.

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

`ShouldBroadcast` 인터페이스를 구현하면 이벤트 클래스에 `broadcastOn` 메서드를 반드시 정의해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널을 반환해야 하며, 이벤트 클래스를 생성하면 기본적으로 메서드의 틀이 제공되므로 내용을 채워주기만 하면 됩니다. 이 예제에선 해당 주문의 생성자(주문자)만 배송 상태를 볼 수 있어야 하므로, 주문에 연결된 비공개 채널로 이벤트를 전송합니다.

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

여러 채널에 동시에 이 이벤트를 브로드캐스트하고 싶다면, `array` 형식으로 여러 채널을 반환할 수 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트가 브로드캐스트될 채널들을 반환합니다.
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

비공개 채널의 이벤트를 수신하려면 사용자가 인가(authorization)되어야 합니다. 이를 위해, 애플리케이션의 `routes/channels.php` 파일에 채널 인가 규칙을 정의할 수 있습니다. 이 예제에서는, 누군가 `orders.1` 비공개 채널을 구독하려 할 때 주문의 실제 작성자인지 확인하는 것이 필요합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인자를 받습니다. 첫 번째는 채널 이름이고, 두 번째는 해당 채널 청취 권한이 있는지 판별하여 `true` 또는 `false`를 반환하는 콜백입니다.

모든 인가 콜백은 첫 번째 인자로 현재 인증된 사용자, 그리고 그 뒤에 와일드카드로 받은 매개변수(이 예제의 `{orderId}`)들을 전달받습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신 대기

이제 마지막으로, 자바스크립트 애플리케이션 쪽에서 해당 이벤트를 수신 대기하면 됩니다. 이 작업은 [Laravel Echo](#client-side-installation)로 할 수 있습니다. Echo의 내장 React/Vue 훅을 사용하면 간단하게 이벤트를 구독할 수 있으며, 이벤트 내의 모든 public 속성들도 기본적으로 함께 포함되어 전송됩니다.

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

특정 이벤트를 브로드캐스트 해야 한다는 것을 Laravel에 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크에서 생성하는 모든 이벤트 클래스에 이미 import되어 있으므로, 쉽게 여러분의 이벤트에 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스에서는 오직 하나의 메서드, 즉 `broadcastOn`만을 구현하면 됩니다. `broadcastOn` 메서드는 이벤트가 브로드캐스트되어야 할 채널 또는 채널 배열을 반환해야 합니다. 이 채널들은 `Channel`, `PrivateChannel`, 또는 `PresenceChannel`의 인스턴스여야 합니다. `Channel` 인스턴스는 누구나 구독할 수 있는 공개 채널을 나타내고, `PrivateChannel`과 `PresenceChannel`은 [채널 인가](#authorizing-channels)가 필요한 비공개 채널입니다.

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

`ShouldBroadcast` 인터페이스를 구현하면, [이벤트를 일반적으로 발생시키는 것](/docs/12.x/events) 외에 추가 작업이 필요하지 않습니다. 이벤트가 발생하면, [대기열 작업](/docs/12.x/queues)이 자동으로 해당 브로드캐스트 드라이버를 사용해 이벤트를 브로드캐스트합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름 지정

기본적으로, Laravel은 이벤트의 클래스명을 사용하여 이벤트를 브로드캐스트합니다. 하지만, 이벤트 내에 `broadcastAs` 메서드를 정의하면 브로드캐스트 이름을 자유롭게 지정할 수 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs` 메서드를 사용하여 이벤트 이름을 커스텀하는 경우, 리스너를 등록할 때 이름 앞에 `.` 문자를 붙여야 합니다. 이렇게 하면 Echo가 이벤트 이름 앞에 애플리케이션의 네임스페이스를 자동으로 붙이지 않습니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트 될 때, 이벤트 내의 모든 `public` 속성이 자동으로 직렬화되어 이벤트의 페이로드(payload)로 브로드캐스트됩니다. 이를 통해 자바스크립트 애플리케이션에서 이벤트의 public 데이터에 즉시 접근할 수 있습니다. 예를 들어, 이벤트에 Eloquent 모델이 담긴 public `$user` 속성 하나만 포함되어 있다면, 브로드캐스트 페이로드는 다음과 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

하지만 브로드캐스트 페이로드를 더 세밀하게 제어하고 싶다면, 이벤트에 `broadcastWith` 메서드를 추가할 수 있습니다. 이 메서드는 브로드캐스트할 데이터를 포함하는 배열을 반환해야 합니다.

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
### 브로드캐스트 대기열

기본적으로, 각 브로드캐스트 이벤트는 `queue.php` 설정 파일에서 지정한 기본 대기열 커넥션의 기본 대기열로 들어갑니다. 브로드캐스트에 사용할 대기열 커넥션 및 이름을 이벤트 클래스에 `connection`과 `queue` 속성을 정의하여 커스텀할 수 있습니다.

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

또는, 이벤트에 `broadcastQueue` 메서드를 정의해 대기열 이름만 변경할 수도 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

만약 기본 대기열 드라이버 대신 `sync` 대기열로 이벤트를 브로드캐스트하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다.

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

어떤 경우에는 지정된 조건이 참일 때만 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이런 경우 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 조건을 정의할 수 있습니다.

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

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내에서 디스패치되면, 대기열 작업이 데이터베이스 트랜잭션이 커밋되기 전에 처리될 수 있습니다. 이때, 트랜잭션 동안 모델이나 데이터베이스 레코드에 한 업데이트가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내에서 새로 생성된 모델 또는 레코드가 아직 데이터베이스에 없을 수도 있습니다. 이벤트가 이러한 모델에 의존하면, 브로드캐스트 작업 처리 시 예기치 않은 오류가 발생할 수 있습니다.

대기열 커넥션의 `after_commit` 설정 옵션이 `false`인 경우에도, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 모든 오픈된 데이터베이스 트랜잭션이 커밋된 후에 해당 이벤트를 디스패치하도록 지정할 수 있습니다.

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
> 이러한 문제를 우회하는 방법에 대해 더 자세히 알아보고 싶다면 [대기열 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인가(Authorization)하기

프라이빗 채널은 현재 인증된 사용자가 실제로 해당 채널을 수신할 수 있는지 인가(authorize)해야 합니다. 이를 위해, 채널 이름을 포함하는 HTTP 요청을 Laravel 애플리케이션에 보내고, 애플리케이션은 해당 사용자가 그 채널을 수신할 수 있는지 판단하게 됩니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 프라이빗 채널 구독에 필요한 HTTP 인증 요청은 자동으로 이루어집니다.

브로드캐스팅이 활성화되면 Laravel은 인증 요청을 처리할 수 있도록 `/broadcasting/auth` 라우트를 자동으로 등록합니다. 이 라우트는 자동으로 `web` 미들웨어 그룹에 포함됩니다.

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의하기

이제 현재 인증된 사용자가 특정 채널을 수신할 수 있는지 실제로 판단할 로직을 정의해야 합니다. 이 작업은 `install:broadcasting` Artisan 명령어로 생성된 `routes/channels.php` 파일에서 이루어집니다. 이 파일에서 `Broadcast::channel` 메서드를 사용해 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 가지 인수를 받습니다. 첫째는 채널 이름이고, 둘째는 사용자가 채널을 수신할 자격이 있는지 여부를 `true` 또는 `false`로 반환하는 콜백입니다.

모든 인가 콜백은 인증된 사용자 인스턴스를 첫 번째 인수로 받고, 추가 와일드카드(wildcard) 파라미터들을 이후 인수로 받습니다. 위 예시에서는 `{orderId}` 플레이스홀더를 사용해 채널의 "ID" 부분이 와일드카드임을 나타냅니다.

애플리케이션 내의 브로드캐스트 인가 콜백 목록을 Artisan 명령어로 확인할 수도 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백의 모델 바인딩

HTTP 라우트와 마찬가지로, 채널 라우트에서도 암묵적, 명시적 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어, 단순히 문자열이나 숫자 order ID를 받는 대신 실제 `Order` 모델 인스턴스를 파라미터로 받을 수도 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 [암묵적 모델 바인딩 스코핑](/docs/12.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 하지만 대부분의 채널은 단일 모델의 고유(Primary Key)로 범위를 한정할 수 있으므로 큰 문제는 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백의 인증

프라이빗 및 프레즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 guard를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않은 경우, 채널 인가는 자동으로 거부되며 인가 콜백은 실행되지 않습니다. 다만, 필요하다면 요청 인증에 사용할 여러 개의 커스텀 guard를 지정할 수도 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션에서 여러 가지 채널을 사용한다면, `routes/channels.php` 파일이 점점 복잡해질 수 있습니다. 이럴 땐, 클로저 대신 채널 클래스를 사용할 수 있습니다. 채널 클래스는 `make:channel` Artisan 명령어로 생성할 수 있으며, 이 명령어는 `App/Broadcasting` 디렉터리에 새 채널 클래스를 생성합니다.

```shell
php artisan make:channel OrderChannel
```

그 다음, `routes/channels.php` 파일에서 해당 채널을 아래와 같이 등록하세요.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

마지막으로, 채널 클래스의 `join` 메서드 안에 인가 로직을 작성하면 됩니다. `join` 메서드는 일반적으로 클로저에 작성했던 인가 로직을 담습니다. 또한, 채널 모델 바인딩도 활용할 수 있습니다.

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
> Laravel의 많은 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/12.x/container)에서 자동으로 resolve됩니다. 따라서, 생성자에 필요한 의존성을 타입으로 지정하여 주입받을 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 지정했다면, 해당 이벤트의 dispatch 메서드를 호출하여 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처(dispatcher)는 해당 이벤트가 `ShouldBroadcast` 인터페이스를 구현했음을 감지하고, 브로드캐스트를 위해 이벤트를 대기열에 등록합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스트하기

이벤트 브로드캐스팅이 적용되는 애플리케이션에서는, 가끔 특정 채널의 모든 구독자에게 이벤트를 전달하되 현재 사용자 본인에게는 전달하지 않아야 하는 경우가 있습니다. 이때는 `broadcast` 헬퍼와 `toOthers` 메서드를 함께 사용하면 됩니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

이 방법이 필요한 상황을 좀 더 명확하게 이해하려면, 예를 들어 할 일 목록 애플리케이션을 생각해봅시다. 사용자가 새로운 할 일을 입력하면, `/task` URL로 요청을 보내고, 이때 할 일 생성 이벤트를 브로드캐스트하며, 새 할 일을 JSON 형식으로 반환합니다. 자바스크립트 애플리케이션은 엔드포인트의 응답을 받아서 할 일 목록에 직접 추가할 수 있습니다.

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

그런데, 할 일 생성 이벤트가 브로드캐스트되고, 자바스크립트 애플리케이션에서도 이 이벤트를 수신해 할 일을 추가하고 있다면, 목록에 똑같은 항목이 두 번 들어갈 수 있습니다(엔드포인트 응답, 브로드캐스트 이벤트 양쪽 모두에서 추가). 이를 방지하기 위해 `toOthers` 메서드를 사용하면, 브로드캐스터가 현재 사용자에게는 이벤트를 브로드캐스트하지 않습니다.

> [!WARNING]
> `toOthers` 메서드를 호출하려면 이벤트에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 반드시 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 추가 설정

Laravel Echo 인스턴스를 초기화하면, 소켓 ID(socket ID)가 연결에 할당됩니다. 자바스크립트 애플리케이션에서 global [Axios](https://github.com/axios/axios) 인스턴스를 사용해 HTTP 요청을 보내면, 이 소켓 ID는 모든 요청의 `X-Socket-ID` 헤더에 자동으로 포함됩니다. 그리고 `toOthers` 메서드를 호출할 때 Laravel이 해당 헤더에서 소켓 ID를 읽어 동일한 소켓 ID를 가진 연결에는 브로드캐스트하지 않도록 지시하게 됩니다.

만약 global Axios 인스턴스를 사용하지 않는다면, 자바스크립트 애플리케이션에서 `X-Socket-ID` 헤더를 직접 모든 요청에 포함시키도록 구성해야 합니다. 소켓 ID는 `Echo.socketId` 메서드로 얻을 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커스텀 브로드캐스트 커넥션 사용

애플리케이션이 여러 브로드캐스트 커넥션과 상호작용하고, 기본 커넥션이 아닌 다른 브로드캐스터를 이용해 이벤트를 브로드캐스트하고 싶을 때, `via` 메서드로 어떤 커넥션에 이벤트를 전달할지 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트 클래스의 생성자에서 `broadcastVia` 메서드를 호출해 브로드캐스트 커넥션을 지정할 수도 있습니다. 이때는 이벤트 클래스에서 `InteractsWithBroadcasting` 트레이트를 사용하고 있어야 합니다.

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
### 익명 이벤트 브로드캐스팅

때로는 전용 이벤트 클래스를 만들 필요 없이, 프런트엔드로 간단하게 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이를 위해 `Broadcast` 파사드는 "익명 이벤트"(anonymous events)를 브로드캐스트하는 기능을 제공합니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예시는 다음과 같은 형식의 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`와 `with` 메서드를 쓰면, 이벤트의 이름과 데이터를 원하는 대로 커스텀할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

위 코드는 다음과 비슷한 형식의 이벤트를 브로드캐스트합니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

프라이빗 또는 프레즌스 채널로 익명 이벤트를 브로드캐스트 하고 싶다면, `private` 또는 `presence` 메서드를 사용할 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드를 사용해 익명 이벤트를 브로드캐스트하면, 해당 이벤트가 [대기열](/docs/12.x/queues)을 통해 처리됩니다. 바로 브로드캐스트 하려면 `sendNow` 메서드를 사용하면 됩니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증된 사용자를 제외한 모든 채널 구독자에게만 이벤트를 브로드캐스트하고 싶다면, `toOthers` 메서드를 호출할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="receiving-broadcasts"></a>
## 브로드캐스트 이벤트 수신하기

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo를 설치 및 인스턴스화](#client-side-installation)했다면, 이제 Laravel 애플리케이션에서 브로드캐스트하는 이벤트를 수신할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻고, 이후 `listen` 메서드를 체이닝해 특정 이벤트를 리스닝하세요.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

프라이빗 채널에서 이벤트를 수신하려면, `private` 메서드를 사용하면 됩니다. 하나의 채널에서 여러 이벤트를 계속해서 수신하려면 `listen` 메서드를 체이닝하면 됩니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중지

[채널에서 나가지 않고](#leaving-a-channel), 특정 이벤트만 리스닝을 중지하고 싶다면 `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 떠나기

채널에서 나가고 싶을 때는, Echo 인스턴스에서 `leaveChannel` 메서드를 호출하면 됩니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널은 물론, 연관된 프라이빗 및 프레즌스 채널도 함께 나가고 싶다면 `leave` 메서드를 호출하세요.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스

앞선 예제에서 이벤트 클래스의 전체 네임스페이스(`App\Events`)를 명시하지 않았던 것을 눈치챌 수 있습니다. 이는 Echo에서 이벤트가 기본적으로 `App\Events` 네임스페이스에 있다고 가정하기 때문입니다. 그러나 Echo 인스턴스를 생성할 때 `namespace` 옵션을 통해 루트 네임스페이스를 직접 지정할 수도 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는, Echo를 통해 이벤트를 구독할 때 클래스명 앞에 `.`을 붙이면, 항상 전체 네임스페이스를 명시할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue에서 사용하기

Laravel Echo는 이벤트 리스닝을 쉽게 할 수 있도록 React 및 Vue용 hook도 제공합니다. 먼저 `useEcho` hook을 호출하세요. 이 hook은 프라이빗 이벤트를 리스닝 할 때 사용하며, 컴포넌트가 언마운트(unmount)되면 채널에서 자동으로 나가게 됩니다.

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

이벤트 배열을 전달하면 여러 이벤트를 리스닝할 수 있습니다.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트 페이로드 데이터의 타입을 직접 지정하여, 타입 안정성을 확보하고 편리하게 개발할 수도 있습니다.

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

`useEcho` hook은 컴포넌트 언마운트 시 채널을 자동으로 떠나지만, 반환되는 함수를 이용해 상황에 따라 수동으로 이벤트 리스닝을 중지·재시작하거나 채널을 떠날 수도 있습니다.

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 채널은 떠나지 않고 리스닝만 중지...
stopListening();

// 리스닝 재시작...
listen();

// 채널 떠나기...
leaveChannel();

// 채널 및 관련 프라이빗/프레즌스 채널까지 모두 떠나기...
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

// 채널은 떠나지 않고 리스닝만 중지...
stopListening();

// 리스닝 재시작...
listen();

// 채널 떠나기...
leaveChannel();

// 채널 및 관련 프라이빗/프레즌스 채널까지 모두 떠나기...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>

#### 퍼블릭 채널 연결하기

퍼블릭 채널에 연결하려면 `useEchoPublic` 훅을 사용할 수 있습니다.

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

프레즌스 채널에 연결하려면 `useEchoPresence` 훅을 사용할 수 있습니다.

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

프레즌스 채널은 프라이빗 채널의 보안성을 기반으로, 현재 채널에 구독 중인 사용자가 누구인지까지 알 수 있는 기능을 추가로 제공합니다. 이를 통해, 같은 페이지를 보고 있는 사용자가 누군지 알리거나, 채팅방의 참여자 목록을 실시간으로 보여주는 등의 강력한 협업 기능을 쉽게 구현할 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인가

모든 프레즌스 채널은 프라이빗 채널이기도 하므로, 반드시 [프라이빗 채널 접근 권한](#authorizing-channels)이 필요합니다. 하지만 프레즌스 채널에 대한 인가 콜백을 정의할 때는, 사용자가 채널에 접속할 수 있다고 해서 `true`를 반환하지 않고, 대신 사용자에 관한 데이터를 담은 배열을 반환해야 합니다.

이 콜백에서 반환한 데이터는 JavaScript 애플리케이션에서 프레즌스 채널 이벤트 리스너를 통해 활용할 수 있습니다. 만약 사용자가 프레즌스 채널에 접속할 수 없는 경우에는 `false` 또는 `null`을 반환하면 됩니다.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널에 참여하기

프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용할 수 있습니다. 이 메서드는 `PresenceChannel` 구현체를 반환하며, 일반 `listen` 메서드뿐 아니라 `here`, `joining`, `leaving` 이벤트에 대한 구독도 함께 지원합니다.

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

`here` 콜백은 채널에 성공적으로 참여했을 때 즉시 실행되며, 현재 채널에 접속해 있는 모든 사용자 정보를 배열로 전달받습니다. `joining` 콜백은 새로운 사용자가 채널에 참가할 때, `leaving` 콜백은 사용자가 채널에서 나갈 때 각각 호출됩니다. `error` 콜백은 인증 엔드포인트에서 200이 아닌 HTTP 상태 코드를 반환하거나, JSON 파싱에 문제가 있을 때 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅하기

프레즌스 채널도 퍼블릭이나 프라이빗 채널과 마찬가지로 이벤트를 받을 수 있습니다. 채팅방 예시를 들어, `NewMessage` 이벤트를 해당 방의 프레즌스 채널로 브로드캐스트할 수 있습니다. 이를 위해 이벤트 클래스의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환합니다.

```php
/**
 * 이벤트가 브로드캐스트될 채널을 반환합니다.
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

다른 이벤트와 마찬가지로, `broadcast` 헬퍼와 `toOthers` 메서드를 사용하여 현재 사용자에게는 브로드캐스트 메시지가 전달되지 않도록 할 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

또한, 다른 종류의 이벤트와 마찬가지로 Echo의 `listen` 메서드를 활용해 프레즌스 채널로 전송된 이벤트를 쉽게 수신할 수 있습니다.

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
> 아래의 모델 브로드캐스팅 문서를 읽기 전에, 라라벨의 모델 브로드캐스팅 서비스의 개념과, 브로드캐스트 이벤트를 수동으로 생성하고 수신하는 방법을 먼저 숙지하는 것을 권장합니다.

애플리케이션의 [Eloquent 모델](/docs/12.x/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 것은 흔히 사용되는 패턴입니다. 물론, 이는 직접 [Eloquent 모델 상태 변경시 커스텀 이벤트를 정의](/docs/12.x/eloquent#events)하고 해당 이벤트에 `ShouldBroadcast` 인터페이스를 구현해서 손쉽게 구현할 수 있습니다.

하지만 이런 이벤트를 다른 곳에서 사용하지 않고 브로드캐스팅 목적으로만 만들 경우, 이벤트 클래스를 매번 생성하는 것이 불필요하게 느껴질 수 있습니다. 이런 불편함을 해소하기 위해 라라벨에서는 Eloquent 모델의 상태 변화가 자동으로 브로드캐스트되도록 설정할 수 있는 기능을 제공합니다.

시작하려면, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하세요. 그리고 `broadcastOn` 메서드를 정의해 이 모델의 이벤트가 브로드캐스트될 채널 배열을 반환해야 합니다.

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
     * 이 포스트가 소속된 유저 반환.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트될 채널 배열 반환.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이처럼 모델에 트레이트를 추가하고 브로드캐스트 채널을 정의하면, 해당 모델 인스턴스가 생성, 수정, 삭제, 소프트 삭제(trashed), 복원(restored)될 때마다 자동으로 모델 이벤트가 브로드캐스트됩니다.

또한, `broadcastOn` 메서드에는 `$event`라는 문자열 인자가 전달됩니다. 이 값은 모델에서 발생한 이벤트 타입(`created`, `updated`, `deleted`, `trashed`, `restored` 중 하나)을 의미합니다. 이 변수를 활용해 이벤트 타입별로 어떤 채널에 브로드캐스트할지 동적으로 결정할 수 있습니다.

```php
/**
 * 모델 이벤트가 브로드캐스트될 채널 배열 반환.
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

가끔은 라라벨이 생성하는 기본 모델 브로드캐스트 이벤트 생성 방식을 커스터마이즈하고 싶을 수 있습니다. 이럴 땐 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의하면 됩니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델에 대한 새로운 브로드캐스트 이벤트 인스턴스를 생성합니다.
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
#### 채널 명명 규칙

위 예시에서 보았던 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않고, Eloquent 모델 그 자체를 반환하는 것도 허용한다는 점을 주목할 만합니다. 만약 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스(또는 이 인스턴스들을 포함한 배열)를 반환하면, 라라벨은 해당 모델의 클래스명과 기본 키(primary key)를 조합하여 자동으로 프라이빗 채널 인스턴스를 생성해줍니다.

예를 들어, `App\Models\User` 모델의 `id`가 1이면, 이 인스턴스는 내부적으로 `App.Models.User.1`이라는 이름의 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환됩니다. 물론 직접 채널 이름을 지정하고 싶다면, `broadcastOn` 메서드에서 완전한 `Channel` 인스턴스를 반환해도 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트가 브로드캐스트될 채널 배열 반환.
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

만약 명시적으로 채널 인스턴스를 반환할 계획이라면, 생성자에 Eloquent 모델 인스턴스를 바로 전달할 수도 있습니다. 이 경우 라라벨은 앞서 설명한 모델 채널 명명 규칙에 따라 모델로부터 채널명을 자동 생성합니다.

```php
return [new Channel($this->user)];
```

모델의 채널 이름을 코드 내에서 직접 확인하고자 한다면, 어떤 모델 인스턴스에서든 `broadcastChannel` 메서드를 호출할 수 있습니다. 예를 들어 `App\Models\User` 모델의 `id` 값이 1이라면, 이 메서드는 `App.Models.User.1`이라는 문자열을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 명명 및 페이로드 규칙

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉토리에 실제 파일로 존재하지 않으므로, 이름과 페이로드(payload)는 라라벨의 규약에 따라 자동 지정됩니다. 라라벨의 기본 규칙은, 모델의 클래스명(네임스페이스 제외)과 발생한 모델 이벤트명을 조합해 이벤트 이름을 만듭니다.

예를 들어, `App\Models\Post` 모델이 업데이트되면, 클라이언트 애플리케이션에는 `PostUpdated`라는 이벤트명이 전송되며, 페이로드는 다음과 같은 형태입니다.

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

`App\Models\User` 모델이 삭제된 경우라면, 이벤트 이름은 `UserDeleted`가 됩니다.

원한다면, `broadcastAs`와 `broadcastWith` 메서드를 모델에 정의하여 이벤트 이름과 페이로드를 직접 커스터마이즈할 수도 있습니다. 이 두 메서드는 모두 모델 이벤트/동작명을 인자로 받아, 각 이벤트마다 이름과 페이로드를 다르게 제어할 수 있습니다. 만약 `broadcastAs`에서 `null`을 반환하면, 앞서 설명한 기본 네이밍 규칙을 따릅니다.

```php
/**
 * 모델 이벤트의 브로드캐스트명 지정.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델의 브로드캐스트 페이로드 반환.
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

모델에 `BroadcastsEvents` 트레이트를 추가하고 `broadcastOn` 메서드를 정의했다면, 이제 클라이언트 애플리케이션에서 모델 이벤트를 수신할 준비가 된 것입니다. 시작하기 전에 [이벤트 수신 방법](#listening-for-events) 전체 문서를 참조하는 것도 좋습니다.

먼저, `private` 메서드를 이용해 채널 인스턴스를 가져오고, 이어서 `listen` 메서드로 특정 이벤트만 수신할 수 있습니다. 이때 채널 이름은 라라벨의 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)에 맞춰야 합니다.

채널 인스턴스를 얻었다면, 이제 `listen` 메서드로 원하는 이벤트만 리스닝할 수 있습니다. 이 모델 브로드캐스트 이벤트는 실제로 애플리케이션의 `App\Events` 디렉토리에 존재하지 않으므로, [이벤트명](#model-broadcasting-event-conventions) 앞에 `.`(마침표)를 붙여 네임스페이스가 없는 이벤트임을 표시해야 합니다. 각 모델 이벤트의 페이로드에는 `model` 속성이 포함되어, 브로드캐스트 대상 모델의 속성 전체가 들어 있습니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

React 또는 Vue에서 모델 브로드캐스트를 수신하려면, Laravel Echo에 기본 제공되는 `useEchoModel` 훅을 사용할 수 있습니다.

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

또한, 모델 이벤트 페이로드의 타입 형태를 직접 지정해 타입 안정성과 편집 편의성을 높일 수도 있습니다.

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
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 반드시 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

간혹 라라벨 서버를 거치지 않고, 다른 클라이언트들에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어, 누가 채팅 입력창에 타이핑 중임을 다른 사용자에게 알려주는 "타이핑 중" 알림 기능 등이 대표적입니다.

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

클라이언트 이벤트를 수신하려면 `listenForWhisper` 메서드를 사용하세요.

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

이벤트 브로드캐스팅과 [알림](/docs/12.x/notifications)을 결합하면, 페이지를 새로고침하지 않아도 JavaScript 애플리케이션에서 새로운 알림을 실시간으로 받아볼 수 있습니다. 먼저 [브로드캐스트 알림 채널](/docs/12.x/notifications#broadcast-notifications) 관련 문서를 확인하고 설정을 마치세요.

브로드캐스트 채널을 사용하도록 알림을 구성했다면, Echo의 `notification` 메서드로 해당 알림을 수신할 수 있습니다. 이때 채널 이름은 알림을 받는 엔티티의 클래스명 규약과 일치해야 합니다.

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

이 예시에서는 `App\Models\User` 인스턴스에 대해 `broadcast` 채널로 전송된 모든 알림이 콜백에서 수신됩니다. `App.Models.User.{id}` 채널에 대한 인증 콜백은 애플리케이션의 `routes/channels.php` 파일에 포함되어 있습니다.