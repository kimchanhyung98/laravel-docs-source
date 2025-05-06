# 릴리스 노트

- [버전 관리 체계](#versioning-scheme)
    - [예외 사항](#exceptions)
- [지원 정책](#support-policy)
- [Laravel 8](#laravel-8)

<a name="versioning-scheme"></a>
## 버전 관리 체계

Laravel 및 공식 1차 패키지들은 [시맨틱 버전 관리](https://semver.org)를 따릅니다. 프레임워크의 주요(메이저) 릴리스는 매년(~2월)에 공개되며, 마이너 및 패치 릴리스는 매주 단위로 배포될 수 있습니다. 마이너 및 패치 릴리스는 **절대** 호환성을 깨뜨리는 변경사항을 포함하지 않아야 합니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 컴포넌트를 참조할 때는 항상 `^8.0`과 같은 버전 제약 조건을 사용해야 합니다. 왜냐하면, Laravel의 메이저 릴리스에는 호환성이 깨지는 변경이 포함될 수 있기 때문입니다. 하지만 최대한 하루 이내로 새로운 메이저 릴리스로 업데이트할 수 있도록 노력하고 있습니다.

<a name="exceptions"></a>
### 예외 사항

<a name="named-arguments"></a>
#### 명명된 인자

현재 PHP의 [명명된 인자](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) 기능은 Laravel의 하위 호환성 가이드라인에 포함되어 있지 않습니다. 필요에 따라 Laravel 코드베이스 개선을 위해 함수 인자명을 변경할 수 있으므로, Laravel 메서드를 호출할 때 명명된 인자를 사용하는 경우 인자명이 향후 변경될 가능성을 염두에 두어, 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 Laravel 릴리스에 대해 버그 수정은 18개월, 보안 패치는 2년간 제공됩니다. Lumen을 포함한 추가 라이브러리의 경우 최신 메이저 릴리스만 버그 수정이 제공됩니다. 또한, Laravel에서 지원하는 데이터베이스 버전을 [여기](/docs/{{version}}/database#introduction)에서 확인해 주세요.

| 버전 | PHP (*) | 릴리스 | 버그 수정 종료일 | 보안 패치 종료일 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | 2019년 9월 3일 | 2022년 1월 25일 | 2022년 9월 6일 |
| 7 | 7.2 - 8.0 | 2020년 3월 3일 | 2020년 10월 6일 | 2021년 3월 3일 |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.1 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 패치만 제공</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-8"></a>
## Laravel 8

Laravel 8은 Laravel 7.x에서 진행된 개선 사항을 이어받아, Laravel Jetstream, 모델 팩토리 클래스, 마이그레이션 스쿼시, 잡 배칭, 향상된 요청 속도 제한, 큐 개선, 동적 Blade 컴포넌트, Tailwind 페이지네이션 뷰, 시간 테스트 도우미, `artisan serve` 개선, 이벤트 리스너 개선 등 다양한 버그 및 사용성 개편이 이루어졌습니다.

<a name="laravel-jetstream"></a>
### Laravel Jetstream

_Laravel Jetstream은 [Taylor Otwell](https://github.com/taylorotwell)에 의해 작성되었습니다._

[Laravel Jetstream](https://jetstream.laravel.com)은 아름답게 디자인된 Laravel 전용 애플리케이션 스캐폴딩입니다. Jetstream은 다음 프로젝트의 완벽한 시작점을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum 기반 API 지원, 선택적 팀 관리 등 다양한 기능을 포함합니다. Jetstream은 이전 Laravel 버전의 인증 UI 스캐폴딩을 대체하며 개선합니다.

Jetstream은 [Tailwind CSS](https://tailwindcss.com)를 사용하여 디자인되었으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia](https://inertiajs.com) 기반의 스캐폴딩을 선택할 수 있습니다.

<a name="models-directory"></a>
### Models 디렉토리

커뮤니티의 강한 요구에 따라, 기본 Laravel 애플리케이션 스켈레톤에 `app/Models` 디렉토리가 추가되었습니다. 이제 Eloquent 모델의 새로운 보금자리를 활용해보세요! 만약 디렉토리가 존재하면, 모든 관련 생성기 명령어들이 모델을 `app/Models` 디렉토리에 생성하도록 기본으로 업데이트되었습니다. 디렉토리가 없다면 프레임워크는 모델을 `app` 디렉토리에 생성합니다.

<a name="model-factory-classes"></a>
### 모델 팩토리 클래스

_모델 팩토리 클래스는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Eloquent의 [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)가 클래스 기반으로 새롭게 개편되었고, 관계 지원이 1급 시민으로 강화되었습니다. 예를 들어, Laravel 내장 `UserFactory`는 다음과 같이 작성됩니다:

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 팩토리가 다루는 모델의 이름
     *
     * @var string
     */
    protected $model = User::class;

    /**
     * 모델의 기본 상태 정의
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

생성된 모델에 기본적으로 포함된 `HasFactory` 트레이트 덕분에, 다음과 같이 팩토리를 간단히 사용할 수 있습니다:

```php
use App\Models\User;

User::factory()->count(50)->create();
```

이제 모델 팩토리는 PHP 클래스이므로 상태 변환을 클래스 메서드로 작성할 수 있고, 필요에 따라 도우미 메서드를 자유롭게 추가할 수 있습니다.

예를 들어, `User` 모델에 기본 속성을 수정하는 `suspended` 상태가 있을 수 있습니다. 상태 변환은 팩토리의 `state` 메서드로 만들며, 메서드 명칭도 자유롭게 지정할 수 있습니다. 당연히 일반적인 PHP 메서드일 뿐입니다:

```php
/**
 * 사용자가 정지된 상태임을 표시
 *
 * @return \Illuminate\Database\Eloquent\Factories.Factory
 */
public function suspended()
{
    return $this->state([
        'account_status' => 'suspended',
    ]);
}
```

상태 변환 메서드 정의 후 다음처럼 사용할 수 있습니다:

```php
use App\Models\User;

User::factory()->count(5)->suspended()->create();
```

언급했듯, Laravel 8 팩토리는 관계 지원이 내장되어 있습니다. 예를 들어, `User` 모델에 `posts` 관계가 있다면, 3개의 게시글을 가진 사용자를 다음과 같이 생성할 수 있습니다:

```php
$users = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

업그레이드 과정을 돕기 위해 [laravel/legacy-factories](https://github.com/laravel/legacy-factories) 패키지가 배포되어, Laravel 8.x에서도 이전 팩토리를 사용할 수 있습니다.

개선된 팩토리는 그 외에도 매력적인 기능들을 많이 제공합니다. 모델 팩토리에 대한 자세한 내용은 [데이터베이스 테스트 문서](/docs/{{version}}/database-testing#defining-model-factories)를 참고하세요.

<a name="migration-squashing"></a>
### 마이그레이션 스쿼시

_마이그레이션 스쿼시는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

애플리케이션을 개발하며 시간이 지남에 따라 마이그레이션이 늘어나 디렉토리가 수백 건의 파일로 넘쳐날 수 있습니다. MySQL이나 PostgreSQL을 사용한다면 이제 마이그레이션을 하나의 SQL 파일로 "스쿼시(압축)"할 수 있습니다. 다음과 같이 `schema:dump` 명령어를 실행하면 됩니다:

```
php artisan schema:dump

// 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션 삭제...
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel이 `database/schema` 디렉토리에 "스키마" 파일을 작성합니다. 이제 데이터베이스 마이그레이션 시 다른 마이그레이션이 실행된 적이 없다면, 가장 먼저 스키마 파일의 SQL이 실행되고 이후 남아 있는 마이그레이션이 실행됩니다.

<a name="job-batching"></a>
### 잡 배칭

_잡 배칭은 [Taylor Otwell](https://github.com/taylorotwell) & [Mohamed Said](https://github.com/themsaid)이 기여했습니다._

Laravel의 잡 배칭 기능을 이용하면 여러 개의 잡을 한번에 실행한 뒤, 전체가 완료되면 후속 작업을 실행할 수 있습니다.

`Bus` 파사드의 새로운 `batch` 메서드로 무더기 잡을 디스패치할 수 있고, `then`, `catch`, `finally` 메서드로 배치 완료 시 콜백을 지정할 수 있습니다. 각각의 콜백은 호출 시 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다.

```php
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
    // 모든 잡이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 잡 실패 발생...
})->finally(function (Batch $batch) {
    // 배치 실행 종료...
})->dispatch();

return $batch->id;
```

잡 배칭에 대한 더 자세한 내용은 [큐 문서](/docs/{{version}}/queues#job-batching)를 참고하세요.

<a name="improved-rate-limiting"></a>
### 향상된 요청 속도 제한

_요청 속도 제한 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

Laravel의 요청 속도 제한(레이트 리미터) 기능이 더 유연하고 강력해졌으며, 기존 `throttle` 미들웨어 API와의 하위 호환성도 유지됩니다.

속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. 이는 속도 제한 이름과 해당 제한을 반환하는 클로저를 인자로 받습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000);
});
```

콜백은 요청 인스턴스를 받으므로, 요청/사용자에 따라 동적으로 제한 값을 조정할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

IP별로 할당량을 나누는 것도 가능합니다. 예를 들어, 각 IP별로 분당 100회를 허용하려면 다음과 같이 할 수 있습니다:

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

속도 제한기는 `throttle` [미들웨어](/docs/{{version}}/middleware)로 라우트나 그룹에 지정할 수 있습니다:

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

속도 제한에 대한 자세한 내용은 [라우팅 문서](/docs/{{version}}/routing#rate-limiting)를 참고하세요.

<a name="improved-maintenance-mode"></a>
### 유지보수 모드 개선

_유지보수 모드 개선은 [Taylor Otwell](https://github.com/taylorotwell)이, [Spatie](https://spatie.be)에서 영감을 얻어 기여하였습니다._

예전 Laravel에서는 `php artisan down` 유지보수 모드를 "허용 IP 목록" 방식으로 우회할 수 있었습니다. 이제는 더 간단한 "시크릿" 또는 토큰 기반 접근으로 변경되었습니다.

유지보수 모드에서 `secret` 옵션을 사용해 토큰을 지정할 수 있습니다:

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

이제 해당 토큰이 포함된 URL에 접속하면, Laravel은 브라우저에 유지보수 모드 우회 쿠키를 발급합니다:

```
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

해당 히든 라우트에 접근하면 `/` 경로로 리디렉션되며, 쿠키가 발급된 후에는 일반적인 환경처럼 애플리케이션을 사용할 수 있습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 사전 렌더링

배포 과정에서 `php artisan down`을 사용할 경우, Composer 의존성이나 인프라 컴포넌트가 업데이트되는 도중에 사용자가 오류를 겪을 수 있습니다. 이는 유지보수 모드 진입과 뷰 렌더링에 Laravel이 상당 부분 로딩되기 때문입니다.

이제 Laravel은 요청 사이클 초기에 반환되는 유지보수 화면을 미리 렌더링할 수 있습니다(애플리케이션 의존성 로딩 전). `down` 명령의 `render` 옵션으로 원하는 템플릿을 미리 렌더할 수 있습니다:

```
php artisan down --render="errors::503"
```

<a name="closure-dispatch-chain-catch"></a>
### 클로저 디스패치/체인 `catch`

_`catch` 개선은 [Mohamed Said](https://github.com/themsaid)가 기여했습니다._

이제 새롭게 추가된 `catch` 메서드로, 큐에 들어간 클로저가 모든 재시도에도 실패했을 때 실행될 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡이 실패함...
});
```

<a name="dynamic-blade-components"></a>
### 동적 Blade 컴포넌트

_동적 Blade 컴포넌트는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

런타임에 렌더링할 컴포넌트가 결정되도록 할 때는, Laravel 내장 `dynamic-component`를 사용할 수 있습니다:

```html
<x-dynamic-component :component="$componentName" class="mt-4" />
```

Blade 컴포넌트에 대해 더 알고 싶다면, [Blade 문서](/docs/{{version}}/blade#components)를 참고하세요.

<a name="event-listener-improvements"></a>
### 이벤트 리스너 개선

_이벤트 리스너 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

클로저 기반 이벤트 리스너를 한층 단순하게, 클로저만 `Event::listen`에 전달하여 등록할 수 있습니다. Laravel은 클로저의 유형 힌트를 통해 어떤 이벤트를 처리하는지 판단합니다.

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

Event::listen(function (PodcastProcessed $event) {
    //
});
```

또한, 클로저 리스너를 `Illuminate\Events\queueable` 함수를 이용해 큐 처리로 등록할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
}));
```

큐 작업과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 리스너 실행을 맞춤 제어할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너 실패 처리를 원한다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 지정하세요:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너 실패...
}));
```

<a name="time-testing-helpers"></a>
### 시간 테스트 도우미

_시간 테스트 도우미는 [Taylor Otwell](https://github.com/taylorotwell)이 Ruby on Rails에서 영감을 받아 기여했습니다._

테스트 중에는, `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 변경해야 할 경우가 가끔 있습니다. Laravel의 기본 Feature 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼를 제공합니다.

```php
public function testTimeCanBeManipulated()
{
    // 미래로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 이동...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재로 복귀...
    $this->travelBack();
}
```

<a name="artisan-serve-improvements"></a>
### Artisan `serve` 개선

_Artisan `serve` 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

이제 Artisan `serve` 명령은 `.env` 파일에 있는 환경 변수 변경 사항을 자동 감지해, 수동으로 껐다 켜지 않아도 자동 재시작되도록 개선되었습니다.

<a name="tailwind-pagination-views"></a>
### Tailwind 페이지네이션 뷰

Laravel 페이지네이터가 기본적으로 [Tailwind CSS](https://tailwindcss.com) 프레임워크를 사용하도록 변경되었습니다. Tailwind CSS는 모든 구성 요소를 자유롭게 커스터마이즈 가능한 저수준 CSS 프레임워크로, 강제되는 스타일 대신 맞춤형 디자인을 만들 수 있게 해줍니다. 물론 Bootstrap 3, 4의 뷰도 계속 사용할 수 있습니다.

<a name="routing-namespace-updates"></a>
### 라우팅 네임스페이스 업데이트

예전 Laravel에서는 `RouteServiceProvider`의 `$namespace` 프로퍼티에 값이 들어가면, 컨트롤러 라우트 정의 및 `action` 헬퍼 / `URL::action` 메서드 호출에 자동으로 네임스페이스가 접두사로 붙었습니다. Laravel 8.x부터는 해당 프로퍼티의 기본값이 `null`이 되었습니다. 즉, 이제 자동 네임스페이스 접두사가 적용되지 않습니다. 따라서 새 앱에서는 아래처럼 표준 PHP 콜러블 구문으로 라우트를 작성해야 합니다:

```php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

`action` 관련 메서드 호출도 마찬가지로 사용합니다:

```php
action([UserController::class, 'index']);

return Redirect::action([UserController::class, 'index']);
```

Laravel 7.x 방식의 컨트롤러 네임스페이스 접두사가 필요하다면, `RouteServiceProvider`에 `$namespace` 프로퍼티를 추가하세요.

> {note} 이 변경은 새로운 Laravel 8.x 애플리케이션에만 적용됩니다. 7.x에서 업그레이드한 앱이라면 기존대로 `RouteServiceProvider`에 `$namespace`가 남아있을 것입니다.