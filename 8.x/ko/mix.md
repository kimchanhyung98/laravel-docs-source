# 자산 컴파일 (Mix) (Compiling Assets (Mix))

- [소개](#introduction)
- [설치 및 설정](#installation)
- [Mix 실행하기](#running-mix)
- [스타일시트 작업하기](#working-with-stylesheets)
    - [Tailwind CSS](#tailwindcss)
    - [PostCSS](#postcss)
    - [Sass](#sass)
    - [URL 처리](#url-processing)
    - [소스 맵](#css-source-maps)
- [자바스크립트 작업하기](#working-with-scripts)
    - [Vue](#vue)
    - [React](#react)
    - [벤더 추출](#vendor-extraction)
    - [커스텀 웹팩 설정](#custom-webpack-configuration)
- [버전 관리 / 캐시 무효화](#versioning-and-cache-busting)
- [Browsersync 리로딩](#browsersync-reloading)
- [환경 변수](#environment-variables)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Mix](https://github.com/JeffreyWay/laravel-mix)는 [Laracasts](https://laracasts.com)의 창시자 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션에서 일반적으로 사용하는 CSS 및 JavaScript 전처리기를 이용해 [webpack](https://webpack.js.org) 빌드 과정을 직관적으로 정의할 수 있는 유려한 API를 제공합니다.

즉, Mix를 사용하면 애플리케이션의 CSS와 JavaScript 파일을 쉽게 컴파일하고 압축할 수 있습니다. 간단한 메서드 체이닝만으로 자산 파이프라인을 선언적으로 구성할 수 있죠. 예를 들어:

```
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

Webpack과 자산 컴파일을 어떻게 시작해야 할지 어려움을 느꼈다면 Laravel Mix가 큰 도움이 될 것입니다. 물론 애플리케이션 개발 시 반드시 사용할 필요는 없으며, 자신이 원하는 자산 파이프라인 도구를 사용하거나 아예 사용하지 않아도 됩니다.

> [!TIP]
> Laravel과 [Tailwind CSS](https://tailwindcss.com)를 함께 사용하는 시작점을 원한다면, [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 참고하세요.

<a name="installation"></a>
## 설치 및 설정 (Installation & Setup)

<a name="installing-node"></a>
#### Node 설치하기

Mix를 실행하기 전에, Node.js와 NPM이 시스템에 설치되어 있는지 확인해야 합니다:

```
node -v
npm -v
```

공식 Node 웹사이트([링크](https://nodejs.org/en/download/))에서 그래픽 설치 프로그램을 통해 최신 버전을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](/docs/{{version}}/sail)을 사용한다면, Sail 명령어로 Node와 NPM을 호출할 수도 있습니다:

```
./sail node -v
./sail npm -v
```

<a name="installing-laravel-mix"></a>
#### Laravel Mix 설치하기

남은 단계는 Laravel Mix를 설치하는 것입니다. 새로운 Laravel 설치 프로젝트의 루트 디렉터리에 `package.json` 파일이 존재하며, 이 기본 파일에는 Laravel Mix 시작에 필요한 모든 패키지들이 포함되어 있습니다. PHP 의존성이 아닌 Node 의존성을 정의하는 `composer.json`과 같은 역할을 한다고 생각하면 됩니다. 다음 명령어로 의존성을 설치하세요:

```
npm install
```

<a name="running-mix"></a>
## Mix 실행하기 (Running Mix)

Mix는 [webpack](https://webpack.js.org) 위에 설정 레이어 역할을 하므로, Larvel의 기본 `package.json` 파일에 정의된 NPM 스크립트 중 하나만 실행하면 Mix 작업을 수행할 수 있습니다. `dev` 또는 `production` 스크립트를 실행하면 애플리케이션의 모든 CSS와 자바스크립트 자산이 컴파일되어 `public` 디렉터리에 배치됩니다:

```
// 모든 Mix 작업 실행...
npm run dev

// 출력물 압축(축소)까지 실행...
npm run prod
```

<a name="watching-assets-for-changes"></a>
#### 자산 변경 감시

`npm run watch` 커맨드는 터미널에서 계속 실행되며 관련 CSS 및 자바스크립트 파일을 감시합니다. 해당 파일들에서 변경이 감지되면 webpack이 자동으로 자산을 다시 컴파일합니다:

```
npm run watch
```

일부 로컬 개발 환경에서는 webpack이 파일 변화를 제대로 감지하지 못할 수 있습니다. 이 경우, `watch-poll` 명령을 고려하세요:

```
npm run watch-poll
```

<a name="working-with-stylesheets"></a>
## 스타일시트 작업하기 (Working With Stylesheets)

`webpack.mix.js` 파일은 자산 컴파일의 진입점입니다. 이는 webpack을 감싸는 가벼운 설정 래퍼라고 볼 수 있습니다. Mix 작업은 체이닝 방식으로 연결해 자산 컴파일 방식을 세밀하게 정의할 수 있습니다.

<a name="tailwindcss"></a>
### Tailwind CSS

[Tailwind CSS](https://tailwindcss.com)는 HTML 코드를 떠나지 않고 멋진 웹사이트를 만들 수 있는 모던한 유틸리티 우선 프레임워크입니다. Laravel 프로젝트에서 Laravel Mix와 함께 사용하려면 다음 단계로 시작하세요. 먼저 NPM으로 Tailwind를 설치하고 설정 파일을 생성합니다:

```
npm install

npm install -D tailwindcss

npx tailwindcss init
```

`init` 명령은 `tailwind.config.js` 파일을 생성하며, 이 파일의 `content` 섹션에서 Tailwind 클래스가 포함된 HTML 템플릿, 자바스크립트 컴포넌트, 기타 파일 경로를 지정할 수 있습니다. 이렇게 하면 사용하지 않는 CSS 클래스는 프로덕션 CSS에서 제거됩니다:

```js
content: [
    './storage/framework/views/*.php',
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
],
```

이후 `resources/css/app.css` 파일에 Tailwind의 각 레이어를 추가하세요:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Tailwind 레이어 설정이 끝나면 `webpack.mix.js` 파일을 업데이트해 Tailwind 기반 CSS를 컴파일할 준비를 합니다:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css', [
        require('tailwindcss'),
    ]);
```

마지막으로, 애플리케이션의 주 레이아웃 템플릿(일반적으로 `resources/views/layouts/app.blade.php`)에 스타일시트를 참조하세요. 만약 없다면, 반응형 뷰포트(meta viewport) 태그도 꼭 추가하세요:

```html
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="/css/app.css" rel="stylesheet">
</head>
```

<a name="postcss"></a>
### PostCSS

[PostCSS](https://postcss.org/)는 CSS를 변환하는 강력한 도구로, Laravel Mix에 기본 포함되어 있습니다. 기본적으로 Mix는 인기 있는 [Autoprefixer](https://github.com/postcss/autoprefixer) 플러그인을 사용해 필요한 모든 CSS3 벤더 접두사를 자동으로 추가합니다. 하지만 필요한 경우 다른 플러그인도 쉽게 추가할 수 있습니다.

원하는 플러그인을 NPM으로 설치한 다음, Mix의 `postCss` 메서드 호출에서 플러그인 배열에 넣으면 됩니다. `postCss`는 첫 번째 인자로 CSS 파일 경로를, 두 번째 인자로 출력 디렉터리를 받습니다:

```
mix.postCss('resources/css/app.css', 'public/css', [
    require('postcss-custom-properties')
]);
```

플러그인 없이 단순히 CSS 컴파일과 압축만 하려면 다음처럼 호출해도 됩니다:

```
mix.postCss('resources/css/app.css', 'public/css');
```

<a name="sass"></a>
### Sass

`sass` 메서드는 [Sass](https://sass-lang.com/)를 웹 브라우저가 인식할 수 있는 CSS로 컴파일합니다. 첫 번째 인자로 Sass 파일 경로를, 두 번째 인자로 결과 CSS 출력 디렉터리를 지정합니다:

```
mix.sass('resources/sass/app.scss', 'public/css');
```

`mix.sass`를 여러 번 호출하면 여러 Sass 파일을 각각 컴파일하고 원하는 출력 디렉터리로 저장할 수 있습니다:

```
mix.sass('resources/sass/app.sass', 'public/css')
    .sass('resources/sass/admin.sass', 'public/css/admin');
```

<a name="url-processing"></a>
### URL 처리

Laravel Mix가 webpack 위에서 작동하므로, 몇 가지 webpack 개념을 이해하는 것이 중요합니다. CSS 컴파일 과정에서 webpack은 스타일시트 내 모든 `url()` 호출을 다시 작성하고 최적화합니다. 처음에는 생소할 수 있으나 매우 강력한 기능입니다. 예를 들어, 이미지에 상대 경로가 포함된 Sass를 컴파일한다고 생각해 보세요:

```
.example {
    background: url('../images/example.png');
}
```

> [!NOTE]
> `url()` 안에 절대 경로가 들어간 경우 URL 재작성 대상에서 제외됩니다. 예를 들어, `url('/images/thing.png')`나 `url('http://example.com/images/thing.png')`는 수정하지 않습니다.

기본적으로 Laravel Mix와 webpack은 `example.png` 파일을 찾아 `public/images` 폴더에 복사하고, 생성된 CSS 내의 `url()` 경로를 재작성합니다. 그래서 컴파일된 CSS는 다음과 같이 됩니다:

```
.example {
    background: url(/images/example.png?d41d8cd98f00b204e9800998ecf8427e);
}
```

이 기능이 유용하지만, 기존 폴더 구조를 이미 선호하는 방식으로 유지하고 싶다면 `url()` 재작성 기능을 비활성화할 수 있습니다:

```
mix.sass('resources/sass/app.scss', 'public/css').options({
    processCssUrls: false
});
```

이렇게 하면 Mix가 `url()`을 처리하거나 자산을 복사하지 않으며, 결과 CSS는 입력한 그대로 유지됩니다:

```
.example {
    background: url("../images/thing.png");
}
```

<a name="css-source-maps"></a>
### 소스 맵 (Source Maps)

기본적으로 비활성화되어 있으나, 소스 맵은 `webpack.mix.js` 파일에서 `mix.sourceMaps()` 메서드를 호출해 활성화할 수 있습니다. 컴파일 성능 향상에는 영향이 있지만, 컴파일된 자산을 사용할 때 브라우저 개발자 도구에 더 자세한 디버깅 정보를 제공합니다:

```
mix.js('resources/js/app.js', 'public/js')
    .sourceMaps();
```

<a name="style-of-source-mapping"></a>
#### 소스 맵 스타일

webpack은 다양한 [소스 맵 스타일](https://webpack.js.org/configuration/devtool/#devtool)을 제공합니다. 기본값은 빠른 재빌드를 지원하는 `eval-source-map`입니다. 필요에 따라 `sourceMaps` 메서드에 매개변수를 전달해 변경할 수 있습니다:

```
let productionSourceMaps = false;

mix.js('resources/js/app.js', 'public/js')
    .sourceMaps(productionSourceMaps, 'source-map');
```

<a name="working-with-scripts"></a>
## 자바스크립트 작업하기 (Working With JavaScript)

Mix는 최신 ECMAScript 컴파일, 모듈 번들링, 축소, 단순 스크립트 연결 등 자바스크립트 작업에 필요한 여러 기능을 제공합니다. 더 좋은 점은 별도의 복잡한 설정 없이 바로 사용할 수 있다는 점입니다:

```
mix.js('resources/js/app.js', 'public/js');
```

위 한 줄만으로 다음 기능을 활용할 수 있습니다:

- 최신 ECMAScript 문법 지원
- 모듈 단위로 기능 분리
- 프로덕션 환경 코드 축소

<a name="vue"></a>
### Vue

`vue` 메서드를 사용하면 Vue 단일 파일 컴포넌트 컴파일에 필요한 Babel 플러그인이 자동으로 설치됩니다. 별도 설정은 필요 없습니다:

```
mix.js('resources/js/app.js', 'public/js')
   .vue();
```

컴파일이 완료되면, 애플리케이션에서 해당 파일을 참조하세요:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="react"></a>
### React

Mix는 React 지원에 필요한 Babel 플러그인도 자동으로 설치합니다. `react` 메서드를 호출해 시작하세요:

```
mix.js('resources/js/app.jsx', 'public/js')
   .react();
```

내부적으로는 적당한 `babel-preset-react` 플러그인을 설치하고 포함합니다. 컴파일 후 애플리케이션에서 다음과 같이 참조하세요:

```html
<head>
    <!-- ... -->

    <script src="/js/app.js"></script>
</head>
```

<a name="vendor-extraction"></a>
### 벤더 추출

애플리케이션 코드를 벤더 라이브러리(예: React, Vue)와 한 파일에 번들링하면, 조금이라도 애플리케이션 코드가 변경됐을 때 벤더 라이브러리까지 모두 다시 다운로드하게 되어 장기 캐싱에 불리합니다.

자주 코드 수정을 한다면, 벤더 라이브러리를 별도 파일로 추출하는 방식을 고려하세요. 이를 통해 애플리케이션 코드가 바뀌어도 벤더.js 캐시는 영향을 받지 않습니다. Mix의 `extract` 메서드가 이를 쉽게 만들어 줍니다:

```
mix.js('resources/js/app.js', 'public/js')
    .extract(['vue'])
```

`extract`는 배열로 벤더 라이브러리를 받아 `vendor.js` 파일로 만듭니다. 예시에서 Mix는 다음 파일들을 생성합니다:

- `public/js/manifest.js`: *Webpack 매니페스트 런타임*
- `public/js/vendor.js`: *벤더 라이브러리*
- `public/js/app.js`: *애플리케이션 코드*

자바스크립트 오류를 피하기 위해 반드시 아래 순서대로 스크립트를 로드하세요:

```
<script src="/js/manifest.js"></script>
<script src="/js/vendor.js"></script>
<script src="/js/app.js"></script>
```

<a name="custom-webpack-configuration"></a>
### 커스텀 웹팩 설정

간혹 직접 Webpack 설정을 수정해야 할 때가 있습니다. 예를 들어 특정 로더나 플러그인을 참조할 필요가 있을 때가 그렇습니다.

Mix는 `webpackConfig` 메서드를 제공해, 짧은 Webpack 설정 덮어쓰기를 병합할 수 있습니다. 이 방법은 별도로 `webpack.config.js`를 복사하고 유지할 필요가 없어 매우 유용합니다. 인자로 전달하는 객체에 [Webpack 설정](https://webpack.js.org/configuration/)을 담으면 됩니다:

```
mix.webpackConfig({
    resolve: {
        modules: [
            path.resolve(__dirname, 'vendor/laravel/spark/resources/assets/js')
        ]
    }
});
```

<a name="versioning-and-cache-busting"></a>
## 버전 관리 / 캐시 무효화 (Versioning / Cache Busting)

개발자들은 보통 컴파일된 자산 파일명에 타임스탬프나 고유 토큰을 붙여, 브라우저가 오래된 캐시가 아닌 최신 파일을 불러오도록 만듭니다. Mix는 `version` 메서드로 이를 자동 처리합니다.

`version`을 호출하면 컴파일된 모든 파일명 뒤에 고유 해시가 붙어 캐시 무효화가 쉬워집니다:

```
mix.js('resources/js/app.js', 'public/js')
    .version();
```

버전이 붙은 파일명이 어떻게 될지 모르므로, [뷰](/docs/{{version}}/views)에서 Laravel 글로벌 `mix` 함수를 사용해 적절한 경로로 불러야 합니다. `mix` 함수가 현재 해시가 붙은 파일명을 자동으로 찾습니다:

```
<script src="{{ mix('/js/app.js') }}"></script>
```

버전 관리된 파일은 보통 개발 중엔 필요 없으므로, `npm run prod`에서만 활성화하는 것도 좋습니다:

```
mix.js('resources/js/app.js', 'public/js');

if (mix.inProduction()) {
    mix.version();
}
```

<a name="custom-mix-base-urls"></a>
#### Mix 기본 URL 사용자 정의

Mix 자산이 애플리케이션과 다른 CDN에 배포된다면, `mix` 함수로 생성되는 기본 URL을 변경해야 합니다. 애플리케이션 `config/app.php` 설정 파일에 `mix_url` 옵션을 추가하세요:

```
'mix_url' => env('MIX_ASSET_URL', null)
```

설정 후 `mix` 함수는 자산 URL에 지정한 기본 URL을 자동으로 접두어로 붙입니다:

```bash
https://cdn.example.com/js/app.js?id=1964becbdd96414518cd
```

<a name="browsersync-reloading"></a>
## Browsersync 리로딩 (Browsersync Reloading)

[BrowserSync](https://browsersync.io/)는 파일 변경을 감지해 브라우저에 자동으로 변경 사항을 주입하며, 수동 새로 고침 없이도 변경을 반영합니다. `mix.browserSync()` 메서드로 지원을 활성화할 수 있습니다:

```js
mix.browserSync('laravel.test');
```

추가 설정은 객체 형태로 전달할 수 있습니다. 예를 들어, 프록시 옵션 사용:

```js
mix.browserSync({
    proxy: 'laravel.test'
});
```

그 다음 `npm run watch` 명령으로 webpack 개발 서버를 시작하세요. PHP나 자바스크립트 파일을 수정하면 페이지가 자동으로 새로고침되어 즉시 변경사항을 확인할 수 있습니다.

<a name="environment-variables"></a>
## 환경 변수 (Environment Variables)

`.env` 파일 내 환경 변수 중 이름이 `MIX_`로 시작하는 변수는 `webpack.mix.js` 스크립트에서 주입할 수 있습니다:

```
MIX_SENTRY_DSN_PUBLIC=http://example.com
```

정의 후, `process.env` 객체를 통해 접근할 수 있지만, 환경 변수 값이 작업 중 변경되면 작업을 재시작해야 합니다:

```
process.env.MIX_SENTRY_DSN_PUBLIC
```

<a name="notifications"></a>
## 알림 (Notifications)

사용 가능한 경우, Mix는 컴파일 과정에서 OS 알림을 자동으로 표시해 컴파일 성공 여부를 즉시 알려줍니다. 다만, 때로는 이를 비활성화하는 것이 필요할 수 있습니다. 예를 들면, 프로덕션 서버에서 컴파일을 트리거할 때 등이 그렇습니다. `disableNotifications` 메서드로 알림을 끌 수 있습니다:

```
mix.disableNotifications();
```