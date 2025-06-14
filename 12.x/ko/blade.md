# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 기능 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔터티 인코딩](#html-entity-encoding)
    - [블레이드와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
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
    - [Index 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어 키워드](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 Index 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성(attribute)](#data-properties-attributes)
    - [상위 데이터 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축하기](#building-layouts)
    - [컴포넌트를 활용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 활용한 레이아웃](#layouts-using-template-inheritance)
- [폼 (Forms)](#forms)
    - [CSRF 필드](#csrf-field)
    - [Method 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택 (Stacks)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 라라벨과 함께 제공되는, 간단하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 순수 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되며, 수정될 때까지 캐시에 저장되므로, Blade는 애플리케이션에 거의 부하를 주지 않습니다. Blade 템플릿 파일의 확장자는 `.blade.php`이며 일반적으로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 설명한 것처럼, `view` 헬퍼의 두 번째 인수를 사용해 Blade 뷰로 데이터를 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 기능 강화하기

Blade 템플릿을 한 단계 업그레이드하여 동적인 인터페이스를 쉽고 빠르게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 참고해보세요. Livewire를 이용하면 React나 Vue와 같은 프론트엔드 프레임워크에서만 가능했던 동적 기능을 갖춘 Blade 컴포넌트를 만들 수 있습니다. 이는 번거로운 빌드 과정이나 클라이언트 사이드 렌더링 없이, 모던하고 반응성이 뛰어난 프론트엔드를 개발할 수 있는 훌륭한 방법을 제공합니다.

<a name="displaying-data"></a>
## 데이터 표시

Blade 뷰로 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해봅시다.

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

위와 같이 `name` 변수를 다음처럼 화면에 표시할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 자동 처리됩니다.

뷰에 전달된 변수의 내용만 표시할 필요는 없습니다. 어떤 PHP 함수의 결과든 에코해서 표시할 수 있습니다. 실제로, Blade 에코 구문 안에 원하는 모든 PHP 코드를 넣을 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔터티 인코딩

기본적으로 Blade(및 라라벨의 `e` 함수)는 HTML 엔터티를 이중 인코딩(double encoding)합니다. 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

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
#### 이스케이프되지 않은 데이터 표시

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 자동 처리됩니다. 만약 데이터가 이스케이프되지 않도록 출력하고 싶다면, 다음 문법을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공한 내용을 그대로 에코할 때에는 매우 주의해야 합니다. 사용자 입력 데이터를 표시할 때는 일반적으로 XSS 공격을 방지하기 위해 이스케이프되는 이중 중괄호(`{{ }}`) 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 JavaScript 프레임워크

많은 JavaScript 프레임워크 역시 브라우저에서 표현식을 표시할 때 중괄호를 사용합니다. 이때 Blade가 해당 표현식을 처리하지 않도록 하려면, `@` 기호를 앞에 붙여 Blade 렌더링 엔진이 해당 구문을 무시하게 만들 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade에 의해 제거되고, `{{ name }}` 표현식은 Blade 엔진에서 손대지 않은 채 그대로 남아, JavaScript 프레임워크가 렌더링할 수 있게 됩니다.

또한, `@` 기호는 Blade 디렉티브(예: `@if`)를 이스케이프(escape)하는 데에도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

때로는 JavaScript 변수를 초기화하기 위해 배열을 JSON으로 변환하여 뷰에 전달하고자 할 수 있습니다. 예를 들어 다음과 같이 작성할 수 있습니다.

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

그러나 수동으로 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받으면서, HTML 인용부호(quotation) 안에 안전하게 포함될 수 있도록 JSON 결과를 적절히 이스케이프 처리해줍니다. `from` 메서드는 제공한 객체 또는 배열을 정상적인 자바스크립트 객체로 변환하는 `JSON.parse` 구문이 포함된 문자열을 반환합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

라라벨 최신 버전의 애플리케이션 기본 구조에는 `Js` 파사드(facade)가 내장되어 있으므로, Blade 템플릿에서 더 간편하게 사용할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿은 정규 표현식 기반으로 파싱되므로, 복잡한 표현식을 이 디렉티브에 전달하면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 많은 부분에서 JavaScript 변수를 표시해야 하는 경우, `@verbatim` 디렉티브로 HTML 구역을 감싸면 매번 `@` 기호를 앞에 붙이지 않아도 됩니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 디렉티브

템플릿 상속, 데이터 표시와 더불어, Blade는 조건문 및 반복문 등 자주 사용하는 PHP 제어 구조를 간편하게 사용할 수 있는 다양한 단축 구문(디렉티브)을 제공합니다. 이러한 단축 구문은 PHP의 제어 구조와 동일한 동작을 하면서도 훨씬 간결하고 읽기 쉬운 코드를 작성할 수 있도록 도와줍니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용하여 `if` 문을 만들 수 있습니다. 이 디렉티브들은 PHP의 기본 `if` 문과 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

더 편리하게 사용할 수 있도록 `@unless` 디렉티브도 제공합니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

앞에서 소개한 조건문 디렉티브 외에도, `@isset`과 `@empty` 디렉티브를 이용해 각각 PHP의 `isset` 및 `empty` 함수와 같은 역할을 간편하게 처리할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브를 통해 현재 사용자가 [인증](/docs/12.x/authentication)되었는지, 혹은 게스트인지 빠르게 확인할 수 있습니다.

```blade
@auth
    // 사용자가 인증되었습니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면 인증 시 사용할 특정 가드를 지정할 수도 있습니다.

```blade
@auth('admin')
    // 사용자가 인증되었습니다...
@endauth

@guest('admin')
    // 사용자가 인증되지 않았습니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 디렉티브

`@production` 디렉티브를 사용해 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // 프로덕션 환경에서만 표시되는 내용...
@endproduction
```

또는, 특정 환경에서 실행 중인지 확인하려면 `@env` 디렉티브를 사용할 수 있습니다.

```blade
@env('staging')
    // 현재 "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // 현재 "staging" 또는 "production" 환경에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션(Section) 디렉티브

템플릿 상속에서 특정 섹션에 내용이 있는지 확인하려면 `@hasSection` 디렉티브를 사용할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

특정 섹션에 내용이 없는지 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 디렉티브

`@session` 디렉티브를 사용하면 [세션](/docs/12.x/session) 값이 존재하는지 확인할 수 있습니다. 세션 값이 존재할 경우, `@session`과 `@endsession` 사이의 템플릿 내용이 평가됩니다. 이 구간 안에서는 `$value` 변수를 에코하여 세션 값을 표시할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 활용해 Switch 문을 작성할 수 있습니다.

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

조건문 외에도, Blade는 PHP의 다양한 반복문 제어 구조에 대응하는 간단한 디렉티브를 제공합니다. 역시 각 디렉티브는 PHP의 반복문과 동일하게 동작합니다.

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
> `foreach` 반복문에서 [loop 변수](#the-loop-variable)를 사용하면 현재 반복이 처음인지, 마지막 반복인지 등 유용한 정보를 확인할 수 있습니다.

반복문 사용 시, `@continue`와 `@break` 디렉티브로 반복을 건너뛰거나 즉시 종료할 수 있습니다.

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

또한, 조건을 디렉티브 선언부에 직접 넣어서 사용할 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 안에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수로 현재 반복의 인덱스, 반복 횟수, 현재가 첫 번째/마지막 반복인지를 포함한 다양한 정보에 접근할 수 있습니다.

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

반복문이 중첩된 경우 상위 반복문(`parent`)의 `$loop` 변수도 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 아래와 같은 다양한 유용한 속성이 있습니다.

<div class="overflow-auto">

| 속성(Property)     | 설명                                                            |
| ------------------ | -------------------------------------------------------------- |
| `$loop->index`     | 현재 반복의 인덱스(0부터 시작).                                 |
| `$loop->iteration` | 현재 반복 횟수(1부터 시작).                                    |
| `$loop->remaining` | 반복문에서 남은 반복 횟수.                                     |
| `$loop->count`     | 반복 대상 배열의 전체 아이템 수.                               |
| `$loop->first`     | 현재 반복이 첫 번째 반복인지 여부.                              |
| `$loop->last`      | 현재 반복이 마지막 반복인지 여부.                              |
| `$loop->even`      | 현재 반복 횟수가 짝수인지 여부.                                |
| `$loop->odd`       | 현재 반복 횟수가 홀수인지 여부.                                |
| `$loop->depth`     | 현재 반복문의 중첩 레벨.                                        |
| `$loop->parent`    | 중첩 반복문에서 상위 반복문의 loop 변수.                       |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 디렉티브를 사용하면 특정 조건에 따라 CSS 클래스 문자열을 손쉽게 조합할 수 있습니다. 이 디렉티브는 배열을 인수로 받아, 키에는 적용할 클래스(또는 클래스 목록), 값에는 불린(Boolean) 표현식을 지정합니다. 숫자 키를 갖는 배열 요소는 조건과 상관없이 항상 클래스 목록에 포함됩니다.

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

마찬가지로, `@style` 디렉티브를 사용하면 조건에 따라 인라인 CSS 스타일을 간단하게 적용할 수 있습니다.

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

더 편리하게, 주어진 HTML 체크박스 입력 요소가 "checked" 상태임을 쉽게 표시하려면 `@checked` 디렉티브를 사용할 수 있습니다. 이 디렉티브의 조건이 `true`로 평가되면 `checked`를 자동으로 출력합니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, 셀렉트 박스의 특정 옵션을 "selected" 상태로 표시하려면 `@selected` 디렉티브를 사용할 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한 `@disabled` 디렉티브는 해당 요소를 "disabled" 상태로, `@readonly` 디렉티브는 "readonly" 속성으로 표시하는 데 사용할 수 있습니다.

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

`@required` 디렉티브를 사용하면 해당 요소가 "required" 상태인지 표시할 수도 있습니다.

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
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 장점이 있으므로 `@include`보다 컴포넌트 사용을 권장합니다.

Blade의 `@include` 디렉티브는 하나의 Blade 뷰에서 다른 Blade 뷰를 간편하게 포함할 수 있도록 해줍니다. 부모 뷰에서 사용할 수 있는 모든 변수들은 포함된 뷰에서도 그대로 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰는 부모 뷰의 모든 데이터를 기본적으로 전달받지만, 추가로 포함 뷰에서만 사용할 데이터 배열을 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

만약 존재하지 않는 뷰를 `@include` 하려고 하면 라라벨에서 오류가 발생합니다. 뷰가 없을 수도 있음을 고려해야 할 경우에는 `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

조건이 `true` 또는 `false`일 때에 따라 뷰를 포함하고자 한다면 `@includeWhen` 및 `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에서 가장 먼저 존재하는 뷰만 포함하고 싶다면 `includeFirst` 디렉티브를 사용하면 됩니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__` 및 `__FILE__` 상수 사용은 피해야 합니다. 이 값들은 캐시에 저장된 컴파일된 뷰 파일의 위치를 가리키게 됩니다.

<a name="rendering-views-for-collections"></a>

#### 컬렉션을 위한 뷰 렌더링

Blade의 `@each` 디렉티브를 사용하면, 반복문과 포함(include)을 한 줄로 합칠 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

`@each` 디렉티브의 첫 번째 인자는 컬렉션이나 배열의 각 요소를 렌더링할 때 사용할 뷰 이름입니다. 두 번째 인자에는 반복할 배열이나 컬렉션을 전달합니다. 세 번째 인자는 현재 반복되는 아이템이 뷰 내부에서 할당될 변수명을 지정합니다. 예를 들어 `jobs` 배열을 반복한다면, 각 반복에서 `job` 변수로 접근하게 됩니다. 현재 반복의 배열 키는 뷰에서 `key` 변수로 사용할 수 있습니다.

추가로 네 번째 인자를 `@each` 디렉티브에 전달할 수 있는데, 이 인자는 전달된 배열이 비어있을 때 렌더링될 뷰를 지정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`를 통해 렌더링된 뷰는 부모 뷰의 변수를 상속받지 않습니다. 만약 자식 뷰에서 이러한 변수를 사용해야 한다면, `@foreach`와 `@include` 디렉티브를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브를 이용하면 페이지 렌더링 주기마다 한 번만 실행되는 템플릿 일부를 정의할 수 있습니다. 예를 들어, [스택(stacks)](#stacks)을 활용하여 특정 자바스크립트 코드를 헤더에 한 번만 삽입하고 싶은 경우에 유용합니다. 반복문 안에서 [컴포넌트](#components)를 렌더링할 때, 자바스크립트를 컴포넌트가 처음 렌더링될 때에만 헤더에 넣고 싶을 수 있습니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once` 디렉티브는 주로 `@push`나 `@prepend` 디렉티브와 함께 사용되기 때문에, 편의상 `@pushOnce`와 `@prependOnce`와 같은 디렉티브도 사용할 수 있습니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP 코드 사용

특정 상황에서는 뷰에 직접 PHP 코드를 삽입하는 것이 유용할 수 있습니다. Blade의 `@php` 디렉티브를 사용하면, 템플릿 안에서 일반 PHP 코드를 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

또는 클래스 임포트와 같이 간단히 PHP를 사용하려면 `@use` 디렉티브를 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

`@use` 디렉티브에 두 번째 인자를 전달하면, 클래스에 별칭(alias)을 지정할 수도 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

동일한 네임스페이스에 여러 클래스가 있을 경우, 이러한 클래스들을 묶어서 임포트할 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

또한, `@use` 디렉티브는 `function` 또는 `const` 키워드를 경로 앞에 붙이면, PHP 함수와 상수도 임포트할 수 있습니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

클래스 임포트와 마찬가지로, 함수와 상수도 별칭(alias)을 지정할 수 있습니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수와 상수 임포트 역시 중괄호({})로 묶어서 한 번에 여러 개를 가져올 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade는 뷰 안에서 주석을 정의할 수 있는 방법도 제공합니다. Blade 주석은 HTML 주석과 달리, 애플리케이션이 반환하는 최종 HTML에 포함되지 않습니다.

```blade
{{-- 이 주석은 렌더링된 HTML에 나타나지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드(@include)와 비슷한 이점을 제공하며, 어떤 개발자에게는 컴포넌트와 슬롯이 더 이해하기 쉬울 수 있습니다. 컴포넌트를 작성하는 방법에는 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트, 이렇게 두 가지가 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` Artisan 명령어를 사용할 수 있습니다. 예를 들어, 간단한 `Alert` 컴포넌트를 생성해 보겠습니다. `make:component` 명령어를 실행하면, 컴포넌트 클래스 파일이 `app/View/Components` 디렉토리에 생성됩니다.

```shell
php artisan make:component Alert
```

이 명령은 컴포넌트용 뷰 템플릿도 생성합니다. 이 뷰 파일은 `resources/views/components` 디렉토리에 저장됩니다. 컴포넌트를 직접 작성할 때는, 기본적으로 `app/View/Components`와 `resources/views/components` 디렉토리 내의 컴포넌트 파일들이 자동으로 감지되기 때문에 별도의 컴포넌트 등록 작업은 필요하지 않습니다.

또한, 하위 디렉토리 내에 컴포넌트를 생성할 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령을 실행하면 `app/View/Components/Forms` 디렉토리에 `Input` 컴포넌트가, 그리고 `resources/views/components/forms` 디렉토리에 뷰 파일이 생성됩니다.

클래스 없이 Blade 템플릿 파일만 존재하는 익명 컴포넌트를 생성하고 싶다면, `make:component` 명령 실행 시 `--view` 플래그를 사용할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

위 명령을 실행하면 `resources/views/components/forms/input.blade.php`에 Blade 파일이 생성되고, 이는 `<x-forms.input />` 형태로 컴포넌트처럼 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자체 애플리케이션의 컴포넌트는 앞서 설명한 경로에서 자동으로 감지됩니다.

하지만 패키지 개발 시에는, Blade 컴포넌트를 직접 등록해주어야 합니다. 이 경우, 보통 패키지의 서비스 제공자(Service Provider)의 `boot` 메서드에서 컴포넌트 클래스와 HTML 태그 별칭(alias)을 등록해야 합니다.

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

컴포넌트를 등록하면, HTML 태그 별칭으로 다음과 같이 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는, `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 네임스페이스별로 자동 로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 있을 때 다음과 같이 설정 가능합니다.

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

이렇게 하면, 벤더 네임스페이스를 활용해 `package-name::` 구문으로 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 태그 이름을 PascalCase로 변환하여 연결된 클래스를 자동으로 감지합니다. 하위 디렉토리 구조도 "점(dot) 표기법"으로 사용할 수 있습니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 화면에 표시하려면 Blade 템플릿 안에 컴포넌트 태그를 사용하면 됩니다. 컴포넌트 태그는 `x-`로 시작하고, 그 뒤에 컴포넌트 클래스명을 케밥(case) 형태로 작성합니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉토리 내에서 더 깊게 중첩되어 있다면, 디렉토리 중첩을 `.` 문자로 표시할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면 아래와 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶다면 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 컴포넌트는 렌더링되지 않습니다.

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

컴포넌트를 그룹별로 디렉토리에 모으고 싶을 때가 종종 있습니다. 예를 들어, 다음과 같이 "카드(card)" 컴포넌트 관련 클래스를 구조화할 수 있습니다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

루트 `Card` 컴포넌트가 `Card` 디렉토리 안에 있기 때문에, 보통은 `<x-card.card>`와 같이 사용해야 할 것 같지만, 라라벨은 컴포넌트 파일명과 디렉토리명이 같으면 해당 컴포넌트를 "루트" 컴포넌트로 간주해, 디렉토리명을 한 번만 적어도 사용할 수 있게 해줍니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트로 데이터 전달하기

Blade 컴포넌트에 데이터를 전달할 때는 HTML 속성(attribute)을 사용할 수 있습니다. 숫자나 문자열 등 하드코딩된 기본 값은 일반 HTML 속성 문자열로 전달하고, PHP 표현식이나 변수를 전달할 때는 `:`(콜론)을 속성명 앞에 붙여 전달합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에 해당 데이터 속성을 정의해주면 됩니다. 컴포넌트의 모든 public 속성(property)은 자동으로 컴포넌트 뷰에서 사용할 수 있습니다. 데이터를 뷰로 따로 전달하기 위해 `render` 메서드에서 별도의 작업을 할 필요가 없습니다.

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
     * 컴포넌트를 렌더링할 뷰 또는 내용을 반환합니다.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, public 변수의 값을 변수명 그대로 출력하면 데이터를 보여줄 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이스 규칙

컴포넌트 생성자 인자는 `camelCase` 표기를 사용해야 하며, HTML 속성에서 참조할 때는 `kebab-case`로 표기해야 합니다. 예를 들어, 아래와 같이 생성자를 정의했다면

```php
/**
 * 컴포넌트 인스턴스를 생성합니다.
 */
public function __construct(
    public string $alertType,
) {}
```

컴포넌트에는 다음과 같이 값을 전달합니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 단축 문법

컴포넌트에 속성을 전달할 때, "단축 속성" 문법을 사용할 수도 있습니다. 이런 방식은 속성명과 변수명이 일치하는 경우 매우 편리합니다.

```blade
{{-- 단축 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 다음과 동일합니다. --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같은 자바스크립트 프레임워크에서는 속성명 앞에 콜론(:)을 사용하는 경우가 있습니다. 이런 경우, Blade에서 해당 속성이 PHP 표현식이 아님을 알리려면 두 개의 콜론(`::`)을 속성명 앞에 붙이면 됩니다. 예를 들어 아래처럼 사용할 수 있습니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

이렇게 하면 다음과 같이 렌더링됩니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서는 public 변수뿐만 아니라, public 메서드도 호출할 수 있습니다. 예를 들어, 다음과 같이 `isSelected`라는 메서드를 가진 컴포넌트가 있다고 가정해 봅시다.

```php
/**
 * 전송된 옵션이 현재 선택된 옵션인지 확인합니다.
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
#### 컴포넌트 클래스 내에서 어트리뷰트 및 슬롯 접근

Blade 컴포넌트에서는 컴포넌트명, 속성, 슬롯(slot)에 접근할 수 있습니다. 이 데이터를 사용하려면 컴포넌트의 `render` 메서드에서 클로저를 반환하면 됩니다.

```php
use Closure;

/**
 * 컴포넌트를 렌더링할 뷰 또는 내용을 반환합니다.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

컴포넌트의 `render` 메서드에서 반환하는 클로저는 `$data` 배열을 인자로 받을 수 있으며, 이 배열에는 여러 컴포넌트 관련 정보가 담깁니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열에 들어있는 값들을 Blade 문자열로 직접 삽입하면, 악의적인 속성 데이터로 인해 원격 코드 실행이 발생할 수 있으니 절대로 직접 삽입해서는 안 됩니다.

`componentName`은 HTML 태그에서 `x-` 접두어 다음에 오는 이름과 동일합니다. 예를 들어 `<x-alert />`의 `componentName`은 `alert`가 됩니다. `attributes` 요소에는 태그의 모든 속성이 담기고, `slot` 요소는 컴포넌트 슬롯의 내용을 갖는 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저는 문자열을 반환해야 하며, 반환된 문자열이 실제 뷰의 이름이라면 해당 뷰를, 아니라면 인라인 Blade 뷰로 렌더링됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트가 라라벨의 [서비스 컨테이너](/docs/12.x/container)에서 의존성을 받아야 할 때는, 생성자의 데이터 속성보다 앞쪽에 추가하면 컨테이너가 자동으로 주입해줍니다.

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
#### 어트리뷰트/메서드 숨김 처리

특정 public 메서드나 속성을 컴포넌트 템플릿에서 변수로 노출하지 않으려면, 컴포넌트 클래스에 `$except` 배열 속성을 추가하면 됩니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출하지 않을 속성/메서드를 정의합니다.
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
### 컴포넌트 어트리뷰트(속성)

위에서 살펴본 것처럼 데이터 속성을 컴포넌트에 전달할 수 있지만, 때로는 컴포넌트의 기능과 직접 관련 없는 추가적인 HTML 속성(예: `class`)을 지정할 필요가 있습니다. 대개 이런 추가 속성들은 컴포넌트 템플릿의 루트 엘리먼트로 전달되길 원합니다. 예를 들어, 아래처럼 alert 컴포넌트를 렌더링한다고 합시다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 정의되지 않은 모든 속성은 자동으로 "속성 백(attribute bag)"에 모아집니다. 이 속성 백은 `$attributes` 변수로 컴포넌트에서 사용할 수 있고, 템플릿에서 해당 변수를 출력하면 모든 속성이 렌더링됩니다.

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현재로서는 컴포넌트 태그 내부에서 `@env`와 같은 디렉티브를 사용하는 것은 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 값/병합된 속성

속성의 기본값을 지정하거나, 속성에 값을 추가(병합)해야 할 때는 속성 백의 `merge` 메서드를 사용할 수 있습니다. 특히 기본 CSS 클래스 목록을 지정하는 데 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 아래와 같이 사용할 때,

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링되는 HTML은 다음과 같습니다.

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### CSS 클래스 조건부 병합

특정 조건일 때만 클래스를 병합하고 싶을 때는 `class` 메서드를 사용할 수 있습니다. 배열의 키에 추가하고 싶은 클래스명을, 값에 해당 조건을 넣습니다. 배열 요소의 키가 숫자일 경우, 항상 렌더링된 클래스가 됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

속성 백에 다른 속성을 함께 병합하고 싶으면, `class` 메서드 뒤에 `merge` 메서드를 연결할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성이 적용되지 않는 다른 HTML 요소에서 조건부 클래스를 컴파일해야 할 경우, [@class 디렉티브](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### class가 아닌 속성 병합

`class` 속성이 아닌 다른 속성을 병합할 때는, `merge`에 지정한 값이 해당 속성의 기본값이 됩니다. 하지만 `class`와 달리, 이 속성들은 병합되지 않고, 주입된 값이 있으면 기본값을 덮어씌웁니다. 예를 들어, 아래는 버튼 컴포넌트 구현 예시입니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

버튼 컴포넌트를 커스텀 `type` 속성과 함께 렌더링하려면 다음과 같이 사용할 수 있습니다. 만약 `type`을 지정하지 않으면 기본값 `button`이 사용됩니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

이 경우 실제로 렌더링되는 HTML은 아래와 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

만약 `class`가 아닌 다른 속성도 기본값과 주입값을 모두 함께 사용하고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예에서는 `data-controller` 속성이 항상 `profile-controller`로 시작되며, 추가로 전달된 `data-controller` 값들이 그 뒤에 붙습니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 사용하면, 조건에 따라 속성을 필터링할 수 있습니다. 이 메서드는 클로저를 인자로 받으며, 클로저에서 `true`를 반환하면 해당 속성이 보존됩니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

특정 문자열로 시작하는 모든 속성을 추출하려면, `whereStartsWith` 메서드를 사용하세요.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, 특정 문자열로 시작하지 않는 속성만 추출하려면, `whereDoesntStartWith` 메서드를 사용합니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용하면, 해당 속성 백에서 첫 번째 속성만 렌더링할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

컴포넌트에 특정 속성이 존재하는지 확인하려면, `has` 메서드를 사용할 수 있습니다. 이 메서드는 속성명을 인자로 받고, 해당 속성이 있으면 `true`를 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열을 전달하면, 주어진 모든 속성이 존재해야 `true`를 반환합니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny` 메서드를 사용하면, 주어진 속성 중 하나라도 존재하면 `true`를 반환합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성값을 가져오려면, `get` 메서드를 사용하세요.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 전달된 속성명만 추출합니다.

```blade
{{ $attributes->only(['class']) }}
```

`except` 메서드는 전달된 속성명을 제외한 나머지 속성을 반환합니다.

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>

### 예약된 키워드

기본적으로, 일부 키워드는 Blade 내부적으로 컴포넌트 렌더링에 사용되기 위해 예약되어 있습니다. 아래에 나열된 키워드들은 컴포넌트 내에서 public 속성이나 메서드명으로 정의할 수 없습니다.

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

컴포넌트에 "슬롯(slot)"을 이용해 추가적인 콘텐츠를 전달해야 할 때가 많습니다. 컴포넌트 슬롯은 `$slot` 변수를 출력함으로써 렌더링됩니다. 이 개념을 살펴보기 위해, `alert` 컴포넌트가 다음과 같은 마크업을 가지고 있다고 가정하겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

아래와 같이 컴포넌트에 내용을 삽입하면 `slot`으로 콘텐츠를 전달할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

때로는 컴포넌트 내의 여러 위치에서 서로 다른 슬롯을 렌더링할 필요가 있습니다. 이번엔 "title"이라는 슬롯을 삽입할 수 있도록 alert 컴포넌트를 수정해 보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯의 내용을 정의하려면 `x-slot` 태그를 사용하면 됩니다. 명시적으로 `x-slot` 태그로 감싸지 않은 콘텐츠는 모두 `$slot` 변수로 컴포넌트에 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 내용이 있는지 확인할 때에는 `isEmpty` 메서드를 사용할 수 있습니다.

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

또한, 슬롯에 HTML 주석이 아닌 "실제" 콘텐츠가 있는지 확인하려면 `hasActualContent` 메서드를 사용할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯(Scoped Slots)

Vue와 같은 JavaScript 프레임워크를 사용해 본 적이 있다면, 컴포넌트 내부의 데이터나 메서드에 슬롯에서 접근할 수 있는 "스코프 슬롯" 개념에 익숙할 수 있습니다. 라라벨에서도 컴포넌트 클래스에 public 메서드나 속성을 정의하고, 슬롯 내에서 `$component` 변수를 통해 컴포넌트에 접근함으로써 유사한 동작을 구현할 수 있습니다. 예를 들어, `x-alert` 컴포넌트 클래스에 `formatAlert`라는 public 메서드가 정의되어 있다고 가정해보겠습니다.

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

Blade 컴포넌트와 마찬가지로, 슬롯에도 CSS 클래스명 등 추가 [속성(attributes)](#component-attributes)을 지정할 수 있습니다.

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

슬롯 속성과 상호작용하려면 슬롯 변수의 `attributes` 속성에 접근할 수 있습니다. 속성 조작 방법에 대한 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요.

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

아주 작은 컴포넌트의 경우, 컴포넌트 클래스와 컴포넌트 뷰 파일을 따로 관리하는 것이 번거롭게 느껴질 수 있습니다. 이런 경우 `render` 메서드에서 직접 컴포넌트의 마크업을 반환할 수 있습니다.

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

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령어 실행 시 `--inline` 옵션을 사용할 수 있습니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

경우에 따라 어떤 컴포넌트를 렌더링해야 할지 런타임까지 알 수 없는 상황이 있을 수 있습니다. 이런 경우, 라라벨의 내장 `dynamic-component` 컴포넌트를 사용해 런타임 값이나 변수에 따라 컴포넌트를 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래 컴포넌트 수동 등록 문서는 패키지에 뷰 컴포넌트를 포함하는 경우에 주로 해당됩니다. 만약 패키지를 작성하지 않는 경우라면 이 부분은 대개 필요하지 않습니다.

자신의 애플리케이션에서 컴포넌트를 개발할 때에는 `app/View/Components` 디렉터리나 `resources/views/components` 디렉터리 내의 컴포넌트가 자동으로 인식됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 작성하거나, 비표준 디렉터리에 컴포넌트를 배치하는 경우에는 반드시 컴포넌트 클래스와 해당 HTML 태그 별칭을 직접 등록해야 라라벨이 해당 컴포넌트를 어디서 찾을지 알 수 있습니다. 일반적으로 이러한 등록 작업은 패키지 서비스 프로바이더의 `boot` 메서드 안에서 수행합니다.

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

컴포넌트를 등록하면 다음과 같이 태그 별칭을 사용하여 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로드

또한 `componentNamespace` 메서드를 활용하면 네임스페이스 규칙에 따라 컴포넌트 클래스를 자동으로 불러올 수 있습니다. 예를 들어, `Nightshade` 패키지가 `Package\Views\Components` 네임스페이스에 `Calendar`와 `ColorPicker` 컴포넌트를 포함하고 있다고 가정해 보겠습니다.

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

이렇게 등록하면 아래처럼 벤더 네임스페이스와 `package-name::` 구문을 조합하여 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 자동으로 해당 클래스를 연결합니다. 하위 디렉터리도 "dot" 표기법을 이용해 지원됩니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트(Anonymous Components)

인라인 컴포넌트와 유사하게, 익명 컴포넌트는 단일 파일로 컴포넌트를 관리할 수 있는 방법을 제공합니다. 단, 익명 컴포넌트는 별도의 클래스 없이 단일 Blade 뷰 파일만 사용합니다. 익명 컴포넌트를 정의하려면 `resources/views/components` 디렉터리 안에 Blade 템플릿을 하나 두기만 하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php` 위치에 컴포넌트를 작성한 경우 다음과 같이 렌더링할 수 있습니다.

```blade
<x-alert/>
```

컴포넌트가 `components` 디렉터리 하위에 더 깊게 중첩되어 있으면 `.` 표기법으로 사용할 수 있습니다. 예를 들어, 다음과 같이 정의했다면

```blade
<x-inputs.button/>
```

과 같이 렌더링됩니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

종종 컴포넌트가 여러 Blade 템플릿으로 구성되는 경우, 관련된 템플릿을 하나의 디렉터리 내부에 그룹화하고 싶을 때가 있습니다. 예를 들어, 아래와 같이 "accordion" 컴포넌트의 디렉터리 구조가 있다고 가정합시다.

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 구조에서는 다음과 같이 accordion 및 그 item을 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 이 방식으로 `x-accordion`을 렌더링하려면 "index" 역할의 accordion 컴포넌트 템플릿을 `resources/views/components` 디렉터리에 놓아야만 했습니다.

Blade는 디렉터리명과 동일한 파일을 해당 컴포넌트의 디렉터리 안에 둘 수 있게 해줍니다. 이렇게 하면 이 템플릿이 "루트" 요소로 렌더링됩니다. 따라서 위의 Blade 예제를 그대로 사용할 수 있고, 디렉터리 구조만 다음과 같이 바꾸면 됩니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성(attribute)

익명 컴포넌트에는 관련된 클래스가 없으므로, 어떤 데이터를 컴포넌트 변수로 전달해야 하는지, 어떤 속성이 [속성 배지(attribute bag)](#component-attributes)에 포함되어야 하는지 구분이 필요할 수 있습니다.

컴포넌트 Blade 템플릿의 최상단에서 `@props` 디렉티브를 사용해 데이터 변수로 간주할 속성을 지정할 수 있습니다. 컴포넌트의 다른 모든 속성은 속성 배지로 전달됩니다. 각 데이터 변수에 기본값을 지정하고 싶다면 배열의 키-값 형태로 정의할 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 컴포넌트를 정의하면 다음처럼 렌더링할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근하기

때로는 자식 컴포넌트 내부에서 부모 컴포넌트의 데이터를 참조하고 싶을 때가 있습니다. 이런 경우에는 `@aware` 디렉티브를 사용할 수 있습니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`으로 구성된 복잡한 메뉴를 만든다고 가정해 보겠습니다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 `<x-menu>` 컴포넌트 구현 예시는 다음과 같습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

위 `color` prop은 부모(`<x-menu>`)에만 전달 되었으므로 자식 `<x-menu.item>`에서는 바로 사용할 수 없습니다. 하지만 `@aware` 디렉티브를 사용하면 자식에서도 해당 prop을 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터에만 접근할 수 있습니다. 부모 컴포넌트의 `@props` 기본값 중에서 명시적으로 전달되지 않은 값은 `@aware`를 통해 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 설명한 것처럼, 익명 컴포넌트는 일반적으로 `resources/views/components` 디렉터리에 Blade 템플릿을 배치합니다. 하지만 추가적인 익명 컴포넌트 경로를 라라벨에 등록하고 싶을 때가 있을 수 있습니다.

`anonymousComponentPath` 메서드는 익명 컴포넌트의 위치에 해당하는 "경로"를 첫 번째 인수로, 그리고 컴포넌트가 사용할 선택적 "네임스페이스"를 두 번째 인수로 받습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나의 `boot` 메서드에서 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

위 예시처럼 접두사를 지정하지 않고 컴포넌트 경로를 등록하면, 해당 경로에 있는 컴포넌트는 Blade에서 접두사 없이 렌더링할 수 있습니다. 즉, 위 경로에 `panel.blade.php`가 있으면 다음과 같이 사용할 수 있습니다.

```blade
<x-panel />
```

`anonymousComponentPath` 메서드의 두 번째 인수로 접두사(네임스페이스)를 지정할 수도 있습니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이렇게 하면, 해당 네임스페이스 내의 컴포넌트를 렌더링할 때 컴포넌트 이름 앞에 네임스페이스 접두사를 붙여 아래처럼 사용합니다.

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 작성하기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에서 동일하거나 유사한 전체 레이아웃을 사용합니다. 만약 우리가 생성하는 모든 뷰마다 전체 레이아웃 HTML을 반복해야 한다면, 매우 번거롭고 유지 관리가 힘들 것입니다. 다행히, [Blade 컴포넌트](#components)로 레이아웃을 한 번만 정의하고 애플리케이션 전반에 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어, "todo" 목록 앱을 만들면서 아래와 같은 `layout` 컴포넌트를 정의했다고 가정해보겠습니다.

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

`layout` 컴포넌트를 정의했다면, 이제 해당 컴포넌트를 활용하는 Blade 뷰를 만들 수 있습니다. 이번 예시에서는 간단하게 할 일 목록을 표시하는 뷰를 정의해 봅니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 전달되는 내용은 `layout` 컴포넌트에서 기본 `$slot` 변수로 제공됩니다. 그리고, 만약 `$title` 슬롯이 제공되면 해당 값을, 그렇지 않으면 기본 제목을 출력하는 걸 볼 수 있습니다. 할 일 목록 뷰에서 [컴포넌트 문서](#components)에서 설명한 슬롯 문법을 사용해 커스텀 제목을 주입할 수도 있습니다.

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

이제 레이아웃과 할 일 목록 뷰가 모두 정의됐으므로, 라우트에서 `tasks` 뷰를 반환하면 됩니다.

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

레이아웃은 "템플릿 상속(template inheritance)" 방식으로도 만들 수 있습니다. 이 방식은 [컴포넌트](#components) 도입 전까지 주로 사용되던 레이아웃 구현 방식입니다.

먼저 간단한 예제를 살펴보겠습니다. 우선, 아래와 같이 페이지 레이아웃을 정의합니다. 대부분의 웹 애플리케이션은 여러 페이지에서 공통된 레이아웃을 갖기 때문에, 하나의 Blade 뷰로 레이아웃을 정의하면 유용합니다.

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

이 파일은 일반적인 HTML 마크업을 포함합니다. 특별히 `@section`과 `@yield` 디렉티브에 주목해 주세요. `@section`은 특정 콘텐츠 영역을 정의하고, `@yield`는 해당 영역의 내용을 출력할 때 사용됩니다.

이제 레이아웃이 준비되었으니, 이를 상속하는 자식 페이지를 정의해 보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

자식 뷰에서는 `@extends` 디렉티브로 어느 Blade 레이아웃을 "상속"할지 지정할 수 있습니다. 레이아웃을 확장하는 뷰는 `@section` 디렉티브를 사용해 레이아웃의 각 섹션에 콘텐츠를 삽입합니다. 위 예시처럼, 각 섹션의 내용은 레이아웃 내부의 `@yield`를 통해 표시됩니다.

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

위 예시에서 `sidebar` 섹션은 `@@parent` 디렉티브를 활용해 부모 레이아웃의 사이드바에 내용을 추가(덮어쓰기 대신)하고 있습니다. 실제 뷰가 렌더링될 때는 `@@parent` 부분이 레이아웃의 해당 콘텐츠로 교체됩니다.

> [!NOTE]
> 앞선 예시와 달리, 여기에서는 `sidebar` 섹션이 `@show`가 아닌 `@endsection`으로 끝납니다. `@endsection`은 단순히 섹션을 정의만 할 뿐이고, `@show`는 해당 섹션을 정의함과 동시에 즉시 출력(**immediately yield**)합니다.

`@yield` 디렉티브는 두 번째 인수로 기본값도 받을 수 있습니다. 지정된 섹션이 정의되지 않았을 경우 이 값이 출력됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때마다, 폼에 숨겨진 CSRF 토큰 필드를 반드시 포함해야 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 해당 요청을 정상적으로 검증할 수 있습니다. `@csrf` Blade 디렉티브를 사용해 쉽게 토큰 필드를 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드(Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 등의 HTTP 메서드를 사용할 수 없으므로, 이러한 HTTP 동사를 흉내내기 위해 숨겨진 `_method` 필드를 추가해야 합니다. 이때는 `@method` Blade 디렉티브를 사용해 해당 필드를 생성할 수 있습니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러(Validation Errors)

`@error` 디렉티브를 사용하면 주어진 속성에 대해 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 있는지 빠르게 확인할 수 있습니다. `@error` 블록 안에서는 `$message` 변수를 출력하여 에러 메시지를 표시합니다.

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

`@error` 디렉티브는 내부적으로 "if" 문으로 컴파일되기 때문에, `@else`를 사용해 에러가 없을 때의 콘텐츠도 렌더링할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

[특정 에러 백(error bag) 이름](/docs/12.x/validation#named-error-bags)을 `@error`의 두 번째 매개변수로 넘기면, 여러 폼이 있는 페이지에서 유효성 검증 에러 메시지를 가져올 수 있습니다.

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

Blade에서는 명명된 스택에 콘텐츠를 추가(push)할 수 있으며, 이 스택은 다른 뷰나 레이아웃의 원하는 위치에서 렌더링할 수 있습니다. 이 기능은 자식 뷰에서 필요로 하는 JavaScript 라이브러리를 지정할 때 특히 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 불리언 조건식이 `true`로 평가될 때만 `@push`를 실행하고 싶다면, `@pushIf` 디렉티브를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

필요하다면 여러 번 스택에 push할 수 있습니다. 스택의 전체 내용을 렌더링하려면 `@stack` 디렉티브에 스택의 이름을 전달해서 사용합니다.

```blade
<head>
    <!-- 머리말(Head) 내용 -->

    @stack('scripts')
</head>
```

스택의 처음에 콘텐츠를 추가하고 싶다면 `@prepend` 디렉티브를 사용해야 합니다.

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
## 서비스 주입(Service Injection)

`@inject` 디렉티브는 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 서비스를 가져올 때 사용할 수 있습니다. `@inject`의 첫 번째 인수는 서비스가 할당될 변수명이고, 두 번째 인수는 해결(resolve)하고자 하는 서비스의 클래스 또는 인터페이스 이름입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    월간 수익: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

가끔 Blade 템플릿이 들어 있는 문자열을, 바로 유효한 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드에서 제공하는 `render` 메서드를 사용할 수 있습니다. 이 `render` 메서드는 Blade 템플릿 문자열과, 템플릿에 전달될 데이터의 배열을 선택적으로 인수로 받습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

라라벨은 인라인 Blade 템플릿을 렌더링할 때 임시 파일을 `storage/framework/views` 디렉터리에 저장합니다. 만약 Blade 템플릿 렌더링 후 이 임시 파일을 자동으로 제거하고 싶다면, `deleteCachedView` 인수를 추가해서 사용할 수 있습니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트(Fragment) 렌더링

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, HTTP 응답의 일부분으로만 Blade 템플릿의 일부만 반환해야 할 때가 있습니다. Blade의 "프래그먼트(Fragment)" 기능을 이용하면 이와 같은 요구를 쉽게 처리할 수 있습니다. 사용 방법은 다음과 같습니다. 먼저, Blade 템플릿 중 일부 구간을 `@fragment`와 `@endfragment` 디렉티브로 감쌉니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

그리고 해당 Blade 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출하여 어떤 프래그먼트만을 반환할 것인지 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면, 주어진 조건에 따라 특정 프래그먼트만 반환할지 아니면 전체 뷰를 반환할지 선택할 수 있습니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`와 `fragmentsIf` 메서드를 사용하면, 한 번에 여러 프래그먼트를 HTTP 응답으로 반환할 수 있습니다. 이때 지정된 프래그먼트들이 합쳐져서 반환됩니다.

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
## Blade 확장하기(Extending Blade)

Blade에서는 직접 커스텀 디렉티브를 만들어 사용할 수 있습니다. `directive` 메서드를 사용하면 자신만의 맞춤 디렉티브를 정의할 수 있습니다. Blade 컴파일러가 이 커스텀 디렉티브를 만나면, 디렉티브에 전달된 표현식(expression)을 파라미터로 하여 지정한 콜백을 호출합니다.

아래 예시는 `@datetime($var)`라는 디렉티브를 만들어, `DateTime` 인스턴스인 `$var`를 원하는 형식으로 출력하도록 합니다.

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

위와 같이 작성하면, 디렉티브에 전달된 표현식에 대해 `format` 메서드를 체이닝해서 사용할 수 있습니다. 즉, 위 예시에서 이 디렉티브로 최종적으로 생성되는 PHP 코드는 아래와 같습니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 코드를 수정한 후에는, 반드시 Blade 캐시 뷰 파일을 모두 삭제해야 합니다. 캐시된 Blade 뷰 파일들은 `view:clear` Artisan 명령어로 쉽게 제거할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러(Custom Echo Handlers)

Blade에서 어떤 객체를 `{{ ... }}`와 같이 "출력(echo)" 하려고 하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 하지만, 사용 중인 클래스가 외부 라이브러리에 속해 있거나, 여러분이 직접 `__toString` 메서드를 구현할 수 없는 상황도 있습니다.

이럴 때, Blade는 해당 타입의 객체에 대해 커스텀 출력(에코) 핸들러를 등록할 수 있는 기능을 제공합니다. 이를 위해서는 Blade의 `stringable` 메서드를 사용하면 됩니다. `stringable` 메서드는 클로저(익명 함수)를 인수로 받으며, 이 클로저에서 출력할 객체의 타입을 타입힌트로 지정합니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

이처럼 커스텀 에코 핸들러를 정의하면, Blade 템플릿에서 해당 객체를 `{{ ... }}`로 바로 출력할 수 있습니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 조건문(Custom If Statements)

직접 디렉티브를 만들어야 할 정도로 복잡하지 않은, 간단한 커스텀 조건문이 필요하다면, Blade의 `Blade::if` 메서드를 활용할 수 있습니다. 이 방법을 사용하면, 클로저만으로 빠르게 커스텀 조건문 디렉티브를 정의할 수 있습니다. 예를 들어, 애플리케이션에서 설정한 기본 "디스크(disk)"를 확인하는 커스텀 조건문을 정의해보겠습니다. 이 코드는 `AppServiceProvider`의 `boot` 메서드에서 작성하면 됩니다.

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

위와 같이 커스텀 조건문을 정의한 후에는, Blade 템플릿에서 아래와 같이 활용할 수 있습니다.

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크를 사용하고 있습니다... -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크를 사용하고 있습니다... -->
@else
    <!-- 애플리케이션이 다른 디스크를 사용하고 있습니다... -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크를 사용하지 않고 있습니다... -->
@enddisk
```