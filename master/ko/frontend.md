# 프론트엔드

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/{{version}}/routing), [검증](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 저장소](/docs/{{version}}/filesystem) 등과 같은 최신 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 저희는 개발자들에게 애플리케이션의 프론트엔드를 아름답고 강력하게 구축할 수 있는 전체 스택 경험을 제공하는 것 또한 중요하다고 생각합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드 개발을 접근하는 두 가지 주요 방법이 있습니다. 어떤 방법을 선택할지는 PHP를 활용할지, 아니면 Vue나 React 같은 자바스크립트 프레임워크를 사용할지에 따라 결정됩니다. 아래에서 두 가지 선택지를 모두 설명하므로, 애플리케이션의 프론트엔드 개발에 가장 적합한 방식을 현명하게 선택하실 수 있습니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP와 Blade

과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 요청 시 가져온 데이터를 PHP의 `echo` 문을 섞은 단순 HTML 템플릿으로 브라우저에 HTML을 렌더링했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이러한 방식의 HTML 렌더링을 [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)를 사용해 구현할 수 있습니다. Blade는 데이터를 출력하거나, 데이터를 반복하는 등 편리한 짧은 문법을 제공하는 매우 경량의 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이런 방식으로 애플리케이션을 구축하면, 폼 전송이나 기타 페이지 상호작용 시 서버로부터 완전히 새로운 HTML 문서를 받아오며 브라우저가 전체 페이지를 다시 렌더링하게 됩니다. 오늘날에도 많은 애플리케이션이 단순한 Blade 템플릿을 이용해 프론트엔드를 구성하는 방식에 충분히 적합합니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자 기대치가 높아지면서, 더욱 역동적이고 세련된 상호작용이 필요한 프론트엔드를 구축해야 하는 경우가 많아졌습니다. 이런 이유로, 일부 개발자들은 Vue나 React와 같은 자바스크립트 프레임워크를 사용해 프론트엔드를 구축하기 시작했습니다.

한편, 자신이 익숙한 백엔드 언어를 고수하고자 하는 개발자들은 주로 백엔드 언어를 활용하면서도 현대적인 웹 애플리케이션 UI를 만들 수 있는 솔루션을 개발해 왔습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 등장했습니다.

