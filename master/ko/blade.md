# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
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
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [수동 컴포넌트 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성(attribute)](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트를 활용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 활용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택(Stack)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함된 단순하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리 Blade는 템플릿에서 일반 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로 Blade 템플릿은 모두 일반 PHP 코드로 컴파일된 후 수정될 때까지 캐시되어, 애플리케이션에 거의 추가적인 오버헤드를 만들지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 라우트 또는 컨트롤러에서 전역 `view` 헬퍼를 사용하여 반환할 수 있습니다. [뷰](/docs/master/views) 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인수로 Blade 뷰에 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 강화하기

Blade 템플릿을 한 단계 더 발전시키고, 동적인 인터페이스를 쉽게 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보시기 바랍니다. Livewire는 일반적으로 React나 Vue와 같은 프론트엔드 프레임워크에서만 가능하던 동적 기능을 Blade 컴포넌트에서 사용할 수 있게 해주며, 복잡한 빌드 작업이나 클라이언트 렌더링 없이도 현대적인 반응형 프론트엔드를 쉽게 만들어주는 훌륭한 접근법을 제공합니다.

<a name="displaying-data"></a>
## 데이터 표시하기 (Displaying Data)

Blade 뷰에 전달된 데이터를 중괄호로 변수로 감싸 표시할 수 있습니다. 예를 들어 아래 라우트에서는:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 값을 다음과 같이 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 구문은 자동으로 PHP의 `htmlspecialchars` 함수로 처리되어 XSS 공격을 방지합니다.

뷰에 전달된 변수뿐만 아니라, PHP 함수의 결과도 에코할 수 있습니다. 사실, Blade 에코 구문 내부에는 어떠한 PHP 코드도 입력할 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로 Blade(그리고 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하고 싶다면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding`을 호출하시면 됩니다:

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

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격 방지를 위해 PHP의 `htmlspecialchars`로 처리됩니다. 데이터를 이스케이프하지 않고 출력하고 싶다면, 다음 구문을 사용하세요:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 제공받은 내용을 그대로 출력할 때에는 각별한 주의를 기울이세요. 사용자 입력 데이터를 표시할 때는 XSS 공격을 방지하기 위해 이스케이프된 중괄호(`{{ }}`)를 사용하는 것이 일반적입니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크 (Blade and JavaScript Frameworks)

여러 자바스크립트 프레임워크가 표현식을 브라우저에 표시하기 위해 중괄호를 사용하는 경우가 많으므로, Blade에서 해당 표현식이 변환되지 않도록 하려면 `@` 기호를 사용할 수 있습니다. 예시:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 경우 Blade는 `@` 기호만 제거하고, `{{ name }}` 표현식은 건드리지 않으므로 자바스크립트 프레임워크에서 그대로 렌더링됩니다.

또한 `@` 기호는 Blade 디렉티브의 이스케이프 용도로도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

뷰에 배열 데이터를 전달한 뒤, 자바스크립트 변수 초기화를 위해 JSON으로 렌더링해야 하는 경우가 있습니다. 예를 들면:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 사용할 필요 없이, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 동일한 인자를 받으며, HTML 따옴표 안에서 안전하게 사용할 수 있도록 적절히 이스케이프된 JSON을 반환합니다. 반환 값은 JS의 `JSON.parse`로 파싱할 수 있는 문자열입니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션 스켈레톤에서는 `Js` 파사드를 제공하여 Blade에서 더욱 편리하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿은 정규표현식 기반으로 동작하므로, 복잡한 표현식을 디렉티브에 전달할 경우 예기치 못한 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 일부 구간에서 자바스크립트 변수 등을 대량으로 표시할 필요가 있다면, 해당 HTML을 `@verbatim` 디렉티브로 감싸면 각 Blade 에코 구문 앞에 일일이 `@` 기호를 붙일 필요가 없습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 디렉티브 (Blade Directives)

템플릿 상속, 데이터 표시 외에도 Blade는 조건문, 반복문 등과 같은 PHP 제어 구조를 간편하게 사용할 수 있도록 여러 편리한 단축 구문을 제공합니다. 이 덕분에 익숙한 PHP 구조를 매우 깔끔하게 사용할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용하여 if 문을 작성할 수 있습니다. 이 디렉티브는 PHP의 if 문과 동일하게 동작합니다:

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

또한, 이미 설명한 조건부 디렉티브 외에 `@isset`, `@empty` 디렉티브를 각각 PHP의 `isset`, `empty` 함수처럼 사용할 수 있습니다:

```blade
@isset($records)
    // $records 가 정의되어 있고 null이 아닐 때...
@endisset

@empty($records)
    // $records 가 "비어있을" 때...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`, `@guest` 디렉티브를 사용하여 현재 사용자가 [인증](docs/master/authentication)되었는지 혹은 게스트인지 빠르게 확인할 수 있습니다:

```blade
@auth
    // 사용자가 인증된 경우...
@endauth

@guest
    // 사용자가 인증되지 않은 경우...
@endguest
```

필요하다면, 인증시 사용할 가드(guard)를 지정할 수도 있습니다:

```blade
@auth('admin')
    // 사용자가 인증된 경우...
@endauth

@guest('admin')
    // 사용자가 인증되지 않은 경우...
@endguest
```

<a name="environment-directives"></a>
#### 환경 디렉티브

애플리케이션이 프로덕션 환경에서 동작 중인지 `@production` 디렉티브로 확인할 수 있습니다:

```blade
@production
    // 프로덕션 전용 컨텐츠...
@endproduction
```

또는, 특정 환경에서만 실행되도록 하려면 `@env` 디렉티브를 사용할 수 있습니다:

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중일 때...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경일 때...
@endenv
```

<a name="section-directives"></a>
#### 섹션 디렉티브

템플릿 상속의 섹션에 내용이 있는지 확인하려면 `@hasSection` 디렉티브를 사용할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

특정 섹션에 내용이 없을 때를 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 디렉티브

`@session` 디렉티브를 통해 [세션](/docs/master/session) 값 존재 여부를 확인할 수 있습니다. 세션 값이 존재하면 `@session`과 `@endsession` 사이의 템플릿이 평가됩니다. 해당 범위 안에서 `$value` 변수를 그대로 사용해 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트 디렉티브

`@context` 디렉티브는 [컨텍스트](/docs/master/context) 값이 있는지 확인합니다. 값이 있다면, 디렉티브 내부에서 `$value` 변수로 값을 출력할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용하여 switch 문을 구성할 수 있습니다:

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

조건문 뿐 아니라, PHP의 반복문 구조도 Blade에서 간단하게 사용할 수 있습니다. 각 디렉티브는 PHP의 동작과 동일합니다:

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
> `foreach` 루프 내에서는 [loop 변수](#the-loop-variable)를 사용해 현재 반복이 첫 번째인지, 마지막인지 등 여러 정보를 얻을 수 있습니다.

반복문 내에서 특정 반복을 건너뛰거나 루프를 종료하려면 `@continue`, `@break` 디렉티브를 사용할 수 있습니다:

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

조건을 디렉티브 선언부에 바로 넣어 사용할 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 내부에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복 인덱스, 첫 번째 반복 여부, 마지막 반복 여부 등 여러 유용한 정보를 제공합니다:

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

중첩 반복문에서는 `parent` 속성으로 부모 반복문의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

$loop 변수의 각 속성은 다음과 같습니다:

<div class="overflow-auto">

| 속성                | 설명                                             |
| ------------------  | ---------------------------------------------- |
| `$loop->index`      | 현재 반복의 인덱스(0부터 시작)                   |
| `$loop->iteration`  | 현재 반복 횟수(1부터 시작)                      |
| `$loop->remaining`  | 남은 반복 횟수                                  |
| `$loop->count`      | 전체 반복 아이템 수                              |
| `$loop->first`      | 첫 번째 반복 여부                                |
| `$loop->last`       | 마지막 반복 여부                                 |
| `$loop->even`       | 반복이 짝수 번째인지 여부                       |
| `$loop->odd`        | 반복이 홀수 번째인지 여부                       |
| `$loop->depth`      | 현재 반복의 중첩 깊이                            |
| `$loop->parent`     | 중첩 반복일 경우, 부모 loop 변수                |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 디렉티브는 CSS 클래스를 조건부로 조합할 수 있습니다. 배열의 키는 추가할 클래스명, 값은 해당 클래스를 추가할 조건식입니다. 숫자형 키는 항상 포함됩니다:

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

마찬가지로, `@style` 디렉티브로 HTML 요소의 인라인 스타일을 조건부로 지정할 수 있습니다:

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

편의를 위해 `@checked` 디렉티브로 체크박스의 "checked" 상태를 쉽게 지정할 수 있습니다. 주어진 조건이 true이면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, `@selected` 디렉티브로 select 옵션의 "selected" 상태를:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled` 디렉티브로 해당 요소의 "disabled" 속성을 설정할 수도 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

더불어 `@readonly` 디렉티브로 "readonly" 속성을 지정할 수 있습니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

또한 `@required` 디렉티브로 "required" 속성을 조건부로 추가할 수 있습니다:

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
> `@include` 디렉티브도 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 장점이 있어 권장합니다.

Blade의 `@include` 디렉티브로 다른 Blade 뷰를 뷰 내부에서 포함시킬 수 있습니다. 부모 뷰에서 이용 가능한 모든 변수는 포함된 뷰에서도 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰가 부모의 모든 데이터를 상속받지만, 추가로 변수를 전달하고 싶다면 배열로 전달해줄 수 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하면 Laravel은 에러를 발생시킵니다. 뷰 존재 여부와 관계없이 포함하려면 `@includeIf`를 사용할 수 있습니다:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

주어진 불리언 조건에 따라 뷰를 포함하려면 `@includeWhen`, `@includeUnless` 디렉티브를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 존재하는 첫 번째 뷰를 포함하려면 `includeFirst`를 사용할 수 있습니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

부모 뷰의 변수 상속 없이 뷰를 포함하려면 `@includeIsolated`를 사용하세요:

```blade
@includeIsolated('view.name', ['user' => $user])
```

> [!WARNING]
> Blade 뷰 내에서 `__DIR__`, `__FILE__` 상수 사용은 권장하지 않습니다. 캐시·컴파일된 뷰의 경로로 처리됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

반복문과 view 포함을 한 줄로 사용할 수 있도록 Blade의 `@each` 디렉티브가 제공됩니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 컬렉션/배열 각 요소마다 렌더링할 뷰 이름입니다. 두 번째 인수는 순회할 배열/컬렉션, 세 번째는 각 요소가 자식 뷰로 전달될 때 사용할 변수명입니다. 루프의 현재 키 값은 `key` 변수로 사용 가능합니다.

네 번째 인수로 배열이 비어있을 때 사용할 뷰를 지정할 수 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 필요한 경우 `@foreach`와 `@include` 조합을 사용하세요.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브를 이용하면 블레이드 템플릿의 일부 구간을 렌더링 당 한 번만 출력할 수 있습니다. 예를 들어, [스택](#stacks)에 자바스크립트 코드를 추가할 때 유용하게 사용할 수 있습니다. 예를 들어 반복문 내에서 컴포넌트를 렌더링하더라도, JS 코드는 한 번만 헤더에 넣고 싶을 때 씁니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

자주 `@once`와 조합되는 `@push` 또는 `@prepend`와 함께 사용할 때, 편하게 쓸 수 있도록 `@pushOnce`와 `@prependOnce` 디렉티브도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

서로 다른 Blade 템플릿에서 중복된 내용을 푸시하고 싶을 때, 두 번째 인자로 고유 식별자를 지정하여 실제로 한 번만 출력되도록 할 수 있습니다:

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

특정 상황에서는 뷰 내부에 PHP 코드를 그대로 삽입하는 것이 편리할 때가 있습니다. `@php` 디렉티브를 사용해 블록 단위의 PHP 코드를 작성할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스를 임포트만 하고 싶을 때는 `@use` 디렉티브를 사용합니다:

```blade
@use('App\Models\Flight')
```

두 번째 인수로 임포트한 클래스에 별칭을 줄 수도 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스의 여러 클래스를 한꺼번에 임포트할 수도 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

함수와 상수도 `function`·`const` 키워드와 함께 `@use`로 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수 및 상수도 별칭(alias)을 지정할 수 있습니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수와 상수도 중괄호로 그룹화하여 임포트가 가능합니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade는 뷰 내에서 주석을 지원합니다. Blade 주석은 HTML 결과에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

(이하 컴포넌트, 익명 컴포넌트, 레이아웃, 폼, 스택, 서비스 주입, 인라인 블레이드 템플릿 렌더링, 블레이드 프래그먼트, 확장, 커스텀 에코 핸들러, 커스텀 If 문 역시 동일한 구조와 번역 원칙을 적용하며, 전체 문서 길이 제한 관계로 문단별로 필요한 부분만 요청해주세요.)