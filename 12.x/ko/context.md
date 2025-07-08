# 컨텍스트 (Context)

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [컨텍스트 저장하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회하기](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 삭제하기](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이팅(Dehydrating)](#dehydrating)
    - [하이드레이티드(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

라라벨의 "컨텍스트(context)" 기능을 사용하면, 애플리케이션 내에서 동작하는 요청, 잡, 명령어 전반에 걸쳐 정보를 저장하고, 조회하며, 공유할 수 있습니다. 이렇게 캡처된 정보는 애플리케이션에서 기록하는 로그에도 자동으로 포함되어, 로그가 작성되기 전에 실행된 코드의 이력을 더 깊이 파악할 수 있게 해주며, 분산 시스템 전반에 걸친 실행 흐름도 추적할 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식

라라벨의 컨텍스트 기능을 가장 쉽게 이해하려면, 내장된 로그 기능과 함께 직접 동작하는 모습을 살펴보는 것이 좋습니다. 우선 [컨텍스트에 정보 추가하기](#capturing-context)를 위해 `Context` 파사드를 사용할 수 있습니다. 아래 예시에서는 모든 들어오는 요청마다 요청 URL과 고유한 트레이스 ID를 컨텍스트에 추가하는 [미들웨어](/docs/12.x/middleware)를 만들어 사용합니다:

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

컨텍스트에 추가된 정보는 요청 처리 과정에서 기록되는 [로그 항목들](/docs/12.x/logging)의 메타데이터로 자동으로 추가됩니다. 이렇게 컨텍스트를 메타데이터로 첨부하면, 개별 로그에 직접 전달된 정보와 `Context`를 통해 공유되는 정보를 명확히 구분할 수 있습니다. 예를 들어, 아래와 같이 로그를 기록한다고 가정해보겠습니다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

작성된 로그에는 로그 항목에 넘긴 `auth_id`뿐만 아니라, 컨텍스트의 `url`과 `trace_id`도 메타데이터로 함께 포함됩니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐에 디스패치하는 잡에도 자동으로 전달됩니다. 예를 들어, 컨텍스트에 일부 정보를 추가한 뒤 `ProcessPodcast` 잡을 큐로 디스패치한다고 가정해봅시다:

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

잡이 디스패치될 때, 현재 컨텍스트에 저장된 모든 정보가 함께 캡처되어 잡과 공유됩니다. 잡이 실행될 때는, 이렇게 캡처된 정보가 다시 현재 컨텍스트로 복원됩니다(하이드레이션). 즉, 잡의 handle 메서드에서 로그를 작성한다면:

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

이 때 기록되는 로그 항목에도, 원래 해당 잡을 디스패치한 요청에서 컨텍스트에 추가했던 정보가 함께 남게 됩니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

지금까지는 주로 라라벨의 내장 로그와 관련된 컨텍스트 기능에 집중했지만, 아래 문서에서는 컨텍스트가 HTTP 요청과 큐 잡을 넘나들며 정보를 공유하는 방식, 그리고 [로그에 기록되지 않는 숨겨진 컨텍스트 데이터](#hidden-context)까지 어떻게 다룰 수 있는지 자세히 설명합니다.

<a name="capturing-context"></a>
## 컨텍스트 저장하기

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 값을 한 번에 추가하려면, 연관 배열을 `add` 메서드에 전달하면 됩니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 같은 키가 이미 존재할 경우, 기존 값을 덮어씁니다. 만약 해당 키가 아직 존재하지 않을 때만 정보를 추가하고 싶다면 `addIf` 메서드를 사용하세요:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트에는 특정 키 값을 증가시키거나 감소시키는 편리한 메서드도 제공됩니다. 이 메서드들은 최소 한 개의 인자(추적할 키)를 받으며, 두 번째 인자로 증가/감소시킬 값을 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드를 사용하면 특정 조건에 따라 컨텍스트에 데이터를 추가할 수 있습니다. 첫 번째 클로저는 조건이 `true`일 때 실행되고, 두 번째 클로저는 조건이 `false`일 때 실행됩니다:

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

`scope` 메서드는 지정한 콜백(클로저)이 실행되는 동안에만 임시로 컨텍스트를 변경하고, 실행이 끝나면 원래 상태로 되돌리는 기능을 제공합니다. 또한 클로저가 실행되는 동안 컨텍스트에 병합할 추가 데이터(두 번째, 세 번째 인자)도 전달할 수 있습니다.

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
> 스코프 클로저 내부에서 컨텍스트 안의 객체를 수정하는 경우, 그 변화는 스코프 바깥에도 반영됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택(stack)" 기능도 제공합니다. 스택은 데이터를 추가된 순서대로 저장하는 리스트로, `push` 메서드를 이용해 값을 추가할 수 있습니다:

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

스택은 요청의 이력을 남기거나, 애플리케이션 곳곳에서 발생하는 이벤트 정보를 추적할 때 유용하게 사용할 수 있습니다. 예를 들어 쿼리가 실행될 때마다 쿼리 SQL과 실행 시간을 튜플 형태로 스택에 남기는 이벤트 리스너를 만들 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// AppServiceProvider.php에서...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

스택에 특정 값이 존재하는지 확인하려면 `stackContains`와 `hiddenStackContains` 메서드를 사용할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains` 및 `hiddenStackContains` 메서드는 두 번째 인자로 클로저를 받을 수도 있어서, 값 비교 방식을 보다 세밀하게 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회하기

컨텍스트에 저장된 정보를 조회하려면 `Context` 파사드의 `get` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

컨텍스트에서 일부 키만 골라 조회하려면 `only`, 일부 키를 제외하고 조회하려면 `except` 메서드를 사용할 수 있습니다:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

`pull` 메서드를 사용하면 정보를 조회함과 동시에 해당 값을 컨텍스트에서 즉시 제거할 수 있습니다:

```php
$value = Context::pull('key');
```

[스택](#stacks)에 저장된 컨텍스트 데이터를 꺼내오려면 `pop` 메서드를 사용할 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

`remember`와 `rememberHidden` 메서드는, 요청한 정보가 존재하지 않을 때 클로저가 반환하는 값을 컨텍스트에 추가하고 그 값을 반환하는 방식으로 데이터를 가져옵니다:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

컨텍스트에 저장된 모든 정보를 가져오고 싶다면 `all` 메서드를 호출하면 됩니다:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

컨텍스트에 주어진 키의 값이 존재하는지 확인하려면 `has`와 `missing` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 해당 키에 저장된 값의 실제 존재 여부와 관계없이(예: 값이 `null`이더라도) 항상 해당 키가 존재하면 `true`를 반환합니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 삭제하기

`forget` 메서드를 사용하면 현재 컨텍스트에서 원하는 키와 그 값을 제거할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

여러 키를 한 번에 삭제하려면 배열을 `forget` 메서드에 전달하면 됩니다:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트

컨텍스트는 "숨겨진(hidden)" 데이터를 저장하는 기능도 제공합니다. 이러한 숨겨진 데이터는 로그에 추가되거나, 앞에서 설명한 일반 데이터 조회 메서드를 통해 접근되지 않습니다. 숨겨진 컨텍스트 정보를 다루기 위해서는 별도의 메서드 집합을 사용합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

이 "숨김" 메서드들은 앞서 소개한 일반 컨텍스트 메서드와 거의 동일한 기능을 제공합니다:

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
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## 이벤트

컨텍스트는 하이드레이션(hydration) 및 디하이드레이션(dehydration) 과정에 훅(hook)을 추가할 수 있도록 두 가지 이벤트를 디스패치합니다.

이 이벤트가 어떻게 활용될 수 있는지 예시로 설명해보겠습니다. 만약 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더를 기준으로 `app.locale` 설정 값을 지정하는 경우, 컨텍스트의 이벤트를 이용해 이 값을 요청 중에 캡처하고 큐로 전달할 수 있습니다. 그러면 큐에서 처리되는 알림(notification) 등도 올바른 `app.locale` 값을 사용할 수 있게 됩니다. 아래 문서에서 컨텍스트 이벤트와 [숨겨진 데이터](#hidden-context)를 활용하는 방법을 구체적으로 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이팅(Dehydrating)

잡이 큐로 디스패치될 때, 컨텍스트의 데이터는 "디하이드레이트(dehydrate)"되어 잡의 페이로드와 함께 저장됩니다. `Context::dehydrating` 메서드를 이용하면, 디하이드레이팅 과정 중에 호출될 클로저를 등록할 수 있습니다. 이 클로저 내부에서 큐 잡에 공유될 데이터를 원하는 대로 수정할 수 있습니다.

일반적으로, `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 등록하는 것이 좋습니다:

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
> `dehydrating` 콜백 내부에서는 `Context` 파사드를 사용하지 마세요. 현재 프로세스의 컨텍스트가 변경될 수 있습니다. 반드시 콜백에 전달된 저장소(Repository) 객체만 다루어야 합니다.

<a name="hydrated"></a>
### 하이드레이티드(Hydrated)

큐에 저장된 잡이 실제로 실행될 때, 잡과 함께 공유된 컨텍스트가 현재 컨텍스트로 "하이드레이트(hydrate)"됩니다. `Context::hydrated` 메서드를 사용하면, 이 하이드레이션 과정 중에 호출할 클로저를 등록할 수 있습니다.

일반적으로, `hydrated` 콜백도 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 등록합니다:

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
> `hydrated` 콜백 내부에서도 `Context` 파사드를 사용하지 말고, 반드시 콜백에 전달된 저장소(Repository) 객체만 사용해야 합니다.
