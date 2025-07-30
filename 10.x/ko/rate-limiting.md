# 요청 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 구성](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [수동으로 시도 횟수 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 간단하게 사용할 수 있는 요청 제한(rate limiting) 추상화를 제공하며, 애플리케이션의 [캐시](cache)와 함께 지정된 시간 동안 특정 작업의 실행 횟수를 제한할 수 있는 쉬운 방법을 제공합니다.

> [!NOTE]  
> 들어오는 HTTP 요청의 요청 제한에 관심이 있으시다면, [rate limiter middleware documentation](routing#rate-limiting)을 참고하시기 바랍니다.

<a name="cache-configuration"></a>
### 캐시 구성 (Cache Configuration)

일반적으로 요청 제한기는 애플리케이션의 `cache` 구성 파일 내 `default` 키에 정의된 기본 캐시 드라이버를 사용합니다. 그러나 요청 제한기가 사용할 캐시 드라이버를 애플리케이션의 `cache` 구성 파일에 `limiter` 키를 정의하여 지정할 수도 있습니다:

```
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

`Illuminate\Support\Facades\RateLimiter` 페이사드를 통해 요청 제한기와 상호작용할 수 있습니다. 요청 제한기가 제공하는 가장 간단한 메서드는 `attempt`로, 지정된 기간 동안 주어진 콜백 실행을 제한합니다.

`attempt` 메서드는 남은 시도 횟수가 없으면 `false`를 반환하며, 그렇지 않으면 콜백 실행 결과나 `true`를 반환합니다. `attempt`의 첫 번째 인자는 제한할 작업을 나타내는 임의의 문자열인 요청 제한기 "키"입니다:

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

필요한 경우, `attempt` 메서드의 네 번째 인자인 "감쇠 시간(decay rate)"을 지정해 시도 가능한 횟수가 초기화되는 시간을 초 단위로 설정할 수 있습니다. 예를 들어, 다음과 같이 2분마다 5번의 시도를 허용하도록 설정할 수 있습니다:

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
### 수동으로 시도 횟수 증가 (Manually Incrementing Attempts)

요청 제한기를 수동으로 제어하고 싶다면, 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 호출해 특정 요청 제한기 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

또는 `remaining` 메서드를 통해 해당 키에 남은 시도 횟수를 조회할 수 있습니다. 남아있는 시도 횟수가 있으면 `increment` 메서드를 호출해서 시도 횟수를 증가시킬 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

특정 요청 제한기 키의 시도 횟수를 1보다 큰 값으로 증가시키고자 할 때는 `increment` 메서드에 증가할 양을 전달할 수 있습니다:

```
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한기 사용 가능 여부 확인

키에 남은 시도가 없으면, `availableIn` 메서드는 다음 시도가 가능해질 때까지 남은 시간을 초 단위로 반환합니다:

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
### 시도 횟수 초기화 (Clearing Attempts)

`clear` 메서드를 사용해 특정 요청 제한기 키에 대한 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 메시지를 확인했을 때 관련 시도 횟수를 초기화할 수 있습니다:

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