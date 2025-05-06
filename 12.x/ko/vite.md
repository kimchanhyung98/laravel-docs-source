# 에셋 번들링(Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트 & 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [자바스크립트 다루기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade 및 라우트 다루기](#working-with-blade-and-routes)
  - [Vite로 정적 자산 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 프리패칭](#asset-prefetching)
- [커스텀 베이스 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [하위 리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 사용자화](#advanced-customization)
  - [개발 서버 CORS](#cors)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 코드를 프로덕션용으로 번들링해주는 최신 프론트엔드 빌드 도구입니다. Laravel 애플리케이션을 빌드할 때는 Vite를 사용해 CSS, 자바스크립트 파일을 프로덕션용 에셋으로 번들링하는 것이 일반적입니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 Vite와 원활하게 통합하며, 개발 및 프로덕션 환경 모두에서 에셋을 로드할 수 있습니다.

> [!NOTE]
> Laravel Mix를 사용하고 계신가요? Vite는 새 Laravel 설치에서 Mix를 대체합니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 사이트에서 확인하세요. Vite로 전환하려면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택

과거의 신규 Laravel 애플리케이션은 에셋 번들링을 위해 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 더욱 빠르고 생산적인 풍부한 자바스크립트 애플리케이션 개발 경험을 제공합니다. [Inertia](https://inertiajs.com) 등과 같은 도구로 SPA(Single Page Application)를 개발한다면 Vite가 최상의 선택지입니다.

Vite는 [Livewire](https://livewire.laravel.com)처럼 서버 사이드 렌더링에 JS "스프링클"을 사용하는 전통적인 앱과도 잘 동작합니다. 하지만 Mix가 지원했던 임의의 에셋 복사 등 일부 기능은 제공하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 되돌아가기

Vite 스캐폴딩으로 새 Laravel 앱을 시작했지만 다시 Laravel Mix와 webpack을 사용하고 싶으신가요? 문제 없습니다. [공식 마이그레이션 안내서](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치 및 설정하는 방법을 안내합니다. 하지만 Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 이 모든 스캐폴딩이 포함되어 있어, 가장 빠르게 Laravel과 Vite를 시작할 수 있습니다.

<a name="installing-node"></a>
### Node 설치

Vite 및 Laravel 플러그인을 실행하려면 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다:

```shell
node -v
npm -v
```

[공식 Node.js 웹사이트](https://nodejs.org/en/download/)에서 간단한 그래픽 설치기를 통해 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용할 경우, Sail을 통해 Node 및 NPM을 실행할 수 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새로 설치한 Laravel 프로젝트의 루트에는 `package.json` 파일이 있습니다. 기본 `package.json`에는 Vite 및 Laravel 플러그인을 시작하는 데 필요한 모든 항목이 포함되어 있습니다. NPM을 통해 프론트엔드 의존성을 설치하세요:

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일로 설정합니다. 필요에 따라 이 파일을 자유롭게 수정할 수 있으며, `@vitejs/plugin-vue`, `@vitejs/plugin-react` 등 다른 플러그인도 추가로 설치 가능합니다.

Laravel Vite 플러그인에서는 앱의 엔트리 포인트를 지정해야 합니다. 이 파일들은 자바스크립트, CSS 파일 또는 TypeScript, JSX, TSX, Sass 등 전처리 언어도 포함됩니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```

Inertia 등으로 SPA를 작성 중이라면 CSS 엔트리 포인트 없이 사용하는 것이 좋습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

대신, JavaScript에서 CSS를 import해야 합니다. 일반적으로 앱의 `resources/js/app.js` 파일에서 아래와 같이 import합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 엔트리 포인트 및 [SSR 엔트리포인트](#ssr)와 같은 고급 구성도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### SSL을 사용하는 개발 서버와 함께 사용

로컬 개발 웹서버가 HTTPS로 앱을 제공하는 경우, Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)로 사이트를 보안 적용하거나 [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지하여 사용합니다.

앱 디렉토리와 다른 호스트명으로 보안을 적용했다면, `vite.config.js`에서 호스트를 직접 지정하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            detectTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

다른 웹서버를 사용할 때는 신뢰할 수 있는 인증서를 생성해 Vite가 해당 인증서를 사용하도록 직접 지정해야 합니다:

```js
// ...
import fs from 'fs'; // [tl! add]

const host = 'my-app.test'; // [tl! add]

export default defineConfig({
    // ...
    server: { // [tl! add]
        host, // [tl! add]
        hmr: { host }, // [tl! add]
        https: { // [tl! add]
            key: fs.readFileSync(`/path/to/${host}.key`), // [tl! add]
            cert: fs.readFileSync(`/path/to/${host}.crt`), // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

시스템에서 신뢰할 수 있는 인증서를 생성할 수 없다면 [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치 및 설정하세요. 신뢰할 수 없는 인증서를 사용하는 경우, 브라우저에서 `npm run dev`로 실행된 Vite 개발 서버의 "Local" 링크를 클릭해 경고를 승인하셔야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행 시 설정

Windows의 WSL2에서 [Laravel Sail](/docs/{{version}}/sail)로 Vite 개발 서버를 실행할 경우, 브라우저와 개발 서버 간 통신을 위해 아래 설정을 `vite.config.js`에 추가하세요:

```js
// ...

export default defineConfig({
    // ...
    server: { // [tl! add:start]
        hmr: {
            host: 'localhost',
        },
    }, // [tl! add:end]
});
```

개발 서버 실행 중 파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 추가 설정이 필요할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 & 스타일 불러오기

Vite 엔트리포인트를 설정했다면, 애플리케이션 루트 템플릿의 `<head>` 부분에 `@vite()` Blade 디렉티브로 불러올 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JS에서 CSS를 import하는 경우에는 JS 엔트리포인트만 지정하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지하여 HMR(Hot Module Replacement)이 가능한 Vite 클라이언트를 주입합니다. 빌드 모드에서는 컴파일 및 버전 관리된 에셋과 import된 CSS까지 로드합니다.

필요하다면 `@vite` 디렉티브에 빌드 에셋의 경로를 지정할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- Build 경로는 public 경로 기준 상대경로로 지정하세요. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋

특정 상황에서는 에셋의 URL을 링크하는 대신 직접 페이지에 원본 컨텐츠를 포함해야 할 때가 있습니다. 예를 들어, PDF 생성기 등에 HTML 컨텐츠를 넘길 때가 그렇습니다. `Vite` 파사드의 `content` 메소드를 이용해 Vite 에셋의 컨텐츠를 바로 출력할 수 있습니다:

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    <style>
        {!! Vite::content('resources/css/app.css') !!}
    </style>
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
## Vite 실행하기

Vite를 실행하는 방법은 두 가지입니다. `dev` 명령을 통해 개발 서버를 실행하면, 파일 변경 사항이 브라우저에 즉시 반영됩니다.

`build` 명령을 실행하면 애플리케이션 에셋을 버전 관리하고 번들링해 프로덕션 배포에 적합한 상태로 만듭니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션 빌드 및 에셋 버전 관리...
npm run build
```

[WSL2에서 Sail](docs/{{version}}/sail)로 개발 서버를 실행 중이라면 [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## 자바스크립트 다루기

<a name="aliases"></a>
### 별칭(Aliases)

기본적으로 Laravel 플러그인은 애플리케이션의 에셋들을 더 쉽게 import할 수 있도록 `'@'` 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`'@'` 별칭을 직접 덮어쓸 경우, `vite.config.js`에서 별칭을 정의할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': '/resources/ts',
        },
    },
});
```

<a name="vue"></a>
### Vue

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 빌드하고자 할 경우, `@vitejs/plugin-vue` 플러그인도 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-vue
```

설치 후, `vite.config.js`에서 플러그인을 포함시키세요. Laravel과 함께 Vue 플러그인을 사용할 때는 추가 옵션 설정이 필요합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
        vue({
            template: {
                transformAssetUrls: {
                    // SFC에서 참조되는 에셋 URL은 기본적으로 Laravel 웹서버로
                    // 리라이팅됩니다. `null`로 지정하면 Vite 서버로 리라이팅됩니다.
                    base: null,

                    // 절대경로 URL은 기본적으로 파일 시스템 경로로 인식됩니다.
                    // false로 지정하면 public 디렉토리 내 에셋의 직접 참조가 가능합니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 Laravel/Vue/Vite에 맞는 모든 환경 설정이 이미 적용되어 있습니다. 스타터킷을 활용하면 가장 빨리 시작할 수 있습니다.

<a name="react"></a>
### React

[React](https://reactjs.org/)로 프론트엔드를 개발하려면, `@vitejs/plugin-react` 플러그인 설치가 필요합니다:

```shell
npm install --save-dev @vitejs/plugin-react
```

`vite.config.js`에 플러그인을 추가하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.jsx']),
        react(),
    ],
});
```

JSX 코드를 포함하는 파일은 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 필요하다면 엔트리 포인트도 [위와 같이](#configuring-vite) 업데이트해야 합니다.

또한, 기존 `@vite` 디렉티브 옆에 추가로 `@viteReactRefresh` Blade 디렉티브를 넣어야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출해야 합니다.

> [!NOTE]
> Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 Laravel/React/Vite에 맞는 모든 설정이 이미 적용되어 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 로드를 도와주는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 사용 예시이며, React 등 다른 프레임워크와도 사용 가능합니다:

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

Vite의 코드 분할(Codesplitting) 기능을 Inertia와 함께 사용할 경우, [에셋 프리패칭](#asset-prefetching)을 추가로 설정하는 것이 좋습니다.

> [!NOTE]
> Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 Inertia/Vite에 최적화된 설정이 이미 포함되어 있습니다.

<a name="url-processing"></a>
### URL 처리

Vite를 사용해 앱의 HTML, CSS, JS에서 에셋을 참조할 때는 몇 가지 유의사항이 있습니다. 첫째, 에셋을 절대경로로 참조하면 Vite는 해당 에셋을 빌드에 포함하지 않습니다. 따라서 그런 파일은 public 디렉토리에 실제로 존재해야 합니다. [CSS 전용 엔트리포인트](#configuring-vite) 사용 시에는 절대경로를 피하세요. 개발 중 브라우저가 CSS를 Vite 개발 서버에서 불러오려 하게 되어 public 디렉토리가 아닌 곳을 찾게 됩니다.

상대경로로 참조한 에셋은 참조되는 파일을 기준으로 경로가 계산됩니다. 상대경로 에셋들은 Vite가 자동으로 리라이팅, 버전관리, 번들링합니다.

예시 프로젝트 구조:

```text
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

Vite의 상대·절대 URL 처리 예시:

```html
<!-- Vite가 처리하지 않으며 빌드에 포함되지 않는 에셋 -->
<img src="/taylor.png">

<!-- Vite가 리라이팅하고 번들링하며, 버전 관리하는 에셋 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기

> [!NOTE]
> Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 Tailwind 및 Vite 기본 설정이 포함되어 있습니다. 스타터킷 없이 Tailwind와 Laravel을 사용하려면 [Tailwind의 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 앱에는 Tailwind와 올바른 `vite.config.js`가 이미 포함되어 있습니다. Vite 개발 서버를 시작하거나 Composer의 `dev` 명령을 실행하면 Laravel과 Vite 개발 서버가 함께 실행됩니다:

```shell
composer run dev
```

앱의 CSS 파일은 `resources/css/app.css`에 배치할 수 있습니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트 다루기

<a name="blade-processing-static-assets"></a>
### Vite로 정적 자산 처리하기

Javascript나 CSS에서 에셋을 참조하면 Vite가 이를 자동으로 처리(버전관리)합니다. 뿐만 아니라, Blade 기반 애플리케이션에서는 Blade 템플릿에서만 참조하는 정적 자산도 Preprocessing/버전관리가 가능합니다.

이를 위해 Vite에 해당 자산을 엔트리포인트에서 import해 알려야 합니다. 예를 들어, `resources/images` 내 이미지와 `resources/fonts`의 폰트 모두를 처리하려면 `resources/js/app.js`에 아래를 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이렇게 하면 `npm run build` 실행 시 Vite가 해당 자산들을 처리합니다. 이후 Blade 템플릿에서는 `Vite::asset` 메소드로 버전 관리된 URL을 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade 기반 서버 사이드 렌더링 앱에서 Vite는 View 파일 수정 시 브라우저를 자동 새로고침해 개발 워크플로우를 개선할 수 있습니다. 단순히 `refresh` 옵션을 `true`로 설정하면 됩니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: true,
        }),
    ],
});
```

`refresh`가 `true`면, 아래 디렉토리 내 파일을 저장할 때마다 `npm run dev`로 실행 중인 브라우저에서 전체 페이지 새로고침이 발생합니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 감시는 [Ziggy](https://github.com/tighten/ziggy)를 써서 프론트엔드에서 라우트 링크를 생성하는 경우 유용합니다.

기본 감시 경로를 변경하려면 직접 경로 목록을 지정할 수도 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: ['resources/views/**'],
        }),
    ],
});
```

내부적으로 Laravel Vite 플러그인은 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 고급 설정이 필요한 경우 아래와 같이 `config` 정의를 추가할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: [{
                paths: ['path/to/watch/**'],
                config: { delay: 300 }
            }],
        }),
    ],
});
```

<a name="blade-aliases"></a>
### 별칭(Aliases)

자바스크립트에서는 [별칭 생성](#aliases)을 자주 하듯, Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 통해 별칭을 만들 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메소드에서 정의합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

매크로를 정의하면 아래처럼 템플릿에서 호출해 사용할 수 있습니다. 예를 들어, 위 매크로로 `resources/images/logo.png`를 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## 에셋 프리패칭

Vite 코드 분할(Codesplitting) 기능을 사용하는 SPA를 개발할 때는 페이지 이동 시마다 필요한 자산을 동적으로 가져오게 되어 UI 렌더링이 느려질 수 있습니다. 이런 경우를 대비해, Laravel은 앱의 JavaScript/CSS 에셋을 초기 페이지 로드시 미리(fast fetch, eager prefetch) 가져올 수 있도록 지원합니다.

서비스 프로바이더의 `boot` 메서드에서 `Vite::prefetch` 메소드를 호출하여 프리패칭을 설정하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

위 예시에서는 최대 3개의 에셋을 동시에 prefetch합니다. 앱 환경에 따라 동시 다운로드 개수를 조정하거나, 모든 에셋을 한 번에 가져오도록 할 수도 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 prefetch는 [page _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) 발생시 시작됩니다. prefetch 시작 시점을 커스터마이즈하려면 Vite가 참조할 이벤트를 지정할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

이렇게 하면, 아래처럼 JS에서 직접 `vite:prefetch` 이벤트를 window에 디스패치하여 prefetch를 시작할 수 있습니다. 예를 들어, 페이지 로드 3초 후 prefetch를 시작:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 베이스 URL

Vite 빌드 에셋을 애플리케이션과 별도의 도메인(CDN 등)에 배포한다면, 앱 `.env` 파일에 `ASSET_URL` 환경변수를 지정하세요:

```env
ASSET_URL=https://cdn.example.com
```

설정 후에는 모든 에셋 URL이 해당 값이 접두사로 붙어 변환됩니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite가 변환하지 않으므로](#url-processing) 접두사가 붙지 않습니다.

<a name="environment-variables"></a>
## 환경 변수

앱의 `.env`에 `VITE_` 접두사를 붙인 변수로 자바스크립트로 환경 변수를 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

이렇게 주입된 변수는 `import.meta.env` 객체로 접근합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화

Laravel의 Vite 통합은 테스트 실행 시 에셋을 resolve하며, 이때 Vite 개발 서버를 실행하거나 에셋 빌드가 필요합니다.

테스트 동안 Vite를 모킹하려면, Laravel의 `TestCase`를 확장하는 테스트 내에서 `withoutVite` 메서드를 호출하세요:

```php tab=Pest
test('without vite example', function () {
    $this->withoutVite();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example(): void
    {
        $this->withoutVite();

        // ...
    }
}
```

모든 테스트에서 Vite를 비활성화하고 싶다면, `TestCase`의 `setUp` 메서드에서 호출하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
## 서버 사이드 렌더링(SSR)

Laravel Vite 플러그인은 Vite를 활용한 서버 사이드 렌더링(SSR)을 손쉽게 설정할 수 있게 해줍니다. 먼저 `resources/js/ssr.js`에 SSR 엔트리포인트 파일을 작성하고, 플러그인 설정에서 명시하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```

SSR 엔트리포인트 빌드를 빼먹지 않으려면, 앱의 `package.json`의 "build" 스크립트를 아래와 같이 확장하는 것도 추천합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이제 다음 명령으로 SSR 서버를 빌드·시작할 수 있습니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia로 SSR](https://inertiajs.com/server-side-rendering)을 사용할 경우, `inertia:start-ssr` 아티즌 명령을 사용하여 SSR 서버를 시작할 수 있습니다:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [스타터킷](/docs/{{version}}/starter-kits)에는 Inertia SSR 및 Vite 설정이 이미 포함되어 있습니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### Content Security Policy(CSP) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) 적용을 위해 스크립트/스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하려면, 사용자 정의 [미들웨어](/docs/{{version}}/middleware) 내에서 `useCspNonce`를 호출하세요:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Vite;
use Symfony\Component\HttpFoundation\Response;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```

`useCspNonce` 호출 시, Laravel은 생성되는 모든 스크립트/스타일 태그에 자동으로 nonce 속성을 포함해 줍니다.

다른 곳(예: [Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy), [스타터킷](/docs/{{version}}/starter-kits))에서 nonce를 지정하려면 `cspNonce` 메소드를 활용하세요:

```blade
@routes(nonce: Vite::cspNonce())
```

직접 nonce 값을 지정하려면, `useCspNonce`에 전달하면 됩니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 하위 리소스 무결성(Subresource Integrity, SRI)

Vite manifest에 에셋의 `integrity` 해시가 포함된 경우, Laravel은 스크립트/스타일 태그에 자동으로 `integrity` 속성을 추가하여 [하위 리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 강제합니다. 기본적으로 Vite는 manifest에 integrity 해시를 포함하지 않으나, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri)를 설치하면 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

플러그인을 `vite.config.js` 파일에 추가합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import manifestSRI from 'vite-plugin-manifest-sri';// [tl! add]

export default defineConfig({
    plugins: [
        laravel({
            // ...
        }),
        manifestSRI(),// [tl! add]
    ],
});
```

integrity 해시를 저장할 manifest 키를 커스터마이즈하려면 아래와 같이 지정합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

이 자동 감지기능을 완전히 비활성화하려면 아래와 같이 false를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성

스크립트 또는 스타일 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등 추가 속성이 필요하다면, `useScriptTagAttributes`, `useStyleTagAttributes`로 지정할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값 지정
    'async' => true, // 값 없이 속성만
    'integrity' => false, // 기본 동작 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부 속성 추가가 필요하다면, 콜백을 넘겨 에셋 경로, URL, manifest chunk, 전체 manifest를 파라미터로 받을 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> [!WARNING]
> `$chunk`와 `$manifest`는 Vite 개발 서버 작동 중에는 `null`입니다.

<a name="advanced-customization"></a>
## 고급 사용자화

기본적으로 Laravel Vite 플러그인은 대부분의 앱에 적합한 설정을 제공합니다. 그러나 가끔 Vite의 동작을 추가로 변경해야 할 수 있습니다. 아래 메소드 및 옵션을 사용하면 `@vite` Blade 디렉티브 대신 더 강력한 사용이 가능합니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 커스텀
            ->useBuildDirectory('bundle') // 빌드 디렉토리 커스텀
            ->useManifestFilename('assets.json') // manifest 파일명 커스텀
            ->withEntryPoints(['resources/js/app.js']) // 엔트리포인트 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋 경로 생성 방식을 사용자 정의
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

동일한 구성은 `vite.config.js`에도 명시해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 커스텀
            buildDirectory: 'bundle', // 빌드 디렉토리 커스텀
            input: ['resources/js/app.js'], // 엔트리포인트 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // manifest 파일명 커스텀
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS

브라우저가 Vite 개발 서버의 에셋을 가져올 때 CORS 오류가 발생한다면, 개발 서버에 접근하도록 커스텀 오리진을 허용해야 합니다. Laravel 플러그인과 함께 쓰는 Vite는 아래 오리진을 별다른 설정 없이 허용합니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트의 `.env`에 설정된 `APP_URL`

프로젝트의 커스텀 도메인을 허용하려면, `.env`의 `APP_URL`이 브라우저에서 접근하는 오리진과 일치하는지 확인하세요. 예를 들어 `https://my-app.laravel`로 접속한다면 아래처럼 설정합니다:

```env
APP_URL=https://my-app.laravel
```

여러 오리진을 세밀하게 제어하려면 [Vite의 내장 CORS 설정](https://vite.dev/config/server-options.html#server-cors)을 `vite.config.js`의 `server.cors.origin` 옵션에 배열로 지정하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [  // [tl! add]
                'https://backend.laravel',  // [tl! add]
                'http://admin.laravel:8566',  // [tl! add]
            ],  // [tl! add]
        },  // [tl! add]
    },  // [tl! add]
});
```

정규표현식 패턴도 지정할 수 있으므로, 예를 들어 `*.laravel` 전체 오리진을 허용할 수도 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [ // [tl! add]
                // 아래와 같이 SCHEME://DOMAIN.laravel[:PORT] 지원 [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정

Vite 생태계의 일부 플러그인에서는 슬래시(`/`)로 시작하는 URL이 반드시 Vite 개발 서버를 가리킨다고 가정하지만, Laravel 통합 환경에서는 그렇지 않을 수 있습니다.

예를 들어 `vite-imagetools` 플러그인은 에셋을 개발 서버에서 제공할 때 다음과 같은 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

이때 플러그인은 `/@imagetools`로 시작하는 URL을 Vite가 가로채 처리할 것으로 기대합니다. 이런 플러그인을 쓸 경우, 수동으로 URL을 수정해줄 필요가 있습니다. `vite.config.js`에서 `transformOnServe` 옵션을 활용해 해결할 수 있습니다.

아래처럼 모든 `/@imagetools`를 개발 서버 URL로 prepend하는 예시:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),
        }),
        imagetools(),
    ],
});
```

이제 Vite가 에셋을 제공할 때 아래처럼 개발 서버를 포함한 URL을 사용합니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
