# 프런트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [자산 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/master/routing), [유효성 검증](/docs/master/validation), [캐시](/docs/master/cache), [큐](/docs/master/queues), [파일 저장](/docs/master/filesystem) 등 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 그러나 개발자에게 강력한 프런트엔드 구축 방식을 포함한 아름다운 풀스택 경험을 제공하는 것도 중요하다고 믿습니다.

Laravel에서 프런트엔드 개발에 접근하는 두 가지 주요 방법이 있으며, 어느 방식을 선택할지는 PHP를 활용해 프런트엔드를 구축할지, Vue나 React 같은 자바스크립트 프레임워크를 사용할지에 따라 결정됩니다. 아래에서 두 가지 옵션을 모두 살펴보고, 애플리케이션 프런트엔드 개발에 가장 적합한 방법을 결정할 수 있도록 안내합니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade

과거 대부분의 PHP 애플리케이션은 데이터베이스에서 가져온 데이터를 출력하는 PHP `echo` 문과 함께 간단한 HTML 템플릿을 사용해 브라우저에 HTML을 렌더링했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이 방식으로 HTML을 렌더링할 때 [뷰](/docs/master/views)와 [Blade](/docs/master/blade)를 사용할 수 있습니다. Blade는 매우 가벼운 템플릿 언어로서, 데이터를 표시하고, 반복문을 실행하는 등 편리하고 간결한 문법을 제공합니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이렇게 애플리케이션을 구축할 때는 폼 제출이나 페이지 내 다른 상호작용 시 보통 서버로부터 완전한 새로운 HTML 문서를 받아 브라우저가 전체 페이지를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션이 단순한 Blade 템플릿으로 프런트엔드를 구성하는 데 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 커져가는 기대감

하지만 사용자들이 웹 애플리케이션에 기대하는 수준이 높아짐에 따라, 더 세련되고 동적인 프런트엔드를 구축해야 할 필요성을 느끼는 개발자가 많아졌습니다. 이런 이유로 많은 개발자가 Vue나 React 같은 자바스크립트 프레임워크로 프런트엔드를 개발하기 시작합니다.

반면, 자신이 익숙한 백엔드 언어를 유지하면서도 현대적인 웹 UI를 구축할 수 있도록 하는 솔루션도 개발되었습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 탄생했습니다.

Laravel 생태계 내에서는 PHP 중심으로 현대적이고 동적인 프런트엔드를 구축하려는 필요성에 따라 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 만들어졌습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React 같은 최신 자바스크립트 프레임워크로 구축한 것처럼 동적이고 현대적이며 생동감 있는 Laravel 프런트엔드를 만들 수 있는 프레임워크입니다.

Livewire를 사용하면 UI의 특정 부분을 렌더링하는 Livewire "컴포넌트"를 만들고, 애플리케이션의 프런트엔드에서 호출 및 상호작용할 수 있는 메서드와 데이터를 노출할 수 있습니다. 예를 들어, 간단한 "Counter" 컴포넌트는 다음과 같습니다:

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

그리고 이에 대응하는 카운터 템플릿은 이렇게 작성할 수 있습니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피, Livewire는 Laravel 애플리케이션의 프런트엔드와 백엔드를 연결하는 `wire:click` 같은 새로운 HTML 속성을 작성할 수 있게 해줍니다. 또한 단순한 Blade 표현식을 사용해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

