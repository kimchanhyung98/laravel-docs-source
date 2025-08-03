# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강력하게 사용하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [원시 PHP 코드](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 어트리뷰트](#data-properties-attributes)
    - [부모 데이터 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검사 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 조각(fragment) 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 포함된 간단하면서도 강력한 템플릿 엔진입니다. 다른 PHP 템플릿 엔진과 달리 Blade는 템플릿 내에 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실 Blade 템플릿은 모두 평범한 PHP 코드로 컴파일되어 저장되며, 수정될 때까지 캐싱되므로, Blade가 애플리케이션에 부담을 거의 주지 않습니다. Blade 템플릿 파일은 보통 `.blade.php` 확장자를 가지며 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰(view)는 라우트나 컨트롤러에서 전역 `view` 헬퍼 함수를 사용해 반환할 수 있습니다. 물론 [뷰 문서](/docs/9.x/views)에서 설명한 것처럼, 뷰에 데이터를 전달할 때는 `view` 헬퍼의 두 번째 인수를 사용할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강력하게 사용하기 (Supercharging Blade With Livewire)

Blade 템플릿을 한 단계 더 발전시키고 동적인 UI를 쉽게 만들고 싶다면 [Laravel Livewire](https://laravel-livewire.com)를 확인하세요. Livewire는 주로 React나 Vue 같은 프론트엔드 프레임워크에서만 가능했던 동적 기능을 Blade 컴포넌트에 추가할 수 있게 해줍니다. 따라서 복잡한 클라이언트 사이드 렌더링이나 빌드 과정 없이도 현대적인 반응형 프론트엔드를 구축하는 훌륭한 방법입니다.

<a name="displaying-data"></a>
## 데이터 출력 (Displaying Data)

Blade 뷰에 전달된 변수를 중괄호(`{{ }}`)로 감싸 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정하면:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 출력할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 문은 자동으로 PHP의 `htmlspecialchars` 함수를 통과하여 XSS 공격을 방지합니다.

뷰로 전달된 변수의 내용뿐만 아니라, 모든 PHP 함수의 결과도 출력할 수 있습니다. 사실 Blade 에코문 내에 원하는 어떤 PHP 코드도 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로 Blade와 Laravel의 `e` 헬퍼는 HTML 엔티티를 이중 인코딩합니다. 만약 이중 인코딩을 사용하지 않으려면, `AppServiceProvider`의 `boot` 메서드 내에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프 처리되지 않은 데이터 출력하기 (Displaying Unescaped Data)

기본적으로 Blade의 `{{ }}` 문은 PHP의 `htmlspecialchars` 함수에 자동으로 전달되어 XSS 공격을 방지합니다. 만약 데이터가 이스케이프 처리되지 않고 그대로 출력되길 원한다면, 다음과 같은 문법을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공한 내용을 출력할 때는 매우 주의해야 합니다. 보통은 사용자 제공 데이터에 대해 XSS 방지를 위해 위와 같이 이스케이프 처리된 중괄호 문법을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크 (Blade & JavaScript Frameworks)

많은 JavaScript 프레임워크들도 중괄호(`{{ }}`)를 사용하여 표현식을 표시합니다. 이때 Blade가 표현식을 건드리지 않게 하려면, `@` 기호를 앞에 붙여 Blade에서 처리하지 않도록 할 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예시에서 `@` 기호는 Blade에 의해 제거되지만, `{{ name }}` 표현식은 그대로 남아 JavaScript 프레임워크가 렌더링할 수 있습니다.

`@`는 Blade 디렉티브를 이스케이프하는 데도 사용할 수 있습니다:

```blade
{{-- Blade 템플릿 --}}
@@if()

<!-- 렌더링된 HTML -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링하기 (Rendering JSON)

종종 배열을 뷰로 전달해 자바스크립트 변수 초기화용 JSON으로 렌더링해야 할 때가 있습니다. 예를 들면:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 같은 인수를 받지만, HTML 내 인용부호에 적절한 이스케이프 처리를 보장합니다. 결과로 문자열의 `JSON.parse` 자바스크립트 문을 반환하여 유효한 JavaScript 객체로 변환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel 최신 버전에는 `Js` 팩사드가 포함되어 있어 Blade 템플릿 내에서 쉽게 쓸 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿 엔진이 정규 표현식을 사용하기 때문에, 복잡한 표현식을 전달하면 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿 내에서 많은 양의 JavaScript 변수를 출력해야 할 경우, 각 Blade 에코문 앞에 매번 `@`를 붙이는 대신 `@verbatim`으로 HTML 블록 전체를 감쌀 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브 (Blade Directives)

템플릿 상속 및 데이터 출력 외에도 Blade는 조건문 및 반복문 같은 PHP 제어구조에 대한 편리한 단축구문을 제공합니다. 이 디렉티브들은 PHP 원문과 기능이 동일하면서도 간결하고 깔끔한 문법을 제공합니다.

<a name="if-statements"></a>
### If 문 (If Statements)

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용해 조건문을 작성할 수 있으며, PHP의 if 문과 동일하게 동작합니다:

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

또한, PHP 함수 `isset`과 `empty`에 대응하는 `@isset`과 `@empty` 디렉티브를 사용할 수 있습니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님...
@endisset

@empty($records)
    // $records가 비어 있음...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 디렉티브 (Authentication Directives)

`@auth`와 `@guest` 디렉티브로 현재 사용자가 [인증된 사용자](/docs/9.x/authentication)인지 아니면 비회원인지를 빠르게 확인할 수 있습니다:

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면, `@auth`와 `@guest`에 검사할 인증 가드를 지정할 수도 있습니다:

```blade
@auth('admin')
    // admin 가드로 인증된 사용자...
@endauth

@guest('admin')
    // admin 가드로 인증되지 않은 사용자...
@endguest
```

<a name="environment-directives"></a>
#### 환경 관련 디렉티브 (Environment Directives)

애플리케이션이 프로덕션 환경에서 실행 중인지 확인하려면 `@production`을 사용할 수 있습니다:

```blade
@production
    // 프로덕션 환경에서만 보여줄 내용...
@endproduction
```

또한, 특정 환경에서 실행 중인지 확인하려면 `@env` 디렉티브를 사용하세요:

```blade
@env('staging')
    // "staging" 환경에서 실행중...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경에서 실행중...
@endenv
```

<a name="section-directives"></a>
#### 섹션 존재 여부 디렉티브 (Section Directives)

템플릿 상속의 섹션에 내용이 있는지 확인하려면 `@hasSection` 디렉티브를 사용합니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

내용이 없는 섹션인지 확인하려면 `@sectionMissing` 디렉티브를 사용합니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="switch-statements"></a>
### Switch 문 (Switch Statements)

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용해 switch 문을 작성할 수 있습니다:

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

조건문 외에도 반복문 작업을 위한 간단한 디렉티브를 제공합니다. 이들 역시 PHP 원문과 동일하게 동작합니다:

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
> `foreach` 루프를 돌면서 [루프 변수](#the-loop-variable)를 사용하면 첫 번째 반복인지, 마지막 반복인지 등의 유용한 정보를 얻을 수 있습니다.

반복문 내부에서 현재 반복을 건너뛰거나 루프를 중단할 때는 `@continue`와 `@break` 디렉티브를 사용합니다:

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

조건식을 괄호 안에 직접 넣을 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수 (The Loop Variable)

`foreach` 반복문 내부에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복문의 여러 상태 정보를 제공합니다:

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

중첩 루프일 경우 부모 루프의 `$loop` 변수는 `parent` 속성으로 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 유용한 속성은 다음과 같습니다:

| 속성               | 설명                                             |
|--------------------|--------------------------------------------------|
| `$loop->index`      | 현재 반복 인덱스 (0부터 시작)                    |
| `$loop->iteration`  | 현재 반복 횟수 (1부터 시작)                       |
| `$loop->remaining`  | 남은 반복 수                                     |
| `$loop->count`      | 총 반복할 아이템 수                               |
| `$loop->first`      | 첫 번째 반복인지 여부                             |
| `$loop->last`       | 마지막 반복인지 여부                             |
| `$loop->even`       | 짝수 반복인지 여부                               |
| `$loop->odd`        | 홀수 반복인지 여부                               |
| `$loop->depth`      | 현재 반복 중첩 수준                              |
| `$loop->parent`     | 중첩 루프일 때 부모 루프의 `$loop` 변수          |

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일 (Conditional Classes & Styles)

`@class` 디렉티브는 조건에 따라 CSS 클래스를 컴파일합니다. 배열을 인자로 받아 key에는 클래스명, value에는 bool 표현식을 넣습니다. 숫자 키가 있을 경우 항상 포함됩니다:

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

마찬가지로 `@style` 디렉티브는 조건에 따라 인라인 CSS 스타일을 추가합니다:

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

다음 디렉티브들은 HTML 요소 속성을 조건에 따라 쉽게 추가할 수 있게 도와줍니다.

- `@checked`: 체크박스가 선택되어야 할 때 `checked` 속성을 출력합니다:

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

- `@selected`: 선택 옵션이 선택되어야 할 때 `selected` 속성을 출력합니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

- `@disabled`: 요소를 비활성화해야 할 때 `disabled` 속성을 출력합니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

- `@readonly`: 읽기 전용이어야 할 때 `readonly` 속성을 출력합니다:

```blade
<input type="email"
        name="email"
        value="email@laravel.com"
        @readonly($user->isNotAdmin()) />
```

- `@required`: 필수 입력이어야 할 때 `required` 속성을 출력합니다:

```blade
<input type="text"
        name="title"
        value="title"
        @required($user->isAdmin()) />
```

<a name="including-subviews"></a>
### 서브뷰 포함하기 (Including Subviews)

> [!NOTE]
> `@include` 디렉티브 사용은 자유롭지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩과 같은 추가 이점을 제공합니다.

`@include` 디렉티브로 부모 뷰 내 다른 Blade 뷰를 포함할 수 있으며, 부모 뷰의 모든 변수도 포함된 뷰에서 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

추가 데이터 배열을 포함 뷰에 전달할 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 포함하려 하여 에러가 나는 것을 피하려면 `@includeIf` 디렉티브를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

주어진 불리언 식이 참일 때만 포함하려면 `@includeWhen`, 거짓일 때만 포함하려면 `@includeUnless`를 사용합니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

다수 뷰 중 가장 먼저 존재하는 뷰만 포함하려면 `@includeFirst` 를 사용하세요:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰 내에서 `__DIR__`와 `__FILE__` 상수를 사용하지 않는 것이 좋습니다. 이들은 캐시된 컴파일된 뷰의 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링 (Rendering Views For Collections)

`@each` 디렉티브로 루프와 뷰 포함을 한 줄로 합칠 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 각 요소에 대해 렌더링할 뷰, 두 번째 인자는 배열 혹은 컬렉션, 세 번째 인자는 각 요소를 뷰 내에서 참조할 변수 이름입니다. 현재 반복 키는 `key` 변수로 접근할 수 있습니다.

네 번째 인자는 해당 배열이 비었을 때 렌더링할 대체 뷰입니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링된 뷰는 부모 뷰 변수들을 상속받지 않습니다. 만약 필요하다면 `@foreach`와 `@include`를 사용하세요.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once`는 템플릿 내에서 특정 구간을 한 번만 평가하게 해줍니다. 예를 들어, 컴포넌트를 루프 내에서 여러번 렌더링할 때, 자바스크립트를 페이지 헤더에 한 번만 추가하고 싶을 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 자바스크립트...
        </script>
    @endpush
@endonce
```

`@once`는 보통 `@push`나 `@prepend`와 함께 쓰이므로, `@pushOnce`와 `@prependOnce`도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 자바스크립트...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 원시 PHP 코드 (Raw PHP)

뷰에 직접 PHP 코드를 넣어야 할 때, `@php` 디렉티브를 사용해 블록 단위 PHP 코드를 실행할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

한 줄짜리 PHP 문장은 다음처럼 작성 가능합니다:

```blade
@php($counter = 1)
```

<a name="comments"></a>
### 주석 (Comments)

Blade 주석은 HTML에 포함되지 않으므로, 주석 내용을 유저에게 표시하지 않고도 템플릿 내에 남길 수 있습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 유사한 장점을 제공합니다. 컴포넌트를 작성하는 방법은 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용하세요. 간단한 `Alert` 컴포넌트를 생성한다고 가정합니다. 이 명령어는 `app/View/Components` 디렉터리에 컴포넌트 클래스를 생성합니다:

```shell
php artisan make:component Alert
```

이 명령은 컴포넌트 뷰도 `resources/views/components` 디렉터리에 생성합니다. 자신의 애플리케이션용 컴포넌트를 작성할 경우, 이 두 위치에 자동으로 컴포넌트를 탐지하므로 추가 등록은 필요 없습니다.

서브디렉터리 내 컴포넌트 생성도 가능합니다:

```shell
php artisan make:component Forms/Input
```

이 명령어는 `app/View/Components/Forms/Input.php` 클래스와 `resources/views/components/forms/input.blade.php` 뷰를 생성합니다.

클래스 없이 Blade 템플릿만 있는 익명 컴포넌트를 만들려면 `--view` 플래그를 사용하세요:

```shell
php artisan make:component forms.input --view
```

그러면 `resources/views/components/forms/input.blade.php`에 파일이 생성되고, `<x-forms.input />`로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록 (Manually Registering Package Components)

자신의 애플리케이션에서는 자동으로 컴포넌트를 인식하지만, 패키지를 개발하는 경우 컴포넌트 클래스와 그 HTML 태그 별칭을 수동으로 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot()
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후 `package-alert` 태그로 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 써서 네임스페이스 기반 자동 로딩도 가능합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이 경우 컴포넌트를 `vendor::` 구문으로 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 파스칼 케이스로 컴포넌트 클래스를 자동 찾으며, 하위 폴더도 "dot" 표기법으로 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링 (Rendering Components)

컴포넌트를 표시하려면 Blade 템플릿 내에서 `x-` 접두어가 붙은 태그를 사용합니다. 컴포넌트 클래스 이름은 `kebab-case`로 변경되어 태그 이름이 됩니다:

```blade
<x-alert/>

<x-user-profile/>
```

만약 컴포넌트 클래스가 `app/View/Components` 내 하위 폴더에 있다면 `.` 문자를 써서 표시합니다. 예를 들어 `app/View/Components/Inputs/Button.php` 컴포넌트는:

```blade
<x-inputs.button/>
```

로 렌더링할 수 있습니다.

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기 (Passing Data To Components)

HTML 속성으로 컴포넌트에 데이터를 전달할 수 있습니다. 고정된 원시값은 기본 HTML 속성 문자열로 전달하고, 변수나 PHP 표현식은 `:` 접두어를 가진 속성으로 전달하세요:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트의 데이터 속성은 클래스 생성자에서 모두 정의해야 합니다. 컴포넌트 클래스의 모든 공개 속성은 자동으로 뷰에서 사용할 수 있도록 제공되며, `render` 메서드 내에서 뷰에 따로 전달할 필요가 없습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 경고 타입
     *
     * @var string
     */
    public $type;

    /**
     * 메시지 내용
     *
     * @var string
     */
    public $message;

    /**
     * 컴포넌트 인스턴스 생성
     *
     * @param  string  $type
     * @param  string  $message
     * @return void
     */
    public function __construct($type, $message)
    {
        $this->type = $type;
        $this->message = $message;
    }

    /**
     * 뷰 혹은 컴포넌트 내용을 반환
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, 공개 변수는 컴포넌트 뷰에서 이름으로 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이스 규칙 (Casing)

컴포넌트 생성자 인수는 `camelCase`를 사용하고, HTML 속성에서는 하이픈으로 구분된 `kebab-case`를 사용합니다. 다음 예제를 참고하세요:

```php
/**
 * 컴포넌트 인스턴스 생성
 *
 * @param  string  $alertType
 * @return void
 */
public function __construct($alertType)
{
    $this->alertType = $alertType;
}
```

컴포넌트 사용 시:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 단축 문법 (Short Attribute Syntax)

컴포넌트에 속성을 전달할 때 종종 속성 이름과 변수 이름이 같을 수 있는데, 이 경우 다음처럼 간략하게 쓸 수 있습니다:

```blade
{{-- 단축 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 위와 동일 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프 (Escaping Attribute Rendering)

Alpine.js 같은 JavaScript 프레임워크도 `:` 접두어가 붙은 속성을 사용할 수 있습니다. 이때 Blade가 PHP 표현식으로 인식하지 않게 하려면 `::` 이중 콜론으로 시작하는 속성을 사용하세요:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

결과물은 다음과 같습니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드 (Component Methods)

공개 변수뿐만 아니라 컴포넌트 클래스의 공개 메서드도 뷰에서 호출할 수 있습니다. 예를 들어 `isSelected` 메서드가 있다면 뷰에서 다음과 같이 사용할 수 있습니다:

```php
/**
 * 선택된 옵션인지 확인
 *
 * @param  string  $option
 * @return bool
 */
public function isSelected($option)
{
    return $option === $this->selected;
}
```

뷰 내 사용법:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내 어트리뷰트 & 슬롯 접근 (Accessing Attributes & Slots Within Component Classes)

컴포넌트 클래스 내 `render` 메서드에서 컴포넌트 이름, 속성, 슬롯 내용을 받을 수 있습니다. 이를 위해 `render` 메서드는 클로저를 반환해야 하며, 인자로 `$data` 배열을 받습니다:

```php
/**
 * 컴포넌트 뷰 / 콘텐츠 반환
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
{
    return function (array $data) {
        // $data['componentName'];
        // $data['attributes'];
        // $data['slot'];

        return '<div>Components content</div>';
    };
}
```

`componentName`은 `<x-alert />` 사용 시 'alert' 입니다. `attributes` 배열에는 태그에 포함된 모든 속성이 들어 있고, `slot`은 `Illuminate\Support\HtmlString` 인스턴스로 슬롯 내용입니다.

클로저가 반환한 문자열이 기존 뷰면 해당 뷰를 렌더링하며, 아니면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입 (Additional Dependencies)

컴포넌트가 Laravel [서비스 컨테이너](/docs/9.x/container)의 의존성을 필요로 하면, 컴포넌트 데이터 속성보다 먼저 생성자의 인자로 선언하면 자동 주입됩니다:

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성
 *
 * @param  \App\Services\AlertCreator  $creator
 * @param  string  $type
 * @param  string  $message
 * @return void
 */
public function __construct(AlertCreator $creator, $type, $message)
{
    $this->creator = $creator;
    $this->type = $type;
    $this->message = $message;
}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성 / 메서드 숨기기 (Hiding Attributes / Methods)

공개 함수나 속성 중 컴포넌트 뷰에서 노출되지 않기를 원하면, 컴포넌트 클래스에 `$except` 배열 속성으로 숨길 목록을 지정할 수 있습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 경고 타입
     *
     * @var string
     */
    public $type;

    /**
     * 컴포넌트 뷰에 노출하지 않을 속성 / 메서드들
     *
     * @var array
     */
    protected $except = ['type'];
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성 (Component Attributes)

컴포넌트에 넘기는 데이터 속성 외에, `class` 같은 추가 HTML 속성을 지정해야 하는 경우가 많습니다. 이런 속성들은 보통 컴포넌트 템플릿의 루트 요소에 전달합니다. 예를 들어:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 포함되지 않은 속성들은 자동으로 "속성 가방(attribute bag)"에 모입니다. 이 가방은 `$attributes` 변수로 컴포넌트에 제공되며, 이를 출력하여 모든 추가 속성을 렌더링할 수 있습니다:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 현재 컴포넌트 태그 내에서 `@env` 같은 디렉티브 사용은 지원하지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 / 병합된 속성 (Default / Merged Attributes)

기본값을 지정하거나 기존 속성에 값을 병합하려면 `$attributes->merge` 메서드를 사용합니다. 보통 기본 CSS 클래스를 지정할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

사용 예:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

결과 HTML:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합 (Conditionally Merge Classes)

조건이 참일 때만 클래스를 병합하려면 `class` 메서드에 배열을 전달합니다. 배열 키는 클래스명, 값은 bool 표현식입니다. 숫자 키는 무조건 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성도 병합하고 싶다면 `class` 뒤에 `merge`를 체이닝하세요:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 특정 HTML 요소에 클래스를 조건부 컴파일할 필요가 있는데 병합 속성이 필요 없다면 [`@class` 디렉티브](#conditional-classes)를 이용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스 이외 속성 병합 (Non-Class Attribute Merging)

`class`가 아닌 속성은 `merge` 메서드로 전달한 값이 기본값이 됩니다. 하지만 `class`와 달리 병합되지 않고 덮어쓰기가 됩니다. 예를 들어 `button` 컴포넌트는 다음처럼 구현됩니다:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트를 사용할 때 `type`을 지정하지 않으면 기본 `'button'`이 사용됩니다:

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

클래스 이외의 속성에서 기본값과 전달된 값을 병합하려면 `prepends` 메서드를 사용하세요. 예:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

`data-controller` 속성은 항상 `profile-controller`로 시작하고 추가 값을 뒤에 붙입니다.

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회하기 (Retrieving & Filtering Attributes)

`filter` 메서드는 클로저를 받아 조건에 맞는 속성만 유지합니다:

```blade
{{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}
```

`whereStartsWith` 메서드는 특정 문자열로 시작하는 속성만 가져옵니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 `whereDoesntStartWith`는 특정 문자열로 시작하지 않는 속성만 가져옵니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드는 주어진 속성 집합의 첫 번째 속성을 출력합니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성이 존재하는지 확인하려면 `has` 메서드를 사용합니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드를 씁니다:

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade 내부에서 컴포넌트 렌더링에 예약된 키워드들이 있으며, 이들은 컴포넌트 내 공개 속성이나 함수 이름으로 사용할 수 없습니다:

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯 (Slots)

컴포넌트에 추가 내용을 전달하려면 "슬롯"을 사용합니다. 기본 슬롯 내용은 `{{$slot}}` 변수로 출력합니다. 예를 들어 `alert` 컴포넌트가 다음과 같이 정의되었다면:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트 호출 시 슬롯 내용을 다음과 같이 전달할 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 슬롯이 필요한 경우, 명명된 슬롯을 추가할 수 있습니다. 예를 들어 제목을 담는 `title` 슬롯을 넣으려면:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

뷰에서 명명된 슬롯은 `x-slot` 태그로 정의합니다:

```blade
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="scoped-slots"></a>
#### 스코프 슬롯 (Scoped Slots)

Vue 같은 JavaScript 프레임워크에서 익숙한 "스코프 슬롯" 개념은 컴포넌트 내 속성이나 메서드에 접근합니다. Laravel에서는 컴포넌트 내에 공개 메서드나 속성을 만들고, 슬롯 내에 `$component` 변수로 접근하여 비슷한 기능을 구현할 수 있습니다:

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

슬롯에도 컴포넌트 [속성](#component-attributes)과 같이 클래스 같은 추가 HTML 속성을 지정할 수 있습니다:

```blade
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

슬롯 속성을 다루려면 슬롯 변수의 `attributes` 속성에 접근할 수 있습니다:

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

아주 작은 컴포넌트는 클래스와 뷰 파일을 분리하는 대신 `render` 메서드에서 바로 컴포넌트 뷰 마크업을 반환할 수 있습니다:

```php
/**
 * 컴포넌트 뷰/내용 반환
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
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

인라인 뷰 컴포넌트를 만들려면 `make:component` 명령에 `--inline` 옵션을 추가하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트 (Dynamic Components)

컴포넌트를 동적으로 렌더링하려면, 뷰에서 `dynamic-component` 컴포넌트를 사용할 수 있습니다. 렌더링할 컴포넌트 이름을 런타임에 결정할 수 있습니다:

```blade
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록 (Manually Registering Components)

> [!WARNING]
> 아래 내용은 주로 패키지 개발자가 Blade 컴포넌트를 포함시킬 때 해당됩니다. 일반 애플리케이션 개발자에겐 필요하지 않을 수 있습니다.

자신의 애플리케이션에서는 `app/View/Components` 및 `resources/views/components` 디렉터리를 자동 스캔하지만, 비표준 위치나 패키지 컴포넌트는 직접 등록해야 Laravel이 컴포넌트를 알 수 있습니다. 보통 서비스 프로바이더 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록 후 다음처럼 렌더링합니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

또는 `componentNamespace` 메서드를 사용해 자동 로딩도 가능합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이 경우 `package-name::` 네임스페이스 문법으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 클래스를 자동 감지하며, 하위 디렉터리도 점 표기법을 지원합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 비슷하게 익명 컴포넌트는 단일 뷰 파일로 컴포넌트를 관리하지만, 클래스는 없습니다. 익명 컴포넌트는 `resources/views/components` 내에 Blade 템플릿만 두면 됩니다. 예를 들어 `resources/views/components/alert.blade.php`라면 다음처럼 호출합니다:

```blade
<x-alert/>
```

컴포넌트가 하위 폴더에 있는 경우 `.`를 사용해 경로를 나타냅니다. 예를 들어 `resources/views/components/inputs/button.blade.php`는:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트 (Anonymous Index Components)

컴포넌트가 여러 Blade 템플릿으로 이루어져 있을 때는 하나의 디렉터리에 모아서 관리할 수 있습니다. 예를 들어 "accordion" 컴포넌트는:

```none
/resources/views/components/accordion.blade.php
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

하지만 `x-accordion`으로 렌더링하려면 최상위 템플릿(`accordion.blade.php`)을 `resources/views/components` 디렉터리에 둬야 했습니다.

Blade는 컴포넌트 디렉터리 내에 `index.blade.php`를 둘 수 있게 해, 이 파일이 "루트" 컴포넌트로 렌더링되도록 지원합니다. 따라서 다음처럼 구조를 만들 수 있습니다:

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

같은 구조로 이전처럼 `x-accordion` 컴포넌트를 사용할 수 있습니다.

<a name="data-properties-attributes"></a>
### 데이터 속성 / 어트리뷰트 (Data Properties / Attributes)

익명 컴포넌트는 클래스가 없기 때문에, 어떤 데이터가 변수로 전달되고 어떤 속성이 속성 가방에 들어갈지 구분이 필요합니다. 이때 `@props` 디렉티브를 컴포넌트 Blade 템플릿 상단에 작성합니다. 기본값을 지정하려면 배열 키에 변수명, 값에 기본값을 추가하세요:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

정의한 컴포넌트를 다음처럼 호출할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근하기 (Accessing Parent Data)

자식 컴포넌트 내부에서 부모 컴포넌트의 데이터를 접근할 때는 `@aware` 디렉티브를 사용합니다. 예를 들어 복잡한 메뉴 컴포넌트에서:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 `<x-menu>` 컴포넌트:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

부모에 전달된 `color`는 기본적으로 자식 `<x-menu.item>`에 전달되지 않지만, `@aware` 디렉티브를 쓰면 가능해집니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware`는 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터만 접근할 수 있습니다. `@props`에 기본값으로만 지정된 데이터는 불가능합니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로 (Anonymous Component Paths)

익명 컴포넌트는 기본적으로 `resources/views/components` 디렉터리에 있습니다. 하지만 다른 디렉터리를 추가 등록할 수 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자로 컴포넌트의 디렉터리 경로, 옵션으로 두 번째 인자로 네임스페이스를 받습니다. 보통 서비스 프로바이더 `boot` 메서드에서 호출합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

네임스페이스 없이 등록한 경로의 컴포넌트는 접두어 없이 렌더링됩니다:

```blade
<x-panel />
```

네임스페이스를 지정하면 네임스페이스를 접두어로 붙여 사용합니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

렌더링 시:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성하기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃 (Layouts Using Components)

대부분 웹 애플리케이션은 여러 페이지가 동일 레이아웃을 공유합니다. 각 뷰에 전체 레이아웃 HTML을 반복해서 작성하기 어렵기 때문에, 공통 레이아웃을 하나의 [Blade 컴포넌트](#components)로 정의해 재사용합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의 (Defining The Layout Component)

예를 들어, "todo" 리스트 앱을 개발한다고 가정하면, 다음처럼 `layout` 컴포넌트를 정의할 수 있습니다:

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
#### 레이아웃 컴포넌트 적용 (Applying The Layout Component)

정의한 `layout` 컴포넌트를 사용하는 Blade 뷰를 작성할 수 있습니다. 예시로 작업 목록을 출력하는 뷰입니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

컴포넌트의 기본 슬롯 `$slot`에 콘텐츠가 전달됩니다. 레이아웃은 `$title` 슬롯도 받으며, 없으면 기본값이 표시됩니다. 다음과 같이 제목 슬롯도 전달할 수 있습니다:

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

라우트에서 뷰를 반환합니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃 (Layouts Using Template Inheritance)

<a name="defining-a-layout"></a>
#### 레이아웃 정의 (Defining A Layout)

레이아웃은 "템플릿 상속" 방식으로도 만들 수 있습니다. 컴포넌트 도입 전 주로 쓰이던 방식입니다.

간단 예제부터 보겠습니다. 페이지 레이아웃입니다:

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

`@section`은 콘텐츠 영역을 정의하고, `@yield`는 섹션 내용을 출력합니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장 (Extending A Layout)

자식 뷰는 `@extends` 디렉티브로 상속할 레이아웃을 지정합니다. 섹션에 내용 주입은 `@section`으로 작성하며, 상위 레이아웃의 `@yield` 위치에 포함됩니다:

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

`sidebar` 섹션에서 `@@parent` 디렉티브를 써서 상위 섹션 내용 뒤에 추가합니다. `@@parent`가 상위 섹션 내용으로 대체됩니다.

> [!NOTE]
> 이전 예제와 달리, 이 `sidebar` 섹션은 `@show`가 아니라 `@endsection`으로 끝납니다. `@endsection`는 섹션을 정의만 하며, `@show`는 즉시 출력까지 함께 합니다.

`@yield`는 두 번째 인자로 기본값을 받을 수 있으며 섹션이 없으면 기본값을 출력합니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드 (CSRF Field)

웹 폼에는 반드시 숨겨진 CSRF 토큰 필드를 포함해 [CSRF 보호](/docs/9.x/csrf) 미들웨어가 요청을 검증할 수 있게 해야 합니다. `@csrf` 디렉티브를 사용해 토큰 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드 (Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없으므로, 가짜 HTTP 메서드를 숨겨진 `_method` 필드로 지정해야 합니다. `@method` 디렉티브가 이 필드를 생성합니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검사 오류 (Validation Errors)

`@error` 디렉티브는 주어진 속성 관련 유효성 오류가 있는지 빠르게 점검할 수 있으며, 오류 메시지는 `$message` 변수로 출력합니다:

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

`@error`는 내부적으로 if문이고 `@else`도 쓸 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

여러 폼이 있는 페이지에선 [특정 에러 백](/docs/9.x/validation#named-error-bags) 이름을 두 번째 인수로 전달할 수 있습니다:

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
## 스택 (Stacks)

Blade에서는 이름 붙은 스택에 콘텐츠를 `push`할 수 있고, 다른 뷰나 레이아웃에서 그 스택 전체를 한꺼번에 렌더링할 수 있습니다. 자식 뷰에서 필요한 자바스크립트 포함에 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

불리언 조건이 참일 때만 `@push`하려면 `@pushIf` 디렉티브를 사용하세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에 여러 번 `push`해도 되고, 완료된 스택은 `@stack` 디렉티브로 렌더링합니다:

```blade
<head>
    <!-- 헤드 내용 -->

    @stack('scripts')
</head>
```

스택 앞에 내용을 추가하려면 `@prepend` 디렉티브를 씁니다:

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
## 서비스 주입 (Service Injection)

`@inject` 디렉티브는 Laravel [서비스 컨테이너](/docs/9.x/container)에서 서비스를 주입받습니다. 첫 번째 인자는 변수명, 두 번째 인자는 서비스 클래스나 인터페이스명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링 (Rendering Inline Blade Templates)

Blade 템플릿 문자열을 HTML로 변환해야 할 때 `Blade` 팩사드의 `render` 메서드를 사용하세요. 첫 번째 인자는 Blade 문자열, 두 번째 인자는 데이터 배열입니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉터리에 저장합니다. 렌더링 후 캐시된 파일을 삭제하려면, `deleteCachedView` 인자를 `true`로 설정하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 조각(fragment) 렌더링 (Rendering Blade Fragments)

[Turbo](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 이용할 때, Blade 템플릿의 일부 조각만 HTTP 응답으로 반환해야 할 경우가 있습니다. 이를 Blade "fragment"로 처리합니다.

템플릿에서 `@fragment` / `@endfragment`로 감싼 부분을 지정하세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

뷰를 렌더링할 때 `fragment` 메서드로 특정 조각만 반환하게 할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf`는 조건을 받아 조각 반환 여부를 결정합니다. 조건이 거짓이면 전체 뷰를 반환합니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`와 `fragmentsIf` 메서드는 여러 조각을 이어서 반환합니다:

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

Blade에 커스텀 디렉티브를 정의하려면 `directive` 메서드를 사용하세요. Blade 컴파일러가 해당 디렉티브를 만나면 콜백에 디렉티브 내 표현식이 전달됩니다.

예를 들어, `@datetime($var)`라는 디렉티브를 만들어 `$var`가 `DateTime` 인스턴스라고 가정하고 포맷팅하는 예제입니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     *
     * @return void
     */
    public function boot()
    {
        Blade::directive('datetime', function ($expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

위 코드는 전달된 식에 `format` 메서드를 호출하는 PHP 코드를 생성합니다. 즉 최종 PHP 코드는 다음과 같습니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브 로직을 수정한 후에는 모든 캐시된 Blade 뷰를 삭제해야 합니다. `view:clear` Artisan 명령을 사용하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러 (Custom Echo Handlers)

Blade는 객체를 출력할 때 해당 클래스의 `__toString` 메서드를 호출합니다. 그러나 외부 라이브러리 클래스처럼 `__toString`을 통제할 수 없을 때가 있습니다.

이 경우 `Blade::stringable` 메서드를 사용해 특정 클래스의 출력 방식을 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에 작성합니다:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

이제 Blade 템플릿에서 객체를 그냥 출력하면:

```blade
Cost: {{ $money }}
```

등록한 핸들러가 호출되어 원하는 형식으로 문자열화됩니다.

<a name="custom-if-statements"></a>
### 커스텀 If 문 (Custom If Statements)

커스텀 조건문을 복잡한 디렉티브로 만들기 복잡할 때, `Blade::if` 메서드를 사용해 간단하게 조건문을 정의할 수 있습니다.

예를 들어, 애플리케이션 기본 파일 시스템 디스크를 검사하는 커스텀 조건을 만들려면 `AppServiceProvider` 내에서 다음을 작성합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Blade::if('disk', function ($value) {
        return config('filesystems.default') === $value;
    });
}
```

이후 템플릿 내에서 다음과 같이 사용합니다:

```blade
@disk('local')
    <!-- 로컬 디스크 사용 시 -->
@elsedisk('s3')
    <!-- s3 디스크 사용 시 -->
@else
    <!-- 다른 디스크 -->
@enddisk

@unlessdisk('local')
    <!-- 로컬 디스크가 아닐 때 -->
@enddisk
```