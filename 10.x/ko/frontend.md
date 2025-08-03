# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [Vue / React 사용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [자산 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 현대적인 웹 애플리케이션을 구축하는 데 필요한 [라우팅](/docs/10.x/routing), [유효성 검증](/docs/10.x/validation), [캐싱](/docs/10.x/cache), [큐](/docs/10.x/queues), [파일 저장소](/docs/10.x/filesystem) 등 모든 기능을 제공하는 백엔드 프레임워크입니다. 그러나 개발자에게 강력한 프론트엔드 구축 방식을 포함하는 아름다운 풀스택 경험을 제공하는 것도 중요하다고 생각합니다.

Laravel로 애플리케이션을 만들 때 프론트엔드 개발을 접근하는 두 가지 주요 방법이 있으며, 어떤 방식을 선택할지는 PHP를 활용해 프론트엔드를 구축할지, Vue나 React 같은 자바스크립트 프레임워크를 사용할지에 따라 정해집니다. 아래에서 이 두 옵션을 모두 다뤄, 애플리케이션에 가장 적합한 프론트엔드 개발 방법을 선택할 수 있도록 도와드리겠습니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP and Blade)

과거 대부분 PHP 애플리케이션은 간단한 HTML 템플릿 안에 PHP `echo` 구문을 섞어, 요청 시 데이터베이스에서 가져온 데이터를 렌더링하여 HTML을 브라우저에 출력했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 [뷰](/docs/10.x/views)와 [Blade](/docs/10.x/blade)를 사용해 이와 같은 HTML 렌더링 방식을 여전히 사용할 수 있습니다. Blade는 데이터 출력, 반복 처리 등을 편리하고 간결한 문법으로 제공하는 매우 가벼운 템플릿 엔진입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이런 식으로 애플리케이션을 구축할 때, 폼 제출이나 페이지 내 다른 인터랙션은 일반적으로 서버에서 완전히 새로운 HTML 문서를 받아서 브라우저가 페이지 전체를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션이 간단한 Blade 템플릿으로 이같이 프론트엔드를 구축하는 것이 충분히 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 점점 높아지는 기대치

하지만 사용자가 웹 애플리케이션에 기대하는 경험이 높아지면서, 더욱 다이내믹하고 매끄러운 인터랙션을 갖춘 프론트엔드를 개발해야 하는 필요성을 느끼는 개발자가 많아졌습니다. 이에 따라 일부 개발자들은 Vue나 React 같은 자바스크립트 프레임워크를 사용해 애플리케이션 프론트엔드를 구축하기 시작했습니다.

한편으로는 익숙한 백엔드 언어로 주로 개발하면서도 최신 웹 UI를 만들 수 있도록 하는 솔루션들도 등장했습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 만들어졌습니다.

Laravel 생태계 내에서는 PHP를 주로 사용해 현대적이고 동적인 프론트엔드를 만들어야 할 필요성으로 인해 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 탄생했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React 같은 현대적인 자바스크립트 프레임워크로 만든 프론트엔드와 같이 동적이고 최신식이며 생동감 있는 Laravel 기반 프론트엔드를 구축할 수 있도록 돕는 프레임워크입니다.

Livewire를 사용하면, UI의 특정 부분을 렌더링하고 메서드와 데이터를 애플리케이션 프론트엔드에서 호출하고 상호작용할 수 있도록 하는 Livewire "컴포넌트"를 만듭니다. 예를 들어, 간단한 "카운터" 컴포넌트는 다음과 같이 생겼을 수 있습니다:

