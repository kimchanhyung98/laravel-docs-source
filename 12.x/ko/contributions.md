# 기여 가이드 (Contribution Guide)

- [버그 보고](#bug-reports)
- [지원 문의](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어느 브랜치에 기여해야 하나요?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 보고

활발한 협업을 장려하기 위해, Laravel은 단순한 버그 보고뿐만 아니라 풀 리퀘스트(Pull Request) 제출을 적극 권장합니다. 풀 리퀘스트는 "Ready for review"(검토 준비됨) 상태(즉, "Draft" 상태가 아님)로 표시되고, 새 기능의 모든 테스트가 통과되어야만 리뷰됩니다. "Draft" 상태로 남아 있는 비활동성 풀 리퀘스트는 며칠 후 자동으로 닫힙니다.

하지만 버그를 신고할 경우, 이슈에는 제목과 문제에 대한 명확한 설명이 포함되어야 합니다. 또한 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 포함해야 합니다. 버그 리포트의 목적은 여러분 자신과 다른 사람들이 해당 버그를 쉽게 재현하고 해결 방법을 개발할 수 있도록 돕는 데 있습니다.

버그 리포트는 동일한 문제를 겪고 있는 다른 사람들이 함께 문제를 해결하도록 협력할 수 있도록 작성됩니다. 이슈가 자동으로 해결되거나 즉시 누군가가 고쳐 주기를 기대해서는 안 됩니다. 버그 리포트 작성은 문제 해결의 출발점입니다. 만약 기여하고 싶다면, [이슈 트래커에 등록된 모든 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 직접 수정해 보는 방법도 있습니다. 모든 Laravel의 이슈를 보려면 GitHub 인증이 필요합니다.

Laravel을 사용하면서 DocBlock, PHPStan, IDE 경고 등 문서화가 잘못된 부분이 보이면 GitHub 이슈를 생성하지 말고, 해당 문제를 직접 수정하여 풀 리퀘스트로 제출해 주시기 바랍니다.

Laravel 소스 코드는 GitHub에서 관리되며, 모든 Laravel 프로젝트별로 별도의 저장소가 있습니다:

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
## 지원 문의

Laravel의 GitHub 이슈 트래커는 Laravel 관련 도움이나 지원을 제공하기 위한 목적이 아닙니다. 아래 채널 중 하나를 이용해 주십시오:

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

Laravel 프레임워크 저장소의 [GitHub 논의 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작의 개선 사항을 제안할 수 있습니다. 새로운 기능을 제안할 때는, 해당 기능을 완성하는 데 필요한 코드의 일부라도 직접 구현할 의지가 있는 것이 바람직합니다.

버그, 신규 기능, 기존 기능의 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel) 내 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자인 Taylor Otwell은 평일(UTC-06:00 또는 America/Chicago 기준) 오전 8시~오후 5시에 주로 해당 채널에 상주하며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
## 어느 브랜치에 기여해야 하나요?

**모든** 버그 수정은 최신 버그 수정 지원 버전(현재 `12.x`)으로 보내야 합니다. 버그 수정은 **절대** `master` 브랜치로 직접 보내서는 안 되며, 다가오는 릴리즈에만 존재하는 기능을 수정하는 경우에만 예외로 허용됩니다.

**완전한 하위 호환성**을 지닌 **마이너 기능 추가**는 최신 안정 브랜치(현재 `12.x`)로 보낼 수 있습니다.

**주요 신규 기능**이나 **호환성이 깨지는 변경 사항**은 항상 다가오는 릴리즈인 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등 컴파일된 파일에 영향을 주는 변경 사항을 제출할 경우, 컴파일된 파일을 커밋하지 마십시오. 이러한 파일은 크기가 커서 유지 관리자가 현실적으로 리뷰할 수 없습니다. 이는 악성 코드를 숨겨 넣는 수단으로 악용될 수 있기에, 모든 컴파일된 파일은 Laravel 유지 관리자가 직접 생성 및 커밋할 예정입니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내 주십시오. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서화 블록의 예시입니다. `@param` 속성 뒤에는 두 칸의 공백, 인수 타입, 다시 두 칸의 공백, 그리고 변수명이 차례로 옵니다:

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

`@param` 또는 `@return` 속성이 네이티브 타입 덕분에 중복되는 경우, 해당 속성들은 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

하지만, 네이티브 타입이 제네릭일 경우에는 `@param` 또는 `@return` 속성을 통해 제네릭 타입을 명시해 주시기 바랍니다:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 Laravel 저장소에 자동으로 스타일 관련 수정을 반영해 줍니다. 이를 통해 우리는 기여의 '내용'에 집중하고 코드 스타일에 지나치게 신경 쓸 필요가 없습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 Ruby 행동 강령을 기반으로 합니다. 행동 강령 위반 시 Taylor Otwell(taylor@laravel.com)에게 신고해 주십시오:

<div class="content-list" markdown="1">

- 참가자는 상반되는 의견에도 관대해야 합니다.
- 참가자는 언어 및 행동에 인신 공격이나 비방적 발언이 없어야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의를 전제로 삼아야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행위는 용납되지 않습니다.

</div>
