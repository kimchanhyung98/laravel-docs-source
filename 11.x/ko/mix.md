# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com) 창립자 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션에 대해 여러 일반적인 CSS 및 JavaScript 전처리기를 사용하여 [webpack](https://webpack.js.org) 빌드 단계를 정의하는 유창한 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 압축하는 작업을 매우 쉽게 만들어 줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 유연하게 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

만약 webpack이나 자산 컴파일을 시작하는 데 혼란스럽고 부담스러웠다면, Laravel Mix가 매우 유용할 것입니다. 하지만 애플리케이션 개발 시 반드시 사용해야 하는 것은 아니며, 원하는 다른 자산 파이프라인 도구를 사용하거나 전혀 사용하지 않아도 됩니다.

> [!NOTE]  
> 새로운 Laravel 설치에서는 Laravel Mix 대신 Vite가 기본 도구로 사용됩니다. Mix 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인할 수 있습니다. Vite로 전환을 원하신다면 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.