# 업그레이드 가이드

- [11.x에서 12.0으로 업그레이드하기](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 주요 변경사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [라라벨 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 수준 영향 변경사항

<div class="content-list" markdown="1">

- [모델 및 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 경미한 영향 변경사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해석](#container-class-dependency-resolution)
- [이미지 유효성 검증 시 SVG 제외](#image-validation)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 머지](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 모든 잠재적 호환성 깨짐(breaking change)을 문서화하려고 노력했습니다. 이러한 변경 중 일부는 프레임워크의 잘 알려지지 않은 부분에 있기 때문에 실제로 애플리케이션에 영향을 미치는 변경은 일부에 불과할 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하여 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성들을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`를 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

[Carbon 2.x](https://carbon.nesbot.com/docs/) 지원이 제거되었습니다. 이제 모든 Laravel 12 애플리케이션은 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)가 필요합니다.

<a name="updating-the-laravel-installer"></a>
### 라라벨 인스톨러 업데이트

새로운 라라벨 애플리케이션 생성을 위해 Laravel 인스톨러 CLI 도구를 사용하는 경우, 인스톨러를 Laravel 12.x 및 [새로운 라라벨 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 업데이트해야 합니다. `composer global require`를 통해 인스톨러를 설치했다면, 다음 명령어로 인스톨러를 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

처음에 PHP 및 Laravel을 `php.new`를 통해 설치한 경우, 단순히 해당 운영체제의 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 라라벨 인스톨러를 설치할 수 있습니다:

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

또는, [Laravel Herd](https://herd.laravel.com)에 번들로 포함된 라라벨 인스톨러를 사용 중이라면, Herd 설치본을 최신 릴리즈로 업데이트해야 합니다.

<a name="concurrency"></a>
### 동시성

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열로 호출할 때, 동시 작업의 결과가 해당 키와 함께 반환됩니다:

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

의존성 주입 컨테이너가 클래스 인스턴스를 해석할 때, 이제 클래스 프로퍼티의 기본값을 존중합니다. 이전에 컨테이너가 기본값 없이 클래스를 해석하길 기대했다면, 이 새로운 동작에 맞게 애플리케이션을 조정해야 할 수 있습니다:

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

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마만 결과로 받으려면 `schema` 인자를 전달할 수 있습니다:

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$table = Schema::getTables(schema: 'main');

// 'main' 및 'blog' 스키마의 모든 테이블...
$table = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블 이름을 반환합니다. 원하는 대로 동작을 변경하려면 `schemaQualified` 인자를 사용할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$table = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$table = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

이제 `db:table` 및 `db:show` 명령어는 MySQL, MariaDB, SQLite에서도 PostgreSQL 및 SQL Server와 마찬가지로 모든 스키마의 결과를 출력합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델 및 UUIDv7

**영향 가능성: 중간**

`HasUuids` 트레이트가 이제 UUID 스펙의 버전 7(정렬 가능한 UUID)와 호환되는 UUID를 반환합니다. 모델 ID에 기존의 순서가 지정된 UUIDv4 문자열을 계속 사용하려면, 이제 `HasVersion4Uuids` 트레이트를 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 삭제되었습니다. 이전에 이 트레이트를 사용했다면, 이제 동일한 동작을 제공하는 `HasUuids` 트레이트를 사용해야 합니다.

<a name="requests"></a>
### 요청

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 머지

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드가 이제 "도트(.)" 표기법을 사용한 중첩 배열 데이터 병합을 지원합니다. 이전에 이 메서드를 사용하여 도트 표기법의 키가 있는 최상위 배열 키를 생성하는 데 의존했다면, 이 새로운 동작을 고려하여 애플리케이션을 조정해야 할 수 있습니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="validation"></a>
### 유효성 검증

<a name="image-validation"></a>
#### 이미지 유효성 검증 시 더 이상 SVG 포함 안 됨

`image` 유효성 규칙이 이제 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙에서 SVG를 허용하려면 명시적으로 지정해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경사항도 참고하시길 권장합니다. 이 변경사항 중 다수는 필수가 아니지만, 애플리케이션과 동기화해 두면 좋습니다. 일부 변경사항은 이 업그레이드 가이드에 포함되어 있지만, 설정 파일이나 주석 등 기타 변경사항은 포함되지 않았습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)로 변경된 내역을 쉽게 확인하고, 필요한 업데이트만 선택할 수 있습니다.