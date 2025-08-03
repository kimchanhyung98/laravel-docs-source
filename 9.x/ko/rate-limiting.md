# 속도 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 간단하게 사용할 수 있는 속도 제한 추상화를 제공하며, 애플리케이션의 [캐시](cache)와 함께 지정된 시간 동안 특정 동작을 제한하는 쉽게 사용할 수 있는 방법을 제공합니다.

> [!NOTE]
> 들어오는 HTTP 요청에 대한 속도 제한에 관심이 있다면, [속도 제한 미들웨어 문서](routing#rate-limiting)를 참조하세요.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키에 정의된 기본 캐시를 사용합니다. 하지만, 애플리케이션의 `cache` 설정 파일 내 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 명시적으로 지정할 수도 있습니다:

```
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 페이사드를 사용하여 속도 제한기와 상호작용할 수 있습니다. 속도 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 지정한 초 동안 특정 콜백에 대해 속도 제한을 적용합니다.

`attempt` 메서드는 더 이상 시도할 수 없을 경우 `false`를 반환하며, 그렇지 않은 경우 콜백의 결과나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 제한할 작업을 표현하는 임의의 문자열인 속도 제한 "키"입니다:

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

<a name="manually-incrementing-attempts"></a>
### 시도 횟수 수동 증가

속도 제한기와 수동으로 상호작용하고 싶다면 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용해 특정 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}
```

또는 `remaining` 메서드를 사용해 특정 키에 남은 시도 횟수를 조회할 수 있습니다. 남은 시도가 있을 경우 `hit` 메서드를 호출하여 시도 횟수를 증가시킬 수 있습니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::hit('send-message:'.$user->id);

    // Send message...
}
```

<a name="determining-limiter-availability"></a>
#### 제한기 사용 가능 시간 확인

키에 더 이상 시도가 남아 있지 않은 경우, `availableIn` 메서드는 다시 시도 가능할 때까지 남은 시간을 초 단위로 반환합니다:

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}
```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 메서드를 사용하면 특정 속도 제한 키에 대한 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 메시지를 읽었을 때 시도 횟수를 초기화할 수 있습니다:

```
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
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