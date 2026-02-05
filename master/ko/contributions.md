# 기여 가이드 (Contribution Guide)

- [버그 보고](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어느 브랜치에 기여해야 하나?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 보고

Laravel은 적극적인 협업을 장려하기 위해 단순한 버그 보고 뿐만 아니라, 풀 리퀘스트 제출을 강력히 권장합니다. 풀 리퀘스트는 반드시 "ready for review"(검토 준비 완료) 상태로 표시되어야 하며("draft" 상태가 아님), 새로운 기능의 모든 테스트가 통과해야만 검토가 이루어집니다. 몇 일간 "draft" 상태로 남아있는 비활성 풀 리퀘스트는 자동으로 닫힐 수 있습니다.

버그 리포트를 작성하는 경우, 이슈에는 제목과 명확한 문제 설명이 반드시 포함되어야 합니다. 또한, 가능한 한 많은 관련 정보와 해당 문제를 재현할 수 있는 코드 예제를 첨부해야 합니다. 버그 리포트의 목적은 본인과 다른 사람들이 문제를 쉽게 재현하고 해결 방안을 마련할 수 있도록 돕는 것입니다.

버그 리포트는 같은 문제를 겪는 다른 개발자와 협력하여 문제를 해결하기 위한 출발점입니다. 버그 리포트를 제출했다고 해서 자동으로 누군가가 즉시 이를 해결하거나, 바로 처리된다고 기대해서는 안 됩니다. 버그 리포트는 문제 해결의 첫 걸음을 내딛는 과정입니다. 여러분이 기여하고 싶다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 해결하는 데 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인해야 합니다.

Laravel 사용 중 잘못된 DocBlock, PHPStan 또는 IDE 경고를 발견했다면, GitHub 이슈를 생성하지 말고 직접 해당 문제를 수정하는 풀 리퀘스트를 제출해 주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트마다 별도의 저장소가 존재합니다:

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
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 Laravel 사용 및 지원 관련 문의를 위한 곳이 아닙니다. 대신 아래의 채널을 이용해 주세요:

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
## 코어 개발 논의

새로운 기능 제안이나 기존 Laravel 동작의 개선 아이디어가 있다면, Laravel framework 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)를 이용해 제안할 수 있습니다. 새로운 기능을 제안할 때는, 기능 완성을 위한 코드의 일부라도 구현할 의지를 가져야 합니다.

버그, 새로운 기능 및 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 진행됩니다. Laravel의 관리자인 Taylor Otwell은 미국 중부 표준시(UTC-06:00 또는 America/Chicago) 기준 평일 오전 8시부터 오후 5시 사이에 주로 접속하며, 다른 시간대에도 가끔 참여합니다.

<a name="which-branch"></a>
## 어느 브랜치에 기여해야 하나?

**모든** 버그 수정은 현재 버그 수정을 지원하는 최신 버전(현재는 `12.x`)으로 보내야 합니다. 이미 출시된 기능에 대한 버그 수정은 절대 `master` 브랜치로 보내서는 안 되며, 오직 다가오는 릴리스에만 존재하는 기능을 수정할 때에만 `master` 브랜치를 사용해야 합니다.

**완전히 하위 호환성을 유지**하는 **작은 기능**은 최신 안정 브랜치(현재는 `12.x`)로 보낼 수 있습니다.

**대규모 새로운 기능** 또는 **호환성이 깨지는 변경이 포함된 기능**은 항상 다가오는 릴리스를 담당하는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소 내 `resources/css` 또는 `resources/js` 등 컴파일된 파일에 영향을 주는 변경 사항을 제출하는 경우, 컴파일된 파일 자체는 커밋하지 말아야 합니다. 이 파일들은 용량이 크기 때문에, 관리자가 현실적으로 수정 내역을 검토할 수 없습니다. 이 점을 악용하여 Laravel에 악성 코드를 주입하는 공격이 있을 수 있으므로, 모든 컴파일된 파일은 Laravel 관리자에 의해 직접 생성 및 커밋됩니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 이메일(<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>)로 신고해 주시기 바랍니다. 모든 보안 취약점은 신속하게 처리될 예정입니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 유효한 Laravel 문서 블록의 예시입니다. `@param` 속성은 두 칸의 공백, 인수 타입, 다시 두 칸 공백, 마지막으로 변수명을 기재합니다:

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

네이티브 타입 지정을 통해 `@param`이나 `@return` 속성이 중복되는 경우, 해당 문서는 생략해도 됩니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

하지만 네이티브 타입이 generic(제네릭)인 경우, `@param` 또는 `@return` 속성을 사용하여 제네릭 타입을 반드시 명시해야 합니다:

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

코드 스타일이 완벽하지 않아도 괜찮습니다! [StyleCI](https://styleci.io/)가 풀 리퀘스트 병합 후 자동으로 스타일을 수정하여 Laravel 저장소에 반영합니다. 덕분에 우리는 코드 스타일보다 기여의 본질적인 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 Ruby 행동 강령을 기반으로 하고 있습니다. 행동 강령 위반은 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 반대 견해를 관용적으로 받아들이며 존중합니다.
- 참가자는 언행에 개인적 공격이나 비하 발언이 없어야 하며, 이를 스스로 책임져야 합니다.
- 타인의 말과 행동을 해석할 때에는 항상 선의로 받아들여야 합니다.
- 일반적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>
