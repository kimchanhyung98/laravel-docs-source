# Precognition

- [소개](#introduction)
- [실시간 유효성 검사](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검사 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

Laravel Precognition을 사용하면 미래의 HTTP 요청 결과를 예측할 수 있습니다. Precognition의 주요 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드 유효성 검사 규칙을 중복 작성하지 않고 "실시간" 유효성 검사를 제공하는 기능입니다. Precognition은 Laravel의 Inertia 기반 [스타터 킷](/docs/{{version}}/starter-kits)과 특히 잘 어울립니다.

Laravel이 "예지적 요청(precognitive request)"을 받으면, 해당 라우트의 모든 미들웨어를 실행하고 컨트롤러의 의존성을 해결하며 [폼 요청](/docs/{{version}}/validation#form-request-validation)의 유효성 검사도 진행합니다. 단, 컨트롤러 메서드는 실제로 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검사

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에서 유효성 검사 규칙을 중복 작성하지 않고도 사용자에게 실시간 유효성 검사 경험을 제공할 수 있습니다. 작동 방식을 살펴보기 위해 신규 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, 라우트에서 Precognition을 활성화하려면 해당 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 그리고 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해 유효성 검사 규칙을 정의하세요:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치하세요:

```shell
npm install laravel-precognition-vue
```

패키지 설치 후, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달합니다.

실시간 유효성 검사를 위해, 각 입력값의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하며 입력값의 이름을 전달하세요:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

이제 사용자가 폼을 작성할 때 Precognition은 라우트의 폼 요청에 정의된 유효성 검사 규칙을 기반으로 실시간 유효성 검사 결과를 제공합니다. 폼 입력값이 변경될 때마다 디바운스(debounce)되어 "예지적" 유효성 검사 요청이 Laravel 애플리케이션에 전송됩니다. 디바운스 시간은 폼의 `setValidationTimeout` 함수를 호출하여 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 진행 중일 땐 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검사 또는 폼 제출 과정에서 반환된 모든 유효성 검사 오류는 폼의 `errors` 객체에 자동으로 할당됩니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력이 유효 또는 무효한지 여부는 해당 입력명을 `valid` 또는 `invalid` 함수에 전달해 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 입력 필드는 변경되어 유효성 검사 응답을 받은 후에만 유효 또는 무효로 표시됩니다.

Precognition으로 폼의 일부 입력만 유효성 검사할 경우에는 오류를 수동으로 지울 수 있습니다. 이를 위해 `forgetError` 함수를 사용할 수 있습니다:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

설명한 것과 같이, 입력 필드의 `change` 이벤트에 후크를 걸어 개별 입력값을 검증할 수 있지만, 사용자가 아직 상호작용하지 않은 입력값까지 검증해야 할 수도 있습니다. 이것은 "다단계(마법사) 폼"을 만들 때 자주 필요한데, 다음 단계로 넘어가기 전에 모든 보이는 입력값을 검증하고 싶을 수 있기 때문입니다.

이를 Precognition으로 달성하려면, `validate` 메서드에 검증하고자 하는 필드명을 `only` 구성 옵션에 전달합니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

물론, 폼 제출 응답에 반응하여 추가 코드도 실행할 수 있습니다. `submit` 함수는 Axios 요청 프로미스를 반환하므로, 응답 데이터에 접근하고, 성공 시 폼 입력을 초기화하거나, 실패 시 예외 처리를 할 수 있습니다:

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 확인하세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기

> [!NOTE]
> Vue와 Inertia 기반의 Laravel 애플리케이션을 개발할 때 빠르게 시작하고 싶다면 [스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 사용하는 것을 추천합니다. Laravel 스타터 킷은 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

Vue와 Inertia에서 Precognition을 사용하기 전에 [Vue에서 Precognition 사용하기](#using-vue)를 살펴보세요. Vue와 Inertia를 함께 사용할 경우, NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면, Precognition의 `useForm` 함수가 위에서 설명한 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 더욱 간소화되어, HTTP 메서드나 URL을 별도로 지정할 필요가 없습니다. 대신, 첫 번째이자 유일한 인자로 Inertia의 [방문 옵션(visit options)](https://inertiajs.com/manual-visits)을 전달하면 됩니다. 또한, React/Vue 예시와 달리 `submit`은 프로미스를 반환하지 않으므로, 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 옵션에 직접 지정하여 처리할 수 있습니다:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit({
    preserveScroll: true,
    onSuccess: () => form.reset(),
});
</script>
```

<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에서 유효성 검사 규칙을 중복 작성하지 않고도 실시간 유효성 검사 경험을 제공할 수 있습니다. 작동 방식을 살펴보기 위해 신규 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 또한, [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해 유효성 검사 규칙을 관리하세요:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-react
```

패키지 설치 후, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 전달합니다.

실시간 유효성 검사 활성화를 위해 각 입력값의 `change` 및 `blur` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수로 해당 입력의 값을 갱신하고, `blur` 이벤트에서 `validate` 메서드를 호출하면 입력값의 이름을 전달합니다:

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

이제 사용자가 폼을 작성하면 Precognition이 라우트의 폼 요청 규칙에 따라 실시간 유효성 검사를 제공합니다. 입력값이 변경될 때마다 디바운스되어 "예지적" 유효성 검사 요청이 서버로 전송됩니다. 디바운스 시간은 `setValidationTimeout` 함수로 지정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청 처리가 진행 중이면 `validating` 속성이 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검사(또는 폼 제출) 중에 반환된 오류는 `errors` 객체에 자동으로 할당됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

입력이 유효 또는 무효임을 확인하려면, 해당 입력명을 `valid` 또는 `invalid` 함수에 전달합니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력 필드는 변경 후 유효성 검사 응답을 받아야만 유효 또는 무효로 표시됩니다.

Precognition으로 폼 일부 입력을 검증할 경우, 오류를 수동으로 지울 수 있습니다. `forgetError` 함수로 처리 가능합니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }}
>
```

`blur` 이벤트에 후크를 걸어 개별 입력값 검증이 가능하지만, 아직 상호작용되지 않은 입력이 남아 있을 수도 있습니다. "마법사" 폼 등에서는 입력값 변경 여부와 관계없이 모든 표시된 필드를 검증하고 싶을 때가 있습니다.

이 경우, `validate` 메서드에 검사하고자 하는 필드명 배열을 `only` 설정값으로 전달하세요. 결과는 `onSuccess` 혹은 `onValidationError` 콜백에서 처리합니다:

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

폼 제출 응답에 따라 추가 코드를 실행할 수도 있습니다. `submit` 함수는 Axios 프로미스를 반환하므로, 응답 처리, 폼 리셋, 실패 요청 처리 등에 유용합니다:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

폼 제출 요청 상태는 `processing` 속성으로 확인할 수 있습니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기

> [!NOTE]
> React와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하려면 [스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 사용해 보세요. Laravel 스타터 킷은 새로운 애플리케이션에 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

React와 Inertia에서 Precognition을 사용하기 전에 [React에서 Precognition 사용하기](#using-react)를 참고하세요. React와 Inertia를 함께 사용할 경우, Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치 후, Precognition의 `useForm` 함수가 위에서 설명한 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 지정할 필요가 없으며, 첫 인자로 Inertia의 [방문 옵션](https://inertiajs.com/manual-visits)을 전달할 수 있습니다. `submit`은 프로미스를 반환하지 않으므로, 지원 이벤트 콜백을 직접 옵션에 지정하세요:

```js
import { useForm } from 'laravel-precognition-react-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = (e) => {
    e.preventDefault();

    form.submit({
        preserveScroll: true,
        onSuccess: () => form.reset(),
    });
};
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기

