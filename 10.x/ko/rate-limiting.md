# 속도 제한(Rate Limiting)

- [소개](#introduction)
    - [캐시 구성](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 수 수동 증가](#manually-incrementing-attempts)
    - [시도 수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 [캐시](cache)와 함께 사용할 수 있는 간단한 속도 제한 추상화를 포함하고 있어, 지정된 시간 내에 어떤 동작이라도 손쉽게 제한할 수 있도록 지원합니다.

> [!NOTE]  
> 들어오는 HTTP 요청에 대한 속도 제한이 궁금하다면 [속도 제한 미들웨어 문서](routing#rate-limiting)를 참고하세요.

<a name="cache-configuration"></a>
### 캐시 구성

일반적으로 속도 제한기는 애플리케이션의 `cache` 구성 파일 내 `default` 키에 정의된 기본 캐시 드라이버를 사용합니다. 하지만, 애플리케이션의 `cache` 구성 파일에서 `limiter` 키를 정의하여 속도 제한에 사용할 캐시 드라이버를 지정할 수도 있습니다:

    'default' => 'memcached',

    'limiter' => 'redis',

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드(facade)를 사용하여 속도 제한 기능과 상호작용할 수 있습니다. 가장 간단하게 사용할 수 있는 메서드는 `attempt` 메서드로, 주어진 콜백을 지정한 초 동안 제한합니다.

`attempt` 메서드는 콜백을 실행할 수 있는 남은 횟수가 없으면 `false`를 반환합니다. 남은 횟수가 있다면 콜백의 실행 결과나 `true`를 반환합니다. `attempt` 메서드가 받는 첫 번째 인자는 속도 제한의 “키”로, 제한할 동작을 나타내는 임의의 문자열이면 됩니다:

    use Illuminate\Support\Facades\RateLimiter;

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perMinute = 5,
        function() {
            // 메세지 전송...
        }
    );

    if (! $executed) {
      return '너무 많은 메세지를 전송했습니다!';
    }

필요하다면 네 번째 인자로 “감쇠율(decay rate)”, 즉 남은 시도 횟수가 리셋되기까지의 초(second)를 지정할 수 있습니다. 예를 들어, 위 예제를 2분마다 5회 시도로 변경할 수 있습니다:

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perTwoMinutes = 5,
        function() {
            // 메세지 전송...
        },
        $decayRate = 120,
    );

<a name="manually-incrementing-attempts"></a>
### 시도 수 수동 증가

속도 제한기를 직접 제어하려면 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용해 특정 키가 분당 최대 허용 시도를 초과했는지 확인할 수 있습니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        return '시도 횟수가 너무 많습니다!';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // 메세지 전송...

또는, `remaining` 메서드를 사용해 주어진 키의 남은 횟수를 확인할 수 있습니다. 재시도할 수 있다면, `increment` 메서드를 호출하여 시도 횟수를 증가시킬 수 있습니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
        RateLimiter::increment('send-message:'.$user->id);

        // 메세지 전송...
    }

특정 키의 시도 횟수를 한 번 이상 증가시키고 싶다면, `increment` 메서드에 원하는 수치(숫자)를 전달하면 됩니다:

    RateLimiter::increment('send-message:'.$user->id, amount: 5);

<a name="determining-limiter-availability"></a>
#### 제한 가능 여부 판단

더 이상 시도할 수 없는 경우, `availableIn` 메서드는 다음 시도가 가능해지기까지 남은 초(second)를 반환합니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        $seconds = RateLimiter::availableIn('send-message:'.$user->id);

        return '다시 시도하려면 '.$seconds.'초 기다려야 합니다.';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // 메세지 전송...

<a name="clearing-attempts"></a>
### 시도 수 초기화

`clear` 메서드를 사용하여 특정 속도 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 메세지를 읽었을 경우에 시도 횟수를 초기화할 수 있습니다:

    use App\Models\Message;
    use Illuminate\Support\Facades\RateLimiter;

    /**
     * 메세지를 읽음 처리합니다.
     */
    public function read(Message $message): Message
    {
        $message->markAsRead();

        RateLimiter::clear('send-message:'.$message->user_id);

        return $message;
    }