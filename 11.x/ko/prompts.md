# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트에어리어](#textarea)
    - [패스워드](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [추천](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [유효성 검사 전에 입력 변환하기](#transforming-input-before-validation)
- [폼](#forms)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스피너](#spin)
- [진행 바](#progress)
- [터미널 초기화](#clear)
- [터미널 관련 사항](#terminal-considerations)
- [지원하지 않는 환경 및 대체 동작](#fallbacks)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지로, 브라우저에서 볼 수 있는 플레이스홀더 텍스트 및 유효성 검증 같은 기능을 지원합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/11.x/artisan#writing-commands)에서 사용자 입력을 받기에 최적이지만, PHP CLI 프로젝트라면 어디에서든 사용할 수 있습니다.

> [!NOTE]  
> Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows를 지원합니다. 자세한 내용은 [지원하지 않는 환경 및 대체 동작](#fallbacks)을 참고해 주세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 Laravel 최신 버전에 기본 포함되어 있습니다.

다른 PHP 프로젝트에 설치하려면 Composer 패키지 매니저로 다음 명령어를 실행하세요:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트 (Text)

`text` 함수는 질문을 표시하고, 사용자의 입력을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

또한 플레이스홀더 텍스트, 기본값, 정보 힌트를 포함할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 값 (Required Values)

값 입력을 반드시 요구하려면 `required` 인수를 전달하세요:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검사 메시지를 사용자 정의하려면 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

추가 유효성 검사 로직을 넣으려면 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력값을 받고 에러 메시지 또는 유효하면 `null`을 반환할 수 있습니다.

또는 Laravel의 [validator](/docs/11.x/validation)를 활용하려면, `validate` 인수에 속성명과 유효성 규칙 배열을 넘기면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트에어리어 (Textarea)

`textarea` 함수는 사용자가 여러 줄 입력할 수 있도록 질문을 표시하고, 입력값을 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 정보 힌트도 포함할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값 (Required Values)

입력을 반드시 요구하려면 `required` 인수를 전달하세요:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

메시지를 커스터마이즈하려면 문자열을 전달해도 됩니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

클로저를 이용해 추가 검사를 처리할 수도 있습니다:

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

클로저는 값 수신 후 에러 메시지 또는 검증 통과 시 `null`을 반환합니다.

Laravel Validator를 사용할 때는 배열로 유효성 규칙을 넘기면 됩니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 패스워드 (Password)

`password` 함수는 `text`와 유사하지만 사용자가 콘솔에서 입력하는 동안 입력 내용이 가려집니다. 비밀번호 같은 민감한 정보를 받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 정보 힌트를 포함할 수도 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값 (Required Values)

값 입력을 필수로 하려면 `required` 인자를 전달하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 메시지를 변경하려면 문자열도 전달 가능:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

추가 유효성 검사를 위한 클로저를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

`validate` 클로저는 값 수신 후 에러 메시지 혹은 `null`을 반환합니다.

Laravel Validator 배열도 지원합니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인 (Confirm)

사용자에게 “예/아니오” 확인을 물을 때 `confirm` 함수를 사용하세요. 사용자는 방향키 또는 `y` / `n`을 눌러 선택하며, 결과는 `true` 또는 `false`입니다:

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예", "아니오" 레이블 텍스트, 정보 힌트도 지정할 수 있습니다:

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
#### "예" 선택 필수 (Requiring "Yes")

필요하다면 `required` 인수를 전달해 "예" 선택을 강제할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 메시지도 문자열로 지정할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택 (Select)

미리 정의된 여러 항목 중 하나를 선택하도록 할 때 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값과 정보 힌트를 지정할 수도 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

`options` 인수에 연관 배열을 전달하면, 선택된 키가 반환됩니다:

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

5개 항목까지만 표시되고 이후 스크롤되며, `scroll` 인수로 표시 수를 조절할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

`select` 함수는 'required' 인수를 지원하지 않습니다. 왜냐하면 아무것도 선택하지 않는 경우가 없기 때문입니다. 그러나 특정 옵션이 선택되는 것을 막는 `validate` 클로저는 사용할 수 있습니다:

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

`options`가 연관 배열일 때는 클로저에 선택된 키가, 배열일 때는 값이 전달됩니다. 에러 메시지 또는 `null`을 반환할 수 있습니다.

<a name="multiselect"></a>
### 다중 선택 (Multi-select)

여러 선택지를 동시에 고르도록 할 때는 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 정보 힌트도 지정 가능:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

키를 반환하도록 `options`에 연관 배열을 전달할 수도 있습니다:

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

5개 항목 후부터 스크롤되며, `scroll` 인수로 표시 수를 지정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값 선택 필수 (Requiring a Value)

기본적으로 0개 이상 선택 가능하지만, `required` 인수를 전달해 1개 이상 선택하도록 강제할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

커스텀 메시지도 문자열로 넘길 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

특정 옵션 선택을 제한하는 `validate` 클로저도 허용됩니다:

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

`options`가 연관 배열이면 선택된 키 배열이, 일반 배열이면 선택된 값 배열이 전달됩니다.

<a name="suggest"></a>
### 추천 (Suggest)

입력 자동완성을 제공할 때 `suggest` 함수를 사용하세요. 사용자는 자동완성과 관계없이 임의 값을 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 전달해 입력이 바뀔 때마다 후보 목록을 동적으로 반환하도록 할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 정보 힌트도 추가할 수 있습니다:

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
#### 필수 값 (Required Values)

입력을 필수로 하려면 `required` 인수를 전달하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

커스텀 메시지도 가능합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검사 (Additional Validation)

입력값에 대해 추가 검사를 처리하려면 클로저를 전달하세요:

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

Laravel Validator 배열도 지원합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색 (Search)

선택할 항목이 많을 때 `search` 함수를 쓰면 사용자가 검색어를 입력해 결과를 필터링한 다음 방향키로 선택할 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

함수 인자로 전달된 클로저는 입력된 문자를 받으며 배열 형태의 선택지를 반환해야 합니다. 연관 배열이면 키가, 일반 배열이면 값이 반환됩니다.

값을 반환하려 할 때 배열이 연관 배열이 되지 않도록 `array_values` 함수 또는 컬렉션의 `values()` 메서드를 활용하세요:

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

플레이스홀더와 정보 힌트 추가도 가능합니다:

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

스크롤 가능 항목 수를 조절하려면 `scroll` 인수를 전달하세요:

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
#### 추가 유효성 검사 (Additional Validation)

추가 유효성 검사를 클로저로 구현할 수 있습니다:

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

`options`가 연관 배열이면 선택된 키가, 아니면 값이 전달됩니다.

<a name="multisearch"></a>
### 다중 검색 (Multi-search)

많은 항목 중 여러 개를 선택하도록 할 때 `multisearch` 함수가 검색과 다중 선택을 동시에 지원합니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

입력에 따라 필터된 후보 목록을 반환하는 클로저를 받으며, 연관 배열을 반환하면 키 배열이, 그렇지 않으면 값 배열이 반환됩니다.

값을 반환할 때 배열이 연관 배열이 되지 않도록 다음 방법을 권장합니다:

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

플레이스홀더 및 정보 힌트도 지정 가능합니다:

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

스크롤 항목 수는 `scroll` 인수로 조정하세요:

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
#### 값 선택 필수 (Requiring a Value)

기본적으로 0개 이상 선택 가능하지만 `required` 인수로 1개 이상을 강제할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

메시지는 문자열로 지정할 수 있습니다:

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
#### 추가 유효성 검사 (Additional Validation)

추가 유효성 로직을 클로저로 구현할 수 있습니다:

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

연관 배열 반환 시 선택 키, 아니면 선택 값 배열이 클로저에 전달됩니다.

<a name="pause"></a>
### 일시정지 (Pause)

`pause` 함수는 사용자에게 정보성 텍스트를 보여주고, Enter/Return 키를 눌러 계속할 때까지 기다립니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검사 전에 입력 변환하기 (Transforming Input Before Validation)

입력값이 유효성 검사를 통과하기 전에 변환이 필요할 수 있습니다. 예컨대 공백을 제거하는 경우입니다. 대부분의 프롬프트 함수는 `transform` 인수로 클로저를 받아 이를 지원합니다:

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

여러 프롬프트를 순서대로 보여줘 정보를 수집한 뒤 추가 작업을 실행할 때 `form` 함수를 사용해 묶을 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼의 모든 응답을 숫자 인덱스 배열로 반환하지만, 각 프롬프트에 `name` 인수를 지정하면 해당 이름으로 결과를 참조할 수 있습니다:

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

`form` 함수의 핵심 이점은 사용자가 `CTRL + U`를 눌러 이전 질문으로 돌아가 선택이나 입력을 수정할 수 있다는 점입니다. 취소 후 처음부터 다시 시작할 필요가 없습니다.

폼 내 특정 프롬프트를 더 세밀하게 제어하려면, 프롬프트 함수를 직접 호출하지 말고 `add` 메서드를 사용할 수 있습니다. `add`는 이전 사용자 응답을 전달받습니다:

```php
use function Laravel\Prompts\form;
use function Laravel\Prompts\outro;

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

`note`, `info`, `warning`, `error`, `alert` 함수로 다양한 정보 메시지를 출력할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수는 여러 행과 열로 구성된 데이터를 쉽게 표시합니다. 열 이름과 데이터를 전달하세요:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스피너 (Spin)

`spin` 함수는 지정한 콜백을 실행하는 동안 스피너와 메시지를 표시합니다. 동작 중임을 알려주고 완료 후 콜백 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching response...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]  
> `spin` 함수는 애니메이션을 위해 `pcntl` PHP 확장 모듈이 필요합니다. 확장이 없을 경우 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행 바 (Progress Bars)

긴 작업의 진행 상태를 알려주기 위해 `progress` 함수를 사용해 진행 바를 표시할 수 있습니다. 주어진 반복 가능한 값에 대해 콜백을 실행할 때마다 진행 바가 자동으로 증가합니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 콜백 반환값들을 배열로 반환합니다.

콜백에 `Laravel\Prompts\Progress` 인스턴스를 전달받아 각 단계마다 레이블과 힌트를 변경할 수도 있습니다:

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

진행 바를 수동으로 조작하려면 전체 단계 수를 지정하고, 각 작업 후 `advance` 메서드로 진행 상태를 갱신하세요:

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

`clear` 함수는 터미널 화면을 지우는데 사용됩니다:

```
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 관련 사항 (Terminal Considerations)

<a name="terminal-width"></a>
#### 터미널 너비 (Terminal Width)

입력 레이블, 선택지, 유효성 메시지가 터미널 열 수보다 길면 자동으로 잘립니다. 사용자 터미널 크기가 작을 수 있으니 가능한 74자 이내로 짧게 유지하세요. 80자 터미널 기준 안전한 최대 길이입니다.

<a name="terminal-height"></a>
#### 터미널 높이 (Terminal Height)

`scroll` 인수를 사용하는 프롬프트는 터미널 높이에 맞게 표시 항목 수가 자동 줄어듭니다. 유효성 메시지에 필요한 공간도 포함됩니다.

<a name="fallbacks"></a>
## 지원하지 않는 환경 및 대체 동작 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, WSL 환경의 Windows를 지원합니다. Windows 네이티브 PHP 버전은 제한적이라 Laravel Prompts를 실행할 수 없습니다.

따라서 Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/7.0/components/console/helpers/questionhelper.html) 같은 대체 구현을 지원합니다.

> [!NOTE]  
> Laravel 프레임워크 사용 시, 각 프롬프트별 대체 구현이 미리 설정되어 있어 지원하지 않는 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 동작 조건 (Fallback Conditions)

Laravel 미사용 또는 대체 동작 조건을 직접 설정하고자 한다면 `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언을 넘기세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 구현 (Fallback Behavior)

Laravel 미사용 시나 대체 동작을 커스터마이즈하려면, 각 프롬프트 클래스에서 `fallbackUsing` 정적 메서드에 클로저를 전달하세요:

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

대체 동작은 각 프롬프트 클래스별로 개별 설정해야 하며, 전달된 프롬프트 인스턴스를 참조해 적절한 값을 반환해야 합니다.