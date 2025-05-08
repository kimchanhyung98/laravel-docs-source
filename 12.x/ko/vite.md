# 에셋 번들링(Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치하기](#installing-node)
  - [Vite와 Laravel 플러그인 설치하기](#installing-vite-and-laravel-plugin)
  - [Vite 구성하기](#configuring-vite)
  - [스크립트와 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [JavaScript 다루기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade 및 라우트와의 연동](#working-with-blade-and-routes)
  - [정적 에셋의 Vite 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭(Aliases)](#blade-aliases)
- [에셋 프리페치(Prefetching)](#asset-prefetching)
- [커스텀 베이스 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트 시 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그의 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책(CSP) Nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의의 속성 추가](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 보정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 최신 프론트엔드 빌드 도구로, 매우 빠른 개발 환경을 제공하며 프로덕션용으로 코드를 번들링합니다. Laravel로 애플리케이션을 개발할 때는 보통 Vite를 사용하여 앱의 CSS 및 JavaScript 파일을 프로덕션에 적합한 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 및 프로덕션 환경에서 에셋을 손쉽게 불러올 수 있도록 Vite와 완벽하게 통합됩니다.

> [!NOTE]  
> Laravel Mix를 사용하고 계신가요? 새로운 Laravel 설치에서는 Vite가 Laravel Mix를 대체하였습니다. Mix에 대한 문서는 [Laravel Mix](https://laravel-mix.com/) 사이트를 참고하세요. Vite로 전환을 원하시면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

Vite로 전환되기 전, Laravel의 새로운 앱은 에셋 번들링에 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 리치 JavaScript 애플리케이션 개발 시 훨씬 빠르고 생산적인 경험을 제공합니다. [Inertia](https://inertiajs.com)와 같은 도구로 개발된 SPA(싱글 페이지 애플리케이션)에 특히 적합합니다.

Vite는 [Livewire](https://livewire.laravel.com) 등 JavaScript "스프링클"이 더해진 전통적인 서버 사이드 렌더 앱과도 잘 호환됩니다. 하지만 JavaScript에서 직접 참조하지 않는 임의의 에셋을 빌드에 복사할 수 있는 기능 등 Laravel Mix가 지원하는 일부 기능은 없습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로의 마이그레이션

Vite 스캐폴딩으로 새롭게 시작한 Laravel 앱을 다시 Laravel Mix 및 webpack 기반으로 이전해야 하나요? 걱정하지 마세요. [Vite에서 Mix로의 마이그레이션 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]  
> 이 문서는 Laravel Vite 플러그인 설치와 구성 방법을 수동으로 설명합니다. 그러나 Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 이미 모든 설정을 포함하고 있어 가장 빠르게 Laravel과 Vite를 시작하는 방법입니다.

<a name="installing-node"></a>
### Node 설치하기

Vite와 Laravel 플러그인을 실행하려면 Node.js(16 이상)와 NPM이 설치되어 있어야 합니다:

```shell
node -v
npm -v
```

최신 Node 및 NPM은 [공식 Node 웹사이트](https://nodejs.org/en/download/)의 그래픽 설치 프로그램을 통해 쉽게 설치할 수 있습니다. [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용하는 경우 Sail을 이용해 Node와 NPM을 실행할 수도 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치하기

새로운 Laravel 프로젝트의 루트에는 `package.json` 파일이 있습니다. 기본 `package.json`에는 Vite와 Laravel 플러그인을 사용하는 데 필요한 모든 것이 포함되어 있습니다. 아래 명령어로 프론트엔드 의존성을 설치할 수 있습니다:

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 구성하기

Vite는 프로젝트 루트의 `vite.config.js` 파일로 구성합니다. 이 파일은 필요에 따라 자유롭게 커스터마이즈할 수 있고, `@vitejs/plugin-vue`, `@vitejs/plugin-react`와 같은 추가 플러그인도 쉽게 설치할 수 있습니다.

Laravel Vite 플러그인에서는 앱의 엔트리 포인트를 지정해야 합니다. JavaScript, CSS 파일뿐 아니라 TypeScript, JSX, TSX, Sass 등 전처리 언어도 지정할 수 있습니다.

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

Inertia 등으로 SPA를 빌드한다면 CSS 엔트리 포인트는 등록 없이 아래처럼 사용하길 권장합니다:

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

대신 JavaScript 파일에서 CSS를 import하세요. 예를 들어 `resources/js/app.js`에서 아래처럼 작성할 수 있습니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

라라벨 플러그인은 여러 엔트리 포인트와 [SSR 엔트리 포인트](#ssr) 등 고급 옵션도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### HTTPS 개발 서버 사용하기

로컬 개발 웹서버가 HTTPS로 서비스를 제공할 때 Vite 개발 서버와의 연결에 문제가 생길 수 있습니다.

[Laravel Herd](https://herd.laravel.com)에서 사이트를 보안 처리했거나 [Laravel Valet](/docs/{{version}}/valet)에서 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 사용했다면 Laravel Vite 플러그인이 자동으로 TLS 인증서를 감지해 사용합니다.

만약 애플리케이션 디렉터리 이름과 일치하지 않는 호스트로 보안 처리를 했다면, `vite.config.js`에서 직접 호스트를 지정할 수 있습니다:

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

다른 웹서버를 사용하는 경우 신뢰할 수 있는 인증서를 생성하여 Vite에 수동으로 등록해줘야 합니다:

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

시스템에 신뢰할 수 있는 인증서를 생성할 수 없다면 [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하여 구성할 수 있습니다. 신뢰되지 않는 인증서를 사용하는 경우 `npm run dev` 실행 후 콘솔에 표시되는 "Local" 링크를 따라가 브라우저에서 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2 환경의 Sail에서 개발 서버 실행하기

[Sail](/docs/{{version}}/sail) 환경에서 WSL2(Windows Subsystem for Linux 2)로 Vite 개발 서버를 실행할 경우 브라우저와 개발 서버의 정상 통신을 위해 `vite.config.js`에 다음 설정을 추가하세요:

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

개발 서버 실행 상태에서 파일 변경 사항이 브라우저에 반영되지 않는 경우 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 함께 설정해 보세요.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 불러오기

Vite 엔트리 포인트를 구성했다면, 이제 애플리케이션 루트 템플릿의 `<head>`에 `@vite()` Blade 디렉티브로 불러올 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript에서 CSS를 import하고 있다면 JavaScript 엔트리 포인트만 추가하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 개발 시 자동으로 Vite 개발 서버를 감지하여 Hot Module Replacement가 가능하도록 Vite 클라이언트를 주입하며, 빌드 모드에서는 컴파일되고 버전링된 에셋을 불러옵니다.

필요하다면 `@vite` 디렉티브에 컴파일된 에셋의 빌드 경로도 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public path 기준 상대경로입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 에셋 인라인 포함

간혹 에셋의 URL이 아닌 실제 내용을 직접 포함해야 할 때가 있습니다. 예를 들어 PDF 생성기에 HTML을 전달할 때 내부 에셋 코드를 직접 넣어야 하는 경우입니다. 이럴 때는 `Vite` 파사드의 `content` 메서드를 사용하세요:

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

Vite는 두 가지 방식으로 실행할 수 있습니다.  
`dev` 명령으로 개발 서버를 실행하면 파일의 변경 사항이 자동으로 감지되어 오픈된 브라우저 창에 즉시 반영됩니다.

`build` 명령으로 에셋을 번들링 및 버전링하여 배포용으로 준비할 수도 있습니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션 빌드 및 버전링...
npm run build
```

[Sail](/docs/{{version}}/sail)의 WSL2 환경에서 개발 서버를 실행 중이라면 [추가 구성](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 다루기

<a name="aliases"></a>
### 별칭(Aliases)

Laravel 플러그인은 기본적으로 아래와 같이 자주 사용하는 디렉터리에 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

이 `'@'` 별칭은 `vite.config.js`에서 자유롭게 덮어쓸 수 있습니다:

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

프론트엔드를 [Vue](https://vuejs.org/) 프레임워크로 빌드하려면 `@vitejs/plugin-vue` 플러그인을 설치해 주세요:

```shell
npm install --save-dev @vitejs/plugin-vue
```

이 후 아래 처럼 `vite.config.js`에 플러그인을 추가합니다:

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
                    // Single File Component의 자산 URL 재작성 처리를 설명하는 옵션입니다.
                    base: null, // Laravel 플러그인에게 Vite 서버 기준으로 URL 재작성 권장

                    // 절대경로 URL 처리 관련 설정
                    includeAbsolute: false, // public 디렉터리의 자산을 그대로 참조
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 이미 올바른 Laravel, Vue, Vite 구성을 포함합니다. 스타터 키트를 사용하면 손쉽게 Laravel, Vue, Vite로 시작할 수 있습니다.

<a name="react"></a>
### React

프론트엔드를 [React](https://reactjs.org/)로 개발하려면 `@vitejs/plugin-react` 플러그인을 설치하세요:

```shell
npm install --save-dev @vitejs/plugin-react
```

그리고 아래처럼 `vite.config.js`에 추가해줍니다:

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

JSX를 사용하는 파일은 `.jsx` 또는 `.tsx` 확장자가 필요하며, 필요한 경우 엔트리 포인트도 [위 예시](#configuring-vite)처럼 업데이트하세요.

또한, 기존 `@vite` 디렉티브와 함께 추가로 `@viteReactRefresh` Blade 디렉티브를 사용해야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`를 `@vite`보다 먼저 호출해야 합니다.

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 이미 올바른 Laravel, React, Vite 구성을 포함합니다. 스타터 키트를 사용하면 손쉽게 Laravel, React, Vite로 시작할 수 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 손쉽게 불러올 수 있는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3을 예로 든 사용법입니다. (React 등에서도 동일하게 사용 가능합니다.)

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

Vite의 코드 스플리팅(code splitting)과 Inertia를 함께 사용할 때는 [에셋 프리페치](#asset-prefetching) 설정을 추천합니다.

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 올바른 Laravel, Inertia, Vite 구성을 이미 포함합니다.

<a name="url-processing"></a>
### URL 처리

Vite와 함께 애플리케이션의 HTML, CSS, JS에서 에셋을 참조할 때 주의할 점이 있습니다.  
먼저 **절대 경로로 에셋을 참조하면** Vite가 해당 에셋을 빌드에 포함하지 않으므로, 에셋이 public 디렉터리에 있는지 확인해야 합니다. [dedicated CSS entrypoint](#configuring-vite)를 사용하는 경우에는, 브라우저가 개발 중 해당 CSS 경로를 Vite 개발 서버에서 찾으려 하니 절대 경로 사용을 피해야 합니다.

**상대 경로로 에셋을 참조하면** 참조하는 파일 기준으로 경로가 계산되어 Vite가 해당 경로의 에셋을 번들링, 버전링, 재작성합니다.

프로젝트 구조 예시:

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

아래는 Vite가 상대/절대 URL을 어떻게 처리하는지 예시입니다:

```html
<!-- Vite가 처리하지 않음, 빌드에 포함되지 않음 -->
<img src="/taylor.png">

<!-- Vite가 재작성, 버전링, 번들링 처리 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기

> [!NOTE]  
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 Tailwind 및 Vite 구성을 이미 포함하고 있습니다. 별도 스타터 키트 없이 Tailwind와 Laravel을 사용하려면 [Tailwind의 라라벨 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 앱에는 이미 Tailwind와 적절한 `vite.config.js`가 포함되어 있습니다. 따라서 Vite 개발 서버를 실행하거나, 아래처럼 Composer로 동시에 Laravel과 Vite 서버를 실행하면 됩니다:

```shell
composer run dev
```

앱의 CSS는 `resources/css/app.css`에 작성하면 됩니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와의 연동

<a name="blade-processing-static-assets"></a>
### 정적 에셋의 Vite 처리

JavaScript 또는 CSS에서 참조한 에셋은 Vite가 자동으로 처리 및 버전링합니다.  
또한, Blade 기반 앱에서는 Blade 템플릿에서 직접 참조하는 정적 에셋도 Vite로 처리할 수 있습니다.

이를 위해서는 정적 에셋을 앱의 엔트리 포인트에서 한 번 import해줘야 합니다. 예를 들어, `resources/images`의 모든 이미지, `resources/fonts` 폴더의 모든 폰트를 처리/버전링하려면:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이렇게 하면 `npm run build` 실행 시 각 에셋도 처리됩니다. Blade에서는 버전링된 URL을 `Vite::asset` 메서드로 참조하면 됩니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade 등 전통적인 서버 사이드 렌더링 앱에서는 Vite가 뷰 파일 변경 시 자동으로 브라우저를 새로고침하여 개발 경험을 향상시킵니다. 아래처럼 간단히 `refresh` 옵션을 `true`로 지정하세요:

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

`refresh: true` 상태에서 `npm run dev`를 실행하면 다음 경로의 파일 저장 시 전체 페이지 새로고침이 발생합니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

특히 [Ziggy](https://github.com/tighten/ziggy)로 라우트 링크를 프론트엔드에서 생성하는 경우 `routes/**` 감시는 유용합니다.

경로를 직접 지정하고 싶다면 아래처럼 나열할 수 있습니다:

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

Laravel Vite 플러그인 내부적으로는 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 딜레이 등 고급 옵션도 지정할 수 있습니다:

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

JavaScript처럼 Blade에서도 자주 참조하는 경로에 [별칭(Alias)를 만들 수 있습니다](#aliases).  
`Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하면 됩니다. 일반적으로 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 별칭을 정의합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

정의 후에는 Blade에서 바로 사용할 수 있습니다. 예시:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="asset-prefetching"></a>
## 에셋 프리페치(Prefetching)

Vite의 코드 스플리팅과 함께 SPA를 개발할 때, 필요한 에셋이 페이지 이동 시마다 불러와져 UI 렌더링이 지연될 수 있습니다. 이런 경우 Laravel은 초기 페이지 로딩 시 JavaScript, CSS 에셋을 미리 프리페치해서 렌더링 지연을 줄일 수 있는 기능을 제공합니다.

[서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출해 프리페치를 활성화합니다:

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

위 예에서는 페이지 로드 시 최대 3개의 에셋을 동시에 프리페치합니다. 필요에 따라 동시성(concurrency) 값을 조절하거나, 제한 없이 한 번에 모든 에셋을 다운로드하도록 할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로는 [page _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)에서 프리페치가 시작됩니다. 시작 이벤트를 직접 지정하려면 아래처럼 사용합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위와 같이 설정하면, `window` 객체에 직접 `vite:prefetch` 이벤트를 dispatch해야 프리페치가 시작됩니다. 예를 들어, 페이지 로드 3초 후에 프리페치를 시작하려면:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 베이스 URL

Vite 번들링 결과물(에셋)을 CDN 등 다른 도메인에 배포하는 경우, 앱의 `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

설정 후 모든 에셋 URL 앞에 해당 값이 접두어로 추가됩니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite가 변환하지 않으므로](#url-processing), 접두어가 추가되지 않습니다.

<a name="environment-variables"></a>
## 환경 변수

`.env`에 `VITE_`로 시작하는 환경 변수는 JavaScript로 주입됩니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

JavaScript에서는 아래처럼 접근 가능합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트 시 Vite 비활성화

Laravel의 Vite 통합은 테스트 실행 시에도 에셋을 처리하려 시도하므로, 개발 서버를 실행 중이거나 에셋이 빌드되어 있어야 합니다.

테스트 시 Vite를 목(mock)으로 대체하고 싶다면, Laravel의 `TestCase` 클래스를 확장한 테스트에서 `withoutVite` 메서드를 사용할 수 있습니다:

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

전체 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase`의 `setUp`에서 `withoutVite`를 호출하세요:

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

Laravel Vite 플러그인은 Vite 기반의 SSR 환경을 쉽게 구축할 수 있게 해줍니다.  
먼저 `resources/js/ssr.js`에 SSR 전용 엔트리 포인트 파일을 만들고, 아래처럼 플러그인 옵션으로 지정합니다:

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

SSR 엔트리 포인트 누락 방지를 위해 `package.json`의 "build" 스크립트를 다음처럼 수정해 SSR 빌드를 추가하세요:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

SSR 서버 빌드 및 실행은 아래처럼 할 수 있습니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia와 SSR 지원](https://inertiajs.com/server-side-rendering)을 사용하는 경우, `inertia:start-ssr` 아티즌 명령어로 SSR 서버를 시작할 수도 있습니다:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel [스타터 키트](/docs/{{version}}/starter-kits)는 Inertia SSR, Vite를 위한 최적 구성을 이미 포함하고 있습니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그의 속성

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) Nonce

[콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 적용하기 위해 script/style 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가하고 싶다면, 커스텀 [미들웨어](/docs/{{version}}/middleware)에서 `useCspNonce` 메서드를 사용하세요:

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

`useCspNonce` 호출 후에는 라라벨이 자동으로 nonce 속성을 모든 script, style 태그에 포함시켜 줍니다.

또한, [Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등 다른 곳에서도 nonce가 필요하다면, `cspNonce` 메서드로 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 생성한 nonce가 있다면, `useCspNonce($nonce)` 식으로 직접 지정할 수도 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI)

Vite manifest에 `integrity` 해시가 포함된 경우, Laravel은 자동으로 스크립트와 스타일 태그에 `integrity` 속성을 추가해 [서브리소스 무결성(Subresource Integrity)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용합니다.  
Vite는 기본적으로 manifest에 해시를 추가하지 않으므로, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) 플러그인을 설치해 활성화하세요:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

다음처럼 `vite.config.js`에 플러그인 추가:

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

필요하다면 무결성 해시가 저장되는 manifest 키를 커스터마이징할 수도 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

반드시 자동 감지를 끄고 싶다면 아래처럼 설정하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의의 속성 추가

script/style 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등 추가 속성이 필요하다면, `useScriptTagAttributes`, `useStyleTagAttributes` 메서드를 통해 설정할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성값 지정 예시
    'async' => true, // 값 없는 속성
    'integrity' => false, // 기본 포함 속성 제외 처리
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 속성을 추가하려면 콜백을 넘겨, 에셋 소스, URL, manifest 정보를 받을 수 있습니다:

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
> Vite 개발 서버 실행 중에는 `$chunk`와 `$manifest` 인자가 null일 수 있습니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

라라벨의 Vite 플러그인은 대부분의 앱에 적합한 기본 convention을 사용합니다.  
보다 세밀한 제어가 필요하다면, 아래처럼 `@vite` Blade 디렉티브 대신 다양한 커스텀 메서드를 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 지정
            ->useBuildDirectory('bundle') // 빌드 디렉터리 변경
            ->useManifestFilename('assets.json') // manifest 파일명 변경
            ->withEntryPoints(['resources/js/app.js']) // 엔트리 포인트 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋의 백엔드 경로 직접 생성
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js`에서도 동일한 옵션을 지정해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot',
            buildDirectory: 'bundle',
            input: ['resources/js/app.js'],
        }),
    ],
    build: {
      manifest: 'assets.json',
    },
});
```

<a name="cors"></a>
### 개발 서버 Cross-Origin Resource Sharing(CORS)

Vite 개발 서버에서 에셋을 불러올 때 CORS 문제가 생길 경우, 맞춤 도메인(origin)에 대한 접근 권한을 부여해야 합니다.  
라라벨 플러그인이 기본으로 허용하는 origin은 다음과 같습니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트의 `.env`에 지정한 `APP_URL`

커스텀 origin을 추가하려면, 앱의 `APP_URL`을 브라우저에서 접속하는 origin과 일치시키세요.  
예: `https://my-app.laravel`로 접속한다면 `.env`를 아래처럼 수정:

```env
APP_URL=https://my-app.laravel
```

여러 origin 등 세밀한 통제가 필요하다면 [Vite의 CORS 서버 옵션](https://vite.dev/config/server-options.html#server-cors)을 활용하세요. 예를 들어, 여러 origin을 허용하려면:

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

정규표현식을 이용해 특정 TLD 전체를 허용할 수도 있습니다(`*.laravel` 등):

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
                // 예시: SCHEME://DOMAIN.laravel[:PORT]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 보정

Vite 생태계의 일부 플러그인은 슬래시(`/`)로 시작하는 URL이 무조건 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel 통합 환경에서는 반드시 그런 것이 아니므로 URL을 수정해야 할 수 있습니다.

예를 들어 [vite-imagetools] 플러그인은 개발 서버에서 아래처럼 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

이 때는 `vite.config.js`의 `transformOnServe` 옵션으로 URL을 보정할 수 있습니다.  
예시는 다음과 같습니다:

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

이제 에셋이 Vite 개발 서버로부터 제공될 때 URL이 올바르게 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```