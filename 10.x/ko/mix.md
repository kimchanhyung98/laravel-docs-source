# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 제작자 Jeffrey Way가 개발한 패키지로, 여러 가지 일반적인 CSS 및 JavaScript 전처리기를 사용하여 Laravel 애플리케이션의 [webpack](https://webpack.js.org) 빌드 단계를 정의할 수 있는 유연한 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 최소화하는 작업을 매우 간단하게 만들어줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 쉽게 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

webpack과 자산 컴파일을 어떻게 시작해야 할지 혼란스러웠거나 부담을 느낀 적이 있다면, Laravel Mix를 매우 좋아하게 될 것입니다. 그러나 애플리케이션을 개발할 때 반드시 Mix를 사용할 필요는 없습니다. 원한다면 어떤 자산 파이프라인 도구도 자유롭게 사용할 수 있으며, 아예 사용하지 않아도 무방합니다.

> [!NOTE]  
> Vite가 새로운 Laravel 설치에서는 Laravel Mix를 대체했습니다. Mix에 대한 공식 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하실 수 있습니다. Vite로 전환하고 싶으시다면 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.