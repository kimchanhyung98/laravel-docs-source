# 기여 안내 (Contribution Guide)

- [버그 보고 (Bug Reports)](#bug-reports)
- [지원 질문 (Support Questions)](#support-questions)
- [코어 개발 토론 (Core Development Discussion)](#core-development-discussion)
- [어떤 브랜치에 기여할까? (Which Branch?)](#which-branch)
- [컴파일된 애셋 (Compiled Assets)](#compiled-assets)
- [보안 취약점 (Security Vulnerabilities)](#security-vulnerabilities)
- [코딩 스타일 (Coding Style)](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령 (Code of Conduct)](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 보고 (Bug Reports)

활발한 협업을 장려하기 위해, Laravel은 단순한 버그 보고뿐만 아니라 풀 리퀘스트(Pull Requests)를 적극 권장합니다. 풀 리퀘스트는 “검토 준비 완료(ready for review)” 상태(“초안(draft)” 상태가 아닌 경우)이고, 새 기능에 대한 테스트가 모두 통과해야만 검토 대상이 됩니다. 몇 일간 “초안(draft)” 상태로 머무는 비활성 풀 리퀘스트는 종료됩니다.

하지만 버그를 보고할 경우, 제목과 문제에 대한 명확한 설명이 포함되어야 합니다. 또한 가능한 많은 관련 정보와 문제를 재현하는 코드 샘플을 첨부해야 합니다. 버그 보고의 목적은 자신과 타인이 문제를 쉽게 재현하고 수정할 수 있도록 돕는 것입니다.

버그 보고는 같은 문제를 가진 사람들이 함께 해결해 나갈 수 있도록 돕기 위해 작성하는 것입니다. 보고했다고 해서 자동으로 활동이 이루어지거나 누군가가 바로 해결할 것이라 기대하지 마십시오. 버그 보고는 문제를 고치는 첫걸음이자 다른 사람이 참여할 수 있는 출발점입니다. 직접 참여하고 싶다면 [Laravel 이슈 트래커](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)에 등록된 버그 수정에 도움을 줄 수도 있습니다. 모든 Laravel 이슈를 보려면 GitHub 인증이 필요합니다.

만약 Laravel 사용 중에 DocBlock, PHPStan 또는 IDE 경고가 부적절하다고 느껴진다면 GitHub 이슈를 생성하지 마시고, 해당 문제를 해결하는 풀 리퀘스트를 제출해 주시기 바랍니다.

Laravel 소스 코드는 GitHub에서 관리되며, 다음은 Laravel 프로젝트별 저장소 목록입니다:

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead) ([Build Scripts](https://github.com/laravel/settler))
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## 지원 질문 (Support Questions)

Laravel의 GitHub 이슈 트래커는 Laravel 도움말이나 지원을 제공하는 용도가 아닙니다. 대신 다음 채널 중 한 곳을 이용해 주세요:

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## 코어 개발 토론 (Core Development Discussion)

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작 개선을 제안할 수 있습니다. 새로운 기능을 제안한다면, 기능 완성을 위해 필요한 코드 중 일부분이라도 구현할 의향이 있어야 합니다.

버그, 새 기능, 기존 기능 구현에 관한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel) 내 `#internals` 채널에서 진행됩니다. Laravel의 메인테이너인 Taylor Otwell은 평일(UTC-06:00 또는 America/Chicago 기준 오전 8시부터 오후 5시) 이 시간대에 채널에 주로 상주하며, 그 외 시간대에도 간간이 접속합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여할까? (Which Branch?)

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재 `12.x`)으로 보내야 합니다. 버그 수정은 곧 출시될 버전에만 존재하는 기능을 고치지 않는 한 `master` 브랜치로 보내서는 안 됩니다.

현재 출시 버전과 완전히 하위 호환되는 **마이너** 기능은 최신 안정화 브랜치(현재 `12.x`)에 보낼 수 있습니다.

중대한 새로운 기능이나 호환에 영향을 주는 변경사항이 있는 기능은 항상 출시 예정 버전을 담고 있는 `master` 브랜치에 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 애셋 (Compiled Assets)

`laravel/laravel` 저장소 내 `resources/css`나 `resources/js`의 대부분 파일처럼 컴파일된 파일에 영향을 주는 변경사항을 제출할 때, 컴파일된 파일은 커밋하지 마십시오. 파일 크기가 크고 검토가 현실적으로 어렵기 때문입니다. 만약 이런 파일을 커밋하면 Laravel에 악성 코드를 주입하는데 이용될 수 있습니다. 이를 방지하기 위해 컴파일된 모든 파일은 Laravel 메인테이너가 직접 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel에서 보안 취약점을 발견하면 Taylor Otwell에게 이메일 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>로 알려주시기 바랍니다. 모든 보안 취약점은 신속하게 대응됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 스타일 가이드와 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 다음에 스페이스 두 칸, 인수 타입, 다시 스페이스 두 칸, 변수명이 순서대로 오는 점에 주의하세요:

```php
/**
 * Register a binding with the container.
 *
 * @param  string|array  $abstract
 * @param  \Closure|string|null  $concrete
 * @param  bool  $shared
 * @return void
 *
 * @throws \Exception
 */
public function bind($abstract, $concrete = null, $shared = false)
{
    // ...
}
```

네이티브 타입이 사용되어 `@param` 또는 `@return` 속성이 중복되는 경우 해당 주석은 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

하지만 네이티브 타입이 제네릭일 경우, `@param` 또는 `@return` 주석으로 구체적인 제네릭 타입을 명시해 주세요:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

<a name="styleci"></a>
### StyleCI

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 자동으로 스타일 수정을 Laravel 저장소에 병합해 줍니다. 덕분에 코드 스타일보다는 기여 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령을 기반으로 합니다. 행동 강령 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 반대 의견에 관대해야 합니다.
- 참여자는 개인 공격이나 경멸적인 발언이 없는 언어와 행동을 해야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의를 전제로 해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>