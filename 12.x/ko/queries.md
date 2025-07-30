# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니언 (Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리적 그룹핑](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 검색(Full Text) Where 절](#full-text-where-clauses)
- [정렬, 그룹핑, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [제한과 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [Update 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 문](#delete-statements)
- [비관적 락(Pessimistic Locking)](#pessimistic-locking)
- [재사용 가능한 쿼리 구성요소](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 유창한 인터페이스로 작성하고 실행할 수 있게 도와줍니다. 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 작동합니다.

쿼리 빌더는 PDO 파라미터 바인딩을 이용해 SQL 인젝션 공격을 방어합니다. 따라서 쿼리 바인딩에 전달되는 문자열을 별도로 정리하거나 필터링할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조하는 컬럼 이름(예: "order by" 컬럼)을 결정하도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드가 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 주어진 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하므로, 추가 조건을 체인으로 연결하고 마지막에 `get` 메서드로 쿼리 결과를 가져올 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 목록으로 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하는데, 이 컬렉션에는 쿼리 결과가 포함되어 있고 각 결과 항목은 PHP의 `stdClass` 객체 인스턴스입니다. 각 컬럼 값을 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터를 매핑하거나 축소하는 데 매우 강력한 다양한 메서드를 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 또는 컬럼 조회하기

데이터베이스에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용하세요. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

일치하는 레코드가 없으면 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용하세요. 예외를 잡지 않으면 404 HTTP 응답이 자동으로 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없고 단일 컬럼 값만 필요하면 `value` 메서드를 사용해 바로 해당 컬럼 값을 추출할 수 있습니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값 리스트를 `Illuminate\Support\Collection`으로 받고 싶다면 `pluck` 메서드를 사용하세요. 예를 들어 사용자 타이틀 목록을 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인수로 키가 될 컬럼명을 지정해 결과 컬렉션의 키를 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기 (Chunking Results)

수천 건 이상의 데이터베이스 레코드를 처리해야 할 때는 `DB` 파사드의 `chunk` 메서드 사용을 고려하세요. 이 메서드는 쿼리 결과를 작은 청크 단위로 나누어 각 청크를 클로저에 전달해 처리합니다. 예를 들어, `users` 테이블 전체를 100개 레코드씩 청크 단위로 처리해 보겠습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

청크 처리를 더 이상 이어가지 않으려면 클로저에서 `false`를 반환하면 됩니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중에 레코드를 업데이트할 경우, 청크 결과가 의도치 않게 바뀔 수 있습니다. 업데이트 작업을 병행할 예정이라면 `chunkById` 메서드 사용을 권장합니다. 이 메서드는 기본 키를 기준으로 자동 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

`chunkById`와 `lazyById` 메서드는 자체적으로 "where" 조건을 추가하기 때문에, 사용자 조건을 클로저로 [논리적으로 그룹핑](#logical-grouping)하는 것이 좋습니다:

```php
DB::table('users')->where(function ($query) {
    $query->where('credits', 1)->orWhere('credits', 2);
})->chunkById(100, function (Collection $users) {
    foreach ($users as $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['credits' => 3]);
    }
});
```

> [!WARNING]
> 청크 콜백 내에서 업데이트나 삭제를 수행할 때, 기본 키나 외래 키가 변경되면 청크 쿼리가 영향을 받아 일부 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [청크 처리](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행합니다. 다만, 각 청크를 클로저에 전달하는 대신, [LazyCollection](/docs/12.x/collections#lazy-collections) 인스턴스를 반환해 결과를 단일 스트림처럼 다룰 수 있게 합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

역시 결과를 반복하면서 업데이트할 계획이라면, 기본 키 기반 자동 페이지네이션을 제공하는 `lazyById` 또는 `lazyByIdDesc` 메서드 사용이 권장됩니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 작업 중에 업데이트 또는 삭제를 수행할 때, 기본 키 또는 외래 키 변경이 쿼리 결과에 영향을 줄 수 있어 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 같은 다양한 집계 함수 메서드를 제공합니다. 쿼리 조건 작성 후 이 메서드들을 호출해 집계 값을 구할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다양한 조건과 결합해서 집계값 산출을 세밀하게 조정할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

`count` 대신 `exists`와 `doesntExist` 메서드를 사용하면 특정 조건에 부합하는 레코드가 존재하는지 쉽게 확인할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정하기

테이블의 모든 컬럼을 선택하지 않고 일부만 선택하고 싶을 때 `select` 메서드를 사용해 커스텀 Select 절을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복 결과를 제거한 고유한 값만 반환할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 선택 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

가끔 임의의 문자열을 쿼리 내에 삽입해야 할 때가 있습니다. 이때 `DB` 파사드의 `raw` 메서드를 사용해 Raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 문은 쿼리에 그대로 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드들

`DB::raw` 대신 쿼리 내 특정 부분에 Raw 표현식을 삽입할 수 있는 여러 메서드를 사용할 수 있습니다. **Raw 표현식을 사용하는 쿼리는 SQL 인젝션 보호가 보장되지 않으므로 주의해야 합니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(...))`를 대신해 쓸 수 있습니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

Raw 조건을 Where 절에 직접 넣을 때 사용합니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

Raw 문자열을 Having 절에 넣을 때 사용됩니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

Raw 문자열을 "order by" 절에 넣을 때 사용합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

Raw 문자열을 `group by` 절에 넣을 때 사용합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 (Inner Join) 절

쿼리 빌더를 이용해 조인 절을 추가할 수 있습니다. 기본 "내부 조인"은 `join` 메서드로 수행하며, 첫 번째 인수는 조인할 테이블명, 나머지 인수는 조인 조건 컬럼을 지정합니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### 좌측 조인 / 우측 조인 절

"왼쪽 조인(left join)" 또는 "오른쪽 조인(right join)"이 필요하다면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 문법은 `join`과 동일합니다:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 (Cross Join) 절

`crossJoin` 메서드를 사용해 두 테이블의 데카르트 곱(Cartesian product)을 생성하는 크로스 조인을 수행할 수 있습니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 조건을 지정하려면 `join` 메서드의 두 번째 인수로 클로저를 전달하세요. 클로저는 `Illuminate\Database\Query\JoinClause` 객체를 받아 조인 조건을 명시할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 컬럼과 값을 비교하는 "where" 조건을 넣으려면 `where` 및 `orWhere` 메서드를 사용할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드로 서브쿼리를 조인할 수 있습니다. 각 메서드는 세 개의 인수를 받으며, 서브쿼리, 별칭, 조건 정의 클로저를 전달합니다. 예를 들어, 각 사용자의 가장 최근 블로그 게시글 생성일을 포함하는 사용자 목록을 조회하는 예시는 다음과 같습니다:

```php
$latestPosts = DB::table('posts')
    ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
    ->where('is_published', true)
    ->groupBy('user_id');

$users = DB::table('users')
    ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
        $join->on('users.id', '=', 'latest_posts.user_id');
    })->get();
```

<a name="lateral-joins"></a>
#### 래터럴 조인 (Lateral Joins)

> [!WARNING]
> 래터럴 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드는 래터럴 조인을 수행합니다. 각 메서드는 두 개의 인수를 받으며, 서브쿼리와 별칭을 지정합니다. 조인 조건은 서브쿼리의 `where` 절 내에서 지정합니다. 래터럴 조인은 각 행마다 평가되며 서브쿼리 외부 컬럼을 참조할 수 있습니다.

예를 들어, 각 사용자와 해당 사용자의 가장 최근 게시글 3개를 가져오는 쿼리는 다음과 같습니다:

```php
$latestPosts = DB::table('posts')
    ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
    ->whereColumn('user_id', 'users.id')
    ->orderBy('created_at', 'desc')
    ->limit(3);

$users = DB::table('users')
    ->joinLateral($latestPosts, 'latest_posts')
    ->get();
```

<a name="unions"></a>
## 유니언 (Unions)

쿼리 빌더는 여러 쿼리를 "union"할 수 있는 메서드를 제공합니다. 예를 들어, 초기 쿼리와 다른 쿼리를 `union`으로 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도 `unionAll` 메서드가 있습니다. `unionAll`은 중복을 제거하지 않고 모든 결과를 포함하며, 메서드 시그니처는 `union`과 같습니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 Where 절을 추가할 수 있습니다. 가장 기본적인 형태는 세 개의 인수를 받으며, 컬럼명, 연산자, 비교 값을 순서대로 지정합니다.

예를 들어, `votes` 컬럼이 100이고 `age` 컬럼이 35보다 큰 사용자를 조회하는 쿼리는 다음과 같습니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의상 특정 컬럼과 `=` 비교 시 연산자를 생략하면 Laravel이 자동으로 가정합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

연관 배열을 전달해 여러 컬럼 조건을 한번에 지정할 수도 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

지원되는 연산자는 데이터베이스가 지원하는 모든 연산자를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>=', 100)
    ->get();

$users = DB::table('users')
    ->where('votes', '<>', 100)
    ->get();

$users = DB::table('users')
    ->where('name', 'like', 'T%')
    ->get();
```

또한 다중 조건을 원할 경우 3개의 인수를 담은 배열을 `where` 메서드에 넘길 수 있습니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조하는 컬럼 이름(예: "order by")으로 사용되지 않도록 해야 합니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교 시 문자열을 자동으로 정수형으로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어 의도치 않은 결과를 초래할 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 경우 `User::where('secret', 0)`을 실행하면 해당 행이 조회됩니다. 이를 피하려면 쿼리 전에 값 타입을 명확히 변환해 주세요.

<a name="or-where-clauses"></a>
### Or Where 절

여러 개의 `where` 메서드를 체인으로 연결하면 기본적으로 `and` 조건으로 연결됩니다. `orWhere` 메서드는 `or` 조건으로 연결할 수 있으며, `where` 메서드와 동일한 인수를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

`orWhere` 안에 그룹핑이 필요할 경우 첫 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Illuminate\Database\Query\Builder; 

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
    })
    ->get();
```

위 쿼리의 결과 SQL:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 막기 위해 `orWhere` 호출은 반드시 적절히 그룹핑해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`과 `orWhereNot` 메서드는 조건 그룹을 부정할 때 사용합니다. 예를 들어, 클리어런스 제품이 아니거나 가격이 10 미만인 제품을 제외하는 쿼리는 다음과 같습니다:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
    })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### Where Any / All / None 절

여러 컬럼 조건을 하나로 묶어 적용하고 싶을 때 다음 메서드를 사용할 수 있습니다.

예를 들어, 컬럼 목록 중 어느 하나라도 특정 값과 `LIKE` 일치하는 레코드를 조회하려면 `whereAny` 사용:

```php
$users = DB::table('users')
    ->where('active', true)
    ->whereAny([
        'name',
        'email',
        'phone',
    ], 'like', 'Example%')
    ->get();
```

생성되는 SQL:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

반대로 모든 컬럼에 조건이 맞는 경우 `whereAll` 사용:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

SQL 결과:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

모든 컬럼이 조건에 맞지 않는 경우는 `whereNone` 사용:

```php
$posts = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

실행되는 SQL:

```sql
SELECT *
FROM albums
WHERE published = true AND NOT (
    title LIKE '%explicit%' OR
    lyrics LIKE '%explicit%' OR
    tags LIKE '%explicit%'
)
```

<a name="json-where-clauses"></a>
### JSON Where 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼을 쿼리할 수 있습니다. `->` 연산자를 이용해 JSON 속성에 접근하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열에 포함 여부 조건은 `whereJsonContains`와 `whereJsonDoesntContain` 메서드를 사용합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL 사용 시 다중 값 배열도 전달 가능합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

특정 JSON 키 존재 조건은 `whereJsonContainsKey` / `whereJsonDoesntContainKey` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

JSON 배열 길이 조건은 `whereJsonLength`를 사용합니다:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가 Where 절

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드로 패턴 매칭용 "LIKE" 절을 추가할 수 있습니다. 데이터베이스 독립적으로 문자열 검색을 지원하며 기본은 대소문자 구분 없이 처리합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수로 대소문자 구분 검색을 활성화할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`를 이용해 "or" 조건을 추가할 수도 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`로 "NOT LIKE" 절을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

`orWhereNotLike`는 "or NOT LIKE" 절을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 옵션은 현재 SQL Server에서 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 특정 컬럼 값이 지정한 배열에 포함되어 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 포함되어 있지 않은 경우를 조회합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

서브쿼리를 전달할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

결과 SQL:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대량의 정수 바인딩 배열을 사용할 때는 메모리 관리를 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하는 것이 좋습니다.

**whereBetween / orWhereBetween**

컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

컬럼 값이 두 값 범위 밖인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

한 행의 두 컬럼 값 사이에 컬럼 값이 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

범위 밖인지 확인하려면 `whereNotBetweenColumns` 사용:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

특정 값이 동일한 타입 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

값이 범위 밖인지 확인하려면 `whereValueNotBetween` 사용:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

컬럼 값이 `NULL`인지 체크:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`NOT NULL`인 경우:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜, 월, 일, 연도, 시간 등 특정 부분을 기준으로 비교할 때 사용합니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();

$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();

$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();

$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();

$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

날짜가 과거, 미래, 오늘인지, 오늘보다 이전 또는 이후인지 확인할 때 사용:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();
```

포함 조건:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

두 컬럼이 동일한지 비교합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

연산자도 지정 가능:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

복수 조건도 배열로 지정할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])
    ->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑

