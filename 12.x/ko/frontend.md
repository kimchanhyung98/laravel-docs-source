# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [React 또는 Vue 사용](#using-react-or-vue)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/12.x/routing), [유효성 검증](/docs/12.x/validation), [캐싱](/docs/12.x/cache), [큐](/docs/12.x/queues), [파일 스토리지](/docs/12.x/filesystem) 등 현대적인 웹 애플리케이션 개발에 필요한 모든 기능을 갖춘 백엔드 프레임워크입니다. 그러나 우리는 개발자가 강력하면서도 아름다운 풀스택 경험을 누릴 수 있도록, 애플리케이션의 프론트엔드 개발을 위한 강력한 방법들도 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드 개발을 진행하는 주요 방법은 두 가지가 있습니다. 어떤 방식을 선택할지는 여러분이 PHP를 활용하여 프론트엔드를 만들지, 혹은 Vue나 React와 같은 JavaScript 프레임워크를 사용할지에 따라 결정됩니다. 아래에서는 두 가지 옵션을 모두 다루므로, 여러분의 애플리케이션에 적합한 프론트엔드 개발 방식을 선택하는 데 참고하시기 바랍니다.

<a name="using-php"></a>
## PHP 사용 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP and Blade)

과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 요청 시 가져온 데이터를 `echo`문을 이용해 HTML 템플릿에 삽입하여 브라우저에 HTML을 렌더링했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)를 사용하여 여전히 이와 같은 방식으로 HTML을 렌더링할 수 있습니다. Blade는 데이터를 출력하거나 반복문을 사용할 때 간단하고 편리한 문법을 제공하는 매우 경량화된 템플릿 언어입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이러한 방식을 사용할 경우, 폼 제출 등 페이지와 상호작용이 발생하면 서버에서 전체 HTML 문서를 다시 받아오고, 브라우저가 페이지 전체를 다시 렌더링하게 됩니다. 실제로 오늘날에도 많은 애플리케이션이 이렇게 간단한 Blade 템플릿 관점에서 프론트엔드를 구성해도 충분합니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자의 기대치가 높아지고, 좀 더 다이나믹하고 세련된 프론트엔드 상호작용이 필요해지면서, 많은 개발자들이 Vue나 React와 같은 JavaScript 프레임워크를 활용해 프론트엔드를 구현하게 되었습니다.

반대로, 자신이 익숙한 백엔드 언어를 최대한 활용하고픈 개발자들은 여전히 PHP 등 기존 언어를 주로 사용하면서도 현대적이고 동적인 웹 UI를 만들 수 있는 솔루션을 개발하기도 했습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 등장했습니다.

