# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Blade를 Livewire로 강화하기](#supercharging-blade-with-livewire)
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
    - [순수 PHP 사용](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링하기](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약된 키워드](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 프로퍼티 / 속성](#data-properties-attributes)
    - [부모 데이터 참조](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 오류](#validation-errors)
- [스택(stacks)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 탑재된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 안에서 순수 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로 Blade의 모든 템플릿은 순수 PHP 코드로 컴파일되고, 변경될 때까지 캐시에 저장되어 애플리케이션에 부담을 거의 주지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며, 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 통해 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 설명한 대로, `view` 헬퍼의 두 번째 인수를 사용하여 Blade 뷰에 데이터를 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Blade를 Livewire로 강화하기

Blade 템플릿을 한 단계 업그레이드하고 손쉽게 동적인 인터페이스를 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면 React나 Vue와 같은 프론트엔드 프레임워크에서나 가능했던 동적 기능을 갖춘 Blade 컴포넌트를 작성할 수 있습니다. 라이브와이어는 복잡한 설정, 클라이언트 사이드 렌더링, 빌드 단계를 거치지 않고도 현대적인 반응형 프론트엔드를 손쉽게 구축할 수 있게 해줍니다.

<a name="displaying-data"></a>
## 데이터 표시하기 (Displaying Data)

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있다면:

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
> Blade의 `{{ }}` 에코 구문은 XSS 공격을 막기 위해 PHP의 `htmlspecialchars` 함수로 자동 처리됩니다.

뷰에 전달된 변수의 내용만 표시하는 것에 제한되지 않고, PHP 함수의 결과를 에코로 내보낼 수도 있습니다. 실제로, Blade 에코 구문 내부에는 원하는 PHP 코드를 자유롭게 쓸 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔터티 인코딩 (HTML Entity Encoding)

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔터티를 이중으로 인코딩합니다. 만약 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

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
#### 이스케이프되지 않은 데이터 표시하기

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 처리됩니다. 이스케이프하지 않고 데이터를 출력하고 싶다면 아래 구문을 사용하면 됩니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자로부터 입력받은 데이터를 이스케이프하지 않고 출력할 때는 매우 주의해야 합니다. 사용자 입력값을 표시할 때에는 항상 이스케이프된 중괄호(`{{ }}`) 문법을 사용하는 것이 XSS 공격을 막는 데 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크 (Blade and JavaScript Frameworks)

많은 JavaScript 프레임워크도 "중괄호" 구문(예: `{{ name }}`)을 사용하여 표현식을 브라우저에 출력합니다. 이 경우 Blade 렌더링 엔진에게 해당 표현식을 건드리지 않도록 `@` 기호를 접두어로 붙여 사용할 수 있습니다.

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서, Blade는 `@` 기호만 제거하고 `{{ name }}` 표현식은 그대로 두어 JavaScript 프레임워크가 처리할 수 있도록 합니다.

또한, `@` 기호는 Blade 디렉티브를 이스케이프할 때도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링하기

뷰에 배열을 전달하고 이를 JSON 형태로 변환하여 JavaScript 변수를 초기화하고 싶은 경우가 있습니다.

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이처럼 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받아들이며, HTML 따옴표 내에 안전하게 사용할 수 있도록 JSON 문자열을 올바르게 이스케이프 처리합니다. 반환되는 값은 JavaScript의 `JSON.parse` 형태로, 주어진 객체나 배열을 올바른 JavaScript 객체로 변환합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 버전의 Laravel 애플리케이션 스켈레톤에는 이 기능을 Blade 템플릿에서 편리하게 사용할 수 있는 `Js` 파사드가 포함되어 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿 엔진은 정규 표현식 기반으로 동작하므로, 복잡한 표현식을 디렉티브에 직접 전달하면 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 상당 부분에 JavaScript 변수가 존재한다면, 매번 Blade 에코 구문에 `@` 기호를 붙이지 않고도 `@verbatim` 디렉티브로 HTML 전체를 감쌀 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브 (Blade Directives)

템플릿 상속 및 데이터 표시뿐 아니라, Blade는 조건문과 반복문 등의 일반적인 PHP 제어문을 쉽게 사용할 수 있도록 편리한 단축 구문도 제공합니다. 이 단축 구문은 PHP의 본래 문법과 매우 유사하여 익숙하게 사용할 수 있으면서도 코드를 간결하게 만들어 줍니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용하여 if 문을 작성할 수 있습니다. 이 디렉티브는 PHP의 if 문과 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

추가로, Blade는 `@unless` 디렉티브도 제공합니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

또한, `@isset` 및 `@empty` 디렉티브로 PHP의 `isset`, `empty` 함수와 동일한 기능을 사용할 수 있습니다.

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증(Authorization) 디렉티브

`@auth` 및 `@guest` 디렉티브를 사용하면 현재 사용자가 [인증되어 있는지](/docs/12.x/authentication) 또는 게스트인지 빠르게 확인할 수 있습니다.

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

필요하다면, `@auth` 및 `@guest` 디렉티브 사용시 인증 가드(guard)를 지정할 수 있습니다.

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 디렉티브

`@production` 디렉티브로 애플리케이션이 운영 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // Production specific content...
@endproduction
```

또는, `@env` 디렉티브로 특정 환경에서 실행 중인지 판별할 수 있습니다.

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a name="section-directives"></a>
#### 섹션(Section) 디렉티브

템플릿 상속에서 섹션에 컨텐츠가 존재하는지 확인할 때 `@hasSection` 디렉티브를 사용할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

`sectionMissing` 디렉티브로 특정 섹션이 비어있는지도 확인할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 디렉티브

`@session` 디렉티브를 사용하면 [세션](/docs/12.x/session) 값이 존재하는지 확인할 수 있습니다. 세션 값이 존재하면, `@session`과 `@endsession` 디렉티브로 감싼 템플릿이 평가됩니다. 그 내부에서는 `$value` 변수를 에코하여 세션 값을 표시할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 디렉티브

`@context` 디렉티브는 [컨텍스트](/docs/12.x/context) 값이 존재하는지 확인할 때 사용할 수 있습니다. 컨텍스트 값이 존재하면, `@context`과 `@endcontext` 디렉티브로 감싼 템플릿이 평가됩니다. 내부에서는 `$value` 변수를 에코하여 컨텍스트 값을 표시할 수 있습니다.

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용하여 switch 문을 작성할 수 있습니다.

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

조건문 외에도, Blade는 PHP의 반복문을 위한 간편한 디렉티브를 제공합니다. 이들 디렉티브 또한 PHP 본연의 반복문과 완전히 동일하게 동작합니다.

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
> `foreach` 루프를 사용할 때는 [loop 변수](#the-loop-variable)를 사용해, 현재 반복이 첫 번째 또는 마지막 순회인지 등의 정보를 얻을 수 있습니다.

반복문 사용 시 `@continue`와 `@break` 디렉티브로 현재 순회를 건너뛰거나 반복문을 종료할 수 있습니다.

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

또한, 디렉티브 선언부에 조건식을 곧바로 포함시킬 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### loop 변수

`foreach` 반복 중에는 `$loop`라는 변수가 제공됩니다. 이 변수로 반복문의 인덱스, 첫 번째/마지막 반복 여부 등 다양한 정보를 얻을 수 있습니다.

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

중첩된 반복문에서는 `parent` 속성을 통해 부모 반복문의 `$loop` 변수에 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 아래와 같은 여러 속성이 있습니다.

<div class="overflow-auto">

| 속성                  | 설명                                                      |
| ----------------------| -------------------------------------------------------- |
| `$loop->index`        | 현재 반복의 인덱스(0부터 시작)                          |
| `$loop->iteration`    | 현재 반복 횟수(1부터 시작)                              |
| `$loop->remaining`    | 반복이 남은 횟수                                         |
| `$loop->count`        | 반복 중인 배열의 총 아이템 수                            |
| `$loop->first`        | 반복의 첫 번째 순회 여부                                 |
| `$loop->last`         | 반복의 마지막 순회 여부                                  |
| `$loop->even`         | 반복이 짝수 번째 순회인지 여부                           |
| `$loop->odd`          | 반복이 홀수 번째 순회인지 여부                           |
| `$loop->depth`        | 현재 반복의 중첩 레벨                                    |
| `$loop->parent`       | 중첩 반복문에서의 부모 loop 변수                        |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 디렉티브를 사용하면 CSS 클래스를 조건부로 적용할 수 있습니다. 이 디렉티브는 클래스 이름을 key로 하고, boolean 값을 value로 하는 배열을 인수로 받습니다. key가 숫자인 경우는 항상 클래스 목록에 포함됩니다.

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

마찬가지로 `@style` 디렉티브를 이용해 CSS 인라인 스타일도 조건부로 추가할 수 있습니다.

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

HTML 체크박스 input이 "checked" 상태인지 간단하게 표시할 때는 `@checked` 디렉티브를 사용할 수 있습니다. 이 디렉티브는 조건식이 `true`로 평가될 경우 `checked`를 출력합니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

유사하게, select option이 "selected" 되어야 하는지 나타내려면 `@selected` 디렉티브를 사용할 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한 `@disabled` 디렉티브로 해당 엘리먼트가 "disabled" 되어야 하는지도 표시할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

더불어 `@readonly` 디렉티브를 사용하여 요소가 "readonly" 상태인지 지정할 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

또한 `@required` 디렉티브를 사용하면 요소가 "required" 되어야 하는지도 지정할 수 있습니다.

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
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, Blade의 [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 장점을 제공하므로 가능한 컴포넌트 사용을 권장합니다.

Blade의 `@include` 디렉티브는 한 Blade 뷰에서 다른 Blade 뷰를 손쉽게 포함할 수 있게 해줍니다. 부모 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에도 그대로 전달됩니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰가 부모 뷰의 모든 데이터를 상속받지만, 별도로 추가 데이터를 배열로 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include` 하면 Laravel은 에러를 발생시킵니다. 만약 뷰가 존재하지 않을 수도 있는 경우, `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

Boolean 조건식에 따라 뷰를 포함하려면 `@includeWhen` 또는 `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 첫 번째로 존재하는 뷰만 포함하려면 `includeFirst` 디렉티브를 사용하세요.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__` 및 `__FILE__` 상수는 사용을 지양해야 합니다. 이들은 캐시된 컴파일 뷰의 경로를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

Blade의 `@each` 디렉티브를 사용하면 반복문과 include를 한 줄로 결합할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 반복시 사용할 뷰 이름, 두 번째는 반복할 배열이나 컬렉션, 세 번째는 각 반복에서 사용할 변수명입니다. 예를 들어, `jobs` 배열을 반복한다면 각 아이템을 `job` 변수로 사용할 수 있습니다. 반복 중인 배열의 키는 `key` 변수로 사용됩니다.

배열이 비어 있는 경우 사용할 뷰를 네 번째 인자로 지정할 수도 있습니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`를 통해 렌더링된 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 부모 변수가 필요하다면 `@foreach`와 `@include` 조합을 사용해야 합니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브를 사용하면 렌더링 사이클 동안 단 한 번만 평가될 템플릿 구역을 지정할 수 있습니다. 예를 들어, 루프 내에서 [스택](#stacks)에 JavaScript를 단 한 번만 넣고싶을 때 사용합니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 종종 `@push` 또는 `@prepend`와 같이 사용하는 경우가 많아, 편의상 `@pushOnce` 및 `@prependOnce` 디렉티브도 제공됩니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 순수 PHP 사용 (Raw PHP)

뷰 내에서 순수 PHP 코드를 삽입해야 할 상황도 있습니다. Blade의 `@php` 디렉티브를 사용하면 템플릿 안에서 PHP 코드 블록을 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

만약 PHP 네임스페이스 클래스 임포트만 필요하다면 `@use` 디렉티브를 사용하세요.

```blade
@use('App\Models\Flight')
```

클래스 임포트에 별칭을 줄 수도 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

동일 네임스페이스 내 여러 클래스를 그룹으로 임포트할 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

또한 `@use` 디렉티브는 PHP 함수와 상수 임포트도 지원합니다. 이 경우 `function` 또는 `const` 접두어를 붙여 경로를 지정합니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수, 상수 임포트에도 별칭 사용이 가능합니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수 또는 상수에 대해 그룹 임포트도 지원하여, 한 번에 여러 심볼을 임포트할 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서는 뷰 안에 주석을 작성할 수 있습니다. Blade 주석은 HTML 코드에는 포함되지 않아 브라우저에 노출되지 않습니다.

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, include 등이 제공하는 이점을 모두 제공하면서, 구조적으로 이해하기 쉬울 수 있습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명 컴포넌트(anonymous component) 두 가지 방식이 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용하세요. 예시로, 간단한 `Alert` 컴포넌트를 생성해보겠습니다. `make:component` 명령은 컴포넌트를 `app/View/Components` 디렉터리에 생성합니다.

```shell
php artisan make:component Alert
```

이 명령으로 컴포넌트에 대한 뷰 템플릿도 만들어집니다. 뷰 파일은 `resources/views/components` 디렉터리에 저장됩니다. 직접 작성한 컴포넌트는 별도의 등록 없이 `app/View/Components`와 `resources/views/components` 디렉터리에서 자동으로 인식됩니다.

하위 디렉터리에도 컴포넌트를 생성할 수 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령어는 `app/View/Components/Forms`에 `Input` 컴포넌트 클래스를, `resources/views/components/forms`에 뷰 파일을 각각 생성합니다.

클래스 없는 익명 컴포넌트를 만들고 싶다면 `--view` 플래그와 함께 `make:component` 명령을 사용하세요.

```shell
php artisan make:component forms.input --view
```

이 명령은 `resources/views/components/forms/input.blade.php`에 Blade 파일을 생성하며, `<x-forms.input />`으로 컴포넌트로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자체 앱의 컴포넌트는 자동으로 인식됩니다. 하지만 패키지에서 Blade 컴포넌트를 작성할 경우 컴포넌트 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 등록합니다.

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

등록 이후에는 태그 별칭을 사용하여 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 사용하여 네임스페이스별로 컴포넌트 클래스를 자동 로딩할 수 있습니다. 예를 들어, `Nightshade` 패키지에서 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스 하에 있을 수 있습니다.

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

이렇게 등록하면, 패키지 네임스페이스를 사용해 다음과 같이 컴포넌트를 쓸 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 자동으로 해당 클래스를 연결합니다. 서브디렉터리도 "dot" 표기로 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링하기

컴포넌트는 Blade 템플릿 내에서 `x-`로 시작하는 컴포넌트 태그로 표시할 수 있습니다. 네이밍은 클래스 이름을 케밥 케이스로 변환하여 사용합니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 하위에 있으나 더 깊은 경로이면, 디렉터리 구조를 `.`로 구분해 표시합니다. 예를 들어 `app/View/Components/Inputs/Button.php`에 있는 경우:

```blade
<x-inputs.button/>
```

컴포넌트를 조건부 렌더링하고 싶다면 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. `shouldRender`가 `false`일 경우 해당 컴포넌트는 렌더링되지 않습니다.

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

여러 컴포넌트를 그룹으로 관리하고 싶을 때, 연관된 컴포넌트들을 한 디렉터리에 묶을 수 있습니다. 예를 들어 "카드" 컴포넌트가 다음과 같이 있을 때:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 `Card` 컴포넌트가 `Card` 디렉터리 안에 있다면 `<x-card.card>`로 렌더링할 것처럼 보이지만, 라라벨은 컴포넌트 파일명이 디렉터리명과 동일하면 해당 컴포넌트를 "루트" 컴포넌트로 간주하고 디렉터리 명 반복 없이 사용할 수 있도록 지원합니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

HTML 속성을 통해 Blade 컴포넌트에 데이터를 전달할 수 있습니다. 상수형 데이터는 일반 HTML 속성으로 전달하고, PHP 식이나 변수는 속성 이름에 `:`를 접두어로 붙여 전달합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스 생성자에서 컴포넌트의 데이터 속성을 모두 정의해야 합니다. 컴포넌트의 모든 public 속성은 자동으로 컴포넌트 뷰에서 사용할 수 있습니다. 즉, `render` 메서드에서 데이터를 뷰로 전달할 필요가 없습니다.

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
     * 컴포넌트 뷰/컨텐츠 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때 public 변수의 값을 변수명으로 에코하여 출력할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 이름 표기법

컴포넌트 생성자 인수는 `camelCase`로 지정해야 하며, HTML 속성에서는 `kebab-case`로 전달해야 합니다. 예를 들어, 아래와 같은 컴포넌트 생성자가 있을 경우:

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

`$alertType` 인수는 컴포넌트에서 다음과 같이 전달할 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 짧은 속성 구문

컴포넌트에 속성을 전달할 때, "짧은 속성" 구문도 사용할 수 있습니다. 속성 이름과 변수명이 일치할 때 편리합니다.

```blade
{{-- 짧은 속성 구문 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일함 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 같은 JavaScript 프레임워크가 콜론 접두사 속성을 사용할 때, Blade에서도 해당 속성을 PHP 식이 아님을 알리기 위해 `::`(더블콜론) 접두사를 사용할 수 있습니다. 예를 들면 아래와 같습니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade가 렌더링한 결과는 아래와 같습니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서는 public 변수뿐 아니라 public 메서드도 사용할 수 있습니다. 예를 들어 `isSelected` 메서드가 있다면:

```php
/**
 * 주어진 옵션이 현재 선택된 것인지 판단합니다.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 템플릿에서 해당 메서드를 아래와 같이 호출할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성 및 슬롯 접근

컴포넌트 내부에서 컴포넌트 이름, 속성, 슬롯을 활용하고 싶을 때는 `render` 메서드에서 클로저를 반환하면 됩니다.

```php
use Closure;

/**
 * 컴포넌트 뷰/컨텐츠 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

클로저는 `$data` 배열을 매개변수로 받을 수 있으며, 여기엔 여러 정보가 담겨있습니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 요소를 클로저에서 바로 Blade 문자열에 삽입하면, 악의적 속성 내용에 의해 원격 코드 실행이 발생할 수 있으므로 절대 직접 삽입해서는 안 됩니다.

`componentName`은 HTML 태그에서 `x-` 다음에 나오는 이름입니다. 예를 들어 `<x-alert />`의 `componentName`은 `alert`이며, `attributes`는 HTML 태그에 지정된 모든 속성, `slot`은 컴포넌트 슬롯의 내용을 담는 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저가 반환하는 값이 존재하는 뷰라면 해당 뷰가 렌더링되며, 아니라면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트에서 Laravel의 [서비스 컨테이너](/docs/12.x/container)에서 의존성을 주입받을 경우, 데이터 어트리뷰트보다 먼저 목록에 나열하면 자동으로 주입됩니다.

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

일부 public 메서드나 프로퍼티를 컴포넌트 템플릿에서 노출하지 않으려면, 컴포넌트 클래스의 `$except` 배열 속성에 등록하면 됩니다.

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
### 컴포넌트 속성

컴포넌트에 데이터 속성을 전달하는 방법을 살펴보았지만, 때로는 `class` 등 컴포넌트 기능상 필수가 아닌 추가 HTML 속성을 지정해야 할 경우가 있습니다. 이런 속성들은 보통 컴포넌트 템플릿의 루트 요소에 전달합니다. 다음 예시처럼 `alert` 컴포넌트를 렌더링한다고 가정해보겠습니다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 정의되지 않은 속성들은 자동으로 컴포넌트의 "attribute bag"으로 모입니다. 해당 bag은 `$attributes` 변수로 컴포넌트 뷰에서 사용할 수 있으며, 전체 속성 값을 에코하면 모두 출력됩니다.

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내에서는 `@env` 같은 Blade 디렉티브 사용을 지원하지 않습니다. 예를 들어 `<x-alert :live="@env('production')"/>` 형태는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본/병합된 속성

기본 CSS 클래스 등 속성 초기값을 지정하거나, 추가 속성 값과 병합이 필요할 때는 `merge` 메서드를 사용할 수 있습니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 아래와 같이 사용했다면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더링되는 HTML은 아래와 같습니다.

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 CSS 클래스를 병합하고 싶으면 `class` 메서드를 이용할 수 있습니다. 이 메서드는 배열 키에 클래스 이름, 값에는 조건식을 입력합니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

여러 속성을 병합하고 싶다면 `merge` 메서드를 체이닝할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성이 필요 없는 다른 요소에 조건부 클래스를 적용하려면 [@class 디렉티브](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### class 속성이 아닌 값 병합

class 외 다른 속성을 병합하는 경우, `merge`에 지정한 값이 속성의 "기본값"이 되고, 해당 속성이 인젝트된 값과 병합되지 않고 덮어쓰기 됩니다. 예시로, 버튼 컴포넌트의 구현은 다음과 같을 수 있습니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시 type 속성을 지정하면 해당 값이 우선 적용됩니다.

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

class 외의 속성에도 기본 값과 인젝션 값이 조합되길 원한다면 `prepends` 메서드를 사용할 수 있습니다. 이 예시에서 `data-controller` 속성은 항상 `profile-controller`로 시작하고, 그 뒤에 추가된 값이 이어집니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 사용하면 속성 bag에서 원하는 속성만 필터링할 수 있습니다. 이 메서드는 콜백 함수에서 true를 반환하면 해당 속성이 유지됩니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith` 메서드로 지정한 문자열로 시작하는 속성을 모두 가져올 수도 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, `whereDoesntStartWith`는 지정한 문자열로 시작하지 않는 속성을 가져올 수 있습니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용하면 attribute bag 내 첫 번째 속성을 렌더링할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성이 존재하는지 확인하려면 `has` 메서드를 사용합니다. 이 메서드는 인수에 전달한 속성이 존재하면 true를 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열을 전달하면, 모든 속성이 존재할 때만 true를 반환합니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny`는 인수 배열 중 하나라도 존재하면 true를 반환합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

속성 값을 조회하려면 `get` 메서드를 사용하세요.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 지정한 키만 추출합니다.

```blade
{{ $attributes->only(['class']) }}
```

`except` 메서드는 지정한 키를 제외한 모든 속성을 반환합니다.

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약된 키워드

Blade 내부적으로 컴포넌트 렌더링을 위해 예약된 키워드가 있습니다. 아래 키워드는 컴포넌트의 public 프로퍼티나 메서드명으로 사용할 수 없습니다.

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
### 슬롯

추가적인 컨텐츠를 "slot"을 통해 컴포넌트로 전달하는 경우가 많습니다. 슬롯은 `$slot` 변수를 통해 렌더링됩니다. 예로 `alert` 컴포넌트가 다음과 같다고 가정합시다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

아래처럼 slot에 컨텐츠를 주입하여 사용할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

한 컴포넌트가 여러 슬롯을 필요로 한다면, 아래처럼 명명된 슬롯을 추가할 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯은 `x-slot` 태그로 정의하며, 명시적으로 지정되지 않은 컨텐츠는 기본 `$slot` 변수에 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

slot의 `isEmpty` 메서드로 컨텐츠가 비어있는지 판별할 수 있습니다.

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

이외에도 `hasActualContent` 메서드로, HTML 주석이 아닌 실제 컨텐츠가 slot에 있는지 판별할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯(Scoped Slots)

Vue 등 JavaScript 프레임워크에서 사용하는 "스코프 슬롯"처럼, 컴포넌트 내부의 데이터나 메서드에 slot에서 접근하고 싶다면, public 메서드나 속성을 컴포넌트 클래스에 정의하고, slot에서 `$component` 변수를 통해 접근할 수 있습니다. 아래는 `x-alert` 컴포넌트 클래스에 public `formatAlert` 메서드가 있을 때의 예시입니다.

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

Blade 컴포넌트와 마찬가지로, 슬롯에도 CSS 클래스 등 [속성](#component-attributes)을 지정할 수 있습니다.

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

슬롯 속성과 상호작용하려면 slot 변수의 `attributes` 속성을 사용할 수 있습니다. 그 외 attribute bag의 조작 방법은 [컴포넌트 속성 문서](#component-attributes)를 참고하세요.

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

아주 간단한 컴포넌트라면, 클래스와 뷰 파일을 따로 관리하는 것이 번거로울 수 있습니다. 이럴 때는 컴포넌트의 `render` 메서드에서 마크업을 직접 반환할 수 있습니다.

```php
/**
 * 컴포넌트 뷰/컨텐츠 반환
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

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령 실행 시 `--inline` 옵션을 사용하세요.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

런타임에 렌더링할 컴포넌트를 결정해야 할 때는 Laravel의 내장 `dynamic-component` 컴포넌트를 사용할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래 수동 컴포넌트 등록 관련 문서는 주로 뷰 컴포넌트를 포함하는 패키지를 작성할 때 필요합니다. 직접 패키지를 작성하지 않는다면 무관합니다.

자신의 앱에서 만드는 컴포넌트는 디폴트 경로에서 자동으로 인식됩니다.

하지만 패키지에서 Blade 컴포넌트를 사용하거나, 비표준 디렉터리에 컴포넌트를 두는 경우 Laravel이 컴포넌트 클래스를 찾을 수 있도록 직접 HTML 태그 별칭과 함께 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 수행합니다.

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

등록 이후에는 태그 별칭을 통해 컴포넌트를 사용할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 오토로딩

또는, `componentNamespace` 메서드를 사용해 네임스페이스별로 컴포넌트 클래스를 오토로딩할 수 있습니다. 예를 들어 Nightshade 패키지에서 `Calendar`와 `ColorPicker`가 `Package\Views\Components` 네임스페이스 아래 있다고 가정했을 때:

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

이렇게 하면, 다음과 같이 벤더 네임스페이스로 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 자동으로 클래스를 연결합니다. "dot" 표기를 통한 서브디렉터리 지원도 가능합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 유사하게, 익명 컴포넌트는 단일 파일로 관리하는 방법입니다. 다만, 익명 컴포넌트는 별도의 클래스 없이 Blade 뷰 파일 하나로만 구성합니다. 정의 방법은 `resources/views/components`에 Blade 템플릿을 두기만 하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의했다면 아래처럼 사용할 수 있습니다.

```blade
<x-alert/>
```

디렉터리 내에 컴포넌트를 중첩하고 싶다면, 컴포넌트 파일명을 `.`으로 구분해서 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

컴포넌트가 다수의 Blade 템플릿으로 구성되어 있다면, 컴포넌트별 디렉터리로 묶어 관리하고 싶을 수 있습니다. 예를 들어 "아코디언" 컴포넌트가 다음과 같은 디렉터리 구조라면:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 하면 아래와 같이 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

기존 구조에서는 index 템플릿을 components 디렉터리 바로 아래 두어야 했지만, now Blade에서는 디렉터리명과 동일한 파일을 해당 디렉터리에 두면, 중첩 디렉터리에 있어도 "루트" 컴포넌트로 렌더할 수 있습니다. 아래는 구조 예시입니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 프로퍼티 / 속성

익명 컴포넌트에는 별도의 클래스가 없으므로, 어떤 속성이 변수로 전달되고, 어떤 속성이 attribute bag에 포함될지 지정해주어야 합니다. 이를 위해 Blade 템플릿 상단에서 `@props` 디렉티브를 사용합니다. 변수에 기본값을 지정하고 싶으면, 배열 형태로 키에 이름, 값에 기본값을 작성하면 됩니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 컴포넌트는 아래처럼 사용할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 참조

자식 컴포넌트 내부에서 부모 컴포넌트의 데이터를 사용하려면, `@aware` 디렉티브를 사용할 수 있습니다. 예를 들어 다음과 같은 메뉴 컴포넌트 구조일 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트의 색상(color) 속성을 자식에서 사용하려면:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

기본적으로 `color` prop는 부모(`<x-menu>`)에만 전달됩니다. 하지만, 자식(`<x-menu.item>`)에서 `@aware`로 참조하면 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 부모 컴포넌트에 명시적으로 HTML 속성으로 전달된 데이터만 접근할 수 있습니다. 부모에서 기본값으로만 설정하고 실제로 속성으로 전달하지 않았다면 자식에서 사용할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 설명한 대로 익명 컴포넌트는 `resources/views/components` 디렉터리에 정의하는 게 기본입니다. 하지만, 추가적인 익명 컴포넌트 경로를 Laravel에 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인수로 익명 컴포넌트 경로를, 두 번째 인수로 네임스페이스(접두사, 필수 아님)를 받습니다. 주로 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) `boot`에서 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

접두사 없이 경로만 등록했다면, 해당 경로의 컴포넌트도 접두사 없이 사용할 수 있습니다.

```blade
<x-panel />
```

접두사(네임스페이스)를 지정했다면, 그 내부의 컴포넌트는 네임스페이스를 붙여 사용합니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구축하기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에서 동일한 레이아웃을 유지합니다. 만약 각 뷰마다 동일한 레이아웃 HTML을 반복한다면 관리가 매우 어렵습니다. 다행히, 한 번만 정의해두고 [Blade 컴포넌트](#components)로 전역에서 사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어 "할 일(todo) 목록" 애플리케이션을 만든다고 할 때, 레이아웃 컴포넌트는 다음과 같이 작성할 수 있습니다.

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

이제 `layout` 컴포넌트를 정의했다면, 해당 컴포넌트를 사용하는 Blade 뷰를 만들 수 있습니다. 예제에서는 단순히 할 일 목록을 출력합니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 주입한 내용은 `layout` 컴포넌트에서는 `$slot` 변수로 받습니다. 참고로 `$title` 슬롯이 주어지지 않으면 기본 타이틀이 표시됩니다. 아래와 같이 명명된 슬롯 구문으로 타이틀을 커스터마이즈할 수 있습니다.

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

이제 라우트에서 위 `tasks` 뷰를 반환하면 됩니다.

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의하기

"템플릿 상속(template inheritance)" 방법으로도 레이아웃을 만들 수 있습니다. 이는 [컴포넌트](#components) 도입 이전에 주로 사용되던 방법입니다.

먼저, 기본 레이아웃 페이지를 살펴보겠습니다. 아래와 같이 작성할 수 있습니다.

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

@로 시작하는 `@section`, `@yield` 디렉티브에 주목하세요. `@section`은 콘텐츠 영역을 정의하고, `@yield`는 해당 섹션 내용을 삽입할 위치를 지정합니다.

이제 상속받을 하위 페이지를 정의해보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

하위 뷰를 정의할 때는 `@extends`로 상속받을 레이아웃을 지정합니다. 하위 뷰에서는 `@section`으로 섹션 내용을 지정합니다. 이 내용은 부모 레이아웃의 `@yield` 위치에 출력됩니다.

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

이 예시에서, `sidebar` 섹션은 `@@parent` 디렉티브를 사용하여 부모 레이아웃의 내용을 덮어쓰지 않고 덧붙입니다.

> [!NOTE]
> 앞선 예제와 달리, 여기서는 `sidebar`가 `@endsection`으로 끝나며, `@show`는 즉시 해당 섹션을 출력하지만 `@endsection`은 섹션만 정의합니다.

`@yield` 디렉티브는 두 번째 인수를 이용해 섹션이 정의되지 않은 경우의 기본값을 지정할 수도 있습니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드

HTML 폼을 정의할 때, [CSRF 보호](/docs/12.x/csrf) 미들웨어에서 요청을 검증할 수 있도록 반드시 숨겨진 CSRF 토큰 필드를 포함해야 합니다. `@csrf` Blade 디렉티브로 토큰 필드를 삽입할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 만들 수 없으므로, 숨겨진 `_method` 필드로 HTTP 메서드를 오버라이드해야 합니다. 이를 위해 `@method` Blade 디렉티브를 사용할 수 있습니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 오류

`@error` 디렉티브는 주어진 속성(attribute)에 대해 [유효성 검증 오류 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 있는지 쉽게 확인할 수 있게 해줍니다. 블록 내에서 `$message` 변수를 에코하면 그 오류 메시지를 표시합니다.

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

`@error`는 내부적으로 if 문으로 컴파일되기 때문에, `@else`를 사용해 오류가 없는 경우 내용을 표시할 수도 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[특정 에러백의 이름](/docs/12.x/validation#named-error-bags)을 두 번째 인수로 전달하여, 여러 폼이 있는 페이지에서 개별 오류 메시지를 구분할 수도 있습니다.

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
## 스택(stacks)

Blade는 명명된 스택에 내용을 "푸시" 해두었다가 다른 뷰나 레이아웃에서 원하는 위치에 렌더링할 수 있습니다. 흔히 자식 뷰에서 필요한 JavaScript 라이브러리 등을 정의할 때 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

Boolean 조건에 따라 push할 때는 `@pushIf` 디렉티브를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

동일 스택에 여러 번 push할 수 있으며, 스택의 모든 내용은 `@stack` 디렉티브에 이름을 넘겨 출력할 수 있습니다.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 앞부분에 내용을 추가하려면 `@prepend` 디렉티브를 사용합니다.

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

`@inject` 디렉티브로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 뷰에 주입할 수 있습니다. 첫 번째 인자는 사용할 변수명, 두 번째 인자는 클래스/인터페이스명입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

순수 Blade 템플릿 문자열을 HTML로 변환해야 할 때는, `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 첫 번째 인자는 Blade 템플릿 문자열, 두 번째는 템플릿에 전달할 데이터입니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉터리에 임시 파일로 저장합니다. 렌더 후 임시 파일을 삭제하려면 `deleteCachedView` 인자를 true로 전달하세요.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 사용할 때, Blade 템플릿 일부만 HTTP 응답으로 반환해야 하는 상황이 있습니다. Blade의 "프래그먼트" 기능으로 이를 처리할 수 있습니다. 사용법은 템플릿 일부를 `@fragment`와 `@endfragment` 디렉티브로 감싸는 것부터 시작합니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이후 해당 뷰를 렌더링할 때, `fragment` 메서드로 반환할 프래그먼트만 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드로 조건에 따라 프래그먼트만 반환할 수도 있습니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments` 및 `fragmentsIf` 메서드로 여러 프래그먼트를 이어서 반환할 수도 있습니다.

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

Blade는 `directive` 메서드를 통해 직접 커스텀 디렉티브를 정의할 수 있습니다. Blade 컴파일러가 커스텀 디렉티브에 도달하면, 콜백에서 받은 인수를 기반으로 처리합니다.

아래 예시는 `@datetime($var)` 디렉티브를 생성하여, 전달된 `$var`가 `DateTime` 인스턴스일 때 포맷팅합니다.

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

이렇게 하면 디렉티브에 전달된 식에 대해 format 메서드가 연결된 PHP 코드가 최종적으로 생성됩니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 뒤에는 반드시 캐시된 Blade 뷰를 모두 삭제해야 합니다. `view:clear` Artisan 명령어로 캐시를 비울 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러

Blade에서 객체를 에코하면 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring)은 PHP의 "매직 메서드" 중 하나입니다. 하지만, 외부 라이브러리의 클래스를 사용할 때는 이 메서드를 직접 제어할 수 없습니다.

이럴 때, Blade의 `stringable` 메서드로 해당 타입에 맞는 에코 핸들러를 직접 지정할 수 있습니다. 이 메서드는 대개 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

정의한 이후에는 Blade 템플릿에서 해당 객체를 그대로 에코하면 됩니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

단순한 조건부문에서 굳이 복잡한 커스텀 디렉티브를 작성하고 싶지 않다면, Blade의 `Blade::if` 메서드를 이용해 클로저로 손쉽게 커스텀 조건문을 정의할 수 있습니다. 아래는 애플리케이션의 기본 "디스크" 설정값을 확인하는 커스텀 조건문을 정의하는 예시입니다(`AppServiceProvider`에서 수행).

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

정의된 조건문은 아래와 같이 사용할 수 있습니다.

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