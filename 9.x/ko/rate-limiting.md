# Rate Limiting
# 속도 제한

- [Introduction](#introduction)
    - [Cache Configuration](#cache-configuration)
- [Basic Usage](#basic-usage)
    - [Manually Incrementing Attempts](#manually-incrementing-attempts)
    - [Clearing Attempts](#clearing-attempts)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## Introduction
## 소개

Laravel은 [캐시](cache)와 결합하여 일정 시간 동안 특정 작업을 제한할 수 있는 간단한 속도 제한 추상화 기능을 제공합니다.

> **참고**
> 들어오는 HTTP 요청에 대한 속도 제한이 궁금하다면 [속도 제한 미들웨어 문서](routing#rate-limiting)를 참고하세요.

<a name="cache-configuration"></a>
### Cache Configuration
### 캐시 설정

일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일 내의 `default` 키에 정의된 기본 애플리케이션 캐시를 사용합니다. 그러나 속도 제한기가 사용할 캐시 드라이버를 명시하고 싶다면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 지정할 수 있습니다.

    'default' => 'memcached',

    'limiter' => 'redis',

<a name="basic-usage"></a>
## Basic Usage
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 속도 제한기에 접근할 수 있습니다. 속도 제한기가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 지정한 초 동안 지정한 콜백의 실행을 제한합니다.

`attempt` 메서드는 더 이상 남은 시도 횟수가 없을 경우 `false`를 반환하며, 남은 시도 횟수가 있다면 콜백의 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자는 속도 제한 "키"로, 제한하고자 하는 작업을 나타내는 임의의 문자열입니다.

    use Illuminate\Support\Facades\RateLimiter;

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perMinute = 5,
        function() {
            // 메시지 전송...
        }
    );

    if (! $executed) {
      return '메시지가 너무 많이 전송되었습니다!';
    }

<a name="manually-incrementing-attempts"></a>
### Manually Incrementing Attempts
### 시도 횟수 수동 증가

속도 제한기와 수동으로 상호작용하고자 할 경우, 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하면 특정 속도 제한 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        return '시도 횟수가 너무 많습니다!';
    }

또는, `remaining` 메서드를 사용하여 주어진 키의 남은 시도 횟수를 가져올 수 있습니다. 만약 재시도 가능 횟수가 남아있다면, `hit` 메서드로 시도 횟수를 1 증가시킬 수 있습니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
        RateLimiter::hit('send-message:'.$user->id);

        // 메시지 전송...
    }

<a name="determining-limiter-availability"></a>
#### Determining Limiter Availability
#### 속도 제한 사용 가능 시간 확인

더 이상 남은 시도 횟수가 없을 경우, `availableIn` 메서드는 더 많은 시도를 할 수 있을 때까지 남은 초(second)를 반환합니다.

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        $seconds = RateLimiter::availableIn('send-message:'.$user->id);

        return '다시 시도하려면 '.$seconds.'초 후에 가능합니다.';
    }

<a name="clearing-attempts"></a>
### Clearing Attempts
### 시도 횟수 초기화

`clear` 메서드를 사용하면 특정 속도 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 특정 메시지가 수신자에 의해 읽힐 때 시도 횟수를 초기화할 수 있습니다.

    use App\Models\Message;
    use Illuminate\Support\Facades\RateLimiter;

    /**
     * 메시지를 읽음으로 표시합니다.
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
