# 기여 가이드

- [버그 제보](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치에?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 제보

Laravel은 적극적인 협업을 장려하기 위해 단순한 버그 리포트뿐만 아니라 풀 리퀘스트(pull request) 제출을 강력하게 권장합니다. 풀 리퀘스트는 "검토 준비 완료(ready for review)"로 표시되고(즉, "초안(draft)" 상태가 아니며) 새로운 기능을 위한 모든 테스트가 통과할 때만 검토됩니다. "초안" 상태로 남아있는 비활성 풀 리퀘스트는 며칠 후에 닫힐 수 있습니다.

그러나 버그 리포트를 작성하는 경우, 제목과 이슈에 대한 명확한 설명을 반드시 담아야 하며, 가능한 많은 관련 정보와 함께 문제를 재현할 수 있는 코드 샘플을 포함해야 합니다. 버그 리포트의 목적은 여러분과 다른 사람들이 버그를 쉽게 재현하고 수정할 수 있도록 하는 것입니다.

버그 리포트는 같은 문제를 가진 다른 사람들이 함께 해결할 수 있기를 바라는 마음으로 작성되는 것임을 기억하세요. 버그 리포트에 자동으로 활동이 붙거나 누군가 즉시 고쳐줄 것이라고 기대하지 마세요. 버그 리포트 작성은 본인과 타인이 문제 해결의 첫걸음을 떼는 데에 도움이 됩니다. 혹시 기여하고 싶다면, [이슈 트래커에 등록된 버그들](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중에서 직접 수정해볼 수 있습니다. Laravel의 이슈 전체를 보려면 GitHub에 인증되어 있어야 합니다.

Laravel을 사용하면서 잘못된 DocBlock, PHPStan, IDE 경고 등을 발견했다면 GitHub 이슈를 만들지 말고, 해당 문제를 수정하는 풀 리퀘스트를 제출해 주세요.

Laravel의 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별로 별도 저장소가 있습니다:

<div class="content-list" markdown="1">

- [Laravel 어플리케이션](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel 문서](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel 프레임워크](https://github.com/laravel/framework)
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

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 Laravel 사용 지원을 위한 곳이 아닙니다. 지원 또는 질문이 있는 경우, 아래 채널 중 하나를 이용해 주세요:

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

Laravel 프레임워크 저장소의 [GitHub Discussion 게시판](https://github.com/laravel/framework/discussions)에서 새로운 기능이나 기존 Laravel 동작의 개선안을 제안할 수 있습니다. 새로운 기능을 제안하는 경우, 해당 기능을 완성하는 데 필요한 코드 중 일부라도 직접 구현할 의사가 있어야 합니다.

버그, 신규 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel 메인테이너인 Taylor Otwell은 평일 오전 8시부터 오후 5시(UTC-06:00, 미국 시카고 기준)까지 주로 이 채널에서 활동하며, 그 외 시간에도 가끔 존재합니다.

<a name="which-branch"></a>
## 어떤 브랜치에?

**모든** 버그 수정은 현재 버그 픽스를 지원하는 최신 버전(현재는 `12.x`) 브랜치로 보내야 합니다. 버그 수정은 **절대** `master` 브랜치로 보내지 마세요. 단, 곧 출시될 새 버전에만 존재하는 기능을 수정하는 경우는 예외입니다.

**완전히 이전 버전과 호환되는** 소규모 기능의 추가는 최신 안정 브랜치(현재는 `12.x`)에 기여할 수 있습니다.

**주요 신규 기능** 또는 **호환성에 영향을 주는 변경 사항**은 항상 출시 예정인 버전의 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css`나 `resources/js`와 같이 컴파일된 파일에 영향을 주는 변경을 제출할 때에는, *컴파일된 파일은 커밋하지 마세요*. 용량이 크기 때문에 메인테이너가 꼼꼼히 리뷰할 수 없으며, 이는 악성 코드를 삽입하는 수단으로 악용될 소지가 있습니다. 이를 방지하기 위해, 모든 컴파일된 파일은 Laravel 메인테이너에 의해 생성 및 커밋됩니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견했다면, <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 Taylor Otwell에게 이메일을 보내주세요. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

다음은 올바른 Laravel 문서 블록(PHPDoc) 예시입니다. `@param` 속성 뒤에는 두 칸 띄우기가 들어가고, 인자 타입, 두 칸 띄우기, 그 다음 변수명이 옵니다:

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

네이티브 타입 덕분에 `@param` 또는 `@return` 어노테이션이 중복될 경우, 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

그러나 네이티브 타입이 제네릭일 경우, 반드시 `@param` 또는 `@return` 어노테이션을 통해 제네릭 타입을 명시해야 합니다:

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

코드 스타일에 너무 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 머지된 이후에 자동으로 Laravel 저장소에 스타일 수정을 머지해줍니다. 덕분에 우리는 코드 스타일보다 기여 내용 자체에 더 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령(Code of Conduct)은 Ruby의 행동 강령에서 파생되었습니다. 행동 강령 위반이 있을 경우 Taylor Otwell(taylor@laravel.com)에게 신고해 주세요:

<div class="content-list" markdown="1">

- 참가자는 서로 다른 견해에 대해 관용을 가져야 합니다.
- 참가자는 언행이 개인에 대한 공격이나 비방이 되지 않도록 신경써야 합니다.
- 타인의 언행을 해석할 때에는 항상 선의로 받아들여야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 어떠한 경우에도 허용되지 않습니다.

</div>