여러 Where 절을 괄호로 묶어 논리 연산을 명확히 해야 할 때가 있습니다. 특히 `orWhere`는 반드시 그룹핑해야 예상치 못한 쿼리 동작이 발생하지 않습니다. `where` 메서드에 클로저를 전달하면 그룹핑이 시작됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 쿼리의 SQL:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> `orWhere`는 항상 그룹핑해서 글로벌 스코프 적용 시 문제를 방지하세요.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 SQL의 "where exists" 절을 작성할 때 사용합니다. 인수로 클로저나 쿼리 객체를 전달할 수 있으며, 서브쿼리를 정의합니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

대신 다음처럼 쿼리 객체를 직접 전달할 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 경우 모두 다음과 같은 SQL이 생성됩니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 절

서브쿼리 결과와 비교하는 Where 절 작성 시, 클로저와 비교값을 넘기거나 컬럼, 연산자, 클로저를 넘겨 작성할 수 있습니다.

예를 들어, 최근에 특정 타입의 멤버십을 가진 사용자를 조회하려면:

```php
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

또는 서브쿼리 결과와 컬럼을 비교:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색(Full Text) Where 절

> [!WARNING]
> 전문 검색 Where 절은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드는 전문 검색 인덱스가 적용된 컬럼에 대해 전문 검색 조건을 추가합니다. Laravel은 내부 데이터베이스에 맞는 SQL을 생성합니다. 예를 들어 `MATCH AGAINST` 구문이 생성됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹핑, 제한 및 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 컬럼을 기준으로 결과를 정렬합니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

복수 컬럼 정렬 시 `orderBy`를 여러 번 호출하세요:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본적으로 오름차순이며, 내림차순으로 하려면 두 번째 인수를 지정하거나 `orderByDesc`를 사용하세요:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

JSON 컬럼 내 값을 기준으로 정렬하려면 `->` 연산자를 사용할 수 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

날짜 컬럼으로 정렬할 때 편리하게 사용합니다. 기본은 `created_at` 컬럼입니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

정렬할 컬럼을 지정할 수도 있습니다.

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거하기

`reorder` 메서드는 기존 모든 "order by" 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

또한 새로운 컬럼과 방향을 지정해 재정렬할 수도 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

간단히 내림차순 정렬은 `reorderDesc` 메서드를 사용하세요:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹핑 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

결과를 그룹핑할 때 `groupBy`와 `having` 메서드를 사용합니다. `having`은 `where`와 유사하게 조건을 지정합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드로 범위 조건도 가능합니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

복수 컬럼을 그룹핑하려면 여러 인수를 전달하세요:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 Having 조건은 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 제한과 오프셋 (Limit and Offset)

`limit`과 `offset` 메서드로 결과 개수를 제한하거나 특정 개수만큼 건너뛸 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

조건에 따라 Where 절 등 쿼리 조건을 동적으로 적용하려면 `when` 메서드를 사용하세요. 예를 들어, 특정 입력값이 있을 때만 조건을 추가하는 경우:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when`의 첫 번째 인수가 `true`일 때만 클로저가 실행됩니다.

