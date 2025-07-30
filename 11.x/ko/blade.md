# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 성능 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 지시어](#blade-directives)
    - [if 문](#if-statements)
    - [switch 문](#switch-statements)
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
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [수동으로 컴포넌트 등록하기](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성](#data-properties-attributes)
    - [상위 데이터 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 오류 처리](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 조각 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 echo 핸들러](#custom-echo-handlers)
    - [커스텀 if 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 기본 포함된 심플하면서도 강력한 템플릿 엔진입니다. 다른 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실, 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어 수정될 때까지 캐시되므로, Blade는 애플리케이션에 거의 오버헤드를 추가하지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 가지며 일반적으로 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 전역 `view` 헬퍼를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰(Views)](/docs/11.x/views) 문서에 언급된 대로, `view` 헬퍼의 두 번째 인수로 데이터를 전달할 수도 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 성능 강화하기

Blade 템플릿을 한 단계 업그레이드하여 동적인 인터페이스를 손쉽게 만들고 싶나요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire는 React나 Vue 같은 프런트엔드 프레임워크에서만 가능했던 동적 기능을 갖춘 Blade 컴포넌트를 작성할 수 있도록 해줍니다. 복잡한 클라이언트 사이드 렌더링이나 빌드 과정 없이도 현대적이고 반응형인 프런트엔드를 구축할 수 있는 훌륭한 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시하기

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 다음 라우트가 있다고 가정해 봅니다:

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
> Blade의 `{{ }}` 에코 구문은 자동으로 PHP의 `htmlspecialchars` 함수에 전달되어 XSS 공격을 방지합니다.

뷰에 전달된 변수의 내용을 표시하는 데 제한되지 않고, PHP 함수 결과를 출력할 수도 있습니다. 사실, Blade 에코문 안에 원하는 어떤 PHP 코드라도 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade (및 Laravel의 `e` 함수)는 HTML 엔티티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

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
#### 이스케이프 처리되지 않은 데이터 표시하기

기본적으로 Blade의 `{{ }}` 문법은 PHP의 `htmlspecialchars` 함수가 자동 적용되어 XSS 공격을 방지합니다. 이스케이프 처리 없이 데이터를 출력하려면 다음 문법을 사용하세요:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]  
> 애플리케이션 사용자로부터 전달받은 내용을 출력할 때는 매우 주의하세요. 일반적으로 XSS 공격 방지를 위해 이스케이프된 중괄호 구문을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크

많은 JavaScript 프레임워크도 "중괄호"를 사용하여 표현식을 표시하므로, Blade 렌더링 엔진에게 표현식을 변경하지 말라고 알려주려면 `@` 기호를 사용할 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

여기서 `@` 기호는 Blade에 의해 제거되지만, `{{ name }}` 표현식은 Blade에 의해 변경되지 않고 남아 JavaScript 프레임워크가 처리하게 됩니다.

`@` 기호는 Blade 지시어를 이스케이프할 때도 사용할 수 있습니다:

```blade
{{-- Blade 템플릿 --}}
@@if()

<!-- HTML 출력 -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

때때로 JavaScript 변수를 초기화하기 위해 배열 데이터를 JSON으로 표현하고 싶을 수 있습니다. 예를 들어:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

하지만 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용하면 HTML 내 따옴표 처리에 적합한 올바른 JSON을 안전하게 생성할 수 있습니다. `from` 메서드는 `JSON.parse` JavaScript 구문을 반환하여 주어진 배열이나 객체를 올바른 JavaScript 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 기본 프로젝트에서는 `Js` 페이사드를 포함하여 편리하게 이 기능을 Blade 템플릿 내에서 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]  
> 변수 값을 JSON으로 렌더링하는 경우에만 `Js::from` 메서드를 사용해야 합니다. 복잡한 표현식을 넘기면 Blade 템플릿 정규식을 기반으로 동작하여 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿의 상당 부분에서 JavaScript 변수를 다뤄야 할 때는 각 Blade 에코 앞에 `@`를 붙이지 않아도 되도록, `@verbatim`과 `@endverbatim`로 묶을 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 지시어

템플릿 상속과 데이터 출력 외에도, Blade는 PHP 제어문(조건문, 반복문 등)을 위한 편리한 축약 구문을 제공합니다. 이 지시어들은 PHP와 동일하게 작동하면서 더 깔끔하고 간결한 코드를 작성할 수 있게 해줍니다.

<a name="if-statements"></a>
### if 문

`@if`, `@elseif`, `@else` 그리고 `@endif` 지시어를 사용해 `if` 문을 작성할 수 있습니다. PHP와 기능이 동일합니다:

```blade
@if (count($records) === 1)
    한 개의 레코드가 있습니다!
@elseif (count($records) > 1)
    여러 개의 레코드가 있습니다!
@else
    레코드가 없습니다!
@endif
```

편의를 위해 `@unless` 지시어도 제공합니다:

```blade
@unless (Auth::check())
    로그인하지 않았습니다.
@endunless
```

또한, `@isset`와 `@empty` 지시어를 PHP 함수 대체용으로 사용할 수 있습니다:

```blade
@isset($records)
    {{-- $records가 정의되어 있으며 null이 아닙니다 --}}
@endisset

@empty($records)
    {{-- $records가 비어있습니다 --}}
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시어

`@auth`와 `@guest` 지시어를 사용하면 현재 사용자가 [인증된 상태](/docs/11.x/authentication)인지 아니면 게스트인지 간단히 확인할 수 있습니다:

```blade
@auth
    {{-- 인증된 사용자 --}}
@endauth

@guest
    {{-- 인증되지 않은 사용자 --}}
@endguest
```

필요하다면, 특정 인증 가드를 지정하여 검사할 수도 있습니다:

```blade
@auth('admin')
    {{-- admin 인증 가드 사용자가 인증됨 --}}
@endauth

@guest('admin')
    {{-- admin 가드 사용자가 인증되지 않음 --}}
@endguest
```

<a name="environment-directives"></a>
#### 환경 지시어

애플리케이션이 프로덕션 환경인지 확인하려면 `@production` 지시어를 사용하세요:

```blade
@production
    {{-- 프로덕션 전용 콘텐츠 --}}
@endproduction
```

또는 특정 환경인지 `@env` 지시어를 통해 검사할 수 있습니다:

```blade
@env('staging')
    {{-- staging 환경 --}}
@endenv

@env(['staging', 'production'])
    {{-- staging 또는 production 환경 --}}
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시어

템플릿 상속에서 섹션에 콘텐츠가 있는지 확인하려면 `@hasSection` 지시어를 사용하세요:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션이 비었는지 확인할 때는 `sectionMissing` 지시어를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시어

`@session` 지시어로 [세션 값](/docs/11.x/session)이 있는지 확인할 수 있습니다. 세션 값이 존재하면 `@session`과 `@endsession` 블록이 실행되며, `$value` 변수를 통해 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어를 사용해 switch 문을 작성할 수 있습니다:

```blade
@switch($i)
    @case(1)
        첫 번째 경우...
        @break

    @case(2)
        두 번째 경우...
        @break

    @default
        기본 경우...
@endswitch
```

<a name="loops"></a>
### 반복문

조건문 외에도 Blade는 PHP 반복문을 위한 간단한 지시어를 제공합니다. 모두 PHP 문법과 동일하게 동작합니다:

```blade
@for ($i = 0; $i < 10; $i++)
    현재 값은 {{ $i }}입니다.
@endfor

@foreach ($users as $user)
    <p>사용자 ID: {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>사용자가 없습니다.</p>
@endforelse

@while (true)
    <p>계속 반복 중입니다.</p>
@endwhile
```

> [!NOTE]  
> `foreach` 반복문 안에서 [루프 변수](#the-loop-variable)를 사용해 첫 번째 또는 마지막 반복인지 등의 정보를 얻을 수 있습니다.

반복 중 현재 루프를 건너뛰거나 종료하려면 `@continue`와 `@break` 지시어를 사용하세요:

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

조건을 지시어 선언부에 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 반복문 내에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수로 현재 인덱스, 첫 번째/마지막 반복 여부 등 유용한 정보를 취득할 수 있습니다:

```blade
@foreach ($users as $user)
    @if ($loop->first)
        첫 번째 반복입니다.
    @endif

    @if ($loop->last)
        마지막 반복입니다.
    @endif

    <p>사용자 ID: {{ $user->id }}</p>
@endforeach
```

중첩된 루프 내에서는 `parent` 속성을 통해 상위 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            상위 루프의 첫 번째 반복입니다.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 주요 속성은 다음과 같습니다:

| 속성              | 설명                                  |
|-----------------|-------------------------------------|
| `$loop->index`   | 현재 반복의 인덱스 (0부터 시작)          |
| `$loop->iteration` | 현재 반복 횟수 (1부터 시작)              |
| `$loop->remaining` | 남은 반복 횟수                        |
| `$loop->count`   | 반복할 총 아이템 수                    |
| `$loop->first`   | 첫 번째 반복 여부                      |
| `$loop->last`    | 마지막 반복 여부                      |
| `$loop->even`    | 짝수 반복 여부                        |
| `$loop->odd`     | 홀수 반복 여부                        |
| `$loop->depth`   | 현재 반복의 중첩 깊이                   |
| `$loop->parent`  | 중첩 루프에서 상위 루프의 `$loop` 변수    |

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 지시어는 조건에 따라 CSS 클래스 문자열을 컴파일합니다. 배열을 받아 키는 클래스명, 값은 부울식입니다. 숫자 키의 경우 무조건 포함됩니다:

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

마찬가지로 `@style` 지시어는 조건부로 인라인 CSS 스타일을 추가할 수 있습니다:

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

`@checked` 지시어는 checkbox 입력이 체크 여부를 쉽게 표시합니다. 조건이 참이면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

`@selected` 지시어는 select 옵션이 선택되었는지 표시합니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled` 지시어는 요소가 비활성화됐는지 다음처럼 표시합니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

또한 `@readonly` 지시어는 읽기 전용 여부를 나타냅니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

`@required` 지시어는 필수 입력 여부를 나타냅니다:

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
> `@include` 지시어를 자유롭게 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 `@include`보다 몇 가지 장점을 제공합니다.

Blade의 `@include` 지시어로 다른 Blade 뷰를 현재 뷰 내에 포함할 수 있습니다. 부모 뷰의 모든 변수가 포함된 뷰에서 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

추가적으로 포함할 뷰에 전달할 데이터를 배열로 넘길 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않을 수도 있는 뷰를 포함하려면 `@includeIf` 지시어를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

조건에 따라 뷰를 포함하려면 `@includeWhen`과 `@includeUnless` 지시어를 사용합니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

뷰 배열에서 존재하는 첫 번째 뷰를 포함하려면 `includeFirst` 지시어를 사용하세요:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]  
> Blade 뷰 내에서 `__DIR__`와 `__FILE__` 상수 사용은 권장하지 않습니다. 이 값들은 캐시된 컴파일 뷰 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

`@each` 지시어로 루프와 포함을 한 줄로 간단히 작성할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 각 항목에 대해 렌더링할 뷰, 두 번째는 루프 대상 배열 또는 컬렉션, 세 번째 인수는 현재 항목을 참조할 뷰 내 변수명입니다. 현재 배열 키는 뷰 내에서 `key` 변수로 참조됩니다.

네 번째 인수를 추가로 지정하여 빈 배열일 때 렌더링할 뷰를 지정할 수 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]  
> `@each`를 통한 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에 필요하다면 `@foreach`와 `@include`를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어는 템플릿 내 특정 부분이 렌더링 사이클 중 한 번만 실행되게 합니다. 반복문 안에서 컴포넌트의 자바스크립트를 한 번만 푸시할 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // 커스텀 JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 주로 `@push`나 `@prepend`와 쓰이므로, 편의를 위해 `@pushOnce`와 `@prependOnce` 지시어도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // 커스텀 JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP

뷰 내에 PHP 코드를 넣어야 할 때는 `@php` 지시어를 사용하세요:

```blade
@php
    $counter = 1;
@endphp
```

클래스를 임포트할 용도라면 `@use` 지시어를 사용합니다:

```blade
@use('App\Models\Flight')
```

별칭을 부여할 수도 있습니다:

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
### 주석

Blade는 HTML 주석과는 다르게, 컴파일 결과에 포함되지 않는 주석도 지원합니다:

```blade
{{-- 렌더링된 HTML에 나타나지 않는 주석 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 유사한 이점을 제공하며, 일부에서는 더 이해하기 쉽습니다. 컴포넌트 작성 방법에는 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` Artisan 명령어를 사용합니다. 예를 들어 간단한 `Alert` 컴포넌트를 만들어 봅시다. 명령어는 `app/View/Components` 디렉토리에 컴포넌트 클래스를 생성합니다:

```shell
php artisan make:component Alert
```

또한 컴포넌트 뷰 템플릿이 `resources/views/components` 디렉토리 내에 생성됩니다. 애플리케이션 컴포넌트는 자동으로 `app/View/Components`와 `resources/views/components`에서 발견되므로, 별도의 등록이 일반적으로 필요하지 않습니다.

서브디렉토리에 컴포넌트를 생성할 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

이 명령은 `app/View/Components/Forms`에 `Input` 컴포넌트를 생성하며, 뷰는 `resources/views/components/forms`에 생성됩니다.

익명 컴포넌트(클래스 없이 Blade 템플릿만)로 생성하려면 `--view` 플래그를 사용하세요:

```shell
php artisan make:component forms.input --view
```

그러면 `resources/views/components/forms/input.blade.php`에 Blade 파일이 생성되며 `<x-forms.input />`으로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션 컴포넌트는 자동으로 발견되지만, 패키지용 컴포넌트를 작성할 경우 컴포넌트 클래스와 태그 별칭을 수동 등록해야 합니다. 패키지 서비스 프로바이더 `boot` 메서드에서 등록하는 것이 일반적입니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

`componentNamespace` 메서드로 네임스페이스 규칙에 따라 자동 로드도 가능합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 벤더 네임스페이스를 접두사로 하여 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 파스칼 케이스 규칙으로 컴포넌트 클래스를 자동 감지하며, 서브디렉토리는 점(`.`) 표기법으로 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 표시할 땐 Blade 컴포넌트 태그를 사용하는데, `x-`로 시작하며 컴포넌트 클래스 이름을 케밥 케이스(kebab-case)로 변환해 사용합니다:

```blade
<x-alert/>

<x-user-profile/>
```

`app/View/Components` 내부에 하위 디렉토리가 있을 땐 `.` 을 사용해 경로를 나타냅니다. 예를 들어 `app/View/Components/Inputs/Button.php` 컴포넌트는 다음과 같이 렌더링합니다:

```blade
<x-inputs.button/>
```

조건부 렌더링이 필요하면 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더링 여부 결정
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

컴포넌트 그룹 내 관련 컴포넌트를 하나의 디렉토리로 관리할 때가 있습니다. 예를 들어 "card" 컴포넌트가 다음과 같은 클래스 구조라면:

```none
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

보통 루트 `Card` 컴포넌트가 포함된 디렉토리명과 같으므로 `<x-card.card>`로 사용해야 할 것 같지만, 이름이 같은 경우 Laravel은 이것이 "루트" 컴포넌트라 간주하고 단순히 `<x-card>`로 렌더링할 수 있게 합니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

컴포넌트에 데이터를 전달하려면 HTML 속성을 이용하며, 단순한 원시 값(문자열 등)은 일반 HTML 속성 문자열로 전달합니다. PHP 변수나 표현식은 속성 이름 앞에 `:`를 붙여 전달하세요:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 전달받을 데이터 속성을 정의하세요. 모든 public 속성은 자동으로 컴포넌트 뷰에서 사용 가능합니다. `render` 메서드에서 별도로 뷰에 전달하지 않아도 됩니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스 생성자.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 컴포넌트 뷰 반환하기.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

렌더링 시 컴포넌트의 public 변수를 뷰 내에서 이름으로 출력합니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 네이밍 규칙

컴포넌트 생성자의 매개변수는 `camelCase`를 사용하고, HTML 속성에서는 `kebab-case`를 사용합니다. 예를 들어:

```php
/**
 * 컴포넌트 인스턴스 생성자.
 */
public function __construct(
    public string $alertType,
) {}
```

HTML에서 이렇게 전달합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성 문법

컴포넌트에 속성을 전달할 때, 변수명과 동일한 이름의 속성이라면 단축 문법을 쓸 수 있습니다:

```blade
{{-- 단축 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 동일한 의미 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같이 콜론(:) 접두사 속성을 사용하는 JavaScript 프레임워크와 겹칠 수 있으므로, 접두사에 두 개(`::`)를 붙여 PHP 표현식이 아님을 알릴 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    제출
</x-button>
```

렌더링 결과:

```blade
<button :class="{ danger: isDeleting }">
    제출
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿 내에서 public 메서드를 호출할 수 있습니다. 예를 들어 `isSelected`라는 메서드가 있다면:

```php
/**
 * 선택된 옵션인지 판별.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 뷰에서 이렇게 호출할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내 속성 및 슬롯 접근하기

컴포넌트 클래스의 `render` 메서드에서 컴포넌트 이름, 속성, 슬롯에 접근하려면 클로저를 반환하세요:

```php
use Closure;

/**
 * 컴포넌트 뷰 / 내용 반환.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>컴포넌트 내용</div>';
    };
}
```

클로저는 `$data` 배열을 인수로 받을 수 있으며, 이 배열에 다음 요소들이 포함됩니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>컴포넌트 내용</div>';
}
```

> [!WARNING]  
> 이 `$data` 배열 값을 Blade 문자열에 직접 삽입하면 악의적 속성으로 인해 원격 코드 실행 위험이 있으므로 주의하세요.

`componentName`은 `x-` 접두사 다음 태그명입니다(예: `<x-alert />`의 경우 `alert`). `attributes`는 HTML 태그의 모든 속성, `slot`은 슬롯 내용이 담긴 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저는 문자열을 반환해야 하며, 반환 문자열이 존재하는 뷰이면 뷰를 렌더링하고 아니면 인라인 Blade로 평가합니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트가 Laravel [서비스 컨테이너](/docs/11.x/container)에서 의존성을 주입받아야 할 경우, 데이터 속성 생성자 매개변수 앞에 타입 힌트를 추가하면 자동 주입됩니다:

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성자.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 숨길 속성 및 메서드

컴포넌트 템플릿에 노출하고 싶지 않은 public 메서드 또는 속성은 `$except` 배열에 포함시켜 차단할 수 있습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출되지 않을 속성 / 메서드 목록.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스 생성자.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성

앞서 데이터 속성 전달 방법을 살펴봤지만, `class` 같은 추가 HTML 속성도 지정해야 하는 경우가 있습니다. 이 경우 컴포넌트 템플릿의 최상위 요소에 이 속성들을 내려보내는 것이 일반적입니다. 예를 들어:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 없던 모든 속성은 자동으로 `$attributes`라는 "속성 가방"으로 컴포넌트에 전달됩니다. 이를 출력하려면 템플릿에서 `$attributes` 변수를 사용하세요:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]  
> 현재 컴포넌트 태그 내에서 `@env` 같은 지시어 사용은 지원되지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 / 병합 속성

속성 값의 기본값 지정이나 병합이 필요하면 `$attributes->merge` 메서드를 사용하세요. 기본 CSS 클래스를 지정할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트를 다음과 같이 호출했다고 가정하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더링 결과는 다음과 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건일 때만 클래스를 병합하려면 `class` 메서드를 사용하세요. 배열로 클래스와 조건을 전달합니다. 숫자 키 요소는 항상 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성과 병합할 땐 `class`와 `merge`를 체이닝할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]  
> 병합된 속성이 필요 없는 다른 HTML 요소에 조건부 클래스를 적용하려면 [`@class` 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

`class`가 아닌 속성을 병합할 때 `merge`에 전달한 값은 기본값으로 간주되며, 인젝션된 값과 병합되지 않고 덮어씌워집니다. 예를 들어 `button` 컴포넌트 구현:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

이 컴포넌트를 호출 시 커스텀 `type` 지정 가능하며, 미지정 시 기본값 사용:

```blade
<x-button type="submit">
    제출
</x-button>
```

위의 경우 렌더링 결과는 다음과 같습니다:

```blade
<button type="submit">
    제출
</button>
```

`class`가 아닌 속성도 기본값과 인젝션 값을 합치고 싶다면 `prepends` 메서드를 이용하세요. 예를 들어 `data-controller` 속성을 항상 `profile-controller`로 시작하게 만들 수 있습니다:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 조회 및 필터링

`filter` 메서드는 클로저를 받아 조건에 맞는 속성만 남깁니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith`는 특정 접두사로 시작하는 속성만 조회합니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 `whereDoesntStartWith`는 특정 접두사로 시작하지 않는 속성을 제외합니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first`는 속성 가방 중 첫 속성을 가져옵니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

속성 존재 여부는 `has` 메서드로 검사합니다:

```blade
@if ($attributes->has('class'))
    <div>클래스 속성이 존재합니다</div>
@endif
```

배열을 전달하면 모든 속성 존재 여부를 검사합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 존재합니다</div>
@endif
```

`hasAny`는 하나라도 존재하면 `true`를 반환합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>하나 이상의 속성이 존재합니다</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드를 사용합니다:

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 예약어

Blade 내부에서 컴포넌트 렌더링에 예약된 키워드는 다음과 같습니다. 이들은 컴포넌트 내 public 속성이나 메서드 이름으로 사용할 수 없습니다:

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯

컴포넌트에 추가 콘텐츠를 전달할 때는 "슬롯"을 사용합니다. 기본 슬롯은 `$slot` 변수를 출력하면 표시됩니다. 예를 들어 `alert` 컴포넌트 뷰가 다음과 같다고 가정합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트에 콘텐츠를 전달하는 방법:

```blade
<x-alert>
    <strong>안내!</strong> 문제가 발생했습니다!
</x-alert>
```

여러 개의 슬롯을 다뤄야 할 때는 "이름있는 슬롯"을 사용할 수 있습니다. 예를 들어 "title" 슬롯을 추가하려면:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이름 있는 슬롯은 `x-slot` 태그로 정의합니다. 명시적 슬롯 태그에 포함되지 않은 내용은 기본 `$slot` 변수에 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        서버 오류
    </x-slot>

    <strong>안내!</strong> 문제가 발생했습니다!
</x-alert>
```

슬롯에 내용이 있는지 검사하려면 `isEmpty` 메서드를 사용합니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        슬롯이 비어있을 때 기본 콘텐츠입니다.
    @else
        {{ $slot }}
    @endif
</div>
```

또한 HTML 주석이 아닌 “실제” 내용이 있는지 판단하는 `hasActualContent` 메서드도 있습니다:

```blade
@if ($slot->hasActualContent())
    슬록에 비주석 내용이 있습니다.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯

Vue 같은 JS 프레임워크에서 사용하는 "스코프 슬롯"과 유사하게, 컴포넌트 내 메서드·속성에 접근하려면 슬롯 내에서 `$component` 변수를 이용할 수 있습니다. 예를 들어 `x-alert` 컴포넌트에 `formatAlert`라는 public 메서드가 있다고 하면:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('서버 오류') }}
    </x-slot>

    <strong>안내!</strong> 문제가 발생했습니다!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성

Blade 컴포넌트처럼 슬롯에도 CSS 클래스 등 추가 [속성](#component-attributes)을 지정할 수 있습니다:

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        제목
    </x-slot>

    내용

    <x-slot:footer class="text-sm">
        바닥글
    </x-slot>
</x-card>
```

슬롯 속성은 슬롯 변수의 `attributes` 속성으로 접근할 수 있습니다. 상세 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

매우 작은 컴포넌트는 클래스와 템플릿을 따로 관리하는 것이 번거로울 수 있습니다. 이럴 때 `render` 메서드에서 마크업을 직접 반환할 수 있습니다:

```php
/**
 * 컴포넌트 뷰 / 내용 반환.
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

인라인 뷰 컴포넌트를 만들려면 `make:component` 명령 시 `--inline` 옵션을 사용하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

어떤 컴포넌트를 렌더링할지 실행 시에 결정해야 한다면 내장된 `dynamic-component` 컴포넌트를 활용하세요:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]  
> 아래 설명은 주로 Blade 컴포넌트를 포함하는 Laravel 패키지를 작성할 때 필요한 내용입니다. 일반 애플리케이션 개발자에게는 필요하지 않을 수 있습니다.

자체 애플리케이션 내 컴포넌트는 `app/View/Components`와 `resources/views/components`에서 자동 발견되지만, 패키지용 컴포넌트나 비표준 디렉토리에 컴포넌트를 둔다면 컴포넌트 클래스와 태그 별칭을 수동 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록 후 태그 별칭으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로드

패키지 컴포넌트가 `Package\Views\Components` 네임스페이스에 있을 경우 `componentNamespace` 메서드를 사용해 규칙에 의한 자동 로딩이 가능합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

벤더 네임스페이스 접두사를 사용해 다음처럼 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 클래스를 자동 감지하며, 서브 디렉토리는 점(`.`) 표기법으로 지원합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 유사하나, 클래스 없이 단일 뷰 파일만 사용하는 컴포넌트입니다. `resources/views/components` 디렉토리에 Blade 템플릿만 위치시키면 정의됩니다. 예를 들어 `resources/views/components/alert.blade.php`가 있다면 다음과 같이 렌더링합니다:

```blade
<x-alert/>
```

`.` 문자를 써서 하위 디렉토리를 표현할 수 있습니다. 예를 들어 `resources/views/components/inputs/button.blade.php` 컴포넌트는 이렇게 렌더링합니다:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

많은 템플릿으로 구성된 복합 컴포넌트는 하나의 디렉토리로 템플릿을 묶고 싶을 때가 있습니다. 예를 들어 "accordion" 컴포넌트가 다음과 같다면:

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

다음처럼 렌더링합니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

그러나 인덱스 컴포넌트를 `'accordion'` 디렉토리 안에 배치하지 못하므로 첫 번째 파일이 최상위 디렉토리에 있었습니다. Blade는 컴포넌트 디렉토리 내에 디렉토리명과 동일한 파일을 두는 것을 지원하며, 이를 루트 컴포넌트로 인식합니다. 따라서 다음과 같이 디렉토리 구조를 바꿀 수 있습니다:

```none
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성

익명 컴포넌트에는 클래스가 없으므로 어떤 속성을 컴포넌트 변수로, 어떤 속성을 [속성 가방](#component-attributes)으로 처리할지 구분해야 합니다.

`@props` 지시어를 템플릿 상단에 써서 데이터 변수로 사용할 속성명을 지정할 수 있습니다. 나머지는 속성 가방에 포함됩니다. 기본값 지정도 가능합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 정의된 컴포넌트는 이렇게 호출할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 상위 데이터 접근하기

상위 컴포넌트 데이터를 하위 컴포넌트에서 사용하려면 `@aware` 지시어를 쓰세요. 예를 들어 복잡한 메뉴 컴포넌트를 만들 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트는 다음과 같을 수 있습니다:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` 속성은 부모 컴포넌트에만 전달되어 자식에게는 기본으로 전달되지 않습니다. 하지만 자식 컴포넌트에서 `@aware`를 쓰면 전달받을 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]  
> `@aware`는 부모 컴포넌트가 HTML 속성으로 명시적으로 전달받은 데이터만 접근할 수 있습니다. 기본값(`@props`의 기본값)은 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

익명 컴포넌트는 기본적으로 `resources/views/components`에 템플릿을 위치하지만, 추가 경로를 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인수로 컴포넌트 경로를, 두 번째 인수로 (선택적) 네임스페이스 접두사를 받습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 호출하세요:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

접두사 없이 등록하면 컴포넌트 이름에 접두사가 없으며 다음과 같이 렌더링합니다:

```blade
<x-panel />
```

접두사를 지정하면 다음과 같이 네임스페이스 접두사를 붙여 렌더링합니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성하기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분 웹 애플리케이션은 여러 페이지에서 공통 레이아웃을 사용합니다. 매번 전체 레이아웃 HTML을 복제하는 것은 비효율적이고 유지보수도 어렵기 때문에, 이를 하나의 [Blade 컴포넌트](#components)로 정의해 재사용하는 것이 편리합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "todo 리스트" 애플리케이션에 다음과 같은 `layout` 컴포넌트를 정의할 수 있습니다:

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

정의된 `layout` 컴포넌트를 사용하는 Blade 뷰를 작성합니다. 예를 들어 작업 목록을 출력하는 뷰:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 주입된 콘텐츠는 기본적으로 `$slot` 변수에 전달됩니다. 이 레이아웃은 `$title` 슬롯도 지원하며, 제공되지 않을 때 기본값을 표시합니다. 작업 목록 뷰에서 슬롯을 이렇게 지정할 수 있습니다:

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

이제 라우트에서 `tasks` 뷰를 반환하기만 하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의

템플릿 상속으로도 레이아웃을 구성할 수 있습니다. 컴포넌트가 도입되기 전의 주요 방법입니다.

간단한 예시를 보겠습니다. 다음은 페이지만의 레이아웃입니다. 대부분 웹앱의 공통 레이아웃으로 유용합니다:

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            이곳은 마스터 사이드바입니다.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

기본 HTML 마크업에 `@section`과 `@yield` 지시어로 구획을 나눈 걸 보실 수 있습니다. `@section`은 콘텐츠 영역을 정의하고 `@yield`는 해당 섹션 출력 위치를 지정합니다.

레이아웃 정의 후 이 레이아웃을 상속받는 자식 뷰를 만듭니다.

<a name="extending-a-layout"></a>
#### 레이아웃 상속

자식 뷰에서 `@extends` 지시어를 통해 상속할 레이아웃을 지정합니다. 섹션 내용을 `@section` 지시어로 주입할 수 있습니다. 앞서 레이아웃에서 `@yield`로 지정한 부분에 삽입됩니다:

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', '페이지 제목')

@section('sidebar')
    @@parent

    <p>마스터 사이드바에 추가합니다.</p>
@endsection

@section('content')
    <p>본문 내용입니다.</p>
@endsection
```

`sidebar` 섹션에서는 `@@parent` 지시어로 기존 레이아웃 사이드바 내용을 이어붙였습니다. 이 지시어는 뷰 렌더링 시 상위 레이아웃의 내용을 대체합니다.

> [!NOTE]  
> 앞 예와 다르게, 이 `sidebar` 섹션은 `@endsection`으로 닫힙니다. `@endsection`은 섹션 정의만 하고, `@show`는 즉시 섹션 내용도 출력합니다.

`@yield` 지시어는 두 번째 인자로 기본값을 지정할 수 있으며, 해당 섹션이 비어 있을 때 출력됩니다:

```blade
@yield('content', '기본 콘텐츠')
```

<a name="forms"></a>
## 폼

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션 내에서 HTML 폼을 작성할 때, CSRF 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF 토큰 필드를 반드시 포함해야 합니다. `@csrf` 지시어로 쉽게 생성 가능합니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 PUT, PATCH, DELETE 메서드를 직접 지원하지 않으므로, `_method` 숨겨진 필드를 추가해 메서드 스푸핑을 해야 합니다. `@method` 지시어가 해당 필드를 만들어 줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 오류 처리

`@error` 지시어로 특정 필드 유효성 오류가 존재하는지 빠르게 검사할 수 있습니다. 이 안에서 `$message` 변수를 이용해 오류 메시지를 출력합니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">게시물 제목</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

또한 `@error`는 "if"문으로 컴파일되어, 오류 없을 시 `@else`를 사용한 조건부 렌더링도 가능합니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">이메일 주소</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 폼이 포함된 페이지에서는 에러 백 이름을 두 번째 인수로 넘겨 특정 에러 백 메시지를 가져올 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">이메일 주소</label>

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

Blade는 명명된 스택에 내용을 `push`하여, 다른 뷰나 레이아웃에서 한꺼번에 렌더링할 수 있게 합니다. 자식 뷰에서 필요한 JavaScript 라이브러리를 지정할 때 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

조건에 맞는 경우에만 푸시하려면 `@pushIf` 지시어를 쓰세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에 여러 번 푸시할 수 있으며, 전체 내용을 렌더링하려면 `@stack` 지시어에 스택 이름을 지정합니다:

```blade
<head>
    <!-- 헤드 내용 -->

    @stack('scripts')
</head>
```

스택 앞쪽에 내용을 추가하려면 `@prepend` 지시어를 사용하세요:

```blade
@push('scripts')
    두 번째 내용...
@endpush

// 이후에...

@prepend('scripts')
    첫 번째 내용...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입

`@inject` 지시어로 Laravel [서비스 컨테이너](/docs/11.x/container)에서 서비스를 간단히 주입할 수 있습니다. 첫 번째 인수는 변수명, 두 번째는 클래스 또는 서비스 이름입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    월간 수익: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

가끔 Blade 템플릿 문자열을 즉시 HTML로 렌더링할 필요가 있을 때가 있습니다. `Blade` 페이사드의 `render` 메서드를 사용하면 됩니다. 템플릿 문자열과 선택적 데이터 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 `storage/framework/views` 디렉토리에 임시 Blade 파일을 작성해 렌더링합니다. 렌더 후 임시 파일을 삭제하려면 `deleteCachedView` 인수를 `true`로 지정하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 조각 렌더링

[Turbo](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프런트엔드 프레임워크 사용시, HTTP 응답에 Blade 템플릿 일부만 반환하고 싶을 때가 있습니다. Blade "조각(fragment)" 기능이 이를 지원합니다. 다음과 같이 `@fragment`와 `@endfragment`로 묶습니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

뷰 렌더링 시 `fragment` 메서드로 반환할 조각을 지정:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드로 조건부 조각 반환도 가능합니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 조각을 반환하려면 `fragments` 및 `fragmentsIf` 메서드를 사용합니다. 반환된 조각들은 연결됩니다:

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

Blade는 `directive` 메서드로 커스텀 지시어를 정의할 수 있습니다. 컴파일러가 해당 지시어를 만나면 주어진 콜백에 표현식을 넘기고, 콜백이 반환하는 PHP 코드를 삽입합니다.

아래 예제는 `@datetime($var)` 지시어를 만들어 `DateTime` 객체를 특정 포맷으로 출력합니다:

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

이 지시어가 컴파일되면 최종 PHP 코드는 다음과 같습니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]  
> Blade 지시어 로직을 변경한 경우, 캐시된 Blade 뷰를 삭제해야 변경 사항이 반영됩니다. `view:clear` Artisan 명령을 이용하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 echo 핸들러

Blade에서 객체를 출력할 때 해당 객체의 `__toString` 메서드를 호출합니다. 그러나, 타사 라이브러리 클래스처럼 `__toString`을 제어할 수 없는 경우도 있습니다.

이럴 때는 Blade의 `stringable` 메서드에 타입별 맞춤 출력 함수를 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 설정합니다:

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

그 후 Blade 템플릿에서 객체를 간단히 출력하세요:

```blade
가격: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 if 문

간단한 커스텀 조건문을 정의하려면 `Blade::if` 메서드를 사용하세요. 클로저로 조건을 지정합니다. 예를 들어 앱 기본 "디스크" 설정을 확인하는 조건문:

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

등록 후 템플릿에서 이렇게 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 로컬 디스크를 사용하는 경우... -->
@elsedisk('s3')
    <!-- s3 디스크 사용 시... -->
@else
    <!-- 기타 디스크 사용 시... -->
@enddisk

@unlessdisk('local')
    <!-- 로컬 디스크가 아닌 경우... -->
@enddisk
```