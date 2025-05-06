# 기여 가이드

- [버그 리포트](#bug-reports)
- [지원 문의](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치에?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

적극적인 협업을 장려하기 위해, Laravel은 버그 리포트뿐만 아니라 풀 리퀘스트 제출을 적극 권장합니다. 풀 리퀘스트는 "검토 준비 완료(ready for review)"로 표시되고(즉, "임시(draft)" 상태가 아님), 새로운 기능에 대한 모든 테스트가 통과하는 경우에만 검토됩니다. "임시" 상태로 남아 있는 비활성 풀 리퀘스트는 며칠 후 자동으로 닫힙니다.

버그 리포트를 제출할 경우, 이슈에는 제목과 문제에 대한 명확한 설명이 포함되어야 합니다. 또한 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 포함해야 합니다. 버그 리포트의 목적은 자신과 다른 사람들이 버그를 손쉽게 재현하고 해결책을 개발할 수 있도록 돕는 것입니다.

버그 리포트는 동일한 문제를 겪는 다른 사람들과 협업할 수 있기를 바라는 마음으로 작성됩니다. 버그 리포트를 제출했다고 해서 자동으로 활동이 일어나거나, 누군가가 바로 고쳐줄 것이라고 기대하지 마세요. 버그 리포트 작성은 문제 해결의 출발점이 될 수 있습니다. 직접 기여하고 싶다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 해결에 참여할 수 있습니다. Laravel의 모든 이슈를 확인하려면 GitHub에 로그인해야 합니다.

Laravel을 사용할 때 DocBlock, PHPStan, 또는 IDE 경고가 올바르지 않은 것을 발견하면, GitHub 이슈를 생성하지 마시고, 문제를 수정하는 풀 리퀘스트를 보내주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트 별로 저장소가 존재합니다:

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
## 지원 문의

Laravel의 GitHub 이슈 트래커는 지원이나 도움을 받기 위한 용도가 아닙니다. 지원이 필요하다면 다음 채널을 이용해 주세요:

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

새로운 기능 제안이나 기존 Laravel 동작 개선 제안은 Laravel framework 저장소의 [GitHub Discussion 보드](https://github.com/laravel/framework/discussions)를 이용해 주시기 바랍니다. 새로운 기능을 제안하는 경우, 해당 기능을 완성하는 데 필요한 코드 일부라도 구현할 의지가 있어야 합니다.

버그, 신규 기능, 기존 기능 구현 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 비공식적으로 진행됩니다. Laravel 관리자 Taylor Otwell은 평일(UTC-06:00, 미국/시카고 기준) 오전 8시부터 오후 5시까지 대부분 채널에 있으며, 그 외 시간에는 간헐적으로 채널에 참여합니다.

<a name="which-branch"></a>
## 어떤 브랜치에?

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재는 `10.x`)에 보내 주십시오. 버그 수정은 **절대** `master` 브랜치에 보내지 마세요. 다만, 아직 출시되지 않은 기능에 한정해서는 예외입니다.

**완전히 하위 호환성이 유지되는** **경미한** 기능은 최신 안정 버전 브랜치(현재 `10.x`)로 보내 주십시오.

**주요** 신규 기능이나 호환성이 깨지는 변경이 포함된 기능은 항상 다음 출시 버전이 포함된 `master` 브랜치에 보내 주십시오.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css`나 `resources/js`와 같이 컴파일된 파일에 영향을 주는 변경을 제출할 경우, 컴파일된 파일은 커밋하지 마세요. 큰 파일 특성상 관리자에 의해 현실적으로 검토하기 어렵고, 이를 악용해 악성 코드가 Laravel에 주입될 수 있습니다. 이러한 보안 방지를 위해, 모든 컴파일 파일은 Laravel 관리자가 생성 및 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel 내의 보안 취약점을 발견한 경우, Taylor Otwell에게 이메일(<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>)로 제보해 주세요. 모든 보안 취약점은 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 뒤에는 두 개의 공백, 인자 타입, 다시 두 개의 공백, 마지막으로 변수명이 옵니다:

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

네이티브 타입 덕분에 `@param`이나 `@return` 속성이 중복될 경우, 해당 속성은 생략할 수 있습니다:

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        //
    }

하지만 네이티브 타입이 제네릭일 경우에는, `@param`이나 `@return` 속성을 사용해 제네릭 타입을 명시해 주세요:

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

<a name="styleci"></a>
### StyleCI

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 자동으로 스타일 수정을 Laravel 저장소에 병합해줍니다. 이는 기여의 내용에 집중할 수 있게 해주며, 코드 스타일 자체에 신경 쓸 필요가 없습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반이 있을 경우 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 상반되는 견해에 대해 관용을 가져야 합니다.
- 참여자는 언어 및 행동에서 개인적인 공격이나 비방이 없어야 합니다.
- 타인의 말과 행동을 해석할 때, 항상 선한 의도를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>