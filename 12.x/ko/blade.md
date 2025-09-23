# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드를 더욱 강력하게 만들기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔터티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시문](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시문](#the-once-directive)
    - [Raw PHP 코드](#raw-php)
    - [주석 처리](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약 키워드](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성](#building-layouts)
    - [컴포넌트로 레이아웃 만들기](#layouts-using-components)
    - [템플릿 상속으로 레이아웃 구성](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함되어 있는 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 순수 PHP 코드를 자유롭게 사용할 수 있습니다. 실제로 모든 Blade 템플릿은 순수 PHP 코드로 컴파일된 뒤, 수정 전까지 캐시되기 때문에, 애플리케이션에 사실상 추가적인 오버헤드를 발생시키지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 가지며 주로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 전역 `view` 헬퍼를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰 관련 문서](/docs/12.x/views)에서 언급한 것처럼, `view` 헬퍼의 두 번째 인자를 통해 Blade 뷰에 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드를 더욱 강력하게 만들기

Blade 템플릿을 한 단계 더 업그레이드하여 동적인 인터페이스를 손쉽게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면 React나 Vue 같은 프론트엔드 프레임워크 없이도, 동적 기능이 추가된 Blade 컴포넌트를 작성할 수 있습니다. 따라서 복잡한 빌드 과정이나 클라이언트 렌더링 없이도, 현대적인 리액티브 프론트엔드를 쉽게 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 출력 (Displaying Data)

Blade 뷰에 전달된 데이터를 출력하려면 변수를 중괄호로 감싸서 사용할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해 보겠습니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 템플릿에서 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 처리됩니다.

뷰에 전달된 변수의 내용만 출력할 수 있는 것은 아닙니다. PHP 함수의 결과도 그대로 출력할 수 있습니다. 실제로 Blade 출력 구문 안에는 원하는 어떤 PHP 코드라도 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔터티 인코딩 (HTML Entity Encoding)

Blade(및 Laravel의 `e` 함수)는 기본적으로 HTML 엔터티를 이중 인코딩 처리합니다. 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

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

Blade의 `{{ }}` 문은 기본적으로 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 처리됩니다. 만약 데이터가 이스케이프되지 않고 그대로 출력되길 원한다면, 아래와 같은 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 출력할 때에는 항상 주의해야 합니다. 일반적으로 XSS 공격을 예방하기 위해 이중 중괄호(`{{ }}`) 구문을 사용하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크에서도 중괄호(`{}`)를 사용하여 데이터를 출력합니다. 이때 Blade에서 해당 구문을 변환하지 않길 원한다면, `@` 기호를 앞에 붙여주면 됩니다. 예시:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade가 제거하지만, `{{ name }}` 구문은 그대로 유지됩니다. 따라서 자바스크립트 프레임워크에서 이를 인식해 렌더링할 수 있습니다.

`@` 기호는 블레이드 지시문을 이스케이프할 때도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

뷰에 배열을 전달해 자바스크립트 변수로 사용하고 싶을 때가 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 지시문을 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode`와 동일한 인자를 받지만, 결과 출력 시 HTML 인용부호 내에서 안전하게 이스케이프 처리합니다. 이 메서드는 유효한 자바스크립트 객체로 변환될 수 있도록 문자열 `JSON.parse` 자바스크립트 구문을 반환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel 기본 애플리케이션에는 이 기능을 쉽게 사용하도록 `Js` 파사드가 포함되어 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. 블레이드 템플릿 엔진은 정규 표현식 기반이므로, 복잡한 표현식을 직접 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시문

템플릿의 상당 부분에서 자바스크립트 변수를 출력할 때, 매번 `@` 기호를 붙이는 것이 번거로울 수 있습니다. 이럴 때는 `@verbatim` 지시문으로 해당 HTML 코드를 감싸면 내부의 Blade 출력 구문을 그대로 둘 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시문 (Blade Directives)

템플릿 상속 및 데이터 출력을 비롯해, Blade는 조건문과 반복문 등 자주 사용하는 PHP 제어문을 쉽고 간결하게 사용할 수 있도록 다양한 단축 구문을 제공합니다. 이 지시문들은 PHP와 거의 동일한 방식으로 동작하지만, 더 읽기 쉽고 간결하게 코드를 작성할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시문을 사용해 if 문을 작성할 수 있습니다. 이들 지시문은 PHP의 조건문과 동일하게 동작합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

더 간결하게 쓸 수 있도록 `@unless` 지시문도 제공됩니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

여기에 더해, `@isset` 및 `@empty` 지시문을 사용하면 해당 PHP 함수의 단축 구문을 사용할 수 있습니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있음" 상태입니다...
@endempty
```

<a name="authentication-directives"></a>
#### 인증(Authenticate) 관련 지시문

`@auth`, `@guest` 지시문을 사용하면 현재 사용자가 [인증](https://laravel.com/docs/12.x/authentication)된 상태인지, 게스트인지를 빠르게 확인할 수 있습니다:

```blade
@auth
    // 사용자가 인증된 상태입니다...
@endauth

@guest
    // 사용자가 인증되지 않은(게스트) 상태입니다...
@endguest
```

필요하다면, 인증 시 사용할 가드를 명시할 수도 있습니다:

```blade
@auth('admin')
    // admin 가드로 인증된 상태입니다...
@endauth

@guest('admin')
    // admin 가드로 인증되지 않은 상태입니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 관련 지시문

`@production` 지시문은 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 때 사용할 수 있습니다:

```blade
@production
    // 프로덕션 환경에서만 노출할 내용...
@endproduction
```

특정 환경인지 확인하려면 `@env` 지시문을 사용하세요:

```blade
@env('staging')
    // "staging" 환경에서만 실행됩니다...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서만 실행됩니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션(Section) 관련 지시문

템플릿 상속 섹션에 내용이 있는지 확인하려면 `@hasSection` 지시문을 사용할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

`sectionMissing` 지시문을 사용하면 섹션에 내용이 없는 경우를 확인할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 관련 지시문

`@session` 지시문을 사용해 [세션](/docs/12.x/session) 값이 존재하는지 확인할 수 있습니다. 세션 값이 존재하면, `@session`과 `@endsession` 사이의 템플릿이 렌더링됩니다. 그리고 내부에서 `$value` 변수를 통해 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 관련 지시문

`@context` 지시문을 사용해 [컨텍스트](/docs/12.x/context) 값이 존재하는지 확인할 수 있습니다. 컨텍스트가 있으면 내부 내용을 렌더링하며, `$value`를 통해 컨텍스트 값을 사용할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시문으로 switch 문을 작성할 수 있습니다:

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

조건문뿐만 아니라, Blade는 PHP의 반복문 구조를 위한 간편한 지시문도 제공합니다. 각 지시문은 PHP 반복문과 동일하게 동작합니다:

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
> `foreach` 반복문 내에서는 [loop 변수](#the-loop-variable)를 사용해, 반복문의 첫 번째/마지막 회차 여부 등 여러 유용한 정보를 확인할 수 있습니다.

반복문 내에서 `@continue`와 `@break` 지시문을 사용하여, 현재 반복을 건너뛰거나 루프를 종료할 수 있습니다:

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

`@continue`와 `@break`에 조건식을 바로 넣어줄 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문을 사용할 때, 반복문 내부에서 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복의 인덱스, 첫/마지막 반복 여부 등 유용한 정보를 제공합니다:

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

중첩 반복문 내에서는 `parent` 속성을 통해 상위 반복문의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수는 아래와 같은 다양한 속성을 가지고 있습니다:

<div class="overflow-auto">

| 속성(Property)      | 설명                                                                    |
| ------------------ | ----------------------------------------------------------------------- |
| `$loop->index`     | 현재 반복의 인덱스(0부터 시작).                                        |
| `$loop->iteration` | 현재 반복 횟수(1부터 시작).                                             |
| `$loop->remaining` | 반복이 남아있는 횟수.                                                  |
| `$loop->count`     | 반복 대상 배열의 전체 개수.                                              |
| `$loop->first`     | 반복의 첫 번째 회차 여부.                                               |
| `$loop->last`      | 반복의 마지막 회차 여부.                                                |
| `$loop->even`      | 현재 반복이 짝수번째인지 여부.                                          |
| `$loop->odd`       | 현재 반복이 홀수번째인지 여부.                                          |
| `$loop->depth`     | 현재 반복문의 중첩 수준.                                                |
| `$loop->parent`    | 중첩 반복문 내에서 부모 루프 변수.                                     |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 지시문은 조건에 따라 CSS 클래스를 동적으로 지정할 수 있습니다. 배열 형태로 클래스를 지정하며, 배열의 키가 클래스명, 값이 조건식입니다. 배열의 키가 숫자인 경우, 항상 해당 클래스가 포함됩니다:

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

마찬가지로, `@style` 지시문을 사용해 조건에 따라 인라인 CSS 스타일을 지정할 수 있습니다:

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

다음과 같은 헬퍼 지시문을 사용해 HTML 속성을 간결하게 표현할 수 있습니다.

- `@checked`: 체크박스가 `checked` 상태여야 하는지 표현

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

- `@selected`: 셀렉트 옵션이 선택되어야 하는지 표현

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

- `@disabled`: 해당 요소가 비활성화되어야 하는지 표현

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

- `@readonly`: 해당 요소가 읽기 전용이어야 하는지 표현

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

- `@required`: 해당 필드가 필수 입력값이어야 하는지 표현

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
> `@include` 지시문을 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등에서 더 강력하고 효율적인 기능을 제공합니다.

Blade의 `@include` 지시문을 통해 다른 Blade 뷰를 현재 뷰에 포함할 수 있습니다. 부모 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에서도 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 하위 뷰에, 부모 뷰의 기존 데이터 외 추가 데이터를 전달할 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

만약 존재하지 않는 뷰를 `@include`하려고 하면 에러가 발생합니다. 존재 여부에 따라 뷰를 조건부로 포함해야 할 경우에는 `@includeIf` 지시문을 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

블레이드 표현식이 참일 때만 뷰를 포함하려면 `@includeWhen`, 거짓일 때 포함하려면 `@includeUnless` 지시문을 사용하세요:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에 가장 먼저 존재하는 뷰를 포함하고 싶다면 `includeFirst` 지시문을 사용할 수 있습니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수를 사용하는 것은 피해야 합니다. 이 값들은 캐시된 컴파일 뷰 파일의 경로를 가리키기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

반복문과 포함을 하나의 줄로 결합해서 사용하려면 Blade의 `@each` 지시문을 사용할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

- 첫 번째 인자: 각 요소마다 렌더링할 뷰
- 두 번째 인자: 반복 대상 배열 또는 컬렉션
- 세 번째 인자: 반복 중 각 아이템을 참조할 변수명  
뷰 내에서는 현재 반복의 배열 키를 `key` 변수로도 사용할 수 있습니다.

네 번째 인자로, 컬렉션이 비어있을 때 사용할 뷰를 지정할 수도 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`를 통해 렌더링된 뷰는 부모 뷰의 변수를 상속받지 않습니다. 하위 뷰에서 부모 뷰의 변수가 필요하다면, `@foreach`와 `@include`를 함께 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 지시문

`@once` 지시문을 사용하면 렌더링 사이클 중 특정 블록을 한 번만 평가하도록 할 수 있습니다. 예를 들어, 반복문 안에서 [스택](#stacks) 기능을 이용해 자바스크립트 코드를 한 번만 헤더에 추가하고 싶을 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

자주 함께 쓰이는 `@push` 또는 `@prepend`와 편리하게 쓸 수 있도록 `@pushOnce`와 `@prependOnce` 지시문도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP 코드

특정 상황에서, 뷰 내에 순수 PHP 코드를 삽입해야 할 수 있습니다. 이때는 Blade의 `@php` 지시문으로 PHP 코드를 묶어주면 됩니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스 임포트처럼, PHP 용도로만 사용하는 경우 `@use` 지시문을 사용할 수도 있습니다:

```blade
@use('App\Models\Flight')
```

별칭(alias)을 지정하고 싶다면 두 번째 인자로 지정할 수 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스의 여러 클래스를 한 번에 임포트하는 것도 가능합니다:

```blade
@use('App\Models\{Flight, Airport}')
```

또한, 함수와 상수도 각각 `function` 또는 `const` 키워드를 붙여 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수와 상수에도 별칭(alias)을 부여할 수 있습니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수/상수를 여러 개 묶어서 임포트하는 것도 가능합니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석 처리

Blade는 뷰 내에 주석을 작성할 수 있도록 지원합니다. Blade 주석은 렌더링된 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 최종 HTML에 노출되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, include와 유사한 기능을 제공하지만, 일부 개발자에게는 컴포넌트와 슬롯의 개념이 더 직관적일 수 있습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명 컴포넌트, 두 가지 방식으로 만들 수 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용할 수 있습니다. 간단한 `Alert` 컴포넌트 예시를 들어보겠습니다. 이 명령어를 실행하면 `app/View/Components` 디렉터리에 컴포넌트 클래스가 생성됩니다:

```shell
php artisan make:component Alert
```

명령어 실행 시 컴포넌트 뷰 템플릿도 같이 만들어지며, 이 뷰는 `resources/views/components` 디렉터리에 저장됩니다. 직접 컴포넌트를 작성할 때, 이 경로들에 있는 컴포넌트는 자동으로 인식됩니다.

서브 디렉토리에 컴포넌트를 생성할 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령어 실행 시, `app/View/Components/Forms`에 `Input` 컴포넌트가 생성되고, 뷰는 `resources/views/components/forms`에 저장됩니다.

만약 클래스 없이 Blade 템플릿 파일만 있는 익명 컴포넌트를 만들고 싶다면 `--view` 옵션을 추가하세요:

```shell
php artisan make:component forms.input --view
```

이 명령어를 사용하면 `resources/views/components/forms/input.blade.php` 파일이 생성되고, `<x-forms.input />` 형태로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션 자체 컴포넌트는 위의 디렉토리에서 자동으로 인식됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 만들 때는 컴포넌트 클래스와 태그 별칭을 직접 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 등록합니다:

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

등록 후에는 태그 별칭으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-package-alert/>
```

또한, `componentNamespace` 메서드를 사용하면 컨벤션에 따라 컴포넌트 클래스를 자동 로드할 수 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있을 경우:

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

이후 아래와 같이 벤더 네임스페이스를 붙여 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 명칭을 파스칼 케이스로 변환해 관련 클래스를 자동으로 찾으며, "dot" 표기법을 활용한 하위 디렉터리도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 출력하려면, Blade 뷰 내에서 컴포넌트 태그를 사용하면 됩니다. 태그는 `x-`로 시작하며, 이어서 컴포넌트 클래스명을 케밥 케이스로 사용합니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 하위 디렉터리에 있다면 `.`을 사용해서 표현합니다. 예를 들어, 클래스가 `app/View/Components/Inputs/Button.php`에 있을 경우:

```blade
<x-inputs.button/>
```

컴포넌트 렌더링을 조건부로 제어하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 구현하세요. `shouldRender`가 `false`를 반환하면 컴포넌트가 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더링 여부
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

여러 컴포넌트가 한 그룹을 이루는 경우, 관련된 컴포넌트를 하나의 디렉터리에 모을 수 있습니다. 예를 들어, 아래와 같은 card 컴포넌트 구조를 가정할 수 있습니다:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

`Card`가 디렉터리 이름과 동일하다면, `<x-card.card>`가 아니라 `<x-card>`로 사용할 수 있습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달

Blade 컴포넌트에 HTML 속성 형태로 데이터를 전달할 수 있습니다. 문자열 등 원시 값은 그대로 속성으로 지정하면 되고, PHP 변수나 표현식은 속성 이름 앞에 `:`를 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

모든 데이터 속성은 컴포넌트 클래스의 생성자에서 정의해야 하며, 해당 컴포넌트의 public 속성은 자동으로 뷰에서 사용할 수 있게 됩니다. 데이터를 `render` 메서드에서 뷰로 넘길 필요는 없습니다:

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
     * 컴포넌트 뷰 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트 렌더 시, public 변수는 아래와 같이 그대로 뷰에서 사용할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 이름 표기법(Casing)

컴포넌트 생성자 인자는 `camelCase`로 지정하고, HTML 속성에서는 `kebab-case`로 변환해서 사용해야 합니다. 예를 들어,

```php
/**
 * 컴포넌트 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

다음과 같이 사용할 수 있습니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성(Short Attribute) 문법

속성 이름과 변수명이 일치할 때 단축 문법으로 사용할 수 있습니다:

```blade
{{-- 단축 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일 --}}
<x-profile :user-id="$userId" :name="$name" />
```

속성에 `false`를 전달하려면, 속성 앞에 `!`를 붙이면 됩니다:

```blade
{{-- 단축 문법 --}}
<x-profile !margin />

{{-- 아래와 동일 --}}
<x-profile :margin="false" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JS 프레임워크에서는 콜론이 붙은 속성도 사용합니다. 이때 Blade에 의해 PHP로 해석되지 않게 하려면 속성 앞에 `::`를 붙여줍니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

렌더링 결과:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

public 속성뿐만 아니라 public 메서드도 컴포넌트 뷰에서 사용할 수 있습니다. 예를 들어, `isSelected` 메서드가 있다면,

```php
/**
 * 해당 옵션이 선택됨 상태인지 판별
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 뷰에서 아래와 같이 호출할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내 속성 및 슬롯 접근

컴포넌트 클래스의 `render` 메서드에서, 컴포넌트 이름, 속성, 슬롯 등에 접근할 수 있습니다. 이때는, `render`에서 클로저를 반환하면 됩니다:

```php
use Closure;

/**
 * 컴포넌트 뷰 반환(클로저로)
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

클로저의 인자 `$data`는 아래 정보들을 포함합니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 값을 블레이드 문자열에 직접 삽입해서는 안 됩니다. 악의적인 속성 값으로 인해 원격 코드 실행이 발생할 수 있기 때문입니다.

`componentName`은 `<x-alert />`라면 `'alert'`이 됩니다. `attributes`에는 태그에 지정된 모든 속성이, `slot`에는 슬롯 내용이 담긴 `Illuminate\Support\HtmlString` 인스턴스가 들어 있습니다.

클로저가 반환한 값이 뷰 파일명과 일치하면 자동으로 해당 뷰를 렌더링하고, 그렇지 않으면 블레이드 인라인 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트에서 Laravel [서비스 컨테이너](/docs/12.x/container)가 관리하는 의존성이 필요하다면, 데이터 속성들보다 앞에 나열하세요. 그러면 컨테이너가 자동으로 주입해줍니다:

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
#### 속성/메서드 숨기기

어떤 public 속성이나 메서드를 컴포넌트 뷰에서 노출하지 않으려고 한다면, `$except` 프로퍼티에 배열 형태로 추가하세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출하지 않을 속성/메서드 목록
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
### 컴포넌트 속성

이미 데이터 속성 전달 방법을 알아보았지만, 동적으로 `class`와 같은 HTML 속성을 추가해야 할 때가 많습니다. 이런 속성들은 "attribute bag"에 자동으로 수집되어, 컴포넌트에서 `$attributes` 변수로 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 정의되지 않은 모든 속성은 `$attributes`로 모여, 아래와 같이 뿌릴 수 있습니다:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현재로서는 컴포넌트 태그 내에서 `@env`같은 지시문 사용이 지원되지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 사용할 수 없습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합(Merge) 속성

일부 HTML 속성에 기본값이나 추가 값을 병합해야 할 때가 있습니다. `merge` 메서드를 사용하면, 예를 들어, 항상 적용될 CSS 클래스를 쉽게 지정할 수 있습니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

만약 아래와 같이 사용했다면:

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
#### 조건부 클래스 병합

특정 조건에서만 클래스를 병합하고 싶다면, `class` 메서드를 사용하면 됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

여러 속성을 동시에 병합해야 한다면 `merge` 메서드를 이어서 사용하세요:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 단순 HTML 태그에서만 조건부 클래스를 지정하려면, [@class 지시문](#conditional-classes)을 활용하세요.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class`가 아닌 속성을 `merge`에 지정하면, 이 값은 "기본값"으로 간주됩니다. 그러나 `class`와 달리, 이 속성은 주입된 값에 덮어씌워집니다. 예를 들어, `button` 컴포넌트에서:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

사용 시 다른 `type`이 지정되면 그 값이, 없으면 기본값이 적용됩니다:

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

class가 아닌 속성도 기본값과 주입값이 함께 합쳐지길 원한다면, `prepends` 메서드를 사용할 수 있습니다. 예를 들어, `data-controller` 속성이 기본값으로 `profile-controller`를 항상 갖도록 하면서, 다른 값도 함께 붙이고 싶다면:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 선택

`filter` 메서드를 사용해 필요한 속성만 필터링할 수 있습니다. 콜백에서 true를 반환하면 해당 속성이 유지됩니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

키가 특정 문자열로 시작하는 속성만 가져오려면 `whereStartsWith`를 사용하세요:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, 특정 접두사로 시작하지 않는 속성만 가져오려면 `whereDoesntStartWith`를 사용하세요:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용해 attribute bag의 첫 번째 속성을 얻을 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

속성 존재 여부 판단은 `has` 메서드를 사용하며, 배열을 넘기면 모두 존재하는지, `hasAny`는 하나라도 있으면 true가 반환됩니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif

@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif

@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성의 값을 얻으려면 `get`을 사용하세요:

```blade
{{ $attributes->get('class') }}
```

특정 속성만 골라서 가져오려면 `only`:

```blade
{{ $attributes->only(['class']) }}
```

특정 속성을 제외하려면 `except`:

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약 키워드

일부 키워드는 Blade 내부적으로 사용하므로, 컴포넌트 클래스의 public 속성 또는 메서드명으로 정의할 수 없습니다:

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

컴포넌트에 추가적인 콘텐츠를 전달할 때 "슬롯" 기능을 자주 사용하게 됩니다. 기본 슬롯은 `$slot` 변수로 렌더링됩니다. 예를 들어, 아래와 같은 `alert` 컴포넌트가 있다고 가정합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트를 사용할 때 아래처럼 슬롯을 전달할 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 위치에 서로 다른 슬롯을 삽입하고 싶을 때도 있습니다. 예를 들어, "title" 슬롯을 추가해보겠습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이때는 `x-slot` 태그로 명시적으로 슬롯을 지정할 수 있습니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯에 내용이 있는지 확인하려면 `isEmpty` 메서드를 사용할 수 있습니다:

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

HTML 주석을 제외한 실제 내용이 있는지 확인하려면 `hasActualContent` 메서드를 사용할 수 있습니다:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 범위 슬롯(Scoped Slots)

Vue 등 자바스크립트 프레임워크에서 사용되는 "범위 슬롯"처럼, 슬롯 내에서 컴포넌트의 메서드·속성에 접근하고 싶을 때가 있습니다. 이때 컴포넌트에 public 메서드/속성을 정의하고, 슬롯 내부에서 `$component`로 접근할 수 있습니다:

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

Blade 컴포넌트와 마찬가지로, 슬롯에도 추가 [속성](#component-attributes)(예: CSS 클래스명 등)을 지정할 수 있습니다:

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

슬롯 속성과 상호작용하려면, 슬롯 변수의 attributes 프로퍼티로 접근하면 됩니다. 자세한 방법은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

아주 단순한 컴포넌트라면, 클래스와 뷰 파일을 관리하는 것이 오히려 번거로울 수 있습니다. 이럴 때는 `render` 메서드에서 바로 마크업을 반환할 수 있습니다:

```php
/**
 * 컴포넌트 뷰 반환
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
#### 인라인 뷰 컴포넌트 생성하기

인라인 뷰를 렌더링하는 컴포넌트를 생성할 때는 `--inline` 옵션을 사용합니다:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

컴포넌트명이나 종류가 런타임 시점에 결정되어야 할 때, Laravel의 내장 `dynamic-component` 컴포넌트를 사용할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 컴포넌트 수동 등록 관련 문서는 Laravel 패키지 개발자에게 주로 필요합니다. 일반 애플리케이션 개발 시에는 해당 내용이 크게 중요하지 않을 수 있습니다.

애플리케이션 내에서는 컴포넌트가 자동으로 인식됩니다.

하지만, Blade 컴포넌트를 활용하는 패키지를 개발하거나, 비표준 디렉터리에 컴포넌트를 두는 경우, 컴포넌트 클래스와 태그 별칭을 직접 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 진행합니다:

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

등록 이후 아래처럼 사용할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

`componentNamespace` 메서드를 활용해, 컨벤션에 따라 패키지 컴포넌트 클래스를 자동으로 사용할 수도 있습니다. 예시:

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

이후 다음과 같이 패키지 네임스페이스를 활용해 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트명 파스칼케이스 자동 변환 및 dot 표기법 하위 디렉터리 지원 기능도 제공합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 유사하게, 익명 컴포넌트는 파일 하나로 컴포넌트를 관리할 수 있게 해줍니다. 익명 컴포넌트는 별도의 클래스 없이 뷰 파일만 사용합니다. 예를 들어, `resources/views/components/alert.blade.php` 파일을 만들었다면 바로 아래와 같이 사용할 수 있습니다:

```blade
<x-alert/>
```

컴포넌트가 서브 디렉터리에 있을 경우, `.`으로 중첩을 표현할 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php`라면:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

여러 Blade 템플릿으로 컴포넌트 하나를 구성할 때, 관련 뷰 파일을 하나의 디렉터리에 묶고자 할 수 있습니다. 예를 들어, 아래와 같은 "accordion" 컴포넌트 구조를 생각해 봅시다:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 구조에서는 아래처럼 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

사실상 `x-accordion` 컴포넌트가 디렉터리 안이 아니라 최상위에 있어야 했습니다.  
하지만, Blade에서는 디렉터리명과 동일한 파일명(`accordion/accordion.blade.php`)이 존재하면, 해당 템플릿을 "루트" 컴포넌트로 자동 인식합니다. 그러면 디렉터리 내부에 모든 관련 뷰를 모을 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성 구분

익명 컴포넌트에는 클래스가 없기 때문에, 어떤 속성이 데이터 변수이고, 어떤 속성이 attribute bag에 포함될지 지정해야 합니다. 이를 위해 템플릿 상단에 `@props` 지시문을 사용할 수 있습니다. 기본값을 주고 싶으면 배열 키-값 쌍으로 지정하세요:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 정의했다면, 아래처럼 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

하위 컴포넌트에서 부모 컴포넌트의 데이터를 접근하고 싶을 때는 `@aware` 지시문을 사용합니다. 예를 들어, 메뉴의 색상 정보를 하위 아이템에도 전달하려면:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트(`x-menu`):

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

자식 컴포넌트에서는 아래와 같이 사용합니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시문은 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터만 접근 가능합니다. 부모 컴포넌트의 기본값은 직접 전달하지 않는 한 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

기본적으로 익명 컴포넌트는 `resources/views/components` 디렉터리에 정의됩니다. 그렇지만, 다른 경로나 네임스페이스로 정의하고 싶을 때, Laravel에 경로를 추가로 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 컴포넌트 경로(필수)와 네임스페이스(선택)를 인자로 받으며, 보통 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) `boot` 메서드에서 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

네임스페이스 없이 등록했다면, 해당 경로 내의 컴포넌트는 네임스페이스 없이 사용할 수 있습니다:

```blade
<x-panel />
```

네임스페이스를 지정했다면, 해당 네임스페이스를 붙여서 사용할 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트로 레이아웃 만들기

웹 애플리케이션은 여러 페이지에서 동일한 레이아웃 구조를 공유하는 경우가 많습니다. 모든 뷰마다 똑같은 HTML 레이아웃을 반복하다 보면 관리가 매우 어렵습니다. 이를 방지하기 위해, 하나의 [Blade 컴포넌트](#components)로 레이아웃을 정의해 활용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "todo" 리스트 앱을 만든다고 가정해보겠습니다. 아래와 같이 레이아웃 컴포넌트를 만들 수 있습니다:

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

`layout` 컴포넌트를 만든 뒤, 이를 사용하는 Blade 뷰를 작성합니다. 예를 들어, 작업 목록을 표시하는 tasks 뷰는 아래와 같이 작성할 수 있습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

이렇게 컴포넌트에 삽입한 내용은 `$slot` 변수로 전달됩니다. 만약 레이아웃에서 `$title` 슬롯이 제공되지 않으면 기본값이 적용됩니다. 필요하다면 `x-slot` 구문으로 다른 슬롯을 전달할 수 있습니다:

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

마지막으로, 라우트에서 해당 뷰를 반환하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속으로 레이아웃 구성

<a name="defining-a-layout"></a>
#### 레이아웃 정의

레이아웃은 "템플릿 상속" 방식으로 정의할 수도 있습니다. 이는 [컴포넌트](#components) 도입 이전에 Blade에서 주로 사용하던 방식입니다.

간단한 예제를 살펴보겠습니다. 가장 먼저 페이지 레이아웃 파일을 만듭니다:

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

이 파일은 일반적인 HTML 마크업으로 되어 있지만, `@section`과 `@yield`에 주목하세요.  
- `@section`: 콘텐츠 영역을 정의  
- `@yield`: 해당 영역의 실제 콘텐츠를 출력

이제 이 레이아웃을 상속받는 자식 페이지를 만들어보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장(Extends)

자식 뷰에서는 `@extends` 지시문으로 어떤 레이아웃을 상속받을지 명시합니다. 그리고 `@section` 지시문으로 해당 영역의 콘텐츠를 지정하면 됩니다. 예시:

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

위 예시에서 `sidebar` 섹션은 `@@parent` 지시문을 통해, 레이아웃에 정의된 내용을 덮어쓰지 않고 뒤에 이어서 추가합니다. `@@parent`는 렌더링 시 부모의 것을 대체합니다.

> [!NOTE]
> 이전 예시와 달리, 이 `sidebar` 영역은 `@endsection`으로 끝나며, 이는 영역의 정의만 하고 바로 출력하지 않습니다. 반면 `@show`는 정의와 즉시 출력이 동시에 이뤄집니다.

`@yield` 지시문은 두 번째 인자로 기본값도 받을 수 있습니다. 해당 영역이 정의되지 않았다면 이 값이 출력됩니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때는 [CSRF 보호 미들웨어](/docs/12.x/csrf)가 요청을 검증할 수 있도록, CSRF 토큰 필드를 폼에 반드시 추가해야 합니다. `@csrf` Blade 지시문을 사용하면 토큰 필드를 자동으로 생성해줍니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 기본적으로 `PUT`, `PATCH`, `DELETE` 요청을 보낼 수 없습니다. 그래서 숨겨진 `_method` 필드로 HTTP 메서드를 지정해야 하며, 이를 위해 `@method` Blade 지시문을 사용할 수 있습니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 지시문은 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 특정 속성에 있는지 빠르게 확인할 때 사용할 수 있습니다. 내부에서는 `$message` 변수를 통해 에러 메시지를 출력할 수 있습니다:

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

`@error`는 내부적으로 if 문으로 컴파일되므로, `@else`를 이용해 에러가 없을 때의 출력도 지정할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[에러 백 이름](/docs/12.x/validation#named-error-bags)이 있을 경우, 두 번째 인자로 전달해 사용할 수도 있습니다:

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

Blade는 다양한 뷰/레이아웃에서 특정 스택에 콘텐츠를 push할 수 있게 해줍니다. 주로 자식 뷰에서 필요한 자바스크립트 라이브러리를 지정할 때 활용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 조건이 참일 때만 push하려면 `@pushIf`를 사용할 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

여러 번 push가 가능하며, 스택의 내용을 출력하려면 해당 이름으로 `@stack` 지시문을 사용하세요:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 앞에 콘텐츠를 추가하려면, `@prepend` 지시문을 사용하세요:

```blade
@push('scripts')
    This will be second...
@endpush

// 이후...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입 (Service Injection)

`@inject` 지시문을 통해 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 주입받을 수 있습니다. 첫 번째 인자는 변수명, 두 번째 인자는 서비스의 클래스나 인터페이스 명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 블레이드 템플릿 렌더링

때로는 순수 블레이드 템플릿 문자열을 바로 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 첫 번째 인자는 블레이드 문자열, 두 번째 인자는 데이터 배열입니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 템플릿을 `storage/framework/views` 디렉터리에 임시로 저장합니다. 렌더링 후, 임시 파일을 자동으로 삭제하려면 `deleteCachedView` 인자를 추가하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## 블레이드 프래그먼트 렌더링

[Tubor](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 사용할 때, Blade 템플릿의 일부분만 HTTP 응답에 포함해야 하는 경우가 있습니다. 이럴 때는 Blade "프래그먼트" 기능을 사용할 수 있습니다.  
템플릿에서 일부 구역을 `@fragment`와 `@endfragment`로 감싸세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이후 해당 프래그먼트만 응답에 포함하려면 아래처럼 사용하세요:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건부로 프래그먼트만 반환하고, 아니라면 전체 뷰를 반환하려면 `fragmentIf`를 사용할 수 있습니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트를 한번에 반환하려면 `fragments/fragmentIf` 메서드를 사용하세요:

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

Blade는 직접 커스텀 지시문(directive)을 정의할 수 있도록 `directive` 메서드를 제공합니다. 블레이드 컴파일러가 해당 커스텀 지시문을 만나면, 콜백이 실행되고, 지시문 내부의 식(Expression)이 전달됩니다.

예를 들어, `@datetime($var)` 지시문을 새로 만들어 DateTime 인스턴스를 원하는 형식으로 출력할 수 있습니다:

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

위 예시처럼, 전달받은 변수에 `format` 메서드를 체이닝하여 출력할 수 있습니다. 즉, 실제 생성되는 PHP 코드는 아래와 같습니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> 블레이드 지시문의 로직을 수정한 뒤에는, 캐시된 뷰 파일들을 모두 삭제해야 변경이 반영됩니다. 캐시 삭제는 `view:clear` Artisan 명령어로 수행할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 Echo 핸들러

Blade에서 객체를 출력(에코)하면, PHP의 매직 메서드 [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring)이 호출됩니다. 하지만 서드파티 라이브러리 등 직접 __toString을 변경할 수 없는 경우에는, Blade의 `stringable` 메서드를 통해 특정 타입의 객체를 위한 echo 핸들러를 등록할 수 있습니다.

예시: `Money` 객체를 포맷팅하려면,

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

등록 후, Blade에서 객체를 그냥 출력하면 아래와 같이 동작합니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

간단한 조건문의 경우 복잡한 directive를 직접 정의하는 것보다, Blade가 제공하는 `Blade::if`를 활용할 수 있습니다. 이 메서드는 클로저로 커스텀 조건문 지시문을 빠르게 만들 수 있도록 해줍니다. 예를 들어, 애플리케이션의 디폴트 스토리지가 특정 값인지 확인하는 커스텀 조건문을 만들어보겠습니다:

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

정의 후 아래처럼 쓸 수 있습니다:

```blade
@disk('local')
    <!-- local 디스크를 사용 중인 경우... -->
@elsedisk('s3')
    <!-- s3 디스크를 사용 중인 경우... -->
@else
    <!-- 그 외 디스크를 사용하는 경우... -->
@enddisk

@unlessdisk('local')
    <!-- local 디스크가 아닌 경우... -->
@enddisk
```
