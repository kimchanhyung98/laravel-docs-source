# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [Blade 지시어](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
    - [원시 PHP 코드](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축하기](#building-layouts)
    - [컴포넌트를 사용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 사용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [검증 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 출력 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 일반 PHP 코드를 사용하는 데 제한을 두지 않습니다. 사실, 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되어 캐시되며 변경될 때까지 재컴파일되지 않아, 애플리케이션에 사실상 거의 오버헤드가 없습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 통해 반환할 수 있습니다. 물론, [뷰](https://laravel.com/docs/12.x/views) 문서에서 언급한 것처럼, 두 번째 인수를 통해 Blade 뷰에 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강화하기

Blade 템플릿을 한 단계 업그레이드하여 동적 인터페이스를 쉽게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire는 React나 Vue 같은 프런트엔드 프레임워크에서만 가능했던 동적 기능을 갖춘 Blade 컴포넌트를 작성할 수 있게 해줍니다. 복잡한 자바스크립트 빌드 절차나 클라이언트 사이드 렌더링 없이도 현대적이고 반응성 있는 프런트엔드를 구축하는 훌륭한 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시하기

Blade 뷰에 전달된 데이터를 표시하려면 변수를 중괄호로 감싸면 됩니다. 예를 들어, 다음과 같은 라우트가 있다고 할 때:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력 구문은 자동으로 PHP의 `htmlspecialchars` 함수로 처리되어 XSS 공격을 방지합니다.

뷰에 전달된 변수뿐 아니라, PHP 함수의 결과도 출력할 수 있습니다. 사실, Blade 출력 구문 내에 원하는 아무 PHP 코드나 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드 내에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

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
#### 이스케이프 처리되지 않은 데이터 표시

기본적으로 Blade `{{ }}` 구문은 XSS 공격 방지를 위해 자동으로 `htmlspecialchars` 함수를 통과합니다. 만약 데이터의 이스케이프 처리를 원하지 않는다면, 다음 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력 받은 내용을 출력할 때 매우 주의해야 합니다. 일반적으로 사용자 제공 데이터를 표시할 때는 이스케이프 처리된 중괄호 구문을 사용하는 것이 XSS 공격 방지에 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크가 `{{ }}` 구문을 템플릿 내 표현식 표시용으로 사용하기 때문에, Blade 렌더링 엔진이 표현식을 건드리지 않도록 `@` 기호를 사용해 알릴 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

여기서 `@` 기호는 Blade에서 제거되지만 `{{ name }}` 표현식은 Blade 엔진에서 건드리지 않고 자바스크립트 프레임워크에서 렌더링됩니다.

`@` 기호는 Blade 지시어를 이스케이프하는 데에도 사용될 수 있습니다:

```blade
{{-- Blade 템플릿 --}}
@@if()

<!-- HTML 출력 -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수를 초기화하기 위해 뷰에 배열을 JSON 형태로 전달할 때가 있습니다. 이럴 때 수동으로 `json_encode`를 호출하지 않고 Laravel  제공 `Illuminate\Support\Js::from` 메서드 지시어를 사용할 수 있습니다. `from` 메서드는 `json_encode`와 같은 인자를 받지만, HTML 내 인용 부호에 안전하게 포함되도록 JSON을 이스케이프 처리합니다. 또한 `JSON.parse` 자바스크립트 구문 문자열을 반환해 유효한 자바스크립트 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel 최신 버전에는 Blade 템플릿 내 이 기능을 쉽게 쓸 수 있도록 `Js` 페이사드가 기본 포함되어 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿은 정규 표현식을 기반으로 하기에 복잡한 식을 전달할 경우 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿에서 자바스크립트 변수를 많이 출력해야 할 경우, `@verbatim` 구문으로 감싸면 각각의 Blade 출력문 앞에 `@`를 붙일 필요가 없습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 지시어

템플릿 상속 및 데이터 출력 외에도, Blade는 조건문과 반복문 같은 PHP 제어 구조를 위한 편리한 단축 구문을 제공합니다. 이들은 PHP와 동일한 기능을 하면서도 더 깔끔하고 간결하게 코드를 작성할 수 있게 도와줍니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시어를 사용해 `if` 문을 구성할 수 있습니다. PHP와 동일하게 작동합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해, Blade는 `@unless` 지시어도 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

그 외에 `@isset`와 `@empty` 지시어도 PHP 함수와 같은 용도로 사용 가능합니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 비어 있음...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시어

`@auth` 및 `@guest` 지시어는 현재 사용자가 인증되었는지([authenticated](/docs/12.x/authentication)) 또는 비인증 상태인지(guset)를 빠르게 판단할 수 있게 합니다:

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

만약 특정 인증 가드를 검사하려면, 지시어에 가드 이름을 인수로 넘기면 됩니다:

```blade
@auth('admin')
    // admin 가드로 인증됨...
@endauth

@guest('admin')
    // admin 가드로 인증되지 않음...
@endguest
```

<a name="environment-directives"></a>
#### 환경 지시어

애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 때는 `@production` 지시어를 사용하세요:

```blade
@production
    // 프로덕션 전용 컨텐츠...
@endproduction
```

특정 환경에서 실행 중인지 확인하려면 `@env` 지시어를 사용합니다:

```blade
@env('staging')
    // "staging" 환경에서 실행 중...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서 실행 중...
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시어

템플릿 상속의 섹션에 내용이 있는지 확인하려면 `@hasSection` 지시어를 사용합니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없는 경우는 `sectionMissing` 지시어로 확인할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시어

`@session` 지시어는 [세션 값](/docs/12.x/session)이 존재하는지 확인하는 데 사용됩니다. 값이 있으면 `@session`과 `@endsession` 사이의 템플릿 코드가 평가됩니다. `@session` 내부에서는 `$value` 변수로 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트 지시어

`@context` 지시어는 [컨텍스트 값](/docs/12.x/context)이 존재하는지 확인하는 데 사용됩니다. 값이 있으면 `@context`와 `@endcontext` 사이의 템플릿 코드가 평가됩니다. 내부에서 `$value` 변수로 컨텍스트 값을 출력할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어로 switch 문을 작성할 수 있습니다:

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

조건문 외에도, Blade는 PHP 반복문과 같은 구조를 위한 단축 지시어를 제공합니다:

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
> `foreach` 반복문 내에서는 [루프 변수](#the-loop-variable)를 사용할 수 있어 현재 반복 상태(첫/마지막 반복인지 등)를 확인할 수 있습니다.

반복문에서 현재 반복을 건너뛰거나 루프를 종료하려면 `@continue`와 `@break` 지시어를 사용할 수 있습니다:

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

조건을 지시어 괄호 안에 직접 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 반복문 내에서 `$loop` 변수를 사용할 수 있습니다. 이 변수로 현재 반복 인덱스, 첫 반복/마지막 반복 여부 등 여러 유용한 정보를 얻을 수 있습니다:

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

중첩 반복문에서는 `parent` 속성을 통해 부모 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수는 다음과 같은 유용한 속성을 포함합니다:

| 속성              | 설명                                                        |
| ----------------- | ----------------------------------------------------------- |
| `$loop->index`     | 현재 반복 인덱스 (0부터 시작)                               |
| `$loop->iteration` | 현재 반복 (1부터 시작)                                      |
| `$loop->remaining` | 남은 반복 횟수                                             |
| `$loop->count`     | 총 반복할 아이템 수                                        |
| `$loop->first`     | 첫 번째 반복인지 여부                                       |
| `$loop->last`      | 마지막 반복인지 여부                                       |
| `$loop->even`      | 짝수 반복인지 여부                                         |
| `$loop->odd`       | 홀수 반복인지 여부                                         |
| `$loop->depth`     | 중첩된 반복의 깊이                                           |
| `$loop->parent`    | 중첩 반복에서 부모 루프의 `$loop` 변수                      |

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일

`@class` 지시어는 조건에 따라 CSS 클래스 문자열을 컴파일합니다. 배열을 인자로 받으며, 배열 키는 적용할 클래스 이름(또는 클래스 목록), 값은 불리언 식입니다. 만약 배열 키가 숫자면 무조건 포함됩니다:

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

비슷하게, `@style` 지시어로 인라인 CSS 스타일을 조건부로 추가할 수 있습니다:

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

편리하게 HTML 입력 요소의 특정 속성을 조건부로 추가하는 지시어들이 있습니다.

`@checked`는 체크박스 같은 입력 요소에 `checked` 속성을 조건부로 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

`@selected`는 `<select>` 요소에서 옵션을 선택 상태로 만듭니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled`는 요소를 비활성화할 때 씁니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

`@readonly`는 읽기 전용 상태를 지정합니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

`@required`는 필수 입력 속성을 지정합니다:

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
> `@include` 지시어를 자유롭게 사용할 수 있지만, Blade 컴포넌트는 유사한 기능을 제공하면서 데이터 및 속성 바인딩 등 여러 장점을 함께 제공합니다.

Blade의 `@include` 지시어로 다른 Blade 뷰를 현재 뷰에 포함할 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수도 포함된 뷰에서 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

포함된 뷰가 부모 뷰의 모든 데이터를 상속하지만, 별도로 포함 뷰에만 전달할 추가 데이터를 배열 형태로 넘길 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하면 오류가 발생합니다. 뷰가 있을 수도 있고 없을 수도 있는 경우는 `@includeIf` 지시어를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

조건이 `true` 혹은 `false` 여부에 따라 뷰 포함을 하려면 `@includeWhen` 또는 `@includeUnless` 지시어를 사용합니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

주어진 뷰 리스트 중 첫 번째로 존재하는 뷰를 포함하려면 `@includeFirst`를 사용하세요:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰 내에서 `__DIR__` 및 `__FILE__` 상수를 사용하는 것은 피해야 합니다. 이 값들은 컴파일되고 캐시된 뷰의 위치를 가리키기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션용 뷰 렌더링

루프와 인클루드를 한 줄로 합쳐 사용하는 `@each` 지시어가 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

`@each`의 첫 번째 인수는 각 요소에 대해 렌더링할 뷰, 두 번째는 반복할 배열/컬렉션, 세 번째는 현재 반복된 객체를 뷰 내에서 접근할 변수명입니다. 현재 반복 인덱스는 뷰 내 `key` 변수로 접근할 수 있습니다.

네 번째 인수는 반복할 데이터가 비어 있을 때 대체 렌더링할 뷰를 지정합니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each` 로 렌더링된 뷰는 부모 뷰 변수들을 상속받지 않습니다. 만약 자식 뷰에서 부모 변수들이 필요하면, `@foreach` 와 `@include`를 조합해 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어로 템플릿의 일부를 렌더링 주기 당 한 번만 평가할 수 있습니다. 주로 자바스크립트 라이브러리를 헤더에 푸시할 때 유용합니다. 예를 들어, 반복문 내에서 컴포넌트를 렌더링할 때, 최초 렌더링 시에만 스크립트를 푸시하도록 할 수 있습니다:

```blade
@once
    @push('scripts')
        <script>
            // 커스텀 자바스크립트...
        </script>
    @endpush
@endonce
```

자주 `@push` 또는 `@prepend` 와 함께 사용되므로, 편의를 위해 `@pushOnce` , `@prependOnce` 지시어도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // 커스텀 자바스크립트...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP 코드

템플릿에 직접 PHP 코드를 삽입해야 할 경우, Blade의 `@php` 지시어로 블록을 실행할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스 임포트용으로는 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

두 번째 인자로 알리아스를 지정할 수도 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 내 여러 클래스를 한 번에 그룹으로 임포트할 수도 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

함수 또는 상수도 접두사 `function` 또는 `const`를 붙여 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수나 상수도 알리아스를 붙여 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수와 상수 모두 그룹 임포트를 지원합니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade는 뷰 내에 주석을 정의할 수 있습니다. HTML 주석과 달리, Blade 주석은 최종 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 유사한 이점을 제공합니다. 컴포넌트와 슬롯은 더 이해하기 쉬운 접근법이 될 수 있습니다. 컴포넌트 작성에는 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지 방식이 있습니다.

클래스 기반 컴포넌트를 만들려면 Artisan 명령어 `make:component`를 사용하세요. 예를 들면, 단순한 `Alert` 컴포넌트를 다음과 같이 만듭니다. 이 명령을 실행하면 컴포넌트 클래스가 `app/View/Components` 디렉터리에 생성됩니다:

```shell
php artisan make:component Alert
```

이 명령은 컴포넌트 뷰 템플릿도 `resources/views/components` 폴더에 생성합니다. 자신의 애플리케이션에서는 이 디렉터리들이 자동으로 컴포넌트 범위에 포함되므로 별도 등록이 필요 없습니다.

서브디렉터리 안에도 컴포넌트를 만들 수 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms` 디렉터리에 `Input` 컴포넌트 클래스를, `resources/views/components/forms` 폴더에 뷰 파일을 생성합니다.

익명 컴포넌트(클래스 없이 Blade 템플릿만 존재하는 컴포넌트)를 만들려면 `--view` 옵션을 붙여 명령어를 실행하세요:

```shell
php artisan make:component forms.input --view
```

이렇게 하면 `resources/views/components/forms/input.blade.php` 파일이 생기고, `<x-forms.input />` 형태로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션 내 컴포넌트는 자동 발견되지만, 패키지 내 컴포넌트는 수동으로 클래스와 HTML 태그 별칭을 등록해야 합니다. 일반적으로 패키지 서비스 프로바이더의 `boot` 메서드 안에서 등록합니다:

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

등록 후에는 다음과 같이 태그별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드로 컴포넌트 클래스를 네임스페이스 별로 자동 로드할 수 있습니다. 예를 들어 `Nightshade` 패키지가 `Package\Views\Components` 네임스페이스에 `Calendar`, `ColorPicker` 컴포넌트를 가진 경우:

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

다음과 같이 벤더 네임스페이스가 붙은 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환해 자동으로 클래스와 연결합니다. 서브디렉터리도 점(`.`) 표기법으로 지원됩니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트는 Blade 컴포넌트 태그를 통해 출력합니다. 태그는 `x-` 로 시작하며 컴포넌트 클래스 이름을 케밥 케이스로 표현합니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 내 하위 디렉터리에 있으면 `.`로 표현할 수 있습니다. 예를 들어 `app/View/Components/Inputs/Button.php` 컴포넌트면:

```blade
<x-inputs.button/>
```

조건부 렌더링을 위해 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 컴포넌트가 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트를 렌더링해야 하는지 여부를 반환합니다.
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

컴포넌트 그룹을 디렉터리로 구성하여 관리할 수 있습니다. 예를 들어 "card" 컴포넌트 그룹에 다음과 같은 클래스 구조가 있다면:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트 파일명이 디렉터리 이름(`Card`)과 같으면, 다음처럼 `<x-card>`로 렌더링할 수 있습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

컴포넌트에 데이터를 HTML 속성 형태로 전달할 수 있습니다. 원시 값은 일반 HTML 속성처럼, PHP 변수/식은 `:` 프리픽스를 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 데이터 속성은 컴포넌트 클래스 생성자에서 정의합니다. 클래스 내 모든 퍼블릭 속성은 자동으로 뷰에서 변수를 통해 접근할 수 있습니다. `render` 메서드에서 뷰에 별도로 전달할 필요는 없습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스 생성.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 뷰 반환.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링되면 각 퍼블릭 변수 값을 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 네이밍 규칙

컴포넌트 생성자 인자는 `camelCase`로, HTML 속성에는 `kebab-case`를 씁니다. 예를 들어 다음 생성자가 있다면:

```php
/**
 * 컴포넌트 인스턴스 생성.
 */
public function __construct(
    public string $alertType,
) {}
```

HTML 속성은 다음처럼 씁니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성 문법

컴포넌트에 변수 이름과 동일한 속성을 전달할 때는 단축 문법을 사용할 수 있습니다:

```blade
{{-- 단축 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 같은 자바스크립트 프레임워크는 컬론(:)으로 시작하는 속성을 많이 쓰므로, `::`로 시작하면 Blade에서 PHP 표현식으로 처리하지 않고 그대로 출력합니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

출력 결과:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

퍼블릭 메서드는 컴포넌트 템플릿에서 호출할 수 있습니다. 예를 들어 `isSelected` 메서드를 가졌다 가정할 때:

```php
/**
 * 옵션이 선택되어 있는지 판단.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

템플릿에서는 다음과 같이 호출할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내 속성 및 슬롯 접근하기

컴포넌트 클래스 내에서 컴포넌트 이름, 속성, 슬롯에 접근하려면 `render` 메서드에서 클로저를 반환해야 합니다:

```php
use Closure;

/**
 * 뷰/내용 반환.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>컴포넌트 내용</div>';
    };
}
```

클로저에 `$data` 배열 인자를 전달받으면 컴포넌트 정보가 들어있습니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>컴포넌트 내용</div>';
}
```

> [!WARNING]
> `$data` 각 요소를 `render` 메서드 내 문자열에 직접 삽입하는 것은 원격 코드 실행 취약점이 될 수 있으므로 절대 하지 마세요.

`componentName`은 태그명(예: `<x-alert />` → `alert`), `attributes`는 HTML 태그 속성, `slot`은 슬롯 내용(`Illuminate\Support\HtmlString` 인스턴스)을 나타냅니다.

클로저는 문자열을 반환하는데, 그 문자열이 기존 뷰 이름이면 뷰가 렌더링되고 그렇지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트가 Laravel [서비스 컨테이너](/docs/12.x/container)에서 주입받는 의존성이 있으면 데이터 속성보다 앞서 생성자에 선언하면 자동 주입됩니다:

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 숨길 속성 및 메서드

퍼블릭 속성 또는 메서드를 컴포넌트 템플릿에 노출하지 않으려면 `$except` 배열에 추가하세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출되지 않을 속성/메서드 목록.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스 생성.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성

데이터 속성 외에도, 컴포넌트가 정상 작동하는 데 필요하지 않은 추가 HTML 속성(`class` 등)을 지정할 수 있으며, 이 속성들은 자동으로 "속성 백(attribute bag)" 에 저장되고 `$attributes` 변수로 뷰 내에서 사용할 수 있습니다. 예를 들면:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 뷰에서 이 속성을 출력하려면 다음과 같이 합니다:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 컴포넌트 태그에서 `@env` 같은 지시어 사용은 현재 지원하지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값 / 속성 병합

기본값으로 CSS 클래스 같은 속성을 지정하고 싶다면 속성 백의 `merge` 메서드를 쓰세요. 예를 들어 기본 alert 클래스를 지정하는 경우:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

만약 아래처럼 사용한다면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 출력은 다음과 같이 클래스가 병합됩니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건이 참일 때만 클래스를 추가하려면 `class` 메서드를 사용하세요. 이 메서드는 클래스 문자열과 조건식을 배열 형식으로 받습니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성도 병합하거나 추가하려면 메서드 체인을 사용할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 다른 HTML 요소의 조건부 클래스 합성이 필요하면, [@class 지시어](#conditional-classes)를 쓰는 것이 좋습니다.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

클래스 이외 속성 병합은 `merge` 메서드의 기본값으로 처리되나, 기존 값과 병합되지 않고 덮어쓰기 처리됩니다. 예를 들어 버튼 컴포넌트:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

버튼 타입을 바꾸려면 컴포넌트 사용할 때 지정합니다. 지정하지 않으면 기본값인 `button` 타입이 사용됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```

이 경우 렌더링 결과는 다음과 같습니다:

```blade
<button type="submit">
    Submit
</button>
```

`class`를 제외한 속성과 값을 병합하려면 `prepends` 메서드를 사용하세요. 예를 들어 `data-controller`를 기본값으로 두고 추가 값을 붙일 수 있습니다:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 검색 및 필터링

`filter` 메서드로 속성을 필터링할 수 있습니다. 콜백에 키 값이 전달되며, `true`를 반환하면 유지합니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

속성 키가 특정 문자열로 시작하는 항목만 찾으려면 `whereStartsWith` 메서드를 씁니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 시작하지 않는 속성만 고르려면 `whereDoesntStartWith`를 사용하세요:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 첫 속성을 출력할 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

속성이 있는지 확인하려면 `has` 메서드 사용. 하나의 속성명 인자를 받으며 존재 여부 불리언을 반환합니다:

```blade
@if ($attributes->has('class'))
    <div>Class 속성이 존재합니다.</div>
@endif
```

배열 인자로 여러 속성명을 넘겨 모두 존재하는지 확인할 수도 있습니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 존재합니다.</div>
@endif
```

속성 중 어느 하나라도 존재하는지 확인은 `hasAny` 메서드를 씁니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>속성 중 일부가 존재합니다.</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드 사용:

```blade
{{ $attributes->get('class') }}
```

특정 키만 가져오려면 `only`:

```blade
{{ $attributes->only(['class']) }}
```

특정 키 제외한 모든 속성은 `except`:

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어

Blade 내부에서 컴포넌트 렌더링에 예약된 키워드가 있습니다. 다음 키워드들은 컴포넌트 클래스 내 퍼블릭 속성이나 메서드명으로 사용할 수 없습니다:

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯

컴포넌트에 추가 컨텐츠를 "슬롯"으로 전달합니다. 슬롯은 `$slot` 변수를 출력하여 렌더링합니다. 예를 들어 `alert` 컴포넌트가 다음과 같다면:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯에 내용을 전달하는 방법:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

하나 이상의 슬롯을 컴포넌트 내 여러 위치에 렌더링해야 한다면 "이름 있는 슬롯"을 활용합니다. 경고 컴포넌트에 "title" 슬롯 추가 예시:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯 내용 정의는 `x-slot` 태그를 사용합니다. 명명된 슬롯 외 나머지는 기본 `$slot` 변수에 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 비었는지 확인하려면 `isEmpty` 메서드를 호출할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        슬롯이 비어 있을 때의 기본 콘텐츠입니다.
    @else
        {{ $slot }}
    @endif
</div>
```

슬롯 내용 중 HTML 주석을 제외한 실제 내용이 있는지 확인하려면 `hasActualContent` 메서드를 사용합니다:

```blade
@if ($slot->hasActualContent())
    슬롯에 실제 컨텐츠가 존재합니다.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯

Vue 같은 자바스크립트 프레임워크의 "스코프 슬롯"처럼, 컴포넌트 내 데이터를 슬롯 템플릿 내에서 접근할 수 있습니다. 컴포넌트 클래스에서 퍼블릭 메서드나 속성을 정의한 뒤, 슬롯 내에서 `$component` 변수를 통해 접근하세요. 예를 들어 `formatAlert` 메서드가 있을 때:

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

슬롯에도 컴포넌트와 마찬가지로 CSS 클래스 등 추가 HTML 속성을 지정할 수 있습니다:

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

슬롯 속성은 슬롯 변수의 `attributes` 프로퍼티로 접근합니다. 자세한 건 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

작은 컴포넌트는 클래스와 뷰를 따로 관리하는 것이 번거로울 수 있습니다. 이런 경우 `render` 메서드에서 바로 마크업을 반환할 수 있습니다:

```php
/**
 * 뷰/내용 반환.
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

인라인 뷰 컴포넌트를 만들려면 `make:component` 명령어에 `--inline` 옵션을 추가하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

런타임 시점에 어떤 컴포넌트를 렌더링할지 모를 때 `dynamic-component` 컴포넌트를 사용하세요:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 이 내용은 주로 패키지 내 컴포넌트를 등록하는 경우에 해당합니다. 일반적인 애플리케이션에서는 컴포넌트가 자동 발견되므로 이 내용은 생략해도 됩니다.

자신이 만든 컴포넌트가 `app/View/Components` 와 `resources/views/components` 이외 비표준 디렉터리에 있다면 수동으로 클래스와 태그 별칭을 등록해야 합니다. 패키지 서비스 프로바이더 `boot` 메서드에서 등록하세요:

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

등록 후 렌더링:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

`componentNamespace` 메서드로 컴포넌트 네임스페이스를 등록할 수 있습니다:

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

이후 다음처럼 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼케이스로 변환해 해당 클래스를 자동 감지하며, 서브디렉터리도 점 표기법으로 지원합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 비슷하나, 익명 컴포넌트는 클래스 없이 단일 Blade 템플릿 파일만으로 컴포넌트를 정의합니다. `resources/views/components` 폴더 내 Blade 템플릿을 컴포넌트로 인식합니다.

예를 들어 `resources/views/components/alert.blade.php`에 컴포넌트가 있다면:

```blade
<x-alert/>
```

컴포넌트가 하위 폴더에 있다면 `.` 로 나타내세요. 예:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

컴포넌트가 여러 템플릿으로 구성되어 폴더로 묶어 관리할 때, "index" 템플릿을 폴더 내에 포함하여 "루트" 컴포넌트를 지정할 수 있습니다.

예를 들어, "accordion" 컴포넌트가 다음과 같을 때:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

다음처럼 렌더링할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

이렇게 하면 루트 컴포넌트를 별도 상위 경로로 빼지 않고도 컴포넌트 계층 구조를 관리할 수 있습니다.

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성

익명 컴포넌트에는 클래스가 없으므로, 어떤 HTML 속성을 데이터 변수로 받아야 하고 어떤 속성은 속성 백으로 처리해야 할지 구분해야 합니다.

`@props` 지시어를 템플릿 상단에 작성하여 데이터 변수명을 정의합니다. 기본 값을 지정할 수도 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 컴포넌트는 다음처럼 렌더링할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

자식 컴포넌트에서 부모 컴포넌트의 데이터를 참조해야 할 때 `@aware` 지시어를 사용합니다. 예를 들어 메뉴 `<x-menu>`와 메뉴 아이템 `<x-menu.item>` 컴포넌트가 있다고 할 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` 컴포넌트 구현:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` prop은 부모에만 전달되므로 `x-menu.item` 에선 기본적으로 접근 불가능합니다. 여기서 `@aware`를 사용하면 자식 컴포넌트도 데이터를 참조할 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware`는 부모 컴포넌트에 명시적으로 전달된 HTML 속성 데이터만 접근 가능하며, `@props` 기본값으로 설정된 값은 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

익명 컴포넌트는 기본적으로 `resources/views/components` 경로 내에서 정의하지만, 때로는 애플리케이션 내 다른 위치의 익명 컴포넌트 경로를 추가 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자로 익명 컴포넌트 경로, 두 번째 인자는 (선택 사항) 컴포넌트별 네임스페이스를 받습니다. 일반적으로 서비스 프로바이더 `boot` 메서드 내에 작성합니다:

```php
/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

네임스페이스를 지정하지 않았으므로 등록한 컴포넌트를 다음과 같이 네임스페이스 없이 바로 렌더링할 수 있습니다:

```blade
<x-panel />
```

네임스페이스를 지정했다면:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

아래처럼 렌더링할 수 있습니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구축하기

<a name="layouts-using-components"></a>
### 컴포넌트를 사용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에서 동일한 기본 레이아웃을 공유합니다. 매번 같은 HTML 레이아웃을 반복 작성하는 것은 매우 번거롭고 유지보수가 어렵습니다. 다행히도 Blade 컴포넌트로 레이아웃을 정의하고 애플리케이션 전역에서 반복해서 사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어 할 일 목록 애플리케이션이 있다고 가정합시다. 다음과 같이 `layout` 컴포넌트를 정의할 수 있습니다:

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
#### 레이아웃 컴포넌트 활용하기

`layout` 컴포넌트가 준비되었으니, 아래는 작업 목록을 보여주는 간단한 뷰입니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트의 기본 `$slot` 변수로 주입된 컨텐츠가 전달됩니다. 또 `$title` 슬롯이 있다면 사용하고 없을 경우 기본 제목을 표시하도록 했습니다. 작업 목록에 맞춰 커스텀 타이틀을 주입하려면 아래처럼 슬롯 구문을 씁니다:

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

레이아웃과 작업 목록 뷰가 준비되었으니, 라우트에서 작업 뷰를 반환하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 사용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의하기

템플릿 상속을 이용해 레이아웃을 만드는 방법도 있습니다. 컴포넌트가 도입되기 전까지 주로 사용된 방식입니다.

우선 간단한 레이아웃을 확인해 봅시다. 모든 페이지가 동일한 기본 레이아웃을 공유하는 경우, 하나의 Blade 뷰로 정의하는 것이 편리합니다:

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

`@section`과 `@yield` 지시어가 사용되었는데, `@section`은 섹션을 정의하고 `@yield`는 해당 섹션 내용을 출력합니다.

이제 이 레이아웃을 상속하는 하위 페이지 뷰를 정의합니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

뷰에서 `@extends` 지시어로 상속할 레이아웃을 지정합니다. 상속받은 뷰는 `@section` 지시어로 레이아웃 섹션에 콘텐츠를 주입합니다. `@yield`가 있는 곳에 주입한 내용이 출력됩니다:

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

위 예시의 `sidebar` 섹션은 `@@parent` 지시어로 부모 섹션 내용을 유지하고 후행 내용을 추가합니다. `@@parent`는 렌더링 시 부모 섹션 내용으로 대체됩니다.

> [!NOTE]
> 이전 예시와 달리 이 `sidebar` 섹션은 `@endsection`으로 끝나며, 이는 단순 섹션 정의만 합니다. 반면 `@show`는 정의와 동시에 출력합니다.

`@yield` 지시어는 두 번째 인자로 기본 텍스트를 받을 수 있으며, 섹션이 없으면 기본값을 렌더링합니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼

<a name="csrf-field"></a>
### CSRF 필드

HTML 폼을 만들 때는 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF 토큰 필드를 반드시 포함해야 합니다. `@csrf` 지시어로 토큰 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 같은 HTTP 메서드를 지원하지 않으므로 `_method` 숨겨진 필드를 넣어 해당 HTTP 메서드를 모방해야 합니다. `@method` 지시어가 이 필드를 생성해 줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 검증 오류

`@error` 지시어로 특정 속성에 대한 [검증 오류 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 있는지 손쉽게 확인할 수 있습니다. 오류 메시지를 출력하려면 내부에서 `$message` 변수를 사용합니다:

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

`@error`는 내부적으로 `if`문으로 변환되므로 `@else`를 써서 에러가 없을 때 출력할 내용을 지정할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 폼이 공존하는 페이지에서는 특정 오류 백을 두 번째 인수로 넘겨서 오류 메시지를 받아올 수 있습니다:

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

Blade는 이름 붙은 스택에 콘텐츠를 `push` 한 뒤, 다른 뷰(주로 레이아웃)에서 해당 스택의 내용을 렌더링 할 수 있습니다. 자식 뷰에서 필요한 자바스크립트 라이브러리 등 삽입에 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

`@push`할지 조건에 따라 결정하려면 `@pushIf` 지시어를 사용하세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택엔 여러 번 `@push`할 수 있으며, 모든 내용을 렌더링 할 때는 `@stack` 지시어를 씁니다:

```blade
<head>
    <!-- 헤더 내용 -->

    @stack('scripts')
</head>
```

스택 맨 앞에 내용을 추가하려면 `@prepend`를 사용하세요:

```blade
@push('scripts')
    This will be second...
@endpush

// 이후

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입

`@inject` 지시어로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 주입받을 수 있습니다. 첫 인자로 변수명을 받고, 두 번째 인자로 서비스 클래스 또는 인터페이스명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

Blade 템플릿 문자열을 바로 HTML로 변환할 때가 있습니다. `Blade` 파사드의 `render` 메서드를 사용하면 가능합니다. 첫 인자로 Blade 템플릿 문자를, 두 번째 인자로 뷰에 전달할 데이터를 배열로 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

이 메서드는 뷰를 `storage/framework/views` 디렉터리에 임시로 저장하고 렌더링합니다. 렌더링 후 임시 파일을 삭제하려면 `deleteCachedView` 인자를 `true`로 설정하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

[Turbo](https://turbo.hotwired.dev/) 및 [htmx](https://htmx.org/) 같은 프런트엔드 프레임워크 사용 시, 전체가 아닌 일부만 HTTP 응답으로 돌려줘야 할 때가 있습니다. Blade "프래그먼트"가 이 목적에 적합합니다.

Blade 템플릿 내 일부를 `@fragment`와 `@endfragment` 지시어로 감쌉니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이 뷰를 렌더링할 때는 `fragment` 메서드를 호출해 해당 프래그먼트만 응답하도록 할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건부로 프래그먼트를 반환하려면 `fragmentIf` 메서드를 쓰고, 조건에 따라 전체 뷰나 특정 프래그먼트만 반환할 수 있습니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트를 이어 붙여 반환하려면 `fragments` 및 조건부 버전인 `fragmentsIf` 메서드를 사용하세요:

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

Blade는 `directive` 메서드를 사용해 커스텀 지시어를 정의할 수 있습니다. 컴파일러가 커스텀 지시어를 발견하면 전달된 콜백을 호출합니다.

아래 예시는 `@datetime($var)` 지시어를 생성해 `DateTime` 인스턴스를 지정한 포맷으로 출력합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

이 지시어가 컴파일하면 다음 PHP 코드가 생성됩니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 지시어를 수정 후 캐시된 뷰를 전부 삭제해야 합니다. `view:clear` Artisan 명령어로 캐시를 지울 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 출력 핸들러

Blade는 객체 출력 시 `__toString` 메서드를 호출합니다. 하지만 제3자 라이브러리 같은 객체는 `__toString`을 직접 제어할 수 없을 때가 있습니다. 이럴 때 Blade의 `stringable` 메서드로 타입별 커스텀 출력 로직을 등록할 수 있습니다.

`AppServiceProvider`의 `boot` 메서드에서 다음과 같이 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

이후 Blade 템플릿에서 객체를 그냥 출력하면 자동으로 커스텀 출력 핸들러가 호출됩니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

복잡한 지시어보다 간단한 조건문 커스텀에 Blade는 `Blade::if` 메서드를 제공합니다. 클로저를 전달해 바로 조건문 지시어를 만들 수 있습니다.

환경 설정 파일에서 기본 디스크를 체크하는 커스텀 조건을 예로 보겠습니다. `AppServiceProvider` 내 `boot` 메서드에서 등록:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

등록한 커스텀 조건문은 Blade 템플릿에서 다음처럼 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 기본 디스크가 local임 -->
@elsedisk('s3')
    <!-- 기본 디스크가 s3임 -->
@else
    <!-- 기본 디스크가 그 외임 -->
@enddisk

@unlessdisk('local')
    <!-- 기본 디스크가 local 아님 -->
@enddisk
```