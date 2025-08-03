# 릴리즈 노트 (Release Notes)

- [버전 관리 정책](#versioning-scheme)
    - [예외 사항](#exceptions)
- [지원 정책](#support-policy)
- [Laravel 8](#laravel-8)

<a name="versioning-scheme"></a>
## 버전 관리 정책 (Versioning Scheme)

Laravel과 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 메이저 프레임워크 릴리즈는 매년 (대략 2월경) 제공되며, 마이너 및 패치 릴리즈는 매주 있을 수도 있습니다. 마이너 및 패치 릴리즈에는 **절대** 파괴적 변경이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 혹은 구성요소를 참조할 때는 항상 `^8.0` 과 같은 버전 제약 조건을 사용해야 하며, 메이저 릴리즈에서는 파괴적 변경이 발생할 수 있음을 염두에 두어야 합니다. 그러나 저희는 신규 메이저 릴리즈로의 업데이트를 하루 이내에 가능한 한 원활하게 할 수 있도록 노력하고 있습니다.

<a name="exceptions"></a>
### 예외 사항 (Exceptions)

<a name="named-arguments"></a>
#### 네임드 아규먼트 (Named Arguments)

현재 PHP의 [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) 기능은 Laravel의 하위 호환성 가이드라인에 포함되어 있지 않습니다. Laravel 코드베이스 개선을 위해 필요에 따라 함수 매개변수 이름이 변경될 수 있기 때문에, Laravel 메서드를 호출할 때 네임드 아규먼트를 사용할 경우 신중해야 하며 향후 파라미터 이름이 변경될 수 있음을 인지하고 있어야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈는 버그 수정이 18개월 동안 지원되며, 보안 수정은 2년 동안 제공됩니다. Lumen을 포함한 기타 라이브러리들은 최신 메이저 릴리즈에 대해서만 버그 수정을 받습니다. 또한, Laravel에서 지원하는 데이터베이스 버전에 대해서는 [데이터베이스 문서](/docs/{{version}}/database#introduction)을 참고하시기 바랍니다.

| 버전 | PHP (*) | 출시일 | 버그 수정 지원 종료 | 보안 수정 지원 종료 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | 2019년 9월 3일 | 2022년 1월 25일 | 2022년 9월 6일 |
| 7 | 7.2 - 8.0 | 2020년 3월 3일 | 2020년 10월 6일 | 2021년 3월 3일 |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.1 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 수정만 지원</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-8"></a>
## Laravel 8

Laravel 8은 Laravel 7.x 버전에서의 개선 사항을 이어받아 Laravel Jetstream, 모델 팩토리 클래스, 마이그레이션 스쿼싱, 작업 배칭, 향상된 속도 제한(rate limiting), 큐 개선, 동적 Blade 컴포넌트, Tailwind 페이징 뷰, 시간 테스트 헬퍼, artisan serve 개선, 이벤트 리스너 향상 및 다양한 버그 수정과 편의성을 개선했습니다.

<a name="laravel-jetstream"></a>
### Laravel Jetstream

_Laravel Jetstream은 [Taylor Otwell](https://github.com/taylorotwell)이 작성했습니다._

[Laravel Jetstream](https://jetstream.laravel.com)은 Laravel을 위한 세련된 애플리케이션 스캐폴딩입니다. Jetstream은 다음 프로젝트를 위한 완벽한 시작점을 제공하며 로그인, 회원가입, 이메일 인증, 이중 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적 팀 관리 기능을 포함합니다. Laravel Jetstream은 이전 버전의 Laravel에서 제공하던 레거시 인증 UI 스캐폴딩을 대체하고 개선했습니다.

Jetstream은 [Tailwind CSS](https://tailwindcss.com)를 사용하여 디자인되었으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia](https://inertiajs.com) 중 선택하여 스캐폴딩할 수 있습니다.

<a name="models-directory"></a>
### 모델 디렉토리

커뮤니티의 압도적인 요청에 따라, 기본 Laravel 애플리케이션 골격에 이제 `app/Models` 디렉토리가 포함됩니다. 이 새 디렉토리가 Eloquent 모델의 기본 위치가 되기를 바랍니다! 관련되는 모든 생성기(generator) 명령어는 `app/Models` 디렉토리가 존재할 경우 해당 위치에 모델이 있다고 가정하도록 업데이트되었습니다. 만약 디렉토리가 없다면, 프레임워크는 모델이 `app` 디렉토리에 있다고 가정합니다.

<a name="model-factory-classes"></a>
### 모델 팩토리 클래스

_모델 팩토리 클래스는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Eloquent [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)가 클래스 기반 팩토리로 완전히 다시 작성되어 관계(relationship)를 1급 객체 수준으로 지원할 수 있게 개선되었습니다. 예를 들어, Laravel 기본 제공 UserFactory는 다음과 같이 작성됩니다:

```
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 팩토리와 연결된 모델 이름.
     *
     * @var string
     */
    protected $model = User::class;

    /**
     * 모델의 기본 상태 정의.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

생성된 모델에서 사용할 수 있는 `HasFactory` 트레이트 덕분에 모델 팩토리는 아래와 같이 사용 가능합니다:

```
use App\Models\User;

User::factory()->count(50)->create();
```

모델 팩토리가 이제는 PHP 클래스이므로, 상태 변환(state transformations)은 클래스 메서드로 작성할 수 있습니다. 또한, 필요에 따라 Eloquent 모델 팩토리에 다른 헬퍼 클래스도 추가할 수 있습니다.

예를 들어, `User` 모델에 기본 속성 값을 변경하는 `suspended` 상태가 있다고 가정합시다. 이 상태 변환은 기본 팩토리의 `state` 메서드를 사용해 정의할 수 있으며, 메서드 이름은 자유롭게 지정 가능합니다. 이는 단순한 PHP 메서드일 뿐입니다:

```
/**
 * 사용자가 정지(suspended) 상태임을 표시.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
public function suspended()
{
    return $this->state([
        'account_status' => 'suspended',
    ]);
}
```

상태 변환 메서드를 정의한 후에는 다음처럼 사용할 수 있습니다:

```
use App\Models\User;

User::factory()->count(5)->suspended()->create();
```

또한, Laravel 8의 모델 팩토리는 관계를 1급 객체로 지원합니다. 따라서 `User` 모델에 `posts` 관계 메서드가 있다면, 다음과 같이 세 개의 게시물을 가진 사용자를 생성할 수 있습니다:

```
$users = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

업그레이드를 편리하게 하기 위해, 이전 모델 팩토리 방식을 Laravel 8.x에서 지원하는 [laravel/legacy-factories](https://github.com/laravel/legacy-factories) 패키지가 출시되었습니다.

Laravel이 다시 작성한 팩토리는 더 많은 훌륭한 기능을 포함하고 있습니다. 모델 팩토리에 대해 더 배우고 싶다면 [데이터베이스 테스트 문서](/docs/{{version}}/database-testing#defining-model-factories)를 참고하세요.

<a name="migration-squashing"></a>
### 마이그레이션 스쿼싱 (Migration Squashing)

_마이그레이션 스쿼싱은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

애플리케이션 개발과정에서 시간이 지남에 따라 많은 마이그레이션이 누적되면, 마이그레이션 디렉토리가 수백 개의 마이그레이션으로 비대해질 수 있습니다. MySQL 또는 PostgreSQL을 사용한다면 이제 마이그레이션을 하나의 SQL 파일로 "스쿼싱" 할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```
php artisan schema:dump

// 현재 데이터베이스 스키마 덤프 및 기존 모든 마이그레이션 제거...
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel은 `database/schema` 디렉토리에 "스키마" 파일을 기록합니다. 이후 마이그레이션을 실행할 때, 아직 실행하지 않은 마이그레이션이 없으면 Laravel이 우선 스키마 파일의 SQL을 실행하고, 그 뒤에 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 순차적으로 실행합니다.

<a name="job-batching"></a>
### 작업 배칭 (Job Batching)

_작업 배칭 기능은 [Taylor Otwell](https://github.com/taylorotwell)과 [Mohamed Said](https://github.com/themsaid)가 기여했습니다._

Laravel의 작업 배칭 기능을 사용하면 여러 작업들을 묶어 쉽게 실행하고, 이 배치 작업이 모두 완료된 후 특정 작업을 수행할 수 있습니다.

`Bus` 파사드의 새로운 `batch` 메서드를 사용해 작업 묶음을 디스패치할 수 있습니다. 물론, 배칭은 주로 완료 콜백과 함께 사용되므로 `then`, `catch`, `finally` 메서드를 사용하여 배치 완료 시 콜백을 정의할 수 있습니다. 이 콜백들은 호출 시 `Illuminate\Bus\Batch` 인스턴스를 인수로 받습니다:

```
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ProcessPodcast(Podcast::find(1)),
    new ProcessPodcast(Podcast::find(2)),
    new ProcessPodcast(Podcast::find(3)),
    new ProcessPodcast(Podcast::find(4)),
    new ProcessPodcast(Podcast::find(5)),
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 작업 실패 감지...
})->finally(function (Batch $batch) {
    // 배치 작업 실행 완료...
})->dispatch();

return $batch->id;
```

작업 배칭에 대해 더 알고 싶다면 [큐 문서](/docs/{{version}}/queues#job-batching)를 참고하세요.

<a name="improved-rate-limiting"></a>
### 향상된 속도 제한 (Improved Rate Limiting)

_속도 제한 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Laravel의 요청 속도 제한(rate limiter) 기능이 더 유연하고 강력하게 향상되었으며, 동시 출시된 이전 버전의 `throttle` 미들웨어 API와 동일하게 하위 호환성을 유지합니다.

속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. 이 메서드는 속도 제한기 이름과, 해당 제한기를 할당받은 라우트가 적용받을 제한 구성을 반환하는 클로저를 인수로 받습니다:

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000);
});
```

속도 제한기 콜백은 요청 객체를 받으므로, 인증된 사용자 등의 요청 상황에 따라 동적으로 제한 정책을 빌드할 수 있습니다:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

종종 임의 값으로 제한을 분리하고 싶을 때도 있습니다. 예를 들어, IP 주소별로 분리하여 라우트 접근을 분당 100회로 제한할 수 있습니다. 이 경우 제한 빌드 시 `by` 메서드를 사용하세요:

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

속도 제한기는 `throttle` [미들웨어](/docs/{{version}}/middleware)를 통해 라우트 혹은 라우트 그룹에 연결할 수 있습니다. `throttle` 미들웨어는 제한기를 지정할 때 이름을 인수로 받습니다:

```
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

속도 제한에 대해 더 알고 싶다면 [라우팅 문서](/docs/{{version}}/routing#rate-limiting)를 확인하세요.

<a name="improved-maintenance-mode"></a>
### 향상된 유지보수 모드 (Improved Maintenance Mode)

_유지보수 모드 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 [Spatie](https://spatie.be)의 영감을 받아 기여했습니다._

이전 Laravel 버전에서 `php artisan down` 유지보수 모드는 IP 주소별 허용 목록을 통해 우회가 가능했습니다. 이 기능은 더 간단한 "비밀" 토큰 방식으로 대체되었습니다.

유지보수 모드 중에는 `secret` 옵션으로 우회 토큰을 지정할 수 있습니다:

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 진입 후, 위 토큰과 일치하는 URL에 접속하면 Laravel이 우회 쿠키를 브라우저에 발행합니다:

```
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

이 숨겨진 경로에 접속하면 애플리케이션의 `/` 라우트로 리다이렉트되며, 쿠키가 브라우저에 설정된 뒤에는 유지보수 모드가 아닌 것처럼 애플리케이션을 정상적으로 탐색할 수 있습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 미리 렌더링하기

배포 시 `php artisan down` 명령을 사용할 경우, 컴포저 의존성 업데이트 등 인프라스트럭처 컴포넌트가 업데이트되는 동안 사용자가 애플리케이션에 접근하면 가끔 오류가 발생할 수 있습니다. 이는 Laravel 프레임워크의 상당 부분이 부트스트랩되어야 유지보수 모드임을 확인하고 템플릿엔진으로 유지보수 모드 뷰를 렌더링하기 때문입니다.

이 문제를 해결하기 위해 Laravel은 요청 주기 초반에 반환될 유지보수 모드 뷰를 미리 렌더링하는 기능을 제공합니다. 이 뷰는 애플리케이션 의존성이 하나도 로드되기 전에 렌더링됩니다. `down` 명령어의 `render` 옵션을 사용해 원하는 템플릿을 미리 렌더링할 수 있습니다:

```
php artisan down --render="errors::503"
```

<a name="closure-dispatch-chain-catch"></a>
### 클로저 디스패치 / 체인 `catch`

_Catch 기능은 [Mohamed Said](https://github.com/themsaid)가 기여했습니다._

새로운 `catch` 메서드를 이용하면, 큐에 보낸 클로저형 작업이 큐에 설정한 재시도 횟수를 모두 소진하고도 실패했을 때 실행할 클로저를 제공할 수 있습니다:

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업이 실패했습니다...
});
```

<a name="dynamic-blade-components"></a>
### 동적 Blade 컴포넌트

_동적 Blade 컴포넌트는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

때때로 어떤 컴포넌트를 렌더링할지 런타임까지 알 수 없는 경우가 있습니다. 이런 경우, Laravel 내장 `dynamic-component` 컴포넌트를 사용해 런타임 변수나 값에 따라 컴포넌트를 렌더링할 수 있습니다:

```
<x-dynamic-component :component="$componentName" class="mt-4" />
```

Blade 컴포넌트에 대해 더 알고 싶다면 [Blade 문서](/docs/{{version}}/blade#components)를 참고하세요.

<a name="event-listener-improvements"></a>
### 이벤트 리스너 개선

_이벤트 리스너 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

클로저 기반 이벤트 리스너는 이제 클로저만 `Event::listen` 메서드에 전달해 등록할 수 있습니다. Laravel이 클로저를 분석해 어떤 이벤트 타입을 처리하는지 판단합니다:

```
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

Event::listen(function (PodcastProcessed $event) {
    //
});
```

또한, 클로저 기반 이벤트 리스너를 `Illuminate\Events\queueable` 함수를 사용해 큐 처리 가능하게 표시할 수 있습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
}));
```

큐 처리되는 작업과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐된 리스너 실행을 커스터마이징할 수 있습니다:

```
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너 실패를 처리하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 제공할 수 있습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 처리 리스너가 실패했습니다...
}));
```

<a name="time-testing-helpers"></a>
### 시간 테스트 헬퍼

_시간 테스트 헬퍼는 [Taylor Otwell](https://github.com/taylorotwell)이 Ruby on Rails에서 영감을 받아 기여했습니다._

테스트할 때, `now`나 `Illuminate\Support\Carbon::now()` 같은 헬퍼가 반환하는 현재 시간을 가끔 조작할 필요가 있습니다. Laravel 기본 테스트 클래스에 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

```
public function testTimeCanBeManipulated()
{
    // 미래로 시간 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 시간 이동...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시점으로 돌아오기...
    $this->travelBack();
}
```

<a name="artisan-serve-improvements"></a>
### Artisan `serve` 개선

_Artisan `serve` 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Artisan `serve` 명령이 환경변수 `.env` 파일 내부 변경 시 자동으로 재시작되도록 개선되었습니다. 이전에는 이 명령을 수동으로 중지 후 재시작해야만 변경 사항을 반영할 수 있었습니다.

<a name="tailwind-pagination-views"></a>
### Tailwind 페이징 뷰

Laravel 페이징 기능이 기본적으로 [Tailwind CSS](https://tailwindcss.com) 프레임워크를 사용하도록 업데이트되었습니다. Tailwind CSS는 사용자 맞춤형 디자인을 만들 수 있도록 기본 빌딩 블록을 제공하는 매우 유연한 로우레벨(low-level) CSS 프레임워크입니다. 물론, Bootstrap 3 및 4 뷰도 계속 사용할 수 있습니다.

<a name="routing-namespace-updates"></a>
### 라우팅 네임스페이스 업데이트

이전 Laravel 버전에서는 `RouteServiceProvider`에 `$namespace` 속성이 있었습니다. 이 변수는 컨트롤러 라우트 정의 및 `action` 헬퍼 혹은 `URL::action` 메서드 호출 시 자동으로 네임스페이스를 접두사로 추가했습니다. Laravel 8.x에서는 이 속성 값이 기본적으로 `null`이며, 따라서 자동 네임스페이스 접두사가 적용되지 않습니다. 새로 생성된 Laravel 8.x 애플리케이션에서 컨트롤러 라우트 정의는 일반 PHP 콜러블(callable) 구문으로 작성해야 합니다:

```
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

`action` 관련 호출도 동일한 콜러블 구문을 사용해야 합니다:

```
action([UserController::class, 'index']);

return Redirect::action([UserController::class, 'index']);
```

Laravel 7.x 스타일의 컨트롤러 라우트 네임스페이스 접두사가 필요하다면, 애플리케이션 `RouteServiceProvider`에 `$namespace` 속성을 다시 추가하면 됩니다.

> [!NOTE]
> 이 변경 사항은 신규 Laravel 8.x 애플리케이션에만 적용됩니다. Laravel 7.x에서 업그레이드하는 애플리케이션에는 여전히 `$namespace` 속성이 `RouteServiceProvider`에 남아 있습니다.