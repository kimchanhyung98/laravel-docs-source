# 프리코그니션 (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정](#configuring-axios)
- [유효성 검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 앞으로 실행될 HTTP 요청의 결과를 미리 예측할 수 있도록 해줍니다. Precognition의 주요 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드의 유효성 검증 규칙을 중복 정의하지 않고도 "실시간" 유효성 검증을 제공하는 기능입니다. Precognition은 특히 Laravel의 Inertia 기반 [스타터 키트](/docs/12.x/starter-kits)와 함께 사용할 때 큰 효과를 발휘합니다.

Laravel이 "프리코그니티브 요청(precognitive request)"을 받으면, 해당 라우트의 모든 미들웨어를 실행하고 라우트의 컨트롤러 의존성을 해결하며, [폼 요청](/docs/12.x/validation#form-request-validation)을 통한 유효성 검증도 수행합니다. 그러나 실제로 라우트의 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 이용하면, 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복 작성하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해 새 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, 프리코그니션을 특정 라우트에서 사용하려면, 해당 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 또한 라우트의 유효성 검증 규칙을 정의할 [폼 요청](/docs/12.x/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, Vue용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-vue
```

패키지 설치가 완료되면, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공합니다.

실시간 유효성 검증을 활성화하려면 각 입력값의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 입력값의 이름을 전달합니다:

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

이제 사용자가 폼을 입력하는 동안 Precognition이 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. 입력값이 바뀔 때마다, 디바운스된 "프리코그니티브" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 메서드로 조정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중인 경우, 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 요청 또는 폼 제출 과정에서 발생한 모든 오류는 자동으로 폼의 `errors` 객체에 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 에러가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력값이 유효하거나 유효하지 않은지 확인하려면 입력값의 이름을 폼의 `valid` 또는 `invalid` 함수에 각각 전달하면 됩니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 입력값은 값이 변경되고 유효성 검증 응답을 받은 이후에만 유효 또는 무효로 표시됩니다.

폼의 일부 입력값만 Precognition으로 유효성 검증하는 경우, 수동으로 에러를 지워야 할 수 있습니다. 이때는 폼의 `forgetError` 함수를 사용할 수 있습니다:

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

지금까지 살펴본 것처럼, 사용자가 값을 입력할 때마다 입력값의 `change` 이벤트에 맞춰 개별적으로 유효성 검증할 수 있습니다. 하지만, 사용자가 아직 상호작용하지 않은 입력값도 유효성 검증이 필요할 때가 있습니다. 예를 들어 "마법사(Wizard)" 형태의 폼에서는 다음 단계로 넘어가기 전에 모든 표시된 입력값의 유효성을 검증해야 하는 경우가 많습니다.

이럴 때 Precognition의 `validate` 메서드에 `only` 옵션으로 필드 이름 배열을 전달해 해당 필드들만 유효성 검증할 수 있습니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리합니다:

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

또한 폼 제출 응답에 따라 후속 코드를 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프라미스를 반환하므로, 이를 이용해 응답 처리, 제출 성공 시 폼 입력값 리셋, 실패 시 에러 처리 등을 할 수 있습니다:

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

폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기

> [!NOTE]
> Vue와 Inertia를 사용하는 Laravel 애플리케이션을 빠르게 시작하려면 [스타터 키트](/docs/12.x/starter-kits) 사용을 고려해보세요. Laravel의 스타터 키트에는 새로운 애플리케이션의 백엔드/프론트엔드 인증 코드가 포함되어 있습니다.

Vue와 Inertia에서 Precognition을 사용하기 전, [Vue에서 Precognition 사용하기](#using-vue) 문서를 먼저 확인하시기 바랍니다. Vue와 Inertia를 함께 사용할 때는 NPM으로 Inertia 전용 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면, Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 별도로 지정할 필요 없이, Inertia의 [방문 옵션(visit options)](https://inertiajs.com/manual-visits)을 첫 번째 인자로 넘기면 됩니다. 또한, `submit` 메서드는 위의 Vue 예시처럼 프라미스를 반환하지 않습니다. 대신, Inertia에서 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 방문 옵션에 추가할 수 있습니다:

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

Laravel Precognition을 이용하면, 프론트엔드 React 애플리케이션에서 유효성 검증 규칙을 중복 작성하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 예시로, 새 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, 프리코그니션을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 해당 라우트에 추가해야 하며, [폼 요청](/docs/12.x/validation#form-request-validation)을 생성해 라우트의 유효성 검증 규칙을 정의해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-react
```

설치 후, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성합니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공합니다.

실시간 유효성 검증을 위해 각 입력값의 `change`와 `blur` 이벤트를 모니터링해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 사용해 입력값을 갱신하고, `blur` 이벤트 핸들러에서는 `validate` 메서드로 해당 입력값을 검증합니다:

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

이제 사용자가 폼을 입력하면, Precognition이 라우트의 폼 요청에 정의된 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. 입력값이 바뀌면 디바운스된 "프리코그니티브" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면, 폼의 `validating` 속성이 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검증 중 또는 제출 과정에서 응답받은 모든 오류는 자동으로 `errors` 객체에 저장됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 에러가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

입력값의 유효성은 `valid`, `invalid` 함수로 각각 확인할 수 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력값은 값이 변경되고 유효성 검증 응답을 받은 이후에만 유효 또는 무효로 표시됩니다.

일부 입력값만 Precognition으로 검증하는 경우, `forgetError` 함수로 특정 필드의 에러를 수동으로 지울 수 있습니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```

이와 같이 입력값의 `blur` 이벤트에서 개별 항목을 검증할 수 있지만, 사용자가 상호작용하지 않은 입력값도 검증해야 하는 경우가 있습니다. "마법사" 스타일의 폼 등에서, 다음 단계로 이동하기 전에 모든 표시된 입력값을 검증해야 할 때 활용 가능합니다.

Precognition의 `validate` 메서드에 `only` 옵션으로 검증할 필드들을 배열로 전달하면 됩니다. 결과는 `onSuccess` 혹은 `onValidationError` 콜백에서 처리합니다:

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

또한, 폼 제출 결과를 기반으로 추가 동작도 할 수 있습니다. `submit` 함수는 Axios 요청 프라미스를 반환해, 성공적으로 제출된 경우 입력값 리셋 또는 실패 시 에러 메시지 표시 등에 사용합니다:

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

폼 제출 요청이 진행 중인지는 `processing` 속성으로 알 수 있습니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기

> [!NOTE]
> React와 Inertia를 사용하는 Laravel 애플리케이션을 빠르게 시작하려면 [스타터 키트](/docs/12.x/starter-kits)를 사용해보세요. Laravel 스타터 키트에는 새로운 애플리케이션의 백엔드/프론트엔드 인증 코드가 제공됩니다.

React와 Inertia에서 Precognition을 사용하기 전, [React에서 Precognition 사용하기](#using-react) 부분을 먼저 참고하시기 바랍니다. React와 Inertia를 함께 사용할 때는 NPM으로 Inertia 전용 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치가 완료되면, Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 별도 지정하지 않아도 되고, 대신 Inertia의 [방문 옵션(visit options)](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달합니다. 또한 `submit` 메서드는 위의 React 예시처럼 프라미스를 반환하지 않습니다. 대신, Inertia에서 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 방문 옵션에 넘길 수 있습니다:

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

Laravel Precognition을 이용하면 프론트엔드 Alpine 애플리케이션에서도 유효성 검증 규칙을 중복 작성하지 않고 실시간 유효성 검증 경험을 제공할 수 있습니다. 예시로 새 사용자를 생성하는 폼 예제를 보겠습니다.

먼저, Precognition을 라우트에서 사용하려면 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 유효성 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, Alpine용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Precognition 플러그인을 Alpine에 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

패키지 설치와 등록 후, Precognition의 `$form` "매직"을 사용해 폼 객체를 생성할 수 있습니다. HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 전달하면 됩니다.

실시간 유효성 검증을 활성화하려면, 각 입력값을 폼 데이터에 바인딩한 뒤 각 입력값의 `change` 이벤트에서 `validate` 메서드를 호출하도록 설정합니다:

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

이제 사용자가 폼을 작성하면, Precognition이 라우트의 폼 요청 검증 규칙을 이용해 실시간으로 유효성 검증 결과를 제공합니다. 입력값이 변경되면, 디바운스된 프리코그니티브 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이라면, 폼의 `validating` 속성이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

유효성 검증 혹은 제출 응답에서 반환된 에러는 자동으로 `errors` 객체에 기록됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 에러가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력값의 유효성을 각각 `valid`·`invalid` 함수를 통해 확인할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값은 값이 변경되고 유효성 검증 응답을 받은 이후에만 유효/무효로 표시됩니다.

위에서 보았듯, 입력값의 `change` 이벤트에 연결해 개별 항목을 검증할 수 있으나, 아직 사용자가 상호작용하지 않은 필드까지 포함해 검증이 필요할 수 있습니다. 이 경우 Precognition의 `validate` 메서드에서 `only` 옵션에 원하는 필드명을 배열로 전달하면 해당 입력값만 검증할 수 있습니다. 결과 처리는 `onSuccess`, `onValidationError` 콜백으로 합니다:

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 기존 폼 데이터 재출력

위의 사용자 생성 예제에서는 Precognition을 실시간 유효성 검증에 사용하고, 폼 제출은 일반적인 서버 사이드 제출 방식으로 처리하고 있습니다. 이 경우, 서버 사이드 폼 제출 후 반환된 "이전(old)" 입력값이나 유효성 검증 에러를 폼에 반영해야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는, XHR 방식으로 제출하고 싶다면 폼의 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios 요청 프라미스를 반환합니다:

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
### Axios 설정

Precognition용 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트로 백엔드에 요청을 전송합니다. 필요에 따라 Axios 인스턴스를 여러분의 애플리케이션에 맞게 커스터마이징할 수 있습니다. 예를 들어 `laravel-precognition-vue` 라이브러리를 사용하는 경우, 각 요청에 추가 헤더를 설정하려면 `resources/js/app.js` 파일에서 다음처럼 설정할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 커스텀 Axios 인스턴스가 있다면, Precognition에 해당 인스턴스를 사용하도록 지정할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 전용 Precognition 라이브러리는 유효성 검증 요청에만 지정된 Axios 인스턴스를 사용합니다. 폼 제출 요청은 항상 Inertia로 전송됩니다.

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

프리코그니티브 요청에서 실행할 유효성 검증 규칙을 요청 객체의 `isPrecognitive` 메서드를 사용해 커스터마이즈할 수 있습니다.

예를 들어, 사용자 생성 폼에서 비밀번호가 "유출되지 않은(uncompromised)" 값인지 최종 제출 단계에서만 검증하고 싶을 수 있습니다. 프리코그니티브 유효성 검증 요청에서는 비밀번호가 필수이며 최소 8자임만 검사하고, 실제 제출에는 추가적으로 uncompromised 검증을 추가합니다. 이를 위해 `isPrecognitive` 메서드로 폼 요청의 규칙을 다음처럼 커스터마이즈할 수 있습니다:

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
## 파일 업로드 처리 (Handling File Uploads)

기본적으로, Laravel Precognition은 프리코그니티브 유효성 검증 요청에서 파일 업로드 또는 파일 유효성 검증을 수행하지 않습니다. 이를 통해 대용량 파일이 불필요하게 여러 번 업로드되는 것을 방지합니다.

이런 동작 때문에, 반드시 해당 [폼 요청의 유효성 검증 규칙을 커스터마이징](#customizing-validation-rules)하여 파일 필드가 전체 폼 제출시에만 필수임을 지정해야 합니다:

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

모든 유효성 검증 요청에 파일을 포함하고 싶다면, 클라이언트의 폼 인스턴스에서 `validateFiles` 함수를 호출할 수 있습니다:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, _다른_ 미들웨어에서 부수 효과가 있다면 프리코그니티브 요청에서는 이를 건너뛸 필요가 있는지 반드시 고려해야 합니다.

예를 들어, 사용자가 애플리케이션에서 수행한 "상호작용(interaction)" 횟수를 증가시키는 미들웨어가 있다고 가정해봅니다. 프리코그니티브 요청까지 이 카운트를 증가시키고 싶지 않다면, 카운트 증가 코드 전에 `isPrecognitive` 메서드로 프리코그니티브 요청 여부를 검사하면 됩니다:

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
## 테스트 (Testing)

테스트에서 프리코그니티브 요청을 만들고 싶다면, Laravel의 `TestCase`에는 `withPrecognition` 헬퍼가 포함되어 있어 자동으로 `Precognition` 요청 헤더를 추가합니다.

또, 프리코그니티브 요청이 성공했는지(즉, 유효성 검증 에러가 없는지) 테스트하려면, 응답의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

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