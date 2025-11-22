# 릴리즈 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 체계 (Versioning Scheme)

Laravel 및 그 외 1차 라이브러리들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)을 따릅니다. 주요 프레임워크 릴리즈는 매년(대략 1분기)마다 발표되며, 마이너 및 패치 릴리즈는 매주 발표될 수 있습니다. 마이너 및 패치 릴리즈에는 **절대로** 호환성을 깨뜨리는 변경 사항이 포함되지 않습니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 혹은 그 컴포넌트를 참조할 때는 `^12.0`과 같은 버전 제약을 항상 사용해야 합니다. Laravel의 주요 버전 릴리즈에는 호환성을 깨뜨리는 변경이 포함될 수 있기 때문입니다. 그러나, 새로운 주요 릴리즈로의 업데이트가 하루, 혹은 그 이하의 시간 안에 이루어질 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 인수(Named Arguments)

[네임드 인수(named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 역호환성(backwards compatibility) 가이드라인에 포함되지 않습니다. 저희는 Laravel 코드베이스의 향상을 위해 함수 인수의 이름을 필요에 따라 변경할 수 있습니다. 따라서, Laravel의 메서드를 호출할 때 네임드 인수를 사용하는 경우에는, 향후 파라미터 이름이 변경될 수 있음을 염두에 두고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈에는 18개월간 버그 수정이 제공되며, 2년간 보안 수정이 제공됩니다. 추가 라이브러리의 경우에는 오직 최신 주요 버전에서만 버그 수정이 이루어집니다. 또한, Laravel이 [지원하는 데이터베이스 버전](/docs/12.x/database#introduction)도 꼭 확인하시기 바랍니다.

<div class="overflow-auto">

| 버전 | PHP (*)   | 릴리즈             | 버그 수정 종료일       | 보안 수정 종료일       |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1 - 8.3 | 2023년 2월 14일      | 2024년 8월 6일         | 2025년 2월 4일         |
| 11      | 8.2 - 8.4 | 2024년 3월 12일      | 2025년 9월 3일         | 2026년 3월 12일        |
| 12      | 8.2 - 8.5 | 2025년 2월 24일      | 2026년 8월 13일        | 2027년 2월 24일        |
| 13      | 8.3 - 8.5 | 2026년 1분기         | 2027년 3분기           | 2028년 1분기           |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 수정만 제공</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 상위 의존성 업그레이드와 함께 React, Vue, Livewire용 신규 스타터 킷(starter kit)을 도입하는 등, Laravel 11.x에서 이루어진 개선 사항을 이어나갑니다. 이 새로운 스타터 킷에는 사용자를 인증할 수 있도록 [WorkOS AuthKit](https://authkit.com) 옵션이 추가되어 있습니다. WorkOS 버전의 스타터 킷은 소셜 인증, 패스키(passkey), SSO(싱글사인온) 지원을 제공합니다.

<a name="minimal-breaking-changes"></a>
### 최소화된 호환성 파괴(Minimal Breaking Changes)

이번 릴리즈 사이클의 주요 초점은 호환성을 깨뜨리는 변경 사항을 최대한 줄이는 것이었습니다. 그 대신, 기존 애플리케이션을 깨뜨리지 않으면서도 연중 내내 지속적으로 개발자 경험을 향상시키는 다양한 개선점을 제공하는 데에 집중했습니다.

이러한 이유로, Laravel 12는 기존 의존성의 업그레이드를 위한 상대적으로 경미한 "유지보수 릴리즈"라고 할 수 있습니다. 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 변경하지 않고도 Laravel 12로 바로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 킷

Laravel 12에서는 React, Vue, Livewire용 새로운 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 제공합니다. React와 Vue 스타터 킷은 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하고, Livewire 스타터 킷은 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 활용합니다.

React, Vue, Livewire 모든 스타터 킷은 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능을 제공합니다. 또한 각각의 킷에는 [WorkOS AuthKit 기반](https://authkit.com) 버전도 제공되며, 소셜 인증, 패스키, SSO(싱글사인온) 기능도 지원합니다. WorkOS는 월간 활성 사용자 100만 명까지 무료로 인증 서비스를 제공합니다.

새로운 애플리케이션 스타터 킷 도입으로 인해, Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트가 제공되지 않습니다.

새로운 스타터 킷으로 시작하려면, [스타터 킷 문서](/docs/12.x/starter-kits)를 참조하세요.
