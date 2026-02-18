# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치에 기여해야 하나?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

Laravel은 활발한 협업을 장려하기 위해 단순한 버그 리포트가 아니라 **풀 리퀘스트**를 적극 권장합니다. 풀 리퀘스트는 "리뷰 요청됨(ready for review)" 상태(드래프트 상태가 아님)여야 하고, 새로운 기능에 대한 모든 테스트가 통과해야만 검토됩니다. "드래프트" 상태로 남아 있는 비활성 풀 리퀘스트는 며칠 후에 닫힐 수 있습니다.

하지만 버그 리포트를 제출할 경우, 제목과 함께 문제가 명확하게 설명되어 있어야 합니다. 또한 가능한 한 많은 관련 정보와, 문제가 재현되는 코드 샘플을 포함해주세요. 버그 리포트의 목적은 당신 또는 다른 개발자가 동일한 버그를 쉽게 재현하고 수정할 수 있도록 하는 데 있습니다.

버그 리포트는 같은 문제를 경험하는 다른 사람이 문제 해결에 함께 참여할 수 있도록 만드는 것이 목적입니다. 버그 리포트가 자동으로 해결되거나, 즉시 다른 사람이 수정해줄 것이라고 기대하지 마세요. 버그 리포트를 생성하는 것은 자신과 다른 사람들이 문제 해결의 첫걸음을 뗄 수 있도록 돕는 과정입니다. 만약 직접 기여하고 싶다면, [문제 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중 작업할 수 있는 것을 고쳐주시는 것도 좋습니다. 모든 Laravel 이슈를 보려면 GitHub에 인증되어 있어야 합니다.

Laravel을 사용하면서 잘못된 DocBlock, PHPStan 또는 IDE 경고를 발견한 경우, GitHub 이슈를 생성하지 말고, 해당 문제를 수정하는 풀 리퀘스트를 보내주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별로 저장소가 마련되어 있습니다:

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Boost](https://github.com/laravel/boost)
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
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit)
- [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit)
- [Laravel Svelte Starter Kit](https://github.com/laravel/svelte-starter-kit)
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 지원 요청이나 질문을 위한 공간이 아닙니다. 도움이나 지원이 필요하다면 아래 채널을 이용해 주세요:

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts 포럼](https://laracasts.com/discuss)
- [Laravel.io 포럼](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## 코어 개발 논의

새로운 기능 제안이나 기존 Laravel 동작 개선 제안이 있다면, Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에 제안할 수 있습니다. 만약 새로운 기능을 제안한다면, 최소한 해당 기능을 완성하는 데 필요한 코드 일부를 직접 작성할 수 있어야 합니다.

버그, 새로운 기능, 기존 기능 구현 등에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지관리자인 Taylor Otwell은 평일(UTC-06:00, America/Chicago 기준) 오전 8시부터 오후 5시까지 해당 채널에서 주로 활동하며, 그 외 시간에도 가끔 접속합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여해야 하나?

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재는 `12.x`) 브랜치로 보내야 합니다. 버그 수정은 **절대로** `master` 브랜치로 보내지 마세요. 단, 다가오는 릴리스에서만 존재하는 기능에 대한 수정인 경우에만 예외입니다.

**완전히 하위 호환**되는 **작은(new minor)** 기능 추가는 최신 안정(stable) 브랜치(현재는 `12.x`)로 보내주시면 됩니다.

**주요(major)** 신규 기능이나 호환성을 깨뜨리는 변경 사항은 항상 차후 릴리스를 준비 중인 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산

`laravel/laravel` 저장소의 대부분 `resources/css` 또는 `resources/js` 파일 등, 컴파일된 파일에 영향을 주는 변경사항을 제출할 경우에는 컴파일된 파일을 커밋하지 마세요. 이 파일들은 용량이 크기 때문에 유지관리자가 실제로 코드를 리뷰하는 것이 현실적으로 불가능합니다. 이 점이 악의적인 코드 삽입 방법으로 악용될 수 있으므로, 방지 차원에서 컴파일된 파일은 항상 Laravel 유지관리자가 직접 생성하여 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

만약 Laravel에서 보안 취약점을 발견한 경우에는 <a href="mailto:taylor@laravel.com">Taylor Otwell</a>에게 이메일로 알려주세요. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 뒤에 공백 두 칸, 인수 타입, 다시 공백 두 칸, 그리고 변수명이 오는 것을 확인할 수 있습니다:

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

메서드에서 이미 네이티브 타입으로 타입을 명시해주었다면, `@param` 또는 `@return` 속성은 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

하지만 네이티브 타입이 제네릭인 경우, `@param` 또는 `@return`을 통해 구체적인 제네릭 타입을 명시해 주세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 Laravel 저장소에 자동으로 스타일 수정을 적용합니다. 이를 통해 기여 내용의 "실질적 내용"에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 루비(Ruby) 커뮤니티의 행동 강령에서 유래되었습니다. 행동 강령 위반 사항은 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 서로 다른 견해를 관용적으로 존중해야 합니다.
- 참가자는 언어나 행동에서 개인을 공격하거나 비방하는 내용을 삼가야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의로 판단해야 합니다.
- 합리적으로 괴롭힘이라 간주될 수 있는 행위는 용인되지 않습니다.

</div>
