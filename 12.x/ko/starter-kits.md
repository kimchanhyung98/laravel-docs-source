# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 이용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [2단계 인증](#two-factor-authentication)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 제공 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

여러분의 새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트들은 다음 Laravel 프로젝트 개발을 빠르게 시작할 수 있도록 도와주며, 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰 등을 미리 포함하고 있습니다.

이러한 스타터 키트의 사용은 선택 사항입니다. 원한다면 Laravel의 새 복사본을 설치하여 바닥부터 애플리케이션을 직접 구축할 수도 있습니다. 어떤 방법을 선택하더라도, 멋진 결과를 만들어낼 수 있을 것이라 믿습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 이용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트를 사용하여 새로운 Laravel 애플리케이션을 만들려면, 먼저 [PHP 및 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 인스톨러 CLI 도구를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그런 다음, Laravel 인스톨러 CLI를 사용하여 새 라이브러리 애플리케이션을 생성합니다. 생성 과정에서 Laravel 인스톨러가 원하는 스타터 키트 선택을 안내합니다:

```shell
laravel new my-app
```

애플리케이션이 생성된 후, 프런트엔드 의존성을 NPM으로 설치하고, Laravel 개발 서버를 시작하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작했다면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)에 접속하여 애플리케이션을 확인할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 활용하여 React 프런트엔드로 Laravel 애플리케이션을 현대적으로 구축할 수 있는 강력한 출발점을 제공합니다.

Inertia는 서버 측 라우팅과 컨트롤러를 그대로 사용하면서도, 현대적인 싱글 페이지 React 애플리케이션을 개발할 수 있도록 도와줍니다. 이렇게 하면 React 기반 프런트엔드의 강점과, Laravel의 놀라운 백엔드 생산성, 그리고 Vite의 빠른 컴파일을 함께 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프런트엔드로 Laravel 애플리케이션을 개발하는 데 최적화된 출발점을 제공합니다.

Inertia를 활용하면, 서버 측 라우팅과 컨트롤러는 그대로 유지하면서, 최신 싱글 페이지 Vue 애플리케이션을 쉽고 효율적으로 만들 수 있습니다. 이를 통해 Vue의 프런트엔드 성능과 Laravel의 백엔드 생산성, 그리고 Vite의 빠른 컴파일을 조합할 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 포함하고 있습니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프런트엔드를 이용해 Laravel 애플리케이션을 구축하기에 완벽한 출발점을 제공합니다.

Livewire는 PHP만으로 동적이고 반응성이 뛰어난 프런트엔드 UI를 개발할 수 있게 해 주는 강력한 도구입니다. Blade 템플릿을 주로 활용하는 팀이 React나 Vue 같은 JavaScript 기반 SPA 프레임워크보다 더 간단한 대안을 찾을 때도 매우 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프런트엔드 전체 코드가 애플리케이션 내에 포함되어 있으므로 완전한 커스터마이징이 가능합니다.

