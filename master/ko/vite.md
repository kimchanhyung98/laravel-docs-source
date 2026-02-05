# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트와 스타일 로딩](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 다루기](#working-with-scripts)
  - [별칭](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade 및 라우트와 함께 사용하기](#working-with-blade-and-routes)
  - [Vite를 활용한 정적 에셋 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 사전 패칭(prefetching)](#asset-prefetching)
- [커스텀 Base URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책(CSP) Nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의의 속성](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 수정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고 코드를 프로덕션용으로 번들링해 주는 최신 프론트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때, 보통 Vite를 이용해 애플리케이션의 CSS와 JavaScript 파일을 프로덕션에 적합한 에셋으로 번들링하게 됩니다.

Laravel은 공식 플러그인과 Blade 지시어(Directive)를 제공하여 Vite와 완벽하게 연동할 수 있도록 지원합니다. 이를 통해 개발 환경과 프로덕션 환경 모두에서 에셋을 편리하게 로드할 수 있습니다.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]
> 다음 문서들은 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 다룹니다. 하지만 Laravel의 [스타터 키트](/docs/master/starter-kits)에는 이미 이러한 기본 설정이 포함되어 있으므로, Laravel과 Vite를 가장 빠르게 시작하려면 스타터 키트를 사용하는 것이 좋습니다.

<a name="installing-node"></a>
### Node 설치 (Installing Node)

Vite와 Laravel 플러그인을 실행하기 전에, Node.js(16 이상)와 NPM이 설치되어 있어야 합니다:

```shell
node -v
npm -v
```

최신 버전의 Node 및 NPM은 [공식 Node 웹사이트](https://nodejs.org/en/download/)의 그래픽 설치 프로그램을 이용해 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/master/sail)을 사용하는 경우, Sail을 통해 Node 및 NPM을 실행할 수도 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치 (Installing Vite and the Laravel Plugin)

Laravel을 처음 설치하면, 애플리케이션의 루트 디렉터리 구조에 `package.json` 파일이 있습니다. 기본 `package.json` 파일에는 이미 Vite와 Laravel 플러그인을 시작하는 데 필요한 모든 내용이 포함되어 있습니다. 다음 명령어로 프론트엔드 의존성을 설치하세요:

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 설정 (Configuring Vite)

Vite는 프로젝트 루트에 위치한 `vite.config.js` 파일로 설정합니다. 이 파일은 필요에 따라 자유롭게 커스터마이즈할 수 있으며, 애플리케이션에 필요한 추가 플러그인(`@vitejs/plugin-vue` 또는 `@vitejs/plugin-react` 등)도 추가할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 엔트리 포인트를 지정해야 합니다. 엔트리 포인트는 JavaScript 또는 CSS 파일일 수 있고, TypeScript, JSX, TSX, Sass 등과 같은 전처리 언어도 포함됩니다.

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

SPA(싱글 페이지 애플리케이션) 혹은 Inertia를 사용할 때에는 CSS 엔트리 포인트 없이 동작하는 것이 가장 좋습니다:

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

대신, JavaScript를 통해 CSS를 직접 import 하세요. 일반적으로는 애플리케이션의 `resources/js/app.js` 파일에서 다음과 같이 import 합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 개의 엔트리 포인트와 [SSR 엔트리 포인트](#ssr)와 같은 고급 설정도 지원합니다.

#### 보안 개발 서버와 함께 사용하기 (Working With a Secure Development Server)

로컬 개발 웹 서버가 HTTPS로 애플리케이션을 제공하는 경우, Vite 개발 서버와의 연결에 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용하여 사이트를 보안 처리했거나, [Laravel Valet](/docs/master/valet)에서 [secure 명령어](/docs/master/valet#securing-sites)를 실행한 경우라면, Laravel Vite 플러그인은 자동으로 생성된 TLS 인증서를 인식하여 사용합니다.

만약 사이트가 애플리케이션 디렉터리 이름과 일치하지 않는 호스트로 보안 처리되었다면, `vite.config.js` 파일에서 수동으로 호스트를 지정할 수 있습니다:

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

다른 웹 서버를 사용하는 경우, 신뢰할 수 있는 인증서를 생성하고 Vite에 이를 직접 설정해야 합니다:

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

시스템에서 신뢰할 수 있는 인증서를 생성할 수 없는 경우, [@vitejs/plugin-basic-ssl](https://github.com/vitejs/vite-plugin-basic-ssl) 플러그인을 설치해 설정할 수 있습니다. 신뢰할 수 없는 인증서를 사용할 때는 `npm run dev`를 실행한 후 콘솔의 "Local" 링크를 따라 브라우저에서 인증서 경고를 수동으로 승인해야 합니다.

#### WSL2에서 Sail로 개발 서버 실행 (Running the Development Server in Sail on WSL2)

Windows Subsystem for Linux 2(WSL2)에서 [Laravel Sail](/docs/master/sail) 내에서 Vite 개발 서버를 실행할 때는, 브라우저가 개발 서버와 통신할 수 있도록 다음과 같이 `vite.config.js`에 설정을 추가해야 합니다:

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

개발 서버가 실행 중임에도 파일 변경 사항이 브라우저에 반영되지 않는다면, Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)을 함께 설정해 보시기 바랍니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 로딩 (Loading Your Scripts and Styles)

Vite 엔트리 포인트를 설정한 이후, 애플리케이션의 루트 템플릿 `<head>`에 `@vite()` Blade 지시어를 추가해서 엔트리 포인트를 참조할 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript로 import하는 경우, JavaScript 엔트리 포인트만 포함하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 지시어는 Vite 개발 서버를 자동으로 감지하여 핫 모듈 리플레이스먼트(Hot Module Replacement)가 가능하도록 Vite 클라이언트를 삽입합니다. 빌드 모드에서는 컴파일 및 버전이 지정된 에셋(및 import 된 CSS 포함)을 로드합니다.

필요에 따라 `@vite` 지시어를 사용할 때 컴파일된 에셋의 빌드 경로를 명시적으로 지정할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- 주어진 빌드 경로는 public 경로를 기준으로 상대적입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

#### 인라인 에셋 (Inline Assets)

경우에 따라 에셋의 버전 URL이 아닌, 에셋의 원본 내용을 페이지에 직접 포함해야 할 때가 있습니다. 예를 들어, HTML을 PDF 생성기로 전달할 때 에셋 내용을 직접 넣어야 할 수 있습니다. 이처럼 Vite 에셋의 내용을 출력할 때는 `Vite` 파사드의 `content` 메서드를 사용할 수 있습니다:

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

Vite를 실행하는 방법은 두 가지가 있습니다. 개발 과정에서는 `dev` 명령어로 개발 서버를 실행할 수 있습니다. 개발 서버는 파일 변경을 자동으로 감지해 모든 열린 브라우저 창에서 즉시 반영합니다.

또는, `build` 명령어를 사용해 애플리케이션의 에셋을 번들링하고 버전을 지정하여 프로덕션 배포를 준비합니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 지정...
npm run build
```

[WSL2의 Sail](/docs/master/sail) 환경에서 개발 서버를 실행하는 경우, [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 다루기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭 (Aliases)

기본적으로, Laravel 플러그인은 애플리케이션 에셋을 좀 더 쉽게 import할 수 있도록 다음과 같은 공통 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js` 파일을 직접 수정하여 `'@'` 별칭을 덮어쓸 수도 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 개발하려면, `@vitejs/plugin-vue` 플러그인을 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-vue
```

설치 후, 해당 플러그인을 `vite.config.js` 설정 파일에 추가할 수 있습니다. Vue 플러그인을 Laravel과 함께 사용할 때는 몇 가지 추가 옵션이 필요합니다:

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
                    // Vue 플러그인은 싱글 파일 컴포넌트에서 참조된 에셋 URL을
                    // Laravel 웹 서버를 가리키도록 재작성합니다.
                    // base를 null로 설정하면, 대신 Vite 서버를 가리키도록
                    // Laravel 플러그인이 에셋 URL을 재작성할 수 있습니다.
                    base: null,

                    // 절대 URL을 파싱해 디스크상의 절대 경로로 처리하지 않도록
                    // false로 설정하면, public 디렉터리 내 에셋 참조가 가능해집니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)에는 이미 올바른 Laravel, Vue, Vite 설정이 포함되어 있습니다. 스타터 키트는 Laravel, Vue, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크로 프론트엔드를 개발하려면, `@vitejs/plugin-react` 플러그인을 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-react
```

설치 후, 해당 플러그인을 `vite.config.js` 설정 파일에 추가하세요:

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

JSX가 포함된 파일은 반드시 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 필요하다면 [위에서 설명한](#configuring-vite) 대로 엔트리 포인트도 변경하세요.

또한, 기존 `@vite` 지시어와 함께 `@viteReactRefresh` Blade 지시어도 추가해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh` 지시어는 반드시 `@vite` 지시어보다 먼저 호출되어야 합니다.

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)에는 이미 올바른 Laravel, React, Vite 설정이 포함되어 있습니다. 스타터 키트는 Laravel, React, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 쉽게 로드할 수 있도록 `resolvePageComponent` 함수를 제공합니다. 아래 예시는 Vue 3 버전으로 사용 방법을 보여주고 있지만, React 등 다른 프레임워크와 함께 사용할 수도 있습니다:

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

Inertia와 함께 Vite의 코드 분할(Code Splitting) 기능을 사용하는 경우, [에셋 사전 패칭](#asset-prefetching) 구성을 추천합니다.

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)에는 이미 올바른 Laravel, Inertia, Vite 설정이 포함되어 있습니다. 스타터 키트는 Laravel, Inertia, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite를 사용할 때 HTML, CSS, JS에서 에셋을 참조할 때 유의할 점이 몇 가지 있습니다. 먼저, 절대 경로로 에셋을 참조하면 Vite는 해당 에셋을 빌드에 포함하지 않습니다. 이 경우, public 디렉터리에 에셋이 있는지 반드시 확인해야 하며, [전용 CSS 엔트리포인트](#configuring-vite)를 사용하는 경우에는 절대 경로 참조를 피해야 합니다. 개발 중에는 브라우저가 Vite 서버에서 CSS를 불러오므로, public 디렉터리에 있는 에셋은 로드되지 않을 수 있습니다.

상대 경로로 참조하는 경우, 참조 경로는 현재 파일의 위치를 기준으로 하므로 유의해야 합니다. 상대 경로로 참조된 에셋은 Vite가 자동으로 URL을 재작성하고, 버전을 붙이며, 번들링합니다.

프로젝트 구조 예시는 다음과 같습니다:

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

아래 예시는 Vite가 상대/절대 URL을 어떻게 처리하는지 보여줍니다:

```html
<!-- 이 에셋은 Vite가 처리하지 않으며 빌드에 포함되지 않습니다 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 자동으로 URL을 재작성하고, 버전 지정하며, 번들링합니다 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기 (Working With Stylesheets)

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)에는 올바른 Tailwind 및 Vite 설정이 이미 포함되어 있습니다. 또는 스타터 키트를 사용하지 않고 Tailwind와 Laravel을 조합하려면 [Tailwind의 Laravel 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

모든 Laravel 애플리케이션에는 이미 Tailwind와 제대로 설정된 `vite.config.js` 파일이 포함되어 있습니다. 따라서 Vite 개발 서버를 실행하거나, `dev` Composer 명령어로 Laravel과 Vite 개발 서버를 동시에 실행하면 됩니다:

```shell
composer run dev
```

애플리케이션의 CSS 파일은 `resources/css/app.css`에 위치할 수 있습니다.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트와 함께 사용하기 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite를 활용한 정적 에셋 처리 (Processing Static Assets With Vite)

JavaScript 또는 CSS에서 에셋을 참조하면 Vite가 자동으로 에셋을 처리하고 버전 지정합니다. Blade 기반 애플리케이션에서는, Blade 템플릿에서만 참조하는 정적 에셋도 Vite가 처리하고 버전 지정할 수 있습니다.

이를 위해서는, 애플리케이션의 엔트리 포인트에서 정적 에셋을 import 하여 Vite에 해당 에셋의 존재를 알려야 합니다. 예를 들어, `resources/images`에 저장된 모든 이미지와 `resources/fonts`의 모든 폰트를 처리하고 싶다면, 다음과 같이 `resources/js/app.js` 엔트리 포인트에 추가합니다:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build`를 실행하면 Vite가 해당 에셋을 처리합니다. 이후 Blade 템플릿에서는 `Vite::asset` 메서드를 사용해 버전이 지정된 에셋의 URL을 얻을 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침 (Refreshing on Save)

Blade를 이용한 전통적 서버사이드 렌더링 애플리케이션 개발 시, 파일을 수정할 때 브라우저가 자동으로 새로고침되면 개발 효율이 크게 향상됩니다. Vite의 `refresh` 옵션을 `true`로 지정하면 간단하게 이 기능을 활성화할 수 있습니다.

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

`refresh` 옵션이 `true`이면, 아래 디렉터리 내 파일이 저장될 때 브라우저가 전체 페이지 새로고침을 수행합니다(`npm run dev` 실행 중일 때):

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 디렉터리 감시는, 프런트엔드에서 경로 링크를 동적으로 생성하는 [Ziggy](https://github.com/tighten/ziggy)를 활용할 때 유용합니다.

이 기본 경로가 필요에 맞지 않으면, 감시할 경로 목록을 명시적으로 지정할 수도 있습니다:

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

Laravel Vite 플러그인 내부적으로는 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하여 고급 설정도 지원합니다. 세밀한 동작 조정이 필요할 경우 `config` 정의로 직접 옵션을 지정할 수 있습니다:

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

JavaScript 애플리케이션에서는 디렉터리 참조를 편하게 하기 위해 [별칭을 만드는 것](#aliases)이 흔합니다. Blade에서도 비슷하게 별칭을 만들 수 있는데, `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용합니다. 보통 이런 "매크로"는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 정의합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

매크로를 정의한 뒤에는 Blade 템플릿에서 다음과 같이 참조할 수 있습니다. 예를 들어, 위에서 정의한 `image` 매크로를 사용해 `resources/images/logo.png` 에셋을 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 사전 패칭 (Asset Prefetching)

Vite의 코드 분할 기능을 사용하여 SPA를 빌드할 때, 화면 간 페이지 이동마다 필요한 에셋을 별도로 다운로드하게 됩니다. 이 동작은 때때로 UI 렌더링 지연을 유발할 수 있습니다. 이런 문제가 있는 경우, Laravel에서는 최초 페이지 로드 시 JavaScript와 CSS 에셋을 미리 패칭(prefetch)하도록 설정할 수 있습니다.

서비스 프로바이더의 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출하면 에셋의 사전 패칭을 시작할 수 있습니다:

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

위 예시에서는 매 페이지 로드마다 최대 3개의 에셋을 동시에 사전 패칭하도록 설정하였습니다. 필요에 따라 동시성(concurrency)를 조절하거나 제한 없이 모든 에셋을 한 번에 다운로드하도록 설정할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 사전 패칭은 [page _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 만약 사전 패칭이 시작되는 시점을 커스터마이즈하고 싶다면, Vite가 감지할 이벤트명을 직접 지정할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위 설정대로라면, 이제 수동으로 `window` 객체에 `vite:prefetch` 이벤트를 디스패치할 때 사전 패칭이 시작됩니다. 예를 들어, 페이지 로드 3초 후에 사전 패칭을 시작할 수도 있습니다:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 Base URL (Custom Base URLs)

Vite로 빌드된 에셋을 애플리케이션과 별도의 도메인(CDN 등)으로 배포하는 경우, 애플리케이션의 `.env` 파일에서 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

에셋 URL을 설정하면, 에셋에 대한 모든 재작성된 URL 앞에 지정한 값이 자동으로 붙게 됩니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[Vite는 절대 URL을 재작성하지 않으므로](#url-processing), 절대 경로로 참조한 URL에는 접두사가 추가되지 않습니다.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

애플리케이션의 `.env` 파일에서 `VITE_` 접두사를 붙여 환경 변수를 정의하면, JavaScript 내에서 해당 변수를 주입받을 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 `import.meta.env` 객체에서 다음과 같이 접근할 수 있습니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화 (Disabling Vite in Tests)

Laravel의 Vite 통합은 테스트 실행 중에도 에셋을 로드하려고 시도하므로, 테스트 시에는 Vite 개발 서버가 실행 중이거나 에셋이 빌드되어 있어야 합니다.

테스트에서 Vite를 모킹(mock)하고 싶다면, Laravel의 `TestCase` 클래스를 확장한 테스트에서 `withoutVite` 메서드를 호출할 수 있습니다:

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

모든 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite`를 호출하세요:

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
## 서버 사이드 렌더링 (SSR) (Server-Side Rendering (SSR))

Laravel Vite 플러그인을 사용하면, Vite와 함께 서버 사이드 렌더링 환경을 쉽게 구축할 수 있습니다. 먼저, `resources/js/ssr.js` 파일에 SSR 엔트리 포인트를 생성하고, 플러그인 설정에서 엔트리 포인트를 지정합니다:

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

SSR 엔트리 포인트 빌드를 깜박하지 않기 위해, 애플리케이션의 `package.json` 내 `"build"` 스크립트를 다음과 같이 수정하는 것이 좋습니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이후, SSR 서버를 빌드하고 실행하려면 다음 명령어를 순서대로 실행하면 됩니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia의 SSR](https://inertiajs.com/server-side-rendering)을 사용하는 경우에는, 대신 `inertia:start-ssr` Artisan 명령어로 SSR 서버를 실행할 수 있습니다:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)에는 올바른 Laravel, Inertia SSR, Vite 설정이 포함되어 있습니다. 스타터 키트는 Laravel, Inertia SSR, Vite를 가장 빠르게 시작하는 방법을 제공합니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) Nonce (Content Security Policy (CSP) Nonce)

[콘텐츠 보안 정책(Content Security Policy)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로, 스크립트와 스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하고 싶다면, 커스텀 [미들웨어](/docs/master/middleware) 내에서 `useCspNonce` 메서드를 사용하여 nonce를 생성하거나 지정할 수 있습니다:

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

`useCspNonce` 메서드 호출 이후에는, Laravel이 생성하는 모든 스크립트 및 스타일 태그에 nonce가 자동으로 포함됩니다.

다른 곳(예: Laravel [스타터 키트](/docs/master/starter-kits)에서 제공하는 [Ziggy의 `@route` 지시어](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) 등)에서 직접 nonce를 지정할 필요가 있다면, `cspNonce` 메서드로 받아올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 nonce를 직접 생성한 경우, `useCspNonce` 메서드에 해당 값을 인자로 전달할 수도 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI) (Subresource Integrity (SRI))

Vite manifest에 에셋에 대한 `integrity` 해시가 포함되어 있다면, Laravel은 생성된 모든 스크립트 및 스타일 태그에 `integrity` 속성을 자동으로 추가하여 [서브리소스 무결성(Subresource Integrity)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 강제합니다. 기본적으로 Vite는 manifest에 `integrity` 해시를 포함하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하여 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

설치 후, `vite.config.js` 파일에서 해당 플러그인을 활성화하세요:

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

필요하다면, 무결성 해시가 저장된 manifest 키를 커스터마이즈 할 수도 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지를 완전히 비활성화하려면, `useIntegrityKey` 메서드에 false를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의의 속성 (Arbitrary Attributes)

스크립트와 스타일 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change)과 같은 추가 속성을 지정하려면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 사용할 수 있습니다. 흔히 이런 메서드는 [서비스 프로바이더](/docs/master/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성값을 지정...
    'async' => true, // 값 없는 속성 지정...
    'integrity' => false, // 기본적으로 포함될 속성은 제외...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 속성을 동적으로 추가하려면, 콜백을 전달할 수 있으며 콜백 인자로는 에셋 소스 경로, URL, manifest 청크, 전체 manifest가 넘어옵니다:

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
> Vite 개발 서버가 실행 중일 때는 `$chunk`와 `$manifest` 인자가 null이 됩니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징 (Advanced Customization)

Laravel Vite 플러그인은 기본적으로 대부분의 애플리케이션에 적합한 이상적인 규칙을 사용하지만, Vite의 동작을 추가로 커스터마이징해야 할 때도 있습니다. 추가적인 커스터마이징이 필요하다면, 아래와 같은 메서드 및 옵션을 활용하여 `@vite` Blade 지시어 대신 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 커스터마이즈...
            ->useBuildDirectory('bundle') // 빌드 디렉터리 커스터마이즈...
            ->useManifestFilename('assets.json') // manifest 파일명 커스터마이즈...
            ->withEntryPoints(['resources/js/app.js']) // 엔트리 포인트 지정...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드 에셋의 경로 생성 커스터마이즈...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js` 파일에서도 동일한 설정이 필요합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 지정...
            buildDirectory: 'bundle', // 빌드 디렉터리 지정...
            input: ['resources/js/app.js'], // 엔트리 포인트 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // manifest 파일명 커스터마이즈...
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS 설정 (Dev Server Cross-Origin Resource Sharing (CORS))

Vite 개발 서버에서 에셋을 가져올 때 브라우저에서 CORS 문제가 발생한다면, 해당 서버에 접속하는 오리진에 대한 접근 권한을 추가로 부여해야 할 수도 있습니다. Vite 및 Laravel 플러그인은 다음 오리진에 대해서는 별다른 설정 없이도 접근을 허용합니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env`의 `APP_URL`

프로젝트의 커스텀 오리진을 허용하려면, 애플리케이션의 `.env`의 `APP_URL` 값이 브라우저에서 접근하는 오리진과 일치하는지 확인하세요. 예를 들어, `https://my-app.laravel`에서 접속한다면, 다음과 같이 `.env` 파일을 수정해야 합니다:

```env
APP_URL=https://my-app.laravel
```

여러 오리진을 지원하거나 좀 더 세밀하게 오리진을 제어하려면 [Vite의 CORS 서버 설정](https://vite.dev/config/server-options.html#server-cors)을 활용하세요. 예를 들어, `vite.config.js`의 `server.cors.origin` 옵션에서 여러 오리진을 지정할 수 있습니다:

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

정규 표현식도 사용 가능하므로, 예를 들어 `*.laravel` 상위 도메인 전체를 허용할 수 있습니다:

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
### 개발 서버 URL 수정 (Correcting Dev Server URLs)

Vite 생태계의 일부 플러그인은 슬래시로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel에서 통합되어 사용할 때는 그렇지 않은 경우도 있습니다.

예를 들어, `vite-imagetools` 플러그인은 다음과 같이 URL을 출력할 수 있습니다(Vite가 에셋을 제공 중일 때):

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

`vite-imagetools` 플러그인은 `/@imagetools`로 시작하는 URL이 Vite에 의해 가로채질 것으로 기대합니다. 만약 이런 동작을 기대하는 플러그인을 사용한다면, URL을 직접 수정해줘야 합니다. `vite.config.js`의 `transformOnServe` 옵션을 활용하여 처리할 수 있습니다.

이 예시에서는, 생성된 코드 내에서 `/@imagetools`가 등장하는 모든 부분에 개발 서버 URL을 먼저 붙입니다:

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

이제 Vite가 에셋을 제공할 때 다음과 같이 개발 서버를 가리키는 URL로 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```