세 번째 인수로 클로저를 넘기면 첫 번째 인수가 `false`일 때 실행되는 대체 작업을 지정할 수 있습니다:

```php
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
    ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
        $query->orderBy('votes');
    }, function (Builder $query) {
        $query->orderBy('name');
    })
    ->get();
```

<a name="insert-statements"></a>
## Insert 문 (Insert Statements)

쿼리 빌더의 `insert` 메서드는 데이터베이스 테이블에 레코드를 삽입합니다. 배열로 컬럼과 값을 넘겨줍니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

배열 안에 배열을 넣으면 여러 레코드를 한번에 삽입합니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 시 오류를 무시합니다. 중복 레코드 에러 뿐 아니라 DB 엔진에 따라 다른 오류도 무시될 수 있으니 주의하세요. 예를 들어 MySQL에서는 [엄격 모드 무시](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution) 효과가 있습니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리 결과를 이용해 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블이 자동 증가하는 `id`가 있다면, `insertGetId` 메서드로 삽입과 동시에 새 ID를 받을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서 `insertGetId`는 기본적으로 자동 증가 컬럼명이 `id`라고 가정합니다. 다른 시퀀스에서 ID를 얻으려면 두 번째 인수로 컬럼명을 지정하세요.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드를 삽입하고, 이미 존재하는 레코드는 지정한 컬럼 기준으로 업데이트합니다. 첫 번째 인수는 삽입 또는 업데이트할 값 목록, 두 번째 인수는 고유 식별에 사용할 컬럼, 세 번째 인수는 업데이트할 컬럼들입니다:

