# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 디렉티브](#blade-directives)
    - [If문](#if-statements)
    - [Switch문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [Index 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯(Slot)](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 Index 컴포넌트](#anonymous-index-components)
    - [데이터 속성/attribute](#data-properties-attributes)
    - [상위 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성](#building-layouts)
    - [컴포넌트 기반 레이아웃](#layouts-using-components)
    - [템플릿 상속 기반 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [Method 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택(Stack)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If문](#custom-if-statements)

<a name="introduction"></a>
## 소개

블레이드는 라라벨에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿 내에서 일반 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로 블레이드의 모든 템플릿은 순수 PHP 코드로 컴파일되어, 변경되기 전까지 캐시에 저장됩니다. 따라서 블레이드는 애플리케이션에 거의 아무런 오버헤드도 추가하지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 사용하며, 일반적으로 `resources/views` 디렉터리에 저장됩니다.

블레이드 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론 [뷰](/docs/12.x/views) 문서에서 설명한 것처럼, `view` 헬퍼의 두 번째 인수로 데이터를 블레이드 뷰에 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 강화하기

블레이드 템플릿을 한 단계 더 끌어올리고, 쉽게 동적인 인터페이스를 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면 블레이드 컴포넌트에 동적 기능을 추가할 수 있습니다. 이런 동적 기능은 일반적으로 React나 Vue 같은 프론트엔드 프레임워크에서만 구현 가능했으나, Livewire를 통해 복잡한 빌드 과정, 클라이언트 렌더링 등 JavaScript 프레임워크의 부담 없이, 모던하고 반응형인 프론트엔드를 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 표시

블레이드 뷰에 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다면:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 값을 아래와 같이 표시할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> 블레이드의 `{{ }}` 출력 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 자동으로 거칩니다.

뷰에 전달된 변수의 값만 표시해야 하는 것은 아닙니다. 모든 PHP 함수의 반환값도 출력할 수 있으며, 실제로 블레이드 출력 구문 내에는 원하는 어떠한 PHP 코드도 사용할 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로, 블레이드(그리고 라라벨의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 원하지 않는 경우, `AppServiceProvider`의 `boot` 메서드 안에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프하지 않은 데이터 표시

기본적으로 블레이드의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수가 자동 적용됩니다. 만약 데이터를 이스케이프하지 않고 그대로 출력하고 싶다면, 아래와 같은 구문을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자로부터 제공된 콘텐츠를 출력할 때는 매우 주의하시기 바랍니다. 사용자 입력을 출력할 때는 XSS 공격 방지를 위해 이스케이프되는 이중 중괄호 문법(`{{ }}`)을 사용하는 것이 권장됩니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크에서도 데이터 바인딩 등에 중괄호(`{}`) 표기법을 사용합니다. 이 경우, 해당 표현식을 블레이드가 건드리지 않고 그대로 두려면 `@` 기호를 붙여주면 됩니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서, 블레이드는 `@` 기호만 제거하고 `{{ name }}` 표현식은 그대로 남겨 두어, 자바스크립트 프레임워크 쪽에서 처리할 수 있도록 합니다.

또한, `@` 기호는 블레이드 디렉티브를 이스케이프할 때도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

때때로 배열을 뷰에 넘긴 뒤, 이를 JSON으로 렌더링하여 자바스크립트 변수로 초기화하고 싶을 수 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

그러나 직접 `json_encode`를 사용하지 않고, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 같은 인수를 받으며, HTML 인용부호 내에 안전하게 포함될 수 있도록 이스케이프 처리된 JSON 문자열을 반환합니다. 또한, `from` 메서드는 자바스크립트의 `JSON.parse` 구문이 포함된 문자열을 반환하므로, 전달한 배열이나 객체가 유효한 자바스크립트 객체로 변환됩니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 라라벨 애플리케이션 스켈레톤에는 이 기능을 더욱 편리하게 쓸 수 있도록 `Js` 퍼사드가 포함되어 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. 블레이드 템플릿 엔진은 정규표현식 기반으로 동작하므로, 복잡한 표현식을 이 디렉티브에 전달하면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿 내에 자바스크립트 변수가 많이 등장해, 매번 블레이드 중괄호 앞에 `@`를 붙이기 번거로운 경우, HTML 부분 전체를 `@verbatim` 디렉티브로 감쌀 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 디렉티브

템플릿 상속이나 데이터 표시뿐만 아니라, 블레이드는 조건문이나 반복문 같은 자주 사용되는 PHP 제어문을 더 간결하고 명확하게 작성할 수 있도록 편의 디렉티브를 제공합니다. 이 디렉티브를 사용하면 PHP 기본 문법과 거의 차이 없이 친숙하면서도 간단하게 제어문을 다룰 수 있습니다.

<a name="if-statements"></a>
### If문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용하여 if문을 만들 수 있습니다. 이 디렉티브들은 PHP의 if문과 완전히 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 블레이드는 `@unless` 디렉티브도 제공합니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

앞에서 소개한 조건문 디렉티브 외에도, 각각 PHP의 `isset`과 `empty` 함수와 동일하게 동작하는 `@isset` 및 `@empty` 디렉티브를 사용할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 디렉티브

`@auth`와 `@guest` 디렉티브로 현재 사용자가 [인증](/docs/12.x/authentication) 상태인지, 비회원(guest)인지 쉽게 확인할 수 있습니다.

```blade
@auth
    // 사용자가 인증된 상태...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면, `@auth` 및 `@guest` 디렉티브에서 검사할 인증 가드를 지정할 수도 있습니다.

```blade
@auth('admin')
    // 사용자가 인증된 상태...
@endauth

@guest('admin')
    // 사용자가 인증되지 않음...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 디렉티브

`@production` 디렉티브를 사용해 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // 프로덕션 전용 내용...
@endproduction
```

또는, `@env` 디렉티브로 원하는 특정 환경에서 실행 중인지도 확인할 수 있습니다.

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging"이나 "production" 환경에서 실행 중...
@endenv
```

<a name="section-directives"></a>
#### Section(섹션) 디렉티브

템플릿 상속에서 섹션에 콘텐츠가 존재하는지 확인하려면 `@hasSection` 디렉티브를 사용합니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 콘텐츠가 없는지 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 디렉티브

`@session` 디렉티브는 [세션](/docs/12.x/session) 값의 존재 유무를 확인하는 데 사용할 수 있습니다. 세션 값이 존재한다면, `@session`과 `@endsession` 디렉티브 내부의 템플릿 내용이 평가됩니다. 이 범위 내에서는 `$value` 변수를 통해 세션 값을 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 디렉티브

`@context` 디렉티브로 [컨텍스트](/docs/12.x/context) 값 존재 여부를 확인하고, 있다면 `@context`와 `@endcontext` 사이의 내용을 평가할 수 있습니다. 이때도 `$value` 변수로 컨텍스트 값을 사용할 수 있습니다.

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브로 스위치문을 구현할 수 있습니다.

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
### 반복문(Loops)

블레이드는 조건문뿐만 아니라 PHP의 반복문을 더 간편하게 쓸 수 있도록 디렉티브를 제공합니다. 각각의 디렉티브는 PHP의 반복문 구문과 동일하게 동작합니다.

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
> `foreach` 반복문을 순회하면서 [loop 변수](#the-loop-variable)를 활용하면 반복문이 처음 또는 마지막 순회 중인지 등 유용한 정보를 얻을 수 있습니다.

반복문 안에서, 현재 순회를 건너뛰거나 반복문을 중단하려면 `@continue` 및 `@break` 디렉티브를 사용할 수 있습니다.

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

조건을 디렉티브 선언에 바로 포함시킬 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 내부에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수는 현재 반복 인덱스나, 첫 번째/마지막 순회 여부 등 반복문 관련 정보를 담고 있습니다.

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

중첩 반복문에서는 상위 반복문의 `$loop` 변수에 `parent` 속성을 통해 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 아래와 같이 다양한 속성이 포함되어 있습니다.

<div class="overflow-auto">

| 속성                | 설명                                                    |
| ------------------- | ----------------------------------------------------- |
| `$loop->index`      | 현재 반복문의 인덱스(0부터 시작).                      |
| `$loop->iteration`  | 현재 반복 순서(1부터 시작).                            |
| `$loop->remaining`  | 반복문에서 남은 반복 횟수.                             |
| `$loop->count`      | 순회 대상 배열의 전체 항목 수.                         |
| `$loop->first`      | 첫 번째 반복인지 여부.                                 |
| `$loop->last`       | 마지막 반복인지 여부.                                  |
| `$loop->even`       | 현재 반복 수가 짝수인지 여부.                          |
| `$loop->odd`        | 현재 반복 수가 홀수인지 여부.                          |
| `$loop->depth`      | 중첩 반복문의 레벨(depth).                             |
| `$loop->parent`     | 중첩 반복문에서는 상위 반복문의 loop 변수.             |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 디렉티브는 CSS 클래스 문자열을 조건에 따라 동적으로 컴파일합니다. 배열의 키에 클래스명을, 값에 불리언 조건을 전달하면, 값이 true인 클래스만 포함됩니다. 만약 배열의 키가 숫자라면, 해당 클래스명은 조건과 상관없이 항상 포함됩니다.

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

`@style` 디렉티브도 마찬가지로, HTML 요소의 인라인 CSS 스타일을 조건에 따라 동적으로 추가할 수 있습니다.

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
### 추가 속성(Attribute)

체크박스 input이 "checked" 상태인지 쉽게 나타내려면 `@checked` 디렉티브를 사용할 수 있습니다. 조건식이 true라면 `checked`가 출력됩니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, select option이 "selected" 되어야 할 때는 `@selected` 디렉티브를 사용할 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, 특정 요소를 비활성화하려면 `@disabled` 디렉티브를 사용할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

입력을 읽기 전용으로 만들고 싶다면, `@readonly` 디렉티브를 사용할 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

그리고 입력값이 필수인지 나타내려면 `@required` 디렉티브를 사용할 수 있습니다.

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### 서브뷰 포함하기

> [!NOTE]
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 블레이드 [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 이점이 있어 `@include` 대신 사용을 권장합니다.

블레이드의 `@include` 디렉티브를 사용하면 한 뷰 안에서 다른 블레이드 뷰를 포함할 수 있습니다. 부모 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에서도 동일하게 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

물론, 포함된 뷰로 추가 데이터를 배열 형태로 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

`@include`하려는 뷰가 존재하지 않을 경우, 라라벨은 오류를 발생시킵니다. 존재할 수도, 존재하지 않을 수도 있는 뷰를 포함하고 싶다면 `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

주어진 불리언 표현식에 따라 뷰를 포함하려면 `@includeWhen` 및 `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에서 먼저 존재하는 뷰 하나만 포함하고 싶다면, `includeFirst` 디렉티브를 사용할 수 있습니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> 블레이드 뷰 내에 `__DIR__` 와 `__FILE__` 상수 사용은 피해야 합니다. 이 상수들은 캐시된 컴파일 뷰의 위치를 가리키게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

반복문과 인클루드를 한 줄로 결합하고 싶다면, 블레이드의 `@each` 디렉티브를 사용할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

`@each` 디렉티브의 첫 번째 인수는 각 요소마다 렌더링할 뷰, 두 번째는 반복할 배열 혹은 컬렉션, 세 번째는 현재 반복 요소에 할당될 변수명입니다. 예를 들어 `jobs` 배열을 순회하면, 각 반복의 `job` 변수로 접근할 수 있게 되며, 현재 반복의 배열 키는 `key` 변수로 사용할 수 있습니다.

네 번째 인수로, 만약 배열이 비어 있을 때 사용할 뷰를 지정할 수도 있습니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식(포함된) 뷰에서 부모의 변수가 필요하다면 반드시 `@foreach`와 `@include`를 함께 사용하세요.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브를 사용하면 해당 블록 내부의 템플릿 내용이 렌더링 주기마다 한 번만 실행되도록 할 수 있습니다. [스택](#stacks)에 JavaScript 등을 한 번만 삽입하고 싶을 때 유용합니다. 예를 들어, 반복문 내에서 [컴포넌트](#components)를 렌더링할 때 해당 JavaScript를 최초 한 번만 헤더에 추가하고 싶다면 아래처럼 사용할 수 있습니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once` 디렉티브는 `@push`나 `@prepend` 디렉티브와 자주 조합되기 때문에, 더 편리하게 사용할 수 있도록 `@pushOnce`와 `@prependOnce` 디렉티브도 제공됩니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

상황에 따라, 뷰에 PHP 코드를 직접 삽입해서 사용해야 할 때가 있습니다. 이 경우 블레이드의 `@php` 디렉티브를 사용해 순수 PHP 코드를 블록으로 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

클래스 import만 필요하다면, `@use` 디렉티브를 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

`@use` 디렉티브는 두 번째 인수로 import된 클래스에 별칭(alias)을 부여하는 것도 가능합니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스의 여러 클래스를 한 번에 그룹 import 할 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

또한 `@use` 디렉티브는 `function`이나 `const` 키워드를 붙여, PHP 함수와 상수도 import할 수 있습니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

클래스 import와 마찬가지로, 함수와 상수 import에도 별칭을 붙일 수 있습니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수와 상수도 그룹 import가 가능하며, 한 디렉티브 내에서 같은 네임스페이스의 여러 심볼을 한꺼번에 가져올 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

블레이드는 뷰 안에서 주석을 작성할 수 있습니다. HTML 주석과 달리 블레이드 주석은 렌더링된 HTML 결과물에는 포함되지 않습니다.

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>

## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 유사한 이점을 제공합니다. 그러나 컴포넌트와 슬롯의 개념이 더 직관적으로 느껴질 수 있습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트, 두 가지 방식으로 작성할 수 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` 아티즌 명령어를 사용할 수 있습니다. 예시로, 간단한 `Alert` 컴포넌트를 만들어보겠습니다. `make:component` 명령어는 컴포넌트를 `app/View/Components` 디렉터리에 생성합니다.

```shell
php artisan make:component Alert
```

`make:component` 명령어는 컴포넌트의 뷰 템플릿도 함께 만듭니다. 해당 뷰는 `resources/views/components` 디렉터리 아래에 위치하게 됩니다. 여러분이 직접 애플리케이션을 개발하는 경우, 컴포넌트는 `app/View/Components`와 `resources/views/components` 디렉터리 내에서 자동으로 인식되기 때문에 별도의 등록 작업이 대부분 필요하지 않습니다.

또한, 하위 디렉터리 내에 컴포넌트를 생성할 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령어를 실행하면 `app/View/Components/Forms` 디렉터리에 `Input` 컴포넌트가 생성되고, 해당 뷰는 `resources/views/components/forms` 디렉터리에 위치하게 됩니다.

만약 Blade 템플릿만 있고 클래스가 없는 익명(anonymous) 컴포넌트를 만들고 싶다면, 명령어 실행 시 `--view` 옵션을 붙여 사용하면 됩니다.

```shell
php artisan make:component forms.input --view
```

위 명령어를 실행하면 `resources/views/components/forms/input.blade.php` 파일이 생성되며, `<x-forms.input />` 형태로 컴포넌트로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자체 애플리케이션에서 컴포넌트를 작성하는 경우, 컴포넌트는 `app/View/Components`와 `resources/views/components` 폴더 내에 위치하면 자동으로 인식합니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 개발하는 경우에는 컴포넌트 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지의 서비스 프로바이더의 `boot` 메서드에 컴포넌트를 등록합니다.

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

이렇게 등록한 컴포넌트는 별칭을 이용해 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는, `componentNamespace` 메서드를 사용하여 네임스페이스에 따라 컴포넌트 클래스들을 자동 등록할 수 있습니다. 예를 들어, `Nightshade`라는 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 있다면 다음과 같이 등록합니다.

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

이렇게 설정하면, 벤더 네임스페이스를 사용하는 `package-name::` 문법으로 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스(Pascal-case)로 변환해서 연결된 클래스를 자동으로 인식합니다. "dot" 표기법을 이용해 하위 디렉터리도 지원됩니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 표시하려면 Blade 템플릿 내에서 Blade 컴포넌트 태그를 사용하면 됩니다. Blade 컴포넌트 태그는 항상 `x-`로 시작하며, 컴포넌트 클래스 이름은 케밥 케이스(kebab-case)로 작성합니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉터리 내의 하위 경로에 위치할 경우, 경로 구분을 위해 `.` 문자를 사용할 수 있습니다. 예를 들어 `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면, 아래처럼 사용할 수 있습니다.

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * 해당 컴포넌트를 렌더링할지 여부를 결정
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

컴포넌트가 여러 구성 요소를 묶은 "컴포넌트 그룹"의 일부인 경우, 관련된 컴포넌트들을 하나의 디렉터리로 그룹화하고 싶을 수 있습니다. 예를 들어, 아래와 같은 형태로 "card" 컴포넌트가 있다고 가정해봅시다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 `Card` 컴포넌트가 `Card` 디렉터리에 위치하고 있기 때문에, `<x-card.card>`처럼 디렉터리와 파일명을 중복해서 지정해야 할 것 같지만, 파일명과 디렉터리명이 같을 때 라라벨은 이를 "루트" 컴포넌트로 간주해서 디렉터리 이름만으로 바로 렌더링할 수 있게 해줍니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트로 데이터 전달

Blade 컴포넌트에 데이터를 전달하려면 HTML 속성을 사용합니다. 값이 고정된 원시 데이터는 HTML 속성 문자열로, PHP 표현식이나 변수를 전달하려면 속성 이름 앞에 `:`(콜론)을 붙여 사용합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트에서 사용할 모든 데이터 속성은 반드시 클래스의 생성자(constructor)에 정의해야 합니다. 컴포넌트의 모든 public 속성(property)은 자동으로 뷰에서 사용할 수 있습니다. 따라서 데이터를 뷰로 직접 전달하기 위해 `render` 메서드를 통해 데이터를 추가로 넘길 필요는 없습니다.

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
     * 컴포넌트를 표현하는 뷰/콘텐츠 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링되면, public 변수를 그대로 출력해서 사용할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 속성 표기법

컴포넌트 생성자 인수(Arguments)는 `camelCase`로 지정해야 하며, HTML 속성에서는 `kebab-case` 표기를 사용합니다. 예를 들어 아래와 같이 컴포넌트 생성자가 정의되어 있다면,

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

컴포넌트를 사용할 때는 다음과 같이 속성을 전달할 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 짧은 속성 문법

컴포넌트에 속성을 전달할 때, "짧은 속성" 문법을 사용할 수 있습니다. 이 방식은 속성 이름이 실제 전달할 변수명과 일치할 때 편리합니다.

```blade
{{-- 짧은 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일한 의미입니다. --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같은 일부 자바스크립트 프레임워크가 속성명 앞에 콜론(`:`)을 사용하는 경우가 있습니다. 이때 Blade에 해당 속성이 PHP 표현식이 아님을 알리려면, 콜론을 한 번 더 붙여 `::`로 시작하는 접두사를 사용하면 됩니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

위 Blade 코드는 아래와 같이 렌더링됩니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 뷰 템플릿 안에서는 public 변수뿐 아니라 public 메서드도 사용할 수 있습니다. 예를 들어, 컴포넌트에 `isSelected` 메서드가 있다면,

```php
/**
 * 주어진 옵션이 현재 선택된 옵션인지 여부
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 템플릿에서는 해당 메서드명을 가진 변수처럼 호출해서 사용할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내부에서 Attribute/Slot 접근

Blade 컴포넌트에서는 컴포넌트 이름, 속성(attributes), 슬롯(slot) 등에 클래스의 render 메서드 내부에서 접근할 수 있습니다. 이 데이터를 사용하려면, 컴포넌트 클래스의 `render` 메서드에서 클로저(closure)를 반환해야 합니다.

```php
use Closure;

/**
 * 컴포넌트를 표현하는 뷰/콘텐츠 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

리턴된 클로저는 `$data`라는 배열을 인자로 받을 수 있습니다. 이 배열에는 컴포넌트와 관련된 여러 정보가 담겨 있습니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열 요소를 Blade 문자열에 직접 삽입해서 반환하면, 악의적인 속성 내용을 통해 원격 코드 실행이 발생할 수 있으므로 절대로 직접 사용하지 마십시오.

`componentName`에는 `x-` 프리픽스 이후 사용한 태그 이름이 저장됩니다. 예를 들어 `<x-alert />`의 경우 `componentName`은 `alert`이 됩니다. `attributes` 요소에는 해당 태그에 지정된 모든 속성이 들어 있으며, `slot` 요소는 해당 컴포넌트의 슬롯 내용을 담고 있는 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저는 반드시 문자열을 반환해야 하며, 반환한 문자열이 실존하는 뷰의 이름이라면 해당 뷰가 렌더링되고, 존재하지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트가 라라벨의 [서비스 컨테이너](/docs/12.x/container)에서 의존성을 필요로 하는 경우, 의존성을 컴포넌트의 데이터 속성보다 앞서 선언하면 컨테이너가 자동으로 주입해줍니다.

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
#### 속성 및 메서드 감추기

컴포넌트 템플릿에 노출하지 않으려는 public 메서드나 프로퍼티가 있다면, 컴포넌트 클래스의 `$except` 배열 속성에 해당 이름을 추가하면 됩니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출하지 않을 속성/메서드 목록
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
### 컴포넌트 속성 (Component Attributes)

앞서 데이터를 컴포넌트로 전달하는 방법을 살펴보았지만, 경우에 따라 컴포넌트가 동작하기 위해 필요한 데이터가 아닌, 단순한 HTML 속성(예: `class`)을 지정해야 할 수 있습니다. 이런 속성들은 주로 컴포넌트 템플릿의 루트 엘리먼트에 전달하게 됩니다. 예를 들어 아래와 같이 `alert` 컴포넌트를 렌더링한다고 가정해봅니다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 정의되지 않은 모든 속성들은 자동으로 "attribute bag"에 담깁니다. 이 attribute bag은 `$attributes` 변수로 컴포넌트에서 바로 사용할 수 있으며, 아래와 같이 템플릿에서 출력해서 사용할 수 있습니다.

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현재로서는 컴포넌트 태그 내부에서 `@env` 디렉티브 등은 사용할 수 없습니다. 예를 들어 `<x-alert :live="@env('production')"/>`와 같은 코드는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합된 속성

경우에 따라 일부 속성의 기본값을 지정하거나 추가적인 값을 병합해서 지정해야 할 수도 있습니다. 이럴 때는 attribute bag의 `merge` 메서드를 사용할 수 있습니다. 이 방식은 컴포넌트에 항상 적용되어야 하는 기본 CSS 클래스를 정의할 때 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 아래와 같이 사용한다면,

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링되는 HTML은 다음과 같이 됩니다.

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건이 true일 때 클래스명을 병합하고 싶다면, `class` 메서드를 사용하면 됩니다. 여기서는 클래스를 키로, 불리언 조건을 값으로 갖는 배열을 전달합니다. 배열의 키가 숫자인 경우에는 항상 해당 클래스를 포함하게 됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

필요하다면 `class` 메서드 뒤에 `merge` 메서드를 체이닝하여 추가 속성을 병합할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성이 필요 없는 별도의 HTML 엘리먼트에서 조건부 클래스를 적용하고 싶다면, [@class 디렉티브](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class` 속성이 아닌 다른 속성을 `merge`로 병합할 경우, `merge`에 전달된 값이 해당 속성의 "기본값"이 됩니다. 단, `class`와 달리 병합하지 않고 주입된 값이 있으면 덮어씁니다. 예를 들어, `button` 컴포넌트의 구현이 다음과 같다고 가정합니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시 아래처럼 커스텀 타입을 지정할 수 있고, 지정하지 않으면 기본적으로 `button` 타입이 사용됩니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

이 경우 최종적으로 렌더링되는 HTML은 아래와 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

만약 `class`가 아닌 속성에서도 기본값과 주입값을 합치고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예시에서 `data-controller` 속성에는 항상 `profile-controller`가 앞에 붙고, 이후 추가로 지정한 값들이 뒤에 붙게 됩니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 이용해 원하는 방식으로 속성들을 필터링할 수 있습니다. 이 메서드는 클로저를 인자로 받으며, true를 반환할 경우 해당 속성이 포함됩니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

편의를 위해, 속성 키가 특정 문자열로 시작하는 속성만 가져오는 `whereStartsWith` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, 특정 문자열로 시작하지 않는 속성만 가져오려면 `whereDoesntStartWith` 메서드를 사용하세요.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 이용하면, attribute bag 내에서 첫 번째 속성만 렌더링할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성이 컴포넌트에 있는지 확인하려면 `has` 메서드를 사용합니다. 이 메서드는 속성 이름을 인자로 받고 해당 속성이 존재하는지 불리언으로 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열을 전달할 경우, 전달한 모든 속성이 존재해야 true를 반환합니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

한 가지만 존재해도 true가 되도록 확인하려면 `hasAny` 메서드를 사용할 수 있습니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드를 사용합니다.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 지정한 키의 속성만 가져올 때, `except`는 지정한 키를 제외한 속성만 가져올 때 사용할 수 있습니다.

```blade
{{ $attributes->only(['class']) }}
```

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade 컴포넌트 렌더링을 위해 일부 키워드는 내부적으로 사용되기 때문에, 컴포넌트의 public 속성이나 메서드 이름으로 사용할 수 없습니다.

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
### 슬롯 (Slots)

컴포넌트에 추가적인 콘텐츠를 전달해야 할 때가 자주 있습니다. 이때 "슬롯(slot)"을 이용하며, 슬롯은 `$slot` 변수를 출력함으로써 렌더링됩니다. 예시로, 아래처럼 `alert` 컴포넌트에 마크업이 있다고 가정합시다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이 슬롯에 콘텐츠를 전달하려면, 아래와 같이 컴포넌트 내부에 내용을 삽입하면 됩니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

경우에 따라 컴포넌트 내부 여러 위치에 다양한 슬롯을 넣어야 할 수도 있습니다. 예를 들어, "title" 슬롯을 추가하는 식으로 컴포넌트를 수정해보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이제 `x-slot` 태그를 사용하여 이름이 붙은 슬롯의 콘텐츠를 정의할 수 있습니다. 명시적으로 `x-slot` 태그 내부에 없는 콘텐츠는 모두 `$slot` 변수로 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯의 `isEmpty` 메서드를 호출하면, 슬롯에 실제로 콘텐츠가 있는지 없는지 판단할 수 있습니다.

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

또한, `hasActualContent` 메서드는 슬롯에 HTML 주석이 아닌 "실제" 콘텐츠가 포함되어 있는지 여부를 판단할 때 사용할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯 (Scoped Slots)

Vue와 같은 자바스크립트 프레임워크를 써본 경험이 있다면, "스코프드 슬롯"이라는 개념에 익숙할 수 있습니다. 스코프드 슬롯은 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근할 수 있게 합니다. 라라벨에서도 컴포넌트에 public 메서드나 속성을 정의하고 슬롯 내부에서 `$component` 변수를 통해 접근하는 방식으로 비슷한 동작을 구현할 수 있습니다. 예를 들어, `x-alert` 컴포넌트 클래스에 public `formatAlert` 메서드가 있다고 가정합니다.

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

Blade 컴포넌트와 마찬가지로, 슬롯에도 [속성](#component-attributes)을 추가할 수 있습니다. 예를 들어, 아래처럼 CSS 클래스를 슬롯에 지정할 수 있습니다.

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

슬롯 속성과 상호작용하려면 해당 슬롯 변수의 `attributes` 속성을 사용할 수 있습니다. 속성 활용에 대한 더 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요.

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

아주 작은 컴포넌트의 경우, 컴포넌트 클래스와 뷰 템플릿 파일을 따로 관리하는 것이 번거로울 수 있습니다. 이럴 때는 `render` 메서드에서 마크업을 직접 문자열로 반환할 수도 있습니다.

```php
/**
 * 컴포넌트를 표현하는 뷰/콘텐츠 반환
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

인라인 뷰를 렌더링하는 컴포넌트를 만들고 싶다면, `make:component` 명령어 실행 시 `--inline` 옵션을 사용하면 됩니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

어떤 컴포넌트를 렌더링할지 런타임 시점에 결정해야 할 때는, 라라벨에 내장된 `dynamic-component` 컴포넌트를 사용해 변수값이나 런타임 값을 기반으로 컴포넌트를 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 컴포넌트 수동 등록에 관한 다음 설명은 주로 뷰 컴포넌트를 포함하는 라라벨 패키지를 작성하는 개발자를 위한 내용입니다. 패키지를 작성하지 않는다면 아래 내용은 대부분 관련이 없을 수 있습니다.

자체 애플리케이션에서 컴포넌트를 작성하는 경우, `app/View/Components` 및 `resources/views/components` 폴더 내의 컴포넌트는 자동으로 인식됩니다.

그러나 Blade 컴포넌트를 사용하는 패키지나, 비표준 디렉터리에 컴포넌트를 배치하는 경우에는 컴포넌트 클래스와 HTML 태그 별칭을 수동으로 등록해야 라라벨에서 해당 컴포넌트 위치를 알 수 있습니다. 일반적으로는 패키지의 서비스 프로바이더 `boot` 메서드에서 컴포넌트 등록을 수행합니다.

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

이렇게 등록한 컴포넌트는 다음과 같이 태그 별칭을 이용해 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트의 자동 로딩

또한, `componentNamespace` 메서드를 사용하여 규칙에 따라 컴포넌트 클래스를 자동으로 로드할 수도 있습니다. 예를 들어, `Nightshade` 패키지에는 `Package\Views\Components` 네임스페이스 아래에 `Calendar`와 `ColorPicker` 컴포넌트가 있을 수 있습니다:

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

이렇게 하면 `package-name::` 문법을 사용하여 벤더(공급자) 네임스페이스로 패키지 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스(PascalCase)로 변환한 뒤, 해당 컴포넌트와 연결된 클래스를 자동으로 찾아줍니다. 하위 디렉터리는 "dot" 표기법을 사용하여 지원됩니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 비슷하게, 익명 컴포넌트는 단일 파일을 통해 컴포넌트를 관리하는 방식도 제공합니다. 하지만 익명 컴포넌트는 단일 뷰 파일만 사용하며, 연결된 클래스가 없습니다. 익명 컴포넌트를 정의하려면 `resources/views/components` 디렉터리에 Blade 템플릿을 하나 추가하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 만들어 두었다면 다음과 같이 바로 렌더링할 수 있습니다:

```blade
<x-alert/>
```

만약 컴포넌트가 `components` 디렉터리 내에 더 깊은 하위 경로에 있다면, `.` 문자를 사용하여 이를 나타낼 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php`에 컴포넌트가 정의되어 있다면 다음과 같이 렌더링할 수 있습니다:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

종종 하나의 컴포넌트가 여러 Blade 템플릿으로 구성될 때, 해당 컴포넌트용 템플릿들을 하나의 디렉터리로 묶어두고 싶을 수 있습니다. 예를 들어, "아코디언" 컴포넌트가 다음과 같은 구조일 수 있습니다:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 디렉터리 구조 덕분에, 아래와 같이 아코디언 컴포넌트와 그 아이템을 함께 렌더링할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

그러나 위 예시처럼 `x-accordion`으로 아코디언 컴포넌트를 렌더링하려면, "index" 역할을 하는 아코디언 컴포넌트 템플릿을 `resources/views/components` 디렉터리 맨 위에 위치시켜야 하므로, 관련 템플릿들과 함께 한 디렉터리에 넣을 수 없었습니다.

다행히도, Blade에서는 컴포넌트 디렉터리 내부에 해당 디렉터리명과 동일한 파일을 두면 인덱스 역할을 수행할 수 있습니다. 이때에는 컴포넌트의 "루트" 요소로 해당 템플릿을 렌더링할 수 있으므로, 아코디언 예제를 같은 문법으로 유지하면서 디렉터리 구조만 다음과 같이 변경할 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 어트리뷰트

익명 컴포넌트에는 연결된 클래스가 없기 때문에, 컴포넌트로 전달되는 데이터 중 어떤 값이 변수로 할당되고 어떤 값이 [어트리뷰트 bag](#component-attributes)에 들어가는지 궁금할 수 있습니다.

이럴 때는 컴포넌트 Blade 템플릿 최상단에 `@props` 디렉티브를 사용하여 어떤 어트리뷰트를 데이터 변수로 쓸지 지정할 수 있습니다. 그 이외의 어트리뷰트는 모두 컴포넌트의 어트리뷰트 bag으로 전달됩니다. 데이터 변수 기본값을 설정하려면, 배열 키에 변수명을, 배열 값에 기본값을 지정하면 됩니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 컴포넌트를 정의했다면, 다음과 같이 렌더링할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근하기

때로는 자식 컴포넌트 내부에서 부모 컴포넌트의 데이터를 참조하고 싶을 수 있습니다. 이럴 때는 `@aware` 디렉티브를 사용할 수 있습니다. 예컨대, `<x-menu>`와 `<x-menu.item>`로 이루어진 복잡한 메뉴 컴포넌트를 만든다고 생각해 보겠습니다:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트 `<x-menu>`는 다음과 같이 구현할 수 있습니다:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

여기서 `color` prop은 부모(`<x-menu>`)에만 전달되었기 때문에 자식(`<x-menu.item>`)에서는 사용할 수 없습니다. 하지만, `@aware` 디렉티브를 사용하면 해당 값을 자식 컴포넌트에서도 쓸 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 반드시 부모 컴포넌트에 HTML 어트리뷰트로 "명시적으로" 전달된 값만 참조할 수 있습니다. 부모 컴포넌트에 전달되지 않고, 디폴트로만 존재하는 `@props` 값은 `@aware`로 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 설명한 대로 익명 컴포넌트는 보통 `resources/views/components` 디렉터리에 Blade 템플릿 파일을 추가하여 정의합니다. 하지만, 이 기본 경로 이외에 다른 경로에 위치한 익명 컴포넌트들도 Laravel에 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자에 익명 컴포넌트가 위치한 "경로"를, (선택적으로) 두 번째 인자에 네임스페이스 역할을 하는 접두어를 받을 수 있습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나의 `boot` 메서드에서 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

위처럼 접두어 없이 경로를 등록하면, 해당 경로에 있는 컴포넌트 역시 접두어 없이 Blade에서 사용할 수 있습니다. 예를 들어, 위 경로에 `panel.blade.php` 컴포넌트가 있다면 다음과 같이 렌더링할 수 있습니다:

```blade
<x-panel />
```

"네임스페이스" 역할을 하는 접두어를 두 번째 인자로 추가할 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

접두어가 지정된 경우, 컴포넌트를 렌더링할 때 해당 네임스페이스를 컴포넌트 이름의 접두사로 함께 작성해야 합니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 만들기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 애플리케이션은 다양한 페이지에서 거의 동일한 일반 레이아웃 구조를 유지합니다. 만약 각각의 뷰마다 전체 레이아웃 HTML을 매번 반복해서 작성해야 한다면, 관리와 유지보수가 매우 번거로워질 것입니다. 다행히 [Blade 컴포넌트](#components)로 레이아웃을 정의해두면, 이를 애플리케이션 전체에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어, "todo" 리스트 애플리케이션을 만든다고 해보겠습니다. 우리는 아래와 같이 레이아웃 컴포넌트를 만들 수 있습니다:

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
#### 레이아웃 컴포넌트 적용하기

`layout` 컴포넌트를 정의했다면, 이제 해당 컴포넌트를 사용하는 Blade 뷰를 만들 수 있습니다. 아래 예시에서는 task 리스트를 보여주는 아주 간단한 뷰를 정의합니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 주입된 내용은 `layout` 컴포넌트 내부에서 기본 `$slot` 변수로 전달됩니다. 참고로, 레이아웃에는 `$title` 슬롯도 인식하여 별도로 주입된 값이 있으면 사용하고, 없을 경우 기본 타이틀을 사용합니다. 태스크 목록 뷰에서 아래와 같이 커스텀 타이틀을 주입할 수 있습니다([컴포넌트 문서](#components)에서 설명한 일반적인 슬롯 문법을 참고하세요):

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

이제 레이아웃과 태스크 리스트 뷰를 정의했다면, 라우트에서 해당 뷰를 반환해주면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속으로 레이아웃 만들기

<a name="defining-a-layout"></a>
#### 레이아웃 정의하기

레이아웃은 "템플릿 상속" 방식을 통해서도 만들 수 있습니다. 이는 [컴포넌트](#components) 기능 도입 이전에 주로 사용하던 레이아웃 방식입니다.

가장 간단한 예로 살펴보겠습니다. 우선 하나의 페이지 레이아웃을 만듭니다. 대부분의 웹 애플리케이션에서 여러 페이지가 같은 레이아웃을 유지하므로, 해당 레이아웃을 하나의 Blade 뷰로 정의하면 편리합니다:

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

위 파일은 기본적인 HTML 마크업을 포함하고 있습니다. `@section`, `@yield` 디렉티브에 주목하세요. `@section`은 컨텐츠 구역을 정의하는 역할이고, `@yield`는 넘겨받은 해당 구역의 컨텐츠를 표시합니다.

이제 이 레이아웃을 상속받는 자식 페이지를 만들어 보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

자식 뷰를 정의할 때는 `@extends` Blade 디렉티브를 사용하여 어떤 레이아웃을 "상속받을지" 지정합니다. 레이아웃을 확장한 뷰는 `@section` 디렉티브를 이용해서 해당 레이아웃 내 구역에 컨텐츠를 주입할 수 있습니다. 위에서 본 것처럼, 각 구역에 넘긴 내용은 레이아웃의 `@yield` 위치에 표시됩니다:

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

이 예시에서 `sidebar` 섹션은 `@@parent` 디렉티브를 사용하여 레이아웃의 사이드바 콘텐츠를 덮어쓰지 않고, 이어 붙이고 있습니다. 뷰가 렌더링될 때 `@@parent` 부분이 레이아웃의 사이드바 내용으로 대체됩니다.

> [!NOTE]
> 위 예시와 달리 이 `sidebar` 섹션은 마지막에 `@endsection`으로 끝납니다. `@endsection`은 해당 섹션만 정의하지만, `@show`는 섹션을 정의함과 동시에 **즉시 yield**도 해줍니다.

`@yield` 디렉티브는 두 번째 파라미터로 기본값을 받을 수도 있습니다. 해당 구역이 정의되지 않았을 때 이 값이 표시됩니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때마다 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 해당 요청을 검증할 수 있도록 폼에 CSRF 토큰 hidden 필드를 항상 포함해야 합니다. 이를 위해 `@csrf` Blade 디렉티브를 사용할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없으므로, 실제로는 hidden `_method` 필드를 추가하여 이런 HTTP 메서드를 흉내내야 합니다. `@method` Blade 디렉티브가 이 hidden 필드를 만들어줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 디렉티브를 사용하면, [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 특정 속성(attribute)에서 발생했는지 빠르게 확인할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 바로 출력할 수 있습니다:

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

`@error` 디렉티브는 내부적으로 "if" 문으로 컴파일되므로, 해당 속성에 에러가 없을 때는 `@else` 디렉티브를 사용해 다른 내용을 렌더링할 수도 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

페이지에 여러 폼이 있을 때 [특정 에러 백(error bag) 이름](/docs/12.x/validation#named-error-bags)을 두 번째 파라미터로 넘겨주면 해당 error bag에서 유효성 검증 오류 메시지만 가져올 수 있습니다:

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
## 스택

Blade는 원하는 위치에 여러 뷰 혹은 레이아웃에서 `push`로 추가해 놓은 내용을 한 번에 렌더링할 수 있도록 "이름 있는 스택" 개념을 제공합니다. 이 기능은 자식 뷰에서 필요한 자바스크립트 라이브러리를 지정할 때 유용하게 사용할 수 있습니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 조건이 참일 때만 `@push` 하고 싶다면, `@pushIf` 디렉티브를 사용할 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

하나의 스택에 원하는 만큼 여러 번 push를 할 수 있습니다. 스택의 내용을 모두 렌더링하려면, 뷰에서 `@stack` 디렉티브에 스택 이름을 넘겨주면 됩니다:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 맨 앞에 내용을 추가하고 싶다면 `@prepend` 디렉티브를 사용합니다:

```blade
@push('scripts')
    This will be second...
@endpush

// 이후에...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입

`@inject` 디렉티브를 사용하면 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 가져올 수 있습니다. 첫 번째 인자는 Blade에서 사용할 변수명, 두 번째 인자는 의존성을 해결할 서비스 클래스 또는 인터페이스명을 지정합니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

때때로, Blade 템플릿 코드 문자열을 바로 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. `render` 메서드는 Blade 템플릿 문자열과, 템플릿에 바인딩할 데이터가 담긴 배열(선택 사항)을 인자로 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 렌더링할 때 내부적으로 이를 `storage/framework/views` 디렉터리에 저장합니다. 렌더링 후 임시 파일을 바로 삭제하고 싶다면, `deleteCachedView` 옵션을 같이 전달할 수 있습니다:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트(조각) 렌더링

[TUro](https://turbo.hotwired.dev/), [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, HTTP 응답에서 Blade 템플릿의 일부만 반환하고 싶은 경우가 있습니다. 이럴 때 Blade "프래그먼트" 기능을 사용할 수 있습니다. 템플릿의 일부 코드를 `@fragment`, `@endfragment` 디렉티브로 감싸 작성하세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

그리고 해당 템플릿이 사용된 뷰를 렌더링할 때, 반환하고 싶은 프래그먼트 이름을 `fragment` 메서드에 인자로 넘기면 해당 프래그먼트만 HTTP 응답에 포함됩니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 어떤 조건이 참일 때만 프래그먼트를 반환하고, 그렇지 않으면 전체 뷰가 반환됩니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`와 `fragmentsIf` 메서드를 사용하면 여러 개의 프래그먼트를 한꺼번에 반환할 수 있습니다. 반환된 프래그먼트들은 모두 연결되어 하나의 응답으로 전달됩니다:

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

Blade에서는 자신만의 커스텀 디렉티브를 `directive` 메서드로 정의할 수 있습니다. Blade 컴파일러가 커스텀 디렉티브를 찾으면, 그 디렉티브에 포함된 표현식을 콜백에 전달하여 처리하게 됩니다.

아래 예시는 `@datetime($var)` 디렉티브를 만들어서, 주어진 `$var`(이 예시에서는 DateTime 인스턴스)를 포맷팅하도록 만듭니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

보시다시피, 해당 디렉티브에 넘겨진 어떤 표현식이든 그 위에 `format` 메서드를 체이닝해서 결과를 출력하게 됩니다. 즉, 이 디렉티브로 컴파일된 결과 PHP 코드는 아래와 같습니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 변경한 뒤에는 캐싱된 모든 Blade 뷰 파일을 삭제해야 합니다. 캐싱된 Blade 뷰 파일은 `view:clear` Artisan 명령어로 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러

Blade 템플릿에서 객체를 `{{ ... }}`로 출력("echo")하면, 그 객체의 `__toString`(PHP 내장 "매직 메서드" 중 하나) 메서드가 호출됩니다. 하지만, 때로는 서드파티 라이브러리에서 제공하는 클래스처럼 `__toString`을 직접 제어할 수 없는 경우가 있습니다.

이럴 때 Blade에서는 해당 객체 타입 전용 커스텀 에코 핸들러를 등록할 수 있도록 `stringable` 메서드를 제공합니다. 이 메서드는 클로저 함수를 인자로 받으며, 렌더링할 객체 타입을 타입힌트로 지정합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 호출하게 됩니다:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

이처럼 커스텀 핸들러가 등록된 뒤에는, Blade 템플릿에서 객체를 아래와 같이 간단히 출력할 수 있습니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문 정의하기

간단한 커스텀 조건문을 만들고 싶을 때 직접 디렉티브를 프로그래밍하기에는 다소 복잡합니다. 이런 경우를 위해 Blade는 `Blade::if` 메서드를 제공하며, 이를 통해 클로저로 커스텀 조건문 디렉티브를 빠르게 만들 수 있습니다. 예를 들어, 애플리케이션의 기본 "디스크"가 어떤 값인지 판단할 커스텀 조건문을 만들어 보겠습니다. 보통은 `AppServiceProvider`의 `boot` 메서드에서 아래와 같이 정의합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

커스텀 조건문이 정의되면, 다음과 같이 Blade 템플릿에서 바로 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크를 사용 중일 때... -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크를 사용 중일 때... -->
@else
    <!-- 애플리케이션이 다른 디스크를 사용 중일 때... -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크를 사용하지 않을 때... -->
@enddisk
```