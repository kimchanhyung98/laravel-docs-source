# 릴리스 노트 (Release Notes)

- [버전 관리 방식](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 방식 (Versioning Scheme)

Laravel 및 기타 공식 패키지는 [SemVer(시맨틱 버전 관리)](https://semver.org)를 따릅니다. 주요 프레임워크 릴리스는 매년(주로 1분기)에 제공되며, 부 릴리스 및 패치 릴리스는 매주처럼 자주 배포될 수 있습니다. 부 릴리스 및 패치 릴리스에는 **절대로** 하위 호환성이 깨지는 변경(Breaking Change)이 포함되지 않습니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 컴포넌트를 참조할 때는 항상 `^12.0`과 같은 버전 제약조건을 사용해야 합니다. 이유는 Laravel의 주요 릴리스에는 하위 호환성이 깨지는 변경이 포함될 수 있기 때문입니다. 하지만 저희는 항상 하루 이내에 새 주요 릴리스로 업그레이드할 수 있도록 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 인수 사용 주의

[네임드 인수(Named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스 개선을 위해 필요하다면 함수 인수명을 변경할 수 있습니다. 따라서, Laravel 메서드 호출 시 네임드 인수를 사용하는 경우, 앞으로 파라미터 이름이 변경될 수 있다는 점을 유념하고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리스에 대해 버그 수정은 18개월, 보안 수정은 2년간 제공됩니다. 부가 라이브러리의 경우, 오직 최신 주요 버전만 버그 수정을 받습니다. 또한 Laravel이 지원하는 데이터베이스 버전을 반드시 확인하세요: [지원되는 데이터베이스 버전](/docs/master/database#introduction).

<div class="overflow-auto">

| 버전    | PHP 버전(*)  | 릴리스 일자           | 버그 수정 종료일        | 보안 수정 종료일       |
| ------- | ----------- | --------------------- | ---------------------- | ---------------------- |
| 10      | 8.1 - 8.3   | 2023년 2월 14일       | 2024년 8월 6일         | 2025년 2월 4일         |
| 11      | 8.2 - 8.4   | 2024년 3월 12일       | 2025년 9월 3일         | 2026년 3월 12일        |
| 12      | 8.2 - 8.5   | 2025년 2월 24일       | 2026년 8월 13일        | 2027년 2월 24일        |
| 13      | 8.3 - 8.5   | 2026년 1분기          | 2027년 3분기           | 2028년 1분기           |

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

Laravel 12는 상위 버전인 Laravel 11.x에서의 개선을 이어받아, 주요 의존성 라이브러리의 업그레이드와 함께 React, Vue, Livewire를 위한 새로운 스타터 키트(starter kit)를 도입하였습니다. 이와 더불어 사용자 인증을 위해 [WorkOS AuthKit](https://authkit.com)을 사용할 수 있는 옵션이 제공됩니다. WorkOS 버전의 스타터 키트는 소셜 인증, 패스키(passkeys), SSO(싱글 사인온) 기능을 지원합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 하위 호환성 깨짐 (Minimal Breaking Changes)

이번 릴리스 주기에서는 하위 호환성이 깨지는 변경을 최소화하는 데 큰 노력을 기울였습니다. 대신, 기존 애플리케이션에 영향을 주지 않으면서 연중 지속적으로 다양한 사용성 개선(QOL Improvement)을 제공하는 데 중점을 두었습니다.

이에 따라 Laravel 12는 기존 의존성을 업그레이드하기 위한 비교적 경미한 "유지보수 릴리스"입니다. 대부분의 Laravel 애플리케이션은 코드 변경 없이도 Laravel 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 키트

Laravel 12에서는 React, Vue, Livewire용 [새로운 애플리케이션 스타터 키트](/docs/master/starter-kits)를 도입했습니다. React와 Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하며, Livewire 스타터 키트는 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Vue, Livewire 스타터 키트 모두 Laravel의 내장 인증 시스템을 활용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 또한, 각각의 스타터 키트에는 [WorkOS AuthKit 기반](https://authkit.com)의 변형 버전을 함께 제공하며, 이를 통해 소셜 인증, 패스키, SSO 기능도 사용할 수 있습니다. WorkOS는 월간 활성 사용자 100만 명까지 무료 인증 서비스를 제공합니다.

새로운 애플리케이션 스타터 키트 도입과 함께, 기존의 Laravel Breeze 및 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.

새로운 스타터 키트 사용 방법은 [스타터 키트 문서](/docs/master/starter-kits)를 참고하시기 바랍니다.