```php
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

위 예시는 `departure`와 `destination` 컬럼 값이 같은 레코드가 있으면 `price`만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 두 번째 인수로 지정한 컬럼에 "primary" 또는 "unique" 인덱스가 존재해야 합니다. MariaDB 및 MySQL 드라이버는 두 번째 인수를 무시하고 테이블의 "primary"와 "unique" 인덱스만 사용합니다.

<a name="update-statements"></a>
## Update 문 (Update Statements)

쿼리 빌더는 `update` 메서드로 기존 레코드를 수정할 수 있습니다. `update`도 `insert`처럼 컬럼과 값을 쌍으로 받으며, 영향을 받은 행 수를 반환합니다. `where` 조건과 함께 사용할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update or Insert

기존 레코드가 있으면 수정하고, 없으면 새로 삽입하는 경우 `updateOrInsert` 메서드를 사용합니다. 첫 번째 인수는 검색조건, 두 번째 인수는 업데이트할 컬럼-값 쌍입니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

존재 여부에 따라 업데이트할 속성을 동적으로 정의하려면 클로저를 인수로 넘길 수도 있습니다:

```php
DB::table('users')->updateOrInsert(
    ['user_id' => $user_id],
    fn ($exists) => $exists ? [
        'name' => $data['name'],
        'email' => $data['email'],
    ] : [
        'name' => $data['name'],
        'email' => $data['email'],
        'marketable' => true,
    ],
);
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼 내 특정 키를 수정할 때는 `->` 구문을 사용합니다. MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