프런트엔드 코드는 대부분 `resources/js` 디렉터리에 위치합니다. 코드의 어느 부분이든 자유롭게 수정하여 애플리케이션의 외관과 동작을 조정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn 컴포넌트를 설치하려면, [추가할 컴포넌트](https://ui.shadcn.com)를 찾은 뒤에 `npx`로 컴포넌트를 퍼블리시합니다:

```shell
npx shadcn@latest add switch
```

예를 들어 위 명령은 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 위치에 퍼블리시합니다. 퍼블리시된 컴포넌트는 원하는 페이지에서 자유롭게 사용할 수 있습니다:

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a name="react-available-layouts"></a>
#### 사용 가능한 레이아웃

React 스타터 키트에는 두 가지 주요 레이아웃(사이드바 레이아웃, 헤더 레이아웃)이 포함되어 있습니다. 기본값은 사이드바 레이아웃이지만, `resources/js/layouts/app-layout.tsx` 파일 상단에서 불러오는 레이아웃을 변경해 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 레이아웃 변형

사이드바 레이아웃에는 기본 사이드바, "인셋" 변형, "플로팅" 변형의 세 가지 유형이 있습니다. 원하는 변형을 사용하려면 `resources/js/components/app-sidebar.tsx` 컴포넌트에서 옵션을 변경하면 됩니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인/회원가입 페이지 등 인증 관련 페이지 역시 "simple", "card", "split"의 세 가지 레이아웃을 지원합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 상단에서 불러오는 레이아웃을 수정하면 됩니다:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구축되었습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프런트엔드 전체 코드가 애플리케이션 내에 포함되어 있으므로 완전한 커스터마이징이 가능합니다.

프런트엔드 코드는 대부분 `resources/js` 디렉터리에 위치합니다. 코드의 어느 부분이든 자유롭게 수정하여 애플리케이션의 외관과 동작을 조정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블/훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn-vue 컴포넌트를 설치하려면, [추가할 컴포넌트](https://www.shadcn-vue.com)를 찾은 뒤 `npx`로 컴포넌트를 퍼블리시합니다:

```shell
npx shadcn-vue@latest add switch
```

예를 들어 위 명령은 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue`에 퍼블리시합니다. 퍼블리시된 컴포넌트는 원하는 페이지에서 자유롭게 사용할 수 있습니다:

```vue
<script setup lang="ts">
import { Switch } from '@/Components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
#### 사용 가능한 레이아웃

Vue 스타터 키트에도 두 가지 주요 레이아웃(사이드바 레이아웃, 헤더 레이아웃)이 포함되어 있습니다. 사이드바 레이아웃이 기본값이지만, `resources/js/layouts/AppLayout.vue` 파일 상단에서 불러오는 레이아웃을 변경해 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 레이아웃 변형

사이드바 레이아웃에는 기본형, "inset" 변형, "floating" 변형 등 세 가지 방식이 있습니다. 원하는 스타일로 사용하려면 `resources/js/components/AppSidebar.vue` 컴포넌트에서 옵션을 변경하면 됩니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트에 포함된 로그인, 회원가입 등의 인증 페이지 역시 "simple", "card", "split"의 세 가지 레이아웃을 지원합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일 상단에서 불러오는 레이아웃을 수정하면 됩니다:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)로 구축되었습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프런트엔드 전체 코드가 애플리케이션 내에 포함되어 있으므로 완전한 커스터마이징이 가능합니다.

#### Livewire와 Volt

프런트엔드 코드는 `resources/views` 디렉터리에 위치합니다. 애플리케이션의 외관이나 동작을 커스터마이즈하려면 이 내부의 파일을 자유롭게 수정할 수 있습니다:

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이징된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 파셜
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트 사용자 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프런트엔드 코드는 `resources/views` 디렉터리에, 해당 Livewire 컴포넌트의 백엔드 로직은 `app/Livewire` 디렉터리에 위치합니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트에는 두 가지 주요 레이아웃(사이드바 레이아웃, 헤더 레이아웃)이 포함되어 있습니다. 기본값은 사이드바 레이아웃이지만, `resources/views/components/layouts/app.blade.php`에서 사용하는 레이아웃을 변경하면 헤더 레이아웃으로 전환할 수 있습니다. 또한 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트에 포함된 로그인, 회원가입 등의 인증 페이지 역시 "simple", "card", "split"의 세 가지 레이아웃을 지원합니다.

인증 레이아웃을 변경하려면, `resources/views/components/layouts/auth.blade.php`에서 사용하는 레이아웃을 수정합니다:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="two-factor-authentication"></a>
## 2단계 인증 (Two-Factor Authentication)

모든 스타터 키트에는 [Laravel Fortify](/docs/12.x/fortify#two-factor-authentication) 기반의 내장 2단계 인증(2FA)이 포함되어 있어, 사용자 계정에 한층 더 강력한 보안을 제공합니다. 사용자는 시간 기반 일회용 비밀번호(TOTP)를 지원하는 인증 애플리케이션을 이용해 자신의 계정을 보호할 수 있습니다.

2단계 인증은 기본적으로 활성화되어 있으며, [Fortify](/docs/12.x/fortify#two-factor-authentication)가 제공하는 모든 설정 옵션을 지원합니다:

```php
Features::twoFactorAuthentication([
    'confirm' => true,
    'confirmPassword' => true,
]);
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트는 Laravel의 내장 인증 시스템을 기반으로 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 일반적인 인증 기능을 제공합니다. 더불어 각 스타터 키트의 [WorkOS AuthKit](https://authkit.com) 기반 변형도 제공하며, 이를 통해 다음 기능도 지원됩니다:

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키(Passkey) 인증
- 이메일 기반 "Magic Auth"
- SSO

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월 1백만 명까지만 무료 인증을 지원합니다.

WorkOS AuthKit을 애플리케이션의 인증 제공자로 사용하려면, `laravel new`로 새로운 스타터 키트 기반 애플리케이션을 생성할 때 WorkOS 옵션을 선택하면 됩니다.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 애플리케이션을 생성한 뒤, 애플리케이션의 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 애플리케이션별로 제공됩니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션의 홈페이지 URL을 설정해야 합니다. 이 URL은 사용자가 로그아웃 후 리디렉션되는 경로입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용할 때는, WorkOS AuthKit의 설정에서 "Email + Password" 인증을 비활성화하고, 소셜 인증, 패스키, "Magic Auth", SSO만 활성화할 것을 권장합니다. 이렇게 하면 애플리케이션에서 사용자의 비밀번호 처리가 완전히 필요 없게 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

추가적으로, WorkOS AuthKit 세션 비활성화 타임아웃 시간도 Laravel 애플리케이션의 세션 타임아웃(보통 2시간)과 일치시키는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. Inertia SSR에 맞게 애플리케이션 번들을 빌드하려면 `build:ssr` 명령어를 실행합니다:

```shell
npm run build:ssr
```

또한, 편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 SSR 호환 번들 빌드 후, Laravel 개발 서버와 Inertia SSR 서버를 함께 실행하여 서버 사이드 렌더링 환경에서 애플리케이션을 로컬에서 바로 테스트할 수 있습니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 제공 스타터 키트 (Community Maintained Starter Kits)

Laravel 인스톨러를 이용해 새로운 Laravel 애플리케이션을 만들 때, Packagist에 공개된 커뮤니티 스타터 키트를 `--using` 플래그로 지정해 사용할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 직접 만들기

스타터 키트를 다른 사람과 공유하려면, [Packagist](https://packagist.org)에 퍼블리시해야 합니다. 스타터 키트는 `.env.example` 파일에 필요한 환경 변수를 정의하고, 설치 후 실행되어야 하는 명령어는 `composer.json`의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

모든 스타터 키트는 새로운 애플리케이션 개발을 위한 확실한 출발점을 제공합니다. 소스 코드 전체가 여러분 소유이므로, 원하는 만큼 자유롭게 수정, 커스터마이징, 확장하여 비전을 실현할 수 있습니다. 하지만, 스타터 키트 자체를 별도로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증 기능은 어떻게 활성화하나요?

이메일 인증 기능을 추가하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` import를 주석 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

회원가입이 완료된 사용자는 이메일 인증 메일을 받게 됩니다. 특정 라우트에 이메일 인증이 완료된 사용자만 접근하도록 제한하려면, 해당 라우트에 `verified` 미들웨어를 추가합니다:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 스타터 키트 변형 사용 시에는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 수정하려면 어떻게 하나요?

기본 이메일 템플릿을 애플리케이션의 브랜드에 맞게 커스터마이징하고 싶다면, 다음 명령어로 이메일 뷰 파일을 퍼블리시합니다:

```
php artisan vendor:publish --tag=laravel-mail
```

이렇게 하면 `resources/views/vendor/mail` 이하에 여러 파일이 생성됩니다. 이 파일들과 `resources/views/vendor/mail/themes/default.css` 파일을 직접 수정하여, 이메일 템플릿의 레이아웃과 스타일을 원하는 대로 바꿀 수 있습니다.
