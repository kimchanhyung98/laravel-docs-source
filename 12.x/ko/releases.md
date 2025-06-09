# 릴리즈 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 체계

라라벨과 라라벨의 공식 패키지들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)을 따릅니다. 주요 프레임워크 릴리즈(major release)는 매년 1분기(Q1) 즈음에 공개되며, 마이너(minor)와 패치(patch) 릴리즈는 매주와 같은 짧은 주기로도 배포될 수 있습니다. 마이너 및 패치 릴리즈에서는 **절대로** 호환성을 깨는 변경(breaking changes)이 포함되지 않아야 합니다.

애플리케이션이나 패키지에서 라라벨 프레임워크 또는 그 컴포넌트를 참조할 때에는 항상 `^12.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. 이는 라라벨의 주요 버전이 업그레이드될 때는 호환성에 영향을 주는 변경이 포함될 수 있기 때문입니다. 그러나 라라벨 팀은 가능한 한 하루 이내로 새 주요 버전으로 업그레이드할 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수(Named Arguments)

[명명된 인수](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 라라벨의 하위 호환성 보장 정책에 포함되지 않습니다. 라라벨 코드의 품질을 위해 필요하다면 함수 인수 이름을 변경할 수 있습니다. 따라서 라라벨 메서드를 호출할 때 명명된 인수를 사용할 경우, 향후 인자명 변경 가능성을 염두에 두고 신중히 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 라라벨 버전은 출시 후 18개월 동안 버그 수정, 2년 동안 보안 패치를 지원합니다. 라라벨의 공식 라이브러리들은 오직 최신 주요 버전만 버그 수정을 받습니다. 또한, 라라벨이 지원하는 데이터베이스 종류에 대해서는 [데이터베이스 지원 문서](/docs/12.x/database#introduction)를 참고하시기 바랍니다.

<div class="overflow-auto">

| Version | PHP (*)   | Release             | Bug Fixes Until     | Security Fixes Until |
| ------- | --------- | ------------------- | ------------------- | -------------------- |
| 10      | 8.1 - 8.3 | February 14th, 2023 | August 6th, 2024    | February 4th, 2025   |
| 11      | 8.2 - 8.4 | March 12th, 2024    | September 3rd, 2025 | March 12th, 2026     |
| 12      | 8.2 - 8.4 | February 24th, 2025 | August 13th, 2026   | February 24th, 2027  |
| 13      | 8.3 - 8.4 | Q1 2026             | Q3 2027             | Q1 2028              |

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
## 라라벨 12

라라벨 12는 라라벨 11.x에서 도입된 개선 사항을 이어받아, 업스트림(상위) 의존성 업데이트와 함께 React, Vue, Livewire용 신규 스타터 키트를 제공합니다. 또한 사용자 인증에 [WorkOS AuthKit](https://authkit.com) 사용 옵션도 추가되었습니다. WorkOS 기반의 스타터 키트에서는 소셜 로그인, 패스키(passkey), SSO(Single Sign-On) 기능을 지원합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 변경(호환성 유지)

이번 릴리즈에서는 기존과의 호환성을 최대한 유지하는 데 집중했습니다. 대신, 연중 지속적으로 기존 애플리케이션에 영향을 미치지 않는 다양한 품질 개선 작업에 힘썼습니다.

이러한 이유로 라라벨 12는 주로 의존성 업그레이드에 중점을 둔 비교적 소규모의 "유지보수 릴리즈"입니다. 대부분의 라라벨 애플리케이션들은 코드 변경 없이도 라라벨 12로 업그레이드가 가능합니다.

<a name="new-application-starter-kits"></a>
### 신규 애플리케이션 스타터 키트

라라벨 12에서는 React, Vue, Livewire를 위한 새로운 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)가 도입되었습니다. React와 Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하며, Livewire 스타터 키트는 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Vue, Livewire 스타터 키트는 모두 라라벨의 내장 인증 시스템을 활용해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 추가로 각 스타터 키트에는 [WorkOS AuthKit](https://authkit.com)을 기반으로 한 버전이 제공되어, 소셜 인증, 패스키, SSO 기능을 지원합니다. WorkOS는 한 달 기준 100만 명의 활성 사용자까지는 무료 인증 서비스를 제공합니다.

이 새로운 스타터 키트가 도입됨에 따라, 이제 Laravel Breeze 및 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.

새로운 스타터 키트를 사용하려면 [스타터 키트 문서](/docs/12.x/starter-kits)를 참고해 주세요.