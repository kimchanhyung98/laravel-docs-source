# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시어](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [@once 지시어](#the-once-directive)
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
    - [데이터 속성 / 속성배열](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 만들기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검사 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과는 달리, Blade는 템플릿 파일에서 일반 PHP 코드를 자유롭게 사용할 수 있습니다. 실제로 모든 Blade 템플릿은 일반 PHP 코드로 컴파일되고, 수정 전까지 캐시에 저장되므로 애플리케이션에 사실상 오버헤드가 없습니다. Blade 템플릿 파일의 확장자는 `.blade.php`이며, 일반적으로 `resources/views` 디렉터리에 위치합니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론 [뷰](/docs/12.x/views) 문서에서 설명한 것처럼, 뷰에 데이터를 전달하려면 `view` 헬퍼의 두 번째 인수를 사용하면 됩니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 강화하기 (Supercharging Blade With Livewire)

Blade 템플릿으로 한 단계 더 진보된, 동적인 인터페이스를 손쉽게 개발하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire는 원래 React나 Vue와 같은 프론트엔드 프레임워크에서만 가능하던 동적 기능을, Blade 컴포넌트에 쉽게 추가할 수 있게 해줍니다. 복잡한 프론트엔드 빌드 과정이나 클라이언트사이드 렌더링 없이, 현대적인 반응형 인터페이스를 구축할 수 있는 훌륭한 접근 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시 (Displaying Data)

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 화면에 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정합니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수를 다음과 같이 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 자동 처리됩니다.

뷰에 전달된 변수뿐 아니라, PHP 함수의 결과도 출력할 수 있습니다. Blade 출력 구문 내에 어떤 PHP 코드든 작성 가능합니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩(즉, 이미 인코딩된 엔티티도 다시 인코딩)합니다. 이중 인코딩을 끄려면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프 처리하지 않은 데이터 표시하기

Blade의 `{{ }}` 구문은 항상 PHP의 `htmlspecialchars` 함수로 인해 자동 이스케이프 처리됩니다. 이스케이프 처리를 하지 않고 데이터를 그대로 출력하려면 다음과 같이 작성하세요:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 출력할 때는 매우 주의해야 합니다. 일반적으로는 XSS 공격 방지를 위해 이스케이프된 이중 중괄호 구문을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크 (Blade and JavaScript Frameworks)

많은 자바스크립트 프레임워크(예: Vue, React 등) 역시 "중괄호"(`{}`) 문법을 화면 표시용으로 사용합니다. 이때 Blade 렌더러가 중괄호 구문을 처리하지 않도록 하려면, `@` 기호를 붙여주세요. 예시:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예제에서 `@` 기호는 Blade가 제거하므로, `{{ name }}` 구문이 그대로 남아 자바스크립트 프레임워크에서 처리됩니다.

마찬가지로 `@` 기호로 Blade 지시어도 이스케이프 처리할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

종종 배열을 뷰에 전달하고 이것을 JSON으로 렌더링해 자바스크립트 변수 초기화에 사용하고 싶을 수 있습니다. 예시:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 지시어를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 동일한 인수를 받지만, HTML 내 인용부호에 안전하도록 JSON을 이스케이프합니다. 반환 결과는 `JSON.parse` JavaScript 구문으로, 객체/배열을 올바른 자바스크립트 객체로 만듭니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션에는 `Js` 파사드가 포함되어 있으므로 더 간단하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 **기존 변수**를 JSON으로 렌더링하는 용도로만 사용하세요. Blade는 정규 표현식 기반으로 동작하므로 복잡한 표현식을 전달하면 예기치 않은 문제가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### @verbatim 지시어

템플릿의 큰 영역에서 자바스크립트 변수를 표시해야 할 때, 모든 Blade 출력문 앞에 `@`를 붙이고 싶지 않다면 `@verbatim` 지시어로 감싸면 됩니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시어 (Blade Directives)

템플릿 상속, 데이터 표시 외에도, Blade는 편리하게 PHP의 주요 제어 구조(조건문, 반복문 등)를 간단하게 사용할 수 있는 단축 지시어를 제공합니다. 이 지시어들은 PHP의 문법과 거의 동일하지만 훨씬 간결하고 읽기 쉽습니다.

<a name="if-statements"></a>
### If 문 (If Statements)

`@if`, `@elseif`, `@else`, `@endif` 지시어로 if 문을 작성할 수 있습니다. PHP 코드와 동작이 같습니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

또한 편리하게 `@unless` 지시어도 사용할 수 있습니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

위 지시어 외에도, `@isset` 및 `@empty`를 PHP 함수처럼 사용할 수도 있습니다:

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시어

`@auth`, `@guest` 지시어로 현재 사용자가 [인증(authenticate)](/docs/12.x/authentication)된 사용자 또는 손님(guest)인지 쉽게 판별 가능합니다:

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

인증 가드를 지정하려면 아래와 같이 작성합니다:

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 지시어

`@production` 지시어로 현재 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // Production specific content...
@endproduction
```

또한 특정 환경에 대한 확인은 `@env` 지시어로 할 수 있습니다:

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a name="section-directives"></a>
#### Section 지시어

템플릿 상속의 섹션에 내용이 있는지 확인하려면 `@hasSection` 지시어를 사용합니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션이 없는 경우를 확인하려면 `sectionMissing` 지시어를 사용하세요:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시어

`@session` 지시어를 통해 [세션](https://laravel.com/docs/12.x/session) 값 존재여부를 확인할 수 있습니다. 세션 값이 있으면 `@session`과 `@endsession` 사이의 템플릿이 실행되며, `$value` 변수로 값을 참조할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 지시어

`@context` 지시어로 [컨텍스트](/docs/12.x/context) 값 존재여부를 확인할 수 있습니다. 값이 있으면 `$value` 변수로 컨텍스트 값을 출력할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문 (Switch Statements)

switch 문은 `@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어로 작성합니다:

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

Blade는 PHP의 반복문 구조도 간단히 사용할 수 있는 지시어를 지원합니다. 아래와 같이 PHP와 동일한 방식으로 루프를 쓸 수 있습니다:

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
> `foreach` 반복문에서는 [루프 변수](#the-loop-variable)를 사용해 현재 반복의 첫 번째 혹은 마지막 반복 등, 다양한 정보를 얻을 수 있습니다.

반복문 내부에서는 `@continue`, `@break` 지시어로 반복을 건너뛰거나 중단할 수 있습니다:

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

조건식을 지시어 선언부에 직접 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수 (The Loop Variable)

`foreach` 반복문을 돌 때에는, `$loop`라는 변수가 루프 내부에서 자동으로 사용 가능해집니다. 현재 인덱스, 첫 번째/마지막 반복 여부 등 다양한 정보를 제공합니다:

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

중첩 반복문에서는 `parent` 속성으로 상위 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

$loop 변수에 포함된 주요 속성:

| 속성                | 설명                                            |
| ------------------- | --------------------------------------------- |
| `$loop->index`      | 현재 루프의 인덱스(0부터 시작).                 |
| `$loop->iteration`  | 현재 반복 횟수(1부터 시작).                     |
| `$loop->remaining`  | 남은 반복 횟수.                                 |
| `$loop->count`      | 반복되는 배열의 전체 아이템 수.                  |
| `$loop->first`      | 첫 번째 반복인지 여부.                          |
| `$loop->last`       | 마지막 반복인지 여부.                           |
| `$loop->even`       | 짝수 반복인지 여부.                             |
| `$loop->odd`        | 홀수 반복인지 여부.                             |
| `$loop->depth`      | 중첩 반복의 깊이.                               |
| `$loop->parent`     | 중첩 반복 시, 상위 반복문의 $loop 변수.         |

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일 (Conditional Classes & Styles)

`@class` 지시어로 CSS 클래스를 조건에 따라 컴파일할 수 있습니다. 배열의 키는 추가할 클래스 이름, 값은 불리언(조건식)이어야 하며, 숫자 키는 무조건 포함됩니다:

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

마찬가지로 `@style` 지시어를 사용해 조건부 인라인 스타일도 적용할 수 있습니다:

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

HTML의 체크박스 input이 "checked" 상태일 경우를 간단히 표시하고 싶을 땐 `@checked` 지시어를 사용하세요. 해당 조건이 true면 `checked`가 출력됩니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

select 옵션에서 "선택됨" 상태를 표시하고 싶으면 `@selected` 지시어를 사용합니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

태그가 비활성(disabled) 상태여야 하는 경우 `@disabled`, 읽기 전용(readonly)이어야 하는 경우 `@readonly`, 필수(required)여야 하는 경우 `@required` 지시어를 각각 사용할 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>

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
### 서브뷰 포함하기 (Including Subviews)

> [!NOTE]
> `@include` 지시어도 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 이점을 제공하므로, 가능하다면 컴포넌트를 활용하는 것이 좋습니다.

Blade의 `@include` 지시어를 사용하면 다른 Blade 뷰를 현재 뷰 내에서 쉽게 포함할 수 있습니다. 부모 뷰에서 이용할 수 있는 모든 변수는 포함된 뷰에서도 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰에 추가로 전달할 데이터가 있다면 배열 형태로 넘길 수 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

만약 존재하지 않는 뷰를 `@include` 하면 에러가 발생합니다. 특정 뷰가 있을 때만 포함하려면 `@includeIf`를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

조건식이 true일 때만 뷰를 포함하고 싶다면 `@includeWhen`, false일 때는 `@includeUnless`를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 실제로 존재하는 첫 번째 뷰를 포함하려면 `includeFirst`를 사용합니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수를 사용하는 것은 권장하지 않습니다. 이 상수들은 캐시된 컴파일 뷰의 파일 경로를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

반복문과 뷰 포함을 한 줄로 처리하고 싶을 땐 `@each` 지시어를 사용하세요:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 렌더링할 뷰 이름, 두 번째는 반복할 배열 또는 컬렉션, 세 번째 인수는 각 반복에서 사용할 변수명입니다. 즉, `$jobs` 배열/컬렉션을 반복하며 각 뷰에서 `job` 변수로 아이템에 접근하게 됩니다. 이 때 배열 키는 `key` 변수로 사용 가능합니다.

네 번째 인수는 배열이 비어있을 때 렌더링할 뷰 이름입니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 부모 데이터를 써야 한다면 `@foreach` + `@include` 조합을 사용하세요.

<a name="the-once-directive"></a>
### @once 지시어 (The `@once` Directive)

`@once` 지시어는 템플릿 내 특정 구문이 렌더링 주기마다 한 번만 실행되도록 보장합니다. 예를 들어, 여러 컴포넌트에서 동일한 자바스크립트를 헤더에 넣고 싶을 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 주로 `@push`나 `@prepend`와 함께 사용되므로, 더욱 편리하게는 `@pushOnce`, `@prependOnce` 지시어도 있습니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

만약 여러 템플릿에서 동일한 내용을 푸시하고 중복 삽입을 방지하려면, `@pushOnce`의 두 번째 인수로 고유 식별자를 지정하세요:

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

특정 상황에서는 뷰 내에 PHP 코드 블록을 직접 작성할 수 있습니다. `@php` 지시어로 PHP 코드를 실행하세요:

```blade
@php
    $counter = 1;
@endphp
```

클래스만 가져오고 싶다면 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

클래스에 별칭을 붙이고 싶다면 두 번째 인수로 이름을 넘깁니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스의 여러 클래스를 한 번에 임포트할 수도 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

함수와 상수도, `function`, `const`로 앞에 붙여 임포트 가능합니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수와 상수에도 별칭을 붙일 수 있습니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

여러 함수/상수를 그룹으로 한 번에 임포트할 수도 있습니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석 (Comments)

Blade에서는 뷰에 주석을 남길 수 있습니다. Blade 주석은 HTML 출력 결과에는 포함되지 않습니다:

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 비슷한 장점을 제공하지만, 컴포넌트와 슬롯의 개념을 더 직관적으로 받아들이는 개발자도 많습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명(뷰 기반) 컴포넌트 두 가지 방식이 있습니다.

클래스 기반 컴포넌트를 만들려면, `make:component` Artisan 명령어를 사용하세요. 예를 들어, `Alert` 컴포넌트를 만들어보겠습니다. 다음 명령은 컴포넌트 클래스를 `app/View/Components` 디렉터리에 생성합니다:

```shell
php artisan make:component Alert
```

해당 명령은 템플릿 뷰도 함께 생성합니다. 뷰 파일은 `resources/views/components` 디렉터리에 위치합니다. 내 애플리케이션에서 직접 작성하는 컴포넌트는 별도 등록 과정 없이 해당 디렉터리에서 자동 인식됩니다.

서브디렉터리 내에 컴포넌트를 생성할 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms/Input.php` 파일과 `resources/views/components/forms/input.blade.php` 뷰 파일을 각각 생성합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

내 애플리케이션의 컴포넌트는 자동 등록되지만, 패키지로 배포하는 경우 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 일반적으로 패키지의 서비스 프로바이더의 `boot` 메서드에서 등록하면 됩니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후에는 별칭으로 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

혹은, `componentNamespace` 메서드로 네임스페이스 기반 자동 로딩도 가능합니다. 예를 들어, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있을 때 다음처럼 구성할 수 있습니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면, 아래와 같이 `package-name::` 네임스페이스 태그를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 매칭하여 자동으로 클래스를 연결합니다. 서브디렉터리는 "dot" 표기법을 사용할 수 있습니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링 (Rendering Components)

컴포넌트를 렌더링하려면, Blade 템플릿 내에 `x-`로 시작하는 케밥 케이스 이름의 컴포넌트 태그를 사용하면 됩니다:

```blade
<x-alert/>

<x-user-profile/>
```

`app/View/Components` 하위의 디렉터리 구조를 사용할 경우, `.` 기호로 디렉터리 중첩을 나타낼 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 있다면 아래처럼 렌더링합니다:

```blade
<x-inputs.button/>
```

컴포넌트의 렌더 조건을 동적으로 지정하려면, 컴포넌트 클래스에 `shouldRender` 메서드를 추가하세요. 이 메서드가 `false`를 반환하면 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더 여부 결정
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트 (Index Components)

컴포넌트 그룹 내에서, 관련 컴포넌트들을 한 디렉터리에 모으고 싶을 때가 있습니다. 예를 들어, "card" 컴포넌트 구조가 다음과 같다고 가정합니다:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 `Card` 컴포넌트가 `Card` 디렉터리 안에 있으므로 `<x-card.card>`로 렌더해야 할 것 같지만, 컴포넌트 파일명과 디렉터리명이 같으면 "루트" 컴포넌트로 간주되어 디렉터리명을 반복할 필요가 없습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달 (Passing Data to Components)

Blade 컴포넌트에는 HTML 속성 형태로 데이터를 전달할 수 있습니다. 하드코딩된 값은 그냥 문자열 속성으로, PHP 변수/표현식은 `:` 접두어를 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트의 데이터 속성(프로퍼티)는 클래스의 생성자에서 모두 선언해주어야 합니다. 컴포넌트의 `render` 메서드에서 뷰로 전달할 필요 없이, public 속성은 뷰에서 자동 사용 가능합니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스 생성
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 컴포넌트가 나타낼 뷰/내용 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링되면, public 변수명을 그대로 뷰 내에서 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 속성명 표기법

생성자 인수는 `camelCase`로, HTML 속성에서는 `kebab-case`로 작성해야 합니다. 예시:

```php
/**
 * 컴포넌트 인스턴스 생성
 */
public function __construct(
    public string $alertType,
) {}
```

이때는 아래처럼 전달합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속기 속성 문법

컴포넌트 속성명과 변수명이 동일할 때는, 아래처럼 속기 문법을 사용할 수 있습니다:

```blade
{{-- 속기 문법 --}}
<x-profile :$userId :$name />

{{-- 일반 문법과 동일함 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같이 `:`로 시작하는 속성을 사용하는 자바스크립트 프레임워크와 충돌이 있다면, `::` 접두어를 써서 Blade가 PHP 표현식으로 인식하지 않게 할 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

이렇게 하면 실제 HTML에는 아래처럼 렌더됩니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서는 public 메서드도 사용할 수 있습니다. 예를 들어, 선택 여부를 판별하는 `isSelected` 메서드가 있다면:

```php
/**
 * 주어진 옵션이 현재 선택된 옵션인지 판별
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

뷰에서는 아래처럼 메서드를 호출하면 됩니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 클래스 내 속성 및 슬롯 접근

컴포넌트 클래스에서 컴포넌트의 이름, 속성, 슬롯 데이터를 사용하려면 `render` 메서드에서 클로저를 반환해야 합니다:

```php
use Closure;

/**
 * 컴포넌트가 나타낼 뷰/내용 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

클로저는 `$data` 배열도 인수로 받을 수 있습니다. 이 배열에는 아래와 같은 정보가 담깁니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 각 요소를 Blade 문자열에 바로 포함하지 마세요. 속성에 악의적 코드가 포함될 수 있으므로 주의해야 합니다.

`componentName`은 태그에서 `x-` 뒤에 오는 이름입니다. 예를 들어 `<x-alert />`의 경우 `componentName`은 `alert`입니다. `attributes`에는 태그의 모든 속성이, `slot`에는 슬롯 콘텐츠가 들어 있습니다.

클로저에서 반환값이 문자열이고 파일명과 일치하면 해당 뷰를 렌더하며, 일치하지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 종속성

컴포넌트가 Laravel의 [서비스 컨테이너](/docs/12.x/container)에서 종속성을 필요로 한다면, 생성자 인수에 데이터 속성 앞에 추가 인수로 선언하면 자동으로 주입됩니다:

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성/메서드 감추기

public 속성이나 메서드를 뷰에서 노출하고 싶지 않으면 `$except` 배열 속성에 이름을 추가하세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출 금지 속성/메서드
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스 생성
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성 (Component Attributes)

데이터 속성 이외에, 예를 들어 `class`처럼 HTML 태그의 추가 속성을 넘어선 값이 필요할 때가 있습니다. 이 경우, 컴포넌트 생성자에 정의되지 않은 모든 속성은 "속성배그(attribute bag)"에 모여 `$attributes` 변수로 전달됩니다. 아래처럼 사용하세요:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현재는 컴포넌트 태그에서 `@env`와 같은 디렉티브를 직접 사용할 수 없습니다. 예) `<x-alert :live="@env('production')"/>` 등의 구문은 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합된 속성

기본 속성값을 지정하거나 특정 속성에 값을 추가로 합치고 싶다면, 속성배그의 `merge` 메서드를 사용하세요. 대표적으로, CSS 클래스를 항상 적용할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

아래처럼 컴포넌트를 사용한다면,

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링된 HTML은 다음과 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건에 따라 클래스를 추가로 합치고 싶다면 `class` 메서드를 사용합니다. 배열로 클래스를 지정하고, 불리언 값으로 조건식을 넣으면 됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성 병합이 필요한 경우, `class` 메서드 다음에 `merge` 체이닝도 가능:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 머지된 속성을 받지 않는 단순한 HTML 요소에서 조건부 클래스를 쓰려면 [@class 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스 이외 속성 병합

`class`가 아닌 다른 속성들도 `merge` 메서드를 통해 기본값으로 지정할 수 있습니다. 단, `class` 속성과 다르게 기본값과 주입된 값을 합치지 않고, 주입값이 있으면 덮어씁니다. 예를 들어 button 컴포넌트가 아래와 같이 구현되어 있다면:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

사용 시 type을 지정하지 않으면 기본으로 `button`이, 지정하면 전달된 값이 사용됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```

최종 렌더링 결과:

```blade
<button type="submit">
    Submit
</button>
```

`class` 외의 속성도 기본값과 주입값을 합치고 싶을 경우, `prepends` 메서드를 사용할 수 있습니다. 예를 들어, 컨트롤러 속성을 항상 맨 앞에 붙이고 싶을 때:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드로 속성을 걸러낼 수 있습니다. 클로저에서 true를 반환하는 속성만 남습니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith`로는 주어진 접두어로 시작하는 모든 속성을 찾고,

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

`whereDoesntStartWith`로는 주어진 접두어가 아닌 속성만 추출할 수 있습니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드는 속성배그에서 첫 번째 속성을 렌더링합니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성 존재 여부는 `has` 메서드로 판단합니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열을 넘기면 모든 속성이 있는지 확인하고,

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny`는 하나라도 존재하는지 확인합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

`get`으로는 특정 속성의 값을, `only`로는 일부 속성만, `except`로는 일부 속성을 제외한 값을 얻을 수 있습니다:

```blade
{{ $attributes->get('class') }}
{{ $attributes->only(['class']) }}
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade 내부적으로 사용하는 몇몇 예약어는 컴포넌트의 public 속성이나 메서드 이름으로 쓸 수 없습니다:

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯 (Slots)

컴포넌트에 추가 콘텐츠를 전달해야 할 때 "슬롯(slot)"을 이용합니다. `$slot` 변수를 출력하여 전달된 내용을 표시합니다. 예시:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트 사용 시, 슬롯 영역에 원하는 내용을 넣을 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 슬롯이 필요한 경우, 아래처럼 이름 있는 슬롯을 만들 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯 내용은 `x-slot` 태그로 명시적으로 넘길 수 있습니다. 지정되지 않은 영역은 `$slot` 변수로 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯의 내용이 있는지 확인하려면 `isEmpty` 메서드를 사용하세요:

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

HTML 주석이 아닌 실제 콘텐츠가 있는지 확인하려면 `hasActualContent` 를 사용할 수 있습니다:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯 (Scoped Slots)

Vue와 같은 자바스크립트 프레임워크의 "스코프 슬롯"처럼, 컴포넌트 내의 데이터나 메서드를 슬롯에서 접근할 수 있습니다. 컴포넌트의 public 메서드나 속성을 선언 후, 슬롯에서 `$component` 변수로 접근하세요:

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

Blade 컴포넌트처럼, 슬롯에도 [속성](#component-attributes)을 추가할 수 있습니다:

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

슬롯 속성과 상호작용하고 싶다면, 슬롯 변수의 `attributes` 속성을 사용하세요. 더 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

아주 작은 컴포넌트는 별도의 클래스와 뷰를 분리해 관리하는 것이 번거로울 수 있습니다. 이 경우, `render` 메서드에서 마크업을 바로 반환할 수 있습니다:

```php
/**
 * 컴포넌트가 나타낼 뷰/내용 반환
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

인라인 뷰 컴포넌트를 Artisan으로 생성하려면, `make:component` 명령에 `--inline` 옵션을 추가하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트 (Dynamic Components)

런타임에 렌더링할 컴포넌트가 바뀔 수 있는 상황에서는 Laravel의 내장 `dynamic-component`를 사용할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록 (Manually Registering Components)

> [!WARNING]
> 컴포넌트 수동 등록 문서는 Laravel 패키지 작성 등 특수한 경우에 해당합니다. 일반 애플리케이션 개발자라면 해당 부분을 건너뛰어도 됩니다.

내 애플리케이션 컴포넌트는 자동으로 인식됩니다. 패키지에서 Blade 컴포넌트를 추가하거나, 비표준 경로에 컴포넌트를 둘 때는 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드 내에서 이 작업을 진행합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록 후, 태그 별칭으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

`componentNamespace`로 네임스페이스 기반 자동 로딩도 가능합니다. 예를 들어, `Nightshade` 패키지에 관련 컴포넌트가 있다면 다음처럼 구성합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이제 아래처럼 네임스페이스 태그로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade가 적절한 클래스를 찾아 자동 매칭합니다. 서브디렉터리는 "dot" 표기법을 사용할 수 있습니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트처럼, 익명 컴포넌트는 컴포넌트 관리를 단일 파일(BLADE 파일)로 할 수 있게 해줍니다. 익명 컴포넌트는 별도의 클래스 없이 하나의 뷰 파일만 존재합니다. `resources/views/components` 디렉터리에 Blade 파일을 직접 생성하면 즉시 사용할 수 있습니다. 예:

```blade
<x-alert/>
```

서브디렉터리에서 선언하고 싶다면, 점(`.`)으로 경로를 표현합니다:

```blade
<x-inputs.button/>
```

익명 컴포넌트를 Artisan으로 만들려면, `--view` 옵션을 사용하세요:

```shell
php artisan make:component forms.input --view
```

이 명령은 `resources/views/components/forms/input.blade.php` 파일을 만듭니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트 (Anonymous Index Components)

여러 Blade 파일로 이루어진 컴포넌트를 관리할 때, 한 디렉터리에 관련 템플릿을 모아두고 싶을 수 있습니다. 예시:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 경우 다음과 같이 렌더링할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

더 깔끔하게, 디렉터리 내부에 해당 이름의 파일을 두어 인덱스 역할을 하게 만들면 아래 구조로 작성할 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 하면 `<x-accordion>`로 렌더 가능하고, 템플릿 관리도 일관성 있게 할 수 있습니다.

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성배열 (Data Properties / Attributes)

익명 컴포넌트는 별도의 클래스가 없기 때문에, 어떤 HTML 속성이 데이터 변수로 들어오고 어떤 것이 속성배그에 들어가는지 직접 지정해야 합니다. 템플릿 상단에 `@props` 지시어로 선언합니다. 기본값을 주고 싶으면 배열 형태로 쓰세요:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 컴포넌트는 아래처럼 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근 (Accessing Parent Data)

하위 컴포넌트에서 부모 컴포넌트가 가진 데이터를 쓰고 싶을 때 `@aware` 지시어를 사용할 수 있습니다. 예제:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 `<x-menu>`:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

자식 `<x-menu.item>`에서 부모의 `color` 속성을 사용하려면 다음과 같이 합니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware`는 부모 컴포넌트에 **명시적으로 HTML 속성으로 전달된 값**만 접근할 수 있습니다. 부모 `@props`의 기본값만 있고 HTML 속성으로 전달되지 않은 값은 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로 (Anonymous Component Paths)

기본적으로 익명 컴포넌트는 `resources/views/components`에 정의되지만, 추가 경로도 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인수로 컴포넌트 경로, 두 번째(선택) 인수로 네임스페이스를 받습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 설정합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

프리픽스 없이 경로를 등록했다면, 컴포넌트 사용 시 별도의 접두어 없이 아래와 같이 사용할 수 있습니다:

```blade
<x-panel />
```

네임스페이스(접두사)를 둘 경우:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

아래처럼 접두사가 붙은 컴포넌트 이름으로 렌더해야 합니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 만들기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃 (Layouts Using Components)

대부분의 웹 애플리케이션은 여러 페이지에 동일한 기본 레이아웃을 적용합니다. 만약 각 뷰마다 레이아웃 HTML을 반복해 작성한다면, 코드 관리가 매우 번거로워질 것입니다. 다행히도 Blade [컴포넌트](#components)로 레이아웃을 한 번만 정의한 뒤, 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "투두" 관리 애플리케이션을 만든다고 하면, 레이아웃 컴포넌트를 다음과 같이 생성할 수 있습니다:

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

레이아웃 컴포넌트가 준비되면, 해당 컴포넌트를 사용하는 Blade 뷰를 작성할 수 있습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 전달된 콘텐츠는 `$slot` 변수로 전달됩니다. 또한, 원하는 경우 아래처럼 슬롯을 이용해 제목도 동적으로 지정할 수 있습니다:

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

뷰 반환 예시:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃 (Layouts Using Template Inheritance)

<a name="defining-a-layout"></a>
#### 레이아웃 정의

"템플릿 상속"을 이용해 레이아웃을 만들 수도 있습니다. 이는 [컴포넌트](#components) 도입 전 Blade의 주요 방식이었습니다.

먼저, 기본 레이아웃 뷰를 정의합니다. 예시:

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

위 코드에서, `@section`은 섹션 내용을 정의하고, `@yield`는 해당 섹션 내용을 출력합니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

하위 뷰에서는 `@extends`로 어떤 레이아웃을 상속받을지 지정합니다. `@section`으로 섹션 내용을 채우고, 이 내용은 레이아웃의 `@yield`에서 출력됩니다:

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

여기서, `sidebar` 섹션은 `@@parent`를 사용해 레이아웃의 기존 사이드바 내용에 이어 붙입니다(`@parent`). `@endsection`과 `@show`의 차이에 유의하세요. `@yield`는 두 번째 인수로 기본값도 지정 가능합니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드 (CSRF Field)

HTML 폼을 작성할 때는 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있도록, 숨겨진 CSRF 토큰 필드를 추가해야 합니다. `@csrf` 지시어로 이를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드 (Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 지원하지 않으므로, 해당 HTTP 메서드를 흉내 내려면 숨겨진 `_method` 필드가 필요합니다. `@method` 지시어가 자동으로 생성해줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검사 오류 (Validation Errors)

`@error` 지시어로 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors) 존재 여부를 빠르게 확인할 수 있습니다. 내부에서 `$message` 변수를 출력하면 에러 메시지가 표시됩니다:

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

`@error`는 if문으로 컴파일되므로 `@else`와 함께 사용할 수도 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 폼이 섞인 페이지에서는 [특정 에러 백 이름](/docs/12.x/validation#named-error-bags)을 두 번째 인수로 전달할 수 있습니다:

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

Blade에서는 명명된 스택에 콘텐츠를 "푸시"한 뒤, 다른 레이아웃/뷰에서 렌더링할 수 있습니다. 이것은 각 자식 뷰에서 필요한 자바스크립트 라이브러리 등을 명확하게 선언하는 데 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

조건부로 스택을 푸시할 때는 `@pushIf` 지시어 사용:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

필요하면 여러 번 푸시할 수 있습니다. 스택 전체 내용을 출력하려면 `@stack('이름')`을 사용합니다:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택 맨 앞에 내용을 추가하려면 `@prepend`:

```blade
@push('scripts')
    This will be second...
@endpush

// 나중에...

@prepend('scripts')
    This will be first...
@endprepend
```

`@hasstack` 지시어로 스택이 비었는지 확인할 수 있습니다:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
## 서비스 주입 (Service Injection)

`@inject` 지시어로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 바로 가져올 수 있습니다. 첫 번째 인수는 변수명, 두 번째는 클래스(혹은 인터페이스)명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 블레이드 템플릿 렌더링 (Rendering Inline Blade Templates)

원시 Blade 템플릿 문자열을 HTML로 변환해야 할 때가 있습니다. `Blade` 파사드의 `render` 메서드로 처리할 수 있습니다. Blade 템플릿 문자열과, 뷰에 전달할 데이터 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 블레이드를 `storage/framework/views` 디렉터리에 임시 파일로 저장합니다. 렌더 후 임시 파일 삭제를 원한다면 `deleteCachedView` 옵션을 사용하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## 블레이드 프래그먼트 렌더링 (Rendering Blade Fragments)

[Turbbo](https://turbo.hotwired.dev/), [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, HTTP 응답에서 뷰의 일부만 반환할 필요가 있을 수 있습니다. Blade "프래그먼트"로 이 기능을 제공합니다. `@fragment`, `@endfragment` 지시어로 프래그먼트 영역을 감쌉니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

뷰를 반환할 때, `fragment` 메서드로 특정 프래그먼트만 응답에 포함시킬 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드로 조건부 프래그먼트 반환도 가능합니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트를 한 번에 반환하려면, `fragments`, `fragmentsIf` 메서드를 사용합니다:

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
## 블레이드 확장하기 (Extending Blade)

`directive` 메서드로 커스텀 블레이드 지시어를 직접 정의할 수 있습니다. Blade 컴파일러가 해당 지시어를 만나면, 지정한 콜백을 호출하고, 그 안에 표현식을 받을 수 있습니다.

예를 들어, `@datetime($var)` 지시어를 작성해 특정 날짜를 포맷팅해보겠습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

이렇게 정의하면, Blade는 `$var`를 포맷팅하는 PHP를 자동으로 생성합니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 지시어의 코드를 업데이트했다면, 캐시된 Blade 뷰를 반드시 삭제해야 합니다. `view:clear` Artisan 명령으로 캐시를 제거하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 Echo 핸들러 (Custom Echo Handlers)

Blade에서 객체를 "echo"하면, PHP의 [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 매직 메서드가 호출됩니다. 하지만 외부 라이브러리와 같이 `__toString`을 수정할 수 없을 땐, Blade의 `stringable` 메서드로 타입별 커스텀 핸들러를 만들 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 사용합니다:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

정의 후에는 Blade에서 객체를 그대로 출력하면 됩니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문 (Custom If Statements)

단순 조건문에 굳이 `directive`로 복잡한 지시어를 만들기 싫을 땐, `Blade::if`로 커스텀 조건문을 만들 수 있습니다. 예를 들어, 애플리케이션의 기본 "디스크"가 특정 값인지 체크하는 커스텀 조건을 추가해봅니다. `AppServiceProvider`의 `boot`에서 등록하세요:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

등록 후에는 아래와 같이 쓸 수 있습니다:

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```
