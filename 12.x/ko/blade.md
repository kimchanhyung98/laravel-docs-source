# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 기능 강화하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔터티 인코딩](#html-entity-encoding)
    - [Blade와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시어](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯(Slot)](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 프로퍼티 / 속성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축하기](#building-layouts)
    - [컴포넌트로 레이아웃 만들기](#layouts-using-components)
    - [템플릿 상속으로 레이아웃 만들기](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택(Stacks)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 내장된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 안에서 순수 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되며, 수정될 때까지 캐시에 저장됩니다. 즉, Blade는 애플리케이션의 성능에 거의 영향을 주지 않습니다. Blade 템플릿 파일 확장자는 `.blade.php`이며 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트 또는 컨트롤러에서 전역 `view` 헬퍼를 사용하여 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views)에서 설명했듯 `view` 헬퍼의 두 번째 인수를 통해 데이터를 Blade 뷰에 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 기능 강화하기

Blade 템플릿을 한 단계 더 업그레이드하여 동적인 UI를 쉽고 빠르게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면 React나 Vue와 같은 프론트엔드 프레임워크에서만 가능했던 동적 기능을 가진 Blade 컴포넌트를 작성할 수 있습니다. 복잡한 빌드 과정 없이도 현대적인 반응형(reactive) 프론트엔드를 쉽게 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 출력 (Displaying Data)

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해보겠습니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

이 경우, `name` 변수를 다음과 같이 화면에 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수를 거칩니다.

뷰에 전달된 변수의 값만 출력해야 하는 것은 아닙니다. 임의의 PHP 함수의 반환값도 출력할 수 있으며, Blade 출력문(`{{ }}`) 내부에 원하는 PHP 코드를 작성할 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔터티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔터티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

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
#### 이스케이프하지 않은 데이터 출력

Blade의 `{{ }}` 문법은 기본적으로 XSS 공격을 막기 위해 내용을 이스케이프 처리합니다. 만약 데이터를 이스케이프하지 않고 출력하려면 아래와 같이 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 출력할 때는 반드시 주의해야 합니다. 사용자 제공 데이터를 출력할 때는 XSS 공격을 방지하기 위해 반드시 이스케이프되는 `{{ }}` 문법을 사용하세요.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크도 중괄호(`{{ }}`)를 사용해 특정 표현식을 브라우저에 표시합니다. 이럴 때는 `@` 기호를 붙여서 Blade가 해당 표현식을 건드리지 않도록 할 수 있습니다. 예시:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예제에서 `@` 기호는 Blade에서 제거되지만, `{{ name }}` 표현식은 Blade가 수정하지 않고 자바스크립트 프레임워크에서 사용할 수 있도록 남겨둡니다.

`@` 기호는 Blade 지시어 또한 이스케이프할 때 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

JavaScript 변수를 초기화하기 위해 배열을 뷰로 전달하고 JSON 문자열로 출력하는 경우가 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이렇게 일일이 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 동일한 인자를 받으며, HTML 속성 안에 안전하게 삽입될 수 있도록 JSON을 적절히 이스케이프 처리해줍니다. 반환값은 `JSON.parse`가 포함된 JavaScript 구문으로, 객체/배열을 유효한 JS 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 프로젝트에서는 `Js` 파사드를 이용해 Blade에서 더 간편하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON 형태로 출력할 때만 사용하세요. Blade는 정규식 기반 파싱이므로 복잡한 표현식을 넘기면 예기치 못한 문제가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿에서 JavaScript 변수를 대량으로 보여줘야 한다면, 매번 `@` 기호로 이스케이프하지 않고 `@verbatim` 지시어로 해당 블록을 감쌀 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시어 (Blade Directives)

Blade는 템플릿 상속, 데이터 출력 외에도 PHP의 조건문, 반복문 등 제어 구조를 간결하게 사용할 수 있도록 다양한 단축 지시어를 제공합니다. 이러한 지시어는 PHP와 매우 유사한 방식으로 동작합니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시어로 조건문을 작성할 수 있습니다. 각각의 동작 방식은 PHP와 동일합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 `@unless`도 제공됩니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

PHP의 `isset`, `empty` 함수를 더 간단하게 사용할 수 있도록 `@isset`, `@empty` 지시어도 지원합니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 지시어

`@auth`, `@guest` 지시어를 사용해 현재 사용자가 [인증](https://laravel.com/docs/12.x/authentication) 되었는지, 게스트인지 빠르게 판별할 수 있습니다:

```blade
@auth
    // 인증된 사용자입니다...
@endauth

@guest
    // 인증되지 않은 사용자입니다...
@endguest
```

필요하다면 인증 Guard도 지정할 수 있습니다:

```blade
@auth('admin')
    // 인증된 사용자입니다...
@endauth

@guest('admin')
    // 인증되지 않은 사용자입니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 지시어

`@production` 지시어로 프로덕션 환경에서만 내용을 출력할 수 있습니다:

```blade
@production
    // 프로덕션 환경 전용 컨텐츠...
@endproduction
```

`@env` 지시어로 특정 환경 여부를 판별할 수 있습니다:

```blade
@env('staging')
    // "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### Section(섹션) 지시어

템플릿 상속 구조에서 섹션에 내용이 존재하는지 `@hasSection`으로 확인할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

특정 섹션이 존재하지 않을 때는 `sectionMissing`을 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 지시어

`@session` 지시어는 [세션](/docs/12.x/session) 값의 존재 여부를 확인할 수 있습니다. 세션 값이 있으면 `@session`과 `@endsession` 사이의 내용이 실행되고, 내부에서는 `$value` 변수를 통해 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### Context(컨텍스트) 지시어

`@context` 지시어는 [컨텍스트](/docs/12.x/context) 값의 존재 여부를 확인할 수 있습니다. 컨텍스트 값이 존재하면 내부에서 `$value` 변수를 통해 값을 출력할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어로 Switch 문을 작성할 수 있습니다:

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

Blade는 PHP의 반복문 구조를 간단하게 사용할 수 있게 해줍니다. 각각 PHP와 동일하게 동작합니다:

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
> `foreach` 반복문에서 [loop 변수](#the-loop-variable)를 통해 현재 반복의 상태 정보를 확인할 수 있습니다.

반복문 사용 중 `@continue`, `@break` 지시어로 현재 반복을 건너뛰거나 중단할 수 있습니다:

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

조건을 지시어 안에 바로 쓸 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 안에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수로 현재 반복 인덱스, 첫/마지막 반복 등 다양한 정보에 접근할 수 있습니다:

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

중첩 반복문에서 부모 반복의 `$loop` 변수에 접근하고 싶다면 `parent` 속성을 사용할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 속성 표:

<div class="overflow-auto">

| 속성                | 설명                                                      |
| ------------------ | -------------------------------------------------------- |
| `$loop->index`     | 반복문의 현재 인덱스(0부터 시작)                           |
| `$loop->iteration` | 현재 반복 횟수(1부터 시작)                                |
| `$loop->remaining` | 반복문에서 남은 반복 횟수                                  |
| `$loop->count`     | 반복 대상 배열의 전체 항목 수                              |
| `$loop->first`     | 첫 번째 반복인지 여부                                      |
| `$loop->last`      | 마지막 반복인지 여부                                       |
| `$loop->even`      | 짝수 번째 반복인지 여부                                    |
| `$loop->odd`       | 홀수 번째 반복인지 여부                                    |
| `$loop->depth`     | 현재 반복의 중첩 수준                                      |
| `$loop->parent`    | 중첩 반복문에서 부모의 loop 변수                           |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일

`@class` 지시어를 사용하면 CSS 클래스를 조건부로 조합할 수 있습니다. 배열의 키에는 클래스명을, 값에는 불리언식을 지정합니다. 숫자 키는 항상 렌더링됩니다:

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

마찬가지로, `@style` 지시어를 사용하여 인라인 CSS 스타일을 조건부로 추가할 수 있습니다:

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

체크박스가 "checked" 상태인지 쉽게 표시하려면 `@checked` 지시어를 사용할 수 있습니다. 조건이 true일 때 `checked` 속성이 출력됩니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

`@selected` 지시어는 select 옵션이 "selected" 상태인지 지정할 때 사용합니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled` 지시어는 요소의 "disabled" 속성을 쉽게 제어할 수 있게 해줍니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

`@readonly` 지시어는 "readonly" 속성을, `@required` 지시어는 "required" 속성을 지정할 때 사용합니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>

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
> `@include` 지시어를 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터/속성 바인딩 등 더 많은 기능을 제공합니다.

`@include` 지시어로 현재 뷰 안에 다른 Blade 뷰를 포함시킬 수 있습니다. 부모 뷰에 전달된 모든 변수는 포함된 뷰에서도 그대로 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

별도의 데이터를 포함된 뷰에 전달하고 싶다면 배열로 넘길 수 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

포함하려는 뷰가 존재하지 않을 경우 에러가 발생합니다. 존재할 수도 있고, 없을 수도 있는 뷰를 포함할 때는 `@includeIf` 지시어를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

특정 조건이 true/false일 때만 뷰를 포함하려면 `@includeWhen`, `@includeUnless`를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 첫 번째로 존재하는 뷰를 포함하려면 `includeFirst` 지시어를 사용할 수 있습니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서는 `__DIR__`, `__FILE__` 상수를 사용하지 않는 것이 좋습니다. 이 값들은 캐시된 Blade 파일의 위치를 참조합니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

반복문과 뷰 포함을 한 줄에 결합하려면 `@each` 지시어를 사용하세요:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 각 배열/컬렉션 항목마다 렌더링할 뷰, 두 번째 인수는 반복할 배열·컬렉션, 세 번째 인수는 반복마다 사용할 변수명입니다. 뷰 안에서는 현재 인덱스를 `key` 변수로 사용할 수 있습니다.

배열이 비어 있을 때 출력할 뷰를 지정하려면 네 번째 인수로 전달하세요:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링한 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 부모의 변수가 필요하다면 `@foreach`와 `@include` 조합을 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어는 해당 블록을 한 번만 렌더링하게 해줍니다. 예를 들어, 반복문 안에서 첫 번째만 [스택](#stacks)에 JavaScript를 추가하고 싶을 때 유용합니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

자주 사용하는 조합에는 `@pushOnce`, `@prependOnce` 지시어도 있습니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

서로 다른 Blade 템플릿에서 중복된 내용을 푸시할 수 있으니, 두 번째 인수에 고유 식별자를 넣어 한 번만 렌더링되도록 할 수 있습니다:

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

뷰 안에 PHP 코드를 직접 삽입하려면 `@php` 지시어로 감쌀 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

PHP 클래스를 import만 하고 싶다면 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

별칭을 지정하려면 두 번째 인수로 별칭을 넘기세요:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 내 여러 클래스도 중괄호로 한번에 가져올 수 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

함수와 상수도 `function`, `const` 키워드를 붙여 import할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

별칭도 지원합니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수/상수도 그룹 import가 가능합니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서 정의한 주석은 렌더된 HTML에는 포함되지 않습니다:

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, include 지시어와 비슷하지만 좀 더 명확한 개념을 제공합니다. 컴포넌트는 클래스 기반 컴포넌트와 익명 컴포넌트가 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용하세요. 예를 들어 간단한 `Alert` 컴포넌트를 만들어 보겠습니다. 이 명령어는 컴포넌트를 `app/View/Components` 디렉터리에 생성합니다:

```shell
php artisan make:component Alert
```

이와 함께 컴포넌트의 뷰 파일도 `resources/views/components`에 생성됩니다. 애플리케이션에서 만드는 컴포넌트는 위 디렉터리 구조에 자동으로 등록되므로 별도 등록이 필요 없습니다.

서브디렉터리에 컴포넌트를 만들 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms`에 `Input` 컴포넌트와, `resources/views/components/forms`에 뷰 파일을 생성합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션에서 만드는 컴포넌트는 자동으로 등록됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 만든다면, 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 등록합니다:

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

등록 후에는 별칭 이름으로 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드로 컴포넌트 클래스를 네임스페이스에 따라 자동으로 로드할 수도 있습니다. 예시:

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

이렇게 등록하면, 아래처럼 벤더 네임스페이스 접두어를 사용하여 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 바꿔 연결된 클래스를 자동으로 찾습니다. 하위 디렉터리 표기는 "dot" 표기법도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

Blade 템플릿에서 `x-`로 시작하는 컴포넌트 태그 문법으로 컴포넌트를 사용할 수 있습니다. 컴포넌트 클래스명이 케밥 케이스로 변환되어 태그 이름이 됩니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 더 깊은 디렉터리에 있으면 `.`를 사용해 디렉터리 구조를 나타냅니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 있다면 아래처럼 렌더링합니다:

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의하면 됩니다. `false`가 반환되면 렌더링되지 않습니다:

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
### 인덱스 컴포넌트

여러 Blade 템플릿이 하나의 컴포넌트 그룹을 이루는 경우, 연관된 컴포넌트들을 한 디렉터리로 묶고 싶을 수 있습니다. 예를 들어 "card" 컴포넌트 구조가 다음과 같다고 가정해보겠습니다:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

디렉터리와 파일명이 같으면, `<x-card.card>` 대신 `<x-card>`로 사용할 수 있습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

컴포넌트에 데이터를 전달하려면 HTML 속성을 사용하세요. 단순한 값은 일반 속성으로, 변수나 PHP 표현식은 `:`를 접두어로 사용합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 데이터 속성을 정의하면 됩니다. 모든 public 속성은 자동으로 컴포넌트 뷰에서 사용 가능합니다. `render` 메서드에서 다시 데이터를 전달할 필요는 없습니다:

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

컴포넌트 뷰에서는 public 변수 이름 그대로 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이싱(Casing)

컴포넌트 생성자 인수명은 `camelCase`로, HTML 속성에서는 `kebab-case`로 작성해야 합니다. 예를 들어 아래와 같이 컴포넌트를 정의하면:

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

블레이드에서는 다음과 같이 전달합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 축약 문법

component에 속성을 전달할 때 `"짧은 속성" 문법`을 사용할 수 있습니다. 변수명과 속성명이 일치할 때 편리합니다:

```blade
{{-- 축약 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같은 일부 자바스크립트 프레임워크에서 콜론(:)으로 시작하는 속성을 쓸 때, Blade에서 해석되지 않게 하려면 `::`(더블 콜론)를 접두어로 붙이세요:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

실제 렌더링되는 HTML은 아래와 같습니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

public 변수뿐 아니라 public 메서드도 템플릿에서 사용할 수 있습니다. 예를 들어, `isSelected`라는 메서드가 있다면 아래처럼 사용할 수 있습니다:

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 뷰에서 메서드명과 동일하게 변수를 호출하면 됩니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성/슬롯 접근하기

컴포넌트명, 속성, 슬롯 등의 데이터를 클래스의 `render` 메서드에서 사용할 수도 있습니다. 이를 위해서는 `render` 메서드에서 클로저(Closure)를 반환해야 합니다:

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

이 클로저는 `$data` 배열을 인수로 받을 수 있습니다. `$data`에는 다음 정보들이 들어 있습니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 요소를 Blade 문자열에 직접 삽입하는 것은 보안상 위험할 수 있으니 피하세요.

`componentName`은 `x-` 접두어 뒤에 오는 실제 컴포넌트 태그 이름입니다. `attributes`에는 태그에 지정한 모든 속성이 담깁니다. `slot`은 슬롯 내용을 담고 있습니다.

클로저의 반환값이 뷰 이름이면 해당 뷰가 렌더링되고, 그렇지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트에서 Laravel [서비스 컨테이너](/docs/12.x/container) 의존성이 필요한 경우, 데이터 속성 앞에 나열하면 자동으로 주입됩니다:

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
#### 속성/메서드 숨기기

일부 public 속성이나 메서드를 컴포넌트 뷰에서 접근하지 못하게 하려면 `$except` 배열 프로퍼티에 추가하세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출시키지 않을 속성/메서드 목록
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성

컴포넌트에 데이터를 전달하는 법은 이미 살펴봤지만, `class`와 같이 컴포넌트 기능에는 필요 없는 HTML 속성도 추가로 지정하고 싶을 수 있습니다. 이런 추가 속성은 "속성 bag"을 통해 컴포넌트에 전달됩니다. 이 속성 bag에는 생성자에서 받지 않은 모든 속성이 포함되며, 컴포넌트 템플릿에서 `$attributes`로 접근할 수 있습니다:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현재로서는 컴포넌트 태그 안에 `@env`와 같은 지시어는 사용할 수 없습니다. 예: `<x-alert :live="@env('production')"/>` 는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본/병합 속성

속성 bag의 `merge` 메서드를 사용하면 기본 클래스를 지정하거나, 속성 값을 병합할 수 있습니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

예를 들어 아래처럼 사용하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 결과는 아래와 같이 렌더링됩니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 클래스를 병합하고 싶으면 `class` 메서드를 사용하세요:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성도 병합하려면 `class` 메서드 뒤에 `merge`를 체이닝할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> HTML 태그에 병합 속성이 필요 없는 부분에는 [@class 지시어](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class`가 아닌 속성(예: `type`)을 병합할 때, `merge`의 값이 기본값이 됩니다. 그러나 `class`와 달리 병합되지 않고, 필요시 상속값으로 덮어써집니다:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시 타입 속성을 지정하지 않으면 기본값(`button`)이, 지정하면 지정한 값이 사용됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```

결과:

```blade
<button type="submit">
    Submit
</button>
```

기본값과 삽입값을 모두 잇고 싶다면 `prepends` 메서드를 사용할 수 있습니다. 예를 들어 `data-controller`의 기본값과 추가값을 잇고 싶으면 아래와 같이 합니다:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 추출 및 필터링

`filter` 메서드를 사용하면 조건에 맞는 속성만 남길 수 있습니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith` 메서드로 특정 접두사로 시작하는 속성만 가져올 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

`whereDoesntStartWith`로는 특정 접두사로 시작하지 않는 속성만 가져옵니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 속성 bag에서 첫 번째 속성만 가져올 수도 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성의 존재 여부는 `has` 메서드로 검사할 수 있습니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

여러 속성을 배열로 전달하면 모두 존재하는지 확인합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny` 메서드는 하나라도 속성이 있으면 true를 반환합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

`get`으로 속성값을 읽고, `only`로 특정 키만, `except`로 특정 키를 제외한 속성만 가져올 수 있습니다:

```blade
{{ $attributes->get('class') }}
{{ $attributes->only(['class']) }}
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어

아래 키워드는 내부적으로 사용되므로, 컴포넌트에서 public 속성이나 메서드로 정의할 수 없습니다:

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
### 슬롯(Slot)

컴포넌트에 추가적인 콘텐츠를 전달하고 싶을 때 "슬롯"을 사용할 수 있습니다. 슬롯은 `$slot` 변수를 통해 컴포넌트에서 사용할 수 있습니다. 예를 들어 `alert` 컴포넌트가 다음과 같다고 할 때:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

단순하게 컴포넌트에 콘텐츠를 전달하면 `$slot`으로 렌더링됩니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

두 개 이상의 슬롯이 필요하다면, 명명된 슬롯을 추가로 사용할 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>
<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯의 내용은 `x-slot` 태그로 정의합니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯에 콘텐츠가 있는지 확인하려면 `isEmpty` 메서드를, HTML 주석 이외의 실제 내용이 있는지 확인하려면 `hasActualContent`를 사용할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>

@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯(Scoped Slots)

Vue 등의 JS 프레임워크에서처럼, 슬롯에서 컴포넌트의 데이터/메서드 호출이 필요하면 컴포넌트 내부에 public 메서드를 정의하고, 슬롯 안에서 `$component` 변수로 접근할 수 있습니다:

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

슬롯에도 [속성](#component-attributes)을 지정할 수 있습니다. 예시:

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

슬롯 속성을 활용하려면 슬롯 변수를 통해 `attributes` 프로퍼티로 접근합니다. 자세한 용법은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

아주 작은 컴포넌트라면 별도의 클래스와 뷰 파일을 분리하는 것이 번거로울 수 있습니다. 이럴 땐, 컴포넌트의 `render` 메서드에서 직접 마크업을 반환하면 됩니다:

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

아래처럼 Artisan에서 `--inline` 옵션을 사용해 인라인 뷰 컴포넌트를 생성할 수 있습니다:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

어떤 컴포넌트를 렌더링할지 런타임에 결정되어야 한다면, Laravel 내장 `dynamic-component`를 사용하세요:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래의 수동 등록 문서는 뷰 컴포넌트를 포함한 패키지 제작자에게 주로 해당됩니다. 그 외에는 크게 필요하지 않을 수 있습니다.

자세한 내용은 앞서 [패키지 컴포넌트 수동 등록](#manually-registering-package-components) 섹션을 참고하세요.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

익명 컴포넌트는 인라인 컴포넌트와 비슷하게, 하나의 파일만으로 컴포넌트를 관리할 수 있습니다. 익명 컴포넌트는 클래스가 없고 뷰 파일만 존재합니다. 예를 들어, `resources/views/components/alert.blade.php`가 정의되어 있다면 아래와 같이 사용할 수 있습니다:

```blade
<x-alert/>
```

디렉터리 구조상 더 깊게 중첩되어 있다면 `.`을 사용하세요:

```blade
<x-inputs.button/>
```

Artisan에서 `--view` 옵션으로 익명 컴포넌트 뷰 파일을 생성할 수 있습니다:

```shell
php artisan make:component forms.input --view
```

위 명령은 `resources/views/components/forms/input.blade.php`를 생성하며, `<x-forms.input />`으로 사용합니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

여러 Blade 파일로 하나의 컴포넌트를 구성할 때, 해당 컴포넌트의 템플릿을 하나의 디렉터리에 모으고 싶을 수 있습니다. 예시:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 디렉터리 구조를 활용해 아래와 같이 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만, `x-accordion`으로 렌더링하려면 인덱스 템플릿이 `resources/views/components`에 있어야 했습니다. Blade는 디렉터리명과 동일한 템플릿 파일이 그 디렉터리 내에 존재할 때, 인덱스 컴포넌트로 인식하게 해줍니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 프로퍼티 / 속성

익명 컴포넌트는 클래스가 없기 때문에, 어떤 속성을 데이터 변수로 사용할지 명확히 해야 합니다. 템플릿 상단에서 `@props` 지시어를 사용하면 지정한 속성만 데이터 변수로 사용할 수 있고, 나머지는 속성 bag에 담깁니다. 기본값을 지정할 수도 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

사용 예시:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

자식 컴포넌트에서 부모의 데이터를 접근하려면 `@aware` 지시어를 사용할 수 있습니다. 예를 들어 `<x-menu>`/`<x-menu.item>` 구조에서, 부모에 지정된 `color` 속성을 자식에서 활용하려면 다음과 같이 합니다:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모(예: `components/menu/index.blade.php`):

```blade
@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

자식(예: `components/menu/item.blade.php`):

```blade
@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시어는 부모 컴포넌트에 HTML 속성으로 전달된 값만 접근 가능합니다. 선언만 하고 실제로 전달하지 않은 기본값은 사용할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

기본적으로 익명 컴포넌트는 `resources/views/components`에 위치합니다. 다른 경로에서도 익명 컴포넌트를 사용하려면, `anonymousComponentPath` 메서드로 경로를 등록할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

별도의 네임스페이스를 두 번째 인수로 지정하고, 해당 접두사로 컴포넌트를 사용할 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이 경우, 컴포넌트는 `<x-dashboard::panel />` 형태로 사용할 수 있습니다.

<a name="building-layouts"></a>
## 레이아웃 구축하기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트로 레이아웃 만들기

일반적으로 웹 애플리케이션은 여러 페이지에 동일한 레이아웃을 사용합니다. 모든 뷰에 레이아웃 마크업을 반복하는 것은 비효율적이므로, 보통 하나의 [Blade 컴포넌트](#components)로 레이아웃을 정의합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "todo" 리스트 앱을 만든다면 다음과 같이 `layout` 컴포넌트를 정의할 수 있습니다:

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

정의한 `layout` 컴포넌트를 실제 뷰에서 사용할 수 있습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 전달된 내용은 `$slot` 변수로 받게 됩니다. `$title` 슬롯도 사용할 수 있습니다:

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

마지막으로, 아래처럼 라우트에서 뷰를 반환하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속으로 레이아웃 만들기

<a name="defining-a-layout"></a>
#### 레이아웃 정의

"템플릿 상속"을 통해서도 레이아웃을 만들 수 있습니다. 이는 [컴포넌트](#components) 도입 전까지 Blade의 주된 방식이었습니다.

기본적인 레이아웃 예시는 아래와 같습니다:

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

여기서 `@section`은 새로운 섹션을 정의하고, `@yield`는 해당 섹션의 내용을 출력합니다.

이제 하위 뷰에서 이 레이아웃을 상속받을 수 있습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

하위 뷰에서 어떤 레이아웃을 상속받을지 `@extends` 지시어로 지정합니다. 레이아웃의 각 섹션에 원하는 내용을 채우려면 `@section`을 사용하세요:

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

`@@parent` 지시어는 부모 레이아웃의 내용을 추가(append)하는 데 사용됩니다.

> [!NOTE]
> 이 예시에서 `sidebar` 섹션은 `@endsection`으로 끝납니다. `@endsection`은 섹션만 정의하고, `@show`는 섹션을 정의함과 동시에 바로 출력합니다.

`@yield`는 두 번째 인자로 기본값을 받아, 섹션이 정의되지 않았을 때 대체 콘텐츠도 출력할 수 있습니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에 HTML 폼을 정의할 때는, 반드시 숨겨진 CSRF 토큰 필드를 포함해야 [CSRF 보호 미들웨어](/docs/12.x/csrf)가 요청을 검증할 수 있습니다. `@csrf` 지시어로 토큰 필드를 추가할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 지원하지 않으므로, 숨겨진 `_method` 필드로 HTTP 메서드를 변경해야 합니다. `@method` 지시어를 사용하면 됩니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 지시어로 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)를 쉽게 확인할 수 있습니다. 내부에서는 `$message`로 에러 메시지를 출력할 수 있습니다:

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

`@error`는 내부적으로 if문으로 컴파일되므로, 에러가 없을 때는 `@else`로 다른 내용을 렌더링할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[명명된 에러백](/docs/12.x/validation#named-error-bags)이 여러 폼에 걸쳐 있을 때는 두 번째 인수로 에러백 이름을 넘겨 메시지를 구분할 수 있습니다:

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

Blade에서는 "스택"에 컨텐츠를 push해서 나중에 다른 뷰나 레이아웃에서 한꺼번에 출력할 수 있습니다. 자식 뷰에서 JS 라이브러리 등을 지정할 때 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

조건에 따라 스택에 추가하려면 `@pushIf`를 쓸 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에 여러 번 push해도 괜찮으며, 스택 전체 내용을 출력하려면 `@stack`을 사용하세요:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 앞에 내용을 붙이려면 `@prepend`를 사용합니다:

```blade
@push('scripts')
    This will be second...
@endpush

// 이후...

@prepend('scripts')
    This will be first...
@endprepend
```

스택이 비어있는지 검사하려면 `@hasstack`을 사용할 수 있습니다:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
## 서비스 주입 (Service Injection)

`@inject` 지시어로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 가져올 수 있습니다. 첫 번째 인수는 변수 이름, 두 번째는 서비스의 클래스 또는 인터페이스명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

원시 Blade 템플릿 문자열을 HTML로 변환해야 하는 경우, `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 이 메서드는 Blade 템플릿 문자열과, 전달할 데이터 배열을 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

인라인 Blade 템플릿은 임시로 `storage/framework/views`에 파일로 저장됩니다. 렌더 후 임시 파일을 삭제하고 싶다면, `deleteCachedView` 인자를 전달하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

[Tubro](https://turbo.hotwired.dev/), [htmx](https://htmx.org/) 등의 프론트엔드 프레임워크를 사용할 때, Blade 템플릿 부분만 일부만 응답에서 반환해야 할 때가 있습니다. 이럴 때 `@fragment`, `@endfragment` 지시어로 프래그먼트를 정의하고, 뷰 반환 시 `fragment` 메서드로 특정 프래그먼트만 응답에 포함시킬 수 있습니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

렌더링 시:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건부로 프래그먼트를 포함하려면 `fragmentIf`를 사용하세요:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트를 합쳐 반환하려면 `fragments` 또는 `fragmentsIf`를 사용합니다:

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
## Blade 확장하기 (Extending Blade)

`directive` 메서드로 커스텀 지시어를 직접 정의할 수 있습니다. Blade가 해당 지시어를 만나면, 콜백에 정의한 로직을 실행합니다.

예를 들어, `@datetime($var)` 지시어를 만들어 `$var`(DateTime 인스턴스)를 포맷하려면:

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

사용 시 Blade가 최종적으로 아래와 같이 PHP 코드를 생성합니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 지시어 로직을 변경한 후에는 캐시된 Blade 뷰 파일을 삭제해야 합니다. 이는 `view:clear` Artisan 명령어로 할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러

Blade에서 객체를 "에코"하면 해당 객체의 `__toString` 메서드가 호출됩니다. 그러나 서드파티 라이브러리 등에서 객체의 `__toString` 메서드를 제어할 수 없는 경우, 커스텀 에코 핸들러를 등록할 수 있습니다.

`Blade::stringable` 메서드에 타입힌트된 클로저를 전달하세요. 보통 `AppServiceProvider`의 `boot` 메서드에서 설정합니다:

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

이후 Blade 템플릿에서 해당 타입의 객체를 출력하면 자동으로 핸들러가 실행됩니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

간단한 커스텀 조건문은 `Blade::if` 메서드로 손쉽게 지원할 수 있습니다. 아래 예시는 애플리케이션의 기본 "disk"가 특정 값인지 확인하는 커스텀 조건문을 정의합니다.

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

정의 후, 템플릿에서 아래처럼 사용합니다:

```blade
@disk('local')
    <!-- local 디스크를 사용하는 경우... -->
@elsedisk('s3')
    <!-- s3 디스크를 사용하는 경우... -->
@else
    <!-- 그 외 디스크를 사용하는 경우... -->
@enddisk

@unlessdisk('local')
    <!-- local 디스크가 아닌 경우... -->
@enddisk
```
