# 기여 가이드 (Contribution Guide)

- [버그 보고](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어느 브랜치에?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 보고 (Bug Reports)

Laravel은 활발한 협업을 독려하기 위해 단순한 버그 보고보다는 풀 리퀘스트를 강력히 권장합니다. 풀 리퀘스트는 "ready for review" 상태로 표시되고(즉, "draft" 상태가 아닐 때) 새 기능에 대한 모든 테스트가 통과한 경우에만 검토됩니다. 오랫동안 활동이 없는 "draft" 상태의 풀 리퀘스트는 며칠 후에 종료될 수 있습니다.

하지만 버그를 보고할 경우, 문제의 제목과 명확한 설명을 포함해야 합니다. 또한 관련된 모든 정보를 최대한 포함하고, 문제를 보여주는 코드 예제도 첨부하는 것이 좋습니다. 버그 보고의 목적은 자신과 다른 사람들이 문제를 쉽게 재현하고 해결책을 개발할 수 있도록 돕는 것입니다.

버그 보고는 같은 문제를 겪고 있는 다른 사람들과 협력하여 해결책을 찾기 위한 첫걸음임을 기억하세요. 버그 보고가 자동으로 활동을 유발하거나 누군가가 즉시 해결해줄 것을 기대하지 마십시오. 버그 보고는 문제를 해결하는 길을 여는 도움을 주기 위한 것이며, 여러분도 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 직접 고쳐 기여할 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub 인증이 필요합니다.

Laravel 사용 중에 DocBlock, PHPStan 또는 IDE 경고가 부적절하다고 생각되면 GitHub 이슈를 만들지 말고, 대신 문제를 고치는 풀 리퀘스트를 제출해 주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별로 별도의 저장소가 있습니다:

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
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Website](https://github.com/laravel/laravel.com-next)

</div>

<a name="support-questions"></a>
## 지원 질문 (Support Questions)

Laravel GitHub 이슈 트래커는 Laravel의 직접적인 도움이나 지원을 제공하기 위한 곳이 아닙니다. 대신 다음 채널 중 하나를 이용하세요:

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
## 코어 개발 토론 (Core Development Discussion)

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 기능 개선을 제안할 수 있습니다. 새로운 기능을 제안할 경우, 최소한 일부 기능 구현 코드를 작성할 의지가 있어야 합니다.

버그, 새로운 기능 및 기존 기능 구현에 대한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자 Taylor Otwell은 일반적으로 평일 오전 8시부터 오후 5시(UTC-06:00 또는 America/Chicago) 사이에 채널에 있으며, 다른 시간에도 간헐적으로 접속합니다.

<a name="which-branch"></a>
## 어느 브랜치에? (Which Branch?)

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재 `10.x`)에 보내야 합니다. 버그 수정은 다가오는 릴리스에만 존재하는 기능을 고치지 않는 이상 절대 `master` 브랜치로 보내지 마세요.

**작은** 기능이 현재 릴리스와 완벽하게 호환될 경우 최신 안정 브랜치(현재 `10.x`)에 보낼 수 있습니다.

**큰** 새로운 기능이나 호환성을 깨뜨리는 기능은 항상 다가오는 릴리스를 포함하는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산 (Compiled Assets)

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 내 대부분 파일 같이 컴파일된 파일에 영향을 미치는 변경 사항을 보낼 때는 컴파일된 파일은 커밋하지 마세요. 크기가 크고 유지 관리자가 현실적으로 검토할 수 없기 때문입니다. 이는 Laravel에 악성 코드를 주입하는 공격 수단으로 악용될 수 있습니다. 이를 방지하기 위해 모든 컴파일된 파일은 Laravel 유지 관리자가 직접 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel에서 보안 취약점을 발견하면, Taylor Otwell에게 이메일 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a> 로 신고해 주세요. 모든 보안 취약점은 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 유효한 Laravel 문서 블록 예시입니다. `@param` 속성은 두 칸 공백, 타입, 두 칸 공백, 변수 이름 순으로 표기하는 점에 주의하세요:

```
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

`@param` 또는 `@return` 속성이 네이티브 타입 사용으로 중복될 경우 삭제할 수 있습니다:

```
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

다만 네이티브 타입이 제네릭일 경우에는 `@param` 또는 `@return` 속성으로 제네릭 타입을 명시하세요:

```
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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 Laravel 저장소에 스타일 수정사항을 자동으로 반영해 줍니다. 덕분에 저희는 기여의 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 서로 다른 의견에 관대해야 합니다.
- 참가자는 언어와 행동에서 개인 공격이나 경멸적인 발언을 하지 않아야 합니다.
- 다른 사람의 말과 행동을 해석할 때는 항상 선의를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>