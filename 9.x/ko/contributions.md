# 기여 가이드

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어느 브랜치에?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

적극적인 협업을 장려하기 위해, Laravel은 단순한 버그 리포트뿐 아니라 풀리퀘스트(pull request)를 강력히 권장합니다. 풀리퀘스트는 "draft" 상태가 아닌 "ready for review"로 표시되고, 새로운 기능에 대한 모든 테스트가 통과한 경우에만 리뷰됩니다. "draft" 상태로 장기간 비활성화된 풀리퀘스트는 며칠 후에 자동으로 닫힐 수 있습니다.

단, 버그 리포트를 작성할 경우 제목과 문제에 대한 명확한 설명이 포함되어야 합니다. 또한 최대한 많은 관련 정보와 문제를 재현할 수 있는 코드 예제를 첨부해야 합니다. 버그 리포트의 목적은 본인과 타인이 문제를 쉽게 재현하고 해결 방법을 찾을 수 있도록 돕는 데 있습니다.

기억하세요, 버그 리포트는 동일한 문제를 겪는 다른 이들이 당신과 함께 문제를 해결할 수 있도록 기대하며 만들어집니다. 버그 리포트가 자동으로 처리되거나 누군가가 신속히 수정해주길 기대하지 마세요. 버그 리포트는 문제 해결의 첫걸음입니다. 원한다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중 직접 수정에 참여할 수도 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인이 필요합니다.

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
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Website](https://github.com/laravel/laravel.com-next)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 도움말이나 지원 질문을 위한 용도가 아닙니다. 대신, 다음 채널을 이용해 주세요:

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

Laravel의 새로운 기능 제안이나 기존 동작에 대한 개선은 Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에 올릴 수 있습니다. 새로운 기능을 제안할 때에는, 해당 기능을 완성하는 데 필요한 코드의 일부라도 직접 구현할 의사가 있어야 합니다.

버그, 신규 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel) 내 `#internals` 채널에서 진행됩니다. Laravel의 메인테이너인 Taylor Otwell은 평일(UTC-06:00 또는 America/Chicago 기준) 오전 8시부터 오후 5시 사이에 주로 활동하며, 다른 시간에도 간헐적으로 채널에 접속합니다.

<a name="which-branch"></a>
## 어느 브랜치에?

**모든** 버그 수정은 버그 픽스를 지원하는 최신 버전(현재는 `9.x`)으로 보내야 합니다. 버그 수정은 **절대** `master` 브랜치로 보내지 마세요. 단, 다가오는 릴리스에만 존재하는 기능을 수정하는 경우는 예외입니다.

**완전히 이전 버전과 호환되는** **마이너** 기능 추가는 최신 안정 브랜치(현재는 `9.x`)에 보낼 수 있습니다.

**주요** 신규 기능이나 기존과 호환되지 않는 변경점이 포함된 기능은 항상 다가오는 릴리스용 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js`처럼, 컴파일된 파일에 영향을 주는 변경사항을 제출할 때에는 컴파일된 파일 자체는 커밋하지 마세요. 파일 크기가 크기 때문에 메인테이너가 실질적으로 리뷰할 수 없습니다. 이는 악의적으로 Laravel에 악성 코드를 주입하는 방법으로 악용될 수 있으므로, 모든 컴파일 파일은 Laravel 메인테이너에 의해 생성되어 커밋됩니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견하셨다면, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내주세요. 모든 보안 취약점 보고는 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준 및 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 뒤에 두 칸 띄우고 인자 타입을 적은 뒤, 다시 두 칸 띄운 후 변수명을 작성하는 점을 유의하세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀리퀘스트가 머지된 후 자동으로 스타일 수정 사항을 Laravel 저장소에 병합해줍니다. 이를 통해 우리는 기여 내용에 집중할 수 있고, 코드 스타일에 신경 쓸 필요가 없습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반 사항은 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 반대 의견에도 관용을 가져야 합니다.
- 참여자는 언어 및 행동에서 개인 공격이나 비방, 폄하 발언이 없어야 합니다.
- 타인의 언어나 행동을 해석할 때에는 항상 선의로 해석해야 합니다.
- 괴롭힘으로 간주될 수 있는 행위는 용납되지 않습니다.

</div>