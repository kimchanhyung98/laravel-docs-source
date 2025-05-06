# Context

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거](#removing-context)
- [숨김 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [탈수(Dehydrating)](#dehydrating)
    - [재수화(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

Laravel의 "컨텍스트" 기능을 사용하면 애플리케이션 내에서 실행되는 요청, 작업, 명령 전체에 걸쳐 정보를 캡처하고 조회하며 공유할 수 있습니다. 캡처된 이 정보는 애플리케이션에서 기록하는 로그에도 메타데이터로 포함되어, 로그가 기록되기 전에 발생했던 주변 코드 실행 이력을 더 깊이 파악할 수 있으며, 분산 시스템 전체의 실행 흐름을 추적할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel 컨텍스트의 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능과 함께 실제로 사용하는 것입니다. 시작하려면, `Context` 파사드를 이용해 [컨텍스트에 정보를 추가](#capturing-context)하세요. 다음 예시에서는 각 요청마다 요청 URL과 고유 추적 ID(trace ID)를 컨텍스트에 추가하는 [미들웨어](/docs/{{version}}/middleware)를 구현합니다.

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

컨텍스트에 추가된 정보는 요청 전체에서 기록되는 [로그 항목](/docs/{{version}}/logging)의 메타데이터로 자동으로 덧붙여집니다. 컨텍스트를 메타데이터로 추가하면 각각의 로그 항목에 전달된 정보와 `Context`를 통해 공유된 정보를 구분할 수 있습니다. 예를 들어 다음과 같이 로그를 기록했다고 가정해봅시다.

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

작성된 로그에는 로그 항목으로 전달된 `auth_id`뿐만 아니라 컨텍스트의 `url`과 `trace_id`도 메타데이터로 포함됩니다.

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐에 디스패치된 작업에서도 사용할 수 있습니다. 예를 들어, 컨텍스트에 정보를 추가한 후 `ProcessPodcast` 작업을 큐에 디스패치한다고 해봅시다.

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때, 현재 컨텍스트에 저장된 모든 정보가 캡처되어 작업과 함께 공유됩니다. 작업이 실행되는 동안 이 캡처된 정보가 다시 현재 컨텍스트에 재수화됩니다. 아래와 같이 작업의 handle 메서드에서 로그를 기록하는 경우를 생각해보세요.

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

결과적으로 생성되는 로그 항목에는 해당 작업을 디스패치했던 요청에서 컨텍스트에 추가했던 정보가 포함됩니다.

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

이 문서에서는 Laravel 컨텍스트와 관련된 기본적인 로깅 기능에 초점을 맞췄지만, 컨텍스트를 활용해 HTTP 요청과 큐 작업 경계에 걸쳐 정보를 공유하는 방법, 그리고 로그에는 기록되지 않는 [숨김 컨텍스트 데이터](#hidden-context)를 추가하는 방법까지도 다룰 것입니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 항목을 한 번에 추가하려면, 연관 배열을 `add` 메서드에 전달하면 됩니다.

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키가 이미 존재하면 기존 값을 덮어씁니다. 만약 해당 키가 아직 없다면에만 정보를 추가하고 싶으면 `addIf` 메서드를 사용하세요.

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트에는 지정된 키의 값을 증가, 감소시키는 편의 메서드도 있습니다. 이 메서드들은 기본적으로 첫 번째 인자로 추적할 키를, 두 번째 인자로는 증가/감소시킬 값을 받습니다.

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드는 특정 조건에 따라 컨텍스트에 데이터를 추가하는 데 사용할 수 있습니다. 첫 번째 클로저는 조건이 `true`일 때, 두 번째 클로저는 조건이 `false`일 때 실행됩니다.

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

`scope` 메서드는 주어진 콜백이 실행되는 동안 일시적으로 컨텍스트를 수정하고, 콜백이 끝나면 원래 상태로 복원시켜줍니다. 클로저 실행 도중 컨텍스트에 합쳐질 추가 데이터(두 번째, 세 번째 인자)도 전달할 수 있습니다.

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
> 스코프 클로저 안에서 컨텍스트 내 객체를 직접 수정하면, 그 변경사항은 스코프 밖에서도 반영됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택"을 생성할 수 있는 기능을 제공합니다. 스택은 추가된 순서대로 저장되는 데이터의 리스트입니다. `push` 메서드로 스택에 데이터를 추가할 수 있습니다.

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

스택은 요청에 대한 이력 정보(예: 애플리케이션 전체에서 발생하는 이벤트 등)를 저장하는 데 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 소요 시간을 튜플로 스택에 추가하는 이벤트 리스너를 만들 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains`와 `hiddenStackContains` 메서드를 사용해 스택에 특정 값이 존재하는지 확인할 수 있습니다.

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

이 메서드들은 두 번째 인자로 클로저도 받을 수 있어 값 비교 작업에 더 많은 제어권을 줄 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회

컨텍스트에서 정보를 조회하려면 `Context` 파사드의 `get` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` 메서드는 컨텍스트에서 일부 데이터만 추출해 가져오는 데 사용할 수 있습니다.

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` 메서드는 컨텍스트에서 값을 가져오고, 즉시 해당 값을 컨텍스트에서 제거합니다.

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)에 저장됐다면, `pop` 메서드로 스택에서 항목을 추출할 수 있습니다.

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs')
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

컨텍스트에 저장된 모든 정보를 가져오려면 `all` 메서드를 호출하세요.

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

컨텍스트에 주어진 키로 값이 저장되어 있는지 확인하려면 `has`와 `missing` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 저장된 값이 무엇이든 간에 무조건 `true`를 반환합니다. 즉, 값이 `null`인 경우에도 존재하는 것으로 간주합니다.

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거

`forget` 메서드를 사용하면 현재 컨텍스트에서 키와 값을 삭제할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

배열을 전달하면 여러 키를 한 번에 삭제할 수 있습니다.

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨김 컨텍스트

컨텍스트는 "숨김" 데이터도 저장할 수 있습니다. 이러한 숨김 정보는 로그에 추가되지 않으며, 위에 안내된 일반 데이터 조회 메서드로는 접근할 수 없습니다. 숨김 컨텍스트 전용의 별도 메서드가 제공됩니다.

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

숨김 관련 메서드는 비숨김 메서드와 동일한 기능을 제공합니다.

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## 이벤트

컨텍스트는 컨텍스트의 탈수(Dehydration)와 재수화(Hydration) 과정에 접근할 수 있도록 두 개의 이벤트를 디스패치합니다.

이벤트 사용법을 보여주기 위해, 예를 들어 애플리케이션의 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더를 기준으로 `app.locale` 설정값을 지정한다고 해봅시다. 컨텍스트 이벤트를 활용하면 이 값을 요청 시점에 캡처해 큐 작업에서도 제대로 복원할 수 있습니다. 이를 위해 컨텍스트 이벤트와 [숨김](#hidden-context) 데이터를 조합해서 사용할 수 있으며, 아래에서 자세히 설명합니다.

<a name="dehydrating"></a>
### 탈수(Dehydrating)

작업이 큐에 디스패치될 때 컨텍스트의 데이터는 "탈수"되어 작업 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드를 이용하면, 탈수 과정 중에 실행될 클로저를 등록할 수 있습니다. 이 클로저 내에서 큐 작업과 함께 공유할 데이터를 수정할 수 있습니다.

일반적으로 `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 등록해야 합니다.

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
> `dehydrating` 콜백 안에서는 `Context` 파사드 사용을 피해야 합니다. 현재 프로세스의 컨텍스트가 변경될 수 있으므로, 반드시 콜백에 전달된 저장소 객체만을 수정하세요.

<a name="hydrated"></a>
### 재수화(Hydrated)

큐 작업이 실행될 때, 작업과 함께 공유된 모든 컨텍스트 데이터가 현재 컨텍스트에 "재수화"됩니다. `Context::hydrated` 메서드를 사용하면, 재수화 과정 중 호출될 클로저를 등록할 수 있습니다.

일반적으로 `hydrated` 콜백은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에 등록합니다.

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
> `hydrated` 콜백 안에서도 `Context` 파사드 사용을 피하고, 반드시 콜백에 전달된 저장소 객체만을 사용하여 변경하십시오.