# 프런트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [Vue / React 사용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [자산 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 현대적인 웹 애플리케이션을 구축하는 데 필요한 [라우팅](/docs/9.x/routing), [유효성 검증](/docs/9.x/validation), [캐시](/docs/9.x/cache), [큐](/docs/9.x/queues), [파일 저장](/docs/9.x/filesystem) 등 다양한 기능을 제공하는 백엔드 프레임워크입니다. 하지만 우리는 개발자에게 프런트엔드 개발을 위한 강력한 방법을 포함한 아름다운 풀스택 경험을 제공하는 것이 중요하다고 믿습니다.

Laravel로 애플리케이션을 구축할 때 프런트엔드 개발에 접근하는 두 가지 주요 방법이 있으며, 어떤 방식을 선택할지는 PHP를 활용해 프런트엔드를 구축할지, 아니면 Vue나 React 같은 자바스크립트 프레임워크를 사용할지에 따라 결정됩니다. 아래에서 이 두 옵션을 모두 소개하니, 자신의 애플리케이션에 가장 적합한 프런트엔드 개발 방식을 선택하는 데 도움이 될 것입니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP & Blade)

과거 대부분의 PHP 애플리케이션은 요청 시 데이터베이스에서 가져온 데이터를 PHP `echo` 문과 섞어 단순한 HTML 템플릿으로 브라우저에 HTML을 렌더링했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이런 HTML 렌더링 방식을 [views](/docs/9.x/views)와 [Blade](/docs/9.x/blade)를 사용해 여전히 구현할 수 있습니다. Blade는 데이터 출력, 반복문 처리 등을 간편하게 할 수 있는 매우 가벼운 템플릿 언어로, 짧고 편리한 문법을 제공합니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이 방식으로 애플리케이션을 구축할 때, 폼 제출이나 페이지 상호작용 후 서버로부터 완전히 새로운 HTML 문서를 받아 브라우저가 전체 페이지를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션에서 간단한 Blade 템플릿만으로 프런트엔드를 구축하는 방식이 충분히 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 점점 높아지는 기대감

하지만 웹 애플리케이션에 대한 사용자 기대가 발전하면서, 많은 개발자는 좀 더 다이내믹하고 다듬어진 사용자 경험을 제공하는 프런트엔드를 필요로 하게 되었습니다. 이런 이유로 일부 개발자는 Vue나 React 같은 자바스크립트 프레임워크를 사용해 애플리케이션의 프런트엔드를 구축하기 시작했습니다.

반면 자신이 익숙한 백엔드 언어만으로도 현대적인 웹 UI를 구축할 수 있도록 하는 솔루션도 개발되어 왔습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 이런 방향을 제시합니다.