```php
<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

카운터에 해당하는 템플릿은 다음과 같이 작성됩니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피, Livewire는 `wire:click` 같은 새로운 HTML 속성을 작성할 수 있게 하여, Laravel 애플리케이션의 프론트엔드와 백엔드를 연결해줍니다. 또한, Blade 표현식을 이용해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

많은 개발자에게 Livewire는 Laravel 내에서 익숙함을 유지하면서도 모던하고 동적인 웹 애플리케이션을 만들 수 있는 혁신적인 프론트엔드 개발 도구가 되었습니다. 일반적으로 Livewire를 사용하는 개발자들은 필요할 때만 프론트엔드에 JavaScript를 “살짝 뿌리는” 용도로 [Alpine.js](https://alpinejs.dev/)도 함께 사용합니다. 예를 들어, 대화창을 렌더링할 때 Alpine.js를 쓸 수 있습니다.

Laravel을 처음 접하는 개발자라면, 먼저 [뷰](/docs/10.x/views)와 [Blade](/docs/10.x/blade)의 기본 사용법에 익숙해지는 것을 추천합니다. 그 후 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고해 대화형 Livewire 컴포넌트를 활용해 애플리케이션을 한 단계 업그레이드하는 방법을 배우세요.

<a name="php-starter-kits"></a>
### 스타터 킷 (Starter Kits)

PHP와 Livewire를 사용해 프론트엔드를 만들고 싶다면, Breeze 또는 Jetstream [스타터 킷](/docs/10.x/starter-kits)을 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 두 스타터 킷은 [Blade](/docs/10.x/blade)와 [Tailwind](https://tailwindcss.com)를 사용해 백엔드와 프론트엔드 인증 흐름을 스캐폴딩 해주므로, 곧바로 다음 대규모 아이디어 개발에 집중할 수 있습니다.

<a name="using-vue-react"></a>
## Vue / React 사용하기 (Using Vue / React)

Laravel과 Livewire로도 현대적인 프론트엔드를 구축할 수 있지만, 여전히 많은 개발자가 Vue나 React 같은 자바스크립트 프레임워크의 강력함을 활용하는 것을 선호합니다. 이는 NPM을 통한 방대한 자바스크립트 패키지와 도구 생태계를 최대한 활용할 수 있기 때문입니다.

하지만 별도의 도구 없이 Laravel을 Vue 또는 React와 결합하면, 클라이언트 측 라우팅, 데이터 하이드레이션(hydration), 인증 등 복잡한 문제들을 해결해야 합니다. 클라이언트 쪽 라우팅은 보통 [Nuxt](https://nuxt.com/)나 [Next](https://nextjs.org/) 같은 Vue / React용 규칙 기반 프레임워크를 사용해 단순화할 수 있지만, 데이터 하이드레이션과 인증 문제는 Laravel과 이들 프론트엔드 프레임워크를 결합할 때 여전히 까다롭고 번거로운 문제로 남습니다.

또한, 두 개의 별도 코드 리포지터리를 관리해야 하며, 유지 보수, 릴리즈, 배포를 두 리포지터리에서 동시에 조율해야 하는 부담도 있습니다. 이런 문제들이 극복 불가능한 것은 아니지만, 생산적이고 즐거운 개발 방법이라고 생각되지는 않습니다.

<a name="inertia"></a>
### Inertia

다행히도 Laravel은 이 두 세계를 모두 경험할 수 있게 해줍니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 최신 Vue 또는 React 프론트엔드 사이의 다리를 놓아 줌으로써, Vue나 React를 사용해 완전한 최신식 프론트엔드를 구축하면서도 라우팅, 데이터 하이드레이션, 인증을 Laravel 라우트와 컨트롤러에서 처리할 수 있게 도와줍니다. 이 모든 기능을 단일 코드베이스 내에서 할 수 있습니다. 이 방식으로 Laravel과 Vue/React의 강력함을 서로 방해하지 않고 모두 누릴 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치한 후에는 기존처럼 라우트와 컨트롤러를 작성합니다. 다만 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 보통 `resources/js/Pages` 디렉터리에 저장되는 Vue 또는 React 컴포넌트에 대응됩니다. `Inertia::render` 메서드로 전달된 데이터는 페이지 컴포넌트의 "props" 하이드레이션에 사용됩니다:

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/vue3';

const props = defineProps(['user']);
</script>

<template>
    <Head title="User Profile" />

    <Layout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Profile
            </h2>
        </template>

        <div class="py-12">
            Hello, {{ user.name }}
        </div>
    </Layout>
</template>
```

이처럼 Inertia는 강력한 Vue나 React의 힘을 프론트엔드 구축에 그대로 활용하면서도, Laravel 기반 백엔드와 자바스크립트 프론트엔드 사이의 가벼운 연결고리를 제공합니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요한 경우 Inertia 사용에 걱정할 필요 없습니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포하면, Inertia의 서버 사이드 렌더링 프로세스를 항상 실행 상태로 유지하기 매우 쉽습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷 (Starter Kits)

Inertia와 Vue / React를 사용해 프론트엔드를 구축하고 싶다면, Breeze 또는 Jetstream [스타터 킷](/docs/10.x/starter-kits#breeze-and-inertia)을 활용해 애플리케이션 개발을 빠르게 시작하세요. 이 스타터 킷들은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용해 백엔드와 프론트엔드 인증 흐름을 스캐폴딩해 주어 곧바로 다음 아이디어 개발에 돌입할 수 있습니다.

<a name="bundling-assets"></a>
## 자산 번들링 (Bundling Assets)

Blade와 Livewire로 프론트엔드를 개발하든, Vue / React와 Inertia를 사용하든, 애플리케이션의 CSS를 프로덕션용 자산으로 번들링할 필요가 있을 것입니다. 물론 Vue나 React로 프론트엔드를 만들 경우, 컴포넌트를 브라우저에서 실행 가능한 자바스크립트 자산으로도 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 자산을 번들링합니다. Vite는 현저히 빠른 빌드 속도와 로컬 개발 중 즉각적인 핫 모듈 교체(HMR)를 제공합니다. 모든 신규 Laravel 애플리케이션, 특히 [스타터 킷](/docs/10.x/starter-kits)에는 Vite와 함께 사용하기 좋은 경량 Laravel Vite 플러그인을 로드하는 `vite.config.js` 파일이 포함되어 있습니다.

Laravel과 Vite를 가장 빠르게 시작하는 방법은, 가장 간단한 스타터 킷인 [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze)를 이용해 백엔드와 프론트엔드 인증 스캐폴딩부터 시작하는 것입니다.

> [!NOTE]  
> Laravel과 함께 Vite 사용법에 관한 더 자세한 문서는 [자산 번들링 및 컴파일 전용 문서](/docs/10.x/vite)를 참고하세요.