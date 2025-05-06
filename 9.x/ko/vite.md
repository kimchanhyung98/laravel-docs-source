# 에셋 번들링(Vite)

- [소개](#introduction)
- [설치 및 설정](#installation)
  - [Node 설치](#installing-node)
  - [Vite 및 Laravel 플러그인 설치](#installing-vite-and-laravel-plugin)
  - [Vite 설정](#configuring-vite)
  - [스크립트와 스타일 로드하기](#loading-your-scripts-and-styles)
- [Vite 실행](#running-vite)
- [JavaScript 다루기](#working-with-scripts)
  - [별칭(Aliases)](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Inertia](#inertia)
  - [URL 처리](#url-processing)
- [스타일시트 다루기](#working-with-stylesheets)
- [Blade & 라우트와 함께 사용하기](#working-with-blade-and-routes)
  - [정적 에셋 처리](#blade-processing-static-assets)
  - [저장 시 새로고침](#blade-refreshing-on-save)
  - [Blade에서 별칭 사용](#blade-aliases)
- [사용자 지정 베이스 URL](#custom-base-urls)
- [환경 변수](#environment-variables)
- [테스트에서 Vite 비활성화](#disabling-vite-in-tests)
- [서버 사이드 렌더링(SSR)](#ssr)
- [스크립트 & 스타일 태그 속성](#script-and-style-attributes)
  - [Content Security Policy(CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity(SRI)](#subresource-integrity-sri)
  - [임의의 속성 추가](#arbitrary-attributes)
- [고급 커스터마이징](#advanced-customization)
  - [개발 서버 URL 교정](#correcting-dev-server-urls)

<a name="introduction"></a>
## 소개

[Vite](https://vitejs.dev)는 매우 빠른 개발 환경을 제공하고, 코드를 프로덕션 용으로 번들링하는 최신 프런트엔드 빌드 도구입니다. Laravel로 애플리케이션을 개발할 때, 일반적으로 Vite를 이용해 애플리케이션의 CSS와 JavaScript 파일을 프로덕션 수준의 에셋으로 번들링하게 됩니다.

Laravel은 공식 플러그인과 Blade 지시어를 통해 Vite와의 완벽한 통합을 제공합니다. 이를 통해 개발 및 프로덕션 환경 모두에서 에셋을 손쉽게 로딩할 수 있습니다.

> **참고**
> Laravel Mix를 실행 중이신가요? Vite는 최근 Laravel 버전에서 Laravel Mix를 대체합니다. Mix에 대한 문서는 [Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하세요. Vite로 전환하고 싶다면, [마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.

<a name="vite-or-mix"></a>
#### Vite와 Laravel Mix 중 선택하기

기존 Laravel 애플리케이션에서는 에셋 번들링을 위해 [webpack](https://webpack.js.org/) 기반의 [Mix](https://laravel-mix.com/)를 사용했습니다. Vite는 풍부한 JavaScript 애플리케이션 개발에서 더 빠르고 생산적인 경험을 주는 것에 초점을 맞춥니다. 특히 [Inertia](https://inertiajs.com) 등 SPA(단일 페이지 앱)를 개발한다면 Vite가 최적입니다.

Vite는 [Livewire](https://laravel-livewire.com)처럼 JavaScript "스프링클"을 사용하는 전통적인 서버 렌더 앱에도 잘 작동합니다. 다만, Laravel Mix가 지원하는 일부 기능(자바스크립트에서 직접 참조하지 않은 임의의 에셋 복사 등)이 Vite에는 포함되어 있지 않습니다.

<a name="migrating-back-to-mix"></a>
#### Mix로 다시 마이그레이션하기

새 Laravel 애플리케이션을 Vite로 시작했지만, 다시 Laravel Mix와 webpack으로 돌아가야 하나요? 걱정하지 마세요. [Vite에서 Mix로 마이그레이션 공식 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-vite-to-laravel-mix)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정

> **참고**
> 아래 문서는 Laravel Vite 플러그인을 수동으로 설치·설정하는 방법을 설명합니다. Laravel의 [스타터 킷](/docs/{{version}}/starter-kits)에는 이 모든 구성작업이 이미 포함되어 있으니, Laravel과 Vite를 가장 빠르게 시작하고 싶다면 스타터 킷을 사용하세요.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인 사용 전, 반드시 Node.js(16+)와 NPM이 설치되어 있어야 합니다:

```sh
node -v
npm -v
```

[공식 Node 웹사이트](https://nodejs.org/en/download/)의 GUI 인스톨러를 사용해 최신 Node 및 NPM을 손쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 쓴다면, Sail을 통해 Node와 NPM을 사용할 수도 있습니다:

```sh
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```

<a name="installing-vite-and-laravel-plugin"></a>
### Vite 및 Laravel 플러그인 설치

새 Laravel 프로젝트의 루트에는 `package.json` 파일이 있습니다. 이 기본 `package.json`에는 Vite 및 Laravel 플러그인 사용에 필요한 모든 것이 이미 들어 있습니다. NPM을 이용해 프런트엔드 의존성을 설치하세요:

```sh
npm install
```

<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트의 `vite.config.js` 파일을 통해 설정됩니다. 이 파일을 필요에 따라 자유롭게 수정할 수 있고, 예를 들어 `@vitejs/plugin-vue`나 `@vitejs/plugin-react` 같은 추가 플러그인도 설치할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점(entry point)을 지정해야 합니다. 이는 JavaScript, CSS 파일 혹은 TypeScript, JSX, TSX, Sass처럼 전처리된 언어 등도 지정 가능합니다.

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

SPA(단일 페이지 앱)나 Inertia 기반 앱을 구축 중이라면, Vite를 CSS 진입점 없이 사용하는 게 더 적합합니다:

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

이 경우 CSS를 JavaScript에서 임포트해야 합니다. 일반적으로 `resources/js/app.js` 파일에서 다음처럼 처리합니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```

Laravel 플러그인은 다중 엔트리 포인트, [SSR 엔트리 포인트](#ssr) 등 고급 설정도 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버(HTTPS)와 함께 사용하기

로컬 개발 웹 서버가 HTTPS로 앱을 제공한다면, Vite 개발 서버와의 연결에 문제를 겪을 수 있습니다.

[Laravel Valet](/docs/{{version}}/valet) 등을 사용 중이고, 애플리케이션에 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행했다면, Vite 개발 서버가 Valet의 TLS 인증서를 자동으로 사용하게 설정할 수 있습니다:

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

다른 웹 서버라면, 신뢰할 수 있는 인증서를 직접 생성하고, Vite가 이를 사용하도록 직접 지정해야 합니다:

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

만약 신뢰할 수 있는 인증서를 생성할 수 없다면, [`@vitejs/plugin-basic-ssl` 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 설정하세요. 비신뢰 인증서 사용 시, 브라우저에서 Vite 개발 서버의 인증서 경고를 수락해야 하며, `npm run dev` 실행 시 콘솔에 표시되는 "Local" 링크를 클릭하면 설정할 수 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트와 스타일 로드하기

Vite 엔트리 포인트를 설정하고 나면, 애플리케이션의 루트 템플릿 `<head>`에 `@vite()` Blade 지시어만 추가하면 자동으로 로드됩니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

CSS를 JavaScript로 임포트하는 경우, JavaScript 진입점만 추가해도 됩니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```

`@vite` 지시어는 Vite 개발 서버를 자동 감지하며, Hot Module Replacement(HMR)를 위한 Vite 클라이언트도 자동 추가합니다. 빌드 모드에서는 컴파일되고 버전이 적용된 에셋(CSS 포함)이 로드됩니다.

필요하다면, `@vite` 지시어 호출 시 컴파일 에셋의 빌드 경로도 지정할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- 빌드 경로는 public 경로 기준 상대경로입니다. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```

<a name="running-vite"></a>
## Vite 실행

Vite는 두 가지 방식으로 실행할 수 있습니다. 개발 중에는 `dev` 명령을 사용해 개발 서버를 띄울 수 있습니다. 이 서버는 파일이 변경되면 열려 있는 브라우저에서 즉시 반영합니다.

또는, `build` 명령을 통해 애플리케이션 에셋에 버전 관리 및 번들링을 적용하여 프로덕션 배포를 준비할 수 있습니다:

```shell
# Vite 개발 서버 실행...
npm run dev

# 프로덕션용 에셋을 빌드 및 버전 적용...
npm run build
```

<a name="working-with-scripts"></a>
## JavaScript 다루기

<a name="aliases"></a>
### 별칭(Aliases)

Laravel 플러그인은 시작하기 쉽게 자주 사용하는 디렉터리의 alias(별칭)를 제공합니다:

```js
{
    '@' => '/resources/js'
}
```

`vite.config.js`에서 '@' 별칭을 원하는 값으로 덮어쓸 수 있습니다:

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

[Vue](https://vuejs.org/) 프레임워크를 이용해 프론트엔드를 빌드하려면 `@vitejs/plugin-vue` 플러그인 추가 설치가 필요합니다:

```sh
npm install --save-dev @vitejs/plugin-vue
```

설치 후, 해당 플러그인을 `vite.config.js`에도 등록하세요. Vue 플러그인을 Laravel과 함께 사용할 때는 몇 가지 추가 옵션이 필요합니다:

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
                    // SFC 내 자원 URL 재작성 설정
                    base: null,
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```

> **참고**
> Laravel의 [스타터 킷](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, Vue, Vite 설정이 포함돼 있습니다. Laravel, Vue, Vite를 가장 빠르게 시작하려면 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 살펴보세요.

<a name="react"></a>
### React

[React](https://reactjs.org/) 프레임워크를 사용하려면 `@vitejs/plugin-react` 플러그인을 설치하세요:

```sh
npm install --save-dev @vitejs/plugin-react
```

`vite.config.js`에 플러그인을 등록합니다:

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

JSX가 포함된 파일은 반드시 `.jsx` 또는 `.tsx` 확장자를 사용해야 하며, 엔트리 포인트도 필요하다면 위와 같이 갱신해야 합니다.

또한 기존 `@vite` Blade 지시어와 함께 추가적으로 `@viteReactRefresh` 지시어도 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```

`@viteReactRefresh`는 반드시 `@vite` 보다 먼저 호출해야 합니다.

> **참고**
> Laravel의 [스타터 킷](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, React, Vite 설정이 포함돼 있습니다. 가장 빠른 방법은 [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)를 사용하세요.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트 로딩을 돕는 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 사용하는 예시지만, React 등에서도 활용 가능합니다:

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

> **참고**
> Laravel의 [스타터 킷](/docs/{{version}}/starter-kits)에는 이미 Inertia, Vite 관련 설정이 되어 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 빠르게 시작하세요.

<a name="url-processing"></a>
### URL 처리

Vite를 사용할 때 HTML, CSS, JS에서 에셋을 참조하면 몇 가지 유의할 점이 있습니다. 절대 경로로 에셋을 참조할 때 Vite는 해당 에셋을 번들에 포함하지 않으니, 반드시 public 디렉터리에 파일이 존재해야 합니다.

반면, 상대 경로로 참조한 에셋은 해당 파일의 위치 기준으로 경로를 작성해야 하며, Vite가 자동으로 재작성, 버전 적용, 번들링을 수행합니다.

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

아래 예시를 보면 Vite가 상대/절대 경로를 어떻게 처리하는지 알 수 있습니다:

```html
<!-- Vite에서 처리하지 않으므로 빌드에 포함되지 않음 -->
<img src="/taylor.png">

<!-- Vite에서 경로 재작성, 버전 부여, 번들에 포함됨 -->
<img src="../../images/abigail.png">
```

<a name="working-with-stylesheets"></a>
## 스타일시트 다루기

Vite의 CSS 지원에 대해 더 알고 싶다면 [Vite 공식문서](https://vitejs.dev/guide/features.html#css)를 참고하세요. Tailwind와 같은 PostCSS 플러그인을 사용할 경우, 프로젝트 루트에 `postcss.config.js` 파일을 생성하면 Vite가 자동 적용합니다:

```js
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
```

<a name="working-with-blade-and-routes"></a>
## Blade & 라우트와 함께 사용하기

<a name="blade-processing-static-assets"></a>
### 정적 에셋 처리

JavaScript나 CSS에서 참조하는 에셋은 Vite가 자동으로 처리하고 버전을 부여합니다. Blade 기반 애플리케이션의 경우, Blade 템플릿에서만 참조하는 정적 에셋도 Vite로 처리·버전 적용이 가능합니다.

이를 위해서는 Vite가 해당 에셋을 인지할 수 있도록 엔트리 포인트에서 명시적으로 import 해야 합니다. 예를 들어, `resources/images`의 모든 이미지와 `resources/fonts`의 모든 폰트를 처리하려면, `resources/js/app.js`에 아래와 같이 추가합니다:

```js
import.meta.glob([
  '../images/**',
  '../fonts/**',
]);
```

이 에셋들은 `npm run build` 실행 시 Vite가 자동 처리합니다. Blade 템플릿에서 에셋을 참조하려면 `Vite::asset` 메서드를 쓰세요:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

Blade로 서버 사이드 렌더링을 하는 경우, Vite는 뷰 파일에 변경사항이 생기면 브라우저를 자동 새로고침해 개발 효율을 높여줍니다. 시작하려면 `refresh` 옵션을 `true`로 지정하세요.

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

`refresh` 옵션이 `true`이면, 다음 디렉터리 내 파일 저장 시 브라우저가 전체 새로고침됩니다(`npm run dev` 중):

- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

라우트 디렉터리 감시는 [Ziggy](https://github.com/tighten/ziggy) 등에서 프런트엔드 라우트 링크 생성 시 유용합니다.

기본 경로가 맞지 않으면 직접 감시할 경로 배열을 지정할 수도 있습니다:

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

내부적으로 Laravel Vite 플러그인은 [`vite-plugin-full-reload`](https://github.com/ElMassimo/vite-plugin-full-reload)를 사용하며, 고급 옵션도 지원합니다. 커스터마이징이 필요하다면 `config` 옵션을 지정하세요:

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
### Blade에서 별칭 사용

JavaScript에서 디렉터리 별칭([aliases](#aliases))을 자주 생성하는 것처럼, Blade에서도 별칭을 만들 수 있습니다. `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 활용하세요. 보통은 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록합니다.

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Vite::macro('image', fn ($asset) => $this->asset("resources/images/{$asset}"));
    }

한 번 매크로를 정의하면 Blade 템플릿에서 바로 사용할 수 있습니다. 예를 들어, 위에서 만든 `image` 매크로로 `resources/images/logo.png`를 이렇게 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

<a name="custom-base-urls"></a>
## 사용자 지정 베이스 URL

Vite로 빌드한 에셋을 CDN 등 애플리케이션과 별도의 도메인에 배포할 경우, 앱의 `.env` 파일에 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```

이후 에셋에 대해 재작성되는 모든 URL은 다음처럼 지정 값이 접두어로 붙게 됩니다:

```nothing
https://cdn.example.com/build/assets/app.9dce8d17.js
```

[절대 URL은 Vite가 재작성하지 않으므로](#url-processing), 접두어가 붙지 않는 점에 유의하세요.

<a name="environment-variables"></a>
## 환경 변수

자바스크립트에서 환경 변수를 사용하려면, `.env` 파일에서 변수명을 `VITE_`로 시작하게 지정하세요:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```

코드에서는 `import.meta.env` 객체를 통해 접근합니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화

Laravel의 Vite 통합은 테스트 실행 시에도 에셋을 resolve하려 하므로, 개발 서버를 띄우거나 에셋을 미리 빌드해야 할 수 있습니다.

테스트 중 Vite를 모킹하고 싶다면, Laravel의 `TestCase`를 상속받는 모든 테스트에서 `withoutVite` 메서드를 호출하세요:

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

전체 테스트에서 Vite를 비활성화하려면, 기본 `TestCase` 클래스의 `setUp`에서 호출하세요:

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
## 서버 사이드 렌더링(SSR)

Laravel Vite 플러그인으로 Vite 기반 SSR 구축이 매우 간단해집니다. 먼저 `resources/js/ssr.js`에 SSR 엔트리 포인트 파일을 만들고, Laravel 플러그인 옵션에 지정하세요:

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

SSR 엔트리 포인트 빌드를 까먹지 않도록, `package.json`의 "build" 스크립트를 아래처럼 수정하는 것이 좋습니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```

SSR 서버를 빌드 및 시작하려면 다음 명령을 사용하세요:

```sh
npm run build
node bootstrap/ssr/ssr.mjs
```

> **참고**
> Laravel의 [스타터 킷](/docs/{{version}}/starter-kits)에는 Inertia SSR, Vite 관련 설정이 포함돼 있습니다. [Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-inertia)로 쉽게 시작할 수 있습니다.

<a name="script-and-style-attributes"></a>
## 스크립트 & 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### Content Security Policy(CSP) Nonce

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일환으로, 스크립트/스타일 태그에 [`nonce` 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하려면, 커스텀 [미들웨어](/docs/{{version}}/middleware)에서 `useCspNonce` 메서드를 사용하세요:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Vite;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
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

`useCspNonce` 호출 이후, Laravel은 생성된 모든 스크립트 및 스타일 태그에 자동으로 nonce 속성을 추가합니다.

다른 곳(예: [Ziggy의 `@route` 지시어](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy))에서도 nonce가 필요하면 `cspNonce` 메서드로 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```

이미 가진 nonce를 Laravel이 사용하도록 하려면 `useCspNonce`에 nonce 값을 전달하세요:

```php
Vite::useCspNonce($nonce);
```

<a name="subresource-integrity-sri"></a>
### Subresource Integrity(SRI)

Vite 매니페스트에 에셋의 `integrity` 해시가 포함되면, Laravel은 생성하는 모든 스크립트·스타일 태그에 자동으로 `integrity` 속성을 추가해 [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)를 강화합니다. Vite는 기본적으로 `integrity` 해시를 매니페스트에 포함하지 않지만, [`vite-plugin-manifest-sri`](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치해 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```

이 플러그인을 `vite.config.js`에 등록하세요:

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

필요하다면 integrity 해시가 저장되는 매니페스트 키 경로를 커스터마이징할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```

이 자동 감지를 완전히 비활성화하고 싶다면, `useIntegrityKey`에 `false`를 전달하세요:

```php
Vite::useIntegrityKey(false);
```

<a name="arbitrary-attributes"></a>
### 임의의 속성 추가

스크립트/스타일 태그에 추가 속성(예: [`data-turbo-track`](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change))을 포함하려면, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 활용하세요. 일반적으로는 [서비스 프로바이더](/docs/{{version}}/providers)에서 호출합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // 값 지정 속성...
    'async' => true, // 값 없는 속성...
    'integrity' => false, // 기본 포함될 속성을 제외...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```

조건에 따라 동적으로 속성을 추가하고 싶으면 콜백도 넘길 수 있습니다. 콜백에는 에셋 경로, URL, 매니페스트 청크, 전체 매니페스트가 인자로 들어옵니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```

> **경고**
> Vite 개발 서버가 실행 중일 때는 `$chunk` 및 `$manifest`가 `null`이 됩니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

기본적으로 Laravel의 Vite 플러그인은 대부분의 애플리케이션에 적합한 설정을 제공하지만, 때로는 더 큰 커스터마이징이 필요할 수도 있습니다. 다음과 같은 메서드/옵션을 사용해 `@vite` Blade 지시어 대신 사용할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // "hot" 파일 경로 지정...
            ->useBuildDirectory('bundle') // 빌드 디렉터리 지정...
            ->useManifestFilename('assets.json') // 매니페스트 파일명 지정...
            ->withEntryPoints(['resources/js/app.js']) // 엔트리포인트 지정...
    }}
</head>
```

`vite.config.js`에도 같은 설정을 명시해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // "hot" 파일 경로 지정...
            buildDirectory: 'bundle', // 빌드 디렉터리 지정...
            input: ['resources/js/app.js'], // 엔트리포인트 지정...
        }),
    ],
    build: {
      manifest: 'assets.json', // 매니페스트 파일명 지정...
    },
});
```

<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 교정

Vite 생태계의 일부 플러그인은 슬래시('/')로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합에서는 꼭 그렇지 않을 수 있습니다.

예를 들어, `vite-imagetools` 플러그인은 Vite가 에셋을 제공할 때 다음과 같은 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

이 플러그인은 `/@imagetools`로 시작하는 URL을 Vite가 가로채 처리하길 기대합니다. 이런 플러그인을 사용할 때는 URL을 직접 교정해야 합니다. `vite.config.js`에서 `transformOnServe` 옵션을 사용하세요.

아래 예시는, 빌드 코드 중 `/@imagetools`를 Vite 개발 서버의 URL로 변경하는 방법입니다:

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

이제 Vite가 에셋을 제공하는 동안, 다음과 같이 Vite 개발 서버를 가리키는 URL이 출력됩니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
