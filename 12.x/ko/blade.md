# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 확장하기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 디렉티브](#blade-directives)
    - [If문](#if-statements)
    - [Switch문](#switch-statements)
    - [루프](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [원시 PHP](#raw-php)
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
    - [데이터 속성/속성(attribute)](#data-properties-attributes)
    - [상위 데이터에 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 만들기](#building-layouts)
    - [컴포넌트로 레이아웃 구성](#layouts-using-components)
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
    - [커스텀 If문](#custom-if-statements)

<a name="introduction"></a>
## 소개

블레이드(Blade)는 라라벨에서는 기본적으로 제공되는 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿 내에서 평범한 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실, 모든 블레이드 템플릿은 순수 PHP 코드로 컴파일되어, 수정이 있을 때까지 캐시됩니다. 즉, 블레이드는 애플리케이션에 실질적으로 아무런 오버헤드도 추가하지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉터리에 저장됩니다.

블레이드 뷰는 전역 `view` 헬퍼를 사용해서 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 언급했듯이, `view` 헬퍼의 두 번째 인수를 통해 블레이드 뷰로 데이터를 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 확장하기

블레이드 템플릿을 한 단계 더 발전시켜, 쉽게 동적 인터페이스를 만들고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면, 리액트(React)나 뷰(Vue)와 같은 프런트엔드 프레임워크에서만 가능했던 동적 기능을, Blade 컴포넌트로 작성할 수 있습니다. 즉, 복잡한 빌드 과정이나 클라이언트 사이드 렌더링 없이도, 최신 반응형 프런트엔드를 쉽게 구현할 수 있는 좋은 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시하기

블레이드 뷰에 전달된 데이터를 중괄호로 감싸서 출력할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해 봅시다.

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 값을 다음과 같이 출력할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> 블레이드의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 처리됩니다.

뷰에 전달된 변수의 값만 출력할 수 있는 것이 아닙니다. PHP 함수의 반환값도 출력할 수 있습니다. 실제로 블레이드 에코 구문 내에 어떤 PHP 코드든 넣을 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 블레이드(그리고 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩(double encode)합니다. 이 이중 인코딩을 사용하지 않으려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

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

블레이드의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 처리됩니다. 만약 데이터를 이스케이프하지 않고 그대로 출력하고 싶다면 다음과 같이 작성합니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공한 내용을 그대로 출력할 때는 특히 주의해야 합니다. 사용자 입력 데이터를 화면에 표시할 때는 XSS 공격을 막기 위해 이스케이프된 중괄호 구문(`{{ }}`)을 기본적으로 사용하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크 또한 브라우저 상에서 표현식을 표시할 때 중괄호를 사용합니다. 이때 블레이드에서는 중괄호 앞에 `@` 기호를 붙이면, 해당 표현식을 블레이드 엔진이 건드리지 않도록 할 수 있습니다. 예를 들어,

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예제에서는 블레이드가 `@` 기호만 제거하고, `{{ name }}` 표현식은 그대로 남기므로, 자바스크립트 프레임워크가 해당 표현식을 렌더링할 수 있습니다.

또한, 블레이드 디렉티브를 이스케이프하려면, `@` 기호를 사용하면 됩니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링하기

때로는 배열을 뷰로 전달한 뒤, JavaScript 변수를 초기화하기 위해 JSON 형태로 렌더링하고자 할 수 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

하지만 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 같은 인수를 전달받으며, 결과로 생성된 JSON이 HTML 인용부호 내에서도 안전하도록 적절히 이스케이프 처리됩니다. `from` 메서드는 주어진 객체나 배열을 JavaScript에서 사용할 수 있는 올바른 객체로 변환할 `JSON.parse` 구문을 반환합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 버전의 라라벨 기본 애플리케이션에는 이 기능을 더욱 쉽게 사용할 수 있는 `Js` 파사드가 포함되어 있습니다. 따라서 블레이드 템플릿 내에서 아래와 같이 사용할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> 이미 존재하는 변수를 JSON으로 렌더링할 때만 `Js::from` 메서드를 사용해야 합니다. 블레이드 템플릿 엔진은 정규표현식을 이용해 파싱되므로, 복잡한 표현식을 전달하면 예기치 않은 동작이 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 상당 부분에서 자바스크립트 변수를 표현해야 하는 경우, 모든 블레이드 에코 구문 앞에 `@` 기호를 붙이지 않고도, 해당 HTML 영역 전체를 `@verbatim` 디렉티브로 감싸면 됩니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 디렉티브

블레이드는 템플릿 상속 및 데이터 표시 외에도, if문, 루프문 등 PHP의 자주 쓰이는 제어 구조를 위한 편리한 단축 구문을 제공합니다. 이 단축 구문들은 PHP의 해당 구문과 친숙한 형태를 유지하면서도, 더 깔끔하고 간결하게 사용할 수 있도록 도와줍니다.

<a name="if-statements"></a>
### If문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 이용하여 if문을 만들 수 있습니다. 이 디렉티브들은 PHP에서의 if문과 동일하게 동작합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의상, 블레이드에서는 `@unless` 디렉티브도 제공합니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

앞서 설명한 조건문 디렉티브 외에도, 각각 PHP의 `isset`, `empty` 함수에 대응하는 `@isset`, `@empty` 디렉티브를 사용할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있음" 상태입니다...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브를 사용하면, 현재 사용자가 [인증](/docs/12.x/authentication)된 상태인지 혹은 게스트인지를 빠르게 확인할 수 있습니다.

```blade
@auth
    // 사용자가 인증되었습니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면, `@auth` 및 `@guest` 디렉티브 사용 시 확인할 인증 가드를 직접 지정할 수도 있습니다.

```blade
@auth('admin')
    // 사용자가 인증되었습니다...
@endauth

@guest('admin')
    // 사용자가 인증되지 않았습니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경 디렉티브

`@production` 디렉티브를 이용하여 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다.

```blade
@production
    // 프로덕션 전용 콘텐츠...
@endproduction
```

또는, `@env` 디렉티브를 사용해서 애플리케이션이 특정 환경에서 실행 중인지 확인할 수도 있습니다.

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging" 또는 "production" 환경에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션 디렉티브

템플릿 상속에서 특정 섹션이 내용이 있는지 확인하려면 `@hasSection` 디렉티브를 사용할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없을 경우 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 디렉티브

`@session` 디렉티브는 [세션](/docs/12.x/session) 값이 존재하는지 확인할 때 사용할 수 있습니다. 세션 값이 있을 경우, `@session` ~ `@endsession` 사이의 템플릿 내용이 렌더링됩니다. 이때 `$value` 변수를 통해 세션 값을 바로 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용하여 switch문을 만들 수 있습니다.

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
### 루프

조건문 외에도, 블레이드는 PHP 루프 구문을 위한 간단한 디렉티브를 제공합니다. 각 디렉티브는 PHP의 대응 구문과 동일하게 동작합니다.

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
> `foreach` 루프를 도는 동안, [루프 변수](#the-loop-variable)를 사용해서 현재 반복이 처음인지, 마지막인지 등 루프에 대한 정보를 얻을 수 있습니다.

루프 내에서 `@continue`와 `@break` 디렉티브를 이용해 현재 반복을 건너뛰거나, 루프를 종료할 수도 있습니다.

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

또, continue나 break 조건을 디렉티브에 직접 명시해서 좀 더 간결하게 작성할 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 루프 내에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수는 현재 루프 인덱스, 첫 번째/마지막 반복 여부 등 다양한 정보를 제공합니다.

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

중첩 루프일 때는, `parent` 속성을 통해 상위 루프의 `$loop` 변수에 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에는 다음과 같은 다양한 속성이 포함되어 있습니다.

<div class="overflow-auto">

| 속성                | 설명                                                        |
| ------------------ | ---------------------------------------------------------- |
| `$loop->index`     | 현재 반복의 인덱스(0부터 시작)                               |
| `$loop->iteration` | 현재 반복 번호(1부터 시작)                                   |
| `$loop->remaining` | 앞으로 남은 반복 횟수                                       |
| `$loop->count`     | 전체 반복 횟수 (배열 원소 개수)                             |
| `$loop->first`     | 현재가 첫 번째 반복인지 여부                                 |
| `$loop->last`      | 현재가 마지막 반복인지 여부                                  |
| `$loop->even`      | 짝수 번째 반복인지 여부                                      |
| `$loop->odd`       | 홀수 번째 반복인지 여부                                      |
| `$loop->depth`     | 현재 루프의 중첩 레벨                                       |
| `$loop->parent`    | 중첩 루프일 경우, 상위 루프의 loop 변수                    |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일

`@class` 디렉티브는 CSS 클래스 문자열을 조건에 따라 컴파일할 때 사용합니다. 클래스를 배열로 전달하며, 배열의 키에는 추가할 클래스명(들), 값에는 true/false로 평가되는 조건식을 지정합니다. 배열의 키가 숫자일 경우, 그 클래스는 언제나 렌더링 결과에 포함됩니다.

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

비슷하게, `@style` 디렉티브를 이용하면 HTML 요소에 인라인 스타일도 조건에 따라 추가할 수 있습니다.

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

체크박스 등 HTML 요소의 속성을 간편하게 지정하고 싶을 때는 `@checked` 디렉티브를 사용할 수 있습니다. 지정한 조건이 참일 경우 `checked`가 출력됩니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, `@selected` 디렉티브는 select 옵션이 선택되어야 할 때 사용합니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, `@disabled` 디렉티브는 어떤 요소를 비활성화해야 할 때 사용할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

`@readonly` 디렉티브로 입력 요소를 읽기 전용으로 지정할 수도 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

그리고, `@required` 디렉티브로 해당 요소를 필수 입력값으로 지정할 수 있습니다.

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
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 블레이드의 [컴포넌트](#components)는 데이터 바인딩 및 속성(attribute) 바인딩 등의 여러 장점이 있으니, 가능하면 컴포넌트 활용을 권장합니다.

블레이드의 `@include` 디렉티브를 사용하면, 다른 블레이드 뷰를 현재 뷰 안에 삽입할 수 있습니다. 이렇게 하면 부모 뷰에서 사용 가능한 모든 변수가 포함된 뷰에서도 사용 가능합니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

포함되는 뷰는 부모 뷰의 모든 데이터를 상속받지만, 추가 데이터를 별도로 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

만약 존재하지 않는 뷰를 `@include`하려고 하면, 라라벨에서 에러가 발생합니다. 뷰가 없을 수도 있는 경우에는 `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

참, 조건에 따라 뷰를 포함하려면, `@includeWhen` 또는 `@includeUnless` 디렉티브를 사용할 수도 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 개의 뷰 중 가장 먼저 존재하는 뷰를 포함하려면, `includeFirst` 디렉티브를 사용할 수 있습니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> 블레이드 뷰에서 `__DIR__`와 `__FILE__` 상수 사용은 피하는 것이 좋습니다. 이 상수들은 캐시된 컴파일 뷰의 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>

#### 컬렉션을 위한 뷰 렌더링

Blade의 `@each` 디렉티브를 사용하면 반복문과 `include`를 한 줄로 결합할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

`@each` 디렉티브의 첫 번째 인수는 배열이나 컬렉션의 각 요소를 렌더링할 때 사용할 뷰 파일입니다. 두 번째 인수는 반복하고자 하는 배열 또는 컬렉션이고, 세 번째 인수는 뷰 내부에서 해당 요소를 참조할 때 사용할 변수명입니다. 예를 들어, `jobs` 배열을 반복한다면, 뷰 내부에서 각 항목을 `job` 변수로 접근할 수 있습니다. 현재 반복에 해당하는 배열의 키는 `key` 변수로 사용할 수 있습니다.

`@each` 디렉티브에는 네 번째 인수도 전달할 수 있습니다. 이 인수는 주어진 배열이 비어 있을 때 렌더링할 뷰를 지정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링한 뷰는 부모 뷰의 변수들을 상속하지 않습니다. 자식 뷰에서 이러한 변수가 필요하다면, `@foreach`와 `@include` 디렉티브를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브는 해당 템플릿 일부가 렌더링 주기당 한 번만 실행되도록 정의할 수 있게 해줍니다. 예를 들어, [스택(stacks)](#stacks)을 이용해 특정 JavaScript를 페이지의 헤더에 한 번만 넣고 싶은 경우에 사용할 수 있습니다. 반복문 안에서 [컴포넌트](#components)를 여러 번 렌더링하더라도, JavaScript는 최초 한 번만 헤더에 추가하고 싶을 때 유용합니다.

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 JavaScript 코드...
        </script>
    @endpush
@endonce
```

`@once`는 주로 `@push` 또는 `@prepend`와 함께 사용되므로, 좀 더 간편하게 쓸 수 있도록 `@pushOnce`, `@prependOnce` 디렉티브도 제공됩니다.

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 JavaScript 코드...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

때로는 뷰에 PHP 코드를 직접 삽입하는 것이 필요할 수 있습니다. Blade의 `@php` 디렉티브를 사용하면 템플릿 안에서 순수 PHP 코드를 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

또한, 클래스만 가져오고 싶을 때는 `@use` 디렉티브를 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

`@use` 디렉티브에는 두 번째 인수를 전달하여 가져온 클래스에 별칭(alias)을 지정할 수도 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

동일한 네임스페이스 아래 여러 클래스를 한 번에 그룹으로 가져올 수도 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

`@use` 디렉티브는 `function` 혹은 `const` 키워드를 앞에 붙이면 PHP 함수나 상수도 가져올 수 있습니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

클래스 가져오기와 마찬가지로, 함수와 상수의 경우에도 별칭(alias)을 지정할 수 있습니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

function 및 const 키워드와 함께 여러 심볼을 그룹으로 가져오는 것도 가능합니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석(Comments)

Blade에서는 뷰 안에 주석을 작성할 수도 있습니다. Blade 주석은 HTML 주석과 달리, 실제로 렌더링된 HTML에 포함되지 않습니다.

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트(Components)

컴포넌트와 슬롯(Slot)은 섹션, 레이아웃, 인클루드와 유사한 이점을 제공하지만, 컴포넌트와 슬롯의 개념이 더 이해하기 쉬운 경우가 많습니다. 컴포넌트는 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트 두 가지 방식으로 작성할 수 있습니다.

클래스 기반 컴포넌트를 만들려면, `make:component` 아티즌 명령어를 사용할 수 있습니다. 컴포넌트 사용법을 설명하기 위해 간단한 `Alert` 컴포넌트를 만들어보겠습니다. 아래 명령어를 실행하면 컴포넌트가 `app/View/Components` 디렉토리에 생성됩니다.

```shell
php artisan make:component Alert
```

`make:component` 명령어는 컴포넌트의 뷰 템플릿도 함께 생성합니다. 뷰 파일은 `resources/views/components` 디렉토리에 생성됩니다. 여러분이 애플리케이션에서 직접 컴포넌트를 작성하는 경우, 라라벨은 `app/View/Components`와 `resources/views/components` 디렉토리를 자동으로 탐색하므로, 별도의 컴포넌트 등록이 필요하지 않습니다.

컴포넌트를 하위 디렉토리에도 만들 수 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령어를 실행하면, `app/View/Components/Forms` 디렉토리에 `Input` 컴포넌트 클래스가 생성되고, 뷰 파일은 `resources/views/components/forms` 디렉토리에 생성됩니다.

익명(anonymous) 컴포넌트(Blade 템플릿 파일만 있고 별도의 클래스가 없는 컴포넌트)를 만들고 싶다면, `make:component` 명령어에 `--view` 옵션을 추가할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

이 명령어를 실행하면, `resources/views/components/forms/input.blade.php`에 Blade 파일이 생성되며, `<x-forms.input />` 형태로 컴포넌트로 사용할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자신의 애플리케이션을 위한 컴포넌트는 `app/View/Components`와 `resources/views/components` 디렉토리에서 자동으로 탐지됩니다.

그러나 Blade 컴포넌트를 활용하는 패키지를 제작하는 경우라면, 컴포넌트 클래스와 HTML 태그 별칭(alias)을 수동으로 등록해야 합니다. 보통 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다.

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

등록한 후에는 태그 별칭으로 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는, `componentNamespace` 메서드를 사용해 네임스페이스에 따라 컴포넌트 클래스를 자동으로 로드하도록 할 수도 있습니다. 예를 들어, `Nightshade`라는 패키지에 `Calendar` 및 `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 있다면 다음과 같이 설정할 수 있습니다.

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

이렇게 하면 `vendor 네임스페이스::` 문법을 사용해서 다음과 같이 패키지 컴포넌트를 쓸 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 해당 클래스를 자동으로 찾아줍니다. 하위 디렉토리는 "dot" 표기법으로 사용할 수 있습니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 화면에 표시하려면, Blade 파일 내부에서 컴포넌트 태그를 사용합니다. Blade 컴포넌트 태그는 `x-`로 시작하며, 뒤에 컴포넌트 클래스명을 케밥 케이스(kebab-case)로 붙입니다.

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉토리 내 더 깊은 하위 폴더에 위치하는 경우, `.` 문자를 사용해 디렉토리 구조를 나타낼 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`의 컴포넌트는 다음과 같이 렌더링합니다.

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하려면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 컴포넌트는 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트의 렌더링 여부를 결정합니다.
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트(Index Components)

컴포넌트를 그룹으로 관리할 때, 관련 컴포넌트들을 하나의 디렉토리에 모아두고 싶을 때가 있습니다. 예를 들어, "card"라는 컴포넌트 그룹이 다음과 같은 구조를 갖는다고 가정합시다.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트가 `Card` 디렉토리 안에 있으므로 `<x-card.card>`로 렌더링해야 할 것 같지만, 컴포넌트 파일명이 디렉토리명과 같을 때 라라벨은 해당 컴포넌트를 "루트(root)" 컴포넌트로 간주하여 디렉토리명을 반복하지 않고도 렌더링할 수 있습니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트로 데이터 전달

컴포넌트에 데이터를 전달할 때 HTML 속성을 사용할 수 있습니다. 고정값이나 원시 타입의 값은 일반 HTML 속성 형태로 전달하면 됩니다. PHP 변수나 표현식은 속성 앞에 `:`을 붙여서 전달해야 합니다.

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트의 데이터 속성들은 모두 클래스의 생성자에 정의해야 하며, 컴포넌트의 모든 public 속성(property)은 자동으로 컴포넌트 뷰에 전달됩니다. 별도로 `render` 메서드에서 데이터를 전달할 필요는 없습니다.

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
     * 컴포넌트를 표현하는 뷰(컨텐츠)를 반환합니다.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, 컴포넌트의 public 변수들은 변수명을 그대로 사용해서 출력할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 케이싱(Casing)

컴포넌트 생성자 인수는 `camelCase`로 표기하며, HTML 속성에서는 `kebab-case`를 사용해야 합니다. 예를 들어, 아래와 같은 컴포넌트 생성자가 있다고 해봅시다.

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

이 경우에는 `$alertType` 인수에 아래와 같이 전달할 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 짧은 속성(Short Attribute) 문법

컴포넌트에 속성을 전달할 때, "짧은 속성" 문법을 사용할 수도 있습니다. 이 방법은 속성 이름과 변수명이 동일할 때 특히 편리합니다.

```blade
{{-- 짧은 속성 문법 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 같은 일부 JavaScript 프레임워크도 `:` 접두사를 가진 속성을 사용하기 때문에, Blade에 이것이 PHP 표현식이 아님을 알려주려면 속성 앞에 `::`(콜론 두 개)를 사용할 수 있습니다. 예를 들어, 다음과 같은 컴포넌트가 있다고 가정해봅시다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

이 코드는 아래와 같은 HTML로 렌더링됩니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서는 public 변수뿐만 아니라 public 메서드도 사용할 수 있습니다. 예를 들어, `isSelected`라는 메서드가 있다고 가정합시다.

```php
/**
 * 주어진 옵션이 현재 선택된 옵션인지 확인합니다.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

이 메서드는, 메서드명과 동일한 변수명을 호출하듯 템플릿에서 바로 사용할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내부에서 속성/슬롯 접근

Blade 컴포넌트에서는 컴포넌트 이름, 속성, 슬롯 내용 등을 클래스의 render 메서드에서 사용할 수 있습니다. 이 정보를 사용하려면 `render` 메서드에서 클로저(closure)를 반환해야 합니다.

```php
use Closure;

/**
 * 컴포넌트를 표현하는 뷰(컨텐츠)를 반환합니다.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

컴포넌트의 `render` 메서드에서 반환하는 클로저는 `$data`라는 배열을 인자로 받을 수 있습니다. 이 배열은 컴포넌트와 관련된 여러 요소를 제공해줍니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열에 담긴 요소를 Blade 문자열에 직접 삽입하지 않아야 합니다. 이렇게 하면 악의적인 속성 내용으로 인한 원격 코드 실행 취약점이 발생할 수 있습니다.

`componentName`은 HTML 태그에서 `x-` 접두사 뒤의 이름과 동일합니다. 즉, `<x-alert />`의 `componentName`은 `alert`입니다. `attributes`에는 실제 태그에 작성한 모든 속성이 담기고, `slot`에는 해당 컴포넌트 슬롯의 내용을 담은 `Illuminate\Support\HtmlString` 인스턴스가 할당됩니다.

반환하는 값이 문자열이면, 존재하는 뷰인 경우 해당 뷰가 렌더링되고, 그렇지 않으면 인라인 Blade 뷰로서 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트에서 라라벨 [서비스 컨테이너](/docs/12.x/container)의 의존성이 필요하다면, 컴포넌트의 데이터 속성들 앞에 해당 의존성을 선언하면 컨테이너가 자동으로 주입해줍니다.

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
#### 속성/메서드 감추기

컴포넌트의 일부 public 메서드나 프로퍼티를 템플릿에서 접근할 수 없도록 하려면, 컴포넌트의 `$except` 배열 속성에 해당 이름을 추가하면 됩니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 컴포넌트 템플릿에 노출하지 않을 프로퍼티/메서드 목록
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
### 컴포넌트 속성(Component Attributes)

앞에서 컴포넌트로 데이터 속성 전달 방법을 살펴봤으나, 때로는 `class`와 같이 컴포넌트 동작에는 필요 없지만 HTML적으로 추가해야 할 속성이 필요할 수도 있습니다. 이런 속성들은 보통 컴포넌트 템플릿의 최상위 요소로 내려보내는 것이 일반적입니다. 예를 들어 아래처럼 `alert` 컴포넌트를 렌더링한다면,

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

생성자에 정의되지 않은 속성들은 자동으로 컴포넌트의 "속성 백(attribute bag)"에 모아집니다. 이 속성 백은 `$attributes` 변수로 컴포넌트 뷰 내에서 바로 사용할 수 있습니다. 모든 속성들을 출력하려면 이 변수를 에코하면 됩니다.

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내부에서 `@env` 같은 디렉티브를 사용하는 것은 아직 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>` 형식은 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본/합쳐진 속성(Default / Merged Attributes)

기본값을 가지는 속성이나, 속성 값에 추가적인 값을 합쳐야 할 때가 있습니다. 이럴 때는 속성 백의 `merge` 메서드를 사용할 수 있습니다. 이 메서드는 항상 적용할 CSS 클래스를 지정할 때 특히 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

예를 들어, 이 컴포넌트를 아래처럼 사용한다고 가정합시다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종적으로 렌더링되는 컴포넌트의 HTML은 다음과 같을 것입니다.

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

특정 조건이 `true`일 때만 클래스가 추가되도록 병합하고 싶을 수도 있습니다. 이럴 때는 `class` 메서드를 사용할 수 있습니다. 이 메서드는 배열을 받으며, 키에는 추가할 클래스명을, 값에는 불리언 조건식을 넣습니다. 배열 키가 숫자인 경우, 해당 값은 항상 클래스 목록에 포함됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성을 컴포넌트에 병합하려면, `class` 메서드 뒤에 `merge` 메서드를 체이닝할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성을 받지 않아야 하는 HTML 요소의 클래스를 조건부로 적용하려면 [@class 디렉티브](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### 클래스 이외의 속성 병합

`class`가 아닌 속성을 병합할 때는, `merge` 메서드에 전달한 값이 해당 속성의 "기본값"으로 간주됩니다. 단, `class` 속성과는 달리 이런 속성들은 주입된 값과 병합되지 않고, 단순히 덮어써집니다. 예를 들어, `button` 컴포넌트를 아래와 같이 구현한다고 해봅시다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

버튼 컴포넌트를 사용할 때 커스텀 `type`을 지정하고 싶다면, 컴포넌트 사용 시 속성을 지정하면 됩니다. 따로 지정하지 않으면 기본값으로 `button` 타입이 사용됩니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

이 예시에서 렌더링되는 HTML은 다음과 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

`class` 외에 특정 속성을 기본값과 주입 값 모두 함께 가지게 하고 싶을 때는, `prepends` 메서드를 사용할 수 있습니다. 아래 예시에서, `data-controller` 속성은 항상 `profile-controller`로 시작하고, 추가로 주입된 값은 그 뒤에 붙게 됩니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 사용하면 원하는 속성만 필터링할 수 있습니다. 이 메서드는 클로저를 받으며, 해당 속성을 유지하려면 `true`를 반환하면 됩니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

특정 문자열로 시작하는 키를 가진 모든 속성을 조회하려면 `whereStartsWith` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로, 특정 문자열로 시작하지 않는 키만 남기고 싶다면 `whereDoesntStartWith`를 사용할 수 있습니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용하면 주어진 속성 백에서 첫 번째 속성만 출력할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

컴포넌트에 특정 속성이 지정되어 있는지 확인하려면, `has` 메서드를 사용합니다. 이 메서드는 속성명을 인수로 받아, 해당 속성이 존재하면 `true`를 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class 속성이 존재합니다</div>
@endif
```

여러 속성을 배열로 전달하면, 지정한 모든 속성이 존재하는지 확인할 수 있습니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 존재합니다</div>
@endif
```

`hasAny` 메서드는 여러 속성 중 하나라도 존재하는지 확인할 때 사용합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>어느 하나의 속성이 존재합니다</div>
@endif
```

특정 속성의 값을 가져오려면 `get` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->get('class') }}
```

`only` 메서드는 전달한 키에 해당하는 속성만 조회합니다.

```blade
{{ $attributes->only(['class']) }}
```

`except` 메서드는 전달한 키를 제외한 모든 속성을 조회합니다.

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>

### 예약된 키워드

기본적으로, 일부 키워드는 Blade 내부적으로 컴포넌트를 렌더링하는 데 사용되기 때문에 예약되어 있습니다. 아래의 키워드들은 컴포넌트 내부에서 public 속성이나 메서드명으로 정의할 수 없습니다.

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

컴포넌트에 추가적인 콘텐츠를 전달해야 할 때가 자주 있습니다. 이를 위해 "슬롯(slot)"이라는 개념을 사용합니다. 컴포넌트 슬롯은 `$slot` 변수를 출력(echo)해서 렌더링할 수 있습니다. 이 개념을 살펴보기 위해, `alert` 컴포넌트가 아래와 같은 마크업으로 구성된다고 가정해보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

컴포넌트에 콘텐츠를 삽입하여 `slot`으로 전달할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

때때로, 컴포넌트 내부의 다양한 위치에 여러 슬롯을 렌더링해야 할 수도 있습니다. 좀 더 다양한 슬롯을 받도록 alert 컴포넌트를 수정해 보겠습니다. 예를 들어, "title" 슬롯을 삽입할 수 있게 만들어볼 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명시적인 슬롯의 내용을 정의하려면 `x-slot` 태그를 사용할 수 있습니다. `x-slot` 태그로 감싸지지 않은 나머지 모든 내용은 `$slot` 변수로 컴포넌트에 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯에 콘텐츠가 있는지 확인하려면, 슬롯의 `isEmpty` 메서드를 사용할 수 있습니다.

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

또한, `hasActualContent` 메서드를 사용하여 슬롯에 HTML 주석 이외의 실제 콘텐츠가 존재하는지 확인할 수도 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯(Scoped Slot)

Vue와 같은 JavaScript 프레임워크를 사용해봤다면, "스코프 슬롯"이라는 개념에 익숙할 수 있습니다. 이 개념은 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근하는 기능입니다. 라라벨에서도 비슷하게, 컴포넌트 클래스에 public 메서드나 속성을 정의하고, 슬롯 내부에서 `$component` 변수를 통해 컴포넌트에 접근할 수 있습니다. 아래에서는 `x-alert` 컴포넌트 클래스에 public `formatAlert` 메서드가 있다고 가정합니다.

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

Blade 컴포넌트처럼, 슬롯에도 CSS 클래스 등 [속성(attribute)](#component-attributes)를 추가할 수 있습니다.

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

슬롯의 속성과 상호작용하려면, 해당 슬롯 변수의 `attributes` 속성에 접근하면 됩니다. 속성과의 상호작용에 대한 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하십시오.

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

아주 작은 컴포넌트의 경우, 컴포넌트 클래스와 컴포넌트 뷰 템플릿을 따로 관리하는 것이 번거롭게 느껴질 수 있습니다. 이런 경우에는 `render` 메서드에서 직접 컴포넌트의 마크업을 반환할 수 있습니다.

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
#### 인라인 뷰 컴포넌트 생성

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령어 실행 시 `--inline` 옵션을 사용할 수 있습니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

때로는 어떤 컴포넌트를 렌더링할지 실행 시점까지 알 수 없는 경우가 있습니다. 이럴 때는 라라벨에 내장된 `dynamic-component` 컴포넌트를 사용하여, 런타임 값이나 변수에 따라 컴포넌트를 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래의 컴포넌트 수동 등록 관련 문서는 주로 뷰 컴포넌트를 포함하는 라라벨 패키지를 작성하는 경우에 해당합니다. 패키지를 작성하지 않는 경우, 해당 컴포넌트 문서는 해당되지 않을 수 있습니다.

자신의 애플리케이션에서 컴포넌트를 작성하는 경우, `app/View/Components` 디렉토리와 `resources/views/components` 디렉토리 내의 컴포넌트들은 자동으로 인식됩니다.

하지만 Blade 컴포넌트를 활용하는 패키지를 개발하거나, 관례적이지 않은 위치(디렉토리)에 컴포넌트가 있다면, 컴포넌트 클래스와 해당 HTML 태그 별칭을 라라벨에 수동으로 등록해줘야 합니다. 보통 패키지의 서비스 프로바이더 `boot` 메서드에서 컴포넌트 등록을 수행합니다.

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

컴포넌트가 등록되면, 등록한 태그 별칭을 이용해 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

또 다른 방법으로, `componentNamespace` 메서드를 사용하여 네임스페이스 규칙에 따라 컴포넌트 클래스를 자동으로 등록할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스 내에 존재한다면, 아래와 같이 사용할 수 있습니다.

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

이렇게 하면, 벤더 네임스페이스를 활용한 `package-name::` 문법으로 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 해당 컴포넌트에 연결된 클래스를 자동으로 찾아줍니다. 또한, 하위 디렉토리는 "dot" 표기법으로 사용할 수 있습니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트(Anonymous Component)

인라인 컴포넌트와 비슷하게, 익명 컴포넌트는 한 개의 파일로 컴포넌트를 관리할 수 있는 방법을 제공합니다. 익명 컴포넌트는 하나의 뷰 파일만 사용하고 별도의 클래스는 존재하지 않습니다. 익명 컴포넌트를 정의하려면, `resources/views/components` 디렉토리에 Blade 템플릿을 배치하기만 하면 됩니다. 예를 들어 `resources/views/components/alert.blade.php`에 컴포넌트를 정의했다면, 아래와 같이 간단하게 렌더링할 수 있습니다.

```blade
<x-alert/>
```

컴포넌트가 `components` 디렉토리 내에 더 깊게 중첩되어 있다면, `.` 문자를 사용해 표현할 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php` 컴포넌트는 다음과 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

때때로, 하나의 컴포넌트가 여러 Blade 템플릿으로 이루어질 수 있습니다. 이 경우 관련된 템플릿을 하나의 디렉토리로 묶고 싶을 수 있습니다. 예를 들어 "accordion" 컴포넌트가 아래와 같은 디렉토리 구조로 되어 있다고 가정해봅시다.

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이 구조에서는 아래와 같이 accordion 컴포넌트와 하위 아이템을 쉽게 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 `x-accordion` 형식으로 accordion 컴포넌트를 렌더링하려면, "인덱스" 용 accordion 컴포넌트 템플릿을 `resources/views/components` 디렉토리에 두어야 해서, 관련 템플릿과 분리됩니다.

다행히 Blade에서는 컴포넌트 디렉토리 이름과 동일한 파일을 해당 디렉토리 안에 둘 수도 있습니다. 이 경우 템플릿이 비록 디렉토리 내부에 위치해도 "루트" 컴포넌트 요소로 렌더링할 수 있습니다. 즉, 앞서 예시의 Blade 문법을 그대로 사용할 수 있고, 디렉토리 구조만 아래와 같이 조정하면 됩니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성(attribute)

익명 컴포넌트에는 별도의 클래스가 없으므로, 어떤 데이터는 컴포넌트로 변수로 전달하고, 어떤 속성(attribute)은 [attribute bag](#component-attributes)에 담아야 할지 고민이 될 수 있습니다.

이 경우, 컴포넌트 Blade 템플릿 상단에 `@props` 디렉티브를 사용해 데이터 변수로 사용할 속성을 지정할 수 있습니다. 지정하지 않은 나머지 속성(attribute)은 attribute bag으로 전달됩니다. 만약 데이터 변수에 기본값을 주고 싶다면, 배열의 키-값 쌍을 이용해 변수명과 기본값을 지정할 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위처럼 컴포넌트를 정의했다면, 아래와 같이 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

가끔 자식 컴포넌트 내에서 부모 컴포넌트의 데이터를 사용하고 싶을 때가 있습니다. 이런 경우에는 `@aware` 디렉티브를 사용하면 됩니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`으로 구성된 복잡한 메뉴 컴포넌트를 만들어본다고 가정해봅시다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` 컴포넌트는 다음과 같이 구현할 수 있습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` prop은 부모에만 전달되었기 때문에, 기본적으로 자식 `<x-menu.item>` 컴포넌트에서는 사용할 수 없습니다. 하지만 `@aware` 디렉티브를 사용하면 자식에서도 해당 값을 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 디렉티브는 부모 컴포넌트에 HTML 속성으로 명시적으로 전달된 데이터만 접근할 수 있습니다. 부모 컴포넌트의 `@props`에 기본값만 선언되어 있고 실제로 전달되지 않았다면, `@aware`로 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 위치(Anonymous Component Paths)

앞에서 설명했듯, 익명 컴포넌트는 주로 `resources/views/components` 디렉토리에 템플릿을 위치시켜 정의합니다. 하지만 경우에 따라, 기본 경로 이외의 다른 익명 컴포넌트 경로를 별도로 라라벨에 등록하고 싶을 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자로 익명 컴포넌트 위치(경로), 두 번째 인자로 해당 컴포넌트들이 소속될 "네임스페이스"(선택사항)를 받습니다. 보통 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) `boot` 메서드에서 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

위처럼 접두사(prefix) 없이 컴포넌트 경로를 등록하면, Blade 컴포넌트 내부에서도 접두사 없이 렌더링할 수 있습니다. 예를 들어, 등록한 경로에 `panel.blade.php` 컴포넌트가 있다면 아래와 같이 렌더링 가능합니다.

```blade
<x-panel />
```

대신, `anonymousComponentPath`의 두 번째 인자로 네임스페이스(접두사)를 전달하면, 컴포넌트를 렌더링할 때 해당 네임스페이스를 컴포넌트 이름 앞에 붙여 사용할 수 있습니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

접두사가 지정된 경우, 해당 "네임스페이스" 내의 컴포넌트는 렌더링할 때 네임스페이스를 컴포넌트 이름 앞에 붙여 사용합니다.

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 만들기

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분의 웹 애플리케이션은 여러 페이지에 걸쳐 공통의 전체 레이아웃을 사용합니다. 만약 우리가 작성하는 각 뷰마다 전체 레이아웃 HTML을 반복해서 작성해야 한다면, 관리가 매우 힘들고 번거로울 것입니다. 다행히 라라벨에서는 이 레이아웃을 하나의 [Blade 컴포넌트](#components)로 정의하고, 애플리케이션 전체에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어, "할 일 목록(todo)" 애플리케이션을 만든다고 가정하면, 아래와 같이 `layout` 컴포넌트를 만들 수 있습니다.

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

`layout` 컴포넌트를 정의했다면, 해당 컴포넌트를 사용하는 Blade 뷰를 만들 수 있습니다. 아래는 작업 목록을 출력하는 간단한 뷰 예시입니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트에 전달된 콘텐츠는 `layout` 컴포넌트 내부에서 기본적으로 `$slot` 변수로 제공됨을 기억하세요. 또한, 레이아웃에서 `$title` 슬롯을 사용할 수 있으며, 슬롯이 없다면 기본 타이틀이 나타납니다. 작업 목록 뷰에서 표준 슬롯 문법을 사용해서 커스텀 타이틀을 주입할 수도 있습니다. ([컴포넌트 문서](#components)에서 설명한 슬롯 문법 참고)

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

이제 레이아웃과 작업 목록 뷰를 정의했으니, 라우트에서 해당 뷰를 반환하면 됩니다.

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

레이아웃은 "템플릿 상속" 방식을 이용해서도 만들 수 있습니다. [컴포넌트](#components) 등장 전까지는 애플리케이션 레이아웃을 만드는 주요 방법이 바로 이 방식이었습니다.

먼저, 간단한 예시를 살펴봅시다. 아래는 페이지 레이아웃입니다. 대부분의 웹 애플리케이션에서는 여러 페이지에 걸쳐 공통의 레이아웃이 반복되므로, 별도의 Blade 뷰로 이 레이아웃을 정의하면 매우 편리합니다.

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

위 파일은 일반적인 HTML 마크업을 포함하고 있습니다. 주목할 점은 `@section`과 `@yield` 디렉티브입니다. `@section`은 말 그대로 특정 구역의 내용을 정의하고, `@yield`는 그 구역의 콘텐츠를 출력합니다.

이제 애플리케이션 레이아웃을 정의했으니, 이 레이아웃을 상속하는 자식 페이지를 정의해보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장(상속)하기

자식 뷰를 만들 때, `@extends` Blade 디렉티브를 통해 상속받을 레이아웃을 지정할 수 있습니다. Blade 레이아웃을 확장하는 뷰는 `@section` 디렉티브를 사용해 레이아웃의 특정 구역에 콘텐츠를 삽입할 수 있습니다. 위 예시에서 본 것처럼, 이 구역의 내용은 `@yield`를 통해 레이아웃에 표시됩니다.

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

위 예시에서 `sidebar` 섹션은 `@@parent` 디렉티브를 사용하여, 기존 레이아웃에 정의된 사이드바의 내용을 그대로 두고 그 뒤에 내용을 추가(append)합니다. `@@parent`는 뷰가 렌더링될 때 레이아웃의 콘텐츠로 대체됩니다.

> [!NOTE]
> 앞선 예제와 달리, 이 `sidebar` 섹션은 `@show` 대신 `@endsection`으로 끝납니다. `@endsection`은 섹션을 정의만 하고, `@show`는 섹션 정의와 동시에 **즉시 출력(yield)** 합니다.

`@yield` 디렉티브는 두 번째 인자로 기본값도 받을 수 있습니다. 만약 해당 섹션이 정의되어 있지 않으면 이 값이 렌더링됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때마다, [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있도록 폼 안에 숨겨진 CSRF 토큰 필드를 반드시 포함해야 합니다. `@csrf` Blade 디렉티브를 사용해 토큰 필드를 쉽게 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드(Method Field)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없기 때문에, 이러한 HTTP 메서드를 사용하려면 숨겨진 `_method` 필드가 필요합니다. `@method` Blade 디렉티브가 이 필드를 자동으로 생성해줍니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러(Validation Errors)

`@error` 디렉티브는 지정한 속성(attribute)에 대해 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 있는지 빠르게 확인할 수 있도록 도와줍니다. `@error` 내부에서는 `$message` 변수를 출력하여 에러 메시지를 표시할 수 있습니다.

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

`@error` 디렉티브는 내부적으로 if 문으로 변환되기 때문에, `@else` 디렉티브를 사용하여 에러가 없을 때의 콘텐츠도 렌더링할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 폼이 있는 페이지에서 [특정 에러 백(error bag) 이름](/docs/12.x/validation#named-error-bags)을 두 번째 인자로 전달하여 해당 폼의 유효성 에러 메시지만 확인할 수도 있습니다.

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

Blade에서는 명명된 스택에 데이터를 `push`하여, 이를 다른 뷰 또는 레이아웃의 원하는 위치에서 렌더링할 수 있습니다. 이 기능은 특히 자식 뷰에서 필요한 JavaScript 라이브러리 등을 명확하게 지정할 때 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 불리언 표현식이 `true`로 평가될 때에만 `@push`를 사용하고 싶다면, `@pushIf` 디렉티브를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

같은 스택에 여러 번 `push`하는 것도 가능합니다. 스택에 쌓인 모든 내용을 렌더링하려면, `@stack` 디렉티브에 해당 스택 이름을 전달하면 됩니다.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택의 가장 앞부분에 콘텐츠를 추가하고 싶다면, `@prepend` 디렉티브를 사용해야 합니다.

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

`@inject` 디렉티브를 사용하면 라라벨 [서비스 컨테이너](/docs/12.x/container)에서 서비스를 가져올 수 있습니다. `@inject`의 첫 번째 인수는 서비스가 할당될 변수 이름이고, 두 번째 인수는 가져오려는 서비스 클래스 또는 인터페이스의 이름입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링(Rendering Inline Blade Templates)

가끔 원시 Blade 템플릿 문자열을 HTML로 변환해야 할 때가 있습니다. 이럴 때는 `Blade` 파사드에서 제공하는 `render` 메서드를 사용하면 됩니다. `render` 메서드에는 Blade 템플릿 문자열과 옵션으로 뷰에 전달할 데이터 배열을 넣을 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

라라벨은 인라인 Blade 템플릿을 `storage/framework/views` 디렉토리에 임시로 저장하여 렌더링합니다. Blade 템플릿 렌더링 이후 이 임시 파일을 삭제하고 싶다면, `deleteCachedView` 인자를 추가로 전달하면 됩니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링(Rendering Blade Fragments)

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, Blade 템플릿 전체가 아닌 일부분만 HTTP 응답으로 반환해야 할 때가 있습니다. Blade의 "프래그먼트(fragment)" 기능을 활용하면 이 작업을 쉽게 할 수 있습니다. 사용 방법은, Blade 템플릿의 일부를 `@fragment`와 `@endfragment` 사이에 감싸면 됩니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

그리고 해당 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출하여 HTTP 응답에 포함될 프래그먼트만 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` 메서드를 사용하면 특정 조건에 따라 뷰의 프래그먼트만을 반환할 수도 있으며, 조건이 충족되지 않으면 뷰 전체가 반환됩니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments`와 `fragmentsIf` 메서드를 사용하면 여러 개의 프래그먼트를 한 번에 반환할 수 있습니다. 반환되는 프래그먼트들은 합쳐져서 응답에 포함됩니다.

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

Blade에서는 `directive` 메서드를 사용해 나만의 커스텀 디렉티브를 만들 수 있습니다. Blade 컴파일러가 커스텀 디렉티브를 만나면, 지정된 콜백을 호출하며 디렉티브에 전달된 식(expression)을 넘겨줍니다.

아래 예시는 주어진 `$var`(반드시 `DateTime` 인스턴스여야 함)를 포맷팅하는 `@datetime($var)` 커스텀 디렉티브를 생성합니다.

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

이처럼, 디렉티브에 전달된 식에 `format` 메서드를 연결하는 방식입니다. 따라서 이 예시에서 실제로 생성되는 최종 PHP 코드는 다음과 같습니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 후에는 반드시 Blade 뷰의 캐시 파일을 모두 삭제해야 합니다. 캐시는 `view:clear` 아티즌 명령어로 간단히 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러(Custom Echo Handlers)

Blade에서 객체를 "에코"할 경우, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring)은 PHP 내장 "매직 메서드" 중 하나입니다. 그러나 사용 중인 클래스가 서드파티 라이브러리 등이라, 직접 `__toString`을 제어할 수 없는 경우도 있습니다.

이럴 때는 Blade에서 해당 타입의 객체를 위한 커스텀 에코 핸들러를 등록할 수 있습니다. 이를 위해 Blade의 `stringable` 메서드를 사용합니다. `stringable`은 클로저를 인자로 받으며, 이 클로저에는 처리 대상 객체 타입에 대한 타입힌트를 추가해야 합니다. 일반적으로 `stringable`은 여러분의 애플리케이션 `AppServiceProvider`의 `boot` 메서드 내에서 호출하는 것이 좋습니다.

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

이렇게 커스텀 에코 핸들러를 등록하면, Blade 템플릿 안에서 해당 객체를 곧바로 에코하여 사용할 수 있습니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 if 구문(Custom If Statements)

간단한 조건문에 대해 커스텀 디렉티브를 구현하는 것은 오히려 복잡하고 번거로울 수 있습니다. Blade는 이러한 경우를 위해, 클로저를 이용해 쉽고 빠르게 커스텀 조건문 디렉티브를 정의할 수 있는 `Blade::if` 메서드를 제공합니다. 예를 들어, 애플리케이션의 기본 "디스크(disk)"가 무엇인지 확인하는 조건문을 만들어 보겠습니다. 이 코드는 `AppServiceProvider`의 `boot` 메서드 내에 추가하면 됩니다.

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

이제 커스텀 조건문을 템플릿 내에서 아래와 같이 사용할 수 있습니다.

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