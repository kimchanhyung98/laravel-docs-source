# 스타터 킷 (Starter Kits)

- [소개](#introduction)
- [스타터 킷을 사용하여 애플리케이션 생성하기](#creating-an-application)
- [사용 가능한 스타터 킷](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 킷 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 관리 스타터 킷](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, [애플리케이션 스타터 킷](https://laravel.com/starter-kits)을 제공하고 있습니다. 이 스타터 킷들은 다음 Laravel 애플리케이션을 구축하는 데 필요한 시작점을 제공하며, 사용자 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 포함하고 있습니다.

이 스타터 킷들은 선택 사항이며, 꼭 사용해야 하는 것은 아닙니다. 원하신다면 Laravel을 새로 설치하여 처음부터 직접 애플리케이션을 구축하셔도 됩니다. 어떤 방법을 선택하든 멋진 애플리케이션을 만드실 수 있을 것이라 확신합니다!

<a name="creating-an-application"></a>
## 스타터 킷을 사용하여 애플리케이션 생성하기

스타터 킷 중 하나를 사용하여 새 Laravel 애플리케이션을 만들려면, 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/master/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치 CLI 도구를 전역으로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그 다음, Laravel 설치 CLI를 사용해서 새 애플리케이션을 만드세요. 설치 도구가 선호하는 스타터 킷을 선택하라는 안내를 제공합니다:

```shell
laravel new my-app
```

애플리케이션 생성 후에는 NPM으로 프론트엔드 의존성을 설치하고, Laravel 개발 서버를 시작하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

개발 서버가 시작되면 브라우저에서 [http://localhost:8000](http://localhost:8000) 으로 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 킷

<a name="react"></a>
### React

React 스타터 킷은 [Inertia](https://inertiajs.com)를 사용하여 React 프론트엔드를 갖춘 Laravel 애플리케이션을 구축할 수 있는 강력하고 현대적인 시작점입니다.

Inertia는 고전적인 서버 사이드 라우팅과 컨트롤러를 사용하면서, React 기반의 최신 단일 페이지 애플리케이션(SPA)을 만들 수 있게 해 줍니다. 이로써 React 프론트엔드의 강력함과 Laravel의 뛰어난 백엔드 생산성, 그리고 Vite의 빠른 컴파일 속도를 동시에 누릴 수 있습니다.

React 스타터 킷은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 킷은 [Inertia](https://inertiajs.com)를 사용한 Vue 프론트엔드를 가진 Laravel 애플리케이션을 만드는 훌륭한 출발점입니다.

Inertia로 최신 단일 페이지 Vue 애플리케이션을 고전적인 서버 라우팅과 컨트롤러로 만들 수 있습니다. 덕분에 Vue의 프론트엔드 역량과 Laravel 백엔드의 탁월함, 그리고 빠른 Vite 컴파일 속도를 동시에 활용할 수 있습니다.

Vue 스타터 킷은 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 킷은 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 갖춘 Laravel 애플리케이션을 위한 최적의 출발점입니다.

Livewire는 PHP만으로 동적이고 반응형 프론트엔드 UI를 구축할 수 있는 강력한 방식입니다. Blade 템플릿을 주로 사용하는 팀이나 React, Vue 같은 자바스크립트 기반 SPA 프레임워크 대신에 더 간단한 대안을 찾는 경우에 매우 적합합니다.

Livewire 스타터 킷은 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 킷 커스터마이징

<a name="react-customization"></a>
### React

React 스타터 킷은 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드는 귀하의 애플리케이션 내에 모두 포함되어 있어 완전한 커스터마이징이 가능합니다.

대부분의 프론트엔드 코드는 `resources/js` 디렉터리에 위치해 있습니다. 애플리케이션의 외관과 동작을 수정하고자 하는 경우 자유롭게 코드를 변경할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn 컴포넌트를 배포하려면, 먼저 [원하는 컴포넌트를 찾아](https://ui.shadcn.com) `npx` 명령어를 사용해 배포합니다:

```shell
npx shadcn@latest add switch
```

예를 들어 위 명령은 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 경로에 배포합니다. 배포한 후에는 페이지 어디에서나 사용할 수 있습니다:

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

React 스타터 킷에는 두 가지 주요 레이아웃이 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일 상단에서 임포트하는 레이아웃을 변경하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본 사이드바, "inset" 변형, "floating" 변형, 총 세 가지가 있습니다. `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 킷에 포함된 로그인, 회원가입 페이지 등 인증 페이지들은 "simple", "card", "split" 세 가지 다른 레이아웃 변형을 제공합니다.

인증 레이아웃을 바꾸려면 애플리케이션의 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 임포트하는 레이아웃을 변경하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 킷은 Inertia 2, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드는 귀하의 애플리케이션 내에 모두 포함되어 있어 완전한 커스터마이징이 가능합니다.

프론트엔드 코드는 대부분 `resources/js` 디렉터리에 위치합니다. 원하는 경우 애플리케이션의 외관과 동작에 맞게 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue composables / 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn-vue 컴포넌트를 배포하려면, 먼저 [원하는 컴포넌트를 찾아](https://www.shadcn-vue.com) `npx` 명령어를 사용해 배포합니다:

```shell
npx shadcn-vue@latest add switch
```

위 명령은 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue` 파일로 배포합니다. 배포한 후에는 페이지 어디에서나 사용할 수 있습니다:

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

Vue 스타터 킷에는 두 가지 주요 레이아웃이 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/AppLayout.vue` 파일 상단에서 임포트하는 레이아웃을 변경하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본 사이드바, "inset" 변형, "floating" 변형, 총 세 가지가 있습니다. `resources/js/components/AppSidebar.vue` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 킷에 포함된 로그인, 회원가입 페이지 등의 인증 페이지들은 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 바꾸려면 `resources/js/layouts/AuthLayout.vue` 파일 상단에서 임포트하는 레이아웃을 변경하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 킷은 Livewire 3, Tailwind, 그리고 [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드는 귀하의 애플리케이션 내에 모두 포함되어 있어 완전한 커스터마이징이 가능합니다.

#### Livewire와 Volt

대부분의 프론트엔드 코드는 `resources/views` 디렉터리에 위치합니다. 애플리케이션의 외관과 동작을 원하는 대로 수정할 수 있습니다:

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스텀 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 파셜
├── dashboard.blade.php   # 인증 사용자 대시보드
├── welcome.blade.php     # 방문자 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resources/views`에 위치하며, `app/Livewire` 디렉터리는 Livewire 컴포넌트에 대응하는 백엔드 로직을 포함합니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 킷에는 두 가지 주요 레이아웃이 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 기본값은 사이드바 레이아웃이며, `resources/views/components/layouts/app.blade.php` 파일에서 사용하는 레이아웃을 변경하여 헤더 레이아웃으로 바꿀 수 있습니다. 또한 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 킷에 포함된 로그인, 회원가입 페이지 등 인증 페이지들도 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 바꾸려면 `resources/views/components/layouts/auth.blade.php` 파일에서 사용하는 레이아웃을 변경하세요:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos"></a>
## WorkOS AuthKit 인증

기본적으로 React, Vue, Livewire 스타터 킷은 Laravel 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 기능을 제공합니다. 이와 더불어, 각 스타터 킷에는 [WorkOS AuthKit](https://authkit.com) 기반의 옵션이 있어 다음 기능들을 제공합니다:

<div class="content-list" markdown="1">

- 소셜 인증 (Google, Microsoft, GitHub, Apple)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO(싱글 사인온)

</div>

WorkOS를 인증 공급자로 사용하려면 [WorkOS 계정이 필요](https://workos.com)하며, WorkOS는 월간 최대 100만 활성 사용자까지 무료 인증을 지원합니다.

WorkOS AuthKit을 애플리케이션의 인증 공급자로 사용하려면, `laravel new` 명령어로 새 애플리케이션을 만들 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 킷 설정

WorkOS 기반 스타터 킷으로 애플리케이션을 만든 후 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 앱에 대해 받은 정보와 일치해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한 WorkOS 대시보드에서 애플리케이션의 홈 페이지 URL도 설정해야 하며, 사용자가 로그아웃 시 이 URL로 리디렉션됩니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 스타터 킷을 사용할 때는 WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하는 것이 좋습니다. 이렇게 하면 사용자는 소셜 인증 공급자, 패스키, "Magic Auth", SSO만으로만 인증할 수 있습니다. 이를 통해 애플리케이션은 사용자 비밀번호를 전혀 다루지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

추가로, WorkOS AuthKit의 세션 비활성화 타임아웃을 Laravel 애플리케이션의 세션 타임아웃(보통 2시간)과 맞추는 것을 권장합니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 킷은 Inertia의 [서버 사이드 렌더링](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. Inertia SSR 호환 번들을 빌드하려면 다음 명령어를 실행하세요:

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령도 제공됩니다. 이 명령은 애플리케이션의 SSR 호환 번들을 빌드한 후 Laravel 개발 서버와 Inertia SSR 서버를 함께 시작하여, 로컬 환경에서 서버 사이드 렌더링을 테스트할 수 있게 해 줍니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 관리 스타터 킷

Laravel 설치 도구로 새 Laravel 애플리케이션을 만들 때, Packagist에 공개된 커뮤니티 관리 스타터 킷을 `--using` 플래그로 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 킷 만들기

자신의 스타터 킷을 다른 이들도 쓸 수 있도록 하려면, Packagist에 배포해야 합니다. 스타터 킷은 `.env.example` 파일에 필요한 환경 변수를 명시해야 하며, 설치 후 실행할 후처리 명령어는 `composer.json` 파일의 `post-create-project-cmd` 배열에 포함시켜야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

각 스타터 킷은 다음 애플리케이션을 위한 탄탄한 출발점을 제공합니다. 코드를 전적으로 소유하고 있으므로, 원하는 대로 수정하고 커스터마이징하며 구축할 수 있습니다. 단, 스타터 킷 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증을 사용하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` 임포트를 주석 해제하고, 해당 인터페이스를 구현하도록 해야 합니다:

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

회원가입 후 사용자에게 인증 메일이 발송되며, 이메일 인증이 완료될 때까지 특정 라우트 접근을 제한하려면 `verified` 미들웨어를 해당 라우트에 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 버전 스타터 킷을 사용할 경우 이메일 인증은 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션 브랜드에 맞게 이메일 템플릿을 수정하려면, 다음 명령어로 이메일 뷰를 애플리케이션 내로 게시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령으로 `resources/views/vendor/mail` 폴더에 여러 파일이 생성됩니다. 이 파일들과 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여 기본 이메일 템플릿의 디자인과 모양을 변경할 수 있습니다.