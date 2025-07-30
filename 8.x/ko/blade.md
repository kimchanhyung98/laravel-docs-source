# Blade 템플릿 (Blade Templates)

- [소개](#introduction)
- [데이터 출력하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [Blade 지시어](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [루프 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
    - [원시 PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링하기](#rendering-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [익명 컴포넌트](#anonymous-components)
    - [동적 컴포넌트](#dynamic-components)
    - [수동으로 컴포넌트 등록하기](#manually-registering-components)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [HTTP 메서드 필드](#method-field)
    - [검증 오류 표시](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [Blade 확장하기](#extending-blade)
    - [맞춤형 에코 핸들러](#custom-echo-handlers)
    - [맞춤형 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본으로 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 내에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어 캐싱되며, 수정 전까지 재컴파일되지 않기 때문에 애플리케이션에 거의 부담을 주지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 일반적으로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 전역 헬퍼 함수 `view`를 통해 라우트나 컨트롤러에서 반환할 수 있습니다. 물론 [뷰 문서](/docs/{{version}}/views)에서 설명하듯이, `view` 헬퍼의 두 번째 인수를 통해 데이터를 뷰에 전달할 수 있습니다:

```
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

> [!TIP]
> Blade 템플릿을 한 단계 업그레이드하여 동적 인터페이스를 쉽게 구축하고 싶다면 [Laravel Livewire](https://laravel-livewire.com)를 참고하세요.

<a name="displaying-data"></a>
## 데이터 출력하기 (Displaying Data)

Blade 뷰에 전달된 데이터를 출력하려면 변수를 중괄호로 감싸면 됩니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해봅시다:

```
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 출력할 수 있습니다:

```
Hello, {{ $name }}.
```

> [!TIP]
> Blade의 `{{ }}` 구문은 자동으로 PHP의 `htmlspecialchars` 함수를 거쳐 XSS 공격을 방지합니다.

뷰에 전달된 변수뿐 아니라, PHP 함수의 결과도 출력할 수 있습니다. 실제로 Blade 에코 구문 안에는 어떤 PHP 코드든 넣을 수 있습니다:

```
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로 Blade (및 Laravel의 `e` 헬퍼)는 HTML 엔티티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
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
#### 이스케이프되지 않은 데이터 출력하기

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격 방지를 위해 자동으로 `htmlspecialchars` 함수를 적용합니다. 만약 데이터를 이스케이프하지 않고 그대로 출력하고 싶다면 다음과 같은 문법을 사용하세요:

```
Hello, {!! $name !!}.
```

> [!NOTE]
> 사용자가 입력한 데이터는 XSS 공격의 위험이 있으니 매우 주의해서 출력해야 합니다. 일반적으로는 이스케이프가 적용되는 중괄호 2개 구문을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 자바스크립트 프레임워크 (Blade & JavaScript Frameworks)

많은 자바스크립트 프레임워크에서도 중괄호(`{{ }}`)를 표현식 출력 표시로 사용합니다. 이렇게 표현식이 Blade와 충돌할 경우, Blade에게 해당 표현식을 건드리지 말라고 알려주는 `@` 기호를 쓸 수 있습니다. 예를 들어:

```
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 예제에서 `@` 기호는 Blade가 제거하지만 `{{ name }}`는 Blade가 건드리지 않고 그대로 출력하므로, 자바스크립트 프레임워크가 이를 해석해 렌더링할 수 있게 됩니다.

`@` 기호는 Blade 지시어를 이스케이프 하는 용도로도 사용 가능합니다:

```
{{-- Blade 템플릿 --}}
@@if()

<!-- HTML 출력 결과 -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

뷰에 전달한 배열을 JSON으로 변환해 자바스크립트 변수 초기화에 사용하고 싶을 때가 있습니다. 이때 보통 다음과 같이 작성할 수 있습니다:

```
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

하지만 수동으로 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. `from` 메서드는 `json_encode`와 동일한 인수를 받으며 HTML 내에서 안전하게 인코딩된 JSON을 반환합니다. 반환값은 JavaScript의 `JSON.parse` 구문 형태로, 유효한 JS 객체로 변환할 수 있습니다:

```
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 앱 기본 골격에는 `Js` 파사드가 포함되어 있어 더 간편합니다:

```
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!NOTE]
> `Js::from` 메서드는 기존 변수를 JSON으로 안전하게 렌더링할 때만 사용하세요. Blade 템플릿은 정규 표현식을 기반으로 하기 때문에 복잡한 표현식을 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿 내에서 자바스크립트 변수를 많이 출력해야 할 경우, 각 Blade 에코문 앞에 `@` 문자를 붙이지 않도록 `@verbatim` 블록으로 감쌀 수 있습니다:

```
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 지시어 (Blade Directives)

템플릿 상속과 데이터 출력 외에도, Blade는 조건문과 반복문 같은 PHP 제어 구조를 위한 편리한 단축 구문을 제공합니다. 이 단축 구문은 PHP 문법과 동일하게 동작하지만 보다 깔끔하고 간결하게 작성할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시어를 사용해 `if` 문을 구성할 수 있습니다. PHP 문법과 동일하게 동작합니다:

```
@if (count($records) === 1)
    단 하나의 레코드가 있습니다!
@elseif (count($records) > 1)
    여러 개의 레코드가 있습니다!
@else
    레코드가 없습니다!
@endif
```

편의를 위해 `@unless` 지시어도 제공합니다:

```
@unless (Auth::check())
    로그인되어 있지 않습니다.
@endunless
```

위에서 설명한 조건문 외에도, `@isset`와 `@empty` 지시어는 PHP의 해당 함수들을 편리하게 사용할 수 있게 해줍니다:

```
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어있음" 상태입니다...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 관련 지시어

`@auth`와 `@guest` 지시어를 사용해 현재 사용자가 인증되었는지 또는 게스트인지를 쉽게 검사할 수 있습니다:

```
@auth
    // 사용자가 인증된 상태입니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면 인증 가드를 지정할 수도 있습니다:

```
@auth('admin')
    // admin 가드에서 인증된 상태...
@endauth

@guest('admin')
    // admin 가드에서 인증하지 않은 상태...
@endguest
```

<a name="environment-directives"></a>
#### 환경 검사 지시어

애플리케이션이 프로덕션 환경인지 확인하려면 `@production` 지시어를 사용하세요:

```
@production
    // 프로덕션 환경 전용 내용...
@endproduction
```

특정 환경인지 확인할 때는 `@env` 지시어를 사용합니다:

```
@env('staging')
    // 현재 "staging" 환경입니다...
@endenv

@env(['staging', 'production'])
    // "staging" 또는 "production" 환경입니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션 검사 지시어

템플릿 상속 섹션에 내용이 있는지 확인하려면 `@hasSection` 지시어를 사용하세요:

```html
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

섹션에 내용이 없을 때는 `@sectionMissing` 지시어를 사용합니다:

```html
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어를 통해 switch 문을 작성할 수 있습니다:

```
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

조건문뿐 아니라, Blade는 PHP의 반복문 제어문도 간단하게 처리할 수 있습니다. 각각 PHP 문법과 동일하게 동작합니다:

```
@for ($i = 0; $i < 10; $i++)
    현재 값은 {{ $i }} 입니다.
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
    <p>무한 루프 중입니다.</p>
@endwhile
```

> [!TIP]
> `foreach` 반복문 내에서 [루프 변수](#the-loop-variable)를 활용하면 현재 반복이 첫 번째인지 마지막인지 등 유용한 정보를 얻을 수 있습니다.

반복문에서 현재 반복을 건너뛰거나 종료하고 싶으면 `@continue`와 `@break` 지시어를 사용할 수 있습니다:

```
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

조건을 바로 지시어에 포함시킬 수도 있습니다:

```
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 반복문을 돌 때, 루프 내부에서 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 루프 인덱스, 첫 반복인지 마지막 반복인지 등의 유용한 정보를 제공합니다:

```
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

중첩 반복문의 경우, 부모 루프의 `$loop` 변수는 `parent` 속성을 통해 접근할 수 있습니다:

```
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            부모 루프의 첫 번째 반복입니다.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수의 기타 유용한 속성들은 다음과 같습니다:

| 속성              | 설명                                      |
|------------------|-----------------------------------------|
| `$loop->index`     | 현재 반복의 인덱스 (0부터 시작)           |
| `$loop->iteration` | 현재 반복의 번호 (1부터 시작)              |
| `$loop->remaining` | 남은 반복 횟수                            |
| `$loop->count`     | 반복 대상 배열의 전체 요소 개수             |
| `$loop->first`     | 현재 반복이 첫 번째인지 여부               |
| `$loop->last`      | 현재 반복이 마지막인지 여부                |
| `$loop->even`      | 현재 반복이 짝수 번째인지 여부             |
| `$loop->odd`       | 현재 반복이 홀수 번째인지 여부             |
| `$loop->depth`     | 중첩 반복문 깊이                           |
| `$loop->parent`    | 부모 루프의 루프 변수 (중첩일 때만 사용)    |

<a name="conditional-classes"></a>
### 조건부 클래스 (Conditional Classes)

`@class` 지시어는 조건에 따라 CSS 클래스를 컴파일합니다. 배열을 인수로 받는데, 배열 키는 클래스명(또는 여러 개의 클래스명), 값은 boolean 표현식입니다. 만약 배열 키가 숫자일 경우 항상 클래스 목록에 포함됩니다:

```
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

<!-- 렌더링 결과 -->
<span class="p-4 text-gray-500 bg-red"></span>
```

<a name="including-subviews"></a>
### 서브뷰 포함하기 (Including Subviews)

> [!TIP]
> `@include` 지시어도 사용 가능하지만, [컴포넌트](#components)는 데이터와 속성 바인딩 같은 추가 기능을 제공해 더 강력합니다.

`@include` 지시어는 다른 Blade 뷰를 현재 뷰에 포함시킬 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서도 사용할 수 있습니다:

```html
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

포함된 뷰가 부모의 모든 데이터를 상속하지만, 추가로 전달할 데이터 배열도 지정할 수 있습니다:

```
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include` 하면 오류가 발생합니다. 가끔 뷰가 없을 수도 있을 때는 `@includeIf`를 써야 합니다:

```
@includeIf('view.name', ['status' => 'complete'])
```

또 특정 불리언 조건이 참일 때 포함하거나 반대로 포함하지 않으려면 각각 `@includeWhen`과 `@includeUnless`를 사용할 수 있습니다:

```
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

배열에 포함된 뷰 중 첫 번째로 존재하는 뷰만 포함하고 싶다면 `@includeFirst`를 사용하세요:

```
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!NOTE]
> Blade 뷰 내에서 `__DIR__`이나 `__FILE__` 상수를 사용하지 않는 것이 좋습니다. 이들은 컴파일된 뷰 캐시 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

`@each` 지시어를 사용하면 반복문과 포함을 한 줄로 작성할 수 있습니다:

```
@each('view.name', $jobs, 'job')
```

`@each`의 첫 번째 인수는 각 요소에 대해 렌더링할 뷰, 두 번째 인수는 반복 대상 배열 또는 컬렉션, 세 번째 인수는 각 요소를 뷰 내에서 참조할 변수명입니다. 예를 들어 `jobs` 배열을 순회하며 각 요소를 `job` 변수로 사용합니다. 추가로 현재 요소 키는 뷰 내에서 `key` 변수로 사용할 수 있습니다.

네 번째 인수를 넘기면 배열이 비어 있을 때 렌더링할 뷰를 지정할 수 있습니다:

```
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!NOTE]
> `@each`를 통해 렌더링되는 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰가 추가 변수들을 필요로 한다면 `@foreach`와 `@include`를 조합해서 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once`는 템플릿 내 특정 부분이 렌더링 사이클 당 한 번만 평가되도록 할 때 씁니다. 예를 들어, 루프 안에서 컴포넌트를 여러 번 렌더링하지만 관련 JavaScript 코드는 한 번만 헤더에 포함시키고 싶을 때 유용합니다:

```
@once
    @push('scripts')
        <script>
            // 커스텀 JavaScript 코드...
        </script>
    @endpush
@endonce
```

<a name="raw-php"></a>
### 원시 PHP

때로는 뷰 내에 PHP 코드를 직접 실행해야 할 때가 있습니다. `@php` 지시어를 사용하면 템플릿 내에 순수 PHP 코드를 넣을 수 있습니다:

```
@php
    $counter = 1;
@endphp
```

<a name="comments"></a>
### 주석

Blade는 뷰 내에서 주석을 지원합니다. HTML 주석과 달리, Blade 주석은 최종 렌더 HTML에 포함되지 않습니다:

```
{{-- 이 주석은 렌더링된 HTML에 나오지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 섹션, 레이아웃, 인클루드와 유사한 이점을 제공합니다. 하지만 컴포넌트와 슬롯은 더 직관적으로 받아들이는 사람들이 많습니다. 컴포넌트 작성 방법은 클래스 기반 컴포넌트와 익명 컴포넌트 두 가지가 있습니다.

클래스 기반 컴포넌트를 만들려면 `make:component` Artisan 명령어를 사용하세요. 예를 들어, `Alert` 컴포넌트를 만들어 봅시다. 해당 명령어는 `app/View/Components` 디렉터리에 컴포넌트 클래스를 생성합니다:

```
php artisan make:component Alert
```

이 명령어는 컴포넌트 뷰 템플릿도 생성합니다. 뷰 템플릿은 `resources/views/components` 디렉터리에 위치합니다. 애플리케이션 내에서는 `app/View/Components`와 `resources/views/components` 내 컴포넌트를 자동으로 발견하므로 별도 등록 작업은 보통 필요하지 않습니다.

하위 디렉터리에도 컴포넌트를 만들 수 있습니다:

```
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms` 내에 `Input` 컴포넌트 클래스를, `resources/views/components/forms` 내에 뷰 템플릿을 생성합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

자신의 애플리케이션에서는 컴포넌트가 자동 발견되지만, 패키지 내 컴포넌트는 클래스와 태그 별칭을 수동으로 등록해야 합니다. 보통 패키지 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot()
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후에는 다음처럼 태그 별칭으로 렌더링할 수 있습니다:

```
<x-package-alert/>
```

`componentNamespace` 메서드를 사용하면 네임스페이스별로 컴포넌트를 자동 로드할 수도 있습니다. 예를 들어 `Nightshade` 패키지가 `Package\Views\Components` 네임스페이스 내에 `Calendar`와 `ColorPicker` 컴포넌트를 포함한다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

다음과 같이 벤더 네임스페이스로 컴포넌트를 사용할 수 있습니다:

```
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 자동으로 클래스를 찾습니다. 하위 디렉터리는 점(dot) 표기법도 지원합니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링하기 (Rendering Components)

컴포넌트를 출력하려면 Blade 템플릿 내에서 Blade 컴포넌트 태그를 사용하면 됩니다. 컴포넌트 태그명은 `x-` 접두어 뒤에 컴포넌트 클래스명을 케밥 케이스로 쓴 형태입니다:

```
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components` 디렉터리 내 중첩되어 있다면 `.` 문자를 사용해 디렉터리 계층을 표현할 수 있습니다. 예를 들어 `app/View/Components/Inputs/Button.php`에 있으면:

```
<x-inputs.button/>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기 (Passing Data To Components)

HTML 속성을 사용하여 컴포넌트에 데이터를 전달할 수 있습니다. 하드코딩된 원시형 값은 단순 HTML 속성 문자열로 전달하세요. PHP 표현식이나 변수를 전달할 때는 속성 이름 앞에 `:` 문자를 붙입니다:

```
<x-alert type="error" :message="$message"/>
```

컴포넌트의 필수 데이터는 클래스 생성자에서 정의합니다. 컴포넌트의 모든 public 속성은 자동으로 뷰에서 사용할 수 있도록 전달됩니다. 따라서 `render` 메서드에서 데이터를 뷰에 넘길 필요가 없습니다:

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 알림 타입
     *
     * @var string
     */
    public $type;

    /**
     * 알림 메시지
     *
     * @var string
     */
    public $message;

    /**
     * 컴포넌트 인스턴스 생성자
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
     * 뷰 / 내용 반환
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때는 public 변수들을 이름으로 출력하면 됩니다:

```html
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 네이밍 규칙

컴포넌트 생성자 인수는 `camelCase`를 사용하고, 컴포넌트를 호출할 때 HTML 속성에서는 `kebab-case`를 사용해야 합니다. 예를 들어 다음과 같은 생성자가 있을 때:

```
/**
 * 컴포넌트 인스턴스 생성자
 *
 * @param  string  $alertType
 * @return void
 */
public function __construct($alertType)
{
    $this->alertType = $alertType;
}
```

호출 시에는 다음처럼 씁니다:

```
<x-alert alert-type="danger" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 같은 자바스크립트 프레임워크가 콜론(`:`) 접두사 속성을 사용하기 때문에, Blade가 PHP 표현식으로 파악하지 않도록 속성명 앞에 콜론 두 개(`::`)를 붙여 구분할 수 있습니다:

```
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade가 렌더링하는 결과 HTML:

```
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서 public 메서드를 호출할 수 있습니다. 예를 들어 `isSelected`라는 메서드가 있다고 가정하면:

```
/**
 * 옵션이 현재 선택된 상태인지 판별
 *
 * @param  string  $option
 * @return bool
 */
public function isSelected($option)
{
    return $option === $this->selected;
}
```

템플릿에서 메서드를 다음과 같이 호출할 수 있습니다:

```
<option {{ $isSelected($value) ? 'selected="selected"' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성 및 슬롯 접근

컴포넌트 클래스의 `render` 메서드에서 컴포넌트 이름, 속성, 슬롯에 접근하려면 클로저를 반환해야 합니다. 클로저는 `$data` 배열을 인수로 받으며, 다음 요소를 포함합니다:

```
/**
 * 뷰 / 컴포넌트 내용을 반환
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
{
    return function (array $data) {
        // $data['componentName'];
        // $data['attributes'];
        // $data['slot'];

        return '<div>컴포넌트 내용</div>';
    };
}
```

`componentName`은 HTML 태그에서 `x-` 접두어 다음에 오는 이름입니다. 예를 들어 `<x-alert />`의 `componentName`은 `alert`입니다. `attributes`는 HTML 태그에 있던 모든 속성, `slot`은 컴포넌트 슬롯 내용이 저장된 `HtmlString` 객체입니다.

클로저에서 문자열을 반환하면, 해당 문자열이 존재하는 뷰 경로일 때는 뷰를 렌더링하며, 그렇지 않으면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성

컴포넌트가 Laravel [서비스 컨테이너](/docs/{{version}}/container)의 의존성을 필요로 한다면, 컴포넌트 생성자에서 데이터 속성 앞에 명시하면 자동 주입됩니다:

```
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성자
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
#### 속성 / 메서드 숨기기

특정 퍼블릭 프로퍼티 또는 메서드를 컴포넌트 템플릿 변수로 노출하지 않으려면, 컴포넌트 클래스 내 `$except` 배열에 이름을 추가하세요:

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 알림 타입
     *
     * @var string
     */
    public $type;

    /**
     * 템플릿에 노출하지 않을 속성/메서드 목록
     *
     * @var array
     */
    protected $except = ['type'];
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성 (Component Attributes)

데이터 속성 외에도 종종 `class` 같은 추가 HTML 속성을 전달해야 할 때가 있습니다. 이런 추가 속성들을 컴포넌트 템플릿의 루트 요소로 내려 보내고 싶을 때가 많습니다. 예를 들어 `alert` 컴포넌트를 다음처럼 호출할 때:

```
<x-alert type="error" :message="$message" class="mt-4"/>
```

생성자에 명시되지 않은 나머지 속성들은 자동으로 컴포넌트의 "속성 모음(attribute bag)"에 저장되고, `$attributes` 변수로 컴포넌트에서 사용할 수 있습니다. 템플릿에서 다음처럼 출력하세요:

```
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!NOTE]
> 현재 컴포넌트 태그 내에 `@env` 같은 Blade 지시어를 사용하는 것은 지원하지 않습니다. 예를 들어 `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본/병합 속성

속성 이름에 기본값을 지정하거나 기존 속성 값에 추가 값을 병합할 때는 `$attributes->merge` 메서드를 사용하세요. 주로 기본 CSS 클래스를 지정할 때 유용합니다:

```
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위 예제를 호출할 때:

```
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더링 HTML은 다음과 같습니다:

```html
<div class="alert alert-error mb-4">
    <!-- $message의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

조건에 따라 클래스를 병합하고 싶으면 `class` 메서드를 사용하세요. 배열 키는 클래스 이름, 값은 boolean 조건입니다. 숫자 키면 무조건 포함됩니다:

```
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

다른 속성과 병합하려면 `class` 뒤에 `merge`를 연결할 수 있습니다:

```
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!TIP]
> 다른 요소가 클래스만 조건부로 컴파일해야 하고 속성 병합이 필요 없다면, [`@class` 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

`merge`에 넘긴 값은 병합되지 않고 기본값으로 처리되며, 기존에 전달된 값이 있으면 덮어 씌웁니다. 예를 들어 버튼 컴포넌트는 다음과 같이 구현될 수 있습니다:

```
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 호출 시 타입을 바꾸려면 다음과 같이 작성하세요. 타입을 지정하지 않으면 기본값인 `button`이 사용됩니다:

```
<x-button type="submit">
    Submit
</x-button>
```

위 예제의 렌더링 결과:

```
<button type="submit">
    Submit
</button>
```

`class`가 아닌 속성에 기본값과 추가값을 붙이고 싶으면 `prepends` 메서드를 사용하세요. 예를 들어, `data-controller` 속성에 `profile-controller`를 항상 앞에 붙이고, 추가로 주입되는 값들을 뒤에 덧붙이는 식입니다:

```
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 조회

`filter` 메서드를 사용해 조건에 맞는 속성만 걸러낼 수 있습니다. 이 메서드는 클로저를 받아, 유지할 속성은 `true`를 반환해야 합니다:

```
{{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}
```

`whereStartsWith` 메서드는 특정 문자열로 시작하는 속성만 조회합니다:

```
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 `whereDoesntStartWith`는 특정 문자열로 시작하지 않는 속성만 조회합니다:

```
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드를 사용하면 속성 모음 내 첫 번째 속성을 렌더링할 수 있습니다:

```
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성 존재 여부는 `has` 메서드로 확인할 수 있습니다. 인수로 속성명을 주고, 있으면 `true`, 없으면 `false`를 반환합니다:

```
@if ($attributes->has('class'))
    <div>class 속성이 존재합니다</div>
@endif
```

특정 속성 값은 `get` 메서드로 얻을 수 있습니다:

```
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 예약어 (Reserved Keywords)

Blade 내부에서 컴포넌트 렌더링에 사용되는 일부 키워드는 예약되어 있습니다. 따라서 컴포넌트 클래스에서 public 멤버나 메서드명으로 다음 항목들을 쓸 수 없습니다:

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<a name="slots"></a>
### 슬롯 (Slots)

컴포넌트에 추가 콘텐츠를 전달하려면 "슬롯"을 사용합니다. 슬롯 내용은 `$slot` 변수를 출력해 렌더링합니다. 예를 들어, `alert` 컴포넌트가 다음과 같다 가정해보겠습니다:

```html
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

다음과 같이 컴포넌트에 내용을 주입할 수 있습니다:

```html
<x-alert>
    <strong>경고!</strong> 문제가 발생했습니다!
</x-alert>
```

컴포넌트 내 여러 다른 위치에 여러 슬롯을 렌더링해야 하는 경우도 있습니다. 예를 들어 "title"이라는 이름 슬롯을 추가해봅시다:

```html
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

이름이 지정된 슬롯은 `x-slot` 태그로 정의합니다. 명시적 `x-slot`에 들어가지 않은 콘텐츠는 기본 슬롯인 `$slot` 변수로 전달됩니다:

```html
<x-alert>
    <x-slot name="title">
        서버 오류
    </x-slot>

    <strong>경고!</strong> 문제가 발생했습니다!
</x-alert>
```

<a name="scoped-slots"></a>
#### 스코프드 슬롯

Vue 같은 프레임워크에서 익숙한 "스코프드 슬롯" 개념도 Laravel에서 비슷하게 구현할 수 있습니다. 컴포넌트에 public 메서드나 속성을 정의하고, 슬롯 내에서 컴포넌트 변수 `$component`를 통해 호출하는 방식입니다. 예를 들어 `x-alert` 컴포넌트에 `formatAlert` 메서드가 있다고 가정할 때:

```html
<x-alert>
    <x-slot name="title">
        {{ $component->formatAlert('서버 오류') }}
    </x-slot>

    <strong>경고!</strong> 문제가 발생했습니다!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성

슬롯에도 컴포넌트처럼 속성(예: CSS 클래스)을 지정할 수 있습니다:

```html
<x-card class="shadow-sm">
    <x-slot name="heading" class="font-bold">
        제목
    </x-slot>

    콘텐츠

    <x-slot name="footer" class="text-sm">
        푸터
    </x-slot>
</x-card>
```

슬롯 속성은 슬롯 변수의 `attributes` 프로퍼티를 통해 접근합니다. 자세한 내용은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

```php
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

아주 작은 컴포넌트의 경우, 컴포넌트 클래스와 뷰 템플릿을 각각 관리하는 게 번거로울 수 있습니다. 이런 경우 컴포넌트의 렌더 메서드에서 직접 마크업을 반환할 수 있습니다:

```
/**
 * 뷰 / 컴포넌트 내용 반환
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
#### 인라인 뷰 컴포넌트 생성

인라인 뷰 컴포넌트를 만들 때 `make:component` 명령어에 `--inline` 옵션을 붙이세요:

```
php artisan make:component Alert --inline
```

<a name="anonymous-components"></a>
### 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 비슷하게, 익명 컴포넌트는 컴포넌트 뷰 파일 하나로 관리하지만 클래스가 없는 방식입니다. 익명 컴포넌트를 정의하려면 `resources/views/components` 디렉터리에 Blade 템플릿 하나만 두면 됩니다. 예를 들어 `resources/views/components/alert.blade.php`가 있으면:

```
<x-alert/>
```

처럼 렌더링할 수 있습니다.

컴포넌트가 하위 디렉터리에 있을 경우 `.` 문자를 이용해 표시합니다. 예를 들어 `resources/views/components/inputs/button.blade.php`는:

```
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
#### 익명 인덱스 컴포넌트

컴포넌트를 구성하는 Blade 템플릿이 여러 개일 때, 컴포넌트 관련 템플릿을 한 디렉터리에 모으고 싶을 수 있습니다. 예를 들어 "accordion" 컴포넌트가 다음과 같은 구조라면:

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

`accordion`과 그 항목을 다음처럼 사용할 수 있습니다:

```html
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만, `x-accordion`을 렌더링하기 위해서는 `accordion.blade.php` 뷰를 `components` 루트에 두어야 했습니다.

이 문제를 위해 `index.blade.php` 파일을 컴포넌트 디렉터리에 둘 수 있습니다. 이렇게 하면 다음과 같은 디렉터리 구조를 가질 수 있습니다:

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

`index.blade.php`가 루트 노드 역할을 해주어 이전과 같은 방식으로 렌더링할 수 있습니다.

<a name="data-properties-attributes"></a>
#### 데이터 변수 / 속성

익명 컴포넌트는 클래스가 없기 때문에 어떤 속성이 컴포넌트 변수인지, 어떤 것이 속성 가방에 들어가는지 구분하려면 `@props` 지시어를 템플릿 최상단에 적어야 합니다. 기본값을 지정할 수도 있습니다:

```
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

위와 같이 정의했을 경우, 컴포넌트 호출은 다음과 같습니다:

```
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
#### 부모 데이터 접근

자식 컴포넌트에서 부모의 데이터를 참조하고 싶을 때는 `@aware` 지시어를 사용하세요. 예를 들어, 복잡한 메뉴 컴포넌트 `<x-menu>`와 항목 컴포넌트 `<x-menu.item>`이 있을 때:

```
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>`는 다음과 같이 구현할 수 있습니다:

```
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` 속성은 부모에만 전달되므로, 자식 `<x-menu.item>`에는 기본적으로 전달되지 않습니다.

하지만 `@aware`를 사용하면 자식 컴포넌트에서도 이 속성을 사용할 수 있습니다:

```
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

<a name="dynamic-components"></a>
### 동적 컴포넌트 (Dynamic Components)

동적으로 어떤 컴포넌트를 렌더링할지 런타임에 결정해야 할 경우 내장된 `dynamic-component` 컴포넌트를 사용하세요:

```
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 수동으로 컴포넌트 등록하기 (Manually Registering Components)

> [!NOTE]
> 이 장은 주로 Laravel 패키지 제작 시 Blade 컴포넌트를 포함할 때 해당합니다. 일반 애플리케이션에서는 자동 발견되는 컴포넌트를 사용하므로 대부분 해당하지 않습니다.

애플리케이션에서는 `app/View/Components`와 `resources/views/components` 내 컴포넌트를 자동으로 찾습니다.

그렇지만 패키지에서 Blade 컴포넌트를 사용하거나 비정상 디렉터리에 컴포넌트를 두는 경우, 다음과 같이 직접 컴포넌트 클래스와 태그 별칭을 등록해야 합니다. 보통 패키지 서비스 프로바이더 `boot` 메서드에서 합니다:

```
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

이후 `x-package-alert` 태그로 렌더링할 수 있습니다:

```
<x-package-alert/>
```

#### 패키지 컴포넌트 자동 로드

앞서 소개한 `componentNamespace` 메서드를 통해 네임스페이스별로 컴포넌트를 자동으로 로드할 수도 있습니다. 예를 들어 `Nightshade` 패키지가 `Package\Views\Components` 네임스페이스를 가진다면:

```
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

다음과 같이 패키지 네임스페이스를 접두사로 컴포넌트를 사용할 수 있습니다:

```
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 변환해 자동으로 클래스 매핑을 지원하며, 하위 디렉터리는 점(.) 표기법을 지원합니다.

<a name="building-layouts"></a>
## 레이아웃 구성하기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트를 이용한 레이아웃 (Layouts Using Components)

대부분의 웹 애플리케이션은 여러 페이지에 걸쳐 동일한 레이아웃을 유지합니다. 모든 뷰마다 레이아웃 HTML을 복사해 쓰는 것은 매우 비효율적이고 유지보수도 어렵습니다. 다행히, 레이아웃을 하나의 [Blade 컴포넌트](#components)로 정의하고 애플리케이션 전체에서 사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의하기

예를 들어 "todo" 리스트 애플리케이션을 만든다면, 다음과 같은 `layout` 컴포넌트를 정의할 수 있습니다:

```html
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

레이아웃 컴포넌트를 정했다면 이를 사용하는 Blade 뷰를 작성할 수 있습니다. 예를 들어 할 일 목록을 출력하는 간단한 뷰를 만듭니다:

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

컴포넌트에 주입된 콘텐츠는 기본 슬롯인 `$slot` 변수로 전달됩니다. 또한 `layout` 컴포넌트는 `$title` 슬롯을 제공하는 경우 이를 출력하고, 없으면 기본 타이틀이 출력됩니다. 타이틀을 커스텀하려면 다음과 같이 슬롯을 지정하세요:

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot name="title">
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

정의한 뷰를 라우트에서 반환하면 됩니다:

```
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 이용한 레이아웃 (Layouts Using Template Inheritance)

<a name="defining-a-layout"></a>
#### 레이아웃 정의하기

템플릿 상속은 컴포넌트 도입 이전에 주로 사용한 레이아웃 구축 방식입니다.

간단한 예시부터 보겠습니다. 다음은 페이지 레이아웃입니다. 대부분의 웹 앱은 여러 페이지에 걸쳐 동일한 레이아웃이 유지되므로, 별도의 Blade 뷰 하나로 정의합니다:

```html
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

보시다시피 HTML 마크업 내에 `@section`과 `@yield` 지시어가 있습니다. `@section`은 섹션을 정의하며, `@yield`는 해당 섹션의 내용을 그 위치에 출력합니다.

레이아웃을 정의했으면, 이제 이 레이아웃을 상속받는 자식 뷰를 만들어 보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장하기

자식 뷰에서는 `@extends` 지시어로 어느 레이아웃을 상속할지 지정합니다. 상속받은 뷰는 `@section`으로 레이아웃의 섹션에 내용을 주입합니다. 이 섹션들의 내용은 레이아웃의 `@yield`가 있는 위치에 출력됩니다:

```html
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

`sidebar` 섹션에서는 `@@parent` 지시어를 사용해 레이아웃의 기존 내용을 덮어쓰지 않고 덧붙였습니다. `@@parent`는 렌더링 시 부모 뷰의 내용을 삽입합니다.

> [!TIP]
> 이전 예시와 달리 이 예제에서 `sidebar` 섹션은 `@endsection`으로 닫습니다(`@show`가 아님). `@endsection`은 섹션만 정의하고 바로 출력하지 않고, `@show`는 정의와 동시에 **즉시 출력**합니다.

`@yield` 지시어는 두 번째 인자로 기본값을 지정할 수 있으며, 해당 섹션이 정의되지 않은 경우 기본값이 출력됩니다:

```
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션 내에 HTML 폼을 정의할 때는 항상 숨겨진 CSRF 토큰 필드를 포함해야 합니다. 이렇게 해야 [CSRF 미들웨어](/docs/{{version}}/csrf)가 요청을 검증할 수 있습니다. Blade에서는 `@csrf` 지시어로 토큰 필드를 쉽게 생성합니다:

```html
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### HTTP 메서드 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 등의 HTTP 동사를 직접 지원하지 않습니다. 이 경우 `_method` 숨겨진 필드를 추가해 HTTP 메서드를 위조할 수 있습니다. Blade의 `@method` 지시어가 이를 생성해 줍니다:

```html
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 검증 오류 표시

`@error` 지시어를 이용하면 지정한 속성에 대해 검증 오류가 있는지 손쉽게 확인할 수 있습니다. 해당 블록 내에서는 `$message` 변수를 출력하면 오류 메시지가 표시됩니다:

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title" type="text" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

`@error`는 내부적으로 `if`문으로 컴파일되므로 대응되는 `@else`를 쓸 수 있어 오류가 없을 경우 표시할 내용을 작성할 수 있습니다:

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email') is-invalid @else is-valid @enderror">
```

여러 폼을 가진 페이지에서 특정 에러 백(error bag)을 지정하려면 `@error` 두 번째 인수에 에러 백 이름을 넘기면 됩니다:

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
## 스택 (Stacks)

Blade에서는 "이름 있는 스택"에 여러 번 콘텐츠를 푸시(push)하고, 다른 곳에서 한꺼번에 렌더링할 수 있습니다. 주로 자식 뷰에서 필요한 JavaScript 라이브러리를 정의할 때 유용합니다:

```html
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

스택에 여러 번 푸시할 수 있습니다. 완성된 스택 내용을 렌더링하려면 `@stack` 지시어에 스택 이름을 전달하세요:

```html
<head>
    <!-- 헤드 내용 -->

    @stack('scripts')
</head>
```

스택 앞부분에 콘텐츠를 추가하려면 `@prepend` 지시어를 씁니다:

```html
@push('scripts')
    두 번째로 실행될 스크립트...
@endpush

// 나중에...

@prepend('scripts')
    가장 먼저 실행될 스크립트...
@endprepend
```

<a name="service-injection"></a>
## 서비스 주입 (Service Injection)

`@inject` 지시어를 사용하면 Laravel [서비스 컨테이너](/docs/{{version}}/container)에서 서비스를 조회할 수 있습니다. 첫 번째 인수는 서비스를 저장할 변수명, 두 번째 인수는 서비스의 클래스나 인터페이스명입니다:

```html
@inject('metrics', 'App\Services\MetricsService')

<div>
    월별 매출: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="extending-blade"></a>
## Blade 확장하기 (Extending Blade)

Blade는 맞춤형 지시어를 정의할 수 있게 `directive` 메서드를 지원합니다. Blade 컴파일러가 맞춤 지시어를 만나면 주어진 콜백을 호출하며, 콜백에는 지시어 내 표현식이 전달됩니다.

다음 예시는 `@datetime($var)`라는 지시어를 정의해, `DateTime` 인스턴스인 `$var`를 형식화합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
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

위와 같이 `format` 메서드를 연속해서 호출합니다. 결과 PHP 코드는 이렇습니다:

```
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!NOTE]
> Blade 지시어의 로직을 변경한 후에는 캐시된 모든 Blade 뷰를 삭제해야 합니다. `view:clear` Artisan 명령어를 사용하세요.

<a name="custom-echo-handlers"></a>
### 맞춤형 에코 핸들러 (Custom Echo Handlers)

Blade는 객체를 에코할 때 기본으로 `__toString` 메서드를 호출합니다. 하지만 일부 객체는 `__toString`을 제어할 수 없거나 적절하게 구현되어 있지 않을 수 있습니다(예: 서드파티 라이브러리).

이럴 때 Blade에 타입별 맞춤형 에코 핸들러를 등록해 특정 객체 타입을 별도로 처리할 수 있습니다. `stringable` 메서드에 클로저를 넘기며, 필요한 경우 타입힌트를 붙입니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 선언합니다:

```
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩.
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

이후 Blade에서 그냥 객체를 출력하면 자동으로 핸들러가 호출됩니다:

```html
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 맞춤형 If 문 (Custom If Statements)

복잡한 맞춤형 지시어 대신, 간단한 조건문을 정의할 때에는 `Blade::if` 메서드를 사용할 수 있습니다. 클로저를 인수로 받고, 조건이 참인지 반환하면 해당 이름의 조건문 지시어가 만들어집니다. 예를 들어, 기본 파일시스템 디스크를 검사하는 맞춤 조건을 만들어 보겠습니다:

```
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스 부트스트랩.
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

정의 후에는 다음과 같이 사용할 수 있습니다:

```html
@disk('local')
    <!-- 현재 로컬 디스크 사용 중 -->
@elsedisk('s3')
    <!-- 현재 s3 디스크 사용 중 -->
@else
    <!-- 다른 디스크 사용 중 -->
@enddisk

@unlessdisk('local')
    <!-- 로컬 디스크가 아닙니다 -->
@enddisk
```