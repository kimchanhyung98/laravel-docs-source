# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [라이브와이어로 블레이드 확장하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시문](#blade-directives)
    - [If문](#if-statements)
    - [Switch문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [하위 뷰 포함하기](#including-subviews)
    - [`@once` 지시문](#the-once-directive)
    - [Raw PHP 사용하기](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [수동 컴포넌트 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성/속성(attribute)](#data-properties-attributes)
    - [부모 데이터에 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [Method 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If문](#custom-if-statements)

<a name="introduction"></a>
## 소개

블레이드는 라라벨에 내장된 간결하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿 내에서 일반 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로 모든 블레이드 템플릿은 평범한 PHP 코드로 컴파일되어, 변경될 때까지 캐시됩니다. 즉, 블레이드는 애플리케이션에 실질적으로 부하를 거의 주지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 사용하며, 보통 `resources/views` 디렉토리에 저장됩니다.

블레이드 뷰는 전역 `view` 헬퍼를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론 [뷰](/docs/12.x/views) 문서에서 언급했듯이, `view` 헬퍼의 두 번째 인수를 활용해 데이터를 블레이드 뷰에 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### 라이브와이어로 블레이드 확장하기

블레이드 템플릿을 한 단계 더 발전시키고 싶으신가요? 동적인 UI도 쉽게 구현하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보시기 바랍니다. Livewire를 이용하면, 원래 React나 Vue 같은 프론트엔드 프레임워크에서만 가능했던 동적 기능을 블레이드 컴포넌트에 손쉽게 추가할 수 있습니다. 즉, 복잡한 클라이언트 렌더링이나 빌드 과정 없이, 현대적인 리액티브 프론트엔드도 쉽게 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 표시하기

블레이드 뷰에 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해 보겠습니다.

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

이때, `name` 변수의 값을 아래와 같이 표시할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> 블레이드의 `{{ }}` 출력 구문은 PHP의 `htmlspecialchars` 함수로 자동 처리되어 XSS 공격을 예방합니다.

뷰에 전달된 변수만 표시하는 것이 아니라, PHP 함수의 결과도 얼마든지 출력할 수 있습니다. 실제로, 블레이드 이코(echo) 구문 안에 원하는 어떤 PHP 코드라도 작성할 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로, 블레이드(그리고 라라벨의 `e` 함수)는 HTML 엔티티를 한 번 더(이중으로) 인코딩합니다. 만약 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프되지 않은 데이터 표시하기

기본적으로, 블레이드의 `{{ }}` 구문은 PHP의 `htmlspecialchars`를 통해 XSS 공격을 예방합니다. 만약 데이터를 이스케이프하지 않고, 있는 그대로 출력하려면 다음과 같은 문법을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 이처럼 무가공으로 출력할 때는 반드시 주의해야 합니다. 일반적으로는 `{{ }}`와 같은 이스케이프된, 중괄호 두 개 구문을 사용해서 XSS 공격을 방지하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크에서도 "중괄호"를 사용해 화면에 표현될 값을 작성하는 경우가 흔합니다. 이럴 때는 `@` 기호를 사용해, 해당 표현식을 블레이드가 해석하지 않고 그대로 남겨두도록 할 수 있습니다. 예를 들면 아래와 같습니다.

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서 `@` 기호는 블레이드에 의해 제거되고, `{{ name }}` 표현식은 블레이드 엔진에 의해 처리되지 않은 채 남아, 자바스크립트 프레임워크(예: Vue)가 해석할 수 있게 됩니다.

또한, `@` 기호는 블레이드 지시문 자체를 이스케이프(그대로 출력)하는 데에도 사용됩니다.

```blade
{{-- 블레이드 템플릿 --}}
@@if()

<!-- HTML 출력 -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링하기

종종, 뷰에 배열을 전달하여 자바스크립트 변수 초기화에 사용할 JSON으로 렌더링하고 싶을 때가 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이렇게 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 지시문을 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인자를 받지만, HTML 따옴표 내부에 안전하게 포함될 수 있도록 JSON 데이터를 올바르게 이스케이프해 줍니다. 이 메서드는 `JSON.parse`가 적용된 문자열 형태를 반환하므로, 주어진 객체나 배열을 유효한 자바스크립트 오브젝트로 변환할 수 있습니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 라라벨 애플리케이션 스켈레톤에는 이 기능을 Blade 템플릿에서 더 편리하게 사용할 수 있도록 `Js` 파사드가 포함되어 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> 기존 변수를 JSON으로 렌더링할 때만 `Js::from` 메서드를 사용해야 합니다. 블레이드 템플릿 처리는 정규표현식 기반이기 때문에, 복잡한 표현식을 이 지시문에 바로 전달하면 예기치 않은 에러가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시문

템플릿의 넓은 영역에서 자바스크립트 변수를 표기하고자 할 때는, HTML을 `@verbatim` 지시문으로 감싸서 블레이드 이코(echo) 앞에 일일이 `@`를 붙이지 않아도 되게 할 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시문

템플릿 상속이나 데이터 출력 외에도, 블레이드는 조건문과 반복문 등 자주 사용되는 PHP 제어 구조에 대해 간결한 단축 지시문을 제공합니다. 이러한 지시문은 PHP 고유의 방식과도 매우 유사하므로, 익숙한 느낌을 유지하면서도 훨씬 깔끔하게 제어 로직을 작성할 수 있습니다.

<a name="if-statements"></a>
### If문

`@if`, `@elseif`, `@else`, `@endif` 지시문을 조합해 `if`문을 만들 수 있습니다. 이들 지시문은 PHP에서 사용하는 것과 똑같이 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

추가적으로, `@unless` 지시문도 제공되어 더욱 간결하게 작성할 수 있습니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

앞서 소개한 조건문 이외에도, `@isset`과 `@empty` 지시문을 각각 PHP의 해당 함수처럼 간편하게 활용할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 지시문

`@auth`와 `@guest` 지시문을 사용하면 현재 사용자가 [인증](/docs/12.x/authentication) 상태인지(로그인) 혹은 게스트인지(비로그인) 쉽게 판별할 수 있습니다.

```blade
@auth
    // 사용자가 인증되어 있습니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면, `@auth`와 `@guest` 지시문 사용 시 어떤 인증가드(guard)를 검사할지도 지정할 수 있습니다.

```blade
@auth('admin')
    // 사용자가 인증되어 있습니다...
@endauth

@guest('admin')
    // 사용자가 인증되지 않았습니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 지시문

`@production` 지시문을 이용해 애플리케이션이 프로덕션 환경에서 동작 중인지 체크할 수 있습니다.

```blade
@production
    // 프로덕션에만 표시할 내용...
@endproduction
```

또한, `@env` 지시문을 사용하면 애플리케이션이 특정 환경에서 실행 중인지도 판별할 수 있습니다.

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging" 또는 "production"에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### Section(섹션) 지시문

템플릿 상속의 특정 섹션에 데이터가 존재하는지 `@hasSection` 지시문을 통해 확인할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

반대로, 섹션에 데이터가 없는 경우를 판별하려면 `sectionMissing` 지시문을 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 지시문

`@session` 지시문을 사용하면 [세션](/docs/12.x/session) 값의 존재 여부를 간단하게 확인할 수 있습니다. 세션 값이 존재하면, `@session`과 `@endsession` 사이의 템플릿 내용이 평가됩니다. 그리고 그 안에서는 `$value` 변수를 바로 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 지시문

`@context` 지시문은 [컨텍스트](/docs/12.x/context) 값의 유무를 판별하는 데 사용할 수 있습니다. 컨텍스트 값이 있다면, `@context`과 `@endcontext` 사이 템플릿 내용이 렌더링되며, `$value` 변수를 활용해 해당 값을 출력할 수 있습니다.

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시문을 활용해 switch문을 구현할 수 있습니다.

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```

<a name="loops"></a>
### 반복문

조건문과 마찬가지로, 블레이드는 PHP 반복문에 활용할 수 있는 지시문도 제공합니다. 각각의 지시문은 PHP 본연의 기능과 똑같이 동작합니다.

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

> [!NOTE]
> `foreach` 반복문을 순회하는 도중, [loop 변수](#the-loop-variable)를 사용하면 현재 반복이 처음 또는 마지막인지 등 유용한 정보를 확인할 수 있습니다.

반복문 내에서 현재 반복을 건너뛰거나 반복을 종료하려면 각각 `@continue`, `@break` 지시문을 사용할 수 있습니다.

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

조건식을 지시문 선언부에 직접 포함시킬 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 안에서 `$loop` 변수가 자동으로 제공됩니다. 이 변수는 현재 반복 인덱스, 처음/마지막 반복 여부 등 반복문 관련 유용한 정보를 여러 가지로 제공합니다.

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

반복문이 중첩되어 있을 경우, `parent` 속성을 통해 상위 반복문의 `$loop` 변수에도 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 다음과 같이 다양한 유용한 속성이 내장되어 있습니다.

<div class="overflow-auto">

| 속성                  | 설명                                                          |
| --------------------- | ------------------------------------------------------------ |
| `$loop->index`        | 현재 반복문의 인덱스(0부터 시작).                             |
| `$loop->iteration`    | 현재 반복 회차(1부터 시작).                                   |
| `$loop->remaining`    | 반복문에서 아직 남은 반복 횟수.                              |
| `$loop->count`        | 반복 대상 배열의 전체 항목 수.                               |
| `$loop->first`        | 현재 반복이 첫 번째 반복인지 여부.                            |
| `$loop->last`         | 현재 반복이 마지막 반복인지 여부.                             |
| `$loop->even`         | 현재 반복이 짝수 번째인지 여부.                              |
| `$loop->odd`          | 현재 반복이 홀수 번째인지 여부.                              |
| `$loop->depth`        | 현재 반복의 중첩 단계(몇 번째 중첩 반복문인지).               |
| `$loop->parent`       | 중첩 반복문에서 부모 반복문의 loop 변수.                     |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일

`@class` 지시문을 사용하면, 조건에 따라 CSS 클래스 문자열을 동적으로 생성할 수 있습니다. 이 지시문에는 클래스 이름을 키로, 불리언 식을 값으로 하는 배열을 인수로 넣습니다. 배열 내 키가 숫자라면, 해당 클래스는 항상 렌더링 결과에 포함됩니다.

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```

마찬가지로, `@style` 지시문을 이용하면 조건부로 HTML 요소의 인라인 스타일을 추가할 수 있습니다.

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```

<a name="additional-attributes"></a>
### 추가 속성

HTML 체크박스 입력 필드가 "checked" 상태인지 쉽게 표시하려면 `@checked` 지시문을 사용할 수 있습니다. 이 지시문에서 제공하는 조건식이 `true`이면 `checked`가 자동으로 출력됩니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

비슷하게, 드롭다운 옵션이 "selected" 상태가 되어야 한다면 `@selected` 지시문을 활용하세요.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, `@disabled` 지시문으로 해당 요소가 "disabled" 상태인지도 쉽게 제어할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

게다가, `@readonly` 지시문을 쓰면 HTML 요소를 "readonly" 상태로도 만들 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

또한, `@required` 지시문을 사용해 입력 필드를 "required"로 표시할 수도 있습니다.

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### 하위 뷰 포함하기

> [!NOTE]
> `@include` 지시문 역시 자유롭게 쓸 수 있지만, 블레이드 [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 이점을 제공하므로 가능하면 컴포넌트 사용을 권장합니다.

블레이드의 `@include` 지시문을 사용하면 다른 블레이드 뷰를 손쉽게 포함할 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 하위 뷰에서도 같이 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

하위 뷰는 부모 뷰의 모든 데이터를 기본적으로 상속받지만, 추가로 별도의 데이터를 배열로 넘길 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

만약 존재하지 않는 뷰를 `@include`로 포함하려 하면, 라라벨은 에러를 발생시킵니다. 존재하지 않을 수도 있는 뷰는 `@includeIf`를 사용하는 것이 좋습니다.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

주어진 불리언 조건에 따라 뷰를 포함하고 싶을 때는 `@includeWhen` 또는 `@includeUnless` 지시문을 활용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에서 존재하는 첫 번째 뷰만 포함하고 싶을 때는 `includeFirst` 지시문을 사용하세요.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> 블레이드 뷰에서는 `__DIR__`와 `__FILE__` 상수 사용을 피하시기 바랍니다. 이 상수들은 캐시된 컴파일 뷰의 경로를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>

#### 컬렉션을 위한 뷰 렌더링

Blade의 `@each` 지시문을 사용하면 반복문과 `include`를 한 줄로 결합할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

`@each` 지시문의 첫 번째 인수는 배열 또는 컬렉션의 각 요소에 대해 렌더링할 뷰입니다. 두 번째 인수는 반복하고자 하는 배열 또는 컬렉션을, 세 번째 인수는 뷰 내부에서 현재 순회되고 있는 요소에 할당될 변수명을 의미합니다. 예를 들어, `jobs` 배열을 반복하는 경우, 뷰 내에서 각 작업을 `job` 변수로 사용할 수 있습니다. 반복의 현재 배열 키는 뷰 내에서 `key` 변수로 접근할 수 있습니다.

또한 `@each`에 네 번째 인수를 전달할 수 있습니다. 이 인수는 지정한 배열이 비어 있을 때 렌더링할 뷰를 지정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 상위 뷰의 변수들을 상속하지 않습니다. 자식 뷰에서 상위 뷰의 변수가 필요하다면 `@foreach`와 `@include` 지시문을 대신 사용해야 합니다.

<a name="the-once-directive"></a>
### `@once` 지시문

`@once` 지시문을 사용하면 템플릿의 일부 구문을 한 번만 평가하도록 만들 수 있습니다. 예를 들어, [스택](#stacks)을 이용해 어떤 JavaScript 코드를 페이지 헤더에 한 번만 삽입하고 싶을 때 유용합니다. 만약 반복문 안에서 [컴포넌트](#components)를 렌더링할 때, 해당 컴포넌트의 첫 렌더링 시에만 JavaScript를 헤더에 추가하고 싶다면 다음과 같이 사용할 수 있습니다.

```blade
@once
    @push('scripts')
        <script>
            // 여기에 사용자 정의 JavaScript 코드...
        </script>
    @endpush
@endonce
```

`@once`는 주로 `@push`나 `@prepend`와 함께 사용하는 경우가 많으므로, 보다 간편하게 사용할 수 있도록 `@pushOnce`, `@prependOnce` 지시문도 제공합니다.

```blade
@pushOnce('scripts')
    <script>
        // 여기에 사용자 정의 JavaScript 코드...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP

특정 상황에서는 뷰 내에 PHP 코드를 직접 삽입해야 할 때가 있습니다. Blade의 `@php` 지시문을 이용하면 템플릿 안에서 일반 PHP 코드를 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

또는 단순히 PHP 클래스를 임포트해야 할 때는 `@use` 지시문을 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

`@use` 지시문에 두 번째 인수를 전달하면 임포트한 클래스에 별칭(alias)을 지정할 수 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 내에서 여러 클래스를 임포트할 경우 한 번에 그룹으로 임포트할 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

또한, `@use`는 `function`, `const` 키워드를 경로 앞에 붙여 PHP 함수나 상수도 임포트할 수 있습니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

클래스 임포트와 마찬가지로 함수와 상수에 별칭(alias)도 지정할 수 있습니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

function과 const 키워드 모두 그룹 임포트가 가능하므로, 한 번의 지시문으로 같은 네임스페이스의 여러 심볼을 임포트할 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서는 주석을 뷰 파일에 작성할 수 있습니다. Blade 주석은 HTML 주석과 달리, 렌더링된 HTML 결과물에는 포함되지 않습니다.

```blade
{{-- 이 주석은 만들어진 HTML에 삽입되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, include와 유사한 장점을 제공합니다. 다만, 어떤 개발자에게는 컴포넌트와 슬롯이라는 개념이 더 직관적으로 다가올 수도 있습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트 두 가지 방식으로 작성할 수 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` 아티즌 명령어를 사용합니다. 예시로 간단한 `Alert` 컴포넌트를 만들어보겠습니다. `make:component` 명령어를 실행하면 해당 컴포넌트가 `app/View/Components` 디렉토리에 생성됩니다.

```shell
php artisan make:component Alert
```

`make:component` 명령어는 컴포넌트의 뷰 템플릿도 함께 생성해줍니다. 뷰 파일은 `resources/views/components` 디렉토리에 위치하게 됩니다. 애플리케이션에서 직접 컴포넌트를 만들 경우, `app/View/Components`와 `resources/views/components` 디렉토리 내의 컴포넌트들은 자동으로 인식되므로 일반적으로 별도의 등록 과정은 필요하지 않습니다.

또한, 하위 디렉토리 내에 컴포넌트를 만들 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령을 실행하면, `app/View/Components/Forms` 디렉토리에 `Input` 컴포넌트가 생성되고, `resources/views/components/forms` 디렉토리에 뷰 파일이 만들어집니다.

만약 별도의 클래스 없이 Blade 템플릿 파일만으로 구성된 익명(anonymous) 컴포넌트를 만들고자 한다면, `make:component` 명령에 `--view` 플래그를 추가해 사용할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

이 명령어는 `resources/views/components/forms/input.blade.php`에 Blade 파일을 생성하며, `<x-forms.input />`과 같은 방식으로 컴포넌트로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

본인 애플리케이션에서 컴포넌트를 작성하는 경우라면, `app/View/Components`와 `resources/views/components` 디렉토리에서 자동으로 감지되기 때문에 별도의 등록이 필요 없습니다.

하지만, 패키지 개발 시 Blade 컴포넌트를 사용할 경우에는 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 등록합니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

이렇게 등록하면, 아래와 같이 태그 별칭을 이용해 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 이용해 컨벤션에 따라 컴포넌트 클래스를 오토로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지에서 `Package\Views\Components` 네임스페이스에 `Calendar`, `ColorPicker` 컴포넌트가 있다고 해봅니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면, 아래처럼 벤더 네임스페이스를 `package-name::` 형식으로 사용해 패키지 컴포넌트들을 쓸 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환해 자동으로 해당 컴포넌트 클래스와 연결해줍니다. 하위 디렉토리가 있는 경우 "dot" 표기법도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 화면에 표시하려면, Blade 컴포넌트 태그를 Blade 템플릿 내에서 사용할 수 있습니다. 컴포넌트 태그는 `x-`로 시작하고, 컴포넌트 클래스 이름을 케밥 케이스(kebab-case, 소문자-하이픈)로 표기해 사용합니다.

```blade
<x-alert/>

<x-user-profile/>
```

만약 컴포넌트 클래스가 `app/View/Components` 하위에 더 깊게 중첩되어 있다면, 디렉토리 구조를 나타내기 위해 `.` 문자를 사용할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다고 하면 아래처럼 렌더링 할 수 있습니다.

```blade
<x-inputs.button/>
```

조금 더 동적으로 컴포넌트를 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 만약 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더링 여부를 결정합니다.
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

때로는 여러 컴포넌트가 하나의 그룹에 속하는 경우, 관련된 컴포넌트들을 하나의 디렉토리에 묶고 싶을 수 있습니다. 예를 들어 “카드(card)”와 관련된 다음 구조를 생각해 봅시다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 `Card` 컴포넌트가 `Card` 디렉토리 안에 위치한다면, `<x-card.card>`처럼 중복해서 사용해야 할 것 같지만, 라라벨은 컴포넌트 파일 이름이 디렉토리 이름과 일치하면 해당 컴포넌트가 "루트 컴포넌트"라고 간주하여 디렉토리 이름을 반복하지 않고 바로 사용할 수 있도록 처리합니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

Blade 컴포넌트에 데이터를 전달하려면 HTML 속성을 사용할 수 있습니다. 기본적인 값(문자열, 숫자 등)은 단순히 HTML 속성 형태로 넘기면 되고, PHP 식이나 변수는 속성 이름 앞에 `:`를 붙여 전달해야 합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자(constructor)에서 컴포넌트의 모든 데이터 속성을 정의해야 합니다. 컴포넌트의 모든 public 속성(property)은 자동으로 뷰에서 사용할 수 있게 되며, 별도로 `render` 메서드에서 뷰에 데이터를 넘겨줄 필요가 없습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스 생성자
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 컴포넌트를 나타내는 뷰/콘텐츠 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, 컴포넌트의 public 변수들은 이름으로 바로 출력할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이싱(casing) 규칙

컴포넌트 생성자 인수는 `camelCase`로 지정해야 하며, HTML 속성에서는 `kebab-case`를 사용해야 합니다. 예를 들어 다음과 같은 컴포넌트 생성자가 있다면:

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

이 경우 컴포넌트의 `$alertType` 인수는 다음과 같은 방식으로 전달할 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 축약(Short Attribute) 문법

컴포넌트에 속성을 전달할 때는 축약 문법도 쓸 수 있습니다. 축약 문법은 속성 이름과 변수명이 같을 때 유용합니다.

```blade
{{-- 축약 문법 사용 예시 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일한 결과 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JavaScript 프레임워크에서는 속성 앞에 콜론(`:`)을 사용하는데, 이 경우 Blade가 PHP 표현식으로 해석하지 않도록 별도로 이스케이프 처리할 수 있습니다. `::`로 접두어를 두 번 붙이면 됩니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

위의 경우 Blade가 렌더링하는 HTML은 다음과 같습니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트의 public 변수 뿐만 아니라, public 메서드도 컴포넌트 템플릿에서 사용할 수 있습니다. 예를 들어, `isSelected` 라는 메서드가 있다고 가정해보겠습니다.

```php
/**
 * 지정한 옵션이 현재 선택된 옵션인지 확인합니다.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 템플릿에서는 해당 메서드명과 동일한 변수를 호출하는 방식으로 실행할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성과 슬롯 접근하기

Blade 컴포넌트에서는 컴포넌트 이름, 속성(attributes), 슬롯(slot)에 접근할 수 있습니다. 이런 데이터에 접근하려면, 컴포넌트의 `render` 메서드에서 클로저를 반환하면 됩니다.

```php
use Closure;

/**
 * 컴포넌트를 나타내는 뷰/콘텐츠 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

컴포넌트의 `render` 메서드가 반환하는 클로저는 `$data` 배열을 인자로 받게 할 수도 있습니다. `$data`에는 다양한 컴포넌트 정보를 담은 요소들이 들어 있습니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 요소를 Blade 문자열로 직접 포함시키지 마십시오. 이를 조심하지 않으면 악의적인 속성값을 통한 원격 코드 실행 취약점이 발생할 수 있습니다.

`componentName`은 HTML 태그에서 `x-` 접두사를 제외한 이름과 같습니다. 즉 `<x-alert />`라면 `componentName` 값은 `alert`이 됩니다. `attributes`에는 모든 HTML 태그 속성이, `slot`에는 컴포넌트 슬롯의 내용이 `Illuminate\Support\HtmlString` 인스턴스로 담깁니다.

클로저의 반환값은 문자열이어야 하며, 반환된 문자열이 실제 뷰 파일의 이름과 일치하면 해당 뷰가 렌더링되고, 그렇지 않은 경우는 Blade 인라인 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트에서 라라벨의 [서비스 컨테이너](/docs/12.x/container)로부터 의존성을 주입받고 싶다면, 컴포넌트 데이터 속성보다 먼저 해당 타입의 변수명을 나열하면 컨테이너가 자동으로 주입합니다.

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성과 메서드 감추기

컴포넌트 템플릿에 노출하지 않고 싶은 특정 public 메서드나 속성이 있다면, 컴포넌트에서 `$except` 배열 속성에 해당 이름들을 추가할 수 있습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출하지 않을 속성/메서드
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스 생성자
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성(attribute)

이미 컴포넌트로 데이터 속성을 전달하는 방법을 살펴봤지만, 경우에 따라 컴포넌트의 핵심 기능에는 필요 없는 추가적인 HTML 속성(예: `class`) 등을 명시해야 할 수도 있습니다. 이런 추가 속성들은 보통 컴포넌트 템플릿의 루트 요소에 그대로 전달되어야 합니다. 예를 들면, 아래와 같이 `alert` 컴포넌트를 사용한다고 가정해봅시다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에서 정의하지 않은 모든 속성들은 자동으로 "속성 백(attribute bag)"에 수집됩니다. 이 속성 백은 컴포넌트 내부에서 `$attributes` 변수로 사용할 수 있습니다. 모든 속성을 컴포넌트에서 출력하려면 `$attributes` 변수를 에코하면 됩니다.

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내부에서 `@env`와 같은 Blade 지시문은 현재 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>` 형태는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합된 속성(Default / Merged Attributes)

경우에 따라 속성의 기본값을 설정하거나, 일부 속성을 추가적으로 병합해서 포함시켜야 할 수도 있습니다. 이럴 땐 속성 백의 `merge` 메서드를 이용할 수 있습니다. 이 메서드는 컴포넌트에 기본적으로 적용할 CSS 클래스를 정의할 때 특히 편리합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 아래와 같이 사용한다고 가정합시다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

이 경우 실제로 렌더링된 HTML은 다음과 같습니다.

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

일부 클래스는 특정 조건을 만족하는 경우에만 병합하고 싶을 때가 있습니다. 이럴 때는 `class` 메서드를 활용할 수 있습니다. 이 메서드는 키가 클래스(또는 클래스 배열), 값이 불리언 조건인 배열을 받습니다. 배열의 키가 숫자이면 항상 클래스 목록에 포함됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

기타 다른 속성을 추가로 병합하고 싶다면, `class` 메서드 뒤에 `merge` 메서드를 체이닝해서 사용할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성을 받아서는 안 되는 다른 HTML 요소에 조건부 클래스를 적용하려면 [@class 지시문](#conditional-classes)을 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### class 이외 속성 병합

`class`가 아닌 속성을 병합할 때는, `merge`의 값이 해당 속성의 "기본값"으로 취급됩니다. 단, `class`와 달리 이 속성들은 병합되지 않고 덮어써집니다. 예, 버튼 컴포넌트가 다음과 같이 구현되어 있다고 가정해봅시다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

아래와 같이 버튼 컴포넌트에 다른 `type` 값을 지정할 수도 있습니다. 만약 따로 지정하지 않으면 `button` 값이 기본적으로 사용됩니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

이 경우 렌더링되는 HTML은 다음과 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

`class`가 아닌 속성도 기본값과 추가 값을 이어붙이고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예제에서는 `data-controller` 속성에 `profile-controller`가 항상 맨 앞에 들어가고, 그 뒤에 추가적으로 전달된 값들이 붙게 됩니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

속성 백을 원하는 조건으로 필터링하려면 `filter` 메서드를 사용할 수 있습니다. 이 메서드는 클로저를 인수로 받으며, true를 반환하는 속성만 남겨둡니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

좀 더 편리하게, `whereStartsWith` 메서드를 쓰면 지정한 문자열로 시작하는 모든 속성만 가져올 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, `whereDoesntStartWith` 메서드를 쓰면 지정한 문자열로 시작하지 않는 속성들만 남깁니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용하면 주어진 속성 백에서 첫 번째 속성만 렌더링할 수도 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

컴포넌트에 특정 속성이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 이 메서드는 속성 이름을 인수로 받아 해당 속성이 있는지 불리언 값으로 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class 속성이 존재합니다</div>
@endif
```

여러 속성이 모두 존재하는지 확인할 때는 배열을 전달하면 됩니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 존재합니다</div>
@endif
```

지정한 여러 속성 중 하나라도 존재하는지 확인하려면 `hasAny` 메서드를 이용할 수 있습니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>속성 중 하나 이상이 존재합니다</div>
@endif
```

특정 속성의 값을 가져오고 싶다면 `get` 메서드를 사용하면 됩니다.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 지정한 키와 일치하는 속성만 가져올 때, `except` 메서드는 지정한 키와 일치하지 않는 속성만 남길 때 사용합니다.

```blade
{{ $attributes->only(['class']) }}
```

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>

### 예약된 키워드

기본적으로, 일부 키워드는 Blade의 내부용으로 예약되어 컴포넌트 렌더링에 사용됩니다. 아래에 나열된 키워드는 컴포넌트 내에서 public 속성이나 메서드 이름으로 정의할 수 없습니다.

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
### 슬롯(Slot)

컴포넌트에 추가적인 내용을 전달할 때 "슬롯(slot)"을 활용하는 경우가 많습니다. 컴포넌트 슬롯은 `$slot` 변수를 출력하여 렌더링할 수 있습니다. 이 개념을 살펴보기 위해, `alert` 컴포넌트에 다음과 같은 마크업이 있다고 가정해봅니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트에 내용을 주입하여 `slot`에 값을 전달할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

때로는 컴포넌트 내부의 여러 위치에서 서로 다른 슬롯을 렌더링해야 할 수도 있습니다. 예를 들어, "title" 슬롯도 주입할 수 있도록 alert 컴포넌트를 수정해보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명시적으로 `x-slot` 태그를 이용해 이름이 지정된 슬롯의 내용을 정의할 수 있습니다. 명시적 `x-slot` 태그 내에 포함되지 않은 모든 내용은 `$slot` 변수에 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 내용을 가지고 있는지 확인하려면, 슬롯의 `isEmpty` 메서드를 사용할 수 있습니다.

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```

또한, 슬롯에 HTML 주석이 아닌 실질적인 "내용"이 있는지 확인하려면 `hasActualContent` 메서드를 사용할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯(Scoped Slots)

Vue와 같은 JavaScript 프레임워크를 사용해본 적이 있다면, "스코프드 슬롯" 개념을 알고 있을 수 있습니다. 이 강력한 기능을 이용하면 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근할 수 있습니다. Laravel에서는 컴포넌트 클래스에 public 메서드나 속성을 정의하고, 슬롯 내에서 `$component` 변수를 통해 컴포넌트 인스턴스에 접근해 이와 비슷한 기능을 구현할 수 있습니다. 아래 예시에서는 `x-alert` 컴포넌트가 `formatAlert`라는 public 메서드를 가지고 있다고 가정합니다.

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성

Blade 컴포넌트와 마찬가지로, 슬롯에도 CSS 클래스명과 같은 [속성(attribute)](#component-attributes)을 추가할 수 있습니다.

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```

슬롯 속성과 상호작용하려면, 슬롯 변수의 `attributes` 속성에 접근할 수 있습니다. 속성과 상호작용하는 방법에 대한 자세한 내용은 [컴포넌트 속성 문서](#component-attributes)를 참고하세요.

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

<a name="inline-component-views"></a>
### 인라인 컴포넌트 뷰

아주 짧은 컴포넌트의 경우, 컴포넌트 클래스와 뷰 템플릿을 따로 관리하는 것이 번거로울 수 있습니다. 이런 상황에서는 `render` 메서드에서 컴포넌트의 마크업을 직접 반환할 수 있습니다.

```php
/**
 * 컴포넌트를 표현하는 뷰 혹은 내용을 반환합니다.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```

<a name="generating-inline-view-components"></a>
#### 인라인 뷰 컴포넌트 생성

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령어 실행 시 `inline` 옵션을 사용할 수 있습니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

경우에 따라 렌더링할 컴포넌트가 런타임에 결정되어야 할 때가 있습니다. 이럴 때는 Laravel의 내장 `dynamic-component` 컴포넌트를 사용해서, 런타임 값이나 변수에 따라 컴포넌트를 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래의 컴포넌트 수동 등록 관련 문서는, 뷰 컴포넌트를 포함한 Laravel 패키지를 개발하는 경우에 주로 해당합니다. 자신의 애플리케이션에서만 개발할 경우 이 내용은 보통 필요하지 않습니다.

개인 애플리케이션에서 컴포넌트를 개발할 때는, `app/View/Components` 디렉터리와 `resources/views/components` 디렉터리 내의 컴포넌트들이 자동으로 인식됩니다.

그러나 Blade 컴포넌트를 활용하는 패키지를 개발하거나, 권장되지 않는 디렉터리에 컴포넌트를 위치시켰을 경우에는 컴포넌트 클래스와 해당 HTML 태그 별칭을 Laravel이 인식할 수 있도록 직접 등록해야 합니다. 일반적으로는 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지의 서비스들을 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

이렇게 컴포넌트를 등록한 후에는, 태그 별칭을 사용하여 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

또한, `componentNamespace` 메서드를 사용하면 컨벤션을 기반으로 컴포넌트 클래스들을 자동 로딩할 수 있습니다. 예를 들어, `Nightshade` 패키지 내에 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 위치한다면 다음과 같이 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지의 서비스들을 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 등록하면 아래와 같이 vendor 네임스페이스가 포함된 `package-name::` 문법으로 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스(Pascal Case)로 변환하여 대응되는 클래스를 자동으로 찾습니다. 하위 디렉터리도 점(.) 표기법을 통해 지원됩니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 유사하게, 익명(anonymous) 컴포넌트는 단일 파일로 컴포넌트를 관리할 수 있게 해줍니다. 하지만 익명 컴포넌트는 뷰 파일 하나만 사용하며, 별도의 클래스는 없습니다. 익명 컴포넌트를 정의하려면, 단순히 `resources/views/components` 디렉터리에 Blade 템플릿 파일을 생성하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의했다면 아래와 같이 바로 렌더링할 수 있습니다.

```blade
<x-alert/>
```

컴포넌트가 `components` 디렉터리 내에서 더 깊이 중첩되어 있다면, `.` 문자로 표현할 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php`에 정의된 컴포넌트는 아래와 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트(Anonymous Index Components)

여러 Blade 템플릿으로 이루어진 컴포넌트를 하나의 디렉터리로 그룹화하고 싶을 때가 있습니다. 예를 들어, "accordion" 컴포넌트가 다음과 같은 디렉터리 구조를 가진다고 해봅시다.

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이런 구조를 사용하면, 아래처럼 accordion 컴포넌트와 그 하위 item을 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

그러나 이렇게 렌더링하려면 "index" accordion 컴포넌트 템플릿을 반드시 `resources/views/components` 디렉터리(즉, accordion 디렉터리의 바깥)에 두어야만 했습니다.

다행히도, Blade는 해당 컴포넌트의 디렉터리 안에 컴포넌트 디렉터리 이름과 동일한 파일을 배치하는 것을 허용합니다. 이 템플릿이 존재한다면, 디렉터리 내에 있어도 그 컴포넌트의 "루트" 요소로 렌더링할 수 있습니다. 즉, 위의 예시와 동일하게 사용할 수 있지만, 디렉터리 구조는 다음처럼 조정할 수 있습니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 프로퍼티 / 속성

익명 컴포넌트에는 별도의 클래스가 없기 때문에, 어떤 데이터가 컴포넌트에 변수로 전달되고 어떤 속성이 [attribute bag](#component-attributes)에 포함되는지 구분하는 방법이 궁금할 수 있습니다.

컴포넌트 Blade 템플릿 상단에 `@props` 지시어를 사용하면, 어떤 속성들을 데이터 변수로 취급할지 지정할 수 있습니다. 나머지 속성들은 모두 컴포넌트의 attribute bag을 통해 접근할 수 있습니다. 데이터 변수에 기본값을 설정하려면 배열의 키로 변수명을, 값으로 기본값을 지정하면 됩니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 컴포넌트를 정의했다면, 다음처럼 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

자식 컴포넌트 내에서 부모 컴포넌트의 데이터를 접근하고 싶은 경우도 있을 수 있습니다. 이런 상황에서는 `@aware` 지시어를 사용할 수 있습니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`으로 이루어진 복잡한 메뉴 컴포넌트를 만들고 있다고 가정해봅시다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` 컴포넌트는 다음과 같이 구성될 수 있습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` prop이 부모(`<x-menu>`)에만 전달되었기 때문에, 자식 `<x-menu.item>`에서는 사용할 수 없습니다. 그러나 `@aware` 지시어를 사용하면 자식에서도 해당 변수를 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시어는 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터만 접근할 수 있습니다. 부모 컴포넌트에서 명시적으로 전달하지 않은 기본 `@props` 값은 `@aware`로 사용할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 설명한 것처럼 익명 컴포넌트는 기본적으로 `resources/views/components` 디렉터리에 Blade 템플릿을 생성하여 정의합니다. 하지만 필요한 경우, Laravel에 추가로 익명 컴포넌트 경로를 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자로 익명 컴포넌트가 위치한 "경로"를, 두 번째 인자로는 선택적으로 해당 컴포넌트가 속할 "네임스페이스"를 전달받습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출하면 됩니다.

```php
/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

위처럼 접두어(prefix) 없이 컴포넌트 경로를 등록하면, Blade 컴포넌트에서 해당 경로 아래에 있는 컴포넌트도 별도의 접두어 없이 아래와 같이 사용할 수 있습니다.

```blade
<x-panel />
```

두 번째 인자로 접두어 "네임스페이스"를 전달할 수도 있습니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이렇게 접두어가 지정되면, 해당 네임스페이스 안의 컴포넌트는 컴포넌트 이름 앞에 네임스페이스를 붙여 렌더링해야 합니다.

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 만들기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에서 동일한 레이아웃을 유지합니다. 만약 모든 뷰마다 전체 레이아웃 HTML을 반복해야 한다면, 애플리케이션을 관리하기 매우 불편할 것입니다. 다행히도, 이 레이아웃을 하나의 [Blade 컴포넌트](#components)로 정의해두고, 애플리케이션 곳곳에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "todo" 목록 애플리케이션을 만든다고 가정하겠습니다. 다음과 같이 `layout` 컴포넌트를 작성할 수 있습니다.

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a name="applying-the-layout-component"></a>
#### 레이아웃 컴포넌트 적용

`layout` 컴포넌트가 준비되었으면, 이 컴포넌트를 활용하는 Blade 뷰를 만들어볼 수 있습니다. 아래는 할 일 목록을 출력하는 간단한 예시입니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 주입되는 콘텐츠는 기본적으로 `layout` 컴포넌트의 `$slot` 변수에 전달됩니다. 그리고, `layout` 컴포넌트는 `$title` 슬롯이 제공될 경우 이를 사용하고, 그렇지 않으면 기본 타이틀을 사용하도록 처리되어 있습니다. 할 일 목록 뷰에서 슬롯 구문을 사용해 커스텀 타이틀도 주입할 수 있습니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

이제 레이아웃과 할 일 목록 뷰가 모두 준비되었으니, 라우트에서 `task` 뷰를 반환하면 됩니다.

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의

레이아웃은 "템플릿 상속" 방식으로도 정의할 수 있습니다. 이 방법은 [컴포넌트](#components) 도입 이전의 주요 레이아웃 관리 방식이었습니다.

간단한 예시로 살펴보겠습니다. 우선, 페이지의 레이아웃을 정의합니다. 대다수 웹 애플리케이션이 여러 페이지에서 동일한 레이아웃을 사용하므로, 아래와 같이 단일 Blade 뷰로 레이아웃을 만들어두면 효율적입니다.

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

위 파일은 일반적인 HTML 마크업을 포함하고 있습니다. 하지만 `@section`과 `@yield` 지시어에 주목해보세요. `@section` 지시어는 이름 그대로 콘텐츠의 구역을 정의하고, `@yield`는 해당 구역(section)의 내용을 원하는 곳에서 출력할 때 사용합니다.

이제 레이아웃이 정의되었으니, 이 레이아웃을 상속하는 자식 페이지를 만들어보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

자식 뷰 파일에서는 `@extends` Blade 지시어로 어느 레이아웃을 상속할지 지정해야 합니다. 레이아웃을 상속한 뷰에서는 `@section` 지시어를 통해 각 구역에 내용을 주입할 수 있습니다. 위 예시에서처럼, 각 section의 내용은 레이아웃 뷰 내의 `@yield`가 위치한 곳에 출력됩니다.

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

이 예시에서, `sidebar` 구역은 `@@parent` 지시어를 사용하여 부모 레이아웃의 sidebar 콘텐츠 뒤에 내용을 추가하고 있습니다. `@@parent`는 뷰 렌더링 시 레이아웃에서 정의된 sidebar 내용을 해당 위치에 삽입합니다.

> [!NOTE]
> 앞서 예시와 달리, 이 `sidebar` 구역은 끝에 `@endsection`으로 마감합니다. `@endsection`은 section만을 정의하고, `@show`는 section 정의와 동시에 **즉시 출력**까지 수행합니다.

`@yield` 지시어는 두 번째 매개변수로 기본값도 받을 수 있습니다. 만약 해당 section이 정의되지 않으면 기본값이 출력됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Form)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때는 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있도록, 반드시 폼 내부에 숨겨진 CSRF 토큰 필드를 포함해야 합니다. Blade의 `@csrf` 지시어를 사용하면 CSRF 토큰 필드를 손쉽게 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드(Method Field)

HTML 폼은 본래 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없으므로, 해당 HTTP 메서드를 흉내내기 위해 숨겨진 `_method` 필드를 추가해야 합니다. `@method` Blade 지시어는 이 필드를 자동으로 생성해줍니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검사 에러(Validation Errors)

`@error` 지시어를 사용하면, 주어진 attribute에 대한 [유효성 검사 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors) 존재 여부를 신속하게 확인할 수 있습니다. `@error` 내부에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

`@error` 지시어는 내부적으로 "if" 문으로 컴파일되므로, `@else` 지시어를 활용하여 해당 attribute에 에러가 없을 때 렌더링할 내용을 정의할 수도 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[여러 폼이 있는 페이지](/docs/12.x/validation#named-error-bags)에서 특정 에러 백(error bag)의 유효성 검사 에러 메시지만 확인하고 싶다면, `@error` 지시어의 두 번째 인자로 에러 백 이름을 전달할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror"
/>

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>

## 스택(Stacks)

Blade에서는 특정 이름을 가진 스택에 내용을 추가(`push`)해두고, 이를 다른 뷰나 레이아웃의 원하는 위치에서 렌더링할 수 있습니다. 이 기능은 자식 뷰에서 필요한 JavaScript 라이브러리 등을 지정할 때 유용하게 사용할 수 있습니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 불린(boolean) 조건이 `true`일 때만 `@push`를 실행하고 싶다면, `@pushIf` 디렉티브를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에는 원하는 만큼 여러 번 내용을 추가할 수 있습니다. 추가된 스택 내용을 모두 렌더링하려면, `@stack` 디렉티브에 해당 스택명을 전달하면 됩니다.

```blade
<head>
    <!-- Head 내용 -->

    @stack('scripts')
</head>
```

스택의 가장 처음에 내용을 추가하고 싶다면, `@prepend` 디렉티브를 사용합니다.

```blade
@push('scripts')
    This will be second...
@endpush

// 나중에...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입(Service Injection)

`@inject` 디렉티브를 사용하면 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 서비스를 바로 가져올 수 있습니다. `@inject`의 첫 번째 인자는 주입된 서비스가 할당될 변수명이고, 두 번째 인자는 가져오려는 서비스의 클래스나 인터페이스명입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

간혹 순수 Blade 템플릿 문자열을 실제 HTML로 변환하고 싶을 때가 있습니다. 이럴 때는 `Blade` 파사드의 `render` 메서드를 사용하면 됩니다. `render` 메서드는 Blade 템플릿 문자열과 템플릿에 전달할 데이터 배열(선택 사항)을 받습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

라라벨은 인라인 Blade 템플릿을 렌더링할 때, 임시 파일을 `storage/framework/views` 디렉토리에 저장합니다. 만약 Blade 템플릿 렌더링 후 이 임시 파일을 자동으로 삭제하고 싶다면, `deleteCachedView` 인자를 추가로 전달하면 됩니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트(Fragments) 렌더링

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, HTTP 응답에서 Blade 템플릿의 일부만 반환해야 할 때가 있습니다. Blade의 "프래그먼트(fragment)" 기능을 사용하면 이를 손쉽게 구현할 수 있습니다. 먼저, 렌더링할 부분을 `@fragment`와 `@endfragment` 디렉티브로 감싸줍니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이제 이 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출해 원하는 프래그먼트만 HTTP 응답으로 반환하도록 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 특정 조건에 따라 프래그먼트만 반환하거나, 조건을 충족하지 않으면 전체 뷰를 반환하도록 할 수 있습니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments` 및 `fragmentsIf` 메서드를 사용하면, 여러 개의 뷰 프래그먼트를 한 번에 응답으로 반환할 수 있습니다. 반환되는 프래그먼트들은 하나로 이어붙여집니다.

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```

<a name="extending-blade"></a>
## Blade 확장하기

Blade에서는 `directive` 메서드를 사용해 커스텀 디렉티브를 직접 정의할 수 있습니다. Blade 컴파일러가 이 커스텀 디렉티브를 만나면, 지정한 콜백 함수에 디렉티브에 전달된 식(expression)을 넘겨 호출합니다.

아래 예시에서는 `@datetime($var)`이라는 디렉티브를 만드는데, 이는 `$var`가 `DateTime` 인스턴스여야 하며 그 값을 원하는 포맷으로 출력해줍니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

이 예제에서 볼 수 있듯, 디렉티브에 전달된 식에 바로 `format` 메서드를 체이닝하여 날짜 포맷을 맞춰줍니다. 그러면 이 디렉티브로 최종적으로 생성된 PHP 코드는 아래와 같습니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정했다면, 캐싱된 모든 Blade 뷰 파일을 반드시 삭제해야 합니다. 캐시된 뷰 파일은 `view:clear` 아티즌 명령어로 정리할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러(Custom Echo Handlers)

Blade에서 객체를 `{{ }}`를 사용해 "에코"하면, 해당 객체의 `__toString` 메서드가 자동으로 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 하지만, 써드파티 라이브러리 등에서 제공하는 클래스처럼, 이 메서드를 직접 수정할 수 없는 경우도 있습니다.

이러한 상황에서는, Blade가 특정 타입의 객체를 렌더링할 때 사용할 커스텀 에코 핸들러를 등록할 수 있습니다. 이를 위해 Blade의 `stringable` 메서드를 호출하면 됩니다. `stringable` 메서드는 클로저를 인자로 받으며, 이 클로저는 처리할 객체 타입을 타입힌트로 명시해야 합니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 작성합니다.

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

커스텀 에코 핸들러가 등록되면, Blade 템플릿에서 해당 객체를 그냥 출력(`{{ $money }}`)하면 자동으로 지정한 방식대로 문자열로 변환되어 출력됩니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문(Custom If Statements)

간단한 커스텀 조건문을 만들 때, 직접 디렉티브를 프로그래밍하는 것은 오히려 복잡할 수 있습니다. 이런 경우에는 Blade의 `Blade::if` 메서드를 활용해 Closure로 쉽게 커스텀 조건 디렉티브를 정의할 수 있습니다. 예를 들어, 애플리케이션의 기본 "disk" 설정값이 특정 값인지 확인하는 조건문을 만들어 보겠습니다. 이 역시 보통 `AppServiceProvider`의 `boot` 메서드에서 작성합니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

이렇게 커스텀 조건문을 정의하고 나면, Blade 템플릿에서 바로 사용할 수 있습니다.

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크를 사용 중일 때... -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크를 사용 중일 때... -->
@else
    <!-- 애플리케이션이 그 외의 디스크를 사용 중일 때... -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크를 사용하지 않을 때... -->
@enddisk
```