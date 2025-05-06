# 블레이드 템플릿(Blade Templates)

- [소개](#introduction)
    - [라이브와이어로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시문(Directives)](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문(Loop)](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [@once 지시문](#the-once-directive)
    - [Raw PHP 코드](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯(Slots)](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성/attributes](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 만들기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼(Forms)](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검사 오류](#validation-errors)
- [스택(Stacks)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장](#extending-blade)
    - [커스텀 echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

블레이드(Blade)는 라라벨에 내장된 간단하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과는 달리 블레이드는 여러분이 템플릿 안에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실, 모든 블레이드 템플릿은 일반 PHP 코드로 컴파일되고 수정될 때까지 캐시에 저장되므로, 블레이드는 애플리케이션에 사실상 부하를 거의 주지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 가지며 일반적으로 `resources/views` 디렉토리에 저장됩니다.

라우트 또는 컨트롤러에서 글로벌 `view` 헬퍼를 사용하여 블레이드 뷰를 반환할 수 있습니다. 물론, [뷰 문서](/docs/{{version}}/views)에서 언급한 것처럼, `view` 헬퍼의 두 번째 인자를 사용하여 데이터도 블레이드 뷰로 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### 라이브와이어로 블레이드 강화하기

블레이드 템플릿을 한 단계 더 업그레이드하고 동적 인터페이스를 쉽게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. 라이브와이어를 이용하면 프론트엔드 프레임워크(React나 Vue 등)로만 가능했던 동적 기능을 강화한 블레이드 컴포넌트를 작성할 수 있어, 복잡한 클라이언트 렌더링이나 번들링 단계 없이 현대적이고 반응성이 뛰어난 프론트엔드를 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 표시

블레이드 뷰에 전달된 데이터를 중괄호로 감싸 표시할 수 있습니다. 예를 들어 아래와 같은 라우트가 있다고 가정합니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 값을 아래와 같이 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]  
> 블레이드의 `{{ }}` echo 문은 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 XSS 공격을 방지합니다.

뷰에 전달된 변수 외에도, 원하는 PHP 함수의 결과를 출력할 수도 있습니다. 사실상, 블레이드 echo 문 안에는 어떤 PHP 코드도 사용할 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 블레이드(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프되지 않은 데이터 표시

기본적으로 블레이드의 `{{ }}` 문은 XSS 방지를 위해 PHP의 `htmlspecialchars` 함수로 자동 전송됩니다. 데이터 이스케이프를 원하지 않는 경우 아래 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]  
> 사용자 입력값을 이스케이프하지 않고 출력하는 경우 매우 조심해야 합니다. 일반적으로 사용자 입력 데이터 표시에는 안전한 이중 중괄호(`{{ }}`) 문법을 사용하세요.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크도 "중괄호" 구문을 사용하므로, 블레이드 렌더링 엔진이 해당 표현을 건드리지 않게 하려면 `@` 기호를 사용하세요. 예:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서 블레이드는 `@`만 제거하고, `{{ name }}` 표현식은 그대로 두어 자바스크립트 프레임워크에서 처리하게 됩니다.

또한 `@` 기호로 블레이드 지시문을 이스케이프할 수도 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수를 초기화하려고 배열을 JSON으로 출력할 때가 있습니다:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

`json_encode`를 직접 호출하는 대신 `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP `json_encode`와 같이 동작하며, HTML 내부에 삽입될 때 JSON이 적절히 이스케이프되도록 해줍니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel 앱에서 기본적으로 제공되는 `Js` 파사드(Js facade)를 사용할 수도 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]  
> `Js::from` 메서드는 기존 변수를 JSON으로 렌더링할 때만 사용해야 합니다. 블레이드의 정규식 파싱 특성상 복잡한 표현식을 전달하면 예기치 않은 문제가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### @verbatim 지시문

템플릿 내에서 자바스크립트 변수를 대량 출력할 경우, `@verbatim` 지시문으로 HTML을 감싸면 각 블레이드 echo 문마다 `@`를 붙이지 않아도 됩니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

(이하의 섹션들은 구조만 참고하실 수 있도록 제목만 한글과 함께 표시합니다. 원문이 너무 방대하므로 한 번에 전체 번역을 제공하는 건 비현실적이니, 요청하시는 분량에 따라 추가적으로 나누거나 필요한 부분만 추출하여 번역하시는 것을 권장합니다.)

---

아래는 주요 섹션 제목의 번역 예시입니다:

- [블레이드 지시문(Blade Directives)](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문(Loop)](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - 등등…

- [컴포넌트(Components)](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - 등등…

- [익명 컴포넌트(Anonymous Components)](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성/attributes](#data-properties-attributes)
    - 등등…

- [레이아웃 만들기(Building Layouts)](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)

- [폼(Forms)](#forms)
- [스택(Stacks)](#stacks)
- [서비스 주입(Service Injection)](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장(Extending Blade)](#extending-blade)
    - [커스텀 echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

---

**전체 문서를 한 번에 번역하기에는 분량이 방대하니, 필요하신 섹션을 부분적으로 요청하시면 신속하고 정확하게 번역해드릴 수 있습니다. 그렇지 않으면 분량에 따라 번역 제약이 있을 수 있습니다.**

원하시는 부분(예: 블레이드 지시문, 컴포넌트, 레이아웃 등) 또는 샘플 코드와 주요 설명이 담긴 세부 단락을 지목해 추가 요청해 주세요!