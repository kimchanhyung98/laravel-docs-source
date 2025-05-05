# 속도 제한(Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel에는 애플리케이션의 [캐시](cache)와 함께 사용할 수 있는 간단한 속도 제한 추상화 기능이 포함되어 있어, 특정 시간 동안의 모든 동작에 쉽고 유연하게 제한을 걸 수 있습니다.

> [!NOTE]
> 들어오는 HTTP 요청에 대한 속도 제한을 적용하고 싶으시면 [속도 제한 미들웨어 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일에서 `default` 키로 지정된 기본 캐시를 사용합니다. 하지만, `cache` 설정 파일에 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 지정할 수도 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 속도 제한기를 다룰 수 있습니다. 속도 제한기가 제공하는 가장 간단한 방법은 `attempt` 메서드로, 지정한 시간(초) 동안 콜백의 실행 횟수를 제한할 수 있습니다.

`attempt` 메서드는 콜백을 실행할 수 있는 잔여 시도가 없다면 `false`를 반환하며, 실행 가능할 때에는 콜백의 결과값이나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자는 속도 제한 "키"로, 제한하려는 동작을 나타내는 임의의 문자열이면 됩니다:

```php
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // 메시지 전송...
    }
);

if (! $executed) {
  return '너무 많은 메시지를 전송하셨습니다!';
}
```

필요하다면 `attempt` 메서드에 네 번째 인자로 "디케이율"(decay rate), 즉 시도 가능 횟수가 초기화되기까지의 시간(초)을 지정할 수 있습니다. 예를 들어 위의 예제를 수정해서 2분에 5회로 제한할 수 있습니다:

```php
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // 메시지 전송...
    },
    $decayRate = 120,
);
```

<a name="manually-incrementing-attempts"></a>
### 시도 횟수 수동 증가

속도 제한기를 직접 제어하고 싶을 경우 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 호출해 특정 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return '시도 횟수가 너무 많습니다!';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송...
```

또는 `remaining` 메서드를 활용해 특정 키의 남은 시도 횟수를 확인할 수 있습니다. 재시도 가능 횟수가 남아 있다면 `increment` 메서드로 시도 횟수를 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // 메시지 전송...
}
```

시도 횟수를 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 증가값을 전달할 수 있습니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한 가능여부 확인

키의 남은 시도 횟수가 모두 소진되었을 때, `availableIn` 메서드는 다음 시도 가능까지 남은 초(second) 수를 반환합니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return '다시 시도하기까지 '.$seconds.'초 남았습니다.';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송...
```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 메서드를 사용해 특정 속도 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 특정 메시지를 수신자가 읽었을 때 시도 횟수를 초기화할 수 있습니다:

```php
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 메시지를 읽은 상태로 표시합니다.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```
