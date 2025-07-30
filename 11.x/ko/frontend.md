# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [Vue / React 사용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/11.x/routing), [유효성 검사](/docs/11.x/validation), [캐싱](/docs/11.x/cache), [큐](/docs/11.x/queues), [파일 저장소](/docs/11.x/filesystem) 등 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 우리는 개발자들에게 강력한 프론트엔드 구축 방식을 포함하는 아름다운 풀스택 경험을 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 구축할 때 프론트엔드 개발에 접근하는 기본적인 방법은 두 가지가 있으며, 어떤 방법을 선택할지는 PHP를 활용해 프론트엔드를 구성할지 또는 Vue, React 같은 자바스크립트 프레임워크를 사용할지에 따라 결정됩니다. 아래에서 두 가지 옵션을 모두 살펴보고 여러분의 애플리케이션에 가장 적합한 프론트엔드 개발 방식을 선택하는 데 도움이 될 것입니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP and Blade)

과거 대부분의 PHP 애플리케이션은 요청 시 데이터베이스에서 조회한 데이터를 출력하는 PHP `echo` 문이 섞인 간단한 HTML 템플릿을 사용해 브라우저에 HTML을 렌더링했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이와 같은 HTML 렌더링 방식이 [뷰](/docs/11.x/views)와 [Blade](/docs/11.x/blade)를 통해 여전히 가능합니다. Blade는 데이터 출력, 반복 처리 등 편리하고 간결한 문법을 제공하는 매우 가벼운 템플릿 언어입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이런 방식으로 애플리케이션을 구축할 경우, 폼 제출이나 다른 페이지 상호작용은 보통 서버에서 완전한 새 HTML 문서를 받아 브라우저가 전체 페이지를 다시 렌더링합니다. 지금도 많은 애플리케이션이 간단한 Blade 템플릿만으로 프론트엔드를 구성하는 데 전혀 문제가 없습니다.

<a name="growing-expectations"></a>
#### 커져가는 기대감

그러나 웹 애플리케이션에 대한 사용자 기대가 높아지면서, 더 다이내믹하고 세련된 상호작용이 가능한 프론트엔드를 만들어야 한다는 필요성을 느끼는 개발자가 많아졌습니다. 이런 흐름에 맞춰 일부 개발자는 Vue, React 같은 자바스크립트 프레임워크로 프론트엔드를 구축하기 시작했습니다.

반면 자신이 익숙한 백엔드 언어를 계속 사용하고 싶어 하는 개발자들은, 주로 백엔드 언어를 사용하면서도 현대적인 웹 애플리케이션 UI를 구축할 수 있도록 하는 해결책들을 만들어 냈습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 등의 라이브러리가 이러한 요구에서 탄생했습니다.

Laravel 생태계에서는 PHP를 주로 사용해 현대적이고 동적인 프론트엔드를 구축해야 할 필요성이 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)를 탄생시켰습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Laravel 기반의 프론트엔드를 자바스크립트 프레임워크(Vue, React)로 구축한 것처럼 동적이고 현대적으로 느껴지도록 만드는 프레임워크입니다.

Livewire를 사용할 때는 UI의 특정 부분을 렌더링하고, 메서드와 데이터를 외부에서 호출하거나 상호작용할 수 있는 Livewire "컴포넌트"를 생성합니다. 예를 들어, 간단한 "Counter" 컴포넌트는 아래와 같습니다:

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

이와 대응하는 템플릿은 다음과 같이 작성합니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

Livewire는 Laravel 프론트엔드와 백엔드를 연결하는 `wire:click` 같은 새로운 HTML 속성들을 쓸 수 있게 해줍니다. 또한 컴포넌트의 현재 상태를 간단한 Blade 표현식으로 렌더링할 수 있습니다.

