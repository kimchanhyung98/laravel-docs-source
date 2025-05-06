# 에셋 번들링(Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트 및 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [JavaScript 작업하기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 작업하기](#working-with-stylesheets)
- [Blade 및 라우트와 작업하기](#working-with-blade-and-routes)
  - [정적 에셋 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 프리패칭](#asset-prefetching)
- [커스텀 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [CSP Nonce](#content-security-policy-csp-nonce)
  - [SRI(Subresource Integrity)](#subresource-integrity-sri)
  - [임의 속성 추가](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [Dev 서버 CORS(Cross-Origin Resource Sharing)](#cors)
  - [Dev 서버 URL 보정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고 프로덕션 용도로 코드를 번들링하는 현대적 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때 일반적으로 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 번들링 및 프로덕션용으로 빌드합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 Vite와의 연동을 간편하게 지원합니다. 이를 통해 개발 및 프로덕션 모두에서 에셋을 쉽게 불러올 수 있습니다.

> [!NOTE]
> Laravel Mix를 사용 중인가요? Vite는 최근 Laravel 설치에서 Laravel Mix를 대체했습니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 사이트에서 확인하세요. Vite로 전환하려면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택

Vite로 전환하기 전까지만 해도, 새로운 Laravel 애플리케이션은 에셋 번들링을 위해 [Mix](https://laravel-mix.com/)([webpack](https://webpack.js.org/) 기반)를 사용했습니다. Vite는 풍부한 JavaScript 애플리케이션 개발 시 더욱 빠르고 생산적인 경험을 제공합니다. [Inertia](https://inertiajs.com) 등 도구로 SPA를 개발한다면 Vite가 완벽하게 어울립니다.

Vite는 [Livewire](https://livewire.laravel.com)와 같이 서버 사이드 렌더링 기반 전통적인 애플리케이션에도 잘 작동합니다. 다만, JavaScript에서 직접 참조하지 않는 임의의 에셋을 빌드 내에 복사하는 기능 등 Laravel Mix가 제공하는 일부 기능은 지원하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 다시 이전하기

Vite 스캐폴딩으로 Laravel 프로젝트를 시작했지만 다시 Laravel Mix와 webpack으로 이전해야 할 필요가 있나요? 문제 없습니다. [Vite에서 Mix로 이전하는 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치 및 설정하는 방법을 안내합니다. 하지만 Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 이미 모든 스캐폴딩을 포함하고 있어, Laravel 및 Vite 시작에 가장 빠른 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하려면 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다.

```shell
node -v
npm -v
```

[Node 공식 웹사이트](https://nodejs.org/en/download/)에서 최신 Node와 NPM을 간단한 GUI 설치 프로그램으로 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용하는 경우 Sail을 통해 Node와 NPM을 실행할 수 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새로운 Laravel 설치에서, 루트 디렉터리에 `package.json` 파일이 있습니다. 이 파일에는 이미 Vite 및 Laravel 플러그인을 시작하는 데 필요한 설정이 포함되어 있습니다. NPM을 통해 프론트엔드 의존성을 설치하세요.

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일로 설정합니다. 필요에 따라 이 파일을 자유롭게 수정하거나, `@vitejs/plugin-vue`, `@vitejs/plugin-react` 등 추가 플러그인을 설치해 사용할 수 있습니다.

Laravel Vite 플러그인에서 애플리케이션의 엔트리 포인트(진입점) 파일을 지정해야 합니다. 이 파일들은 JS, CSS 또는 TypeScript, JSX, TSX, Sass와 같은 전처리 언어일 수 있습니다.

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

SPA(특히 Inertia 기반 앱 등)를 빌드한다면 CSS 엔트리 포인트 없이 Vite를 사용하는 것이 가장 좋습니다.

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

대신, JavaScript 파일 내부에서 CSS를 import하여 사용해야 합니다. 보통 `resources/js/app.js` 파일에서 아래와 같이 import합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 진입점 및 [SSR 진입점](#ssr)과 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버로 작업하기

로컬 개발 웹 서버가 HTTPS로 애플리케이션을 제공한다면, Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)로 사이트를 보안 처리했거나, [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령](/docs/{{version}}/valet#securing-sites)을 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지하여 사용합니다.

만일 사이트를 앱 디렉토리명과 다른 호스트명으로 보안 처리했을 경우에는, `vite.config.js`에 직접 호스트명을 지정할 수 있습니다.

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

다른 웹 서버를 사용할 경우, 신뢰할 수 있는 인증서를 직접 생성하여 아래와 같이 Vite에 설정해야 합니다.

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

신뢰할 수 있는 인증서 생성을 할 수 없다면 [`@vitejs/plugin-basic-ssl`](https://github.com/vitejs/vite-plugin-basic-ssl) 플러그인을 설치/설정할 수 있습니다. 신뢰할 수 없는 인증서를 사용할 때는 브라우저에서 Vite 개발 서버의 인증서 경고를 수동으로 ‘Local’ 링크를 통해 허용해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행하기

[Sail](/docs/{{version}}/sail)에서 WSL2(Windows Subsystem for Linux 2) 환경에서 Vite를 실행할 때는 브라우저와의 통신을 위해 아래 설정을 `vite.config.js`에 추가해야 합니다.

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

파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 추가로 설정해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 불러오기

엔트리 포인트가 준비되면, 앱의 최상위 템플릿 `<head>`에 `@vite()` Blade 디렉티브를 추가해 불러올 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript에서 CSS를 import하는 경우에는 JS 엔트리 포인트만 추가하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동 감지하여 Hot Module Replacement를 위한 Vite 클라이언트를 inject합니다. 빌드 모드에서는 컴파일된 버전 에셋(CSS 포함)을 로드합니다.

필요한 경우, `@vite` 호출 시 빌드 에셋 경로도 지정할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- 주어진 빌드 경로는 public 경로에 상대적입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋

가끔 에셋의 URL 링크가 아니라 실제 내용을 페이지에 직접 포함해야 할 때가 있습니다. 예를 들어, PDF 생성기 등에 HTML 콘텐츠를 넘길 때가 그러합니다. 이럴 때는 `Vite` 파사드의 `content` 메서드를 사용할 수 있습니다.

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

Vite를 실행하는 방식은 두 가지가 있습니다. 개발 중에는 `dev` 명령어로 개발 서버를 실행해 파일 변경 사항을 실시간으로 반영할 수 있습니다.

또한, `build` 명령어로 에셋을 버전 관리하고 번들링하여 프로덕션 배포용으로 준비할 수도 있습니다.

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션 배포용 빌드 및 에셋 버전 관리...
npm run build
```

[WSL2의 Sail 환경](/docs/{{version}}/sail)에서 개발 서버를 실행 중이라면, [별도 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 작업하기

<a name="aliases"></a>
### 별칭(Aliases)

Laravel 플러그인은 아래와 같은 공통 별칭을 기본 제공하여, 애플리케이션의 에셋을 편리하게 import할 수 있게 해줍니다.

```js
{
    '@' => '/resources/js'
}
```

별칭은 `vite.config.js`에서 직접 덮어쓸 수 있습니다.

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하려면 `@vitejs/plugin-vue` 플러그인을 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-vue
```

설치 후 아래와 같이 `vite.config.js`에 플러그인을 포함시킬 수 있습니다. Laravel과 Vue 플러그인 사용 시 몇 가지 추가 설정이 필요합니다.

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
                    // 싱글 파일 컴포넌트 내에서 에셋 URL을 재작성할 때,
                    // Laravel 웹 서버 대신 Vite 서버로 지정하려면 base를 null로 설정.
                    base: null,
                    // 절대 URL 파싱 및 처리 - false면 public 디렉터리 내의 에셋을 정상 참조
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 Laravel, Vue, Vite 설정이 이미 적용된 형태로 제공됩니다. 가장 빠른 시작 방법입니다.

<a name="react"></a>
### React

[React](https://reactjs.org/)로 프론트엔드를 개발한다면 `@vitejs/plugin-react` 플러그인을 설치합니다.

```shell
npm install --save-dev @vitejs/plugin-react
```

이제 아래와 같이 `vite.config.js`에 플러그인을 포함시켜 사용합니다.

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

JSX가 포함된 파일은 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 엔트리 포인트 역시 이에 맞게 수정해야 합니다(위 예시 참고).

또한, Blade에 기존 `@vite` 디렉티브와 함께 `@viteReactRefresh` 디렉티브도 추가해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite` 보다 먼저 호출해야 합니다.

> [!NOTE]
> Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 Laravel, React, Vite 설정이 이미 포함되어 있어 더욱 빠르게 시작할 수 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 로딩을 도와주는 `resolvePageComponent` 헬퍼를 제공합니다. 아래는 Vue 3 기준 사용 예시지만, React 등 다른 프레임워크에서도 응용할 수 있습니다.

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

Vite 코드 스플리팅 기능과 Inertia를 함께 사용할 경우, [에셋 프리패칭](#asset-prefetching) 설정을 권장합니다.

> [!NOTE]
> Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 Laravel, Inertia, Vite 설정이 모두 준비되어 있습니다.

<a name="url-processing"></a>
### URL 처리

Vite를 사용할 때, HTML/CSS/JS 내에서 에셋을 참조하는 경우 몇 가지 주의할 점이 있습니다.  
먼저, 절대 경로(`/image.png`)로 에셋을 참조하는 경우 Vite가 해당 에셋을 빌드에 포함하지 않으므로 반드시 public 디렉터리 내에 에셋이 있어야 합니다. 특히 [CSS 전용 엔트리 포인트](#configuring-vite) 사용 시 절대 경로를 피해야 하며, 개발 중에는 브라우저가 public 디렉터리 대신 Vite 서버에서 해당 경로를 찾으려 하기 때문입니다.

반면, 상대 경로로 에셋을 참조하면 참조 파일 기준으로 경로가 해석되어 Vite가 경로를 재작성하고, 버전 및 번들링까지 처리합니다.

예를 들어, 다음과 같은 프로젝트 구조가 있을 때:
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

아래 예시는 Vite가 상대/절대 경로를 어떻게 처리하는지 보여줍니다.
```html
<!-- Vite가 처리하지 않으며 빌드에 포함되지 않음 -->
<img src="/taylor.png">

<!-- Vite가 경로를 재작성하고, 버전 관리하며 번들링 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업하기

> [!NOTE]
> Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 Tailwind 및 Vite가 이미 설정되어 있습니다. 혹은, 별도로 Tailwind만 이용할 경우 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 애플리케이션에는 이미 Tailwind 및 올바르게 구성된 `vite.config.js`가 포함되어 있습니다. 그러니 Vite 개발 서버 또는 `dev` Composer 명령어만 실행하면 Laravel과 Vite 모두 서버가 구동됩니다.

```shell
composer run dev
```

애플리케이션의 CSS는 보통 `resources/css/app.css`에 작성합니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와 작업하기

<a name="blade-processing-static-assets"></a>
### 정적 에셋을 Vite로 처리

JS 또는 CSS 내에서 에셋을 참조하면 Vite가 자동으로 처리 및 버전 관리합니다.  
하지만 Blade 템플릿에서만 참조되는 정적 에셋도 Vite가 처리 및 버전 관리를 할 수 있습니다.

이를 위해서는 해당 정적 에셋을 애플리케이션 엔트리 포인트에서 import 하여 Vite에 인식시켜야 합니다.  
예를 들어, `resources/images`의 모든 이미지, `resources/fonts`의 모든 폰트를 처리하려면 엔트리 포인트(예: `resources/js/app.js`)에 아래 코드를 추가합니다.

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이렇게 하면 `npm run build` 시 Vite가 해당 에셋도 처리합니다. Blade 템플릿에서는 `Vite::asset` 메서드로 버전이 반영된 URL을 가져올 수 있습니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade 기반으로 서버 사이드 렌더링을 하는 경우, Vite는 뷰 파일이 변경될 때 브라우저를 자동 새로고침하여 개발 경험을 개선할 수 있습니다. `refresh` 옵션을 `true`로 지정하면 아래와 같이 동작합니다.

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

`refresh: true`일 때, 아래 디렉터리의 파일 저장 시 `npm run dev` 상태에서 브라우저를 전체 새로고침합니다.

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 감시는 [Ziggy](https://github.com/tighten/ziggy) 사용 시 라우트 링크 변경 감지에 유용합니다.

만약 기본 경로가 맞지 않다면, 직접 감시할 경로를 지정할 수도 있습니다.

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

내부적으로 Laravel Vite 플러그인은 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하는데, 동작을 더 세밀하게 제어하려면 아래와 같이 `config` 정의를 넘길 수 있습니다.

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

JavaScript 애플리케이션에서 [별칭](#aliases)을 만들어 자주 참조하는 디렉터리를 관리하는 것은 일반적인 일입니다. Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용해 별칭을 만들 수 있습니다.  
보통 "매크로"는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 정의합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

정의한 매크로는 블레이드 템플릿에서 아래와 같이 사용할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## 에셋 프리패칭(Asset Prefetching)

Vite의 코드 스플리팅으로 SPA를 빌드할 때, 각 페이지 이동 시 필요한 에셋이 동적으로 요청됩니다. 이로 인해 UI 렌더링이 지연될 수 있는데, Laravel은 초기 페이지 로드 때 JS/CSS 에셋을 미리 프리패치(predictive load) 할 수 있게 지원합니다.

서비스 프로바이더의 `boot` 메서드에서 `Vite::prefetch`를 호출해 프리패치 기능을 활성화합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

위 코드에선 한 번에 최대 3개의 에셋을 프리패칭합니다.  
concurrency 값을 조정하거나 전체 에셋을 한 번에 다운로드하려면 아래처럼 호출하면 됩니다.

```php
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 [page _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) 발생 시 프리패칭이 시작됩니다. 프리패칭 시작 타이밍을 변경하고 싶다면 이벤트명을 지정할 수 있습니다.

```php
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

이렇게 하면, JavaScript에서 명시적으로 `vite:prefetch` 이벤트를 디스패치해야 프리패칭이 시작됩니다. 예를 들어, 페이지 로드 3초 후 프리패칭을 시작하고 싶다면:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 Base URL

Vite에서 빌드된 에셋을 CDN 등 별도의 도메인에 배포하는 경우, 애플리케이션의 `.env` 파일에 `ASSET_URL`을 지정해야 합니다.

```env
ASSET_URL=https://cdn.example.com
```

이렇게 설정하면 에셋의 모든 재작성된 URL 앞에 지정한 값이 붙습니다.

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite가 재작성하지 않으므로](#url-processing), 이 경우 접두사가 붙지 않습니다.

<a name="environment-variables"></a>
## 환경 변수

애플리케이션의 `.env` 파일에서 변수명 앞에 `VITE_`를 붙이면 그 값을 자바스크립트 코드 안에서 사용할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

자바스크립트에서는 아래와 같이 변수에 접근할 수 있습니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화

Laravel의 Vite 통합 기능은 테스트 실행 시에도 에셋을 해석하려 시도하며, 이를 위해 개발 서버 실행 또는 빌드가 필요합니다.

테스트 중에 Vite를 mock하고 싶다면, Laravel의 `TestCase` 클래스를 상속받는 테스트에서 `withoutVite` 메서드를 사용할 수 있습니다.

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

모든 테스트 실행 시 Vite 비활성화를 원하면, base `TestCase` 클래스의 `setUp` 메서드에서 호출하십시오.

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

Laravel Vite 플러그인을 사용하면 Vite로 SSR(Server-Side Rendering) 환경을 손쉽게 구축할 수 있습니다.  
먼저 `resources/js/ssr.js`에 SSR 진입점 파일을 만들고, 아래처럼 Laravel 플러그인에 옵션을 전달합니다.

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

SSR 빌드 누락 방지를 위해 `package.json`의 "build" 스크립트 역시 아래처럼 확장하는 것을 권장합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이제 SSR 서버 빌드 및 실행은 아래 명령어로 진행합니다.

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia와 SSR](https://inertiajs.com/server-side-rendering)을 사용할 경우 `inertia:start-ssr` artisan 명령어로 SSR 서버를 시작할 수 있습니다.

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [시작 키트](/docs/{{version}}/starter-kits)는 Inertia SSR 및 Vite 설정도 모두 준비되어 있습니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### CSP(콘텐츠 보안 정책) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로 script, style 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하려면, 커스텀 [미들웨어](/docs/{{version}}/middleware)에서 `useCspNonce` 메서드를 사용할 수 있습니다.

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

`useCspNonce` 실행 후에는, Laravel이 모든 script/style 태그에 자동으로 nonce 속성을 추가합니다.

[Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등 다른 곳에서 nonce가 필요하면 `cspNonce` 메서드로 값을 가져올 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

이미 가진 nonce 값을 Laravel에 전달하고 싶다면, 아래처럼 지정합니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### SRI(Subresource Integrity)

Vite 매니페스트에 `integrity` 해시가 포함되어 있다면, Laravel은 생성된 script/style 태그에 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) 강제를 위해 자동으로 해당 속성을 추가합니다.  
Vite는 기본적으로 `integrity` 해시를 포함하지 않지만, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인 설치로 가능해집니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

설치 후 `vite.config.js`에서 플러그인을 활성화합니다.

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

필요하다면 해시가 위치할 매니페스트 키도 커스터마이즈할 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지 비활성화는 아래와 같이 할 수 있습니다.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의(Arbitrary) 속성

script/style 태그에 추가적인 속성(e.g. [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change))이 필요하다면, `useScriptTagAttributes`, `useStyleTagAttributes` 메서드로 지정할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값 지정
    'async' => true, // 값없는 속성 지정
    'integrity' => false, // 기존 속성 제거
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부로 속성을 추가하려면, 콜백을 넘겨 asset 경로, URL, 매니페스트 청크, 전체 매니페스트를 활용할 수도 있습니다.

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
> Vite 개발 서버가 동작 중일 때는 `$chunk`, `$manifest` 인자가 `null`이 됩니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

Laravel의 Vite 플러그인은 기본 설정만으로 대부분의 애플리케이션에서 곧바로 사용 가능합니다.  
하지만 특정 상황에서는 Vite 동작을 세밀하게 조정할 필요가 있습니다.  
`@vite` Blade 디렉티브 대신 사용할 수 있는 다양한 메서드와 옵션 예시는 아래와 같습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 지정
            ->useBuildDirectory('bundle') // 빌드 디렉터리 지정
            ->useManifestFilename('assets.json') // 매니페스트 파일명 지정
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 에셋 URL 생성 커스터마이징
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

동일한 설정을 `vite.config.js`에서 아래와 같이 지정합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 지정
            buildDirectory: 'bundle', // 빌드 디렉터리 지정
            input: ['resources/js/app.js'], // 엔트리 포인트 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 지정
    },
});
```

<a name="cors"></a>
### Dev 서버 CORS(Cross-Origin Resource Sharing)

Vite dev 서버의 에셋을 브라우저에서 불러올 때 CORS 문제가 발생한다면, 커스텀 origin에 대한 접근 권한을 dev 서버에 부여해야 합니다.  
Laravel 플러그인과 함께 사용하는 경우, 아래의 origin들은 별도 설정 없이 허용됩니다.

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env`의 `APP_URL`

커스텀 origin 허용의 가장 쉬운 방법은 `.env`의 `APP_URL` 값을 브라우저에서 접속하는 origin과 일치시키는 것입니다.  
예를 들어 `https://my-app.laravel`로 접근한다면, 다음처럼 `.env`를 수정하세요.

```env
APP_URL=https://my-app.laravel
```

더 세밀한 origin 제어(여러 origin 지원 등)가 필요하다면, [Vite의 CORS server 옵션](https://vite.dev/config/server-options.html#server-cors)을 활용하세요.  
예시는 아래와 같습니다.

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

정규식 패턴도 사용할 수 있어, 예를 들어 `*.laravel`과 같은 도메인을 전체 허용할 수 있습니다.

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
                // 지원: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### Dev 서버 URL 보정

Vite 생태계의 일부 플러그인은 슬래시(`/`)로 시작하는 URL이 항상 Vite dev 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합에서는 그렇지 않으므로 주의해야 합니다.

예를 들어, `vite-imagetools` 플러그인은 개발 서버에서 아래와 같은 URL을 생성합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

이런 경우, 해당 URL이 Vite 서버로 연결되도록 사용자 코드에서 별도 처리해야 합니다. 아래처럼 `vite.config.js`의 `transformOnServe` 옵션으로 처리할 수 있습니다.

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

이제 Vite가 에셋을 서비스하는 동안 아래처럼 dev 서버를 가리키는 URL이 생성됩니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
