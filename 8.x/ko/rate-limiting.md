# 속도 제한(Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션의 [캐시](cache)와 결합하여 지정된 시간 동안의 모든 동작을 쉽게 제한할 수 있는 간단한 속도 제한 추상화를 제공합니다.

> {tip} 들어오는 HTTP 요청에 대한 속도 제한에 관심이 있다면, [속도 제한 미들웨어 문서](routing#rate-limiting)를 참고하세요.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내 `default` 키에 정의된 기본 애플리케이션 캐시를 사용합니다. 다만, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 지정할 수도 있습니다.

    'default' => 'memcached',

    'limiter' => 'redis',

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 속도 제한기에 접근할 수 있습니다. 속도 제한기가 제공하는 가장 간단한 메서드는 `attempt`로, 지정된 시간(초) 동안 콜백의 실행을 제한합니다.

`attempt` 메서드는 더 이상 남은 시도 횟수가 없을 때 `false`를 반환합니다. 그렇지 않으면 콜백의 반환값 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자는 속도 제한 "키"로, 제한할 동작을 대표하는 임의의 문자열을 사용할 수 있습니다.

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

<a name="manually-incrementing-attempts"></a>
### 시도 횟수 수동 증가

속도 제한기에 수동으로 접근하고 싶다면, 다양한 메서드를 사용할 수 있습니다. 예를 들어 `tooManyAttempts` 메서드를 호출하여, 특정 속도 제한 키가 분당 허용 최대 시도 횟수를 초과했는지 확인할 수 있습니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        return '시도 횟수가 너무 많습니다!';
    }

또는 `remaining` 메서드를 사용해 특정 키에 남은 시도 횟수를 가져올 수도 있습니다. 남은 시도 횟수가 있다면 `hit` 메서드를 사용해 시도 횟수를 1 증가시킬 수 있습니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
        RateLimiter::hit('send-message:'.$user->id);

        // 메시지 전송...
    }

<a name="determining-limiter-availability"></a>
#### 제한 가능 시간 확인

키의 시도 횟수가 더 이상 남아있지 않은 경우, `availableIn` 메서드는 다음 시도가 가능해질 때까지 남은 초(초 단위 시간)를 반환합니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        $seconds = RateLimiter::availableIn('send-message:'.$user->id);

        return '약 '.$seconds.'초 후에 다시 시도할 수 있습니다.';
    }

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 메서드를 사용하여 특정 속도 제한 키에 대한 시도 횟수를 초기화할 수 있습니다. 예를 들어, 수신자가 메시지를 읽었을 때 시도 횟수를 초기화할 수 있습니다.

    use App\Models\Message;
    use Illuminate\Support\Facades\RateLimiter;

    /**
     * 메시지를 읽음 처리합니다.
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
