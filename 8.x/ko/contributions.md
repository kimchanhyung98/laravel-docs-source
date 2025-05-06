# 기여 안내서

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [핵심 개발 논의](#core-development-discussion)
- [어떤 브랜치?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

적극적인 협업을 장려하기 위해, Laravel은 단순한 버그 리포트뿐 아니라 풀 리퀘스트 형태로의 기여를 강력히 권장합니다. 실패하는 테스트를 포함한 풀 리퀘스트로도 "버그 리포트"를 보낼 수 있습니다. 풀 리퀘스트는 "리뷰 준비 완료"(draft 상태가 아님)로 표시되고 새 기능의 모든 테스트가 통과할 때에만 검토됩니다. 몇 일 동안 draft 상태로 남아있는 비활성 풀 리퀘스트는 닫힙니다.

그러나, 버그 리포트를 제출하는 경우에는 제목과 문제의 명확한 설명이 포함되어야 합니다. 또한 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 포함해야 합니다. 버그 리포트의 목적은 본인과 다른 사람들이 버그를 쉽게 재현하고 수정할 수 있도록 하는 것입니다.

버그 리포트는 같은 문제를 가진 다른 사람들이 문제 해결에 함께 협력할 수 있기를 바라는 마음으로 작성됩니다. 버그 리포트에 바로 활동이 일어나거나, 바로 수정될 것이라 기대하지 마십시오. 문제 해결의 첫 단계를 스스로와 다른 사람들을 위해 제공하는 것이 중요합니다. 기여하고 싶으시다면, [이슈 트래커에 등록된 버그 수정](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)에 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub 인증이 필요합니다.

Laravel 소스 코드는 GitHub에서 관리되고 있으며, 각 Laravel 프로젝트마다 저장소가 있습니다:

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Website](https://github.com/laravel/laravel.com-next)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 Laravel의 사용법이나 지원 제공을 위한 용도가 아닙니다. 대신 다음 채널 중 하나를 활용해주세요:

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
## 핵심 개발 논의

Laravel 프레임워크 저장소의 [GitHub 토론 보드](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작의 개선을 제안할 수 있습니다. 새로운 기능을 제안할 경우, 해당 기능 구현에 필요한 코드 일부를 직접 구현할 의향이 있어야 합니다.

버그, 새 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 메인테이너인 Taylor Otwell은 평일 기준(UTC-06:00, 미국/시카고시간) 오전 8시~오후 5시에 주로 채널에 있으며, 그 외 시간에도 가끔 입장합니다.

<a name="which-branch"></a>
## 어떤 브랜치?

**모든** 버그 수정은 최신 안정 브랜치로 보내야 합니다. 버그 수정은 다가오는 릴리스에만 존재하는 기능을 수정하는 경우가 아니라면 **절대** `master` 브랜치로 보내지 마세요.

**완전히 하위 호환되는** **사소한** 기능은 최신 안정 브랜치로 보낼 수 있습니다.

**주요** 신규 기능은 항상 향후 릴리스를 포함하는 `master` 브랜치로 보내야 합니다.

본인의 기능이 주요(major) 또는 사소(minor) 기능인지 확실하지 않다면, [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 Taylor Otwell에게 문의해주세요.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등 컴파일된 파일에 영향을 주는 변경을 제출하는 경우, 컴파일된 파일을 커밋하지 마십시오. 파일 크기가 커서 메인테이너가 현실적으로 검토하기 어렵습니다. 이는 악성 코드를 Laravel에 주입하는 데 악용될 수 있습니다. 이러한 위험을 방지하기 위해 모든 컴파일된 파일은 Laravel 메인테이너가 생성 및 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견했다면 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 Taylor Otwell에게 이메일을 보내주시기 바랍니다. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 유효한 Laravel 문서화 블록의 예시입니다. `@param` 속성 뒤에 공백 2개, 인자 타입, 다시 공백 2개, 그 다음 변수명이 오는 것을 주의하세요:

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
        //
    }

<a name="styleci"></a>
### StyleCI

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트 병합 이후 Laravel 저장소에 모든 스타일 수정을 자동으로 병합해줍니다. 덕분에 우리는 기여의 내용에 집중할 수 있으며, 코드 스타일에 대해서는 걱정하지 않아도 됩니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 Ruby의 행동 강령에서 비롯되었습니다. 행동 강령 위반 사례는 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 반대 의견에 대해 관용적이어야 합니다.
- 참가자는 자신의 언행이 개인에 대한 공격이나 폄하하는 발언이 없도록 주의해야 합니다.
- 타인의 말과 행동을 해석할 때 항상 선의를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>