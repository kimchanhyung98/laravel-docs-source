# 컨텍스트 (Context)

- [소개](#introduction)
    - [작동 원리](#how-it-works)
- [컨텍스트 캡처하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 가져오기](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거하기](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이트(Dehydrating)](#dehydrating)
    - [하이드레이트(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "컨텍스트(context)" 기능은 애플리케이션 내에서 실행되는 요청, 작업(job), 명령어 전반에 걸쳐 정보를 캡처하고, 가져오며, 공유할 수 있게 해줍니다. 이렇게 캡처한 정보는 애플리케이션이 작성하는 로그에도 포함되어, 로그가 기록되기 전에 실행된 주변 코드의 이력을 더 깊게 이해할 수 있게 하고 분산 시스템 전반에 걸친 실행 흐름 추적을 가능하게 합니다.

<a name="how-it-works"></a>
### 작동 원리 (How it Works)

Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능을 사용해 직접 확인하는 것입니다. 우선 `Context` 파사드를 사용하여 [컨텍스트에 정보를 추가](#capturing-context)할 수 있습니다. 다음 예제에서는 [미들웨어](/docs/master/middleware)를 사용해 모든 들어오는 요청마다 요청 URL과 고유한 추적 ID를 컨텍스트에 추가하는 방법을 보여줍니다:

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

컨텍스트에 추가된 정보는 요청 처리 전반에 생성되는 [로그 항목](/docs/master/logging)에 자동으로 메타데이터로 첨부됩니다. 이렇게 컨텍스트 정보를 메타데이터로 덧붙이면, 개별 로그 항목에 전달되는 정보와 `Context`를 통해 공유되는 정보를 구분할 수 있습니다. 예를 들어, 다음과 같은 로그 항목을 작성한다고 가정해봅시다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

작성되는 로그는 `auth_id`를 포함하는 동시에, 컨텍스트에 추가된 `url`과 `trace_id`를 메타데이터로 함께 포함합니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐에 디스패치된 작업에게도 전달됩니다. 예를 들어, 다음과 같이 컨텍스트에 일부 정보를 추가한 뒤 `ProcessPodcast` 작업을 큐에 등록한다고 가정해봅시다:

```php
// 미들웨어 내에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러 내에서...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때, 컨텍스트에 현재 저장된 모든 정보가 함께 캡처되어 작업에 공유됩니다. 작업이 실행되는 동안 캡처된 정보는 다시 현재 컨텍스트로 하이드레이트됩니다. 따라서 만약 작업의 handle 메서드에서 로그를 작성하면 다음과 같이, 작업을 디스패치한 원래 요청에서 추가한 컨텍스트 정보가 함께 포함됩니다:

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

작성된 로그 항목에 포함되는 내용:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

여기서는 Laravel의 컨텍스트가 내장된 로깅 기능과 어떻게 연동되는지에 초점을 맞췄지만, 뒤이어 설명할 문서에서는 컨텍스트를 사용해 HTTP 요청과 큐 작업 간 경계를 넘나들며 정보를 공유하는 방법과, 로그 항목에 기록되지 않는 [숨겨진 컨텍스트 데이터](#hidden-context)를 추가하는 방법도 다룰 것입니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처하기 (Capturing Context)

`Context` 파사드의 `add` 메서드를 사용하여 현재 컨텍스트에 정보를 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 항목을 한 번에 추가하려면, 연관 배열을 `add` 메서드에 전달하세요:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 같은 키가 이미 존재하면 기존 값을 덮어씁니다. 만약 키가 존재하지 않을 때만 정보를 추가하고 싶다면 `addIf` 메서드를 사용하세요:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트는 지정한 키의 값을 증가시키거나 감소시키는 편리한 메서드도 제공합니다. 두 메서드는 최소 한 개의 인수, 즉 추적할 키를 받으며, 두 번째 인수로 증가/감소할 값을 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트 (Conditional Context)

`when` 메서드는 특정 조건에 따라 컨텍스트에 데이터를 추가할 때 유용합니다. 첫 번째 클로저는 조건이 `true`일 때 실행되며, 두 번째 클로저는 조건이 `false`일 때 실행됩니다:

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
#### 스코프 컨텍스트 (Scoped Context)

`scope` 메서드는 주어진 콜백 실행 중에 컨텍스트를 일시적으로 수정하고, 콜백이 종료되면 원래 상태로 복원하는 기능을 제공합니다. 또한 두 번째와 세 번째 인수로 콜백 실행 도중 병합되어야 하는 추가 데이터(일반 및 숨겨진)를 전달할 수 있습니다.

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
// []

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> [!WARNING]
> 스코프 내부 클로저 안에서 컨텍스트 내 객체를 수정하면, 그 변화가 스코프 외부에도 반영됩니다.

<a name="stacks"></a>
### 스택 (Stacks)

컨텍스트는 "스택"이라는 기능도 제공합니다. 스택은 요소가 추가된 순서대로 저장되는 데이터 목록입니다. `push` 메서드로 스택에 정보를 추가할 수 있습니다:

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

스택은 요청 과정에서 발생하는 이벤트 등, 순차적으로 누적되는 이력을 캡처하는 데 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 실행 시간을 튜플로 스택에 저장하는 이벤트 리스너를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains` 및 `hiddenStackContains` 메서드를 사용해 지정한 값이 스택에 포함되어 있는지 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

두 메서드는 두 번째 인수로 클로저도 받아, 값 비교 방식을 세밀하게 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 가져오기 (Retrieving Context)

`Context` 파사드의 `get` 메서드를 사용해 컨텍스트에서 정보를 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` 메서드는 컨텍스트 내 데이터 중 일부만 선택해서 가져올 때 사용합니다:

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` 메서드는 값을 가져오면서 동시에 컨텍스트에서 해당 데이터를 제거합니다:

```php
$value = Context::pull('key');
```

[스택](#stacks)에 저장된 컨텍스트 데이터를 가져올 때는 `pop` 메서드를 사용해 스택의 마지막 항목을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs')
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

컨텍스트에 저장된 모든 정보를 가져오려면 `all` 메서드를 호출하세요:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인 (Determining Item Existence)

`has` 와 `missing` 메서드를 사용해 특정 키가 컨텍스트에 존재하는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 값이 `null`이어도 키가 존재하면 `true`를 반환합니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거하기 (Removing Context)

`forget` 메서드를 사용해 컨텍스트 내 특정 키와 그 값을 제거할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

여러 키를 한 번에 제거하려면 배열로 전달하세요:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트 (Hidden Context)

컨텍스트는 "숨겨진(hidden)" 데이터를 저장할 수도 있습니다. 이 숨겨진 정보는 로그에 첨부되지 않으며, 위에서 설명한 일반 데이터 조회 메서드로 접근할 수 없습니다. 숨겨진 컨텍스트와 상호작용하려면 별도의 메서드 집합을 사용하세요:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

숨겨진 데이터에 대한 메서드 목록은 일반 데이터 메서드와 동일한 기능을 제공합니다:

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
## 이벤트 (Events)

컨텍스트는 컨텍스트의 하이드레이트와 디하이드레이트 과정에 훅을 걸 수 있도록 두 개의 이벤트를 제공합니다.

예를 들어, 애플리케이션 미들웨어에서 HTTP 요청의 `Accept-Language` 헤더를 기반으로 `app.locale` 설정값을 지정했다고 가정합시다. 컨텍스트의 이벤트 기능을 사용하면 이 값을 요청 과정 중에 캡처하여 큐에서 작업을 실행할 때 복원할 수 있어, 큐에서 전송되는 알림들이 올바른 `app.locale` 값을 갖도록 할 수 있습니다. 다음 문서에서는 이와 같은 숨겨진([hidden](#hidden-context)) 데이터를 다루는 방법과 이벤트 사용법을 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이트 (Dehydrating)

작업이 큐에 디스패치될 때, 컨텍스트 데이터는 "디하이드레이트"되어 작업 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드는 디하이드레이션 과정 중 호출할 클로저를 등록하는 데 사용됩니다. 이 클로저 내에서 큐 작업과 공유될 데이터를 변경할 수 있습니다.

일반적으로 `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 등록합니다:

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
> `dehydrating` 콜백 내에서는 `Context` 파사드를 사용하지 마세요. 이는 현재 프로세스의 컨텍스트를 변경하기 때문입니다. 오직 콜백에 전달된 저장소(repository)에 대해서만 변경을 수행해야 합니다.

<a name="hydrated"></a>
### 하이드레이트 (Hydrated)

큐에서 작업이 실행되기 시작할 때, 작업과 함께 공유된 컨텍스트는 "하이드레이트"되어 현재 컨텍스트에 복원됩니다. `Context::hydrated` 메서드를 사용해 하이드레이션 과정 중 실행할 클로저를 등록할 수 있습니다.

일반적으로 `hydrated` 콜백은 애플리케이션 `AppServiceProvider` 내 `boot` 메서드에서 등록합니다:

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
> `hydrated` 콜백 내에서도 `Context` 파사드를 사용하지 말고, 콜백에 전달된 저장소(repository)에 대해서만 변경을 수행하세요.