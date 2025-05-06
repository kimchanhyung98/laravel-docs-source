# Context

- [소개](#introduction)
    - [작동 원리](#how-it-works)
- [컨텍스트 캡처하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회하기](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거하기](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [비활성화(Dehydrating)](#dehydrating)
    - [복원(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개

Laravel의 "컨텍스트(context)" 기능을 사용하면 애플리케이션 내에서 실행되는 요청, 작업(job), 명령(command) 전반에 걸쳐 정보를 캡처, 조회 및 공유할 수 있습니다. 이렇게 캡처된 정보는 애플리케이션이 기록하는 로그에도 포함되어, 로그 엔트리가 작성되기 전까지의 코드 실행 히스토리를 더 깊이 파악할 수 있게 하며, 분산 시스템 전체에서 실행 흐름을 추적할 수 있도록 해줍니다.

<a name="how-it-works"></a>
### 작동 원리

Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장 로깅 기능과 함께 실제로 사용해보는 것입니다. 먼저, `Context` 파사드를 사용하여 [컨텍스트에 정보를 추가](#capturing-context)할 수 있습니다. 아래 예시에서는 [미들웨어](/docs/{{version}}/middleware)를 사용하여 모든 요청에 대해 요청 URL과 고유한 트레이스 ID를 컨텍스트에 추가하는 방법을 보여줍니다.

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

컨텍스트에 추가된 정보는 해당 요청 전체에서 작성된 모든 [로그 엔트리](/docs/{{version}}/logging)에 자동으로 메타데이터로 포함됩니다. 컨텍스트를 메타데이터로 추가하면, 개별 로그 엔트리에 직접 전달된 정보와 `Context`를 통해 공유된 정보를 구분할 수 있습니다. 예를 들어, 아래와 같이 로그를 기록한다고 가정해보겠습니다.

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

기록된 로그에는 로그 엔트리에 전달된 `auth_id`뿐만 아니라, 컨텍스트의 `url`과 `trace_id`도 메타데이터로 포함됩니다.

```
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐로 디스패치된 작업(job)에도 그대로 전달됩니다. 예를 들어, 컨텍스트에 정보를 추가한 뒤 `ProcessPodcast` 작업을 큐에 디스패치한다고 해봅시다.

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때 컨텍스트에 저장된 모든 정보가 해당 작업과 함께 캡처되고 공유됩니다. 이렇게 캡처된 정보는 작업 실행 시 현재 컨텍스트에 다시 주입(hydrate)됩니다. 만약 작업의 handle 메서드에서 로그를 기록한다면:

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

결과적으로, 해당 로그 엔트리에는 원래 이 작업을 디스패치했던 요청 당시 컨텍스트에 추가됐던 정보 역시 포함됩니다.

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

위 예시는 Laravel의 내장 로깅 관련 기능에 초점을 맞췄지만, 아래 문서에서는 컨텍스트로 HTTP 요청과 큐 작업 사이에 정보를 공유하는 방법, 그리고 [숨겨진 컨텍스트 데이터](#hidden-context)를 추가하는 방법 등도 자세히 다룹니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처하기

`Context` 파사드의 `add` 메서드를 사용하여 현재 컨텍스트에 정보를 저장할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 개의 항목을 한 번에 추가하려면 연관 배열을 `add` 메서드에 전달하면 됩니다.

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 같은 키를 가진 기존 값을 덮어씁니다. 만약 해당 키가 없을 때만 컨텍스트에 정보를 추가하고 싶다면, `addIf` 메서드를 사용할 수 있습니다.

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드를 사용하여 주어진 조건에 따라 데이터를 컨텍스트에 추가할 수 있습니다. 조건이 `true`이면 첫 번째 클로저가 실행되고, `false`이면 두 번째 클로저가 실행됩니다.

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="stacks"></a>
### 스택

컨텍스트는 "스택(stack)"을 생성할 수 있는 기능을 제공합니다. 스택은 데이터가 추가된 순서대로 저장되는 리스트입니다. `push` 메서드를 사용하여 스택에 정보를 추가할 수 있습니다.

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

스택은 요청의 이력을 남기거나, 애플리케이션 전체에서 발생하는 이벤트 등을 저장하는 데 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 실행 시간을 튜플로 스택에 추가하는 이벤트 리스너를 만들 수도 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains` 및 `hiddenStackContains` 메서드를 사용해 값이 스택에 포함되어 있는지 확인할 수 있습니다.

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

이 두 메서드는 두 번째 인수로 클로저를 받을 수도 있어 값 비교 작업을 세밀하게 제어할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회하기

`Context` 파사드의 `get` 메서드를 이용해 컨텍스트에서 정보를 조회할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` 메서드는 컨텍스트에서 일부 정보만 추출합니다.

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` 메서드는 컨텍스트에서 정보를 조회한 후 곧바로 제거합니다.

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)에 저장되어 있다면 `pop` 메서드를 사용해 스택에서 항목을 꺼낼 수 있습니다.

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

`has` 및 `missing` 메서드를 사용해 해당 키에 값이 저장되어 있는지 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 저장된 값의 값과 상관없이, 즉 값이 `null`이어도 `true`를 반환합니다.

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거하기

`forget` 메서드를 사용하면 현재 컨텍스트에서 키와 해당 값을 제거할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

배열을 전달하면 여러 키를 한 번에 제거할 수도 있습니다.

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트

컨텍스트는 "숨겨진" 데이터를 저장할 수 있는 기능을 제공합니다. 숨겨진 정보는 로그에 추가되지 않으며, 위에서 설명한 데이터 조회 메서드로는 접근할 수 없습니다. 숨겨진 컨텍스트 데이터는 별도의 메서드를 통해 조작합니다.

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

"숨겨진" 메서드는 위에서 설명한 비숨김(일반) 메서드와 동일한 기능을 제공합니다.

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

컨텍스트는 컨텍스트의 비활성화(탈수, dehydration) 및 복원(수화, hydration) 과정에 연결할 수 있도록 두 가지 이벤트를 디스패치합니다.

이러한 이벤트의 사용 예를 들자면, 애플리케이션 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더를 바탕으로 `app.locale` 설정값을 지정할 때를 생각할 수 있습니다. 컨텍스트 이벤트를 활용하면 이 값을 요청 중에 캡처하고 큐에서 복원함으로써, 큐에서 발송되는 알림 등이 올바른 `app.locale`을 사용하도록 할 수 있습니다. 아래 문서는 이를 달성하기 위해 컨텍스트 이벤트와 [숨겨진](#hidden-context) 데이터를 어떻게 활용할 수 있는지 보여줍니다.

<a name="dehydrating"></a>
### 비활성화(Dehydrating)

작업(job)이 큐에 디스패치될 때마다 컨텍스트 내부의 데이터는 "비활성화(탈수)" 되어 작업의 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드는 비활성화 과정에서 호출되는 클로저를 등록할 수 있습니다. 이 클로저 내부에서, 큐 작업과 함께 공유될 데이터를 수정할 수 있습니다.

일반적으로, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 `dehydrating` 콜백을 등록하는 것이 좋습니다.

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
> `dehydrating` 콜백 내부에서는 `Context` 파사드를 사용하지 마세요. 현재 프로세스의 컨텍스트가 변경될 수 있습니다. 꼭 콜백에 전달된 저장소(repository)만 수정해야 합니다.

<a name="hydrated"></a>
### 복원(Hydrated)

큐에 작업이 들어가 실행되기 시작하면, 해당 작업에 공유된 컨텍스트가 현재 컨텍스트로 "복원(수화)"됩니다. `Context::hydrated` 메서드는 복원 과정에서 호출되는 클로저를 등록할 수 있습니다.

일반적으로, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 `hydrated` 콜백을 등록하는 것이 좋습니다.

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
> `hydrated` 콜백 내부에서는 `Context` 파사드를 사용하지 말고, 반드시 콜백에 전달된 저장소(repository)만 변경해야 합니다.