많은 개발자에게 Livewire는 Laravel 환경 내에서 벗어나지 않고도 현대적이고 동적인 웹 애플리케이션을 구축할 수 있게 해주어 프론트엔드 개발의 혁신을 일으켰습니다. 보통 Livewire를 사용하는 개발자는 필요한 부분에만 [Alpine.js](https://alpinejs.dev/)를 덧붙여, 예를 들어 다이얼로그 창 렌더링 등의 단순한 자바스크립트 효과를 구현합니다.

Laravel을 처음 접한다면, 우선 [뷰](/docs/11.x/views)와 [Blade](/docs/11.x/blade)의 기본 사용법을 익히기를 추천합니다. 이후 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고해 인터랙티브 Livewire 컴포넌트 구성법을 배워 애플리케이션을 한 단계 끌어올리세요.

<a name="php-starter-kits"></a>
### 스타터 킷 (Starter Kits)

PHP와 Livewire를 사용해 프론트엔드를 구축하고 싶다면, Breeze나 Jetstream [스타터 킷](/docs/11.x/starter-kits)을 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 두 스타터 킷 모두 [Blade](/docs/11.x/blade)와 [Tailwind](https://tailwindcss.com)를 사용해 백엔드와 프론트엔드 인증 흐름의 골격을 만들어 주기 때문에 바로 다음 아이디어 구현에 집중할 수 있습니다.

<a name="using-vue-react"></a>
## Vue / React 사용하기 (Using Vue / React)

Laravel과 Livewire로도 현대적인 프론트엔드 개발이 가능하지만, 많은 개발자가 여전히 Vue나 React와 같은 자바스크립트 프레임워크를 활용하길 선호합니다. 이는 NPM을 통한 방대한 자바스크립트 패키지 및 도구 생태계의 이점을 누릴 수 있기 때문입니다.

하지만 추가 도구 없이는 Laravel과 Vue 또는 React를 조합할 경우, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 같은 복잡한 문제를 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/), [Next](https://nextjs.org/) 같은 Vue/React에 특화된 프레임워크 덕분에 많이 간소화되었으나, 데이터 하이드레이션 및 인증 문제는 Laravel 같은 백엔드 프레임워크와 결합할 때 여전히 해결하기 어렵고 까다로운 과제입니다.

게다가 두 개의 별도 코드 저장소를 유지하며, 각 저장소의 유지보수, 릴리즈, 배포를 조율해야 하는 부담도 있습니다. 이런 문제들이 불가능한 것은 아니지만, 효율적이고 즐거운 개발 방법이라고 보기는 어렵습니다.

<a name="inertia"></a>
### Inertia

다행히 Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 Vue 또는 React 프론트엔드 사이의 다리 역할을 하여, Vue 또는 React를 사용해 완전한 현대적 프론트엔드를 구축하면서도 라우팅, 데이터 하이드레이션, 인증에 Laravel의 라우트와 컨트롤러를 그대로 활용할 수 있게 해줍니다. 이 모든 것이 단일 코드 저장소 내에서 이루어집니다. 덕분에 Laravel과 Vue / React 양쪽의 강력한 기능을 온전히 누릴 수 있습니다.

Inertia를 Laravel 애플리케이션에 설치한 뒤에는 평소처럼 라우트와 컨트롤러를 작성합니다. 그러나 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다:

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

Inertia 페이지는 보통 애플리케이션의 `resources/js/Pages` 디렉터리에 저장된 Vue 또는 React 컴포넌트에 대응합니다. `Inertia::render`로 전달된 데이터는 해당 페이지 컴포넌트의 "props"를 하이드레이트하는 데 사용됩니다:

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

보시다시피, Inertia는 Laravel 백엔드와 자바스크립트 프론트엔드 간 경량 브릿지를 제공하면서 Vue 또는 React의 모든 강력한 기능을 활용할 수 있게 합니다.

#### 서버 사이드 렌더링

Inertia에 도전하는 것이 부담스럽거나 서버 사이드 렌더링이 필요한 애플리케이션이라면 걱정하지 마세요. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한, [Laravel Forge](https://forge.laravel.com)를 통한 배포 시 Inertia의 서버 사이드 렌더링 프로세스가 항상 실행되도록 쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷 (Starter Kits)

Inertia와 Vue / React를 사용해 프론트엔드를 구축하고 싶다면, Breeze나 Jetstream [스타터 킷](/docs/11.x/starter-kits#breeze-and-inertia)을 활용해 애플리케이션 개발을 시작할 수 있습니다. 이 두 스타터 킷은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용해 백엔드와 프론트엔드 인증 흐름을 동시에 구성해 줘 바로 다음 아이디어에 집중할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링 (Bundling Assets)

Blade와 Livewire, 또는 Vue / React와 Inertia 중 어떤 프론트엔드 개발 방식을 선택하든, 보통 애플리케이션의 CSS를 프로덕션용으로 번들링해야 합니다. 물론 Vue 또는 React를 선택했다면 컴포넌트들을 브라우저가 실행 가능한 자바스크립트 에셋으로 번들링할 필요도 있습니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 에셋을 번들링합니다. Vite는 매우 빠른 빌드 시간과 개발 중 거의 즉시 적용 가능한 핫 모듈 교체(HMR)를 제공합니다. 새로운 모든 Laravel 애플리케이션에서는 [스타터 킷](/docs/11.x/starter-kits)을 포함해 `vite.config.js` 파일을 확인할 수 있는데, 이는 Laravel Vite 플러그인을 가볍게 불러와 Laravel 애플리케이션에서 Vite 사용이 매우 편리하도록 해줍니다.

Laravel과 Vite를 가장 빠르게 시작하려면 백엔드와 프론트엔드 인증 골격을 제공하는 가장 간단한 스타터 킷인 [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)로 애플리케이션 개발을 시작하세요.

> [!NOTE]  
> Laravel과 함께 Vite를 활용하는 방법에 대한 자세한 문서는 [에셋 번들링 및 컴파일 관련 전용 문서](/docs/11.x/vite)를 참고하세요.