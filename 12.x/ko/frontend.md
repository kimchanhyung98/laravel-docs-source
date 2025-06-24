# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/12.x/routing), [유효성 검증](/docs/12.x/validation), [캐싱](/docs/12.x/cache), [큐](/docs/12.x/queues), [파일 저장소](/docs/12.x/filesystem) 등, 현대적인 웹 애플리케이션 개발에 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 저희는 개발자에게 강력하면서도 아름다운 전체 스택(full-stack) 경험을 제공하는 것도 중요하다고 생각하며, 이를 위해 프론트엔드 구축을 위한 다양한 방법 역시 지원합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드를 구축하는 주요 방법은 크게 두 가지입니다. 한 가지는 PHP를 활용하여 프론트엔드를 구현하는 방식이고, 다른 한 가지는 Vue나 React와 같은 JavaScript 프레임워크를 사용하는 방식입니다. 아래에서 두 가지 선택지를 모두 설명하니, 본인의 프로젝트에 가장 알맞은 프론트엔드 개발 방식을 선택하실 수 있을 것입니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP와 Blade

과거에는 대부분의 PHP 애플리케이션이 간단한 HTML 템플릿에 PHP의 `echo` 구문을 삽입하여 데이터베이스에서 조회한 데이터를 브라우저에 직접 HTML로 렌더링하는 방식이었습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이와 같은 방식의 HTML 렌더링을 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)를 통해 여전히 손쉽게 구현할 수 있습니다. Blade는 데이터를 출력하거나 반복 처리하는 등의 작업을 매우 간결하고 편리한 구문으로 제공하는, 매우 가벼운 템플릿 엔진입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이런 방식으로 애플리케이션을 만들 때, 폼 제출이나 기타 페이지 상호작용이 발생하면 서버에서 완전히 새로운 HTML 문서를 받아와 브라우저가 전체 페이지를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션의 프론트엔드는 이렇게 간단한 Blade 템플릿만으로 충분한 경우가 많습니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자들의 기대가 점점 높아지면서, 좀 더 다이나믹하고 세련된 프론트엔드를 구현하고자 하는 개발자들도 많아졌습니다. 이에 따라 일부 개발자들은 Vue, React와 같은 JavaScript 프레임워크를 활용하여 프론트엔드를 개발하는 방식을 선택하고 있습니다.

