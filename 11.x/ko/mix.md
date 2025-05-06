# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자 제프리 웨이(Jeffrey Way)가 개발한 패키지로, 여러 일반적인 CSS 및 JavaScript 전처리기를 사용하여 Laravel 애플리케이션의 [webpack](https://webpack.js.org) 빌드 단계를 정의할 수 있는 유연한 API를 제공합니다.

즉, Mix를 사용하면 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 압축하는 작업이 매우 간단해집니다. 간결한 메서드 체이닝을 통해 자산 파이프라인을 효율적으로 정의할 수 있습니다. 예를 들면 다음과 같습니다:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

만약 webpack과 자산 컴파일을 처음 시작하면서 혼란스럽거나 부담을 느꼈다면, Laravel Mix가 큰 도움이 될 것입니다. 그러나 애플리케이션을 개발할 때 반드시 Mix를 사용할 필요는 없으며, 원하는 자산 파이프라인 도구를 자유롭게 사용할 수 있고, 아예 사용하지 않아도 됩니다.

> [!NOTE]  
> Laravel의 신규 설치에서는 Laravel Mix 대신 Vite가 기본으로 사용됩니다. Mix 관련 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트를 참고하세요. Vite로 전환하고 싶으실 경우에는 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하십시오.