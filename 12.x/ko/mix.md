# 라라벨 믹스 (Laravel Mix)

- [소개](#introduction)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 라라벨 믹스는 더 이상 적극적으로 유지 관리되지 않는 레거시 패키지입니다. 현대적인 대안으로 [Vite](/docs/12.x/vite)를 사용할 수 있습니다.

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)의 창립자인 Jeffrey Way가 개발한 패키지로, 라라벨 애플리케이션에서 자주 사용하는 CSS 및 JavaScript 전처리기를 활용하여 [webpack](https://webpack.js.org) 빌드 과정을 손쉽게 정의할 수 있는 유연한 API를 제공합니다.

즉, Mix를 사용하면 애플리케이션의 CSS와 JavaScript 파일을 쉽고 빠르게 컴파일하고, 용량을 줄일 수 있습니다. 간단한 메서드 체인 방식으로 자산(asset) 파이프라인을 직관적으로 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

만약 webpack과 자산 빌드 작업을 처음 접하면서 어려움이나 혼란을 느낀 적이 있다면, 라라벨 믹스가 많은 도움이 될 것입니다. 하지만, 애플리케이션 개발 시 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 다른 자산 빌드 도구를 자유롭게 선택해 사용하거나, 아예 사용하지 않아도 무방합니다.

> [!NOTE]
> Vite는 새로운 라라벨 프로젝트에서 라라벨 믹스를 대체하여 기본 도구로 채택되었습니다. Mix 관련 공식 문서는 [라라벨 믹스 공식 사이트](https://laravel-mix.com/)에서 확인할 수 있습니다. Mix에서 Vite로 전환하고 싶다면, [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.
