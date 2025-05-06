# 에셋 번들링 (Vite)

- [소개](#introduction)
- [설치 & 설정](#installation)
  - [Node 설치하기](#installing-node)
  - [Vite와 Laravel 플러그인 설치하기](#installing-vite-and-laravel-plugin)
  - [Vite 설정하기](#configuring-vite)
  - [스크립트 및 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [자바스크립트 다루기](#working-with-scripts)
  - [별칭(Alias)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade 및 라우트와 함께 사용하기](#working-with-blade-and-routes)
  - [정적 에셋 Vite로 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [커스텀 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화하기](#disabling-vite-in-tests)
- [서버사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [임의의 속성 추가](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션 배포를 위한 코드 번들링을 지원하는 최신 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때 Vite를 사용해 애플리케이션의 CSS와 자바스크립트 파일을 프로덕션용 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 지시어를 제공하여 개발 및 배포 환경에서 에셋을 쉽게 불러올 수 있도록 Vite와 원활하게 통합됩니다.

> [!NOTE]  
> Laravel Mix를 사용하고 계신가요? 이제 신규 Laravel 프로젝트에서는 Vite가 Mix를 대체했습니다. Mix 관련 문서는 [Laravel Mix](https://laravel-mix.com/) 공식 웹사이트를 참조하세요. Vite로 전환하고자 한다면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

기존 Laravel 애플리케이션은 에셋 번들링에 [webpack](https://webpack.js.org/) 기반 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 빠르고 생산적인 풍부한 자바스크립트 앱 개발 경험을 제공합니다. [Inertia](https://inertiajs.com) 같은 도구로 SPA(Single Page Application)를 개발한다면 Vite가 적합합니다.

또한 전통적인 서버 사이드 렌더링 방식의 애플리케이션(예: [Livewire](https://livewire.laravel.com) 사용)에 자바스크립트 "스프링클"을 적용하는 경우에도 Vite가 잘 작동합니다. 단, JavaScript에서 직접 참조하지 않는 임의의 에셋을 빌드 과정에 복사하는 기능 등 Mix가 제공하는 일부 기능은 Vite에서 지원하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 다시 마이그레이션하기

Vite 스캐폴딩을 이용해 새 Laravel 프로젝트를 시작했지만 다시 Laravel Mix 및 webpack으로 이전해야 한다면, [Vite에서 Mix로 마이그레이션하는 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 & 설정

> [!NOTE]  
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 구성하는 방법을 소개합니다. 하지만 Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 이 모든 설정이 포함되어 있어 가장 빠르게 Laravel과 Vite를 시작할 수 있습니다.

<a name="installing-node"></a>
### Node 설치하기

Vite와 Laravel 플러그인을 실행하기 전에 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

최신 버전의 Node와 NPM은 [공식 Node 웹사이트](https://nodejs.org/en/download/)의 그래픽 설치 프로그램으로 간단히 설치할 수 있습니다. [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용할 경우 Sail을 통해 Node와 NPM을 사용할 수도 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치하기

Laravel를 새로 설치했다면, 애플리케이션 루트 디렉터리에 `package.json` 파일이 있으며 기본적으로 Vite와 Laravel 플러그인을 사용할 준비가 되어 있습니다. NPM으로 프론트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 설정하기

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 이 파일을 자유롭게 수정할 수 있습니다. 예를 들어, `@vitejs/plugin-vue` 또는 `@vitejs/plugin-react` 등의 다른 플러그인도 추가할 수 있습니다.

Laravel Vite 플러그인에서는 JavaScript 또는 CSS, 그리고 TypeScript, JSX, TSX, Sass와 같은 전처리 언어 파일 등 애플리케이션의 엔트리 포인트를 명시해야 합니다.

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

SPA(싱글 페이지 애플리케이션, 예: Inertia) 빌드를 할 때는 CSS 엔트리 포인트 없이 사용하는 것이 더 적합합니다:

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

대신 자바스크립트에서 CSS를 임포트해야 합니다. 보통 `resources/js/app.js`에서 아래처럼 처리합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 [SSR 엔트리 포인트](#ssr) 등 다중 엔트리 포인트와 고급 옵션도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버와 함께 사용하기

로컬 개발 웹서버가 HTTPS로 애플리케이션을 제공한다면 Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)로 사이트를 보안 처리했거나, [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 인식하여 사용합니다.

만약 호스트명이 앱 경로 이름과 다르다면, 애플리케이션의 `vite.config.js`에서 호스트를 직접 지정해야 합니다:

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

다른 웹 서버를 사용할 경우, 신뢰할 수 있는 인증서를 생성한 후, Vite에 직접 인증서 경로를 지정하세요:

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

시스템에서 신뢰할 수 있는 인증서를 생성할 수 없다면 [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치·설정할 수 있습니다. 신뢰되지 않은 인증서를 사용할 경우, 브라우저가 Vite의 개발 서버 인증서 경고를 표시하면, `npm run dev` 명령 실행 후 콘솔에 표시된 "Local" 링크를 따라가서 경고를 수동으로 승인해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행하기

[Laravel Sail](/docs/{{version}}/sail)을 Windows Subsystem for Linux 2(WSL2)에서 사용할 경우, 브라우저와 개발 서버가 통신할 수 있도록 `vite.config.js`에 아래 설정을 추가하세요:

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

개발 서버 실행 중 파일 변경이 브라우저에 반영되지 않는다면, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch)을 추가로 설정해야 할 수도 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 불러오기

Vite 엔트리 포인트를 설정한 후, 애플리케이션 루트 템플릿의 `<head>`에 `@vite()` Blade 지시어로 불러올 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

자바스크립트에서 CSS를 임포트하는 경우에는 자바스크립트 엔트리 포인트만 지정하면 됩니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 지시어는 개발 서버 실행 중 자동으로 Vite 클라이언트를 주입해 핫 모듈 리플레이스먼트를 활성화합니다. 빌드 모드에서는 컴파일된 버전 에셋(임포트된 CSS 포함)을 자동으로 불러옵니다.

필요하다면 `@vite` 호출 시 빌드된 에셋의 빌드 경로도 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋

에셋의 버전 URL 대신, 에셋의 원본 내용을 직접 페이지에 포함해야 하는 경우가 있습니다.(예: PDF 생성 시 HTML 내 에셋 직접 삽입 등) `Vite` 파사드의 `content` 메서드로 Vite 에셋의 내용을 출력할 수 있습니다:

```blade
@php
use Illuminate\Support\Facades\Vite;
@endphp

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

Vite를 실행하는 방법은 두 가지입니다. 개발 중에는 `dev` 명령어를 사용해 개발 서버를 실행하면, 파일 변경을 감지해 바로 브라우저에 반영됩니다.

또는 `build` 명령어로 애플리케이션 에셋을 번들링 및 버전 관리하여 배포 준비를 할 수 있습니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 관리...
npm run build
```

[WSL2의 Sail](/docs/{{version}}/sail) 환경에서 개발 서버를 실행하는 경우, [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## 자바스크립트 다루기

<a name="aliases"></a>
### 별칭(Alias)

기본적으로, Laravel 플러그인은 코드에서 자주 사용하는 경로에 쉽게 접근할 수 있도록 공통 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`'@'` 별칭을 자신의 필요에 맞게 `vite.config.js`에 덮어쓸 수 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 구축하려면, `@vitejs/plugin-vue` 플러그인을 추가 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

이후 `vite.config.js`에 아래처럼 플러그인을 포함시킵니다. Laravel과 함께 사용할 때는 몇 가지 추가 옵션이 필요합니다:

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
                    // Vue 플러그인은 싱글 파일 컴포넌트 내 에셋 URL을 Laravel 웹서버용으로 재작성합니다.
                    // base를 null로 설정하면, 대신 Vite 서버를 참조합니다.
                    base: null,

                    // 절대경로 URL 파싱 시, 기본값(false)으로 하면 public 디렉터리 에셋 참조가 정상 동작합니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, Vue, Vite 설정이 포함되어 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 Laravel, Vue, Vite를 가장 빠르게 시작할 수 있습니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크로 프론트엔드를 구축하려면, `@vitejs/plugin-react` 플러그인을 추가 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-react
```

그리고 `vite.config.js`에 플러그인을 포함합니다:

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

JSX가 포함된 파일은 확장자가 `.jsx` 또는 `.tsx` 여야 하며, 필요하다면 엔트리 포인트도 위 예시처럼 변경해야 합니다.

또한, 기존 `@vite` Blade 지시어와 함께 `@viteReactRefresh` 지시어도 추가해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출해야 합니다.

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, React, Vite 설정이 포함되어 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 Laravel, React, Vite를 가장 빠르게 시작할 수 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 쉽게 로드할 수 있는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서의 사용 예시이며, React 등 다른 프레임워크에서도 사용할 수 있습니다:

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    return createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 적절한 Laravel, Inertia, Vite 설정이 이미 포함되어 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 Laravel, Inertia, Vite를 가장 빠르게 시작할 수 있습니다.

<a name="url-processing"></a>
### URL 처리

Vite를 사용할 때, HTML, CSS, JS에서 에셋 참조 시 주의할 점이 있습니다. 첫째, 절대경로(`/`로 시작하는) 에셋은 Vite가 빌드에 포함하지 않으므로 public 디렉터리에 해당 에셋이 있어야 합니다.

상대경로로 에셋을 참조하면, 참조하는 파일에 상대적이며, Vite가 이 경로를 재작성, 버전 관리, 번들링 해줍니다.

예시 프로젝트 구조:

```nothing
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```

아래는 Vite가 상대/절대 URL을 어떻게 처리하는지 보여줍니다:

```html
<!-- 이 에셋은 Vite에서 처리하지 않으며 빌드에 포함되지 않습니다 -->
<img src="/taylor.png">

<!-- 이 에셋은 Vite에서 재작성, 버전 관리, 번들링됩니다 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기

Vite의 CSS 지원에 대한 자세한 내용은 [Vite 공식 문서](https://vitejs.dev/guide/features.html#css)를 참고하세요. [Tailwind](https://tailwindcss.com)와 같은 PostCSS 플러그인을 사용한다면 프로젝트 루트에 `postcss.config.js` 파일을 만들어 아래처럼 설정하면 됩니다:

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 Tailwind, PostCSS, Vite 설정이 이미 포함되어 있습니다. 별도의 스타터 키트 없이 Tailwind와 Laravel을 함께 쓰고 싶다면 [Tailwind Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와 함께 사용하기

<a name="blade-processing-static-assets"></a>
### 정적 에셋 Vite로 처리하기

자바스크립트나 CSS에서 에셋을 참조하면 Vite가 자동으로 처리(버전 관리와 번들)합니다. 또, Blade 기반 앱에서는 Blade 템플릿에서 직접 참조하는 정적 에셋도 Vite가 처리할 수 있습니다.

이때 Vite가 해당 에셋을 인지하도록, 앱의 엔트리 포인트(js 등)에서 정적 에셋을 임포트해야 합니다. 예를 들어, `resources/images`의 이미지와 `resources/fonts`의 폰트 모두 처리하려면 `resources/js/app.js`에 아래 구문을 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build` 실행 시 위 에셋들도 Vite가 처리합니다. 이후 Blade 템플릿에서 `Vite::asset` 메서드로 버전된 URL을 참조하세요:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade 기반의 전통적 서버사이드 렌더링 앱 개발 시, Vite로 뷰 파일을 수정하면 브라우저가 자동 새로고침 되도록 워크플로우를 개선할 수 있습니다. 시작하려면 `refresh` 옵션을 `true`로 지정하면 됩니다.

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

`refresh`가 `true`일 때 아래 디렉터리 내 파일 저장 시 `npm run dev` 실행 중이라면 브라우저가 전체 페이지 새로고침을 수행합니다:

- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 디렉터리 감시는 [Ziggy](https://github.com/tighten/ziggy)로 프론트엔드에 라우트 링크를 생성할 때 유용합니다.

기본 경로들이 맞지 않다면, 감시할 경로 목록을 직접 지정할 수 있습니다:

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

Laravel Vite 플러그인 내부에서 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 고급 옵션을 통해 더욱 세밀한 제어가 가능합니다. 아래처럼 config 정의를 전달할 수 있습니다:

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
### 별칭(Alias)

자바스크립트에서는 [별칭](#aliases)을 자주 사용하지만, Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드로 별칭을 만들 수 있습니다. 보통 "매크로"는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 정의합니다.

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
    }

매크로를 정의한 후에는 Blade 템플릿에서 아래와 같이 사용할 수 있습니다. 예시로 `resources/images/logo.png` 에셋을 참조합니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="custom-base-urls"></a>
## 커스텀 Base URL

Vite 빌드 에셋을 CDN 등 애플리케이션과 별개의 도메인에 배포한다면 `.env` 파일의 `ASSET_URL` 환경 변수를 설정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

설정 후, 모든 에셋 경로가 해당 URL로 프리픽스됩니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite가 재작성하지 않으니](#url-processing) 프리픽스 적용 대상이 아닙니다.

<a name="environment-variables"></a>
## 환경 변수

자바스크립트에서 환경 변수를 사용하려면, `.env` 파일에서 `VITE_` 프리픽스를 붙여 선언해야 합니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

이후 자바스크립트 코드에서는 `import.meta.env` 객체로 접근하세요:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화하기

Laravel의 Vite 통합은 테스트 실행 중 에셋을 찾으려고 합니다. 따라서 Vite 개발 서버를 실행하거나 빌드된 에셋이 필요합니다.

테스트 중 Vite를 목(mock) 처리하려면, Laravel의 `TestCase` 클래스를 확장한 테스트에서 `withoutVite` 메서드를 호출하세요:

```php
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

모든 테스트에서 Vite를 비활성화하려면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 호출하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```

<a name="ssr"></a>
## 서버사이드 렌더링(SSR)

Laravel Vite 플러그인은 SSR 설정도 매우 간단합니다. 먼저 `resources/js/ssr.js`에 SSR 엔트리 포인트를 만들고, 플러그인 옵션으로 해당 엔트리 포인트를 지정하세요:

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

SSR 엔트리 포인트 빌드를 잊지 않기 위해, `package.json`의 "build" 스크립트를 다음과 같이 바꿔줍니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이제 애플리케이션 SSR 서버를 빌드 및 시작하려면:

```sh
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia SSR](https://inertiajs.com/server-side-rendering)을 사용할 경우, SSR 서버 시작을 위해 `inertia:start-ssr` 아티즌(Artisan) 명령어를 사용할 수 있습니다:

```sh
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 적절한 Laravel, Inertia SSR, Vite 설정이 이미 포함되어 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 Laravel, Inertia SSR, Vite를 빠르게 시작해보세요.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### Content Security Policy (CSP) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로 스크립트 및 스타일 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하려면, 커스텀 [미들웨어](/docs/{{version}}/middleware)에서 `useCspNonce` 메서드를 사용하세요:

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

`useCspNonce`를 호출하면, Laravel이 자동으로 모든 스크립트 및 스타일 태그에 `nonce` 속성을 포함시킵니다.

[Ziggy의 `@route` 지시어](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)처럼 다른 곳에서 nonce가 필요하다면, `cspNonce` 메서드로 값을 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 사용하려는 nonce가 있다면, `useCspNonce`에 전달할 수 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### Subresource Integrity (SRI)

Vite manifest에 에셋별 `integrity` 해시가 포함된 경우, Laravel은 자동으로 생성하는 script 및 style 태그에 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 위한 `integrity` 속성을 추가합니다. 기본적으로 Vite는 manifest에 integrity 해시를 포함하지 않으나, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치해 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

이제 `vite.config.js`에서 플러그인을 활성화하세요:

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

필요하다면 해시가 기록되는 manifest의 key를 커스터마이즈할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

이 기능의 자동 감지를 비활성화하려면, `false`로 설정하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의의 속성 추가

스크립트와 스타일 태그에 [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 같은 추가 속성이 필요하면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드로 지정하세요. 보통 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성에 값을 지정...
    'async' => true, // 값 없는 속성 지정...
    'integrity' => false, // 이미 포함될 속성 제외...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부 속성 추가가 필요하다면, 콜백으로 자원 경로, URL, 매니페스트 청크, 전체 매니페스트를 받아 처리할 수 있습니다:

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
> 개발 서버 실행 중에는 `$chunk`와 `$manifest` 인자가 `null`입니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

Laravel Vite 플러그인은 대부분 애플리케이션에 적합한 관습(convention)을 내장하지만, 추가적인 커스텀이 필요하다면 아래 메서드와 옵션을 `@vite` Blade 지시어 대신 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 커스텀...
            ->useBuildDirectory('bundle') // 빌드 디렉토리 커스텀...
            ->useManifestFilename('assets.json') // 매니페스트 파일명 커스텀...
            ->withEntryPoints(['resources/js/app.js']) // 엔트리포인트 지정...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드 자산 백엔드 경로 생성 커스텀...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js`에도 동일한 설정을 반영해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 커스텀...
            buildDirectory: 'bundle', // 빌드 디렉토리 커스텀...
            input: ['resources/js/app.js'], // 엔트리포인트 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 커스텀...
    },
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정

Vite 에코시스템 내 일부 플러그인은 슬래시(`/`)로 시작하는 URL이 무조건 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합에서는 이 가정이 항상 맞지 않습니다.

예를 들어 `vite-imagetools` 플러그인은 아래와 같이 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

이 플러그인은 `/@imagetools`로 시작하는 URL이 Vite에 의해 가로채져 처리된다고 예상합니다. 이런 플러그인을 사용할 경우, URL을 수동으로 바로잡아야 합니다. 아래처럼 `vite.config.js`의 `transformOnServe` 옵션으로 처리할 수 있습니다.

예시로, 코드 내 `/@imagetools`가 모두 개발 서버 URL을 프리픽스하도록 수정합니다:

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

이제 Vite가 에셋을 제공할 때, 개발 서버를 가리키는 URL이 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
