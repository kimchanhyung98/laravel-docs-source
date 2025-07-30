# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com) 창립자인 Jeffrey Way가 개발한 패키지로, Laravel 애플리케이션에서 여러 일반적인 CSS 및 JavaScript 전처리기를 사용하여 [webpack](https://webpack.js.org) 빌드 단계를 선언적으로 정의할 수 있는 직관적인 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 최소화하는 과정을 매우 쉽게 만들어줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 자연스럽게 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

webpack과 자산 컴파일을 처음 시작할 때 혼란스럽고 어렵게 느껴졌다면 Laravel Mix를 매우 좋아할 것입니다. 하지만 애플리케이션 개발 시에 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 어떤 자산 파이프라인 도구를 사용해도 되고 아예 사용하지 않아도 됩니다.

> [!NOTE]  
> Vite가 새 Laravel 설치 환경에서 Laravel Mix를 대체했습니다. Mix 관련 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인할 수 있습니다. Vite로 전환하고 싶다면 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.