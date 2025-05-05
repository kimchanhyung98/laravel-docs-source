# 릴리즈 노트

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 정책

라라벨과 그 외 공식 패키지들은 [Semantic Versioning(시맨틱 버저닝)](https://semver.org)을 따릅니다. 주요 프레임워크 릴리즈는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리즈는 매주라도 배포될 수 있습니다. 마이너 및 패치 릴리즈에는 절대적으로 **호환성이 깨지는 변경 사항이 포함되지 않아야 합니다.**

애플리케이션이나 패키지에서 라라벨 프레임워크 또는 그 구성요소를 참조할 때는, `^12.0`과 같은 버전 제약자를 항상 사용해야 합니다. 이는 라라벨의 주요 릴리즈에는 호환성에 영향을 줄 수 있는 변경 사항이 포함되기 때문입니다. 그러나, 저희는 사용자가 하루 이내에 주요 릴리즈로 업그레이드할 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 아규먼트(명명된 인자)

[네임드 아규먼트(명명된 인자)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 라라벨의 하위 호환성 지침에 포함되지 않습니다. 라라벨 코드베이스 개선을 위해 필요할 경우 함수 인자 이름을 변경할 수 있습니다. 따라서, 라라벨 메서드를 호출할 때 네임드 아규먼트 사용은 주의해서 하고, 향후 인자명이 변경될 수 있음을 인지해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 라라벨 릴리즈는 버그 수정이 18개월간, 보안 수정이 2년간 제공됩니다. Lumen을 포함한 기타 모든 추가 라이브러리는 오직 최신 메이저 릴리즈만 버그 수정을 받습니다. 또한, 라라벨에서 [지원하는 데이터베이스 버전](/docs/{{version}}/database#introduction)도 참고해 주세요.

<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 종료일 | 보안 수정 종료일 |
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
        <div>보안 수정만 제공</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## 라라벨 12

라라벨 12는 상위 의존성 업데이트와 React, Vue, Livewire를 위한 새로운 스타터 키트 도입 등 11.x에서의 개선을 이어갑니다. 사용자 인증을 위해 [WorkOS AuthKit](https://authkit.com)을 활용할 수 있는 옵션도 함께 제공합니다. WorkOS 버전의 스타터 키트는 소셜 인증, 패스키, SSO 지원을 포함합니다.

<a name="minimal-breaking-changes"></a>
### 최소화된 호환성 파괴 변경

이번 릴리즈 주기의 많은 부분은 호환성 파괴 변경을 최소화하는 데 집중했습니다. 그 대신, 기존 애플리케이션을 깨뜨리지 않는 다양한 품질 개선을 연중 지속적으로 제공하고자 노력했습니다.

이에 따라 라라벨 12 릴리즈는 기존 의존성 업그레이드를 위한 비교적 소규모의 "유지보수 릴리즈"입니다. 이러한 점을 고려하면, 대부분의 라라벨 애플리케이션은 별도의 코드 변경 없이 라라벨 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 신규 애플리케이션 스타터 키트

라라벨 12에서는 React, Vue, Livewire를 위한 새로운 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 도입했습니다. React 및 Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 사용하며, Livewire 스타터 키트는 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

이 모든 스타터 키트는 라라벨의 내장 인증 시스템을 활용해 로그인, 회원가입, 비밀번호 초기화, 이메일 인증 등 기능을 제공합니다. 또한, 각 스타터 키트의 [WorkOS AuthKit 기반](https://authkit.com) 버전을 새롭게 도입하여, 소셜 인증, 패스키, SSO 지원을 제공합니다. WorkOS는 월간 활성 사용자 100만 명까지 무료 인증 서비스를 제공합니다.

새로운 애플리케이션 스타터 키트 도입으로, Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트를 제공하지 않습니다.

새 스타터 키트로 시작하려면 [스타터 키트 문서](/docs/{{version}}/starter-kits)를 참고하세요.