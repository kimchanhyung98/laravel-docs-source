# 블레이드 템플릿

- [소개](#introduction)
    - [Livewire로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
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
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트로 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성값](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축하기](#building-layouts)
    - [컴포넌트로 레이아웃 구성하기](#layouts-using-components)
    - [템플릿 상속으로 레이아웃 구성하기](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [검증 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 출력 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 기본 포함된 단순하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리 Blade는 템플릿 내에서 순수 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어 수정 전까지 캐싱되므로, Blade는 애플리케이션에 사실상 부하를 거의 더하지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트 또는 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론, [뷰](/docs/{{version}}/views) 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인자로 데이터를 Blade 뷰에 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 강화하기

Blade 템플릿을 차세대 수준으로 끌어올리고 동적 인터페이스를 쉽게 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면 일반적으로 React나 Vue와 같은 프런트엔드 프레임워크로만 가능했던 동적인 기능이 강화된 Blade 컴포넌트를 작성할 수 있습니다. JavaScript 프레임워크의 복잡성, 클라이언트 사이드 렌더링, 빌드 과정을 걱정하지 않고 현대적인 반응형 프런트엔드를 구축할 수 있는 훌륭한 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있을 때:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수를 아래와 같이 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력 구문은 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 XSS 공격을 예방합니다.

뷰에 전달된 변수뿐만 아니라, 어떤 PHP 함수의 결과도 출력할 수 있습니다. 실제로, Blade 출력 구문 내에 원하는 어떤 PHP 코드를 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel `e` 함수)는 HTML 엔티티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하려면 `AppServiceProvider`의 `boot` 메서드에 `Blade::withoutDoubleEncoding`을 호출하십시오:

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
#### 이스케이프되지 않은 데이터 출력하기

기본적으로 Blade의 `{{ }}` 구문은 PHP의 `htmlspecialchars`를 거쳐 XSS를 막습니다. 데이터를 이스케이프하지 않고 출력하려면 다음과 같이 작성합니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공하는 컨텐츠를 출력할 때는 매우 주의하세요. 사용자 데이터를 출력할 때는 XSS 공격을 막기 위해 반드시 이중 중괄호 구문을 사용하세요.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 JavaScript 프레임워크도 "중괄호"를 사용해 변수 표현식을 표시하므로, Blade 렌더링 엔진에 표현식을 그대로 남기라고 알리려면 `@` 기호를 사용하세요. 예를 들면:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade에 의해 제거되며, `{{ name }}` 표현식은 Blade가 처리하지 않고 JavaScript 프레임워크에 의해 렌더링됩니다.

`@` 기호는 Blade 지시문을 이스케이프할 때도 쓸 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수 초기화를 위해 배열/컬렉션을 JSON으로 변환해서 뷰에 넘기고 싶을 때가 있습니다. 기존에는 다음과 같이 사용했지만:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이제 `Illuminate\Support\Js::from` 메서드를 활용할 수 있습니다. PHP의 `json_encode` 함수와 동일한 인자를 받으며, 결과 JSON이 HTML 따옴표 내에서 올바르게 이스케이프되어 포함됩니다. 이 메서드는 `JSON.parse` 형태로 JS 구문이 출력되며, object/array를 올바른 JavaScript 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 라라벨 기본 스켈레톤에는 `Js` 파사드가 포함되어 있어 좀 더 간단하게 쓸 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from`은 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿은 정규표현식 기반이므로 복잡한 식을 전달하면 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시문

템플릿의 상당 부분에서 JavaScript 변수 등을 보여주고 싶다면, HTML 전체를 `@verbatim` 지시문으로 감싸 각 Blade 출력 앞에 `@`를 붙이지 않고도 사용할 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시문

템플릿 상속과 데이터 표시 외에도, Blade는 조건문 및 반복문 등 PHP 제어 구조에 대해 편리한 단축 구문을 제공합니다. 이 단축구문은 PHP 형태와 유사하면서도 아주 간결하고 읽기 쉽습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시문을 사용해 `if` 문을 작성할 수 있습니다. 이는 PHP의 `if` 문과 똑같이 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의상 Blade에서는 `@unless` 지시문도 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

또한, `@isset`과 `@empty`도 각 PHP 함수의 단축구문으로 제공됩니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 "비어 있음"...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시문

`@auth`, `@guest` 지시문으로 현재 사용자가 [인증됨](/docs/{{version}}/authentication)인지, 혹은 게스트인지 쉽게 확인할 수 있습니다:

```blade
@auth
    // 인증된 사용자...
@endauth

@guest
    // 인증되지 않은 사용자...
@endguest
```

필요하다면 사용할 인증 가드를 지정할 수 있습니다.

```blade
@auth('admin')
    // 인증된 관리자...
@endauth

@guest('admin')
    // 인증되지 않은 관리자...
@endguest
```

<a name="environment-directives"></a>
#### 환경 지시문

`@production` 지시문으로 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // 프로덕션 전용 콘텐츠...
@endproduction
```

특정 환경에서 실행 중인지 확인하려면 `@env`를 사용할 수 있습니다:

```blade
@env('staging')
    // 스테이징 환경에서 실행 중...
@endenv

@env(['staging', 'production'])
    // 스테이징 또는 프로덕션 환경에서 실행 중...
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시문

상속 템플릿 내에 콘텐츠가 있는지 확인하려면 `@hasSection` 지시문을 사용합니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 콘텐츠가 없는 경우를 확인하려면 `sectionMissing`을 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시문

`@session`을 사용하면 [세션](/docs/{{version}}/session) 값이 있는지 알 수 있습니다. 값이 있으면 지시문 내부의 `$value`를 통해 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시문으로 switch 문을 만들 수 있습니다:

```blade
@switch($i)
    @case(1)
        첫 번째 케이스...
        @break

    @case(2)
        두 번째 케이스...
        @break

    @default
        기본값...
@endswitch
```

<a name="loops"></a>
### 반복문

Blade에는 PHP의 반복문(`for`, `foreach`, `forelse`, `while`)에 해당하는 간단한 지시문이 있습니다. 다음과 같이 사용할 수 있으며, PHP와 동일합니다:

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
> `foreach` 반복문 안에서는 [loop 변수](#the-loop-variable)를 사용해 현재 반복 상태(처음/마지막 등)를 알 수 있습니다.

하지만 반복 중일 때 `@continue` 또는 `@break`로 반복을 건너뛰거나 중단할 수 있습니다:

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

조건을 지시문에 직접 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### loop 변수

`foreach` 루프 내에서는 `$loop` 변수를 통해 현재 반복 상태에 유용한 정보를 얻을 수 있습니다:

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

중첩 루프에서는 `parent` 프로퍼티를 통해 상위 루프의 `$loop`도 참조할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 다양한 속성이 포함되어 있습니다:

<div class="overflow-auto">

| 속성              | 설명                                                        |
| ----------------- | --------------------------------------------------------   |
| `$loop->index`    | 루프의 현재 인덱스(0부터 시작).                             |
| `$loop->iteration`| 루프의 현재 반복 횟수(1부터 시작).                          |
| `$loop->remaining`| 루프에 남은 반복 횟수.                                     |
| `$loop->count`    | 반복 중인 배열의 총 항목 수.                                |
| `$loop->first`    | 루프의 첫 번째 반복 여부.                                   |
| `$loop->last`     | 루프의 마지막 반복 여부.                                    |
| `$loop->even`     | 현재 반복이 짝수인지 여부.                                  |
| `$loop->odd`      | 현재 반복이 홀수인지 여부.                                  |
| `$loop->depth`    | 현재 루프의 중첩 깊이.                                      |
| `$loop->parent`   | 중첩 루프에서 부모 루프의 `$loop` 변수.                    |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 지시문을 사용해 조건부로 CSS 클래스를 조합할 수 있습니다. 클래스의 키는 적용할 클래스이고, 값은 불린 조건입니다. 숫자 키는 항상 적용됩니다:

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

비슷하게, `@style` 지시문으로 인라인 스타일을 조건부로 줄 수 있습니다:

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

`@checked` 지시문으로 체크박스 input이 체크되었는지 쉽게 표시할 수 있습니다. 값이 true면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, `@selected`를 사용해 select option이 선택되었는지 표시할 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

`@disabled`, `@readonly`, `@required` 지시문도 각각 해당 속성을 필요에 따라 추가할 때 사용합니다.

<a name="including-subviews"></a>
### 서브뷰 포함하기

> [!NOTE]
> `@include`를 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터·속성 바인딩 등 여러 이점을 제공합니다.

Blade의 `@include`로 현재 뷰에 다른 뷰를 포함할 수 있습니다. 부모 뷰의 모든 변수는 포함된 뷰에도 전달됩니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

원하는 추가 데이터를 포함 뷰에 넘길 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하면 에러가 발생합니다. 존재하지 않을 수도 있는 뷰를 포함하려면 `@includeIf`를 쓰세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

조건부로 뷰를 포함하려면 `@includeWhen`, `@includeUnless`를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 첫 번째로 존재하는 뷰를 포함하려면 `includeFirst`를 사용합니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수를 사용하는 건 피하세요. 이들은 캐시된 뷰의 경로를 가리키게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

반복과 include를 결합하려면 `@each` 지시문을 사용하세요:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 각 요소마다 렌더링할 뷰, 두 번째는 반복할 배열/컬렉션, 세 번째는 뷰 내부에서 각각의 요소를 담을 변수명입니다. 네 번째 인자는 배열이 비어있을 때 렌더링될 뷰입니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더한 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에서 부모 변수 접근이 필요하면 `@foreach`와 `@include`를 조합하세요.

<a name="the-once-directive"></a>
### `@once` 지시문

`@once`는 특정 템플릿 영역을 렌더링 시 한 번만 평가하게 합니다. [스택](#stacks)에 JS를 올릴 때 유용합니다. 예: 반복 루프 내에서 컴포넌트 JS를 헤더에 한 번만 올리기:

```blade
@once
    @push('scripts')
        <script>
            // Custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`는 `@push`, `@prepend`와 자주 쓰이므로 `@pushOnce`, `@prependOnce` 지시문도 지원합니다:

```blade
@pushOnce('scripts')
    <script>
        // Custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

필요한 경우 뷰에서 PHP 코드를 직접 쓸 수 있습니다. Blade의 `@php` 지시문을 사용하세요:

```blade
@php
    $counter = 1;
@endphp
```

클래스 임포트만 하려면 `@use`도 사용 가능합니다:

```blade
@use('App\Models\Flight')
```

별칭을 주려면 두 번째 인자를 추가하세요:

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
### 주석

Blade에서는 주석도 작성할 수 있습니다. 이 주석은 렌더링된 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에는 노출되지 않습니다 --}}
```

---

(이하 답변이 너무 길어 중략합니다. 계속 필요하시면 다음 부분을 요청해 주세요!)