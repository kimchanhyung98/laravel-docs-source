# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 셋업](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 구성](#configuring-vite)
  - [스크립트 및 스타일 로딩](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 작업](#working-with-scripts)
  - [별칭](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 작업](#working-with-stylesheets)
- [Blade 및 라우트 작업](#working-with-blade-and-routes)
  - [Vite로 정적 자산 처리](#blade-processing-static-assets)
  - [저장 시 새로 고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 프리페칭](#asset-prefetching)
- [커스텀 기본 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화하기](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책 (CSP) 논스](#content-security-policy-csp-nonce)
  - [서브리소스 무결성 (SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS](#cors)
  - [개발 서버 URL 보정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션을 위해 코드를 번들링하는 최신 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 구축할 때, 일반적으로 Vite를 사용하여 애플리케이션의 CSS 및 JavaScript 파일을 프로덕션에 적합한 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공함으로써, 개발 및 프로덕션 환경에서 에셋을 간편하게 로드할 수 있도록 Vite와 완벽하게 통합됩니다.

<a name="installation"></a>
## 설치 및 셋업 (Installation & Setup)

> [!NOTE]  
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 구성하는 방법에 대해 설명합니다. 그러나 Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이러한 모든 설정이 이미 포함되어 있어, Laravel과 Vite를 가장 빠르게 시작할 수 있습니다.

<a name="installing-node"></a>
### Node 설치 (Installing Node)

Vite와 Laravel 플러그인을 실행하기 전에 Node.js(16버전 이상)와 NPM이 설치되어 있어야 합니다:

```shell
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램을 사용해 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/12.x/sail)을 사용 중이라면 아래와 같이 Sail을 통해 Node와 NPM을 실행할 수 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치 (Installing Vite and the Laravel Plugin)

Laravel을 새로 설치하면 애플리케이션 디렉터리 루트에 `package.json` 파일이 있습니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하는 데 필요한 모든 내용이 포함되어 있습니다. 다음 명령어로 애플리케이션 프론트엔드 의존성을 설치하세요:

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 구성 (Configuring Vite)

Vite 구성은 프로젝트 루트의 `vite.config.js` 파일에서 이루어집니다. 필요에 따라 이 파일을 자유롭게 커스터마이징할 수 있으며, `@vitejs/plugin-vue`나 `@vitejs/plugin-react` 같은 다른 플러그인을 설치해 사용할 수도 있습니다.

Laravel Vite 플러그인을 사용할 때는 애플리케이션의 진입점(entry points)을 지정해야 합니다. 진입점은 JavaScript나 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass 같은 전처리 언어도 포함됩니다.

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

SPA(Single Page Application) 또는 Inertia 기반 애플리케이션을 빌드하는 경우, CSS 진입점을 포함하지 않고 Vite를 구성하는 것이 좋습니다:

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

대신 CSS는 JavaScript를 통해 임포트해야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js` 파일에서 아래와 같이 작성합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 다중 진입점과 [SSR 진입점](#ssr) 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 사용하기

로컬 개발 웹 서버가 HTTPS로 서비스를 제공한다면, Vite 개발 서버에 연결하는 데 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용하고 사이트를 보안 처리하거나, [Laravel Valet](/docs/12.x/valet)에서 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행한 경우, Laravel Vite 플러그인은 자동으로 생성된 TLS 인증서를 인식해 사용합니다.

만약 사이트를 애플리케이션 디렉터리 이름과 다른 호스트로 보안 처리했다면, `vite.config.js` 파일에서 수동으로 호스트를 지정할 수 있습니다:

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

다른 웹 서버를 사용한다면, 신뢰할 수 있는 인증서를 생성하고 Vite를 수동으로 구성해야 합니다:

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

만약 시스템에 신뢰할 수 있는 인증서 생성이 어렵다면, [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하여 구성할 수 있습니다. 신뢰되지 않은 인증서를 사용할 때는 `npm run dev` 명령어 실행 후 콘솔에 나타나는 "Local" 링크를 따라가 브라우저에서 인증서 경고를 허용해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행하기

Windows Subsystem for Linux 2 (WSL2)의 [Laravel Sail](/docs/12.x/sail) 환경에서 Vite 개발 서버를 실행할 경우, 브라우저와 개발 서버 간 통신을 위해 `vite.config.js` 파일에 다음 설정을 추가해야 합니다:

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

개발 서버가 실행 중인데 파일 변경 사항이 브라우저에 반영되지 않는 경우, Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 구성해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 로딩 (Loading Your Scripts and Styles)

Vite 진입점을 구성했으면, 이제 애플리케이션 루트 템플릿의 `<head>`에서 `@vite()` Blade 디렉티브로 참조할 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript를 통해 임포트하는 경우에는 JavaScript 진입점만 포함하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지해 Vite 클라이언트를 삽입하여 핫 모듈 교체를 활성화합니다. 빌드 모드에서는 컴파일되고 버전 관리된 에셋, 그리고 임포트된 CSS까지 로드합니다.

필요하다면, `@vite` 디렉티브 호출 시 컴파일된 에셋의 빌드 경로를 지정할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 경로 상대입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋 (Inline Assets)

때로는 버전 관리된 URL 링크 대신 에셋의 원본 내용을 포함해야 할 때가 있습니다. 예를 들어 PDF 생성기 등으로 HTML 콘텐츠를 전달할 때 필요할 수 있습니다. `Vite` 파사드의 `content` 메서드로 Vite 에셋의 내용을 출력할 수 있습니다:

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
## Vite 실행 (Running Vite)

Vite 실행 방법은 두 가지입니다. 로컬 개발 중에는 `dev` 명령어로 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경을 자동으로 감지해 열려 있는 브라우저에 즉시 반영합니다.

또 다른 방법은 `build` 명령어를 실행해 애플리케이션 에셋을 버전 관리하고 번들링하여 프로덕션 배포를 준비하는 것입니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 관리...
npm run build
```

WSL2에서 [Sail](/docs/12.x/sail)을 사용해 개발 서버를 실행 중이라면, [추가 구성](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 작업 (Working With JavaScript)

<a name="aliases"></a>
### 별칭 (Aliases)

Laravel 플러그인은 기본적으로 자주 사용하는 경로에 바로 접근할 수 있도록 익숙한 별칭 하나를 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js`에서 별칭 `'@'`를 덮어써서 자신만의 별칭을 지정할 수도 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 구축하고자 할 경우, `@vitejs/plugin-vue` 플러그인을 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-vue
```

이후 `vite.config.js` 파일에 플러그인을 추가합니다. Laravel과 함께 Vue 플러그인을 사용할 때는 몇 가지 추가 옵션이 필요합니다:

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
                    // Vue 플러그인은 싱글 파일 컴포넌트 내에서 참조된
                    // 에셋 URL을 Laravel 웹 서버를 가리키도록 재작성합니다.
                    // 이를 `null`로 설정하면 Laravel 플러그인이
                    // Vite 서버를 가리키도록 대신 재작성합니다.
                    base: null,

                    // Vue 플러그인은 절대 URL을 파일 시스템의 절대 경로로 인식합니다.
                    // `false`로 설정하면 절대 URL 그대로 두어 public 디렉터리 내 에셋을 참조할 수 있습니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이미 적절한 Laravel, Vue, Vite 구성이 포함되어 있습니다. 이 스타터 킷들이 Laravel, Vue, Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크를 사용하려면, `@vitejs/plugin-react` 플러그인을 설치해야 합니다:

```shell
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

JSX가 포함된 파일은 `.jsx` 또는 `.tsx` 확장자를 가져야 하며, 필요하다면 진입점도 위 예시처럼 변경해 줍니다.

또한 기존 `@vite` 디렉티브와 함께 `@viteReactRefresh` Blade 디렉티브를 추가해야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite`보다 먼저 호출되어야 합니다.

> [!NOTE]  
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이미 적절한 Laravel, React, Vite 구성이 포함되어 있습니다. 이 스타터 킷들이 Laravel, React, Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인에서 제공하는 `resolvePageComponent` 함수는 Inertia 페이지 컴포넌트를 간편하게 해결할 수 있도록 도와줍니다. 아래 예시는 Vue 3에서의 사용법이며, React 등 다른 프레임워크에서도 활용할 수 있습니다:

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

Vite의 코드 분할 기능을 Inertia와 함께 사용한다면, [에셋 프리페칭](#asset-prefetching) 구성을 권장합니다.

> [!NOTE]  
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이미 적절한 Laravel, Inertia, Vite 구성이 포함되어 있습니다. 이 스타터 킷들이 Laravel, Inertia, Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite로 애플리케이션의 HTML, CSS, JS 내에서 에셋을 참조할 때 몇 가지 주의할 점이 있습니다. 절대 경로를 사용해 에셋을 참조하면, Vite가 해당 에셋을 빌드에 포함하지 않으므로 public 디렉터리에 해당 에셋이 있어야 합니다. 특히 [전용 CSS 진입점](#configuring-vite)을 사용하는 경우, 개발 중 브라우저가 Vite 개발 서버에서 CSS를 로드하려고 하므로 절대 경로 사용을 피해야 합니다.

반면 상대 경로로 에셋을 참조하면, 참조한 파일 기준 상대 경로가 되어 Vite가 경로를 재작성 및 버전 관리하고 번들링합니다.

예를 들어 다음과 같은 프로젝트 구조가 있다면:

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

다음과 같이 작동합니다:

```html
<!-- 이 에셋은 Vite에서 처리하지 않고 빌드에 포함되지 않습니다 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 재작성, 버전 관리, 번들링합니다 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업 (Working With Stylesheets)

> [!NOTE]  
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 Tailwind와 Vite 구성이 이미 포함되어 있습니다. 또는 스타터 킷 없이 Tailwind를 Laravel과 함께 쓰려면 [Tailwind 공식 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 애플리케이션은 Tailwind와 적절히 구성된 `vite.config.js`를 기본적으로 포함합니다. 따라서 Vite 개발 서버 또는 Composer `dev` 명령어를 실행하는 것만으로 Laravel과 Vite 개발 서버를 동시에 시작할 수 있습니다:

```shell
composer run dev
```

애플리케이션의 CSS는 보통 `resources/css/app.css` 파일에 위치합니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트 작업 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 자산 처리 (Processing Static Assets With Vite)

JavaScript나 CSS에서 에셋을 참조하면 Vite가 자동으로 처리하고 버전 관리를 수행합니다. Blade 기반 애플리케이션에서는 Vite가 Blade 템플릿 내에서만 참조하는 정적 에셋도 처리와 버전 관리를 해줄 수 있습니다.

하지만 이를 위해서는, 애플리케이션 진입점에서 정적 에셋을 임포트하여 Vite에게 에셋을 인지시켜야 합니다. 예를 들어 `resources/images`의 모든 이미지와 `resources/fonts`의 모든 폰트를 처리하고 싶다면, `resources/js/app.js` 진입점에 다음을 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build` 실행 시 해당 에셋을 처리하며, Blade 템플릿에서는 `Vite::asset` 메서드를 사용해 버전 관리된 URL을 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로 고침 (Refreshing on Save)

Blade를 사용하여 전통적인 서버 사이드 렌더링 기반 애플리케이션을 개발할 때, Vite는 뷰 파일 변경 시 브라우저를 자동 새로 고침하여 개발 생산성을 높여줍니다. 설정은 단순히 `refresh` 옵션을 `true`로 지정하는 것으로 시작할 수 있습니다:

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

이 옵션이 `true`일 때, 다음 경로에 저장된 파일 변경을 감지하면 `npm run dev` 실행 중 전체 페이지가 브라우저에서 새로 고쳐집니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**`를 감시하면 [Ziggy](https://github.com/tighten/ziggy)로 프론트엔드 라우트 링크 생성 시 도움됩니다.

기본 경로가 마음에 들지 않는다면, 감시할 경로 목록을 직접 지정할 수도 있습니다:

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

Laravel Vite 플러그인은 내부적으로 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 고급 옵션이 필요하면 아래처럼 `config` 정의를 할 수 있습니다:

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
### 별칭 (Aliases)

JavaScript 애플리케이션에서 흔히 사용하는 [별칭](#aliases)을 Blade에서도 사용하려면, `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 활용할 수 있습니다. 보통은 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에 정의합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

정의한 매크로는 템플릿에서 다음과 같이 사용할 수 있습니다. 예를 들어, 위 `image` 매크로를 이용해 `resources/images/logo.png` 에셋을 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 프리페칭 (Asset Prefetching)

Vite의 코드 분할 기능을 사용하는 SPA를 빌드할 때, 페이지 네비게이션 시 필요한 에셋이 각 페이지마다 로드되므로 UI 렌더링이 지연될 수 있습니다. 이런 문제를 해결하기 위해 Laravel은 초기 페이지 로드 시 애플리케이션 JavaScript 및 CSS 에셋을 적극적으로 미리 가져오는 프리페칭 기능을 제공합니다.

`[서비스 프로바이더](/docs/12.x/providers)`의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출하면 프리페칭이 활성화됩니다:

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

위 예제는 페이지 로드 시 최대 `3`개의 동시 다운로드로 에셋을 프리페칭합니다. 필요에 따라 동시성(concurrency)을 조정하거나, 모든 에셋을 한 번에 다운로드하려면 다음처럼 동시 제한 없이 호출할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 프리페칭은 [페이지 _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 시작 시점을 바꾸고 싶다면 프리페칭을 시작할 이벤트명을 지정할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위와 같이 설정하면, `window` 객체에서 직접 `vite:prefetch` 이벤트를 디스패치할 때 프리페칭이 시작됩니다. 예를 들어 페이지 로드 후 3초 뒤에 프리페칭을 시작할 수 있습니다:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 기본 URL (Custom Base URLs)

Vite 컴파일된 에셋이 애플리케이션과 다른 도메인(예: CDN)에 배포된 경우, 애플리케이션의 `.env` 파일에 `ASSET_URL` 환경 변수를 설정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

설정 후에는 모든 재작성된 에셋 URL에 지정한 링크가 접두사로 붙습니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

참고로 [절대 URL은 Vite에서 재작성하지 않습니다](#url-processing). 따라서 자동 접두사가 붙지 않으니 주의하세요.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

애플리케이션의 `.env` 파일에서 `VITE_` 접두사를 붙여 환경 변수를 정의하면, 해당 값이 JavaScript에 주입됩니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 JavaScript 내 `import.meta.env` 객체를 통해 접근할 수 있습니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화하기 (Disabling Vite in Tests)

Laravel의 Vite 통합은 테스트 실행 시 에셋을 해결하려고 시도하기 때문에, 개발 서버를 실행하거나 에셋을 빌드해야 합니다.

테스트 중 Vite를 모킹(mocking)하고 싶다면, Laravel의 `TestCase`를 확장한 테스트 클래스에서 `withoutVite` 메서드를 호출하면 됩니다:

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

모든 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에 `withoutVite` 호출을 추가하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void // [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    } // [tl! add:end]
}
```

<a name="ssr"></a>
## 서버 사이드 렌더링 (SSR) (Server-Side Rendering (SSR))

Laravel Vite 플러그인을 사용하면 Vite 기반 서버 사이드 렌더링(SSR)을 쉽게 설정할 수 있습니다. 우선 `resources/js/ssr.js` 위치에 SSR 진입점을 만들고, Laravel 플러그인 설정에 해당 경로를 명시합니다:

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

SSR 진입점 빌드를 잊지 않도록, `package.json`의 `"build"` 스크립트를 이렇게 변경하는 걸 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

그 다음, SSR 서버 빌드 및 시작은 아래 명령어를 사용합니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

Inertia와 함께 SSR을 사용하는 경우, `inertia:start-ssr` Artisan 명령어를 사용해 SSR 서버를 시작할 수 있습니다:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel의 [스타터 킷](/docs/12.x/starter-kits)에는 이미 적절한 Laravel, Inertia SSR, Vite 구성이 포함되어 있습니다. 이 스타터 킷들이 Laravel, Inertia SSR, Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책 (CSP) 논스 (Content Security Policy (CSP) Nonce)

스크립트 및 스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함해 [콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 강화하고 싶다면, 직접 생성하거나 지정한 nonce 값을 커스텀 [미들웨어](/docs/12.x/middleware)에서 `useCspNonce` 메서드를 사용해 지정할 수 있습니다:

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
     * 인커밍 요청 처리
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

`useCspNonce` 호출 후, Laravel은 생성하는 모든 스크립트 및 스타일 태그에 자동으로 `nonce` 속성을 붙입니다.

`Ziggy`의 `@route` 디렉티브 등 다른 곳에서 nonce 값을 지정하려면 다음처럼 `cspNonce` 메서드를 사용해 획득할 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 nonce를 보유하고 있을 경우 `useCspNonce`에 직접 넘겨줄 수 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성 (SRI) (Subresource Integrity (SRI))

Vite 매니페스트에 에셋 무결성 해시(`integrity`)가 포함되어 있으면, Laravel은 스크립트 및 스타일 태그에 `integrity` 속성을 자동으로 추가하여 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용합니다. 기본적으로 Vite는 무결성 해시를 매니페스트에 포함하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치해 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

이후 `vite.config.js` 파일에서 플러그인을 활성화합니다:

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

무결성 해시가 저장된 매니페스트 키를 커스터마이징할 필요가 있다면 다음을 사용하세요:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

완전히 무결성 자동 감지를 비활성화하려면 `false`를 넘기면 됩니다:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성 (Arbitrary Attributes)

스크립트 및 스타일 태그에 `[data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change)` 같은 추가 속성을 붙이고 싶을 경우, `useScriptTagAttributes` 와 `useStyleTagAttributes` 메서드를 통상 [서비스 프로바이더](/docs/12.x/providers)에서 호출해 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값이 있는 속성 지정
    'async' => true, // 값 없는 속성 지정
    'integrity' => false, // 기본 포함 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

속성을 조건부로 추가해야 한다면, 자산 소스 경로와 URL, 청크 정보, 매니페스트 전체를 인자로 받는 콜백을 넘길 수 있습니다:

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
> `$chunk`과 `$manifest` 인자는 Vite 개발 서버 실행 중에는 `null`입니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징 (Advanced Customization)

Laravel Vite 플러그인은 기본적으로 대부분의 애플리케이션에 적절한 관례를 사용하지만, 필요에 따라 Vite 동작을 더욱 세밀하게 조정할 수 있습니다. 기본 `@vite` Blade 디렉티브 대신 다음 메서드 체인을 사용해 설정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // hot 파일 커스터마이징...
            ->useBuildDirectory('bundle') // 빌드 디렉터리 커스터마이징...
            ->useManifestFilename('assets.json') // 매니페스트 파일명 커스터마이징...
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋 백엔드 경로 생성 커스터마이징...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js` 파일에도 동일한 구성 옵션을 지정해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // hot 파일 커스터마이징...
            buildDirectory: 'bundle', // 빌드 디렉터리 커스터마이징...
            input: ['resources/js/app.js'], // 진입점 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 커스터마이징...
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS (Dev Server Cross-Origin Resource Sharing (CORS))

Vite 개발 서버에서 에셋을 불러오며 브라우저에서 CORS 이슈가 발생할 경우, 개발 서버에 접근할 맞춤 출처(origin)를 허용해야 합니다. Laravel 플러그인과 Vite는 다음 출처들을 기본 허용합니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env`의 `APP_URL`

가장 간단한 방법은 브라우저에서 접근하는 출처와 애플리케이션의 `APP_URL` 환경 변수를 일치시키는 것입니다. 예를 들어 브라우저에서 `https://my-app.laravel`에 접근한다면, `.env` 파일에 다음과 같이 작성합니다:

```env
APP_URL=https://my-app.laravel
```

복수 출처를 지원하거나 더 세밀한 제어가 필요하면, [Vite의 CORS 서버 설정](https://vite.dev/config/server-options.html#server-cors)을 활용할 수 있습니다. 예를 들어 `vite.config.js`에서 여러 출처를 지정할 수 있습니다:

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

정규 표현식도 지정할 수 있어서, 예컨대 `*.laravel`같은 최상위 도메인 전체를 허용할 수도 있습니다:

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
                // SCHEME://DOMAIN.laravel[:PORT] 를 지원합니다. [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 보정 (Correcting Dev Server URLs)

Vite 생태계의 일부 플러그인은 URL이 슬래시(`/`)로 시작하면 항상 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel 통합 특성상 그렇지 않을 수 있습니다.

예를 들어, `vite-imagetools` 플러그인은 다음처럼 Vite 서비스 중인 상태에서 URL을 내보냅니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

`vite-imagetools`는 `/@imagetools`로 시작하는 URL을 Vite가 처리한다고 가정합니다. 이런 플러그인을 사용한다면, URL을 수동으로 수정해야 하며 `vite.config.js`에서 `transformOnServe` 옵션을 사용해 해결할 수 있습니다.

다음은 `transformOnServe`를 사용해 모든 `/@imagetools` 발생 위치에 개발 서버 URL을 붙이는 예입니다:

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

이제 Vite가 에셋을 서비스할 때, 아래처럼 개발 서버 URL이 포함된 올바른 URL을 출력합니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```