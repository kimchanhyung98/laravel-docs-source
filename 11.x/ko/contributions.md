# 기여 안내 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어느 브랜치에?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트 (Bug Reports)

활발한 협업을 장려하기 위해 Laravel은 단순 버그 리포트보다 풀 리퀘스트를 적극 권장합니다. 풀 리퀘스트는 "ready for review" 상태(초안 상태인 "draft"가 아님)이고 새 기능에 대한 모든 테스트가 통과할 때만 검토됩니다. "draft" 상태로 오래 방치된 비활성 풀 리퀘스트는 며칠 후에 닫힙니다.

그럼에도 불구하고 버그 리포트를 제출할 경우, 제목과 명확한 문제 설명을 포함해야 합니다. 또한 가능한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 첨부해야 합니다. 버그 리포트의 목적은 자신과 다른 사람들이 버그를 쉽게 재현하고 수정할 수 있도록 돕는 데 있습니다.

버그 리포트는 같은 문제를 겪는 사람들이 함께 해결할 수 있길 바라는 마음으로 작성됩니다. 버그 리포트만으로 자동으로 활동이 일어나거나 다른 사람이 바로 고쳐줄 것이라 기대하지 마십시오. 버그 리포트는 문제 해결의 시작점을 마련하는 것입니다. 직접 기여하고 싶다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)의 수정을 도와주실 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인해야 합니다.

Laravel을 사용하다가 DocBlock, PHPStan, 또는 IDE 경고가 부적절하다고 생각되면 GitHub 이슈를 생성하지 말고, 대신 해당 문제를 고치는 풀 리퀘스트를 제출해 주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별 저장소가 있습니다:

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Breeze](https://github.com/laravel/breeze)
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
- [Laravel Jetstream](https://github.com/laravel/jetstream)
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
- [Laravel Website](https://github.com/laravel/laravel.com)

</div>

<a name="support-questions"></a>
## 지원 질문 (Support Questions)

Laravel의 GitHub 이슈 트래커는 Laravel 사용법이나 지원을 제공하기 위한 공간이 아닙니다. 대신 다음 채널 중 하나를 이용해 주세요:

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

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작 개선을 제안할 수 있습니다. 새 기능 제안을 할 때는 기능 구현에 필요한 코드 일부를 직접 작성할 의향이 있어야 합니다.

버그, 새로운 기능, 기존 기능 구현에 대한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel 유지 관리자인 Taylor Otwell은 보통 평일 08:00~17:00 (UTC-06:00, 시카고 시간 기준)에 채널에 상주하며 때때로 다른 시간에도 접속합니다.

<a name="which-branch"></a>
## 어느 브랜치에? (Which Branch?)

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재 `11.x`)으로 보내야 합니다. 버그 수정은 다가올 릴리즈에만 존재하는 기능을 고치지 않는 이상 절대 `master` 브랜치로 보내지 않습니다.

현재 릴리스와 완전한 역호환성을 보장하는 **사소한** 기능은 최신 안정 브랜치(현재 `11.x`)에 보낼 수 있습니다.

**주요** 신규 기능이나 호환성에 영향을 주는 변경을 포함한 기능은 항상 다가올 릴리스를 포함하는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋 (Compiled Assets)

`laravel/laravel` 저장소 내 `resources/css` 또는 `resources/js`에 있는 대부분의 파일과 같이 컴파일된 파일에 영향을 주는 변경을 제출할 경우, 컴파일된 파일을 커밋하지 마십시오. 컴파일된 파일은 용량이 크고 유지 관리자가 검토하기 어렵기 때문입니다. 악의적인 코드 삽입을 방지하기 위한 조치로, 모든 컴파일된 파일은 Laravel 유지 관리자가 직접 생성해 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 직접 이메일을 보내주시기 바랍니다: <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. 모든 보안 취약점은 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 Laravel 문서 블록의 예시입니다. `@param` 속성 뒤에는 공백 두 칸, 인수 타입, 다시 공백 두 칸, 그리고 변수명이 옵니다:

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

`@param`이나 `@return`이 네이티브 타입으로 중복될 경우 삭제해도 됩니다:

```
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

그러나 네이티브 타입이 일반 제네릭 타입인 경우, `@param`이나 `@return`을 사용해 제네릭 타입을 명시해야 합니다:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 자동으로 스타일 수정을 Laravel 저장소에 병합해 줍니다. 덕분에 우리는 기여하는 내용에 더 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령을 기반으로 합니다. 행동 강령 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 서로 다른 견해에 관용을 베풀어야 합니다.
- 참가자는 개인 공격이나 모욕적인 발언을 하지 않아야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행위는 용납되지 않습니다.

</div>