# Blade 템플릿

- [소개](#introduction)
    - [Blade를 Livewire로 강화하기](#supercharging-blade-with-livewire)
- [데이터 표시](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [Blade 지시문](#blade-directives)
    - [조건문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함](#including-subviews)
    - [`@once` 지시문](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [수동 컴포넌트 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 Index 컴포넌트](#anonymous-index-components)
    - [데이터 프로퍼티 / 속성](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구축](#building-layouts)
    - [컴포넌트를 활용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 활용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검사 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개

Blade는 Laravel에 내장되어 있는 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과는 다르게 Blade는 템플릿 파일에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어 수정될 때까지 캐시되므로, Blade는 애플리케이션에 사실상 부하를 거의 주지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며, 일반적으로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 통해 반환할 수 있습니다. 물론 [뷰](/docs/{{version}}/views) 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인자를 이용해 데이터를 Blade 뷰로 전달할 수 있습니다.

    Route::get('/', function () {
        return view('greeting', ['name' => 'Finn']);
    });

<a name="supercharging-blade-with-livewire"></a>
### Blade를 Livewire로 강화하기

Blade 템플릿에서 동적 UI를 손쉽게 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면 React나 Vue와 같은 프론트엔드 프레임워크로만 가능했던 동적 기능을 Blade 컴포넌트에 손쉽게 추가할 수 있습니다. 복잡한 빌드 과정이나 클라이언트 렌더링 없이도 현대적이고 반응성이 뛰어난 프론트엔드를 구축할 수 있는 훌륭한 방법입니다.

<a name="displaying-data"></a>
## 데이터 표시

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어 아래와 같은 라우트가 있다고 가정해봅시다.

    Route::get('/', function () {
        return view('welcome', ['name' => 'Samantha']);
    });

`name` 변수의 내용을 다음과 같이 표시할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]  
> Blade의 `{{ }}` 출력문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 통해 자동 인코딩됩니다.

뷰로 전달된 변수만 표시하는 데 제한되지 않습니다. 어떤 PHP 함수의 결과든 출력할 수 있습니다. 실제로 Blade 출력문 내에 원하는 모든 PHP 코드를 쓸 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하고 싶다면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding`을 호출하세요.

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

<a name="displaying-unescaped-data"></a>
#### 이스케이프되지 않은 데이터 표시

기본적으로 Blade `{{ }}` 출력문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 통해 자동 인코딩됩니다. 데이터를 이스케이프하지 않고 표시하려면 아래와 같은 구문을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]  
> 사용자가 입력한 데이터를 그대로 출력할 때는 각별히 주의하세요. 사용자 데이터 표시 시에는 XSS 공격을 방지하기 위해 일반적으로 이스케이프된 이중 중괄호 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 자바스크립트 프레임워크

많은 자바스크립트 프레임워크도 중괄호 `{}`를 사용해 브라우저에 표현식을 렌더링합니다. Blade 렌더러에 해당 표현식을 건드리지 않도록 하려면 `@` 기호를 붙이세요. 예:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예에서 `@` 기호는 Blade가 제거하지만, `{{ name }}` 표현식은 Blade가 손대지 않아 자바스크립트 프레임워크가 렌더링할 수 있습니다.

`@` 기호는 Blade 지시문을 이스케이프하는 데도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

자바스크립트 변수 초기화를 위해 배열을 JSON으로 렌더링해야 할 때가 있습니다.

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

수동으로 `json_encode`를 호출하는 대신 `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 같은 인자와 함께, HTML 속성 내 안전하게 포함될 수 있도록 이스케이프를 보장합니다. 반환 값은 `JSON.parse` JavaScript 문장입니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션에는 이 기능에 편리하게 접근할 수 있도록 `Js` 파사드가 포함되어 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]  
> `Js::from` 메서드는 기존 변수만 JSON으로 렌더링할 때 사용해야 합니다. Blade는 정규식 기반으로 동작하므로 복잡한 표현식을 직접 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시문

템플릿에서 자바스크립트 변수를 대량으로 사용하는 경우 `@verbatim`으로 감싸면 각 Blade 출력문마다 `@`를 붙이지 않아도 됩니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 지시문

템플릿 상속 및 데이터 출력 외에도 Blade는 조건문이나 반복문과 같은 PHP의 제어 구조에 대한 간결하고 직관적인 단축 구문을 제공합니다.

<a name="if-statements"></a>
### 조건문

`@if`, `@elseif`, `@else`, `@endif` 지시문을 사용해 조건문을 만들 수 있습니다. 이 지시문들은 PHP 기본 구조와 동일하게 작동합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의상 Blade에는 `@unless` 지시문도 있습니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

또한, `@isset`과 `@empty` 지시문도 각각 PHP의 `isset`과 `empty` 함수와 같은 용도로 활용할 수 있습니다.

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아님
@endisset

@empty($records)
    // $records가 "empty"임...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 지시문

`@auth` 및 `@guest` 지시문을 사용해 현재 사용자가 [인증](docs/{{version}}/authentication)이 되었는지, 게스트인지 빠르게 확인할 수 있습니다.

```blade
@auth
    // 사용자가 인증됨...
@endauth

@guest
    // 사용자가 인증되지 않음...
@endguest
```

필요하다면, 인증 가드를 지정할 수도 있습니다.

```blade
@auth('admin')
    // 관리자 인증됨...
@endauth

@guest('admin')
    // 관리자 인증 안됨...
@endguest
```

<a name="environment-directives"></a>
#### 환경관련 지시문

`@production` 지시문으로 애플리케이션이 프로덕션 환경에서 실행 중인지 체크할 수 있습니다.

```blade
@production
    // 프로덕션 환경에서만 출력됨...
@endproduction
```

또는 `@env` 지시문을 사용해 특정 환경임을 판단할 수 있습니다.

```blade
@env('staging')
    // 스테이징에서 실행 중...
@endenv

@env(['staging', 'production'])
    // 스테이징 또는 프로덕션...
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시문

템플릿 상속 섹션에 내용이 있는지 `@hasSection`으로 확인할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없음을 확인하려면 `sectionMissing` 지시문을 쓰세요.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 관련 지시문

`@session` 지시문으로 [세션](/docs/{{version}}/session)에 값이 존재하는지 확인할 수 있습니다. 세션 값이 있으면 내부 내용이 실행되며, `$value` 변수로 세션 값을 출력할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시문으로 Switch 문을 구성할 수 있습니다.

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

Blade는 PHP의 반복문 구조와 동일하게 동작하는 반복문용 간단한 지시문을 제공합니다.

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
> `foreach` 반복문에서 [loop 변수](#the-loop-variable)를 사용해 첫 번째, 마지막 반복 여부 등 유용한 정보에 접근할 수 있습니다.

반복문에서 특정 반복을 생략하거나 종료하려면 `@continue`, `@break` 지시문을 사용하세요.

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

조건을 지시문에 직접 넣는 것도 가능합니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 안에서는 `$loop` 변수가 자동 생성됩니다. 현재 인덱스, 첫/마지막 반복 여부 등 다양한 정보를 제공합니다.

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

중첩 반복문의 경우 `parent` 속성을 통해 부모의 `$loop` 변수에 접근할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 객체는 아래와 같은 속성도 제공합니다.

| 속성               | 설명                                         |
|--------------------|---------------------------------------------|
| `$loop->index`     | 현재 반복 인덱스(0부터 시작)                     |
| `$loop->iteration` | 현재 반복 횟수(1부터 시작)                      |
| `$loop->remaining` | 남은 반복 횟수                                 |
| `$loop->count`     | 배열/컬렉션의 총 항목 수                        |
| `$loop->first`     | 첫번째 반복인지 여부                            |
| `$loop->last`      | 마지막 반복인지 여부                            |
| `$loop->even`      | 짝수번째 반복인지 여부                          |
| `$loop->odd`       | 홀수번째 반복인지 여부                          |
| `$loop->depth`     | 중첩 반복의 깊이                                |
| `$loop->parent`    | 중첩 반복문에서 부모 반복문의 loop 객체          |

<a name="conditional-classes"></a>
### 조건부 클래스 & 스타일

`@class` 지시문은 조건에 따라 CSS 클래스를 조합할 수 있습니다. 배열의 키는 클래스명, 값은 불린 식입니다. 숫자 키는 항상 포함됩니다.

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

비슷하게, `@style` 지시문으로 조건부 인라인 스타일도 추가할 수 있습니다.

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

HTML 체크박스의 체크 여부를 간편하게 표시하려면 `@checked` 지시문을 사용하세요. 조건이 true면 `checked`를 출력합니다.

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

셀렉트 옵션의 선택 여부는 `@selected` 지시문으로 처리할 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, `@disabled`(비활성화), `@readonly`(읽기전용), `@required`(필수) 지시문도 사용할 수 있습니다.

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
### 서브뷰 포함

> [!NOTE]  
> `@include`를 사용할 수 있지만, Blade [컴포넌트](#components)는 데이터 및 속성 바인딩 등 여러 장점이 있습니다.

`@include` 지시문을 사용하면 다른 Blade 뷰를 포함할 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서도 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

별도로 데이터를 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include`하면 에러가 발생합니다. 뷰 존재 여부에 따라 포함하고 싶다면 `@includeIf`를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

주어진 불린 값에 따라 포함할 뷰를 결정하고 싶을 때는 `@includeWhen`, `@includeUnless`를 사용합니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중 존재하는 첫 번째 뷰만 포함하려면 `includeFirst` 지시문을 사용하세요.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]  
> Blade 뷰에서 `__DIR__`, `__FILE__` 상수 사용은 피하세요. 이는 캐시된 뷰 파일 경로를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션의 뷰 렌더링

반복과 include를 한 줄로 합쳐 작성할 때는 `@each` 지시문을 사용하세요.

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 렌더링할 뷰, 두 번째는 반복 대상 배열/컬렉션, 세 번째는 뷰 내부에서 접근할 변수명입니다. 현재 반복의 배열 키는 `key`로 전달됩니다.

배열이 비어있을 때 렌더링할 뷰도 네 번째 인자로 지정할 수 있습니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]  
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 필요하다면 `@foreach`와 `@include`를 함께 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시문

`@once` 지시문을 사용하면 한 번만 렌더링되어야 하는 템플릿 일부를 정의할 수 있습니다. [스택](#stacks)과 함께 JS 코드를 한번만 포함할 때 등 유용합니다.

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 JavaScript...
        </script>
    @endpush
@endonce
```

자주 `@push` 또는 `@prepend`와 함께 사용하므로, `@pushOnce`, `@prependOnce`도 사용할 수 있습니다.

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### Raw PHP

Blade 뷰에서 PHP 코드를 실행하려면 `@php` 지시문을 사용하세요.

```blade
@php
    $counter = 1;
@endphp
```

클래스 임포트 정도만 필요하다면 `@use` 지시문을 사용하세요.

```blade
@use('App\Models\Flight')
```

별칭을 주고 싶다면 두 번째 인자를 사용합니다.

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
### 주석

Blade 주석은 렌더링된 HTML에 포함되지 않습니다.

```blade
{{-- 이 주석은 렌더링 결과에 나타나지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트

컴포넌트와 슬롯은 섹션, 레이아웃, include와 유사한 이점을 제공하지만, A/B 직접적인 사용 감각에서 더 익숙할 수 있습니다. 컴포넌트에는 클래스 기반과 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` 아티즌 명령어를 사용하세요. 예시로 간단한 `Alert` 컴포넌트를 만들어보겠습니다.

```shell
php artisan make:component Alert
```

위 명령은 `app/View/Components`에 컴포넌트 클래스를 생성하고, `resources/views/components`에 뷰를 생성합니다. 여러분이 직접 만드는 컴포넌트는 별도의 등록과정 없이 자동으로 인식됩니다.

서브디렉터리 내에 컴포넌트도 생성할 수 있습니다.

```shell
php artisan make:component Forms/Input
```

위 명령어는 `app/View/Components/Forms/Input.php`와 `resources/views/components/forms/input.blade.php`를 만듭니다.

클래스 없이 Blade 뷰 파일만 있는 익명 컴포넌트는 `--view` 플래그로 생성할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

이렇게 생성된 컴포넌트는 `<x-forms.input />`로 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

직접 만든 앱 컴포넌트는 자동으로 등록되지만, 패키지 개발 시에는 수동으로 컴포넌트 클래스와 HTML 태그 별칭을 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다.

    use Illuminate\Support\Facades\Blade;

    /**
     * 패키지 서비스 부트스트랩
     */
    public function boot(): void
    {
        Blade::component('package-alert', Alert::class);
    }

등록 후에는 다음과 같이 태그로 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

또는 `componentNamespace`를 사용하여 네임스페이스별로 컴포넌트를 자동 등록할 수 있습니다.

    use Illuminate\Support\Facades\Blade;

    public function boot(): void
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

이렇게 하면 다음과 같이 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 명을 파스칼케이스로 변환하여 연결합니다. 서브디렉터리는 dot 표기법을 사용합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 표시하려면 Blade 템플릿 내에 `x-`로 시작하는 컴포넌트 태그를 사용하세요.

```blade
<x-alert/>

<x-user-profile/>
```

`app/View/Components`의 서브디렉터리에 위치한 컴포넌트는 `.`으로 경로를 명시할 수 있습니다.

```blade
<x-inputs.button/>
```

`shouldRender` 메서드가 false를 반환하면 해당 컴포넌트는 표시되지 않습니다.

    /**
     * 컴포넌트 표시 여부
     */
    public function shouldRender(): bool
    {
        return Str::length($this->message) > 0;
    }

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달

HTML 속성을 통해 데이터를 전달할 수 있습니다. 고정 값은 그대로, PHP 변수나 식은 `:` 접두사를 씁니다.

```blade
<x-alert type="error" :message="$message"/>
```

모든 데이터 속성은 클래스 생성자에 정의해야 하며, public 프로퍼티는 컴포넌트 뷰에서 그대로 사용할 수 있습니다.

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
         * 컴포넌트 뷰 반환
         */
        public function render(): View
        {
            return view('components.alert');
        }
    }

컴포넌트가 렌더링되면 public 변수명을 그대로 이용해 값을 뷰에서 출력할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 네이밍 케이스

컴포넌트 생성자 인자는 `camelCase`로 작성하고, HTML 속성 참조시에는 `kebab-case`를 사용합니다. 예:

    public function __construct(
        public string $alertType,
    ) {}

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 단축 속성 구문

변수명과 속성명이 동일할 때 단축 구문을 사용할 수 있습니다.

```blade
{{-- 단축 구문 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JS 프레임워크의 콜론 접두사 속성과 충돌을 피하려면 `::`(이중콜론)으로 Blade에 PHP 표현식이 아님을 알릴 수 있습니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade가 렌더링하면

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

public 메서드도 템플릿에서 호출 가능합니다. 예:

    public function isSelected(string $option): bool
    {
        return $option === $this->selected;
    }

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내 속성 및 슬롯 접근

컴포넌트 클래스의 `render`에서 클로저를 반환하면 컴포넌트명, 속성, 슬롯 등에 접근할 수 있습니다.

    use Closure;

    public function render(): Closure
    {
        return function (array $data) {
            // $data['componentName'];
            // $data['attributes'];
            // $data['slot'];

            return '<div>Components content</div>';
        };
    }

클로저 반환 문자열이 뷰 파일이면 뷰가, 아니면 인라인 Blade 뷰로 해석됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

[서비스 컨테이너](/docs/{{version}}/container)에서 의존성을 자동 주입받으려면 데이터 속성 앞에 의존성을 나열하세요.

```php
use App\Services\AlertCreator;

public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성/메서드 노출 제외

컴포넌트 템플릿에 노출하고 싶지 않은 public 메서드나 프로퍼티가 있다면, `$except` 프로퍼티에 배열로 나열하세요.

    class Alert extends Component
    {
        /**
         * 템플릿에 노출하지 않을 속성/메서드
         *
         * @var array
         */
        protected $except = ['type'];
    }

<a name="component-attributes"></a>
### 컴포넌트 속성

컴포넌트에 데이터 외의 추가 HTML 속성(예: class)을 전달할 때, 생성자에 정의되지 않은 속성은 자동으로 `$attributes` 속성에 저장됩니다. 이 속성은 컴포넌트 뷰에서 출력할 수 있습니다.

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]  
> `@env` 등 지시문을 컴포넌트 태그 내에서 사용하는 것은 지원하지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 값/병합 속성

속성의 기본값을 설정하거나, CSS 클래스 병합이 필요하면 `merge` 메서드를 사용하세요.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

다음과 같이 사용하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

결과는:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건부로 클래스를 병합하려면 `class` 메서드를 활용하세요.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성 추가가 필요하면 체이닝 가능합니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]  
> 병합 속성을 사용하지 않는 요소의 조건부 클래스는 [`@class` 지시문](#conditional-classes)을 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스 이외 속성 병합

클래스 이외의 속성 병합 시, merge 값은 기본값으로 적용되고, 전달된 속성이 있으면 덮어쓰기됩니다. 예:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

사용 예시:

```blade
<x-button type="submit">
    Submit
</x-button>
```

결과:

```blade
<button type="submit">
    Submit
</button>
```

클래스 이외에도 기본값과 추가값을 이어붙이고 싶으면 `prepends`를 사용할 수 있습니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 검색

`filter`로 속성을 필터링할 수 있습니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

`whereStartsWith`로 특정 접두사의 속성만, `whereDoesntStartWith`로 제외한 속성을 가져올 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 첫 번째 속성을 가져옵니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성 존재 여부는 `has`를 사용합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

여러 속성 모두가 존재하는지 확인할 수도 있습니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

`hasAny`는 하나라도 존재하면 true를 반환합니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

특정 속성의 값을 받을 때는 `get`을 사용합니다.

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 예약어

일부 키워드는 Blade 내부에서 예약되어 있습니다. 다음 키워드는 public 속성 또는 메서드로 정의할 수 없습니다.

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

컴포넌트에 컨텐츠를 전달해야 할 때 "슬롯"을 사용합니다. 컴포넌트 내부에서는 `$slot`으로 렌더링할 수 있습니다. 예:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

사용법:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

다중 슬롯이 필요한 경우, 명명된 슬롯(namaed slot)을 정의할 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯은 `x-slot` 태그로 전달할 수 있습니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 비었는지 확인하려면 `isEmpty`를 쓰세요.

```blade
@if ($slot->isEmpty())
    This is default content if the slot is empty.
@else
    {{ $slot }}
@endif
```

HTML 주석이 아닌 "실제" 컨텐츠 포함 여부는 `hasActualContent`로 확인합니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### Scoped 슬롯

Vue 등에서 본 것처럼, 컴포넌트 내부의 데이터/메서드를 슬롯에서 접근하려면, 컴포넌트의 public 메서드·속성에 `$component`로 접근할 수 있습니다.

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

슬롯에도 추가 [속성](#component-attributes)을 부여할 수 있습니다.

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

슬롯 속성에 접근하려면 변수가 가진 `attributes` 속성을 사용하세요.

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

작은 컴포넌트는 클래스와 뷰 파일을 따로 관리하는 것이 번거로울 수 있습니다. 이럴 땐 `render`에서 직접 마크업을 반환할 수 있습니다.

    public function render(): string
    {
        return <<<'blade'
            <div class="alert alert-danger">
                {{ $slot }}
            </div>
        blade;
    }

<a name="generating-inline-view-components"></a>
#### 인라인 뷰 컴포넌트 생성

`make:component` 명령에 `--inline` 옵션을 사용하세요.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

런타임에 렌더링할 컴포넌트를 결정해야 한다면, `x-dynamic-component`를 사용할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 수동 컴포넌트 등록

> [!WARNING]  
> 수동 컴포넌트 등록 문서는 Laravel 패키지 개발자에게만 해당합니다. 일반 앱 개발 시 자동 등록됩니다.

직접 만든 컴포넌트는 자동으로 등록되지만, 패키지 또는 비정형 디렉터리에 둘 때는 수동 등록이 필요합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 아래처럼 등록하세요.

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    public function boot(): void
    {
        Blade::component('package-alert', AlertComponent::class);
    }

등록 후에는 다음처럼 사용합니다.

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 등록

네임스페이스 컨벤션 기반 자동 로딩도 지원합니다.

    use Illuminate\Support\Facades\Blade;

    public function boot(): void
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

이렇게 하면

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

와 같이 렌더링할 수 있습니다. 파스칼케이스 변환/서브디렉터리(dot 표기법) 지원.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 유사하게 익명 컴포넌트는 단일 Blade 파일로 관리하며, 클래스가 필요 없습니다. `resources/views/components` 디렉터리에 Blade 파일만 있으면 됩니다.

예:

```blade
<x-alert/>
```

서브디렉터리 구조도 `.`으로 렌더링합니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 익명 Index 컴포넌트

여러 Blade 파일로 구성된 컴포넌트를 관리하려면 그 컴포넌트 전용 디렉터리에 `index.blade.php`를 두면 됩니다.

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

아래처럼 사용:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<a name="data-properties-attributes"></a>
### 데이터 프로퍼티 / 속성

익명 컴포넌트에는 클래스가 없으니, 상위에 `@props` 지시문을 사용해 데이터 변수를 지정합니다. 나머지는 [속성 백](#component-attributes)으로 전달됩니다. 기본값은 배열로 지정할 수 있습니다.

```blade
@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

사용 예시:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근

자식 컴포넌트에서 부모 데이터를 사용하려면 `@aware`를 활용합니다.

부모:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`menu/index.blade.php`:

```blade
@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

자식(`menu/item.blade.php`)에서:

```blade
@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]  
> `@aware`는 부모에게 HTML 속성으로 명시적으로 전달된 데이터만 접근 가능하며, 부모의 `@props` 기본값에는 접근 불가합니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

기본 디렉터리 외 추가 익명 컴포넌트 경로를 등록할 수 있습니다.

    Blade::anonymousComponentPath(__DIR__.'/../components');
    Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');

등록된 경로에 파일이 있으면 접두사 없이, 네임스페이스가 있으면 아래처럼 렌더링합니다.

```blade
<x-panel />
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구축

<a name="layouts-using-components"></a>
### 컴포넌트를 활용한 레이아웃

웹 앱은 여러 페이지에 공통 레이아웃을 가집니다. 매번 전체 HTML을 반복하는 것은 비효율적이므로, Blade [컴포넌트](#components)로 레이아웃을 정의해 재사용하는 것이 좋습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "todo" 앱이라면 아래처럼 구성할 수 있습니다.

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

아래처럼 활용:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

`$slot`에 전달된 내용이 레이아웃에 삽입됩니다. `$title` 슬롯이 있다면 제목을 커스텀할 수도 있습니다.

```blade
<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

라우트 등록:

    use App\Models\Task;

    Route::get('/tasks', function () {
        return view('tasks', ['tasks' => Task::all()]);
    });

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 활용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의

컴포넌트 도입 전에는 템플릿 상속이 표준적인 방법이었습니다.

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

`@section`은 내용을 정의, `@yield`는 해당 섹션을 표시합니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

자식 뷰에서는 `@extends`로 레이아웃을 상속받고, `@section`으로 내용을 오버라이드합니다.

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

`@@parent`는 부모(마스터)가 정의한 sidebar 내용 뒤에 추가할 때 사용합니다.

> [!NOTE]  
> 이전 예제와 달리 `sidebar`가 `@endsection`으로 끝나는데, `@endsection`은 섹션만 정의하고, `@show`는 즉시 표시합니다.

`@yield`는 두 번째 인자를 통해 기본값 지정도 지원합니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼(Forms)

<a name="csrf-field"></a>
### CSRF 필드

HTML 폼을 작성할 때는 CSRF 보호 미들웨어를 위해 숨겨진 CSRF 토큰 필드를 넣어야 합니다. `@csrf` 지시문을 사용하세요.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### 메서드 필드

HTML 폼은 PUT, PATCH, DELETE를 지원하지 않으므로, `_method` 필드를 추가해 요청 메서드를 속일 수 있습니다. `@method` 지시문을 이용하세요.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검사 오류

`@error` 지시문으로 [유효성 검사 메시지](/docs/{{version}}/validation#quick-displaying-the-validation-errors)가 있는지 빠르게 확인할 수 있습니다. `@error` 내부에서는 `$message`로 오류 메시지를 출력합니다.

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

`@else`를 활용해 에러 미존재시 처리도 가능합니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

[오류백을 지정](docs/{{version}}/validation#named-error-bags)할 수도 있습니다.

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

Blade는 이름이 지정된 스택에 여러 뷰나 레이아웃에서 내용을 push/렌더링할 수 있도록 지원합니다. 이 기능은 자식 뷰에서 필요한 JS 라이브러리를 명시할 때 유용합니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

조건부로 push하려면 `@pushIf` 지시문을 사용합니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

스택에 여러 번 push할 수 있으며, 렌더링 위치에서 `@stack`으로 출력합니다.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

스택 맨 앞에 추가하려면 `@prepend`를 사용합니다.

```blade
@push('scripts')
    This will be second...
@endpush

// 이후...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입

`@inject` 지시문으로 Laravel [서비스 컨테이너](/docs/{{version}}/container)에서 서비스를 주입받을 수 있습니다. 첫 인자는 사용할 변수명, 두 번째는 클래스 또는 인터페이스 명입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 Blade 템플릿 렌더링

원시 Blade 문자열을 HTML로 변환해야 할 때는 `Blade` 파사드의 `render` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Blade는 임시 파일을 `storage/framework/views`에 저장합니다. 렌더 후 임시파일을 삭제하려면 `deleteCachedView` 옵션을 활용하세요.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Blade 프래그먼트 렌더링

[Tubro](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 등 프론트엔드 프레임워크에서 뷰의 일부만 HTTP 응답에 포함해야 할 때가 있습니다. 이럴 때 Blade `@fragment`/`@endfragment`로 프래그먼트를 지정할 수 있습니다.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

뷰 렌더시 `fragment` 메서드로 해당 프래그먼트만 포함시키세요.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

조건부 프래그먼트는 `fragmentIf` 메서드를 사용합니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

여러 프래그먼트는 `fragments`/`fragmentsIf`로 반환할 수 있습니다.

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

`directive` 메서드로 사용자 정의 지시문을 만들 수 있습니다. Blade가 해당 지시문을 만나면 지정한 콜백을 호출합니다.

아래는 `@datetime($var)` 지시문을 만드는 예입니다. `$var`는 `DateTime` 인스턴스여야 하며, 지정된 형식으로 출력됩니다.

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        public function register(): void
        {
            // ...
        }

        public function boot(): void
        {
            Blade::directive('datetime', function (string $expression) {
                return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
            });
        }
    }

이렇게 정의하면 Blade는 다음과 같은 PHP로 변환합니다.

    <?php echo ($var)->format('m/d/Y H:i'); ?>

> [!WARNING]  
> Blade 지시문의 코드를 수정하면 캐시된 Blade 뷰를 삭제해야 합니다. `view:clear` 아티즌 명령으로 삭제하세요.

<a name="custom-echo-handlers"></a>
### 커스텀 Echo 핸들러

Blade에서 객체를 `{{ }}`로 출력하면 해당 객체의 `__toString`이 호출됩니다. 하지만 서드파티 라이브러리 등에서 `__toString`을 제어하지 못하는 경우, `stringable`로 커스텀 핸들러를 등록할 수 있습니다.

    use Illuminate\Support\Facades\Blade;
    use Money\Money;

    public function boot(): void
    {
        Blade::stringable(function (Money $money) {
            return $money->formatTo('en_GB');
        });
    }

등록하면 Blade 템플릿에서 그대로 출력 가능합니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

간단한 커스텀 조건문 정의에는 `Blade::if`를 사용할 수 있습니다. 예를 들어 "기본 디스크"를 판별하는 조건문을 만든다면:

    use Illuminate\Support\Facades\Blade;

    public function boot(): void
    {
        Blade::if('disk', function (string $value) {
            return config('filesystems.default') === $value;
        });
    }

사용 예시:

```blade
@disk('local')
    <!-- local 디스크 사용 중 -->
@elsedisk('s3')
    <!-- s3 디스크 사용 중... -->
@else
    <!-- 기타 디스크 사용 중... -->
@enddisk

@unlessdisk('local')
    <!-- local 디스크가 아님... -->
@enddisk
```
