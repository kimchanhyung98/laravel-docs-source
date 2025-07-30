# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강화하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [Raw PHP](#raw-php)
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
    - [데이터 속성 / 속성들](#data-properties-attributes)
    - [부모 데이터 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [검증 오류](#validation-errors)
- [스택](#stacks)
- [서비스 의존성 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 포함된 간단하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리 Blade는 템플릿 내에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실, 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되어 변경될 때까지 캐시되므로, Blade 자체의 오버헤드는 거의 없습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며, 보통 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 전역 `view` 헬퍼 함수를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론, [뷰(Views)](/docs/master/views) 문서에서 설명된 것처럼, `view` 헬퍼 함수의 두 번째 인수로 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강화하기

Blade 템플릿을 한 단계 더 발전시키고, 동적인 인터페이스를 손쉽게 구축하고 싶다면 [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire는 React나 Vue와 같은 프런트엔드 프레임워크에서만 가능했던 동적 기능을 Blade 컴포넌트에 추가할 수 있게 해주며, 복잡한 클라이언트 사이드 렌더링이나 빌드 과정 없이도 최신 반응형 프런트엔드를 구축할 수 있는 훌륭한 방법을 제공합니다.

<a name="displaying-data"></a>
## 데이터 출력

Blade 뷰에 전달된 데이터를 출력하려면, 변수를 중괄호로 감싸면 됩니다. 예를 들어 다음과 같은 라우트가 있을 때:

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
> Blade의 `{{ }}` 출력 문은 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 XSS 공격을 방지합니다.

뷰에 전달된 변수 외에도, PHP 함수의 결과나 원하는 어떤 PHP 코드도 Blade 출력 문 안에 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
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
#### 이스케이프되지 않은 데이터 출력

기본적으로 Blade `{{ }}` 문은 PHP의 `htmlspecialchars` 함수를 자동으로 거쳐 XSS 공격을 방지합니다. 만약 데이터의 이스케이프 처리를 원치 않는 경우, 다음 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자 입력 등 외부에서 제공된 콘텐츠를 출력할 때는 매우 주의해야 합니다. 보통은 XSS 공격 방지를 위해 이스케이프 처리된 이중 중괄호(`{{ }}`) 구문을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크가 브라우저에 표현할 표현식 표시에 중괄호를 사용하기 때문에, Blade에서 특정 표현식을 그대로 두고 싶으면 `@` 기호를 앞에 붙이면 됩니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 경우 `@` 기호는 Blade에서 제거되지만, `{{ name }}` 표현식은 Blade가 처리하지 않아 자바스크립트 프레임워크가 렌더링합니다.

`@` 기호는 Blade 디렉티브를 이스케이프하는 데도 사용할 수 있습니다:

```blade
{{-- Blade 템플릿 --}}
@@if()

<!-- HTML 출력 -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

때때로 자바스크립트 변수 초기화를 위해 배열 데이터를 JSON 형태로 뷰에 전달할 수 있습니다. 예를 들어:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP `json_encode`와 같은 인자를 받지만, HTML 내 따옴표 안에 적절히 이스케이프된 JSON을 생성해 줍니다. 반환값은 JavaScript `JSON.parse` 문을 포함하는 문자열입니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel 최신 버전에서는 `Js` 파사드가 기본 제공되어 Blade 내에서 더 간편하게 사용할 수 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. Blade 템플릿은 정규 표현식을 기반으로 하므로, 복잡한 표현식을 이 디렉티브에 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿 내에 자바스크립트 변수가 큰 비중을 차지한다면, 각 Blade 출력 앞에 `@`를 붙이지 않아도 되도록 `@verbatim` 디렉티브로 감쌀 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브

템플릿 상속과 데이터 출력 외에도, Blade는 조건문, 반복문 같은 PHP 제어 구조의 편리한 단축 구문들을 제공합니다. 이들은 PHP와 비슷한 문법으로 아주 간결하게 작성할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브로 `if` 문을 작성할 수 있습니다. 동작은 PHP의 그것과 동일합니다:

```blade
@if (count($records) === 1)
    레코드가 1개 있습니다!
@elseif (count($records) > 1)
    여러 개의 레코드가 있습니다!
@else
    레코드가 없습니다!
@endif
```

편의를 위해 `@unless` 디렉티브도 제공합니다:

```blade
@unless (Auth::check())
    로그인되어 있지 않습니다.
@endunless
```

조건부 디렉티브 외에도 `@isset`와 `@empty` 디렉티브는 해당하는 PHP 함수와 같은 역할을 합니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님
@endisset

@empty($records)
    // $records가 "비어 있음"
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브로 현재 사용자가 [인증](/docs/master/authentication)되었는지 또는 게스트인지 빠르게 판단할 수 있습니다:

```blade
@auth
    // 사용자가 인증됨
@endauth

@guest
    // 사용자가 인증되지 않음
@endguest
```

특정 인증 가드를 검사하고 싶다면 다음과 같이 가드명을 인수로 넘길 수 있습니다:

```blade
@auth('admin')
    // admin 가드를 통해 인증됨
@endauth

@guest('admin')
    // admin 가드를 통해 인증되지 않음
@endguest
```

<a name="environment-directives"></a>
#### 환경 디렉티브

애플리케이션이 프로덕션 환경에서 실행 중인지 확인하려면 `@production` 디렉티브를 사용할 수 있습니다:

```blade
@production
    // 프로덕션 전용 컨텐츠
@endproduction
```

또한 특정 환경인지 확인하려면 `@env` 디렉티브를 사용하세요:

```blade
@env('staging')
    // 스테이징 환경에서 실행 중...
@endenv

@env(['staging', 'production'])
    // 스테이징 또는 프로덕션 환경에서 실행 중...
@endenv
```

<a name="section-directives"></a>
#### 섹션 디렉티브

`@hasSection`으로 템플릿 상속 섹션에 내용이 있는지 확인할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

반대로, 섹션이 비어있는지 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 디렉티브

`@session` 디렉티브로 특정 [세션](/docs/master/session) 값이 존재하는지 판별할 수 있습니다. 해당 값이 존재하면 `@session`과 `@endsession` 사이의 콘텐츠가 출력되고, `$value` 변수로 세션 값을 출력할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브로 switch문을 작성할 수 있습니다:

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

Blade는 PHP 반복문을 위한 단축 구문도 제공합니다. 각 디렉티브는 PHP 반복문과 동작이 같습니다:

```blade
@for ($i = 0; $i < 10; $i++)
    현재 값은 {{ $i }}
@endfor

@foreach ($users as $user)
    <p>사용자 {{ $user->id }} 입니다.</p>
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
> `foreach` 반복 중에 [루프 변수](#the-loop-variable)를 사용하면 현재 반복 인덱스나 첫 번째 반복인지 등의 정보를 얻을 수 있습니다.

반복문 내에서 현재 반복을 건너뛰거나 루프를 종료하려면 `@continue`와 `@break`를 사용할 수 있습니다:

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

조건문을 포함해서 아래와 같이 줄여서 쓸 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach`문 내에서 `$loop` 변수를 활용할 수 있으며, 현재 루프 정보들을 제공합니다. 예를 들어 이 루프가 첫번째인지, 마지막인지 확인 가능합니다:

```blade
@foreach ($users as $user)
    @if ($loop->first)
        첫 번째 반복입니다.
    @endif

    @if ($loop->last)
        마지막 반복입니다.
    @endif

    <p>사용자 {{ $user->id }} 입니다.</p>
@endforeach
```

중첩된 루프에서는 `parent` 속성을 통해 부모 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            부모 루프의 첫 번째 반복입니다.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수는 다음과 같은 유용한 속성을 가집니다:

<div class="overflow-auto">

| 속성             | 설명                                                        |
| ---------------- | ----------------------------------------------------------- |
| `$loop->index`     | 현재 루프 인덱스 (0부터 시작)                               |
| `$loop->iteration` | 현재 루프 반복 횟수 (1부터 시작)                            |
| `$loop->remaining` | 남은 반복 횟수                                              |
| `$loop->count`     | 반복하는 아이템 총 개수                                    |
| `$loop->first`     | 현재 반복이 첫 번째인지 여부                                |
| `$loop->last`      | 현재 반복이 마지막인지 여부                                |
| `$loop->even`      | 현재 반복이 짝수 인덱스인지 여부                           |
| `$loop->odd`       | 현재 반복이 홀수 인덱스인지 여부                           |
| `$loop->depth`     | 현재 루프 중첩 깊이                                        |
| `$loop->parent`    | 중첩된 루프에서 부모 루프의 `$loop` 변수                   |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일

`@class` 디렉티브는 조건에 따라 CSS 클래스를 컴파일합니다. 배열을 인수로 받는데, 키에는 클래스명, 값은 Boolean 조건입니다. 숫자 키일 경우 항상 포함됩니다:

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

`@style` 디렉티브를 사용해 조건부로 인라인 스타일을 추가할 수도 있습니다:

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

`@checked` 디렉티브를 사용하면 특정 체크박스가 체크 상태인지 쉽게 지정할 수 있습니다. 조건이 참일 때 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

비슷하게, 선택 옵션이 선택되었는지 `@selected` 디렉티브로 나타낼 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한 요소가 비활성화되어야 할 때는 `@disabled`를, 읽기 전용일 때는 `@readonly`를, 필수 입력이어야 할 때는 `@required`를 사용할 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>

<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>

<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### 서브뷰 포함

> [!NOTE]
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 컴포넌트(#components)가 유사한 기능을 제공하며 데이터 및 속성 바인딩 같은 장점을 제공합니다.

`@include`는 다른 Blade 뷰를 현재 뷰 안에 포함할 수 있습니다. 부모 뷰의 모든 변수는 포함된 뷰에서도 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

포함되는 뷰가 상위 뷰의 모든 데이터를 상속받지만, 추가로 데이터 배열을 전달할 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

뷰가 없으면 `@include`로는 오류가 나지만, 존재 여부에 따라 포함 여부를 결정하고 싶다면 `@includeIf`를 사용하세요:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

불리언 조건에 따라 포함 여부를 정하려면 `@includeWhen`과 `@includeUnless`를 사용하세요:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 첫 번째 존재하는 뷰를 포함하려면 `includeFirst`를 사용하세요:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__`와 `__FILE__` 상수를 사용하지 마세요. 캐시된 컴파일된 뷰 위치를 나타내므로 의도와 다를 수 있습니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

`@each` 디렉티브로 반복문과 인클루드를 한 줄로 처리할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인수는 렌더링할 뷰, 두 번째는 반복할 배열 혹은 컬렉션, 세 번째는 뷰 내에서 각 요소를 가리키는 변수명입니다. 현재 이터레이션의 키는 `key` 변수로 접근 가능하다:

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

네 번째 인수를 지정하면 배열이 비었을 때 대체해서 렌더링할 뷰입니다.

> [!WARNING]
> `@each`로 렌더링하는 뷰는 부모 뷰의 변수를 상속받지 않습니다. 필요한 경우 `@foreach`와 `@include`를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once`는 템플릿 내 특정 부분을 렌더링 사이클마다 단 한 번만 평가하도록 합니다. 자바스크립트 코드를 헤더에 푸시할 때 유용합니다. 예를 들어, 반복되는 컴포넌트에서 첫 렌더링 시에만 스크립트를 푸시하고 싶다면:

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 자바스크립트...
        </script>
    @endpush
@endonce
```

`@once`는 `@push` 또는 `@prepend`와 자주 함께 쓰이므로, 이를 위한 `@pushOnce`와 `@prependOnce` 디렉티브도 있습니다:

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 자바스크립트...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

뷰 내에 직접 PHP 코드를 넣어야 할 때 `@php` 디렉티브를 사용하세요:

```blade
@php
    $counter = 1;
@endphp
```

단순히 클래스를 임포트하려면 `@use` 디렉티브를 쓸 수 있습니다:

```blade
@use('App\Models\Flight')
```

별칭을 지정하려면 두 번째 인수를 넘기세요:

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
### 주석

Blade에서는 HTML 주석과는 달리, 렌더링된 HTML에 포함되지 않는 주석을 작성할 수 있습니다:

```blade
{{-- 이 주석은 렌더링된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 비슷한 기능을 제공하지만, 컴포넌트와 슬롯의 사고 모델이 더 이해하기 쉽다는 의견도 많습니다. 컴포넌트 작성 방법은 크게 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트는 `make:component` Artisan 명령으로 만듭니다. 간단한 `Alert` 컴포넌트를 만들어 보겠습니다. 이 명령은 `app/View/Components` 디렉토리에 클래스를 생성합니다:

```shell
php artisan make:component Alert
```

이 명령은 컴포넌트 뷰도 함께 만듭니다. 뷰는 `resources/views/components` 디렉토리에 위치합니다. 애플리케이션 내 컴포넌트는 기본적으로 `app/View/Components`와 `resources/views/components` 디렉토리에서 자동으로 발견되므로 별도 등록이 보통 필요하지 않습니다.

하위 디렉토리 내에 컴포넌트를 만들 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms`에 `Input` 클래스를, 뷰를 `resources/views/components/forms`에 생성합니다.

익명 컴포넌트(클래스 없이 Blade 템플릿만 있는 컴포넌트)를 만들려면 `--view` 플래그를 사용하세요:

```shell
php artisan make:component forms.input --view
```

이제 `resources/views/components/forms/input.blade.php` 파일이 생성되며 `<x-forms.input />` 으로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션 컴포넌트는 자동 발견되지만, 패키지용 컴포넌트는 클래스와 태그 별칭을 수동 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

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

등록 후에는 아래처럼 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 써서 규칙 기반 자동 로드도 가능합니다. 예를 들어 `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 있다면:

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

이 경우 컴포넌트는 `package-name::` 구문으로 벤더 네임스페이스 접두사를 붙여서 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

컴포넌트 이름에서 파스칼 케이스 클래스를 자동 탐지하며, 하위 디렉토리는 점(`.`) 표기법으로 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

Blade 컴포넌트 태그는 `x-`로 시작하며, 그 뒤에 컴포넌트 클래스의 케밥 케이스 이름이 옵니다:

```blade
<x-alert/>

<x-user-profile/>
```

`app/View/Components` 내부에서 더 깊이 중첩된 컴포넌트는 `.`을 써서 경로를 명시합니다. 예를 들어 `app/View/Components/Inputs/Button.php` 라면:

```blade
<x-inputs.button/>
```

컴포넌트 렌더링 여부를 조건부로 결정하려면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다:

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

컴포넌트 그룹이 있고 관련 컴포넌트를 단일 디렉토리에 모을 때가 있습니다. 예를 들어 "card" 컴포넌트 트리 구조가 다음과 같을 때:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

컴포넌트 이름과 디렉토리 이름이 같으면 `<x-card.card>` 대신 `<x-card>`로 최상위 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

컴포넌트에 데이터를 전달하는 방법은 HTML 속성 형태입니다. 고정된 원시 값은 일반 문자열로, PHP 변수나 표현식은 `:` 접두사를 붙인 속성으로 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트의 데이터 속성은 생성자로 정의합니다. 컴포넌트의 모든 public 속성은 자동으로 뷰에서 사용 가능하며, `render` 메서드에서 별도로 데이터 전달은 필요 없습니다:

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
     * 컴포넌트의 뷰 반환
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트 렌더링 시 public 변수들을 이름으로 출력할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 캐싱 규칙

컴포넌트 생성자 인자명은 `camelCase`로 작성하고, HTML 속성명은 `kebab-case`를 사용해야 합니다. 예를 들어 아래 생성자는:

```php
/**
 * 컴포넌트 인스턴스 생성자
 */
public function __construct(
    public string $alertType,
) {}
```

아래와 같이 전달해야 합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성 구문

속성 이름이 변수와 일치하면 아래처럼 단축 구문을 사용할 수 있습니다:

```blade
{{-- 단축 속성 구문 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js처럼 콜론 접두사로 속성을 사용하는 프레임워크와 충돌할 때는, 속성 이름 앞에 `::`를 붙여 Blade가 PHP 표현식으로 해석하지 않도록 할 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

렌더링 결과는 다음과 같습니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿 내에서 public 메서드를 호출할 수 있습니다. 예를 들어 `isSelected` 라는 메서드가 있으면, 다음처럼 사용 가능합니다:

```php
/**
 * 선택된 옵션인지 판단
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

뷰에서 호출:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내부에서 속성 및 슬롯 접근

컴포넌트의 `render` 메서드가 클로저를 반환하면 컴포넌트 이름, 속성, 슬롯을 클로저에서 받을 수 있습니다:

```php
use Closure;

/**
 * 컴포넌트 뷰 반환
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>컴포넌트 내용</div>';
    };
}
```

클로저가 `$data` 배열 인수를 받으면 다음 내용을 포함합니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>컴포넌트 내용</div>';
}
```

> [!WARNING]
> `$data` 배열 요소를 이 문자열 안에 직접 포함시키면 악의적인 속성 내용으로 원격 코드 실행이 유발될 위험이 있으므로 절대 하지 마세요.

`componentName`은 `x-` 접두사 뒤 컴포넌트 태그명이며, `attributes`는 HTML 태그에 포함된 모든 속성, `slot`은 슬롯 내용이 HTML 문자열로 들어있습니다.

클로저는 문자열을 반환해야 하며, 반환된 문자열이 기존 뷰 이름이면 뷰로 렌더링하고, 아니면 인라인 Blade 뷰로 처리합니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트가 Laravel [서비스 컨테이너](/docs/master/container)의 의존성을 필요로 하면, 생성자에 선언된 일반 매개변수를 데이터 속성보다 앞에 나열하면 자동 주입됩니다:

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
#### 속성 / 메서드 숨기기

일부 public 속성이나 메서드를 컴포넌트 템플릿에서 변수로 노출하고 싶지 않으면, `$except` 배열에 포함시키세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출하지 않을 속성과 메서드
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

컴포넌트 동작에 필요한 데이터 속성 외에, `class` 같은 추가 HTML 속성을 포함해야 할 때가 있습니다. 이런 추가 속성들은 자동으로 `$attributes` 변수로 컴포넌트에 전달됩니다. 템플릿에서 해당 속성들을 이렇게 출력하세요:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내에서 `@env` 같은 디렉티브 사용은 지원되지 않습니다. 예를 들어 `<x-alert :live="@env('production')"/>` 는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 / 병합 속성

속성에 기본값을 주거나 추가 값을 병합하려면, `$attributes`의 `merge` 메서드를 사용합니다. 주로 기본 CSS 클래스를 지정할 때 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

만약 이렇게 사용한다면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더링 결과는 아래와 같습니다:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 클래스를 병합하려면 `class` 메서드를 쓰세요. 배열 형태로 키에 클래스, 값은 boolean 표현식을 넣습니다. 숫자 키 항목은 항상 병합됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

클래스 병합과 다른 속성 병합을 함께 쓰려면 체이닝도 가능합니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 다른 HTML 요소에서 병합된 속성을 쓰지 않을 경우, [`@class` 디렉티브](#conditional-classes)를 활용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

`merge` 메서드에 클래스가 아닌 속성을 넘기면, 기본값으로 간주되어 기존 속성을 덮어씁니다. 예를 들어 `button` 컴포넌트의 구현은:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시 `type`을 지정하면 해당 값이 적용되고, 지정하지 않으면 기본 `button` 타입이 사용됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```

렌더링 결과는:

```blade
<button type="submit">
    Submit
</button>
```

`class`가 아닌 다른 속성에 기본값과 전달된 값을 결합하려면 `prepends` 메서드를 사용하세요. 예를 들어 `data-controller` 속성이 `profile-controller`로 시작하고, 추가 값이 이어지게 하려면:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 조회 및 필터링

`filter` 메서드는 콜백을 받아 조건에 맞는 속성만 남깁니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith`는 지정 문자열로 시작하는 속성만 가져옵니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

`whereDoesntStartWith`는 지정 문자열로 시작하지 않는 속성을 가져옵니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 첫 번째 속성 값을 가져올 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

컴포넌트에 특정 속성이 존재하는지 여부를 확인하려면 `has` 메서드를 씁니다:

```blade
@if ($attributes->has('class'))
    <div>class 속성이 존재합니다</div>
@endif
```

배열을 넘기면 모든 속성이 존재하는지 판단합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 존재합니다</div>
@endif
```

`hasAny` 메서드는 주어진 속성 중 하나라도 존재하는지 확인합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>속성 중 하나가 존재합니다</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드를 사용하세요:

```blade
{{ $attributes->get('class') }}
```

`only`는 지정한 속성만 반환합니다:

```blade
{{ $attributes->only(['class']) }}
```

`except`는 지정한 속성을 제외한 나머지를 반환합니다:

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어

Blade가 내부적으로 사용하는 몇몇 예약어가 있어, 컴포넌트 클래스 내 public 속성명이나 메서드명으로 사용할 수 없습니다:

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯

컴포넌트에 추가 콘텐츠를 전달할 때 "슬롯"을 사용합니다. 기본 슬롯 내용은 `$slot` 변수로 출력합니다. 예를 들어 `alert` 컴포넌트에 다음 마크업이 있으면:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이렇게 콘텐츠를 전달할 수 있습니다:

```blade
<x-alert>
    <strong>에러!</strong> 문제가 발생했습니다!
</x-alert>
```

여러 슬롯을 지원하려면, 예를 들어 "title" 슬롯을 이렇게 정의할 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯 내용은 `x-slot` 태그로 지정합니다. 명시적 `x-slot`에 없는 내용은 기본 `$slot`에 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        서버 에러
    </x-slot>

    <strong>에러!</strong> 문제가 발생했습니다!
</x-alert>
```

슬롯이 비었는지 확인하려면 `isEmpty` 메서드를 호출할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        슬롯이 비어있을 때 기본 내용입니다.
    @else
        {{ $slot }}
    @endif
</div>
```

또한 `hasActualContent` 메서드로 HTML 주석이 아닌 실제 콘텐츠가 있는지 확인 가능합니다:

```blade
@if ($slot->hasActualContent())
    슬롯에 실제 콘텐츠가 있습니다.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯

Vue 같은 프런트엔드 프레임워크 경험자에게 익숙한 "스코프 슬롯"과 유사합니다. 컴포넌트 내 public 메서드나 속성을 정의하고, 슬롯 내에서 `$component` 변수로 접근해 데이터를 사용할 수 있습니다:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('서버 에러') }}
    </x-slot>

    <strong>에러!</strong> 문제가 발생했습니다!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성

블레이드 컴포넌트처럼 슬롯에도 `class` 같은 추가 속성을 부여할 수 있습니다:

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        제목
    </x-slot>

    내용

    <x-slot:footer class="text-sm">
        푸터
    </x-slot>
</x-card>
```

슬롯의 `attributes` 프로퍼티를 통해 슬롯에 전달된 속성에 접근할 수 있습니다. 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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

매우 작은 컴포넌트는 클래스와 뷰 각각을 관리하는 대신 `render` 메서드에서 직접 마크업을 반환할 수 있습니다:

```php
/**
 * 컴포넌트 뷰 반환
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

인라인 뷰를 렌더링하는 컴포넌트를 만들려면, `make:component` 명령 시 `--inline` 옵션을 사용하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

실행 시점까지 렌더링할 컴포넌트를 모를 때, 내장 `dynamic-component` 컴포넌트를 사용하세요:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 이 수동 등록 방법은 주로 Laravel 패키지 작성 시 필요한 내용입니다. 애플리케이션을 작성 중이라면 이 내용은 건너뛰셔도 무방합니다.

애플리케이션 컴포넌트는 자동 발견되지만, 패키지용 컴포넌트나 비표준 디렉토리 위치 컴포넌트는 수동 등록이 필요합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

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

등록 후 태그 별칭으로 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로딩

`componentNamespace` 메서드로 규칙 기반 자동 로딩도 가능합니다. 예를 들어 `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 `Package\Views\Components` 네임스페이스에 있다면:

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

이렇게 하면 벤더 네임스페이스 구문 `package-name::`로 컴포넌트 사용 가능합니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

컴포넌트 이름에 따라 자동으로 클래스가 매핑되며, 하위 디렉토리는 점(`.`) 표기법으로 지원합니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트처럼, 익명 컴포넌트는 단일 파일로 컴포넌트를 관리하지만, 클래스가 전혀 없습니다. `resources/views/components` 디렉토리에 Blade 템플릿을 두기만 하면 됩니다. 예를 들어 `resources/views/components/alert.blade.php` 파일이 있다면 이 컴포넌트를 이렇게 렌더링할 수 있습니다:

```blade
<x-alert/>
```

컴포넌트가 하위 폴더에 있다면 `.`을 통해 명시할 수 있습니다. 예를 들어 `resources/views/components/inputs/button.blade.php`라면:

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

컴포넌트가 여러 개 템플릿이라면, 컴포넌트 템플릿들을 하나의 디렉토리에 묶고 싶을 수 있습니다. 예를 들어 "accordion" 컴포넌트가 다음과 같이 구조화되어 있다면:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 사용할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 `x-accordion` 컴포넌트를 렌더링하려면 파일명을 `accordion`으로 하위 디렉토리 밖에 둬야 해서 다소 불편합니다. 이를 해결하려면 아래처럼 컴포넌트 디렉토리 안에 루트 컴포넌트를 `accordion.blade.php` 파일명으로 둡니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

이렇게 하면 위 사용법 그대로 유지하되, 컴포넌트 구조는 하위 디렉토리 내에 잘 정리됩니다.

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성들

익명 컴포넌트는 클래스가 없으므로 어떤 데이터가 컴포넌트 변수이고, 어떤 속성이 속성 가방에 들어갈지 구분이 필요합니다.

컴포넌트 템플릿 최상단에 `@props` 디렉티브로 변수 목록과 기본값을 정의하면, 해당 속성은 변수로, 나머지는 속성 가방에 들어갑니다:

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
### 부모 데이터 접근하기

때때로, 부모 컴포넌트 데이터를 자식 컴포넌트에서 접근해야 할 경우가 있습니다. 이럴 때 `@aware` 디렉티브를 사용하세요. 예를 들어, 복잡한 메뉴 컴포넌트 `<x-menu>`와 `<x-menu.item>`가 있을 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` 구현 예시는:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` 속성은 부모에만 전달되어 `<x-menu.item>` 에선 기본적으로 접근할 수 없습니다. 하지만 `@aware`를 이용하면:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

이제 자식 컴포넌트에서도 `color`를 사용할 수 있습니다.

> [!WARNING]
> `@aware`는 부모 컴포넌트에 명시적으로 HTML 속성으로 전달되지 않은 기본 `@props` 값을 액세스할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

보통 익명 컴포넌트는 `resources/views/components` 디렉토리에 둡니다. 하지만 기본 경로 외에 다른 경로를 추가 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 익명 컴포넌트가 위치한 경로(첫 번째 인수)와 선택적인 네임스페이스(두 번째 인수)를 받습니다. 보통 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

이렇게 등록하면, 경로 내의 `panel.blade.php` 컴포넌트를 그냥 `<x-panel />`로 렌더링할 수 있습니다.

네임스페이스 접두사를 지정할 수도 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이 경우 컴포넌트는 다음과 같이 네임스페이스를 포함해서 호출합니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구축

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃

대부분 웹 애플리케이션은 여러 페이지에서 거의 동일한 레이아웃을 공유합니다. 모든 뷰에 레이아웃 HTML을 반복하는 것은 번거롭습니다. 대신, 레이아웃을 하나의 [Blade 컴포넌트](#components)로 정의한 후 애플리케이션 전반에 걸쳐 활용하는 것이 편리합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "할 일(todo)" 목록 앱을 만든다면, 아래와 같은 `layout` 컴포넌트를 정의할 수 있습니다:

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
#### 레이아웃 컴포넌트 사용

레이아웃 컴포넌트를 정의하면, 블레이드 뷰에서 다음과 같이 사용할 수 있습니다. 예를 들어 간단한 작업 리스트를 출력하는 뷰:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트의 기본 슬롯 `$slot`에 컨텐츠가 주입됩니다. 위 레이아웃 컴포넌트는 `$title` 변수도 인식하며, 없으면 기본 타이틀 표시합니다. 뷰에서 아래처럼 명시적 슬롯을 통해 제목을 지정할 수 있습니다:

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

이제 라우트에서 `tasks` 뷰를 반환하면 됩니다:

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

레이아웃은 "템플릿 상속" 방식으로도 만들 수 있습니다. (컴포넌트 도입 전 주로 사용하던 방식)

간단한 예시를 봅시다. 공통 레이아웃을 Blade 뷰로 정의:

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            이곳이 마스터 사이드바입니다.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

여기서 `@section`으로 이름 있는 섹션을 정의하고, `@yield`로 해당 섹션 내용을 출력합니다.

자, 이 레이아웃을 상속하는 자식 페이지도 만들어봅시다.

<a name="extending-a-layout"></a>
#### 레이아웃 상속

자식 뷰에서는 `@extends`로 상속할 레이아웃을 지정하고, `@section`으로 레이아웃의 섹션을 채웁니다. 위 예시에서는 이 섹션들이 `@yield`로 출력됩니다:

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', '페이지 제목')

@section('sidebar')
    @@parent

    <p>마스터 사이드바에 내용 추가</p>
@endsection

@section('content')
    <p>본문 내용입니다.</p>
@endsection
```

`sidebar` 섹션에서는 `@@parent` 디렉티브를 써서 기존 마스터 사이드바 내용을 유지하면서 뒤에 내용을 덧붙였습니다. 렌더링 시 `@@parent`는 레이아웃 쪽 내용을 삽입합니다.

> [!NOTE]
> 이 예시의 `sidebar` 섹션은 `@endsection`으로 닫는데, `@show`와는 달리 즉시 출력하지 않고 정의만 하는 차이가 있습니다.

`@yield` 디렉티브는 두 번째 인수로 기본값도 받을 수 있습니다. 섹션이 없으면 기본값이 출력됩니다:

```blade
@yield('content', '기본 내용입니다')
```

<a name="forms"></a>
## 폼

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때, [CSRF 보호](/docs/master/csrf) 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF 토큰 필드를 포함해야 합니다. `@csrf` 디렉티브로 토큰 필드를 생성하세요:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없기 때문에, 이 HTTP 메서드들을 흉내내기 위한 `_method` 숨겨진 필드를 추가해야 합니다. `@method` 디렉티브로 생성 가능합니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 검증 오류

`@error` 디렉티브를 사용하면, 특정 입력 속성에 대해 [검증 오류 메시지](/docs/master/validation#quick-displaying-the-validation-errors)가 존재하는지 빠르게 확인할 수 있습니다. `@error` 블록 내에서는 `$message` 변수로 오류 메시지를 출력합니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">게시글 제목</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

`@error`는 내부적으로 조건문으로 컴파일되기 때문에, `@else`와 조합해 오류가 없을 때 내용을 출력할 수도 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">이메일 주소</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 폼이 있는 페이지에서 명명된 오류 백을 사용하려면, `@error`의 두 번째 인수로 오류 백 이름을 전달하세요:

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

Blade는 이름 있는 스택을 만들고, 다른 뷰나 레이아웃에서 이 스택에 내용을 푸시(`@push`)하거나 앞에 붙일 수 있습니다. 자식 뷰가 필요한 자바스크립트 라이브러리를 선언할 때 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

불리언 조건에 따라 푸시할 때는 `@pushIf` 디렉티브를 쓰세요:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에 여러 번 푸시할 수 있으며, 전체 스택 내용을 렌더링하려면 `@stack` 디렉티브를 사용합니다:

```blade
<head>
    <!-- 헤드 내용 -->

    @stack('scripts')
</head>
```

스택 맨 앞에 내용을 추가하려면 `@prepend` 디렉티브를 씁니다:

```blade
@push('scripts')
    두 번째 내용입니다...
@endpush

// 나중에...

@prepend('scripts')
    첫 번째 내용입니다...
@endprepend
```

<a name="service-injection"></a>
## 서비스 의존성 주입

`@inject` 디렉티브로 Laravel [서비스 컨테이너](/docs/master/container)에서 서비스를 주입받을 수 있습니다. 첫 번째 인수는 주입된 서비스를 담을 변수명, 두 번째 인수는 서비스 클래스나 인터페이스입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    월별 매출: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

원시 Blade 템플릿 문자열을 HTML로 변환해야 하는 경우, `Blade` 파사드의 `render` 메서드를 사용하세요. 첫 인자는 Blade 템플릿 문자열, 두 번째 인자는 템플릿에 전달할 데이터 배열입니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 렌더링을 위해 `storage/framework/views` 디렉토리에 임시 파일을 생성합니다. 렌더링 후 이 임시 파일을 삭제하려면 `deleteCachedView` 인수를 `true`로 지정하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

[Turbo](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프런트엔드 프레임워크 사용 시 HTTP 응답에 Blade 템플릿 일부만 반환해야 할 때가 있습니다. Blade "프래그먼트"를 사용하면 가능합니다. 먼저 뷰 일부를 `@fragment`와 `@endfragment`로 감쌉니다:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

그리고 이 뷰를 렌더링할 때 `fragment` 메서드로 해당 프래그먼트만 응답으로 보냅니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건에 따라 프래그먼트를 반환할 때는 `fragmentIf`를 쓰고, 조건이 거짓이면 전체 뷰가 반환됩니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 개 프래그먼트를 한 번에 반환하려면 `fragments` 메서드를 사용합니다. 프래그먼트 내용은 모두 이어 붙여 응답됩니다:

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

Blade는 `directive` 메서드를 통해 직접 커스텀 디렉티브를 정의할 수 있습니다. Blade 컴파일러가 커스텀 디렉티브를 발견하면, 정의한 콜백을 호출하며 인수로 디렉티브 표현식을 넘깁니다.

다음 예시는 `@datetime($var)` 라는 디렉티브를 만들어 `$var` (DateTime 인스턴스)의 포맷된 문자열을 반환합니다:

```php
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

이렇게 하면, 아래와 같이 PHP 코드가 생성됩니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브를 수정한 뒤에는 캐시된 Blade 뷰 파일을 모두 삭제해야 합니다. `view:clear` Artisan 명령어를 사용하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러

Blade로 객체를 출력하면 `__toString` 매직 메서드가 호출됩니다. 하지만 제어할 수 없는 서드파티 클래스는 `__toString`을 커스텀할 수 없습니다.

이럴 때 Blade의 `stringable` 메서드를 사용해 해당 타입 객체 출력 방식을 커스터마이징할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에 작성합니다:

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

이제 Blade 템플릿에서 다음과 같이 출력하면:

```blade
Cost: {{ $money }}
```

자동으로 지정한 포맷으로 출력됩니다.

<a name="custom-if-statements"></a>
### 커스텀 If 문

복잡한 커스텀 디렉티브보다 간단한 조건문은 `Blade::if` 메서드로 쉽게 만들 수 있습니다. 예를 들어 애플리케이션 기본 "디스크" 설정을 확인하는 조건을 만든다고 하면:

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

템플릿 내에서 다음처럼 사용할 수 있습니다:

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