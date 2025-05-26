# 릴리스 노트 (Release Notes)

- [버전 관리 방식](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 방식

라라벨과 그 외의 공식 패키지들은 [시맨틱 버전(Semantic Versioning)](https://semver.org)에 따라 버전이 관리됩니다. 프레임워크의 주요(Major) 릴리스는 매년(대략 1분기)에 한 번씩 배포되며, 마이너(Minor) 및 패치(Patch) 릴리스는 필요에 따라 주 단위로 배포될 수 있습니다. 마이너 및 패치 릴리스에서는 기존 기능을 깨뜨리는 변경(breaking changes)이 **절대로** 포함되지 않습니다.

애플리케이션이나 패키지에서 라라벨 프레임워크 또는 그 구성요소를 참조할 때는 `^12.0`과 같은 버전 제약을 사용하는 것이 좋습니다. 이는 라라벨의 주요(Major) 릴리스에 기존과 호환되지 않는 변경이 포함될 수 있기 때문입니다. 하지만 저희는 새로운 주요 릴리스로의 업그레이드를 하루 혹은 그 이하의 시간 안에 할 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수

[명명된 인수(named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 라라벨의 하위 호환성(backwards compatibility) 정책에 포함되지 않습니다. 라라벨 코드 베이스를 개선하기 위해 필요하다면 함수 인수(파라미터)의 이름이 변경될 수 있습니다. 따라서 라라벨 메서드를 호출할 때 명명된 인수를 사용할 경우, 앞으로 인수 이름이 변경될 수 있음을 염두에 두고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 라라벨 릴리스는 18개월 동안 버그 수정, 2년 동안 보안 패치를 제공합니다. 추가 라이브러리의 경우, 오직 최신 주요 릴리스만 버그 수정을 지원합니다. 또한, 라라벨이 [지원하는 데이터베이스 버전](/docs/12.x/database#introduction)도 반드시 확인하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리스 | 버그 수정 지원 종료 | 보안 패치 지원 종료 |
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

(*) 지원하는 PHP 버전

<a name="laravel-12"></a>
## 라라벨 12

라라벨 12는 상위 의존성 패키지의 최신화와 함께 React, Vue, Livewire를 위한 신규 스타터 킷을 도입하는 등, 라라벨 11.x에서 이루어진 개선 작업을 이어갑니다. 이 스타터 킷에는 사용자인증을 위한 [WorkOS AuthKit](https://authkit.com) 활용 옵션도 포함되어 있습니다. WorkOS 버전의 스타터 킷은 소셜 로그인, 패스키(passkey), SSO(싱글 사인온) 지원 기능을 제공합니다.

<a name="minimal-breaking-changes"></a>
### 최소화된 호환성 깨짐(브레이킹 체인지)

이번 릴리스 주기 동안 저희는 기존 기능과의 호환성을 최대한 깨뜨리지 않는 데 초점을 맞췄습니다. 대신, 기존 애플리케이션에 영향을 주지 않는 범위 내에서 연중 다양한 품질 개선 사항을 지속적으로 제공하는 데에 힘썼습니다.

따라서 라라벨 12는 현재 의존성 패키지의 업그레이드가 주된 목적이기 때문에, 비교적 작은 "유지보수용 릴리스"로 볼 수 있습니다. 이로 인해 대부분의 라라벨 애플리케이션은 기존 코드 변경 없이도 라라벨 12로 쉽게 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 킷

라라벨 12에서는 React, Vue, Livewire를 위한 새로운 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)이 도입되었습니다. React와 Vue 스타터 킷은 Inertia 2, 타입스크립트(TypeScript), [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하며, Livewire 스타터 킷은 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Vue, Livewire 각 스타터 킷 모두 라라벨의 내장 인증 시스템을 활용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 관련 기능을 제공합니다. 또한 각 스타터 킷에는 [WorkOS AuthKit](https://authkit.com) 기반 버전도 제공되어 소셜 로그인, 패스키, SSO 기능을 사용할 수 있습니다. WorkOS는 월간 활성 사용자가 100만 명까지는 무료로 인증 기능을 제공합니다.

이러한 신규 애플리케이션 스타터 킷이 도입됨에 따라, Laravel Breeze 및 Laravel Jetstream은 더 이상 추가적인 업데이트가 제공되지 않습니다.

새로운 스타터 킷을 바로 시작하려면 [스타터 킷 문서](/docs/12.x/starter-kits)를 참고하십시오.

