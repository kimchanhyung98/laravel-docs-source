# Asset Bundling (Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 구성하기](#configuring-vite)
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
- [커스텀 기본 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트 시 Vite 비활성화](#disabling-vite-in-tests)
- [서버사이드 렌더링(SSR)](#ssr)
- [스크립트 및 스타일 태그 속성](#script-and-style-attributes)
  - [콘텐츠 보안 정책(CSP) nonce](#content-security-policy-csp-nonce)
  - [서브리소스 무결성(SRI)](#subresource-integrity-sri)
  - [임의 속성](#arbitrary-attributes)
- [고급 사용자 정의](#advanced-customization)
  - [개발 서버 URL 수정하기](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하면서 프로덕션 배포용으로 코드를 번들링하는 최신 프론트엔드 빌드 도구입니다. Laravel 애플리케이션을 빌드할 때는 보통 Vite를 사용하여 CSS와 JavaScript 파일을 프로덕션에 적합한 자산으로 묶습니다.

Laravel은 공식 플러그인과 Blade 디렉티브를 제공하여 개발 및 프로덕션 환경에서 자산을 손쉽게 불러올 수 있도록 Vite와 완벽하게 통합되어 있습니다.

> [!NOTE]
> Laravel Mix를 사용 중이신가요? Vite는 새 Laravel 설치에서 Laravel Mix를 대체했습니다. Mix 관련 문서는 [Laravel Mix](https://laravel-mix.com/) 공식 사이트에서 확인하실 수 있습니다. Vite로 전환하려면 [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

기존 Laravel 애플리케이션은 자산 번들링에 [webpack](https://webpack.js.org/) 기반 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 더 빠르고 생산적인 JavaScript 애플리케이션 개발 경험을 제공합니다. 만약 SPA(Single Page Application)를 개발 중이고, [Inertia](https://inertiajs.com) 같은 툴을 사용한다면 Vite가 적합합니다.

Vite는 또한 JavaScript "스프링클"이 포함된 전통적인 서버사이드 렌더링 애플리케이션, 예를 들어 [Livewire](https://laravel-livewire.com)와도 잘 작동합니다. 다만 Laravel Mix가 지원하는, JavaScript에서 직접 참조하지 않는 임의 자산 복사 기능 등 일부 기능은 제공하지 않습니다.

<a name="migrating-back-to-mix"></a>
#### 다시 Mix로 마이그레이션하기

Vite 기반으로 새 Laravel 앱을 시작했지만 다시 Laravel Mix와 webpack으로 전환하려면 [공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정

> [!NOTE]
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치하고 구성하는 방법을 설명합니다. 하지만 Laravel의 [스타터 킷들](/docs/9.x/starter-kits)은 이미 모든 설정을 포함하고 있어 Laravel과 Vite를 가장 빠르게 시작할 수 있는 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite 및 Laravel 플러그인을 실행하려면 Node.js(16 이상)와 NPM이 반드시 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 간편한 그래픽 설치 프로그램을 사용해 최신 버전을 설치하거나, [Laravel Sail](https://laravel.com/docs/9.x/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새 Laravel 설치 프로젝트 루트에는 `package.json` 파일이 존재하며, 기본 파일에 Vite와 Laravel 플러그인을 사용하기 위한 모든 의존성이 포함되어 있습니다. 다음 명령어로 프론트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 구성하기

Vite는 프로젝트 루트의 `vite.config.js` 파일로 구성합니다. 필요에 따라 자유롭게 이 파일을 수정하고, `@vitejs/plugin-vue` 또는 `@vitejs/plugin-react` 같은 다른 플러그인을 추가할 수도 있습니다.

Laravel Vite 플러그인은 애플리케이션 진입점(entry points) 설정이 필요합니다. 이는 JavaScript 혹은 CSS 파일이며, TypeScript, JSX, TSX, Sass 같은 전처리 언어도 포함됩니다.

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

만약 SPA나 Inertia 기반 앱을 빌드한다면, CSS 진입점 없이 Vite를 사용하는 것이 더 좋습니다:

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

대신 CSS는 JavaScript에서 import하는 방식을 권장합니다. 보통 `resources/js/app.js`에서 다음과 같이 처리합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 다중 진입점과 [SSR 진입점](#ssr) 등 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안이 적용된 개발 서버에서 작업하기

로컬 개발 서버가 HTTPS를 통해 애플리케이션을 제공한다면, Vite 개발 서버 연결에 문제가 발생할 수 있습니다.

[Laravel Valet](/docs/9.x/valet)를 사용하며 애플리케이션을 [secure 명령어](/docs/9.x/valet#securing-sites)로 보안했을 경우, Vite 개발 서버가 Valet에서 생성한 TLS 인증서를 자동으로 사용하도록 설정할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            valetTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```

다른 웹 서버를 사용 중이라면 신뢰된 인증서를 직접 생성하고, Vite에 인증서 경로를 수동으로 지정해야 합니다:

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

만약 OS 신뢰 된 인증서를 만들 수 없다면, [`@vitejs/plugin-basic-ssl`](https://github.com/vitejs/vite-plugin-basic-ssl) 플러그인을 설치하고 구성할 수 있습니다. 신뢰하지 않은 인증서를 사용할 경우, `npm run dev` 실행 시 콘솔 출력의 "Local" 링크를 클릭해 브라우저에서 수동으로 인증서 경고를 허용해야 합니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 불러오기

Vite 진입점을 구성한 후, 애플리케이션 최상위 Blade 템플릿 `<head>`에 `@vite()` 디렉티브를 추가해 해당 자산을 불러오기만 하면 됩니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript에서 import한다면, JavaScript 진입점만 포함하세요:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 디렉티브는 자동으로 Vite 개발 서버를 감지하여 Hot Module Replacement를 사용할 수 있게 클라이언트를 삽입합니다. 빌드 모드에서는 컴파일되고 버전 관리된 자산(임포트된 CSS 포함)을 로드합니다.

필요하다면 컴파일된 자산의 빌드 경로를 명시할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 공용(public) 경로를 기준으로 합니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="running-vite"></a>
## Vite 실행하기

Vite를 실행하는 방법은 두 가지입니다. 로컬 개발 시 변경된 파일을 즉시 반영하는 개발 서버를 실행하려면 `dev` 명령어를 사용하세요:

```shell
npm run dev
```

프로덕션 배포용으로 자산을 번들링하고 버전 관리를 하려면 `build` 명령어를 실행합니다:

```shell
npm run build
```

<a name="working-with-scripts"></a>
## JavaScript 작업하기

<a name="aliases"></a>
### 별칭(Aliases)

Laravel 플러그인은 애플리케이션 자산을 편리하게 import할 수 있도록 기본 별칭을 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

별칭 `'@'`는 `vite.config.js`에서 직접 덮어쓸 수도 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크로 프론트엔드를 빌드하려면 `@vitejs/plugin-vue` 플러그인을 설치해야 합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

다음처럼 `vite.config.js`에 플러그인을 포함시키고, Laravel과 호환되도록 몇 가지 옵션을 추가하세요:

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
                    // Vue 플러그인은 싱글 파일 컴포넌트에서 참조하는 자산 URL을
                    // Laravel 웹 서버 기준으로 다시 작성합니다.
                    // 이를 null로 설정하면 Laravel 플러그인이 대신 Vite 서버로
                    // URL을 다시 작성하도록 허용합니다.
                    base: null,

                    // Vue 플러그인은 절대 URL을 파일 경로로 해석합니다.
                    // false로 설정하면 절대 URL을 그대로 두어 퍼블릭(public) 디렉토리 내 자산 참조가 가능합니다.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> [!NOTE]
> Laravel [스타터 킷](/docs/9.x/starter-kits)은 Laravel, Vue, Vite 구성 파일을 이미 포함하고 있습니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 참고하여 가장 빠르게 시작할 수 있습니다.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크로 프론트엔드를 빌드하려면 `@vitejs/plugin-react` 플러그인을 설치하세요:

```sh
npm install --save-dev @vitejs/plugin-react
```

설치 후 `vite.config.js`에 플러그인을 추가합니다:

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

JSX가 포함된 파일은 `.jsx` 또는 `.tsx` 확장자를 꼭 사용하고, 진입점을 필요에 따라 업데이트하세요([설정 가이드](#configuring-vite) 참조).

`@viteReactRefresh` Blade 디렉티브도 `@vite` 디렉티브 앞에 반드시 포함해야 합니다:

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

> [!NOTE]
> Laravel [스타터 킷](/docs/9.x/starter-kits)은 Laravel, React, Vite 구성을 이미 포함합니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 손쉽게 해결할 수 있는 `resolvePageComponent` 헬퍼를 제공합니다. 아래는 Vue 3 사용 예시지만 React 등 다른 프레임워크에도 사용할 수 있습니다:

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
> Laravel [스타터 킷](/docs/9.x/starter-kits)은 Laravel, Inertia, Vite 구성을 기본으로 포함합니다. [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="url-processing"></a>
### URL 처리

Vite와 함께 자산을 HTML, CSS, JS에서 참조할 때 주의할 점이 있습니다. 절대 경로 자산은 Vite가 빌드에 포함하지 않으므로 퍼블릭(public) 디렉토리에 해당 자산이 반드시 있어야 합니다.

상대경로 자산은 참조하는 파일을 기준으로 경로가 해석됩니다. 이러한 자산은 Vite가 재작성, 버전 관리, 번들링을 수행합니다.

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

Vite의 상대경로와 절대경로 처리 예시는 다음과 같습니다:

```html
<!-- 이 자산은 Vite에서 처리하지 않고 빌드에 포함되지 않습니다 -->
<img src="/taylor.png" />

<!-- 이 자산은 Vite에서 다시 쓰이고 버전 관리되며 번들 됩니다 -->
<img src="../../images/abigail.png" />
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업하기

Vite의 CSS 지원에 대한 자세한 내용은 [Vite 문서](https://vitejs.dev/guide/features.html#css)를 참고하세요. PostCSS 플러그인 예를 들어 [Tailwind](https://tailwindcss.com)를 사용한다면 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 자동으로 적용합니다:

```js
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

<a name="working-with-blade-and-routes"></a>
## Blade 및 라우트 작업하기

<a name="blade-processing-static-assets"></a>
### Vite로 정적 자산 처리하기

JavaScript 또는 CSS에서 자산을 참조하면 Vite가 자동으로 처리하고 버전 관리를 수행합니다. Blade 기반 애플리케이션의 경우, 오직 Blade 템플릿에서만 참조하는 정적 자산도 Vite로 처리하려면, 해당 정적 자산을 애플리케이션 진입점에 임포트하여 Vite가 이를 인지하도록 만들어야 합니다.

예를 들어 `resources/images` 폴더 내 모든 이미지와 `resources/fonts` 폴더 내 모든 폰트를 처리하고자 할 때, 진입점인 `resources/js/app.js`에 다음 코드를 추가합니다:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이제 `npm run build` 실행 시 이 자산들도 Vite에 의해 처리됩니다. Blade 템플릿에서는 `Vite::asset` 메서드로 버전 관리된 URL을 참조할 수 있습니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}" />
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade 기반 서버사이드 렌더링 앱에서는 Vite가 개발 중 뷰 파일 변경 시 브라우저를 자동으로 새로 고치도록 도와 개발 생산성을 높입니다. 사용하려면 `refresh` 옵션을 `true`로 설정하세요.

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

`refresh`가 `true`일 때 파일 저장 시 다음 경로 내 파일 변경을 감지하고 전체 페이지 새로고침을 수행합니다:

- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

특히 `routes/**` 경로 감시는 [Ziggy](https://github.com/tighten/ziggy)를 활용해 프론트엔드에서 라우트 링크를 생성할 때 유용합니다.

기본 경로 목록이 맞지 않으면 직접 커스텀 경로 배열을 지정할 수 있습니다:

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

Laravel Vite 플러그인은 내부적으로 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 고급 설정이 필요한 경우 `refresh` 옵션에 객체 배열을 전달할 수 있습니다:

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

자바스크립트 애플리케이션에서 자주 참조하는 디렉토리에는 보통 별칭을 만듭니다([별칭 설명](#aliases) 참고). Blade에서도 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드로 별칭(매크로)을 만들 수 있습니다. 보통은 서비스 프로바이더의 `boot` 메서드에서 정의합니다:

```php
/**
 * 애플리케이션 서비스 초기화.
 *
 * @return void
 */
public function boot()
{
    Vite::macro('image', fn ($asset) => $this->asset("resources/images/{$asset}"));
}
```

이 매크로는 Blade 템플릿에서 호출할 수 있습니다. 예를 들어 위와 같이 정의한 `image` 매크로로 `resources/images/logo.png` 자산을 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo" />
```

<a name="custom-base-urls"></a>
## 커스텀 기본 URL

Vite로 빌드한 자산이 애플리케이션과 별도의 도메인(예: CDN)에 배포되는 경우, `.env` 파일에서 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

이렇게 설정하면 모든 재작성된 자산 URL은 지정한 값으로 접두사 처리됩니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

단, [절대 URL은 Vite가 재작성하지 않습니다](#url-processing). 따라서 별도로 접두사 처리되지 않습니다.

<a name="environment-variables"></a>
## 환경 변수

애플리케이션 `.env` 파일에서 `VITE_` 접두사를 붙이면 환경 변수를 JavaScript에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

주입된 변수는 `import.meta.env` 객체를 통해 접근 가능합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트 시 Vite 비활성화

Laravel의 Vite 통합은 테스트 실행 시에도 자산을 해결하려 시도하므로, 개발 서버 실행이나 빌드가 필요합니다.

테스트용으로 Vite를 모킹(Mock)하려면 Laravel의 `TestCase` 클래스를 상속하는 테스트에서 `withoutVite` 메서드를 호출하세요:

```php
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example()
    {
        $this->withoutVite();

        // ...
    }
}
```

모든 테스트에서 Vite를 비활성화하려면 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite`를 호출합니다:

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

Laravel Vite 플러그인은 Vite와 함께 서버사이드 렌더링 환경 구성을 쉽게 도와줍니다. 시작하려면 `resources/js/ssr.js`에 SSR 진입점 파일을 만들고 Laravel 플러그인에 `ssr` 옵션을 지정하세요:

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

SSR 진입점 빌드를 잊지 않도록 `package.json`의 빌드 스크립트를 다음과 같이 수정하는 것을 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

이후 SSR 서버를 빌드하고 시작하려면 다음 명령어를 실행하세요:

```sh
npm run build
node bootstrap/ssr/ssr.mjs
```

> [!NOTE]
> Laravel [스타터 킷](/docs/9.x/starter-kits)은 Laravel, Inertia SSR, Vite 구성을 포함합니다. 빠르게 시작하려면 [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-inertia)를 참고하세요.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) nonce

스크립트와 스타일 태그에 [nonce 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함해 [콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)을 적용하려면, 맞춤 [미들웨어](/docs/9.x/middleware)에서 `useCspNonce` 메서드를 호출하여 nonce를 생성하거나 지정할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Vite;

class AddContentSecurityPolicyHeaders
{
    /**
     * 들어오는 요청 처리.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```

`useCspNonce`를 호출하면 Laravel은 생성하는 모든 스크립트와 스타일 태그에 자동으로 `nonce` 속성을 삽입합니다.

다른 곳에서도 nonce가 필요할 경우(예: Laravel 스타터 킷에 포함된 [Ziggy `@route` 디렉티브](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)) `cspNonce` 메서드로 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 nonce를 가지고 있다면 이를 인자로 전달해 Vite에 지정할 수도 있습니다:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI)

만약 Vite 매니페스트에 `integrity` 해시가 포함되어 있다면, Laravel이 만드는 모든 스크립트와 스타일 태그에 자동으로 `integrity` 속성을 추가해 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용합니다.

기본적으로 Vite는 매니페스트에 `integrity`를 포함하지 않습니다. 사용하려면 [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하세요:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

그리고 `vite.config.js`에 활성화합니다:

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

매니페스트 내 무결성 해시 키를 변경하려면 다음과 같이 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

자동 감지를 완전히 비활성화하려면 `false`를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의 속성

`data-turbo-track` 같은 추가적인 속성을 스크립트와 스타일 태그에 넣고 싶다면, `useScriptTagAttributes`와 `useStyleTagAttributes` 메서드를 사용하세요. 보통 서비스 프로바이더에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 속성에 값 지정
    'async' => true, // 값 없이 속성만 지정
    'integrity' => false, // 기본 삽입 속성 제외
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

속성을 조건부로 지정할 때는 콜백 함수를 사용할 수 있습니다. 콜백 인자로는 자산 경로, URL, 매니페스트 청크, 전체 매니페스트 배열이 전달됩니다:

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
> 개발 서버 실행 중에는 `$chunk`와 `$manifest` 인자가 `null`일 수 있습니다.

<a name="advanced-customization"></a>
## 고급 사용자 정의

Laravel Vite 플러그인은 기본적으로 대부분 애플리케이션에 적합한 합리적인 설정을 제공합니다. 하지만 추가로 다음 메서드 및 옵션을 사용해 `@vite` Blade 디렉티브를 대체하며 옵션을 세밀하게 조절할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 위치 변경
            ->useBuildDirectory('bundle') // 빌드 디렉토리 변경
            ->useManifestFilename('assets.json') // 매니페스트 파일 이름 변경
            ->withEntryPoints(['resources/js/app.js']) // 진입점 지정
    }}
</head>
```

`vite.config.js`에도 동일한 구성을 지정해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 위치 변경
            buildDirectory: 'bundle', // 빌드 디렉토리 변경
            input: ['resources/js/app.js'], // 진입점 지정
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일 이름 변경
    },
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정하기

Vite 생태계 일부 플러그인은 경로가 `/`로 시작하면 항상 Vite 개발 서버임을 가정합니다. 하지만 Laravel 통합 환경에서는 그렇지 않습니다.

예를 들어 `vite-imagetools` 플러그인은 다음과 같이 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" />
```

`vite-imagetools` 플러그인은 `/@imagetools`로 시작하는 URL이 Vite에서 인터셉트되어 처리된다고 예상합니다. 이런 플러그인을 사용한다면 수동으로 URL을 수정해야 하며, `vite.config.js`에 `transformOnServe` 옵션을 사용해 개발 서버 URL을 붙여줄 수 있습니다:

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

이제 Vite 개발 서버가 실행되는 동안 다음처럼 개발 서버 URL을 포함하는 완전한 경로를 출력합니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520" /><!-- [tl! add] -->
```