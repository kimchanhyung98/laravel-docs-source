# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어느 브랜치에 기여해야 하나요?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트 (Bug Reports)

활발한 협업을 장려하기 위해 Laravel은 단순한 버그 리포트보다 풀 리퀘스트를 적극 권장합니다. 풀 리퀘스트는 "검토 준비(ready for review)" 상태일 때만 검토하며, "초안(draft)" 상태인 경우는 제외됩니다. 또한 새로운 기능에 대한 모든 테스트가 통과해야 검토가 시작됩니다. 오랫동안 활동이 없는 초안 상태의 풀 리퀘스트는 며칠 후 종료됩니다.

하지만 버그를 신고할 경우, 문제를 명확히 설명하는 제목과 함께 구체적인 설명이 포함되어야 합니다. 또한 관련 정보와 버그를 재현할 수 있는 코드 샘플을 최대한 제공해야 합니다. 버그 리포트의 목적은 작성자뿐 아니라 다른 사람도 문제를 쉽게 재현하고 해결책을 개발할 수 있게 하는 것입니다.

버그 리포트는 같은 문제를 겪는 사람들이 함께 해결하고자 할 때 생성하는 것입니다. 리포트만 올리면 자동으로 활동이 발생하거나 누군가가 즉시 문제를 고쳐줄 것이라고 기대하지 마십시오. 버그 리포트를 만드는 것은 문제 해결의 시작점을 마련하는 것이며, 직접 기여하고 싶다면 [Laravel 이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 직접 수정하는 것도 방법입니다. 모든 Laravel 이슈를 보려면 GitHub에 인증되어 있어야 합니다.

Laravel 사용 중에 부적절한 DocBlock, PHPStan 경고, IDE 경고 등이 발견된다면 GitHub 이슈를 생성하지 마시고, 문제를 고치는 풀 리퀘스트를 제출해주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 프로젝트별 저장소가 있습니다:

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
- [Laravel Homestead](https://github.com/laravel/homestead) ([빌드 스크립트](https://github.com/laravel/settler))
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)
- [Laravel Website](https://github.com/laravel/laravel.com)

</div>

<a name="support-questions"></a>
## 지원 질문 (Support Questions)

Laravel의 GitHub 이슈 트래커는 Laravel 사용 도움이나 지원을 위한 곳이 아닙니다. 대신, 다음 채널들 중 하나를 이용해 주세요:

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

Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 동작 개선 아이디어를 제안할 수 있습니다. 새 기능을 제안한다면, 기능 완성을 위해 필요한 코드 일부라도 직접 구현할 의지가 있어야 합니다.

버그, 새 기능, 기존 기능 구현에 대한 비공식 토론은 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel 유지관리자인 Taylor Otwell는 보통 평일 오전 8시부터 오후 5시(UTC-06:00, America/Chicago 기준) 사이에 이 채널에 상주하며, 그 외의 시간에도 간헐적으로 접속합니다.

<a name="which-branch"></a>
## 어느 브랜치에 기여해야 하나요? (Which Branch?)

**모든** 버그 수정은 버그 수정 지원이 가능한 최신 버전(현재 `12.x`)에 보내야 합니다. 다가오는 릴리즈에서만 존재하는 기능을 고치는 경우를 제외하고, 버그 수정이 `master` 브랜치에 보내져서는 안 됩니다.

현재 릴리즈와 완전히 하위 호환되는 **소규모** 기능은 최신 안정화 브랜치(현재 `12.x`)에 보내도 됩니다.

새로운 주요 기능 또는 호환성을 깨는 변경이 있는 기능은 항상 다가오는 릴리즈용 `master` 브랜치에 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산 (Compiled Assets)

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js`에 있는 대부분 파일처럼 컴파일된 파일에 영향을 주는 변경을 제출할 경우, 컴파일된 파일은 커밋하지 마십시오. 이들 파일은 크기가 커서 유지관리자가 현실적으로 검토하기 어렵고, Laravel에 악의적인 코드를 주입하는 수단으로 악용될 수 있습니다. 이를 예방하기 위해 컴파일된 파일은 Laravel 유지관리자가 직접 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점 (Security Vulnerabilities)

Laravel 내에서 보안 취약점을 발견하면, <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내 알려주세요. 모든 보안 취약점은 신속히 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일 (Coding Style)

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 유효한 Laravel 문서 블록 예시입니다. `@param` 태그 뒤에는 두 칸의 공백이 오며, 인수 타입, 다시 두 칸 공백, 그리고 변수명이 옵니다:

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

네이티브 타입을 사용하는 경우 `@param` 또는 `@return` 속성이 중복되면 삭제할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

하지만 네이티브 타입이 제네릭일 경우, `@param` 또는 `@return`을 사용하여 제네릭 타입을 명시하세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트 병합 후 Laravel 저장소에 자동으로 스타일 수정을 병합합니다. 이를 통해 기여 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령 (Code of Conduct)

Laravel 행동 강령은 Ruby 행동 강령을 바탕으로 합니다. 행동 강령 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 반대 의견에 대해 관용을 가져야 합니다.
- 참여자는 언어와 행동에서 개인 공격과 모욕적인 발언을 삼가야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의로 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행위는 용납되지 않습니다.

</div>