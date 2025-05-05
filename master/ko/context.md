# Context

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [탈수(Dehydrating)](#dehydrating)
    - [수화(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

Laravel의 "컨텍스트(context)" 기능을 사용하면 애플리케이션 내에서 실행되는 요청, 작업(jobs), 명령(command) 전반에 걸쳐 정보를 캡처, 조회 및 공유할 수 있습니다. 캡처된 정보는 애플리케이션이 기록한 로그에도 자동으로 포함되어, 로그가 작성되기 전에 발생한 코드 실행 이력을 더 깊이 파악하고 분산 시스템 전반의 실행 흐름을 쉽게 추적할 수 있게 해줍니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능과 함께 실제 사용 예시를 보는 것입니다. 먼저, `Context` 파사드를 사용해 [컨텍스트에 정보를 추가](#capturing-context)할 수 있습니다. 아래 예시에서는 [미들웨어](/docs/{{version}}/middleware)를 이용해 모든 들어오는 요청마다 요청 URL과 고유한 트레이스 ID를 컨텍스트에 추가합니다:

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

컨텍스트에 추가된 정보는 요청 전체에서 작성되는 [로그 항목](/docs/{{version}}/logging)에 메타데이터로 자동으로 붙어서 기록됩니다. 컨텍스트 정보를 메타데이터로 추가하면, 개별 로그 항목에 전달된 정보와 `Context`를 통해 공유된 정보를 구분할 수 있습니다. 예를 들어, 다음과 같이 로그를 작성했다고 가정해봅시다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

기록된 로그는 로그 항목에 전달된 `auth_id`뿐만 아니라 컨텍스트의 `url`과 `trace_id`도 메타데이터로 포함합니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐에 디스패치된 작업(job)에서도 사용할 수 있습니다. 예를 들어, 컨텍스트에 정보를 추가한 뒤에 `ProcessPodcast` 작업을 큐에 디스패치한다고 가정합시다:

```php
// 미들웨어 내에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러 내에서...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때, 현재 컨텍스트에 저장된 정보가 캡처되어 작업과 함께 공유됩니다. 그리고 해당 작업이 실행되는 동안 캡처된 정보가 현재 컨텍스트에 다시 수화(hydrate)됩니다. 따라서 작업의 handle 메서드에서 로그를 기록하면:

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

작성된 로그 항목에는 작업을 디스패치한 요청 중에 컨텍스트에 추가된 정보가 함께 들어갑니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

여기서는 주로 Laravel의 내장 로깅 관련 컨텍스트 기능에 초점을 맞추었지만, 이 문서의 다음 부분에서는 컨텍스트가 HTTP 요청과 큐 작업 간 경계를 넘어 정보를 어떻게 공유할 수 있는지, 그리고 로그 항목과 함께 기록되지 않는 [숨겨진 컨텍스트 데이터](#hidden-context)는 어떻게 추가할 수 있는지 등도 설명합니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처

`Context` 파사드의 `add` 메서드를 사용하여 현재 컨텍스트에 정보를 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 항목을 한 번에 추가하고 싶다면, 연관 배열을 `add` 메서드에 전달하면 됩니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키가 이미 존재한다면 기존 값을 덮어씁니다. 만약 해당 키가 존재하지 않을 때만 정보를 추가하고 싶다면, `addIf` 메서드를 사용할 수 있습니다:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트에는 특정 키에 대한 값을 증가(increment) 또는 감소(decrement)시키는 편리한 메서드도 제공됩니다. 두 메서드 모두 첫 번째 인수로 추적하려는 키를 받고, 두 번째 인수로 증가/감소시킬 양을 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드는 특정 조건에 따라 컨텍스트에 데이터를 추가할 수 있게 해줍니다. 첫 번째 클로저는 조건이 `true`이면 실행되고, 두 번째 클로저는 조건이 `false`이면 실행됩니다:

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

`scope` 메서드는 지정된 콜백 실행 중에만 임시로 컨텍스트를 수정하고, 콜백 실행이 끝나면 컨텍스트를 원래 상태로 복원할 수 있습니다. 또한 콜백 실행 중에 컨텍스트에 병합할 추가 데이터(두 번째, 세 번째 인수)를 전달할 수도 있습니다.

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
> 스코프 클로저 내에서 컨텍스트에 있는 객체를 수정하면, 해당 변경 사항이 스코프 외부에도 반영됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택"을 생성할 수 있습니다. 스택은 추가된 순서대로 데이터를 저장하는 리스트입니다. `push` 메서드를 사용하여 스택에 정보를 추가할 수 있습니다:

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

스택은 요청에 대한 히스토리 정보(예: 애플리케이션 전체에서 발생하는 이벤트 등)를 캡처하는 데 유용합니다. 예를 들어, 쿼리가 실행될 때마다 스택에 push하는 이벤트 리스너를 만들어, 쿼리 SQL과 실행 시간을 튜플로 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains` 및 `hiddenStackContains` 메서드를 사용하여 스택에 값이 포함되어 있는지 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains`와 `hiddenStackContains` 메서드는 두 번째 인수로 클로저를 받을 수도 있어, 값 비교 동작을 더 세밀하게 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회

컨텍스트에서 정보를 조회하려면 `Context` 파사드의 `get` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` 메서드를 사용하면 컨텍스트에 있는 정보 중 일부만 선택적으로 조회할 수 있습니다:

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` 메서드는 컨텍스트에서 정보를 조회한 후 즉시 해당 값을 컨텍스트에서 제거합니다:

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)에 저장되어 있다면, `pop` 메서드로 스택에서 항목을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs')
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

저장된 모든 컨텍스트 정보를 조회하려면 `all` 메서드를 호출하면 됩니다:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

지정된 키에 대해 컨텍스트에 값이 저장되어 있는지 확인하려면 `has`와 `missing` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 저장된 값이 어떤 값이더라도(심지어 `null`이어도) `true`를 반환합니다. 예를 들면:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거

`forget` 메서드는 현재 컨텍스트에서 키와 그 값을 제거할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

여러 키를 한 번에 지우려면, 배열을 `forget` 메서드에 전달하면 됩니다:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트

컨텍스트는 "숨겨진" 데이터를 저장할 수 있는 기능을 제공합니다. 숨겨진 정보는 로그에 포함되지 않으며, 위에서 설명한 일반 데이터 조회 메서드로 접근할 수 없습니다. 숨겨진 컨텍스트 정보를 다루기 위한 별도의 메서드 집합이 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

"숨김" 메서드는 앞서 설명한 비숨김용 메서드들과 동일한 기능을 제공합니다:

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

컨텍스트는 수화(hydration) 및 탈수(dehydration) 과정에서 후킹(중간 개입)할 수 있도록 두 가지 이벤트를 디스패치합니다.

이러한 이벤트의 사용 예시로, 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더값을 바탕으로 `app.locale` 설정 값을 지정하는 경우를 들 수 있습니다. 컨텍스트 이벤트를 사용하면 요청 중에 해당 값을 캡처하고, 큐 작업에서도 값을 복원할 수 있어, 큐에서 전송되는 알림 등에서도 올바른 `app.locale` 값이 반영되게 할 수 있습니다. 이는 컨텍스트 이벤트와 [숨겨진](#hidden-context) 데이터를 활용해 구현할 수 있으며, 아래에 구체적인 방법이 나와 있습니다.

<a name="dehydrating"></a>
### 탈수(Dehydrating)

작업이 큐에 디스패치될 때마다 컨텍스트에 저장된 데이터는 "탈수(dehydrate)"되어 작업 페이로드와 함께 저장됩니다. `Context::dehydrating` 메서드를 통해 탈수 과정에서 실행할 클로저를 등록할 수 있습니다. 이 클로저 안에서는 큐 작업과 공유할 데이터를 변경할 수도 있습니다.

보통 `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에 등록하는 것이 일반적입니다:

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
> `dehydrating` 콜백 내에서는 `Context` 파사드를 사용하지 마세요. 그렇게 하면 현재 프로세스의 컨텍스트가 바뀌게 됩니다. 콜백에 전달된 repository만 수정하도록 하세요.

<a name="hydrated"></a>
### 수화(Hydrated)

큐 작업이 실행될 때, 큐 작업과 함께 공유된 컨텍스트 정보는 현재 컨텍스트에 "수화(hydrate)"되어 복원됩니다. `Context::hydrated` 메서드를 이용하면 수화 과정 동안 실행할 클로저를 등록할 수 있습니다.

보통 `hydrated` 콜백도 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 등록합니다:

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
> `hydrated` 콜백 내에서는 `Context` 파사드를 사용하지 말고, 콜백에 전달된 repository만 수정하세요.
