# 기여 가이드

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치에 기여해야 하나요?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

활발한 협업을 장려하기 위해, Laravel은 단순 버그 리포트뿐만 아니라 풀 리퀘스트 작성을 적극 권장합니다. 풀 리퀘스트는 "ready for review"(검토 준비됨) 상태로 표시되고(즉, "draft" 상태가 아님), 새로운 기능의 모든 테스트가 통과해야만 검토합니다. 오랫동안 "draft" 상태로 비활성적으로 남아있는 풀 리퀘스트는 며칠 후 닫힙니다.

하지만 버그 리포트를 작성할 경우, 제목과 문제에 대한 명확한 설명이 반드시 포함되어야 합니다. 또한 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 꼭 포함해 주세요. 버그 리포트의 목표는 자신과 다른 사람들이 버그를 쉽게 재현하고 해결책을 개발할 수 있도록 하는 것입니다.

버그 리포트는 동일한 문제를 겪고 있는 다른 사람들이 문제 해결에 협력할 수 있도록 작성됩니다. 버그 리포트에 자동으로 응답이 달리거나, 다른 사람이 즉시 고쳐줄 것이라고 기대하지 마세요. 버그 리포트는 문제를 해결하기 위한 출발점이자, 자신과 타인을 돕기 위한 것입니다. 기여하고 싶으시면 [이슈 트래커에 등록된 모든 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 고치는 데 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인해야 합니다.

Laravel을 사용하다가 잘못된 DocBlock, PHPStan 혹은 IDE 경고를 발견했다면 GitHub 이슈를 생성하지 말고, 문제를 고치는 풀 리퀘스트를 보내 주세요.

Laravel 소스 코드는 GitHub에서 관리되고 있으며, 각 프로젝트별로 저장소가 따로 존재합니다:

<div class="content-list" markdown="1">

- [Laravel 어플리케이션](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Breeze](https://github.com/laravel/breeze)
- [Laravel 문서](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel 프레임워크](https://github.com/laravel/framework)
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
- [Laravel 웹사이트](https://github.com/laravel/laravel.com)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 Laravel에 대한 도움이나 지원을 제공하기 위해 만들어진 것이 아닙니다. 대신 다음 채널 중 하나를 이용해 주세요:

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

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능이나 기존 Laravel 동작의 개선안을 제안할 수 있습니다. 새로운 기능을 제안할 경우, 해당 기능을 완성하는 데 필요한 코드 일부라도 직접 구현할 의향이 있어야 합니다.

버그, 새로운 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이뤄집니다. Laravel 메인테이너인 Taylor Otwell은 주로 평일 오전 8시~오후 5시(UTC-06:00, America/Chicago)에 채널에 상주하며, 그 외 시간에도 간간이 활동합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여해야 하나요?

**모든** 버그 수정은 버그 수정이 지원되는 최신 버전에 보내야 합니다(현재는 `11.x`). 버그 수정은 **절대** `master` 브랜치로 보내지 마세요. 단, 다가올 릴리스에만 존재하는 기능을 수정한다면 예외입니다.

**완전히 하위 호환성**이 보장되는 **작은 기능 추가**는 최신 안정 브랜치(현재는 `11.x`)로 보내면 됩니다.

**주요** 신규 기능이나 호환성이 깨지는 변경 사항은 항상 향후 릴리스가 포함된 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등 컴파일 파일에 영향을 주는 변경 사항을 제출하는 경우, 컴파일된 파일은 커밋하지 마세요. 파일이 너무 크기 때문에 메인테이너가 충분히 검토할 수 없으며, 이는 악의적인 코드가 삽입될 수 있는 가능성을 만듭니다. 이를 방지하기 위해, 모든 컴파일된 파일은 Laravel 메인테이너가 직접 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel 내에서 보안 취약점을 발견한 경우, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내주세요. 모든 보안 취약점은 신속히 처리합니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 뒤에는 두 칸을 띄우고, 인자 타입, 두 칸 띄우기 그리고 변수명이 순서대로 옵니다:

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

만약 네이티브 타입 지정 덕분에 `@param` 또는 `@return` 속성이 중복될 경우, 해당 DocBlock은 제거할 수 있습니다:

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        //
    }

그러나 네이티브 타입이 제네릭인 경우, 반드시 `@param` 또는 `@return` 속성을 이용해 제네릭 타입을 명시해 주세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트 병합 후 Laravel 저장소에 스타일을 자동으로 맞춰줍니다. 덕분에 기여 내용(로직)에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 루비 행동 강령을 바탕으로 합니다. 행동 강령 위반은 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 서로 다른 의견도 관용적으로 받아들여야 합니다.
- 참여자는 언어와 행동이 인신공격이나 비방성 발언이 아닌지 항상 유의해야 합니다.
- 타인의 언어나 행동을 해석할 때 항상 선의로 바라봐야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>