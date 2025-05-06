# Precognition

- [소개](#introduction)
- [실시간 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 함께 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 함께 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부작용 관리하기](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

Laravel Precognition을 사용하면 미래에 일어날 HTTP 요청의 결과를 미리 예측할 수 있습니다. Precognition의 주요 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드 검증 규칙을 중복하지 않고도 "실시간" 검증을 제공하는 기능입니다. Precognition은 Laravel의 Inertia 기반 [스타터 키트](/docs/{{version}}/starter-kits)와 특히 잘 어울립니다.

Laravel이 "예측적 요청(precognitive request)"을 받으면, 해당 라우트의 모든 미들웨어를 실행하고, 컨트롤러 의존성을 해결하며, [폼 요청](/docs/{{version}}/validation#form-request-validation) 검증까지 진행합니다. 그러나 실제로 컨트롤러 메서드를 실행하지는 않습니다.

<a name="live-validation"></a>
## 실시간 검증

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 이용하면 프론트엔드 Vue 애플리케이션에서 검증 규칙을 중복 정의할 필요 없이 실시간 검증 경험을 사용자에게 제공할 수 있습니다. 동작 방식을 예시로 보여주기 위해, 새로운 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, Precognition을 라우트에 활성화하기 위해 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 또한 해당 라우트의 검증 규칙을 포함하는 [폼 요청](/docs/{{version}}/validation#form-request-validation)도 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, NPM을 통해 Vue용 Laravel Precognition 프런트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-vue
```

Precognition 패키지 설치가 완료되면, Precognition의 `useForm` 함수를 통해 HTTP 메소드(`post`), 대상 URL(`/users`), 초기 폼 데이터와 함께 폼 객체를 생성할 수 있습니다.

실시간 검증을 활성화하려면 각 입력의 `change` 이벤트에서 폼의 `validate` 메서드를 호출해 해당 입력의 이름을 전달하세요:

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

이제 사용자가 폼을 작성할 때, Precognition이 라우트의 폼 요청에 정의된 검증 규칙을 기반으로 실시간 검증 결과를 제공합니다. 폼 입력이 변경될 때마다 디바운스된 "예측적" 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중일 때는, 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청이나 폼 제출 중 반환된 모든 검증 에러는 폼의 `errors` 객체에 자동으로 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 에러가 존재하는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력이 검증에 통과하거나 실패했는지 여부는 각 입력의 이름을 `valid` 또는 `invalid` 함수에 전달하여 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력값은 값이 변경되고, 검증 응답을 수신한 후에만 유효 또는 무효로 표시됩니다.

Precognition으로 폼 입력의 일부만 검증한다면, 에러를 수동으로 지워야 할 때가 있습니다. 이 경우 `forgetError` 함수를 사용할 수 있습니다:

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

위와 같이, 입력의 `change` 이벤트에 후킹해서 사용자 상호작용 시 개별 입력 검증이 가능합니다. 다만, 아직 사용자가 상호작용하지 않은 입력도 검증해야 하는 상황(예: "위저드" 형태의 폼)에서는, 다음 스텝으로 이동하기 전에 모든 표시된 입력을 검증해야 할 수 있습니다.

이런 경우 Precognition의 `validate` 메서드에서 검증할 필드명을 `only` 설정 키로 전달하면 됩니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백에서 처리할 수 있습니다:

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

물론, 폼 제출 응답에 따라 추가적인 코드를 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프라미스를 반환하므로, 응답 페이로드에 접근하거나, 제출 성공 시 폼을 리셋하거나, 실패 요청을 핸들링할 수 있습니다:

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인 가능합니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 함께 사용하기

> [!NOTE]
> Vue와 Inertia를 활용해 Laravel 애플리케이션을 빠르게 개발하고 싶다면 [스타터 키트](/docs/{{version}}/starter-kits) 사용을 고려해 보세요. 스타터 키트는 backend 및 frontend 인증 스캐폴딩을 기본 제공합니다.

Vue와 Inertia에서 Precognition을 사용하기 전에, [Vue에서 Precognition 사용하기](#using-vue) 섹션을 먼저 읽으시기 바랍니다. Inertia를 사용할 때는, NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면, Precognition의 `useForm` 함수는 위에서 논의한 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 간결하게 설계되어 HTTP 메서드나 URL을 명시할 필요가 없습니다. 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달하면 됩니다. 또한 이 메서드는 Vue 예제와 달리 Promise를 반환하지 않습니다. 필요하다면 지원되는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 옵션에 추가할 수 있습니다:

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

Laravel Precognition을 이용하면 프론트엔드 React 애플리케이션에서 검증 규칙을 중복 정의할 필요 없이 실시간 검증 경험을 사용자에게 제공할 수 있습니다. 동작 방식을 예시로 보여주기 위해 새로운 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, Precognition을 라우트에 활성화하기 위해 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 또한 해당 라우트의 검증 규칙을 포함하는 [폼 요청](/docs/{{version}}/validation#form-request-validation)도 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, NPM을 통해 React용 Laravel Precognition 프런트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-react
```

Precognition 패키지 설치 후, `useForm` 함수를 이용하여 HTTP 메소드(`post`), 대상 URL(`/users`), 초기 폼 데이터와 함께 폼 객체를 생성합니다.

실시간 검증을 활성화하려면 각 입력의 `change` 및 `blur` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 통해 폼 데이터를 갱신하고, `blur` 이벤트 핸들러에서는 `validate` 메서드로 해당 입력을 검증합니다:

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

입력이 변경될 때마다 Precognition은 라우트의 폼 요청에 정의된 검증 규칙을 기반으로 실시간 검증 결과를 제공합니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중일 때는, 폼의 `validating` 속성이 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```

검증 요청이나 폼 제출 도중 반환된 모든 검증 에러는 `errors` 객체에 자동 반영됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 에러가 존재하는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

검증 통과/실패 여부는 입력명을 각각 `valid` 및 `invalid` 함수에 전달하여 확인 가능합니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력값은 값이 변경되고, 검증 응답을 받은 후에만 유효 또는 무효 표시가 나타납니다.

Precognition으로 폼의 일부 입력만 검증한다면, `forgetError` 함수를 사용해 에러를 수동으로 지울 수 있습니다:

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

위와 같이, 입력의 `blur` 이벤트에 후킹해서 개별 입력을 검증할 수 있습니다. 아직 상호작용하지 않은 입력도 검증하려면, `validate` 메서드의 `only` 키에 필드명을 넘기면 됩니다. 결과는 `onSuccess` 또는 `onValidationError` 콜백에서 처리합니다:

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

또한, 폼 제출 응답을 기반으로 추가 코드 실행이 가능합니다. `submit` 함수는 Axios 요청 프라미스를 반환하므로, 응답 데이터 접근이나 성공 시 폼 리셋, 실패 에러 처리 등을 할 수 있습니다:

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

폼 제출 요청 진행 여부는 `processing` 속성으로 확인 가능합니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 함께 사용하기

> [!NOTE]
> React 및 Inertia로 Laravel 애플리케이션을 빠르게 개발하고 싶다면 [스타터 키트](/docs/{{version}}/starter-kits)를 고려하세요. 스타터 키트는 백엔드 및 프론트엔드 인증 스캐폴딩을 기본 제공합니다.

React와 Inertia에서 Precognition을 사용하기 전에, [React에서 Precognition 사용하기](#using-react) 문서를 반드시 읽으세요. Inertia를 사용하는 경우 NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치가 끝나면, Precognition의 `useForm` 함수는 Inertia [form helper](https://inertiajs.com/forms#form-helper)에 앞서 설명한 검증 기능을 추가해 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 명시하지 않아도 되고, 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달할 수 있습니다. 또한, 이 메서드는 React 예제와 달리 Promise를 반환하지 않습니다. 필요하다면 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 옵션에 넘기면 됩니다:

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

Laravel Precognition을 이용하면 Alpine 기반 프론트엔드 애플리케이션에서도 검증 규칙을 중복 정의할 필요 없이 실시간 검증 경험을 제공할 수 있습니다. 동작 방식은 새로운 유저 생성 폼을 예시로 들어 설명합니다.

먼저, Precognition을 라우트에 활성화하기 위해 `HandlePrecognitiveRequests` 미들웨어를 추가하고, [폼 요청](/docs/{{version}}/validation#form-request-validation)을 구현해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그리고 NPM을 통해 Alpine용 Precognition 프런트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-alpine
```

이후, `resources/js/app.js` 파일에서 Precognition 플러그인을 Alpine에 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

이제 Precognition의 `$form` 마법 메서드를 사용해 HTTP 메소드(`post`), URL(`/users`), 초기 데이터를 전달하여 폼 객체를 생성할 수 있습니다.

실시간 검증을 위해 입력값과 폼 데이터 바인딩, 그리고 각 입력의 `change` 이벤트에서 `validate` 메서드를 호출하면 됩니다:

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

사용자가 폼을 작성할 때, Precognition은 라우트의 폼 요청에 정의된 검증 규칙을 기반으로 실시간 검증 결과를 제공합니다. 입력값이 바뀌면 디바운스된 예측적 검증 요청이 Laravel 애플리케이션에 전달되며, 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정 가능합니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중인 경우 폼의 `validating` 속성이 `true`로 바뀝니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 과정에서 반환된 모든 오류들은 폼의 `errors` 객체에 자동 반영됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 에러가 존재하는지 여부는 `hasErrors` 속성으로 판별할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력값이 검증에 통과/실패했는지는 `valid` 및 `invalid` 함수와 입력명을 함께 전달하여 확인할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값은 값이 변경되고, 검증 응답을 수신한 뒤에야 유효/무효 표시가 나타납니다.

입력의 `change` 이벤트에서 개별 입력을 검증할 수 있고, "위저드" 형태처럼 아직 상호작용되지 않은 입력도 검증해야 할 때는 `validate` 메서드에 `only` 키로 필드 목록을 넘겨주고, 완료 콜백을 활용할 수 있습니다:

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

폼 제출이 진행 중인지 여부는 `processing` 속성으로 판단할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 과거 폼 데이터 복원하기

위 사용자 생성 예시에서, Precognition으로 실시간 검증을 수행하지만 실제 제출은 전통적인 서버 사이드 폼 제출을 사용합니다. 따라서, 폼은 서버로부터 반환되는 "이전" 입력값 및 검증 에러로 자동 채워져야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는, XHR을 통해 폼을 제출하고 싶을 경우, 폼의 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios 요청 프라미스를 반환합니다:

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
                    form.reset();

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

Precognition 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 통해 애플리케이션 백엔드로 요청을 보냅니다. 필요하다면 Axios 인스턴스를 커스터마이즈할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리에서는 `resources/js/app.js` 파일에서 각 요청마다 추가 헤더를 삽입할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 별도의 Axios 인스턴스를 사용 중이라면, Precognition이 해당 인스턴스를 사용하도록 설정할 수 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia용 Precognition 라이브러리는 검증 요청에 한해서만 커스텀 Axios 인스턴스를 사용합니다. 폼 제출은 항상 Inertia가 담당합니다.

<a name="customizing-validation-rules"></a>
## 검증 규칙 커스터마이징

예측적 요청(precognitive request)에서 실행되는 검증 규칙은 요청 객체의 `isPrecognitive` 메서드를 통해 커스터마이즈할 수 있습니다.

예를 들어, 사용자 생성 폼에서 패스워드가 "침해되지 않음(uncompromised)" 검증은 최종 제출에서만 실행하고, 실시간 검증에서는 단순히 필수 및 최소 8자만 검증하게 하고 싶을 수 있습니다. 이런 경우, `isPrecognitive` 메서드로 폼 요청의 규칙을 제어할 수 있습니다:

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

기본적으로 Laravel Precognition은 예측적 검증 요청 내에서 파일을 업로드하거나 검증하지 않습니다. 이는 대용량 파일이 불필요하게 여러 번 업로드되는 것을 방지합니다.

따라서, 해당 필드가 전체 폼 제출시에만 필수임을 [폼 요청의 검증 규칙을 커스터마이즈](#customizing-validation-rules)해서 명확히 해주어야 합니다:

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

모든 검증 요청에 파일을 포함하고 싶다면, 클라이언트 폼 인스턴스에서 `validateFiles` 함수를 호출하면 됩니다:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부작용 관리하기

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, 예측적 요청에서는 _다른_ 미들웨어가 일으킬 부작용을 건너뛰어야 할지 고려해야 합니다.

예를 들어, 사용자와의 "상호작용" 횟수를 증가시키는 미들웨어가 있다면, 예측적 요청에서는 상호작용으로 카운트하지 않도록 조건을 추가해야 할 수 있습니다. 이를 위해, 미들웨어 내에서 `isPrecognitive` 메서드로 확인하면 됩니다:

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

테스트에서 예측적 요청을 만들고 싶다면, Laravel의 `TestCase`에는 `withPrecognition` 헬퍼가 포함되어 있어 `Precognition` 요청 헤더를 추가할 수 있습니다.

또한, 예측적 요청이 성공(즉, 검증 에러가 반환되지 않음)했는지 단언하려면 응답에서 `assertSuccessfulPrecognition` 메서드를 사용하면 됩니다:

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