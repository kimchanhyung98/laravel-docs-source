# 컨텍스트 (Context)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 가져오기](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거하기](#removing-context)
- [숨김 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이팅(Dehydrating)](#dehydrating)
    - [하이드레이티드(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

라라벨의 "컨텍스트(Context)" 기능은 애플리케이션 내에서 실행되는 요청, 작업, 명령어 전반에 걸쳐 정보를 캡처하고, 조회하고, 공유할 수 있도록 해줍니다. 이렇게 캡처된 정보는 애플리케이션이 기록하는 로그에도 메타데이터로 포함되므로, 로그가 남겨지기 전 실행된 코드의 히스토리를 더 깊이 파악할 수 있으며, 분산 시스템 내에서 실행 흐름을 추적하는 데에도 도움이 됩니다.

<a name="how-it-works"></a>
### 작동 방식

라라벨의 컨텍스트 기능을 가장 잘 이해하는 방법은 내장된 로깅 기능과 함께 실제로 사용하는 과정을 살펴보는 것입니다. 먼저, [`Context` 파사드](#capturing-context)를 활용해 컨텍스트에 정보를 추가할 수 있습니다. 예를 들어, [미들웨어](/docs/12.x/middleware)를 사용해서 들어오는 모든 요청에 대해 요청 URL과 고유 트레이스 ID를 컨텍스트에 추가할 수 있습니다:

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

컨텍스트에 추가한 정보는 요청 처리 과정에서 남기는 모든 [로그 엔트리](/docs/12.x/logging)에 자동으로 메타데이터로 덧붙여집니다. 컨텍스트 정보가 메타데이터 형태로 추가되면, 개별 로그 엔트리에 전달한 정보와 `Context`를 통해 전체적으로 공유한 정보를 구분할 수 있습니다. 예를 들어, 다음과 같이 로그를 작성했다고 가정해봅니다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

기록된 로그에는 해당 로그 엔트리에 전달한 `auth_id`와 함께, 컨텍스트에 추가된 `url` 및 `trace_id`도 메타데이터로 담깁니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

이처럼 컨텍스트에 추가된 정보는 큐에 디스패치되는 작업(job)에도 전달됩니다. 예를 들어, 컨텍스트에 정보를 추가한 뒤 `ProcessPodcast` 작업을 큐에 디스패치했다고 가정할 수 있습니다:

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때, 현재 컨텍스트에 저장된 모든 정보가 함께 캡처되어 작업에 전달됩니다. 작업이 실행되는 동안에는 이렇게 캡처된 정보가 현재 컨텍스트에 다시 하이드레이션(hydration)됩니다. 즉, 작업의 handle 메서드에서 로그를 남기면:

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

해당 로그에는 작업을 최초로 디스패치할 당시 요청에서 컨텍스트에 추가했던 정보도 함께 담기게 됩니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

이처럼 지금까지는 라라벨의 컨텍스트와 관련된 내장 로깅 기능에 초점을 뒀지만, 이어지는 문서에서는 컨텍스트가 HTTP 요청과 큐에 올라간 작업 간에 어떻게 정보를 공유할 수 있게 하는지, 그리고 [로그에 남기지 않는 숨김 컨텍스트 데이터](#hidden-context)는 어떻게 추가하는지도 설명합니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처하기

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용하면 됩니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

한 번에 여러 항목을 추가하고 싶다면, 연관 배열(associative array)를 `add` 메서드에 전달할 수 있습니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키가 이미 존재하는 경우 항상 값을 덮어씁니다. 만약 키가 이미 없을 때만 정보를 추가하고 싶다면, `addIf` 메서드를 사용하세요:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트는 특정 키의 값을 편리하게 증가 또는 감소시키는 메서드도 제공합니다. 이 메서드는 최소 한 개의 인수(추적할 키)를 받으며, 두 번째 인수를 통해 얼마나 증감할지 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드는 특정 조건에 따라 컨텍스트에 데이터를 추가할 수 있게 해줍니다. 첫 번째 클로저는 조건이 `true`일 때 실행되며, 두 번째 클로저는 `false`일 때 실행됩니다:

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

`scope` 메서드는 특정 콜백이 실행되는 동안 일시적으로 컨텍스트를 수정하고, 콜백 실행이 끝나면 원래의 컨텍스트 상태로 되돌릴 수 있게 해줍니다. 또한, 콜백이 실행되는 동안 컨텍스트에 병합할 추가 데이터(두 번째, 세 번째 인수)도 전달할 수 있습니다.

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
> 스코프 클로저 내부에서 컨텍스트의 객체를 수정하는 경우, 이 변경은 스코프 바깥에도 영향을 미치게 됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택"이라는 개념도 제공합니다. 스택은 데이터를 추가한 순서대로 저장하는 리스트입니다. `push` 메서드를 사용해 스택에 정보를 추가할 수 있습니다:

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

스택은 요청 처리 과정에서 발생하는 이벤트나 이력 정보를 추적할 때 유용합니다. 예를 들어, 쿼리가 실행될 때마다 이벤트 리스너에서 스택에 정보를 추가하여, 쿼리 SQL과 소요 시간을 튜플로 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains` 및 `hiddenStackContains` 메서드를 사용하면, 스택에 특정 값이 있는지 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

이 메서드들은 두 번째 인수로 클로저를 받아 값 비교 방식을 세밀하게 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 가져오기

컨텍스트에서 정보를 조회하려면 `Context` 파사드의 `get` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only`와 `except` 메서드를 사용하면 컨텍스트에서 특정 정보만 부분적으로 추출할 수 있습니다:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

`pull` 메서드를 사용하면, 컨텍스트에서 정보를 가져오자마자 즉시 해당 정보를 컨텍스트에서 제거할 수 있습니다:

```php
$value = Context::pull('key');
```

[스택](#stacks)에 저장된 컨텍스트 데이터를 조회하고 싶을 경우, `pop` 메서드를 사용하여 스택에서 항목을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

컨텍스트에 저장된 전체 정보를 한 번에 가져오려면 `all` 메서드를 호출하면 됩니다:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

컨텍스트에 특정 키가 저장되어 있는지 확인하려면 `has` 및 `missing` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 저장된 값이 무엇이든(예: `null`일지라도) 키가 존재하면 항상 `true`를 반환합니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거하기

`forget` 메서드는 현재 컨텍스트에서 특정 키와 그 값을 제거합니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

여러 키를 한 번에 제거하려면 키 배열을 `forget`에 전달하세요:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨김 컨텍스트

컨텍스트는 "숨김" 데이터를 저장하는 기능도 제공합니다. 이렇게 저장한 정보는 로그에 함께 기록되지 않으며, 위에서 설명한 일반 데이터 조회 방식으로도 접근할 수 없습니다. 숨김 컨텍스트에는 별도의 메서드들을 사용합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

"숨김" 관련 메서드는 위에서 설명한 일반 메서드와 거의 동일한 기능을 제공합니다:

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

컨텍스트에서는 하이드레이션(hydration) 및 디하이드레이션(dehydration) 과정에 후킹(hook)할 수 있도록 두 가지 이벤트를 제공합니다.

예를 들어, 애플리케이션의 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더를 활용해 `app.locale` 설정값을 변경한다고 가정해 봅시다. 컨텍스트의 이벤트를 사용하면, 요청 중 설정값을 캡처해두었다가 큐에서 작업이 처리될 때 복원할 수 있습니다. 이로써, 큐에서 전송되는 알림도 올바른 `app.locale` 값으로 설정될 수 있습니다. 아래에서 이 과정과 [숨김 데이터](#hidden-context) 활용법을 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이팅(Dehydrating)

작업이 큐에 디스패치될 때마다 컨텍스트에 있던 데이터는 "디하이드레이션"되어 작업 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드를 이용하면 디하이드레이션 시점에 호출할 클로저를 등록할 수 있습니다. 이 클로저 내에서, 큐 작업에 공유할 데이터를 추가로 가공하거나 변경할 수 있습니다.

보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 `dehydrating` 콜백을 등록합니다:

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
> `dehydrating` 콜백 내부에서는 `Context` 파사드를 사용하지 않는 것이 좋습니다. 현재 프로세스의 컨텍스트가 변경될 수 있으므로, 반드시 콜백에 전달된 저장소(repository) 객체만 수정해야 합니다.

<a name="hydrated"></a>
### 하이드레이티드(Hydrated)

큐에서 작업이 실행되면, 작업과 함께 공유된 모든 컨텍스트 정보가 다시 "하이드레이션"되어 현재 컨텍스트로 복원됩니다. `Context::hydrated` 메서드를 사용하면 이 하이드레이션 과정에서 호출할 클로저를 등록할 수 있습니다.

보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 `hydrated` 콜백을 등록합니다:

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
> `hydrated` 콜백 내부에서는 `Context` 파사드를 사용하지 말고, 반드시 콜백에 전달된 저장소(repository) 객체만 수정해야 합니다.
