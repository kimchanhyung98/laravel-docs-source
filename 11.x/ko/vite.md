# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치하기](#installing-node)
  - [Vite와 Laravel 플러그인 설치하기](#installing-vite-and-laravel-plugin)
  - [Vite 설정하기](#configuring-vite)
  - [스크립트와 스타일 불러오기](#loading-your-scripts-and-styles)
- [Vite 실행하기](#running-vite)
- [JavaScript 작업하기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 작업하기](#working-with-stylesheets)
- [Blade와 라우트 작업하기](#working-with-blade-and-routes)
  - [Vite로 정적 에셋 처리하기](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [별칭(Aliases)](#blade-aliases)
- [에셋 프리페칭(미리 가져오기)](#asset-prefetching)
- [커스텀 기본 URL 설정](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트 시 Vite 비활성화하기](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책(CSP) 논스(nonce)](#content-security-policy-csp-nonce)
  - [하위 리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의 속성 추가](#arbitrary-attributes)
- [고급 설정](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 수정하기](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 프로덕션용으로 코드 번들링을 처리하는 최신 프론트엔드 빌드 도구입니다. Laravel 애플리케이션을 구축할 때, 보통 Vite를 사용하여 애플리케이션의 CSS와 JavaScript 파일을 프로덕션용 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 지시어를 제공하여 개발 및 프로덕션 시 에셋을 쉽게 불러올 수 있도록 Vite와 원활하게 통합됩니다.

> [!NOTE]  
> Laravel Mix를 사용 중이신가요? Vite는 새 Laravel 설치에서 Laravel Mix를 대체했습니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 공식 사이트를 참고하세요. Vite로 전환하고 싶다면, [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 확인하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

기존 새 Laravel 애플리케이션들은 자산 번들링 시 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 풍부한 JavaScript 애플리케이션 개발 시 더 빠르고 생산적인 환경을 제공합니다. 특히 [Inertia](https://inertiajs.com) 같은 SPA(Single Page Application)를 개발할 때는 Vite가 더 적합합니다.

Vite는 JavaScript를 일부만 사용하는 전통적인 서버 측 렌더링 애플리케이션(예: [Livewire](https://livewire.laravel.com) 사용 앱)과도 잘 작동하지만, Laravel Mix가 지원하는 "직접 참조되지 않는 임의 에셋 복사 기능"과 같은 일부 기능은 지원하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### 다시 Mix로 마이그레이션하기

Vite 스캐폴딩을 사용하여 새 Laravel 앱을 시작했지만 Mix와 webpack으로 다시 전환해야 할 경우 문제가 없습니다. [Vite에서 Mix로 마이그레이션하는 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]  
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 다룹니다. 하지만 Laravel의 [스타터 키트](/docs/11.x/starter-kits)에는 이미 이 모든 스캐폴딩이 포함되어 있어 Laravel과 Vite를 빠르게 시작할 수 있는 가장 쉬운 방법입니다.

<a name="installing-node"></a>
### Node 설치하기 (Installing Node)

Vite와 Laravel 플러그인을 실행하기 전에 Node.js (16버전 이상)와 NPM이 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

최신 버전의 Node와 NPM은 [Node 공식 웹사이트](https://nodejs.org/en/download/)에서 GUI 설치 프로그램으로 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/11.x/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치하기 (Installing Vite and the Laravel Plugin)

새 Laravel 설치 내에 `package.json` 파일이 프로젝트 루트에 있습니다. 기본 `package.json`에는 Vite와 Laravel 플러그인을 사용하기 위한 필요한 모든 항목이 이미 포함되어 있습니다. 다음 명령어로 프론트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 설정하기 (Configuring Vite)

Vite는 프로젝트 루트에 있는 `vite.config.js` 파일을 통해 설정합니다. 필요에 따라 자유롭게 이 파일을 수정하고, 앱에서 필요한 추가 플러그인(예: `@vitejs/plugin-vue`, `@vitejs/plugin-react`)도 설치할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점(entry points)을 지정해야 합니다. 이 진입점은 JavaScript나 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass 등의 전처리된 언어도 포함할 수 있습니다.

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

SPA, 특히 Inertia 등을 사용해 구축하는 애플리케이션의 경우 CSS 진입점 없이 Vite를 사용하는 것이 더 좋습니다:

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

대신 CSS는 JavaScript에서 import하는 방식으로 불러와야 하며, 보통 애플리케이션의 `resources/js/app.js` 파일에 다음과 같이 작성합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

또한 Laravel 플러그인은 다중 진입점과 [SSR 진입점](#ssr) 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 연결 개발 서버 사용하기

로컬 개발 웹서버가 HTTPS로 앱을 서비스할 경우, Vite 개발 서버 연결 시 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용 중이고 사이트를 보안(SSL) 설정했거나, [Laravel Valet](/docs/11.x/valet)를 쓰면서 [보안 명령](/docs/11.x/valet#securing-sites)을 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지해 사용합니다.

만약 앱 디렉터리명과 맞지 않는 호스트로 보안 설정한 경우, `vite.config.js`에서 직접 호스트를 지정할 수 있습니다:

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

다른 웹 서버를 사용할 경우, 신뢰된 인증서를 생성한 뒤 직접 Vite 설정에 인증서 경로를 지정해야 합니다:

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

만약 신뢰된 인증서를 생성할 수 없다면 [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 설정할 수 있습니다. 신뢰되지 않은 인증서 사용 시, `npm run dev` 실행 후 콘솔에 표시되는 "Local" 링크를 클릭해 브라우저에서 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail 내 개발 서버 실행하기

Windows Subsystem for Linux 2 (WSL2) 환경에서 [Laravel Sail](/docs/11.x/sail)로 Vite 개발 서버를 실행할 때, 브라우저가 개발 서버와 통신할 수 있도록 아래 설정을 `vite.config.js`에 추가하세요:

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

만약 개발 서버 구동 중 파일 변경 사항이 브라우저에 반영되지 않는 경우, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch) 설정도 함께 검토하세요.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 불러오기 (Loading Your Scripts and Styles)

Vite 진입점을 설정한 후, Blade 템플릿의 `<head>` 안에 `@vite()` 지시어를 추가하여 해당 에셋을 불러올 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript에서 import한다면, JavaScript 진입점 만으로 충분합니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 지시어는 Vite 개발 서버를 자동 감지하여 핫 모듈 교체(Hot Module Replacement)가 활성화된 클라이언트를 삽입해 줍니다. 빌드 모드에서는 컴파일된 버전과 버전 관리된 에셋(불러온 CSS 포함)을 자동으로 로드합니다.

필요 시 `@vite` 호출 시 컴파일된 에셋의 빌드 경로도 별도로 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 경로를 기준으로 합니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋 (Inline Assets)

때로 버전 URL을 링크하는 대신 에셋의 원본 내용을 바로 포함해야 할 때가 있습니다. 예를 들어 PDF 생성 시 HTML 내용을 직접 포함할 때가 그렇습니다. 이 경우 `Vite` 페이사드가 제공하는 `content` 메서드로 에셋 내용을 출력할 수 있습니다:

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
## Vite 실행하기 (Running Vite)

Vite 실행 방법은 두 가지입니다. 개발 중에는 `dev` 명령어로 개발 서버를 띄우세요. 이 서버는 파일 변경을 실시간 감지해 열린 브라우저에 즉시 반영합니다.

프로덕션용으로는 `build` 명령을 실행해 애플리케이션 에셋을 버전 관리하고 번들링한 뒤 배포 준비를 합니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 번들 빌드 및 버전 관리...
npm run build
```

WSL2에서 [Sail](/docs/11.x/sail)로 개발 서버 실행 시, [추가 설정](#configuring-hmr-in-sail-on-wsl2)을 참고해야 할 수도 있습니다.

<a name="working-with-scripts"></a>
## JavaScript 작업하기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭(Aliases)

기본적으로 Laravel 플러그인은 아래와 같은 편리한 별칭(alias)을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js`에서 직접 `resolve.alias` 속성을 설정하면 `'@'` 별칭을 다른 경로로 덮어쓸 수 있습니다:

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

Vue 프레임워크([Vue](https://vuejs.org/))를 쓰고 싶다면 `@vitejs/plugin-vue` 플러그인을 추가로 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

그리고 `vite.config.js`에 플러그인을 포함하고, Laravel과 Vue를 동시에 쓸 때 필요한 추가 옵션을 설정하세요:

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
                    // Vue 플러그인은 Single File Component에서 참조하는 에셋 URL을
                    // Laravel 웹 서버를 가리키도록 다시 작성합니다.
                    // 이를 null로 설정하면 Laravel 플러그인이 Vite 서버를 가리키도록 URL을 다시 씁니다.
                    base: null,

                    // Vue 플러그인은 절대 URL을 실제 파일 경로로 인식합니다.
                    // false로 설정하면 public 디렉터리에 있는 에셋 참조를 그대로 유지합니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]  
> Laravel [스타터 키트](/docs/11.x/starter-kits)에는 Laravel, Vue, Vite 설정이 이미 포함되어 있습니다. 가장 손쉽게 시작하려면 [Laravel Breeze](/docs/11.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="react"></a>
### React

React 프레임워크([React](https://reactjs.org/))를 사용하려면 `@vitejs/plugin-react` 플러그인을 설치하세요:

```sh
npm install --save-dev @vitejs/plugin-react
```

설치 후 `vite.config.js`에 플러그인을 포함합니다:

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

JSX를 포함하는 파일은 `.jsx` 혹은 `.tsx` 확장자를 가져야 하며, 진입점도 필요에 따라 수정해야 합니다([설정 부분](#configuring-vite) 참고).

추가로 `@viteReactRefresh` Blade 지시어를 기존 `@vite` 지시어와 함께 넣어야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 `@vite` 보다 먼저 호출되어야 합니다.

> [!NOTE]  
> Laravel [스타터 키트](/docs/11.x/starter-kits)에는 Laravel, React, Vite 설정이 미리 포함되어 있습니다. 시작하기 가장 좋은 방법은 [Laravel Breeze](/docs/11.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 해석을 도와주는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3 예제이며, React 등 다른 프레임워크에서도 쓸 수 있습니다:

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

Vite의 코드 분할 기능과 함께 Inertia를 쓴다면 [에셋 프리페칭](#asset-prefetching) 설정을 권장합니다.

> [!NOTE]  
> Laravel [스타터 키트](/docs/11.x/starter-kits)에는 Laravel, Inertia, Vite 설정이 이미 포함되어 있습니다. 가장 빠른 시작 방법은 [Laravel Breeze](/docs/11.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite 사용 시 애플리케이션 HTML, CSS, JS 내에서 에셋을 참조할 때 주의할 점이 있습니다. 절대 경로로 참조하면 Vite가 빌드에 포함하지 않고, 따라서 해당 에셋은 반드시 `public` 디렉터리에 있어야 합니다. 전용 CSS 진입점을 사용하는 경우 절대 경로는 개발 시 브라우저가 Vite 개발 서버에서 해당 경로를 찾으려 해 문제를 일으킵니다.

반면 상대 경로로 참조한 에셋은 해당 참조가 위치한 파일을 기준으로 경로가 해석되고, Vite가 URL을 다시 쓰고 버전 관리 및 번들링도 수행합니다.

예제를 위해 다음과 같은 프로젝트 구조를 생각해 봅시다:

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

아래 예시는 Vite가 상대 및 절대 URL을 어떻게 처리하는지 보여줍니다:

```html
<!-- 이 에셋은 Vite가 처리하지 않아 빌드에 포함되지 않음 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 다시 쓰고 버전 관리 및 번들링함 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업하기 (Working With Stylesheets)

Vite의 CSS 지원 기능은 [Vite 문서](https://vitejs.dev/guide/features.html#css)에서 자세히 살펴볼 수 있습니다. PostCSS 플러그인(예: [Tailwind](https://tailwindcss.com))을 사용하는 경우, 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 이를 자동으로 적용합니다:

```js
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

> [!NOTE]  
> Laravel [스타터 키트](/docs/11.x/starter-kits)에는 Tailwind, PostCSS, Vite 설정이 이미 포함되어 있습니다. 또는 스타터 키트를 사용하지 않고 Tailwind와 Laravel을 통합하고 싶다면 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

<a name="working-with-blade-and-routes"></a>
## Blade와 라우트 작업하기 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 에셋 처리하기

JavaScript나 CSS에서 참조하는 에셋은 Vite가 자동으로 처리 및 버전 관리합니다. Blade 기반 애플리케이션에서는 정적 에셋을 오로지 Blade 템플릿에서만 참조하는 경우도 처리가 가능합니다.

이를 위해서는 앱의 진입점에 정적 에셋 경로를 `import`하여 Vite가 인지하도록 해야 합니다. 예를 들어 `resources/images`와 `resources/fonts`에 있는 모든 이미지와 폰트를 처리하려면 `resources/js/app.js`에 다음을 추가합니다:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build` 시 해당 에셋들이 Vite에 의해 처리되고, Blade 템플릿에선 `Vite::asset` 메서드로 버전 관리된 URL을 가져올 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침 (Refreshing on Save)

Blade 기반 SSR 앱을 개발할 때, Vite는 뷰 파일 변경 시 브라우저 자동 새로고침으로 개발 흐름을 개선할 수 있습니다. 간단히 `refresh` 옵션을 `true`로 지정하면 시작됩니다:

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

`refresh`가 `true`일 때 `npm run dev` 실행 중 아래 디렉터리 내 파일 저장 시 브라우저가 전체 페이지를 새로 로드합니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**`를 감시하는 것은, 프론트엔드에서 [Ziggy](https://github.com/tighten/ziggy)를 사용해 라우트 링크를 생성하는 경우 유용합니다.

원하는 경로만 직접 지정할 수도 있습니다:

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

Laravel Vite 플러그인은 내부적으로 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 고급 설정을 위해 `refresh`에 다음과 같이 객체를 넣을 수 있습니다:

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

자바스크립트에서 자주 참조하는 디렉터리에 별칭을 만드는 경우가 많습니다([별칭](#aliases) 참고). Blade에서도 같은 별칭 기능을 쓰고 싶다면 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하세요.

보통 "매크로"는 [서비스 프로바이더](/docs/11.x/providers)의 `boot` 메서드 내에서 정의합니다:

```php
/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

한번 정의된 매크로는 템플릿 내부에서 호출할 수 있습니다. 예를 들어 위 `image` 매크로로 `resources/images/logo.png` 에셋을 참조하려면 다음처럼 사용합니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 프리페칭(미리 가져오기) (Asset Prefetching)

Vite 코드 분할 기능을 활용한 SPA에서는 페이지가 바뀔 때마다 필요한 에셋들을 가져오기 때문에 UI 렌더링이 지연될 수 있습니다. 이 문제를 해결하려면 Laravel에서 애플리케이션의 JavaScript와 CSS 에셋을 초기 페이지 로드 시 적극적으로 프리페칭(미리 가져오기)할 수 있습니다.

프리페칭 활성화는 [서비스 프로바이더](/docs/11.x/providers)의 `boot` 메서드에서 `Vite::prefetch`를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 초기화
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```

위 예제는 페이지당 최대 `3`개 동시 다운로드로 에셋을 프리페칭합니다. 애플리케이션 요구에 따라 동시성 수를 변경하거나 제한 없이 한 번에 모두 다운로드하도록 할 수도 있습니다:

```php
/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 프리페칭은 [페이지 _load_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작합니다. 프리페칭 시작 시기를 변경하고 싶으면 이벤트 이름을 지정할 수도 있습니다:

```php
/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

위 코드를 사용하면 `window` 객체에 `vite:prefetch` 이벤트를 수동 발송할 때 프리페칭이 시작됩니다. 예컨대 페이지가 로드된 뒤 3초 후 프리페칭을 시작하려면 다음과 같이 할 수 있습니다:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 기본 URL 설정 (Custom Base URLs)

Vite가 컴파일한 에셋이 CDN 등 앱이 호스팅되는 도메인과 다른 도메인에 배포된 경우, `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

이 설정을 하면 모든 다시 쓰여진 에셋 URL이 지정한 값으로 접두사가 붙습니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

단, [절대 URL은 Vite가 다시 쓰지 않으므로](#url-processing), 접두사가 붙지 않는 점을 기억하세요.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

`.env` 파일에 `VITE_` 접두사를 붙인 변수를 추가하면 JavaScript에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 환경 변수는 `import.meta.env` 객체를 통해 엑세스합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트 시 Vite 비활성화하기 (Disabling Vite in Tests)

Laravel의 Vite 통합은 테스트 실행 시 에셋 해석을 시도하므로, 로컬 개발 서버를 구동하거나 에셋 빌드가 선행돼야 합니다.

테스트 중 Vite 동작을 모킹(mocking)하고 싶다면, 모든 Laravel `TestCase` 확장 테스트에서 사용할 수 있는 `withoutVite` 메서드를 호출하세요:

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

모든 테스트에서 자동으로 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에 다음을 추가하세요:

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

Laravel Vite 플러그인을 사용하면 Vite와 서버 사이드 렌더링 설정이 매우 간편합니다. 시작하려면 `resources/js/ssr.js`에 SSR 진입점을 만들고 Laravel 플러그인에 옵션을 전달하세요:

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

SSR 진입점 빌드를 잊지 않도록, `package.json` 내 `build` 스크립트를 다음과 같이 변경하는 것을 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

그 후, SSR 서버 빌드 및 시작 명령은 다음과 같습니다:

```sh
npm run build
node bootstrap/ssr/ssr.js
```

[Inertia SSR](https://inertiajs.com/server-side-rendering)을 사용하는 경우, 대신 `inertia:start-ssr` Artisan 명령어로 SSR 서버를 시작할 수 있습니다:

```sh
php artisan inertia:start-ssr
```

> [!NOTE]  
> Laravel [스타터 키트](/docs/11.x/starter-kits)에는 Laravel, Inertia SSR, Vite 설정이 미리 포함되어 있습니다. 가장 빠른 시작 방법은 [Laravel Breeze](/docs/11.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) 논스(nonce) (Content Security Policy (CSP) Nonce)

스크립트와 스타일 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 추가해 [콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 강화하려면, 커스텀 [미들웨어](/docs/11.x/middleware)에서 `useCspNonce` 메서드를 호출하세요:

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
     * 수신된 요청을 처리합니다.
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

`useCspNonce`를 호출하면 Laravel은 생성하는 모든 스크립트와 스타일 태그에 자동으로 `nonce` 속성을 삽입합니다.

`nonce`를 다른 곳에서 사용해야 한다면(예: Laravel [스타터 키트]의 [Ziggy `@route` 지시어](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)) `cspNonce` 메서드로 값을 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

기존에 nonce 값이 있다면 이를 직접 `useCspNonce`에 전달할 수도 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 하위 리소스 무결성(SRI) (Subresource Integrity (SRI))

Vite 매니페스트에 에셋 `integrity` 해시가 포함되어 있다면, Laravel은 자동으로 스크립트와 스타일 태그에 `integrity` 속성을 추가하여 [하위 리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용합니다.

기본적으로 Vite는 매니페스트에 `integrity` 해시를 포함하지 않지만, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) 플러그인을 설치하면 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

`vite.config.js`에 플러그인을 추가하세요:

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

필요하다면 무결성 해시가 저장된 매니페스트 키를 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 탐지를 완전히 비활성화하려면 `false`를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성 추가 (Arbitrary Attributes)

스크립트 및 스타일 태그에 [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 등의 추가 속성이 필요하다면, `useScriptTagAttributes`와 `useStyleTagAttributes` 메서드를 사용하세요. 보통 [서비스 프로바이더](/docs/11.x/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성 값 지정
    'async' => true, // 값이 없는 속성 추가
    'integrity' => false, // 기본 포함 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건부 속성 추가가 필요하면, 현재 에셋 경로, URL, 청크(Manifest 조각), 전체 매니페스트를 인자로 받는 콜백을 넘길 수 있습니다:

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
> `$chunk`와 `$manifest` 인자는 Vite 개발 서버 실행 중일 때는 `null`입니다.

<a name="advanced-customization"></a>
## 고급 설정 (Advanced Customization)

Laravel Vite 플러그인은 기본적으로 대부분 앱에 적합한 기본 설정을 제공합니다. 그러나 상황에 따라 Vite 동작을 커스터마이징해야 할 때도 있습니다.

`@vite` Blade 지시어 대신 다음 메서드들을 조합해 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 변경
            ->useBuildDirectory('bundle') // 빌드 디렉터리 변경
            ->useManifestFilename('assets.json') // 매니페스트 파일명 변경
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드된 에셋 경로 커스터마이징
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

그리고 `vite.config.js`의 설정도 아래와 같이 일치시켜야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 위치 변경
            buildDirectory: 'bundle', // 빌드 디렉터리 변경
            input: ['resources/js/app.js'], // 진입점 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 지정
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS 설정 (Dev Server Cross-Origin Resource Sharing (CORS))

Vite 개발 서버에서 에셋을 불러올 때 브라우저 CORS 문제가 발생하면, 개발 서버에 접근 권한이 있는 도메인을 지정해야 할 수 있습니다.

Laravel Vite 플러그인은 다음 도메인들을 자동 허용합니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트 `.env` 내 `APP_URL`

커스텀 도메인을 허용하려면, `.env`에서 `APP_URL`을 방문하려는 도메인과 일치하도록 설정하는 것이 가장 간단합니다. 예를 들어 `https://my-app.laravel`에 접속하려면:

```env
APP_URL=https://my-app.laravel
```

복수 도메인 지원 등 더 세밀한 제어가 필요하면, Vite의 강력한 내장 CORS 설정 옵션을 써야 합니다. 예를 들어 프로젝트 `vite.config.js`에 다음처럼 여러 도메인을 지정할 수 있습니다:

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

정규표현식 패턴도 쓸 수 있어 최상위 도메인 등 특정 패턴을 허용하기 편리합니다. 예: `*.laravel` 도메인 전부 허용:

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
                // SCHEME://DOMAIN.laravel[:PORT] 형식 지원 [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정하기 (Correcting Dev Server URLs)

Vite 플러그인 일부는 `/`로 시작하는 URL이 항상 Vite 개발 서버로 가리킬 것이라 가정합니다. 그러나 Laravel 통합 특성상 이 가정이 맞지 않을 수 있습니다.

예를 들어, `vite-imagetools` 플러그인은 에셋 공급 중 다음과 같은 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

이 플러그인은 `/@imagetools`로 시작하는 URL을 Vite가 가로채 처리한다고 기대합니다. 이런 플러그인을 사용할 때는 URL을 직접 수정해야 하며, `vite.config.js` 파일의 `transformOnServe` 옵션을 활용합니다.

아래 예시는 모든 `/@imagetools` 경로 앞에 개발 서버 URL을 덧붙이는 방법입니다:

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

이제 Vite 개발 서버 실행 중에는 에셋 URL이 개발 서버를 가리키도록 올바르게 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```