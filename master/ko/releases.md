# 릴리즈 노트 (Release Notes)

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 정책 (Versioning Scheme)

Laravel과 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 버전은 매년(대략 1분기)에 릴리즈되며, 마이너 및 패치 릴리즈는 주 단위로 자주 배포될 수 있습니다. 마이너 및 패치 릴리즈에는 **절대** 파괴적 변경 사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 혹은 그 컴포넌트를 참조할 때는 항상 `^12.0`과 같은 버전 제약을 사용해야 합니다. 주요 릴리즈는 파괴적 변경을 포함할 수 있기 때문입니다. 그러나 Laravel은 항상 새 주요 릴리즈로 하루 이내에 안전하게 업데이트할 수 있도록 노력하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트 (Named Arguments)

[네임드 아규먼트](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스 개선을 위해 필요할 경우 함수 아규먼트명이 변경될 수 있으므로, Laravel 메서드를 호출할 때 네임드 아규먼트를 사용할 경우 추후 파라미터 이름 변경 가능성을 염두에 두고 신중히 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈에 대해 버그 수정은 18개월간 제공되며 보안 패치는 2년간 지원됩니다. Lumen을 포함한 추가 라이브러리는 최신 주요 릴리즈에 대해서만 버그 수정을 받습니다. 또한, Laravel에서 지원하는 데이터베이스 버전도 반드시 확인하시기 바랍니다. ([지원 데이터베이스 버전](/docs/master/database#introduction))

<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 지원 종료 | 보안 패치 지원 종료 |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>End of life</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>Security fixes only</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 Laravel 11.x에서 진행된 개선 사항을 이어가며 상위 의존성 패키지를 업데이트하고 React, Vue, Livewire용 신규 스타터 킷을 선보입니다. 이와 함께 사용자인증을 위해 [WorkOS AuthKit](https://authkit.com)을 사용하는 옵션도 포함되어 있습니다. WorkOS 기반 스타터 킷은 소셜 인증, 패스키, SSO(싱글 사인온)를 지원합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 파괴적 변경

이번 릴리즈 주기 동안 가장 중점을 둔 부분은 파괴적 변경 최소화입니다. 대신, 기존 애플리케이션을 깨뜨리지 않는 연속적인 품질 개선에 집중해 왔습니다.

따라서 Laravel 12는 기존 의존성 업그레이드를 위한 비교적 사소한 “유지 보수 릴리즈”로 분류됩니다. 이 때문에 대부분의 Laravel 애플리케이션은 애플리케이션 코드 변경 없이 Laravel 12로 안전하게 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 킷

Laravel 12는 React, Vue, Livewire용 새로운 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 도입했습니다. React와 Vue 스타터 킷은 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 사용하며, Livewire 스타터 킷은 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 활용합니다.

이 스타터 킷들은 모두 Laravel 내장 인증 시스템을 사용해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 제공합니다. 추가로, 각각의 스타터 킷에는 소셜 인증, 패스키, SSO를 지원하는 [WorkOS AuthKit 기반](https://authkit.com) 변형도 포함되어 있습니다. WorkOS는 월 100만 명 이하 활성 사용자 애플리케이션에 대해 무료 인증 서비스를 제공합니다.

새로운 스타터 킷 도입에 따라 Laravel Breeze와 Laravel Jetstream은 더 이상 업데이트되지 않습니다.

새 스타터 킷 시작법은 [스타터 킷 문서](/docs/master/starter-kits)를 참고하세요.