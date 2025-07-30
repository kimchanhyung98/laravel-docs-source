# 컨텍스트 (Context)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처하기](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 검색하기](#retrieving-context)
    - [항목 존재 여부 판단](#determining-item-existence)
- [컨텍스트 제거하기](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이팅](#dehydrating)
    - [하이드레이티드](#hydrated)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "컨텍스트" 기능은 애플리케이션 내에서 요청, 잡, 명령어가 실행되는 동안 정보를 캡처하고, 검색하며, 공유할 수 있게 해줍니다. 이렇게 캡처된 정보는 애플리케이션에서 작성하는 로그에도 포함되어, 로그 항목이 기록되기 전에 실행된 코드의 이력에 대한 더 깊은 이해를 제공하며, 분산 시스템 전반의 실행 흐름을 추적할 수 있게 해줍니다.

<a name="how-it-works"></a>
### 작동 방식 (How it Works)

Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능을 실제로 사용하는 것입니다. 시작하려면, `Context` 파사드를 사용하여 [컨텍스트에 정보를 추가](#capturing-context)할 수 있습니다. 예를 들어, [미들웨어](/docs/11.x/middleware)를 사용하여 들어오는 모든 요청에 대해 요청 URL과 고유한 추적 ID를 컨텍스트에 추가할 수 있습니다:

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

컨텍스트에 추가된 정보는 요청 처리 중 작성되는 모든 [로그 항목](/docs/11.x/logging)의 메타데이터로 자동으로 첨부됩니다. 이렇게 컨텍스트를 메타데이터로 추가하면, 개별 로그 항목에 전달된 정보와 `Context`를 통해 공유되는 정보를 구분할 수 있습니다. 예를 들어, 다음과 같이 로그를 작성한다고 가정해 보겠습니다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

작성된 로그에는 `auth_id`가 포함되지만, 컨텍스트의 `url`과 `trace_id`도 메타데이터로 포함됩니다:

```
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐에 디스패치되는 잡에서도 사용할 수 있습니다. 예를 들어, 컨텍스트에 몇 가지 정보를 추가한 후 `ProcessPodcast` 잡을 큐에 디스패치한다고 가정해 보겠습니다:

```php
// 미들웨어에서...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// 컨트롤러에서...
ProcessPodcast::dispatch($podcast);
```

잡이 디스패치될 때, 현재 컨텍스트에 저장된 모든 정보가 캡처되어 잡과 함께 공유됩니다. 그리고 잡 실행 중에는 캡처된 정보가 현재 컨텍스트로 다시 하이드레이트됩니다. 따라서 잡의 handle 메서드에서 로그를 작성하면:

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

생성되는 로그 항목은 원래 잡을 디스패치한 요청 시 컨텍스트에 추가된 정보를 포함하게 됩니다:

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Laravel 컨텍스트의 내장 로깅 관련 기능에 중점을 뒀지만, 다음 문서는 컨텍스트가 HTTP 요청과 큐 잡 경계를 넘나들며 정보를 공유하는 방법과 로그 항목에 작성되지 않는 [숨겨진 컨텍스트 데이터](#hidden-context)를 추가하는 방법도 설명할 것입니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처하기 (Capturing Context)

`Context` 파사드의 `add` 메서드를 사용하여 현재 컨텍스트에 정보를 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

한 번에 여러 항목을 추가하려면, 연관 배열을 `add` 메서드에 전달할 수 있습니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키가 이미 존재할 경우 해당 값을 덮어씁니다. 만약 키가 아직 존재하지 않을 때만 정보를 추가하고 싶다면, `addIf` 메서드를 사용할 수 있습니다:

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

`when` 메서드는 특정 조건에 따라 컨텍스트에 데이터를 추가할 때 사용됩니다. `when`에 전달된 첫 번째 클로저는 조건이 `true`일 때 호출되고, 두 번째 클로저는 조건이 `false`일 때 호출됩니다:

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
### 스택 (Stacks)

컨텍스트는 추가된 순서대로 저장되는 데이터 목록인 "스택"을 생성할 수 있는 기능을 제공합니다. `push` 메서드를 호출하여 스택에 정보를 추가할 수 있습니다:

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

스택은 애플리케이션 전반에 걸쳐 발생하는 이벤트처럼 요청에 대한 이력 정보를 캡처할 때 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 실행 시간을 튜플로 스택에 푸시하는 이벤트 리스너를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains`와 `hiddenStackContains` 메서드를 사용해 특정 값이 스택에 포함되어 있는지 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains`와 `hiddenStackContains` 메서드는 두 번째 인수로 클로저를 받을 수도 있어, 값 비교 작업을 세밀하게 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 검색하기 (Retrieving Context)

`Context` 파사드의 `get` 메서드를 사용해 컨텍스트에서 정보를 검색할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` 메서드는 컨텍스트 내 정보 중 일부만 선택적으로 검색할 때 사용합니다:

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` 메서드는 컨텍스트에서 값을 가져오면서 해당 값을 즉시 컨텍스트에서 제거합니다:

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)에 저장된 경우, `pop` 메서드를 사용해 스택에서 아이템을 꺼낼 수 있습니다:

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
### 항목 존재 여부 판단 (Determining Item Existence)

`has`와 `missing` 메서드를 사용하여 특정 키에 값이 저장되어 있는지 판단할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 값의 내용과 관계없이 키가 존재하면 `true`를 반환합니다. 따라서 `null` 값도 존재하는 것으로 간주됩니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거하기 (Removing Context)

`forget` 메서드는 현재 컨텍스트에서 키와 값을 제거할 때 사용합니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

한 번에 여러 키를 제거하려면, 배열을 `forget` 메서드에 전달하면 됩니다:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트 (Hidden Context)

컨텍스트는 "숨겨진" 데이터를 저장할 수 있습니다. 숨겨진 데이터는 로그에 첨부되지 않으며, 앞서 설명한 데이터 검색 메서드로 접근할 수 없습니다. 숨겨진 컨텍스트 정보와 상호작용하려면 별도의 메서드를 사용해야 합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

"숨겨진" 메서드는 비숨겨진 메서드와 유사한 기능을 제공합니다:

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

컨텍스트는 컨텍스트의 하이드레이션과 디하이드레이션 과정에 개입할 수 있게 해주는 두 가지 이벤트를 발생시킵니다.

예를 들어, 애플리케이션 미들웨어에서 HTTP 요청의 `Accept-Language` 헤더에 따라 `app.locale` 설정 값을 지정한다고 합시다. 컨텍스트 이벤트는 이 값을 요청 중에 캡처하고 큐에서도 복원하여, 큐에서 실행되는 알림이 올바른 `app.locale` 값을 갖도록 보장합니다. 다음 문서는 컨텍스트 이벤트와 [숨겨진](#hidden-context) 데이터를 활용하는 방법을 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이팅 (Dehydrating)

잡이 큐에 디스패치될 때마다 컨텍스트에 저장된 데이터가 "디하이드레이트"되어 잡 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드를 사용하여 디하이드레이션 과정 중 호출될 클로저를 등록할 수 있습니다. 이 클로저 내에서 큐에 공유될 데이터를 변경할 수 있습니다.

일반적으로 `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에 등록해야 합니다:

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
> `dehydrating` 콜백 내에서는 현재 프로세스의 컨텍스트를 변경할 수 있는 `Context` 파사드를 사용하면 안 됩니다. 콜백에 전달된 리포지토리 인스턴스에 대해서만 변경사항을 적용해야 합니다.

<a name="hydrated"></a>
### 하이드레이티드 (Hydrated)

큐 잡이 실행될 때 공유된 컨텍스트가 현재 컨텍스트로 "하이드레이트"되어 복원됩니다. `Context::hydrated` 메서드를 사용하여 하이드레이션 과정 중 호출될 클로저를 등록할 수 있습니다.

일반적으로 `hydrated` 콜백 역시 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에 등록합니다:

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
> `hydrated` 콜백 내에서도 `Context` 파사드를 사용하지 말고, 콜백에 전달된 리포지토리 인스턴스만 변경해야 합니다.