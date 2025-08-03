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
- [유효성 검사 전 입력 변환](#transforming-input-before-validation)
- [폼](#forms)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스피너](#spin)
- [진행 바](#progress)
- [터미널 초기화](#clear)
- [터미널 관련 고려사항](#terminal-considerations)
- [미지원 환경 및 대체 방식](#fallbacks)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 아름답고 사용하기 편리한 폼을 추가할 수 있는 PHP 패키지입니다. 브라우저에서 제공하는 플레이스홀더 텍스트와 유효성 검사 같은 기능을 포함합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/master/artisan#writing-commands)에서 사용자 입력을 받기에 매우 적합하지만, PHP로 작성된 모든 명령줄 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux 및 WSL이 설치된 Windows를 지원합니다. 더 자세한 정보는 [미지원 환경 및 대체 방식](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 최신 Laravel 버전에 기본 포함되어 있습니다.

다른 PHP 프로젝트에서 사용하려면 Composer 패키지 관리자를 이용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트 (Text)

`text` 함수는 사용자에게 질문을 제시하고, 사용자의 입력을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더, 기본값, 안내 메시지(힌트)를 추가할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수 입력 값

값 입력을 필수로 하려면 `required` 인수를 넘길 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 검사 메시지를 직접 지정하고 싶다면 문자열을 넘길 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검사

추가 검증 로직을 실행하고 싶으면 `validate` 인수로 클로저(익명 함수)를 넘길 수 있습니다:

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

클로저는 입력된 값을 받아서 오류 메시지 문자열을 반환하거나, 검증에 통과하면 `null`을 반환해야 합니다.

또는 Laravel의 [validator](/docs/master/validation)를 활용할 수 있습니다. `validate`에 속성 이름과 유효성 규칙을 포함하는 배열을 전달하면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트에어리어 (Textarea)

`textarea` 함수는 여러 줄 입력을 받기 위한 텍스트 상자를 표시하여 응답을 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 안내 메시지를 함께 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 입력 값

값 입력을 필수로 하려면 `required` 인수를 넘길 수 있습니다:

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
#### 추가 유효성 검사

추가 검증 로직을 실행하려면 `validate` 인수에 클로저를 넘길 수 있습니다:

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

클로저는 입력값을 받아 오류 메시지 문자열 또는 `null`을 반환합니다.

Laravel validator 배열도 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호 (Password)

`password` 함수는 `text` 함수와 비슷하지만, 입력값을 콘솔에서 마스킹하여 비밀번호 같은 민감한 정보를 받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 메시지도 포함할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 입력 값

값 입력을 반드시 요구하려면 `required` 인수를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 메시지를 커스텀하는 것도 가능합니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검사

추가 검증 로직을 위해 클로저를 `validate` 인수로 전달할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

Laravel validator 배열도 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인 (Confirm)

사용자에게 '예' 또는 '아니오'로 대답할 질문을 할 때 `confirm` 함수를 사용할 수 있습니다. 화살표 키나 `y`, `n` 키로 선택할 수 있으며 결과는 `true` 또는 `false`로 반환됩니다:

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, '예', '아니오' 문구 커스터마이징, 안내 메시지도 넣을 수 있습니다:

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
#### "예" 선택 필수화

사용자에게 반드시 '예'를 선택하도록 하려면 `required` 인수를 사용하세요:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 메시지도 문자열로 커스텀할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택 (Select)

사용자에게 미리 정의된 선택지 중 하나를 고르게 하려면 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본값과 안내 메시지 설정도 가능합니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

`options`에 연관 배열을 넘기면, 선택 시 값이 아니라 키가 반환됩니다:

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

최대 5개 항목까지 표시 후 스크롤이 시작됩니다. 스크롤 표시 개수는 `scroll` 인수로 조절할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검사

`select` 함수는 필수 선택이므로 `required` 인수를 받지 않습니다. 하지만 특정 옵션을 비활성화하고 싶다면 `validate` 인수에 클로저를 전달할 수 있습니다:

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

`options`가 연관 배열이면 선택 키가, 아니면 값이 클로저에 전달됩니다. 클로저는 오류 메시지 문자열 또는 `null`을 반환해야 합니다.

<a name="multiselect"></a>
### 다중 선택 (Multi-select)

사용자가 여러 옵션을 고르게 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 안내 메시지 지정도 가능합니다:

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

연관 배열로 옵션을 지정하면 선택한 키가 반환됩니다:

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

최대 5개 항목까지 표시 후 스크롤이 시작되며, `scroll` 인수로 조절할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 입력 값 필수화

기본적으로 사용자가 0개 이상 옵션을 선택할 수 있습니다. 1개 이상을 반드시 선택하도록 하려면 `required` 인수를 넘기세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

커스텀 유효성 메시지도 문자열로 지정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검사

특정 옵션을 비활성화하려면 `validate` 인수에 클로저를 전달하세요:

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

`options`가 연관 배열일 경우 선택된 키가, 아니면 값이 클로저에 전달됩니다. 클로저는 오류 메시지 문자열 또는 `null`을 반환해야 합니다.

<a name="suggest"></a>
### 추천 (Suggest)

`suggest` 함수는 선택지 자동완성 기능을 제공합니다. 사용자는 자동완성 힌트를 참고하되 자유롭게 답변할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또한 클로저를 두 번째 인수로 전달할 수 있습니다. 사용자가 입력할 때마다 호출되어 제안 목록을 반환해야 합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 메시지도 함께 쓸 수 있습니다:

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
#### 필수 입력 값

입력을 필수로 지정하려면 `required` 인수를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

유효성 메시지 커스터마이징도 가능합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검사

추가 검증 로직용 클로저도 전달할 수 있습니다:

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

Laravel validator 배열도 사용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색 (Search)

옵션이 많은 경우 `search` 함수를 사용하면 사용자가 입력하는 검색어로 미리 결과를 필터링 할 수 있습니다. 화살표키로 선택합니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

`options` 클로저는 지금까지 입력된 문자열을 받고 배열을 반환해야 합니다. 반환값이 연관 배열이면 키가, 아니면 값이 선택 결과로 반환됩니다.

값을 반환할 때는 `array_values` 또는 Laravel 컬렉션의 `values()`를 사용하여 배열이 연관 배열이 되지 않도록 해야 합니다:

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

플레이스홀더와 안내 메시지도 넣을 수 있습니다:

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

최대 5개까지 표시 후 스크롤이 시작됩니다. `scroll` 인수로 조절 가능합니다:

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
#### 추가 유효성 검사

추가 검증 로직용 클로저도 전달할 수 있습니다:

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

`options`가 연관 배열이면 키, 아니면 값이 클로저로 넘어갑니다. 오류 메시지 또는 `null` 반환을 지원합니다.

<a name="multisearch"></a>
### 다중 검색 (Multi-search)

많은 검색 가능한 항목 중 여러 개를 선택하려면 `multisearch` 함수를 사용해 검색어로 필터링 후, 화살표키와 스페이스바로 선택할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

`options` 클로저는 지금까지 입력한 문자열을 받고 배열을 반환해야 합니다. 연관 배열이면 키가, 아니면 값이 선택 결과로 반환됩니다.

값을 반환할 때는 `array_values` 또는 컬렉션의 `values()`를 사용해 배열이 연관 배열로 바뀌지 않도록 합니다:

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

플레이스홀더와 안내 메시지도 넣을 수 있습니다:

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

스크롤 동작은 `scroll` 인수로 조절합니다:

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
#### 필수 선택 값

기본적으로 사용자가 0개 이상 선택할 수 있습니다. 1개 이상 반드시 선택해야 한다면 `required`를 넘기세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

커스텀 유효성 메시지도 문자열로 지정할 수 있습니다:

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
#### 추가 유효성 검사

검증용 클로저도 넘길 수 있습니다:

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

`options`가 연관 배열이면 키, 아니면 값이 클로저 인수로 넘어갑니다.

<a name="pause"></a>
### 일시정지 (Pause)

`pause` 함수는 사용자에게 안내 문구를 보여주고, Enter 키 입력을 기다립니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검사 전 입력 변환 (Transforming Input Before Validation)

입력 값을 유효성 검사 전에 가공하고 싶을 때가 있습니다. 예를 들어, 문자열 양쪽 공백을 제거하고 싶을 때 `transform` 인수에 클로저를 제공하세요:

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

여러 개 프롬프트를 순서대로 묶어 한 번에 처리하려면 `form` 함수를 사용하세요:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 각 프롬프트 응답을 숫자 인덱스 배열로 반환합니다. 하지만 `name` 인수로 각 프롬프트에 이름을 부여하면, 응답 배열에서 해당 이름으로 접근할 수 있습니다:

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

`form` 함수의 가장 큰 장점은 사용자가 `CTRL + U` 키를 눌러 이전 프롬프트로 돌아가 입력을 수정할 수 있다는 점입니다. 전체 폼을 취소하지 않고도 잘못된 답변을 정정할 수 있습니다.

더 정교한 컨트롤이 필요할 경우, 프롬프트 함수를 직접 호출하는 대신 `add` 메서드에 클로저를 넘기세요. 이때 클로저는 이전까지의 응답을 인수로 받습니다:

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

`note`, `info`, `warning`, `error`, `alert` 함수로 사용자에게 정보 메시지를 표시할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수는 여러 행과 열 형태의 데이터를 간편하게 표시할 수 있게 해줍니다. 열 이름과 데이터를 전달하세요:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스피너 (Spin)

`spin` 함수는 콜백 실행 중 회전하는 스피너와 메시지를 표시합니다. 콜백 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching response...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]
> `spin` 함수는 애니메이션을 위해 `pcntl` PHP 확장 모듈이 필요합니다. 확장이 없으면 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행 바 (Progress Bars)

긴 작업 진행률을 시각적으로 보여주면 좋습니다. `progress` 함수는 콜렉션 등을 순회하며 진행 바를 표시하고, 콜백을 각 항목에 실행합니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 각 콜백 반환값을 배열로 담아 반환합니다.

콜백에 `Laravel\Prompts\Progress` 인스턴스를 추가로 전달받아 라벨이나 힌트도 수정할 수 있습니다:

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

좀 더 수동 제어가 필요하면, 전체 단계 수를 정의하고 `advance` 메서드로 진행도를 갱신할 수 있습니다:

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

사용자의 터미널을 초기화하려면 `clear` 함수를 사용하세요:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 관련 고려사항 (Terminal Considerations)

<a name="terminal-width"></a>
#### 터미널 가로 폭

라벨, 옵션, 유효성 메시지가 터미널 가로 칸 수를 넘으면 자동으로 잘립니다. 좁은 터미널을 사용하는 사용자를 고려해 문자열 길이를 74자 이내로 유지하는 것이 안전합니다(일반적인 80자 터미널 기준).

<a name="terminal-height"></a>
#### 터미널 세로 높이

`scroll` 인수를 받는 프롬프트는 터미널 높이에 맞춰 스크롤 표시할 개수를 자동 조절합니다. 유효성 메시지 공간도 포함합니다.

<a name="fallbacks"></a>
## 미지원 환경 및 대체 방식 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, 그리고 WSL 환경의 Windows를 지원합니다. Windows 환경에서는 PHP 자체의 한계로 인해 WSL 외 환경에서는 사용 불가능합니다.

따라서 Laravel Prompts는 대체 구현 방식으로 [Symfony Console Question Helper](https://symfony.com/doc/7.0/components/console/helpers/questionhelper.html) 같은 방법을 지원합니다.

> [!NOTE]
> Laravel 프레임워크와 함께 사용할 때는 각 프롬프트별 대체 방식이 자동으로 설정되어 미지원 환경에선 자동 적용됩니다.

<a name="fallback-conditions"></a>
#### 대체 사용 조건 설정

Laravel을 사용하지 않거나 대체 사용 조건을 조절하려면, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언 값을 넘기세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 방식 정의

대체 동작 방식을 커스터마이징하려면, 각각 프롬프트 클래스에서 `fallbackUsing` 정적 메서드에 클로저를 설정하세요:

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

대체 방식은 각 프롬프트 클래스마다 개별 설정해야 하며, 클로저는 프롬프트 객체를 받습니다. 반드시 프롬프트에 적합한 반환값을 내야 합니다.