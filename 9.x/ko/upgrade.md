# 업그레이드 가이드

- [8.x에서 9.0으로 업그레이드](#upgrade-9.0)

<a name="high-impact-changes"></a>
## 주요 변경점

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Flysystem 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경점

<div class="content-list" markdown="1">

- [Belongs To Many의 `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드](#belongs-to-many-first-or-new)
- [커스텀 캐스트 & `null`](#custom-casts-and-null)
- [기본 HTTP 클라이언트 타임아웃](#http-client-default-timeout)
- [PHP 반환 타입](#php-return-types)
- [Postgres "Schema" 설정](#postgres-schema-configuration)
- [`assertDeleted` 메서드](#the-assert-deleted-method)
- [`lang` 디렉터리](#the-lang-directory)
- [`password` 규칙](#the-password-rule)
- [`when` / `unless` 메서드](#when-and-unless-methods)
- [검증되지 않은 배열 키](#unvalidated-array-keys)

</div>

<a name="upgrade-9.0"></a>
## 8.x에서 9.0으로 업그레이드

<a name="estimated-upgrade-time-30-minutes"></a>
#### 예상 소요 시간: 30분

> **참고**  
> 가능한 모든 하위 호환성 이슈를 문서화하려 노력했습니다. 하지만 이들 중 일부는 프레임워크의 잘 알려지지 않은 부분에 해당하므로 실제로 여러분의 애플리케이션에 영향을 미치는 변경점은 일부일 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하면 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향도: 높음**

#### PHP 8.0.2 필요

Laravel은 이제 PHP 8.0.2 이상이 필요합니다.

#### Composer 의존성

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^9.0`으로
- `nunomaduro/collision`을 `^6.1`로

</div>

또한, `facade/ignition`을 `"spatie/laravel-ignition": "^1.0"`으로, `pusher/pusher-php-server`(사용 중인 경우)를 `"pusher/pusher-php-server": "^5.0"`으로 교체해야 합니다.

아울러, 다음 1st-party 패키지는 Laravel 9.x 지원을 위해 새로운 메이저 릴리스를 배포했습니다. 해당되는 경우, 업그레이드 전에 각각의 업그레이드 가이드를 꼭 참고하세요.

<div class="content-list" markdown="1">

- [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Nexmo를 대체)

</div>

마지막으로, 애플리케이션에서 사용하는 모든 써드파티 패키지를 확인하여 Laravel 9을 지원하는 버전을 사용하는지 확인하세요.

<a name="php-return-types"></a>
#### PHP 반환 타입

PHP는 이제 `offsetGet`, `offsetSet` 등과 같은 메서드에 반환 타입 정의를 요구하는 쪽으로 전환하고 있습니다. 이에 따라, Laravel 9에서는 이러한 반환 타입이 코드베이스에 적용되었습니다. 대부분 사용자 작성 코드는 영향을 받지 않지만, 만약 Laravel의 코어 클래스를 확장하면서 이러한 메서드를 오버라이드했다면, 본인 코드에도 반환 타입을 추가해야 합니다.

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

또한, PHP의 `SessionHandlerInterface`를 구현하는 메서드에도 반환 타입이 추가되었습니다. 이 변경점이 애플리케이션에 영향을 줄 가능성은 낮습니다:

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
#### `Application` 인터페이스

**영향도: 낮음**

`Illuminate\Contracts\Foundation\Application` 인터페이스의 `storagePath` 메서드는 `$path` 인자를 받도록 업데이트되었습니다. 이 인터페이스를 직접 구현하고 있다면 구현체도 맞추어 수정해야 합니다.

    public function storagePath($path = '');

마찬가지로, `Illuminate\Foundation\Application` 클래스의 `langPath` 메서드도 `$path` 인자를 받도록 변경되었습니다.

    public function langPath($path = '');

#### 예외 핸들러의 `ignore` 메서드

**영향도: 낮음**

예외 핸들러의 `ignore` 메서드는 이제 `protected`가 아닌 `public`이어야 합니다. 이 메서드는 기본 애플리케이션 스켈레톤에는 없습니다. 만약 직접 정의했다면 접근 제한자를 `public`으로 변경해야 합니다:

```php
public function ignore(string $class);
```

#### 예외 핸들러 인터페이스 바인딩

**영향도: 매우 낮음**

이전에는 기본 Laravel 예외 핸들러를 오버라이드하려면 `\App\Exceptions\Handler::class` 타입을 사용해 서비스 컨테이너에 바인딩했지만, 이제는 `\Illuminate\Contracts\Debug\ExceptionHandler::class` 타입을 사용해야 합니다.

### Blade

#### Lazy Collections & `$loop` 변수

**영향도: 낮음**

Blade 템플릿에서 `LazyCollection` 인스턴스를 순회할 때, `$loop` 변수를 더 이상 사용할 수 없습니다. 이 변수를 참조하면 전체 `LazyCollection`을 메모리에 로드하므로, lazy 컬렉션의 장점이 사라지기 때문입니다.

#### Checked / Disabled / Selected Blade 지시어

**영향도: 낮음**

새로운 `@checked`, `@disabled`, `@selected` Blade 지시어는 같은 이름의 Vue 이벤트와 충돌할 수 있습니다. 이 충돌을 피하려면 `@@`를 사용해 지시어를 이스케이프할 수 있습니다(`@@selected` 등).

### 컬렉션

#### `Enumerable` 인터페이스

**영향도: 낮음**

`Illuminate\Support\Enumerable` 인터페이스에 `sole` 메서드가 새로 정의되었습니다. 이 인터페이스를 직접 구현하고 있다면, 해당 메서드를 구현해야 합니다:

```php
public function sole($key = null, $operator = null, $value = null);
```

#### `reduceWithKeys` 메서드

`reduceWithKeys` 메서드는 삭제되었습니다. 동일한 기능을 `reduce`에서 제공하므로, 코드를 `reduce`로 변경하면 됩니다.

#### `reduceMany` 메서드

`reduceMany` 메서드는 네이밍 일관성을 위해 `reduceSpread`로 이름이 변경되었습니다.

### 컨테이너

#### `Container` 인터페이스

**영향도: 매우 낮음**

`Illuminate\Contracts\Container\Container` 인터페이스에 `scoped`와 `scopedIf` 메서드가 새로 추가되었습니다. 수동으로 이 인터페이스를 구현한다면 해당 메서드도 추가해야 합니다.

#### `ContextualBindingBuilder` 인터페이스

**영향도: 매우 낮음**

`Illuminate\Contracts\Container\ContextualBindingBuilder` 인터페이스에 `giveConfig` 메서드가 추가되었습니다. 구현하고 있다면, 다음과 같이 추가하세요:

```php
public function giveConfig($key, $default = null);
```

### 데이터베이스

<a name="postgres-schema-configuration"></a>
#### Postgres "Schema" 설정

**영향도: 중간**

애플리케이션의 `config/database.php` 파일에서 Postgres 연결의 검색 경로를 지정하는 `schema` 설정 옵션은 `search_path`로 이름이 변경되어야 합니다.

<a name="schema-builder-doctrine-method"></a>
#### Schema Builder의 `registerCustomDoctrineType` 메서드

**영향도: 낮음**

`Illuminate\Database\Schema\Builder` 클래스에서 `registerCustomDoctrineType` 메서드가 제거되었습니다. 대신 `DB` 파사드의 `registerDoctrineType`을 사용하거나, 커스텀 Doctrine 타입을 `config/database.php`에 등록하세요.

### Eloquent

<a name="custom-casts-and-null"></a>
#### 커스텀 캐스트 & `null`

**영향도: 중간**

이전에는 커스텀 캐스트 클래스의 `set` 메서드는 캐스트 속성이 `null`로 설정될 때 호출되지 않았으나, 이는 문서화된 동작과 달랐습니다. 9.x에서는 값이 `null`일 때도 `set` 메서드가 호출되므로, 커스텀 캐스트 구현이 이 상황을 적절히 처리하도록 해야 합니다.

```php
/**
 * 주어진 값을 저장용으로 준비합니다.
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

이전에는 `belongsToMany` 관계 메서드에서 첫 번째 인자인 속성 배열을 "pivot" 테이블에서 비교했으나, 이제는 관련 모델의 테이블에서 비교하도록 변경되었습니다.

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

또한, `firstOrCreate` 메서드는 두 번째 인자로 `$values` 배열을 받을 수 있으며, 새로운 관련 모델을 생성할 경우 해당 속성과 병합되어 사용됩니다. 이제 다른 관계의 `firstOrCreate`와 동작이 일치합니다.

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

#### `touch` 메서드

**영향도: 낮음**

`touch` 메서드는 이제 터치할 속성 이름을 인자로 받을 수 있습니다. 오버라이딩하고 있다면 시그니처를 다음과 같이 변경하세요:

```php
public function touch($attribute = null);
```

### 암호화

#### Encrypter 인터페이스

**영향도: 낮음**

`Illuminate\Contracts\Encryption\Encrypter` 인터페이스에 `getKey` 메서드가 추가되었습니다. 직접 구현한다면 다음을 추가하세요:

```php
public function getKey();
```

### 파사드

#### `getFacadeAccessor` 메서드

**영향도: 낮음**

`getFacadeAccessor` 메서드는 항상 컨테이너 바인딩 키를 반환해야 합니다. 이전에는 객체 인스턴스를 반환할 수 있었으나, 이제는 지원하지 않습니다. 파사드를 직접 작성했다면 문자열 바인딩 키를 반환해야 합니다:

```php
/**
 * 컴포넌트의 등록된 이름 반환
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

### 파일시스템

#### `FILESYSTEM_DRIVER` 환경 변수

**영향도: 낮음**

`FILESYSTEM_DRIVER` 환경 변수는 사용 목적을 더 명확히 하기 위해 `FILESYSTEM_DISK`로 이름이 변경되었습니다. 애플리케이션 스켈레톤에서만 바뀌었으므로, 필요시 환경 변수명을 직접 변경하면 됩니다.

#### "Cloud" 디스크

**영향도: 낮음**

`cloud` 디스크 설정은 2020년 11월 이후 기본 스켈레톤에서 제외되었습니다. "cloud" 디스크를 사용중이라면 앱에 해당 설정값을 계속 추가해두세요.

<a name="flysystem-3"></a>
### Flysystem 3.x

**영향도: 높음**

Laravel 9.x는 [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x에서 3.x로 마이그레이션했습니다. Flysystem은 `Storage` 파사드가 제공하는 파일 조작 메서드의 기반이 됩니다. 몇 가지 변경 사항이 있으니 애플리케이션에 맞게 수정이 필요할 수 있습니다.

#### 드라이버 사전 준비

S3, FTP, SFTP 드라이버 사용 전 Composer로 각 패키지를 설치하세요:

- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

#### 기존 파일 덮어쓰기

`put`, `write`, `writeStream` 등의 쓰기 작업은 이제 기본적으로 기존 파일을 덮어씁니다. 덮어쓰기를 원하지 않는다면, 쓰기 전에 파일 존재 여부를 수동으로 확인해야 합니다.

#### 쓰기 예외 처리

`put`, `write`, `writeStream` 등의 쓰기 작업에서 실패 시 더 이상 예외가 발생하지 않고, `false`가 반환됩니다. 이전처럼 예외를 원한다면 파일시스템 디스크 설정 배열에 `throw` 옵션을 명시하세요:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

#### 존재하지 않는 파일 읽기

존재하지 않는 파일을 읽으려 하면 이제 `null`이 반환됩니다. 이전에는 `Illuminate\Contracts\Filesystem\FileNotFoundException`이 발생했습니다.

#### 존재하지 않는 파일 삭제

존재하지 않는 파일을 삭제하면 항상 `true`가 반환됩니다.

#### 캐시 어댑터

Flysystem에서는 캐시 어댑터를 더 이상 지원하지 않으므로, Laravel에서도 관련 설정(예: 디스크 설정 내 `cache` 키)은 제거할 수 있습니다.

#### 커스텀 파일시스템

커스텀 파일시스템 드라이버 등록 방법이 약간 변경되었습니다. 직접 정의하거나 커스텀 드라이버를 제공하는 패키지를 사용할 경우 코드와 의존성을 업데이트하세요.

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

Flysystem SFTP 어댑터에서 개인-공개 키 인증을 사용하는 경우, 개인 키 복호화에 사용하던 설정 항목 `password`의 이름을 `passphrase`로 변경하세요.

### 헬퍼

<a name="data-get-function"></a>
#### `data_get` 헬퍼 & 이터러블 객체

**영향도: 매우 낮음**

이전에는 `data_get` 헬퍼가 배열이나 `Collection` 인스턴스의 중첩 데이터를 가져오는데만 사용 가능했으나, 이제 모든 이터러블 객체의 중첩 데이터도 가져올 수 있습니다.

<a name="str-function"></a>
#### `str` 헬퍼

**영향도: 매우 낮음**

Laravel 9.x에는 이제 글로벌 `str` [헬퍼 함수](/docs/{{version}}/helpers#method-str)가 내장되어 있습니다. 앱에서 동일한 이름으로 글로벌 `str` 헬퍼를 정의했을 경우, 충돌을 피하기 위해 이름을 변경하거나 제거해야 합니다.

<a name="when-and-unless-methods"></a>
#### `when` / `unless` 메서드

**영향도: 중간**

프레임워크의 다양한 클래스에서 제공하는 `when`/`unless` 메서드는, 첫 번째 인자인 불리언 값의 참/거짓에 따라 조건부로 동작을 수행합니다.

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

이전에는 클로저를 전달하면 항상 참으로 간주되어 조건이 무의미했으나, 9.x에서는 클로저를 실행한 반환값을 조건으로 사용합니다.

```php
$collection->when(function ($collection) {
    // 이 클로저가 실행됨...
    return false;
}, function ($collection) {
    // 첫 번째 클로저가 false를 반환하면 이 부분은 실행되지 않음...
    $collection->merge([1, 2, 3]);
});
```

### HTTP 클라이언트

<a name="http-client-default-timeout"></a>
#### 기본 타임아웃

**영향도: 중간**

[HTTP 클라이언트](/docs/{{version}}/http-client)는 이제 기본 타임아웃이 30초로 설정되어 있습니다. 즉, 서버가 30초 내로 응답하지 않으면 예외가 발생합니다. 이전에는 별도의 타임아웃이 없어 요청이 무한정 대기할 수 있었습니다.

요청별로 더 긴 타임아웃을 지정하려면 `timeout` 메서드를 사용하세요:

    $response = Http::timeout(120)->get(/* ... */);

#### HTTP Fake & 미들웨어

**영향도: 낮음**

이전에는 [HTTP 클라이언트](/docs/{{version}}/http-client)를 "faked" 했을 때 Guzzle 미들웨어가 실행되지 않았으나, 이제는 fake 상태에서도 Guzzle 미들웨어가 실행됩니다.

#### HTTP Fake & 의존성 주입

**영향도: 낮음**

이전에는 `Http::fake()` 호출이 클래스 생성자에 주입된 `Illuminate\Http\Client\Factory` 인스턴스에 영향을 미치지 못했으나, 이제는 의존성 주입된 HTTP 클라이언트에도 fake 응답이 반환됩니다. 이는 다른 파사드/페이크의 동작과 일치합니다.

<a name="symfony-mailer"></a>
### Symfony Mailer

**영향도: 높음**

Laravel 9.x의 가장 큰 변화 중 하나는 더 이상 유지보수되지 않는 SwiftMailer(2021년 12월 종료)에서 Symfony Mailer로의 전환입니다. 최대한 앱에 영향이 없도록 했으나, 아래 변경 내용을 꼼꼼히 읽고 애플리케이션 호환성을 반드시 확인하세요.

#### 드라이버 사전 준비

Mailgun 전송을 계속 사용하려면, 아래 Composer 패키지를 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

`wildbit/swiftmailer-postmark` 패키지는 제거하고 대신 아래 패키지를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

#### 반환 타입 변경

`Illuminate\Mail\Mailer`의 `send`, `html`, `raw`, `plain` 메서드는 더 이상 `void`를 반환하지 않습니다. 대신 `Illuminate\Mail\SentMessage` 인스턴스를 반환합니다. 이 객체에서 `Symfony\Component\Mailer\SentMessage`를 `getSymfonySentMessage` 메서드 또는 동적 호출로 접근할 수 있습니다.

#### "Swift" 접두어 메서드 이름 변경

SwiftMailer 관련 메서드(일부는 문서화되어 있지 않음)는 Symfony Mailer에 맞춰 이름이 변경되었습니다. 예를 들어, `withSwiftMessage`는 `withSymfonyMessage`로 변경되었습니다.

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

> **경고**  
> [Symfony Mailer 문서](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages)를 꼼꼼히 읽고 `Symfony\Component\Mime\Email` 객체와의 모든 상호작용을 확인하세요.

다음은 더 상세한 메서드 이름 변경 목록입니다. 대부분 SwiftMailer/Symfony Mailer를 직접 다룰 때 필요한 저수준 메서드로, 대부분의 Laravel 앱에서는 잘 사용하지 않습니다:

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

#### Proxied `Illuminate\Mail\Message` 메서드

`Illuminate\Mail\Message`는 누락된 메서드를 Swift_Message 인스턴스로 프록시했으나, 이제는 `Symfony\Component\Mime\Email` 인스턴스로 프록시됩니다. 관련 코드는 새 메서드에 맞게 업데이트해야 합니다.

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

#### 생성된 메시지 ID

SwiftMailer는 생성된 메시지 ID에 도메인을 커스터마이징할 수 있었으나, Symfony Mailer는 이를 지원하지 않고 발신자로부터 자동 생성합니다.

#### `MessageSent` 이벤트 변경점

`Illuminate\Mail\Events\MessageSent` 이벤트의 `message` 속성은 이제 `Swift_Message` 대신 `Symfony\Component\Mime\Email` 인스턴스를 담고 있습니다(이메일 발송 전).

또한 `sent` 속성이 추가되어, 전송된 이메일 정보(`Illuminate\Mail\SentMessage` 인스턴스, 메시지 ID 등)를 포함합니다.

#### 강제 재연결

이제 트랜스포트(발송 드라이버) 재연결을 강제로 할 수 없습니다(데몬 프로세스에서 수행하던 방식). 대신 Symfony Mailer가 필요시 자동으로 재연결을 시도하고, 실패 시 예외를 발생시킵니다.

#### SMTP 스트림 옵션

SMTP 트랜스포트에 대한 스트림 옵션 지정은 더 이상 지원되지 않습니다. 지원되는 옵션은 설정파일에서 직접 지정하세요. 예시로, TLS 피어 검증 비활성화:

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

자세한 설정 옵션은 [Symfony Mailer 문서](https://symfony.com/doc/6.0/mailer.html#transport-setup)를 참고하세요.

> **경고**  
> 위 예시처럼 SSL 검증을 비활성화하는 것은 일반적으로 권장하지 않습니다. "중간자 공격"과 같은 보안 위협이 생길 수 있습니다.

#### SMTP `auth_mode`

메일 설정 파일에서 SMTP `auth_mode`를 따로 지정할 필요가 없습니다. 인증 모드는 Symfony Mailer와 SMTP 서버가 자동 협상합니다.

#### 실패한 수신자

이제 메시지 전송 이후 실패한 수신자 목록을 가져올 수 없습니다. 대신, 메시지 전송 실패 시 `Symfony\Component\Mailer\Exception\TransportExceptionInterface` 예외가 발생합니다. 전송 후 잘못된 이메일을 파악하기보다, 전송 전 이메일 주소 유효성을 검증하는 것이 좋습니다.

### 패키지

<a name="the-lang-directory"></a>
#### `lang` 디렉터리

**영향도: 중간**

새로운 Laravel 애플리케이션에서는 `resources/lang` 디렉터리가 루트 프로젝트 경로(`lang`)로 이동했습니다. 패키지가 이 디렉터리로 언어파일을 퍼블리시한다면, 하드코딩 경로 대신 `app()->langPath()`를 사용하세요.

<a name="queue"></a>
### 큐

<a name="the-opis-closure-library"></a>
#### `opis/closure` 라이브러리

**영향도: 낮음**

Laravel의 `opis/closure` 의존성은 `laravel/serializable-closure`로 대체되었습니다. `opis/closure`를 직접 사용하거나, 삭제된 `Illuminate\Queue\SerializableClosureFactory`/`SerializableClosure` 클래스를 사용한다면, [Laravel Serializable Closure](https://github.com/laravel/serializable-closure)로 대체하세요.

#### Failed Job Provider의 `flush` 메서드

**영향도: 낮음**

`Illuminate\Queue\Failed\FailedJobProviderInterface` 인터페이스의 `flush` 메서드는 이제 `$hours` 인자를 받습니다(플러시될 실패한 잡의 '최소 시간(시간 단위)'). 직접 구현한다면 시그니처를 아래처럼 변경하세요:

```php
public function flush($hours = null);
```

### 세션

#### `getSession` 메서드

**영향도: 낮음**

Laravel의 `Illuminate\Http\Request`가 상속하는 `Symfony\Component\HttpFoundation\Request` 클래스는 세션 스토리지 핸들러를 가져오는 `getSession` 메서드를 제공합니다. Laravel 문서에는 별도 안내가 없지만, 해당 메서드는 이제 `Symfony\Component\HttpFoundation\Session\SessionInterface` 인스턴스를 반환하거나 세션이 없으면 `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` 예외를 발생시킵니다.

### 테스트

<a name="the-assert-deleted-method"></a>
#### `assertDeleted` 메서드

**영향도: 중간**

모든 `assertDeleted` 호출을 `assertModelMissing`으로 변경해야 합니다.

### 신뢰할 수 있는 프록시

**영향도: 낮음**

Laravel 8에서 9로 애플리케이션 코드를 새로운 9.x 스켈레톤으로 가져오는 경우, "신뢰할 수 있는 프록시" 미들웨어를 업데이트해야 할 수 있습니다.

`app/Http/Middleware/TrustProxies.php` 파일에서,

`use Fideloper\Proxy\TrustProxies as Middleware`를  
`use Illuminate\Http\Middleware\TrustProxies as Middleware`로 바꾸세요.

그리고 `$headers` 속성을 아래처럼 수정하세요:

```php
// 변경 전
protected $headers = Request::HEADER_X_FORWARDED_ALL;

// 변경 후
protected $headers =
    Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB;
```

마지막으로, `fideloper/proxy` Composer 의존성을 제거하세요.

```shell
composer remove fideloper/proxy
```

### 검증(Validation)

#### Form Request의 `validated` 메서드

**영향도: 낮음**

Form Request가 제공하는 `validated` 메서드는 이제 `$key`와 `$default` 인자를 받을 수 있습니다. 이 메서드를 오버라이드 했다면, 시그니처를 수정하세요:

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
#### `password` 규칙

**영향도: 중간**

입력값이 인증된 사용자의 현재 비밀번호와 일치하는지 확인하는 `password` 규칙이 `current_password`로 이름이 변경되었습니다.

<a name="unvalidated-array-keys"></a>
#### 검증되지 않은 배열 키

**영향도: 중간**

이전에는 검증되지 않은 배열 키를 반환값에서 제외할지 직접 지정해야 했지만, Laravel 9.x에서는 `array` 규칙에 허용 키를 지정하지 않은 경우에도 "validated" 데이터에 항상 포함되지 않습니다.  
기존 방식으로 돌아가고 싶다면, 서비스 프로바이더의 `boot` 메서드에서 `includeUnvalidatedArrayKeys`를 호출하세요:

```php
use Illuminate\Support\Facades\Validator;

/**
 * 애플리케이션 서비스 등록
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

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경사항도 참고하길 권장합니다. 이 가이드에 포함되지 않은 설정 파일/주석 등은 직접 [GitHub 비교 도구](https://github.com/laravel/laravel/compare/8.x...9.x)를 통해 필요한 변경만 선택적으로 반영할 수 있습니다.