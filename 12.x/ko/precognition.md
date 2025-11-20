# 프리코그니션 (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 함께 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 함께 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검증 규칙 커스터마이즈](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부작용 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래에 발생할 HTTP 요청의 결과를 예측할 수 있도록 도와줍니다. Precognition의 주요 사용 사례 중 하나는 애플리케이션의 백엔드 유효성 검증 규칙을 프론트엔드 JavaScript 애플리케이션에 복제하지 않고도 "실시간" 유효성 검증(Live Validation)을 제공할 수 있다는 점입니다.

Laravel이 "프리코그니티브(precognitive) 요청"을 받으면, 해당 라우트의 모든 미들웨어를 실행하고, 라우트 컨트롤러의 의존성을 해결하며, [폼 요청](/docs/12.x/validation#form-request-validation) 기반의 유효성 검증까지 모두 처리합니다. 단, 실제로 컨트롤러의 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면, 프론트엔드 Vue 애플리케이션의 유효성 검증 규칙을 별도로 복제하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 예시로, 새 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, Precognition을 라우트에 적용하려면 해당 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 동시에, 라우트의 유효성 검증 규칙을 보관할 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, Vue용 Laravel Precognition 프론트엔드 헬퍼를 NPM을 통해 설치해야 합니다:

```shell
npm install laravel-precognition-vue
```

Precognition 패키지가 설치되면, Precognition의 `useForm` 함수를 활용하여 폼 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공합니다.

실시간 유효성 검증을 활성화하려면 각 입력값의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 해당 입력의 이름을 인수로 전달합니다:

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

이제 사용자가 폼을 입력하는 즉시, Precognition이 라우트의 폼 요청에 정의된 유효성 규칙에 따라 실시간 유효성 검증 결과를 제공합니다. 입력값이 변경될 때마다 디바운스 처리된 "프리코그니티브" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수를 이용해 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청이나 폼 제출 과정에서 반환된 유효성 검증 에러는 자동으로 폼의 `errors` 객체에 채워집니다:

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

입력이 유효한지, 혹은 유효하지 않은지는 해당 입력의 이름을 인수로 전달하여 `valid`, `invalid` 함수를 통해 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력은 값을 변경하고 유효성 검증 결과를 받은 경우에만 유효 또는 유효하지 않은 것으로 표시됩니다.

폼 입력 일부만 Precognition으로 검증하는 경우, 에러를 직접 초기화해야 할 때가 있습니다. 이때는 `forgetError` 메서드를 사용할 수 있습니다:

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

지금까지 살펴본 것처럼, 입력의 `change` 이벤트에 연결해 사용자의 상호작용에 따라 개별 입력값을 실시간 검증할 수 있습니다. 그러나 사용자가 아직 상호작용하지 않은 입력값도 검증이 필요할 때가 있습니다. 이는 "위저드(wizard)" 타입의 폼 등에서, 다음 단계로 넘어가기 전에 모든 보이는 입력값을 한 번에 검증하려 할 때 많이 사용합니다.

이런 경우 `validate` 메서드를 호출하되, 검증할 필드명을 `only` 설정값에 배열 형태로 전달합니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다:

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

물론, 폼 제출에 대한 응답에 따라 별도의 코드를 실행할 수도 있습니다. `submit` 함수는 Axios 요청 Promise를 반환하므로, 응답 결과에 접근하거나 제출 성공 시 폼을 리셋하거나 실패 시 오류 처리를 할 수 있습니다:

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 함께 사용하기

> [!NOTE]
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하고 싶으시다면, [스타터 키트](/docs/12.x/starter-kits) 중 하나를 활용해 보세요. Laravel 스타터 키트는 백엔드와 프론트엔드 인증 기능이 모두 포함된 기본 구조를 제공합니다.

Precognition을 Vue와 Inertia에서 사용하기 전에, 먼저 [Vue와 함께 Precognition 사용하기](#using-vue) 문서를 숙지하시기 바랍니다. Vue와 Inertia를 함께 사용할 때는 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면 Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

form helper의 `submit` 메서드는 HTTP 메서드나 URL을 따로 지정할 필요 없이, Inertia의 [visit option](https://inertiajs.com/manual-visits)을 첫 번째이자 유일한 인수로 넘겨주면 됩니다. 그리고 `submit` 함수는 위의 Vue 예제와 다르게 Promise를 반환하지 않습니다. 대신 `submit`에 전달한 visit option에서 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 사용할 수 있습니다:

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

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증을 제공할 수 있습니다. 예시로, 새 사용자를 만드는 폼을 예로 들어보겠습니다.

먼저 Precognition을 라우트에 적용하려면, 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 라우트의 유효성 규칙을 담은 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-react
```

Precognition 패키지가 설치되면 `useForm` 함수를 통해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 각각 전달합니다.

실시간 유효성 검증을 활성화하려면 각 입력값의 `change`와 `blur` 이벤트를 모두 감지해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 사용해 입력값을 갱신하고, `blur` 이벤트 핸들러에서는 `validate` 함수를 사용해 해당 입력값을 검증합니다:

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

이제 사용자가 폼을 채우는 동안 Precognition이 폼 요청에 정의된 유효성 검증 규칙에 따라 실시간 유효성 검증 결과를 제공합니다. 입력 변경 시, 디바운스된 프리코그니티브 유효성 검증 요청이 Laravel로 전송됩니다. 디바운스 타임아웃은 다음과 같이 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이라면 `validating` 속성은 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검증 에러가 반환될 경우, 폼의 `errors` 객체에 자동으로 반영됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 확인하려면 `hasErrors` 속성을 사용할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

각 입력 데이터가 유효한지, 유효하지 않은지는 다음과 같이 확인합니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력 필드는 값이 변경되고 유효성 검증 응답을 받은 뒤에만 유효 또는 유효하지 않은 상태가 표시됩니다.

Precognition을 이용해 일부 입력값만 검증하는 경우, 수동으로 에러를 초기화할 필요가 있습니다. 이럴 때는 `forgetError` 함수를 사용할 수 있습니다:

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

입력의 `blur` 이벤트에서 검증하는 것 외에도, 아직 상호작용하지 않은 입력값까지 한 번에 검증하려는 경우도 있습니다(예: "위저드" 폼). 이럴 때는 `validate` 함수의 `only` 옵션에 검증할 필드명을 배열로 전달하면 됩니다. 검증 결과는 `onSuccess`, `onValidationError` 콜백으로 처리할 수 있습니다:

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

폼 제출에 대한 응답을 다루는 로직도 가능합니다. `submit` 함수는 Axios 요청 Promise를 반환하므로, 응답에 따라 폼을 리셋하거나 실패 시 오류 처리를 할 수 있습니다:

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

폼 제출이 진행 중인지 여부는 `processing` 속성을 참고하세요:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 함께 사용하기

> [!NOTE]
> React와 Inertia로 Laravel 애플리케이션을 개발하려는 경우, [스타터 키트](/docs/12.x/starter-kits)를 사용하여 빠르게 개발 환경을 구축할 수 있습니다. 스타터 키트는 백엔드 및 프론트엔드 인증이 기본적으로 포함된 구조를 제공합니다.

Precognition을 React와 Inertia에서 사용하기 전에, [React에서 Precognition 사용하기](#using-react)를 먼저 참고하시기 바랍니다. React와 Inertia를 사용할 경우, Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치가 완료되면, Precognition의 `useForm` 함수가 Inertia [form helper](https://inertiajs.com/forms#form-helper)에 위에서 설명한 유효성 검증 기능을 추가한 형태로 반환됩니다.

form helper의 `submit` 메서드는 HTTP 메서드나 URL 지정이 필요하지 않으며, Inertia의 [visit option](https://inertiajs.com/manual-visits)을 첫 인자로 넘겨주면 됩니다. 그리고 이 `submit` 함수는 위의 React 예제와 달리 Promise를 반환하지 않습니다. 대신 해당 option에서 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 제공할 수 있습니다:

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

Laravel Precognition을 이용하면 프런트엔드 Alpine 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 검증 경험을 제공할 수 있습니다. 예시로 사용자 생성 폼을 만들어 보겠습니다.

먼저 Precognition을 라우트에 적용하려면 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 라우트의 유효성 검증 규칙은 [폼 요청](/docs/12.x/validation#form-request-validation)을 생성해 관리해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 Alpine용 Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Precognition 패키지를 등록했다면 이제 `$form` "매직"을 사용해 폼 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 라우트 URL(`/users`), 초기 데이터도 함께 지정합니다.

실시간 유효성 검증을 사용하려면 입력값을 폼 데이터에 바인딩하고 각 입력의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하면 됩니다:

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

이제 폼이 입력될 때 Precognition이 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 검증 결과를 제공합니다. 입력값이 변경되면 디바운스된 "프리코그니티브" 검증 요청이 Laravel로 전송됩니다. 디바운스 타임아웃은 다음과 같이 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이라면 `validating` 속성이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 중 발생한 에러는 `errors` 객체에 자동 반영됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 에러가 있는지 `hasErrors` 속성을 통해 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

각 입력에 대해 유효/무효 여부도 다음처럼 확인할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력 필드는 값이 바뀌고 유효성 검증 응답을 받은 경우에만 유효 또는 무효로 표시됩니다.

입력값 변경(`change`) 이벤트에 연결해 각 필드를 실시간 검증할 수 있지만, 사용자가 상호작용하지 않은 입력까지 한 번에 검증하고 싶을 때도 있습니다(예: "위저드" 폼). 이럴 땐 `validate` 함수의 `only` 옵션에 필드명을 배열로 전달하면 되고, 검증 결과는 `onSuccess`, `onValidationError` 콜백으로 처리합니다:

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

폼 제출 요청의 진행 중 여부는 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 다시 채우기

위의 사용자 생성 예제에서는 Precognition으로 실시간 검증만 사용했으므로, 폼 제출 자체는 전통적인 서버 사이드 제출 방식이 사용됩니다. 따라서 서버에서 리턴되는 "old" 입력 데이터와 검증 에러를 Blade에서 폼에 반영해야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

만약 폼 제출을 XHR로 처리하고 싶다면, 폼의 `submit` 함수(Axios Promise 반환)를 활용할 수 있습니다:

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

Precognition 프론트엔드 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 통해 백엔드에 요청을 보냅니다. 필요하다면, 애플리케이션에 맞게 Axios 인스턴스를 커스터마이즈할 수 있습니다. 예를 들어 `laravel-precognition-vue` 라이브러리를 사용할 경우, `resources/js/app.js` 파일에서 각 요청에 추가 헤더를 붙여 보낼 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 별도 설정이 완료된 Axios 인스턴스가 있다면, Precognition이 그 인스턴스를 사용하도록 지정할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 기반 Precognition 라이브러리의 경우 유효성 검증 요청에만 지정한 Axios 인스턴스를 사용합니다. 폼 제출은 항상 Inertia가 전송합니다.

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이즈 (Customizing Validation Rules)

프리코그니티브(precognitive) 요청에서는 `isPrecognitive` 메서드를 사용해 실제로 실행되는 유효성 검증 규칙을 자유롭게 커스터마이즈할 수 있습니다.

예를 들어, 사용자 생성 폼에서는 최종 제출 시에만 비밀번호가 "유출되지 않았는지(uncompromised)" 검증하고, 프리코그니티브 검증 시에는 비밀번호가 필수이며 8자 이상인지 정도만 검사하고 싶다고 가정해보겠습니다. `isPrecognitive` 메서드를 활용해 폼 요청의 규칙을 다음과 같이 다르게 정의할 수 있습니다:

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

기본적으로 Precognition은 프리코그니티브 유효성 검증 요청 시 파일을 업로드하거나 검사하지 않습니다. 이로 인해, 대용량 파일이 여러 번 불필요하게 업로드되는 것을 방지할 수 있습니다.

이러한 동작 때문에, [폼 요청의 검증 규칙을 커스터마이즈](#customizing-validation-rules)하여 전체 폼 제출 시에만 해당 필드가 필수임을 지정해야 합니다:

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

모든 유효성 검증 요청에 파일도 포함하고 싶다면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 함수를 호출하면 됩니다:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부작용 관리 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, _다른_ 미들웨어에서 프리코그니티브 요청 시에는 실행하면 안 되는 부작용(side-effects)이 있는지 반드시 확인해야 합니다.

예를 들어, 사용자별로 "상호작용(interaction)" 횟수를 증가시키는 미들웨어가 있다면, Precognition 요청이 상호작용으로 집계되지 않도록 조치해야 할 수 있습니다. 이를 위해, 상호작용 카운트 증가 전 `isPrecognitive` 메서드를 확인할 수 있습니다:

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

테스트 코드에서 프리코그니티브 요청을 보내려면, Laravel의 `TestCase`에 포함된 `withPrecognition` 헬퍼가 `Precognition` 요청 헤더를 자동으로 추가해 줍니다.

이와 함께, 프리코그니티브 요청이 성공적으로 처리되어(즉, 유효성 검증 에러가 없는 경우) 반환되는지를 테스트하려면, 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

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