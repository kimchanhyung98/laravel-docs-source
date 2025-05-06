# 요청 제한(Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 [캐시](cache)와 결합하여 특정 시간 동안의 모든 동작을 간편하게 제한할 수 있는 사용하기 쉬운 요청 제한 추상화를 제공합니다.

> [!NOTE]  
> 들어오는 HTTP 요청에 대한 요청 제한(rate limiting)에 관심이 있는 경우, [요청 제한 미들웨어 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 요청 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키에 정의된 기본 캐시를 사용합니다. 하지만, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 정의하여 요청 제한기가 사용할 캐시 드라이버를 별도로 지정할 수 있습니다:

    'default' => env('CACHE_STORE', 'database'),

    'limiter' => 'redis',

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드는 요청 제한기와 상호작용할 때 사용할 수 있습니다. 요청 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 주어진 콜백을 일정 초 동안 횟수 제한으로 실행합니다.

`attempt` 메서드는 더 이상 남은 시도 횟수가 없을 때 `false`를 반환하며, 그렇지 않으면 콜백의 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자는 "요청 제한 키"로, 제한하려는 동작을 나타내는 아무 문자열이나 전달할 수 있습니다:

    use Illuminate\Support\Facades\RateLimiter;

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perMinute = 5,
        function() {
            // 메시지 전송...
        }
    );

    if (! $executed) {
      return '메시지를 너무 많이 전송하셨습니다!';
    }

필요하다면, `attempt` 메서드의 네 번째 인자로 "감쇠 시간(초)"을 지정해 남은 시도 횟수가 리셋되는 시간을 설정할 수 있습니다. 예를 들어, 위의 예시를 수정해 2분마다 5번 시도할 수 있도록 할 수 있습니다:

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perTwoMinutes = 5,
        function() {
            // 메시지 전송...
        },
        $decayRate = 120,
    );

<a name="manually-incrementing-attempts"></a>
### 시도 횟수 수동 증가

요청 제한기와 직접적으로 상호작용하려는 경우 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용해 특정 제한 키가 분당 최대 허용 시도 횟수를 초과했는지 확인할 수 있습니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        return '시도 횟수가 너무 많습니다!';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // 메시지 전송...

또한 `remaining` 메서드를 사용해 지정한 키의 남은 시도 횟수를 확인할 수 있습니다. 남은 시도 횟수가 있다면 `increment` 메서드를 사용해 총 시도 횟수를 증가시킬 수 있습니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
        RateLimiter::increment('send-message:'.$user->id);

        // 메시지 전송...
    }

특정 제한 키의 값을 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 값을 인자로 전달할 수 있습니다:

    RateLimiter::increment('send-message:'.$user->id, amount: 5);

<a name="determining-limiter-availability"></a>
#### 제한기 사용 가능 시간 확인

더 이상 남은 시도 횟수가 없을 때, `availableIn` 메서드는 재시도 가능까지 남은 초를 반환합니다:

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        $seconds = RateLimiter::availableIn('send-message:'.$user->id);

        return '약 '.$seconds.'초 후에 다시 시도할 수 있습니다.';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // 메시지 전송...

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 메서드를 사용하면 특정 제한 키에 대한 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 특정 메시지를 읽었을 때 시도 횟수를 초기화할 수 있습니다:

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