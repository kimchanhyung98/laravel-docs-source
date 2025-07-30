# 속도 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 수 수동 증가](#manually-incrementing-attempts)
    - [시도 수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 사용하기 간편한 속도 제한(rate limiting) 추상화를 제공하며, 애플리케이션의 [캐시](cache)와 함께 동작하여 지정된 시간 동안 특정 작업을 제한하는 쉬운 방법을 제시합니다.

> [!NOTE]
> 들어오는 HTTP 요청에 대한 속도 제한에 관심이 있다면, [rate limiter middleware 문서](/docs/master/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
### 캐시 설정 (Cache Configuration)

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키로 정의된 기본 캐시 드라이버를 사용합니다. 하지만, 속도 제한기에 별도의 캐시 드라이버를 지정하고 싶다면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 정의하여 설정할 수 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하면 속도 제한기와 상호작용할 수 있습니다. 속도 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 지정된 초 동안 주어진 콜백의 실행을 제한합니다.

`attempt` 메서드는 남아있는 시도가 없으면 `false`를 반환하며, 그렇지 않으면 콜백 실행 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 제한할 작업을 나타내는 문자열인 속도 제한기 "키"(key)입니다:

```php
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // 메시지 전송 처리...
    }
);

if (! $executed) {
  return '너무 많은 메시지를 보냈습니다!';
}
```

필요하다면 `attempt` 메서드의 네 번째 인수로 "감쇠 시간(decay rate)"을 제공할 수 있으며, 이는 시도 횟수가 리셋되기까지의 초 단위 시간을 의미합니다. 예를 들어, 아래 코드는 2분마다 5회의 시도를 허용하도록 설정합니다:

```php
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // 메시지 전송 처리...
    },
    $decayRate = 120,
);
```

<a name="manually-incrementing-attempts"></a>
### 시도 수 수동 증가 (Manually Incrementing Attempts)

속도 제한기와 직접 상호작용하고 싶다면, 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 호출하여 특정 키에 대해 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return '너무 많은 시도가 발생했습니다!';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송 처리...
```

또한, `remaining` 메서드를 사용하여 해당 키에 남은 시도 횟수를 조회할 수 있습니다. 남은 시도가 있을 경우, `increment` 메서드를 호출하여 시도 수를 증가시키면 됩니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // 메시지 전송 처리...
}
```

`increment` 메서드에 원하는 증가량을 지정하면, 한 번에 여러 번 시도 수를 올리는 것도 가능합니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한기 사용 가능 여부 확인

해당 키에 남은 시도 수가 없을 때, `availableIn` 메서드는 다시 시도가 가능해질 때까지 남은 초 수를 반환합니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return $seconds . '초 후에 다시 시도할 수 있습니다.';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송 처리...
```

<a name="clearing-attempts"></a>
### 시도 수 초기화 (Clearing Attempts)

주어진 속도 제한기 키에 대한 시도 수를 초기화하고 싶다면, `clear` 메서드를 사용하면 됩니다. 예를 들어, 메시지가 수신자에게 읽혔을 때 시도 수를 초기화할 수 있습니다:

```php
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 메시지를 읽음으로 표시합니다.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```