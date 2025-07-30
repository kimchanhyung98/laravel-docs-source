# 업그레이드 가이드 (Upgrade Guide)

- [8.x에서 9.0으로 업그레이드](#upgrade-9.0)

<a name="high-impact-changes"></a>
## 주요 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [종속성 업데이트](#updating-dependencies)
- [Flysystem 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [Belongs To Many의 `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드](#belongs-to-many-first-or-new)
- [커스텀 캐스트와 `null`](#custom-casts-and-null)
- [기본 HTTP 클라이언트 타임아웃](#http-client-default-timeout)
- [PHP 반환 타입](#php-return-types)
- [Postgres "Schema" 설정](#postgres-schema-configuration)
- [`assertDeleted` 메서드](#the-assert-deleted-method)
- [`lang` 디렉토리](#the-lang-directory)
- [`password` 규칙](#the-password-rule)
- [`when` / `unless` 메서드](#when-and-unless-methods)
- [검증되지 않은 배열 키](#unvalidated-array-keys)

</div>

<a name="upgrade-9.0"></a>
## 8.x에서 9.0으로 업그레이드

<a name="estimated-upgrade-time-30-minutes"></a>
#### 예상 업그레이드 소요 시간: 30분

> [!NOTE]
> 가능한 모든 주요 변경 사항을 문서화하려 노력했습니다. 다만 프레임워크의 잘 알려지지 않은 부분에서만 일부 변경 사항이 실제 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶다면 [Laravel Shift](https://laravelshift.com/)를 이용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 종속성 업데이트

**영향도: 높음**

#### PHP 8.0.2 이상 필요

Laravel은 이제 PHP 8.0.2 이상을 요구합니다.

#### Composer 종속성

애플리케이션 `composer.json` 파일 내 다음 종속성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework` → `^9.0`
- `nunomaduro/collision` → `^6.1`

</div>

또한, `facade/ignition`을 `"spatie/laravel-ignition": "^1.0"`로, 그리고 (해당하는 경우) `pusher/pusher-php-server`는 `"pusher/pusher-php-server": "^5.0"`로 대체하세요.

더불어, 다음과 같은 공식 패키지들이 Laravel 9.x 지원을 위해 주요 버전 업그레이드 되었습니다. 해당된다면 개별 업그레이드 가이드를 참고해 주세요:

<div class="content-list" markdown="1">

- [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Nexmo 대체)

</div>

마지막으로, 애플리케이션에서 사용하는 써드파티 패키지들 역시 Laravel 9 지원용 올바른 버전을 사용하고 있는지 확인해야 합니다.

<a name="php-return-types"></a>
#### PHP 반환 타입

PHP는 `offsetGet`, `offsetSet` 등의 메서드에 반환 타입 정의를 요구하는 방향으로 전환 중이며, Laravel 9에서는 해당 반환 타입이 코드에 반영되었습니다. 보통 사용자 작성 코드에 영향은 없으나, Laravel 코어 클래스를 상속하여 이 메서드들을 오버라이드하는 경우 직접 반환 타입을 추가해야 합니다:

<div class="content-list" markdown="1">

- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`

</div>

또한 PHP의 `SessionHandlerInterface` 구현부 메서드에도 반환 타입이 추가되었습니다. 이 역시 사용자 코드에 영향을 미치지 않을 가능성이 높습니다:

<div class="content-list" markdown="1">

- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`

</div>

<a name="application"></a>
### 애플리케이션

<a name="the-application-contract"></a>
#### `Application` 계약

**영향도: 낮음**

`Illuminate\Contracts\Foundation\Application` 인터페이스의 `storagePath` 메서드가 이제 `$path` 인수를 받을 수 있도록 변경되었습니다. 해당 인터페이스를 구현하고 있다면 구현부를 다음과 같이 수정해야 합니다:

```
public function storagePath($path = '');

```
유사하게, `Illuminate\Foundation\Application` 클래스의 `langPath` 메서드도 `$path` 인수를 받도록 업데이트되었습니다: 

```
public function langPath($path = '');
```

#### 예외 핸들러 `ignore` 메서드

**영향도: 낮음**

예외 핸들러의 `ignore` 메서드가 이제 `protected`에서 `public`으로 변경되었습니다. 기본 애플리케이션 스켈레톤에는 포함되어 있지 않지만, 수동으로 정의한 경우 가시성을 `public`으로 수정하세요:

```php
public function ignore(string $class);
```

#### 예외 핸들러 계약 바인딩

**영향도: 매우 낮음**

이전에는 기본 Laravel 예외 핸들러를 오버라이드할 때 `\App\Exceptions\Handler::class` 타입으로 서비스 컨테이너에 바인딩했지만, 이제는 `\Illuminate\Contracts\Debug\ExceptionHandler::class` 타입으로 바인딩해야 합니다.

### Blade

#### Lazy Collections 및 `$loop` 변수

**영향도: 낮음**

Blade 템플릿 내에서 `LazyCollection` 인스턴스를 순회할 때 `$loop` 변수가 더 이상 제공되지 않습니다. `$loop`에 접근하면 LazyCollection 전체가 메모리에 로드되어, LazyCollection 사용 목적이 무색해지기 때문입니다.

#### `@checked`, `@disabled`, `@selected` Blade 디렉티브

**영향도: 낮음**

새롭게 추가된 Blade 디렉티브 `@checked`, `@disabled`, `@selected`가 Vue 이벤트명과 충돌할 수 있습니다. 이를 피하려면 `@@` 이스케이프를 사용해 디렉티브를 출력할 수 있습니다: `@@selected`.

### 컬렉션 (Collections)

#### `Enumerable` 계약

**영향도: 낮음**

`Illuminate\Support\Enumerable` 계약에 `sole` 메서드가 추가되었습니다. 직접 구현 중이라면 다음 메서드를 포함하도록 업데이트하세요:

```php
public function sole($key = null, $operator = null, $value = null);
```

#### `reduceWithKeys` 메서드

`reduceWithKeys` 메서드가 제거되었습니다. 동일한 기능은 `reduce` 메서드가 제공하므로, `reduceWithKeys` 대신에 `reduce` 호출로 변경하면 됩니다.

#### `reduceMany` 메서드

`reduceMany` 메서드 이름이 `reduceSpread`로 변경되어, 다른 유사한 메서드명과 일관성을 갖도록 했습니다.

### 컨테이너 (Container)

#### `Container` 계약

**영향도: 매우 낮음**

`Illuminate\Contracts\Container\Container` 계약에 `scoped`와 `scopedIf` 두 메서드가 추가되었습니다. 직접 구현 중이면 새 메서드를 반영하세요.

#### `ContextualBindingBuilder` 계약

**영향도: 매우 낮음**

`Illuminate\Contracts\Container\ContextualBindingBuilder` 계약에 `giveConfig` 메서드가 추가되었습니다. 직접 구현 중이라면 다음 메서드를 구현에 포함하세요:

```php
public function giveConfig($key, $default = null);
```

### 데이터베이스

<a name="postgres-schema-configuration"></a>
#### Postgres "Schema" 설정

**영향도: 중간**

`config/database.php` 내 Postgres 연결의 `schema` 설정 옵션 이름이 이제 `search_path`로 변경되어야 합니다.

<a name="schema-builder-doctrine-method"></a>
#### Schema Builder `registerCustomDoctrineType` 메서드

**영향도: 낮음**

`Illuminate\Database\Schema\Builder` 클래스에서 `registerCustomDoctrineType` 메서드가 제거되었습니다. 대신, `DB` 페이스를 통해 `registerDoctrineType` 메서드를 사용하거나 `config/database.php`에서 Doctrine 커스텀 타입을 등록하세요.

### Eloquent

<a name="custom-casts-and-null"></a>
#### 커스텀 캐스트와 `null`

**영향도: 중간**

이전 Laravel 버전에서는 캐스트 속성을 `null`로 설정할 때 커스텀 캐스트 클래스의 `set` 메서드가 호출되지 않았습니다. 이는 공식 문서와 일치하지 않는 동작이었는데, Laravel 9.x부터는 `set` 메서드를 호출하며 `$value`에 `null`이 전달됩니다. 따라서 커스텀 캐스트가 `null`을 적절히 처리하도록 구현을 점검해야 합니다:

```php
/**
 * 저장할 값을 준비합니다.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  AddressModel  $value
 * @param  array  $attributes
 * @return array
 */
public function set($model, $key, $value, $attributes)
{
    if (! $value instanceof AddressModel) {
        throw new InvalidArgumentException('The given value is not an Address instance.');
    }

    return [
        'address_line_one' => $value->lineOne,
        'address_line_two' => $value->lineTwo,
    ];
}
```

<a name="belongs-to-many-first-or-new"></a>
#### Belongs To Many의 `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드

**영향도: 중간**

`belongsToMany` 관계의 `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드는 첫 번째 인수로 배열 형태의 속성을 받습니다. 이전 Laravel 버전에서는 이 배열이 "피벗(pivot)" 테이블의 데이터를 기준으로 비교됐습니다.

하지만 이 동작은 보통 기대하지 않는 것이었고, 이제 이 배열은 관련 모델의 테이블 칼럼과 비교합니다:

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

또한 `firstOrCreate` 메서드가 두 번째 인수로 `$values` 배열을 받도록 변경되어, 기존에 존재하지 않을 때 첫 번째 인수(`$attributes`)와 병합되어 새 모델을 생성하는 데 사용됩니다. 이는 다른 관계 타입의 동일한 메서드와 일관성을 갖도록 한 변경입니다:

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

#### `touch` 메서드

**영향도: 낮음**

`touch` 메서드는 이제 수정할 속성명을 인수로 받을 수 있습니다. 만약 `touch`를 오버라이드했다면 새로운 인수를 반영하도록 시그니처를 다음과 같이 변경하세요:

```php
public function touch($attribute = null);
```

### 암호화 (Encryption)

#### Encrypter 계약

**영향도: 낮음**

`Illuminate\Contracts\Encryption\Encrypter` 계약에 `getKey` 메서드가 추가되었습니다. 직접 구현 중이라면 구현에 포함시키세요:

```php
public function getKey();
```

### 파사드 (Facades)

#### `getFacadeAccessor` 메서드

**영향도: 낮음**

`getFacadeAccessor` 메서드는 항상 컨테이너 바인딩 키를 반환해야 합니다. 이전에는 객체 인스턴스를 반환할 수 있었지만, 이제는 지원하지 않습니다. 직접 파사드를 작성했다면 반드시 문자열을 반환하도록 수정하세요:

```php
/**
 * 컴포넌트에 등록된 이름을 반환합니다.
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

### 파일시스템 (Filesystem)

#### `FILESYSTEM_DRIVER` 환경 변수

**영향도: 낮음**

`FILESYSTEM_DRIVER` 환경 변수 이름이 실제 역할을 좀 더 명확히 하기 위해 `FILESYSTEM_DISK`로 변경되었습니다. 애플리케이션 Skeleton에만 영향이 있으며, 원하는 경우 직접 설정을 바꿔도 무방합니다.

#### Cloud 디스크

**영향도: 낮음**

`cloud` 디스크 설정은 2020년 11월부터 기본 애플리케이션 Skeleton에서 제거되었습니다. 만약 앱 내에서 `cloud` 디스크를 사용 중이라면, 자신의 Skeleton에서는 해당 설정을 유지해야 합니다.

<a name="flysystem-3"></a>
### Flysystem 3.x

**영향도: 높음**

Laravel 9.x는 파일 조작 관련 모든 메서드를 제공하는 `Storage` 페이스가 사용하는 Flysystem 패키지를 1.x 버전에서 3.x 버전으로 업그레이드했습니다. 앱 내에서 일부 변경이 필요할 수 있지만 가능한 원활한 이행을 위해 노력했습니다.

#### 드라이버 전제 조건

S3, FTP, SFTP 드라이버를 사용하려면 Composer 명령어로 관련 패키지를 설치해야 합니다:

- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

#### 기존 파일 덮어쓰기

`put`, `write`, `writeStream` 등의 쓰기 작업은 기본적으로 기존 파일을 덮어씁니다. 덮어쓰기를 원하지 않는 경우, 쓰기 전에 파일 존재 여부를 수동으로 확인해야 합니다.

#### 쓰기 작업 예외 처리

쓰기 작업 실패 시 더 이상 예외를 던지지 않고 `false` 반환합니다. 이전처럼 예외를 원한다면 각 디스크 설정에 `'throw' => true`를 추가하세요:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

#### 없는 파일 읽기

존재하지 않는 파일을 읽으려 하면 이제 `null`이 반환됩니다. 이전 Laravel에서는 `Illuminate\Contracts\Filesystem\FileNotFoundException` 예외가 발생했습니다.

#### 없는 파일 삭제

존재하지 않는 파일을 `delete` 시도하면 `true`가 반환됩니다.

#### 캐시된 어댑터

Flysystem에서 "cached adapters"는 더 이상 지원되지 않아 Laravel에서 제거되었으며, 관련된 디스크 설정(`cache` 키 등)도 제거할 수 있습니다.

#### 커스텀 파일시스템

커스텀 파일시스템 드라이버 등록 방식에 약간 변경이 있습니다. 직접 커스텀 드라이버를 등록하거나 해당 기능을 제공하는 패키지를 사용 중이라면, 코드를 다음과 같이 수정해야 합니다.

Laravel 8.x 예시:

```php
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $client = new DropboxClient(
        $config['authorization_token']
    );

    return new Filesystem(new DropboxAdapter($client));
});
```

Laravel 9.x 예시:

```php
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $adapter = new DropboxAdapter(
        new DropboxClient($config['authorization_token'])
    );

    return new FilesystemAdapter(
        new Filesystem($adapter, $config),
        $adapter,
        $config
    );
});
```

#### SFTP 개인-공개 키 암호

Flysystem의 SFTP 어댑터 및 개인-공개 키 인증을 사용할 때, 개인 키 해독용 `password` 설정 항목 이름이 `passphrase`로 변경되었습니다.

### 헬퍼 (Helpers)

<a name="data-get-function"></a>
#### `data_get` 헬퍼와 이터러블 객체

**영향도: 매우 낮음**

이전에는 `data_get` 헬퍼가 배열과 컬렉션에서 중첩 데이터를 조회할 수 있었으나, 이제는 모든 이터러블 객체에서도 중첩 데이터 조회가 가능합니다.

<a name="str-function"></a>
#### `str` 헬퍼

**영향도: 매우 낮음**

Laravel 9.x는 전역 `str` 헬퍼 함수를 포함합니다. 애플리케이션에서 동일 이름의 전역 헬퍼가 있다면 이름을 변경하거나 제거해야 충돌을 방지할 수 있습니다.

<a name="when-and-unless-methods"></a>
#### `when` / `unless` 메서드

**영향도: 중간**

Laravel 프레임워크 여러 클래스가 제공하는 `when` 와 `unless` 메서드는 첫 번째 인수의 불리언 판정에 따라 조건부 동작을 수행합니다:

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

이전에는 `when` 또는 `unless` 메서드에 클로저를 전달하면 클로저 객체가 항상 참으로 평가되어 조건부 작업이 무조건 실행됐습니다. 따라서 의도와 다르게 동작하는 경우가 있었습니다.

Laravel 9.x부터는 전달된 클로저를 실행하여 반환값을 이용해 불리언 판정을 합니다:

```php
$collection->when(function ($collection) {
    // 이 클로저가 실행됩니다...
    return false;
}, function ($collection) {
    // 첫 클로저가 "false" 반환하므로 이 부분은 실행되지 않습니다...
    $collection->merge([1, 2, 3]);
});
```

### HTTP 클라이언트

<a name="http-client-default-timeout"></a>
#### 기본 타임아웃

**영향도: 중간**

[HTTP 클라이언트](/docs/9.x/http-client)는 기본 타임아웃이 30초로 설정되었습니다. 즉, 서버가 30초 내 응답하지 않으면 예외가 발생합니다. 이전에는 타임아웃이 없거나 무한대여서 요청이 무한히 대기되는 경우가 있었습니다.

요청마다 타임아웃 값을 조정하고 싶으면 `timeout` 메서드를 사용하세요:

```
$response = Http::timeout(120)->get(/* ... */);
```

#### HTTP Fake & 미들웨어

**영향도: 낮음**

과거에는 HTTP 클라이언트가 "가짜(faked)" 상태일 때, Guzzle HTTP 미들웨어가 실행되지 않았으나, Laravel 9.x부터는 faked 상태에서도 해당 미들웨어가 실행됩니다.

#### HTTP Fake & 의존성 주입

**영향도: 낮음**

이전에는 `Http::fake()` 호출이 클래스 생성자에 의존성 주입된 `Illuminate\Http\Client\Factory` 인스턴스에 영향을 주지 않았으나, Laravel 9.x에서는 주입된 HTTP 클라이언트에도 faked 응답이 반환되어 다른 페이스들과 일관성 있습니다.

<a name="symfony-mailer"></a>
### Symfony Mailer

**영향도: 높음**

Laravel 9.x의 가장 큰 변화 중 하나는 2021년 12월 이후 유지보수가 중단된 SwiftMailer에서 Symfony Mailer로의 교체입니다. 이 전환은 가능하면 무리 없이 진행할 수 있도록 했으나, 애플리케이션 호환성을 위해 아래 변경 사항 확인이 필요합니다.

#### 드라이버 전제 조건

Mailgun 전송 방식을 계속 사용할 경우, `symfony/mailgun-mailer` 및 `symfony/http-client` Composer 패키지를 설치해야 합니다:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

`wildbit/swiftmailer-postmark` 패키지는 제거해야 하고, 대신 `symfony/postmark-mailer` 및 `symfony/http-client` 패키지를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

#### 반환 타입 변경

`Illuminate\Mail\Mailer` 클래스의 `send`, `html`, `raw`, `plain` 메서드는 더 이상 `void`를 반환하지 않고, `Illuminate\Mail\SentMessage` 인스턴스를 반환합니다. 이 객체는 내부에 `Symfony\Component\Mailer\SentMessage` 인스턴스를 갖고 있으며 `getSymfonySentMessage` 메서드나 동적 호출로 접근할 수 있습니다.

#### "Swift" 메서드명 변경

SwiftMailer 관련 메서드명(일부 문서화 안 된 것 포함)이 대응하는 Symfony Mailer 메서드명으로 변경되었습니다. 예를 들어 `withSwiftMessage`가 `withSymfonyMessage`로 변경되었습니다:

```
// Laravel 8.x...
$this->withSwiftMessage(function ($message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});

// Laravel 9.x...
use Symfony\Component\Mime\Email;

$this->withSymfonyMessage(function (Email $message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});
```

> [!WARNING]
> `Symfony\Component\Mime\Email` 객체와 관련된 모든 조작에 대해서는 [Symfony Mailer 문서](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages)를 반드시 꼼꼼히 검토하세요.

아래는 주요 메서드명 변경 목록입니다. 대부분 SwiftMailer/Symfony Mailer 내부 동작용 저수준 메서드로 일반 Laravel 애플리케이션에서는 자주 사용하지 않을 수 있습니다:

```
Message::getSwiftMessage();
Message::getSymfonyMessage();

Mailable::withSwiftMessage($callback);
Mailable::withSymfonyMessage($callback);

MailMessage::withSwiftMessage($callback);
MailMessage::withSymfonyMessage($callback);

Mailer::getSwiftMailer();
Mailer::getSymfonyTransport();

Mailer::setSwiftMailer($swift);
Mailer::setSymfonyTransport(TransportInterface $transport);

MailManager::createTransport($config);
MailManager::createSymfonyTransport($config);
```

#### `Illuminate\Mail\Message` 프록시 메서드 변경

`Illuminate\Mail\Message`는 기존에 누락된 메서드를 내부 `Swift_Message` 인스턴스로 프록시했습니다. 이제부터는 누락된 메서드가 `Symfony\Component\Mime\Email` 인스턴스로 프록시됩니다. 따라서, 이전 코드가 SwiftMailer 메서드 호출에 의존했다면 대응하는 Symfony Mailer 메서드로 업데이트해야 합니다.

예:

```
// Laravel 8.x...
$message
    ->setFrom('taylor@laravel.com')
    ->setTo('example@example.org')
    ->setSubject('Order Shipped')
    ->setBody('<h1>HTML</h1>', 'text/html')
    ->addPart('Plain Text', 'text/plain');

// Laravel 9.x...
$message
    ->from('taylor@laravel.com')
    ->to('example@example.org')
    ->subject('Order Shipped')
    ->html('<h1>HTML</h1>')
    ->text('Plain Text');
```

#### 생성되는 메시지 ID

SwiftMailer는 `mime.idgenerator.idright` 설정으로 메시지 ID를 생성할 때 사용되는 도메인을 지정할 수 있었지만, Symfony Mailer는 이를 지원하지 않고 발신자 정보를 바탕으로 메시지 ID를 자동 생성합니다.

#### `MessageSent` 이벤트 변경

`Illuminate\Mail\Events\MessageSent` 이벤트의 `message` 속성은 이제 `Swift_Message`가 아닌 `Symfony\Component\Mime\Email` 인스턴스를 포함하며, 이는 메일 전송 전 상태를 의미합니다.

새로 추가된 `sent` 속성은 `Illuminate\Mail\SentMessage` 인스턴스를 담고 있으며, 메시지 ID 등 전송 관련 정보를 제공합니다.

#### 강제 재연결 불가

운영 데몬 프로세스 등에서 메일러 재연결을 강제로 수행할 수 없고, Symfony Mailer가 자동으로 재연결을 시도하고 실패 시 예외를 던집니다.

#### SMTP 스트림 옵션

SMTP 전송 옵션에 대한 스트림 옵션 정의가 더 이상 지원되지 않습니다. 대신 지원하는 옵션은 구성 파일에 직접 명확히 정의해야 합니다. 예를 들어 TLS peer 검증 비활성화는 다음과 같습니다:

```
'smtp' => [
    // Laravel 8.x...
    'stream' => [
        'ssl' => [
            'verify_peer' => false,
        ],
    ],

    // Laravel 9.x...
    'verify_peer' => false,
],
```

자세한 설정 옵션은 [Symfony Mailer 문서](https://symfony.com/doc/6.0/mailer.html#transport-setup)를 참고하세요.

> [!WARNING]
> 위 예시처럼 SSL 인증 무효화는 중간자 공격 등의 위험을 초래하므로 일반적으로 권장되지 않습니다.

#### SMTP `auth_mode`

SMTP 인증 방식 `auth_mode` 설정을 `mail` 설정 파일에 명시할 필요가 없으며, Symfony Mailer와 SMTP 서버가 자동 협상합니다.

#### 실패한 수신자

메일 발송 실패 수신자 목록을 가져오는 기능은 제거되었습니다. 실패 시 `Symfony\Component\Mailer\Exception\TransportExceptionInterface` 예외가 발생합니다. 메일 발송 전에 이메일 주소를 검증하는 방식을 권장합니다.

### 패키지

<a name="the-lang-directory"></a>
#### `lang` 디렉토리

**영향도: 중간**

새 Laravel 애플리케이션은 `resources/lang`가 아닌 루트 프로젝트 디렉토리의 `lang` 폴더를 사용합니다. 패키지를 제작 중이며 언어 파일을 퍼블리시할 경우, 하드코딩된 경로 대신 `app()->langPath()`를 사용하도록 패키지를 업데이트해야 합니다.

<a name="queue"></a>
### 큐

<a name="the-opis-closure-library"></a>
#### `opis/closure` 라이브러리

**영향도: 낮음**

Laravel이 기존에 의존한 `opis/closure`가 `laravel/serializable-closure`로 대체되었습니다. 직접 `opis/closure`를 사용하거나, 이전에 deprecated 된 `Illuminate\Queue\SerializableClosureFactory`, `Illuminate\Queue\SerializableClosure` 클래스를 사용하는 경우, [Laravel Serializable Closure](https://github.com/laravel/serializable-closure)로 전환할 수 있습니다.

#### 실패한 작업 제공자의 `flush` 메서드

**영향도: 낮음**

`Illuminate\Queue\Failed\FailedJobProviderInterface`의 `flush` 메서드가 `$hours` 인수를 받도록 변경되었습니다. 수동 구현 시 다음 시그니처로 업데이트하세요:

```php
public function flush($hours = null);
```

### 세션

#### `getSession` 메서드

**영향도: 낮음**

Laravel의 `Illuminate\Http\Request` 클래스가 확장하는 Symfony의 `Symfony\Component\HttpFoundation\Request` 클래스의 `getSession` 메서드는 이제 정확한 반환 타입(`Symfony\Component\HttpFoundation\Session\SessionInterface` 구현체)을 갖거나, 세션이 없으면 `SessionNotFoundException` 예외를 던집니다. 기존에는 `Illuminate\Session\Store` 인스턴스를 반환하거나 `null`이었으나 변경됐으니 참고하세요.

### 테스트

<a name="the-assert-deleted-method"></a>
#### `assertDeleted` 메서드

**영향도: 중간**

`assertDeleted` 메서드 호출은 모두 `assertModelMissing`로 변경해야 합니다.

### 신뢰된 프록시 (Trusted Proxies)

**영향도: 낮음**

Laravel 8에서 Laravel 9로 새 애플리케이션 Skeleton에 기존 코드를 이식하는 경우, `app/Http/Middleware/TrustProxies.php` 내에 다음을 수정해야 합니다.

먼저,

```php
use Fideloper\Proxy\TrustProxies as Middleware;
```

를

```php
use Illuminate\Http\Middleware\TrustProxies as Middleware;
```

로 변경하고, `$headers` 프로퍼티도 다음과 같이 업데이트하세요:

```php
// 이전...
protected $headers = Request::HEADER_X_FORWARDED_ALL;

// 이후...
protected $headers =
    Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB;
```

마지막으로, `fideloper/proxy` Composer 의존성을 제거할 수 있습니다:

```shell
composer remove fideloper/proxy
```

### 검증 (Validation)

#### Form Request의 `validated` 메서드

**영향도: 낮음**

폼 요청의 `validated` 메서드가 `$key`와 `$default` 인수를 받을 수 있도록 변경되었습니다. 직접 오버라이드 중이라면 시그니처를 다음과 같이 업데이트하세요:

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
#### `password` 규칙

**영향도: 중간**

사용자 입력값이 인증된 사용자의 현재 비밀번호와 일치하는지 검증하는 `password` 규칙 이름이 `current_password`로 변경되었습니다.

<a name="unvalidated-array-keys"></a>
#### 검증되지 않은 배열 키

**영향도: 중간**

이전 Laravel 버전에서는 배열 규칙과 함께 유효성 검사하지 않은 키를 "validated" 데이터에서 제외하려면 별도의 지시가 필요했습니다. Laravel 9.x부터는 `array` 규칙이 허용 키를 명시하지 않아도 검증되지 않은 키는 항상 제외됩니다. 이는 보통 기대하는 동작입니다.

기존 8.x 방식처럼 이 동작을 사용하려면, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 다음 코드를 호출하세요:

```php
use Illuminate\Support\Facades\Validator;

/**
 * 애플리케이션 서비스를 등록합니다.
 *
 * @return void
 */
public function boot()
{
    Validator::includeUnvalidatedArrayKeys();
}
```

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel) 내의 변경사항도 확인하는 것을 권장합니다. 많은 변경이 필수는 아니지만, 구성 파일이나 주석 등 여러 업데이트를 애플리케이션과 맞춰 관리할 수 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/8.x...9.x)를 활용해 중요한 변경만 선택 적용할 수 있습니다.