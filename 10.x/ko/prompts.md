# 프롬프트 (Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [추천](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시 정지](#pause)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스핀](#spin)
- [진행 바](#progress)
- [터미널 고려사항](#terminal-considerations)
- [지원하지 않는 환경 및 대체방법](#fallbacks)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Prompts](https://github.com/laravel/prompts)는 아름답고 사용하기 쉬운 폼을 커맨드라인 애플리케이션에 추가할 수 있는 PHP 패키지로, 브라우저에서 사용하는 플레이스홀더 텍스트와 유효성 검증 같은 기능을 제공합니다.

<img src="https://laravel.com/img/docs/prompts-example.png" />

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/10.x/artisan#writing-commands)에서 사용자 입력을 받을 때 이상적이지만, 모든 PHP 기반 커맨드라인 프로젝트에서 사용할 수도 있습니다.

> [!NOTE]  
> Laravel Prompts는 macOS, Linux, 그리고 Windows WSL 환경을 지원합니다. 자세한 내용은 [지원하지 않는 환경 및 대체방법](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치 (Installation)

Laravel Prompts는 최신 Laravel 릴리스에 기본 포함되어 있습니다.

다른 PHP 프로젝트에 Composer 패키지 매니저를 사용해 설치할 수도 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트 (Available Prompts)

<a name="text"></a>
### 텍스트 (Text)

`text` 함수는 사용자에게 질문을 보여주고 입력을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더 텍스트, 기본값, 정보 힌트도 포함할 수 있습니다:

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

검증 메시지를 커스텀하려면 문자열도 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 검증 (Additional Validation)

추가 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력된 값을 받고, 검증 실패 시 오류 메시지를, 성공 시에는 `null`을 반환해야 합니다.

<a name="password"></a>
### 비밀번호 (Password)

`password` 함수는 `text` 함수와 비슷하지만, 입력할 때 콘솔에서 사용자의 입력이 가려집니다. 비밀번호와 같은 민감정보 입력에 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더 텍스트와 정보 힌트도 포함할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수 값 (Required Values)

값 입력을 반드시 요구하려면 `required` 인수를 전달하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

검증 메시지를 커스텀하려면 문자열도 전달할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 검증 (Additional Validation)

추가 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달하세요:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

클로저는 입력된 값을 받고, 검증 실패 시 오류 메시지를, 성공 시에는 `null`을 반환해야 합니다.

<a name="confirm"></a>
### 확인 (Confirm)

"예" 또는 "아니오"를 묻고 싶을 때 `confirm` 함수를 사용하세요. 사용자는 화살표 키나 `y`, `n` 키로 응답할 수 있습니다. 이 함수는 `true` 또는 `false`를 반환합니다:

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예"/"아니오" 문구 수정, 정보 힌트도 포함할 수 있습니다:

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
#### "예" 응답 강제 (Requiring "Yes")

필요하다면 `required` 인수를 통해 사용자에게 "예"를 선택하도록 강제할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

검증 메시지를 커스텀하려면 문자열도 전달할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 선택 (Select)

미리 정의된 옵션 중에서 선택하게 하려면 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    'What role should the user have?',
    ['Member', 'Contributor', 'Owner'],
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

연관 배열을 `options`에 전달하면, 선택된 값 대신 해당 키가 반환됩니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner'
    ],
    default: 'owner'
);
```

리스트가 스크롤되기 전에 최대 다섯 개 옵션이 표시됩니다. `scroll` 인수로 표시 개수를 조절할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 검증 (Validation)

다른 프롬프트와 달리 `select`는 아무것도 선택하지 않는 것이 불가능하므로 `required` 인수를 받지 않습니다. 대신, 특정 옵션의 선택을 금지하고 싶을 경우 `validate` 인수에 클로저를 전달하세요:

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner'
    ],
    validate: fn (string $value) =>
        $value === 'owner' && User::where('role', 'owner')->exists()
            ? 'An owner already exists.'
            : null
);
```

`options`가 연관 배열이면 클로저는 선택된 키를 받고, 아니면 값이 전달됩니다. 클로저는 오류 메시지 또는 검증 통과 시 `null`을 반환해야 합니다.

<a name="multiselect"></a>
### 다중 선택 (Multi-select)

사용자가 여러 옵션을 선택하도록 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    'What permissions should be assigned?',
    ['Read', 'Create', 'Update', 'Delete']
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

연관 배열을 `options`에 전달하면, 선택된 옵션의 값 대신 키가 반환됩니다:

```
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete'
    ],
    default: ['read', 'create']
);
```

기본적으로 다섯 개 옵션이 표시된 후 리스트가 스크롤됩니다. `scroll` 인수로 표시 개수를 조절할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값 선택 강제 (Requiring a Value)

기본적으로 사용자는 0개 이상의 옵션을 선택할 수 있습니다. 하나 이상의 선택을 강제로 요구하려면 `required` 인수를 전달하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true,
);
```

검증 메시지를 커스텀하려면 문자열을 전달할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category',
);
```

<a name="multiselect-validation"></a>
#### 검증 (Validation)

특정 옵션의 선택을 금지하려면 `validate` 인수에 클로저를 전달하세요:

```
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete'
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

`options`가 연관 배열이라면 클로저는 선택된 키 배열을, 아니라면 값 배열을 받습니다. 클로저는 오류 메시지 또는 검증 통과 시 `null`을 반환해야 합니다.

<a name="suggest"></a>
### 추천 (Suggest)

`suggest` 함수는 자동완성 기능을 제공합니다. 하지만 사용자는 자동완성 목록에 포함되지 않은 답변도 가능하게 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수에 클로저를 전달할 수 있습니다. 이 클로저는 사용자가 입력할 때마다 호출되며, 현재까지 입력된 문자열을 매개변수로 받아 자동완성 옵션들의 배열을 반환해야 합니다:

```php
$name = suggest(
    'What is your name?',
    fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더 텍스트, 기본값, 정보 힌트도 포함할 수 있습니다:

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

값 입력을 반드시 요구하려면 `required` 인수를 전달하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

검증 메시지를 커스텀하려면 문자열도 전달할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 검증 (Additional Validation)

추가 검증 로직을 수행하려면 `validate` 인수에 클로저를 전달하세요:

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

클로저는 입력된 값을 받고, 검증 실패 시 오류 메시지를, 성공 시에는 `null`을 반환해야 합니다.

<a name="search"></a>
### 검색 (Search)

옵션이 많을 때, `search` 함수는 사용자가 검색어를 입력해 결과를 필터링한 뒤 화살표 키로 선택할 수 있도록 해줍니다:

```php
use function Laravel\Prompts\search;

$id = search(
    'Search for the user that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 입력한 문자열을 받으며, 옵션 배열을 반환해야 합니다. 연관 배열이면 선택된 옵션의 키를, 아니면 값을 반환합니다.

플레이스홀더 텍스트와 정보 힌트도 포함할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 다섯 개 옵션이 표시된 후 스크롤됩니다. `scroll` 인수로 표시 개수를 조절할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
#### 검증 (Validation)

추가 검증을 하려면 `validate` 인수에 클로저를 전달할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

`options`가 연관 배열이면 클로저는 선택한 키를, 아니면 값을 받습니다. 클로저는 오류 메시지나 검증 통과 시 `null`을 반환해야 합니다.

<a name="multisearch"></a>
### 다중 검색 (Multi-search)

많은 검색 옵션 중에서 사용자가 여러 항목을 선택할 수 있게 하려면 `multisearch` 함수를 사용하세요. 검색어를 입력해 결과를 필터링 후 화살표 키와 스페이스바로 선택합니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 현재 입력 문자열을 받고 옵션 배열을 반환해야 합니다. 연관 배열이면 선택한 키 배열을, 아니면 값 배열을 반환합니다.

플레이스홀더 텍스트와 정보 힌트도 포함할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

기본적으로 다섯 개 옵션이 표시된 후 스크롤됩니다. `scroll` 인수로 표시 개수를 조절할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-required"></a>
#### 값 선택 강제 (Requiring a Value)

기본적으로 사용자는 0개 이상의 옵션을 선택할 수 있습니다. 하나 이상의 선택을 강제로 요구하려면 `required` 인수를 전달하세요:

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true,
);
```

검증 메시지를 커스텀하려면 문자열을 전달할 수 있습니다:

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
#### 검증 (Validation)

추가 검증 로직이 필요하다면 `validate` 인수에 클로저를 전달하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::where('name', 'like', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';
        }
    }
);
```

`options`가 연관 배열일 경우 클로저는 선택된 키 배열을, 아니면 선택된 값 배열을 받습니다. 클로저는 오류 메시지 또는 `null`을 반환해야 합니다.

<a name="pause"></a>
### 일시 정지 (Pause)

`pause` 함수는 사용자에게 정보 메시지를 보여주고, Enter/Return 키를 눌러 계속 진행할 때까지 기다립니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="informational-messages"></a>
## 정보 메시지 (Informational Messages)

`note`, `info`, `warning`, `error`, `alert` 함수는 사용자에게 정보 메시지를 출력할 때 사용할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 (Tables)

`table` 함수는 여러 행과 열의 데이터를 쉽게 출력할 수 있게 해줍니다. 컬럼 이름과 데이터만 전달하면 됩니다:

```php
use function Laravel\Prompts\table;

