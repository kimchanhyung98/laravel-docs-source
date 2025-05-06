# 릴리즈 노트

- [버전 관리 방식](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 방식

Laravel 및 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)(시맨틱 버저닝)을 따릅니다. 주요 프레임워크 릴리즈는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리즈는 매주 출시될 수 있습니다. 마이너 및 패치 릴리즈에는 **절대로** 하위 호환성에 영향을 주는 변경 사항이 포함되지 않아야 합니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 혹은 컴포넌트를 참조할 때는, `^12.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. Laravel의 주요 릴리즈에는 하위 호환성에 영향을 주는 변경이 포함될 수 있기 때문입니다. 하지만, 새로운 주요 릴리즈로 하루 이내에 업데이트할 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트

[네임드 아규먼트](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스의 개선을 위해 필요한 경우 함수의 인자명을 변경할 수 있습니다. 따라서, Laravel 메소드 호출 시 네임드 아규먼트를 사용할 때는 신중히 사용해야 하며, 향후 파라미터 이름이 변경될 수 있다는 점을 염두에 두어야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 Laravel 릴리즈에 대해 버그 수정은 18개월 동안 제공되며, 보안 패치는 2년간 제공됩니다. Lumen을 포함한 추가 라이브러리의 경우, 오직 최신 주요 릴리즈만 버그 수정을 받습니다. 또한, Laravel에서 지원하는 데이터베이스 버전은 [공식 문서](/docs/{{version}}/database#introduction)를 참고하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리즈 | 버그 수정 종료일 | 보안 패치 종료일 |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 패치만 제공</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 상위 의존성 패키지 업데이트 및 React, Vue, Livewire용 신규 스타터 키트 도입 등 Laravel 11.x에서의 개선을 이어갑니다. 신규 키트에는 [WorkOS AuthKit](https://authkit.com)을 이용한 사용자 인증 옵션도 포함되어 있습니다. WorkOS 기반 스타터 키트는 소셜 인증, 패스키, SSO 지원을 제공합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 파괴적 변경

이번 릴리즈에서는 하위 호환성에 영향을 주는 변경을 최소화하는 데 중점을 두었습니다. 그 대신, 연중 기존 애플리케이션에 영향을 주지 않는 지속적인 품질 개선을 제공하는 데 집중했습니다.

따라서, Laravel 12 릴리즈는 기존 의존성 업그레이드를 위한 비교적 소규모의 "유지보수" 릴리즈입니다. 이로 인해 대부분의 Laravel 애플리케이션은 코드 변경 없이도 Laravel 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 신규 애플리케이션 스타터 키트

Laravel 12에서는 React, Vue, Livewire용 신규 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 도입했습니다. React, Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 사용하며, Livewire 스타터 키트는 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 활용합니다.

React, Vue, Livewire 스타터 키트 모두 Laravel의 내장 인증 시스템을 활용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 또한, 각 스타터 키트의 [WorkOS AuthKit 기반](https://authkit.com) 버전을 도입하여 소셜 인증, 패스키, SSO 지원을 제공합니다. WorkOS는 월 100만 명 활동 사용자까지 무료 인증 서비스를 제공합니다.

신규 애플리케이션 스타터 키트가 도입되면서, Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.

새로운 스타터 키트 시작 방법은 [스타터 키트 문서](/docs/{{version}}/starter-kits)를 참고하세요.