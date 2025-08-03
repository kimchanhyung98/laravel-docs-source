# 컨트리뷰션 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 관련 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어느 브랜치에?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트 (Bug Reports)

적극적인 협업을 장려하기 위해, Laravel은 단순히 버그 리포트를 받는 것뿐만 아니라 풀 리퀘스트(PR) 제출을 강력히 권장합니다. 풀 리퀘스트는 "ready for review"(초안 상태가 아닌)로 표시되고 새로운 기능에 대한 모든 테스트가 통과해야만 검토됩니다. 미완성 상태로 오래 방치된 초안 상태의 풀 리퀘스트는 며칠 후 자동으로 닫힙니다.

그러나 버그 리포트를 제출할 경우, 문제에 대한 제목과 명확한 설명이 포함되어야 합니다. 또한 가능한 한 관련 정보와 문제를 재현할 수 있는 코드 예제를 포함해야 합니다. 버그 리포트의 목표는 자신과 다른 사람들이 문제를 쉽게 재현하고 수정할 수 있도록 하는 것입니다.

버그 리포트는 같은 문제를 겪는 사람들이 함께 해결책을 찾도록 돕기 위해 작성하는 것입니다. 자동으로 누군가가 활동하거나 즉시 고쳐줄 것을 기대하지 마세요. 버그 리포트 작성은 문제 해결의 출발점 역할을 합니다. 직접 기여하고 싶다면 [Laravel의 이슈 트래커](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)에서 등록된 버그를 고치는 데 도움을 줄 수 있습니다. 모든 Laravel 이슈를 보려면 GitHub 로그인이 필요합니다.

Laravel 소스 코드는 GitHub에서 관리되며, Laravel 관련 프로젝트별 저장소는 다음과 같습니다:

<div class="content-list" markdown="1">

- [Laravel 애플리케이션](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel 문서](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead 빌드 스크립트](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel 웹사이트](https://github.com/laravel/laravel.com-next)

</div>

<a name="support-questions"></a>
## 지원 관련 질문 (Support Questions)

Laravel의 GitHub 이슈 트래커는 Laravel 지원 또는 도움 제공 용도로 사용되지 않습니다. 도움을 원한다면 아래 채널 중 하나를 이용하세요:

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

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작 개선을 제안할 수 있습니다. 새로운 기능을 제안할 경우, 그 기능 완성을 위해 필요한 코드 중 일부라도 직접 구현할 의지가 있어야 합니다.

버그, 새로운 기능, 기존 기능 구현에 관한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 오갑니다. Laravel 유지관리자인 Taylor Otwell은 보통 평일 오전 8시부터 오후 5시(UTC-06:00, America/Chicago 기준)에 채널에 접속해 있으며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
## 어느 브랜치에? (Which Branch?)

**모든** 버그 수정은 버그 수정 지원이 이루어지는 최신 버전 (현재 `9.x`)에 보내야 합니다. 기능이 오직 다가오는 릴리스에만 존재하는 경우를 제외하고는 버그 수정을 `master` 브랜치로 보내면 안 됩니다.

**경미한** 기능이 현재 릴리스와 완전히 하위 호환 가능한 경우, 최신 안정 브랜치 (현재 `9.x`)에 보낼 수 있습니다.

**중대한** 새 기능이나 파괴적 변경(breaking changes)이 있는 기능은 항상 다가올 릴리스가 담긴 `master` 브랜치에 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산 (Compiled Assets)

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등의 컴파일된 파일에 영향을 주는 변경사항을 제출하는 경우, 컴파일된 파일은 커밋하지 마세요. 파일 크기가 크기 때문에 유지관리자가 현실적으로 검토할 수 없고, 악의적인 코드 삽입 경로로 악용될 수도 있습니다. 이를 방지하기 위해 모든 컴파일된 파일은 Laravel 유지관리자가 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel 내 보안 취약점을 발견하면, 바로 Taylor Otwell에게 이메일(<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>)로 신고하세요. 모든 보안 취약점은 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 Laravel에서 유효한 문서 블록 예시입니다. `@param` 태그 뒤에는 두 칸 띄움, 인수 타입, 다시 두 칸 띄움, 그리고 변수명이 오는 점을 유의하세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 머지된 후 자동으로 스타일 수정을 Laravel 저장소에 병합합니다. 덕분에 기여자는 코드 스타일보다는 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령을 바탕으로 합니다. 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 반대 의견에 관용을 가져야 합니다.
- 참여자는 개인 공격이나 모욕적인 발언을 삼가야 합니다.
- 다른 사람의 말과 행동을 해석할 때는 항상 선의로 가정해야 합니다.
- 합리적으로 괴롭힘이라 판단되는 행동은 용납되지 않습니다.

</div>