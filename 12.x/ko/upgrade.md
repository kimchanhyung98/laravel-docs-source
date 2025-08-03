# 업그레이드 가이드 (Upgrade Guide)

- [11.x 버전에서 12.0 버전으로 업그레이드하기](#upgrade-12.0)

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
- [이미지 유효성 검사 시 SVG 제외](#image-validation)
- [로컬 파일 시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x 버전에서 12.0 버전으로 업그레이드하기 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 모든 가능한 깨지는 변경(Breaking Change)을 문서화하기 위해 노력했습니다. 그중 일부는 프레임워크의 잘 알려지지 않은 부분에 존재해 실제 애플리케이션에 영향을 미치는 것은 일부에 불과할 수 있습니다. 시간을 절약하고 싶다면 [Laravel Shift](https://laravelshift.com/)를 사용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`를 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

[Carbon 2.x](https://carbon.nesbot.com/docs/)에 대한 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)를 요구합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 설치 프로그램 업데이트 (Updating the Laravel Installer)

새로운 Laravel 애플리케이션을 만들 때 Laravel 설치 프로그램 CLI 도구를 사용한다면, Laravel 12.x 및 [새로운 Laravel 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 설치 프로그램을 업데이트해야 합니다. 만약 `composer global require` 명령어로 Laravel 설치 프로그램을 설치했다면, 다음 명령어로 설치 프로그램을 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

만약 PHP와 Laravel을 `php.new`로 설치했다면, 운영 체제에 맞게 `php.new` 설치 명령어를 다시 실행해 최신 PHP 버전과 Laravel 설치 프로그램을 설치할 수 있습니다:

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

또는 [Laravel Herd](https://herd.laravel.com) 번들 내의 Laravel 설치 프로그램을 사용 중이라면, Herd 설치를 최신 릴리스로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### 변경된 `DatabaseTokenRepository` 생성자 시그니처

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자는 이제 `$expires` 인수를 분(minute)이 아닌 초(second) 단위로 받습니다.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드 호출 시 연관 배열(associative array)을 인수로 넘기면, 동시 작업의 결과가 해당 키와 함께 반환됩니다:

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
#### 컨테이너 클래스 의존성 해결

**영향 가능성: 낮음**

의존성 주입 컨테이너는 이제 클래스 인스턴스를 해석할 때 클래스 속성의 기본값을 존중합니다. 이전에 컨테이너가 기본값 없이 인스턴스를 해결하는 데 의존했다면, 이 새로운 동작에 맞게 애플리케이션을 조정해야 할 수 있습니다:

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
#### 다중 스키마 데이터베이스 검사

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함해 반환합니다. 특정 스키마의 결과만 받고 싶으면 `schema` 인수를 전달하면 됩니다:

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 지정된 테이블 이름을 반환합니다. `schemaQualified` 인수로 동작을 변경할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어도 MySQL, MariaDB, SQLite에서 PostgreSQL 및 SQL Server처럼 모든 스키마의 결과를 출력합니다.

<a name="updated-blueprint-constructor-signature"></a>
#### 변경된 `Blueprint` 생성자 시그니처

**영향 가능성: 매우 낮음**

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Illuminate\Database\Connection` 인스턴스를 기대합니다.

<a name="eloquent"></a>
### 엘로퀀트 (Eloquent)

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

`HasUuids` 트레이트는 이제 UUID 사양 버전 7(정렬된 UUID)과 호환되는 UUID를 반환합니다. 모델 ID로 여전히 정렬된 UUIDv4 문자열을 사용하려면, 이제 `HasVersion4Uuids` 트레이트를 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

기존에 사용하던 `HasVersion7Uuids` 트레이트는 제거되었습니다. 만약 이 트레이트를 사용 중이었다면, 동일한 동작을 하는 `HasUuids` 트레이트를 대신 사용해야 합니다.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용해 중첩 배열 데이터를 병합할 수 있습니다. 만약 이 메서드가 "dot" 표기법 키를 최상위 배열 키로 만드는 데 의존했다면, 이 새로운 동작에 맞게 애플리케이션을 조정해야 할 수 있습니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="storage"></a>
### 스토리지 (Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일 시스템 디스크 기본 루트 경로

**영향 가능성: 낮음**

애플리케이션에서 파일 시스템 설정에 `local` 디스크를 명시적으로 정의하지 않으면, Laravel은 이제 로컬 디스크의 루트를 이전의 `storage/app` 대신 `storage/app/private`로 기본 설정합니다. 따라서 `Storage::disk('local')` 호출은 별도 설정이 없으면 `storage/app/private`에서 읽고 쓰기를 수행합니다. 이전 동작을 복원하려면, `local` 디스크를 직접 설정하고 원하는 루트 경로를 지정할 수 있습니다.

<a name="validation"></a>
### 유효성 검사 (Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검사에서 SVG 제외

**영향 가능성: 낮음**

`image` 유효성 검사 규칙은 기본적으로 더 이상 SVG 이미지를 허용하지 않습니다. `image` 규칙으로 SVG를 허용하려면 명시적으로 허용해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 참고할 것을 권장합니다. 많은 변경 사항이 필수는 아니지만, 애플리케이션과의 동기화를 위해 이러한 파일들을 검토할 수 있습니다. 이 업그레이드 가이드에서 일부 변경 사항은 다루지만, 구성 파일이나 주석 변경과 같은 다른 변경 사항은 다루지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용해 변경 사항을 쉽게 확인하고 중요한 업데이트만 선택할 수 있습니다.