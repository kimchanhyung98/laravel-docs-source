# 프롬프트

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트영역](#textarea)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [단일 선택](#select)
    - [다중 선택](#multiselect)
    - [자동완성 제안](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [검증 전에 입력 변환하기](#transforming-input-before-validation)
- [폼](#forms)
- [안내 메시지](#informational-messages)
- [테이블](#tables)
- [스핀](#spin)
- [진행률 표시줄](#progress)
- [터미널 초기화](#clear)
- [터미널 고려사항](#terminal-considerations)
- [미지원 환경 및 대체 동작](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 커맨드라인 애플리케이션에 아름답고 사용자 친화적인 폼을 추가할 수 있게 해주는 PHP 패키지로, 플레이스홀더 텍스트나 검증과 같은 브라우저 스타일의 기능들을 제공합니다.

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/{{version}}/artisan#writing-commands)에서 사용자 입력을 받을 때 완벽하게 사용할 수 있으며, 어떠한 커맨드라인 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]  
> Laravel Prompts는 macOS, Linux, 그리고 WSL 환경의 Windows를 지원합니다. 자세한 정보는 [지원되지 않는 환경과 대체 동작](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 Laravel에 이미 포함되어 있습니다.

또한 Composer 패키지 매니저를 사용하여 다른 PHP 프로젝트에도 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 지정한 질문으로 사용자를 프롬프트하고, 입력을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더, 기본값, 안내 힌트도 포함할 수 있습니다:

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

입력이 꼭 필요하다면 `required` 옵션을 사용할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 검증

추가적인 검증이 필요하다면 클로저를 `validate` 옵션으로 전달할 수 있습니다:

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

클로저는 사용자가 입력한 값을 받으며, 검증이 통과되면 `null`을, 아니면 에러 메시지를 반환합니다.

또는, Laravel의 [validator](/docs/{{version}}/validation) 기능을 사용할 수도 있습니다. 이 경우 `validate` 옵션에 속성명과 검증 규칙의 배열을 전달하면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트영역

`textarea` 함수는 사용자를 주어진 질문으로 프롬프트하고, 여러 줄의 입력을 받습니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 안내 힌트도 포함할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값

입력이 꼭 필요하다면 `required` 옵션을 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 검증

추가적인 검증이 필요하다면 클로저를 `validate` 옵션으로 전달할 수 있습니다:

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

클로저는 사용자가 입력한 값을 받으며, 검증이 통과되면 `null`을, 아니면 에러 메시지를 반환합니다.

또는, Laravel의 [validator](/docs/{{version}}/validation) 기능을 사용할 수 있습니다. 이 경우 다음과 같이 사용합니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 유사하지만, 콘솔 입력이 마스킹되어 보여집니다. 비밀번호 등 민감한 정보를 받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 힌트도 포함할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값

입력이 꼭 필요하다면 `required` 옵션을 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

검증 메시지를 직접 지정하고 싶다면 문자열을 전달할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 클로저를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력한 값을 받아 검증이 통과되면 `null`을, 아니면 에러 메시지를 반환합니다.

Laravel의 [validator](/docs/{{version}}/validation)도 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인

"예/아니오" 확인이 필요할 때 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키 또는 `y`, `n`키로 응답을 선택할 수 있습니다. 반환값은 `true` 또는 `false`입니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값과 "예/아니오" 라벨 문구, 안내 힌트도 지정할 수 있습니다:

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
#### "예" 응답 필요

필요하다면 `required` 옵션을 전달해서 반드시 "예"를 선택하도록 할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

검증 메시지를 직접 지정할 수도 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 단일 선택

미리 정해진 선택지 중 하나를 선택받고 싶을 때는 `select` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값과 안내 힌트도 지정할 수 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

선택지로 연관 배열을 전달하면 선택한 키가 반환됩니다:

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

최대 5개까지 옵션을 스크롤 없이 표시하며, `scroll` 옵션으로 조절할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 검증

`select` 함수는 기본적으로 아무것도 선택하지 않는 것이 불가능하기 때문에 `required` 옵션이 없습니다. 하지만 특정 선택지를 선택하지 못하게 제한하려면 `validate` 클로저를 사용할 수 있습니다:

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

연관 배열을 사용할 경우 선택된 키를, 그렇지 않으면 값을 인자로 받습니다. 검증 통과 시 `null`, 실패 시 에러 메시지를 반환합니다.

<a name="multiselect"></a>
### 다중 선택

여러 옵션을 선택할 수 있도록 하려면 `multiselect` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 안내 힌트도 지정할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

선택지로 연관 배열을 전달하면 선택한 키들이 반환됩니다:

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

최대 5개의 옵션이 스크롤 없이 표시되며, `scroll` 옵션으로 조정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수 선택

기본적으로 사용자는 0개 이상의 옵션을 선택할 수 있습니다. 하나 이상 선택이 필수라면 `required` 옵션을 사용하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

검증 메시지를 커스터마이즈하려면 문자열을 전달하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 검증

특정 옵션을 막고 싶다면 `validate` 클로저를 사용할 수 있습니다:

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

연관 배열일 경우 선택된 키를, 아니면 값을 받으며, 검증이 통과되면 `null`을 반환합니다.

<a name="suggest"></a>
### 자동완성 제안

`suggest` 함수는 사용자가 입력할 때 자동완성 옵션을 제공할 수 있습니다. 사용자는 항상 자신이 원하는 어떤 값도 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는, 두 번째 인수로 클로저를 전달할 수 있습니다. 사용자가 입력할 때마다 클로저가 실행되고, 사용자가 입력한 내용을 인자로 받아 자동완성 배열을 반환해야 합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 힌트도 사용할 수 있습니다:

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

필수 입력이 필요하다면 `required` 옵션을 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

검증 메시지를 직접 지정할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 클로저를 사용할 수 있습니다:

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

클로저는 입력 값을 받으며, 검증을 통과하면 `null`을 반환합니다.

또는, Laravel의 [validator](/docs/{{version}}/validation) 기능을 사용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색

옵션이 많은 경우, `search` 함수를 사용하면 사용자가 문자열로 검색하여 결과를 필터링한 뒤, 방향키로 원하는 옵션을 고를 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 지금까지 입력한 문자열을 인자로 받고, 옵션의 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 키가, 아니면 값이 반환됩니다.

값을 반환하는 배열을 필터링할 때는 배열이 연관 배열이 되지 않도록 `array_values`나 `values` Collection 메서드를 사용하세요:

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

플레이스홀더와 안내 힌트도 추가할 수 있습니다:

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

최대 5개 결과가 스크롤 없이 표시되며, `scroll` 옵션으로 조정할 수 있습니다:

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
#### 추가 검증

클로저를 `validate` 옵션으로 전달해서 추가 검증 로직을 구현할 수 있습니다:

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

옵션 클로저가 연관 배열을 반환하면 선택된 키, 아니면 값을 받습니다. 반환값이 `null`이면 검증이 통과합니다.

<a name="multisearch"></a>
### 다중 검색

검색 가능한 옵션이 많고, 여러 항목을 선택할 수 있도록 하려면 `multisearch` 함수를 사용하세요. 사용자가 검색 문자열로 결과를 필터링 후 방향키와 스페이스바로 여러 옵션을 선택할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력 중인 문자열을 인자로 받고, 옵션 배열을 반환해야 합니다. 연관 배열이면 선택한 키들, 아니면 값들이 반환됩니다.

값을 반환할 때는 배열이 연관 배열이 되지 않도록 `array_values`나 `values`를 사용하세요:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더와 안내 힌트도 사용할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 5개의 옵션이 스크롤 없이 표시되며, `scroll` 인수로 조정할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
#### 필수 선택

기본적으로 사용자는 0개 이상을 선택할 수 있습니다. 필수로 하나 이상 선택받고 싶다면 `required` 옵션을 사용하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

검증 메시지를 직접 지정하려면 문자열을 전달하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 `validate` 옵션에 클로저를 전달할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
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

연관 배열을 반환하면 선택된 키들을, 아니면 값을 받습니다. 반환값이 `null`이면 통과입니다.

<a name="pause"></a>
### 일시정지

`pause` 함수는 안내 메시지를 표시하고 사용자가 Enter 키를 누를 때까지 대기합니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 검증 전에 입력 변환하기

때때로 입력값을 검증 전에 변환하고 싶을 수 있습니다. 예를 들어, 문자열에서 공백을 제거하고 싶을 때, 많은 프롬프트 함수들은 클로저를 받는 `transform` 옵션을 제공합니다:

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
## 폼

여러 프롬프트로 순차적으로 정보를 수집하고 추가 작업을 하기 위해, `form` 함수를 사용해 하나의 그룹으로 묶을 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼의 모든 프롬프트에 대한 응답을 숫자로 인덱싱된 배열로 반환합니다. 각 프롬프트에 `name`을 지정하면 해당 응답을 더 쉽게 접근할 수 있습니다:

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

`form` 함수의 주요 장점은 사용자가 `CTRL + U` 키로 이전 프롬프트로 자유롭게 돌아갈 수 있다는 점입니다. 이를 통해 실수나 변경이 있을 때 전체 폼을 취소하고 다시 시작할 필요가 없습니다.

더 세밀하게 제어하고 싶다면, 프롬프트 직접 호출 대신 `add` 메서드를 사용할 수 있습니다. `add` 메서드는 이전까지의 응답을 인자로 전달합니다:

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
## 안내 메시지

`note`, `info`, `warning`, `error`, `alert` 함수를 사용해 정보성 메시지를 표시할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블

`table` 함수로 여러 행과 열의 데이터를 쉽게 표시할 수 있습니다. 열 이름과 각 행의 데이터를 배열로 전달하면 됩니다:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(Spinner)

`spin` 함수는 스피너와 메시지를 표시하며 지정된 콜백을 실행합니다. 진행 중임을 나타내고 콜백의 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching response...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]  
> `spin` 함수는 스피너 애니메이션을 위해 `pcntl` PHP 확장 모듈을 필요로 합니다. 이 확장이 없으면 정적인 스피너만 표시됩니다.

<a name="progress"></a>
## 진행률 표시줄

장시간 작업엔 사용자가 진행도를 확인할 수 있도록 진행률 표시줄을 보여주면 좋습니다. `progress` 함수를 사용하면, 주어진 iterable을 반복하며 진행률 바를 자동으로 업데이트합니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map 함수처럼 동작하며, 각 반복의 반환값을 배열로 반환합니다.

콜백에서 `Laravel\Prompts\Progress` 인스턴스를 받아 반복마다 라벨이나 힌트도 변경할 수 있습니다:

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

진행률 바를 수동으로 제어하고 싶다면, 전체 스텝 수를 지정 후 각 아이템 처리 후마다 `advance` 메서드로 진행시킬 수 있습니다:

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
## 터미널 초기화

`clear` 함수는 사용자의 터미널 화면을 즉시 초기화합니다:

```
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 고려사항

<a name="terminal-width"></a>
#### 터미널 폭

라벨, 선택지, 검증 메시지의 길이가 사용자의 터미널 너비(컬럼 수)를 초과하면 자동으로 잘립니다. 사용자 터미널이 좁을 수도 있으니 문자열 길이를 74자 이하로 맞추는 것이 안전합니다. (보통 80컬럼 기준)

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 받는 프롬프트에서는, 값이 터미널의 높이에 맞게 자동 조정되며, 검증 메시지 공간도 포함됩니다.

<a name="fallbacks"></a>
## 미지원 환경 및 대체 동작

Laravel Prompts는 macOS, Linux, WSL의 Windows를 지원합니다. Windows에서 PHP 버전의 한계로 WSL이 아닌 Windows에서는 현재 사용할 수 없습니다.

이 이유로, Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/7.0/components/console/helpers/questionhelper.html)와 같은 대체 구현을 지원합니다.

> [!NOTE]  
> Laravel 프레임워크에서 Prompts를 사용할 때는 각 프롬프트 유형에 대한 대체 구현이 이미 구성되어 있으며, 미지원 환경에서 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 동작 조건

Laravel을 사용하지 않거나 대체 동작의 사용 조건을 변경하고 싶을 땐, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 boolean을 전달하면 됩니다:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 동작 커스터마이징

Laravel을 사용하지 않거나, 대체 동작 자체를 커스터마이즈하고 싶다면 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달하면 됩니다:

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

대체 동작은 각 프롬프트 클래스별로 개별적으로 설정해야 하며, 클로저는 프롬프트 인스턴스를 받아 해당 프롬프트에 맞는 타입을 반환해야 합니다.