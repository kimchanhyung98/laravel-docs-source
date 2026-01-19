# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔터티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [원시 PHP](#raw-php)
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
    - [컴포넌트 수동 등록하기](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성 지정](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 만들기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러 처리](#validation-errors)
- [스택(Stack)](#stacks)
- [서비스 인젝션(Service Injection)](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 내장된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 순수 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되어, 수정될 때까지 캐시되므로, Blade는 애플리케이션에 거의 부하를 주지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며, 보통 `resources/views` 디렉터리에 보관됩니다.

Blade 뷰는 전역 `view` 헬퍼를 사용하여 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 언급한 대로, 데이터를 `view` 헬퍼의 두 번째 인수로 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강화하기

Blade 템플릿을 한 단계 업그레이드하여 동적 인터페이스를 쉽게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire는 보통 React나 Vue와 같은 프론트엔드 프레임워크를 통해서만 구현할 수 있는 동적 기능을 Blade 컴포넌트에 손쉽게 추가할 수 있습니다. 즉, 복잡한 빌드 과정, 클라이언트 사이드 렌더링, 많은 JavaScript 프레임워크 없이도 현대적인 리액티브 프론트엔드를 만들 수 있는 뛰어난 방법을 제공합니다.

<a name="displaying-data"></a>
## 데이터 표시하기 (Displaying Data)

Blade 뷰에 전달된 데이터를 표시하려면 중괄호로 변수를 감싸서 출력합니다. 예를 들어, 다음과 같은 라우트를 가진다고 가정합니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수를 다음과 같이 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 구문은 XSS(교차 사이트 스크립팅) 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 자동으로 거칩니다.

뷰로 전달된 변수만 표시하는 데 제한되지 않습니다. 어떤 PHP 함수의 결과도 에코로 출력할 수 있습니다. 실제로 Blade 에코 구문에는 원하는 PHP 코드를 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔터티 인코딩 (HTML Entity Encoding)

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔터티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

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
#### 이스케이프되지 않은 데이터 표시

기본적으로 Blade의 `{{ }}` 구문은 PHP의 `htmlspecialchars` 함수로 자동 이스케이프됩니다(XSS 방지). 이스케이프하지 않고 데이터를 출력하려면 다음과 같은 문법을 사용하세요:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력된 데이터를 그대로 에코 출력할 때는 매우 주의해야 합니다. 사용자 데이터 출력에는 항상 이스케이프되는 이중 중괄호 구문(`{{ }}`)을 사용하여 XSS 공격을 방지하세요.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크 (Blade and JavaScript Frameworks)

많은 JavaScript 프레임워크도 중괄호(`{}`)를 사용해 브라우저에 표현식을 표시합니다. 이 경우, Blade 렌더링 엔진이 해당 표현식은 그대로 남겨두도록 `@` 심볼을 사용하세요. 예를 들면:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서 Blade는 `@` 심볼을 제거하고, `{{ name }}` 표현식은 건드리지 않아서 JavaScript 프레임워크가 렌더링할 수 있게 됩니다.

`@` 심볼은 Blade 디렉티브를 이스케이프하는 데도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

뷰에 배열을 전달하고 이를 자바스크립트 변수 초기화 용도로 JSON으로 렌더링하고 싶을 때가 있습니다. 예시:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이렇게 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용하면 더욱 안전하게 HTML 안에 JSON 값을 렌더링할 수 있습니다. `from` 메서드는 PHP의 `json_encode`와 동일한 인수를 받고, JSON 문자열이 HTML 인용부호 안에 들어가도 문제없게 안전하게 이스케이프 처리합니다. 반환값은 `JSON.parse` JavaScript 구문입니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션 스캐폴딩에는 `Js` 파사드가 포함되어 있어, Blade 템플릿에서 더욱 간편하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수나 값을 JSON으로 렌더링하는 용도로만 사용해야 합니다. Blade 템플릿 엔진은 정규 표현식 기반이므로, 복잡한 표현식을 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 넓은 영역에서 JavaScript 표현식(`{{ }}`)을 그대로 출력해야 한다면, 해당 HTML 영역을 `@verbatim` 디렉티브로 감쌀 수 있습니다. 이렇게 하면 일일이 각 에코 구문 앞에 `@`를 붙이지 않아도 됩니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브 (Blade Directives)

템플릿 상속, 데이터 표시 등 외에도 Blade는 조건문이나 반복문과 같은 일반적인 PHP 제어 구조에 대한 간편한 단축 구문을 제공합니다. 이 단축 구문들은 PHP의 구조와 일치하면서도 더 깔끔하고 간결하게 사용할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브로 `if` 조건문을 작성할 수 있습니다. 이 디렉티브들은 PHP의 문법과 동일하게 동작합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 Blade는 `@unless` 디렉티브도 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

또한 PHP 함수와 동일하게, `@isset` 및 `@empty` 디렉티브도 사용할 수 있습니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증(Authenticate) 디렉티브

`@auth` 및 `@guest` 디렉티브를 사용하면 현재 사용자가 [인증](docs/12.x/authentication)되었는지(로그인된 상태) 또는 게스트(비로그인 상태)인지 쉽게 판단할 수 있습니다:

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면, `@auth` 및 `@guest` 디렉티브에 사용할 인증 가드를 지정할 수도 있습니다:

```blade
@auth('admin')
    // 사용자가 인증됨...
@endauth

@guest('admin')
    // 사용자가 인증되지 않음...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 디렉티브

`@production` 디렉티브를 사용해 현재 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // 프로덕션 환경에서만 보이는 내용...
@endproduction
```

`@env` 디렉티브로 특정 환경에서 실행 중인지 판단할 수도 있습니다:

```blade
@env('staging')
    // "staging" 환경에서 실행 중...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서 실행 중...
@endenv
```

<a name="section-directives"></a>
#### 섹션(Section) 디렉티브

템플릿 상속의 섹션에 내용이 있는지 확인하려면 `@hasSection` 디렉티브를 사용할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없는지 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 디렉티브

`@session` 디렉티브를 사용하면, [세션](/docs/12.x/session) 값이 존재하는지 쉽게 확인할 수 있습니다. 값이 존재하면, `@session`부터 `@endsession`까지의 블록이 실행되며 `$value` 변수를 사용해 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 디렉티브

`@context` 디렉티브로 [컨텍스트 값](/docs/12.x/context)의 존재 여부도 확인할 수 있습니다. 값이 있으면 `@context ~ @endcontext` 블록이 실행되며, 내용 안에서 `$value`로 값을 출력할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브로 switch 조건문을 작성할 수 있습니다:

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

조건문 외에도 Blade는 PHP의 반복문 구조와 동일하게 사용할 수 있는 간단한 디렉티브를 제공합니다:

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
> `foreach` 반복문에서는 [loop 변수](#the-loop-variable)를 사용해 반복의 첫/마지막 여부 등 다양한 정보를 확인할 수 있습니다.

반복문에서는 `@continue`와 `@break`로 현재 반복을 건너뛰거나 반복문 자체를 종료할 수 있습니다:

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

조건 자체를 디렉티브에 바로 작성할 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수 (The Loop Variable)

`foreach` 반복문을 돌 때, 반복문 안에서 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복 인덱스, 반복 횟수, 첫 번째/마지막 반복 여부 등 다양한 정보를 제공합니다:

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

중첩된 반복문에서는 부모 반복문의 `$loop` 변수에 `parent` 속성을 통해 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 다양한 속성 목록:

| 속성                | 설명                                                                |
| ------------------ | ------------------------------------------------------------------- |
| `$loop->index`     | 현재 반복의 인덱스(0부터 시작)                                       |
| `$loop->iteration` | 현재 반복의 횟수(1부터 시작)                                         |
| `$loop->remaining` | 반복문에서 남아있는 반복 횟수                                         |
| `$loop->count`     | 반복되는 배열의 전체 아이템 개수                                      |
| `$loop->first`     | 현재 반복이 첫 번째인지 여부                                          |
| `$loop->last`      | 현재 반복이 마지막인지 여부                                          |
| `$loop->even`      | 현재 반복이 짝수 번째인지 여부                                       |
| `$loop->odd`       | 현재 반복이 홀수 번째인지 여부                                       |
| `$loop->depth`     | 반복문의 중첩 수준                                                    |
| `$loop->parent`    | 중첩 반복문에서 부모 반복문의 loop 변수                              |

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 디렉티브는 CSS 클래스 문자열을 조건부로 컴파일합니다. 배열의 키에는 추가하고 싶은 클래스(복수 가능), 값에는 불(bool) 조건식을 넣으면 됩니다. 배열의 키가 숫자인 경우 해당 클래스는 항상 포함됩니다:

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

이와 유사하게, `@style` 디렉티브로 특정 조건에 따라 인라인 CSS 스타일을 추가할 수 있습니다:

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

HTML 체크박스가 "checked" 상태인지 쉽게 표시하려면 `@checked` 디렉티브를 사용할 수 있습니다. 조건이 true이면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, 셀렉트 옵션이 "selected" 상태인지 나타내려면 `@selected` 디렉티브를 사용하세요:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, `@disabled` 디렉티브로 특정 요소를 "disabled" 상태로 표시할 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

`@readonly` 디렉티브는 요소를 읽기 전용으로 만들 수 있습니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

`@required` 디렉티브로 필수(required) 입력란임을 표시할 수 있습니다:

```blade
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
> `@include` 디렉티브도 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩, 재사용성 등 여러 측면에서 `@include`에 비해 많은 이점을 제공합니다.

Blade의 `@include` 디렉티브는 다른 Blade 뷰를 현재 뷰에 포함시킬 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서도 동일하게 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함되는 하위 뷰에 추가로 데이터를 전달하려면, 배열 형태로 넘길 수 도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 포함하려고 하면 Laravel은 에러를 발생시킵니다. 뷰가 존재할 때만 포함하려면 `@includeIf` 디렉티브를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

진위값에 따라 뷰를 포함하고 싶다면 `@includeWhen`, `@includeUnless` 디렉티브를 사용하세요:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

복수 개의 뷰 중 첫 번째로 존재하는 뷰만 포함하려면 `includeFirst` 디렉티브를 사용합니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

부모 뷰의 변수를 상속받지 않고 지정한 데이터만 전달하고 싶다면 `@includeIsolated` 디렉티브를 사용합니다:

```blade
@includeIsolated('view.name', ['user' => $user])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수를 사용하는 것은 권장하지 않습니다. 이 상수들은 캐시된 Blade 파일의 위치를 참조합니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

반복문과 뷰 포함을 한 줄로 결합하려면 Blade의 `@each` 디렉티브를 사용하세요:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 반복마다 렌더링할 뷰, 두 번째는 반복할 배열/컬렉션, 세 번째는 뷰 내부에서 사용할 단일 아이템의 변수명입니다. 반복의 배열 키는 `key` 변수로도 전달됩니다.

배열이 비어 있을 때 렌더링할 뷰를 네 번째 인수로 지정할 수 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속하지 않습니다. 하위 뷰에서 부모 변수가 꼭 필요하다면 `@foreach`와 `@include`를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브는 특정 코드 블록을 렌더링 사이클마다 한 번만 실행되게 합니다. 이는 반복적으로 컴포넌트를 렌더링할 때, 필요한 JavaScript를 단 한 번만 헤더에 삽입해야 할 때 유용합니다. 예를 들어, 반복문에서 동일한 [컴포넌트](#components)를 여러 번 렌더링해도 해당 스크립트를 딱 한 번만 포함하도록 할 수 있습니다:

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 JavaScript...
        </script>
    @endpush
@endonce
```

`@once`와 자주 함께 사용되는 `@push`, `@prepend`를 위한 단축 구문 `@pushOnce`, `@prependOnce`도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 JavaScript...
    </script>
@endPushOnce
```

서로 다른 Blade 템플릿에서 같은 내용을 푸시할 때는 두 번째 인수로 고유 식별자를 지정하세요. 그래야 내용이 단 한 번만 렌더링됩니다:

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
### 원시 PHP (Raw PHP)

상황에 따라 뷰 안에 PHP 코드를 직접 삽입해야 할 수도 있습니다. Blade의 `@php` 디렉티브를 사용해 PHP 블록을 실행할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스만 임포트해야 한다면 `@use` 디렉티브도 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

두 번째 인수로 별칭(alias)을 지정해 임포트할 수 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 하위의 여러 클래스를 한 번에 임포트할 수 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

`function`, `const` 키워드로 PHP 함수와 상수도 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수/상수도 별칭 지정이 가능합니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

그룹 임포트도 지원합니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석 (Comments)

Blade에서는 뷰 내에 주석을 작성할 수 있습니다. HTML 주석과 다르게, Blade 주석은 애플리케이션이 반환하는 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 나타나지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯(Slot)은 섹션, 레이아웃, include와 유사한 이점을 제공하지만, 더 직관적이고 이해하기 쉬운 방식으로 뷰를 관리할 수 있게 해줍니다. 컴포넌트는 클래스 기반과 익명 컴포넌트 방식, 두 가지 접근법이 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` Artisan 명령어를 사용하세요. 예를 들어 `Alert` 컴포넌트를 만든다면 다음과 같습니다:

```shell
php artisan make:component Alert
```

이 명령어는 `app/View/Components` 디렉터리에 컴포넌트를 생성합니다. 뷰 템플릿은 `resources/views/components` 안에 만들어집니다. 자신의 애플리케이션에서 작성하는 컴포넌트는 위 두 디렉터리에서 자동으로 감지되기 때문에, 별도 등록할 필요가 없습니다.

하위 디렉터리에서도 컴포넌트를 생성할 수 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령어는 `app/View/Components/Forms`에 `Input` 컴포넌트를 생성하고, 뷰는 `resources/views/components/forms`에 저장합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자신의 애플리케이션 코드에서 작성하는 컴포넌트는 위에서 설명한 디렉터리에서 자동 감지됩니다.

하지만 Blade 컴포넌트를 포함하는 패키지를 만들 때는 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 패키지용 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록이 완료되면 HTML 태그 별칭으로 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

컨벤션에 따라 `componentNamespace` 메서드로 컴포넌트 클래스를 자동 로드할 수도 있습니다. 예시로, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있고, 네임스페이스가 `Package\Views\Components`라면:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

그러면 아래처럼 vendor 네임스페이스 방식으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환하여 자동으로 해당 클래스를 연결합니다. "dot" 표기법을 써서 하위 디렉터리도 지원됩니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링 (Rendering Components)

컴포넌트를 사용하려면 Blade 템플릿 내에 `x-`로 시작하는 HTML 태그를 작성하세요. 이름은 컴포넌트 클래스명을 케밥케이스로 변환한 것입니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 하위 디렉터리에 있다면 `.`(점)으로 디렉터리 깊이를 표현할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있으면 다음과 같이 렌더링합니다:

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하려면 클래스에 `shouldRender` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 컴포넌트가 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더 여부
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트 (Index Components)

컴포넌트 그룹을 하나의 디렉터리로 묶을 수 있습니다. 예를 들어 "card" 컴포넌트에 대해 다음과 같은 구조를 가질 수 있습니다:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트가 `Card` 디렉터리 내부에 있으면 보통 `<x-card.card>`로 렌더해야 할 것 같지만, 파일명과 디렉터리명이 같을 때, 해당 컴포넌트가 "루트" 컴포넌트로 간주되어 디렉터리명을 반복하지 않아도 됩니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달 (Passing Data to Components)

컴포넌트에 데이터를 전달할 때 HTML 속성을 사용합니다. 상수/문자열 등 단순 값은 HTML 속성으로 전달하면 되고, PHP 변수·표현식은 속성 앞에 `:`을 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트의 생성자(constructor)에서 필요한 데이터를 모두 선언합니다. 컴포넌트의 퍼블릭 속성은 자동으로 뷰에 전달됩니다. 데이터를 뷰로 수동 전달할 필요가 없습니다:

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
     * 컴포넌트 뷰/내용 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트 렌더 시에는 퍼블릭 변수명을 그대로 에코해서 사용할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이싱(Casing)

컴포넌트의 생성자 인수는 `camelCase`로, HTML 속성은 `kebab-case`로 표기합니다. 예를 들어, 다음과 같은 생성자가 있을 때:

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

컴포넌트 사용 시 다음과 같이 전달할 수 있습니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 단축 문법

컴포넌트의 속성 전달 시, 변수명과 속성명이 같다면 "속성 단축 문법"을 사용할 수 있습니다:

```blade
{{-- 단축 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일함 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같이 `:` 접두사를 쓰는 프레임워크와 충돌하지 않게 하려면, 속성에 `::`를 붙여 Blade가 PHP 표현식이 아님을 알릴 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade가 아래와 같이 HTML을 렌더링합니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트의 퍼블릭 메서드도 템플릿에서 변수 호출하듯 사용할 수 있습니다. 예를 들어, `isSelected`라는 메서드를 가진 컴포넌트라면:

```php
/**
 * 옵션이 현재 선택된 항목인지 판별
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

템플릿에서 다음과 같이 호출합니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스에서 속성 및 슬롯 접근

컴포넌트 클래스 `render` 메서드에서 컴포넌트 이름, 속성(attribute), 슬롯(slot) 정보에 접근하고 싶다면, `render` 메서드에서 클로저(익명 함수)를 반환해야 합니다:

```php
use Closure;

/**
 * 컴포넌트 뷰/내용 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

반환되는 클로저는 `$data` 배열을 인수로 받을 수 있습니다. 배열에는 아래와 같은 요소들이 있습니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열 요소를 Blade 문자열에 직접 삽입하면, 악의적인 속성값을 통해 원격 코드 실행이 발생할 수 있으므로 절대 직접 삽입하지 마세요.

`componentName`은 HTML 태그에서 `x-` 를 뺀 컴포넌트 이름이고, `attributes`는 전달된 모든 HTML 속성, `slot`은 슬롯 내용(`Illuminate\Support\HtmlString` 인스턴스)입니다.

클로저는 문자열을 반환해야 합니다. 반환된 문자열이 실제 뷰라면 해당 뷰가 렌더링되고, 아니라면 인라인 Blade 뷰로 처리됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트에 Laravel [서비스 컨테이너](/docs/12.x/container)의 의존 객체가 필요하면, 생성자에서 데이터 속성 앞에 선언하세요. 컨테이너가 자동으로 의존성을 주입합니다:

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
#### 속성·메서드 감추기

퍼블릭 메서드나 속성 중 뷰에 노출하지 않으려면, `$except` 배열 속성에 이름을 나열하면 됩니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출되지 않아야 하는 속성/메서드
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

컴포넌트에 데이터 속성을 전달하는 방법은 앞서 살펴보았습니다. 그러나 종종 컴포넌트의 동작과 직접 관련 없는 HTML 속성(예: `class`) 같은 추가 속성을 전달해야 할 때가 있습니다. 이런 속성들은 보통 컴포넌트의 루트 요소에 내려주기를 원합니다. 아래 예시를 봅시다:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 정의되지 않은 모든 속성은 자동으로 "속성 가방(attribute bag)"에 모아져 `$attributes` 변수로 컴포넌트에서 사용할 수 있습니다. 컴포넌트에서 해당 속성을 출력하려면 다음과 같이 하면 됩니다:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 안에서는 `@env`와 같은 Blade 디렉티브를 사용할 수 없습니다. 예를 들어 `<x-alert :live="@env('production')"/>` 는 지원되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본/병합된 속성

기본값을 지정하거나 특정 속성을 무조건 추가하는 등의 처리가 필요하다면, 속성 가방의 `merge` 메서드를 사용할 수 있습니다. 특히 항상 적용할 기본 CSS 클래스를 지정할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 다음과 같이 사용할 경우:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링되는 HTML은 다음과 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 클래스를 병합하고 싶다면, `class` 메서드를 사용하세요. 배열의 키에 추가할 클래스(여러 개 가능), 값에 불리언 조건식을 넣습니다. 키가 숫자라면 항상 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

속성 병합이 더 필요하다면 `merge` 메서드를 체이닝하세요:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 클래스 명을 조건부로 컴파일해야 하는 경우, [@class 디렉티브](#conditional-classes)를 사용할 수도 있습니다.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class` 외 속성 병합 시, `merge`로 지정된 값이 기본값이 되며, 주입된 값과 병합되지 않고 항상 덮어쓰기(override) 됩니다. 예를 들어, `button` 컴포넌트가 다음과 같이 구현되어 있을 때:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

이 컴포넌트를 속성 없이 사용하면 기본값이 적용되고, 명시적으로 지정하면 그 값이 사용됩니다:

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

`class` 이외의 속성도 값 병합(이어붙이기)이 필요하다면 `prepends` 메서드를 사용할 수 있습니다. 예를 들어, `data-controller` 속성에 무조건 `profile-controller`가 먼저 오게 하고 싶다면:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 추출

속성을 필터링하려면 `filter` 메서드를 사용할 수 있습니다. 이 메서드는 true를 반환할 경우 속성이 유지됩니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith` 메서드는 키가 지정한 문자열로 시작하는 속성만 추출합니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, `whereDoesntStartWith`는 해당 문자열로 시작하지 않는 속성만 추출합니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 속성 가방에서 첫 번째 속성을 출력할 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성이 존재하는지 확인하려면 `has` 메서드를 사용하세요:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열을 넘기면 모든 속성의 존재 여부를 확인합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny` 메서드를 사용하면 주어진 속성 중 하나라도 존재하는지 확인합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성 값을 얻으려면 `get` 메서드를 사용하세요:

```blade
{{ $attributes->get('class') }}
```

특정 속성만 남기려면 `only`, 제외하려면 `except`를 사용할 수 있습니다:

```blade
{{ $attributes->only(['class']) }}

{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade의 내부 동작에 사용되는 일부 예약어는 컴포넌트에서 퍼블릭 속성 또는 메서드 이름으로 사용할 수 없습니다:

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯(Slots) (Slots)

컴포넌트에 추가 콘텐츠를 전달하려면 "슬롯(Slot)"을 사용할 수 있습니다. 슬롯은 `$slot` 변수로 출력합니다. 예를 들어, `alert` 컴포넌트의 마크업이 다음과 같을 때:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

아래처럼 내용을 슬롯에 전달할 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 개의 슬롯이 필요한 경우에는 슬롯명을 명시하고, 명시되지 않은 부분은 기본 `$slot`으로 전달됩니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯은 `x-slot` 태그로 지정합니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯의 `isEmpty` 메서드를 사용해 내용 유무를 판단할 수 있습니다:

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

실제 HTML 주석이 아니라 진짜 콘텐츠가 포함되어 있는지 확인하려면 `hasActualContent` 메서드를 사용하세요:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯(Scoped Slots)

Vue 등에서 볼 수 있는 스코프드 슬롯처럼, 슬롯 내부에서 컴포넌트의 데이터나 메서드를 접근할 수 있습니다. 이를 위해 컴포넌트에 퍼블릭 메서드나 속성을 선언한 후, 슬롯 내부에서 `$component` 변수를 활용하면 됩니다. 예를 들어, `x-alert` 컴포넌트에 `formatAlert` 메서드가 있을 때:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성 (Slot Attributes)

슬롯에도 CSS 클래스 같은 [속성](#component-attributes)을 지정할 수 있습니다:

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

슬롯 속성에 접근하려면 슬롯 변수의 `attributes` 프로퍼티를 이용하세요. 자세한 속성 활용 방식은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

컴포넌트가 매우 단순하다면 클래스와 뷰 파일을 별도로 유지하는 것이 번거로울 수 있습니다. 이럴 땐 `render` 메서드에서 마크업을 직접 반환할 수 있습니다:

```php
/**
 * 컴포넌트 뷰/내용 반환
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

인라인 뷰 컴포넌트를 만들려면 `make:component` 명령어 실행 시 `--inline` 옵션을 사용하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트 (Dynamic Components)

실행 시점에 렌더링할 컴포넌트가 동적으로 결정될 수도 있습니다. 그런 경우, Laravel의 내장 `dynamic-component` 컴포넌트를 사용하세요:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록하기 (Manually Registering Components)

> [!WARNING]
> 이 부분은 주로 Laravel 패키지를 작성할 때 관련이 있습니다. 일반적인 애플리케이션 작성자는 대개 신경 쓸 필요가 없습니다.

자신의 애플리케이션에서 작성한 컴포넌트는 지정된 디렉터리에서 자동으로 감지되므로 별도 등록이 필요 없습니다.

하지만 패키지를 제작하거나, 컨벤션이 아닌 위치에 컴포넌트를 둘 때는 Blade에 컴포넌트 클래스를 직접 등록해 두어야 합니다. 보통 서비스 프로바이더의 `boot` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록 후에는 다음처럼 사용하면 됩니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

`componentNamespace` 메서드를 사용하면 네임스페이스 기준 컴포넌트 클래스 오토로딩이 가능합니다. 예를 들어 `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있고 네임스페이스가 `Package\Views\Components`이면 다음과 같이 설정합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

그러면 vendor 네임스페이스로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환하여 알아서 클래스를 찾습니다. "dot" 표기법으로 하위 디렉터리에도 대응합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 유사하게, 익명 컴포넌트는 단일 파일로 컴포넌트를 관리할 수 있게 해줍니다. 익명 컴포넌트는 별도의 클래스 없이 뷰 파일만으로 정의됩니다. 예를 들어 `resources/views/components/alert.blade.php`에 컴포넌트를 만들었다면 다음과 같이 사용할 수 있습니다:

```blade
<x-alert/>
```

컴포넌트가 `components` 폴더 안쪽에 중첩되어 있다면, 점(`.`) 표기법으로 렌더링합니다. 예를 들어 `resources/views/components/inputs/button.blade.php` 라면:

```blade
<x-inputs.button/>
```

Artisan을 이용해 익명 컴포넌트를 생성하려면 `--view` 플래그를 사용하세요:

```shell
php artisan make:component forms.input --view
```

이 명령어는 `resources/views/components/forms/input.blade.php` 파일을 생성하며 `<x-forms.input />` 형태로 렌더링할 수 있습니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트 (Anonymous Index Components)

하나의 컴포넌트가 여러 Blade 파일로 구성되면, 디렉터리로 묶어 관리할 수 있습니다. 예를 들어, "accordion" 컴포넌트는 다음과 같이 구조화할 수 있습니다:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 구조에서 `accordion` 과 `item` 컴포넌트를 아래와 같이 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

이전에 위와 같은 마크업을 사용하려면 디렉터리 최상단에 인덱스 템플릿을 두어야 했지만, Blade는 디렉터리명과 동일한 파일이 있는 경우, 그 파일을 "루트" 컴포넌트로 인식하여 디렉터리 안에 템플릿을 둘 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성 지정 (Data Properties / Attributes)

익명 컴포넌트는 별도 클래스가 없으므로, 어떤 데이터가 컴포넌트 변수로 전달되고, 어떤 값이 속성 가방에 저장되는지 구분할 방법이 없습니다. 이를 위해 Blade 템플릿 상단에서 `@props` 디렉티브로 변수명을 명시합니다. 나머지 속성은 자동으로 속성 가방에 들어갑니다. 기본값도 지정 가능합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 사용할 때는 다음과 같이 작성할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근 (Accessing Parent Data)

자식 컴포넌트에서 부모 컴포넌트의 데이터를 사용하고 싶을 때는 `@aware` 디렉티브를 사용할 수 있습니다. 예를 들어, 아래처럼 `<x-menu>`와 `<x-menu.item>` 구조일 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트는 다음과 같이 구현합니다:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` 속성은 부모에만 있으므로 원래는 자식에서 접근할 수 없습니다. 하지만 자식에서 `@aware`를 사용하면 부모의 값을 물려받을 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 부모에 명시적으로 HTML 속성으로 전달된 데이터만 접근 가능합니다. 부모의 `@props` 기본값 등, 명시적으로 전달되지 않은 데이터는 가져올 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로 (Anonymous Component Paths)

익명 컴포넌트는 보통 `resources/views/components` 내에 두지만, 추가로 익명 컴포넌트 경로를 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인수로 경로, 두 번째 인수로 네임스페이스(선택)를 받습니다. 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) `boot` 메서드에서 호출하면 됩니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

네임스페이스 없이 경로를 등록하면, 그 경로에 있는 컴포넌트는 접두사 없이 바로 렌더링 가능합니다:

```blade
<x-panel />
```

네임스페이스를 두 번째 인수로 지정하면, 해당 네임스페이스로 접두어를 붙여 컴포넌트를 렌더링할 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 만들기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃 (Layouts Using Components)

대부분의 웹 애플리케이션은 여러 페이지에 걸쳐 동일한 기본 레이아웃을 가집니다. 모든 뷰에 일일이 전체 레이아웃 코드를 반복 작성하는 것은 유지보수를 어렵게 합니다. 다행히 Blade에서는 일반 [컴포넌트](#components) 하나로 레이아웃을 정의하고, 애플리케이션 전체에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "todo" 리스트 애플리케이션을 만든다고 가정하면, 레이아웃 컴포넌트는 다음과 같을 수 있습니다:

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

레이아웃 컴포넌트가 준비되면, 해당 컴포넌트를 사용하는 뷰를 만듭니다. 예를 들어, 할 일 리스트를 출력하는 뷰는 다음과 같을 수 있습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 전달된 내용은 `layout` 컴포넌트의 기본 `$slot`에 들어갑니다. 또한, `$title` 슬롯이 주어지면 해당 제목을, 없으면 기본 제목을 사용하도록 했습니다. 할 일 리스트 뷰에서 아래처럼 제목 슬롯을 지정할 수도 있습니다:

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

이제 레이아웃과 할 일 리스트 뷰가 준비됐으니, 해당 뷰를 라우트에서 반환하면 됩니다:

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

레이아웃은 "템플릿 상속" 기능으로도 만들 수 있습니다. 컴포넌트가 소개되기 전에는 이 방식이 표준이었습니다.

우선 간단한 예시로, 기본적인 페이지 레이아웃을 만들어봅시다. 여러 페이지에서 재사용할 레이아웃을 하나의 Blade 뷰로 정의합니다:

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

여기에서 주목해야 할 디렉티브는 `@section`과 `@yield`입니다. `@section`은 콘텐츠의 구역을 정의하고, `@yield`는 해당 구역의 콘텐츠를 보여주는 역할을 합니다.

이제 레이아웃을 상속받는 자식 페이지를 만들어 봅시다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

자식 뷰에서는 `@extends` Blade 디렉티브로 확장할 레이아웃을 지정합니다. `@section`으로 각 영역의 내용을 채우면, 레이아웃의 `@yield` 부분에 표시됩니다:

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

여기에서 `sidebar` 영역에서는 `@@parent` 디렉티브를 사용해 기존 내용을 그대로 두고, 그 뒤에 추가 내용을 붙였습니다. `@@parent`는 렌더 시 레이아웃의 해당 영역 내용으로 대체됩니다.

> [!NOTE]
> 위 예제와 달리, `sidebar` 영역은 `@show`가 아닌 `@endsection`으로 끝납니다. `@endsection`은 섹션만 정의하며, `@show`는 섹션을 정의하고 **즉시 출력**합니다.

`@yield` 디렉티브는 두 번째 인수로 기본값을 받을 수 있습니다. 해당 섹션이 정의되지 않으면 기본값이 렌더링됩니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드 (CSRF Field)

HTML 폼을 작성할 때는 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 유효성 검증할 수 있도록, 반드시 숨겨진 CSRF 토큰 필드를 포함해야 합니다. `@csrf` Blade 디렉티브를 사용하면 필드를 쉽게 삽입할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드 (Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 할 수 없습니다. 따라서 이 메서드를 흉내내려면 `_method` 필드를 추가해야 합니다. `@method` Blade 디렉티브가 이 작업을 도와줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러 처리 (Validation Errors)

`@error` 디렉티브로 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 존재하는지 쉽게 확인할 수 있습니다. `@error` 디렉티브 안에서는 `$message` 변수를 에코해 에러 메시지를 출력할 수 있습니다:

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

`@error` 디렉티브는 내부적으로 "if"문으로 컴파일되므로, `@else`문을 사용해 에러가 없을 때 다른 내용을 렌더할 수도 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[에러 백 이름](/docs/12.x/validation#named-error-bags)이 필요한 경우, 두 번째 인수로 에러 백 이름을 전달하면 됩니다:

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
## 스택(Stack) (Stacks)

Blade는 명명된 스택에 콘텐츠를 push하여, 다른 뷰나 레이아웃에서 원하는 위치에 렌더할 수 있습니다. 이는 자식 뷰에서 필요한 JavaScript 라이브러리를 선언할 때 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

진위값에 따라 조건부로 push하려면 `@pushIf` 디렉티브를 사용하세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

여러 번 push해도 누적되며, stack의 내용을 모두 출력하려면 `@stack('스택명')` 디렉티브를 사용합니다:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 맨 앞에 내용을 추가하려면 `@prepend` 디렉티브를 사용합니다:

```blade
@push('scripts')
    This will be second...
@endpush

// 나중에...

@prepend('scripts')
    This will be first...
@endprepend
```

스택이 비었는지 확인하려면 `@hasstack` 디렉티브를 사용하세요:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
## 서비스 인젝션 (Service Injection)

`@inject` 디렉티브로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 주입 받을 수 있습니다. 첫 번째 인수는 뷰에서 사용할 변수명, 두 번째 인수는 서비스 클래스 혹은 인터페이스명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링 (Rendering Inline Blade Templates)

가끔은 Blade 템플릿 문자열을 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 첫 번째 인수는 템플릿 문자열, 두 번째는 뷰에 전달할 데이터(옵션)입니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉토리에 저장하여 렌더링합니다. 렌더링 후 임시 파일을 바로 삭제하고 싶다면 `deleteCachedView` 인수를 전달하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링 (Rendering Blade Fragments)

[Tubro](https://turbo.hotwired.dev/), [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 사용할 경우, HTTP 응답에서 Blade 템플릿의 일부만 반환해야 할 때가 있습니다. Blade "프래그먼트" 기능이 이를 지원합니다. 템플릿의 특정 영역을 `@fragment ~ @endfragment`로 감싸세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이제 뷰를 렌더링할 때 `fragment` 메서드로 특정 프래그먼트만 반환할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 조건에 따라 전체 뷰 대신 일부 프래그먼트만 반환할 수 있습니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`, `fragmentsIf` 메서드는 여러 프래그먼트를 동시에 반환합니다. 프래그먼트들은 서로 붙여서 반환됩니다:

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

Blade는 `directive` 메서드를 통해 커스텀 디렉티브를 직접 정의할 수 있습니다. Blade 컴파일러가 해당 디렉티브를 만나면, 여러분이 제공한 콜백에서 정의한 코드를 생성합니다.

예를 들어, `@datetime($var)` 디렉티브를 만들어 `$var`(DateTime 인스턴스)를 원하는 포맷으로 출력하려면:

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

이 예시에서는, 전달받은 값을 `format` 메서드와 함께 PHP로 출력합니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 후에는 캐시된 Blade 뷰를 **반드시** 삭제해야 합니다. 캐시는 `view:clear` Artisan 명령어로 지울 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러 (Custom Echo Handlers)

Blade에서 오브젝트를 에코 출력하면 그 객체의 `__toString` 메서드가 호출됩니다. 하지만 외부 패키지 등에서 `__toString`을 제어할 수 없을 때가 있습니다.

이럴 때는 Blade의 `stringable` 메서드로 특정 타입의 오브젝트에 대해 커스텀 에코 핸들러를 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 사용합니다:

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

등록 후에는 Blade 템플릿에서 해당 객체를 그대로 에코할 수 있습니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문 (Custom If Statements)

새로운 디렉티브까지 만들 필요 없는 간단한 커스텀 조건문은 `Blade::if` 메서드를 활용할 수 있습니다. 예를 들어, 애플리케이션의 기본 "disk"를 확인하는 커스텀 조건을 만든다고 가정해 보겠습니다. `AppServiceProvider`의 `boot` 메서드에서 등록합니다:

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

커스텀 조건문은 템플릿에서 아래와 같이 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 로컬 디스크 사용 중... -->
@elsedisk('s3')
    <!-- s3 디스크 사용 중... -->
@else
    <!-- 그 외 디스크 사용 중... -->
@enddisk

@unlessdisk('local')
    <!-- 로컬 디스크 사용 중이 아님... -->
@enddisk
```