Laravel Precognition을 사용하면 프론트엔드 Alpine 애플리케이션에서도 백엔드 규칙을 중복 작성하지 않고 실시간 유효성 검사 기능을 제공할 수 있습니다. 신규 사용자 생성 폼을 예로 들어보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 추가하고, [폼 요청](/docs/{{version}}/validation#form-request-validation)으로 유효성 검사 규칙을 관리하십시오:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음 NPM을 통해 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치하세요:

```shell
npm install laravel-precognition-alpine
```

이후 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

이제 Precognition의 `$form` "매직"을 사용해 폼 객체를 만들고, HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 넘길 수 있습니다.

실시간 유효성 검사를 위해, 각 입력값과 폼 데이터를 바인딩한 후 `change` 이벤트에서 `validate` 메서드를 호출하세요:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

이제 폼에 값이 입력되면 Precognition이 폼 요청의 유효성 검사 규칙을 기준으로 실시간 유효성 검사 결과를 제공합니다. 입력값이 변경될 때마다 디바운스되어 "예지적" 유효성 검사 요청이 전송됩니다. 디바운스 시간을 설정하려면 `setValidationTimeout` 함수를 사용하세요:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 처리 중일 때는, `validating` 속성이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

차단 또는 제출 시 유효성 검사 오류는 `errors` 객체에 자동 반영됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류 발생 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

개별 입력의 유효 또는 무효 여부는 `valid`/`invalid` 함수에 해당 입력명을 넘겨 확인합니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력필드는 값이 변경되고, 서버의 유효성 검사 응답을 받은 경우에만 유효/무효 상태로 표시됩니다.

입력의 `change` 이벤트에 후크를 걸어 개별 입력 검증이 가능하지만, 사용자가 아직 편집하지 않은 입력까지 모두 검증해야 하는 경우가 있습니다(예: "마법사" 폼에서 다음 단계로 진행 전 모든 표시 입력 검증 등).

이때 Precognition의 `validate` 메서드에서 검증 대상 필드명을 `only` 설정값에 전달하고, 결과는 `onSuccess` 또는 `onValidationError` 콜백에서 처리할 수 있습니다:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

폼 제출 요청 진행 여부는 `processing` 속성을 확인하세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 복원

위 예제에서는 Precognition으로 실시간 유효성 검사를 활용하면서, 실제 폼 제출은 전통적인 서버 방식(submit)으로 진행합니다. 따라서 서버로부터 반환된 "이전" 입력값과 유효성 검사 오류가 폼에 올바르게 반영되어야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는, 폼을 XHR로 제출하고자 한다면, 폼의 `submit` 함수를 사용할 수 있으며, 이 함수는 Axios 요청 프로미스를 반환합니다:

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Axios 설정하기

Precognition 유효성 검사 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용해 백엔드로 요청을 전송합니다. 필요하다면 Axios 인스턴스를 원하는 대로 커스터마이즈할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때 `resources/js/app.js`에서 추가 요청 헤더를 지정할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

또는 이미 커스텀 Axios 인스턴스를 사용하고 있다면, Precognition이 해당 인스턴스를 사용하도록 할 수 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia용 Precognition 라이브러리는 유효성 검사 요청에만 커스텀 Axios 인스턴스를 사용합니다. 폼 제출 요청은 항상 Inertia가 직접 전송합니다.

<a name="customizing-validation-rules"></a>
## 유효성 검사 규칙 커스터마이징

precognitive 요청 시 실행되는 유효성 검사 규칙은 요청의 `isPrecognitive` 메서드를 사용해 커스터마이즈할 수 있습니다.

예를 들어, 사용자 가입 폼에서 최종 제출 시에만 "password uncompromised(유출 비밀번호 아님)" 검사를 수행하고 싶고, precognitive 검증 요청에는 최소 8자 등만 검사하고 싶다면 다음과 같이 폼 요청에서 규칙을 정의할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
## 파일 업로드 처리

기본적으로, Laravel Precognition은 예지적 유효성 검사 요청(precognitive validation request)에서는 파일을 업로드하거나 검증하지 않습니다. 이로 인해 대용량 파일이 여러 번 업로드되는 일을 방지합니다.

이러한 특성 때문에, 전체 폼 제출 시에만 파일 필드가 필수가 되도록 [폼 요청의 규칙을 커스터마이즈](#customizing-validation-rules)하는 것이 좋습니다:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

모든 유효성 검사 요청에 파일을 포함하고 싶다면, 클라이언트 폼 인스턴스에서 `validateFiles` 함수를 호출하세요:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, _다른_ 미들웨어에서 예지적 요청 시 건너뛰어야 할 부수효과(side-effect)가 있는지도 고려해야 합니다.

예를 들어, 사용자의 "인터랙션" 수를 증가시키는 미들웨어가 있을 경우, 예지적 요청이 인터랙션으로 집계되지 않게 하고 싶을 수 있습니다. 이를 위해 미들웨어에서 요청의 `isPrecognitive` 메서드를 체크 후, 집계를 진행하거나 건너뛸 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
## 테스트

테스트에서 예지적 요청을 보내고 싶다면, Laravel의 `TestCase`는 요청 헤더에 `Precognition`을 추가하는 `withPrecognition` 헬퍼를 제공합니다.

또한, 예지적 요청이 정상(유효성 검사 오류 없음) 처리됐는지를 확인하고 싶을 때는 반환된 응답에서 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```