반면, 익숙한 백엔드 언어(PHP)를 선호하는 개발자들은 여전히 자신이 잘 아는 언어 위주로 현대적인 웹 UI를 구축할 수 있는 솔루션을 고안하기도 했습니다. 예를 들어, [Rails](https://rubyonrails.org/) 커뮤니티에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 생겨났습니다.

Laravel 생태계에서도 주로 PHP를 사용하면서도 모던하고 동적인 프론트엔드를 만들고자 하는 요구에 힘입어, [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 탄생했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Laravel을 기반으로, Vue나 React 같은 최신 JavaScript 프레임워크 못지않게 동적이고 현대적인 프론트엔드를 쉽게 구현할 수 있게 해주는 프레임워크입니다.

Livewire를 사용할 때는, UI의 독립적인 일부를 렌더링하고 프론트엔드에서 호출하거나 상호작용할 수 있도록 데이터와 메서드를 제공하는 "Livewire 컴포넌트"를 작성하게 됩니다. 예를 들어, 간단한 "카운터" 컴포넌트는 다음과 같이 만들 수 있습니다.

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

그리고 카운터의 템플릿은 다음과 같이 작성할 수 있습니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

위와 같이 Livewire를 사용하면, Laravel 애플리케이션의 프론트엔드와 백엔드를 연결해주는 `wire:click`과 같은 새로운 HTML 속성을 작성할 수 있습니다. 또한, 컴포넌트의 현재 상태는 간단한 Blade 표현식으로 출력할 수 있습니다.

많은 개발자들은 Livewire 덕분에, 익숙한 Laravel 환경 안에서 모던하고 동적인 웹 애플리케이션을 쉽게 개발할 수 있게 되었다고 평가합니다. 보통 Livewire 사용자들은 프론트엔드에서 오직 필요한 부분에만 [Alpine.js](https://alpinejs.dev/)를 활용해 자바스크립트 기능을 "조금씩" 더하는 방식으로 다이얼로그 창 등 특정 UI에 효과적으로 적용합니다.

Laravel을 처음 접하신다면, 먼저 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)의 기본 사용법을 익히는 것을 권장합니다. 이후 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여, Livewire 컴포넌트를 통해 좀 더 인터랙티브한 애플리케이션을 만드는 방법도 공부해보세요.

<a name="php-starter-kits"></a>
### 스타터 킷

PHP와 Livewire로 프론트엔드를 개발하고 싶다면, Laravel에서 제공하는 [Livewire 스타터 킷](/docs/12.x/starter-kits)을 사용하여 프로젝트의 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기

Laravel과 Livewire만으로도 모던한 프론트엔드를 만들 수 있지만, 여전히 많은 개발자들은 React나 Vue 같은 JavaScript 프레임워크의 생태계와 NPM에서 제공하는 다양한 패키지와 툴을 활용하고자 합니다.

그러나 별도의 추가 도구 없이 Laravel과 React 또는 Vue를 조합해서 개발하다 보면, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증과 같은 복잡한 문제들을 직접 해결해야 할 수도 있습니다. 클라이언트 사이드 라우팅은 보통 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/)와 같이 표준 방식을 정의한 React/Vue 프레임워크를 통해 좀 더 쉽게 처리할 수 있지만, 데이터 하이드레이션이나 인증은 백엔드 프레임워크(Laravel)와 프론트엔드 프레임워크를 함께 사용할 때 여전히 까다롭고 복잡한 문제로 남아 있습니다.

또한, 프론트엔드와 백엔드 코드를 별도의 저장소에서 관리하게 되면 각 저장소의 유지보수, 릴리즈, 배포도 각각 관리해야 하므로 작업 효율성이 떨어질 수 있습니다. 물론 이러한 문제들이 극복 불가능한 것은 아니지만, 저희는 이것이 생산적이거나 즐거운 개발 방식이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히도 Laravel은 이 두 가지 접근 방식의 장점을 모두 누릴 수 있는 솔루션을 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 React, Vue 기반의 최신 프론트엔드 사이를 연결해 주는 다리 역할을 합니다. 덕분에 라우팅, 데이터 하이드레이션, 인증 같은 주요 기능을 Laravel routes와 controllers를 통해 처리하면서도, 한 저장소에서 전체 React 또는 Vue 프론트엔드를 구축할 수 있습니다. 즉, Laravel과 React/Vue의 강점을 모두 제대로 활용할 수 있습니다.

Inertia를 Laravel에 설치한 후에는 기존과 동일하게 route와 controller를 작성할 수 있습니다. 다만 컨트롤러에서 Blade 템플릿 대신 Inertia 페이지를 반환하게 됩니다.

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

Inertia의 각 페이지는 React 또는 Vue 컴포넌트에 해당하고, 일반적으로 애플리케이션의 `resources/js/pages` 디렉토리에 저장됩니다. `Inertia::render` 메서드를 통해 넘겨준 데이터는 해당 페이지 컴포넌트의 "props"로 전달되어 하이드레이션됩니다.

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

보시다시피 Inertia를 활용하면, React나 Vue의 모든 기능을 적극적으로 사용할 수 있으면서도, Laravel이 제공하는 강력하고 간편한 라우팅, 데이터 처리 등은 그대로 활용할 수 있습니다.

#### 서버 사이드 렌더링

혹시 애플리케이션에서 서버 사이드 렌더링이 꼭 필요해 Inertia 사용을 망설이고 계시다면, 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)도 제공합니다. 또한 [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)로 배포할 경우, Inertia의 서버 사이드 렌더링 프로세스가 항상 동작하도록 손쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷

Inertia와 Vue/React로 프론트엔드를 구축하고 싶다면, Laravel에서 제공하는 [React 또는 Vue 애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 활용해 개발을 빠르게 시작할 수 있습니다. 두 종류의 스타터 킷 모두, Inertia, Vue/React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 조합해, 애플리케이션의 백엔드 및 프론트엔드 인증 흐름이 기본적으로 구현된 상태에서 새 프로젝트를 시작하실 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 Livewire 기반이든, 또는 Vue/React와 Inertia 기반이든, 프론트엔드 개발을 한다면 최종적으로는 애플리케이션의 CSS 등을 배포용 에셋으로 번들링해야 할 필요가 있습니다. 특히 Vue 또는 React를 사용하는 경우, 프론트엔드 컴포넌트 역시 브라우저에서 실행 가능한 JavaScript 에셋으로 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용하여 에셋을 번들링합니다. Vite는 매우 빠른 빌드 속도와 거의 즉각적인 수준의 Hot Module Replacement(HMR)를 로컬 개발 중 제공하므로, 개발 경험이 탁월합니다. 모든 신규 Laravel 프로젝트(스타터 킷 포함)에는 `vite.config.js` 파일이 생성되어 있으며, 라라벨용 Vite 플러그인을 자동으로 로드해 Laravel과 Vite를 매우 손쉽게 연동할 수 있도록 돕고 있습니다.

Laravel과 Vite로 개발을 바로 시작하고 싶다면, [애플리케이션 스타터 킷](/docs/12.x/starter-kits)을 사용해 프론트엔드와 백엔드 인증 구조가 기본적으로 준비된 상태에서 신속하게 프로젝트를 시작할 수 있습니다.

> [!NOTE]
> Laravel에서 Vite를 활용하는 방법에 대해 더 자세한 내용을 알고 싶으시다면, [에셋 번들링 및 컴파일 전용 문서](/docs/12.x/vite)를 참고하시기 바랍니다.
