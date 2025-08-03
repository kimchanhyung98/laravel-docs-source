# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강화하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 지시어](#blade-directives)
    - [if문](#if-statements)
    - [switch문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
    - [원시 PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록하기](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [검증 오류 표시](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장](#extending-blade)
    - [커스텀 출력 핸들러](#custom-echo-handlers)
    - [커스텀 if문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 다른 PHP 템플릿 엔진과 다르게, Blade는 템플릿 내에서 순수 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되어 캐싱되며, 변경될 때까지 다시 컴파일되지 않으므로 Blade가 애플리케이션에 추가적인 부하를 거의 발생시키지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 전역 `view` 헬퍼 함수를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰 문서](/docs/10.x/views)에서 설명된 대로 `view` 헬퍼의 두 번째 인수로 데이터를 전달할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강화하기

Blade 템플릿을 한층 더 강화하여 동적인 인터페이스를 쉽게 구축하고 싶나요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면 React나 Vue 같은 프론트엔드 프레임워크에서만 가능하던 동적 기능을 가진 Blade 컴포넌트를 작성할 수 있습니다. 이를 통해 복잡한 클라이언트 사이드 렌더링이나 빌드 과정 없이 최신의 반응형 프론트엔드를 쉽게 빌드할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 출력

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있을 때:

```
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]  
> Blade의 `{{ }}` 출력 구문은 자동으로 PHP의 `htmlspecialchars` 함수로 처리되어 XSS 공격을 방지합니다.

뷰에 전달된 변수 내용을 출력하는 데 제한되지 않고, 어떠한 PHP 함수의 결과도 출력할 수 있습니다. 실제로 Blade 출력 구문 안에 원하는 PHP 코드를 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 두 번 인코딩합니다. 이중 인코딩을 비활성화하려면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```
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
#### 이스케이프 처리하지 않은 데이터 출력

기본적으로 Blade `{{ }}` 구문은 PHP의 `htmlspecialchars`를 거쳐 XSS 공격을 막습니다. 만약 데이터 이스케이프를 원하지 않는다면, 다음 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]  
> 사용자로부터 입력받은 내용을 출력할 때는 매우 주의해야 합니다. 일반적으로 사용자 입력 데이터를 출력할 때는 XSS 공격을 방지하기 위해 반드시 이스케이프된 중괄호 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크

많은 JavaScript 프레임워크가 중괄호(`{{ }}`)를 사용해 표현식을 표시하기 때문에, Blade 렌더링 엔진이 표현식을 처리하지 않고 그대로 두도록 하려면 `@` 기호를 사용하세요. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade가 제거하지만, `{{ name }}` 표현식은 Blade가 건드리지 않고 JavaScript 프레임워크가 렌더링하게 됩니다.

`@` 기호는 Blade 지시어를 이스케이프할 때도 사용됩니다:

```blade
{{-- Blade 템플릿 --}}
@@if()

<!-- 이때 출력되는 HTML -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수를 초기화하기 위해 배열을 JSON 형태로 뷰에 전달하고자 할 때가 있습니다. 예를 들어:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

수동으로 `json_encode` 함수를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. `from` 메서드는 `json_encode`와 같은 인수를 받지만, HTML 내에서 안전하게 인용될 수 있도록 올바르게 이스케이프된 JSON을 반환합니다. 또한 `from` 메서드는 JSON 문자열을 자바스크립트의 `JSON.parse` 구문으로 감싸 유효한 자바스크립트 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션 스켈레톤에는 `Js` 파사드가 포함되어 있어 Blade 템플릿에서 편리하게 쓸 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]  
> JSON 렌더링 용도로만 `Js::from` 메서드를 사용하세요. Blade 템플릿은 정규 표현식 기반이어서 복잡한 표현식을 전달하면 의도하지 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿 내에서 JavaScript 변수를 많이 출력해야 할 경우, 각 구문 앞에 `@`를 붙이지 않고 `@verbatim`과 `@endverbatim`으로 감싸면 Blade가 내부 내용을 처리하지 않고 그대로 출력합니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 지시어

Blade는 템플릿 상속과 데이터 출력 외에도 조건문, 반복문과 같은 PHP 제어 구조를 편리하게 표현하는 지시어를 제공합니다. 이러한 지시어들은 간결하고 깔끔하며 PHP 문법과 매우 유사합니다.

<a name="if-statements"></a>
### if문

`@if`, `@elseif`, `@else`, `@endif` 지시어로 `if`문을 작성할 수 있습니다. 이는 PHP의 대응 구문과 동일한 기능을 합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 `@unless` 지시어도 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

기존 조건 지시어에 더해, `@isset`와 `@empty` 지시어는 각각 PHP 함수의 간편한 축약형입니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시어

`@auth`와 `@guest` 지시어로 현재 사용자가 [인증](/docs/10.x/authentication)되었는지 또는 게스트인지 쉽게 확인할 수 있습니다:

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면 `@auth`와 `@guest`에 인증 가드를 명시할 수 있습니다:

```blade
@auth('admin')
    // 'admin' 가드로 인증된 사용자...
@endauth

@guest('admin')
    // 'admin' 가드로 인증되지 않은 사용자...
@endguest
```

<a name="environment-directives"></a>
#### 환경 지시어

앱이 프로덕션 환경에서 동작하는지 검사할 때 `@production` 지시어를 사용할 수 있습니다:

```blade
@production
    // 프로덕션 환경일 때만 보여줄 콘텐츠...
@endproduction
```

특정 환경인지 확인할 땐 `@env` 지시어를 사용합니다:

```blade
@env('staging')
    // 앱이 'staging' 환경으로 실행중...
@endenv

@env(['staging', 'production'])
    // 'staging' 또는 'production' 환경...
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시어

템플릿 상속 시 특정 섹션에 콘텐츠가 존재하는지 `@hasSection`으로 알 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션이 비어있는지 확인하려면 `sectionMissing` 지시어를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시어

세션 값이 존재하는지 검사하려면 `@session` 지시어를 쓸 수 있습니다. 지정한 세션 값이 존재하면 `@session`과 `@endsession` 사이 콘텐츠가 렌더링됩니다. 이때 `$value` 변수로 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### switch문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어로 switch문을 표현할 수 있습니다:

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

Blade는 조건문 뿐 아니라 PHP의 반복문에도 대응하는 간단한 지시어를 제공합니다. 이 지시어도 PHP 문법과 동일하게 동작합니다:

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
> `foreach` 구문 안에서는 [루프 변수](#the-loop-variable)를 사용해 현재 반복이 첫 번째인지 마지막인지 등의 유용한 정보를 얻을 수 있습니다.

반복문 내에서 현재 반복을 건너뛰거나 종료할 때 `@continue`와 `@break` 지시어를 쓸 수 있습니다:

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

조건을 지시어에 직접 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 문 안에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복의 인덱스, 첫 번째/마지막 반복 여부 등 다양한 정보를 제공합니다:

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

중첩된 반복문에서는 부모 루프의 `$loop` 변수에 `parent`를 통해 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수가 가진 주요 속성은 다음과 같습니다:

| 속성                  | 설명                                              |
|-----------------------|----------------------------------------------------|
| `$loop->index`         | 0부터 시작하는 현재 반복 인덱스                     |
| `$loop->iteration`     | 1부터 시작하는 현재 반복 번호                       |
| `$loop->remaining`     | 남은 반복 횟수                                     |
| `$loop->count`         | 전체 반복 횟수                                     |
| `$loop->first`         | 첫 번째 반복 여부                                   |
| `$loop->last`          | 마지막 반복 여부                                   |
| `$loop->even`          | 짝수 반복 여부                                     |
| `$loop->odd`           | 홀수 반복 여부                                     |
| `$loop->depth`         | 현재 중첩된 반복 깊이                               |
| `$loop->parent`        | 상위 반복문의 `$loop` 변수                          |

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 지시어를 사용하면 CSS 클래스 문자열을 조건부로 컴파일할 수 있습니다. 배열에서 키는 추가할 클래스, 값은 불리언 조건입니다. 숫자 키는 항상 포함됩니다:

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

마찬가지로 `@style` 지시어는 조건부로 인라인 CSS 스타일을 추가할 때 사용합니다:

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

`@checked` 지시어로 체크박스가 체크된 상태인지 손쉽게 표시할 수 있습니다. 조건이 참이면 `checked`가 출력됩니다:

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

`@selected` 지시어는 `<select>` 옵션에 선택 상태를 적용할 때 쓸 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한 `@disabled` 지시어로 특정 요소를 비활성화, `@readonly` 지시어로 읽기 전용, `@required` 지시어로 필수 속성을 적용할 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>

<input type="email"
        name="email"
        value="email@laravel.com"
        @readonly($user->isNotAdmin()) />

<input type="text"
        name="title"
        value="title"
        @required($user->isAdmin()) />
```

<a name="including-subviews"></a>
### 서브뷰 포함하기

> [!NOTE]  
> `@include` 지시어를 자유롭게 사용할 수 있지만, Blade [컴포넌트](#components)를 사용하면 데이터 및 속성 바인딩과 같은 여러 이점을 제공합니다.

`@include` 지시어는 부모 뷰 내에서 다른 Blade 뷰를 포함할 수 있으므로, 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

뷰가 존재하지 않을 수도 있는 경우 오류가 발생하므로 `@includeIf`를 사용해 조건부 포함이 가능합니다:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

또한 주어진 불리언 값에 따라 포함 여부를 결정하는 `@includeWhen`, `@includeUnless` 지시어도 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 존재하는 첫 번째 뷰를 포함하려면 `@includeFirst`를 사용합니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]  
> Blade 뷰 내에서 `__DIR__` 또는 `__FILE__` 상수 사용은 피해야 합니다. 왜냐하면 캐시된 컴파일 뷰 위치를 가리키기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

`@each` 지시어를 사용하면 루프와 포함을 한 줄로 합칠 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 각 배열 혹은 컬렉션 항목에 대해 렌더링할 뷰, 두 번째는 배열 또는 컬렉션, 세 번째는 현재 항목 변수명입니다. 각 항목의 키는 `key` 변수로 뷰에서 접근 가능합니다.

네 번째 인수를 지정하면 배열이 비었을 때 렌더링할 뷰를 정의할 수 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]  
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 필요한 경우 `@foreach`와 `@include`를 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어를 사용하면 해당 템플릿 영역을 렌더링 주기 당 한 번만 평가하도록 할 수 있습니다. 예를 들어, 루프 내에서 컴포넌트를 렌더링할 때 자바스크립트 코드는 처음 한 번만 푸시하고 싶을 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 종종 `@push` 또는 `@prepend`와 함께 쓰이므로 편의를 위해 `@pushOnce` 및 `@prependOnce` 지시어도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP

어떤 상황에서는 템플릿 내에 PHP 코드를 직접 포함하는 것이 유용할 수 있습니다. Blade `@php` 지시어를 사용하여 순수 PHP 코드를 실행할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스를 단순히 임포트할 경우 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

두 번째 인수로 별칭도 지정할 수 있습니다:

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
### 주석

Blade에서도 주석을 만들 수 있습니다. HTML 주석과 달리 Blade 주석은 렌더링된 HTML에 포함되지 않습니다:

```blade
{{-- 렌더링된 HTML에 포함되지 않는 주석 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 비슷한 이점을 제공하지만, 컴포넌트와 슬롯의 개념이 더 이해하기 쉽다고 느끼는 사람이 많습니다. 컴포넌트 작성은 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지 방식이 있습니다.

클래스 기반 컴포넌트를 만들기 위해 `make:component` Artisan 명령어를 사용할 수 있습니다. 간단한 `Alert` 컴포넌트를 만들려면 다음처럼 실행합니다. 컴포넌트 클래스는 `app/View/Components` 디렉터리에 생성됩니다:

```shell
php artisan make:component Alert
```

`make:component` 명령은 컴포넌트 뷰 템플릿도 함께 만들어 줍니다. 컴포넌트 뷰는 `resources/views/components` 디렉터리에 배치됩니다. 애플리케이션용 컴포넌트는 `app/View/Components`와 `resources/views/components`에서 자동으로 검색되어 별도 등록이 필요 없습니다.

하위 디렉터리에 컴포넌트를 생성할 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

이 명령은 `app/View/Components/Forms`에 `Input` 컴포넌트를, `resources/views/components/forms`에 뷰를 생성합니다.

클래스 없이 Blade 템플릿만 사용하는 익명 컴포넌트를 생성하려면 `--view` 옵션을 사용하세요:

```shell
php artisan make:component forms.input --view
```

위 명령은 `resources/views/components/forms/input.blade.php`를 생성하며 `<x-forms.input />`으로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

일반 애플리케이션 컴포넌트는 자동으로 검색되지만, 패키지용 컴포넌트는 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후 컴포넌트는 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 사용해 컨벤션에 따라 자동 로딩할 수도 있습니다. 예를 들어 `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 있다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이후 다음과 같이 벤더 네임스페이스 방식으로 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

컴포넌트 이름에 따라 Blade가 pascal-case 클래스를 찾아 자동으로 연결합니다. 하위 디렉터리는 점(`.`) 표기도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 출력하려면 Blade 템플릿 내에서 `x-` 접두사가 붙은 태그를 사용하세요. 접두사 뒤에는 컴포넌트 클래스 이름을 케밥케이스로 표기합니다:

```blade
<x-alert/>

<x-user-profile/>
```

클래스가 `app/View/Components` 하위 폴더에 있을 경우 점(`.`) 표기로 경로를 나타낼 수 있습니다. 예를 들어 `app/View/Components/Inputs/Button.php` 컴포넌트는 다음과 같이 렌더링합니다:

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶으면 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다:

```
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더링 여부 반환
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

HTML 속성을 통해 컴포넌트에 데이터를 전달할 수 있습니다. 원시값은 문자열로, PHP 표현식이나 변수는 `:` 접두사를 붙인 속성으로 전달하세요:

```blade
<x-alert type="error" :message="$message"/>
```

모든 컴포넌트의 데이터 속성은 생성자에서 정의합니다. 컴포넌트 클래스의 모든 public 프로퍼티는 자동으로 뷰에 전달되며, `render` 메서드에서 따로 전달할 필요가 없습니다:

```
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
     * 컴포넌트 뷰 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

렌더링 시 public 변수는 이름으로 출력 가능합니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 네이밍 스타일

컴포넌트 생성자 인수는 `camelCase`(낙타 표기법)로 작성하고, HTML 속성명은 `kebab-case`(케밥 표기법)를 사용해야 합니다. 예를 들어:

```
/**
 * 컴포넌트 인스턴스 생성
 */
public function __construct(
    public string $alertType,
) {}
```

컴포넌트를 다음과 같이 호출합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 축약 속성 문법

컴포넌트 속성 전달 시 이름과 변수명이 같다면 다음과 같이 축약형을 사용할 수 있습니다:

```blade
{{-- 축약 속성 --}}
<x-profile :$userId :$name />

{{-- 위와 동등 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 출력 이스케이프

Alpine.js 같은 JavaScript 프레임워크도 `:` 접두 속성을 사용하므로, Blade가 PHP 표현식으로 인식하지 않게 하려면 `::`(이중 콜론) 접두를 사용하세요:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

이렇게 하면 Blade가 다음 HTML로 렌더링합니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드 호출

컴포넌트 템플릿에서 public 메서드를 호출할 수 있습니다. 예를 들어 `isSelected`라는 메서드가 있다면:

```
/**
 * 선택된 옵션인지 판단
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

템플릿에서 다음과 같이 호출할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성 및 슬롯 접근

컴포넌트 클래스 내 `render` 메서드에서 컴포넌트 이름, 속성, 슬롯을 접근하려면 클로저를 반환해야 합니다. 클로저는 `$data` 배열을 매개변수로 받아 다음 값을 포함합니다:

```
use Closure;

/**
 * 컴포넌트 뷰 또는 내용 반환
 */
public function render(): Closure
{
    return function (array $data) {
        // $data['componentName']; // 컴포넌트 이름 (태그의 x- 이후)
        // $data['attributes'];    // 속성 모음
        // $data['slot'];          // 슬롯 내용(HTMLString 인스턴스)

        return '<div>컴포넌트 내용</div>';
    };
}
```

반환하는 문자열이 존재하는 뷰명이면 해당 뷰가 렌더링되고, 그렇지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트가 Laravel [서비스 컨테이너](/docs/10.x/container)의 의존성을 요구할 경우, 데이터 속성 앞에 작성하면 자동으로 주입됩니다:

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
#### 속성 / 메서드 숨기기

컴포넌트 템플릿에 노출시키지 않을 메서드나 프로퍼티를 `$except` 배열에 명시할 수 있습니다:

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출시키지 않을 프로퍼티/메서드
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
### 컴포넌트 속성

데이터 속성 외에도 `class` 같은 HTML 추가 속성을 지정해야 할 경우가 있습니다. 이러한 추가 속성은 컴포넌트 템플릿의 루트 엘리먼트에 전달하는 경우가 많습니다. 예를 들어:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 없는 모든 속성은 자동으로 `$attributes` 변수에 할당됩니다. 이를 출력하면 모든 추가 속성을 포함할 수 있습니다:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]  
> 컴포넌트 태그에 `@env` 같은 지시어를 직접 사용하는 것은 아직 지원되지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값 / 속성 병합

기본값을 지정하거나 컴포넌트에 CSS 클래스를 병합하려면 `$attributes->merge` 메서드를 사용하세요. 주로 기본 CSS 클래스를 지정할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 컴포넌트를 다음과 같이 호출하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

렌더링된 HTML은 다음과 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- 메시지 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 클래스 병합이 필요하면 `class` 메서드를 사용하세요. 배열의 키는 클래스, 값은 불리언입니다. 숫자 키 클래스는 항상 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성과 함께 병합할 때는 `class` 메서드 체인 뒤에 `merge`를 붙이면 됩니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]  
> 병합할 필요 없는 다른 HTML 요소에 조건부 클래스를 적용할 땐 [`@class` 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

`class` 속성이 아닌 경우, `merge` 메서드에 전달한 값은 기본값으로 간주되며, 주입된 속성이 있으면 덮어씁니다. 예를 들어 버튼 컴포넌트는 다음과 같습니다:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시 `type`을 지정하지 않으면 기본 `button`이 적용되고, 지정하면 우선합니다:

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

만약 기본값 뒤에 주입된 값을 이어 붙이고 싶다면 `prepends` 메서드를 사용할 수 있습니다. 예를 들어 `data-controller` 속성 기본값 앞에 `profile-controller`를 붙이고 뒤에 추가된 값을 이어 붙이는 경우:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 검색 및 필터링

`filter` 메서드는 조건에 맞는 속성만 남겨줍니다. 클로저는 속성값, 키를 받아 관련 속성만 남깁니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith`는 키가 특정 문자열로 시작하는 모든 속성을 찾습니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 `whereDoesntStartWith`는 해당 문자열로 시작하지 않는 속성을 반환합니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first`는 속성 모음 중 첫 번째 속성을 제공합니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성이 있는지 여부는 `has` 메서드로 확인합니다:

```blade
@if ($attributes->has('class'))
    <div>Class 속성이 있음</div>
@endif
```

여러 속성을 한 번에 확인하려면 배열을 넘기면 됩니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 있음</div>
@endif
```

한 가지라도 존재하는지 확인하려면 `hasAny`를 사용하세요:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>속성 중 하나 이상이 존재</div>
@endif
```

속성값을 가져오려면 `get` 메서드를 사용합니다:

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 예약어

Blade 컴포넌트의 내부 처리 용도로 기본 예약어들이 존재하므로, 컴포넌트 클래스에서 public 프로퍼티나 메서드명을 다음 단어로 지정해서는 안 됩니다:

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
### 슬롯

컴포넌트에 추가 콘텐츠를 전달할 때 "슬롯"을 사용합니다. 기본 슬롯은 `$slot` 변수로 출력합니다. 예를 들어 `alert` 컴포넌트가 다음과 같을 때:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

다음과 같이 슬롯에 콘텐츠를 넣을 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 슬롯이 필요할 경우, "title" 슬롯을 추가한 예제는 다음과 같습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

`x-slot` 태그로 이름 있는 슬롯을 지정합니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 비었는지 확인할 때 `isEmpty` 메서드를 사용할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        슬롯이 비어 있을 때의 기본 콘텐츠
    @else
        {{ $slot }}
    @endif
</div>
```

또는 `hasActualContent` 메서드로 실제 내용(HTML 주석 아닌)이 있는지도 검증 가능합니다:

```blade
@if ($slot->hasActualContent())
    실제 콘텐츠가 있는 슬롯입니다.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯

Vue 같은 프레임워크에서 사용하던 스코프드 슬롯과 유사하게, 컴포넌트 클래서의 public 메서드나 프로퍼티를 슬롯 내에서 `$component` 변수를 통해 호출할 수 있습니다. 예를 들어 `x-alert` 컴포넌트 클래스에 다음 메서드가 있다면:

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

컴포넌트와 마찬가지로 슬롯에도 CSS 클래스와 같은 추가 속성을 지정할 수 있습니다:

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

슬롯 속성은 슬롯 변수의 `attributes` 프로퍼티로 접근합니다. 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

매우 작은 컴포넌트는 클래스와 별도의 뷰 템플릿 분리가 번거로울 수 있습니다. 이때는 `render` 메서드에서 바로 마크업을 반환할 수 있습니다:

```
/**
 * 컴포넌트 뷰 또는 내용 반환
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

인라인 뷰 컴포넌트를 만들 때는 `make:component` 명령 시 `--inline` 옵션을 추가합니다:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

어떤 컴포넌트를 렌더링할지 런타임에 정해야 할 때는 Laravel 내장 `dynamic-component` 컴포넌트를 사용할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]  
> 이 수동 등록 방법은 주로 뷰 컴포넌트를 포함하는 Laravel 패키지를 작성하는 경우에 해당합니다. 일반 애플리케이션에서는 자동 검색되므로 보통 필요 없습니다.

애플리케이션 내 컴포넌트는 자동으로 검색되지만, 비표준 폴더에 컴포넌트를 두거나 패키지용 컴포넌트를 작성하는 경우 수동 등록이 필요합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```
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

등록 후 다음과 같이 태그로 사용할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

또는 `componentNamespace` 메서드로 컨벤션 기반 자동 로딩도 가능합니다. 예를 들어 `Nightshade` 패키지에서 `Package\Views\Components` 네임스페이스를 가진 컴포넌트 그룹이 있다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

벤더 네임스페이스 방식으로 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade가 컴포넌트 이름을 pascal-case 클래스로 자동 판단하며, 하위 폴더는 점(`.`) 표기법을 지원합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트처럼 익명 컴포넌트는 클래스 없이 하나의 뷰 파일로만 컴포넌트를 정의합니다. 보통 `resources/views/components` 디렉터리에 Blade 템플릿을 두면 익명 컴포넌트가 됩니다. 예를 들어 `resources/views/components/alert.blade.php`가 있으면 다음처럼 쓸 수 있습니다:

```blade
<x-alert/>
```

컴포넌트가 더 하위 폴더에 있을 경우 `.` 표기를 사용합니다. 예를 들어 `resources/views/components/inputs/button.blade.php`라면:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

컴포넌트가 여러 뷰 파일로 이루어졌을 때 특정 컴포넌트 템플릿 파일들을 폴더로 묶을 수 있습니다. 예시로 'accordion' 컴포넌트:

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

다음과 같이 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 위는 인덱스 뷰가 `resources/views/components` 폴더에 있어야 했습니다. Blade는 `index.blade.php` 파일을 하위 폴더 내에 넣으면 이 파일을 루트 컴포넌트로 렌더링합니다:

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 하면 기존처럼 다음과 같이 컴포넌트를 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성

익명 컴포넌트는 클래스가 없으므로 어떤 속성을 데이터 변수로, 어떤 속성을 속성 모음(어트리뷰트 백)에 넣을지 구분해야 합니다. 이를 위해 템플릿 상단에 `@props` 지시어를 사용해 데이터 변수 목록과 기본값을 지정할 수 있습니다. 나머지 속성은 속성 모음에 들어갑니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 컴포넌트는 이렇게 호출할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

부모 컴포넌트의 데이터를 자식 컴포넌트에서 사용하고 싶다면 `@aware` 지시어를 씁니다. 예를 들어 복합 메뉴 컴포넌트가 있다고 할 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 `x-menu` 컴포넌트는 다음과 같습니다:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

부모에만 전달된 `color`는 자식 `x-menu.item`에서 기본적으로 접근 불가하지만, `@aware` 지시어를 쓰면 됩니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]  
> `@aware`는 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터만 접근할 수 있습니다. 부모의 기본값으로 설정된 `@props` 값은 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

익명 컴포넌트 경로는 기본적으로 `resources/views/components`이고, 추가 경로를 등록해 여러 경로를 둘 수도 있습니다. `anonymousComponentPath` 메서드를 호출하면 됩니다. 보통 서비스 프로바이더에서 호출합니다:

```
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

경로 등록 시 별도 네임스페이스를 지정하지 않으면 컴포넌트 호출 시에도 접두어 없이 사용합니다. 예컨대 위 경로에 `panel.blade.php`가 있다면:

```blade
<x-panel />
```

네임스페이스를 지정 시:

```
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

다음과 같이 접두어가 필요합니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분 웹앱은 여러 페이지에서 공통 레이아웃을 가집니다. 모든 뷰마다 레이아웃 HTML을 반복하는 것은 비효율적이므로, 하나의 [Blade 컴포넌트](#components)로 레이아웃을 정의한 후 재사용하는 것이 편리합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "todo" 앱 레이아웃 컴포넌트는 다음과 같을 수 있습니다:

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

작성한 컴포넌트를 적용한 아래와 같은 뷰를 만듭니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

컴포넌트에 전달된 콘텐츠는 기본 슬롯 `$slot` 변수로 넘어갑니다. 위 레이아웃은 `$title` 슬롯도 지원하므로 이를 지정하려면 다음과 같이 작성합니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

레이아웃과 태스크 뷰를 만든 후 라우트에서 해당 뷰를 반환합니다:

```
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의

레이아웃은 "템플릿 상속" 기능으로도 만들 수 있으며, 컴포넌트 도입 전 주요 방식이었습니다.

예제로 간단한 레이아웃을 살펴봅니다. 대부분 웹앱은 여러 페이지에서 공통 레이아웃을 유지하므로, 다음과 같은 Blade 뷰 하나에 레이아웃을 정의할 수 있습니다:

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

HTML 마크업 내 `@section`과 `@yield`에 주목하세요. `@section`은 내용 블록을 정의하고, `@yield`는 해당 섹션의 내용을 출력합니다.

이제 이 레이아웃을 상속하는 자식 페이지를 만들어봅니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

자식 뷰에서는 `@extends` 지시어로 상속할 레이아웃을 명시합니다. 그리고 `@section` 지시어로 레이아웃 섹션에 콘텐츠를 주입합니다. 위 레이아웃에서 `@yield`가 해당 섹션을 출력합니다:

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

`sidebar` 섹션에서 `@@parent`는 레이아웃의 기존 사이드바 내용을 덧붙이는 역할을 합니다. `@@parent`는 출력 시 레이아웃의 사이드바 내용으로 대체됩니다.

> [!NOTE]  
> 이전과 달리 이 `sidebar` 섹션은 `@endsection`으로 끝납니다. `@endsection`은 섹션을 정의만 하고 렌더링하지 않고, `@show`는 정의와 즉시 출력까지 합니다.

`@yield` 지시어는 두 번째 파라미터로 기본값도 받을 수 있습니다. 해당 섹션이 없으면 기본값을 렌더링합니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼

<a name="csrf-field"></a>
### CSRF 필드

HTML 폼을 만들 때는 [CSRF 보호](/docs/10.x/csrf) 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF 토큰 필드를 반드시 포함해야 합니다. Blade `@csrf` 지시어를 사용해 간단히 토큰 필드를 생성하세요:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않으므로, 숨겨진 `_method` 필드로 이 메서드들을 모방해야 합니다. `@method` 지시어가 이를 생성합니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 검증 오류 표시

`@error` 지시어로 특정 필드의 [검증 오류 메시지](/docs/10.x/validation#quick-displaying-the-validation-errors)가 있는지 빠르게 검사할 수 있습니다. 내장된 `$message` 변수로 오류 메시지를 출력합니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

`@error`는 컴파일 시 if문으로 변환되므로, 오류가 없을 때 표시할 내용은 `@else`로 렌더링합니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

여러 검증 오류 그룹(에러백)이 있을 때는 두 번째 인수로 오류백 이름을 지정할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
## 스택

Blade는 이름 있는 스택에 콘텐츠를 여러 번 푸시할 수 있으며, 다른 뷰나 레이아웃에서 해당 스택을 출력할 수 있습니다. 주로 자바스크립트 라이브러리 로딩 등에서 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

불리언 조건에 따라 푸시하려면 `@pushIf` 지시어를 사용하세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

원하는 만큼 여러 번 `@push` 할 수 있습니다. 스택 내 모든 콘텐츠를 출력하려면 `@stack` 지시어를 사용합니다:

```blade
<head>
    <!-- Head contents -->

    @stack('scripts')
</head>
```

스택 맨 앞에 내용 추가는 `@prepend` 지시어를 쓰세요:

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
## 서비스 주입

`@inject` 지시어로 Laravel [서비스 컨테이너](/docs/10.x/container)에서 서비스를 뷰에 주입할 수 있습니다. 첫 번째 인수로 변수명, 두 번째 인수로 클래스나 인터페이스명을 전달합니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

원시 Blade 템플릿 문자열을 유효한 HTML로 변환해야 할 때 `Blade` 파사드의 `render` 메서드를 사용하세요. 첫 번째 인수로 템플릿 문자열, 두 번째 인수로 데이터를 넘깁니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 템플릿을 `storage/framework/views`에 임시 저장하고 렌더링합니다. 렌더링 후 임시 파일을 삭제하려면 `deleteCachedView` 인수를 `true`로 전달하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

Turbo, htmx 같은 프론트엔드 프레임워크를 쓸 때, 뷰 일부만 반환하는 경우가 있습니다. Blade "프래그먼트" 기능을 활용하세요. 먼저, 템플릿 내 `@fragment`와 `@endfragment`로 일부 영역을 감쉉니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이 뷰를 렌더링할 때 특정 프래그먼트만 반환하려면 `fragment` 메서드를 호출하세요:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건부로 프래그먼트 반환 시 `fragmentIf`를 씁니다. 조건이 거짓이면 전체 뷰를 반환합니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

복수 프래그먼트를 반환하려면 `fragments`와 `fragmentsIf` 메서드를 사용하고, 프래그먼트들이 연결됩니다:

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
## Blade 확장

Blade는 `directive` 메서드로 커스텀 지시어를 정의할 수 있습니다. 컴파일러가 해당 지시어를 발견하면, 파라미터 표현식을 인수로 콜백 함수를 호출합니다.

예를 들어 `@datetime($var)` 지시어를 만들어 `DateTime` 객체의 포맷을 지정할 수 있습니다. 다음 코드를 `AppServiceProvider`에 추가하세요:

```
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

이 지시어는 전달받은 표현식에 `format` 메서드를 호출해 다음과 같은 PHP 코드로 변환됩니다:

```
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]  
> Blade 지시어 로직을 수정한 후에는 캐시된 뷰를 모두 삭제해야 합니다. `view:clear` Artisan 명령어를 사용하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 출력 핸들러

Blade로 객체를 출력하면 객체의 `__toString` 메서드가 호출됩니다. 하지만 제어할 수 없는 외부 클래스가 있을 수 있습니다.

이럴 때는 Blade에 해당 타입에 맞는 커스텀 출력 핸들러를 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 등록합니다:

```
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

이후 Blade 템플릿에서 간단히 다음과 같이 객체를 출력하면 커스텀 핸들러가 실행됩니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 if문

복잡한 커스텀 지시어 대신 단순 조건을 위한 `Blade::if` 메서드가 있습니다. 클로저를 넘겨 새 조건부 지시어를 만듭니다. 예를 들어 앱의 기본 디스크를 확인하는 조건부를 만들려면 `AppServiceProvider`의 `boot`에서 다음과 같이 작성하세요:

```
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

이후 템플릿에서 다음과 같이 쓸 수 있습니다:

```blade
@disk('local')
    <!-- 로컬 디스크 사용 중 -->
@elsedisk('s3')
    <!-- s3 디스크 사용 중 -->
@else
    <!-- 기타 디스크 사용 중 -->
@enddisk

@unlessdisk('local')
    <!-- 로컬 디스크가 아님 -->
@enddisk
```