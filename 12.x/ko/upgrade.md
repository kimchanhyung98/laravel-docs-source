# 업그레이드 가이드 (Upgrade Guide)

- [12.0 버전으로 11.x에서 업그레이드](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 주요 변경점 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경점 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 경미한 영향 변경점 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과의 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해결](#container-class-dependency-resolution)
- [이미지 유효성 검증에서 SVG 제외](#image-validation)
- [로컬 파일 시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 조회](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 12.0 버전으로 11.x에서 업그레이드 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 소요 시간: 5분

> [!NOTE]
> 모든 잠재적인 변경 사항을 문서화하려고 최선을 다했습니다. 이 중 일부는 프레임워크의 특이한 부분에서 발생하므로, 실제로는 소수만이 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

여러분의 애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework` : `^12.0`으로 업그레이드
- `phpunit/phpunit` : `^11.0`으로 업그레이드
- `pestphp/pest` : `^3.0`으로 업그레이드

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x에 대한 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션에서는 이제 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)를 사용해야 합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 인스톨러 업데이트 (Updating the Laravel Installer)

Laravel 애플리케이션을 새로 생성할 때 CLI 기반 Laravel 인스톨러 툴을 사용 중이라면, Laravel 12.x와 [새로운 Laravel 스타터 키트](https://laravel.com/starter-kits)에 호환되도록 인스톨러를 업데이트해야 합니다. `composer global require`로 인스톨러를 설치했다면, 다음 명령어로 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

만약 PHP와 Laravel을 `php.new`를 통해 설치했다면, 사용하는 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 Laravel 인스톨러를 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 반드시 관리자 권한으로 실행하세요...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는, [Laravel Herd](https://herd.laravel.com)의 번들된 Laravel 인스톨러를 사용 중이라면 Herd 설치본을 최신 릴리즈로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자가 `$expires` 파라미터를 분(minute) 단위가 아닌 초(second) 단위로 받도록 변경되었습니다.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과의 인덱스 매핑 (Concurrency Result Index Mapping)

**영향 가능성: 낮음**

`Concurrency::run` 메서드에 연관 배열(associative array)을 전달할 때, 동시 작업의 결과가 이제 해당 키와 함께 반환됩니다.

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
#### 컨테이너 클래스 의존성 해결 (Container Class Dependency Resolution)

**영향 가능성: 낮음**

의존성 주입 컨테이너가 클래스 인스턴스를 생성할 때, 이제 클래스 속성의 기본값을 존중합니다. 이전에는 기본값 없이 인스턴스가 생성되었을 수 있으므로, 이 변경을 고려해 애플리케이션을 조정해야 할 수 있습니다.

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
#### 다중 스키마 데이터베이스 조회 (Multi-Schema Database Inspecting)

**영향 가능성: 낮음**

이제 `Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 기본적으로 모든 스키마에서 결과를 조회합니다. 특정 스키마만 조회하려면 `schema` 인수를 전달할 수 있습니다.

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 기본값으로 스키마가 포함된 테이블 이름을 반환합니다. 동작을 변경하려면 `schemaQualified` 인수를 사용할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

이제 `db:table`과 `db:show` 명령어는 PostgreSQL과 SQL Server뿐만 아니라 MySQL, MariaDB, SQLite에서도 모든 스키마의 결과를 출력합니다.

<a name="database-constructor-signature-changes"></a>
#### 데이터베이스 생성자 시그니처 변경 (Database Constructor Signature Changes)

**영향 가능성: 매우 낮음**

Laravel 12에서는 여러 저수준 데이터베이스 클래스가 생성자에서 `Illuminate\Database\Connection` 인스턴스를 반드시 전달받도록 변경되었습니다.

**이 변경점은 주로 데이터베이스 패키지 관리자에게 적용됩니다. 일반적인 애플리케이션 개발에 영향이 있을 가능성은 매우 낮습니다.**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫번째 인수로 `Connection` 인스턴스를 기대합니다. 수동으로 `Blueprint` 인스턴스를 생성하는 애플리케이션이나 패키지에 영향이 있습니다.

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` 클래스도 이제 생성자에서 `Connection` 인스턴스를 요구합니다. 이전 버전에서는 `setConnection()` 메서드로 연결을 주입했지만, Laravel 12에서는 이 메서드가 제거되었습니다.

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
```

또한, 다음 API가 제거 또는 폐기(deprecated)되었습니다.

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` 메서드는 폐기되었습니다.
- `Connection::withTablePrefix()` 메서드는 제거되었습니다.
- `Grammar::getTablePrefix()` 및 `setTablePrefix()` 메서드는 폐기되었습니다.
- `Grammar::setConnection()` 메서드는 제거되었습니다.

</div>

테이블 접두사를 사용할 때에는 이제 데이터베이스 연결에서 직접 값을 가져와야 합니다.

```php
$prefix = $connection->getTablePrefix();
```

커스텀 데이터베이스 드라이버나 스키마 빌더, Grammar 구현을 유지보수한다면, 생성자를 확인하여 반드시 `Connection` 인스턴스를 전달하는지 검토해야 합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7 (Models and UUIDv7)

**영향 가능성: 중간**

`HasUuids` 트레이트는 이제 UUID 사양의 버전 7(정렬된 UUID)에 호환되는 UUID를 반환합니다. 기존의 Ordered UUIDv4 문자열 사용을 계속 원한다면, 이제 `HasVersion4Uuids` 트레이트를 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 제거되었습니다. 기존에 이 트레이트를 사용했다면, 이제 동일한 동작을 하는 `HasUuids` 트레이트로 대체해야 합니다.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합 (Nested Array Request Merging)

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용해 중첩 배열 데이터를 병합할 수 있습니다. 이전에는 "dot" 표기법 키를 가진 최상위 배열 키를 생성하는 동작에 의존했다면, 이 새로운 동작을 반영하도록 애플리케이션을 조정해야 할 수 있습니다.

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

애플리케이션의 파일시스템 설정에서 `local` 디스크를 명시적으로 정의하지 않은 경우, Laravel은 이제 기본적으로 로컬 디스크의 루트를 `storage/app/private`로 설정합니다. 이전 릴리즈에서는 기본 경로가 `storage/app`였습니다. 따라서 `Storage::disk('local')` 호출 시 별도 설정이 없으면 `storage/app/private` 디렉터리에서 파일을 읽고 쓰게 됩니다. 이전 동작으로 되돌리려면 `local` 디스크를 수동으로 정의하여 원하는 루트 경로를 설정해야 합니다.

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검증에서 SVG 제외 (Image Validation Now Excludes SVGs)

**영향 가능성: 낮음**

`image` 유효성 검증 규칙이 이제 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙 사용 시 SVG를 허용하려면 반드시 명시적으로 설정해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 (Miscellaneous)

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경사항도 함께 참고할 것을 권장합니다. 다소 필수적이지 않은 변경도 있으나, 여러분의 애플리케이션과 동기화하는 것이 유익할 수 있습니다. 이 업그레이드 가이드에서 다루는 일부 변경 외에도, 설정 파일이나 주석 변경 등은 다루지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 변경된 모든 내역을 한눈에 확인하고, 필요한 업데이트를 선택할 수 있습니다.
