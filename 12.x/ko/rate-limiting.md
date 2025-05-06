# 속도 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 [캐시](cache)와 결합하여, 지정된 시간 동안 어떤 동작이든 손쉽게 제한할 수 있는 사용하기 간편한 속도 제한 추상화 기능을 제공합니다.

> [!NOTE]
> 들어오는 HTTP 요청에 대한 속도 제한에 관심이 있다면 [속도 제한 미들웨어 문서](/docs/{{version}}/routing#rate-limiting)를 참고해주세요.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키에 정의된 기본 캐시를 사용합니다. 하지만 `cache` 설정 파일에 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 지정할 수도 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis',
```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 속도 제한기에 접근할 수 있습니다. 속도 제한기에서 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 지정한 초 단위 기간 동안 콜백의 실행을 제한합니다.

콜백에 남은 시도 횟수가 없으면 `attempt` 메서드는 `false`를 반환하며, 남아있는 경우 콜백의 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자로는 속도 제한의 “키”를 지정하는 문자열을 전달하는데, 이 문자열은 제한하고자 하는 동작을 표현할 수 있습니다:

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
  return '너무 많은 메시지를 보냈습니다!';
}
```

필요하다면 `attempt` 메서드에 네 번째 인자를 추가로 전달할 수 있습니다. 이는 “감쇠율(decay rate)”로, 사용 가능한 시도 횟수가 재설정되기까지의 초 단위 시간입니다. 예를 들어, 위의 예시를 2분마다 다섯 번 시도할 수 있게 수정할 수 있습니다:

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

속도 제한기를 수동으로 조작하고자 한다면 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하여 특정 속도 제한 키가 분당 최대 허용 횟수를 초과했는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return '너무 많은 시도를 했습니다!';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송...
```

또한 `remaining` 메서드를 사용하여 특정 키에 대해 남은 시도 횟수를 조회할 수 있습니다. 시도 가능 횟수가 남아있다면 `increment` 메서드를 통해 시도 횟수를 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // 메시지 전송...
}
```

특정 속도 제한 키의 값을 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 증가량을 전달하면 됩니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한 가능 시간 확인

키의 남은 시도 횟수가 없을 때, `availableIn` 메서드는 다음 시도를 할 수 있기까지 남은 초를 반환합니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return ''.$seconds.'초 후 다시 시도할 수 있습니다.';
}

RateLimiter::increment('send-message:'.$user->id);

// 메시지 전송...
```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 메서드를 사용하면 특정 속도 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 메시지를 읽을 때 시도 횟수를 리셋할 수 있습니다:

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