# 프롬프트(Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [자동완성 제안](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [안내 메시지](#informational-messages)
- [테이블](#tables)
- [스핀(Spin)](#spin)
- [진행 바](#progress)
- [터미널 관련 고려사항](#terminal-considerations)
- [지원되지 않는 환경 및 폴백](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 명령행 애플리케이션에 플레이스홀더 텍스트, 유효성 검사 등 브라우저 유사 기능을 갖춘 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지입니다.

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel Prompts는 [Artisan 콘솔 커맨드](/docs/{{version}}/artisan#writing-commands)에서 사용자 입력을 받을 때 특히 이상적이지만, 모든 명령행 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]  
> Laravel Prompts는 macOS, Linux, 그리고 WSL이 설치된 Windows를 지원합니다. 자세한 내용은 [지원되지 않는 환경 및 폴백](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 Laravel에 기본 포함되어 있습니다.

다른 PHP 프로젝트에서도 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 사용자에게 질문을 표시하고, 입력을 받아 이를 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더, 기본값, 그리고 안내 힌트도 추가할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: '예: Taylor Otwell',
    default: $user?->name,
    hint: '이 정보는 프로필에 표시됩니다.'
);
```

<a name="text-required"></a>
#### 필수 입력값

값 입력이 필수일 경우 `required` 인자를 사용할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

유효성 메시지를 커스텀하고 싶다면 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: '이름은 필수 입력값입니다.'
);
```

<a name="text-validation"></a>
#### 추가 유효성 검사

추가적인 유효성 검사를 원한다면, `validate` 인자에 클로저를 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => '이름은 최소 3자 이상이어야 합니다.',
        strlen($value) > 255 => '이름은 255자를 초과할 수 없습니다.',
        default => null
    }
);
```

클로저는 입력된 값을 받아 오류 메시지를 반환하거나, 유효한 경우 `null`을 반환해야 합니다.

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 유사하지만, 입력값을 콘솔에서 마스킹해 표시합니다. 비밀번호 등 민감한 정보를 받을 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더와 안내 힌트도 입력할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: '최소 8자 이상.'
);
```

<a name="password-required"></a>
#### 필수 입력값

값 입력이 필수일 경우 `required` 인자를 사용할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

유효성 메시지를 커스텀하고 싶다면 문자열을 전달할 수도 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: '비밀번호는 필수 입력값입니다.'
);
```

<a name="password-validation"></a>
#### 추가 유효성 검사

추가 유효성 검사는 `validate` 인자에 클로저를 전달해 구현할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => '비밀번호는 최소 8자 이상이어야 합니다.',
        default => null
    }
);
```

클로저는 입력값을 받아 에러 메시지 또는 `null`을 반환해야 합니다.

<a name="confirm"></a>
### 확인

사용자에게 "예/아니오" 확인을 받으려면 `confirm` 함수를 사용할 수 있습니다. 사용자는 방향키 또는 `y`, `n` 키로 답을 선택할 수 있으며, 반환값은 `true` 또는 `false`입니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예"/"아니오" 레이블 커스텀, 안내 힌트도 추가할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: '동의',
    no: '동의하지 않음',
    hint: '계속하려면 약관에 동의해야 합니다.'
);
```

<a name="confirm-required"></a>
#### "예" 강제 선택

사용자에게 반드시 "예"를 선택하게 하려면 `required` 인자를 사용할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

유효성 메시지를 커스텀하고 싶으면 문자열을 사용할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: '계속하려면 약관을 반드시 동의해야 합니다.'
);
```

<a name="select"></a>
### 선택

미리 정의된 옵션 중에서 선택받으려면 `select` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\select;

$role = select(
    'What role should the user have?',
    ['Member', 'Contributor', 'Owner'],
);
```

기본 선택값, 안내 힌트도 선택할 수 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: '역할은 언제든 변경이 가능합니다.'
);
```

선택된 옵션 값이 아닌, 해당 키를 반환받으려면 연관 배열을 사용하면 됩니다:

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

기본적으로 최대 5개 옵션만 표시되고 그 이상은 스크롤 됩니다. `scroll` 인자로 표시 개수를 조절할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 유효성 검사

`select` 함수는 아무것도 선택하지 않는 것이 불가능하므로 `required` 인자를 받지 않습니다. 다만, 특정 옵션이 선택될 수 없도록 막으려면 `validate`에 클로저를 전달할 수 있습니다:

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
            ? '소유자는 이미 존재합니다.'
            : null
);
```

`options`가 연관 배열이면 클로저로는 선택된 키가, 그렇지 않으면 값이 전달됩니다. 에러 메시지 또는 `null`을 반환해야 합니다.

<a name="multiselect"></a>
### 다중 선택

사용자가 여러 옵션을 동시에 선택할 수 있게 하려면 `multiselect` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    'What permissions should be assigned?',
    ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값 또는 안내 힌트도 추가할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: '권한은 언제든 변경 가능합니다.'
);
```

선택한 옵션의 키 값만 반환하려면 연관 배열을 전달하면 됩니다:

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

최대 5개 옵션까지 표시되며, `scroll` 인자로 표시 수를 설정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수 선택값

기본적으로 0개 이상의 옵션을 선택할 수 있지만, `required` 인자를 전달하면 최소 1개 이상 선택을 강제할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true,
);
```

유효성 메시지를 커스텀하려면 문자열로 전달할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: '최소 한 가지 카테고리는 선택해야 합니다',
);
```

