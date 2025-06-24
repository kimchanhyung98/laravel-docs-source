# 에셋 번들링 (Asset Bundling) (Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite와 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트와 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 다루기](#working-with-scripts)
  - [별칭(Alias)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade 및 라우트와의 연동](#working-with-blade-and-routes)
  - [Vite로 정적 에셋 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭(Alias)](#blade-aliases)
- [에셋 프리페칭](#asset-prefetching)
- [커스텀 기준 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의의 속성 부여](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 교정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 최신 프론트엔드 빌드 도구로, 매우 빠른 개발 환경을 제공하며 코드를 프로덕션에 적합하도록 번들링해줍니다. 라라벨 애플리케이션을 구축할 때는 일반적으로 Vite를 사용하여 여러분의 애플리케이션 CSS와 JavaScript 파일을 프로덕션 배포용 에셋으로 번들링하게 됩니다.

라라벨은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 환경과 프로덕션 환경 모두에서 Vite의 에셋을 손쉽게 불러올 수 있도록 긴밀하게 통합되어 있습니다.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 직접 설치하고 구성하는 방법을 안내합니다. 하지만 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 이 모든 사전 구성 내용이 이미 포함되어 있어, 라라벨과 Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하기 전에 Node.js(16버전 이상)와 NPM이 반드시 설치되어 있어야 합니다.

```shell
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램을 사용하면 Node와 NPM을 손쉽게 최신 버전으로 설치하실 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/12.x/sail)을 사용하고 있다면 Sail 명령어로 Node와 NPM을 실행할 수도 있습니다.

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치

라라벨을 새로 설치하면, 애플리케이션의 루트 디렉토리에 `package.json` 파일이 생성되어 있습니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하는 데 필요한 모든 설정이 이미 포함되어 있습니다. 아래 명령어로 애플리케이션의 프론트엔드 의존성을 NPM으로 설치할 수 있습니다.

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정합니다. 이 파일은 필요에 따라 자유롭게 커스터마이즈할 수 있으며, `@vitejs/plugin-vue`나 `@vitejs/plugin-react` 같이 프로젝트에 필요한 추가 플러그인도 설치할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 엔트리 포인트를 지정해야 합니다. 이 엔트리 포인트는 JavaScript 또는 CSS 파일이 될 수 있으며, TypeScript, JSX, TSX, Sass와 같은 전처리 언어도 지원합니다.

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

SPA(Single Page Application), 특히 Inertia 등으로 구축한 애플리케이션에서는 CSS 엔트리 포인트 없이 Vite를 사용하는 것이 가장 좋습니다.

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

이 경우, CSS는 JavaScript에서 직접 임포트하는 방식으로 불러와야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js` 파일에서 다음과 같이 임포트합니다.

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 엔트리 포인트와 [SSR 엔트리 포인트](#ssr)와 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 사용하기

로컬 개발 웹 서버에서 애플리케이션을 HTTPS로 제공할 경우, Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)로 사이트를 보안 처리했거나, [Laravel Valet](/docs/12.x/valet)에서 애플리케이션에 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인은 해당 TLS 인증서를 자동으로 감지하여 사용할 수 있습니다.

만약 사이트를 보호한 호스트명이 애플리케이션의 디렉터리명과 일치하지 않는다면, `vite.config.js` 파일에서 호스트 명을 수동으로 지정해야 합니다.

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

다른 웹 서버를 사용한다면 신뢰할 수 있는 인증서를 생성한 뒤, 생성된 인증서를 직접 Vite에 지정해야 합니다.

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

만약 운영체제에서 신뢰할 수 있는 인증서를 직접 생성하기 어렵다면 [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 설정할 수 있습니다. 신뢰되지 않는 인증서를 사용하는 경우, `npm run dev` 명령 실행 후 콘솔에 표시되는 "Local" 링크를 브라우저에서 클릭하여 Vite 개발 서버의 인증서 경고를 직접 승인해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행하기

Windows Subsystem for Linux 2(WSL2) 환경에서 [Laravel Sail](/docs/12.x/sail)을 통해 Vite 개발 서버를 실행하는 경우, 브라우저가 개발 서버와 통신할 수 있도록 `vite.config.js` 파일에 다음 설정을 추가해야 합니다.

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

개발 서버 실행 중에 파일 변경이 브라우저에 반영되지 않는다면 Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)을 함께 설정해야 할 수도 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 불러오기

Vite 엔트리 포인트를 설정했으면, 이제 `@vite()` Blade 디렉티브를 애플리케이션의 루트 템플릿 `<head>` 영역에 추가하여 엔트리 포인트 파일을 불러올 수 있습니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript에서 CSS를 임포트하는 경우에는 JavaScript 엔트리 포인트만 추가하면 됩니다.

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 자동으로 Vite 개발 서버를 감지하여, Hot Module Replacement(HMR)를 위해 Vite 클라이언트를 삽입합니다. 빌드 모드에서는 컴파일 및 버전 관리된 에셋, 그리고 임포트한 모든 CSS 파일을 불러옵니다.

필요하다면, `@vite` 디렉티브를 사용할 때 컴파일된 에셋의 빌드 경로도 지정할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋

때로는 에셋 파일의 버전 관리된 URL을 링크로 연결하는 대신, 에셋의 원본 내용을 페이지 내에 직접 포함해야 할 수도 있습니다. 예를 들어, PDF 생성기로 HTML 콘텐츠를 넘길 때 에셋 내용을 직접 삽입하는 것이 필요할 수 있습니다. 이런 경우, `Vite` 파사드의 `content` 메서드를 활용하여 Vite 에셋의 내용을 출력할 수 있습니다.

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
## Vite 실행

Vite를 실행하는 방법은 두 가지가 있습니다. 개발을 할 때는 `dev` 명령어를 이용하여 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경 사항을 자동으로 감지하여, 열려 있는 브라우저 창에 즉시 반영해줍니다.

`build` 명령어는 애플리케이션의 에셋 파일을 번들링 및 버전 관리하여, 실제 배포에 적합한 상태로 만들어줍니다.

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 관리...
npm run build
```

[Laravel Sail](/docs/12.x/sail)의 WSL2 환경에서 개발 서버를 실행한다면, [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 다루기

<a name="aliases"></a>
### 별칭(Alias)

라라벨 플러그인은 기본적으로 여러분이 애플리케이션의 에셋을 쉽게 임포트할 수 있도록 널리 사용하는 별칭을 제공합니다.

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js` 파일에서 직접 별칭을 추가하여 `'@'` 별칭을 커스터마이즈할 수도 있습니다.

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하려면 `@vitejs/plugin-vue` 플러그인을 추가 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-vue
```

설치 후, 플러그인을 `vite.config.js` 설정 파일에 추가할 수 있습니다. 라라벨에서 Vue 플러그인을 사용할 때는 다음과 같이 몇 가지 추가 옵션을 설정해야 합니다.

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
                    // Vue 플러그인은 싱글 파일 컴포넌트 내에서 작성한
                    // 에셋 URL 경로를 라라벨 웹 서버 기준으로 다시 작성합니다.
                    // base를 null로 설정하면, Laravel 플러그인이
                    // 에셋 경로를 Vite 개발 서버 기준으로 다시 작성하게 됩니다.
                    base: null,

                    // Vue 플러그인은 절대 경로의 URL을 파싱하여
                    // 파일 시스템 상의 절대 경로로 처리합니다.
                    // false로 설정할 경우, 절대 URL을 그대로 유지하므로
                    // public 디렉터리 내 에셋을 정상적으로 참조할 수 있습니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 라라벨, Vue, Vite의 적합한 설정이 이미 포함되어 있습니다. 스타터 키트는 라라벨, Vue, Vite 개발을 가장 빠르게 시작할 수 있는 방법입니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크로 프론트엔드를 개발하려면 `@vitejs/plugin-react` 플러그인을 추가 설치해야 합니다.

```shell
npm install --save-dev @vitejs/plugin-react
```

설치 후, 플러그인을 `vite.config.js` 파일에 추가하면 됩니다.

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

JSX가 사용된 파일은 파일 확장자가 `.jsx` 또는 `.tsx`여야 하며, 필요하다면 엔트리 포인트도 [위에서 설명한 대로](#configuring-vite) 맞춰 수정해야 합니다.

기존 `@vite` 디렉티브와 함께 추가로 `@viteReactRefresh` Blade 디렉티브도 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 선언되어야 합니다.

> [!NOTE]
> 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 라라벨, React, Vite의 적합한 설정이 이미 포함되어 있습니다. 스타터 키트는 라라벨, React, Vite 개발을 가장 빠르게 시작할 수 있는 방법입니다.

<a name="inertia"></a>
### Inertia

라라벨 Vite 플러그인은 Inertia 페이지 컴포넌트를 간편하게 로드할 수 있도록 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 사용하는 예시이지만, React 등 다른 프레임워크에서도 사용할 수 있습니다.

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

Inertia와 함께 Vite의 코드 분할(code splitting) 기능을 사용하는 경우, [에셋 프리페칭](#asset-prefetching) 설정을 권장합니다.

> [!NOTE]
> 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 라라벨, Inertia, Vite의 적합한 설정이 이미 포함되어 있습니다. 스타터 키트는 라라벨, Inertia, Vite 개발을 가장 빠르게 시작할 수 있는 방법입니다.

<a name="url-processing"></a>
### URL 처리

Vite를 사용하여 HTML, CSS, JS에서 에셋을 참조할 때는 몇 가지 주의할 점이 있습니다. 우선, 에셋을 절대 경로로 참조하면 Vite가 해당 에셋을 빌드 결과에 포함시키지 않으므로, 반드시 public 디렉터리에 에셋이 존재해야 합니다. [CSS 엔트리 포인트](#configuring-vite)를 따로 둘 경우, 개발 환경에서는 브라우저가 Vite 개발 서버에서 CSS를 로드하려고 시도하므로, 절대 경로를 사용하면 public 디렉터리 외의 에셋을 찾지 못할 수 있습니다.

상대 경로로 에셋을 참조하면, 참조한 파일을 기준으로 경로를 해석합니다. 이렇게 참조된 에셋은 Vite에 의해 경로가 다시 작성되고, 버전 관리 및 번들링되어 제공됩니다.

프로젝트 구조 예시는 다음과 같습니다.

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

아래 예제는 상대 URL과 절대 URL이 어떻게 처리되는지를 보여줍니다.

```html
<!-- 이 에셋은 Vite가 처리하지 않으며 빌드에 포함되지 않습니다 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 경로를 다시 작성하고, 버전 관리 및 번들링합니다 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기

> [!NOTE]
> 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 Tailwind와 Vite의 적합한 설정이 이미 포함되어 있습니다. 만약 스타터 키트 없이 Tailwind와 라라벨을 사용하고자 한다면, [Tailwind의 라라벨 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 라라벨 애플리케이션에는 Tailwind와 적절히 설정된 `vite.config.js` 파일이 이미 포함되어 있습니다. 따라서 Vite 개발 서버를 실행하거나, 아래와 같이 Composer의 `dev` 명령어를 실행하기만 하면 라라벨과 Vite 개발 서버가 함께 시작됩니다.

```shell
composer run dev
```

애플리케이션의 CSS 파일은 `resources/css/app.css`에 작성할 수 있습니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와의 연동

<a name="blade-processing-static-assets"></a>
### Vite로 정적 에셋 처리하기

JavaScript 또는 CSS에서 에셋을 참조하면 Vite가 자동으로 에셋을 처리하고 버전 관리합니다. Blade 기반 애플리케이션을 개발할 때, Blade 템플릿 내에서만 참조하는 정적 에셋도 Vite가 처리하고 버전 관리할 수 있습니다.

이렇게 하려면, 반드시 해당 에셋을 애플리케이션의 엔트리 포인트 파일에서 임포트하여 Vite가 에셋 존재를 인식하도록 해야 합니다. 예를 들어, `resources/images` 디렉터리에 저장된 모든 이미지와 `resources/fonts`에 저장된 모든 폰트를 처리하려면, 엔트리 포인트인 `resources/js/app.js` 파일에 다음과 같이 작성합니다.

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build` 명령어로 빌드할 때 위 에셋들도 함께 처리됩니다. Blade 템플릿에서 이 에셋을 사용할 때는 `Vite::asset` 메서드를 사용하면, 버전 관리된 URL을 반환받을 수 있습니다.

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade를 사용한 전통적인 서버사이드 렌더링 방식으로 애플리케이션을 구축한다면, Vite의 자동 새로고침 기능이 개발 워크플로우를 크게 향상시켜줍니다. view 파일에 변경이 생길 때마다 브라우저가 자동으로 새로고침됩니다. 이를 위해 `refresh` 옵션을 `true`로 지정하면 됩니다.

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

`refresh` 옵션이 `true`일 때, 아래 디렉터리 내 파일을 저장하면 개발 서버가 실행 중(`npm run dev` 상태)인 브라우저에서 전체 페이지 새로고침이 일어납니다.

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

라우트(`routes/**`) 디렉터리를 감시하는 것은, [Ziggy](https://github.com/tighten/ziggy)로 프론트엔드 라우트 링크를 생성하는 경우에 유용합니다.

이 기본 경로들이 필요에 맞지 않다면, 감시할 경로 목록을 직접 지정할 수도 있습니다.

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

내부적으로 Laravel Vite 플러그인은 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 활용하여 이 기능을 제어하며, 고급 설정도 지원합니다. 더 세밀한 동작 제어가 필요하다면 `config` 정의를 사용할 수 있습니다.

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

JavaScript 애플리케이션에서 [별칭 기능](#aliases)을 자주 사용하는 것처럼, Blade 템플릿에서도 별칭을 쓸 수 있습니다. 이를 위해 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하면 됩니다. 일반적으로 이러한 "매크로"는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 정의합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

매크로가 정의되면 템플릿 내에서 직접 사용할 수 있습니다. 예를 들어, 위에서 정의한 `image` 매크로를 사용해서 `resources/images/logo.png` 에셋을 다음과 같이 참조할 수 있습니다.

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 프리페칭

Vite의 코드 분할(code splitting) 기능을 활용해 SPA를 구축할 때는, 페이지 이동마다 필요한 에셋을 가져오게 됩니다. 이로 인해 UI 렌더링이 지연될 수 있습니다. 이런 경우를 위해 라라벨은 JavaScript, CSS 에셋을 페이지 최초 로딩 시 미리(적극적으로) 프리페칭(prefetching)하는 기능을 제공합니다.

[서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출하면, 에셋 프리페칭을 활성화할 수 있습니다.

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

위 예시에서는 에셋을 페이지 로딩마다 최대 3개씩 동시 다운로드로 프리페칭합니다. 필요에 따라 동시성(concurrency) 설정을 변경하거나 제한 없이 모든 에셋을 한 번에 내려받도록 할 수도 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 프리페칭은 [page _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 프리페칭 시작 시점을 커스터마이즈하려면, Vite가 감지할 이벤트명을 지정할 수도 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위처럼 코드를 작성하면, 브라우저의 `window` 객체에서 `vite:prefetch` 이벤트가 수동으로 디스패치 될 때 프리페칭이 시작됩니다. 예를 들어, 페이지 로드 후 3초 뒤에 프리페칭을 시작하도록 할 수 있습니다.

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>

## 커스텀 베이스 URL

Vite로 컴파일된 에셋을 CDN과 같이 애플리케이션과 다른 도메인에 배포하는 경우, 애플리케이션의 `.env` 파일에서 반드시 `ASSET_URL` 환경 변수를 지정해야 합니다.

```env
ASSET_URL=https://cdn.example.com
```

에셋 URL을 설정하면, 모든 에셋의 재작성된 URL 앞에 설정된 값이 자동으로 붙게 됩니다.

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[Vite는 절대 경로(absolute URL)는 재작성하지 않으므로](#url-processing) 프리픽스가 추가되지 않는다는 점을 기억하세요.

<a name="environment-variables"></a>
## 환경 변수

`.env` 파일에서 환경 변수 앞에 `VITE_`를 붙이면, 해당 값을 자바스크립트 코드로 주입할 수 있습니다.

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 `import.meta.env` 객체를 통해 접근할 수 있습니다.

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화

라라벨의 Vite 통합 기능은 테스팅 시에도 에셋을 자동으로 연결하려고 시도합니다. 따라서 Vite 개발 서버를 실행하거나 에셋을 미리 빌드해 두어야 합니다.

테스트 중에 Vite 동작을 모킹(mocking)하고 싶다면, 라라벨의 `TestCase` 클래스를 상속하는 테스트에서 사용할 수 있는 `withoutVite` 메서드를 호출하면 됩니다.

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

모든 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite`를 호출합니다.

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

라라벨 Vite 플러그인을 사용하면, 서버 사이드 렌더링(SSR)을 아주 쉽게 설정할 수 있습니다. 먼저 `resources/js/ssr.js`에 SSR 진입점(entry point) 파일을 만들고, 라라벨 플러그인 설정 옵션에 해당 파일 경로를 지정하세요.

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

SSR 진입점 빌드를 빼먹지 않도록, 애플리케이션의 `package.json`에 있는 "build" 스크립트를 아래와 같이 수정하는 것을 추천합니다.

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

그다음, SSR 서버를 빌드하고 실행하려면 아래 명령어를 사용합니다.

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia와 SSR을 함께 사용하는 경우](https://inertiajs.com/server-side-rendering), 대신에 `inertia:start-ssr` Artisan 명령어로 SSR 서버를 시작할 수 있습니다.

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> 라라벨의 [스타터 키트](/docs/12.x/starter-kits)에는 이미 SSR용 Inertia와 Vite, 그리고 관련 설정이 모두 포함되어 있습니다. 스타터 키트는 라라벨, Inertia SSR, Vite로 개발을 시작하는 가장 빠른 방법입니다.

<a name="script-and-style-attributes"></a>
## Script 및 Style 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) Nonce

[콘텐츠 보안 정책(Content Security Policy)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로, 스크립트와 스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하고자 한다면, 커스텀 [미들웨어](/docs/12.x/middleware)에서 `useCspNonce` 메서드를 이용해 nonce를 생성 또는 지정할 수 있습니다.

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

`useCspNonce`를 호출하면, 라라벨이 자동으로 모든 생성된 script 및 style 태그에 `nonce` 속성을 추가합니다.

[Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등 다른 곳에서도 nonce를 지정해야 할 경우, `cspNonce` 메서드로 값을 얻을 수 있습니다.

```blade
@routes(nonce: Vite::cspNonce())
```

이미 사용할 nonce가 정해진 경우, 해당 값을 `useCspNonce` 메서드에 인수로 전달하면 됩니다.

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI)

Vite 매니페스트에 에셋에 대한 `integrity` 해시가 포함되어 있다면, 라라벨은 생성하는 모든 script 및 style 태그에 자동으로 `integrity` 속성을 추가하여 [서브리소스 무결성(Subresource Integrity)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) 보안을 제공합니다. 기본적으로는 Vite가 `integrity` 해시를 매니페스트에 추가하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하여 활성화할 수 있습니다.

```shell
npm install --save-dev vite-plugin-manifest-sri
```

`vite.config.js` 파일에서 아래와 같이 플러그인을 활성화하세요.

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

필요하다면, 무결성 해시를 저장하는 매니페스트 키도 커스터마이징할 수 있습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

이 기능을 완전히 비활성화하려면, `useIntegrityKey` 메서드에 `false`를 전달합니다.

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의의 속성 추가하기

스크립트나 스타일 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change)과 같은 추가 속성이 필요하다면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드로 지정할 수 있습니다. 일반적으로 이 메서드들은 [서비스 프로바이더](/docs/12.x/providers)에서 호출하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성의 값을 지정할 수 있습니다...
    'async' => true, // 값 없는 속성도 지정 가능...
    'integrity' => false, // 기본적으로 추가되는 속성을 제외하려면 false로 지정...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 속성을 추가하려면, 자산의 소스 경로, URL, 매니페스트 청크, 전체 매니페스트를 인자로 받는 콜백을 전달할 수 있습니다.

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
> Vite 개발 서버가 실행 중일 때는 `$chunk`와 `$manifest` 인수가 `null`입니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

기본적으로 라라벨의 Vite 플러그인은 대부분의 애플리케이션에 바로 사용할 수 있을 정도로 합리적인 규칙을 사용합니다. 하지만 때로는 Vite의 동작을 세부적으로 조정해야 할 수도 있습니다. 이를 위해, `@vite` Blade 디렉티브 대신 사용할 수 있는 다양한 메서드와 옵션을 제공합니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로를 커스터마이즈...
            ->useBuildDirectory('bundle') // 빌드 디렉터리 변경...
            ->useManifestFilename('assets.json') // 매니페스트 파일명 변경...
            ->withEntryPoints(['resources/js/app.js']) // 진입점(entry points) 지정...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋의 백엔드 경로 생성 방식을 변경...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js` 파일에서도 동일한 설정을 지정해야 합니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 변경...
            buildDirectory: 'bundle', // 빌드 디렉터리 변경...
            input: ['resources/js/app.js'], // 진입점 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 변경...
    },
});
```

<a name="cors"></a>
### 개발 서버의 CORS(교차 출처 리소스 공유)

브라우저에서 Vite 개발 서버로부터 에셋을 가져올 때 CORS(교차 출처 리소스 공유) 문제가 발생한다면, 커스텀 오리진(origin)에 개발 서버 접근을 허용할 필요가 있습니다. 라라벨 플러그인과 결합된 Vite는 아래 오리진에서 별도의 추가 설정 없이 접근을 허용합니다.

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env`의 `APP_URL`

가장 쉬운 방법은, 애플리케이션의 `APP_URL` 환경 변수 값과 브라우저에서 접속하는 오리진을 일치시키는 것입니다. 예를 들어, `https://my-app.laravel`에서 접근한다면, `.env`를 아래와 같이 설정해야 합니다.

```env
APP_URL=https://my-app.laravel
```

여러 오리진을 지원하는 등 더 세밀한 제어가 필요하다면, [Vite의 유연한 내장 CORS 서버 설정](https://vite.dev/config/server-options.html#server-cors)을 활용할 수 있습니다. 예를 들어, 프로젝트의 `vite.config.js` 파일에서 `server.cors.origin` 옵션에 여러 오리진을 지정할 수 있습니다.

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

정규 표현식도 사용할 수 있어, 예를 들어 특정 톱레벨 도메인(예: `*.laravel`)의 모든 오리진을 허용할 수 있습니다.

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
### 개발 서버 URL 바로잡기

Vite 생태계의 일부 플러그인은 슬래시(`/`)로 시작하는 URL이 무조건 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 라라벨 통합 환경에서는 항상 그런 것이 아닙니다.

예를 들어, `vite-imagetools` 플러그인은 Vite가 에셋을 제공할 때 아래와 같은 URL을 출력합니다.

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

`vite-imagetools` 플러그인은 `/@imagetools`로 시작하는 URL을 Vite가 가로채서 별도로 처리해주기를 기대합니다. 이런 동작을 기대하는 플러그인을 사용할 때는 URL을 수동으로 바로잡아야 합니다. `vite.config.js`에서 `transformOnServe` 옵션으로 해당 작업을 구현할 수 있습니다.

아래 예제에서는, 생성된 코드에서 `/@imagetools`가 나오면 개발 서버 URL을 앞에 붙이게 만듭니다.

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

이렇게 하면 Vite가 에셋을 제공할 때, 아래와 같이 개발 서버를 가리키는 URL이 출력됩니다.

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```