# 업그레이드 가이드 (Upgrade Guide)

- [11.x에서 12.0으로 업그레이드하기](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 주요 영향 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 설치 프로그램 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 낮은 영향 변경 사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해결](#container-class-dependency-resolution)
- [이미지 검증에서 SVG 제외](#image-validation)
- [멀티 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 소요 시간: 5분

> [!NOTE]
> 가능한 모든 주의해야 할 변경 사항을 문서화하려 노력했지만, 프레임워크의 일부 덜 알려진 부분의 변경 사항은 실제로 애플리케이션에 영향을 미치지 않을 수도 있습니다. 시간을 절약하고 싶다면, [Laravel Shift](https://laravelshift.com/)를 사용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성들을 업데이트하세요:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`를 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

[Carbon 2.x](https://carbon.nesbot.com/docs/) 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)를 요구합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 설치 프로그램 업데이트 (Updating the Laravel Installer)

Laravel 설치 CLI 도구를 사용해 새 Laravel 애플리케이션을 생성한다면, Laravel 12.x 및 [새 Laravel 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 설치 프로그램을 업데이트해야 합니다. `composer global require`로 설치했다면 다음 명령어로 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

만약 `php.new`를 통해 PHP와 Laravel을 설치했다면, 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 Laravel 설치 프로그램을 설치하세요:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자로 실행...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는 [Laravel Herd](https://herd.laravel.com)의 번들 버전 Laravel 설치 프로그램을 사용하는 경우 Herd 설치를 최신 버전으로 업데이트하세요.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑 (Concurrency Result Index Mapping)

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열(associative array)로 호출할 경우, 동시 작업 결과가 각 키와 연결되어 반환됩니다:

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

의존성 주입 컨테이너가 이제 클래스 인스턴스를 해석할 때 클래스 속성의 기본값을 존중합니다. 이전에는 컨테이너가 기본값 없이 인스턴스를 해결했을 경우, 이 새로운 동작을 고려해 애플리케이션을 수정해야 할 수 있습니다:

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
#### 멀티 스키마 데이터베이스 검사 (Multi-Schema Database Inspecting)

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드가 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마만 결과를 얻고 싶다면 `schema` 인수를 전달할 수 있습니다:

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$table = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 모든 테이블...
$table = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 지정된 테이블 이름을 반환합니다. 필요에 따라 `schemaQualified` 인수를 전달해 동작을 변경할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$table = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$table = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table`과 `db:show` 명령어는 이제 PostgreSQL과 SQL Server처럼 MySQL, MariaDB, SQLite에서 모든 스키마의 결과를 출력합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7 (Models and UUIDv7)

**영향 가능성: 중간**

`HasUuids` 트레이트가 UUID 사양 버전 7(순차적 UUID)과 호환되는 UUID를 반환하도록 변경되었습니다. 모델의 ID로 계속해서 순차 UUIDv4 문자열을 사용하려면 이제 `HasVersion4Uuids` 트레이트를 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레이트는 제거되었습니다. 이전에 이 트레이트를 사용했다면, 동일한 동작을 제공하는 `HasUuids` 트레이트를 대신 사용하세요.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합 (Nested Array Request Merging)

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드가 이제 "dot" 표기법을 사용한 중첩 배열 데이터 병합을 지원합니다. 이 메서드를 사용해 "dot" 표기법 상태의 키를 포함하는 최상위 배열 키를 생성하는 데 의존하던 경우, 이 새로운 동작에 맞게 애플리케이션을 수정해야 할 수 있습니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### 이미지 검증에서 SVG 제외 (Image Validation Now Excludes SVGs)

`image` 유효성 검증 규칙이 이제 기본적으로 SVG 이미지를 허용하지 않습니다. SVG를 허용하려면 명시적으로 허용해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)에서 변경 사항도 확인할 것을 권장합니다. 많은 변경 사항들이 필수는 아니지만, 애플리케이션과 동기화하는 것이 좋을 수 있습니다. 이 업그레이드 가이드에서 다루는 내용도 있지만, 구성 파일이나 주석 변경과 같은 일부 변경 사항은 포함되어 있지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 변경 사항을 쉽게 확인하고 필요한 부분만 선택해 업데이트할 수 있습니다.