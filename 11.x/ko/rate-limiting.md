# 요청 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 구성](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [수동으로 시도 횟수 증가하기](#manually-incrementing-attempts)
    - [시도 횟수 초기화하기](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 사용하기 간편한 요청 제한(rate limiting) 추상화를 포함하고 있으며, 애플리케이션의 [캐시(cache)](cache)와 함께 지정된 시간 동안 특정 작업을 제한하는 쉬운 방법을 제공합니다.

> [!NOTE]  
> 들어오는 HTTP 요청에 대한 요청 제한에 관심이 있다면, [rate limiter middleware documentation](/docs/11.x/routing#rate-limiting)을 참고하세요.

<a name="cache-configuration"></a>
### 캐시 구성

일반적으로 요청 제한기는 애플리케이션 `cache` 구성 파일 내 `default` 키로 정의된 기본 캐시를 사용합니다. 그러나 요청 제한기가 사용할 캐시 드라이버를 지정하고 싶다면 애플리케이션 `cache` 구성 파일 내에 `limiter` 키를 정의할 수 있습니다:

```
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 요청 제한기와 상호작용할 수 있습니다. 요청 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 지정한 초 동안 주어진 콜백의 실행 횟수를 제한합니다.

`attempt` 메서드는 이용 가능한 시도 횟수가 남아있지 않으면 `false`를 반환하며, 그렇지 않으면 콜백 결과나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 요청 제한 "키"로, 제한할 작업을 나타내는 임의의 문자열을 사용할 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // Send message...
    }
);

if (! $executed) {
  return 'Too many messages sent!';
}
```

필요하다면 `attempt` 메서드에 네 번째 인수로 "감쇠 시간(decay rate)" 즉, 시도 횟수가 초기화되기까지 걸리는 초 단위를 지정할 수 있습니다. 예를 들어, 위 예제를 2분마다 5번의 시도로 변경할 수 있습니다:

```
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // Send message...
    },
    $decayRate = 120,
);
```

<a name="manually-incrementing-attempts"></a>
### 수동으로 시도 횟수 증가하기

요청 제한기를 수동으로 조작하고 싶다면 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드로 특정 요청 제한 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

또한 `remaining` 메서드를 이용해 특정 키에 남은 시도 횟수를 조회할 수 있습니다. 남은 시도가 있다면 `increment` 메서드로 시도 횟수를 증가시킬 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

`increment` 메서드에 증가시킬 횟수를 직접 지정하여 한 번에 여러 번 증가시킬 수도 있습니다:

```
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한 가능 여부 확인하기

키에 남은 시도가 없을 때, `availableIn` 메서드는 다음 시도 가능 시점까지 남은 초 단위 시간을 반환합니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화하기

`clear` 메서드를 이용해 특정 요청 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 메시지가 수신자에게 읽혔을 때 시도 횟수를 초기화할 수 있습니다:

```
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```