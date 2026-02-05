# 업그레이드 가이드 (Upgrade Guide)

- [12.0으로 업그레이드하기 (11.x에서)](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 영향도가 큰 변경사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해석](#container-class-dependency-resolution)
- [이미지 유효성 검증 시 SVG 제외](#image-validation)
- [로컬 파일 시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 12.0으로 업그레이드하기 (11.x에서) (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 소요 시간: 5분

> [!NOTE]
> 가능한 모든 동작에 영향을 줄 수 있는 변경사항을 최대한 문서화하고 있습니다. 이러한 변경사항 중 일부는 프레임워크의 특정 부분에만 해당되며, 실제로는 일부 애플리케이션에만 영향을 줄 수 있습니다. 시간을 절약하고 싶다면, 애플리케이션 업그레이드를 자동화해주는 [Laravel Shift](https://laravelshift.com/)를 사용할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성 패키지 버전을 반드시 업그레이드해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`을 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x에 대한 지원이 제거되었습니다. 이제 모든 Laravel 12 애플리케이션은 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)가 필요합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 인스톨러 업데이트 (Updating the Laravel Installer)

새로운 Laravel 애플리케이션을 생성할 때 Laravel 인스톨러 CLI 도구를 사용하는 경우, 인스톨러가 Laravel 12.x 및 [새로운 Laravel 스타터 킷](https://laravel.com/starter-kits)과 호환되도록 업데이트해야 합니다. 인스톨러를 `composer global require`로 설치했다면, 다음 명령어로 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

PHP와 Laravel을 `php.new`를 통해 설치하였다면, 사용 중인 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 Laravel 인스톨러를 설치하세요:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는 [Laravel Herd](https://herd.laravel.com)가 제공하는 Laravel 인스톨러를 사용 중인 경우, Herd를 최신 버전으로 업데이트해 주시기 바랍니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자가 이제 `$expires` 파라미터를 분 단위가 아니라 초 단위로 받도록 변경되었습니다.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑 (Concurrency Result Index Mapping)

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열(associative array)과 함께 호출하면, 동시 작업의 결과가 해당 키와 매핑되어 반환됩니다:

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 컨테이너 (Container)

<a name="container-class-dependency-resolution"></a>
#### 컨테이너 클래스 의존성 해석 (Container Class Dependency Resolution)

**영향 가능성: 낮음**

의존성 주입 컨테이너는 이제 클래스 인스턴스 해석 시 클래스 속성의 기본값(default value)을 존중합니다. 이전에는 컨테이너가 기본값 없이 클래스를 해석하도록 의존하고 있었다면, 이 변경 사항에 맞춰 애플리케이션을 조정해야 할 수 있습니다:

```php
class Example
{
    public function __construct(public ?Carbon $date = null) {}
}

$example = resolve(Example::class);

// <= 11.x
$example->date instanceof Carbon;

// >= 12.x
$example->date === null;
```

<a name="database"></a>
### 데이터베이스 (Database)

<a name="multi-schema-database-inspecting"></a>
#### 다중 스키마 데이터베이스 검사 (Multi-Schema Database Inspecting)

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마(schema)의 결과를 포함합니다. 특정 스키마에 대한 결과만 조회하고 싶다면 `schema` 인수를 전달할 수 있습니다:

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 테이블만...
$tables = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 테이블만...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마명이 포함된 테이블명(스키마-자격 이름)을 반환합니다. 원하는 동작으로 변경하려면 `schemaQualified` 인수를 전달할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어는 이제 MySQL, MariaDB, SQLite에서도 PostgreSQL, SQL Server와 마찬가지로 모든 스키마의 결과를 출력합니다.

<a name="database-constructor-signature-changes"></a>
#### 데이터베이스 생성자 시그니처 변경 (Database Constructor Signature Changes)

**영향 가능성: 매우 낮음**

Laravel 12에서는 여러 낮은 계층의 데이터베이스 클래스 생성자에 `Illuminate\Database\Connection` 인스턴스가 필수로 전달되어야 합니다.

**이 변경 내용은 주로 데이터베이스 패키지 관리자에게 해당되며, 일반적인 애플리케이션 개발에서는 영향받을 가능성이 매우 낮습니다.**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Connection` 인스턴스를 받습니다. 직접적으로 Blueprint 인스턴스를 생성하는 애플리케이션이나 패키지에 주로 영향을 미칩니다.

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` 클래스의 생성자도 이제 `Connection` 인스턴스를 필요로 합니다. 이전 버전에서는 생성 후 `setConnection()` 메서드를 사용하여 연결을 할당했습니다. 이 메서드는 Laravel 12에서 제거되었습니다:

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
```

또한, 다음 API가 제거되거나 deprecated되었습니다:

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` 메서드는 deprecated되었습니다.
- `Connection::withTablePrefix()` 메서드는 제거되었습니다.
- `Grammar::getTablePrefix()`, `setTablePrefix()` 메서드는 deprecated되었습니다.
- `Grammar::setConnection()` 메서드는 제거되었습니다.

</div>

테이블 prefix를 다룰 때는, 이제 데이터베이스 연결에서 직접 가져와야 합니다:

```php
$prefix = $connection->getTablePrefix();
```

사용자 지정 데이터베이스 드라이버, 스키마 빌더, grammar 구현체 등을 관리한다면, 생성자에서 반드시 `Connection` 인스턴스를 전달하고 있는지 확인해야 합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7 (Models and UUIDv7)

**영향 가능성: 중간**

`HasUuids` 트레이트는 이제 UUID 스펙의 7버전(ordered UUID)에 호환되는 UUID를 반환합니다. 모델의 ID로 기존에 순차적 ordered UUIDv4 문자열을 계속 사용하고 싶다면, 이제 `HasVersion4Uuids` 트레이트를 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 제거되었습니다. 기존에 이 트레이트를 사용 중이었다면, 이제 동일한 동작을 제공하는 `HasUuids` 트레이트를 이용하세요.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합 (Nested Array Request Merging)

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드가 이제 "dot" 표기법을 이용해 중첩 배열 데이터를 병합할 수 있습니다. 기존에는 이 메서드가 "dot" 표기법의 키명을 가진 최상위 배열 키를 만들었다면, 이제 변경된 동작에 맞춰 애플리케이션을 조정해야 할 수 있습니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="storage"></a>
### 스토리지 (Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일 시스템 디스크 기본 루트 경로 (Local Filesystem Disk Default Root Path)

**영향 가능성: 낮음**

애플리케이션에서 파일시스템 설정에 `local` 디스크를 명시적으로 정의하지 않은 경우, Laravel은 이제 로컬 디스크의 루트를 `storage/app`이 아닌 `storage/app/private`으로 기본 설정합니다. 이로 인해 `Storage::disk('local')`로 파일을 읽거나 쓸 때 설정을 변경하지 않았다면 `storage/app/private`을 사용하게 됩니다. 기존의 경로로 동작하게 하려면, 파일시스템 설정에서 직접 `local` 디스크와 원하는 루트 경로를 지정해야 합니다.

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검증 시 SVG 제외 (Image Validation Now Excludes SVGs)

**영향 가능성: 낮음**

`image` 유효성 검증 규칙은 이제 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙을 사용할 때 SVG를 허용하려면 명시적으로 설정해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 (Miscellaneous)

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 참고하기를 권장합니다. 이러한 변경 사항의 대부분은 필수는 아니지만, 애플리케이션을 최신 상태로 유지하고 싶다면 이 파일들과 동기화할 수 있습니다. 일부 변경 사항은 이 업그레이드 가이드에서 다르지만, 설정 파일이나 주석 등의 변화는 포함되지 않을 수 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 변경된 내용을 한눈에 쉽게 확인하고 적용할 것만 선택할 수 있습니다.