table(
    ['Name', 'Email'],
    User::all(['name', 'email'])
);
```

<a name="spin"></a>
## 스핀 (Spin)

`spin` 함수는 콜백 실행 중 스피너와 메시지를 보여줍니다. 진행 중임을 표시하고, 콜백 실행 후 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    fn () => Http::get('http://example.com'),
    'Fetching response...'
);
```

> [!WARNING]  
> 스피너 애니메이션을 위해 `spin` 함수는 `pcntl` PHP 확장 모듈이 필요합니다. 해당 확장이 없으면 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행 바 (Progress Bars)

오래 걸리는 작업에 진행 상황을 보여주면 유용합니다. `progress` 함수를 사용하면 Laravel이 진행 바를 표시하며, 주어진 반복 가능한 값의 각 항목 처리 후 진행도를 자동으로 갱신합니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user),
);
```

`progress` 함수는 콜백 실행 결과를 배열로 반환하며, `map` 함수처럼 동작합니다.

콜백에서 `\Laravel\Prompts\Progress` 인스턴스를 받아 각 단계의 레이블과 힌트를 수정할 수도 있습니다:

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
    hint: 'This may take some time.',
);
```

진행 바 제어를 직접 하고 싶으면 총 스텝 수를 지정하여 시작 후 각 작업 완료마다 `advance` 메서드로 진행을 갱신하고, 완료 시 `finish` 메서드를 호출하세요:

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

