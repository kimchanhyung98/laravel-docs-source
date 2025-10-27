# 기여 가이드 (Contribution Guide)

- [버그 신고](#bug-reports)
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
## 버그 신고

Laravel은 적극적인 협업을 장려하기 위해 단순한 버그 신고뿐만 아니라 pull request(풀 리퀘스트)를 통한 기여를 강하게 권장합니다. pull request는 "ready for review"(검토 대기) 상태로 표시되어 있어야 하며(즉, "draft" 상태가 아니어야 함), 새 기능을 위한 모든 테스트가 통과해야만 검토됩니다. "draft" 상태로 남아있으며 비활성화된 pull request는 며칠 후 자동으로 닫힙니다.

그러나, 버그를 신고하려면 이슈에는 제목과 명확한 문제 설명이 포함되어야 합니다. 또한 최대한 관련 정보와 문제를 재현할 수 있는 코드 예제를 함께 알려주셔야 합니다. 버그 신고의 목적은 버그를 쉽고 명확하게 재현할 수 있게 하여 본인과 다른 사람이 문제를 해결해 나갈 수 있도록 돕는 데 있습니다.

버그 신고는 동일한 문제를 겪는 다른 사람들이 함께 해결책을 찾기 위해 작성된다는 점을 명심하십시오. 버그를 신고했다고 해서 자동으로 처리되거나 누군가가 바로 고쳐주리라고 기대하지 마십시오. 버그 신고는 문제 해결의 첫 걸음을 뗄 수 있도록 본인과 다른 기여자들에게 도움을 주는 것입니다. 추가로 기여하고 싶다면, [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중 자유롭게 고치는 것도 가능합니다. 모든 Laravel 이슈를 보려면 GitHub에 인증되어 있어야 합니다.

Laravel을 사용하다가 DocBlock, PHPStan, IDE 경고와 관련된 오타나 오류를 발견하셨다면 GitHub 이슈를 생성하지 말고, 문제를 직접 고쳐서 pull request로 제출해 주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트마다 별도의 저장소가 있습니다:

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Boost](https://github.com/laravel/boost)
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

Laravel의 GitHub 이슈 트래커는 Laravel 사용법이나 기술 지원을 제공하는 용도가 아닙니다. 지원이 필요하다면 아래 채널 중 하나를 이용해 주세요.

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

새로운 기능 제안이나 기존 Laravel 동작에 대한 개선점을 논의하려면, Laravel 프레임워크 저장소의 [GitHub Discussion 보드](https://github.com/laravel/framework/discussions)를 이용하십시오. 만약 새로운 기능을 제안한다면, 그 기능을 완성하는 데 필요한 코드의 일부라도 직접 구현할 의향이 있어야 합니다.

버그, 신규 기능, 기존 기능 구현 등에 관한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel) 내 `#internals` 채널에서 진행됩니다. Laravel의 메인테이너인 Taylor Otwell은 평일 08:00~17:00 (UTC-06:00 또는 America/Chicago)에 보통 채널에 상주하며, 그 외 시간에도 간헐적으로 참석합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여해야 하나?

**모든** 버그 수정은 현재 버그 수정이 지원되는 최신 버전(`12.x`) 브랜치로 보내야 합니다. 버그 수정은 **절대로** `master` 브랜치로 보내서는 안 되며, 다만 앞으로 릴리즈될 기능만 포함하는 경우에는 해당 기능이 존재하는 브랜치에만 보내야 합니다.

**완벽하게 하위 호환되는** **소규모** 신규 기능은 최신 안정 브랜치(현재는 `12.x`)로 보내도 됩니다.

**대규모** 신규 기능 또는 호환성이 깨지는 변경이 포함된 기능은 항상 `master` 브랜치(차기 릴리즈용 브랜치)로만 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등과 같이, 컴파일된 파일에 영향을 주는 변경 사항을 제출할 경우 컴파일된 파일 자체는 커밋하지 마십시오. 컴파일된 파일은 용량이 커서 메인테이너가 실질적으로 리뷰할 수 없습니다. 이는 악성 코드를 Laravel에 주입하는 데 악용될 수 있으므로, 모든 컴파일 에셋은 Laravel 메인테이너가 직접 생성 후 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견할 경우 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 Taylor Otwell에게 이메일을 보내주십시오. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 문서 블록 예시입니다. `@param` 속성 뒤에는 두 칸의 공백, 인수 타입, 다시 두 칸의 공백, 마지막으로 변수명이 나옵니다:

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

`@param` 이나 `@return` 속성이 네이티브 타입으로 충분히 표현될 경우에는 생략할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

단, 네이티브 타입이 제네릭(generic)인 경우에는 `@param` 또는 `@return` 속성을 통해 반드시 제네릭 타입을 명시해야 합니다:

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

코드 스타일이 완벽하지 않아도 걱정하지 마십시오! [StyleCI](https://styleci.io/)가 pull request가 병합된 이후 자동으로 코드 스타일 문제를 수정해 줍니다. 따라서 기여 내용 그 자체에 더 집중하실 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령(Code of Conduct)은 Ruby의 행동 강령에서 파생되었습니다. 행동 강령 위반 사례는 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 반대 의견에 대해 관용적으로 대해야 합니다.
- 참가자는 언어나 행동에서 개인 공격, 비방성 발언을 삼가야 합니다.
- 타인의 말과 행동을 해석할 때는 언제나 선의로 가정해야 합니다.
- 합리적으로 괴롭힘이라고 판단될 수 있는 행동은 용납되지 않습니다.

</div>
