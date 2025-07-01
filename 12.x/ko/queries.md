# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크로 분할 처리](#chunking-results)
    - [스트리밍 방식의 느린 처리](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [UNION](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 절](#where-any-all-none-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리적인 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
    - [전문 검색(Full Text) WHERE 절](#full-text-where-clauses)
- [정렬, 그룹화, LIMIT, OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [LIMIT과 OFFSET](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [업서트(upsert)](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 유연하게 작성하고 실행할 수 있는 플루언트 인터페이스를 제공합니다. 쿼리 빌더를 사용하면 애플리케이션 내에서 대부분의 데이터베이스 작업을 손쉽게 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 연동됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 통해 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더에 전달하는 값들은 따로 문자열 정제나 필터링을 할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력으로 쿼리에서 참조되는 컬럼명(예: "order by"에 사용되는 컬럼명 포함)을 직접 지정하도록 해서는 절대로 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

쿼리를 시작하려면 `DB` 파사드의 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하며, 여기에 추가 제약조건을 체이닝하여 붙이고 마지막에 `get` 메서드를 사용해 결과를 가져올 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 오브젝트입니다. 각 컬럼 값은 오브젝트의 프로퍼티로써 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 맵핑과 축소(reduce)에 매우 강력한 다양한 메서드를 제공합니다. 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행/컬럼 조회

테이블에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 오브젝트를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 조회 조건에 맞는 행이 없을 경우, 예외(`Illuminate\Database\RecordNotFoundException`)를 발생시키길 원한다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이때 예외가 캐치되지 않으면 자동으로 404 HTTP 응답이 클라이언트에 전달됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없는 경우, `value` 메서드를 사용해서 원하는 컬럼의 값만 바로 추출할 수 있습니다. 이 메서드는 해당 컬럼의 값 자체를 바로 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

특정 `id` 값을 가진 행을 조회하려면 `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

특정 컬럼의 값만 모아놓은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면 `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 사용자들의 직책(title)만 모아서 컬렉션으로 가져올 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인수로 컬렉션 키로 사용할 컬럼명을 지정하면, 결과 컬렉션의 키를 해당 컬럼으로 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크로 분할 처리

수천 개에 이르는 대량의 데이터베이스 레코드를 다뤄야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 소규모 청크 단위로 한 번에 가져오고, 각 청크를 클로저에 전달하여 처리합니다. 예를 들어, `users` 테이블을 한 번에 100개씩 청크로 나눠서 전부 처리하는 코드는 다음과 같습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후의 청크 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 단위로 레코드를 갱신(update)하는 경우, 청크 결과가 의도치 않게 바뀔 수 있습니다. 청크 단위로 데이터를 가져오면서 해당 데이터를 수정해야 한다면, `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 레코드의 기본 키(primary key)를 기준으로 자동으로 페이지네이션합니다.

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

`chunkById`와 `lazyById` 메서드는 실행되는 쿼리에 자체적으로 "where" 조건을 추가하므로, 보통 본인이 지정하는 조건들은 클로저 내에서 [논리적으로 그룹화](#logical-grouping)해 주는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 수정(update)하거나 삭제(delete)하는 경우, 기본 키 또는 외래 키가 변경될 수 있으므로 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청크 결과에 포함되지 않을 위험이 있습니다.

<a name="streaming-results-lazily"></a>
### 스트리밍 방식의 느린 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 쿼리를 청크 단위로 실행한다는 점에서 비슷하지만, 각 청크를 콜백에 전달하는 대신 [LazyCollection](/docs/12.x/collections#lazy-collections) 인스턴스를 반환하여 전체 데이터를 하나의 스트림처럼 다룰 수 있도록 해줍니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 이렇게 순회하면서 데이터를 갱신하려면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 게 더 안전합니다. 이들 메서드는 레코드의 기본 키 기준으로 자동으로 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 순회 과정에서 레코드를 업데이트하거나 삭제할 시, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 줄 수 있으니 주의해야 합니다. 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 값을 가져올 수 있는 메서드도 제공합니다. 쿼리 빌드 이후 이 메서드들을 호출하면 됩니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론 집계 함수와 다른 절(조건)을 조합해 집계 대상을 세밀하게 지정할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 판별

쿼리 조건에 해당하는 레코드가 존재하는지 `count` 메서드로 확인하지 않고, `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT 구문

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정

데이터베이스 테이블의 전체 컬럼을 모두 선택하지 않고, 원하는 컬럼만 조회하려면 `select` 메서드를 사용해 SELECT 절을 커스텀할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복되지 않는(중복 제거된) 결과만 반환하도록 쿼리를 강제할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있는 상태에서 SELECT 절에 컬럼을 하나 더 추가하고 싶으면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

쿼리에 임의의 문자열을 삽입해야 할 때는 `DB` 파사드의 `raw` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리 내에 문자열로 그대로 삽입되기 때문에, SQL 인젝션이 발생하지 않도록 반드시 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 관련 메서드

`DB::raw` 메서드 대신, 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있는 아래 메서드들도 사용할 수 있습니다. **주의: Raw 표현식을 사용하는 모든 쿼리는 SQL 인젝션으로부터 안전함을 Laravel이 보장해 줄 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩할 값 배열도 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 그대로 삽입할 수 있습니다. 두 번째 인수로 바인딩할 값 배열을 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절 값으로 raw 문자열을 넘길 수 있습니다. 이 메서드들도 바인딩 값 배열을 두 번째 인수로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절 값으로 raw 문자열을 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 사용할 때 사용합니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Join)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더에서도 쿼리에 join 절을 쉽게 추가할 수 있습니다. 기본적인 "inner join"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블명, 나머지 인수들은 조인 조건을 지정합니다. 한 쿼리에서 여러 테이블을 동시에 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 절

"inner join" 대신 "left join"이나 "right join"을 사용하고 싶다면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 메서드 시그니처는 `join` 메서드와 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Cross Join 절

"cross join"을 수행할 때는 `crossJoin` 메서드를 사용할 수 있습니다. Cross Join은 첫 번째 테이블과 두 번째 테이블의 모든 조합(데카르트 곱)을 만듭니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복합적인 조인 조건이 필요하다면, `join` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아, 조인 절에 제약을 정교하게 추가할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서도 "where" 절이 필요하다면, JoinClause 인스턴스에서 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이때는 두 컬럼을 비교하는 대신 컬럼 값과 특정 값을 비교하게 됩니다.

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 쿼리와 서브쿼리를 조인할 수도 있습니다. 각 메서드는 세 개의 인수를 받는데, 서브쿼리, 그 테이블 별칭(alias), 그리고 관련 컬럼을 지정하는 클로저입니다. 예를 들어, 각 사용자의 가장 최근에 작성된 블로그 글의 `created_at` 정보도 함께 조회하려면 다음과 같이 작성할 수 있습니다.

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
#### Lateral Joins

> [!WARNING]
> Lateral Join은 현재 PostgreSQL, MySQL 8.0.14 이상, 그리고 SQL Server에서 지원됩니다.

"lateral join"을 사용하려면 `joinLateral` 및 `leftJoinLateral` 메서드를 사용할 수 있습니다. 이 메서드들은 두 가지 인수(서브쿼리와 그 테이블 별칭)를 받습니다. 조인 조건은 해당 서브쿼리의 `where` 구문 안에서 정의해야 합니다. Lateral Join은 각 행에 대해 실행되며, 서브쿼리 바깥 쪽의 컬럼도 참조할 수 있습니다.

아래 예시는 각 사용자의 최근 블로그 포스트 3개까지 포함하여 결과를 조회합니다. 한 명의 사용자가 최대 3개의 포스트 행을 결과에 가질 수 있습니다. 조인 조건은 서브쿼리의 `whereColumn` 구문을 통해 현재 user 행을 참조합니다.

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
## UNION

쿼리 빌더는 두 개 이상의 쿼리를 "union"하는 편리한 방법도 제공합니다. 먼저 기본 쿼리를 만들고 나서, `union` 메서드를 사용해 추가 쿼리를 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도, `unionAll` 메서드가 있습니다. `unionAll`은 결과를 중복 제거하지 않고 단순히 합칠 뿐입니다. `unionAll`의 메서드 시그니처도 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용해 "where" 절을 쿼리에 추가할 수 있습니다. 가장 기본적인 사용은 세 개의 인수를 받는데, 첫 번째는 컬럼명, 두 번째는 연산자(지원되는 DB 연산자 모두 가능), 세 번째는 비교할 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼이 100이고 `age` 컬럼이 35보다 큰 사용자를 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의를 위해 컬럼이 특정 값과 "같음(=)"을 비교할 때는 두 번째 인수로 값을 바로 넘길 수 있습니다. Laravel은 자동으로 `=` 연산자로 처리합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

앞서 설명한 것처럼, 데이터베이스에서 지원하는 모든 연산자를 자유롭게 사용할 수 있습니다.

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

또한, 조건을 배열로 한 번에 넘겨줄 수도 있습니다. 배열의 각 요소는 `where` 메서드에 전달하는 3개 인수를 담은 배열이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조되는 컬럼명(특히 "order by" 컬럼 등)에 사용자 입력을 직접 사용하는 것은 절대 피해야 합니다.

> [!WARNING]
> MySQL과 MariaDB에서는 문자열-숫자 비교시 문자열이 자동으로 정수로 변환됩니다. 이 때 숫자가 아닌 문자열은 `0`으로 변환되므로, 예기치 않은 결과가 나올 수 있습니다. 예를 들어, 테이블에 `secret` 컬럼이 `aaa`라는 값을 가지고 있고 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이런 현상을 방지하려면 값이 쿼리에 들어가기 전에 반드시 적절한 타입으로 변환해 주는 것이 좋습니다.

<a name="or-where-clauses"></a>
### OR WHERE 절

쿼리 빌더의 `where` 메서드를 연달아 체이닝하면, 각 "where" 절은 `and` 연산자로 묶입니다. 하지만 "or" 조건으로 연결하려면 `orWhere` 메서드를 사용해야 합니다. `orWhere`도 `where`와 동일한 인수를 받습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

"or" 조건을 괄호로 묶어 그룹화하고 싶다면, `orWhere`의 첫 번째 인수로 클로저를 넘겨주면 됩니다.

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

위 예시는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> `orWhere` 호출은 항상 괄호로 그룹화하는 게 좋습니다. 그렇지 않으면 글로벌 스코프가 적용될 때 예기치 않은 동작이 발생할 수 있습니다.

<a name="where-not-clauses"></a>

### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정(negate)하는 데 사용할 수 있습니다. 예를 들어, 아래의 쿼리는 특가(clearance) 상품이거나 가격이 10 미만인 상품들을 제외합니다.

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

여러 컬럼에 동일한 쿼리 제약 조건을 적용해야 할 때가 있습니다. 예를 들어, 특정 컬럼 목록 중 하나라도 주어진 값과 `LIKE` 연산자를 만족하는 모든 레코드를 조회하고 싶을 수 있습니다. 이럴 때 `whereAny` 메서드를 사용할 수 있습니다.

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

위의 쿼리는 다음과 같은 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

마찬가지로, `whereAll` 메서드를 사용하면 지정한 여러 컬럼이 모두 주어진 조건을 만족하는 레코드를 조회할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위의 쿼리는 다음과 같은 SQL을 생성합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 컬럼들 중 그 어떤 것도 조건에 일치하지 않는 레코드를 조회하는 데 사용할 수 있습니다.

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

위의 쿼리는 다음과 같은 SQL을 생성합니다.

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

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스(현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼에 대한 쿼리도 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용합니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 쿼리하려면 `whereJsonContains`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

애플리케이션이 MariaDB, MySQL, PostgreSQL 데이터베이스를 사용할 경우, `whereJsonContains` 메서드에 값의 배열을 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

JSON 배열의 길이를 조건으로 쿼리하려면 `whereJsonLength` 메서드를 사용합니다.

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

`whereLike` 메서드는 패턴 일치(문자열 매칭)를 위해 "LIKE" 절을 쿼리에 추가할 수 있습니다. 이 메서드들은 데이터베이스 종류에 상관없이 문자열 매칭 쿼리를 수행할 수 있도록 하며, 대소문자 구분 여부도 선택적으로 지정할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 사용해 대소문자를 구분하는 검색을 활성화할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 쿼리에 "NOT LIKE" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`를 사용해서 NOT LIKE 조건이 포함된 "or" 절을 추가할 수도 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> SQL Server에서는 `whereLike`의 대소문자 구분 검색 기능이 현재 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 컬럼의 값이 지정한 배열에 포함되어 있는지 검사합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 해당 컬럼의 값이 배열에 포함되어 있지 않은지 검사합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 다음과 같은 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 대량의 정수 배열을 바인딩해야 하는 경우, 메모리 사용량을 크게 줄이기 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하는 것이 좋습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지 검증합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼의 값이 두 값의 범위를 벗어나는지 검증합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 특정 컬럼의 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 컬럼의 값이 같은 행의 두 컬럼 값의 범위를 벗어나는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 지정된 컬럼의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 컬럼의 값이 `NULL`이 아님을 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼의 값을 날짜와 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 컬럼의 값을 특정 월(month)과 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼의 값을 특정 일(day)과 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼의 값을 특정 연도와 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼의 값을 특정 시간과 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture` 메서드는 컬럼의 값이 과거(past)인지, 혹은 미래(future)인지 판단할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast` 및 `whereNowOrFuture` 메서드를 사용하면, 현재 날짜 및 시간도 포함한 과거/미래 판별이 가능합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 컬럼의 값이 오늘이거나, 오늘 이전, 오늘 이후인 경우를 각각 판단할 수 있습니다.

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

마찬가지로, `whereTodayOrBefore`, `whereTodayOrAfter` 메서드를 사용하면, 오늘 포함 이전/이후를 판별할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼의 값이 서로 같은지 검사할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 `whereColumn` 메서드에 전달하는 것도 가능합니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 배열을 인자로 전달하는 것도 가능합니다. 이 경우 조건들은 `and`로 결합됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑(Logical Grouping)

쿼리의 원하는 논리 구조를 얻기 위해 여러 개의 "where" 절을 괄호로 묶어 그룹화해야 할 때가 있습니다. 특히, 원치 않는 쿼리 동작을 방지하기 위해 `orWhere` 메서드의 호출은 항상 괄호로 그룹화하는 것이 일반적으로 바람직합니다. 이를 위해 `where` 메서드에 클로저(익명 함수)를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 예시처럼, `where` 메서드에 클로저를 전달하면 쿼리 빌더에 제약 조건 그룹을 시작하라고 알립니다. 클로저에는 쿼리 빌더 인스턴스가 전달되며, 괄호 그룹 안에 들어갈 조건들을 추가할 수 있습니다. 위 예시는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 원치 않는 동작을 방지하려면 항상 `orWhere` 호출을 그룹으로 묶어야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있게 해줍니다. 이 메서드는 클로저를 인수로 받아, "exists" 절 내부에 들어갈 쿼리를 정의할 수 있도록 쿼리 빌더 인스턴스를 전달합니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 `whereExists`에 전달하는 방법도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예시 모두 다음과 같은 SQL을 생성합니다.

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

때로는 "where" 절에서 서브쿼리의 결과와 주어진 값을 비교해야 할 수도 있습니다. 이를 위해 `where` 메서드에 클로저와 값을 함께 전달하면 됩니다. 예를 들어, 아래 쿼리는 최근에 특정 타입의 "membership"이 존재하는 모든 사용자를 조회합니다.

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

또는 컬럼과 서브쿼리 결과를 비교할 필요가 있는 경우, 컬럼명, 연산자, 그리고 클로저를 `where` 메서드에 전달할 수 있습니다. 아래 쿼리는 금액(`amount`)이 평균값보다 작은 모든 수입 레코드를 조회합니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전체 텍스트(Full Text) Where 절

> [!WARNING]
> 전체 텍스트 where 절은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 설정된 컬럼에 전체 텍스트 "where" 절을 쿼리에 추가할 수 있도록 해줍니다. 이 메서드들은 사용 중인 데이터베이스 시스템에 맞는 적절한 SQL로 변환됩니다. 예를 들어, MariaDB 또는 MySQL을 사용하는 애플리케이션에서는 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹핑, Limit, Offset

<a name="ordering"></a>
### 정렬(Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 특정 컬럼 기준으로 정렬할 수 있게 해줍니다. 첫 번째 인수는 정렬하고자 하는 컬럼명이고, 두 번째 인수는 정렬 방향으로 `asc` 또는 `desc` 중 하나를 지정할 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼을 기준으로 정렬하고 싶다면, 필요한 만큼 반복해서 `orderBy`를 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향 인자는 생략할 수 있으며, 기본값은 오름차순(ascending)입니다. 내림차순 정렬을 원할 경우 두 번째 인수로 `desc`를 지정하거나, 또는 `orderByDesc`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

마지막으로, `->` 연산자를 이용해 JSON 컬럼 내부의 값 기준으로도 정렬이 가능합니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드를 사용하면 날짜 기준으로 결과를 쉽게 정렬할 수 있습니다. 기본적으로 해당 테이블의 `created_at` 컬럼을 기준으로 정렬됩니다. 정렬 기준 컬럼명을 직접 지정할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>

#### 무작위 정렬

`inRandomOrder` 메서드는 쿼리 결과를 무작위로 정렬하는 데 사용할 수 있습니다. 예를 들어, 이 메서드를 사용해 임의의 사용자를 가져올 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 쿼리에 이미 적용된 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드 사용 시 컬럼과 정렬 방향을 전달하면, 기존의 모든 "order by" 절을 제거한 뒤 완전히 새로운 정렬 조건을 적용할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

더 편리하게, `reorderDesc` 메서드를 사용하면 쿼리 결과를 내림차순으로 다시 정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상하신 것처럼, `groupBy`와 `having` 메서드를 사용하여 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드는 `where` 메서드와 유사한 시그니처를 가집니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하면, 지정된 범위 내의 결과만 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인수를 전달하여, 여러 컬럼으로 그룹화할 수도 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 구문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참고하시기 바랍니다.

<a name="limit-and-offset"></a>
### Limit와 Offset

`limit` 및 `offset` 메서드를 통해 쿼리에서 반환되는 결과의 개수를 제한하거나, 지정한 개수의 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

경우에 따라, 특정 조건이 충족될 때만 쿼리에 특정 절을 추가하고 싶을 수 있습니다. 예를 들어, HTTP 요청에서 특정 입력값이 있을 때에만 `where` 구문을 적용하려면, `when` 메서드를 사용할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`로 평가될 때만 지정된 클로저를 실행합니다. 첫 번째 인수가 `false`이면, 해당 클로저는 실행되지 않습니다. 따라서 위의 예시에서는, 요청에서 `role` 필드가 전달되어 `true`로 평가될 때에만 `when` 메서드의 클로저가 호출됩니다.

또한, `when` 메서드의 세 번째 인수로 또 다른 클로저를 전달할 수 있습니다. 이 추가 클로저는 첫 번째 인수가 `false`로 평가될 때에만 실행됩니다. 아래 예시에서는 이 기능을 사용하여 쿼리의 기본 정렬 방식을 설정합니다.

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
## Insert 구문

쿼리 빌더는 데이터베이스 테이블에 레코드를 삽입할 수 있도록 `insert` 메서드도 제공합니다. `insert` 메서드는 컬럼명과 값을 담은 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

중첩된 배열의 배열을 전달하여 한 번에 여러 레코드를 삽입할 수도 있습니다. 각 배열은 테이블에 삽입될 하나의 레코드를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 데이터베이스에 레코드를 삽입하면서 오류가 발생해도 무시합니다. 이 방식을 사용할 때는, 중복 레코드로 인한 오류뿐 아니라 데이터베이스 엔진에 따라 다른 유형의 오류까지도 무시될 수 있음을 알아야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict 모드를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리를 활용해, 그 결과를 기반으로 새 레코드를 테이블에 삽입할 수 있습니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id 컬럼이 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입한 뒤 id를 바로 받아올 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 경우, `insertGetId` 메서드는 자동 증가 컬럼의 이름이 반드시 `id` 이어야 합니다. 다른 "시퀀스"에서 id를 받아오고 싶다면, 해당 컬럼명을 `insertGetId` 메서드의 두 번째 인수로 전달하면 됩니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 있는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인수에는 삽입 또는 업데이트할 값들의 배열이 들어가며, 두 번째는 해당 테이블에서 레코드를 고유하게 식별하는 컬럼(들)의 배열입니다. 세 번째이자 마지막 인수는, 일치하는 레코드가 이미 존재할 경우 업데이트할 컬럼들을 배열로 전달합니다.

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

위 예시에서, 라라벨은 두 개의 레코드를 삽입하려 시도합니다. 만약 동일한 `departure`와 `destination` 값을 가진 레코드가 이미 존재한다면, 해당 레코드의 `price` 컬럼만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인수로 전달된 컬럼들이 "기본키" 또는 "고유" 인덱스를 가지고 있어야 합니다. 또한, MariaDB와 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하며, 항상 테이블의 "기본키"나 "고유" 인덱스만을 기준으로 기존 레코드의 존재 여부를 판단합니다.

<a name="update-statements"></a>
## Update 구문

레코드를 삽입할 뿐 아니라, 쿼리 빌더는 `update` 메서드를 통해 기존 레코드를 업데이트할 수도 있습니다. `update` 역시 수정할 컬럼과 값의 쌍으로 구성된 배열을 전달받습니다. 이 메서드는 영향을 받은 행(row)의 개수를 반환합니다. 또한, `where` 절을 활용해 `update` 쿼리의 대상을 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

경우에 따라, 기존 레코드를 업데이트하거나, 일치하는 레코드가 없으면 새로 생성하고 싶을 수 있습니다. 이러한 상황에서는 `updateOrInsert` 메서드를 사용할 수 있습니다. 이 메서드는 두 개의 인수를 받습니다: 첫 번째는 조건을 작성하는 컬럼/값 쌍의 배열, 두 번째는 실제로 업데이트(또는 삽입)할 컬럼/값 쌍의 배열입니다.

`updateOrInsert`는 첫 번째 인수의 조건을 통해 일치하는 데이터베이스 레코드를 찾으려고 시도합니다. 레코드가 존재하면, 두 번째 인수의 값들로 업데이트합니다. 만약 찾을 수 없다면, 두 인수를 합친 값으로 새 레코드를 생성하여 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

일치하는 레코드 존재 여부에 따라 데이터베이스에 삽입 또는 업데이트할 속성을 동적으로 지정하고 싶다면, `updateOrInsert` 메서드에 클로저를 전달할 수 있습니다.

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

JSON 컬럼을 업데이트할 때는, `->` 문법을 사용해 해당 객체의 특정 키를 지정해야 합니다. 이 연산은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 지정된 컬럼의 값을 간편하게 증가시키거나 감소시키는 메서드도 제공합니다. 이 메서드들은 최소 한 개의 인수(변경할 컬럼명)를 받으며, 두 번째 인수로 증가 또는 감소량을 지정할 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증가/감소 연산 중에 추가 컬럼들도 함께 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach`와 `decrementEach` 메서드를 활용해 여러 컬럼의 값을 한 번에 증가/감소시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제할 때 사용할 수 있습니다. 이 메서드는 영향을 받은 행(row)의 개수를 반환합니다. "where" 절을 추가해 삭제할 대상을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 락(Pessimistic Locking)

쿼리 빌더에는 `select` 실행 시 "비관적 락"을 걸 수 있는 몇 가지 메서드가 준비되어 있습니다. "공유 락(shared lock)"을 적용하려면 `sharedLock` 메서드를 사용하면 됩니다. 이 락은 선택된 행들이 트랜잭션이 커밋될 때까지 수정되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate` 메서드를 사용해 "for update" 락을 걸 수 있습니다. 이 락은 선택된 레코드가 다른 트랜잭션의 "공유 락" 또는 수정 작업에 의해 변경되는 것을 모두 막아줍니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 락을 반드시 사용해야 하는 것은 아니지만, 코드에서는 이를 [트랜잭션](/docs/12.x/database#database-transactions) 안에 감싸는 것이 권장됩니다. 트랜잭션을 사용하면 전체 작업이 끝날 때까지 데이터가 변경되지 않으며, 도중에 오류가 발생하면 모든 변경 사항을 롤백하고 락도 자동으로 해제됩니다.

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
## 재사용 가능한 쿼리 컴포넌트

애플리케이션 내에서 반복적으로 사용되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 이용해 별도의 재사용 객체로 추출할 수 있습니다. 예를 들어, 애플리케이션에서 아래와 같이 유사한 쿼리를 여러 번 작성한다고 가정해 봅시다.

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

이처럼 여러 쿼리에서 공통적으로 존재하는 목적지(destination) 필터링 로직을 별도 객체로 추출할 수 있습니다.

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

그 다음, 쿼리 빌더의 `tap` 메서드를 활용해 이 객체의 로직을 쿼리에 적용할 수 있습니다.

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### 쿼리 파이프(Query Pipes)

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 쿼리 결과를 반환하거나 쿼리를 실행하는 별도의 객체로 추출하고 싶다면, `pipe` 메서드를 사용할 수 있습니다.

아래는 애플리케이션에서 공통적으로 사용되는 [페이지네이션](/docs/12.x/pagination) 로직을 담은 쿼리 객체(Paginate) 예시입니다. `DestinationFilter` 객체가 쿼리 조건만 적용하는 것과 달리, `Paginate` 객체는 직접 쿼리를 실행해 페이지네이터 인스턴스를 반환합니다.

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
        private string $perPage = 25,
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

쿼리 빌더의 `pipe` 메서드를 사용하면, 이렇게 추출된 객체를 통해 공통 페이지네이션 로직을 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하는 중에, `dd` 및 `dump` 메서드를 사용하면 현재 쿼리의 바인딩 정보와 SQL을 출력할 수 있습니다. `dd` 메서드는 디버깅 정보를 출력한 뒤 실행을 종료하고, `dump` 메서드는 실행을 계속 진행합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드는 쿼리가 실행될 때 실제로 바인딩된 값을 치환한 SQL문을 출력합니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```