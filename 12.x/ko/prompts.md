# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트에어리어](#textarea)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [추천](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [유효성 검증 전 입력값 변환](#transforming-input-before-validation)
- [폼](#forms)
- [안내 메시지](#informational-messages)
- [테이블](#tables)
- [스핀(로딩 애니메이션)](#spin)
- [진행 바](#progress)
- [터미널 화면 지우기](#clear)
- [터미널 고려사항](#terminal-considerations)
- [지원되지 않는 환경과 대체 방법](#fallbacks)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에서 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지입니다. 입력란의 플레이스홀더 텍스트와 유효성 검증 등 브라우저와 유사한 기능을 제공합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/12.x/artisan#writing-commands)에서 사용자 입력을 받을 때 최적이지만, 어떤 커맨드라인 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL 포함)를 지원합니다. 보다 자세한 내용은 [지원되지 않는 환경 & 대체 방법](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 라라벨(Laravel) 릴리즈에는 이미 기본 포함되어 있습니다.

Laravel Prompts를 다른 PHP 프로젝트에서 사용하려면 Composer 패키지 매니저를 사용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 지정된 질문을 사용자에게 보여주고, 입력을 받은 뒤 그 값을 반환합니다.

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더 텍스트, 기본값, 안내 힌트도 함께 지정할 수 있습니다.

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 값

입력이 반드시 필요하다면 `required` 인수를 전달하면 됩니다.

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

필요하다면 유효성 검증 메시지도 직접 지정할 수 있습니다.

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증 로직을 수행하고 싶다면, `validate` 인수로 클로저를 전달할 수 있습니다.

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

클로저는 사용자가 입력한 값을 전달받으며, 에러 메시지를 반환하거나 유효하다면 `null`을 반환합니다.

또는 라라벨의 [유효성 검증기(validator)](/docs/12.x/validation)를 활용할 수도 있습니다. 이 방법을 사용하려면 `validate` 인수에 속성명과 원하는 유효성 규칙을 담은 배열을 전달하세요.

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트에어리어

`textarea` 함수는 사용자가 여러 줄로 입력할 수 있는 텍스트에어리어(입력창)를 제공하고, 입력한 값을 반환합니다.

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더 텍스트, 기본값, 안내 힌트도 함께 지정할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값

입력이 반드시 필요하다면 `required` 인수를 전달할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

필요하다면 유효성 검증 메시지도 직접 지정할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

추가적으로 유효성 검증 로직이 필요하다면 `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: fn (string $value) => match (true) {
        strlen($value) < 250 => 'The story must be at least 250 characters.',
        strlen($value) > 10000 => 'The story must not exceed 10,000 characters.',
        default => null
    }
);
```

클로저는 입력값을 전달받고, 에러 메시지를 반환하거나 유효하다면 `null`을 반환합니다.

또는 라라벨의 [유효성 검증기(validator)](/docs/12.x/validation)를 사용할 수도 있습니다. 속성명과 유효성 규칙의 배열을 `validate` 인수로 전달하면 됩니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 유사하지만, 입력란에 사용자의 입력값이 보이지 않고 가려집니다. 비밀번호 등 민감한 정보를 입력받을 때 유용합니다.

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 힌트도 지정할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값

입력이 반드시 필요하다면 `required` 인수를 사용할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 검증 메시지를 직접 지정할 수도 있습니다.

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력값을 전달받아, 에러 메시지를 반환하거나 통과시킬 경우 `null`을 반환하면 됩니다.

또는 라라벨의 [유효성 검증기(validator)](/docs/12.x/validation)를 활용할 수도 있습니다.

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인

사용자에게 "예/아니오"로 확인을 받아야 할 때는 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키 혹은 `y`/`n` 키로 대답을 선택할 수 있으며, 이 함수는 `true` 또는 `false`를 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본 선택값, "예"/"아니오" 레이블, 안내 힌트도 함께 지정할 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: 'I accept',
    no: 'I decline',
    hint: 'The terms must be accepted to continue.'
);
```

<a name="confirm-required"></a>
#### "예" 강제 필요

"예"를 반드시 선택해야 할 필요가 있다면, `required` 인수를 사용할 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 검증 메시지를 직접 지정하고 싶다면 문자열로 지정하면 됩니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택

정해진 여러 선택지 중에서 하나를 선택받고 싶다면 `select` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값, 안내 힌트도 함께 지정할 수 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

선택지 키(key)가 선택 결과로 반환되길 원한다면, `options` 인수에 연관 배열을 사용할 수도 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    default: 'owner'
);
```

5개까지의 선택지는 한 번에 표시되고, 그 이상부터는 스크롤됩니다. `scroll` 인수로 표시 개수를 변경할 수 있습니다.

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

다른 프롬프트 함수들과 달리, `select` 함수는 아무 것도 선택하지 않는 것이 불가능하므로 `required` 인수를 지원하지 않습니다. 하지만 특정 선택지를 표시만 하고, 선택을 제한하려면 `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    validate: fn (string $value) =>
        $value === 'owner' && User::where('role', 'owner')->exists()
            ? 'An owner already exists.'
            : null
);
```

`options` 인수가 연관 배열인 경우, 클로저에는 선택된 키가 전달되고, 그렇지 않으면 선택된 값이 전달됩니다. 클로저는 에러 메시지 또는 검증 통과 시 `null`을 반환합니다.

<a name="multiselect"></a>
### 다중 선택

여러 개의 옵션을 동시에 선택할 수 있도록 할 경우 `multiselect` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값, 안내 힌트도 함께 지정할 수 있습니다.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

선택된 옵션의 키(key)를 결과로 반환하길 원한다면, `options` 인수에 연관 배열을 사용하면 됩니다.

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    default: ['read', 'create']
);
```

5개까지의 옵션이 표시된 후, 그 이상 옵션은 스크롤됩니다. `scroll` 인수로 출력 개수를 조정할 수 있습니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값을 반드시 선택해야 하는 경우

기본적으로 사용자는 옵션을 0개 이상 선택할 수 있습니다. 하나 이상을 반드시 선택하게 하려면 `required` 인수를 사용하세요.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

유효성 검증 메시지를 직접 지정하려면 문자열로 전달하세요.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

특정 옵션을 표시하되 선택을 제한하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

`options` 인수가 연관 배열이면 클로저에는 선택된 키들의 배열이, 그렇지 않다면 선택된 값들의 배열이 전달됩니다. 클로저는 에러 메시지나, 검증이 통과되면 `null`을 반환합니다.

<a name="suggest"></a>
### 추천(자동완성)

`suggest` 함수는 자동완성 방식으로 사용자의 입력에 따라 추천 옵션을 보여줍니다. 사용자는 추천 힌트와 상관없이 원하는 모든 값을 입력할 수 있습니다.

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또한 `suggest` 함수의 두 번째 인수로 클로저를 전달할 수도 있습니다. 클로저는 사용자가 입력한 각 문자마다 호출되며, 입력된 값을 인수로 받아 자동완성에 보여줄 옵션 배열을 반환해야 합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 힌트도 추가로 제공할 수 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="suggest-required"></a>
#### 필수 값

입력을 반드시 받으려면 `required` 인수를 사용할 수 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열로 전달합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하다면 `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

클로저는 입력값을 전달받고, 에러 메시지를 반환하거나 통과 시 `null`을 반환합니다.

또는 라라벨의 [유효성 검증기(validator)](/docs/12.x/validation)를 사용할 수도 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색

선택지가 매우 많은 경우, `search` 함수를 통해 사용자가 원하는 대상을 검색하고, 결과를 좁힌 뒤 방향키로 옵션을 선택할 수 있습니다.

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 현재까지 사용자가 입력한 텍스트를 받아서, 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 키가 결과로, 일반 배열일 경우 값을 반환합니다.

값 배열을 필터링해서 반환하려면, 배열이 연관 배열이 되지 않게 `array_values` 함수나 컬렉션의 `values` 메서드를 사용하는 것이 좋습니다.

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($name) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더와 안내 힌트도 제공할 수 있습니다.

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 5개까지의 옵션이 스크롤 없이 표시되며, `scroll` 인수로 변경할 수 있습니다.

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증이 필요한 경우 `validate` 인수에 클로저를 넘길 수 있습니다.

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

옵션 클로저가 연관 배열을 반환하면, 검증 클로저에는 선택된 키가 전달되고, 그렇지 않은 경우 선택된 값이 전달됩니다. 클로저는 에러 메시지나 통과 시 `null`을 반환합니다.

<a name="multisearch"></a>
### 다중 검색

검색 가능한 옵션이 많고, 여러 항목을 동시에 선택해야 한다면 `multisearch` 함수를 이용해 사용자가 검색어로 필터링하고, 방향키 및 스페이스바로 여러 개의 옵션을 선택할 수 있습니다.

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 입력한 내용을 전달받고, 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 '키' 배열을, 일반 배열일 경우 값 배열을 반환합니다.

옵션 값 배열을 필터링할 때 연관 배열이 되지 않도록 `array_values` 함수 또는 컬렉션의 `values` 메서드를 활용하세요.

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더 및 안내 힌트도 함께 지정할 수 있습니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 5개의 옵션이 기본으로 표시되며, `scroll` 인수로 개수를 변경할 수 있습니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
#### 값을 반드시 선택해야 하는 경우

기본적으로 사용자에게 0개 이상의 선택이 허용됩니다. 하나 이상의 선택을 반드시 요구하려면 `required` 인수를 사용하세요.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열로 지정하면 됩니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>

#### 추가 유효성 검증

추가적인 유효성 검사 로직을 수행하고 싶다면, `validate` 인수에 클로저를 전달할 수 있습니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::whereLike('name', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';
        }
    }
);
```

`options` 클로저가 연관 배열(associative array)을 반환하는 경우, 검사용 클로저는 선택된 key 값을 받게 됩니다. 그렇지 않은 경우, 선택된 value 값들을 전달받게 됩니다. 클로저는 에러 메시지를 반환하거나, 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="pause"></a>
### 일시 중지 (Pause)

`pause` 함수는 사용자가 Enter / Return 키를 눌러 계속 진행하길 원할 때까지 안내 메시지를 표시하고 대기하는 용도로 사용할 수 있습니다.

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검사 전 입력 값 변환

때로는 유효성 검사가 실행되기 전에 프롬프트 입력값을 변환하고 싶을 수 있습니다. 예를 들어, 입력된 문자열의 공백을 제거하는 경우가 있습니다. 이를 위해, 많은 프롬프트 함수에서 `transform` 인수를 제공하며, 이는 클로저를 받을 수 있습니다.

```php
$name = text(
    label: 'What is your name?',
    transform: fn (string $value) => trim($value),
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<a name="forms"></a>
## 폼(Form)

여러 프롬프트를 순차적으로 보여주고 추가 작업을 수행하기 위해 정보를 입력받아야 할 때가 자주 있습니다. 이럴 때는 `form` 함수를 사용하여 한 번에 여러 개의 프롬프트를 그룹으로 만들어 사용자에게 입력을 받을 수 있습니다.

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼에서 받은 모든 응답값을 숫자 인덱스가 있는 배열 형태로 반환합니다. 하지만 각 프롬프트에 `name` 인수를 지정하면, 해당 이름을 통해 응답값에 접근할 수 있습니다.

```php
use App\Models\User;
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->password(
        label: 'What is your password?',
        validate: ['password' => 'min:8'],
        name: 'password'
    )
    ->confirm('Do you accept the terms?')
    ->submit();

User::create([
    'name' => $responses['name'],
    'password' => $responses['password'],
]);
```

`form` 함수를 사용할 때의 가장 큰 장점은, 사용자가 `CTRL + U` 단축키를 사용해 이전 프롬프트로 되돌아갈 수 있다는 점입니다. 이 기능 덕분에 입력 실수를 수정하거나 선택을 변경해야 할 때 전체 폼을 취소하고 처음부터 다시 입력하지 않아도 됩니다.

폼 내에 있는 특정 프롬프트에 대해 더 세밀한 제어가 필요하다면, 프롬프트 함수를 직접 호출하는 대신 `add` 메서드를 사용할 수 있습니다. `add` 메서드로 전달되는 클로저에는 사용자가 이전에 응답한 모든 값이 전달됩니다.

```php
use function Laravel\Prompts\form;
use function Laravel\Prompts\outro;
use function Laravel\Prompts\text;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->add(function ($responses) {
        return text("How old are you, {$responses['name']}?");
    }, name: 'age')
    ->submit();

outro("Your name is {$responses['name']} and you are {$responses['age']} years old.");
```

<a name="informational-messages"></a>
## 정보성 메시지

`note`, `info`, `warning`, `error`, `alert` 함수들을 이용하면 정보성 메시지를 출력할 수 있습니다.

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블

`table` 함수는 여러 행과 열로 구성된 데이터를 쉽게 보여줄 수 있도록 해줍니다. 테이블의 컬럼명과 테이블 데이터만 전달하면 됩니다.

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(Spin)

`spin` 함수는 지정한 콜백이 실행되는 동안 스피너와 선택적으로 메시지를 표시하여, 동작이 진행 중임을 보여주고 작업 완료 시 콜백의 결과를 반환합니다.

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> `spin` 함수를 사용할 때 스피너 애니메이션을 위해 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다. 해당 확장 모듈이 없을 경우, 스피너는 정적인 형태로 표시됩니다.

<a name="progress"></a>
## 진행률 표시줄(Progress Bars)

오래 걸리는 작업의 경우, 진행 상황을 사용자에게 보여주는 진행률 표시줄이 유용합니다. `progress` 함수를 사용하면, Laravel이 주어진 iterable 값을 각각 순회할 때마다 진행률 표시줄을 업데이트하여 보여줍니다.

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 `map` 함수처럼 동작하며, 콜백의 결과를 각 반복마다 수집해서 배열로 반환합니다.

콜백 함수에서는 `Laravel\Prompts\Progress` 인스턴스를 추가로 받을 수도 있어, 각 반복마다 label(레이블)과 hint(힌트)를 동적으로 바꿀 수 있습니다.

```php
$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("Updating {$user->name}")
            ->hint("Created on {$user->created_at}");

        return $this->performTask($user);
    },
    hint: 'This may take some time.'
);
```

경우에 따라 진행률 표시줄을 수동으로 조작하고자 할 때도 있습니다. 먼저, 프로세스가 반복할 전체 단계 수(steps)를 지정하고, 각 항목 처리가 끝날 때마다 `advance` 메서드로 진행률을 직접 올릴 수 있습니다.

```php
$progress = progress(label: 'Updating users', steps: 10);

$users = User::all();

$progress->start();

foreach ($users as $user) {
    $this->performTask($user);

    $progress->advance();
}

$progress->finish();
```

<a name="clear"></a>
## 터미널 화면 지우기

`clear` 함수를 이용하면 사용자의 터미널 화면을 지울 수 있습니다.

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 환경 고려사항

<a name="terminal-width"></a>
#### 터미널 가로 길이

레이블, 옵션, 유효성 메시지의 길이가 사용자의 터미널 "컬럼" 개수(너비)를 초과하면 자동으로 잘려서 표시됩니다. 사용자들이 좁은 터미널에서 사용할 가능성이 있다면, 과도하게 긴 문자열 사용을 삼가야 합니다. 일반적으로 안전한 최대 길이는 80컬럼 터미널 기준 74자 이내입니다.

<a name="terminal-height"></a>
#### 터미널 세로 높이

`scroll` 인수를 받는 프롬프트의 경우, 사용자의 터미널 높이에 맞춰 자동으로 표시되는 항목 수가 조절되며, 유효성 메시지 표시 공간도 함께 고려됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경과 대체 동작(Fallbacks)

Laravel Prompts는 macOS, Linux, Windows(WLS 사용 시) 환경을 지원합니다. 그러나 Windows용 PHP의 한계로 인해, 현재로서는 Windows(WLS 외 환경)에서는 사용할 수 없습니다.

이러한 환경에서는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) 같은 대체 구현 방식(fallback)을 사용할 수 있도록 지원합니다.

> [!NOTE]
> 라라벨 프레임워크에서 Laravel Prompts를 사용 중이라면, 각 프롬프트에 대한 대체 동작이 이미 설정되어 있고, 지원되지 않는 환경에서는 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 동작 조건

라라벨을 사용하지 않거나, 언제 대체 동작을 사용할지 직접 설정하려면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 boolean 값을 전달할 수 있습니다.

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 정의

라라벨을 사용하지 않거나, 대체 동작 방식을 직접 정의하고 싶다면, 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다.

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(
                    is_string($prompt->required) ? $prompt->required : 'Required.'
                );
            }

            if ($prompt->validate) {
                $error = ($prompt->validate)($answer ?? '');

                if ($error) {
                    throw new \RuntimeException($error);
                }
            }

            return $answer;
        });

    return (new SymfonyStyle($input, $output))
        ->askQuestion($question);
});
```

대체 동작(fallback)은 각 프롬프트 클래스마다 개별적으로 설정해야 합니다. 클로저에는 해당 프롬프트 클래스의 인스턴스가 전달되며, 사용자가 입력한 알맞은 타입의 값을 반환해야 합니다.

<a name="testing"></a>
## 테스트

라라벨에서는 명령어가 예상한 프롬프트 메시지를 정상적으로 표시하는지 테스트하기 위한 여러 메서드를 제공합니다.

```php tab=Pest
test('report generation', function () {
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
public function test_report_generation(): void
{
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
}
```