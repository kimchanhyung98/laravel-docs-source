# 컨텍스트 (Context)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회하기](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거하기](#removing-context)
- [숨김 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이트(Dehydrating)](#dehydrating)
    - [하이드레이팅(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

Laravel의 "컨텍스트(Context)" 기능을 사용하면 애플리케이션 내에서 실행되는 요청, 작업(잡), 명령어 전체에 걸쳐 정보를 수집하고 조회하며 공유할 수 있습니다. 이렇게 캡처된 정보는 애플리케이션이 작성하는 로그에도 자동으로 포함되어, 로그가 기록되기 전에 어떤 코드 실행 이력이 있었는지 더 깊이 있게 파악할 수 있으며, 분산 시스템에서도 실행 흐름을 효과적으로 추적할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장 로깅 기능과 함께 사용하는 모습을 살펴보는 것입니다. 먼저, [`Context` 파사드](#capturing-context)를 이용해 컨텍스트에 정보를 추가할 수 있습니다. 이 예시에서는 [미들웨어](/docs/12.x/middleware)를 사용해, 들어오는 모든 요청마다 요청 URL과 고유한 트레이스 ID를 컨텍스트에 추가해보겠습니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}
```

컨텍스트에 추가된 정보는 해당 요청 동안 작성되는 모든 [로그 항목](/docs/12.x/logging)에 메타데이터 형태로 자동으로 덧붙여집니다. 이때, 컨텍스트에 저장된 정보와 각각의 로그 항목에 직접 전달한 정보는 분리되어 구분할 수 있습니다. 예를 들어, 다음과 같이 로그를 작성해보겠습니다.

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

실제로 기록되는 로그에는 로그 항목에 전달한 `auth_id` 뿐 아니라, 컨텍스트의 `url`과 `trace_id`도 메타데이터로 함께 저장됩니다.

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가한 정보는 큐(queue)로 디스패치되는 잡(job)에도 함께 전달됩니다. 예를 들어, 컨텍스트에 값을 추가한 후 `ProcessPodcast` 잡을 큐로 디스패치한다고 가정해 봅니다.

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

잡이 디스패치되는 시점에 컨텍스트에 저장된 모든 정보가 함께 캡처되어 잡에 전달됩니다. 그리고 잡이 실행될 때 해당 정보가 다시 현재 컨텍스트에 "하이드레이션"되어 복원됩니다. 따라서, 잡의 handle 메서드에서 로그를 남긴다면:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}
```

이때 남겨진 로그 항목에도 최초 요청 시 컨텍스트에 추가한 정보가 함께 기록됩니다.

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

지금까지는 컨텍스트의 내장 로깅 관련 기능에 집중해서 설명했지만, 아래 페이지에서는 컨텍스트를 활용해 HTTP 요청과 큐 작업 사이에 정보를 안전하게 공유하는 방법, 그리고 [로그에는 기록되지 않는 숨겨진 컨텍스트](#hidden-context) 데이터까지 추가하는 방법도 안내합니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처하기

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

한 번에 여러 항목을 추가하려면, `add` 메서드에 연관 배열을 전달하면 됩니다.

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키에 기존 값이 있으면 덮어씁니다. 만약 해당 키에 값이 없을 때만 정보를 추가하고 싶다면 `addIf` 메서드를 사용할 수 있습니다.

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트에는 지정한 키의 값을 증가(increment)하거나 감소(decrement)시키는 편리한 메서드도 있습니다. 각각 적어도 하나의 인수(추적할 키)를 받고, 두 번째 인수로 증가 또는 감소시킬 값도 지정할 수 있습니다.

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드를 사용하면 특정 조건에 따라 컨텍스트에 데이터를 추가할 수 있습니다. 첫 번째로 받은 클로저는 조건이 `true`일 때 호출되고, 두 번째 클로저는 조건이 `false`일 때 호출됩니다.

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="scoped-context"></a>
#### 스코프 컨텍스트

`scope` 메서드를 사용하면, 특정 콜백이 실행되는 동안만 컨텍스트를 임시로 변경하고 실행이 끝나면 원래 상태로 되돌릴 수 있습니다. 또한, 콜백 실행 동안 컨텍스트에 병합할 추가 데이터(두 번째 인수, 세 번째 인수)를 전달할 수도 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> [!WARNING]
> 스코프 클로저 내부에서 컨텍스트의 객체를 수정하면, 그 변경 사항이 스코프 바깥에도 그대로 반영됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택(stack)"도 지원합니다. 스택은 데이터를 추가한 순서대로 쌓는 리스트입니다. `push` 메서드를 이용해 스택에 정보를 추가할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

스택은 요청 처리 과정에서 발생하는 이벤트 등, 연속적으로 일어나는 히스토리 정보를 기록할 때 유용합니다. 예를 들어, 쿼리가 실행될 때마다 이벤트 리스너를 만들어 스택에 쿼리 SQL과 실행 시간을 튜플로 기록할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

스택에 특정 값이 포함되어 있는지 확인할 때는 `stackContains` 및 `hiddenStackContains` 메서드를 사용할 수 있습니다.

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains` 및 `hiddenStackContains`는 두 번째 인수로 클로저를 받아, 값 비교 방법을 직접 정의할 수도 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회하기

컨텍스트에 저장된 정보를 조회하려면 `Context` 파사드의 `get` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

컨텍스트에서 원하는 일부 키만 조회하거나, 특정 키를 제외하고 조회하려면 `only`와 `except` 메서드를 활용할 수 있습니다.

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

컨텍스트에서 값을 읽으면서 동시에 삭제하고 싶을 때는 `pull` 메서드를 사용합니다.

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)으로 저장되어 있다면, `pop` 메서드를 사용해 스택에서 항목을 꺼낼 수 있습니다.

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

컨텍스트에 저장된 모든 데이터를 한 번에 조회하려면 `all` 메서드를 호출하세요.

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

특정 키에 값이 저장되어 있는지 확인하려면 `has` 또는 `missing` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 해당 키에 저장된 값이 무엇이든(심지어 `null`일지라도) `true`를 반환합니다.

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거하기

현재 컨텍스트에서 특정 키와 그 값을 삭제하려면 `forget` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

삭제할 키가 여러 개인 경우 배열로 전달하면 됩니다.

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨김 컨텍스트

컨텍스트는 "숨김(hidden)" 데이터를 저장하는 기능도 제공합니다. 이런 숨김 정보는 로그에 기록되지 않으며, 위에서 설명한 일반 데이터 조회 메서드로도 접근할 수 없습니다. 숨김 컨텍스트와 상호작용하려면 전용 메서드를 사용해야 합니다.

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

"숨김" 메서드는 위에서 설명한 일반 메서드와 동일한 기능을 제공합니다.

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## 이벤트

컨텍스트는 하이드레이션(hydration), 디하이드레이션(dehydration) 과정에서 후킹할 수 있는 두 개의 이벤트를 제공합니다.

예를 들어, 애플리케이션의 미들웨어에서 HTTP 요청의 `Accept-Language` 헤더를 분석해 `app.locale` 설정 값을 지정한다고 가정해 보겠습니다. 컨텍스트 이벤트를 활용하면 요청 도중 이 값을 캡처해서 큐 작업 실행 시에 다시 복원할 수 있으므로, 큐를 통해 발송되는 알림 역시 올바른 `app.locale` 값을 갖게 됩니다. 아래 예제에서는 컨텍스트 이벤트와 [숨김 데이터](#hidden-context)를 함께 활용하는 방법을 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이트(Dehydrating)

잡이 큐에 디스패치될 때, 컨텍스트 내의 데이터는 "디하이드레이션"되어 잡의 페이로드와 함께 저장됩니다. `Context::dehydrating` 메서드는, 디하이드레이션 과정 중에 실행될 클로저를 등록할 수 있도록 해줍니다. 이 클로저에서 큐 작업에 전달될 데이터를 변경할 수 있습니다.

일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 `dehydrating` 콜백을 등록합니다.

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}
```

> [!NOTE]
> `dehydrating` 콜백 내부에서는 `Context` 파사드를 사용하지 않아야 합니다. 현재 프로세스의 컨텍스트가 변경될 수 있으므로, 콜백에 전달된 repository 객체만 사용해 주세요.

<a name="hydrated"></a>
### 하이드레이팅(Hydrated)

큐에 들어간 작업이 실행될 때, 잡에 전달된 컨텍스트가 현재 컨텍스트에 "하이드레이션"되어 복구됩니다. `Context::hydrated` 메서드를 사용하면, 하이드레이션 과정에서 실행할 클로저를 등록할 수 있습니다.

이 콜백 역시 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 등록하는 것이 일반적입니다.

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> [!NOTE]
> `hydrated` 콜백 내부에서도 `Context` 파사드를 사용하지 말고, 콜백에 전달된 repository 객체만을 사용해 작업해야 합니다.
