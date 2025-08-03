# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어느 브랜치에 보낼까?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트 (Bug Reports)

활발한 협업을 장려하기 위해 Laravel은 단순한 버그 리포트뿐만 아니라 풀 리퀘스트를 적극 권장합니다. 버그 리포트는 실패하는 테스트를 포함한 풀 리퀘스트 형태로도 제출될 수 있습니다. 풀 리퀘스트는 "검토 준비 완료"로 표시되어야 하며("드래프트" 상태가 아님), 새 기능에 대한 모든 테스트가 통과할 때만 리뷰됩니다. 활성 상태가 아닌 "드래프트" 상태로 남아 있는 풀 리퀘스트는 며칠 후에 닫힙니다.

버그 리포트를 제출할 경우, 제목과 문제에 대한 명확한 설명을 포함해야 합니다. 또한 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 샘플을 포함해야 합니다. 버그 리포트의 목적은 본인과 다른 사람들이 버그를 쉽게 재현하고 문제를 해결할 수 있도록 돕는 데 있습니다.

버그 리포트는 같은 문제를 가진 다른 사람들이 함께 문제 해결에 참여하기를 기대하며 작성됩니다. 따라서 리포트 제출만으로 자동으로 처리되거나 다른 사람들이 즉시 수정해 줄 것을 기대해서는 안 됩니다. 버그 리포트 작성은 문제 해결의 출발점이 될 뿐입니다. 기여를 원한다면 [Laravel 이슈 트래커에 등록된 버그 중](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 직접 수정에 참여할 수 있습니다. 모든 Laravel 이슈를 보려면 GitHub 인증이 필요합니다.

Laravel 소스 코드는 GitHub에서 관리되며, Laravel 프로젝트별로 다음과 같은 저장소가 있습니다:

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
## 지원 질문 (Support Questions)

Laravel GitHub 이슈 트래커는 Laravel 도움말이나 지원을 제공하기 위한 곳이 아닙니다. 대신 다음 채널 중 하나를 이용해 주세요:

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

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작 개선에 대해 제안할 수 있습니다. 새 기능을 제안할 경우, 그 기능 완성을 위해 최소한 일부 코드 구현을 기꺼이 책임질 의향이 있어야 합니다.

버그, 새 기능, 기존 기능 구현에 관한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자인 Taylor Otwell은 평일 오전 8시부터 오후 5시(UTC-06:00 또는 America/Chicago 기준)에 주로 채널에 있으며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
## 어느 브랜치에 보낼까? (Which Branch?)

**모든** 버그 수정은 최신 안정 브랜치에 보내야 합니다. 다가오는 릴리스에만 있는 기능을 수정하는 경우를 제외하고, 버그 수정은 절대 `master` 브랜치로 보내지 마세요.

**작은** 기능이 현재 릴리스와 완전히 하위 호환된다면 최신 안정 브랜치에 보낼 수 있습니다.

**중대한** 신규 기능은 항상 다가오는 릴리스를 위한 `master` 브랜치에 보내야 합니다.

기능이 중대하거나 사소한지 확실하지 않으면 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 Taylor Otwell에게 문의하세요.

<a name="compiled-assets"></a>
## 컴파일된 자산 (Compiled Assets)

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 폴더 내 대부분 파일처럼 컴파일된 파일에 영향을 주는 변경을 제출할 경우, 컴파일된 파일은 커밋하지 마세요. 이들은 크기가 크고 유지 관리자가 현실적으로 리뷰하기 어렵기에, 악성 코드를 삽입할 위험이 있습니다. 이를 예방하기 위해 모든 컴파일된 파일은 Laravel 유지 관리자가 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel에서 보안 취약점을 발견할 경우, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내 주세요. 모든 보안 문제는 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 Laravel에서 사용하는 유효한 문서 블록 예시입니다. `@param` 속성 다음에 두 칸, 인수 타입, 두 칸, 그리고 변수명이 옵니다:

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
    //
}
```

<a name="styleci"></a>
### StyleCI

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 후 자동으로 스타일 수정 사항을 Laravel 저장소에 병합해 줍니다. 이를 통해 우리는 기여 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 반대 의견에 관용을 가져야 합니다.
- 참가자는 자신의 언어와 행동이 개인 공격이나 비방적인 발언이 없도록 해야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>