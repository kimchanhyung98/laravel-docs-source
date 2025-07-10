# 프롬프트(Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트에어리어](#textarea)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [추천 입력](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시 정지](#pause)
- [유효성 검증 전 입력값 변환하기](#transforming-input-before-validation)
- [폼](#forms)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스핀(Spin)](#spin)
- [진행 바(Progress Bar)](#progress)
- [터미널 초기화](#clear)
- [터미널 사용 시 주의 사항](#terminal-considerations)
- [지원되지 않는 환경 및 대체 동작](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄(command-line) 애플리케이션에 아름답고 사용하기 쉬운 폼을 추가할 수 있도록 해주는 PHP 패키지입니다. 브라우저와 유사한 기능들, 예를 들어 플레이스홀더 텍스트와 유효성 검증(Validation) 등을 지원합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/12.x/artisan#writing-commands)에서 사용자 입력을 받을 때 매우 유용하지만, 모든 명령줄 기반 PHP 프로젝트에서 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL 포함)를 지원합니다. 더 자세한 내용은 [지원되지 않는 환경 및 대체 동작](#fallbacks) 문서를 참고하시기 바랍니다.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 라라벨 릴리즈에는 이미 포함되어 있습니다.

또한, Composer 패키지 관리자를 이용해 다른 PHP 프로젝트에서도 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 사용자에게 질문을 표시하고, 입력값을 받아서 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더 텍스트, 기본값, 참고 힌트도 추가할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 값 필수 입력

값을 반드시 입력해야 한다면 `required` 인수를 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검증 메시지를 직접 지정하고 싶다면, 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하다면, `validate` 인수로 클로저(익명 함수)를 넘길 수 있습니다:

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

이 클로저는 사용자가 입력한 값을 받아서, 에러 메시지(string)나 유효한 경우 `null`을 반환합니다.

또한, Laravel의 [validator](/docs/12.x/validation) 기능도 그대로 사용할 수 있습니다. 이를 위해서는 속성 이름과 원하는 유효성 규칙을 배열로 묶어서 `validate` 인수에 전달하면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트에어리어

`textarea` 함수는 사용자에게 질문을 표시하고, 여러 줄 입력이 가능한 텍스트 에어리어를 통해 값을 받아 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더 텍스트, 기본값, 참고 힌트 역시 지원합니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 값 필수 입력

입력이 반드시 필요하다면 `required` 인수를 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

유효성 검증 메시지를 커스터마이즈하려면 문자열을 전달할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하면 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력된 값을 받아 에러 메시지나 `null`을 돌려줍니다.

Laravel [validator](/docs/12.x/validation)를 활용할 수도 있습니다. 속성명과 유효성 규칙을 배열로 묶어 전달하면 됩니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 비슷하지만, 입력값이 콘솔에 입력되는 동안 마스킹 처리됩니다. 비밀번호와 같은 민감한 정보를 받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더 텍스트, 참고 힌트도 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 값 필수 입력

값 입력을 필수로 하려면 `required` 인수를 전달하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 검증 메시지를 변경하고자 하면 문자열을 넘길 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증 로직이 필요하다면 `validate` 인수에 클로저를 전달할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력된 값을 받아서 에러 메시지 또는 검증에 통과하면 `null`을 반환합니다.

Laravel의 [validator](/docs/12.x/validation)를 그대로 사용하려면 속성명과 유효성 규칙을 배열로 전달하면 됩니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인(Confirm)

사용자에게 "예/아니오" 형태로 확인을 받고 싶을 때는 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키나 `y`, `n` 키를 눌러 응답을 선택할 수 있습니다. 이 함수는 `true` 또는 `false`를 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본 선택값, "예/아니오"의 라벨 등을 커스터마이즈하고 참고 힌트도 표시할 수 있습니다:

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
#### "예" 선택 필수

필요하다면 사용자가 반드시 "예"를 선택하도록 `required` 인수를 전달할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 검증 메시지를 직접 지정하려면 문자열을 사용할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택(Select)

사용자에게 미리 정의된 선택지 중 하나를 고르게 하고 싶다면 `select` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본값, 힌트도 지정 가능합니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

`options` 인수에 연관 배열(associative array)을 전달하면 값 대신 선택된 "키"가 반환됩니다:

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

기본적으로 최대 5개의 옵션이 한 번에 표시되며, 목록 스크롤 기준은 `scroll` 인수로 변경할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

다른 프롬프트 함수와 다르게, `select` 함수는 빈 값(선택하지 않음)을 고르는 것이 불가능하기 때문에 `required` 인수를 지원하지 않습니다. 그러나 특정 옵션을 표시하되 선택은 막고 싶다면 `validate` 인수로 클로저를 전달할 수 있습니다:

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

`options` 인수가 연관 배열이면 클로저로 선택된 키가, 그렇지 않으면 선택된 값이 전달됩니다. 클로저는 에러 메시지나 `null`을 반환할 수 있습니다.

<a name="multiselect"></a>
### 다중 선택(Multi-select)

여러 개의 옵션을 동시에 선택할 수 있게 하고 싶을 때는 `multiselect` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값, 참고 힌트도 지정할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

`options` 인수에 연관 배열을 전달하면 값 대신 선택된 "키 목록"이 반환됩니다:

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

기본적으로 최대 5개 옵션까지만 한 번에 표시되며, 스크롤 시작 기준은 `scroll` 인수로 커스터마이즈 가능합니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수 선택 제한

기본적으로 사용자는 0개 이상의 옵션을 선택할 수 있습니다. 최소 1개 이상 선택을 강제하려면 `required` 인수를 사용하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

유효성 메시지를 지정하고 싶다면, `required` 인수에 문자열을 전달하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

특정 옵션을 표시하지만 선택은 금지하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다:

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

`options` 인수가 연관 배열인 경우 클로저로 선택된 키 목록이, 그렇지 않으면 선택된 값 목록이 전달됩니다. 클로저는 에러 메시지나 `null`을 반환할 수 있습니다.

<a name="suggest"></a>
### 추천 입력(Suggest)

`suggest` 함수는 자동완성 형태로 추천 선택지를 보여줄 수 있습니다. 다만, 사용자는 자동완성에 없더라도 아무 값이나 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는, `suggest` 함수 두 번째 인수로 클로저를 전달할 수도 있습니다. 이 클로저는 사용자가 문자를 입력할 때마다 호출되며, 지금까지 입력된 값을 받아서 자동완성 옵션 배열을 반환해야 합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 참고 힌트도 사용할 수 있습니다:

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
#### 값 입력 필수

입력이 반드시 필요하면 `required` 인수를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

유효성 검증 메시지를 변경하려면 문자열을 넘길 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증이 필요하면 `validate` 인수에 클로저를 전달할 수 있습니다:

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

클로저는 입력된 값을 받아서 에러 메시지 또는 유효한 경우 `null`을 반환합니다.

Laravel의 [validator](/docs/12.x/validation)를 이용해도 됩니다. 속성명과 유효성 규칙을 배열로 전달하면 됩니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색(Search)

사용자에게 선택할 옵션이 많을 때, `search` 함수는 사용자가 검색어를 입력하여 결과를 먼저 필터링한 후 방향키로 하나를 선택할 수 있게 해줍니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

여기서 클로저는 사용자가 지금까지 입력한 텍스트를 받아, 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 "키"가, 일반 배열로 반환하면 선택된 "값"이 반환됩니다.

값을 반환할 배열을 필터링할 때는, 배열이 연관 배열로 바뀌지 않도록 `array_values` 또는 컬렉션의 `values` 메서드를 이용해야 합니다:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더, 참고 힌트도 지정할 수 있습니다:

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

기본적으로 옵션은 최대 5개까지 표시되며, 이 개수는 `scroll` 인수로 변경할 수 있습니다:

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

추가적인 유효성 검증 로직을 수행하고 싶다면, `validate` 인수에 클로저를 전달할 수 있습니다.

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

`options` 클로저가 연관 배열(associative array)을 반환하는 경우, 클로저는 선택된 key를 전달받으며, 그렇지 않다면 선택된 value를 전달받게 됩니다. 클로저는 에러 메시지를 반환하거나, 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="multisearch"></a>
### 멀티서치(Multi-search)

검색할 수 있는 옵션이 매우 많아서 사용자가 여러 항목을 선택해야 한다면, `multisearch` 함수를 사용할 수 있습니다. 이 함수는 사용자가 검색어를 입력해 결과를 필터링한 다음, 화살표 키와 스페이스바로 여러 옵션을 선택할 수 있도록 지원합니다.

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 입력 중인 텍스트를 전달받으며, 옵션 배열을 반환해야 합니다. 만약 연관 배열을 반환한다면, 선택된 옵션들의 key가 반환되고, 그렇지 않으면 해당 값(value)들이 반환됩니다.

옵션의 value를 반환하고 싶을 때 배열에서 필터링한다면, `array_values` 함수나 컬렉션의 `values` 메서드를 사용해 배열이 연관 배열로 변하지 않도록 해야 합니다.

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($name) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더 텍스트나 인포메이션 힌트를 함께 포함할 수도 있습니다.

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

최대 다섯 개의 옵션이 표시되며 그 이후부터는 스크롤이 활성화됩니다. `scroll` 인수를 통해 표시되는 옵션 개수를 조정할 수도 있습니다.

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
#### 값 필수 지정

기본적으로, 사용자는 0개 이상의 옵션을 선택할 수 있습니다. `required` 인수를 전달하여 하나 이상의 옵션을 반드시 선택하도록 할 수 있습니다.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

유효성 검증 메시지를 사용자 정의하고 싶다면, `required` 인수에 문자열을 전달할 수도 있습니다.

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

추가 유효성 검증 로직을 사용하고 싶다면, `validate` 인수에 클로저를 전달할 수 있습니다.

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

`options` 클로저가 연관 배열을 반환하는 경우에는 선택된 key 들이, 그렇지 않으면 value 들이 클로저로 전달됩니다. 클로저는 에러 메시지를 반환하거나, 유효성 검증이 통과하면 `null`을 반환할 수 있습니다.

<a name="pause"></a>
### 일시정지(Pause)

`pause` 함수는 사용자에게 안내 메시지를 보여주고 Enter(엔터) 또는 Return 키를 눌러 진행 의사를 확인할 때 사용할 수 있습니다.

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검증 전 입력값 변환하기

때로는 유효성 검증 전에 프롬프트 입력값을 변환하고 싶을 때가 있습니다. 예를 들어, 입력된 문자열에서 공백을 제거하고자 할 수 있습니다. 이때, 많은 프롬프트 함수들은 `transform` 인수를 제공하며, 클로저를 전달할 수 있습니다.

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
## 폼(Forms)

여러 프롬프트를 연달아 표시하여 필요한 정보를 모은 후, 추가 동작을 수행하는 경우가 자주 있습니다. 이럴 때는 `form` 함수를 사용해 한 번에 작동하는 프롬프트 그룹을 만들 수 있습니다.

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼에서 입력받은 모든 응답을 숫자 인덱스 기반 배열로 반환합니다. 하지만 각 프롬프트에 `name` 인수를 제공하여 이름을 지정할 수도 있습니다. 이름이 지정된 경우, 응답을 해당 이름으로 접근할 수 있습니다.

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

`form` 함수를 사용하는 가장 큰 장점 중 하나는 사용자가 `CTRL + U` 단축키로 폼 내에서 이전 프롬프트로 돌아가 실수를 수정하거나 선택을 변경할 수 있다는 점입니다. 폼 전체를 취소하고 다시 시작할 필요 없이, 손쉽게 수정이 가능합니다.

폼 구성에서 각 프롬프트를 더 세밀하게 제어할 필요가 있다면, 프롬프트 함수 대신 `add` 메서드를 사용할 수 있습니다. 이 메서드에는 사용자가 이전에 입력한 모든 응답이 전달됩니다.

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
## 안내 메시지(Informational Messages)

`note`, `info`, `warning`, `error`, `alert` 함수들을 사용해 다양한 안내 메시지를 표시할 수 있습니다.

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블(Tables)

`table` 함수는 여러 행(row)과 열(column)의 데이터를 쉽게 보여줄 수 있도록 해줍니다. 컬럼명과 테이블에 표시할 데이터만 제공하면 됩니다.

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(Spin)

`spin` 함수는 동작 실행 중임을 나타내는 스피너와, 선택적으로 메시지를 함께 표시합니다. 지정된 콜백을 실행하는 동안 프로세스가 진행 중임을 사용자에게 알리고, 완료 시 콜백의 결과를 반환합니다.

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching response...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]
> `spin` 함수를 사용하려면 스피너 애니메이션을 위해 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다. 이 확장 모듈이 없으면 애니메이션 대신 정적인 스피너가 나타납니다.

<a name="progress"></a>
## 진행률 표시줄(Progress Bars)

작업이 오래 걸리는 경우, 작업 진행 상황을 알려주는 진행률 표시줄을 보여주는 것이 유용합니다. `progress` 함수를 사용하면, 라라벨이 주어진 이터러블 값에 대해 반복되는 각각의 단계마다 진행률 표시줄을 갱신합니다.

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map 함수처럼 동작하며, 각 콜백 반복 호출의 반환값을 담은 배열을 반환합니다.

콜백에서 `Laravel\Prompts\Progress` 인스턴스를 인자로 받아, 반복할 때마다 라벨이나 힌트를 변경하는 것도 가능합니다.

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

때로는 진행률 표시줄을 수동으로 더 세밀하게 제어해야 할 수 있습니다. 먼저 전체 반복 단계 수를 지정하고, 각 항목 처리 후 `advance` 메서드로 표시줄을 한 단계씩 갱신할 수 있습니다.

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

`clear` 함수를 사용하면 사용자의 터미널 화면을 지울 수 있습니다.

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 고려사항

<a name="terminal-width"></a>
#### 터미널 너비

어떤 라벨, 옵션, 유효성 메시지의 길이가 사용자의 터미널 열 수(컬럼 수)를 초과하면, 자동으로 길이가 잘려 표시됩니다. 사용자가 좁은 터미널을 사용할 수도 있으니 문자열 길이를 최소화하는 것이 좋습니다. 표준 80자 터미널을 고려할 때 안전한 최대 길이는 74자 정도입니다.

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 지원하는 프롬프트의 경우, 해당 값은 자동으로 사용자의 터미널 높이에 맞도록 줄어듭니다. 이때 유효성 메시지가 표시될 공간도 함께 고려됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경과 대체 동작(Fallbacks)

Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows를 지원합니다. Windows용 PHP의 한계로 인해, 현재 WSL이 아닌 일반 Windows 환경에서 Laravel Prompts를 사용할 수 없습니다.

따라서, Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현 방식으로 자동 전환(fallback)을 지원합니다.

> [!NOTE]
> Laravel 프레임워크와 함께 Laravel Prompts를 사용할 경우, 환경마다 각 프롬프트에 맞는 자동 대체 설정이 이미 완료되어 있어서, 지원되지 않는 환경에서는 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 동작 조건

Laravel을 사용하지 않거나, 대체 동작의 조건을 직접 정의하고 싶다면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언 값을 전달할 수 있습니다.

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 커스터마이징

Laravel을 사용하지 않거나, 대체 동작 자체를 커스터마이징(control)하고 싶을 때는, 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다.

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

대체 동작은 각 프롬프트 클래스마다 개별적으로 설정해야 합니다. 클로저는 해당 프롬프트 클래스의 인스턴스를 인자로 받으며, 프롬프트에 맞는 적절한 타입을 반환해야 합니다.