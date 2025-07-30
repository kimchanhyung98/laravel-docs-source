# 속도 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 간단하게 사용할 수 있는 속도 제한(rate limiting) 추상화를 제공합니다. 이 기능은 애플리케이션의 [캐시](cache)와 연동하여, 일정 기간 내에 어떤 동작을 제한하는 간단한 방법을 제공합니다.

> [!TIP]
> 수신 HTTP 요청에 대한 속도 제한에 관심이 있으시다면 [rate limiter 미들웨어 문서](routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키로 정의된 기본 캐시를 사용합니다. 하지만, `cache` 설정 파일 내에 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 별도로 지정할 수도 있습니다:

```php
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 페이사드를 통해 속도 제한기와 상호작용할 수 있습니다. 속도 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드이며, 지정한 초 단위 시간 동안 특정 콜백 실행 횟수를 제한합니다.

`attempt` 메서드는 시도가 남아있지 않을 때 `false`를 반환하고, 그렇지 않으면 콜백 결과나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 속도 제한 "키"이며, 제한할 동작을 나타내는 임의의 문자열입니다:

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
  return '메시지를 너무 많이 보냈습니다!';
}
```

<a name="manually-incrementing-attempts"></a>
### 시도 횟수 수동 증가

속도 제한기와 수동으로 상호작용하고 싶다면 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 호출하여 특정 속도 제한 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return '시도 횟수를 초과했습니다!';
}
```

또는 `remaining` 메서드를 사용하여 특정 키에 남은 시도 횟수를 조회할 수 있습니다. 남은 재시도 횟수가 있다면, `hit` 메서드를 호출하여 총 시도 횟수를 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::hit('send-message:'.$user->id);

    // 메시지 전송...
}
```

<a name="determining-limiter-availability"></a>
#### 속도 제한 가능 시간 확인

키에 남은 시도 횟수가 없을 경우, `availableIn` 메서드는 다시 시도할 수 있을 때까지 남은 시간을 초 단위로 반환합니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return $seconds.'초 후에 다시 시도할 수 있습니다.';
}
```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

특정 속도 제한 키에 대한 시도 횟수를 `clear` 메서드로 초기화할 수 있습니다. 예를 들어, 수신자가 메시지를 읽었을 때 시도 횟수를 초기화할 수 있습니다:

```php
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 메시지를 읽음 상태로 표시합니다.
 *
 * @param  \App\Models\Message  $message
 * @return \App\Models\Message
 */
public function read(Message $message)
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```