Laravel 생태계 내에서는 PHP 중심으로 현대적이고 동적인 프런트엔드를 구축할 필요성으로 인해 [Laravel Livewire](https://laravel-livewire.com)과 [Alpine.js](https://alpinejs.dev/)가 탄생했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://laravel-livewire.com)는 Vue나 React 같은 최신 자바스크립트 프레임워크로 만든 프런트엔드처럼 동적이고 모던하며 생동감 있는 Laravel 기반 프런트엔드를 구축할 수 있게 해주는 프레임워크입니다.

Livewire를 사용할 때는 UI의 특정 부분을 담당하는 Livewire "컴포넌트"를 작성하며, 이 컴포넌트는 메서드와 데이터를 노출하여 애플리케이션의 프런트엔드에서 호출하거나 상호작용할 수 있습니다. 예를 들면, 간단한 "카운터" 컴포넌트는 다음과 같습니다:

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

그리고 이 카운터에 대응하는 템플릿은 다음과 같이 작성할 수 있습니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피, Livewire는 `wire:click` 같은 새로운 HTML 속성을 작성해 Laravel 프런트엔드와 백엔드를 연결할 수 있도록 합니다. 또한, 컴포넌트의 현재 상태는 간단한 Blade 표현식을 통해 렌더링할 수 있습니다.

많은 개발자에게 Livewire는 Laravel 내에서 편안함을 유지하면서도 현대적이고 동적인 웹 애플리케이션을 구축할 수 있게 해주는 혁신적인 도구가 되었습니다. 보통 Livewire를 사용하는 개발자는 [Alpine.js](https://alpinejs.dev/)도 함께 사용해, 다이얼로그 창 같은 JavaScript가 필요한 부분에만 적절히 스크립트를 추가하곤 합니다.

Laravel을 처음 사용하는 분이라면, 먼저 [views](/docs/9.x/views)와 [Blade](/docs/9.x/blade)의 기본 사용법을 익히는 것을 추천합니다. 이후 공식 [Laravel Livewire 문서](https://laravel-livewire.com/docs)를 참고하여 인터랙티브한 Livewire 컴포넌트를 통해 애플리케이션을 한 단계 발전시키는 방법을 배우세요.

<a name="php-starter-kits"></a>
### 스타터 키트 (Starter Kits)

PHP와 Livewire를 사용해 프런트엔드를 구축하려면, Breeze 또는 Jetstream [스타터 키트](/docs/9.x/starter-kits)를 활용해 빠르게 애플리케이션 개발을 시작할 수 있습니다. 이들 스타터 키트는 [Blade](/docs/9.x/blade)와 [Tailwind](https://tailwindcss.com)를 사용해 백엔드와 프런트엔드 인증 흐름을 스캐폴딩해 주므로, 바로 다음 아이디어 구현에 집중할 수 있습니다.

<a name="using-vue-react"></a>
## Vue / React 사용하기 (Using Vue / React)

Laravel과 Livewire로도 현대적인 프런트엔드 구축이 가능하지만, 많은 개발자는 여전히 Vue나 React 같은 자바스크립트 프레임워크를 활용하는 것을 선호합니다. 이를 통해 NPM을 통한 풍부한 자바스크립트 패키지와 도구를 최대한 활용할 수 있기 때문입니다.

하지만 별도의 도구 없이 Laravel과 Vue 또는 React를 조합하면 클라이언트 사이드 라우팅, 데이터 하이드레이션(hydration), 인증 처리 등 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/)나 [Next](https://nextjs.org/) 같은 특정 Vue/React 프레임워크를 사용해 많이 간소화할 수 있지만, 데이터 하이드레이션과 인증은 Laravel과 이들 프런트엔드 프레임워크를 결합할 때 여전히 어려운 과제로 남습니다.

또한 개발자는 두 개의 분리된 코드 저장소를 관리해야 하며, 유지보수, 출시, 배포를 양쪽에서 조율해야 하는 번거로움이 있습니다. 비록 이런 문제들이 불가능한 것은 아니지만, 생산적이거나 즐거운 개발 환경이라고 보기 어렵다고 생각합니다.

<a name="inertia"></a>
### Inertia

다행히 Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 Vue 혹은 React 프런트엔드 사이의 다리를 만들어 줍니다. 이를 통해 Vue나 React로 완전한 모던 프런트엔드를 구축하면서, 라우팅, 데이터 하이드레이션, 인증 등은 Laravel의 라우트와 컨트롤러를 활용해 처리할 수 있습니다. 그리고 모든 것을 한 코드 저장소에서 관리할 수 있습니다. 이 방법으로 Laravel과 Vue/React 두 도구의 강점을 모두 누릴 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치한 이후에는 기존처럼 라우트와 컨트롤러를 작성하되, 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     *
     * @param  int  $id
     * @return \Inertia\Response
     */
    public function show($id)
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 보통 애플리케이션 내 `resources/js/Pages` 디렉토리에 저장된 Vue 또는 React 컴포넌트에 해당하며, `Inertia::render` 메서드를 통해 제공된 데이터는 페이지 컴포넌트의 "props"를 하이드레이트하는 데 사용됩니다:

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/inertia-vue3';

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

보시다시피 Inertia는 Laravel 기반 백엔드와 자바스크립트 기반 프런트엔드 사이에 가벼운 다리를 제공하면서, Vue나 React의 전반적인 능력을 최대한 활용해 프런트엔드를 구축할 수 있게 합니다.

#### 서버 사이드 렌더링

Inertia 사용이 걱정되는 이유가 여러분의 애플리케이션이 서버 사이드 렌더링을 필요로 하기 때문이라면 안심해도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공하며, [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포하면 Inertia의 서버 사이드 렌더링 프로세스가 항상 실행되도록 간단히 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트 (Starter Kits)

Inertia와 Vue / React를 사용해 프런트엔드를 구축하려면, Breeze 또는 Jetstream [스타터 키트](/docs/9.x/starter-kits#breeze-and-inertia)를 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 키트들은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용해 백엔드 및 프런트엔드 인증 흐름을 스캐폴딩해 줍니다. 덕분에 즉시 다음 프로젝트 아이디어 구현에 집중할 수 있습니다.

<a name="bundling-assets"></a>
## 자산 번들링 (Bundling Assets)

Blade와 Livewire를 사용하든 Vue / React와 Inertia를 사용하든, 애플리케이션의 CSS를 프로덕션 환경에 맞게 번들링해야 할 필요가 있습니다. 물론 Vue 또는 React로 프런트엔드를 구축하는 경우, 컴포넌트를 브라우저에 맞는 JavaScript 자산으로도 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 자산을 번들링합니다. Vite는 초고속 빌드 속도와 로컬 개발 중 거의 즉각적인 핫 모듈 교체(HMR)를 제공합니다. 모든 새로운 Laravel 애플리케이션, 특히 [스타터 키트](/docs/9.x/starter-kits)를 사용하는 경우 `vite.config.js` 파일을 찾아볼 수 있는데, 이 파일은 Laravel Vite 플러그인을 로드하여 Laravel 프로젝트에서 Vite를 편리하게 사용할 수 있게 합니다.

Laravel과 Vite를 시작하는 가장 빠른 방법은 프런트엔드 및 백엔드 인증 스캐폴딩을 제공하는 가장 간단한 스타터 키트인 [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze)를 사용해 애플리케이션 개발을 시작하는 것입니다.

> [!NOTE]
> Laravel과 Vite를 함께 사용하는 방법에 대한 자세한 문서는 [자산 번들링 및 컴파일에 관한 전용 문서](/docs/9.x/vite)도 참조하세요.