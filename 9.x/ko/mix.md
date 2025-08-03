# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com) 창시자 Jeffrey Way가 개발한 패키지로, [webpack](https://webpack.js.org) 빌드 단계를 정의하기 위한 유려한 API를 제공합니다. 이를 통해 Laravel 애플리케이션에서 여러 일반적인 CSS 및 JavaScript 전처리기를 손쉽게 사용할 수 있습니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 축소(minify)하는 작업을 매우 간편하게 만들어 줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 자연스럽게 정의할 수 있습니다. 예를 들면 다음과 같습니다.

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

webpack과 자산 컴파일을 처음 시작할 때 혼란스럽고 막막했던 경험이 있다면, Laravel Mix가 매우 유용하게 느껴질 것입니다. 다만, 애플리케이션 개발 시 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 다른 자산 파이프라인 도구를 자유롭게 사용할 수 있고, 전혀 사용하지 않아도 됩니다.

> [!NOTE]
> 새로운 Laravel 설치에서는 Laravel Mix 대신 Vite가 기본으로 사용됩니다. Mix에 관한 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트에서 확인하세요. Vite로 전환하고자 한다면 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.