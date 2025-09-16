# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치에 기여해야 하나?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

Laravel에서는 적극적인 협업을 장려하기 위해, 버그 리포트뿐 아니라 pull request(풀 리퀘스트) 제출을 강력히 권장합니다. 풀 리퀘스트는 "ready for review"(검토 준비 완료) 상태로 표시되고(즉, "draft" 상태가 아님), 새로운 기능의 모든 테스트가 통과할 때만 리뷰가 진행됩니다. "draft"(초안) 상태에서 오랫동안 비활성 상태로 남아 있는 풀 리퀘스트는 며칠 후 자동으로 닫힙니다.

만약 버그 리포트를 작성할 경우, 이슈에는 제목과 함께 해당 문제에 대한 명확한 설명이 포함되어야 합니다. 또한, 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 예시를 포함해 주시기 바랍니다. 버그 리포트의 목적은 자신과 다른 사용자가 해당 버그를 쉽게 재현하고, 해결책을 마련할 수 있도록 돕는 것입니다.

버그 리포트는 동일한 문제를 겪는 다른 사용자가 협력하여 함께 문제를 해결하기 위한 목적으로 만들어집니다. 버그 리포트 작성만으로 자동으로 활동이 이루어지거나, 다른 사람이 즉시 해결해줄 것이라고 기대해서는 안 됩니다. 버그 리포트 작성은 문제 해결의 첫걸음을 내딛는 과정입니다. 더욱 적극적으로 참여하고 싶다면, [이슈 트래커에 등재된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 직접 해결하는 데에도 참여할 수 있습니다. Laravel의 모든 이슈를 확인하려면 GitHub에 로그인되어 있어야 합니다.

Laravel을 사용하면서 DocBlock, PHPStan, 혹은 IDE 경고가 잘못된 것을 발견했다면, GitHub 이슈를 생성하지 말고, 문제를 수정하는 풀 리퀘스트를 제출해 주시기 바랍니다.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별로 별도의 저장소가 존재합니다:

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
## 지원 질문

Laravel의 GitHub 이슈 트래커는 Laravel 관련 지원이나 도움을 받기 위한 공간이 아닙니다. 대신 아래 채널 중 하나를 이용해 질문해 주세요:

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

Laravel의 새로운 기능 제안이나 기존 동작의 개선 사항은 Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에 올릴 수 있습니다. 새로운 기능을 제안하는 경우, 해당 기능을 구현하는 코드 중 일부라도 직접 작성할 의사가 있어야 합니다.

버그, 신규 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이뤄집니다. Laravel의 메인테이너인 Taylor Otwell은 평일(UTC-06:00 또는 America/Chicago 기준) 오전 8시부터 오후 5시 사이에는 채널에 주로 상주하며, 그 외 시간대에도 간헐적으로 접속합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여해야 하나?

**모든** 버그 수정은 버그 수정이 지원되는 최신 버전(현재는 `12.x`)의 브랜치로 보내야 합니다. 버그 수정은 앞으로 출시될 기능만 있는 경우가 아니라면, `master` 브랜치로 절대 보내지 마십시오.

**완전히 하위 호환**되는 **마이너 기능**은 최신 안정 버전 브랜치(현재는 `12.x`)에 기여할 수 있습니다.

**주요 신규 기능**이나 **호환성이 깨지는 변경사항**은 항상 `master` 브랜치(차기 릴리스가 진행 중인 브랜치)에 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등 컴파일된 파일에 영향을 주는 변경사항을 제출하는 경우, 컴파일된 파일은 커밋하지 마십시오. 컴파일된 파일 용량이 커서 메인테이너가 검토하는 것이 실질적으로 어렵고, 이를 악용해 악성 코드를 Laravel에 삽입할 수 있기 때문입니다. 이를 방지하기 위해, 모든 컴파일 파일은 Laravel 메인테이너가 직접 생성하여 커밋하게 되어 있습니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견한 경우, <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 Taylor Otwell에게 이메일을 보내 주시기 바랍니다. 발견된 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 유효한 Laravel 문서 블록의 예시입니다. `@param` 속성 뒤에 두 칸의 공백, 인수 타입, 두 칸의 공백, 그리고 변수명이 오는 것을 확인할 수 있습니다:

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

만약 네이티브 타입 명시로 인해 `@param` 또는 `@return` 속성이 중복된다면, 해당 속성은 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

그러나 네이티브 타입이 제네릭일 경우, `@param` 또는 `@return` 속성을 통해 제네릭 타입을 명확히 기입해야 합니다:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 이후 자동으로 코드 스타일을 정리해줍니다. 우리는 기여 내용 자체에 집중할 수 있도록 코드 스타일에 대한 부담을 줄이고 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 Ruby 행동 강령을 기반으로 합니다. 행동 강령 위반 사항은 Taylor Otwell (taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참여자는 자신과 반대되는 의견에도 관용을 가져야 합니다.
- 참여자는 개인을 공격하거나, 비방하는 언행을 해서는 안 됩니다.
- 타인의 언행을 해석할 때 항상 선의로 받아들여야 합니다.
- 괴롭힘으로 간주될 수 있는 행동은 어떠한 경우에도 허용되지 않습니다.

</div>
