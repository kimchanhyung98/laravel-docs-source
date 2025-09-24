# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시어(Directives)](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
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
    - [데이터 속성/특성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 빌드하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼(Forms)](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택(Stacks)](#stacks)
- [서비스 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장](#extending-blade)
    - [사용자 정의 에코 핸들러](#custom-echo-handlers)
    - [사용자 정의 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함된 단순하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade에서는 평범한 PHP 코드를 자유롭게 사용할 수 있습니다. 사실, 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되고 수정될 때까지 캐싱됩니다. 즉, Blade는 애플리케이션에 추가적인 부하를 거의 발생시키지 않습니다. Blade 템플릿 파일의 확장자는 `.blade.php`이며, 일반적으로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 글로벌 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 설명한 것처럼, `view` 헬퍼의 두 번째 인수를 사용해 Blade 뷰로 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 강화하기

Blade 템플릿으로 더욱 동적이고 현대적인 인터페이스를 손쉽게 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면, 일반적으로 React나 Vue와 같은 프론트엔드 프레임워크로만 가능했던 동적 기능을 갖춘 Blade 컴포넌트를 작성할 수 있습니다. 이로써 복잡한 빌드나 클라이언트 사이드 렌더링 없이, 현대적이고 반응성 있는 프론트엔드를 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 표시 (Displaying Data)

Blade 뷰로 전달된 데이터를 중괄호로 감싸서 화면에 표시할 수 있습니다. 예를 들어 다음과 같은 라우트가 있다면:

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
> Blade의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 자동 이스케이프 처리됩니다.

뷰로 전달한 변수뿐만 아니라, PHP 함수의 결과도 에코로 출력할 수 있습니다. 실제로, 원하는 모든 PHP 코드를 Blade 에코 구문에 사용할 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(그리고 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 원하지 않는 경우, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다:

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
#### 이스케이프 해제된 데이터 표시

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 자동 이스케이프 처리됩니다. 만약 데이터를 이스케이프 없이 출력하고 싶다면, 다음 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 에코로 출력할 때에는 매우 주의해야 합니다. 보통은 안전을 위해 이중 중괄호를 사용하는 이스케이프 방식을 사용하는 것이 좋습니다. (XSS 공격 예방)

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크가 "중괄호"를 사용해 브라우저에서 표현식을 렌더링합니다. 이럴 때 `@` 기호를 붙이면 해당 표현식을 Blade 엔진이 처리하지 않고 그대로 둘 수 있습니다. 예시:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예시에서 `@` 기호는 Blade에 의해 제거되지만, `{{ name }}` 표현식은 그대로 남아서 자바스크립트 프레임워크에서 렌더링될 수 있습니다.

`@` 기호는 Blade 지시어를 이스케이프하는 데에도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수를 초기화하기 위해 배열을 JSON으로 렌더링해야 할 때가 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이렇게 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 지시어를 쓸 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받으며, 결과 JSON이 HTML 인용부호 내에서 적절히 이스케이프되도록 보장합니다. 또한, 이 메서드는 JavaScript에서 객체나 배열을 올바른 객체로 변환하는 `JSON.parse` 문을 반환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션 스켈레톤에는 `Js` 파사드가 기본 포함되어 있어, Blade 템플릿에서 더욱 간편하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수를 JSON으로 렌더링할 때만 사용하세요. Blade 템플릿 엔진은 정규식 기반이므로, 복잡한 표현식을 지시어에 넘기려 하면 예상치 못한 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿의 큰 영역에 걸쳐 자바스크립트 변수를 표시해야 할 때는, 각각의 Blade 에코 구문마다 `@`를 붙이지 않고도, `@verbatim` 지시어로 해당 블록 전체를 감쌀 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시어 (Blade Directives)

템플릿 상속, 데이터 표시 외에도 Blade는 조건문, 반복문 등 일반적인 PHP 제어 구조를 위한 지시어를 제공합니다. 이러한 지시어는 PHP 문법과 매우 유사하며 간결하게 사용할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시어를 사용해 if 문을 작성할 수 있습니다. 이들 지시어는 PHP의 if 문과 동일하게 동작합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

더 간결하게 사용할 수 있는 `@unless` 지시어도 제공됩니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

이미 설명한 조건문 외에도, 각각의 PHP 함수에 대응하는 `@isset` 및 `@empty` 지시어를 사용할 수 있습니다:

```blade
@isset($records)
    // $records가 정의되어 있으며 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있음" 상태입니다...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 지시어

`@auth` 및 `@guest` 지시어를 사용하면 현재 사용자가 [인증](/docs/12.x/authentication)된 상태인지, 게스트인지 쉽게 확인할 수 있습니다:

```blade
@auth
    // 사용자가 인증되었습니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면, 인증 guard를 지정해 검사할 수도 있습니다:

```blade
@auth('admin')
    // 사용자가 인증되었습니다...
@endauth

@guest('admin')
    // 사용자가 인증되지 않았습니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경(Environment) 지시어

`@production` 지시어로 애플리케이션이 운영 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // 운영 환경 전용 콘텐츠...
@endproduction
```

또는, `@env` 지시어로 특정 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging" 또는 "production" 환경에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션 관련 지시어

템플릿 상속 섹션에 내용이 있는지 `@hasSection` 지시어로 확인할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없음을 확인하려면 `sectionMissing` 지시어를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션(Session) 지시어

`@session` 지시어를 사용하면 [세션](/docs/12.x/session) 값이 존재하는지 확인할 수 있습니다. 값이 존재하면, `@session` ~ `@endsession` 블록 내의 템플릿이 실행됩니다. `$value` 변수를 사용해 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트(Context) 지시어

`@context` 지시어를 사용하면 [컨텍스트](/docs/12.x/context) 값이 존재하는지 확인할 수 있습니다. 값이 존재하면, `@context` ~ `@endcontext` 블록 내의 템플릿이 실행됩니다. `$value` 변수를 사용해 컨텍스트 값을 출력할 수 있습니다:

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

Blade에서는 PHP 반복문 구조를 위한 간편한 지시어도 제공합니다. 이들 지시어는 PHP 반복문과 완전히 동일하게 동작합니다:

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
> `foreach` 루프에서 [루프 변수](#the-loop-variable)를 활용해, 현재 반복 중 첫 번째나 마지막 반복인지 등을 파악할 수 있습니다.

루프 안에서는 `@continue`와 `@break` 지시어를 사용해 반복을 건너뛰거나 종료할 수 있습니다:

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

또는, 조건문을 지시어 선언부에 포함시켜 더 간결하게 쓸 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 루프를 실행할 때는 `$loop` 변수가 자동으로 제공됩니다. 이 변수로 현재 인덱스, 반복 횟수, 첫/마지막 반복 여부 등 다양한 정보를 얻을 수 있습니다:

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

중첩 루프에서는 `parent` 속성으로 부모 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 주요 속성들은 다음과 같습니다:

<div class="overflow-auto">

| 속성                 | 설명                                                      |
| ------------------ | ------------------------------------------------------- |
| `$loop->index`     | 현재 반복의 인덱스(0부터 시작)                              |
| `$loop->iteration` | 현재 반복 횟수(1부터 시작)                                  |
| `$loop->remaining` | 남아있는 반복 횟수                                         |
| `$loop->count`     | 반복 대상 배열의 전체 갯수                                  |
| `$loop->first`     | 첫 번째 반복인지 여부                                      |
| `$loop->last`      | 마지막 반복인지 여부                                       |
| `$loop->even`      | 현재 반복이 짝수 반복인지 여부                              |
| `$loop->odd`       | 현재 반복이 홀수 반복인지 여부                              |
| `$loop->depth`     | 루프의 중첩 깊이                                           |
| `$loop->parent`    | 중첩 루프일 때, 부모의 `$loop` 변수                        |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 지시어는 조건에 따라 CSS 클래스를 동적으로 추가할 수 있는 문자열을 만듭니다. 각 배열의 키에 클래스명을 지정하고, 값에 조건식을 배정하면 됩니다. 만약 키가 숫자라면 항상 포함됩니다:

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

마찬가지로, `@style` 지시어를 사용하면 HTML 요소에 조건부 인라인 스타일을 추가할 수 있습니다:

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

체크박스 등의 HTML 입력 요소가 "checked" 상태인지 손쉽게 표기하려면 `@checked` 지시어를 사용할 수 있습니다. 조건이 `true`이면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

비슷하게, `@selected` 지시어로 select 옵션이 선택되었는지 표시할 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, `@disabled` 지시어로 요소의 "disabled" 상태를, `@readonly` 지시어로 "readonly" 상태를, `@required` 지시어로 "required" 상태를 조건에 따라 제어할 수 있습니다:

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
> `@include` 지시어 대신 [컴포넌트](#components) 사용을 권장합니다. 컴포넌트는 데이터/속성 바인딩 등 여러 장점이 있습니다.

Blade의 `@include` 지시어로, 다른 Blade 뷰를 포함할 수 있습니다. 부모 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에서도 사용할 수 있습니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함된 뷰에 추가 데이터를 전달하고 싶다면 배열을 넘길 수 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하려 하면 에러가 발생합니다. 뷰가 없을 수도 있을 때에는 `@includeIf` 지시어를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

특정 조건이 `true` 또는 `false`일 때만 뷰를 포함하려 한다면, `@includeWhen`, `@includeUnless` 지시어를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

지정한 여러 뷰 중 존재하는 첫 번째 뷰만 포함하고 싶다면, `includeFirst` 지시어를 쓸 수 있습니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서는 `__DIR__`, `__FILE__` 상수 사용을 피하세요. 이 값들은 캐시된 컴파일 뷰의 경로를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

Blade의 `@each` 지시어를 사용하면 반복문과 뷰 포함을 한 줄로 처리할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

여기서 첫 번째 인수는 반복마다 렌더링할 뷰 이름, 두 번째는 반복할 컬렉션, 세 번째는 뷰에서 사용할 변수명입니다. 컬렉션의 현재 키 값도 `key` 변수로 사용할 수 있습니다.

배열이 비어있을 때 대신 렌더링할 뷰를 네 번째 인수로 지정할 수도 있습니다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에서 부모 변수 사용이 필요하다면, `@foreach`와 `@include`를 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어를 사용하면, 해당 템플릿 영역을 렌더링 사이클당 한 번만 실행할 수 있습니다. 예를 들어, [스택](#stacks)을 이용해 자바스크립트를 페이지 헤더에 한 번만 추가하고 싶을 때 유용합니다. 예시로, [컴포넌트](#components)가 반복될 때 자바스크립트를 처음 렌더링하는 경우에만 헤더에 넣고 싶을 때 사용할 수 있습니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

`@once`가 자주 `@push` 혹은 `@prepend`와 함께 사용되므로, `@pushOnce`, `@prependOnce` 편의 지시어도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

특정 상황에서는 뷰 내에서 PHP 코드를 직접 실행할 수 있으면 편리합니다. Blade에서 `@php` 지시어로 순수 PHP 블록을 실행할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스만 임포트할 때에는 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

두 번째 인수로 별칭을 줄 수도 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

동일 네임스페이스의 여러 클래스를 한 번에 임포트할 수 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

함수, 상수도 `function`, `const` 접두사를 붙여 임포트할 수 있습니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

함수·상수 임포트 시에도 별칭 사용 가능:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수·상수 모두 그룹 임포트가 지원됩니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서는 뷰에 주석을 남길 수 있습니다. 이 주석은 최종 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 표시되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션·레이아웃·인클루드와 유사한 이점을 제공하지만, 컴포넌트/슬롯 방식이 더 직관적일 수 있습니다. 컴포넌트 작성 방식은 클래스 기반과 익명(anon) 방식 두 가지가 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용할 수 있습니다. 예시로, `Alert` 컴포넌트를 만들면 `app/View/Components` 디렉터리에 컴포넌트가 생성됩니다:

```shell
php artisan make:component Alert
```

이 명령은 뷰 템플릿도 함께 만듭니다. 뷰는 `resources/views/components`에 생성됩니다. 직접 만든 앱의 컴포넌트는 이 경로에서 자동으로 인식되므로 별도의 등록이 필요하지 않습니다.

서브디렉터리 안에 컴포넌트를 만들 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms`의 `Input` 컴포넌트와, `resources/views/components/forms` 뷰를 만듭니다.

클래스 없이 Blade 템플릿만 있는 익명 컴포넌트를 만들려면, `--view` 플래그를 사용합니다:

```shell
php artisan make:component forms.input --view
```

위 명령을 실행하면 `resources/views/components/forms/input.blade.php` 파일이 생성되며, `<x-forms.input />` 컴포넌트로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

직접 만든 앱의 컴포넌트는 자동으로 `app/View/Components`와 `resources/views/components` 경로에서 인식됩니다.

하지만 패키지 개발 시에는 컴포넌트 클래스 및 HTML 태그 별칭을 직접 등록해야 합니다. 패키지의 서비스 프로바이더 `boot` 메서드에서 등록하는 것이 일반적입니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후, 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는, `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 네이밍 규칙에 따라 자동 로드할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 있다면:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이제 다음과 같이 벤더 네임스페이스 형태로 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트명에서 파스칼 케이스 적용, 서브디렉터리와 도트 표기법도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 화면에 표시하려면 Blade 템플릿 내에 `x-`로 시작하는 컴포넌트 태그를 사용합니다. 컴포넌트 클래스명을 케밥 케이스로 변경해 사용합니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 더 깊이 중첩된 구조라면, `.` 문자를 사용해 디렉터리 구조를 나타냅니다. 예를 들어, `app/View/Components/Inputs/Button.php` 컴포넌트는 다음과 같이 렌더링합니다:

```blade
<x-inputs.button/>
```

컴포넌트 렌더링 조건을 제어하려면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트 렌더링 여부
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

여러 Blade 템플릿이 하나의 컴포넌트 그룹을 이룰 때, 관련 컴포넌트를 같은 디렉터리에 모아둘 수 있습니다. 예를 들어 "카드" 컴포넌트의 클래스 구조가 아래와 같다고 가정합니다:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트가 `Card` 디렉터리 안에 있으므로, `<x-card.card>`로 렌더링할 것이라 생각할 수 있습니다. 하지만, 파일명과 디렉터리명이 같을 때, Laravel은 이 컴포넌트를 "루트" 컴포넌트로 간주해 이름을 반복하지 않아도 됩니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달

HTML 속성으로 컴포넌트에 데이터를 전달할 수 있습니다. 하드코딩된 값은 그대로 속성 문자열로, PHP 표현식·변수는 `:`을 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 데이터 속성(인수)을 정의해야 합니다. 컴포넌트의 모든 public 속성은 자동으로 뷰에서 사용 가능합니다. `render` 메서드 내에서 별도 전달할 필요는 없습니다:

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
     * 컴포넌트의 뷰/내용 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, public 변수의 값을 뷰에서 이름 그대로 에코로 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이스 표기법

컴포넌트 생성자 인수는 `camelCase`로 작성합니다. HTML 속성에서는 `kebab-case`를 사용해야 합니다. 예를 들어 아래와 같이 생성자에 정의되어 있다면:

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

Blade에서는 다음과 같이 쓸 수 있습니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 속성 축약 표기법

컴포넌트에 속성을 전달할 때 "축약 표기"를 쓸 수 있습니다. 보통 변수명과 속성명이 일치할 때 편리합니다:

```blade
{{-- 축약 표기법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JS 프레임워크는 콜론 접두 속성을 사용하므로, Blade에서 속성 앞에 더블 콜론(`::`)을 붙여 PHP 표현식이 아님을 표시할 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

렌더링 결과:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서 public 변수뿐만 아니라, public 메서드도 호출할 수 있습니다. 예시로, `isSelected` 메서드가 있을 경우:

```php
/**
 * 주어진 옵션이 선택된 상태인지 판별
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

컴포넌트 템플릿에서 다음과 같이 메서드를 호출할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성·슬롯 접근

컴포넌트 이름, 속성, 슬롯 정보에 접근하려면, `render` 메서드에서 클로저를 반환하면 됩니다:

```php
use Closure;

/**
 * 컴포넌트의 뷰/내용 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

클로저는 `$data` 배열을 인자로 받을 수 있습니다. 이 배열은 다음과 같은 컴포넌트 관련 정보를 담고 있습니다:

```php
return function (array $data) {
    // $data['componentName']
    // $data['attributes']
    // $data['slot']

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열을 그대로 Blade 문자열 내에 임베드해서는 안 됩니다. 악의적인 속성 값이 공격에 이용될 수 있습니다.

`componentName`은 `x-` 접두어 이후 등장하는 태그명과 같습니다. 즉, `<x-alert />`의 `componentName`은 `alert`가 됩니다. `attributes`는 해당 태그에 전달된 모든 속성, `slot`은 슬롯의 컨텐츠(`Illuminate\Support\HtmlString` 인스턴스)입니다.

클로저는 문자열을 반환해야 하며, 이 문자열이 뷰 이름과 일치하면 해당 뷰를 렌더링하고, 그렇지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트가 Laravel [서비스 컨테이너](/docs/12.x/container)의 의존성을 필요로 할 경우, 생성자에서 데이터 속성 앞에 의존성 타입을 나열하면 자동으로 주입됩니다:

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

일부 public 메서드나 속성을 컴포넌트 템플릿에 노출하고 싶지 않다면, `$except` 배열 속성에 해당 이름을 추가하세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출되지 않을 속성/메서드 배열
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

앞서 데이터 속성을 컴포넌트로 전달하는 법을 배웠습니다. 하지만 CSS 클래스 등 부가 HTML 속성이 컴포넌트 기능과 직접 관련 없을 때도 있습니다. 이런 추가 속성들은 컴포넌트 "속성 백(Attributes Bag)"에 자동으로 담겨 `$attributes` 변수로 템플릿에서 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

컴포넌트 생성자에 없는 속성들은 `$attributes` 변수로 템플릿에서 사용할 수 있으며, 해당 변수를 출력하면 속성이 모두 렌더링됩니다:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내에 `@env` 등 디렉티브 사용은 지원되지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합 속성

속성의 기본값을 지정하거나, 추가 값을 기존 속성에 병합해야 할 수도 있습니다. 이럴 땐 속성 백의 `merge` 메서드를 사용하세요. 주로 기본 CSS 클래스 지정 등에 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

다음처럼 사용할 경우:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더링된 HTML은 다음과 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건이 참일 때만 클래스를 병합하려면 `class` 메서드를 사용할 수 있습니다. 배열의 키는 클래스명, 값은 조건식이며, 숫자 키는 무조건 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

추가 속성 병합이 필요하다면, `class` 호출 뒤에 `merge`를 체이닝할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 속성 병합이 필요 없는 HTML 요소에 조건부 클래스를 컴파일하려면 [@class 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class` 외 속성을 병합할 땐, `merge` 메서드에 전달한 값이 속성의 "기본값"이 됩니다. 단, `class`와는 달리 injected 속성 값과 합쳐지지 않고, 덮어씁니다. 다음처럼 사용합니다:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

사용 시에만 custom `type`을 지정해주고, 없으면 기본값으로 `button`이 됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```

랜더링 결과:

```blade
<button type="submit">
    Submit
</button>
```

`class` 외에도 injected 값과 기본값을 합쳐주고 싶으면, `prepends` 메서드를 사용하세요. 예를 들어, `data-controller` 속성에서 기본값을 항상 앞에 붙이고 싶을 때:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드로 속성을 필터링할 수 있습니다. 클로저 반환값이 true면 해당 속성이 속성 백에 남습니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

특정 문자열로 시작하는 속성만 가져오고 싶을 때 `whereStartsWith`를 사용합니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, 특정 문자열로 시작하지 않는 속성만 가져오려면 `whereDoesntStartWith`를 사용합니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 속성 백에서 첫 번째 속성을 출력할 수도 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

해당 속성이 있는지 확인하려면 `has` 메서드를 사용합니다. 인수로 속성명을 넣으면, 존재 여부에 따라 boolean을 반환합니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

배열로 여러 속성 확인도 가능합니다. 모두 존재해야 true를 반환합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny` 메서드는 지정한 속성 중 하나라도 있으면 true를 반환합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

`get` 메서드로 단일 속성 값을, `only`·`except` 메서드로 일부 속성만 가져오거나, 몇 개를 제외한 나머지 속성을 가져올 수 있습니다:

```blade
{{ $attributes->get('class') }}

{{ $attributes->only(['class']) }}

{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어

기본적으로, 블레이드 내부에서 컴포넌트 렌더링에 사용되는 예약어가 있습니다. 다음 키워드는 컴포넌트의 public 속성, 메서드명으로 사용할 수 없습니다:

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
### 슬롯(Slots)

컴포넌트에 추가적인 콘텐츠를 "슬롯"을 통해 전달할 수 있습니다. 슬롯 내용은 `$slot` 변수로 렌더링됩니다. 예를 들어 `alert` 컴포넌트가 다음과 같다고 가정합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

아래처럼 컴포넌트에 콘텐츠를 삽입해 전달할 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 위치에 각각 다른 슬롯을 렌더링해야 한다면, 명명된 슬롯(named slot)을 지원할 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯 내용은 `x-slot` 태그로 정의합니다. 명시적으로 `x-slot` 태그 안에 있지 않은 콘텐츠는 기본 슬롯(`$slot`)에 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 비어 있는지 확인하려면, 슬롯의 `isEmpty` 메서드를 사용할 수 있습니다:

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

실제 콘텐츠(HTML 주석 제외)가 있는지 확인하려면, `hasActualContent` 메서드를 사용할 수 있습니다:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯(Scoped Slots)

Vue 등 JS 프레임워크처럼, 슬롯에서 컴포넌트의 데이터나 메서드에 접근할 수 있습니다. 컴포넌트에 public 속성/메서드를 정의하고, 슬롯에서 `$component` 변수로 접근하면 됩니다. 예를 들어, `x-alert` 컴포넌트에 public `formatAlert` 메서드가 있다면:

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

슬롯에도 [속성](#component-attributes)을 부여할 수 있습니다(예: CSS 클래스):

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

슬롯 속성은 슬롯의 변수에서 `attributes` 속성으로 접근할 수 있습니다. 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

아주 작거나 단순한 컴포넌트의 경우, 클래스와 뷰 파일을 따로 만들기 번거로울 수 있습니다. 이런 경우 `render` 메서드에서 직접 마크업을 문자열로 반환할 수 있습니다:

```php
/**
 * 컴포넌트의 뷰/내용 반환
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

인라인 뷰를 렌더링하는 컴포넌트를 만들려면 `make:component` 명령어에 `--inline` 옵션을 추가하면 됩니다:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

런타임 시점에 렌더링할 컴포넌트가 결정되는 경우가 있습니다. 이럴 땐 Laravel의 내장 `dynamic-component` 컴포넌트를 사용할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래 컴포넌트 수동 등록 문서는 주로 Laravel 패키지로 뷰 컴포넌트를 제공할 때 적용됩니다. 패키지 개발이 아니라면 해당 내용은 필요하지 않을 수 있습니다.

직접 만든 앱의 컴포넌트는 앞서 설명한 기본 경로에서 자동 감지됩니다.

하지만 패키지 제작 또는 비표준 경로에 컴포넌트를 둘 경우, 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 패키지 서비스 프로바이더의 `boot` 메서드에서 등록하는 게 일반적입니다:

```php
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

등록 후, 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

네이밍 규칙에 따라 자동 로딩을 하고 싶다면, `componentNamespace` 메서드를 사용할 수 있습니다. (`Nightshade` 패키지 예시 참조)

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

벤더 네임스페이스(`<x-nightshade::calendar />` 등)로 컴포넌트를 사용할 수 있습니다. Blade가 컴포넌트 이름을 파스칼 케이스로 변환해 해당 클래스를 찾아줍니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트처럼, 익명 컴포넌트를 통해 하나의 파일만으로 컴포넌트 관리를 할 수 있습니다. 익명 컴포넌트는 Blade 뷰 파일만 필요하며, 별도의 클래스는 없습니다. 예를 들어, `resources/views/components/alert.blade.php` 파일이 있다면, 아래와 같이 쉽게 사용할 수 있습니다:

```blade
<x-alert/>
```

컴포넌트가 더 깊이 중첩된 디렉터리에 있다면 `.` 문자를 사용합니다. 예를 들어, `resources/views/components/inputs/button.blade.php`라면:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

여러 Blade 템플릿이 하나의 컴포넌트 그룹을 이룰 때, 해당 템플릿을 한 디렉터리에 모아두고 싶을 수 있습니다. 예를 들어 "아코디언" 컴포넌트의 디렉터리 구조가 다음과 같다고 가정합니다:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 하면 다음과 같이 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 `x-accordion`을 사용하려면, "인덱스"용 아코디언 템플릿을 최상위 디렉터리에 둬야 했습니다.

Blade에서는 디렉터리명과 동일한 이름의 파일을 디렉터리 안에 둘 수 있으며, 이 파일이 "루트" 컴포넌트로 사용됩니다. 즉, 디렉터리 구조를 아래와 같이 바꿔도 동일하게 사용할 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성/특성

익명 컴포넌트에는 클래스가 없으므로, 어떤 데이터가 변수로 전달되고 어떤 속성이 attribute bag에 담기는지 명확하지 않을 수 있습니다. 컴포넌트 템플릿 상단에서 `@props` 지시어로 변수를 선언하면, 나머지 속성은 attribute bag으로 들어갑니다. 기본값은 배열 형태로 지정할 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이 컴포넌트는 다음처럼 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

하위 컴포넌트에서 부모 컴포넌트의 데이터를 활용하고 싶을 때, `@aware` 지시어를 사용할 수 있습니다. 예를 들어, 아래와 같이 부모 `<x-menu>`와 자식 `<x-menu.item>`이 있습니다:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모 컴포넌트(`x-menu`)는 다음과 같이 구현한다고 할 때:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

부모에만 전달된 `color` prop이 하위 아이템에서도 필요하다면, 자식 컴포넌트에서 `@aware` 지시어를 사용할 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시어는 부모에 HTML 속성으로 명시적으로 전달된 데이터만 접근 가능합니다. 단순 `@props` 기본값은 자식에서 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 설명했듯, 익명 컴포넌트는 기본적으로 `resources/views/components`에 파일을 둡니다. 그러나 추가적인 컴포넌트 경로를 등록하고 싶은 경우, `anonymousComponentPath` 메서드로 할 수 있습니다.

첫 인수는 컴포넌트 위치의 "경로", 두 번째 인수는 컴포넌트 네임스페이스 지정입니다. 일반적으로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출하면 됩니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

별도의 prefix 없이 등록했다면, Blade에서 prefix 없이 사용할 수 있습니다. 예를 들어 위 경로에 `panel.blade.php`가 있다면:

```blade
<x-panel />
```

두 번째 인수로 prefix "네임스페이스"를 지정할 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이 경우, 네임스페이스를 컴포넌트 이름에 붙여 사용합니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 빌드하기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 앱은 여러 페이지에서 동일한 레이아웃을 유지합니다. 모든 뷰마다 전체 레이아웃 HTML을 반복 작성하면 비효율적이므로, [Blade 컴포넌트](#components)로 레이아웃을 한 번 정의하고 전체 앱에 재사용하는 것이 효율적입니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "todo" 리스트 앱을 만든다고 가정할 때, 다음과 같은 방식으로 `layout` 컴포넌트를 만들 수 있습니다:

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

`layout` 컴포넌트를 정의한 후, 이 컴포넌트를 사용하는 Blade view를 만들 수 있습니다. 예를 들어 간단한 할 일 리스트 뷰를 만들면:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트로 전달한 콘텐츠는 컴포넌트의 기본 `$slot` 변수로 전달됩니다. 또한, `$title` 슬롯이 제공되면 해당 값이, 없으면 기본 타이틀이 출력됩니다. 할 일 리스트 뷰에서 다음과 같이 커스텀 타이틀도 삽입할 수 있습니다([컴포넌트 문서](#components) 참고):

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

모든 설정이 끝나면 라우트에서 해당 뷰만 반환하면 됩니다:

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

레이아웃은 "템플릿 상속" 방식으로도 만들 수 있습니다. 이 방식은 [컴포넌트](#components)가 도입되기 전 Blade에서 레이아웃 사용의 표준 방식이었습니다.

간단한 예제를 살펴보겠습니다. 먼저, 가장 상위 레이아웃 파일을 정의합니다. 일반적으로 앱 전체가 공통적으로 사용하는 HTML 구조를 정의합니다:

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

`@section`은 콘텐츠 영역을 정의하며, `@yield`는 해당 영역의 실제 콘텐츠를 표시합니다.

이제 이 레이아웃을 상속하는 하위 페이지를 만듭니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

하위 뷰에서는 Blade의 `@extends` 지시어로 어느 레이아웃을 상속받을지 지정합니다. 그리고 `@section` 지시어로 상위 레이아웃에서 정의한 콘텐츠 섹션에 내용을 삽입할 수 있습니다:

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

위 예시에서 `sidebar` 섹션은 `@@parent` 지시어를 사용해 상위 레이아웃의 sidebar에 내용을 추가(append)합니다. `@@parent`는 렌더링 시 상위 레이아웃 내용으로 대체됩니다.

> [!NOTE]
> 위 예제와 달리, 이 `sidebar` 섹션은 `@show`로 끝나지 않고 `@endsection`으로 종료됩니다. `@endsection`은 해당 영역을 **정의만** 하고, `@show`는 **정의와 동시에 즉시 출력**까지 수행합니다.

`@yield`는 두 번째 인수로 기본값을 줄 수 있습니다. 해당 섹션이 미정의일 때 기본값이 출력됩니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때는 반드시 숨겨진 CSRF 토큰 필드를 포함해야 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있습니다. Blade의 `@csrf` 지시어로 토큰 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없습니다. 이는 숨겨진 `_method` 필드를 통해 HTTP 메서드를 스푸핑(spoof)하여 해야 하며, `@method` Blade 지시어가 이 역할을 해줍니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 지시어를 사용하면, 주어진 속성에 대한 [유효성 검증 오류 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors) 존재 여부를 쉽게 확인할 수 있습니다. `@error` 블록 내에서는 `$message` 변수로 에러 메시지를 출력할 수 있습니다:

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

`@error`는 내부적으로 "if" 문으로 컴파일되기 때문에, `@else`를 조합해 에러가 없을 때 다른 내용을 렌더링할 수도 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

페이지에 여러 폼이 있을 때, [특정 에러 백](/docs/12.x/validation#named-error-bags)에 대해 두 번째 인수로 에러백 이름을 지정할 수 있습니다:

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

Blade에서는 여러 뷰/레이아웃 사이에서 나중에 한 번에 렌더링할 수 있는 스택(stack)에 콘텐츠를 "푸시"할 수 있습니다. 주로 자식 뷰에서 필요한 자바스크립트 라이브러리 지정용으로 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

조건이 true일 때만 push하려면 `@pushIf`를 사용할 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

하나의 스택에 여러 번 push할 수 있습니다. 누적 내용을 출력하려면 해당 스택 이름을 `@stack` 지시어에 전달하세요:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택 앞부분에 내용을 삽입하고 싶다면, `@prepend`를 사용하세요:

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
## 서비스 주입

`@inject` 지시어를 사용하면 Laravel [서비스 컨테이너](/docs/12.x/container)에서 서비스를 주입받을 수 있습니다. 첫 번째 인수는 뷰에서 사용할 변수명, 두 번째 인수는 클래스/인터페이스명입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 블레이드 템플릿 렌더링

원시 Blade 템플릿 문자열을 HTML로 변환해야 할 일이 있을 때, `Blade` 파사드의 `render` 메서드를 사용할 수 있습니다. 이 메서드는 Blade 템플릿 문자열과, 뷰에 전달할(선택) 데이터 배열을 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉터리에 저장합니다. 렌더 후 임시 파일 자동 삭제를 원하면, `deleteCachedView` 인수를 메서드에 추가하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## 블레이드 프래그먼트 렌더링

[Tubro](https://turbo.hotwired.dev/) 나 [htmx](https://htmx.org/) 등 프론트엔드 프레임워크를 사용할 때, HTTP 응답으로 Blade 템플릿의 일부만 반환하고 싶을 수도 있습니다. Blade "프래그먼트"로 이것이 가능합니다. 먼저, Blade 템플릿 내에서 특정 영역을 `@fragment` ~ `@endfragment`로 감쌉니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이 뷰를 렌더링할 때, `fragment` 메서드로 어느 프래그먼트만 포함할지 지정할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 조건부로 프래그먼트만 또는 전체 뷰를 반환할 수 있습니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`, `fragmentsIf` 메서드로 여러 프래그먼트를 한 번에 반환할 수도 있습니다. 여러 프래그먼트가 연결되어 응답으로 전달됩니다:

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
## 블레이드 확장 (Extending Blade)

Blade에서는 `directive` 메서드로 직접 커스텀 지시어를 정의할 수 있습니다. Blade 컴파일러가 사용자의 지시어를 만나면, expression을 인자로 콜백을 실행합니다.

아래 예시는 `@datetime($var)` 지시어를 만들어, 주어진 `$var`(DateTime 인스턴스)를 포맷팅합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 추가 애플리케이션 서비스 등록
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

즉, 지시어에 넘긴 expression에 `format`이 연결된 PHP 코드를 생성합니다. 예를 들어:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 지시어 로직을 수정한 후에는 모든 캐시된 Blade 뷰를 삭제해야 합니다. `view:clear` Artisan 명령어로 캐시를 지울 수 있습니다.

<a name="custom-echo-handlers"></a>
### 사용자 정의 에코 핸들러

Blade에서 객체를 "echo"할 때는 객체의 `__toString` 메서드가 호출됩니다. 하지만 어떤 경우(서드파티 클래스 등) `__toString`을 직접 제어할 수 없을 수 있습니다.

이럴 때는 Blade의 `stringable` 메서드로 해당 객체 타입의 에코 핸들러를 등록할 수 있습니다. 이 메서드는 클로저를 받으며, 전달받는 타입을 명시해야 합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 등록합니다:

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

핸들러 등록 후에는 Blade 템플릿에서 해당 객체를 그대로 출력할 수 있습니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 사용자 정의 If 문

지시어를 직접 만드는 것보다, 간단한 조건문은 Blade의 `Blade::if` 메서드로 커스텀 if 지시어를 만들 수 있습니다. 예를 들어, 앱이 어떤 디스크를 기본값으로 사용하는지 확인하고 싶다면 아래처럼 정의할 수 있습니다. `AppServiceProvider`의 `boot` 메서드에서 사용하세요:

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

정의된 커스텀 조건문은 다음처럼 템플릿에서 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크를 사용 -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크를 사용 -->
@else
    <!-- 다른 디스크를 사용 -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크가 아님 -->
@enddisk
```