Laravel 생태계에서도 PHP 중심의 현대적이고 동적인 프론트엔드를 만들고자 하는 수요가 높아지면서, [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 개발되었습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React로 개발한 프론트엔드처럼 동적이고 모던하며 생동감 있는 Laravel 기반 프론트엔드를 만들기 위한 프레임워크입니다.

Livewire를 사용하면 프론트엔드의 특정 UI 영역을 담당하는 Livewire "컴포넌트"를 만들 수 있으며, 이 컴포넌트는 다양한 메서드와 데이터를 외부(즉, 프론트엔드)에서 호출하고 조작할 수 있습니다. 예를 들어, 간단한 "Counter" 컴포넌트는 아래와 같이 구성됩니다:

```php
<?php

use Livewire\Component;

new class extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }
};
?>

<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>

```

위 예시처럼, Livewire를 사용하면 `wire:click`과 같은 새로운 HTML 속성을 활용하여 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결할 수 있습니다. 또한, 간단한 Blade 표현식을 통해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

Livewire는 많은 개발자에게 Laravel 환경을 벗어나지 않고도 현대적이고 동적인 웹 애플리케이션을 개발할 수 있도록 프론트엔드 개발의 새로운 패러다임을 열어주었습니다. 보통 Livewire를 사용하는 개발자들은 [Alpine.js](https://alpinejs.dev/)를 함께 사용하여, 예를 들어 다이얼로그 창 렌더링과 같이 필요한 곳에만 JavaScript를 "톡톡 뿌리는" 방식을 선호합니다.

Laravel가 처음이라면, [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)의 기본적인 사용법을 익힌 뒤, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여, 인터랙티브한 Livewire 컴포넌트를 통해 한 단계 더 발전된 애플리케이션을 만들어보시기 바랍니다.

<a name="php-starter-kits"></a>
### 스타터 킷 (Starter Kits)

PHP와 Livewire를 사용해 프론트엔드를 구축하고자 한다면, [Livewire 스타터 킷](/docs/12.x/starter-kits)을 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용 (Using React or Vue)

Laravel과 Livewire를 이용해 현대적인 프론트엔드를 구현할 수도 있지만, 여전히 많은 개발자들이 React나 Vue 같은 JavaScript 프레임워크의 강력함을 선호합니다. 이 방식을 선택하면, NPM을 통한 풍부한 JavaScript 패키지 및 툴 생태계도 함께 활용할 수 있습니다.

하지만 별도의 도구 없이 Laravel과 React/Vue를 직접 조합한다면, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/)와 같은 뚜렷한 방향성을 가진 프레임워크를 사용하여 간소화할 수 있지만, 데이터 하이드레이션과 인증 문제는 백엔드 프레임워크인 Laravel과 프론트엔드 프레임워크인 React/Vue의 조합에서는 여전히 어렵고 복잡합니다.

또한, 이 접근법의 경우 백엔드와 프론트엔드의 별도 코드 저장소를 별도로 관리해야 하므로, 유지보수, 릴리즈, 배포를 조율하는 작업이 필요합니다. 물론 이 문제들이 극복 불가능한 것은 아니지만, 이 방식이 생산적이거나 즐거운 개발 경험이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히도, Laravel은 두 가지 세계의 장점을 모두 활용할 수 있는 방법을 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 React/Vue로 개발한 최신 프론트엔드를 연결해주는 다리 역할을 하여, 하나의 코드 저장소에서 라우팅, 데이터 하이드레이션, 인증 등의 작업을 모두 Laravel의 라우트 및 컨트롤러 단에서 처리할 수 있게 해줍니다. 이를 통해 Laravel과 React/Vue의 강점을 모두 살릴 수 있습니다.

Inertia를 Laravel 애플리케이션에 설치하면, 기존과 동일하게 라우트와 컨트롤러를 작성할 수 있습니다. 다만, 컨트롤러에서 Blade 템플릿을 반환하는 대신, Inertia 페이지를 반환합니다:

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

Inertia 페이지는 일반적으로 애플리케이션의 `resources/js/pages` 디렉터리에 위치한 React 또는 Vue 컴포넌트와 매칭됩니다. `Inertia::render` 메서드로 전달되는 데이터는 페이지 컴포넌트의 "props"에 자동으로 할당되어 하이드레이션됩니다:

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

이처럼 Inertia를 사용하면 React 또는 Vue의 모든 기능을 프론트엔드에 활용하면서도, Laravel 기반 백엔드와 JavaScript 기반 프론트엔드를 가볍게 연결해 줄 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 꼭 필요해서 Inertia 도입이 걱정된다면, 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 그리고 [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)를 이용해 배포할 경우, Inertia의 서버 사이드 렌더링 프로세스를 항상 작동하도록 쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷 (Starter Kits)

Inertia와 Vue/React를 활용하여 프론트엔드 개발을 시작하고 싶다면, [React 또는 Vue 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 사용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 킷은 Inertia, Vue/React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 기반으로 한 백엔드 및 프론트엔드 인증 플로우를 자동으로 구성해 주므로, 여러분의 새로운 아이디어를 바로 구현할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링 (Bundling Assets)

Blade와 Livewire, 혹은 Vue/React와 Inertia를 이용하는 어떤 방식을 선택하든, 애플리케이션의 CSS를 프로덕션용 에셋으로 번들링할 필요가 있습니다. 그리고 Vue나 React로 프론트엔드를 개발한다면, 해당 컴포넌트 역시 브라우저에서 사용할 수 있는 JavaScript 에셋으로 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 이용해 에셋을 번들링합니다. Vite는 매우 빠른 빌드 속도와 실시간에 가까운 핫 모듈 교체(Hot Module Replacement, HMR)를 제공하여, 로컬 개발 효율성을 극대화합니다. 모든 최신 Laravel 애플리케이션(스타터 킷을 포함)에는 Vite와 연동되는 `vite.config.js` 파일이 기본 제공되어, Laravel 환경에서 Vite를 편하게 사용할 수 있습니다.

Laravel과 Vite로 개발을 시작하는 가장 빠른 방법은 바로 [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 사용하여, 프론트엔드와 백엔드 인증 스캐폴딩까지 한 번에 받는 것입니다.

> [!NOTE]
> Laravel에서 Vite를 활용하는 방법에 대해서는, [에셋 번들링 및 컴파일 전용 문서](/docs/12.x/vite)를 참고하시기 바랍니다.
