# Precognition (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래의 HTTP 요청에 대한 결과를 미리 예측할 수 있도록 도와줍니다. Precognition의 주요 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드의 유효성 검증 규칙을 중복 구현하지 않고도 "실시간" 유효성 검증을 제공하는 것입니다. Precognition은 특히 Laravel의 Inertia 기반 [시작 키트](/docs/12.x/starter-kits)와 함께 사용할 때 매우 효과적입니다.

Laravel이 "precognitive request(예측 요청)"를 받으면, 해당 라우트의 모든 미들웨어를 실행하고 컨트롤러의 의존성(예: [폼 요청](/docs/12.x/validation#form-request-validation))을 해결하지만, 실제로 라우트의 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면, 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 실시간 유효성 검증을 사용자에게 제공할 수 있습니다. 동작 방식을 설명하기 위해, 애플리케이션 내에서 새 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, Precognition을 특정 라우트에서 사용할 수 있도록 하려면, 해당 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 그리고 라우트의 유효성 검증 규칙을 포함할 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, Vue용 Laravel Precognition 프론트엔드 헬퍼를 NPM을 통해 설치합니다:

```shell
npm install laravel-precognition-vue
```

이제 Laravel Precognition 패키지가 설치되면, Precognition의 `useForm` 함수를 사용하여 폼 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 타겟 URL(`/users`), 초기 폼 데이터를 전달합니다.

그런 다음 실시간 유효성 검증을 활성화하려면 각 입력 필드의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하여 입력 값의 이름을 전달합니다:

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

이제 사용자가 폼을 입력할 때 Precognition이 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. 입력 값이 변경되면 디바운스된 "precognitive" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 함수를 호출하여 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 요청 또는 폼 제출 중 반환된 모든 유효성 검증 오류는 자동으로 폼의 `errors` 객체에 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 있는지 확인하려면 `hasErrors` 속성을 사용할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

각 입력 값이 유효성 검증을 통과했는지(`valid`) 혹은 실패했는지(`invalid`) 확인하려면 입력 이름을 각각의 함수에 전달합니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력 값의 유효 여부는 해당 값이 변경되어 유효성 검증 응답을 받은 이후에만 표시됩니다.

폼의 특정 입력만 Precognition으로 유효성 검증하는 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 이를 위해 폼의 `forgetError` 함수를 사용할 수 있습니다:

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

앞에서 살펴본 것처럼, 입력의 `change` 이벤트에 연결하여 사용자가 상호작용하는 순간 개별 입력값을 검증할 수 있지만, 아직 사용자가 직접 수정하지 않은 값까지 사전에 검증하고 싶을 때가 있습니다. 이는 여러 단계를 진행하는 "위자드" 형태의 폼에서 흔하게 발생합니다. 모든 표시된 입력 필드를 다음 단계로 넘어가기 전에 검증하려면,

Precognition에서는 `validate` 메서드 호출 시 `only` 설정에 검증하려는 필드명을 전달합니다. 결과 처리는 `onSuccess` 또는 `onValidationError` 콜백을 활용합니다:

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

물론, 폼 제출 응답에 따라 추가 작업을 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환하며, 이를 통해 응답 데이터 접근, 성공 시 입력값 초기화, 실패 시 에러 처리 등을 손쉽게 할 수 있습니다:

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

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 확인합니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기

> [!NOTE]
> Vue와 Inertia를 활용한 Laravel 애플리케이션 개발을 빠르게 시작하고자 한다면, [시작 키트](/docs/12.x/starter-kits)를 사용하는 것을 고려해보시기 바랍니다. Laravel의 시작 키트는 새로운 애플리케이션에 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

Vue에서 Precognition을 사용하기 전, [Vue에서 Precognition 사용하기](#using-vue) 문서를 먼저 확인하시기 바랍니다. Vue와 Inertia를 함께 사용하는 경우, NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면 Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 따로 명시할 필요 없이, Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째이자 유일한 인자로 전달합니다. 그리고 `submit` 메서드는 위에 나온 Vue 예시처럼 Promise를 반환하지 않습니다. 대신, `submit`에 전달한 옵션에서 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 사용할 수 있습니다:

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

Laravel Precognition을 활용하면, 프론트엔드 React 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증을 구현할 수 있습니다. 아래 예시로, 새 사용자를 생성하는 폼을 만들어봅니다.

먼저 Precognition을 해당 라우트에서 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가하고, 유효성 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 React용 Laravel Precognition 프론트엔드 헬퍼를 NPM을 통해 설치합니다:

```shell
npm install laravel-precognition-react
```

패키지가 설치되면 Precognition의 `useForm` 함수를 통해 폼 객체를 생성합니다. HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 전달합니다.

실시간 유효성 검증을 위해, 각 입력 필드의 `change`와 `blur` 이벤트를 감지해야 합니다. `change`에서는 `setData` 함수로 입력 값을 업데이트하고, `blur`에서는 `validate` 함수에 입력 필드명을 넘겨 검증을 실행합니다:

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

이제 사용자가 폼을 입력하는 동안 Precognition은 라우트의 폼 요청에 정의된 유효성 검증 규칙에 따라 실시간 검증을 수행합니다. 입력값이 변경되면 디바운스된 "precognitive" 유효성 검증 요청이 Laravel로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 폼의 `validating` 속성이 `true`입니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검증 요청 또는 폼 제출 시 반환된 오류는 자동으로 폼의 `errors` 객체에 저장됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 확인하려면 `hasErrors` 속성을 사용합니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

각 입력의 유효성 상태는 입력명을 `valid` 또는 `invalid` 함수에 전달하여 확인할 수 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 폼 입력의 유효/무효 여부는 값이 변경되고 유효성 검증 응답을 받은 후에만 표시됩니다.

Precognition으로 폼의 일부 입력 값만 검증한다면, 오류를 수동으로 지우는 것이 유용할 수 있습니다. `forgetError` 함수를 사용할 수 있습니다:

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

위에서 살펴본 것처럼 각 입력의 `blur` 이벤트에 연결해 개별 검증이 가능합니다. 그러나, 사용자가 아직 직접 입력하지 않은 값까지도 검증하고자 할 때가 있습니다. (예: 위자드 구현 등)

Precognition에서는 `validate` 메서드 호출 시 `only` 옵션에 필드 이름 배열을 전달해 해당 필드들만 검사할 수 있습니다. 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리합니다:

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

또한, 폼 제출 응답에 따라 추가 작업을 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환하므로, 성공 시 입력값 초기화, 에러 발생 시 오류 처리 등을 간단하게 할 수 있습니다:

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

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 사용할 수 있습니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기

> [!NOTE]
> React와 Inertia 조합으로 Laravel 애플리케이션을 빠르게 시작하고 싶다면, [시작 키트](/docs/12.x/starter-kits)를 참고하시기 바랍니다. 이 키트는 백엔드 및 프론트엔드 인증 스캐폴딩을 지원합니다.

React에서 Precognition을 사용하기 전, [React에서 Precognition 사용하기](#using-react) 문서를 꼭 참고하십시오. React와 Inertia를 함께 사용하는 경우, NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치가 완료되면 Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 명시할 필요 없이, Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 전달합니다. 또한, `submit` 메서드는 위의 React 예시처럼 Promise를 반환하지 않습니다. 대신, 옵션에 Inertia 지원 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 지정할 수 있습니다:

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

Laravel Precognition을 사용하면, 프론트엔드 Alpine 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증을 구현할 수 있습니다. 여기서는 사용자 생성 폼 예시로 동작 방식을 설명합니다.

먼저 Precognition을 해당 라우트에서 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가하고, 그 라우트에서 사용할 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 NPM을 통해 설치합니다:

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

Precognition 패키지 설치 및 등록이 완료되었다면, Precognition의 `$form` "magic"을 이용해 폼 객체를 생성할 수 있습니다. HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 지정합니다.

실시간 유효성 검증을 활성화하려면 폼의 데이터를 해당 입력값과 바인딩하고, 각 입력 필드의 `change` 이벤트에서 `validate` 함수를 호출해 입력명을 전달합니다:

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

이제 사용자가 폼을 입력할 때 Precognition이 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 결과를 제공합니다. 입력값이 변경되면, 디바운스된 "precognitive" 유효성 검증 요청이 Laravel로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조절합니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 폼의 `validating` 속성이 `true`입니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 요청이나 폼 제출 시 반환된 오류는 자동으로 `errors` 객체를 채웁니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류가 있는지 확인하려면 `hasErrors`를 사용합니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

각 입력값의 유효 여부는 입력명을 `valid` 또는 `invalid` 함수에 전달해 확인할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값은 값이 한 번 변경되고 유효성 검증 응답을 받은 후에만 유효/무효가 표시됩니다.

마찬가지로 입력의 `change` 이벤트에 연결해 개별 입력값을 검증할 수 있지만, 아직 상호작용하지 않은 입력값까지 미리 검증하고 싶을 때가 있습니다. (예: "위자드" 폼 등)

Precognition에서는 `validate` 함수 호출 시 `only` 옵션으로 검증할 필드명을 배열로 전달해 처리할 수 있습니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리합니다:

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

폼 제출 요청 진행 상태는 `processing` 속성을 통해 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재설정하기

위의 사용자 생성 예시에서는 Precognition을 이용해 실시간 유효성 검증을 수행하고, 폼 제출은 전통적인 서버 사이드 방식으로 처리했습니다. 이 경우 서버에서 반환된 "old" 입력값과 유효성 오류를 폼에 반영해 주는 것이 좋습니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

XHR을 이용해 폼을 제출하고 싶다면 폼의 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios 요청 프로미스를 반환합니다:

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

Precognition 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 이용해 백엔드로 요청을 보냅니다. 필요하다면 Axios 인스턴스를 애플리케이션 상황에 맞게 커스터마이즈할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용한다면, 각 요청에 추가 헤더를 붙이려면 `resources/js/app.js` 에서 다음처럼 설정할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 애플리케이션에서 별도의 Axios 인스턴스를 사용 중이라면, Precognition에 해당 인스턴스를 사용하도록 지정할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 버전 Precognition 라이브러리는 유효성 검증 요청에만 커스텀 Axios 인스턴스를 사용합니다. 폼 제출 요청은 항상 Inertia에서 전송합니다.

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

precognitive 요청에서 실행되는 유효성 검증 규칙은 요청 객체의 `isPrecognitive` 메서드를 이용해 커스터마이즈할 수 있습니다.

예를 들어, 사용자 생성 폼에서 비밀번호가 "uncompromised"(해킹 이력 없음)인지의 검증은 폼 최종 제출 시에만 시행하고, precognitive 유효성 검증 시에는 최소 글자 수만 검사하도록 하고 싶을 수 있습니다. 이런 경우 `isPrecognitive` 메서드를 활용해 폼 요청 클래스 내의 규칙을 다음과 같이 정의할 수 있습니다:

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

Laravel Precognition은 기본적으로 precognitive 유효성 검증 요청에서 파일을 업로드하거나 검증하지 않습니다. 이는 대용량 파일이 불필요하게 여러 번 업로드되는 것을 방지하기 위함입니다.

이런 동작을 고려하여, 해당 입력값이 실제 폼 완전 제출 시에만 필수로 검증되도록 [폼 요청의 유효성 검증 규칙](#customizing-validation-rules)을 커스터마이즈하십시오:

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

만약 모든 유효성 검증 요청에 파일을 포함하고 싶다면, 클라이언트 사이드 폼 인스턴스에서 `validateFiles` 함수를 호출하면 됩니다:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리 (Managing Side-Effects)

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, _다른_ 미들웨어에서 precognitive 요청 중에는 실행하지 않아야 할 부수 효과가 있는지 고려해야 합니다.

예를 들어, 사용자별로 애플리케이션과의 "상호작용" 횟수를 증가시키는 미들웨어가 있다면, precognitive 요청은 상호작용 횟수에 포함되지 않게 하고 싶을 수 있습니다. 이런 경우, 상호작용 카운트를 증가시키기 전에 요청의 `isPrecognitive` 메서드로 검사할 수 있습니다:

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

테스트에서 precognitive 요청을 만들고 싶다면, Laravel의 `TestCase`에서 제공하는 `withPrecognition` 헬퍼를 사용할 수 있습니다. 이 헬퍼는 `Precognition` 요청 헤더를 추가해 줍니다.

추가로, precognitive 요청이 성공인지(즉, 유효성 검증 오류가 없는 경우) 확인하고자 한다면, 응답에서 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

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
