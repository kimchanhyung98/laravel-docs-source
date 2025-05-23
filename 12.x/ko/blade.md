# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [라이브와이어로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
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
    - [데이터 속성 / Attributes](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성](#building-layouts)
    - [컴포넌트 기반 레이아웃](#layouts-using-components)
    - [템플릿 상속 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

블레이드(Blade)는 라라벨에 기본 탑재된 간결하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿에서 순수 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 블레이드 템플릿은 일반 PHP 코드로 컴파일되어, 수정되기 전까지 캐시되기 때문에 블레이드는 애플리케이션에 사실상 추가적인 부하를 거의 주지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 사용하며, 주로 `resources/views` 디렉터리에 저장됩니다.

블레이드 뷰는 `view` 글로벌 헬퍼를 사용해서 라우트나 컨트롤러에서 반환할 수 있습니다. 물론 [뷰](/docs/12.x/views)에 관한 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인수를 통해 데이터를 블레이드 뷰에 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### 라이브와이어로 블레이드 강화하기

블레이드 템플릿을 한 단계 더 발전시키고, 쉽고 간편하게 동적인 인터페이스를 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면 보통 React나 Vue 같은 프런트엔드 프레임워크에서나 가능했던 동적 기능을 블레이드 컴포넌트로 구현할 수 있습니다. 복잡한 빌드 단계나 클라이언트 사이드 렌더링 없이도 모던하고 반응성 높은 프런트엔드를 만들 수 있는 좋은 방법을 Livewire가 제공합니다.

<a name="displaying-data"></a>
## 데이터 출력

블레이드 뷰로 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해봅시다.

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

이 경우, `name` 변수를 다음과 같이 출력할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> 블레이드의 `{{ }}` 에코 구문은 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 출력되므로 XSS 공격을 방지할 수 있습니다.

뷰로 전달된 변수뿐만 아니라, 어떠한 PHP 함수의 결과도 에코 구문 내에서 출력할 수 있습니다. 실제로 원하는 어떠한 PHP 코드도 블레이드 에코 구문 안에 넣을 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 블레이드(그리고 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 만약 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

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

기본적으로 블레이드의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 거칩니다. 만약 데이터를 이스케이프 처리하지 않고 그대로 출력하고 싶다면, 다음과 같은 문법을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션의 사용자로부터 제공받은 데이터를 그대로 출력할 땐 각별히 주의해야 합니다. 직접 입력한 데이터를 표시할 때는 일반적으로 XSS 공격을 막기 위해 이스케이프 처리된 중괄호(`{{ }}`) 구문을 사용하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크에서도 중괄호를 사용해 브라우저에 표현식을 표시하는데, 이럴 때는 블레이드 렌더링 엔진에 해당 표현식을 건드리지 말라고 `@` 기호를 붙이면 됩니다. 예를 들면 아래와 같습니다.

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예제에서는 `@` 기호가 블레이드에 의해 제거되며, `{{ name }}` 표현식은 블레이드 엔진에 의해 처리되지 않고 그대로 남아 자바스크립트 프레임워크에서 렌더링되게 됩니다.

`@` 기호는 블레이드 디렉티브를 이스케이프할 때도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

때때로 배열을 뷰로 전달하여 자바스크립트 변수의 초기값으로 JSON 형태로 렌더링하고 싶을 때가 있습니다. 예를 들어,

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이렇게 직접 `json_encode`를 사용할 수도 있지만, `Illuminate\Support\Js::from` 메서드 디렉티브를 활용하면 더 간편합니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받을 수 있으며, 결과 JSON이 HTML의 따옴표 안에서도 안전하게 쓰이도록 적절히 이스케이프 처리해줍니다. 이때 반환되는 문자열은 `JSON.parse`로 자바스크립트 객체 또는 배열로 변환할 수 있습니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최근의 라라벨 애플리케이션 스캐폴딩에는 `Js` 파사드가 포함되어 있어, 블레이드 템플릿에서 더욱 편리하게 사용할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> 이미 존재하는 변수를 JSON으로 렌더링할 때만 `Js::from` 메서드를 사용해야 합니다. 블레이드 템플릿 엔진은 정규 표현식을 기반으로 동작하므로, 복잡한 표현식을 해당 디렉티브에 전달하려고 시도하면 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 넓은 영역에서 자바스크립트 변수를 표시해야 할 때, 블레이드 에코 구문 하나하나마다 `@`를 붙이는 대신, HTML 전체를 `@verbatim` 블록으로 감싸면 블레이드가 그 내부를 그대로 출력하게 할 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 디렉티브

템플릿 상속과 데이터 출력 외에도, 블레이드는 조건문 및 반복문 등 일반적인 PHP 제어 구조를 위해 간결한 단축 문법을 제공합니다. 이 단축 문법을 사용하면 PHP의 친숙한 제어 구조를, 더욱 짧고 깔끔하게 사용할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용해 `if` 문을 만들 수 있습니다. 이 디렉티브는 PHP의 해당 문법과 완전히 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

보다 간결하게 사용할 수 있는 `@unless` 디렉티브도 있습니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

이전에 설명한 조건문 디렉티브 외에도, `@isset`과 `@empty` 디렉티브는 각각 PHP의 `isset`과 `empty` 함수를 사용할 때 더 편리하게 쓸 수 있도록 제공합니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닐 때...
@endisset

@empty($records)
    // $records가 "비어있을" 때...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브를 사용하면 현재 사용자가 [인증](/docs/12.x/authentication)되었는지, 아니면 게스트인지 빠르게 확인할 수 있습니다.

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면, `@auth`와 `@guest` 디렉티브를 사용할 때 확인하고자 하는 인증 가드를 지정할 수 있습니다.

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

`@production` 디렉티브로 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // 프로덕션 환경 전용 콘텐츠...
@endproduction
```

또는, `@env` 디렉티브를 사용해 애플리케이션이 특정 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중일 때...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging" 또는 "production" 환경에서 실행 중일 때...
@endenv
```

<a name="section-directives"></a>
#### Section 디렉티브

템플릿 상속용 섹션에 콘텐츠가 존재하는지 확인하고 싶다면 `@hasSection` 디렉티브를 사용할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

반대로 섹션에 콘텐츠가 없는지를 확인하고자 한다면, `sectionMissing` 디렉티브를 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 디렉티브

`@session` 디렉티브는 [세션](/docs/12.x/session) 값이 존재하는지 확인할 때 사용할 수 있습니다. 세션 값이 존재하면 `@session`과 `@endsession` 사이의 템플릿 내용이 평가됩니다. 이 디렉티브 내에서는 `$value` 변수를 에코하여 세션 값을 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 조합해 Switch 문을 만들 수 있습니다.

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

조건문뿐 아니라, 블레이드는 PHP의 반복문 구조를 위한 간단한 디렉티브도 제공합니다. 역시 각 디렉티브는 PHP 구조와 완전히 동일하게 동작합니다.

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
> `foreach` 반복문을 순회할 때는, [loop 변수](#the-loop-variable)를 사용해 현재 반복 횟수나, 첫/마지막 반복 여부 등 다양한 정보를 확인할 수 있습니다.

반복문을 사용할 때 현재 반복을 건너뛰거나 종료하려면 각각 `@continue`, `@break` 디렉티브를 사용할 수 있습니다.

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

또한, 반복을 건너뛰거나 종료하는 조건을 디렉티브 선언에 바로 사용할 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문을 순회하는 동안, 루프 내부에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 인덱스, 첫/마지막 반복 여부 등, 루프에 대한 다양한 정보를 제공합니다.

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

중첩 루프의 경우, 부모 반복문의 `$loop` 변수는 `parent` 속성으로 참조할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 다음과 같은 다양한 속성이 있습니다.

<div class="overflow-auto">

| 속성              | 설명                                                  |
| ------------------ | ------------------------------------------------------ |
| `$loop->index`     | 현재 반복의 인덱스(0에서 시작).                       |
| `$loop->iteration` | 현재 반복 횟수(1에서 시작).                            |
| `$loop->remaining` | 반복이 남은 횟수.                                     |
| `$loop->count`     | 반복 대상 배열의 전체 항목 수.                        |
| `$loop->first`     | 현재 반복이 첫 번째인지 여부.                         |
| `$loop->last`      | 현재 반복이 마지막인지 여부.                          |
| `$loop->even`      | 현재 반복이 짝수번째 반복인지 여부.                   |
| `$loop->odd`       | 현재 반복이 홀수번째 반복인지 여부.                   |
| `$loop->depth`     | 현재 루프의 중첩(깊이) 단계.                           |
| `$loop->parent`    | 중첩 루프에서 부모 루프의 loop 변수.                 |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 디렉티브는 조건에 따라 CSS 클래스 문자열을 동적으로 컴파일할 수 있도록 해줍니다. 이 디렉티브는 클래스를 배열 형태로 받고, 배열의 key에는 추가하려는 클래스명을, value에는 해당 클래스가 적용될 조건식을 작성합니다. 만약 배열 항목의 key가 숫자라면, 그 클래스는 조건 없이 무조건 포함됩니다.

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

마찬가지로, `@style` 디렉티브를 사용하면 조건에 따라 인라인 CSS 스타일을 동적으로 추가할 수 있습니다.

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

편리하게 체크박스의 "checked" 여부를 나타내려면 `@checked` 디렉티브를 사용할 수 있습니다. 조건식이 `true`일 때 `"checked"` 속성이 출력됩니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, select 옵션에서 "selected" 여부를 지정하려면 `@selected` 디렉티브를 활용합니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, 요소를 비활성화("disabled")해야 할 때는 `@disabled` 디렉티브를 사용할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

이 외에도, 입력 필드를 읽기 전용("readonly")으로 하고 싶다면 `@readonly` 디렉티브를 사용할 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

마지막으로, 입력 필드가 필수("required")임을 표시하고자 할 때는 `@required` 디렉티브를 사용할 수 있습니다.

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
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 블레이드 [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 장점을 제공하므로, `@include`보다 컴포넌트 방식을 사용하는 것이 더 유리한 경우가 많습니다.

블레이드의 `@include` 디렉티브를 사용하면 하나의 뷰 내에서 다른 블레이드 뷰를 포함할 수 있습니다. 부모 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에서도 그대로 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰에 부모 뷰의 모든 데이터가 전달되긴 하지만, 추가적으로 별도의 데이터를 배열로 전달해줄 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하려 할 경우 라라벨은 에러를 발생시킵니다. 만약 포함하려는 뷰가 존재할 수도, 존재하지 않을 수도 있다면 `@includeIf` 디렉티브를 사용해야 합니다.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

불리언 조건에 따라 뷰를 포함하려면 `@includeWhen` 또는 `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에서 첫 번째로 존재하는 뷰를 포함하고 싶다면, `includeFirst` 디렉티브를 사용하면 됩니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> 블레이드 뷰에서는 `__DIR__` 및 `__FILE__` 상수 사용을 피하는 것이 좋습니다. 해당 상수들은 캐시되어 컴파일된 뷰 파일의 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>

#### 컬렉션의 뷰 렌더링

Blade의 `@each` 디렉티브를 사용하면 루프와 include를 한 줄로 결합하여 사용할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

`@each` 디렉티브의 첫 번째 인자는 배열이나 컬렉션의 각 요소를 렌더링할 뷰입니다. 두 번째 인자는 반복하고자 하는 배열 또는 컬렉션이고, 세 번째 인자는 뷰 내에서 현재 반복 항목에 할당될 변수명입니다. 예를 들어, `jobs`라는 배열을 반복한다면, 보통 각 job을 뷰 내부에서 `job` 변수로 접근할 수 있습니다. 반복의 현재 배열 키는 뷰 안에서 `key` 변수로 사용할 수 있습니다.

`@each` 디렉티브에는 네 번째 인자를 넘길 수도 있습니다. 이 인자는 해당 배열이 비어 있을 때 렌더링할 뷰를 지정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`를 통해 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에서 이러한 변수가 필요하다면 `@foreach`와 `@include` 디렉티브를 대신 사용해야 합니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브는 템플릿의 특정 부분이 렌더링 사이클마다 한 번만 실행되도록 정의할 수 있게 해줍니다. 예를 들어, [스택](#stacks)을 사용하여 특정 JavaScript 코드를 페이지 헤더에 한 번만 추가하고 싶을 때 유용합니다. 반복문에서 [컴포넌트](#components)를 렌더링할 때, 처음 렌더링될 때만 JavaScript를 헤더에 넣고 싶을 때 아래와 같이 사용할 수 있습니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 `@push` 또는 `@prepend` 디렉티브와 자주 함께 사용되기 때문에, `@pushOnce`와 `@prependOnce` 디렉티브도 제공됩니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 순수 PHP 코드 작성

상황에 따라 뷰 안에 PHP 코드를 직접 작성하는 것이 유용할 때가 있습니다. Blade의 `@php` 디렉티브를 사용하면 템플릿 내에서 순수 PHP 블록을 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

클래스만 임포트하고 싶다면 `@use` 디렉티브를 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

`@use` 디렉티브에 두 번째 인자를 넘기면 임포트한 클래스에 별칭을 지정할 수 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 하에 여러 클래스를 임포트할 경우, 클래스명을 묶어서 임포트할 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

`@use` 디렉티브는 `function`이나 `const` 키워드를 경로 앞에 붙이면 PHP 함수 및 상수도 임포트할 수 있습니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

클래스 임포트와 마찬가지로, 함수와 상수에도 별칭을 지정할 수 있습니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수와 상수도 그룹 임포트를 지원하므로, 같은 네임스페이스의 여러 심볼을 한 번에 임포트할 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서는 뷰 내에 주석을 정의할 수도 있습니다. Blade 주석은 HTML 주석과 달리, 실제 애플리케이션에서 반환되는 HTML에는 포함되지 않습니다.

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, include가 제공하는 것과 유사한 이점을 제공합니다. 다만, 일부는 컴포넌트와 슬롯의 개념이 더 이해하기 쉽다고 느낄 수 있습니다. 컴포넌트를 작성하는 방법에는 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` 아티즌 명령어를 사용할 수 있습니다. 사용 방법을 보여주기 위해 간단한 `Alert` 컴포넌트를 예시로 들겠습니다. `make:component` 명령어를 실행하면 컴포넌트가 `app/View/Components` 디렉터리에 생성됩니다.

```shell
php artisan make:component Alert
```

이 명령은 컴포넌트용 뷰 템플릿도 동시에 생성합니다. 뷰는 `resources/views/components` 디렉터리에 위치하게 됩니다. 애플리케이션 자체의 컴포넌트를 작성할 때는 보통 `app/View/Components` 또는 `resources/views/components` 디렉터리 내의 컴포넌트가 자동으로 탐지되므로, 별도로 컴포넌트를 등록할 필요는 거의 없습니다.

하위 디렉터리 내에 컴포넌트를 만들 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령을 실행하면 `app/View/Components/Forms` 디렉터리에 `Input` 컴포넌트가 생성되고, 뷰는 `resources/views/components/forms` 디렉터리에 위치합니다.

별도의 클래스 없이 Blade 템플릿만 사용하는 익명 컴포넌트를 만들고 싶다면, `make:component` 명령어 실행 시 `--view` 플래그를 사용할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

위 명령을 실행하면 `resources/views/components/forms/input.blade.php` 파일이 생성되며, `<x-forms.input />`와 같이 컴포넌트로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자체 애플리케이션의 컴포넌트는 위에서 설명한 디렉터리 내에 두면 자동으로 인식됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 개발할 때는 컴포넌트 클래스와 그에 대응하는 HTML 태그 별칭을 직접 등록해야 합니다. 일반적으로 패키지 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지의 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

이렇게 컴포넌트를 등록하면, 지정한 태그 별칭으로 아래와 같이 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 사용해 네임스페이스의 컴포넌트 클래스를 컨벤션에 따라 자동 로드할 수도 있습니다. 예를 들어, `Nightshade`라는 패키지에 `Package\Views\Components` 네임스페이스에 속하는 `Calendar`, `ColorPicker` 컴포넌트가 있다고 가정하면 다음과 같이 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지의 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이제 `package-name::` 문법을 사용해 벤더 네임스페이스 별칭으로 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해서 대응되는 클래스를 자동으로 매핑합니다. 하위 디렉터리는 "dot" 표기법으로도 지원됩니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 뷰에서 표시하려면, Blade 컴포넌트 태그를 사용하면 됩니다. 컴포넌트 태그는 `x-`로 시작하고, 그 뒤에 컴포넌트 클래스 이름을 케밥 케이스로 붙여 사용합니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉터리 하위에 더 깊이 위치한 경우, 디렉터리 구조를 `.` 문자로 표기할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면 아래와 같이 사용할 수 있습니다.

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트를 렌더링할지 여부를 반환합니다.
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

컴포넌트 그룹의 일부로 컴포넌트를 한 디렉터리에 묶고 싶은 경우가 있습니다. 예를 들어, "card" 컴포넌트가 아래와 같은 클래스 구조를 가진다고 가정해봅시다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트가 `Card` 디렉터리 안에 있으므로 보통 `<x-card.card>`로 렌더해야 할 것 같지만, 라라벨은 파일 이름이 디렉터리명과 같으면 해당 컴포넌트를 "루트" 컴포넌트로 간주하여 디렉터리명을 반복하지 않아도 렌더링할 수 있도록 해줍니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

Blade 컴포넌트에 데이터를 전달하려면 HTML 속성(attribute) 형식으로 값을 넘길 수 있습니다. 일반 문자열이나 간단한 값은 HTML 속성 형식으로 넘길 수 있고, PHP 표현식이나 변수를 전달할 때는 속성 앞에 `:`을 붙여 사용합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 컴포넌트의 데이터 속성을 모두 정의해야 합니다. 컴포넌트의 public 속성은 뷰에서 자동으로 사용할 수 있습니다. 데이터를 굳이 `render` 메서드에서 뷰로 전달할 필요는 없습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스를 생성합니다.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 컴포넌트를 렌더링할 뷰/내용을 반환합니다.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링되면, public 변수의 값은 변수명을 그대로 echo해서 사용할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 속성 이름 표기법

컴포넌트 생성자의 인자는 `camelCase`(카멜케이스)로 작성해야 하며, HTML 애트리뷰트로 값을 전달할 때는 `kebab-case`(케밥 케이스) 표기법을 사용해야 합니다. 예를 들어 아래와 같은 컴포넌트 생성자가 있다고 합시다.

```php
/**
 * 컴포넌트 인스턴스를 생성합니다.
 */
public function __construct(
    public string $alertType,
) {}
```

이때 `$alertType` 인자는 다음과 같이 넘길 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 짧은 속성 문법

컴포넌트에 속성을 넘길 때 "짧은 속성" 문법도 사용할 수 있습니다. 속성명이 그 값을 담고 있는 변수명과 일치할 때 주로 쓰입니다.

```blade
{{-- 짧은 속성 문법... --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 같은 일부 JavaScript 프레임워크는 `:`가 앞에 붙은 속성을 사용합니다. 이때 Blade에게 해당 속성이 PHP 표현식이 아님을 알리고자 한다면, `::`(콜론 두 개) 접두사를 사용할 수 있습니다. 예를 들어, 아래와 같이 컴포넌트를 작성하면

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade가 렌더링하는 HTML은 다음과 같습니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서는 public 변수를 사용할 수 있을 뿐 아니라, public 메서드도 호출할 수 있습니다. 예를 들어, `isSelected`라는 메서드가 있는 컴포넌트를 생각해봅시다.

```php
/**
 * 주어진 option이 현재 선택된 값인지 확인합니다.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 템플릿에서 아래와 같이 해당 메서드를 실행할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성과 슬롯 접근

Blade 컴포넌트는 컴포넌트 이름, 속성, 슬롯 값을 클래스의 render 메서드 안에서 가져올 수도 있습니다. 이때 render 메서드에서 클로저를 반환해야 합니다.

```php
use Closure;

/**
 * 컴포넌트를 렌더링할 뷰/내용을 반환합니다.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

컴포넌트의 render 메서드에서 반환하는 클로저는 `$data` 배열 하나를 인자로 받을 수 있습니다. 이 배열에는 컴포넌트 관련 정보가 포함됩니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 값들은 `render` 메서드에서 반환하는 Blade 문자열에 직접 삽입해서는 안 됩니다. 악의적인 속성 값으로 인해 원격 코드 실행이 발생할 수 있기 때문입니다.

`componentName`은 `x-` 접두사 다음 컴포넌트 태그명과 동일합니다. 예를 들어 `<x-alert />`의 `componentName` 값은 `alert`입니다. `attributes` 요소에는 해당 태그에 부여된 모든 속성이 담깁니다. `slot` 요소는 컴포넌트 슬롯의 내용을 가진 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저는 반드시 문자열을 반환해야 하며, 반환된 문자열이 실제 뷰 이름과 일치하면 해당 뷰를 렌더링하고, 일치하지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트가 Laravel [서비스 컨테이너](/docs/12.x/container)의 의존성을 필요로 한다면, 컴포넌트 데이터 속성보다 앞에 해당 의존성을 나열하면 컨테이너가 자동으로 주입해줍니다.

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스를 생성합니다.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성/메서드 숨기기

특정 public 메서드나 속성을 컴포넌트 템플릿에서 변수로 노출하지 않으려면, `$except` 배열 속성에 추가하면 됩니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에서 노출하지 않을 속성/메서드 목록입니다.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스를 생성합니다.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 애트리뷰트

컴포넌트에 데이터 속성을 전달하는 방법은 이미 살펴봤습니다. 다만, 컴포넌트 기능과 관계없이 추가로 `class`와 같은 HTML 속성을 지정해야 할 때가 있습니다. 이러한 속성들은 일반적으로 컴포넌트의 루트 요소로 전달되기를 원할 때가 많습니다. 예를 들어 아래와 같이 `alert` 컴포넌트를 렌더링한다고 합시다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에서 정의하지 않은 속성들은 자동으로 "애트리뷰트 백(attribute bag)"에 저장됩니다. 이 애트리뷰트 백은 컴포넌트에서 `$attributes` 변수로 사용할 수 있습니다. 모든 속성을 컴포넌트 내에서 아래와 같이 렌더링하면 됩니다.

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 현재로서는 컴포넌트 태그 내에서 `@env`와 같은 디렉티브를 사용할 수 없습니다. 예를 들어, `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/속성 병합

애트리뷰트 값의 기본값을 지정하거나 추가 값을 병합해야 할 때가 있습니다. 이럴 땐, 애트리뷰트 백의 `merge` 메서드를 활용하면 됩니다. 주로 컴포넌트에 항상 적용되어야 하는 CSS 클래스를 정의할 때 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 아래와 같이 사용한다고 하면,

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링되는 HTML은 다음과 같이 나타납니다.

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 클래스 조건부 병합

특정 조건이 `true`일 때만 클래스를 병합하고 싶을 때는 `class` 메서드를 사용합니다. 이 메서드는 배열을 받아, 배열의 키로 class명을 넣고 값으로 불린 조건식을 지정하면 됩니다. 배열 요소의 키가 숫자라면 해당 클래스는 항상 출력됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성까지 병합하려면, `class` 메서드 뒤에 `merge` 메서드를 체이닝 할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 속성 병합이 필요 없는 다른 HTML 요소에서 조건부 클래스를 컴파일하고 싶으면 [@class 디렉티브](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### class가 아닌 속성 병합

`class`가 아닌 속성을 병합할 때, `merge` 메서드에 전달한 값은 해당 속성의 "기본값"으로 간주됩니다. 하지만 `class` 속성과 다르게, 이런 속성들은 덮어쓰기만 되고 주입된 값과 병합되지 않습니다. 예를 들어, button 컴포넌트를 아래와 같이 구현했다고 가정해 봅니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

버튼 컴포넌트 사용 시 아래와 같이 커스텀 `type` 속성을 줄 수 있고, 지정하지 않으면 기본값(`button`)이 사용됩니다.

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

class 외의 속성도 기본값에 주입된 속성값을 이어붙이고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예시에서는, `data-controller` 속성이 늘 `profile-controller`로 시작하며, 추가로 주입된 값은 뒤에 이어집니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 사용하여 속성을 필터링할 수 있습니다. 이 메서드는 클로저를 받아, 반환값이 `true`인 속성만 애트리뷰트 백에 남깁니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

편의상, `whereStartsWith` 메서드를 사용해 키가 특정 문자열로 시작하는 모든 속성을 조회할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, `whereDoesntStartWith`는 지정한 접두사로 시작하지 않는 모든 속성을 제외합니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

그리고 `first` 메서드를 사용하면 주어진 애트리뷰트 백에서 첫 번째 속성을 렌더링할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

컴포넌트에 특정 속성이 포함되어 있는지 확인하려면, `has` 메서드를 사용할 수 있습니다. 이 메서드는 속성명을 인자로 받고, 속성이 존재하는지에 따라 불린 값을 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

`has` 메서드에 배열을 넘기면, 해당 배열의 모든 속성이 컴포넌트에 존재하는지 검사합니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny` 메서드는 지정한 속성 중 하나라도 존재하는지 확인합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성 값을 조회하려면 `get` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 전달한 키 목록만 추출해서 가져옵니다.

```blade
{{ $attributes->only(['class']) }}
```

`except` 메서드는 지정한 키 목록을 제외한 속성만 반환합니다.

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>

### 예약된 키워드

기본적으로 Blade의 내부 컴포넌트 렌더링에 사용되는 몇 가지 키워드는 예약되어 있습니다. 아래의 키워드들은 컴포넌트 내부에서 public 속성이나 메서드명으로 정의할 수 없습니다.

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

컴포넌트에 "슬롯"을 통해 추가적인 내용을 전달해야 할 때가 많습니다. 컴포넌트 슬롯은 `$slot` 변수를 출력하여 렌더링할 수 있습니다. 이 개념을 이해하기 위해, `alert` 컴포넌트가 다음과 같은 마크업을 가진다고 가정해 보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

아래와 같이 컴포넌트 내부에 내용을 삽입하면, 해당 내용이 `slot`으로 전달됩니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

때로는 컴포넌트가 여러 개의 슬롯을 추가로 받아서, 서로 다른 위치에 각각의 슬롯을 출력해야 할 수 있습니다. 아래 예시는 "title" 슬롯을 추가로 주입할 수 있도록 `alert` 컴포넌트를 수정한 모습입니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이렇게 명명된 슬롯의 내용을 정의하려면 `x-slot` 태그를 사용할 수 있습니다. 명시적인 `x-slot` 태그 외부에 작성된 모든 내용은 `$slot` 변수로 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯에 값이 있는지 확인하고 싶다면, 슬롯의 `isEmpty` 메서드를 호출하세요.

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

또한, `hasActualContent` 메서드를 사용하면 해당 슬롯에 HTML 주석이 아닌 실제 내용이 존재하는지 확인할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯(Scoped Slots)

Vue와 같은 JavaScript 프레임워크를 사용해보셨다면, "스코프드 슬롯"에 익숙하실 수 있습니다. 스코프드 슬롯은 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근할 수 있게 해줍니다. 라라벨에서는 컴포넌트 클래스에 public 메서드나 속성을 정의한 후, 슬롯 내부에서 `$component` 변수를 통해 해당 컴포넌트에 접근할 수 있습니다. 아래 예시는 `x-alert` 컴포넌트 클래스에 public `formatAlert` 메서드가 정의되어 있다고 가정한 경우입니다.

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯의 속성(Attribute)

Blade 컴포넌트와 마찬가지로, 슬롯에도 CSS 클래스와 같은 [속성](#component-attributes)을 추가할 수 있습니다.

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

슬롯의 속성에 접근하려면, 슬롯 변수의 `attributes` 속성을 이용하면 됩니다. 속성 활용법에 대한 자세한 내용은 [컴포넌트 속성 문서](#component-attributes)를 참고하세요.

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

아주 작은 컴포넌트라면 컴포넌트 클래스와 뷰 템플릿 파일을 따로 관리하는 것이 번거로울 수 있습니다. 이런 경우에는 `render` 메서드에서 직접 마크업을 반환해도 됩니다.

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
#### 인라인 뷰 컴포넌트 생성하기

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령 실행 시 `--inline` 옵션을 사용하면 됩니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

가끔은 어떤 컴포넌트를 렌더링할지 실행 시점까지 알 수 없는 경우가 있습니다. 이런 상황에서는 라라벨에 내장된 `dynamic-component` 컴포넌트를 사용해, 런타임 값이나 변수에 따라 컴포넌트를 동적으로 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 다음의 컴포넌트 수동 등록 관련 설명은 주로 뷰 컴포넌트를 포함하는 라라벨 패키지를 개발하는 경우에 적용됩니다. 패키지를 작성하지 않는 일반적인 사용자는 이 부분을 참고하지 않아도 됩니다.

자신의 애플리케이션에서 컴포넌트를 작성하는 경우, 컴포넌트들은 기본적으로 `app/View/Components` 디렉터리와 `resources/views/components` 디렉터리에서 자동으로 발견됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 제작 중이거나, 컴포넌트를 비표준 디렉터리에 둘 경우에는, 컴포넌트 클래스와 HTML 태그 별칭(alias)를 수동으로 등록해야 라라벨에서 해당 컴포넌트를 찾을 수 있습니다. 이런 경우 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 컴포넌트를 등록합니다.

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

컴포넌트를 등록하면, 다음과 같이 태그 별칭을 통해 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트의 자동 로딩

또는, `componentNamespace` 메서드를 이용하여 컴포넌트 클래스를 관례에 따라 자동으로 로딩할 수도 있습니다. 예를 들어, `Nightshade`라는 패키지 내부에 `Calendar`와 `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 위치할 수 있습니다.

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

이렇게 하면 패키지 컴포넌트를 벤더 네임스페이스를 통해 `package-name::` 구문으로 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 지정된 컴포넌트 이름을 파스칼 케이스로 변환해서, 컴포넌트와 연결된 클래스를 자동으로 찾습니다. "dot" 표기법을 사용하여 하위 디렉터리도 지원합니다.

<a name="anonymous-components"></a>
## 무명(Anonymous) 컴포넌트

인라인 컴포넌트와 유사하게, 무명(Anonymous) 컴포넌트는 하나의 파일로 컴포넌트를 관리할 수 있는 방법을 제공합니다. 단, 무명 컴포넌트는 별도의 클래스 파일 없이, 오직 하나의 뷰 파일만 사용합니다. 무명 컴포넌트를 정의하려면 단순히 `resources/views/components` 디렉터리에 Blade 템플릿을 추가하면 됩니다. 예를 들어 `resources/views/components/alert.blade.php`에 컴포넌트를 정의한 경우, 바로 아래처럼 사용할 수 있습니다.

```blade
<x-alert/>
```

컴포넌트가 `components` 디렉터리의 더 깊은 하위 디렉터리에 있는 경우에는 점(`.`)을 이용해 컴포넌트 이름을 표시할 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php`에 컴포넌트를 정의한 경우 다음과 같이 사용할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 무명 인덱스 컴포넌트

컴포넌트가 여러 개의 Blade 템플릿으로 구성될 때, 각각의 컴포넌트 템플릿을 하나의 디렉터리로 그룹화하고자 할 때가 있습니다. 예를 들어, 아래와 같이 "accordion(아코디언)" 컴포넌트의 디렉터리 구조가 있다고 가정합니다.

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 구조를 통해, 아래처럼 아코디언 컴포넌트와 내부 항목을 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 위 구조에서는 `x-accordion`을 사용하려면, "인덱스" 역할의 아코디언 컴포넌트 템플릿을 반드시 `resources/views/components` 디렉터리에 두어야 했습니다. 즉, 다른 아코디언 관련 템플릿들과 같은 디렉터리에 넣을 수 없었습니다.

다행히 Blade에서는 컴포넌트 디렉터리 내부에 디렉터리명과 동일한 파일을 두어도 해당 디렉터리의 "루트" 컴포넌트로 렌더링할 수 있도록 지원합니다. 즉, 아래와 같이 구조를 구성해도, 앞서 예시에서 사용한 Blade 문법을 그대로 쓸 수 있습니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성(attribute)

무명 컴포넌트는 별도의 클래스 파일이 없으므로, 어떤 데이터를 변수로 전달하고 어떤 데이터를 [속성 배깅](#component-attributes)에 포함해야 할지 혼동될 수 있습니다.

이럴 때는 컴포넌트의 Blade 템플릿 맨 위에서 `@props` 디렉티브를 사용해 데이터 변수를 명시할 수 있습니다. 컴포넌트에 전달된 그 외의 모든 속성은 attribute bag을 통해 접근할 수 있습니다. 특정 데이터 변수에 기본값을 주고 싶으면, 배열 구조의 키-값 형태로 지정하면 됩니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 컴포넌트를 정의하면, 아래처럼 사용할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 컴포넌트의 데이터 접근

간혹 자식 컴포넌트에서 부모 컴포넌트의 데이터에 접근하고 싶을 때가 있습니다. 이 경우에는 `@aware` 디렉티브를 사용할 수 있습니다. 예를 들어, `<x-menu>`와 `<x-menu.item>`으로 이루어진 복잡한 메뉴 컴포넌트를 만든다고 할 때 아래처럼 사용할 수 있습니다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` 컴포넌트는 다음과 같이 구현될 수 있습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

여기서 `color` prop은 부모(`<x-menu>`)에만 전달되고, 자식인 `<x-menu.item>`에서는 기본적으로 접근할 수 없습니다. 하지만 `@aware` 디렉티브를 사용하면 자식 컴포넌트에서도 해당 값을 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 반드시 부모 컴포넌트의 HTML 속성(attribute)으로 명시적으로 전달된 데이터만 접근할 수 있습니다. 부모 컴포넌트의 `@props` 기본값으로만 지정된 데이터는 `@aware`로 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 무명 컴포넌트 경로 등록

앞서 설명한 대로, 무명 컴포넌트는 보통 `resources/views/components` 디렉터리에 Blade 템플릿을 추가하여 정의합니다. 하지만 경우에 따라, 이 기본 경로 외에 별도의 무명 컴포넌트 경로를 라라벨에 등록하고 싶을 수 있습니다.

`anonymousComponentPath` 메서드는 무명 컴포넌트가 위치한 "경로"를 첫 번째 인자로 받고, 두 번째 인자로는 컴포넌트가 소속될 "네임스페이스"를 선택적으로 지정할 수 있습니다. 이 메서드는 보통 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

위 예시처럼 접두어(prefix) 없이 컴포넌트 경로를 등록하면, 해당 경로에 있는 컴포넌트들도 블레이드에서 접두어 없이 사용할 수 있습니다. 예를 들어, 저 경로에 `panel.blade.php`가 있으면 아래처럼 사용할 수 있습니다.

```blade
<x-panel />
```

접두어 네임스페이스는 `anonymousComponentPath`의 두 번째 인자로 지정할 수 있습니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이렇게 접두어가 지정되면, 해당 네임스페이스 내부의 컴포넌트는 렌더링 시 네임스페이스를 컴포넌트 이름에 붙여서 사용할 수 있습니다.

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성하기

<a name="layouts-using-components"></a>
### 컴포넌트를 사용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에서 동일한 레이아웃 구조를 공유합니다. 만약 각 뷰마다 전체 레이아웃 HTML을 반복해서 작성해야 한다면, 애플리케이션 유지 보수가 매우 어렵고 불편해질 것입니다. 다행히, 레이아웃을 [Blade 컴포넌트](#components)로 정의해두고 애플리케이션 전체에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어, "TODO" 목록 애플리케이션을 만든다고 가정합시다. `layout` 컴포넌트를 아래와 같이 정의할 수 있습니다.

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

`layout` 컴포넌트를 정의한 후에는, 해당 컴포넌트를 사용하는 Blade 뷰를 작성할 수 있습니다. 예를 들어, 아래처럼 할 일 목록을 보여주는 뷰를 만들 수 있습니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 삽입되는 내용은 기본적으로 `layout` 컴포넌트의 `$slot` 변수로 전달됩니다. 또한, 레이아웃에서 `$title` 슬롯이 제공되면 해당 값을 사용하고, 없으면 기본 제목이 표시됩니다. 아래와 같이 표준 슬롯 문법을 사용해서 할 일 목록 뷰에서 커스텀 타이틀을 지정할 수 있습니다.

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

레이아웃과 할 일 목록 뷰를 정의했다면, 이제 라우트에서 `tasks` 뷰를 반환하면 됩니다.

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

레이아웃은 "템플릿 상속" 기능을 통해서도 생성할 수 있습니다. 이 방식은 [컴포넌트](#components)가 도입되기 전 레이아웃을 구성하는 일반적인 방법이었습니다.

먼저 간단한 예제를 살펴보겠습니다. 아래는 페이지 레이아웃입니다. 많은 웹 애플리케이션에서 여러 페이지가 동일한 레이아웃을 공유하므로, 하나의 Blade 뷰로 레이아웃을 따로 정의해두면 편리합니다.

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

이 파일은 일반적인 HTML 구조를 가지지만, `@section`과 `@yield` 디렉티브가 있는 것을 볼 수 있습니다. `@section`은 특정 구역의 내용을 정의할 때 사용하고, `@yield`는 해당 구역의 내용을 보여줄 위치에 사용합니다.

레이아웃이 정의되었으니, 이 레이아웃을 상속하는 자식 페이지를 만들어 보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

자식 뷰에서는 `@extends` Blade 디렉티브를 사용해 어떤 레이아웃을 상속받을지 지정할 수 있습니다. 이렇게 Blade 레이아웃을 상속하는 뷰는 `@section`을 이용해 레이아웃의 구역에 내용을 삽입할 수 있습니다. 위 예시에서처럼 `@yield`로 지정된 위치에 이 내용들이 출력됩니다.

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

위 예시에서는 `sidebar` 구역에서 `@@parent` 디렉티브를 활용해, 기본 레이아웃의 사이드바 내용을 덮어쓰는 대신 추가(append)하고 있습니다. 렌더링 시 `@@parent` 부분은 상위 레이아웃의 해당 구역 내용으로 대체됩니다.

> [!NOTE]
> 이전 예시와 달리, 여기서는 `sidebar` 구역이 `@show`가 아니라 `@endsection`으로 끝납니다. `@endsection`은 해당 구역만 정의하며, `@show`는 정의와 동시에 **즉시 출력(yield)**합니다.

`@yield` 디렉티브는 두 번째 인자로 기본값도 받을 수 있습니다. 해당 섹션이 정의되어 있지 않으면 이 값이 출력됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 토큰 필드

애플리케이션에서 HTML 폼을 정의할 때마다, [CSRF 보호 미들웨어](/docs/12.x/csrf)가 요청을 검증할 수 있도록 폼 내에 숨겨진 CSRF 토큰 필드를 추가해야 합니다. `@csrf` Blade 디렉티브로 토큰 필드를 쉽게 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### HTTP 메서드 필드

HTML 폼에서는 `PUT`, `PATCH`, `DELETE` 요청을 직접 만들 수 없기 때문에, 이와 같은 HTTP 메서드를 흉내내기 위해 숨겨진 `_method` 필드를 추가해야 합니다. `@method` Blade 디렉티브가 이 필드를 만들어줍니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 디렉티브는 주어진 속성(attribute)에 대한 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)를 빠르게 확인할 때 사용합니다. 이 안에서 `$message` 변수를 출력하면 에러 메시지를 보여줄 수 있습니다.

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

`@error` 디렉티브는 내부적으로 "if" 문으로 처리되므로, 해당 속성에 에러가 없는 경우에는 `@else` 디렉티브를 활용해 다른 내용을 렌더링할 수도 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

페이지에 여러 폼이 존재하는 경우, `@error` 디렉티브의 두 번째 인자로 [특정 에러 배그의 이름](/docs/12.x/validation#named-error-bags)을 전달해 해당 폼의 유효성 검증 메시지만 가져올 수 있습니다.

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

Blade에서는 이름이 지정된 스택에 내용을 넣고, 이 스택을 다른 뷰나 레이아웃에서 렌더링할 수 있습니다. 이 기능은 자식 뷰에서 필요로 하는 JavaScript 라이브러리를 지정할 때 특히 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

주어진 불리언 조건식이 `true`일 때에만 `@push`로 내용을 추가하고 싶다면, `@pushIf` 디렉티브를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에는 필요한 만큼 여러 번 내용을 추가할 수 있습니다. 스택에 쌓인 모든 내용을 렌더링하려면, `@stack` 디렉티브에 해당 스택의 이름을 전달하면 됩니다.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 맨 앞에 내용을 추가하고 싶다면, `@prepend` 디렉티브를 사용해야 합니다.

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

`@inject` 디렉티브를 사용하면 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 서비스를 가져올 수 있습니다. `@inject`에 전달되는 첫 번째 인수는 서비스가 저장될 변수명이며, 두 번째 인수는 주입하고자 하는 서비스의 클래스 또는 인터페이스명입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

때때로 Blade 템플릿 문자열을 즉석에서 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드가 제공하는 `render` 메서드를 사용할 수 있습니다. `render` 메서드는 Blade 템플릿 문자열과, 템플릿에 전달할 선택적 데이터 배열을 인수로 받습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

라라벨은 인라인 Blade 템플릿을 렌더링할 때, 임시 파일을 `storage/framework/views` 디렉터리에 생성합니다. Blade 템플릿 렌더링 후 이 임시 파일을 삭제하고 싶다면, `deleteCachedView` 인수를 메서드에 전달하면 됩니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트(Fragment) 렌더링

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 사용할 때는, HTTP 응답에서 Blade 템플릿의 일부만 반환해야 하는 경우가 있습니다. Blade의 "프래그먼트(fragment)" 기능을 사용하면 이를 손쉽게 구현할 수 있습니다. 우선 템플릿의 원하는 부분을 `@fragment`와 `@endfragment` 디렉티브로 감싸주십시오.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이후, 해당 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출하여 원하는 프래그먼트만 응답에 포함하도록 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 특정 조건에 따라 뷰의 일부 프래그먼트만 반환하거나, 조건이 만족하지 않으면 뷰 전체를 반환할 수 있습니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments` 및 `fragmentsIf` 메서드는 응답에서 여러 개의 뷰 프래그먼트를 반환할 때 사용할 수 있습니다. 반환된 프래그먼트들은 이어 붙여집니다.

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

Blade에서는 `directive` 메서드를 사용해 나만의 커스텀 디렉티브를 정의할 수 있습니다. Blade 컴파일러가 커스텀 디렉티브를 발견하면, 해당 디렉티브에 포함된 표현식과 함께 제공한 콜백이 호출됩니다.

다음 예제는 `@datetime($var)` 디렉티브를 정의하며, 이 디렉티브를 사용해 `$var`(DateTime 인스턴스여야 함)가 원하는 형식의 날짜로 표시되도록 만듭니다.

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

이처럼, 전달받은 표현식에 `format` 메서드를 체이닝하여, 해당 표현식을 원하는 형식으로 렌더링합니다. 이 예제의 결과로 실제 Blade가 생성하는 PHP 코드는 다음과 같습니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 후에는 모든 Blade 뷰의 캐시를 삭제해야 합니다. 캐시된 Blade 뷰는 `view:clear` Artisan 명령어로 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러(Custom Echo Handlers)

Blade에서 객체를 `{{ }}`로 "에코"할 때, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 그러나 사용 중인 클래스가 외부 라이브러리 소속이어서 `__toString` 메서드를 수정할 수 없는 상황도 있습니다.

이러한 경우, Blade에서는 특정 객체 타입에 대한 커스텀 에코 핸들러를 등록할 수 있습니다. 이를 위해 Blade의 `stringable` 메서드를 호출하면 됩니다. `stringable` 메서드는 클로저를 인수로 받으며, 이 클로저는 렌더링을 책임지는 객체의 타입을 타입힌트로 지정해야 합니다. 일반적으로 이 코드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 작성합니다.

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

이렇게 커스텀 에코 핸들러를 정의하면, Blade 템플릿에서 해당 객체를 그냥 에코(출력)만 해도 됩니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문(Custom If Statements)

단순한 커스텀 조건문을 정의할 때는, 직접 디렉티브를 만드는 것보다 더 간단하게 처리할 수 있습니다. 이를 위해 Blade는 클로저를 활용한 커스텀 조건 디렉티브를 빠르게 정의할 수 있는 `Blade::if` 메서드를 제공합니다. 예를 들어, 애플리케이션의 기본 "디스크" 설정값이 무엇인지 확인하는 커스텀 조건문을 정의해보겠습니다. 이 작업은 `AppServiceProvider`의 `boot` 메서드에서 수행할 수 있습니다.

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

맞춤형 조건 디렉티브를 정의했다면, 이제 템플릿에서 아래와 같이 사용할 수 있습니다.

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