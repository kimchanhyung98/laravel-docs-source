# Precognition

- [소개](#introduction)
- [실시간 유효성 검사](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 함께 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 함께 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 구성하기](#configuring-axios)
- [유효성 검사 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

Laravel Precognition은 미래에 실행될 HTTP 요청의 결과를 미리 예측할 수 있도록 해줍니다. Precognition의 주요 사용 사례 중 하나는 백엔드에서 정의한 유효성 검사 규칙을 프론트엔드 자바스크립트 애플리케이션에 중복 없이 "실시간" 유효성 검사를 제공하는 것입니다. Precognition은 Laravel의 Inertia 기반 [스타터 키트](/docs/{{version}}/starter-kits)와 특히 잘 어울립니다.

Laravel이 "precognitive request(예측 요청)"을 받으면 해당 라우트의 모든 미들웨어를 실행하고, 라우트의 컨트롤러 의존성(포함 [폼 요청](/docs/{{version}}/validation#form-request-validation) 유효성 검사)을 해결합니다. 하지만 실제로 라우트의 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검사

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 이용하면 프론트엔드 Vue 애플리케이션에서 유효성 검사 규칙을 중복 작성하지 않고도 사용자에게 실시간 유효성 검사 경험을 제공할 수 있습니다. 예시로, 새 사용자 생성을 위한 폼을 만들어보겠습니다.

먼저, 라우트에서 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 또한, 라우트의 유효성 검사 규칙을 담을 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, 프론트엔드에서 Precognition Vue 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-vue
```

패키지 설치 후, Precognition의 `useForm` 함수를 통해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 지정하여 폼 객체를 생성할 수 있습니다.

이제 실시간 유효성 검사를 활성화하려면 각 입력 필드의 `change` 이벤트에서 폼의 `validate` 메소드를 호출하고, 입력의 이름을 전달하면 됩니다:

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
        <label for="name">이름</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">이메일</label>
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
            사용자 생성
        </button>
    </form>
</template>
```

이제 사용자가 폼을 채워나가면, Precognition이 라우트의 폼 요청에 정의된 유효성 검사 규칙을 기반으로 실시간 유효성 검사 결과를 제공합니다. 입력값이 변경될 때마다, 디바운스된 "예측" 유효성 검사 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수를 통해 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    유효성 검사 중...
</div>
```

유효성 검사 또는 폼 제출 시 반환된 모든 유효성 오류는 폼의 `errors` 객체에 자동으로 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 존재하는지는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력값이 유효 혹은 무효한지 여부는 입력명으로 각각 `valid`와 `invalid` 메서드를 호출하여 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]  
> 입력 필드는 변경되고 유효성 검사 응답을 받은 이후에만 유효 혹은 무효 상태로 표시됩니다.

Precognition으로 폼 내 일부 입력값만 검사 중이라면, 수동으로 오류를 초기화하는 것이 유용할 수 있습니다. 이때, `forgetError` 함수를 사용할 수 있습니다:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
/>
```

또한, 폼 제출 응답 후 특정 동작을 수행할 수도 있습니다. `submit` 함수는 Axios 요청 프로미스를 반환하므로, 응답에 접근하거나 성공 시 입력값 리셋, 실패 시 예외 처리가 가능합니다:

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('사용자가 생성되었습니다.');
    })
    .catch(error => {
        alert('오류가 발생했습니다.');
    });
```

폼 제출 요청 진행 여부는 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    제출
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 함께 사용하기

> [!NOTE]  
> Vue와 Inertia로 Laravel 애플리케이션 개발을 빠르게 시작하고 싶다면, 공식 [스타터 키트](/docs/{{version}}/starter-kits)를 활용해보세요. 스타터 키트는 새로운 Laravel 앱의 백엔드/프론트엔드 인증까지 포함해줍니다.

Precognition을 Vue와 Inertia에서 사용하기 전, [Vue에서 Precognition 사용](#using-vue) 문서를 참고하세요. Inertia를 사용할 때는 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치 후 `useForm` 함수는 위에서 설명한 유효성 검사 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL 지정 없이, Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로만 전달하면 됩니다. 이 외에도, `submit`은 Promise를 반환하지 않습니다. 대신 방문 옵션 내에 Inertia에서 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 등록할 수 있습니다:

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

Laravel Precognition을 이용해 프론트엔드 React 애플리케이션에서도 유효성 검사 규칙을 중복 작성하지 않고 실시간 유효성 검사 환경을 제공합니다. 사용자 등록 폼 예시로 살펴보겠습니다.

먼저 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, 유효성 검사 규칙을 담을 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

프론트엔드에서 Precognition React 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-react
```

설치 후, `useForm` 함수를 사용해 폼 객체를 만듭니다. 실시간 유효성 검사를 위해 각 입력의 `change`와 `blur` 이벤트에 리스너를 등록해야 합니다. `change`에서는 `setData`로 값을 지정하고, `blur`에서는 `validate`를 호출합니다:

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
            <label for="name">이름</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label for="email">이메일</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                사용자 생성
            </button>
        </form>
    );
};
```

폼이 작성될 때 Precognition이 라우트 폼 요청 규칙에 기반하여 실시간으로 결과를 제공합니다. 입력값 변경 시, 디바운스된 "예측" 유효성 검사 요청이 Laravel로 보내집니다. 디바운스 타임아웃은 다음과 같이 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청 진행 중엔 `validating` 속성이 `true`가 됩니다:

```jsx
{form.validating && <div>유효성 검사 중...</div>}
```

유효성 검사 또는 폼 제출 시 반환된 오류는 자동으로 `errors` 객체에 반영됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼 오류 유무는 `hasErrors`로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

입력값이 유효/무효한지 각각 `valid`와 `invalid`를 통해 확인합니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]  
> 입력값은 변경 후 유효성 검사 응답을 받은 이후에만 유효/무효 상태가 가능합니다.

Precognition으로 입력의 부분 집합만 검사한다면, `forgetError`로 오류를 수동 초기화하는 것도 가능합니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => 
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }
/>
```

폼 제출 응답에 따라 코드 실행도 가능합니다. `submit` 함수는 Axios 프로미스를 반환하므로 응답을 활용하거나 성공 시 초기화, 실패 시 처리할 수 있습니다:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('사용자가 생성되었습니다.');
        })
        .catch(error => {
            alert('오류가 발생했습니다.');
        });
};
```

진행 중엔 `processing` 속성으로 버튼 비활성화 처리할 수 있습니다:

```html
<button disabled={form.processing}>
    제출
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 함께 사용하기

