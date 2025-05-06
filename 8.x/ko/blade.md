# Blade 템플릿

- [소개](#introduction)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [컴포넌트로 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약 키워드](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [익명 컴포넌트](#anonymous-components)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [레이아웃 구축](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메소드 필드](#method-field)
    - [유효성 검사 에러](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [Blade 확장](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 포함되어 있는 간결하고 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿에서 순수 PHP 코드의 사용을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 순수 PHP 코드로 컴파일되고 수정될 때까지 캐싱되어, Blade가 애플리케이션에 실질적으로 오버헤드를 거의 추가하지 않음을 의미합니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 보통 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론, [뷰](https://laravel.com/docs/{{version}}/views) 문서에서 언급했듯이, `view` 헬퍼의 두 번째 인자를 사용해 Blade 뷰로 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

> {tip} Blade 템플릿의 한계를 넘어 동적인 인터페이스를 쉽고 빠르게 만들고 싶으신가요? [Laravel Livewire](https://laravel-livewire.com)를 확인해보세요.

<a name="displaying-data"></a>
## 데이터 표시

Blade 뷰에 전달된 변수를 중괄호로 감싸서 데이터를 출력할 수 있습니다. 다음과 같은 라우트가 있다고 가정해봅시다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 출력할 수 있습니다:

```php
Hello, {{ $name }}.
```

> {tip} Blade의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 자동으로 거쳐 출력됩니다.

뷰에 전달된 변수 출력에만 한정되지 않고, PHP 함수의 결과값이나 원하는 어떤 PHP 코드도 Blade 에코 구문(`{{ }}`)에 작성할 수 있습니다:

```php
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 헬퍼)는 HTML 엔티티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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
#### 이스케이프되지 않은 데이터 출력

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 처리됩니다. 데이터 이스케이프를 원하지 않는 경우, 다음 구문을 사용하세요:

```php
Hello, {!! $name !!}.
```

> {note} 사용자 입력값을 출력할 때에는 반드시 주의해야 합니다. 대부분의 경우, 사용자 입력값을 화면에 표시할 땐 이스케이프된 `{{ }}` 구문을 활용해 XSS 공격을 예방해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크

많은 JavaScript 프레임워크도 중괄호(`{}`)로 표현식을 표시하므로, Blade 렌더러에게 해당 표현식을 건드리지 말라고 `@` 기호를 접두사로 붙여 사용할 수 있습니다. 예시:

```php
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예제에서 `@` 기호는 Blade가 제거하지만, `{{ name }}` 표현식은 Blade가 변형하지 않아 JavaScript 프레임워크에서 렌더링할 수 있습니다.

`@` 기호는 Blade 디렉티브의 이스케이프에도 사용할 수 있습니다:

```php
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

JavaScript 변수를 초기화하기 위해 배열을 뷰에 전달하여 JSON으로 렌더링해야 하는 경우가 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 사용하기보다, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode`와 동일한 인자를 받고, HTML 인용부호 내에 안전하게 JSON을 인코딩합니다. 반환값은 유효한 JavaScript 객체로 변환되는 `JSON.parse` 구문입니다:

```php
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 버전의 Laravel 애플리케이션 스켈레톤에는 이 기능을 Blade 템플릿에서 편리하게 사용할 수 있도록 하는 `Js` 파사드가 포함되어 있습니다:

```php
<script>
    var app = {{ Js::from($array) }};
</script>
```

> {note} `Js::from`은 반드시 기존 변수를 JSON으로 렌더링할 때만 사용하세요. Blade 템플릿 엔진은 정규표현식 기반이므로 복잡한 표현식을 이 디렉티브에 넘기면 예기치 않은 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 여러 부분에서 JavaScript 변수를 출력해야 할 때, 각 Blade 에코 구문 앞에 `@`를 붙이는 번거로움을 피하기 위해, `@verbatim` 디렉티브로 HTML을 감쌀 수 있습니다:

```php
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브

템플릿 상속이나 데이터 표시 외에도, Blade는 조건문이나 반복문과 같은 PHP의 일반적인 제어 구조를 위한 짧고 간결한 문법을 제공합니다. 이러한 단축 구문은 기존 PHP와 익숙한 구조와 동시에 코드를 깔끔하게 작성할 수 있게 해줍니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 디렉티브로 `if` 문을 작성할 수 있습니다. 동작은 PHP의 `if` 문과 동일합니다:

```php
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해, Blade는 `@unless` 구문도 제공합니다:

```php
@unless (Auth::check())
    You are not signed in.
@endunless
```

또한 `@isset`, `@empty` 디렉티브를 각각 PHP의 `isset` 및 `empty` 함수처럼 사용할 수 있습니다:

```php
@isset($records)
    // $records는 정의되어 있고 null이 아님
@endisset

@empty($records)
    // $records가 "비어 있음"
@endempty
```

<a name="authentication-directives"></a>
#### 인증 디렉티브

`@auth`와 `@guest` 디렉티브를 사용해 현재 사용자가 [인증](https://laravel.com/docs/{{version}}/authentication)되었는지 또는 게스트인지 쉽게 판단할 수 있습니다:

```php
@auth
    // 사용자가 인증됨
@endauth

@guest
    // 사용자가 인증되지 않음
@endguest
```

필요에 따라 인증 가드를 지정할 수도 있습니다:

```php
@auth('admin')
    // 관리자로 인증됨
@endauth

@guest('admin')
    // 관리자로 인증되지 않음
@endguest
```

<a name="environment-directives"></a>
#### 환경 디렉티브

`@production` 디렉티브로 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다:

```php
@production
    // 프로덕션 전용 내용
@endproduction
```

또는, `@env` 디렉티브로 특정 환경에서 실행 중인지 확인할 수 있습니다:

```php
@env('staging')
    // 현재 "staging" 환경
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경
@endenv
```

<a name="section-directives"></a>
#### Section 디렉티브

템플릿 상속용 section에 내용이 있는지 `@hasSection` 디렉티브로 확인할 수 있습니다:

```html
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

`sectionMissing` 디렉티브로 section이 비어있는지도 확인할 수 있습니다:

```html
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브로 Switch 문을 작성할 수 있습니다:

```php
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

Blade는 PHP의 반복문을 사용할 수 있도록 간단한 디렉티브를 제공합니다. 각 디렉티브는 PHP와 동일하게 동작합니다:

```php
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

> {tip} `foreach` 반복문 내에서는 [loop 변수](#the-loop-variable)를 사용해 첫 번째/마지막 반복 여부 등 유용한 정보를 얻을 수 있습니다.

반복문 중간에 반복을 건너뛰거나 종료하고 싶을 때는 `@continue`와 `@break` 디렉티브를 사용할 수 있습니다:

```php
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

조건을 바로 디렉티브에 포함시킬 수도 있습니다:

```php
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 루프를 반복하는 동안, `$loop` 변수가 루프 내부에서 사용 가능합니다. 이를 통해 현재 인덱스, 첫/마지막 반복 여부 등 다양한 정보를 얻을 수 있습니다:

```php
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

중첩된 반복문에서는 부모 반복문의 `$loop` 변수에 `parent` 속성으로 접근할 수 있습니다:

```php
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 다양한 속성:

| 속성                | 설명                                               |
|---------------------|---------------------------------------------------|
| `$loop->index`      | 현재 반복의 인덱스(0부터 시작)                     |
| `$loop->iteration`  | 현재 반복 회수(1부터 시작)                         |
| `$loop->remaining`  | 반복문에서 남은 횟수                              |
| `$loop->count`      | 배열 또는 컬렉션의 전체 항목 개수                 |
| `$loop->first`      | 첫 번째 반복인지 여부                              |
| `$loop->last`       | 마지막 반복인지 여부                               |
| `$loop->even`       | 짝수 번째 반복인지 여부                            |
| `$loop->odd`        | 홀수 번째 반복인지 여부                            |
| `$loop->depth`      | 현재 반복의 중첩 깊이                               |
| `$loop->parent`     | 중첩 루프의 경우, 부모 루프의 `$loop` 변수        |

<a name="conditional-classes"></a>
### 조건부 클래스

`@class` 디렉티브는 CSS 클래스 문자열을 조건부로 컴파일합니다. 배열의 키는 추가하고자 하는 클래스, 값은 조건문입니다. 만약 키가 숫자라면 항상 포함됩니다:

```php
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

<a name="including-subviews"></a>
### 서브뷰 포함하기

> {tip} `@include` 디렉티브를 자유롭게 사용할 수 있지만, Blade의 [컴포넌트](#components)는 데이터와 속성 바인딩 등 여러 장점을 제공하므로 더욱 권장됩니다.

`@include` 디렉티브로 한 Blade 뷰에서 다른 뷰를 쉽게 포함할 수 있습니다. 부모 뷰의 모든 변수는 포함된 뷰에서도 사용할 수 있습니다:

```html
<div>
    @include('shared.errors')

    <form>
        <!-- Form 내용 -->
    </form>
</div>
```

포함되는 뷰에 추가 데이터를 넘기고 싶다면 배열로 전달 가능합니다:

```php
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하려 하면 Laravel은 오류를 발생시킵니다. 뷰가 없어도 오류 없이 진행하고 싶다면 `@includeIf`를 사용하세요:

```php
@includeIf('view.name', ['status' => 'complete'])
```

불리언 값을 기준으로 포함 여부를 다르게 하고 싶다면 `@includeWhen`이나 `@includeUnless`를 사용할 수 있습니다:

```php
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 하나라도 존재하면 가장 먼저 발견되는 뷰를 포함하려면 `includeFirst` 디렉티브를 사용하세요:

```php
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> {note} Blade 뷰에서는 `__DIR__`, `__FILE__` 등의 상수 사용을 피하세요. 컴파일/캐시된 뷰 위치를 가리키게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션을 위한 뷰 렌더링

반복문과 포함을 조합해, `@each` 디렉티브로 한줄에 간단하게 작성할 수 있습니다:

```php
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 렌더링할 뷰, 두 번째는 반복 처리할 배열 혹은 컬렉션, 세 번째는 뷰에서 사용할 반복 변수명입니다. 키는 `key` 변수로도 접근할 수 있습니다.

네 번째 인자를 추가로 줄 경우, 배열이 비었을 때 렌더링할 뷰를 지정할 수 있습니다:

```php
@each('view.name', $jobs, 'job', 'view.empty')
```

> {note} `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속받지 않습니다. 이런 경우 `@foreach`와 `@include`를 사용하세요.

<a name="the-once-directive"></a>
### `@once` 디렉티브

`@once` 디렉티브로 렌더링 사이클마다 한 번만 실행되는 부분을 정의할 수 있습니다. 예를 들어 반복되는 [컴포넌트](#components) 내에서 JavaScript를 헤더에 한 번만 추가하고 싶을 때 유용합니다:

```php
@once
    @push('scripts')
        <script>
            // 커스텀 JavaScript
        </script>
    @endpush
@endonce
```

<a name="raw-php"></a>
### Raw PHP

Blade `@php` 디렉티브를 사용해 뷰 내에 순수 PHP 코드를 직접 실행할 수 있습니다:

```php
@php
    $counter = 1;
@endphp
```

<a name="comments"></a>
### 주석

Blade는 HTML 주석과 달리, 렌더된 HTML에 포함되지 않는 Blade 전용 주석을 지원합니다:

```php
{{-- 이 주석은 렌더된 HTML에 포함되지 않습니다 --}}
```

---

**나머지 내용(컴포넌트, 레이아웃, 폼, 스택, 서비스 주입, Blade 확장 등)은 글이 매우 길어 연속 답변으로 제공해야 합니다. 계속 번역을 원하시면 요청해 주세요.**