<a name="terminal-considerations"></a>
## 터미널 고려사항 (Terminal Considerations)

<a name="terminal-width"></a>
### 터미널 가로 길이 (Terminal Width)

레이블, 옵션, 검증 메시지가 사용자의 터미널 칸 수보다 길면 자동으로 잘리므로, 보다 좁은 터미널 사용자를 위해 가능한 짧게 작성하는 것이 좋습니다. 일반적으로 80칸 터미널에서는 74자 내외가 안전한 최대 길이입니다.

<a name="terminal-height"></a>
### 터미널 세로 길이 (Terminal Height)

`scroll` 인수를 사용하는 프롬프트에서 설정한 값은 검증 메시지 공간을 포함해 사용자 터미널 높이에 맞춰 자동으로 줄어듭니다.

<a name="fallbacks"></a>
## 지원하지 않는 환경 및 대체방법 (Unsupported Environments and Fallbacks)

Laravel Prompts는 macOS, Linux, Windows WSL 환경만 지원합니다. Windows PHP 버전의 한계로 WSL 외 Windows에서는 Laravel Prompts 사용이 불가능합니다.

이 때문에 Laravel Prompts는 [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html) 같은 대체 구현체로 폴백하는 기능을 지원합니다.

> [!NOTE]  
> Laravel 프레임워크와 함께 사용할 때는 각 프롬프트별 대체 코드가 설정되어 있어, 환경에 따라 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
### 폴백 조건 (Fallback Conditions)

Laravel을 사용하지 않거나 폴백 조건을 커스텀하고 싶다면, `Prompt` 클래스의 `fallbackWhen` 메서드에 불리언 값을 전달할 수 있습니다:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
### 폴백 동작 (Fallback Behavior)

Laravel을 사용하지 않거나 각 프롬프트 클래스별 폴백 동작을 커스텀하려면, 각 프롬프트 클래스의 `fallbackUsing` 메서드에 클로저를 전달하세요:

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(is_string($prompt->required) ? $prompt->required : 'Required.');
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

폴백은 각 프롬프트 클래스마다 개별 설정이 필요하며, 클로저는 해당 프롬프트 인스턴스를 받고 프롬프트에 맞는 적절한 결과 값을 반환해야 합니다.