Laravel 생태계에서도 PHP를 주로 사용하여 동적이고 현대적인 프론트엔드를 구축하려는 니즈가 [Laravel Livewire](https://livewire.laravel.com) 및 [Alpine.js](https://alpinejs.dev/)를 탄생시켰습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 현대적인 자바스크립트 프레임워크인 Vue나 React로 구축한 프론트엔드처럼 동적이고 살아있는 프론트엔드를 Laravel 위에서 구현할 수 있게 해 주는 프레임워크입니다.

Livewire를 사용하면 UI의 독립적인 부분을 렌더링하고 프론트엔드에서 호출 및 상호작용할 수 있는 메서드와 데이터를 노출하는 Livewire "컴포넌트"를 작성하게 됩니다. 예를 들어 간단한 "카운터" 컴포넌트는 다음과 같습니다.

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

이에 대응하는 카운터 템플릿은 다음과 같이 작성할 수 있습니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피, Livewire를 사용하면 `wire:click`과 같은 새로운 HTML 속성을 작성해 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결할 수 있습니다. 또한, Blade의 간단한 표현식을 사용해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

많은 개발자들에게 Livewire는 Laravel 프론트엔드 개발의 혁신을 가져왔습니다. Laravel의 익숙한 환경을 떠나지 않고도 현대적이고 동적인 웹 애플리케이션을 개발할 수 있게 해줍니다. 보통 Livewire를 사용하는 개발자들은 [Alpine.js](https://alpinejs.dev/)도 함께 활용하여, 다이얼로그 창 렌더링 등 필요한 부분에만 최소한으로 자바스크립트를 추가합니다.

Laravel을 처음 접하신 경우, [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)의 기본 사용법에 익숙해지는 것이 좋습니다. 그 후, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여, 상호작용이 가능한 Livewire 컴포넌트로 애플리케이션을 한 단계 업그레이드해 보세요.

<a name="php-starter-kits"></a>
### 스타터 키트

PHP와 Livewire로 프론트엔드를 구축하고 싶다면, [Livewire 스타터 키트](/docs/{{version}}/starter-kits)를 활용하여 애플리케이션 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기

Laravel과 Livewire를 사용해 현대적인 프론트엔드를 개발할 수 있긴 하지만, 여전히 많은 개발자들은 React나 Vue 같은 강력한 자바스크립트 프레임워크를 선호합니다. 이는 NPM을 통해 제공되는 다양한 자바스크립트 패키지 및 도구의 풍부한 생태계를 활용할 수 있기 때문입니다.

하지만 추가적인 도구 없이 Laravel과 React/Vue를 연동하려면 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 다양한 복잡한 문제를 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/)와 같은 견해가 강한 React/Vue 프레임워크를 사용하면 간단해지지만, 데이터 하이드레이션과 인증 문제는 여전히 해결하기 어렵습니다.

게다가, 개발자들은 백엔드와 프론트엔드의 별도 코드 저장소를 관리해야 하며, 유지보수, 릴리즈, 배포를 양쪽 저장소에서 일관성 있게 처리해야 하는 부담도 있습니다. 이런 문제들이 극복 불가능한 것은 아니지만, 저희는 이런 방식이 생산적이거나 즐거운 개발 방법이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히도 Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 React 또는 Vue 프론트엔드 사이를 연결하는 다리 역할을 합니다. Inertia를 사용하면 React 또는 Vue를 통해 완전한 프론트엔드를 구축하면서도, 라우팅·데이터 하이드레이션·인증 등은 Laravel의 라우트와 컨트롤러를 그대로 이용할 수 있습니다. 이 모든 것이 하나의 코드 저장소에서 이루어지죠. 이런 방식 덕분에, 어느 쪽의 장점도 희생하지 않고 Laravel과 React/Vue의 모든 힘을 누릴 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치한 후에는 기존과 동일하게 라우트와 컨트롤러를 작성합니다. 다만 컨트롤러에서 Blade 템플릿 대신 Inertia 페이지를 반환합니다.

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

Inertia 페이지는 React 또는 Vue 컴포넌트에 해당하며, 일반적으로 애플리케이션의 `resources/js/pages` 디렉터리에 위치합니다. `Inertia::render` 메서드를 통해 전달된 데이터는 페이지 컴포넌트의 "props"로 전달되어 하이드레이션에 사용됩니다.

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

보시다시피, Inertia는 프론트엔드 개발 시 React 또는 Vue의 힘을 온전히 안전하면서, Laravel 기반 백엔드와 자바스크립트 프론트엔드를 가볍게 연결해주는 다리 역할을 합니다.

#### 서버 사이드 렌더링

애플리케이션에서 서버 사이드 렌더링이 필요한 경우 Inertia를 도입하는 것이 걱정되신다면, 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포할 때도 Inertia의 서버 사이드 렌더링을 간편하게 운영할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트

Inertia와 Vue/React를 사용해 프론트엔드를 구축하려면 [React 또는 Vue 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 두 가지 스타터 키트 모두 Inertia, Vue/React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 조합해 백엔드와 프론트엔드 인증 플로우를 스캐폴딩하므로, 곧바로 다음 아이디어를 바로 구현할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 Livewire를 사용할지, Vue/React와 Inertia를 사용할지와 상관없이, 애플리케이션의 CSS를 운영 환경에 맞는 번들 에셋으로 묶어야 할 필요가 있습니다. 그리고 프론트엔드를 Vue나 React로 구축했다면, 브라우저에서 사용할 수 있도록 컴포넌트도 자바스크립트 번들로 묶어야 합니다.

기본적으로 Laravel은 에셋 번들링 도구로 [Vite](https://vitejs.dev)를 사용합니다. Vite는 번개처럼 빠른 빌드 속도와 로컬 개발 시 거의 즉각적인 Hot Module Replacement(HMR)를 제공합니다. 새로운 Laravel 애플리케이션(스타터 키트 포함)을 시작하면 `vite.config.js` 파일 내에 가볍고 편리한 Laravel Vite 플러그인이 미리 적용되어 있으므로, Vite와의 연동이 매우 쉽습니다.

Laravel과 Vite로 빠르게 시작하려면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)로 개발을 시작해 보세요. 스타터 키트는 프론트엔드와 백엔드 인증 스캐폴딩을 제공해 애플리케이션 개발을 한층 빠르게 도와줍니다.

> [!NOTE]
> Laravel에서 Vite 사용 및 에셋 번들링에 대한 더 자세한 문서는 [에셋 번들링 및 컴파일에 대한 전용 문서](/docs/{{version}}/vite)를 참고해 주세요.