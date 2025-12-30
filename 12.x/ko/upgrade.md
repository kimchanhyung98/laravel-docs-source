# 업그레이드 가이드 (Upgrade Guide)

- [11.x에서 12.0으로 업그레이드하기](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 주의가 필요한 주요 변경사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경사항

<div class="content-list" markdown="1">

- [모델 및 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 사소한 영향 변경사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해석](#container-class-dependency-resolution)
- [이미지 유효성 검사에서 SVG 제외](#image-validation)
- [로컬 파일시스템 디스크의 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 인스펙팅](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 모든 잠재적인 변경사항을 문서화하려고 노력하지만, 일부는 프레임워크의 드문 부분에 해당하므로 실제로는 일부 변경사항만 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하여 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`을 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x 지원이 제거되었습니다. 이제 모든 Laravel 12 애플리케이션은 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)를 필요로 합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 인스톨러 업데이트

새로운 Laravel 애플리케이션을 생성할 때 Laravel 인스톨러 CLI 도구를 사용하는 경우, Laravel 12.x 및 [새로운 Laravel 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 인스톨러를 업데이트해야 합니다. `composer global require`로 인스톨러를 설치했다면, 다음 명령어로 인스톨러를 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

만약 `php.new`를 통해 PHP와 Laravel을 설치했다면, 사용하는 운영체제에 맞는 `php.new` 설치 명령을 다시 실행하여 최신 버전의 PHP와 Laravel 인스톨러를 설치할 수 있습니다.

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

또는, [Laravel Herd](https://herd.laravel.com)가 제공하는 Laravel 인스톨러를 사용 중이라면 Herd 설치본을 최신 릴리스로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자는 이제 `$expires` 인수를 **분 단위가 아닌 초 단위**로 입력받아야 합니다.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열로 호출하면, 동시 작업의 결과가 이제 각 키와 같이 반환됩니다.

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
#### 컨테이너 클래스 의존성 해석

**영향 가능성: 낮음**

의존성 주입 컨테이너는 이제 클래스 인스턴스를 해석할 때 프로퍼티의 기본값을 존중합니다. 만약 이 전에는 기본값 대신 컨테이너가 인스턴스를 해석해주길 기대했다면, 이 동작 변화를 고려하여 애플리케이션을 수정해야 할 수 있습니다.

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
#### 다중 스키마 데이터베이스 인스펙팅

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마만 조회하려면 `schema` 인수를 전달하면 됩니다.

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블명(스키마-테이블 형태)을 반환합니다. 필요에 따라 `schemaQualified` 인수로 동작을 변경할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어는 이제 MySQL, MariaDB, SQLite에서 PostgreSQL 및 SQL Server와 마찬가지로 모든 스키마의 결과를 출력합니다.

<a name="updated-blueprint-constructor-signature"></a>
#### `Blueprint` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 가장 첫 번째 인수로 `Illuminate\Database\Connection` 인스턴스를 요구합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델 및 UUIDv7

**영향 가능성: 중간**

`HasUuids` 트레이트는 이제 UUID 스펙 버전 7(정렬이 가능한 UUID)에 호환되는 값을 반환합니다. 모델의 ID로 계속해서 순서가 있는 UUIDv4 문자열을 사용하고 싶다면, `HasVersion4Uuids` 트레이트를 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 제거되었습니다. 만약 이 트레이트를 사용했다면, 대신 `HasUuids` 트레이트를 사용하면 동일한 동작이 제공됩니다.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "도트" 표기법을 사용한 중첩 배열 데이터를 병합할 수 있습니다. 기존에는 이 메서드로 상위 배열 키에 도트 표기법 전체를 키값으로 사용하는 동작에 의존했다면, 이 변경에 맞게 코드를 조정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="storage"></a>
### 스토리지 (Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일시스템 디스크의 기본 루트 경로

**영향 가능성: 낮음**

애플리케이션에서 `local` 디스크를 filesystems 설정에서 명시적으로 정의하지 않은 경우, Laravel은 이제 기본적으로 local 디스크의 루트를 `storage/app/private`으로 설정합니다. 이전 릴리스에서는 기본 루트가 `storage/app`이었습니다. 따라서 `Storage::disk('local')` 호출 시 별도 설정이 없으면 `storage/app/private`에서 파일을 읽고 쓰게 됩니다. 기존 동작으로 되돌리려면, `local` 디스크를 직접 정의하고 원하는 루트 경로로 설정해야 합니다.

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검사에서 SVG 제외

**영향 가능성: 낮음**

`image` 유효성 검사 규칙은 이제 기본적으로 SVG 이미지를 허용하지 않습니다. 만약 `image` 규칙을 사용할 때 SVG를 허용하고 싶다면, 명시적으로 허용 옵션을 추가해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 변경사항

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)에서 변경 내역을 확인하는 것도 권장합니다. 이러한 변경사항 중 상당수는 필수는 아니지만, 애플리케이션과의 동기화를 고려할 수 있습니다. 일부 변경 사항은 본 업그레이드 가이드에서 다루지만, 설정 파일이나 주석 등의 변경은 포함되지 않을 수 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 어떤 업데이트가 중요한지 쉽게 확인할 수 있습니다.
