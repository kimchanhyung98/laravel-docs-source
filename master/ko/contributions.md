# 기여 가이드

- [버그 리포트](#bug-reports)
- [지원 문의](#support-questions)
- [핵심 개발 논의](#core-development-discussion)
- [어떤 브랜치에 기여해야 하나요?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

적극적인 협업을 장려하기 위해 Laravel은 단순한 버그 리포트뿐만 아니라 풀 리퀘스트(Pull Request) 제출을 강력히 권장합니다. 풀 리퀘스트는 "검토 준비 완료(ready for review)"로 표시되어야(즉 "draft" 상태가 아니어야) 검토되며, 새로운 기능에 대한 모든 테스트가 통과해야 합니다. "draft" 상태로 남아 비활성화된 풀 리퀘스트는 며칠 후에 닫힙니다.

하지만 버그 리포트를 작성하는 경우, 이슈에는 제목과 명확한 설명이 포함되어야 합니다. 그리고 가능한 한 많은 관련 정보와 문제를 재현할 수 있는 코드 예제를 첨부해 주세요. 버그 리포트의 목적은 본인과 다른 사람들이 버그를 쉽게 재현하고 수정할 수 있도록 하는 데 있습니다.

버그 리포트는 같은 문제를 겪는 다른 사람들이 해결에 협업할 수 있도록 하는 취지로 작성됩니다. 버그 리포트가 자동으로 수정되거나 즉시 반영될 것이라고 기대하지 마세요. 버그 리포트를 생성하는 것은 자신의 문제 해결을 위한 출발점이며, 여러분과 다른 이들에게 도움이 됩니다. 기여를 희망한다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중 하나를 직접 수정하는 것도 좋습니다. 모든 이슈를 보려면 GitHub에 로그인해야 합니다.

Laravel을 사용하는 과정에서 잘못된 DocBlock, PHPStan, IDE 경고 등을 발견했다면 GitHub 이슈를 생성하지 말고, 대신 해당 문제를 수정하는 풀 리퀘스트를 제출해 주세요.

Laravel 소스 코드는 GitHub에서 관리되며, 각 프로젝트별 저장소가 존재합니다:

<div class="content-list" markdown="1">

- [Laravel 애플리케이션](https://github.com/laravel/laravel)
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
- [Laravel Livewire 시작 키트](https://github.com/laravel/livewire-starter-kit)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel React 시작 키트](https://github.com/laravel/react-starter-kit)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Vue 시작 키트](https://github.com/laravel/vue-starter-kit)
- [Laravel 공식 웹사이트](https://github.com/laravel/laravel.com)

</div>

<a name="support-questions"></a>
## 지원 문의

Laravel의 GitHub 이슈 트래커는 Laravel 도움이나 지원을 받기 위한 용도가 아닙니다. 대신 아래 공식 채널을 이용해 주세요:

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
## 핵심 개발 논의

Laravel의 새로운 기능이나 기존 동작 개선을 제안하려면 Laravel 프레임워크 저장소의 [GitHub 토론 게시판](https://github.com/laravel/framework/discussions)에 올릴 수 있습니다. 새 기능을 제안한다면, 해당 기능을 완성하기 위한 일부 코드 작성에도 직접 참여할 의사가 있으면 좋습니다.

버그, 새 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자 Taylor Otwell은 평일 오전 8시~오후 5시(UTC-06:00 또는 미국/시카고 기준) 사이에는 주로 채널에 있으며, 기타 시간대에도 가끔 접속합니다.

<a name="which-branch"></a>
## 어떤 브랜치에 기여해야 하나요?

**모든** 버그 픽스는 최신 버그 픽스 지원 버전(현재는 `12.x`) 브랜치로 보내야 합니다. 버그 픽스는 다가오는 릴리스에만 존재하는 기능을 고치는 경우를 제외하고 **절대** `master` 브랜치로 보내지 마세요.

**완전히 이전 버전과 호환되는** **마이너** 기능 추가는 최신 안정 브랜치(현재는 `12.x`)로 보내도 됩니다.

**주요** 신규 기능 혹은 호환성을 깨는 변경(major breaking change)은 반드시 다가오는 릴리스가 반영되는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산

`laravel/laravel` 저장소 내 `resources/css` 또는 `resources/js` 등과 같이 컴파일 파일에 영향을 주는 변경 사항을 제출할 경우, 컴파일된 파일을 커밋하지 마세요. 크기가 커서 유지관리자가 실제로 검토할 수 없으므로, 이를 악용해 악성 코드를 Laravel에 주입할 가능성이 있습니다. 이를 방지하기 위해, 모든 컴파일된 파일은 Laravel 유지관리자가 생성 및 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견하면, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내주세요. 모든 보안 취약점은 신속히 대응합니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

아래는 올바른 Laravel 주석 블록(PHPDoc) 예시입니다. `@param` 속성 뒤에는 두 칸의 공백, 인자 타입, 다시 두 칸의 공백, 변수명이 옵니다:

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

`@param` 또는 `@return` 속성이 네이티브 타입으로 이미 명확해진 경우, 주석에서 생략 가능합니다:

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

단, 네이티브 타입이 제네릭일 경우 `@param` 또는 `@return` 속성에서 제네릭 타입을 명시해 주세요:

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

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 풀 리퀘스트 병합 이후 자동으로 스타일을 맞춰줍니다. 덕분에 우리는 기여 코드의 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반 시 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다:

<div class="content-list" markdown="1">

- 참가자는 서로 상반된 견해에 대해 관용적으로 대해야 합니다.
- 참가자는 언어 및 행동에서 인신공격이나 비방을 하지 않아야 합니다.
- 타인의 말과 행동을 해석할 때는 항상 선의로 받아들여야 합니다.
- 괴롭힘(harassment)으로 간주될 수 있는 행동은 허용되지 않습니다.

</div>