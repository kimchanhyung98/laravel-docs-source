# 릴리즈 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 체계 (Versioning Scheme)

Laravel과 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 메이저 프레임워크 릴리즈는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리즈는 매주 같이 자주 출시될 수 있습니다. 마이너 및 패치 릴리즈에는 절대로 파괴적 변경사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크나 그 구성요소를 참조할 때는 메이저 릴리즈에 파괴적 변경이 포함되므로 항상 `^12.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. 그러나 저희는 새로운 메이저 버전으로의 업데이트를 하루 이내로 완료할 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트 (Named Arguments)

[네임드 아규먼트](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스 품질 개선을 위해 필요에 따라 함수 인수명이 변경될 수 있으므로, Laravel 메서드 호출 시 네임드 아규먼트 사용은 주의해서 하셔야 하며 미래에 파라미터 이름이 바뀔 수 있음을 염두에 두셔야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈는 버그 수정이 18개월간 제공되며 보안 패치가 2년간 지원됩니다. 부가 라이브러리들은 최신 메이저 릴리즈에 대해서만 버그 수정을 지원합니다. 아울러 Laravel이 지원하는 데이터베이스 버전도 참고하시기 바랍니다.([지원 데이터베이스](/docs/12.x/database#introduction))

<div class="overflow-auto">

| 버전  | PHP (*)   | 출시일             | 버그 수정 지원 종료   | 보안 패치 지원 종료    |
| ------ | --------- | ------------------- | -------------------- | --------------------- |
| 10     | 8.1 - 8.3 | 2023년 2월 14일    | 2024년 8월 6일       | 2025년 2월 4일        |
| 11     | 8.2 - 8.4 | 2024년 3월 12일    | 2025년 9월 3일       | 2026년 3월 12일       |
| 12     | 8.2 - 8.4 | 2025년 2월 24일    | 2026년 8월 13일      | 2027년 2월 24일       |
| 13     | 8.3 - 8.4 | 2026년 1분기       | 2027년 3분기         | 2028년 1분기          |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 패치 전용</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 Laravel 11.x에서 시작된 개선 사항을 이어가며, 상위 의존성을 업데이트하고 React, Vue, Livewire용 새로운 스타터 킷을 도입했습니다. 또한 사용자 인증을 위해 [WorkOS AuthKit](https://authkit.com)을 사용할 수 있는 옵션을 포함하고 있습니다. WorkOS 기반의 스타터 킷에서는 소셜 인증, 패스키(passkeys), SSO(Single Sign-On) 지원도 제공합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 파괴적 변경 (Minimal Breaking Changes)

이번 릴리즈 주기에서 저희는 파괴적 변경을 최대한 줄이는 데 집중했습니다. 대신 기존 애플리케이션을 깨뜨리지 않는 연속적인 품질 개선을 연중 제공하는 데 힘썼습니다.

그 결과, Laravel 12 릴리즈는 상위 의존성 업그레이드를 주목적으로 하는 비교적 작은 "유지 보수 릴리즈"라고 할 수 있습니다. 따라서 대부분의 Laravel 애플리케이션은 애플리케이션 코드 변경 없이 Laravel 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 킷 (New Application Starter Kits)

Laravel 12는 React, Vue, Livewire 용의 새로운 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 도입했습니다. React와 Vue 스타터 킷은 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하며, Livewire 스타터 킷은 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Vue, Livewire 스타터 킷 모두 Laravel 내장 인증 시스템을 이용해 로그인, 회원가입, 비밀번호 재설정, 이메일 검증 등의 기능을 제공합니다. 아울러 각 스타터 킷에는 [WorkOS AuthKit 기반](https://authkit.com) 변형판도 제공되어, 소셜 인증, 패스키, SSO 지원을 함께 포함하고 있습니다. WorkOS는 한 달에 최대 100만 명의 활성 사용자를 위한 무료 인증을 제공합니다.

새로운 애플리케이션 스타터 킷 도입에 따라 Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.

새 스타터 킷을 시작하려면 [스타터 킷 문서](/docs/12.x/starter-kits)를 참고하세요.