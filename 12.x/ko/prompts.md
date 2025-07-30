# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트 (Text)](#text)
    - [텍스트 영역 (Textarea)](#textarea)
    - [비밀번호 (Password)](#password)
    - [확인 (Confirm)](#confirm)
    - [선택 (Select)](#select)
    - [다중 선택 (Multi-select)](#multiselect)
    - [자동 완성 (Suggest)](#suggest)
    - [검색 (Search)](#search)
    - [다중 검색 (Multi-search)](#multisearch)
    - [일시 정지 (Pause)](#pause)
- [유효성 검증 전 입력 변환](#transforming-input-before-validation)
- [폼 (Forms)](#forms)
- [정보 메시지 (Informational Messages)](#informational-messages)
- [테이블 (Tables)](#tables)
- [스피너 (Spin)](#spin)
- [진행 바 (Progress Bar)](#progress)
- [터미널 초기화 (Clearing the Terminal)](#clear)
- [터미널 관련 고려 사항](#terminal-considerations)
- [지원하지 않는 환경과 대체 방법](#fallbacks)
- [테스트 (Testing)](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 명령어 기반 애플리케이션에서 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지로, 브라우저에서 볼 수 있는 자리 표시자 텍스트와 유효성 검증 같은 기능들을 제공합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령](/docs/12.x/artisan#writing-commands)에서 사용자 입력을 받기에 아주 적합하지만, PHP의 모든 커맨드라인 프로젝트에서 사용할 수도 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows를 지원합니다. 자세한 내용은 [지원하지 않는 환경과 대체 방법](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 최신 Laravel 릴리스에 이미 포함되어 있습니다.

다른 PHP 프로젝트에서 사용하려면 Composer 패키지 관리자를 사용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트 (Text)

`text` 함수는 사용자에게 질문을 제시한 후 입력을 받고 결과를 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

자리 표시자, 기본값, 정보 힌트를 포함할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 값 지정

값 입력을 필수로 하는 경우 `required` 인수를 전달하세요:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검사 메시지를 커스텀하고 싶다면 문자열로도 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가로 유효성 검증 로직을 구현하려면 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력받은 값을 인수로 받고, 유효하지 않은 경우 에러 메시지 문자열 또는 검증 성공시 `null`을 반환할 수 있습니다.

또는 Laravel의 [validator](/docs/12.x/validation)를 이용할 수도 있습니다. `validate`에 속성명과 규칙을 담은 배열을 전달하세요:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트 영역 (Textarea)

`textarea` 함수는 여러 줄 입력을 받는 텍스트 영역을 사용자에게 보여주고, 입력 값을 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

자리 표시자, 기본값, 정보 힌트를 포함할 수도 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값 지정

입력 값을 꼭 받아야 한다면 `required` 인수를 사용하세요:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

커스텀 유효성 메시지도 문자열로 지정할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증 조작이 필요한 경우 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력값을 받고 에러 메시지 또는 `null`을 반환할 수 있습니다.

또는 Laravel의 [validator](/docs/12.x/validation)를 활용할 수도 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호 (Password)

`password` 함수는 `text`와 비슷하지만, 입력 중인 글자가 콘솔에 마스킹 처리되어 보이지 않습니다. 비밀번호 같은 민감한 정보를 입력받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

자리 표시자와 정보 힌트도 지정할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값 지정

입력값을 필수로 하려면 `required` 인수를 사용하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

커스텀 메시지도 지정할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증 로직은 `validate` 인수에 클로저로 구현할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력값을 받고 에러 메시지 또는 `null`을 반환합니다.

또는 Laravel [validator](/docs/12.x/validation)를 활용하세요:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인 (Confirm)

사용자에게 "예/아니오" 질문이 필요할 때 `confirm` 함수를 사용하세요. 사용자는 방향키 또는 `y`, `n` 입력으로 응답할 수 있고, 결과는 `true` 또는 `false`를 반환합니다:

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예" / "아니오" 문구, 정보 힌트도 지정할 수 있습니다:

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
#### "예" 필수 응답

필요한 경우 "예" 응답을 요구하려면 `required` 인수를 사용하세요:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

커스텀 메시지도 문자열로 전달할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택 (Select)

사용자에게 사전에 지정된 옵션 중 하나를 선택하도록 할 때 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값과 정보 힌트도 지정할 수 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

`options`에 연관 배열을 전달하면 선택한 키가 반환됩니다:

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

스크롤 전까지 최대 다섯 개의 옵션이 표시됩니다. `scroll` 인수로 표시 가능 항목 수를 조정할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

`select`는 선택 안 함이 불가능해 `required` 인수는 지원하지 않습니다. 하지만 특정 옵션은 선택 불가하게 하려면 `validate`에 클로저를 사용할 수 있습니다:

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

`options`가 연관 배열이면 클로저에는 선택한 키가, 그렇지 않으면 값이 전달됩니다. 클로저는 에러 메시지 또는 `null`을 반환합니다.

<a name="multiselect"></a>
### 다중 선택 (Multi-select)

사용자가 여러 옵션을 선택할 수 있게 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 정보 힌트도 지정할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

`options`에 연관 배열을 전달하면 선택된 옵션 키가 반환됩니다:

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

스크롤 전 최대 다섯 개 옵션이 보입니다. `scroll` 인수로 조절 가능합니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값 필수 지정

기본값으로는 0개 이상 선택할 수 있으나, `required` 인수를 전달하면 1개 이상 선택을 강제합니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

커스텀 메시지도 문자열로 전달할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

특정 옵션 선택을 막으려면 `validate` 인수에 클로저를 전달하세요:

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

`options`가 연관 배열이면 선택된 키 배열이, 아니면 값 배열이 클로저에 전달됩니다. 클로저는 에러 메시지 또는 `null`을 반환할 수 있습니다.

<a name="suggest"></a>
### 자동 완성 (Suggest)

`suggest` 함수는 자동 완성을 제공하며, 사용자가 지정한 옵션 중 일부를 추천합니다. 하지만 추천에 제한 없이 어떤 답변이든 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 전달하여 입력할 때마다 자동 완성 옵션을 동적으로 필터링할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

자리 표시자, 기본값, 정보 힌트도 지정할 수 있습니다:

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
#### 필수 값 지정

입력값을 필수로 하려면 `required` 인수를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

커스텀 메시지도 지정 가능합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증을 위해 `validate`에 클로저를 전달하세요:

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

클로저는 입력값을 받고 에러 메시지 또는 `null`을 반환합니다.

또는 Laravel [validator](/docs/12.x/validation)를 활용할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색 (Search)

옵션이 많을 때, 사용자가 검색 쿼리를 입력해 결과를 필터링하고 방향키로 선택할 수 있게 하려면 `search` 함수를 사용하세요:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 입력한 쿼리를 받고 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택한 키, 아니면 선택한 값을 반환합니다.

값이 반환되는 필터 배열이라면 `array_values` 혹은 컬렉션의 `values` 메서드를 사용해 배열이 연관 배열이 되지 않도록 해야합니다:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

자리 표시자와 정보 힌트도 설정 가능합니다:

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

스크롤 전 5개까지 옵션이 보이며, `scroll` 인수로 개수를 조절할 수 있습니다:

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

추가 검증이 필요하면 `validate`에 클로저를 넘기세요:

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

옵션이 연관 배열이면 선택한 키, 아니면 값을 클로저가 받고, 에러 메시지 또는 `null`을 반환합니다.

<a name="multisearch"></a>
### 다중 검색 (Multi-search)

검색 가능한 옵션이 매우 많고, 사용자가 여러 항목을 선택할 수 있게 하려면 `multisearch`를 사용하세요. 검색 후 방향키와 스페이스로 선택할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력된 검색어를 받고 옵션 배열을 반환합니다. 연관 배열이 반환되면 선택된 키 배열, 아니면 값 배열이 반환됩니다.

값 배열을 반환할 경우도 배열이 연관 배열이 되지 않도록 `array_values` 또는 `values` 메서드를 사용하세요:

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

자리 표시자와 정보 힌트도 지정할 수 있습니다:

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

스크롤 전 기본 최대 5개 옵션을 보여주며, `scroll`로 조정 가능합니다:

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
#### 필수 값 지정

기본적으로 0개 이상의 선택이 가능한데, 1개 이상을 강제로 받으려면 `required` 인수를 사용하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

커스텀 메시지도 지정할 수 있습니다:

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

추가 검증이 필요하면 `validate`에 클로저를 전달하세요:

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

`options` 클로저가 연관 배열 반환 시 선택한 키 배열, 그렇지 않으면 값 배열이 인수로 전달됩니다. 에러 메시지 또는 `null`을 반환하세요.

<a name="pause"></a>
### 일시 정지 (Pause)

`pause` 함수는 정보 메시지를 보여주고, 사용자에게 Enter / Return 키를 눌러 계속 진행하도록 요청합니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검증 전 입력 변환 (Transforming Input Before Validation)

가끔 입력값을 검증하기 전에 변환이 필요할 수 있습니다. 예를 들어, 입력 문자열에 포함된 공백을 제거하고 싶을 때 `transform` 인수에 클로저를 지정하세요:

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
## 폼 (Forms)

여러 프롬프트를 순차적으로 표시해 정보를 수집해야 할 때 `form` 함수를 사용해 그룹화할 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 각 프롬프트 응답을 숫자 인덱스 배열로 반환합니다. `name` 인수를 통해 각 응답에 이름을 붙여서 연관 배열로 접근할 수도 있습니다:

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

`form` 함수의 주요 장점은 `CTRL + U` 키로 이전 프롬프트로 돌아가 입력을 수정할 수 있다는 점입니다. 덕분에 폼 전체를 다시 시작하지 않아도 됩니다.

더 세밀한 제어가 필요하다면, 직접 프롬프트 함수를 호출하는 대신 `add` 메서드에 클로저를 넘겨 이전 사용자의 응답을 받아 프롬프트를 생성할 수 있습니다:

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
## 정보 메시지 (Informational Messages)

`note`, `info`, `warning`, `error`, `alert` 함수를 사용해 사용자에게 정보 메시지를 표시할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수는 여러 행과 열 데이터를 쉽게 출력할 수 있습니다. 열 이름과 테이블 데이터를 전달하세요:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스피너 (Spin)

`spin` 함수는 콜백 함수 실행 중에 스피너와 메시지를 보여줍니다. 작업이 진행 중임을 알리고, 완료 시 콜백의 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> 스피너 애니메이션은 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 필요합니다. 이 확장이 없으면 스피너가 정적인 형태로 표시됩니다.

<a name="progress"></a>
## 진행 바 (Progress Bars)

긴 작업 동안 진행 상황을 사용자에게 알려주기 위해 `progress` 함수를 사용하면, 제공한 반복자(iterable)를 순회하며 각 단계마다 진행 바가 갱신됩니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 콜백의 각 반환값을 배열로 모아서 반환합니다.

콜백에 `Laravel\Prompts\Progress` 인스턴스를 추가 인수로 받아서 반복 중 라벨이나 힌트를 동적으로 변경할 수도 있습니다:

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

더 세밀하게 제어하려면 총 단계 수를 정한 뒤, `advance` 메서드를 호출해 수동으로 진행 바를 갱신할 수도 있습니다:

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
## 터미널 초기화 (Clearing the Terminal)

`clear` 함수를 사용해 터미널 화면을 지울 수 있습니다:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 관련 고려 사항 (Terminal Considerations)

<a name="terminal-width"></a>
#### 터미널 너비

레이블, 옵션, 유효성 메시지 길이가 터미널의 "컬럼" 수보다 길면 자동으로 줄임표(...)로 잘립니다. 사용자가 좁은 터미널을 쓸 수 있으므로 최대 74자 이하로 유지하는 것이 좋습니다(통상 80자 터미널 지원).

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 받는 프롬프트들은 터미널 높이를 고려해서 값이 자동 조절되며, 유효성 메시지 공간도 포함됩니다.

<a name="fallbacks"></a>
## 지원하지 않는 환경과 대체 방법 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, WSL이 포함된 Windows 환경을 지원합니다. Windows PHP의 한계로 인해 WSL 없이 Windows 워크스테이션에서 Laravel Prompts를 쓸 수 없습니다.

따라서 Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) 같은 대체 구현을 지원합니다.

> [!NOTE]
> Laravel 프레임워크 내에서 Laravel Prompts를 사용할 때는 각 프롬프트별 대체 구현이 미리 설정되어 있어, 지원하지 않는 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 활성 조건

Laravel을 사용하지 않거나 대체 활성화 조건을 직접 제어하려면 `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 부울값을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작

Laravel을 사용하지 않거나 대체 동작을 직접 정의하려면 각 프롬프트 클래스별로 `fallbackUsing` 정적 메서드에 클로저를 전달하세요:

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

각 프롬프트 클래스별로 대체 구현을 별도로 설정해야 하며, 클로저는 프롬프트 인스턴스를 받아 적절한 타입을 반환해야 합니다.

<a name="testing"></a>
## 테스트 (Testing)

Laravel은 명령어가 예상대로 Prompt 메시지를 출력하는지 확인할 수 있는 다양한 테스트 메서드를 제공합니다:

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