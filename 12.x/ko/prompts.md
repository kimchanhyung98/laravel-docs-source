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
- [유효성 검증 전 입력값 변환](#transforming-input-before-validation)
- [폼](#forms)
- [안내 메시지](#informational-messages)
- [테이블](#tables)
- [회전 애니메이션](#spin)
- [진행 바](#progress)
- [터미널 화면 지우기](#clear)
- [터미널 고려사항](#terminal-considerations)
- [지원되지 않는 환경과 대체 방법](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가할 수 있게 해주는 PHP 패키지로, 플레이스홀더 텍스트나 유효성 검증 등 브라우저와 유사한 기능을 지원합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [아티즌 콘솔 명령어](/docs/12.x/artisan#writing-commands)에서 사용자 입력을 받을 때 매우 적합하며, 그 외 모든 명령줄 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL 포함)를 지원합니다. 자세한 내용은 [지원되지 않는 환경과 대체 방법](#fallbacks) 문서를 참고하시기 바랍니다.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 버전의 라라벨에는 이미 포함되어 있습니다.

Laravel Prompts를 다른 PHP 프로젝트에 별도로 설치하려면 Composer 패키지 매니저를 사용하세요:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 지정된 질문을 사용자에게 보여주고, 입력을 받아 그 값을 반환합니다.

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
#### 필수 값 입력

값 입력이 필수라면 `required` 인수를 전달합니다.

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 메시지를 커스텀하고 싶다면 문자열을 전달할 수도 있습니다.

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증 로직이 필요하다면, `validate` 인수로 클로저를 전달할 수 있습니다.

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

클로저에는 입력값이 전달되며, 오류 메시지를 반환하거나 유효할 경우 `null`을 반환하면 됩니다.

또는, 라라벨의 [유효성 검증기](/docs/12.x/validation)를 활용할 수 있습니다. 이 경우 `validate` 인수로 속성명과 원하는 유효성 규칙을 포함하는 배열을 전달하세요.

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트에어리어

`textarea` 함수는 지정된 질문을 사용자에게 보여주고, 여러 줄 입력값을 받아 반환합니다.

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

이 함수도 플레이스홀더, 기본값, 안내 힌트를 받을 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수 값 입력

값 입력이 필수라면 `required` 인수를 전달하세요.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열을 지정할 수 있습니다.

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증 로직이 필요하다면, `validate` 인수로 클로저를 전달할 수 있습니다.

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

클로저에는 입력값이 전달되며, 오류 메시지를 반환하거나 유효할 경우 `null`을 반환하면 됩니다.

또는, 라라벨의 [유효성 검증기](/docs/12.x/validation)를 사용할 수도 있습니다. 속성명과 원하는 유효성 규칙을 포함한 배열을 전달하세요.

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 패스워드

`password` 함수는 `text` 함수와 비슷하지만, 사용자가 콘솔에 입력할 때 입력값이 마스킹(표시가 가려짐)됩니다. 따라서 비밀번호 등 민감한 정보를 받을 때 적합합니다.

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 힌트도 입력할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값 입력

입력이 필수라면 `required` 인수를 전달하세요.

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 메시지를 직접 지정하고 싶다면 문자열로 전달합니다.

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검증

추가적인 유효성 검증 로직이 필요하다면, `validate` 인수로 클로저를 전달할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

입력값이 클로저로 전달되며, 오류 메시지를 반환하거나 유효할 경우 `null`을 반환하면 됩니다.

또는 라라벨의 [유효성 검증기](/docs/12.x/validation)를 사용할 수 있습니다. 속성명과 원하는 유효성 규칙이 담긴 배열을 전달하세요.

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인

사용자에게 '예' 또는 '아니오'를 확인하도록 물을 필요가 있을 때는 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키 또는 `y`, `n` 키로 응답을 선택할 수 있습니다. 이 함수는 `true` 또는 `false`를 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예"와 "아니오"의 라벨, 추가 안내 힌트도 지정할 수 있습니다.

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
#### "예" 필수 선택

필요하다면, 사용자에게 반드시 "예"를 선택하도록 `required` 인수를 전달할 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열로 지정할 수 있습니다.

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택

사용자에게 미리 정의된 여러 선택지 중 하나를 고르게 할 때는 `select` 함수를 사용할 수 있습니다.

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값이나 안내 힌트도 지정할 수 있습니다.

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

선택된 값 대신 선택된 키를 반환받으려면 `options` 인수에 연관 배열을 전달할 수 있습니다.

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

기본적으로 다섯 개까지의 선택지가 한 번에 표시되며, 그 이상일 경우 스크롤이 만들어집니다. `scroll` 인수를 통해 표시 개수를 직접 설정할 수 있습니다.

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 유효성 검증

다른 프롬프트 함수와 달리, `select` 함수는 값을 선택하지 않는 상황이 발생하지 않으므로 `required` 인수를 사용하지 않습니다. 그러나 특정 선택지를 보여주되, 선택을 막고 싶을 경우 `validate` 인수로 클로저를 전달할 수 있습니다.

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

`options` 인수에 연관 배열을 전달하면 클로저로 선택된 키가, 단순 배열을 전달하면 선택된 값이 전달됩니다. 클로저는 오류 메시지 또는 `null`을 반환할 수 있습니다.

<a name="multiselect"></a>
### 다중 선택

여러 개의 옵션을 사용자가 동시에 선택할 수 있도록 하려면 `multiselect` 함수를 사용하세요.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

여러 기본값 또는 안내 힌트도 지정할 수 있습니다.

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

선택된 값 대신 선택된 키들을 반환받으려면 `options` 인수에 연관 배열을 전달하세요.

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

기본적으로 다섯 개까지의 선택지가 한 번에 표시되며, 그 이상일 경우 목록에 스크롤이 생성됩니다. `scroll` 인수로 표시 개수를 조정할 수 있습니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수 선택 값

기본적으로 사용자는 아무 옵션도 선택하지 않을 수도 있습니다. 한 개 이상의 값을 반드시 선택하도록 제한하려면 `required` 인수를 사용하세요.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

유효성 메시지를 직접 커스텀하려면 `required` 인수에 문자열을 지정할 수 있습니다.

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 유효성 검증

특정 옵션은 보여주면서 선택을 막고 싶을 때, `validate` 인수로 클로저를 전달하여 제한할 수 있습니다.

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

`options` 인수가 연관 배열이면 선택된 키들이, 단순 배열이면 선택된 값들이 클로저로 전달됩니다. 클로저는 오류 메시지 또는 `null`을 반환할 수 있습니다.

<a name="suggest"></a>
### 추천

`suggest` 함수는 자동 완성 기능을 통해 선택할 수 있는 값을 추천할 수 있습니다. 단, 사용자는 추천 값과 상관 없이 자유롭게 입력할 수도 있습니다.

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또한, `suggest` 함수의 두 번째 인수로 클로저를 전달할 수도 있습니다. 이 경우 사용자가 글자를 입력할 때마다 클로저가 호출되며, 현재까지 입력한 값을 받아 자동완성 후보 배열을 반환해야 합니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 힌트도 지정할 수 있습니다.

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
#### 필수 값 입력

입력이 필수라면 `required` 인수를 사용하세요.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열로 지정할 수 있습니다.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검증

추가 유효성 검증 로직이 필요하다면, `validate` 인수로 클로저를 전달할 수 있습니다.

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

클로저에는 입력값이 전달되며, 오류 메시지를 반환하거나 유효할 경우 `null`을 반환하면 됩니다.

또는, 라라벨의 [유효성 검증기](/docs/12.x/validation)를 사용할 수 있습니다. 속성명과 원하는 유효성 규칙이 포함된 배열을 전달하세요.

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색

사용자가 선택할 수 있는 옵션이 많은 경우, `search` 함수를 사용하면 사용자가 검색어를 입력해 결과를 필터링하고, 방향키로 원하는 값을 선택할 수 있습니다.

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저에는 지금까지 사용자가 입력한 텍스트가 인수로 전달되며, 옵션들의 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 옵션의 키가, 일반 배열을 반환하면 값이 반환됩니다.

값 배열에서 값을 반환하려면 배열이 연관 배열이 되지 않도록, `array_values` 함수나 컬렉션의 `values` 메서드를 사용하는 것이 좋습니다.

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

플레이스홀더나 안내 메시지도 함께 지정할 수 있습니다.

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

최대 다섯 개까지의 옵션이 스크롤 없이 노출되며, `scroll` 인수로 한 번에 표시할 옵션 개수를 조절할 수 있습니다.

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

추가 유효성 검증 로직이 필요하다면, `validate` 인수로 클로저를 전달할 수 있습니다.

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

`options` 클로저가 연관 배열을 반환하면 선택된 키가, 일반 배열이면 선택된 값이 클로저로 전달됩니다. 클로저는 오류 메시지 또는 `null`을 반환할 수 있습니다.

<a name="multisearch"></a>
### 다중 검색

검색 옵션이 매우 많고 여러 항목을 동시에 선택해야 한다면, `multisearch` 함수로 사용자가 직접 검색어를 입력해 결과를 필터링한 후, 방향키와 스페이스바로 여러 항목을 선택할 수 있습니다.

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저에는 현재까지 사용자가 입력한 텍스트가 전달되며, 옵션들의 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 항목의 키들이, 일반 배열을 반환하면 선택된 값들이 반환됩니다.

값 배열에서 값을 반환하려면 배열이 연관 배열이 되지 않도록, `array_values` 함수나 컬렉션의 `values` 메서드를 사용하는 것이 좋습니다.

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

플레이스홀더나 안내 메시지도 함께 지정할 수 있습니다.

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

기본적으로 다섯 개까지의 옵션이 한 번에 표시되며, `scroll` 인수로 표시 개수를 직접 설정할 수 있습니다.

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

기본적으로 사용자는 아무 옵션도 선택하지 않을 수 있습니다. 한 개 이상의 값을 필수로 선택하도록 하려면 `required` 인수를 지정하세요.

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

유효성 메시지를 직접 커스텀하려면 `required` 인수에 문자열을 제공할 수 있습니다.

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

추가적인 유효성 검증 로직이 필요하다면, `validate` 인수에 클로저를 전달할 수 있습니다.

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

만약 `options` 클로저에서 연관 배열을 반환한다면, 해당 클로저는 선택된 키를 전달받게 됩니다. 그 외의 경우에는 선택된 값을 전달받습니다. 이 클로저에서 에러 메시지를 반환하거나, 검증이 통과할 경우에는 `null`을 반환하면 됩니다.

<a name="pause"></a>
### 일시 정지

`pause` 함수는 사용자에게 정보를 출력한 뒤, Enter 또는 Return 키를 누를 때까지 대기하도록 할 수 있습니다.

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 유효성 검증 전 입력값 변환

때로는 유효성 검증 전에 프롬프트 입력값을 변환하고 싶을 때가 있습니다. 예를 들어, 입력받은 문자열에서 공백을 제거하고자 할 수 있습니다. 이를 위해, 대부분의 프롬프트 함수는 클로저를 받는 `transform` 인수를 제공합니다.

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

여러 개의 프롬프트를 순차적으로 표시하여 정보를 수집한 후, 추가 작업을 수행해야 할 때가 많습니다. 이럴 때, `form` 함수를 사용하여 사용자가 입력을 모두 완료해야 하는 그룹 형태의 프롬프트 집합을 만들 수 있습니다.

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 폼 내의 모든 프롬프트 응답을 숫자 인덱스를 가진 배열로 반환합니다. 하지만 각 프롬프트에 `name` 인수를 설정해주면 지정한 이름을 통해 해당 프롬프트의 응답을 접근할 수 있습니다.

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

`form` 함수를 사용할 주요 이점은 사용자가 `CTRL + U` 단축키를 통해 폼 내 이전 프롬프트로 돌아갈 수 있다는 점입니다. 덕분에 전체 폼을 취소하고 다시 시작하지 않아도 실수를 수정하거나 선택을 변경할 수 있습니다.

더 세밀하게 프롬프트를 제어하려면, 프롬프트 함수를 직접 호출하는 대신 `add` 메서드를 호출할 수 있습니다. `add` 메서드에는 지금까지 사용자가 입력한 이전 응답들이 전달됩니다.

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
## 정보성 메시지 출력

`note`, `info`, `warning`, `error`, `alert` 함수들은 다양한 정보 메시지를 출력할 수 있도록 도와줍니다.

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블

`table` 함수는 여러 행과 컬럼(열)로 구성된 데이터를 간편하게 출력할 수 있게 해줍니다. 출력할 테이블의 컬럼명과 실제 데이터를 전달해주기만 하면 됩니다.

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(Spin)

`spin` 함수는 특정 콜백을 실행하는 동안 스피너와 선택적으로 메시지를 함께 표시해줍니다. 이는 사용자가 진행 중인 작업을 인지할 수 있도록 도와주며, 작업이 완료되면 콜백의 반환값을 그대로 반환합니다.

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> `spin` 함수는 스피너 애니메이션을 위해 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다. 해당 확장이 없을 경우, 애니메이션 대신 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행률 표시줄(Progress Bars)

실행 시간이 오래 걸릴 수 있는 작업에서는 작업이 얼마나 진행되었는지 보여주는 진행률 표시줄이 유용합니다. `progress` 함수를 활용하면, 지정한 반복 가능한 값(Iterable)을 순회할 때마다 자동으로 진행률 표시줄을 갱신할 수 있습니다.

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map 함수처럼 동작하며, 콜백의 반환값을 담은 배열을 반환합니다.

콜백에서 `Laravel\Prompts\Progress` 인스턴스를 추가적으로 받아 각 반복마다 라벨이나 힌트를 동적으로 변경할 수도 있습니다.

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

진행률 표시줄을 좀 더 수동으로 제어해야 할 상황도 있을 수 있습니다. 이럴 때는 작업을 순회할 전체 단계 수를 먼저 지정하고, 각 항목 처리 후 `advance` 메서드로 진행률을 직접 갱신할 수 있습니다.

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
## 터미널 화면 초기화

`clear` 함수를 사용해서 사용자의 터미널 화면을 깨끗하게 지울 수 있습니다.

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 환경 고려사항

<a name="terminal-width"></a>
#### 터미널 너비

라벨, 옵션, 또는 유효성 검증 메시지 등 어떤 문자열이든 사용자의 터미널 "컬럼" 수보다 길 경우, 자동으로 잘려서 표시됩니다. 사용자가 좁은 터미널 환경에서 이용할 수도 있으므로, 문자열 길이를 되도록 짧게 작성하는 것이 좋습니다. 80 컬럼 터미널을 지원하기 위해 일반적으로 안전한 최대 길이는 74자입니다.

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인수를 받는 프롬프트의 경우, 설정된 scroll 값이 터미널 높이에 맞게 자동으로 줄어들며, 유효성 메시지가 표시될 공간도 함께 고려됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경 및 대체(fallback) 처리

Laravel Prompts는 macOS, Linux, Windows (WSL)에서 지원됩니다. 하지만 PHP의 Windows 버전 한계로 WSL 외의 Windows 환경에서는 라라벨 프롬프트를 사용할 수 없습니다.

이러한 이유로 라라벨 프롬프트는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현 방식으로 처리할 수 있습니다.

> [!NOTE]
> 라라벨 프레임워크와 함께 Prompts를 사용할 경우, 모든 프롬프트에 대해 대체(fallback)가 이미 설정되어 있으며, 지원되지 않는 환경에서는 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체(fallback) 조건 설정

라라벨을 사용하지 않거나, 대체 동작이 적용되는 조건을 직접 제어해야 하는 경우, `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불린 값을 전달할 수 있습니다.

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체(fallback) 동작 커스터마이즈

라라벨을 사용하지 않거나, 대체 동작 자체를 직접 커스터마이즈하려면, 각 프롬프트 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달할 수 있습니다.

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

대체 동작은 프롬프트 클래스별로 각각 따로 설정해주어야 합니다. 클로저는 해당 프롬프트 클래스의 인스턴스를 전달받고, 해당 프롬프트에 적합한 값을 반환해야 합니다.