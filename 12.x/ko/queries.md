# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 게으르게 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Joins)](#joins)
- [유니언(Unions)](#unions)
- [기본 WHERE 구문](#basic-where-clauses)
    - [WHERE 구문](#where-clauses)
    - [OR WHERE 구문](#or-where-clauses)
    - [WHERE NOT 구문](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 구문](#where-any-all-none-clauses)
    - [JSON WHERE 구문](#json-where-clauses)
    - [추가 WHERE 구문](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 WHERE 구문](#advanced-where-clauses)
    - [WHERE EXISTS 구문](#where-exists-clauses)
    - [서브쿼리 WHERE 구문](#subquery-where-clauses)
    - [전체 텍스트 WHERE 구문](#full-text-where-clauses)
    - [벡터 유사도(VECTOR SIMILARITY) 구문](#vector-similarity-clauses)
- [정렬, 그룹화, LIMIT, OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬하기](#ordering)
    - [그룹화하기](#grouping)
    - [LIMIT 및 OFFSET](#limit-and-offset)
- [조건부 절(Conditional Clauses)](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [UPSERT](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [INCREMENT 및 DECREMENT](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행할 수 있도록 편리하고 유연한 인터페이스를 제공합니다. 애플리케이션에서 대부분의 데이터베이스 작업을 처리할 수 있으며, Laravel에서 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩(PHP Data Object의 바인딩)을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 빌더에 전달하는 문자열에 대해 별도로 정제(clean)하거나 필터링(sanitize)할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력값이 쿼리에서 참조하는 컬럼명을 직접 결정하도록 해서는 절대 안 되며, "order by" 컬럼도 마찬가지입니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

쿼리를 시작하려면 `DB` 파사드(Facade)에서 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대해 플루언트 쿼리 빌더 인스턴스를 반환하며, 다양한 제약 조건을 체이닝(연결)하고 최종적으로 `get` 메서드로 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리의 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각각의 결과는 PHP의 `stdClass` 객체입니다. 각 컬럼의 값은 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑(mapping) 및 리듀싱(reducing)에 매우 강력한 메서드를 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 또는 컬럼 조회하기

데이터베이스 테이블에서 하나의 행만 조회해야 한다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 조회 조건에 맞는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 처리되지 않으면 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고, 특정 컬럼 값만 추출하려면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 해당 컬럼의 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하고 싶다면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 리스트 조회하기

특정 컬럼의 값들만 모아서 `Illuminate\Support\Collection` 형태로 가져오고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 아래 예시에서는 사용자 타이틀을 컬렉션으로 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 결과 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기 (Chunking Results)

수천 건에 달하는 데이터베이스 레코드를 다뤄야 한다면 `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 한 번에 작은 청크 단위로 조회하며, 각 청크를 클로저(익명 함수)에 전달하여 처리할 수 있습니다. 예를 들어, `users` 테이블의 전체 데이터를 100개씩 청크로 나누어 처리할 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가 청크 처리도 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 단위로 결과를 조회하는 중에 레코드를 업데이트하는 경우, 결과가 예상치 못한 방식으로 변할 수 있습니다. 청크 중에 데이터를 업데이트할 계획이라면 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 기본 키(Primary Key) 기준으로 자동으로 페이지네이션 처리하여 청크를 만듭니다:

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

`chunkById` 및 `lazyById` 메서드는 쿼리 실행 시 자체적으로 "where" 조건을 추가하므로, 직접 조건을 추가하고 싶을 때는 반드시 클로저 내에서 [논리 그룹화](#logical-grouping)를 사용하는 것이 좋습니다:

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
> 청크 콜백 내부에서 레코드의 기본 키나 외래 키를 변경하면서 업데이트 또는 삭제할 경우, 청크 쿼리에 영향이 있으므로 일부 레코드가 청크 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 게으르게 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백에 전달하는 대신 하나의 [LazyCollection](/docs/12.x/collections#lazy-collections)으로 반환합니다. 이를 통해 전체 결과를 스트림처럼 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

조회한 레코드를 순회(iterate)하면서 업데이트할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이 역시 기본 키를 기준으로 결과를 자동 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복문 안에서 레코드의 기본 키 또는 외래 키를 변경하여 업데이트/삭제하면 청크 쿼리에 영향이 있으므로, 일부 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더에는 `count`, `max`, `min`, `avg`, `sum` 등과 같은 다양한 집계 함수 메서드가 제공됩니다. 쿼리 생성 후 해당 메서드를 호출하여 집계 값을 구할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론 집계 함수와 다른 구문을 조합하여 집계 값을 세밀하게 조정할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리 결과가 존재하는지 단순히 확인하려면 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT 구문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### SELECT 구문 지정하기

항상 테이블의 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용하면 원하는 "select" 구문을 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복된 결과 없이 고유한 레코드만 반환하도록 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 select 구문에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 이때는 `DB` 파사드의 `raw` 메서드를 사용하여 Raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 그대로 문자열로 쿼리문에 삽입되므로 SQL 인젝션 취약점이 발생하지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 관련 메서드

`DB::raw` 대신, 쿼리의 다양한 위치에 Raw 표현식을 삽입할 수 있는 여러 메서드도 제공됩니다. **Raw 표현식을 사용하는 쿼리는 SQL 인젝션으로부터 완전히 보호되지 않는다는 점을 반드시 유념하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있으며, 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 와 `orWhereRaw`는 쿼리에 Raw 형태의 WHERE 절을 삽입할 때 사용할 수 있습니다. 이들 역시 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 와 `orHavingRaw`는 HAVING 절에 Raw 문자열을 값으로 지정할 때 사용할 수 있으며, 바인딩 배열도 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw`는 ORDER BY 절에 Raw 문자열을 사용할 때 유용합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw`는 GROUP BY 절에 Raw 문자열을 제공할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Joins) (Joins)

<a name="inner-join-clause"></a>
#### INNER JOIN 구문

쿼리 빌더에서는 조인 구문을 추가할 수 있습니다. 기본적인 "inner join"을 수행하려면 `join` 메서드를 사용합니다. 첫 번째 인수에는 조인할 테이블명을, 나머지 인수에는 조인을 위한 컬럼 조건을 지정합니다. 하나의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

```php
use Illuminate\Support\Facades.DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### LEFT JOIN / RIGHT JOIN 구문

"inner join" 대신 "left join" 혹은 "right join"을 하고 싶다면 `leftJoin`이나 `rightJoin` 메서드를 사용하면 됩니다. 이 메서드들도 `join`과 동일한 시그니처를 가집니다:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### CROSS JOIN 구문

"cross join"을 수행하려면 `crossJoin` 메서드를 사용할 수 있습니다. Cross join은 첫 번째 테이블과 조인하는 테이블의 데카르트 곱(Cartesian product)을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인(Advanced Join) 구문

더 복잡한 조인 구문도 지정할 수 있습니다. `join` 메서드의 두 번째 인수로 클로저를 전달하면, 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 조인 절의 다양한 제약 조건을 적용할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 절이 필요하다면, `JoinClause` 인스턴스의 `where`, `orWhere` 메서드를 사용하면 됩니다. 이때 두 컬럼이 아니라, 컬럼과 값을 비교합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 활용해 쿼리와 서브쿼리를 조인할 수 있습니다. 각 메서드는 세 개의 인수를 받으며, 순서대로 서브쿼리, 테이블 별칭, 관련 컬럼을 정의하는 클로저입니다. 아래 예시는 각 사용자별로 최근 게시글의 `created_at` 값을 함께 조회합니다:

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
#### Lateral 조인

> [!WARNING]
> Lateral 조인은 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 이용해 서브쿼리와 "lateral join"을 할 수 있습니다. 두 메서드는 서브쿼리와 별칭 두 개의 인수를 받으며, 조인 조건은 서브쿼리 내 `where` 절에서 지정해야 합니다. Lateral 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

아래 예시는 각 사용자별로 최근 3개의 게시글을 함께 조회합니다. 서브쿼리 내에서 `whereColumn`을 이용해 조인 조건을 걸 수 있습니다:

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
## 유니언(Unions) (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "union"으로 결합할 수 있는 편리한 메서드도 제공합니다. 우선 하나의 쿼리를 만들고, `union` 메서드로 추가 쿼리를 결합할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```

`union` 외에, 결과 중복을 제거하지 않는 `unionAll` 메서드도 있습니다. `unionAll` 메서드는 `union`과 동일한 시그니처를 가집니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 구문 (Basic Where Clauses)

<a name="where-clauses"></a>
### WHERE 구문

쿼리 빌더의 `where` 메서드를 사용해서 쿼리에 "WHERE" 구문을 추가할 수 있습니다. 가장 기본적인 `where` 호출은 세 개의 인수를 받습니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 모든 연산자 사용 가능), 세 번째는 컬럼값과 비교할 값입니다.

아래 쿼리는 `votes`가 100이고 `age`가 35보다 큰 사용자를 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의를 위해, 컬럼값이 `=` 인지 확인할 경우에는 두 번째 인수만 생략하고 값을 바로 전달할 수 있습니다. Laravel은 자동으로 `=` 연산자를 사용합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 컬럼을 빠르게 조건으로 추가하고 싶으면, 연관 배열을 `where`에 전달하세요:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

앞서 설명한 대로, 데이터베이스에서 지원하는 모든 연산자를 사용할 수 있습니다:

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

여러 개의 조건을 배열 형태로 전달할 수도 있습니다. 각 조건은 세 개의 인자를 갖는 배열로 전달합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자 입력으로 쿼리에서 참조할 컬럼명을 결정하는 방식(특히 "order by" 컬럼 지정)은 절대 금지해야 합니다.

> [!WARNING]
> MySQL 및 MariaDB는 문자열-숫자 비교 시 문자열을 자동으로 정수로 변환합니다. 이 과정에서 비숫자 문자열은 `0`으로 변환되므로, 예기치 않은 결과가 발생할 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 경우 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이를 방지하려면 쿼리값을 미리 타입캐스팅하세요.

<a name="or-where-clauses"></a>
### OR WHERE 구문

`where` 메서드는 체이닝 시 기본적으로 AND 연산자로 결합됩니다. 그러나 `orWhere` 메서드를 사용하면 OR 연산자를 사용할 수 있습니다. `orWhere`는 `where`와 동일한 인수를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호(())로 묶어 조건을 그룹화해야 할 때는, `orWhere` 첫 번째 인수에 클로저를 넘기면 됩니다:

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

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 스코프가 적용되는 경우 예기치 않은 결과를 피하려면 항상 `orWhere` 호출을 그룹화해야 합니다.

<a name="where-not-clauses"></a>
### WHERE NOT 구문

`whereNot`와 `orWhereNot` 메서드는 쿼리에서 제약 조건 그룹을 반전(부정)할 때 사용합니다. 아래 예시는 클리어런스 상품이거나 가격이 10보다 작은 상품을 제외합니다:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### WHERE ANY / ALL / NONE 구문

동일한 제약 조건을 여러 컬럼에 한꺼번에 적용해야 할 때가 있습니다. 예를 들어, 특정 값으로 LIKE 검색할 때, 여러 컬럼 중 하나라도 일치하는 레코드를 조회하려면 `whereAny` 메서드를 사용할 수 있습니다:

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

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

`whereAll` 메서드는 모든 컬럼이 주어진 제약 조건을 만족하는 레코드를 조회합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 제약 조건에 아무 컬럼도 만족하지 않는 레코드를 조회합니다:

```php
$albums = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

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
### JSON WHERE 구문

Laravel은 JSON 컬럼 타입을 제공하는 데이터베이스(현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼을 쉽게 쿼리할 수 있습니다. JSON 컬럼 조회에는 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열을 쿼리하려면 `whereJsonContains`, `whereJsonDoesntContain` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL에서는 값 배열을 `whereJsonContains`, `whereJsonDoesntContain` 두 번째 인수로 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

JSON 키의 존재 여부만 판별하려면 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey`를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이(요소 개수)로 조건을 만들고 싶다면 `whereJsonLength`를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가 WHERE 구문

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

패턴 매칭을 위한 "LIKE" 조건은 `whereLike` 메서드로 간편하게 추가할 수 있습니다. 이 메서드는 데이터베이스에 독립적인(agnostic) 문자열 패턴 검색을 지원하며, 기본적으로 대소문자 구분 없이(케이스 인식 비활성) 동작합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 통해 대소문자 구분 검색을 활성화할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`는 LIKE 조건을 OR 연산자로 추가할 때 사용합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 조건을 추가하고, `orWhereNotLike`는 OR NOT LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> SQL Server에서는 `whereLike`의 대소문자 구분 옵션이 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 지정한 배열 내에 컬럼값이 포함되어 있음을 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼값이 배열에 포함되어 있지 않음을 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 두 번째 인수로 쿼리 빌더를 전달할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대량의 정수 배열을 바인딩할 경우 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼값이 두 값 사이에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼값이 두 값 밖에 위치하는지를 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 한 컬럼이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 하나의 값이 두 컬럼의 값 범위 밖에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 특정 값이 행 내 두 컬럼 값 사이에 있는지 확인합니다:

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 해당 값이 컬럼 값 범위 밖에 있는지 확인합니다:

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼값이 `NULL`인지를 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼값이 `NULL`이 아닌지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜나 시간에 대한 비교가 필요할 때 각각 `whereDate`, `whereMonth`, `whereDay`, `whereYear`, `whereTime` 메서드를 사용할 수 있습니다:

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

`wherePast`와 `whereFuture`는 컬럼값이 과거 또는 미래인지 판별합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture`는 현재 날짜와 시간도 포함하여 비교합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 오늘, 오늘 이전, 오늘 이후를 비교합니다:

```php
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

`whereTodayOrBefore`, `whereTodayOrAfter`는 오늘을 포함하여 이전/이후를 비교합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼의 값이 같은지 확인합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 추가할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 쌍을 배열로 전달하여 and 조건으로 결합할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화 (Logical Grouping)

여러 "where" 절을 소괄호로 묶어 논리적으로 그룹화할 필요가 있습니다. 특히 `orWhere` 연산을 사용할 때는 반드시 그룹화해야 예기치 않은 쿼리 결과를 방지할 수 있습니다. 클로저를 `where` 메서드에 전달하면 그룹이 생깁니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 예시처럼 클로저에 쿼리 빌더 인스턴스가 전달되며, 소괄호로 그룹화된 제약 조건들을 설정할 수 있습니다. 위 쿼리는 다음 SQL을 만듭니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프 등이 적용될 때 예기치 않은 쿼리 결과를 방지하기 위해 항상 `orWhere`를 그룹화하는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 WHERE 구문 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### WHERE EXISTS 구문

`whereExists` 메서드는 "where exists" SQL 절을 작성할 때 사용할 수 있습니다. 이 메서드에 클로저를 전달하면 쿼리 빌더 인스턴스가 인수로 전달되며, 이 쿼리가 "exists" 절에 들어갑니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 오브젝트를 바로 전달할 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 WHERE 구문

때로는 "where" 절과 값 비교에 서브쿼리 결과를 사용해야 할 때가 있습니다. 이 경우 클로저와 값을 `where`에 전달하면 됩니다. 아래 예시는 특정 타입의 최근 "membership"을 가진 모든 사용자를 조회합니다:

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

또한, 컬럼과 서브쿼리 결과를 비교하는 WHERE 절을 작성하려면, 컬럼명, 연산자, 클로저를 차례대로 넘기면 됩니다. 아래 예시는 수입이 평균보다 작은 모든 레코드를 조회합니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전체 텍스트 WHERE 구문

> [!WARNING]
> 전체 텍스트 WHERE 구문은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드로 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)를 가진 컬럼에 대해 전체 텍스트 "WHERE" 절을 쉽게 추가할 수 있습니다. 각각의 데이터베이스에 맞게 쿼리가 자동 변환되며, MariaDB나 MySQL의 경우 `MATCH AGAINST` 구문이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### 벡터 유사도 구문 (Vector Similarity Clauses)

> [!NOTE]
> 벡터 유사도 WHERE 구문은 현재 PostgreSQL의 `pgvector` 확장에서만 지원됩니다. 벡터 컬럼 및 인덱스 정의는 [마이그레이션 문서](/docs/12.x/migrations#available-column-types)를 참고하세요.

`whereVectorSimilarTo` 메서드는 지정한 벡터에 대한 코사인 유사도(cosine similarity)를 기준으로 결과를 필터링하고, 유사도가 높은 순서로 정렬합니다. `minSimilarity`는 0.0 ~ 1.0 사이의 값이며, 1.0은 완전 일치입니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

벡터 자리에 일반 문자열을 전달하면, Laravel이 [Laravel AI SDK](/docs/12.x/ai-sdk#embeddings)를 사용하여 자동으로 임베딩 벡터를 생성합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

`whereVectorSimilarTo`는 기본적으로 거리 기반 정렬(가장 유사한 것부터 우선)을 자동 적용합니다. 이 정렬을 비활성화하려면 `order` 인수를 `false`로 지정하세요:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

더 세밀한 제어가 필요하다면, `selectVectorDistance`, `whereVectorDistanceLessThan`, `orderByVectorDistance` 메서드를 각각 사용할 수 있습니다:

```php
$documents = DB::table('documents')
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, LIMIT, OFFSET (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬하기 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 원하는 컬럼 기준으로 정렬할 수 있습니다. 첫 번째 인수는 정렬하고자 하는 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하고 싶을 때는 `orderBy`를 여러 번 호출하세요:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

두 번째 인수를 생략하면 기본값은 오름차순입니다. 내림차순 정렬을 원한다면 두 번째 인수로 명시하거나, `orderByDesc` 메서드를 사용해도 됩니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한, `->` 연산자를 사용해 JSON 컬럼 내부 값으로도 정렬할 수 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest`는 날짜 기준으로 결과를 정렬하는데 사용됩니다. 기본적으로 `created_at` 컬럼으로 정렬하며, 정렬할 컬럼명을 인수로 지정할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤(RANDOM) 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어 랜덤 사용자 1명을 가져올 때 쓸 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거

`reorder` 메서드는 기존 쿼리의 "order by" 절을 모두 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

원하는 컬럼과 정렬 방향을 인수로 지정하면 기존 "order by" 절을 모두 제거한 뒤 새로운 정렬을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

내림차순으로 정렬을 재설정하고 싶을 때는 `reorderDesc` 메서드를 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화하기 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having` 메서드는 결과를 그룹화할 때 사용합니다. `having`은 `where`와 사용법이 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드는 값의 범위로 결과를 필터링할 수 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy`에는 여러 컬럼을 인수로 전달해 다중 그룹화도 가능합니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 having 쿼리를 만들려면 [havingRaw](#raw-methods)를 참고하세요.

<a name="limit-and-offset"></a>
### LIMIT 및 OFFSET

`limit`, `offset` 메서드로 결과 개수를 제한하거나 지정한 개수만큼 결과를 건너뛸 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

특정 상황에서만 쿼리 조건을 적용하고 싶다면, `when` 메서드를 사용할 수 있습니다. 예를 들어, HTTP 요청에 특정 입력 값이 있을 때만 `where` 조건을 추가하고 싶을 때 쓸 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 클로저를 실행합니다. 위 예시에서는 `role` 필드가 요청에 존재하고, `true`로 평가될 때만 클로저가 실행됩니다.

세 번째 인수로 추가 클로저를 넘길 수도 있는데, 이 경우 첫 번째 인수가 `false`일 때만 해당 클로저가 실행됩니다. 이 기능을 활용해 쿼리의 기본 정렬 로직을 지정할 수 있습니다:

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
## INSERT 구문 (Insert Statements)

쿼리 빌더는 테이블에 레코드를 삽입하기 위한 `insert` 메서드도 제공합니다. `insert`는 컬럼명과 값의 배열을 인수로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 각각의 레코드를 각기 다른 배열로 묶어 이중 배열로 전달하세요:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드를 사용하면 레코드 삽입 중 발생하는 오류를 무시할 수 있습니다. 이 방법을 쓸 때는 중복 레코드 오류 등 일부 오류가 무시된다는 점, 그리고 일부 데이터베이스에서는 다른 종류의 오류도 무시될 수 있다는 점을 유의하세요. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리를 활용해 삽입할 데이터를 결정합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 auto-increment id 컬럼이 있을 때, `insertGetId` 메서드로 레코드를 삽입한 뒤 ID 값을 바로 가져올 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서 `insertGetId`를 사용할 때 auto-increment 컬럼 이름이 반드시 `id`여야 합니다. 다른 이름의 "시퀀스"를 사용할 경우 두 번째 인수로 컬럼명을 지정하세요.

<a name="upserts"></a>
### UPSERT

`upsert` 메서드는 존재하지 않는 레코드는 삽입(insert), 이미 존재하는 레코드는 지정한 컬럼값으로 업데이트(update)합니다. 첫 번째 인수는 삽입/업데이트할 값 배열, 두 번째는 테이블 내에서 레코드를 고유하게 식별할 컬럼(들)의 배열, 세 번째는 기존 레코드에서 업데이트할 컬럼 배열입니다:

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

위 예시에서 `departure`와 `destination` 값이 같은 레코드가 이미 존재한다면 `price` 컬럼만 업데이트되고, 없으면 새 레코드가 삽입됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서 `upsert` 두 번째 인수(고유식별 컬럼)는 "primary" 혹은 "unique" 인덱스가 있어야 하며, MariaDB와 MySQL 드라이버는 두 번째 인수를 무시하고 항상 테이블의 "primary"/"unique" 인덱스로 기존 레코드를 식별합니다.

<a name="update-statements"></a>
## UPDATE 구문 (Update Statements)

쿼리 빌더는 레코드 삽입뿐 아니라, `update` 메서드로 기존 데이터를 수정할 수도 있습니다. `update`는 컬럼명-값 쌍 배열을 받으며, 영향을 받은 행의 개수를 반환합니다. `where` 조건과 함께 사용하는 것이 일반적입니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### UPDATE 또는 INSERT

기존 레코드를 업데이트, 없으면 새로 생성하는 동작이 필요할 때는 `updateOrInsert` 메서드가 유용합니다. 첫 번째 인수는 레코드 탐색용 조건 배열, 두 번째 인수는 업데이트할 컬럼명-값 쌍 배열입니다.

`updateOrInsert`는 첫 번째 인수로 레코드를 조회해 존재하면 두 번째 인수 값으로 업데이트, 없으면 합친 값으로 새 레코드를 생성합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

현재 레코드 상태에 따라 업데이트 또는 삽입할 값을 동적으로 결정하려면, 두 번째 인수로 클로저를 넘길 수 있습니다:

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

JSON 컬럼을 업데이트할 때는 `->` 구문을 활용해 JSON 객체 내 특정 키에 값을 지정할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### INCREMENT 및 DECREMENT

쿼리 빌더는 컬럼 값을 증가(increment) 또는 감소(decrement)시키는 편리한 메서드도 제공합니다. 필수 인수는 컬럼명, 두 번째 인수(옵션)는 증가/감소할 값입니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증가/감소와 동시에 추가 컬럼도 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach`, `decrementEach`로 여러 컬럼을 동시에 변경할 수도 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## DELETE 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제합니다. 영향을 받은 행의 개수를 반환하며, `where` 절을 추가해 일부만 삭제할 수도 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문 실행 시 "비관적 잠금(pessimistic locking)"을 지원하는 메서드를 제공합니다. "공유 잠금(shared lock)"을 걸고 싶다면 `sharedLock` 메서드를 사용하세요. 공유 잠금은 트랜잭션이 완료될 때까지 해당 행의 수정이 불가하도록 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

`lockForUpdate` 메서드를 사용하면 "for update" 잠금을 거는데, 공유 잠금은 물론, 다른 곳에서 선택하는 것도 차단합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

필수는 아니지만, 비관적 잠금은 [트랜잭션](/docs/12.x/database#database-transactions) 안에 쓰는 것이 좋습니다. 이렇게 하면 전체 작업이 완료될 때까지 데이터가 고정되어 외부 영향이 없으며, 실패 시 롤백과 동시에 잠금도 해제됩니다:

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
## 재사용 가능한 쿼리 컴포넌트 (Reusable Query Components)

애플리케이션 곳곳에서 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap`과 `pipe` 메서드를 이용해 재사용 가능한 클래스로 추출할 수 있습니다. 예를 들어, 아래와 같이 비슷한 쿼리가 두 번 나오고 있다면:

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

공통 로직(목적지 필터)을 별도의 재사용 가능한 객체로 추출할 수 있습니다:

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

이제 쿼리 빌더의 `tap` 메서드를 써서 객체의 로직을 적용할 수 있습니다:

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
#### Query Pipes

`tap` 메서드는 항상 쿼리 빌더 객체 자체를 반환합니다. 쿼리를 실행한 뒤 다른 값을 반환하는 객체를 만들고 싶다면 `pipe` 메서드를 쓰면 됩니다.

아래는 [페이지네이션](/docs/12.x/pagination) 로직을 공유하는 쿼리 객체 예시입니다. `DestinationFilter`와 달리, `Paginate`는 쿼리 조건을 적용하는 대신 쿼리를 실행하여 페이지네이터 인스턴스를 반환합니다:

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

이제 쿼리 빌더의 `pipe` 메서드를 사용해 위 객체의 페이징 로직을 적용하면 됩니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 작성하면서 디버깅하고 싶다면, `dd`와 `dump` 메서드를 쓸 수 있습니다. `dd`는 현재 쿼리 바인딩과 SQL을 출력한 뒤 실행을 즉시 중단하고, `dump`는 정보만 출력하고 계속 실행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql` 메서드는 SQL과 모든 파라미터 바인딩이 치환된 쿼리문을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