특정 컬럼 값을 증가 또는 감소시키는 편리한 메서드를 제공합니다. 첫 번째 인수는 컬럼, 두 번째 인수(선택적)는 증가/감소 값입니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증감 중 추가 컬럼 업데이트도 가능:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

복수 컬럼을 한번에 증가/감소하려면 `incrementEach`와 `decrementEach` 메서드를 사용하세요:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 문 (Delete Statements)

`delete` 메서드로 테이블에서 레코드를 삭제할 수 있으며 삭제한 행 수를 반환합니다. 삭제할 때도 `where` 조건을 걸 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 락(Pessimistic Locking)

쿼리 빌더는 `select` 문 실행 시 비관적 락을 지원하는 메서드를 포함합니다. `sharedLock`은 행을 공유 락 상태로 가져와 트랜잭션 완료 전까지 수정 못 하도록 합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

`lockForUpdate`는 행을 배타 락 상태로 잠궈 다른 공유 락이 불가하게 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 락은 [트랜잭션](/docs/12.x/database#database-transactions) 내에서 처리하는 걸 권장합니다. 실패 시 변경을 롤백하고 락도 해제합니다:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate()
        ->find(2);

    if ($sender->balance < 100) {
        throw new RuntimeException('Balance too low.');
    }

    DB::table('users')
        ->where('id', $sender->id)
        ->update([
            'balance' => $sender->balance - 100
        ]);

    DB::table('users')
        ->where('id', $receiver->id)
        ->update([
            'balance' => $receiver->balance + 100
        ]);
});
```

<a name="reusable-query-components"></a>
## 재사용 가능한 쿼리 구성요소 (Reusable Query Components)

애플리케이션에 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap`과 `pipe` 메서드를 사용해 재사용 가능한 객체로 추출할 수 있습니다. 예를 들어 다음과 같이 목적지가 필요할 때 쿼리가 두 군데 있다면:

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->orderByDesc('price')
    ->get();

