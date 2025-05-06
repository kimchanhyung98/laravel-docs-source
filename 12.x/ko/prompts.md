# 프롬프트(Prompts)

- [소개](#introduction)
- [설치](#installation)
- [사용 가능한 프롬프트](#available-prompts)
    - [텍스트](#text)
    - [텍스트영역](#textarea)
    - [비밀번호](#password)
    - [확인](#confirm)
    - [선택](#select)
    - [다중 선택](#multiselect)
    - [자동완성 제안](#suggest)
    - [검색](#search)
    - [다중 검색](#multisearch)
    - [일시정지](#pause)
- [검증 전 입력값 변환하기](#transforming-input-before-validation)
- [폼](#forms)
- [정보 메시지](#informational-messages)
- [테이블](#tables)
- [스핀(로딩)](#spin)
- [진행률 바(Progress Bar)](#progress)
- [터미널 초기화](#clear)
- [터미널 환경 고려사항](#terminal-considerations)
- [미지원 환경 및 대체 처리](#fallbacks)

<a name="introduction"></a>
## 소개

[Laravel Prompts](https://github.com/laravel/prompts)는 브라우저와 유사한 플레이스홀더, 검증 등의 기능을 포함하여 명령행 애플리케이션에 아름답고 사용하기 쉬운 폼을 추가할 수 있는 PHP 패키지입니다.

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel Prompts는 [Artisan 콘솔 명령어](/docs/{{version}}/artisan#writing-commands)에서 사용자 입력을 받을 때 특히 유용하며, 모든 커맨드라인 PHP 프로젝트에서도 사용할 수 있습니다.

> [!NOTE]
> Laravel Prompts는 macOS, Linux, Windows(WSL)에서 지원됩니다. 자세한 내용은 [미지원 환경 및 대체 처리](#fallbacks) 문서를 참고하세요.

<a name="installation"></a>
## 설치

Laravel Prompts는 최신 버전의 Laravel에 기본 포함되어 있습니다.

또한, 다른 PHP 프로젝트에서는 Composer 패키지 매니저를 이용해 설치할 수 있습니다:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## 사용 가능한 프롬프트

<a name="text"></a>
### 텍스트

`text` 함수는 지정한 질문을 사용자에게 보여주고, 입력값을 받아 반환합니다:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

플레이스홀더, 기본값, 안내 힌트도 추가할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    placeholder: '예: Taylor Otwell',
    default: $user?->name,
    hint: '이 이름은 프로필에 표시됩니다.'
);
```

<a name="text-required"></a>
#### 필수 값 지정

입력이 필수라면 `required` 인자를 사용할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

검증 메시지를 커스텀하려면 문자열로 지정할 수도 있습니다:

```php
$name = text(
    label: 'What is your name?',
    required: '이름은 필수 입력 항목입니다.'
);
```

<a name="text-validation"></a>
#### 추가 검증

추가 검증이 필요하다면, `validate` 인자에 클로저를 전달할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => '이름은 최소 3자 이상 입력해야 합니다.',
        strlen($value) > 255 => '이름은 255자 이하로 입력해야 합니다.',
        default => null
    }
);
```

해당 클로저에는 입력값이 전달되며, 에러 메시지나 `null`(검증 통과 시)을 반환할 수 있습니다.

또는 Laravel의 [유효성 검사기](/docs/{{version}}/validation)의 힘을 활용할 수도 있습니다. 이 경우, 속성명과 검증 규칙 배열을 `validate` 인자에 전달하세요:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### 텍스트영역

`textarea` 함수는 질문을 보여주고, 여러 줄의 입력을 받아 반환합니다:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

플레이스홀더, 기본값, 힌트도 추가할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: '이야기의 시작...',
    hint: '이 내용은 프로필에 공개됩니다.'
);
```

<a name="textarea-required"></a>
#### 필수 값 지정

입력이 꼭 필요하다면 `required` 인자를 지정하세요:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

검증 메시지를 커스텀하려면 문자열로 지정할 수도 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: '이야기를 입력해야 합니다.'
);
```

<a name="textarea-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 클로저를 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: fn (string $value) => match (true) {
        strlen($value) < 250 => '이야기는 최소 250자 이상이어야 합니다.',
        strlen($value) > 10000 => '이야기는 10,000자를 넘을 수 없습니다.',
        default => null
    }
);
```

Laravel의 [유효성 검사기](/docs/{{version}}/validation)도 사용할 수 있습니다:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="password"></a>
### 비밀번호

`password` 함수는 `text` 함수와 유사하나, 콘솔에 입력값이 마스킹되어 표시됩니다. 비밀번호 등 민감한 정보를 물어볼 때 유용합니다:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

플레이스홀더, 힌트 추가도 가능합니다:

```php
$password = password(
    label: 'What is your password?',
    placeholder: '비밀번호',
    hint: '최소 8자 이상 입력'
);
```

<a name="password-required"></a>
#### 필수 값 지정

입력이 필수라면 `required` 인자를 지정하세요:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

검증 메시지 커스텀도 문자열로 할 수 있습니다:

```php
$password = password(
    label: 'What is your password?',
    required: '비밀번호를 입력해야 합니다.'
);
```

<a name="password-validation"></a>
#### 추가 검증

추가 검증도 가능합니다:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => '비밀번호는 8자 이상이어야 합니다.',
        default => null
    }
);
```

Laravel의 [유효성 검사기](/docs/{{version}}/validation)를 사용할 수도 있습니다:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### 확인

사용자에게 예/아니오(yes/no) 확인을 요청하려면 `confirm` 함수를 사용하세요. 사용자는 방향키 또는 `y`, `n` 키로 답변을 선택할 수 있습니다. 이 함수는 `true` 또는 `false`를 반환합니다.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

기본 선택, "예"/"아니오" 레이블, 힌트도 사용자화할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: '동의함',
    no: '거부함',
    hint: '계속하려면 약관 동의가 필요합니다.'
);
```

<a name="confirm-required"></a>
#### "예" 필수 선택

"예"를 반드시 선택하게 하려면 `required` 인자를 지정하세요:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

검증 메시지 문자열도 지정할 수 있습니다:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: '약관에 동의해야 계속 진행할 수 있습니다.'
);
```

<a name="select"></a>
### 선택

미리 정의한 목록에서 하나를 선택하도록 하려면 `select` 함수를 사용하세요:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

기본 선택, 힌트도 추가 가능합니다:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: '역할은 언제든 변경할 수 있습니다.'
);
```

`options`에 연관 배열을 넘기면, 값 대신 선택된 키가 반환됩니다:

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

설정한 옵션이 5개를 넘으면 스크롤이 활성화됩니다. `scroll`로 표시 개수를 조절 가능합니다:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-validation"></a>
#### 추가 검증

`select` 함수는 아무것도 선택하지 않는 상황이 없으므로 `required` 인자를 지원하지 않습니다. 하지만 특정 값을 고를 수 없게 해야 한다면 `validate`에 클로저를 전달할 수 있습니다:

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
            ? '이미 오너 권한의 사용자가 있습니다.'
            : null
);
```

`options`가 연관 배열이면 클로저는 선택된 키를, 순차 배열이면 선택된 값을 받습니다.

<a name="multiselect"></a>
### 다중 선택

여러 개의 항목을 선택하게 하려면 `multiselect` 함수를 사용하세요:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

기본 선택 및 힌트도 지정할 수 있습니다:

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: '권한은 언제든 변경할 수 있습니다.'
);
```

`options`에 연관 배열을 넘기면, 선택된 옵션의 키들이 반환됩니다:

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

표시되는 옵션이 5개를 넘을 경우 `scroll`로 개수 설정이 가능합니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-required"></a>
#### 값 필수 지정

기본적으로 사용자는 0개 이상을 선택할 수 있습니다. 한 개 이상의 선택을 강제하려면 `required` 인자를 지정하세요:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

검증 메시지도 지정할 수 있습니다:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: '최소 한 개 이상의 카테고리를 선택해야 합니다'
);
```

<a name="multiselect-validation"></a>
#### 추가 검증

특정 값을 선택하지 못하게 하려면 `validate`에 클로저를 전달할 수 있습니다:

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
        ? '모든 사용자는 읽기 권한이 필요합니다.'
        : null
);
```

<a name="suggest"></a>
### 자동완성 제안

`suggest` 함수는 자동완성 후보를 제시할 수 있습니다. 후보와 관계없이 사용자는 임의의 값을 입력할 수 있습니다:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인자로 클로저를 넘겨 사용자가 입력할 때마다 후보를 동적으로 반환할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

플레이스홀더, 기본값, 힌트도 추가할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: '예: Taylor',
    default: $user?->name,
    hint: '이 이름은 프로필에 표시됩니다.'
);
```

<a name="suggest-required"></a>
#### 필수 값 지정

입력이 반드시 필요하다면 `required` 인자를 지정하세요:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

검증 메시지도 문자열로 지정할 수 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: '이름은 필수 입력 항목입니다.'
);
```

<a name="suggest-validation"></a>
#### 추가 검증

추가 검증도 가능합니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => '이름은 최소 3자 이상 입력해야 합니다.',
        strlen($value) > 255 => '이름은 255자 이하로 입력해야 합니다.',
        default => null
    }
);
```

또는 Laravel의 [유효성 검사기](/docs/{{version}}/validation)를 사용할 수도 있습니다:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### 검색

옵션이 아주 많을 때, `search` 함수로 사용자가 검색어를 입력해 목록을 필터링하고 방향키로 선택할 수 있습니다:

```php
use function Laravel\Prompts\search;

$id = search(
    label: '메일 수신자를 검색',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

연관 배열을 반환하면 선택된 키가, 순차 배열이면 값이 반환됩니다.

값 배열을 필터링할 때는 배열이 연관 배열이 아닌지 `array_values`나 `values` 메서드를 써 주세요:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: '메일 수신자를 검색',
    options: fn ($value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

플레이스홀더, 힌트도 추가할 수 있습니다:

```php
$id = search(
    label: '메일 수신자를 검색',
    placeholder: '예: Taylor Otwell',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: '해당 사용자에게 즉시 메일이 발송됩니다.'
);
```

5개가 넘는 옵션은 스크롤 상태로 표시되며, `scroll` 인자로 조절 가능합니다:

```php
$id = search(
    label: '메일 수신자를 검색',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-validation"></a>
#### 추가 검증

추가 검증을 하고 싶으면 `validate`에 클로저를 넘기세요:

```php
$id = search(
    label: '메일 수신자를 검색',
    options: fn ($value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return '이 사용자는 메일 수신을 거부했습니다.';
        }
    }
);
```

<a name="multisearch"></a>
### 다중 검색

여러 항목을 검색하고 선택할 수 있게 하려면 `multisearch`를 사용하세요:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    '메일을 받을 사용자 검색',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

여러 개의 항목을 선택할 수 있습니다. 값 배열을 사용하는 경우 `array_values`나 `values`를 꼭 사용하세요.

플레이스홀더, 힌트 추가, 스크롤 개수 조정도 위의 예시와 동일하게 가능합니다.

<a name="multisearch-required"></a>
#### 값 필수 지정

선택이 필수라면 `required` 인자를 추가하세요:

```php
$ids = multisearch(
    label: '메일을 받을 사용자 검색',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

검증 메시지도 문자열로 지정할 수 있습니다:

```php
$ids = multisearch(
    label: '메일을 받을 사용자 검색',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: '최소 한 명의 사용자를 선택해야 합니다.'
);
```

<a name="multisearch-validation"></a>
#### 추가 검증

추가 검증이 필요하다면 클로저를 전달하세요:

```php
$ids = multisearch(
    label: '메일을 받을 사용자 검색',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::whereLike('name', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', 그리고 ').' 님은 메일 수신을 거부했습니다.';
        }
    }
);
```

<a name="pause"></a>
### 일시정지

`pause` 함수는 안내 문구를 표시하고 사용자가 Enter(리턴)를 누를 때까지 대기합니다:

```php
use function Laravel\Prompts\pause;

pause('계속하려면 ENTER를 누르세요.');
```

<a name="transforming-input-before-validation"></a>
## 검증 전 입력값 변환하기

입력값을 검증 전에 변환해야 할 때, 여러 프롬프트 함수의 `transform` 인자에 클로저를 넘겨 사용할 수 있습니다. 예를 들어 공백을 제거할 수 있습니다:

```php
$name = text(
    label: 'What is your name?',
    transform: fn (string $value) => trim($value),
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => '이름은 최소 3자 이상 입력해야 합니다.',
        strlen($value) > 255 => '이름은 255자 이하로 입력해야 합니다.',
        default => null
    }
);
```

<a name="forms"></a>
## 폼

여러 개의 프롬프트를 연속적으로 표시해 추가 정보를 수집할 때는 `form` 함수를 사용할 수 있습니다:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

`submit` 메서드는 프롬프트의 응답을 번호 순서의 배열로 반환합니다. 각 프롬프트별로 `name` 인자를 주면 이름으로도 결과에 접근할 수 있습니다:

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

`form` 함수의 가장 큰 장점은 사용자가 `CTRL + U`로 이전 프롬프트 단계로 돌아갈 수 있다는 것입니다. 실수를 수정하거나 선택을 변경할 때, 폼을 전체 취소하고 다시 시작하지 않아도 됩니다.

더 세밀하게 프롬프트를 제어해야 한다면, 직접 프롬프트 함수를 호출하기보다 `add` 메서드를 사용할 수 있습니다. 이때 모든 이전 응답값이 인자로 전달됩니다:

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

outro("이름: {$responses['name']}, 나이: {$responses['age']}세");
```

<a name="informational-messages"></a>
## 정보 메시지

`note`, `info`, `warning`, `error`, `alert` 함수를 통해 다양한 정보 메시지를 표시할 수 있습니다:

```php
use function Laravel\Prompts\info;

info('패키지가 성공적으로 설치되었습니다.');
```

<a name="tables"></a>
## 테이블

`table` 함수는 여러 행과 열의 데이터를 쉽게 표시합니다. 열 이름과 행 데이터를 넘기세요:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## 스핀(로딩)

`spin` 함수는 지정된 콜백이 실행되는 동안 스피너(로딩 표시)와 메시지를 보여주며, 완료되면 콜백의 결과를 반환합니다:

```php
use function Laravel\Prompts\spin;

$response = spin(
    message: '응답을 가져오는 중...',
    callback: fn () => Http::get('http://example.com')
);
```

> [!WARNING]
> `spin` 함수는 스피너 애니메이션을 위해 PHP `pcntl` 확장 모듈이 필요합니다. 확장이 없으면 정적인 스피너가 표시됩니다.

<a name="progress"></a>
## 진행률 바(Progress Bar)

소요 시간이 긴 작업에서는 진행률 바를 통해 얼마나 남았는지 사용자에게 보여줄 수 있습니다. `progress` 함수는 하나의 반복(iterable) 값에 대해 각각 표기를 하며, 결과도 배열로 반환합니다:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: '사용자 업데이트 중',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

콜백은 `Laravel\Prompts\Progress` 인스턴스를 받아 각 반복마다 라벨 및 힌트를 수정할 수 있습니다:

```php
$users = progress(
    label: '사용자 업데이트 중',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("{$user->name} 업데이트 중")
            ->hint("생성 일자: {$user->created_at}");

        return $this->performTask($user);
    },
    hint: '다소 시간이 걸릴 수 있습니다.'
);
```

진행률 바를 직접 제어하고 싶으면 step 개수를 미리 정하고, 항목마다 `advance` 메서드를 사용하면 됩니다:

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

<a name="clear"></a>
## 터미널 초기화

터미널 화면을 초기화하려면 `clear` 함수를 사용하세요:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## 터미널 환경 고려사항

<a name="terminal-width"></a>
#### 터미널 너비

라벨, 옵션, 검증 메시지의 길이가 터미널의 "열(col)"보다 길면 자동으로 잘립니다. 사용자 터미널이 좁을 수 있으니 74자 이내로 작성하는 것을 권장합니다(80자 너비 기준).

<a name="terminal-height"></a>
#### 터미널 높이

`scroll` 인자를 사용하는 경우, 터미널 높이에 맞게 자동으로 값이 조정되어 검증 메시지 표시 공간도 확보됩니다.

<a name="fallbacks"></a>
## 미지원 환경 및 대체 처리

Laravel Prompts는 macOS, Linux, Windows(WSL)에서만 사용 가능하며, PHP for Windows 환경에서는 현재 사용할 수 없습니다.

이에 따라, [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)와 같은 대체 구현으로 자동 전환될 수 있습니다.

> [!NOTE]
> Laravel 프레임워크와 함께 사용할 경우, 각 프롬프트의 대체 구현이 이미 설정되어 있어 미지원 환경에서 자동 활성화됩니다.

<a name="fallback-conditions"></a>
#### 대체 처리 조건

Laravel이 아닌 환경이거나, 대체 처리 사용 조건을 커스터마이징하려면 `Prompt` 클래스의 `fallbackWhen` 정적 메서드에 불리언 값을 전달하세요:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### 대체 처리 방법

또는 사용하려는 프롬프트 클래스 별로 `fallbackUsing` 정적 메서드에 클로저를 전달해 대체 동작을 정의할 수 있습니다:

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(
                    is_string($prompt->required) ? $prompt->required : '필수 입력 항목입니다.'
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

대체 동작은 각 프롬프트 클래스별로 개별적으로 설정되어야 합니다. 클로저에는 해당 프롬프트 인스턴스가 전달되며, 알맞은 타입을 반환해야 합니다.