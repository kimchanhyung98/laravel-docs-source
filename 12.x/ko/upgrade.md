# 업그레이드 가이드 (Upgrade Guide)

- [11.x에서 12.0으로 업그레이드](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 영향도가 높은 변경 사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [라라벨 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경 사항

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경 사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해석](#container-class-dependency-resolution)
- [이제 SVG는 이미지 유효성 검증에서 제외됨](#image-validation)
- [로컬 파일시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드

#### 예상 소요 시간: 5분

> [!NOTE]
> 가능한 모든 호환성 깨짐(breaking change) 변경 사항을 문서화하려고 노력했습니다. 이런 변경 사항 중 일부는 프레임워크의 잘 알려지지 않은 부분에서 발생하기 때문에 실제로는 일부만 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하면 애플리케이션 업그레이드를 자동화하는 데 도움이 됩니다.

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

[Carbon 2.x](https://carbon.nesbot.com/docs/)에 대한 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)를 필요로 합니다.

<a name="updating-the-laravel-installer"></a>
### 라라벨 인스톨러 업데이트

새로운 라라벨 애플리케이션을 생성할 때 라라벨 인스톨러 CLI 도구를 사용하고 있다면, 인스톨러를 12.x 및 [새로운 라라벨 스타터 키트](https://laravel.com/starter-kits)와 호환되는 버전으로 반드시 업데이트해야 합니다. `composer global require`로 설치했다면 아래 명령어로 인스톨러를 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

PHP와 라라벨을 `php.new`를 통해 처음 설치했었다면, 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 라라벨 인스톨러를 설치할 수 있습니다.

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행해야 합니다...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는 [Laravel Herd](https://herd.laravel.com)에 기본 내장된 라라벨 인스톨러를 사용하고 있다면, Herd 설치본을 최신 릴리스로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자에서 `$expires` 인수가 이제 분 단위가 아닌 **초 단위**로 입력되어야 합니다.

<a name="concurrency"></a>
### 동시성(Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열(associative array)과 함께 호출할 때, 동시 작업의 결과가 각각의 키와 매핑되어 반환됩니다.

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 컨테이너

<a name="container-class-dependency-resolution"></a>
#### 컨테이너 클래스 의존성 해석

**영향 가능성: 낮음**

이제 의존성 주입 컨테이너가 클래스 인스턴스를 해석할 때 해당 클래스 속성의 기본값을 존중합니다. 이전에는 컨테이너를 통해 클래스 인스턴스를 생성하면 기본값이 무시될 수 있었으나, 이제는 기본값이 반영됩니다. 이에 따라 애플리케이션에서 이 동작에 의존하고 있다면 코드를 조정해야 할 수 있습니다.

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
### 데이터베이스

<a name="multi-schema-database-inspecting"></a>
#### 다중 스키마 데이터베이스 검사

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 반환합니다. 특정 스키마의 결과만 받고 싶다면 `schema` 인수를 전달할 수 있습니다.

```php
// 모든 스키마의 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main', 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

또한, `Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 지정된 테이블명(schema-qualified table name)을 반환합니다. 동작을 변경하려면 `schemaQualified` 인수를 넘기면 됩니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table`과 `db:show` 명령어 또한 이제 MySQL, MariaDB, SQLite에서 PostgreSQL 및 SQL Server와 마찬가지로 모든 스키마의 결과를 출력합니다.

<a name="updated-blueprint-constructor-signature"></a>
#### `Blueprint` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자가 첫 번째 인수로 `Illuminate\Database\Connection` 인스턴스를 받도록 변경되었습니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

`HasUuids` 트레이트는 이제 UUID 명세(version 7)에 호환되는 UUID(정렬 가능한 UUID)를 반환합니다. 모델의 ID에 계속해서 정렬 가능한 UUIDv4 문자열을 사용하고 싶다면, 이제 `HasVersion4Uuids` 트레이트를 대신 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 삭제되었습니다. 이전에 이 트레이트를 사용하고 있었다면, 이제는 `HasUuids` 트레이트를 사용해야 하며, 동일한 동작을 제공합니다.

<a name="requests"></a>
### 요청(Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "점(dot) 표기법"을 사용해 중첩 배열 데이터를 병합할 수 있습니다. 이전에는 이 메서드를 통해 "dot" 표기 형식의 키로 최상위 배열 항목이 생성되었으나, 이제는 실제로 중첩된 배열 구조가 병합됩니다. 이에 따라 기존의 동작에 의존하고 있었다면 코드를 수정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="storage"></a>
### 저장소(Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일시스템 디스크 기본 루트 경로

**영향 가능성: 낮음**

파일시스템 설정에 `local` 디스크가 명시적으로 정의되어 있지 않은 경우, 라라벨은 이제 기본적으로 `local` 디스크의 root를 `storage/app/private`으로 설정합니다. 이전 릴리스에서는 기본값이 `storage/app`이었습니다. 따라서 `Storage::disk('local')`을 호출할 경우 별도 설정하지 않았다면 `storage/app/private`에서 파일을 읽고 쓰게 됩니다. 예전 동작을 복원하려면 `local` 디스크를 직접 설정하고 원하는 root 경로를 지정하면 됩니다.

<a name="validation"></a>
### 유효성 검증(Validation)

<a name="image-validation"></a>
#### 이제 이미지 유효성 검증이 SVG를 제외함

**영향 가능성: 낮음**

`image` 유효성 검증 규칙이 기본적으로 SVG 이미지를 허용하지 않게 변경되었습니다. 만약 `image` 규칙 사용 시 SVG도 허용하고 싶다면, 명시적으로 허용 옵션을 추가해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 변경 사항

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 참고하시기를 권장합니다. 이런 변경의 상당수는 필수가 아니지만, 애플리케이션 코드와 동기화해둘 수 있습니다. 이 업그레이드 가이드에서 다루는 변경 외에도, 설정 파일이나 주석 등 다양한 부분이 변경되었을 수 있으니 [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 통해 어떤 업데이트가 중요한지 직접 확인해볼 수 있습니다.