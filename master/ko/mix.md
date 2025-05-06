# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자인 Jeffrey Way가 개발한 패키지로, 여러 일반적인 CSS 및 JavaScript 전처리기를 활용하여 Laravel 애플리케이션의 [webpack](https://webpack.js.org) 빌드 단계를 정의할 수 있는 유연한 API를 제공합니다.

다시 말해, Mix를 사용하면 애플리케이션의 CSS 및 JavaScript 파일을 손쉽게 컴파일하고 최소화할 수 있습니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 유연하게 정의할 수 있습니다. 예를 들면 다음과 같습니다:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

만약 webpack과 자산 컴파일 작업을 어떻게 시작해야 할지 혼란스럽고 막막했던 경험이 있다면, Laravel Mix가 큰 도움이 될 것입니다. 물론, 애플리케이션 개발 시 Mix를 꼭 사용할 필요는 없습니다. 원하는 어떤 자산 파이프라인 툴을 사용해도 되고, 아예 사용하지 않아도 무방합니다.

> [!NOTE]
> 최신 Laravel 설치에서는 Vite가 Laravel Mix를 대체했습니다. Mix 관련 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하실 수 있습니다. Vite로 전환하고 싶으시다면, [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고해 주세요.