# 프롬프트(Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트영역(Textarea)](#textarea)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [단일 선택(Select)](#select)
    - [다중 선택(Multi-select)](#multiselect)
    - [자동완성 제안(Suggest)](#suggest)
    - [검색(Search)](#search)
    - [다중 검색(Multi-search)](#multisearch)
    - [일시정지(Pause)](#pause)
- [검증 전 입력값 변환](#transforming-input-before-validation)
- [폼(Forms)](#forms)
- [정보 메시지](#informational-messages)
- [테이블 출력](#tables)
- [스핀(Spin)](#spin)
- [진행률 표시줄(Progress Bar)](#progress)
- [터미널 초기화](#clear)
- [터미널 사용 시 유의사항](#terminal-considerations)
- [지원되지 않는 환경 및 폴백](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 명령줄 애플리케이션에 아름답고 사용자 친화적인 폼을 추가할 수 있게 해주는 PHP 패키지입니다. 브라우저와 유사한 플레이스홀더 텍스트와 검증 기능을 포함합니다.

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel Prompts는 [아티즌 콘솔 명령어](/docs/{{version}}/artisan#writing-commands)에서 사용자 입력을 받을 때 탁월하며, 모든 PHP 커맨드라인 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL)에서 지원됩니다. 더 자세한 내용은 [지원되지 않는 환경 및 폴백](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 Laravel 릴리즈에 기본 탑재되어 있습니다.

다른 PHP 프로젝트에서도 Composer 패키지 매니저를 사용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 사용자가 질문에 답변할 수 있도록 입력을 받고, 입력값을 반환합니다.

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더, 기본값, 추가 설명(힌트) 텍스트도 제공할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### 필수값 지정

입력이 반드시 필요하다면 `required` 인자를 넘길 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

검증 메시지를 커스터마이징하려면 문자열을 전달할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### 추가 검증

추가적인 검증 로직이 필요한 경우, `validate` 인자에 클로저를 넘길 수 있습니다:

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

클로저는 입력값을 받아 실패 시 에러 메시지를, 통과 시에는 `null`을 반환해야 합니다.

또는, Laravel의 [validator](/docs/{{version}}/validation) 기능을 활용할 수도 있습니다. 이 경우, 속성명과 검증 규칙을 배열로 전달하면 됩니다:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트영역(Textarea)

`textarea` 함수는 여러 줄로 입력받는 텍스트 영역을 제공하고, 입력값을 반환합니다.

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 추가 설명도 지정할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### 필수값 지정

값이 반드시 필요하다면 `required` 인자를 넘깁니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

검증 메시지를 직접 지정할 수도 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 `validate` 인자에 클로저를 전달하세요:

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

또한, [validator](/docs/{{version}}/validation)를 사용해 검증할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text`와 유사하지만, 입력한 문자가 콘솔에서 마스킹됩니다. 주로 비밀번호와 같이 민감한 정보를 입력받을 때 사용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더 및 설명도 입력 가능합니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### 필수값 지정

입력이 필수라면 `required` 인자를 사용하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

커스텀 메시지도 가능합니다:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### 추가 검증

추가 검증은 `validate` 인자를 통해 클로저로 구현할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

또는 [validator](/docs/{{version}}/validation) 규칙을 사용할 수 있습니다.

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인(Confirm)

"예/아니오"와 같이 사용자의 확답이 필요할 때는 `confirm` 함수를 사용하세요. 사용자는 방향키 또는 `y`, `n` 키로 선택할 수 있습니다. 반환값은 `true` 또는 `false`입니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본값, "예/아니오" 라벨 문구, 안내 문구도 지정할 수 있습니다:

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
#### "예" 강제 선택

사용자로 하여금 반드시 "예"를 선택하도록 하려면 `required` 인자를 사용합니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

검증 메시지를 커스터마이즈하고 싶다면 문자열을 전달하세요:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### 단일 선택(Select)

미리 정해진 항목 중 하나를 선택하게 하려면 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택값과 안내문도 지정할 수 있습니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

`options` 인자에 연관 배열을 전달하면, 선택된 키가 반환됩니다:

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

최대 5개 옵션까지만 스크롤 없이 표시합니다. 표시 개수는 `scroll` 인자로 조정할 수 있습니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 검증

`select` 함수는 아무것도 선택하지 않는 것이 불가능하기 때문에 `required` 인자를 지원하지 않습니다. 그러나 특정 옵션의 선택을 막고 싶으면 `validate`에 클로저를 넘길 수 있습니다:

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

옵션이 연관 배열일 경우 선택된 키가, 그렇지 않으면 선택된 값이 클로저에 전달됩니다.

<a name="multiselect"></a>
### 다중 선택(Multi-select)

여러 옵션을 선택하도록 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택값과 안내문도 지정할 수 있습니다:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

연관 배열을 전달하면, 선택된 옵션의 키 배열이 반환됩니다:

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

최대 5개 옵션까지만 스크롤 없이 표시하며, `scroll` 인자를 통해 조정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 필수값 지정

기본적으로 0개 이상의 옵션을 선택할 수 있습니다. 1개 이상 선택을 강제하려면 `required` 인자를 사용하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

검증 메시지를 직접 입력할 수도 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### 추가 검증

특정 옵션의 선택을 막으려면 `validate`에 클로저를 전달하세요:

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

옵션이 연관 배열일 경우 선택된 키 배열이, 그렇지 않으면 값 배열이 전달됩니다.

<a name="suggest"></a>
### 자동완성 제안(Suggest)

`suggest` 함수는 자동완성 기능이 필요한 경우 사용합니다. 사용자는 자동완성 힌트와 무관하게 어떤 값도 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

두 번째 인자로 클로저를 넘기면, 사용자가 입력할 때마다 실행되어 자동완성 옵션 목록을 반환합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 안내문도 지정할 수 있습니다:

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
#### 필수값 지정

필수 입력이 필요하다면 `required` 인자를 사용하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

검증 메시지를 커스터마이즈하고 싶다면 문자열을 사용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 `validate`에 클로저를 넘기세요:

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

또는 [validator](/docs/{{version}}/validation) 규칙을 사용할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색(Search)

옵션이 많을 때는 `search` 함수를 사용하여 키워드로 검색한 후 선택할 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

클로저는 사용자가 입력한 텍스트를 받아 옵션 배열을 반환해야 합니다. 연관 배열을 반환하면 선택한 옵션의 키가 반환되며, 그렇지 않으면 값이 반환됩니다.

값 배열로 반환할 때는 `array_values` 함수나 `values` 메서드로 인덱스 배열로 변환해야 합니다:

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

플레이스홀더, 안내문도 추가할 수 있습니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

최대 5개 옵션까지만 스크롤 없이 표시하며, `scroll` 인자로 조정 가능합니다:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
#### 추가 검증

추가 검증이 필요하면 `validate`에 클로저를 넘기세요:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn ($value) => strlen($value) > 0
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

옵션 클로저가 연관 배열을 반환하면 키가, 아니면 값이 전달됩니다.

<a name="multisearch"></a>
### 다중 검색(Multi-search)

옵션이 많고 여러 항목을 선택해야 한다면 `multisearch` 함수를 사용할 수 있습니다. 사용자는 입력 후 화살표와 스페이스바로 항목을 다중 선택할 수 있습니다:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for the users that should receive the mail',
    fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

연관 배열을 반환하면 선택된 키 배열이, 아니면 값 배열이 반환됩니다. 값 배열로 반환할 때는 `array_values` 함수를 통해 인덱스 배열로 변환해 주세요.

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

플레이스홀더, 안내문도 추가할 수 있습니다:

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

최대 5개까지만 스크롤 없이 표시하며, `scroll` 인자로 조정할 수 있습니다:

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
#### 필수값 지정

기본적으로 0개 이상의 옵션을 선택할 수 있습니다. 1개 이상 선택을 강제하려면 `required`를 사용하세요:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

검증 메시지를 커스터마이즈하려면 문자열을 전달할 수 있습니다:

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

추가 검증이 필요하다면 `validate`에 클로저를 넘기세요:

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

옵션 클로저가 연관 배열일 때는 키 배열, 그렇지 않으면 값 배열이 전달됩니다.

<a name="pause"></a>
### 일시정지(Pause)

`pause` 함수는 사용자가 ENTER키를 눌러 계속 진행할 때까지 안내 문구를 보여줍니다:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="transforming-input-before-validation"></a>
## 검증 전 입력값 변환

입력값을 검증 전에 변환하고 싶을 때, 많은 프롬프트 함수에서 `transform` 인자가 제공됩니다. 예를 들어 문자열의 공백을 제거할 때 사용할 수 있습니다:

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

여러 프롬프트를 연속해서 입력받고 싶을 때는 `form` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 프롬프트에서 받은 응답을 인덱스 배열로 반환합니다. 각 프롬프트에 `name` 인자를 지정하면 이름별로 응답에 접근할 수 있습니다:

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

`form` 함수의 주요 장점은 사용자가 `CTRL + U`로 이전 프롬프트로 돌아가 잘못된 내용을 수정하거나 선택을 변경할 수 있다는 점입니다. 전체 폼을 취소하고 다시 시작할 필요가 없습니다.

더 세밀한 제어가 필요하다면 `add` 메서드를 사용할 수 있습니다. `add`로 추가된 프롬프트는 이전 응답값을 참조할 수 있습니다:

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
## 정보 메시지

`note`, `info`, `warning`, `error`, `alert` 함수로 다양한 정보 메시지를 출력할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="tables"></a>
## 테이블 출력

`table` 함수는 여러 행과 열의 데이터를 쉽게 보여줄 수 있게 해줍니다. 컬럼명과 데이터만 넘기면 됩니다:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(Spin)

`spin` 함수는 지정한 콜백이 실행되는 동안 작업이 진행 중임을 표시합니다. 실행이 끝나면 콜백의 반환값을 전달합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching response...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]
> `spin` 함수는 애니메이션 효과를 위해 PHP의 `pcntl` 확장이 필요합니다. 이 확장이 없을 경우 정적인 스피너만 표시됩니다.

<a name="progress"></a>
## 진행률 표시줄(Progress Bars)

작업이 오래 걸릴 경우, `progress` 함수를 활용해 작업 진행 상황을 한눈에 보여줄 수 있습니다. 지정한 iterable 만큼 반복되며, 각 반복마다 진행률이 표시됩니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

`progress` 함수는 map과 유사하게 동작하며 각 반복의 반환값을 배열로 반환합니다.

콜백에서 `Laravel\Prompts\Progress` 인스턴스를 받아 매 반복마다 라벨, 힌트 메시지를 동적으로 변경할 수 있습니다:

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

수동 제어가 필요하다면, 전체 반복 횟수를 명시하고 반복마다 `advance` 메서드로 진행률을 업데이트할 수 있습니다:

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

`clear` 함수로 현재 터미널 화면을 비울 수 있습니다:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 사용 시 유의사항

<a name="terminal-width"></a>
#### 터미널 너비

라벨, 옵션, 검증 메시지의 길이가 터미널의 "컬럼 수"를 초과하면 자동으로 줄이집니다. 사용자가 좁은 터미널을 사용할 수 있으므로 가급적 74자 이내로 작성하는 것이 좋습니다(표준 80자 터미널 기준).

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인자를 사용하는 프롬프트는 터미널의 높이에 맞게 자동으로 표시 항목 수가 조절됩니다.

<a name="fallbacks"></a>
## 지원되지 않는 환경 및 폴백

Laravel Prompts는 macOS, Linux, Windows(WSL만 지원)에서 동작합니다. 윈도우용 PHP의 한계로, 현재 WSL 이외의 윈도우 환경에선 사용할 수 없습니다.

이런 이유로, 대체 구현체(예: [Symfony Console Question Helper](https://symfony.com/doc/7.0/components/console/helpers/questionhelper.html))로 자동 폴백하는 기능을 제공합니다.

> [!NOTE]
> Laravel 프레임워크에서 사용하는 경우, 각 프롬프트의 폴백이 이미 적용되어 있어 지원되지 않는 환경에서 자동 활성화됩니다.

<a name="fallback-conditions"></a>
#### 폴백 조건

Laravel을 사용하지 않거나 폴백 조건을 직접 제어하려면 `Prompt` 클래스의 `fallbackWhen` 스태틱 메서드에 boolean 값을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 폴백 동작 커스터마이징

Laravel을 사용하지 않거나, 폴백 동작을 맞춤 설정하려면 각 프롬프트 클래스의 `fallbackUsing` 스태틱 메서드에 클로저를 전달할 수 있습니다:

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

각 프롬프트 클래스에 대해 별도로 폴백을 설정해야 하며, 클로저는 프롬프트 인스턴스를 받아 프롬프트에 맞는 값을 반환해야 합니다.