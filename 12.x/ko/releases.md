# 릴리즈 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 체계

라라벨과 그 외 공식 패키지들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)을 따릅니다. 주요 프레임워크 버전은 매년(보통 1분기경)에 출시되며, 마이너 및 패치 버전은 매주와 같이 더 자주 출시될 수 있습니다. 마이너 버전과 패치 버전은 **절대로** 파괴적인 변경을 포함해서는 안 됩니다.

애플리케이션이나 패키지에서 라라벨 프레임워크 또는 그 컴포넌트를 참조할 때에는 항상 `^12.0`과 같은 버전 제약을 사용하는 것이 좋습니다. 라라벨의 주요 릴리즈에는 파괴적인 변경이 포함될 수 있기 때문입니다. 그러나 라라벨 팀은 항상 하루 이내에 새 주요 버전으로 업그레이드할 수 있도록 최대한 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수

[명명된 인수(named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 라라벨의 하위 호환성(backwards compatibility) 정책에 포함되지 않습니다. 라라벨 코드베이스 품질 향상을 위해, 필요시 함수 인수명을 변경하는 경우가 있습니다. 따라서 라라벨 메서드를 호출할 때 명명된 인수를 사용하는 경우, 앞으로 파라미터 이름이 변경될 수 있다는 점을 유념하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 라라벨 릴리즈는 버그 수정이 18개월 동안, 보안 수정이 2년간 제공됩니다. Lumen을 비롯한 모든 추가 라이브러리의 경우, 오직 최신 주요 버전만이 버그 수정을 받습니다. 또한, 라라벨이 지원하는 데이터베이스 버전에 대해서는 [관련 문서](/docs/12.x/database#introduction)를 참고하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 지원 종료일 | 보안 수정 지원 종료일 |
| --- | --- | --- | --- | --- |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |
| 13 | 8.3 - 8.4 | 2026년 1분기 | 2027년 3분기 | 2028년 1분기 |

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

라라벨 12는 라라벨 11.x에서 이루어진 개선사항을 이어받아 상위 종속성을 업데이트하고, React, Vue, Livewire를 위한 새로운 스타터 킷을 도입했습니다. 여기에는 사용자 인증을 위한 [WorkOS AuthKit](https://authkit.com) 옵션도 포함됩니다. WorkOS 기반의 스타터 킷에서는 소셜 인증, 패스키, SSO(Single Sign-On)를 지원합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 파괴적 변경

이번 릴리즈 사이클에서 핵심적으로 초점을 맞춘 부분은 파괴적인 변경을 최소화하는 것이었습니다. 대신, 이미 존재하는 애플리케이션에 영향을 주지 않으면서 연중 내내 지속적인 생산성 향상(quality-of-life) 개선사항을 제공하는 데 집중했습니다.

따라서 라라벨 12 릴리즈는 기존 의존성 업그레이드를 위한 비교적 소규모의 '유지보수 릴리즈'입니다. 이러한 이유로, 대부분의 라라벨 애플리케이션은 코드 변경 없이도 라라벨 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 킷

라라벨 12는 React, Vue, Livewire를 위한 새로운 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 도입했습니다. React와 Vue 스타터 킷은 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하며, Livewire 스타터 킷은 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Vue, Livewire 스타터 킷 모두 라라벨의 내장 인증 시스템을 통해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 또한, 각각의 스타터 킷에는 [WorkOS AuthKit 기반](https://authkit.com) 버전도 추가되어, 소셜 로그인, 패스키, SSO 기능을 지원합니다. WorkOS를 이용하면 월 100만 활성 사용자까지 무료 인증 서비스를 제공합니다.

새로운 애플리케이션 스타터 킷의 도입에 따라, 기존의 Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.

새로운 스타터 킷으로 시작하려면 [스타터 킷 문서](/docs/12.x/starter-kits)를 참고하시기 바랍니다.
