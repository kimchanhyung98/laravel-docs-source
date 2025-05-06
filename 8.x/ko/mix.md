# 에셋 컴파일링 (Mix)

- [소개](#introduction)
- [설치 및 설정](#installation)
- [Mix 실행](#running-mix)
- [스타일시트 작업](#working-with-stylesheets)
    - [Tailwind CSS](#tailwindcss)
    - [PostCSS](#postcss)
    - [Sass](#sass)
    - [URL 처리](#url-processing)
    - [소스맵](#css-source-maps)
- [자바스크립트 작업](#working-with-scripts)
    - [Vue](#vue)
    - [React](#react)
    - [벤더 추출](#vendor-extraction)
    - [커스텀 Webpack 설정](#custom-webpack-configuration)
- [버전 관리 / 캐시 무효화](#versioning-and-cache-busting)
- [Browsersync 자동 리로드](#browsersync-reloading)
- [환경 변수](#environment-variables)
- [알림](#notifications)

<a name="introduction"></a>
## 소개

[Laravel Mix](https://github.com/JeffreyWay/laravel-mix)는 [Laracasts](https://laracasts.com) 창립자인 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션의 [webpack](https://webpack.js.org) 빌드 스텝을 여러 CSS 및 JavaScript 프리프로세서와 함께 간결하게 정의할 수 있는 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 쉽고 빠르게 컴파일하고 최소화(Minify)할 수 있게 해줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 유연하게 정의할 수 있습니다. 예를 들면 다음과 같습니다:

    mix.js('resources/js/app.js', 'public/js')
        .postCss('resources/css/app.css', 'public/css');

webpack이나 자산 컴파일 시작에 대해 혼란스럽고 막막했던 경험이 있다면, Laravel Mix를 통해 쉽게 시작할 수 있습니다. 그러나 애플리케이션 개발 시 Mix 사용은 필수가 아니며, 원하는 자산 파이프라인 도구를 자유롭게 사용하거나 아예 사용하지 않아도 됩니다.

> {tip} Laravel과 [Tailwind CSS](https://tailwindcss.com)를 함께 사용하여 애플리케이션을 빠르게 시작하고 싶다면, [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 확인해보세요.

<a name="installation"></a>
## 설치 및 설정

<a name="installing-node"></a>
#### Node 설치

Mix를 실행하기 전에, 먼저 Node.js와 NPM이 시스템에 설치되어 있어야 합니다:

    node -v
    npm -v

[공식 Node 웹사이트](https://nodejs.org/en/download/)에서 제공하는 그래픽 설치 프로그램을 이용해 Node와 NPM의 최신 버전을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](/docs/{{version}}/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 사용할 수도 있습니다:

    ./sail node -v
    ./sail npm -v

<a name="installing-laravel-mix"></a>
#### Laravel Mix 설치

마지막으로 해야 할 일은 Laravel Mix 설치입니다. Laravel을 새로 설치하면, 루트 디렉토리 구조에 `package.json` 파일이 생성됩니다. 기본 `package.json` 파일에는 Laravel Mix를 사용 시작하는 데 필요한 모든 패키지들이 이미 포함되어 있습니다. 이 파일은 `composer.json`과 비슷하지만, PHP가 아닌 Node 의존성 관리를 위한 파일입니다. 의존성을 설치하려면 다음을 실행하세요:

    npm install

<a name="running-mix"></a>
## Mix 실행

Mix는 [webpack](https://webpack.js.org) 위에 구성된 설정 레이어이므로, Mix 태스크를 실행하려면 기본 Laravel `package.json`에 포함된 NPM 스크립트 중 하나만 실행하면 됩니다. `dev` 또는 `production` 스크립트를 실행하면 애플리케이션의 모든 CSS와 JavaScript 에셋이 컴파일되어 `public` 디렉토리에 배치됩니다:

    // 모든 Mix 태스크 실행...
    npm run dev

    // 모든 Mix 태스크 실행 후 결과물 최소화...
    npm run prod

<a name="watching-assets-for-changes"></a>
#### 에셋 변경 감시

`npm run watch` 명령을 실행하면 터미널에서 계속 실행되며, 관련된 CSS 및 JavaScript 파일의 변경 사항을 감시합니다. webpack은 이 파일들에 변경이 감지되면 자동으로 에셋을 다시 컴파일합니다:

    npm run watch

특정 로컬 개발 환경에서는 webpack이 파일 변경 사항을 감지하지 못할 수 있습니다. 이 경우, `watch-poll` 명령 사용을 고려하세요:

    npm run watch-poll

<a name="working-with-stylesheets"></a>
## 스타일시트 작업

애플리케이션의 `webpack.mix.js` 파일은 모든 에셋 컴파일의 엔트리 포인트입니다. 이는 [webpack](https://webpack.js.org)의 가벼운 구성 래퍼 역할을 합니다. Mix 태스크는 체이닝으로 결합하여 원하는 대로 에셋 컴파일 방식을 정의할 수 있습니다.

<a name="tailwindcss"></a>
### Tailwind CSS

[Tailwind CSS](https://tailwindcss.com)는 HTML에서 벗어나지 않고 멋진 사이트를 만들 수 있는 모던 유틸리티-퍼스트 CSS 프레임워크입니다. Laravel 프로젝트에서 Laravel Mix로 Tailwind를 사용하려면 다음과 같이 진행합니다. 먼저, NPM을 이용해 Tailwind를 설치하고 Tailwind 설정 파일을 생성합니다:

    npm install

    npm install -D tailwindcss

    npx tailwindcss init

`init` 명령은 `tailwind.config.js` 파일을 생성합니다. 이 파일의 `content` 섹션에서 HTML 템플릿, JavaScript 컴포넌트, Tailwind 클래스 이름을 포함하는 기타 소스 파일의 경로를 지정하면, 불필요한 CSS 클래스가 프로덕션 빌드에서 제거됩니다:

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

다음으로, Tailwind의 각 "레이어"를 애플리케이션의 `resources/css/app.css` 파일에 추가하세요:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

레이어 구성을 마쳤다면, 다음과 같이 Tailwind를 적용한 CSS를 컴파일하도록 `webpack.mix.js` 파일을 수정하세요:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

마지막으로, 애플리케이션의 주요 레이아웃 템플릿에서 스타일시트를 참조해야 합니다. 대부분의 애플리케이션은 `resources/views/layouts/app.blade.php`와 같은 위치에 템플릿을 저장합니다. 또한, 반응형 뷰포트 `meta` 태그가 없다면 추가하세요:

```html
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="/css/app.css" rel="stylesheet">
</head>
```

<a name="postcss"></a>
### PostCSS

[PostCSS](https://postcss.org/)는 Laravel Mix에 기본 포함되어 있는 강력한 CSS 트랜스포머 툴입니다. 기본적으로 Mix는 인기 있는 [Autoprefixer](https://github.com/postcss/autoprefixer) 플러그인을 활용하여 필요한 CSS3 공급사 프리픽스(벤더 프리픽스)를 자동으로 추가합니다. 물론 원하는 플러그인도 추가하여 사용할 수 있습니다.

먼저, 원하는 플러그인을 NPM으로 설치한 후, Mix의 `postCss` 메서드 호출 시 플러그인 배열에 추가하세요. `postCss`는 첫 번째 인자로 CSS 파일 경로, 두 번째 인자로 컴파일 결과 파일을 배치할 디렉터리를 받습니다:

    mix.postCss('resources/css/app.css', 'public/css', [
        require('postcss-custom-properties')
    ]);

또는, 별도의 플러그인 없이 간단한 CSS 컴파일 및 최소화만 하고자 할 경우 다음과 같이 사용하면 됩니다:

    mix.postCss('resources/css/app.css', 'public/css');

<a name="sass"></a>
### Sass

`sass` 메서드를 사용하면 [Sass](https://sass-lang.com/)를 웹 브라우저가 이해할 수 있는 CSS로 컴파일할 수 있습니다. `sass`의 첫 번째 인자는 Sass 파일 경로, 두 번째 인자는 컴파일된 CSS가 저장될 디렉터리입니다:

    mix.sass('resources/sass/app.scss', 'public/css');

여러 개의 Sass 파일을 각각의 CSS 파일로 컴파일하거나, 결과 CSS의 출력 디렉터리를 맞춤 설정할 수도 있습니다:

    mix.sass('resources/sass/app.sass', 'public/css')
        .sass('resources/sass/admin.sass', 'public/css/admin');

<a name="url-processing"></a>
### URL 처리

Laravel Mix는 webpack 위에서 동작하므로 webpack의 몇 가지 개념을 이해하는 것이 중요합니다. CSS를 컴파일할 때 webpack은 스타일시트 내의 모든 `url()` 호출을 다시 작성(리라이트)하고 최적화합니다. 처음에는 다소 생소할 수도 있지만 매우 강력한 기능입니다. 예를 들어, 이미지에 상대 경로를 사용하는 Sass를 컴파일한다고 가정해 보세요:

    .example {
        background: url('../images/example.png');
    }

> {note} `url()`에 절대 경로를 사용한 경우, URL 재작성 대상에서 제외됩니다. 예: `url('/images/thing.png')` 또는 `url('http://example.com/images/thing.png')` 등은 변경되지 않습니다.

기본적으로 Laravel Mix와 webpack은 `example.png`를 찾아 `public/images` 폴더로 복사한 뒤, 결과 스타일시트에서 `url()`을 다시 작성합니다. 따라서 컴파일된 CSS는 다음과 같이 됩니다:

    .example {
        background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
    }

이 기능이 유용하지만, 기존 폴더 구조를 그대로 유지하고 싶으면 `url()` 재작성을 비활성화할 수 있습니다:

    mix.sass('resources/sass/app.scss', 'public/css').options({
        processCssUrls: false
    });

이렇게 하면, Mix는 어떠한 `url()` 도 재작성하지 않고 파일도 복사하지 않습니다. 즉, 컴파일된 CSS는 원본과 동일하게 유지됩니다:

    .example {
        background: url("../images/thing.png");
    }

<a name="css-source-maps"></a>
### 소스맵

기본적으로 비활성화 되어 있지만, `webpack.mix.js`에서 `mix.sourceMaps()` 메서드를 호출하여 소스맵을 활성화할 수 있습니다. 소스맵을 사용하면 브라우저 개발자 도구에서 컴파일된 에셋을 디버깅할 때 더 많은 정보를 얻을 수 있습니다(단, 컴파일 및 성능 비용이 발생할 수 있음):

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps();

<a name="style-of-source-mapping"></a>
#### 소스맵 스타일 지정

webpack은 다양한 [소스맵 스타일](https://webpack.js.org/configuration/devtool/#devtool)을 지원합니다. 기본적으로 Mix의 소스맵 스타일은 `eval-source-map`으로 빠른 재빌드를 지원합니다. 특정 스타일로 변경하고 싶다면 두 번째 인자에 스타일 명칭을 전달하세요:

    let productionSourceMaps = false;

    mix.js('resources/js/app.js', 'public/js')
        .sourceMaps(productionSourceMaps, 'source-map');

<a name="working-with-scripts"></a>
## 자바스크립트 작업

Mix는 모던 ECMAScript의 컴파일, 모듈 번들링, 최소화, 단순 자바스크립트 파일 연결 등 여러 기능을 제공합니다. 추가 설정 없이도 완벽하게 동작합니다:

    mix.js('resources/js/app.js', 'public/js');

이 한 줄만으로도 다음 기능을 이용할 수 있습니다:

<div class="content-list" markdown="1">

- 최신 EcmaScript 문법 지원
- 모듈 (Module)
- 프로덕션 환경에서 코드 최소화

</div>

<a name="vue"></a>
### Vue

`vue` 메서드를 사용하면 Vue 싱글 파일 컴포넌트 컴파일을 위한 Babel 플러그인이 자동으로 설치됩니다. 별도의 추가 설정이 필요하지 않습니다:

    mix.js('resources/js/app.js', 'public/js')
       .vue();

JavaScript 컴파일이 완료되면 애플리케이션에서 다음처럼 참조할 수 있습니다:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="react"></a>
### React

Mix는 React 지원을 위한 Babel 플러그인도 자동 설치할 수 있습니다. 사용을 시작하려면 `react` 메서드를 추가하면 됩니다:

    mix.js('resources/js/app.jsx', 'public/js')
       .react();

내부적으로 Mix는 적절한 `babel-preset-react` Babel 플러그인을 다운로드하고 포함합니다. 컴파일이 완료된 후에는 다음처럼 JavaScript 파일을 참조하면 됩니다:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="vendor-extraction"></a>
### 벤더 추출

React, Vue와 같은 벤더 라이브러리와 애플리케이션 전용 자바스크립트를 함께 번들하면 장기 캐싱(Long-term cache)이 어려워질 수 있습니다. 예를 들어, 코드 한 줄만 변경해도 벤더 라이브러리 전체를 브라우저가 다시 받아야 합니다.

만약 자바스크립트 코드를 자주 업데이트할 계획이라면, 모든 벤더 라이브러리를 별도의 파일로 분리하는 것이 좋습니다. 이렇게 하면 애플리케이션 코드가 변경되어도, 대용량 `vendor.js` 파일의 캐싱에는 영향이 없습니다. 이 작업은 Mix의 `extract` 메서드로 간편하게 처리할 수 있습니다:

    mix.js('resources/js/app.js', 'public/js')
        .extract(['vue'])

`extract` 메서드는 분리할 라이브러리나 모듈의 배열을 받습니다. 위 코드 조각을 사용하면 Mix는 아래 파일들을 생성합니다:

<div class="content-list" markdown="1">

- `public/js/manifest.js`: *Webpack 매니페스트 런타임*
- `public/js/vendor.js`: *벤더 라이브러리*
- `public/js/app.js`: *애플리케이션 코드*

</div>

JavaScript 오류를 방지하려면 반드시 아래 순서대로 파일을 로드해야 합니다:

    <script src="/js/manifest.js"></script>
    <script src="/js/vendor.js"></script>
    <script src="/js/app.js"></script>

<a name="custom-webpack-configuration"></a>
### 커스텀 Webpack 설정

때로는 기본 Webpack 설정을 수동으로 수정해야 할 수도 있습니다. 예를 들어, 특정 로더(loader)나 플러그인을 추가해야 하는 경우가 있습니다.

Mix는 `webpackConfig` 메서드를 제공하여 Webpack 설정을 부분적으로 덮어쓸 수 있습니다. `webpack.config.js` 파일을 직접 복사해 관리하지 않아도 되므로 편리합니다. `webpackConfig`는 객체를 인자로 받아 [Webpack 전용 설정](https://webpack.js.org/configuration/)을 추가할 수 있습니다.

    mix.webpackConfig({
        resolve: {
            modules: [
                path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
            ]
        }
    });

<a name="versioning-and-cache-busting"></a>
## 버전 관리 / 캐시 무효화

많은 개발자가 컴파일된 에셋에 타임스탬프나 고유 토큰을 덧붙여 브라우저가 최신 에셋을 반드시 불러오도록 합니다. Mix의 `version` 메서드를 사용하면 이 과정을 자동 처리할 수 있습니다.

`version` 메서드는 모든 컴파일 결과 파일 뒤에 고유 해시를 추가하여 손쉬운 캐시 무효화(cache busting)가 가능합니다:

    mix.js('resources/js/app.js', 'public/js')
        .version();

버전 관리된 파일은 정확한 파일명을 알 수 없으므로, [뷰](/docs/{{version}}/views)에서 Laravel의 전역 `mix` 함수를 사용해 적절한 파일명을 자동으로 참조하세요:

    <script src="{{ mix('/js/app.js') }}"></script>

개발 환경에서는 보통 버전 관리가 필요 없으므로, `npm run prod` 실행 시에만 버전 작업을 수행하도록 할 수 있습니다:

    mix.js('resources/js/app.js', 'public/js');

    if (mix.inProduction()) {
        mix.version();
    }

<a name="custom-mix-base-urls"></a>
#### 커스텀 Mix Base URL

만약 Mix로 컴파일된 에셋을 애플리케이션과 다른 CDN에 배포한다면, `mix` 함수가 생성하는 기본 URL을 수정해야 할 수 있습니다. 이때는 애플리케이션의 `config/app.php` 설정 파일에 `mix_url` 옵션을 추가하세요:

    'mix_url' => env('MIX_ASSET_URL', null)

Mix URL을 설정하면, `mix` 함수가 자산 URL을 생성할 때 미리 지정된 URL을 접두사로 사용합니다:

```bash
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
## Browsersync 자동 리로드

[BrowserSync](https://browsersync.io/)를 이용하면 파일 변경 시 자동으로 브라우저에 변경사항을 주입하거나, 페이지를 새로고침하지 않고도 반영할 수 있습니다. `mix.browserSync()` 메서드 호출로 이 기능을 활성화할 수 있습니다:

```js
mix.browserSync('laravel.test');
```

[BrowserSync 옵션](https://browsersync.io/docs/options)은 JavaScript 객체를 `browserSync` 메서드에 전달하여 지정할 수 있습니다:

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

이제 `npm run watch` 명령으로 webpack 개발 서버를 시작하세요. 스크립트나 PHP 파일을 수정하면, 브라우저가 즉시 페이지를 새로고침해 변경사항을 반영합니다.

<a name="environment-variables"></a>
## 환경 변수

`.env` 파일에 `MIX_`로 시작하는 환경 변수를 정의하면, 이를 `webpack.mix.js` 스크립트에서 그대로 사용할 수 있습니다:

    MIX_SENTRY_DSN_PUBLIC=http://example.com

변수를 `.env`에 정의한 후, `process.env` 객체로 접근할 수 있습니다. 단, 태스크 실행 중 변수 값이 변경되면 재시작이 필요합니다:

    process.env.MIX_SENTRY_DSN_PUBLIC

<a name="notifications"></a>
## 알림

가능한 환경에서는, Mix가 컴파일링 시 OS 알림을 자동 표시하여 성공 또는 실패 여부를 즉시 확인할 수 있게 해줍니다. 하지만 서버에서 Mix를 트리거하는 등 알림을 끄고 싶은 경우, `disableNotifications` 메서드로 알림을 비활성화할 수 있습니다:

    mix.disableNotifications();