> [!NOTE]  
> React와 Inertia로 Laravel 앱을 빠르게 개발하려면 공식 [스타터 키트](/docs/{{version}}/starter-kits)를 고려하세요. 스타터 키트는 인증 등의 백엔드, 프론트엔드 구조를 제공합니다.

Precognition을 React와 Inertia에서 사용하기 전, [React에서 Precognition 사용](#using-react) 문서를 참고하세요. Inertia와 사용할 때는 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치 후, `useForm`은 유효성 검사 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL 지정 없이 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 받습니다. 또한, `submit`은 Promise를 반환하지 않으며, 옵션에서 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 사용할 수 있습니다:

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

Laravel Precognition을 사용하면 프론트엔드 Alpine 애플리케이션에서도 유효성 검사 규칙을 중복 작성하지 않고 실시간 검사를 제공할 수 있습니다. 사용자 등록 폼 예시를 살펴봅니다.

먼저, Precognition 활성화를 위해 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, 필요한 [폼 요청](/docs/{{version}}/validation#form-request-validation) 클래스를 만듭니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

프론트엔드 Alpine 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에 Precognition 플러그인을 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

이제 Precognition의 `$form` "매직"을 이용해 폼 객체를 생성할 수 있습니다. 실시간 유효성 검사를 위해 입력값과 폼 데이터 바인딩, 각 입력의 `change` 이벤트에서 `validate`를 호출해야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">이름</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">이메일</label>
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
        사용자 생성
    </button>
</form>
```

이제 입력값이 변경될 때 Precognition이 라우트의 유효성 규칙을 기반으로 실시간 결과를 제공합니다. 입력값 변경 시, 디바운스된 예측 유효성 검사 요청이 Laravel로 보내집니다. 디바운스 타임아웃도 설정 가능합니다:

```js
form.setValidationTimeout(3000);
```

검사 요청 진행 중에는 `validating`이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>유효성 검사 중...</div>
</template>
```

검사 도중 혹은 폼 제출 시 발생한 오류는 자동으로 `errors` 객체에 반영됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류 존재 여부는 `hasErrors`로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력값 유효/무효 여부는 각각 `valid`와 `invalid`로 확인 가능합니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]  
> 입력값은 변경 후 유효성 검사 응답을 받을 때만 유효/무효로 표시됩니다.

폼 제출 요청 진행 여부는 `processing`을 참고합니다:

```html
<button :disabled="form.processing">
    제출
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재설정

위의 사용자 생성 예시에서는 Precognition으로 실시간 유효성 검사를 하지만, 전통적인 서버 사이드 폼 제출을 직접 수행합니다. 이 경우 서버의 "old" 입력값과 유효성 오류로 폼을 다시 채워야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는, XHR로 폼을 제출하고 싶다면 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios 요청 프로미스를 반환합니다:

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

                    alert('사용자가 생성되었습니다.')
                })
                .catch(error => {
                    alert('오류가 발생했습니다.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Axios 구성하기

Precognition 유효성 검사 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용하여 백엔드로 요청을 전송합니다. 필요하다면 해당 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 사용 시 `resources/js/app.js`에서 추가 헤더를 설정할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 별도의 Axios 인스턴스를 구성했다면, Precognition에서 해당 인스턴스를 사용하도록 설정할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]  
> Inertia 기반 Precognition 라이브러리는 유효성 검사 요청에만 지정한 Axios 인스턴스를 사용합니다. 폼 제출 요청은 항상 Inertia로 전송됩니다.

<a name="customizing-validation-rules"></a>
## 유효성 검사 규칙 커스터마이징

요청의 `isPrecognitive` 메서드를 이용하면, precognitive 요청 중에 실행되는 유효성 검사 규칙을 커스터마이징할 수 있습니다.

예를 들어, 회원가입 폼에서 비밀번호가 "compromised"(노출된 적 없는 비밀번호)인지 검증은 최종 제출 시에만 수행하고, 실시간 검사(precognitive)에는 최소 8자 등만 검사하고 싶을 수 있습니다. `isPrecognitive` 메서드로 폼 요청 클래스의 규칙을 조정할 수 있습니다:

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

기본적으로 Laravel Precognition은 precognitive 유효성 검사 요청 중 파일은 업로드/검증하지 않습니다. 이는 대용량 파일의 불필요한 반복 업로드를 막기 위함입니다.

따라서 파일 필드는 [해당 폼 요청의 유효성 검사 규칙을 커스터마이징](#customizing-validation-rules)하여 전체 폼 제출시에만 required가 적용되도록 구성해야 합니다:

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

모든 유효성 검사 요청에 파일을 포함하려면, 클라이언트의 폼 인스턴스에서 `validateFiles`를 호출하세요:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, _다른_ 미들웨어에서 precognitive 요청 중 생길 수 있는 부수 효과를 고려해야 합니다.

예를 들어, 사용자의 "상호작용" 횟수를 증가시키는 미들웨어가 있다면 precognitive 요청은 상호작용 횟수에 포함되지 않도록 할 수 있습니다. 그럴 때는 다음과 같이 `isPrecognitive` 메서드로 분기 처리할 수 있습니다:

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

테스트에서 precognitive 요청을 작성하려면, Laravel의 `TestCase`에 포함된 `withPrecognition` 헬퍼를 사용할 수 있습니다. 이 헬퍼는 요청 헤더에 `Precognition`을 추가합니다.

또한, precognitive 요청이 성공적(즉, 유효성 오류가 없음)임을 단언하려면, 응답에서 `assertSuccessfulPrecognition` 메서드를 사용하면 됩니다:

```php
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
