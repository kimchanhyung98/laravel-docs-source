# 에셋 번들링 (Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite와 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트 및 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [자바스크립트 사용하기](#working-with-scripts)
  - [별칭(Alias)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 사용하기](#working-with-stylesheets)
- [Blade 및 라우트와 함께 사용하기](#working-with-blade-and-routes)
  - [정적 에셋 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭(Alias)](#blade-aliases)
- [에셋 프리페치(prefetching)](#asset-prefetching)
- [커스텀 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 보정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션 용도에 맞게 코드를 번들링하는 최신 프론트엔드 빌드 툴입니다. Laravel로 애플리케이션을 구축할 때는 대개 Vite를 사용해 CSS와 JavaScript 파일을 프로덕션에 맞는 에셋으로 번들링하게 됩니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 Vite와의 통합을 매끄럽게 지원합니다. 이를 통해 개발 및 프로덕션 환경 모두에서 에셋을 간편하게 불러올 수 있습니다.

> [!NOTE]  
> Laravel Mix를 사용하고 계신가요? 최근의 Laravel 설치본에서는 Vite가 Laravel Mix를 대체했습니다. Mix 관련 문서는 [Laravel Mix](https://laravel-mix.com/) 웹사이트를 참고하세요. Vite로 전환하고 싶으시면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

Vite 도입 전, 신규 Laravel 애플리케이션은 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)를 통해 에셋을 번들링했습니다. Vite는 풍부한 JavaScript 애플리케이션을 좀 더 빠르고 생산적으로 개발할 수 있도록 설계되었습니다. [Inertia](https://inertiajs.com)와 같은 도구로 구축한 SPA(싱글 페이지 애플리케이션)를 개발 중이라면 Vite가 최적의 선택입니다.

Vite는 [Livewire](https://livewire.laravel.com)와 같은 전통적인 서버 사이드 렌더링 방식에도 적합하지만, JavaScript 애플리케이션에서 직접 참조하지 않는 임의의 에셋 복사 기능 등 Laravel Mix가 제공하던 일부 기능은 지원하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 마이그레이션

Vite로 시작한 새 Laravel 프로젝트를 다시 Laravel Mix 및 webpack 기반으로 전환해야 하나요? 걱정하지 마세요. [공식 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고해주세요.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]  
> 다음 문서에서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 다룹니다. 그러나, Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 모든 기본 구성 요소가 포함되어 있어 가장 빠르게 프로젝트를 시작할 수 있습니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하려면 Node.js(16+)와 NPM이 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

최신 Node 및 NPM은 [공식 Node 웹사이트](https://nodejs.org/en/download/)에서 손쉽게 설치할 수 있습니다. [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용한다면, Sail을 통해서도 Node와 NPM을 실행할 수 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치

Laravel의 새 프로젝트를 생성하면, 프로젝트 루트에 `package.json` 파일이 포함됩니다. 기본 `package.json`에는 Vite와 Laravel 플러그인을 바로 사용할 수 있는 모든 설정이 들어 있습니다. 프론트엔드 의존성은 NPM으로 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일에서 설정합니다. 필요에 따라 이 파일을 자유롭게 커스터마이즈할 수 있고, `@vitejs/plugin-vue`·`@vitejs/plugin-react` 등 플러그인도 추가 가능입니다.

Laravel Vite 플러그인에서는 애플리케이션의 진입점(entry point: JS/CSS 파일, TypeScript/JSX/TSX/Sass 등 포함)을 지정해야 합니다.

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

Inertia 등으로 SPA를 만드는 경우에는 CSS 엔트리 포인트 없이 사용해야 최적의 성능을 얻을 수 있습니다:

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

대신, CSS를 JavaScript에서 직접 임포트하세요. 일반적으로 `resources/js/app.js`에서 다음과 같이 처리합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 엔트리 포인트 및 [SSR 엔트리 포인트](#ssr)와 같은 고급 옵션도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안(HTTPS) 개발 서버 사용하기

로컬 개발 서버를 HTTPS로 제공하는 경우, Vite 개발 서버와 연결 시 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)에서 사이트를 보안(HTTPS) 처리했거나, [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행한 경우, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지하여 사용합니다.

만약 사이트를 앱 디렉토리명과 다른 도메인으로 보안 처리했다면, `vite.config.js` 파일에서 호스트(host)를 수동 지정할 수 있습니다:

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

기타 웹서버 사용 시에는 신뢰할 수 있는 인증서를 직접 생성해 Vite에 지정해야 합니다:

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

시스템에 신뢰할 수 있는 인증서를 생성하지 못할 경우, [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치해 사용할 수 있습니다. 이때 브라우저에서 인증서 경고를 수락해야 하며, `npm run dev` 명령 실행 시 터미널에 표시되는 "Local" 링크를 클릭해 접속하면 됩니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행

WSL2 기반 [Laravel Sail](/docs/{{version}}/sail) 환경에서 Vite 개발 서버를 실행할 때, 브라우저가 개발 서버에 정상적으로 연결될 수 있도록 `vite.config.js`에 다음 설정을 추가하세요:

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

또한, 코드 변경 사항이 브라우저에 즉시 반영되지 않을 경우, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch)을 추가로 조정해야 할 수도 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 불러오기

Vite 엔트리 포인트를 설정했다면, 애플리케이션 루트 템플릿의 `<head>`에 `@vite()` Blade 디렉티브로 참조할 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript에서 임포트하는 구조라면, JavaScript 엔트리 포인트만 지정하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지하여 Hot Module Replacement를 위한 Vite 클라이언트를 삽입합니다. 빌드 모드에서는 컴파일 및 버전 관리된 에셋(CSS 포함)의 경로를 자동으로 불러옵니다.

별도의 빌드 경로에 에셋을 두었다면, 다음과 같이 빌드 경로도 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 디렉토리에 상대적입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### Inline 에셋 처리

에셋의 링크 대신 실제 CSS/JS 내용을 페이지에 직접 삽입해야 할 때가 있습니다. 예를 들어 PDF 생성기로 HTML을 전달할 경우 그렇습니다. 이때는 `Vite` 파사드의 `content` 메서드를 이용하세요:

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

Vite를 실행하는 방법은 두 가지입니다. `dev` 명령은 개발 중 로컬에서 파일 변경을 즉시 감지해 브라우저에 반영합니다. 

`build` 명령을 실행하면 에셋을 프로덕션용으로 버전 관리하여 번들링하고, 배포할 수 있게 준비됩니다:

```shell
# Vite 개발 서버 실행(실시간 반영)...
npm run dev

# 에셋 빌드 및 버전 관리(프로덕션용)...
npm run build
```

WSL2의 [Sail](/docs/{{version}}/sail) 환경에서 개발 서버를 실행하는 경우 [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## 자바스크립트 사용하기

<a name="aliases"></a>
### 별칭(Alias)

Laravel 플러그인은 자주 사용하는 경로의 자산을 더 쉽게 임포트할 수 있도록 일반적인 alias를 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

원하는 경우, `vite.config.js` 파일의 설정에서 `'@'` 별칭을 덮어쓸 수 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하고 싶다면, `@vitejs/plugin-vue` 플러그인을 설치하세요:

```sh
npm install --save-dev @vitejs/plugin-vue
```

이후 `vite.config.js`에 플러그인을 추가하고, 몇 가지 추가 옵션을 넣어야 합니다:

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
                    // Single File Component 내부 에셋 URL을 Laravel 웹서버가 아닌, Vite 서버로 변환
                    base: null,

                    // 절대 경로 URL을 디스크의 파일로 판단하지 않고, public 디렉토리 기반으로 유지
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 Laravel, Vue, Vite가 올바로 구성되어 있습니다. Laravel, Vue, Vite를 빠르게 시작하려면 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크를 사용할 경우, `@vitejs/plugin-react` 플러그인을 설치하세요:

```sh
npm install --save-dev @vitejs/plugin-react
```

`vite.config.js`에 플러그인을 추가합니다:

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

JSX가 포함된 파일은 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 필요하다면 엔트리 포인트 경로도 [위에서 설명한 대로](#configuring-vite) 수정해야 합니다.

또한, `@vite` Blade 디렉티브와 함께 추가적으로 `@viteReactRefresh` Blade 디렉티브를 사용해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출해야 합니다.

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 이미 React 및 Vite 구성이 되어 있습니다. Laravel, React, Vite로 빠르게 시작하려면 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 해석하는 데 편리한 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에 사용하는 예시입니다. (React 등 다른 프레임워크에서도 사용 가능):

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

Vite의 코드 분할 기능을 Inertia와 함께 사용한다면, [에셋 프리페치](#asset-prefetching)를 추가로 설정하는 것이 좋습니다.

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 Inertia 및 Vite 구성이 이미 포함되어 있습니다. Laravel, Inertia, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="url-processing"></a>
### URL 처리

Vite를 쓰면서 HTML, CSS, JS에서 에셋을 참조할 때 주의할 점이 있습니다. 

1. **절대 경로(/로 시작)** 에셋은 Vite 빌드에 포함되지 않습니다. 반드시 public 디렉토리에 에셋이 존재해야 하며, [CSS 엔트리포인트](#configuring-vite)를 쓸 때는 절대경로를 피해야 합니다. 개발 중 브라우저가 Vite 개발 서버에서 경로를 찾으려 하기 때문입니다.
2. **상대 경로**로 에셋을 참조할 때, 참조 위치 파일 기준의 상대 경로를 사용해야 하며, Vite가 해당 에셋을 리라이트, 버전 관리, 번들 처리합니다.

프로젝트 구조 예시:

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

Vite가 처리하는 방식:

```html
<!-- Vite가 처리하지 않으며 빌드에 포함되지 않음 -->
<img src="/taylor.png">

<!-- Vite가 리라이트, 버전 관리, 번들링 함 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 사용하기

Vite의 CSS 지원에 대해서는 [Vite 공식 문서](https://vitejs.dev/guide/features.html#css)를 참고하세요. [Tailwind](https://tailwindcss.com) 등 PostCSS 플러그인을 사용할 경우, 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 자동 적용합니다:

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 Tailwind, PostCSS, Vite가 이미 구성되어 있습니다. Starter kit 없이 Tailwind와 Laravel만 사용하려면 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와 함께 사용하기

<a name="blade-processing-static-assets"></a>
### Vite로 정적 에셋 처리

JavaScript나 CSS에서 참조한 에셋은 Vite가 자동 처리(버전 관리, 번들)합니다. Blade 기반 애플리케이션에서는 Blade 템플릿에서만 참조하는 정적 에셋도 처리·버전 관리할 수 있습니다.

이를 위해서는 정적 에셋을 애플리케이션의 엔트리포인트(예시: `resources/js/app.js`)에서 불러와 Vite에 알리고, Blade에서 `Vite::asset` 메서드로 경로를 가져오면 됩니다:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

빌드 후에는 아래처럼 `Vite::asset`으로 버전 경로를 참조하세요:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade를 쓰는 서버사이드 렌더 애플리케이션 개발 시, Vite는 뷰 파일 변경 시 브라우저를 자동 새로고침할 수 있습니다. `refresh` 옵션을 `true`로 간단히 지정하세요:

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

`refresh: true`이면 아래 경로의 파일이 저장될 때 `npm run dev` 실행 중인 브라우저가 새로고침됩니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 디렉토리 감시는 [Ziggy](https://github.com/tighten/ziggy) 사용 시 유용합니다.

감시 경로 커스터마이즈도 가능합니다:

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

내부적으로 Laravel Vite 플러그인은 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하는데, 고급 옵션이 필요하다면 `config` 정의도 제공할 수 있습니다:

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

JS처럼 자주 사용하는 디렉토리에 별칭([alias](#aliases))을 추가할 수 있습니다. Blade에서도 `Illuminate\Support\Facades\Vite`의 `macro` 메서드로 별칭을 정의할 수 있습니다. 보통 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 설정합니다:

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
    }

이후 템플릿에서 `image` 매크로를 이용해 쉽게 경로를 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## 에셋 프리페치(prefetching)

Vite의 코드 분할을 사용하는 SPA는 각 페이지 이동 시 필요한 에셋을 그때그때 불러옵니다. 프리페치를 활성화하면 초기 페이지 로딩 시 JS·CSS 에셋을 미리 내려받아 UI 렌더링 지연을 줄일 수 있습니다.

서비스 프로바이더의 `boot` 메서드에서 `Vite::prefetch`를 호출하세요:

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

위처럼 설정하면 페이지 로딩마다 최대 3개씩 동시 프리페치합니다. 제한을 제거하려면 concurrency를 지정하지 않으면 됩니다:

```php
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 브라우저의 [load 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) 발생 시 프리페치가 시작됩니다. 시작 트리거를 바꾸고 싶다면 이벤트명을 지정할 수 있습니다:

```php
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위 코드에서는 JS에서 다음과 같이 이벤트를 발생시켜 프리페치 타이밍을 제어할 수 있습니다:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 Base URL

에셋을 CDN처럼 별도의 도메인에 배포한다면, `.env` 파일의 `ASSET_URL` 환경 변수에 해당 URL을 반드시 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

이후 에셋 경로에 자동으로 base URL이 프리픽스(prefix)로 붙습니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 경로 URL은 Vite가 리라이트하지 않으므로](#url-processing), 이 경우에는 프리픽스가 적용되지 않습니다.

<a name="environment-variables"></a>
## 환경 변수

`.env` 파일에서 `VITE_`로 시작하는 환경변수는 JavaScript에서 접근할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

접근 방법:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화

Laravel의 Vite 통합은 테스트 실행 중에도 에셋을 해석하려 하므로 개발 서버를 켜두거나 에셋 빌드가 필요합니다.

테스트 시 Vite 동작을 막으려면, 테스트가 Laravel의 `TestCase`를 상속한다면 `withoutVite` 메서드를 호출하세요:

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

모든 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 호출하면 됩니다:

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

Laravel Vite 플러그인을 사용하면 SSR(Server-Side Rendering) 설정을 쉽게 할 수 있습니다. 먼저 `resources/js/ssr.js`에 SSR 엔트리 포인트를 생성한 후, Laravel 플러그인에 옵션을 전달하여 지정하세요:

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

SSR 빌드 파일 생성을 잊지 않기 위해, `package.json`의 "build" 스크립트에 SSR 빌드 명령을 추가하는 것이 좋습니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

SSR 서버 빌드 및 실행:

```sh
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia와 SSR](https://inertiajs.com/server-side-rendering)을 사용하는 경우, `inertia:start-ssr` 아티즌(artisan) 명령어를 이용하세요:

```sh
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 Inertia SSR 및 Vite 구성이 이미 포함되어 있습니다. Inertia SSR 및 Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### Content Security Policy (CSP) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 스크립트 및 스타일 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하려면, 커스텀 [미들웨어](/docs/{{version}}/middleware)에서 `useCspNonce` 메서드를 사용하세요:

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

`useCspNonce` 호출 후에는 생성된 모든 스크립트·스타일 태그에 `nonce` 속성이 자동 추가됩니다.

타 미들웨어 또는 [Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등 다른 위치에서 nonce를 참조하려면 `cspNonce` 메서드를 사용하세요:

```blade
@routes(nonce: Vite::cspNonce())
```

미리 생성한 nonce가 있다면, `useCspNonce`에 파라미터로 전달하면 됩니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### Subresource Integrity (SRI)

Vite 매니페스트에 `integrity` 해시가 포함되어 있을 경우, Laravel은 생성하는 모든 스크립트 및 스타일 태그에 자동으로 `integrity` 속성을 추가해 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 적용합니다. 기본적으로 Vite는 manifest에 해시를 포함하지 않으나, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) 플러그인 설치 시 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

`vite.config.js`에 플러그인을 추가합니다:

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

integrity 해시의 manifest 키를 변경하고 싶다면 다음과 같이 지정합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지를 완전히 끄고 싶으면 false로 설정할 수 있습니다:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성

스크립트/스타일 태그에 [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등 다양한 속성을 추가해야 한다면, `useScriptTagAttributes`와 `useStyleTagAttributes` 메서드를 사용하세요. 주로 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값 있는 속성 지정
    'async' => true, // 값 없이 속성만 지정
    'integrity' => false, // 기본적으로 포함될 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부로 속성을 추가하려면 콜백을 전달할 수도 있습니다:

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
> Vite 개발 서버 실행 중에는 `$chunk`, `$manifest` 기본값이 `null`입니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

기본적으로 Laravel Vite 플러그인은 대부분의 애플리케이션에서 바로 쓸 수 있는 합리적인 설정을 제공합니다. 그러나, Vite의 동작을 더 세밀하게 변경해야 한다면 `@vite` Blade 디렉티브 대신 아래와 같이 다양한 메서드를 조합할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 위치 변경
            ->useBuildDirectory('bundle') // 빌드 디렉토리 변경
            ->useManifestFilename('assets.json') // 매니페스트 파일명 변경
            ->withEntryPoints(['resources/js/app.js']) // 엔트리포인트 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 에셋 경로 생성 커스터마이징
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js`에도 동일하게 맞게 지정합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 위치 변경
            buildDirectory: 'bundle', // 빌드 디렉토리 변경
            input: ['resources/js/app.js'], // 엔트리포인트 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 변경
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS 설정

Vite 개발 서버에서 에셋을 불러올 때 브라우저에서 CORS 오류가 발생할 경우, 개발 서버의 Origin(출처) 처리 권한을 추가해야 합니다. Laravel 플러그인 내장 지원 대상은:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env`의 `APP_URL`

커스텀 Origin을 사용하려면 `.env`의 `APP_URL`을 브라우저에서 접근하는 주소와 동일하게 맞추는 것이 가장 간단합니다. 예시:

```env
APP_URL=https://my-app.laravel
```

여러 Origin 지원 등 더 세밀한 제어가 필요하다면 [Vite의 CORS 설정](https://vite.dev/config/server-options.html#server-cors)을 이용하세요. `vite.config.js`에서 여러 Origin을 지정하는 예시:

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

정규식도 사용할 수 있습니다. 예시: `.laravel` 최상위 도메인 전체 허용

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
                // 지원 형식: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 보정

Vite 생태계 내 일부 플러그인은 `/`로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel 통합 시에는 그렇지 않을 수 있습니다.

예를 들어, `vite-imagetools` 플러그인은 개발 서버에서 아래와 같은 URL을 생성합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

플러그인은 `/@imagetools`로 시작하는 요청이 Vite에 의해 처리되기를 기대합니다. 이런 플러그인 사용 시에는 URL을 직접 보정해야 하며, `vite.config.js`의 `transformOnServe` 옵션이 유용합니다.

예시: 생성된 코드 내 `/@imagetools`를 개발 서버 URL + `/@imagetools`로 치환

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

이제 Vite가 에셋을 제공하는 동안 다음과 같이 URL이 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
