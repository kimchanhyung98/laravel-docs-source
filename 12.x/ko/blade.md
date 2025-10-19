# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Blade와 Livewire로 기능 확장](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성값](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 빌드](#building-layouts)
    - [컴포넌트를 활용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 활용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 안에서 일반 PHP 코드를 자유롭게 사용할 수 있습니다. 실제로 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어, 수정 시까지 캐시에 저장되므로, Blade는 애플리케이션에 거의 부하를 추가하지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며, 주로 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론 [뷰 문서](/docs/12.x/views)에서 설명한 것처럼, `view` 헬퍼의 두 번째 인자를 통해 Blade 뷰로 데이터를 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Blade와 Livewire로 기능 확장 (Supercharging Blade With Livewire)

Blade 템플릿을 한 단계 더 발전시키고, 동적인 인터페이스를 손쉽게 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire는 Blade 컴포넌트에 React나 Vue 같은 프런트엔드 프레임워크로만 가능했던 동적 기능을 손쉽게 추가해 주는 라이브러리로, 복잡한 빌드 과정 없이도 현대적인 반응형 프론트엔드를 구현할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 출력 (Displaying Data)

Blade 뷰로 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있을 때:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

아래와 같이 `name` 변수를 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력문은 XSS(교차 사이트 스크립팅) 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 출력됩니다.

뷰로 전달된 변수의 내용만 출력하는 데 한정되지 않습니다. 출력문에 원하는 PHP 함수를 자유롭게 사용할 수 있습니다. 실제로 Blade 출력문 안에는 어떤 PHP 코드도 사용할 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로 Blade (및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 만약 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding`을 호출하면 됩니다.

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
#### 이스케이프 처리되지 않은 데이터 출력

기본적으로 Blade의 `{{ }}` 구문은 PHP의 `htmlspecialchars` 함수로 데이터가 자동 이스케이프되어 안전하게 출력됩니다. 만약 이스케이프하지 않고 원본 데이터를 출력해야 한다면, 다음과 같은 문법을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 이스케이프 없이 출력할 때는 매우 주의해야 합니다. 보통 사용자 데이터에는 이중 중괄호(`{{ }}`)로 감싸진 안전한 구문을 사용하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크 (Blade and JavaScript Frameworks)

많은 JavaScript 프레임워크도 중괄호(`{}`)를 사용해 화면에 값을 출력합니다. 이런 경우, Blade에서 해당 부분을 건드리지 않게 하려면 `@` 기호를 중괄호 앞에 붙입니다.

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade에서 삭제되며, `{{ name }}` 표현식은 그대로 남아 JavaScript 프레임워크가 렌더링할 수 있도록 합니다.

또한, `@` 기호로 Blade 디렉티브 자체를 이스케이프할 수도 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 출력

종종 JavaScript 변수 초기화를 위해 배열을 JSON 형태로 뷰에 전달해야 할 때가 있습니다.

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. 이 메서드는 JSON이 HTML 안의 따옴표에서 올바르게 이스케이프되도록 처리하며, JavaScript의 `JSON.parse` 구문으로 반환되어 실제 객체로 사용할 수 있습니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 프로젝트 스켈레톤에서는 `Js` facade가 포함되어 있으므로, 더 간편하게 사용할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 출력하는 데만 사용하세요. Blade의 템플릿 파싱은 정규식 기반이므로, 복잡한 표현식을 전달하면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 많은 부분에서 JavaScript 변수 출력이 필요하다면, `@verbatim` 디렉티브로 해당 HTML 블록을 감싸 각 Blade 출력문에 매번 `@` 기호를 붙이지 않아도 됩니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브 (Blade Directives)

템플릿 상속 및 데이터 출력 외에도, Blade는 PHP의 조건문과 반복문을 위한 간편 단축 구문을 제공합니다. 이들 디렉티브는 PHP 본연의 형태와 유사하며, 읽기 쉽고 간결한 구문으로 PHP 제어 구조를 다룰 수 있습니다.

<a name="if-statements"></a>
### If 문 (If Statements)

`@if`, `@elseif`, `@else`, `@endif` 디렉티브로 조건문을 작성할 수 있습니다. 이들은 PHP의 조건문과 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 `@unless` 디렉티브도 제공됩니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

여기에 더해, `@isset`과 `@empty` 디렉티브로 PHP의 해당 함수 역할을 간단히 대신할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있습니다"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브로, 현재 사용자가 [인증](https://laravel.com/docs/12.x/authentication)에 성공했는지(또는 게스트인지) 빠르게 확인할 수 있습니다.

```blade
@auth
    // 인증된 사용자입니다...
@endauth

@guest
    // 인증되지 않은 사용자입니다...
@endguest
```

필요하다면, 인증에 사용할 가드를 지정할 수도 있습니다.

```blade
@auth('admin')
    // 인증된 사용자입니다...
@endauth

@guest('admin')
    // 인증되지 않은 사용자입니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경 디렉티브

`@production` 디렉티브로 현재 애플리케이션이 운영 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // 운영 환경에서만 보일 내용...
@endproduction
```

`@env` 디렉티브로 특정 환경을 지정할 수도 있습니다.

```blade
@env('staging')
    // "staging" 환경에서 실행됩니다...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서 실행됩니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션 디렉티브

템플릿 상속에서 특정 섹션에 내용이 존재하는지 `@hasSection`으로 확인할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

반대로 해당 섹션에 내용이 없을 때는 `@sectionMissing`을 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 디렉티브

`@session` 디렉티브로 [세션](/docs/12.x/session) 값 존재 여부를 간단히 확인할 수 있습니다. 값이 존재한다면, 디렉티브 블록 내에서 `$value` 변수로 해당 값을 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트 디렉티브

`@context` 디렉티브로 [컨텍스트](/docs/12.x/context) 값의 존재 여부를 확인할 수 있습니다. 값이 존재하면 블록 내에서 `$value`로 출력 가능합니다.

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문 (Switch Statements)

Switch 문은 `@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용해 작성할 수 있습니다.

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
### 반복문 (Loops)

조건문과 마찬가지로, Blade에서는 PHP의 반복문 구조를 위한 간단한 디렉티브가 제공됩니다. 이들 디렉티브는 PHP 본연의 반복문과 동일하게 동작합니다.

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
> `foreach` 반복문에서는 [loop 변수](#the-loop-variable)를 통해 첫 번째/마지막 반복 등 유용한 정보를 Reference 할 수 있습니다.

반복문에서는 `@continue`와 `@break` 디렉티브로 현재 반복을 건너뛰거나 종료할 수 있습니다.

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

조건식을 디렉티브 선언문에 직접 전달할 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수 (The Loop Variable)

`foreach` 반복문 안에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수로 현재 반복 인덱스, 첫 번째/마지막 반복 여부 등을 확인할 수 있습니다.

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

중첩 반복문에서 상위 반복문의 `$loop` 변수는 `parent` 속성으로 접근합니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에서 참조할 수 있는 속성은 다음과 같습니다:

<div class="overflow-auto">

| 속성                | 설명                                               |
| ------------------- | ------------------------------------------------- |
| `$loop->index`      | 현재 반복의 인덱스(0부터 시작)                    |
| `$loop->iteration`  | 현재 반복 횟수(1부터 시작)                        |
| `$loop->remaining`  | 남은 반복 수                                      |
| `$loop->count`      | 전체 컬렉션 요소 개수                             |
| `$loop->first`      | 첫 번째 반복 여부                                 |
| `$loop->last`       | 마지막 반복 여부                                  |
| `$loop->even`       | 짝수번째 반복 여부                                |
| `$loop->odd`        | 홀수번째 반복 여부                                |
| `$loop->depth`      | 현재 반복의 중첩 레벨                             |
| `$loop->parent`     | 중첩 반복일 때, 상위 루프의 `$loop` 변수         |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 디렉티브를 사용하면 CSS 클래스 문자열을 조건부로 컴파일할 수 있습니다. 배열의 키에 클래스를, 값에 조건식을 지정하면 조건이 참일 때 해당 클래스가 적용됩니다. 숫자형 키는 무조건 클래스에 포함됩니다.

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

마찬가지로 `@style` 디렉티브를 사용해 인라인 스타일도 조건부로 적용 가능합니다.

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
### 추가 속성 (Additional Attributes)

체크박스와 같이 특정 HTML 요소 속성에 조건이 필요할 때, 편리하게 사용할 수 있는 디렉티브가 제공됩니다.

`@checked`는 조건이 참이면 `checked` 속성을 출력합니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

`@selected`는 select 옵션에서 선택 여부를 간편하게 처리합니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled`는 요소에 `disabled` 속성을, `@readonly`는 `readonly`, `@required`는 `required` 속성을 조건부로 출력합니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### 서브뷰 포함 (Including Subviews)

> [!NOTE]
> `@include` 디렉티브도 쓸 수 있으나, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 다양한 장점을 제공합니다.

`@include` 디렉티브로 한 Blade 뷰에서 다른 뷰(서브뷰)를 손쉽게 포함할 수 있습니다. 부모 뷰에서 사용할 수 있는 모든 변수가 자식(포함된) 뷰에서 그대로 사용 가능합니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

물론, 추가로 데이터를 넘기고 싶다면 배열 형태로 전달할 수 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

포함하려는 뷰가 존재하지 않을 수도 있는 경우에는 `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

불리언 조건에 따라 뷰를 포함할 경우엔 `@includeWhen`, `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 첫 번째로 존재하는 뷰만 포함하고 싶을 때는 `includeFirst` 디렉티브를 사용합니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수를 사용하면 캐시된 컴파일된 뷰의 경로를 참조하게 되므로 사용을 피하세요.

<a name="rendering-views-for-collections"></a>
#### 컬렉션의 각 요소를 위한 뷰 렌더링

Blade의 `@each` 디렉티브를 활용하면, 반복문과 포함을 한 줄로 간편하게 작성할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 반복 출력할 뷰, 두 번째는 반복할 배열 또는 컬렉션, 세 번째는 포함 뷰 내에서 단일 요소에 접근할 변수명입니다. 반복의 인덱스는 `key` 변수로 사용됩니다.

배열이 비어 있을 경우 출력할 대체 뷰를 네 번째 인자로 전달할 수 있습니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에서 부모의 변수가 필요하다면 `@foreach`와 `@include` 조합을 사용해야 합니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브로 템플릿 내 특정 블록을 렌더링 사이클당 한 번만 평가할 수 있습니다. 예를 들어, 반복문 안에서 [스택](#stacks) 기능과 결합해 자바스크립트 코드를 처음 한 번만 헤더에 추가하고 싶을 때 유용합니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

대개 `@once`는 `@push`나 `@prepend`와 함께 사용하므로, 이를 위해 `@pushOnce`, `@prependOnce` 디렉티브도 제공합니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

서로 다른 Blade 템플릿에서 동일한 콘텐츠를 중복해서 푸시한다면, 두 번째 인자로 고유 식별자를 전달해 한 번만 출력되도록 할 수 있습니다.

```blade
<!-- pie-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce

<!-- line-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

필요에 따라 Blade 뷰 내에 PHP 코드를 직접 사용할 수 있습니다. `@php` 디렉티브로 일반 PHP 블록을 실행할 수도 있고,

```blade
@php
    $counter = 1;
@endphp
```

클래스 임포트만 진행할 땐 `@use` 디렉티브를 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

두 번째 인자로 별칭을 지정할 수도 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

동일한 네임스페이스 내 여러 클래스 임포트는 중괄호를 사용할 수 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

`function`, `const` 수식어로 함수 및 상수도 임포트가 가능합니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수, 상수에도 별칭 가능합니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수 또는 const 그룹도 지원하여, 여러 심볼을 한 번에 임포트할 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석 (Comments)

Blade에서는 주석을 사용할 수 있습니다. Blade 주석은 일반 HTML 주석과 달리, 렌더링된 HTML 소스에는 표시되지 않습니다.

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, include와 비슷한 역할과 이점이 있습니다. 일부 개발자들은 컴포넌트와 슬롯의 개념이 더 이해하기 쉽다고 느낄 수 있습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트 두 가지 방식이 있습니다.

클래스 기반 컴포넌트를 만들려면, `make:component` Artisan 명령어를 사용합니다. 단순한 `Alert` 컴포넌트를 예로 들어 보겠습니다. 다음 명령어로 `app/View/Components` 디렉터리에 컴포넌트가 생성됩니다.

```shell
php artisan make:component Alert
```

이 명령어는 컴포넌트의 뷰 템플릿도 `resources/views/components` 디렉터리에 생성합니다. 자신의 애플리케이션에서 작성하는 컴포넌트는 위 디렉터리 내에서 자동으로 인식되므로, 별도의 등록 과정이 필요 없습니다.

하위 디렉터리에 컴포넌트를 생성할 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms`에 `Input` 컴포넌트를, 뷰는 `resources/views/components/forms`에 생성합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자신의 애플리케이션에서 작성한 컴포넌트는 자동으로 인식됩니다.

하지만, 패키지 형태로 Blade 컴포넌트를 배포할 경우, 컴포넌트 클래스와 HTML 태그 별칭을 수동 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 아래처럼 등록합니다.

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

이후엔 아래처럼 태그 별칭으로 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드로 네임스페이스 기반 자동 로딩도 지원합니다. 예를 들어, `Nightshade`라는 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있다면 다음과 같이 구성할 수 있습니다.

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

이제 아래와 같이 벤더 네임스페이스를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스 처리해서 클래스와 자동 매칭합니다. "dot" 표기법으로 하위 디렉터리도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링 (Rendering Components)

컴포넌트는 Blade 템플릿에서 `x-`로 시작하는 태그를 사용해 표시할 수 있습니다. 컴포넌트 클래스명이 케밥 케이스로 매핑됩니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉터리 하위에 중첩되었다면, `.` 문자로 디렉터리 계층을 표현할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php` 에 위치한 컴포넌트는 다음과 같이 렌더링합니다.

```blade
<x-inputs.button/>
```

컴포넌트의 렌더 여부를 동적으로 결정하려면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의하세요. false를 반환하면 컴포넌트가 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트 (Index Components)

컴포넌트 그룹의 일부로 여러 컴포넌트를 만들 때, 관련 컴포넌트들을 하나의 디렉터리로 묶을 수 있습니다. 예시 구조를 보겠습니다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 컴포넌트 파일명이 디렉터리명과 같을 때(이 예시에서 `Card`), Laravel은 중복된 이름 없이 아래처럼 렌더할 수 있다고 간주합니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달 (Passing Data to Components)

컴포넌트에 값을 전달할 때는 HTML 속성 형태로 지정합니다. 간단한 문자열 값은 그대로 쓸 수 있고, 변수나 PHP 표현식은 `:` 접두어를 붙여 사용합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 사용될 데이터를 모두 정의해야 합니다. 컴포넌트의 각 public 속성은 자동으로 뷰에서도 사용할 수 있습니다. `render` 메서드에서 별도로 데이터 전달하는 작업은 필요하지 않습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링되면, public 변수명을 그대로 출력해 사용할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 표기법(Casing)

컴포넌트 생성자 인수는 `camelCase`로 작성하되, HTML 속성 참조 시에는 `kebab-case`로 변환해서 사용해야 합니다. 예시:

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

Blade에서의 사용

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성 문법

속성을 컴포넌트에 전달할 때, 변수명과 속성명이 같을 땐 단축 문법을 사용할 수 있습니다.

```blade
{{-- 단축 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JavaScript 프레임워크는 `:`로 시작하는 속성을 사용합니다. 이때 `::` 이중 콜론을 붙여 Blade가 PHP 식으로 해석하지 않도록 할 수 있습니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

결과:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

public 변수 외에도, public 메서드는 뷰에서 변수처럼 호출할 수 있습니다. 예를 들어 다음과 같이 메서드를 정의하면,

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

템플릿에서 이렇게 쓸 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 클래스 내에서 속성 및 슬롯 접근

컴포넌트 내에서 이름, 속성, 슬롯 정보를 활용하려면 `render` 메서드에서 클로저를 반환하세요.

```php
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

클로저는 `$data` 배열을 인자로 받아 해당 정보에 접근할 수 있습니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열 요소를 Blade 문자열에 직접 삽입하면 악의적인 속성값을 통한 원격 코드 실행 취약점이 생길 수 있으니 절대로 직접 삽입해 사용하지 마세요.

`componentName`은 태그의 `x-` 뒤 이름 (`<x-alert />`의 경우 `alert`)입니다. `attributes`는 모든 전달된 HTML 속성이며, `slot`은 컴포넌트 슬롯 내용을 담은 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저가 반환한 문자열이 실제 뷰명과 일치하면 뷰를, 아니라면 인라인 Blade 뷰로 평가·렌더링합니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트에서 Laravel의 [서비스 컨테이너](/docs/12.x/container)에서 의존성을 주입하려면, 데이터 속성보다 먼저 선언하면 됩니다.

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성 / 메서드 비공개 처리

특정 public 메서드나 속성을 컴포넌트 뷰에서 노출하고 싶지 않을 때는, 컴포넌트의 `$except` 배열 속성에 이름을 추가하세요.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 뷰에서 노출되지 않아야 할 속성 / 메서드 목록
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

앞서 데이터 속성 전달을 살펴보았지만, 경우에 따라 `class`와 같은 추가 HTML 속성을 동적으로 지정하고 싶을 수 있습니다. 이런 경우, 데이터 속성이 아닌 나머지 속성들은 자동으로 `$attributes` "속성 백"에 저장되고, 컴포넌트 뷰에서는 `$attributes` 변수로 출력할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트에서:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내에서 `@env` 등의 디렉티브를 사용할 수 없습니다. (예: `<x-alert :live="@env('production')"/>`는 정상 컴파일되지 않습니다.)

<a name="default-merged-attributes"></a>
#### 속성 기본값 / 병합

속성에 기본값을 지정하거나, 특정 속성(특히 CSS class 등)에 값을 병합하려면, 속성 백의 `merge` 메서드를 사용하세요. 대표적으로 CSS 클래스를 지정할 때 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

사용 예시:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

렌더링 결과:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 클래스 조건부 병합

특정 조건을 만족할 때 클래스 추가가 필요하다면, `class` 메서드를 사용할 수 있습니다. 배열의 키는 클래스명, 값은 조건식입니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

기타 속성 병합도 가능하며, `class` 뒤에 `merge` 체이닝 사용이 가능합니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 다른 HTML 요소에 조건부 클래스를 적용해야 하되, 속성 백의 병합이 불필요하다면 [@class 디렉티브](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스 외 속성 병합

`class` 외의 속성을 병합할 때는, `merge`로 지정한 값은 "기본값"이 되며, 속성 백에 주입된 값이 있으면 해당 값이 덮어써집니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

사용 예시:

```blade
<x-button type="submit">
    Submit
</x-button>
```

렌더링 결과:

```blade
<button type="submit">
    Submit
</button>
```

특정 속성에서도 기본값과 추가값을 결합하고 싶다면, `prepends` 메서드를 사용하세요. (아래 예시에서 `data-controller`가 항상 `profile-controller`로 시작)

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 추출

`filter` 메서드로 속성을 필터링할 수 있습니다. 클로저가 true를 반환하면 속성이 남습니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

키가 지정 문자열로 시작하는 속성만 추출하려면 `whereStartsWith`를, 반대로 시작하지 않는 속성만 남기려면 `whereDoesntStartWith`를 사용합니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

속성 백에서 첫 번째 속성만 추출하려면 `first` 메서드를 사용합니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성의 존재 여부는 `has`로, 여러 속성의 존재 여부는 배열로 전달해 확인할 수 있습니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif

@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny`는 여러 속성 중 하나라도 존재하는지 확인합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성의 값을 추출하려면 `get`을 사용하세요.

```blade
{{ $attributes->get('class') }}
```

여러 속성만 추릴 땐 `only`, 제외할 때는 `except`를 사용합니다.

```blade
{{ $attributes->only(['class']) }}
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade 내장 처리에 필요한 일부 키워드는 컴포넌트 public 속성명이나 메서드명으로 사용할 수 없습니다:

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
### 슬롯 (Slots)

컴포넌트에 "슬롯"을 활용해 추가 콘텐츠를 전달할 수 있습니다. 슬롯 내용은 `$slot` 변수로 렌더링합니다. 예시로, `alert` 컴포넌트의 다음 마크업을 보겠습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯에는 다음처럼 내용을 주입할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 개의 슬롯이 필요한 경우도 있습니다. 예를 들어, "title" 슬롯을 추가하려면 다음처럼 컴포넌트를 수정합니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이름 있는 슬롯 내용은 `x-slot` 태그로 지정할 수 있습니다. 명시적으로 지정하지 않은 내용을 `$slot`으로 받습니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯 내용이 비어있는지 확인하려면 `isEmpty` 메서드를 호출할 수 있습니다.

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

HTML 주석이 아닌 실제 콘텐츠가 있는지 확인할 때는 `hasActualContent`를 사용합니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯(Scoped Slots)

Vue 등 자바스크립트 프레임워크에서 제공하는 "스코프 슬롯"과 유사하게, Blade 컴포넌트 내 public 메서드/속성을 슬롯에서 사용할 수 있습니다. 슬롯 내에서는 `$component` 변수로 컴포넌트에 접근합니다.

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

슬롯에도 컴포넌트 속성과 동일하게 [추가 속성](#component-attributes)을 지정하여 CSS class 등 사용이 가능합니다.

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

슬롯 속성과 상호작용하려면, 슬롯 변수의 `attributes` 프로퍼티를 통해 접근합니다. 관련 정보는 [컴포넌트 속성 문서](#component-attributes)를 참고하세요.

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
### 인라인 컴포넌트 뷰 (Inline Component Views)

작은 컴포넌트의 경우, 뷰 파일과 컴포넌트 클래스를 따로 두는 게 오히려 불편할 수 있습니다. 이럴 때는 `render` 메서드에서 직접 마크업을 반환할 수 있습니다.

```php
/**
 * Get the view / contents that represent the component.
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

인라인 뷰를 렌더링하는 컴포넌트를 만들려면 `make:component` 명령어 실행 시 `--inline` 옵션을 추가하세요.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트 (Dynamic Components)

런타임에 렌더링할 컴포넌트 종류를 동적으로 지정해야 한다면, Laravel 내장 `dynamic-component` 컴포넌트를 사용하면 됩니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록 (Manually Registering Components)

> [!WARNING]
> 아래 문서는 Laravel 패키지 제작자 등, 뷰 컴포넌트가 포함된 패키지를 개발할 때 주로 필요한 정보입니다. 일반적인 애플리케이션 개발자라면 생략해도 무방합니다.

애플리케이션용 컴포넌트는 자동 인식되지만, 패키지 혹은 비정형 디렉터리에 컴포넌트를 둘 경우, 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 패키지의 서비스 프로바이더의 `boot` 메서드에서 아래와 같이 등록하세요.

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

등록 후 HTML 태그 별칭으로 컴포넌트를 사용할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 오토로딩

또는 `componentNamespace`를 사용하면 네임스페이스 규칙 기반으로 오토로딩할 수 있습니다. 아래 예시 참조:

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

이제 아래처럼 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

클래스는 파스칼 케이스 변환과 "dot" 표기법으로 자동 매칭됩니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 비슷하지만, 익명 컴포넌트는 컴포넌트 클래스 없이 단일 뷰 파일로 관리합니다. 단순히 Blade 템플릿을 `resources/views/components`에 두면, 클래스를 따로 생성하지 않고도 사용할 수 있습니다.

예) `resources/views/components/alert.blade.php` 존재 → 아래처럼 렌더링

```blade
<x-alert/>
```

디렉터리 하위에 중첩된 컴포넌트는 `.` 표기 사용

```blade
<x-inputs.button/>
```

Artisan으로 익명 컴포넌트 생성은 `--view` 플래그를 사용

```shell
php artisan make:component forms.input --view
```

위 명령어는 `resources/views/components/forms/input.blade.php` 파일을 생성합니다. `<x-forms.input />` 으로 사용할 수 있습니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트 (Anonymous Index Components)

큰 컴포넌트는 여러 Blade 템플릿으로 구성할 수 있으므로, 하나의 디렉터리로 묶는 경우가 있습니다. 예를 들어 아래 구조:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

아래처럼 사용할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

여기서 인덱스 역할의 템플릿이 항상 상위 디렉터리에 위치해야 하는 번거로움이 있지만, Blade는 디렉터리 자체 이름을 가진 파일이 있으면 해당 디렉터리 하위에서도 “루트” 컴포넌트로 인식합니다.

즉, 아래처럼 구조를 갖춰도,

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

동일한 구문으로 사용할 수 있습니다.

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성값 (Data Properties / Attributes)

익명 컴포넌트는 클래스가 없기 때문에, 어떤 속성이 변수(프로퍼티)로 전달되어야 하는지, 어떤 속성이 attribute bag으로 전달되어야 하는지 명시할 필요가 있습니다.

`@props` 지시자를 템플릿 상단에 선언해 변수로 사용할 속성을 지정하세요. 배열의 키는 속성명, 값은 기본값입니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이제 아래와 같이 컴포넌트를 사용할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근 (Accessing Parent Data)

하위 컴포넌트에서 부모 컴포넌트의 데이터를 활용하고 싶다면 `@aware` 지시자를 사용할 수 있습니다. 예를 들어, 복잡한 메뉴 컴포넌트에서 부모의 색상 속성을 자식에서 사용하고 싶다면,

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

자식에서 `@aware`를 사용하여 부모의 값을 받아올 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware`는 부모에서 명시적으로 전달한 HTML 속성만 사용할 수 있습니다. 부모에서 전달하지 않은 기본값(`@props`의 값)은 자식에서 사용할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로 (Anonymous Component Paths)

기본적으로 익명 컴포넌트는 `resources/views/components`에 두지만, 필요에 따라 다른 경로를 추가 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 경로(1번째 인자)와 네임스페이스 접두사(2번째 인자, 생략 가능)를 받아 익명 컴포넌트의 경로와 네임스페이스를 지정합니다. 주로 [서비스 프로바이더](/docs/12.x/providers)에서 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

접두사가 없을 경우, 컴포넌트 이름 그대로 사용

```blade
<x-panel />
```

접두사를 포함해 네임스페이스로 등록한 경우:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

사용 예시

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 빌드 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 활용한 레이아웃 (Layouts Using Components)

대부분의 웹 애플리케이션은 여러 페이지에서 공통 레이아웃을 사용합니다. 각 뷰마다 동일한 레이아웃 코드를 반복하는 것은 비효율적입니다. [Blade 컴포넌트](#components)를 활용하면, 레이아웃을 하나의 컴포넌트로 정의해 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "todo" 리스트 앱에서 다음과 같이 레이아웃 컴포넌트를 만들 수 있습니다.

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

이제 위에서 만든 `layout` 컴포넌트를 활용하는 뷰를 만들어 보겠습니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 주입하는 내용은 컴포넌트 뷰의 기본 `$slot` 변수로 전달됩니다. `$title` 슬롯에 값을 전달하지 않아도 기본값이 적용됩니다. 커스텀 제목을 주입하려면 명시적인 슬롯 문법을 사용합니다.

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

이제 라우트에서 아래처럼 뷰를 반환하면 완성됩니다.

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 활용한 레이아웃 (Layouts Using Template Inheritance)

<a name="defining-a-layout"></a>
#### 레이아웃 정의

"템플릿 상속"을 통해 레이아웃을 작성할 수도 있습니다. [컴포넌트](#components)가 도입되기 전의 주된 방법입니다.

먼저 레이아웃 뷰의 예를 살펴봅시다.

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

여기서는 `@section`과 `@yield`를 함께 사용합니다. `@section`은 섹션 시작, `@yield`는 해당 섹션의 값을 출력합니다.

이제 해당 레이아웃을 상속받는 하위 페이지를 정의해보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

하위 뷰에서는 `@extends`로 상속할 레이아웃을 지정하고, `@section`으로 콘텐츠를 주입합니다. 해당 섹션 내용은 상위 뷰의 `@yield` 위치에 출력됩니다.

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

예제처럼 `@@parent` 디렉티브로, 부모(/상위)에서 정의한 내용을 그대로 두면서 추가로 내용을 덧붙일 수 있습니다.

> [!NOTE]
> 이전 예제와 달리, 이 `sidebar` 섹션은 `@endsection`으로 끝납니다. `@endsection`은 "섹션 정의만" 하고, `@show`는 "정의 후 바로 출력"합니다.

`@yield`는 두 번째 인자로 기본값을 받으므로, 해당 섹션이 정의되지 않은 경우 기본값을 출력하게 할 수 있습니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드 (CSRF Field)

HTML 폼을 정의할 때는 반드시 CSRF 토큰 필드를 포함해야 [CSRF 보호 미들웨어](/docs/12.x/csrf)가 요청을 올바르게 인증할 수 있습니다. `@csrf` 디렉티브로 손쉽게 토큰 필드를 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드 (Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 직접 전송할 수 없으므로, 숨은 필드로 HTTP 메서드 값을 지정해야 합니다. `@method` 디렉티브로 쉽게 처리합니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 오류 (Validation Errors)

`@error` 디렉티브로 [유효성 검증 오류 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)를 빠르게 확인할 수 있습니다. 블록 내에서 `$message` 변수를 출력해 해당 오류 메시지를 표시할 수 있습니다.

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

`@error`는 if 문처럼 동작하므로, `@else`로 오류가 없을 때 다른 내용을 출력할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 개의 폼이 있고, 특정 에러백의 오류 메시지만 출력하려면 두 번째 인자로 에러백 이름을 전달하세요.

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
## 스택 (Stacks)

Blade의 스택 기능을 이용하면, 여러 뷰나 레이아웃에서 명명된 스택에 내용을 누적하고 원하는 위치에 출력할 수 있습니다. 이는 각 자식 뷰별로 필요한 JavaScript 라이브러리 등을 스택에 모아 한 번에 출력하는 데 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

불리언 조건에 따라 내용 푸시가 필요하다면, `@pushIf` 디렉티브를 사용하세요.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에는 여러 번 푸시해도 되고, 해당 스택 내용 전체를 출력할 때는 `@stack` 디렉티브 사용

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택 앞에 내용을 추가하려면 `@prepend` 디렉티브 사용

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
## 서비스 주입 (Service Injection)

`@inject` 디렉티브로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 뷰에 주입할 수 있습니다. 첫 번째 인자는 변수명, 두 번째 인자는 클래스 또는 인터페이스 이름입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링 (Rendering Inline Blade Templates)

원시 Blade 템플릿 문자열을 HTML로 변환해야 하는 경우, `Blade` facade의 `render` 메서드를 사용하세요. 첫 번째 인자로 Blade 템플릿 문자열, 두 번째 인자로 템플릿에 전달할 데이터 배열을 받습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉터리에 임시 파일로 저장합니다. 렌더링 후 임시 파일을 삭제하려면, `deleteCachedView` 인자를 true로 전달하면 됩니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링 (Rendering Blade Fragments)

[Turbo](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프런트엔드 프레임워크를 사용할 때, HTTP 응답으로 Blade 템플릿의 일부만 반환해야 하는 경우가 있습니다. Blade "프래그먼트" 기능으로 이 부분만 선택적으로 반환할 수 있습니다. 렌더링할 영역을 `@fragment`, `@endfragment`로 감쌉니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

그리고 뷰를 반환할 때 `fragment` 메서드로 원하는 프래그먼트만 응답에 포함시킵니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf`로 조건에 따라 프래그먼트를 반환, 아니면 전체 뷰 반환도 가능합니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트를 동시에 반환하려면 `fragments`, `fragmentsIf` 메서드를 사용합니다. 이 경우 프래그먼트가 순서대로 이어서 응답됩니다.

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
## Blade 확장 (Extending Blade)

`directive` 메서드로 Blade의 커스텀 디렉티브를 직접 정의할 수 있습니다. Blade 컴파일러가 이 디렉티브를 만나면, 해당 콜백에 전달된 식(expression)을 활용해 원하는 동작을 추가할 수 있습니다.

다음 예시는 `@datetime($var)` 디렉티브를 만들고, 전달받은 `DateTime` 인스턴스를 원하는 형식으로 포맷하여 출력합니다.

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

실제로는 다음과 같은 PHP 코드로 변환되어 실행됩니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 경우, 캐시된 Blade 뷰 파일을 모두 삭제해야 합니다. `view:clear` Artisan 명령어로 캐시를 삭제하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 Echo 핸들러 (Custom Echo Handlers)

Blade에서 객체를 "echo" 할 때, PHP의 `__toString` 메서드가 자동 호출됩니다. 하지만 외부 라이브러리 등에서 이 메서드를 직접 제어할 수 없는 경우가 있습니다.

이럴 때는 Blade의 `stringable` 메서드로 특정 타입의 객체에 대한 커스텀 핸들러를 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 사용합니다.

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

등록 후에는 Blade에서 해당 객체를 단순히 출력해도 커스텀 핸들러가 적용됩니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문 (Custom If Statements)

간단한 커스텀 조건문이 필요하다면, 직접 디렉티브를 만드는 것보다 `Blade::if` 메서드로 커스텀 조건문 디렉티브를 정의하는 것이 편리합니다. 예를 들어, 애플리케이션의 기본 "디스크" 설정값을 체크하는 커스텀 조건문을 만들어보겠습니다.

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

이제 아래처럼 템플릿에서 사용할 수 있습니다.

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크를 사용 중일 때... -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크를 사용 중일 때... -->
@else
    <!-- 애플리케이션이 다른 디스크를 사용 중일 때... -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크가 아닐 때... -->
@enddisk
```
