# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 구성](#configuring-vite)
  - [스크립트 및 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [JavaScript 작업하기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 작업하기](#working-with-stylesheets)
- [Blade 및 라우트 작업하기](#working-with-blade-and-routes)
  - [Vite로 정적 자산 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭(Aliases)](#blade-aliases)
- [커스텀 베이스 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책(CSP) 논스(Nonce)](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 사용자 지정](#advanced-customization)
  - [개발 서버 URL 수정하기](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 코드를 프로덕션용으로 번들링하는 현대적인 프런트엔드 빌드 도구입니다. Laravel 애플리케이션을 구축할 때, 보통 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 프로덕션 준비가 된 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발과 프로덕션 환경에서 에셋을 쉽게 로드할 수 있도록 Vite와 원활하게 통합됩니다.

> [!NOTE]  
> Laravel Mix를 사용하고 계신가요? 새로운 Laravel 설치에서는 Laravel Mix 대신 Vite가 사용됩니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 웹사이트를 참고하세요. Vite로 전환하시려면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

과거에는 Laravel 신규 애플리케이션에서 [Mix](https://laravel-mix.com/)를 사용했으며, 이는 내부적으로 [webpack](https://webpack.js.org/)을 기반으로 합니다. Vite는 풍부한 JavaScript 애플리케이션을 빠르고 효율적으로 개발할 수 있도록 설계되었습니다. 특히 [Inertia](https://inertiajs.com) 같은 도구를 활용하는 싱글 페이지 애플리케이션(SPA) 개발에 적합합니다.

기존 서버 사이드 렌더링 애플리케이션에 JavaScript "강화"를 추가하는 경우에도 Vite는 잘 작동하며, [Livewire](https://livewire.laravel.com) 같은 툴을 사용하는 프로젝트에도 적합합니다. 다만, Laravel Mix에서 지원하는 것처럼, JavaScript 코드에서 직접 참조하지 않는 임의 에셋을 별도 복사하는 기능 등 일부 기능은 부족할 수 있습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 되돌아가기

만약 Vite 기반으로 새 Laravel 프로젝트를 시작했지만 다시 Laravel Mix와 webpack으로 전환해야 한다면 문제없습니다. [공식 Vite에서 Mix로의 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]  
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 안내합니다. 다만, Laravel의 [스타터 킷](/docs/10.x/starter-kits)에는 이미 해당 설정이 포함되어 있어서 Laravel과 Vite를 가장 빠르게 시작할 수 있습니다.

<a name="installing-node"></a>
### Node 설치 (Installing Node)

Vite와 Laravel 플러그인을 실행하기 전에 Node.js (16버전 이상)와 NPM이 설치되어 있는지 확인하세요:

```sh
node -v
npm -v
```

공식 Node 웹사이트([the official Node website](https://nodejs.org/en/download/))에서 간단한 그래픽 설치 프로그램으로 최신 버전을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/10.x/sail)을 사용하는 경우 Sail을 통해 Node와 NPM을 실행할 수 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치 (Installing Vite and the Laravel Plugin)

새로운 Laravel 설치를 보면 애플리케이션 루트 디렉토리에 `package.json` 파일이 있습니다. 기본 구성된 `package.json` 파일에 Vite와 Laravel 플러그인 사용에 필요한 모든 의존성이 이미 포함되어 있습니다. 다음 명령어로 프런트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 구성 (Configuring Vite)

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 자유롭게 이 파일을 커스터마이징할 수 있으며, `@vitejs/plugin-vue` 또는 `@vitejs/plugin-react` 같은 다른 플러그인도 설치해서 사용할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점(entry points)을 지정해야 합니다. 진입점은 JavaScript나 CSS 파일이며, TypeScript, JSX, TSX, Sass 같은 전처리 언어도 포함할 수 있습니다.

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

만약 Inertia 같은 SPA를 빌드한다면, CSS 진입점 없이 Vite를 사용하는 것이 가장 좋습니다:

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

대신 CSS는 JavaScript에서 import해야 합니다. 보통 `resources/js/app.js`에서 이렇게 처리합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 다중 진입점과 [SSR 진입점](#ssr) 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안이 적용된 개발 서버 사용하기

로컬 개발 웹 서버가 HTTPS를 통해 애플리케이션을 서비스하는 경우, Vite 개발 서버에 연결할 때 문제가 생길 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용해 사이트를 보안 설정했거나, [Laravel Valet](/docs/10.x/valet)에서 [secure 명령어](/docs/10.x/valet#securing-sites)를 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 탐지해 사용합니다.

만약 애플리케이션 디렉토리 이름과 다른 호스트명을 사용해 사이트를 보안 설정했다면, `vite.config.js` 파일에서 호스트를 직접 지정해야 할 수 있습니다:

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

다른 웹 서버를 사용한다면, 신뢰할 수 있는 인증서를 생성 후 Vite에 인증서 파일 경로를 직접 지정해야 합니다:

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

시스템에 신뢰할 수 있는 인증서를 생성할 수 없다면, [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치 후 구성할 수 있습니다. 신뢰되지 않은 인증서를 사용할 경우, `npm run dev` 실행 시 콘솔에 표시되는 "Local" 링크를 클릭해 브라우저에서 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2 환경에서 Sail 개발 서버용 HMR 설정

Windows Subsystem for Linux 2(WSL2)에서 [Laravel Sail](/docs/10.x/sail)을 사용 중이라면, 브라우저가 개발 서버와 통신할 수 있도록 아래 설정을 `vite.config.js`에 추가하세요:

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

개발 서버가 실행 중일 때 파일 변경 내용이 브라우저에 반영되지 않으면, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch) 역시 설정해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 불러오기 (Loading Your Scripts and Styles)

Vite 진입점 설정을 마쳤다면, 애플리케이션의 루트 템플릿 `<head>` 안에 `@vite()` Blade 디렉티브를 사용해 불러올 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

JavaScript 내에서 CSS를 import하는 경우, JavaScript 진입점만 불러오면 됩니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동으로 감지해 Hot Module Replacement용 클라이언트를 삽입하며, 빌드 모드에서는 컴파일되고 버전이 매겨진 에셋과 import된 CSS를 로드합니다.

필요하다면, `@vite` 호출 시 컴파일 결과물이 위치한 빌드 경로도 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 경로 기준 상대 경로입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋 (Inline Assets)

가끔 버전된 URL 대신 에셋의 원시 콘텐츠를 직접 포함해야 할 때도 있습니다. 예를 들어, PDF 생성 시 HTML 콘텐츠를 직접 전달해야 하는 경우입니다. 이럴 땐 `Vite` 파사드를 통해 `content` 메서드로 에셋 내용을 출력할 수 있습니다:

```blade
@php
use Illuminate\Support\Facades\Vite;
@endphp

<!doctype html>
<head>
    {{-- ... --}}

    
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```

<a name="running-vite"></a>
## Vite 실행하기 (Running Vite)

Vite를 실행하는 방법은 두 가지입니다. 로컬 개발 중에는 `dev` 명령어로 개발 서버를 실행하여 파일 변경 시 자동으로 브라우저에 즉시 반영되도록 할 수 있습니다.

또는 `build` 명령어를 실행하면 애플리케이션 에셋을 번들링 및 버전 관리하여 프로덕션 배포를 준비합니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 관리...
npm run build
```

WSL2 환경의 [Sail](/docs/10.x/sail)에서 개발 서버를 돌릴 경우, [추가 설정](#configuring-hmr-in-sail-on-wsl2)이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 작업하기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭(Aliases)

기본적으로 Laravel 플러그인은 빠른 시작을 돕기 위해 자주 사용하는 별칭 하나를 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

원한다면 `vite.config.js` 파일에 직접 별칭을 덮어쓸 수도 있습니다:

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

프런트엔드를 [Vue](https://vuejs.org/) 프레임워크로 작성하고 싶다면 `@vitejs/plugin-vue` 플러그인도 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

그후 `vite.config.js`에 Vue 플러그인을 추가하고, Laravel과 함께 사용할 때 필요한 추가 옵션을 지정하세요:

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
                    // Vue 플러그인은 Single File Components 내에서 참조한 에셋 URL을
                    // Laravel 웹 서버로 재작성합니다.
                    // null로 설정하면 Laravel 플러그인이 대신 Vite 서버로 URL을 수정합니다.
                    base: null,

                    // Vue 플러그인은 절대 URL을 파싱해 파일 시스템의 절대 경로라 판단합니다.
                    // false로 설정 시 절대 URL이 변경되지 않고 public 디렉토리 내 에셋을 가리킵니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel [스타터 킷](/docs/10.x/starter-kits)에는 Laravel, Vue, Vite 설정이 미리 포함되어 있습니다. 가장 빠른 시작 방법은 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="react"></a>
### React

프런트엔드를 [React](https://reactjs.org/)로 작성할 경우, `@vitejs/plugin-react` 플러그인 설치가 필요합니다:

```sh
npm install --save-dev @vitejs/plugin-react
```

설치 후 `vite.config.js` 에 React 플러그인을 포함하세요:

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

JSX 문법을 사용하는 파일들은 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 진입점도 필요시 적절히 업데이트하세요([위 내용](#configuring-vite) 참고).

또한 기존 `@vite` 디렉티브 옆에 추가로 `@viteReactRefresh` Blade 디렉티브도 포함해야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 `@vite` 앞에 위치해야 합니다.

> [!NOTE]  
> Laravel [스타터 킷](/docs/10.x/starter-kits)에는 Laravel, React, Vite 설정이 함께 포함되어 있습니다. 빠른 시작은 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 편리하게 해결하는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3 환경에서 해당 헬퍼를 사용하는 예시이며, React 등 다른 프레임워크에서도 사용할 수 있습니다:

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
> Laravel [스타터 킷](/docs/10.x/starter-kits)은 Laravel, Inertia, Vite 구성이 포함되어 있어, [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 통해 가장 빠르게 시작할 수 있습니다.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite를 사용할 때 애플리케이션의 HTML, CSS, JS에서 에셋을 참조하는 경우 주의할 점이 있습니다. 절대 경로로 참조하는 에셋은 Vite 빌드에 포함되지 않으므로, public 디렉토리에 해당 에셋이 반드시 존재해야 합니다.

상대 경로를 통해 참조하는 에셋은 Vite가 상대 경로를 기준으로 찾아서 재작성, 버전 관리, 번들링합니다.

다음 프로젝트 구조를 예로 보겠습니다:

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

아래 예시는 Vite가 상대 URL과 절대 URL을 어떻게 취급하는지 보여줍니다:

```html
<!-- 이 에셋은 Vite가 처리하지 않으며, 빌드에 포함되지 않습니다. -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 재작성, 버전 관리, 번들링합니다. -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업하기 (Working With Stylesheets)

Vite의 CSS 지원에 대해서는 [Vite 문서](https://vitejs.dev/guide/features.html#css)에서 자세히 확인할 수 있습니다. [Tailwind](https://tailwindcss.com) 같은 PostCSS 플러그인을 사용하는 경우, 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 자동 적용합니다:

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]  
> Laravel [스타터 킷](/docs/10.x/starter-kits)은 Tailwind, PostCSS, Vite 설정을 포함합니다. 또는 스타터 킷 없이 Tailwind와 Laravel을 사용하고 싶다면 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트 작업하기 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 자산 처리하기 (Processing Static Assets With Vite)

JavaScript나 CSS에서 에셋을 참조하면 Vite가 자동으로 처리하고 버전 관리합니다. Blade 템플릿 기반 애플리케이션을 빌드하는 경우, Blade 내에서만 사용하는 정적 에셋도 Vite가 처리하고 버전 관리를 할 수 있습니다.

이를 위해 엔트리 포인트에서 정적 에셋을 직접 import하여 Vite가 인지하도록 해야 합니다. 예를 들어 `resources/images` 폴더 내 이미지와 `resources/fonts` 내 글꼴 모두 처리하려면, 애플리케이션의 `resources/js/app.js` 엔트리 포인트에 다음과 같이 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

그 후 `npm run build` 시 Vite가 해당 에셋을 처리합니다. Blade 템플릿에서 `Vite::asset` 메서드로 해당 에셋의 버전된 URL을 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침 (Refreshing on Save)

Blade 기반 서버 사이드 렌더링 애플리케이션에서는, Vite가 뷰 파일 변경을 감지해 브라우저를 자동 새로고침하도록 개발 워크플로우를 향상시킬 수 있습니다. 이를 활성화하려면 `refresh` 옵션을 `true`로 지정하세요:

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

`refresh`가 `true`면, 아래 디렉토리에 있는 파일을 저장 시 `npm run dev` 중 브라우저가 전체 페이지 새로고침을 실행합니다:

- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

특히 `routes/**` 감시는 [Ziggy](https://github.com/tighten/ziggy)와 같은 라우트링크 생성 도구를 프런트엔드에서 쓸 때 유용합니다.

기본 값에 맞지 않는다면, 직접 감시 경로 배열을 지정할 수도 있습니다:

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

Laravel Vite 플러그인은 내부적으로 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 세밀한 설정을 위해 `config` 옵션을 제공할 수 있습니다:

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

자바스크립트에서는 자주 참조하는 디렉토리에 [별칭](#aliases)을 만드는 것이 일반적입니다. Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드로 별칭을 정의할 수 있습니다. 보통 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드 내에 작성합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

이렇게 별칭이 정의된 후, Blade 템플릿 내에서 사용할 수 있습니다. 예를 들어 위 `image` 매크로를 사용해 `resources/images/logo.png` 에셋을 참조하는 방법입니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="custom-base-urls"></a>
## 커스텀 베이스 URL (Custom Base URLs)

Vite로 컴파일된 에셋이 CDN처럼 애플리케이션과 다른 도메인에 배포될 경우, 애플리케이션 `.env` 파일 내에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

설정 후 모든 에셋 URL은 해당 값을 접두사로 붙여 반환합니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

절대 URL은 Vite가 재작성하지 않으므로 접두사가 붙지 않는 점 유의하세요([URL 처리](#url-processing) 참고).

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

`.env` 파일에서 `VITE_` 접두사가 붙은 환경 변수를 JavaScript에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 `import.meta.env` 객체에서 접근합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화 (Disabling Vite in Tests)

Laravel의 Vite 통합은 테스트 실행 시에도 에셋을 해결하려 하기 때문에, 개발 서버 실행 또는 에셋 빌드가 필요합니다.

테스트 중 Vite 호출을 모킹하고 싶으면, Laravel `TestCase` 클래스를 상속한 테스트 내에서 `withoutVite` 메서드를 호출하세요:

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

모든 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드 내에 호출합니다:

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
## 서버 사이드 렌더링 (SSR) (Server-Side Rendering (SSR))

Laravel Vite 플러그인을 사용하면 Vite 기반 서버 사이드 렌더링을 쉽게 설정할 수 있습니다. 우선 `resources/js/ssr.js`에 SSR 진입점을 만들고, Laravel 플러그인 옵션으로 지정하세요:

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

SSR 빌드를 잊지 않도록, `package.json`의 `build` 스크립트를 다음과 같이 수정하는 것을 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이후 다음 명령어로 SSR을 빌드 및 실행할 수 있습니다:

```sh
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia의 SSR](https://inertiajs.com/server-side-rendering) 사용 시에는, Artisan 명령어로 SSR 서버를 시작할 수 있습니다:

```sh
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel [스타터 킷](/docs/10.x/starter-kits)에는 Laravel, Inertia SSR, Vite 구성이 미리 포함되어 있습니다. 가장 손쉬운 시작은 [Laravel Breeze](/docs/10.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) 논스(Nonce) (Content Security Policy (CSP) Nonce)

스크립트 및 스타일 태그에 [선택적 `nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함해 [콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 적용하려면, 커스텀 [미들웨어](/docs/10.x/middleware) 내에서 `useCspNonce` 메서드를 호출하세요:

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

`useCspNonce` 호출 후 Laravel은 생성하는 모든 스크립트 및 스타일 태그에 `nonce` 속성을 자동으로 포함합니다.

다른 곳, 예를 들어 Laravel 스타터 킷에 포함된 [Ziggy의 `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)에서 논스를 지정하려면 `cspNonce` 메서드로 값을 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 논스 값을 가지고 있다면, `useCspNonce`에 직접 전달해 instruct 할 수 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI) (Subresource Integrity (SRI))

빌드된 Vite 매니페스트에 에셋 무결성 해시(`integrity`)가 포함되어 있다면, Laravel이 생성하는 스크립트 및 스타일 태그에 자동으로 `integrity` 속성을 추가해 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용합니다.

기본적으로 Vite는 매니페스트에 `integrity` 해시를 포함하지 않습니다. 원한다면 [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치해 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

설치 후, `vite.config.js` 파일에 플러그인을 추가하세요:

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

필요하면 무결성 해시 키 이름을 커스터마이징할 수도 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지를 완전히 비활성화하려면 `false`를 전달합니다:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성 (Arbitrary Attributes)

스크립트 및 스타일 태그에 [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 같은 추가 속성을 포함하고 싶다면, `useScriptTagAttributes` 와 `useStyleTagAttributes` 메서드로 지정할 수 있습니다. 보통 [서비스 프로바이더](/docs/10.x/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값이 있는 속성 지정
    'async' => true, // 값 없는 boolean 속성 지정
    'integrity' => false, // 포함되지 않아야 할 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부로 속성 추가가 필요하면, 에셋 파일 경로, URL, 매니페스트 청크 및 전체 매니페스트를 인자로 받는 콜백도 전달할 수 있습니다:

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
> `$chunk`과 `$manifest` 인자는 Vite 개발 서버 실행 중일 때 `null` 입니다.

<a name="advanced-customization"></a>
## 고급 사용자 지정 (Advanced Customization)

Laravel Vite 플러그인은 기본적으로 대부분 애플리케이션에 적합한 합리적인 관례를 따릅니다. 그러나 경우에 따라 Vite 동작을 더 세밀히 조정하고 싶을 수 있습니다. 다음 메서드들과 옵션들을 `@vite` Blade 디렉티브 대신 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 커스텀...
            ->useBuildDirectory('bundle') // 빌드 디렉토리 변경...
            ->useManifestFilename('assets.json') // 매니페스트 파일명 변경...
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋 백엔드 경로 생성 커스텀...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

대응해 `vite.config.js`에서도 동일 설정을 지정하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 명 설정...
            buildDirectory: 'bundle', // 빌드 디렉토리 변경...
            input: ['resources/js/app.js'], // 진입점 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 변경...
    },
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정하기 (Correcting Dev Server URLs)

Vite 생태계의 일부 플러그인은 URL이 슬래시(`/`)로 시작할 경우 항상 Vite 개발 서버를 가리킨다고 가정합니다. 하지만 Laravel 통합 특성상 항상 그렇지 않습니다.

예를 들어 `vite-imagetools` 플러그인은 Vite 서버가 에셋을 서비스할 때 아래처럼 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

이 플러그인은 출력된 URL을 Vite가 가로채서 `/@imagetools`로 시작하는 모든 URL을 처리할 것으로 기대합니다. 이런 플러그인을 사용한다면, 수동으로 URL을 수정해야 하며, `vite.config.js`에서 `transformOnServe` 옵션을 사용해 해결할 수 있습니다.

아래 예시는 모든 `/@imagetools` 발생부에 개발 서버 URL을 앞에 붙입니다:

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

이제 Vite가 에셋을 제공할 때 출력 URL이 개발 서버를 가리킵니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```