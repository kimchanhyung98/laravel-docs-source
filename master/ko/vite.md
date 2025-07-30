# 에셋 번들링 (Vite) (Asset Bundling (Vite))

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치하기](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
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
- [Blade와 라우트 다루기](#working-with-blade-and-routes)
  - [Vite로 정적 에셋 처리하기](#blade-processing-static-assets)
  - [저장 시 자동 새로고침](#blade-refreshing-on-save)
  - [별칭](#blade-aliases)
- [에셋 프리페칭](#asset-prefetching)
- [커스텀 기본 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트 시 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링 (SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [컨텐츠 보안 정책 (CSP) nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성 (SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 사용자화](#advanced-customization)
  - [개발 서버 CORS 설정](#cors)
  - [개발 서버 URL 보정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개 (Introduction)

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고 프로덕션용 코드를 번들링하는 현대적인 프론트엔드 빌드 도구입니다. Laravel 애플리케이션을 구축할 때, 보통 Vite를 사용하여 CSS와 JavaScript 파일을 프로덕션 준비가 완료된 에셋으로 번들링합니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 및 프로덕션 단계에서 에셋을 쉽게 로드할 수 있도록 Vite와 매끄럽게 통합됩니다.

> [!NOTE]
> Laravel Mix를 사용하고 있나요? Vite는 새로운 Laravel 설치에선 Laravel Mix를 대체했습니다. Mix 문서는 [Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하세요. Vite로 전환하려면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참조하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기 (Choosing Between Vite and Laravel Mix)

Vite가 도입되기 전, 새로운 Laravel 애플리케이션에서는 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)가 에셋 번들러로 사용됐습니다. 하지만 Vite는 풍부한 JavaScript 애플리케이션 개발 시 더 빠르고 생산적인 경험을 제공합니다. SPA(Single Page Application)를 개발하거나 [Inertia](https://inertiajs.com) 같은 도구를 사용하는 경우, Vite가 탁월한 선택입니다.

Vite는 JavaScript가 약간 첨가된 전통적인 서버 사이드 렌더링 애플리케이션, 예를 들어 [Livewire](https://livewire.laravel.com)를 사용하는 앱과도 잘 작동합니다. 다만 Laravel Mix가 지원하는, JavaScript 코드에서 직접 참조되지 않은 임의의 자산을 빌드에 복사하는 기능 등은 Vite에서 지원하지 않는 점을 유념하세요.

<a name="migrating-back-to-mix"></a>
#### 다시 Mix로 마이그레이션하는 방법 (Migrating Back to Mix)

Laravel에서 Vite 설정으로 프로젝트를 시작했지만 다시 Laravel Mix와 webpack으로 전환해야 한다면 걱정하지 마세요. [Vite에서 Mix로 마이그레이션하는 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 수동으로 설치하고 설정하는 방법을 다룹니다. 하지만 Laravel의 [스타터 키트](/docs/master/starter-kits)는 이미 이 모든 스캐폴딩을 포함하고 있어, Laravel과 Vite를 시작하는 가장 빠른 방법입니다.

<a name="installing-node"></a>
### Node 설치하기 (Installing Node)

Vite와 Laravel 플러그인을 실행하려면 Node.js(버전 16 이상)와 NPM이 설치되어 있어야 합니다:

```shell
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램을 사용해 최신 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/master/sail)을 사용하는 경우, Sail을 통해 Node와 NPM을 호출할 수도 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치 (Installing Vite and the Laravel Plugin)

Laravel을 새로 설치하면 애플리케이션 루트 디렉토리에 이미 `package.json` 파일이 존재합니다. 기본 `package.json`에는 Vite와 Laravel 플러그인을 사용하기 위한 필요한 모든 종속성이 포함되어 있습니다. NPM을 통해 프론트엔드 종속성을 설치하세요:

```shell
npm install
```

<a name="configuring-vite"></a>
### Vite 구성하기 (Configuring Vite)

Vite는 프로젝트 루트의 `vite.config.js` 파일로 구성됩니다. 필요에 따라 자유롭게 이 파일을 수정할 수 있으며, `@vitejs/plugin-vue`나 `@vitejs/plugin-react` 같은 다른 플러그인도 설치해 사용할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점(entry points)을 지정해야 합니다. 이 진입점은 JavaScript 또는 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass 같은 전처리 언어도 포함됩니다.

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

SPA, 특히 Inertia를 이용해 구축하는 앱이라면, CSS 진입점 없이 JavaScript만 지정하는 편이 더 좋습니다:

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

대신 CSS는 JavaScript 내부에서 임포트해야 합니다. 일반적으로 애플리케이션의 `resources/js/app.js`에 아래처럼 작성합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 여러 개의 진입점과 [SSR 진입점](#ssr) 같은 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 사용하기 (Working With a Secure Development Server)

개발용 로컬 웹 서버가 HTTPS로 서비스를 제공한다면, Vite 개발 서버와 연결하는 데 문제가 생길 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 이용해 사이트를 보안 설정했거나, [Laravel Valet](/docs/master/valet)에서 애플리케이션에 대해 [보안 명령](/docs/master/valet#securing-sites)을 실행했다면, Laravel Vite 플러그인이 자동으로 생성된 TLS 인증서를 감지하고 사용합니다.

하지만 애플리케이션 디렉토리 이름과 일치하지 않는 호스트 이름으로 보안 설정을 했다면, `vite.config.js` 파일에서 직접 호스트 이름을 지정할 수 있습니다:

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

다른 웹 서버를 사용한다면, 신뢰할 수 있는 인증서를 생성한 뒤, Vite가 인증서를 사용하도록 수동으로 설정해야 합니다:

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

만약 시스템에서 신뢰할 수 있는 인증서를 생성할 수 없다면, [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl) 설치 및 구성을 고려하세요. 이 경우 인증서가 신뢰되지 않아 `npm run dev` 실행 시 콘솔에 표시되는 “Local” 링크를 통해 브라우저가 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### Sail + WSL2에서 개발 서버 실행하기 (Running the Development Server in Sail on WSL2)

Windows Subsystem for Linux 2 (WSL2)에서 [Laravel Sail](/docs/master/sail)로 Vite 개발 서버를 실행할 경우, 브라우저와 개발 서버가 원활히 통신하도록 `vite.config.js`에 아래 설정을 추가해야 합니다:

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

개발 서버 실행 중 파일 변경사항이 브라우저에 반영되지 않는다면, Vite의 [`server.watch.usePolling` 옵션](https://vitejs.dev/config/server-options.html#server-watch)도 구성해야 할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 불러오기 (Loading Your Scripts and Styles)

진입점 설정을 완료했으면, `@vite()` Blade 디렉티브를 사용해 애플리케이션 루트 템플릿의 `<head>`에 에셋을 참조할 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript에서 임포트하는 경우, JavaScript 진입점만 포함하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 Vite 개발 서버를 자동 감지해 Hot Module Replacement 클라이언트를 주입하며, 빌드 모드에서는 컴파일되고 버전 관리된 에셋을 (임포트된 CSS 포함) 불러옵니다.

필요하면 `@vite` 호출 시 컴파일된 에셋의 빌드 경로를 지정할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 경로를 기준으로 합니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="inline-assets"></a>
#### 인라인 에셋 (Inline Assets)

가끔 버전 관리된 URL로 링크하는 대신 에셋의 원본 내용을 페이지에 직접 포함해야 할 수도 있습니다. 예를 들어 PDF 생성기로 HTML 콘텐츠를 전달할 때 사용할 수 있습니다. 이 경우, `Vite` 파사드의 `content` 메서드를 사용해 Vite 에셋의 내용을 출력할 수 있습니다:

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

Vite를 실행하는 방법은 두 가지가 있습니다. 로컬에서 개발 중일 때는 `dev` 명령어로 개발 서버를 실행하세요. 개발 서버는 파일 변경 사항을 자동으로 감지하고, 열린 모든 브라우저 창에 즉시 반영합니다.

또는, `build` 명령어로 애플리케이션 에셋을 번들링 및 버전 관리해 프로덕션 배포 준비를 할 수 있습니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋 빌드 및 버전 관리...
npm run build
```

WSL2에서 [Sail](/docs/master/sail) 사용시 추가 설정이 필요할 수 있으니 [여기](#configuring-hmr-in-sail-on-wsl2)를 참고하세요.

<a name="working-with-scripts"></a>
## JavaScript 다루기 (Working With JavaScript)

<a name="aliases"></a>
### 별칭 (Aliases)

기본적으로 Laravel 플러그인은 편리하게 애플리케이션의 자산을 임포트할 수 있도록 다음과 같은 일반 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js`에서 본인만의 별칭을 덮어쓸 수 있습니다:

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

프론트엔드를 [Vue](https://vuejs.org/) 프레임워크로 개발하려면 `@vitejs/plugin-vue` 플러그인을 설치하세요:

```shell
npm install --save-dev @vitejs/plugin-vue
```

그 후 `vite.config.js`에 플러그인을 포함합니다. Vue 플러그인을 Laravel과 함께 쓸 때는 몇 가지 추가 옵션이 필요합니다:

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
                    // Vue 플러그인은 싱글 파일 컴포넌트 내 자산 URL을 Laravel 웹 서버를 가리키도록 재작성합니다.
                    // 이를 null로 설정하면 Laravel 플러그인이 Vite 서버를 가리키도록 URL을 재작성합니다.
                    base: null,

                    // Vue 플러그인은 절대 URL을 파일시스템 상의 절대 경로로 간주합니다.
                    // false로 설정하면 절대 URL을 변경하지 않아 public 디렉토리 내 자산 참조가 가능합니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)는 이미 Laravel, Vue, Vite 구성과 설정을 포함하고 있어 가장 빠르게 시작할 수 있습니다.

<a name="react"></a>
### React

[React](https://reactjs.org/)를 사용하려면 `@vitejs/plugin-react` 플러그인을 설치하세요:

```shell
npm install --save-dev @vitejs/plugin-react
```

그 후 `vite.config.js` 파일에 다음과 같이 플러그인을 포함합니다:

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

JSX를 포함하는 파일은 `.jsx` 또는 `.tsx` 확장자를 가져야 하며, 필요하면 진입점도 위 [설정 방법](#configuring-vite)을 참고해 업데이트하세요.

`@viteReactRefresh` Blade 디렉티브를 기존 `@vite` 디렉티브 앞에 반드시 추가해야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)는 이미 Laravel, React, Vite 구성을 포함해 빠르게 시작할 수 있습니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 해결을 돕는 `resolvePageComponent` 헬퍼를 제공합니다. 아래는 Vue 3에서 사용하는 예시이며, React 등 다른 프레임워크에서도 사용할 수 있습니다:

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

Vite의 코드 분할 기능과 함께 Inertia를 쓰는 경우, [에셋 프리페칭](#asset-prefetching)을 설정하는 것을 권장합니다.

> [!NOTE]
> Laravel [스타터 키트](/docs/master/starter-kits)는 Laravel, Inertia, Vite 구성을 포함하고 있어 가장 빠른 시작을 지원합니다.

<a name="url-processing"></a>
### URL 처리 (URL Processing)

Vite를 사용하고 앱 HTML, CSS, JS에서 자산을 참조할 때 몇 가지 주의 사항이 있습니다. 절대 경로로 자산을 참조하면 Vite가 빌드에 포함하지 않으므로, public 디렉토리에 해당 자산이 반드시 존재해야 합니다. CSS 전용 진입점을 사용할 때는, 개발 시 브라우저가 CSS를 호스팅하는 Vite 개발 서버에서 절대 경로 자산을 로드하려 하므로 절대 경로 사용을 피해야 합니다.

상대 경로로 참조하는 자산은, 참조하는 파일을 기준으로 경로를 해석하며, Vite가 리라이트, 버전 관리, 번들링을 수행합니다.

예를 들어 프로젝트 구조가 다음과 같다면:

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

아래 예시는 Vite가 절대 URL과 상대 URL을 어떻게 처리하는지 보여줍니다:

```html
<!-- 이 에셋은 Vite가 처리하지 않으며 빌드에 포함되지 않습니다 -->
<img src="/taylor.png" />

<!-- 이 에셋은 Vite가 리라이트, 버전 관리, 번들링합니다 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기 (Working With Stylesheets)

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)는 Tailwind와 Vite 구성을 이미 포함합니다. 별도의 키트 없이 Tailwind와 Laravel을 쓰고 싶다면 [Tailwind의 Laravel 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 참고하세요.

Laravel 앱은 기본적으로 Tailwind와 잘 구성된 `vite.config.js`가 포함되어 있으니, 그냥 Vite 개발 서버를 시작하거나 `dev` Composer 명령어로 Laravel과 Vite 개발 서버를 동시에 실행하면 됩니다:

```shell
composer run dev
```

CSS는 `resources/css/app.css`에 작성하면 됩니다.

<a name="working-with-blade-and-routes"></a>
## Blade와 라우트 다루기 (Working With Blade and Routes)

<a name="blade-processing-static-assets"></a>
### Vite로 정적 에셋 처리하기 (Processing Static Assets With Vite)

JavaScript나 CSS에서 자산을 참조하면 Vite가 자동으로 처리 및 버전 관리합니다. Blade 기반 애플리케이션을 빌드할 때, Vite가 Blade 템플릿에서만 참조하는 정적 에셋도 처리할 수 있습니다.

이를 위해서는 정적 에셋을 애플리케이션 진입점에 임포트해 Vite가 자산을 인지하도록 해야 합니다. 예를 들어 `resources/images` 내 모든 이미지와 `resources/fonts` 내 모든 폰트를 처리·버전 관리하려면, 진입점인 `resources/js/app.js`에 다음을 추가하세요:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이 자산들은 `npm run build` 시 Vite에 의해 처리됩니다. Blade에서는 `Vite::asset` 메서드를 사용해 버전 관리된 URL을 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 자동 새로고침 (Refreshing on Save)

전통적인 서버 사이드 렌더링 Blade 앱에서는, Vite가 뷰 파일 변경 시 브라우저를 자동으로 새로고침해 개발 흐름을 개선할 수 있습니다. 사용하려면 `refresh` 옵션을 `true`로 지정하세요.

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

`refresh`가 `true`일 때, 다음 디렉토리 내 파일 저장 시 개발 서버 실행 중인 브라우저에서 전체 페이지 새로고침이 발생합니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

`routes/**` 디렉토리 감시는 프론트엔드에서 [Ziggy](https://github.com/tighten/ziggy)를 사용해 라우트 링크를 생성할 때 유용합니다.

기본 경로 외에 커스텀 경로 목록도 지정할 수 있습니다:

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

Laravel Vite 플러그인은 내부적으로 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 고급 설정을 원한다면 `config` 옵션으로 세밀하게 구성 가능합니다:

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

자바스크립트 앱에서 자주 참조하는 디렉토리에 [별칭](#aliases)을 많이 만듭니다. Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 통해 별칭 기능을 만들 수 있으며, 보통 [서비스 프로바이더](/docs/master/providers) `boot` 메서드에서 정의합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```

이제 정의한 매크로를 템플릿에서 호출할 수 있습니다. 예를 들어 위에서 `image` 매크로를 정의했다면, 다음처럼 `resources/images/logo.png` 에셋을 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="asset-prefetching"></a>
## 에셋 프리페칭 (Asset Prefetching)

Vite 코드 분할을 활용한 SPA를 만들 경우, 각 페이지 탐색 시 필요한 에셋을 페치하는데, 이로 인해 UI 렌더링이 늦어질 수 있습니다. 이런 문제를 개선하기 위해 Laravel은 초기 페이지 로드 시 JavaScript와 CSS 에셋을 적극적으로 미리 가져오도록 지원합니다.

서비스 프로바이더 `boot` 메서드에서 `Vite::prefetch` 메서드를 호출해 프리페칭을 설정하세요:

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

위 코드와 같이, 각 페이지 로드 시 동시 최대 3개의 에셋을 다운로드하도록 설정했습니다. 필요에 따라 동시성 값을 조정하거나, 제한 없이 모든 에셋을 동시에 다운로드할 수도 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch();
}
```

기본적으로 프리페칭은 페이지 _load_ 이벤트가 발생할 때 시작됩니다. 시작 시점을 커스텀하려면 이벤트 이름을 지정할 수 있습니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```

이 경우 `window` 객체에서 `vite:prefetch` 이벤트를 수동으로 디스패치할 때 프리페칭이 시작됩니다. 예를 들어 페이지 로드 후 3초 뒤에 시작하게 하려면:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```

<a name="custom-base-urls"></a>
## 커스텀 기본 URL (Custom Base URLs)

Vite로 컴파일된 에셋이 CDN 등 애플리케이션과 별도의 도메인에 배포된다면, `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

이렇게 설정하면, 모든 리라이트된 에셋 URL에 설정한 값이 접두사로 붙습니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```

절대 URL은 [Vite가 리라이트하지 않습니다](#url-processing) 따라서 접두사가 붙지 않습니다.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

`.env` 파일에서 `VITE_` 접두사가 붙은 환경 변수를 JavaScript에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

JavaScript에서 `import.meta.env` 객체를 통해 접근하세요:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트 시 Vite 비활성화 (Disabling Vite in Tests)

Laravel Vite 통합은 테스트 실행 중에도 자산을 해결하려고 시도합니다. 이는 Vite 개발 서버를 실행하거나 빌드된 자산이 있어야 가능한 작업입니다.

테스트 중에 Vite를 모킹(mocking)하려면, Laravel의 `TestCase` 클래스를 확장한 테스트에서 `withoutVite` 메서드를 호출하세요:

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

전체 테스트에서 Vite를 비활성화하려면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite`를 호출하세요:

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

Laravel Vite 플러그인은 Vite로 SSR을 쉽게 설정할 수 있도록 지원합니다. 먼저 `resources/js/ssr.js` 위치에 SSR 진입점을 만들고, Laravel 플러그인에 구성 옵션으로 진입점을 지정하세요:

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

SSR 진입점 빌드를 잊지 않도록, `package.json`의 "build" 스크립트를 다음과 같이 변경하는 것을 권장합니다:

```json
"scripts": {
     "dev": "vite",
-    "build": "vite build" // [tl! remove]
+    "build": "vite build && vite build --ssr" // [tl! add]
}
```

그 후, 다음 명령어로 SSR 빌드 후 서버를 시작합니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```

Inertia SSR을 사용하는 경우 아래 Artisan 명령어로 SSR 서버를 시작할 수 있습니다:

```shell
php artisan inertia:start-ssr
```

> [!NOTE]
> Laravel의 [스타터 키트](/docs/master/starter-kits)는 Laravel, Inertia SSR 및 Vite 구성을 포함하고 있어 가장 빠른 시작을 지원합니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성 (Script and Style Tag Attributes)

<a name="content-security-policy-csp-nonce"></a>
### 컨텐츠 보안 정책(CSP) nonce (Content Security Policy (CSP) Nonce)

[컨텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로 스크립트와 스타일 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함시키려면, 커스텀 [미들웨어](/docs/master/middleware)에서 `useCspNonce` 메서드를 호출해 nonce를 생성하거나 지정할 수 있습니다:

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
     * 들어오는 요청 처리.
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

`useCspNonce` 호출 후 Laravel은 모든 생성하는 스크립트와 스타일 태그에 `nonce` 속성을 자동으로 추가합니다.

`Ziggy`의 `@route` 디렉티브처럼 다른 곳에서 nonce가 필요할 때는 `cspNonce` 메서드를 통해 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 nonce가 있는 경우, `useCspNonce` 메서드에 전달할 수도 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성 (SRI) (Subresource Integrity (SRI))

Vite 매니페스트에 에셋에 대한 `integrity` 해시가 포함돼 있다면, Laravel은 자동으로 모든 스크립트와 스타일 태그에 해당 `integrity` 속성을 추가해 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 보장합니다.

기본적으로 Vite는 매니페스트에 `integrity` 해시가 포함되지 않으니, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) 플러그인을 설치하면 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

`vite.config.js`에 플러그인 포함하기:

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

필요시 무결성 해시가 위치하는 매니페스트 키를 커스텀할 수도 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지를 완전히 끄려면 `useIntegrityKey` 메서드에 `false`를 넘기면 됩니다:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성 (Arbitrary Attributes)

`data-turbo-track` 같은 추가 속성을 스크립트와 스타일 태그에 포함해야 한다면, `useScriptTagAttributes`와 `useStyleTagAttributes` 메서드를 사용하세요. 보통 서비스 프로바이더에서 설정합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값을 가진 속성 지정
    'async' => true, // 값 없는 속성 지정
    'integrity' => false, // 기본적으로 포함된 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 속성 추가를 컨트롤하려면, 에셋 경로나 URL, 매니페스트 정보를 파라미터로 받는 콜백을 넘길 수 있습니다:

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
> Vite 개발 서버 실행 중에는 `$chunk`와 `$manifest` 인자가 `null`입니다.

<a name="advanced-customization"></a>
## 고급 사용자화 (Advanced Customization)

Laravel Vite 플러그인은 기본적으로 다수 앱에서 잘 작동하는 합리적인 규칙을 따릅니다. 그러나 Vite 동작을 좀 더 세부적으로 조절하려면, `@vite` Blade 디렉티브 대신 아래의 메서드와 옵션을 조합해 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 지정
            ->useBuildDirectory('bundle') // 빌드 디렉토리 변경
            ->useManifestFilename('assets.json') // 매니페스트 파일 이름 변경
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // 빌드 자산 경로 생성 방식 커스텀
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```

`vite.config.js`에서는 같은 설정을 반영하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 위치 지정
            buildDirectory: 'bundle', // 빌드 폴더명 변경
            input: ['resources/js/app.js'], // 진입점 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 이름 변경
    },
});
```

<a name="cors"></a>
### 개발 서버 CORS 설정 (Dev Server Cross-Origin Resource Sharing (CORS))

Vite 개발 서버에서 에셋을 가져올 때 브라우저의 CORS 오류가 발생한다면, 커스텀 오리진(도메인) 접근 권한을 부여해야 할 수 있습니다. Laravel 플러그인이 기본적으로 허용하는 오리진은 다음과 같습니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- `.env`의 `APP_URL`

사용자가 접속하는 브라우저 오리진과 `.env` 내 `APP_URL`을 일치시키는 것이 가장 쉽습니다. 예를 들어, `https://my-app.laravel`로 접속 시 `.env`를 아래와 같이 맞추세요:

```env
APP_URL=https://my-app.laravel
```

복수 오리진 등 보다 세밀한 설정이 필요하면, Vite의 강력한 CORS 서버 옵션을 활용하세요. 예를 들어, `vite.config.js`에서 `server.cors.origin` 배열로 여러 오리진을 지정할 수 있습니다:

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

정규식을 포함할 수도 있어 특정 최상위 도메인 전체(`*.laravel`)를 허용하는 경우 유용합니다:

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
                // 형식: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 보정 (Correcting Dev Server URLs)

Vite 생태계 일부 플러그인은 `/`로 시작하는 URL이 항상 Vite 개발 서버를 가리킬 것으로 가정합니다. 하지만 Laravel 통합에서는 그렇지 않은 경우가 많습니다.

예를 들어, `vite-imagetools` 플러그인은 다음처럼 `/@imagetools`로 시작하는 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

`vite-imagetools`는 이런 URL을 Vite가 가로채서 제대로 처리할 것이라고 기대하지만, Laravel 통합에서는 그렇지 않으므로 URL을 수동으로 바꿔줘야 합니다. `vite.config.js`에서 `transformOnServe` 옵션을 사용해 모든 `/@imagetools` 출현 부분에 개발 서버 URL을 앞에 붙일 수 있습니다:

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

이제 Vite 개발 서버가 에셋을 서비스할 때 Vite 개발 서버 URL이 URL 앞에 붙어 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```