<a name="multiselect-validation"></a>
#### 유효성 검사

특정 옵션이 선택되지 않도록 하려면 `validate`에 클로저를 전달할 수 있습니다:

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
        ? '모든 사용자는 읽기 권한이 필요합니다.'
        : null
);
```

`options`가 연관 배열이면 선택된 키 배열이, 아니면 값 배열이 전달됩니다. 에러 메시지나, 유효할 경우 `null`을 반환해야 합니다.

<a name="suggest"></a>
### 자동완성 제안

`suggest` 함수는 자동완성 기능이 필요한 경우에 사용합니다. 사용자는 제안 외 다른 답도 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는 클로저를 두 번째 인자로 전달해 동적으로 옵션을 제공할 수 있습니다. 이 클로저는 사용자가 입력할 때마다 호출되어, 현재 입력값을 받아 자동완성 옵션 배열을 반환해야 합니다:

```php
$name = suggest(
    'What is your name?',
    fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내 힌트 역시 추가할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: '예: Taylor',
    default: $user?->name,
    hint: '이 정보는 프로필에 표시됩니다.'
);
```

<a name="suggest-required"></a>
#### 필수 입력값

필수 입력을 강제하려면 `required` 인자를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

유효성 메시지를 커스텀하려면 문자열을 입력하면 됩니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: '이름은 필수 입력값입니다.'
);
```

<a name="suggest-validation"></a>
#### 추가 유효성 검사

추가 유효성 검사는 `validate`에 클로저를 전달하여 구현할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => '이름은 최소 3자 이상이어야 합니다.',
        strlen($value) > 255 => '이름은 255자를 초과할 수 없습니다.',
        default => null
    }
);
```

클로저는 입력값을 받아 에러 메시지 또는 `null`을 반환합니다.

<a name="search"></a>
### 검색

옵션이 많을 때는 `search` 함수를 사용해 사용자가 키 입력으로 검색어를 입력, 필터링 후 화살표로 선택할 수 있도록 할 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    'Search for the user that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력값을 받아 옵션 배열을 반환해야 합니다. 연관 배열이면 선택된 옵션의 키가, 아니면 값이 반환됩니다.

플레이스홀더, 안내 힌트도 추가할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: '예: Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: '선택된 사용자는 곧바로 메일을 받습니다.'
);
```

최대 5개 옵션까지 표시되며, `scroll` 인자로 변경 가능합니다:

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
#### 유효성 검사

추가 유효성 검사는 `validate` 인자에 클로저를 넘겨 구현할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return '이 사용자는 메일 수신을 거부하였습니다.';
        }
    }
);
```

`options` 클로저가 연관 배열을 반환하면 선택된 키가, 아니면 값이 전달됩니다. 에러 메시지 또는 `null`을 반환합니다.

<a name="multisearch"></a>
### 다중 검색

검색 가능한 옵션이 많고, 여러 항목을 선택할 수 있어야 한다면 `multisearch` 함수가 적합합니다. 사용자는 검색 후, 화살표 및 스페이스바로 항목을 선택할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 입력값을 받아 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택된 키 배열이, 아니면 값 배열이 반환됩니다.

플레이스홀더, 안내 힌트도 추가할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    placeholder: '예: Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: '선택된 사용자에게 곧바로 메일이 발송됩니다.'
);
```

최대 5개 옵션까지 표시되며, `scroll` 인자로 변경 가능합니다:

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
#### 필수 선택값

기본적으로 0개 이상의 옵션을 선택할 수 있지만, `required` 인자로 최소 1개 이상을 강제할 수 있습니다:

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true,
);
```

유효성 메시지를 커스텀하려면 문자열로 전달할 수 있습니다:

```php
$ids = multisearch(
    'Search for the users that should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: '최소 한 명 이상의 사용자를 선택해야 합니다.'
);
```

<a name="multisearch-validation"></a>
#### 유효성 검사

추가 유효성 검사는 `validate` 인자에 클로저를 넘겨 구현할 수 있습니다:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::where('name', 'like', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', 그리고 ').'님은 수신 거부 상태입니다.';
        }
    }
);
```