많은 이들에게 Livewire는 Laravel 내에서 머물면서도 현대적이고 동적인 웹 애플리케이션을 만들 수 있도록 프런트엔드 개발 방식을 혁신했습니다. 보통 Livewire를 사용하는 개발자들은 [Alpine.js](https://alpinejs.dev/)를 함께 활용해, 다이얼로그 창 같은 꼭 필요한 부분에만 간단한 자바스크립트를 추가해 사용합니다.

Laravel 초보자라면 기본적인 [뷰](/docs/master/views)와 [Blade](/docs/master/blade) 사용법에 익숙해진 후, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고해 인터랙티브한 Livewire 컴포넌트로 애플리케이션을 한 단계 업그레이드하는 방법을 배울 것을 권장합니다.

<a name="php-starter-kits"></a>
### 스타터 킷 (Starter Kits)

PHP와 Livewire를 이용해 프런트엔드를 개발하려면, [Livewire 스타터 킷](/docs/master/starter-kits)을 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기 (Using React or Vue)

Laravel과 Livewire로도 현대적인 프런트엔드를 만들 수 있지만, 여전히 많은 개발자가 React나 Vue 같은 자바스크립트 프레임워크의 강력함을 활용하는 것을 선호합니다. 이렇게 하면 NPM을 통해 제공되는 다양한 자바스크립트 패키지와 도구들을 손쉽게 활용할 수 있습니다.

하지만 추가 도구 없이 Laravel과 React 혹은 Vue를 조합하면 클라이언트 사이드 라우팅, 데이터 하이드레이션(초기 데이터 주입), 인증 같은 복잡한 문제를 해결해야 합니다. 클라이언트 사이드 라우팅은 [Next](https://nextjs.org/)와 [Nuxt](https://nuxt.com/) 같은 특정 React/Vue 프레임워크를 사용하면 간소화되지만, 데이터 하이드레이션과 인증 문제는 여전히 백엔드 프레임워크인 Laravel과 프런트엔드 프레임워크를 함께 사용할 때 어려운 부분입니다.

또한 각각 별도의 코드 저장소를 관리해야 하며, 두 저장소 간 유지보수, 배포, 릴리즈를 조율해야 하는 번거로움도 있습니다. 물론 이런 문제들이 해결 불가능한 것은 아니지만, 효과적이고 즐거운 개발 방식이라고 보기는 어렵습니다.

<a name="inertia"></a>
### Inertia

다행히 Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 React나 Vue 프런트엔드 사이를 잇는 다리 역할을 하며, 라우팅, 데이터 하이드레이션, 인증 등을 위해 Laravel의 라우트와 컨트롤러를 사용하면서도 React나 Vue로 완전한 현대적 프런트엔드를 구축하게 해줍니다. 이 모든 것을 단일 코드 저장소에서 가능합니다. 이렇게 하면 Laravel과 React/Vue 두 도구의 기능을 최대한 활용하면서 어느 쪽도 기능상 제약받지 않는 개발이 가능합니다.

Laravel 애플리케이션에 Inertia를 설치한 후에는 보통처럼 라우트와 컨트롤러를 작성합니다. 그러나 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다:

```php
<?php

namespace App\Http\Controllers;

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
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 보통 애플리케이션의 `resources/js/pages` 디렉토리에 저장된 React 또는 Vue 컴포넌트에 대응합니다. `Inertia::render` 메서드를 통해 페이지에 전달하는 데이터는 페이지 컴포넌트의 "props"를 하이드레이션하는 데 사용됩니다:

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}
```

보시듯 Inertia는 React나 Vue의 강력함을 최대한 활용하면서도, Laravel을 백엔드로 사용하고 JavaScript 프런트엔드와 가볍게 연결하는 다리를 제공합니다.

#### 서버 사이드 렌더링

만약 서버 사이드 렌더링이 필요한 애플리케이션이라면 걱정하지 마십시오. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한 [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포하면 Inertia의 서버 사이드 렌더링 프로세스를 항상 쉽게 실행할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷 (Starter Kits)

Inertia와 Vue / React를 사용해 프런트엔드를 개발하려면 [React 또는 Vue 애플리케이션 스타터 킷](/docs/master/starter-kits)을 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이들 스타터 킷은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용해 백엔드와 프런트엔드 인증 흐름의 기본 구조를 제공하므로, 새로운 아이디어 개발을 바로 시작할 수 있습니다.

<a name="bundling-assets"></a>
## 자산 번들링 (Bundling Assets)

Blade와 Livewire로 프런트엔드를 개발하든, Vue / React와 Inertia로 개발하든, 애플리케이션의 CSS를 운영 환경에 맞게 번들링해야 할 필요가 있을 것입니다. 물론 Vue나 React로 프런트엔드를 개발하면 브라우저가 실행할 수 있는 자바스크립트 컴포넌트도 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 자산을 번들링합니다. Vite는 현지 개발 환경에서 매우 빠른 빌드 속도와 거의 즉각적인 핫 모듈 교체(HMR)를 제공합니다. 모든 새로운 Laravel 애플리케이션, 특히 [스타터 킷](/docs/master/starter-kits)을 사용하는 프로젝트에서는 `vite.config.js` 파일이 포함되어 있는데, 이 파일은 Laravel Vite 플러그인을 경량으로 불러와 Laravel과 Vite 사용을 편리하게 합니다.

Laravel과 Vite로 시작하는 가장 빠른 방법은 [애플리케이션 스타터 킷](/docs/master/starter-kits)으로 개발을 시작하는 것입니다. 이 킷은 프런트엔드와 백엔드 인증 기본 구조를 제공해 애플리케이션 개발을 빠르게 진행할 수 있게 돕습니다.

> [!NOTE]
> Vite와 Laravel을 함께 사용하는 자세한 문서는 [자산 번들링 및 컴파일 관련 문서](/docs/master/vite)를 참고하십시오.