// ...

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

공통된 목적지 필터링을 객체로 추출할 수 있습니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Query\Builder;

class DestinationFilter
{
    public function __construct(
        private ?string $destination,
    ) {
        //
    }

    public function __invoke(Builder $query): void
    {
        $query->when($this->destination, function (Builder $query) {
            $query->where('destination', $this->destination);
        });
    }
}
```

`tap` 메서드로 쿼리에 적용할 수 있습니다:

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### 쿼리 파이프 (Query Pipes)

`tap`은 쿼리 빌더를 반환하지만, 다른 값을 반환하는 객체 실행을 원한다면 `pipe` 메서드를 사용하세요.

예를 들어, 애플리케이션 전반에 사용하는 공유 [페이지네이션](/docs/12.x/pagination) 로직을 가진 객체가 있다면:

```php
<?php

namespace App\Scopes;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Query\Builder;

class Paginate
{
    public function __construct(
        private string $sortBy = 'timestamp',
        private string $sortDirection = 'desc',
        private int $perPage = 25,
    ) {
        //
    }

    public function __invoke(Builder $query): LengthAwarePaginator
    {
        return $query->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage, pageName: 'p');
    }
}
```

`pipe` 메서드를 이용해 쿼리 객체로 활용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리 작성 중 `dd`와 `dump` 메서드로 현재 쿼리 바인딩과 SQL을 출력할 수 있습니다. `dd`는 출력 후 실행을 멈추고, `dump`는 계속 진행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드는 바인딩 값이 모두 치환된 SQL문을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```