`options` 클로저가 연관 배열을 반환하면 선택된 키 배열이, 아니면 값 배열이 전달됩니다. 에러 메시지 또는 `null`을 반환합니다.

<a name="pause"></a>
### 일시정지

`pause` 함수는 사용자에게 안내 텍스트를 보여주고, Enter/Return 키를 누를 때까지 대기합니다:

```php
use function Laravel\Prompts\pause;

pause('계속하려면 ENTER를 누르세요.');
```

<a name="informational-messages"></a>
## 안내 메시지

`note`, `info`, `warning`, `error`, `alert` 함수들은 안내 메시지 출력을 위해 사용할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('패키지가 성공적으로 설치되었습니다.');
```

<a name="tables"></a>
## 테이블

`table` 함수는 여러 행, 열로 이루어진 데이터를 손쉽게 출력할 수 있습니다. 열 이름과 표에 들어갈 데이터만 제공하세요:

```php
use function Laravel\Prompts\table;

table(
    ['Name', 'Email'],
    User::all(['name', 'email'])
);
```

<a name="spin"></a>
## 스핀(Spin)

`spin` 함수는 콜백이 실행되는 동안 스피너와 메시지를 표시합니다. 진행 중인 작업을 알릴 수 있으며, 완료 후 콜백의 결과값을 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    fn () => Http::get('http://example.com'),
    '응답 받아오는 중...'
);
```

> [!WARNING]  
> `spin` 함수는 스피너 애니메이션 구현을 위해 `pcntl` PHP 확장 모듈이 필요합니다. 이 확장 모듈이 없을 경우, 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행 바(Progress Bars)

작업 시간이 오래 걸릴 경우, 작업의 진행도를 사용자에게 안내하는 것이 유용합니다. `progress` 함수를 사용하면 반복 가능한 객체를 돌면서 진행 바를 표시할 수 있습니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: '사용자 업데이트 중',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user),
);
```

`progress` 함수는 map 함수처럼 동작하며, 콜백의 반환값으로 이루어진 배열을 반환합니다.

콜백에서 `\Laravel\Prompts\Progress` 인스턴스를 받아 라벨/힌트를 각 반복마다 동적으로 적용할 수도 있습니다:

```php
$users = progress(
    label: '사용자 업데이트 중',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("{$user->name} 업데이트 중")
            ->hint("생성일: {$user->created_at}");

        return $this->performTask($user);
    },
    hint: '이 작업에는 시간이 소요될 수 있습니다.',
);
```

직접 진행 바를 제어하려면 전체 단계를 미리 정의하고, 각 항목 처리 후 `advance` 메서드로 수동 갱신할 수 있습니다:

```php
$progress = progress(label: '사용자 업데이트 중', steps: 10);

$users = User::all();

$progress->start();

foreach ($users as $user) {
    $this->performTask($user);

    $progress->advance();
}

$progress->finish();
```

<a name="terminal-considerations"></a>
## 터미널 관련 고려사항

<a name="terminal-width"></a>
#### 터미널 너비

라벨, 옵션, 유효성 메시지의 길이가 사용자의 터미널 "열(column)" 수보다 클 경우 자동으로 잘려서 표시됩니다. 사용자가 좁은 터미널을 사용할 수 있으므로, 이 문자열의 길이를 줄이는 것을 권장합니다. 80자 터미널을 지원하려면 최대 74자 이하가 안전합니다.

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인자를 받는 프롬프트의 경우, 설정한 값이 자동으로 터미널 높이에 맞춰 줄어듭니다(유효성 메시지 공간 포함).

<a name="fallbacks"></a>
## 지원되지 않는 환경 및 폴백

Laravel Prompts는 macOS, Linux, 그리고 WSL 환경의 Windows를 지원합니다. 일반 Windows 버전의 PHP에서는 제약 때문에 WSL 환경 이외에서는 사용이 불가합니다.

그로 인해, [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현으로 자동 폴백을 지원합니다.

> [!NOTE]  
> Laravel 프레임워크와 함께 Laravel Prompts를 사용할 때는 각 프롬프트별로 폴백이 이미 설정되어 있으며, 지원되지 않는 환경에서는 자동으로 활성화됩니다.

<a name="fallback-conditions"></a>
#### 폴백 조건

Laravel을 사용하지 않거나, 폴백 적용 조건을 직접 지정하려면 `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 폴백 동작

Laravel을 사용하지 않거나, 각 프롬프트 클래스의 폴백 동작을 직접 정의하려면, 해당 클래스의 `fallbackUsing` 정적 메서드에 클로저를 전달하세요:

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(is_string($prompt->required) ? $prompt->required : '필수 항목입니다.');
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

각 프롬프트 클래스별로 폴백을 개별 설정해야 합니다. 클로저는 해당 프롬프트 클래스의 인스턴스를 받아 적절한 타입을 반환해야 합니다.