# 스타터 키트

- [소개](#introduction)
- [스타터 키트를 이용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이즈](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, 우리는 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 여러분이 다음 Laravel 애플리케이션을 빠르게 개발할 수 있도록 도와주며, 사용자의 회원가입 및 인증을 처리하기 위한 라우트, 컨트롤러, 뷰가 포함되어 있습니다.

이 스타터 키트의 사용은 선택 사항입니다. 여러분은 언제든지 Laravel의 새 복사본을 설치하여 직접 애플리케이션을 처음부터 개발할 수 있습니다. 어떤 방법을 택하시더라도 멋진 결과를 만들어낼 것을 믿습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 이용한 애플리케이션 생성

스타터 키트 중 하나를 사용하여 새로운 Laravel 애플리케이션을 생성하려면 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/{{version}}/installation#installing-php)해야 합니다. PHP와 Composer가 이미 설치되어 있다면, Composer를 통해 Laravel 설치 CLI를 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

이제 Laravel 설치 CLI를 사용하여 새로운 Laravel 애플리케이션을 생성하세요. Laravel 설치기는 원하는 스타터 키트를 선택할 수 있도록 안내합니다:

```shell
laravel new my-app
```

Laravel 애플리케이션을 생성한 후, NPM을 통해 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 시작합니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 시작되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 이용하여 React 프론트엔드와 함께 견고하고 현대적인 Laravel 애플리케이션 개발을 위한 시작점을 제공합니다.

Inertia를 사용하면 고전적인 서버 사이드 라우팅과 컨트롤러를 활용하면서도 최신 싱글 페이지 React 애플리케이션을 만들 수 있습니다. React의 프론트엔드 파워와 Laravel의 강력한 백엔드 생산성, 초고속 Vite 컴파일의 장점을 모두 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 이용하여 Vue 프론트엔드와 함께 Laravel 애플리케이션 개발을 위한 훌륭한 시작점을 제공합니다.

Inertia를 사용하면 고전적인 서버 사이드 라우팅과 컨트롤러를 활용하면서도 최신 싱글 페이지 Vue 애플리케이션을 만들 수 있습니다. Vue의 프론트엔드 파워와 Laravel의 강력한 백엔드 생산성, 초고속 Vite 컴파일의 장점을 모두 누릴 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 기반으로 하는 Laravel 애플리케이션 개발에 최적화된 시작점을 제공합니다.

Livewire는 오직 PHP만으로 동적인 반응형 프론트엔드 UI를 구축하는 강력한 도구입니다. Blade 템플릿을 주로 사용하는 팀이나 React, Vue와 같은 자바스크립트 기반 SPA 프레임워크보다 더 간단한 대안을 선호하는 경우에 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이즈

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로 백엔드와 프론트엔드 코드는 애플리케이션 내에 모두 존재하므로 자유롭게 커스터마이즈가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 위치합니다. 원하는 디자인과 동작을 만들기 위해 코드를 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn 컴포넌트를 추가하려면, 먼저 [원하는 컴포넌트를 검색](https://ui.shadcn.com)합니다. 그런 다음, `npx`를 사용하여 컴포넌트를 배포합니다:

```shell
npx shadcn@latest add switch
```

이 예에서는 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 생성됩니다. 컴포넌트가 추가되면, 해당 페이지 어디서든 사용할 수 있습니다:

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

React 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 주요 레이아웃이 내장되어 있습니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일 상단에서 import 경로를 수정하여 헤더 레이아웃으로 변경할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본형, "inset"형, "floating"형 등 세 가지 변형이 있습니다. `resources/js/components/app-sidebar.tsx` 컴포넌트 내에서 원하는 변형으로 수정할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split" 등 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 상단의 import 경로를 수정합니다:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로 백엔드와 프론트엔드 코드는 애플리케이션 내에 모두 존재하므로 자유롭게 커스터마이즈가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 위치합니다. 원하는 디자인과 동작을 만들기 위해 코드를 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블 / 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn-vue 컴포넌트를 추가하려면, 먼저 [원하는 컴포넌트를 검색](https://www.shadcn-vue.com)합니다. 그런 다음, `npx`를 사용하여 컴포넌트를 배포합니다:

```shell
npx shadcn-vue@latest add switch
```

이 예에서는 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 생성됩니다. 컴포넌트가 추가되면, 해당 페이지 어디서든 사용할 수 있습니다:

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

Vue 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 주요 레이아웃이 내장되어 있습니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/AppLayout.vue` 파일 상단에서 import 경로를 수정하여 헤더 레이아웃으로 변경할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본형, "inset"형, "floating"형 등 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.vue` 컴포넌트 내에서 원하는 변형으로 수정할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트에 포함된 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split" 등 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일 상단의 import 경로를 수정합니다:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로 백엔드와 프론트엔드 코드는 애플리케이션 내에 모두 존재하므로 커스터마이즈가 가능합니다.

#### Livewire와 Volt

프론트엔드 코드의 대부분은 `resources/views` 디렉터리에 위치합니다. 원하는 디자인과 동작을 만들기 위해 코드를 자유롭게 수정할 수 있습니다:

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 부분 뷰
├── dashboard.blade.php   # 인증 사용자 대시보드
├── welcome.blade.php     # 비회원 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resources/views` 디렉터리에, Livewire 컴포넌트에 대한 백엔드 로직은 `app/Livewire` 디렉터리에 위치합니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트에는 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 주요 레이아웃이 내장되어 있습니다. 기본값은 사이드바 레이아웃이며, `resources/views/components/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 수정하여 헤더 레이아웃으로 변경할 수 있습니다. 또한, main Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트에 포함된 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split" 등 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면, `resources/views/components/layouts/auth.blade.php` 파일에서 사용되는 레이아웃을 수정합니다:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos"></a>
## WorkOS AuthKit 인증

기본적으로 React, Vue, Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 초기화, 이메일 인증 등 다양한 기능을 제공합니다. 또한, 각 스타터 키트에는 [WorkOS AuthKit](https://authkit.com)이 적용된 변형도 있으며, 다음과 같은 인증 기능을 추가로 제공합니다:

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, GitHub, 애플)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월 활성 사용자 100만 명까지 무료로 인증을 제공합니다.

WorkOS AuthKit을 인증 시스템으로 사용하려면, `laravel new`를 통해 새로운 스타터 키트 기반 애플리케이션을 생성할 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 새 애플리케이션을 만든 후, 애플리케이션의 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정하세요. 이 변수 값은 WorkOS 대시보드에서 제공받은 값을 입력해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션 홈 URL도 설정해야 합니다. 이 URL로 사용자가 로그아웃 후 리디렉션됩니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용할 때는 애플리케이션의 WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하고, 소셜 로그인, 패스키, "Magic Auth", SSO로만 로그인하도록 설정하는 것을 권장합니다. 이렇게 하면 사용자 비밀번호를 직접 관리하지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 만료 시간 설정

또한, WorkOS AuthKit 세션 비활성화 만료 시간을 Laravel 애플리케이션이 지정한 세션 만료 임계값(일반적으로 2시간)과 맞추는 것을 권장합니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. SSR 호환 번들을 빌드하려면 다음 명령어를 실행합니다:

```shell
npm run build:ssr
```

또한, `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 SSR 호환 번들 빌드 후 Laravel 개발 서버와 Inertia SSR 서버를 동시에 시작하여, 로컬에서 SSR 환경을 테스트할 수 있게 해줍니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트

Laravel 인스톨러로 새 애플리케이션을 생성할 때, Packagist에 등록된 커뮤니티 유지 스타터 키트를 `--using` 플래그로 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 만들기

여러분이 만든 스타터 키트를 다른 개발자와 공유하려면 [Packagist](https://packagist.org)에 배포해야 합니다. 스타터 키트는 필요한 환경 변수를 `.env.example` 파일에 정의하고, 설치 후 실행할 명령어가 있다면 `composer.json`의 `post-create-project-cmd` 배열에 등록해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드를 하나요?

각 스타터 키트는 다음 애플리케이션을 위한 탄탄한 출발점을 제공합니다. 모든 코드를 직접 소유하게 되므로, 원하는 대로 수정 및 커스터마이즈가 가능합니다. 하지만 스타터 키트 자체를 별도로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증 기능을 추가하려면 `App/Models/User.php` 모델에서 `MustVerifyEmail` import 부분의 주석을 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 합니다:

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

회원가입 후 사용자에게 인증 이메일이 전송됩니다. 사용자의 이메일이 인증될 때까지 특정 라우트 접근을 제한하려면 해당 라우트에 `verified` 미들웨어를 추가합니다:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 스타터 키트 변형을 사용할 때는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션 브랜딩에 맞게 기본 이메일 템플릿을 커스터마이즈할 수 있습니다. 다음 명령어로 이메일 뷰를 애플리케이션에 배포하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail` 폴더에 여러 파일이 생성됩니다. 이 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 자유롭게 수정하여, 기본 이메일 템플릿의 모양을 변경할 수 있습니다.