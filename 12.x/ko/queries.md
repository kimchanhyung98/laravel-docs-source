# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과 청크 단위 처리](#chunking-results)
    - [지연(lazy) 방식으로 결과 스트리밍](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 구문](#select-statements)
- [원시 표현식 사용](#raw-expressions)
- [조인(Joins)](#joins)
- [유니언(Unions)](#unions)
- [기본 WHERE 구문](#basic-where-clauses)
    - [WHERE 구문](#where-clauses)
    - [OR WHERE 구문](#or-where-clauses)
    - [WHERE NOT 구문](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 구문](#where-any-all-none-clauses)
    - [JSON WHERE 구문](#json-where-clauses)
    - [추가 WHERE 구문](#additional-where-clauses)
    - [논리적 그룹핑](#logical-grouping)
- [고급 WHERE 구문](#advanced-where-clauses)
    - [WHERE EXISTS 구문](#where-exists-clauses)
    - [서브쿼리 WHERE 구문](#subquery-where-clauses)
    - [전체 텍스트 WHERE 구문](#full-text-where-clauses)
- [정렬, 그룹핑, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 구문](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [Upsert](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소(Increment and Decrement)](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리 작성과 실행을 위한 편리하고 유연한(flunet) 인터페이스를 제공합니다. 이 쿼리 빌더를 사용해 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, 라라벨에서 지원하는 모든 데이터베이스 시스템과 완벽하게 연동됩니다.

라라벨 쿼리 빌더는 SQL 인젝션 공격으로부터 애플리케이션을 보호하기 위해 PDO 파라미터 바인딩을 사용합니다. 따라서, 쿼리 빌더에 문자열을 전달할 때 따로 정제(clean)하거나 필터링(sanitize)할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자로부터 입력 받은 값이 쿼리 내에서 참조되는 컬럼명을 결정하도록 절대 허용해서는 안 됩니다. 이에는 "order by"에 사용할 컬럼명도 포함됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

쿼리를 시작하려면 `DB` 파사드에서 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대해 유연한 쿼리 빌더 인스턴스를 반환하며, 이 빌더로 여러 제약 조건을 연결(chain)한 후 마지막에 `get` 메서드로 결과를 가져올 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 표시합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과가 담긴 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 이 컬렉션의 각 결과는 PHP `stdClass` 객체입니다. 각 컬럼의 값은 해당 객체의 속성으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨 컬렉션은 데이터를 매핑하거나 집계할 때 매우 강력한 다양한 메서드를 제공합니다. 라라벨 컬렉션에 대해 더 알아보고 싶다면 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블의 단일 행 또는 단일 컬럼 조회하기

테이블에서 하나의 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용하면 됩니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 조건에 일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이때 예외가 잡히지 않으면 404 HTTP 응답이 클라이언트로 자동 전송됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아닌 특정 컬럼 값만 필요하다면 `value` 메서드로 레코드에서 해당 컬럼 값을 바로 추출할 수 있습니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 행 하나를 조회하려면 `find` 메서드를 사용합니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

특정 컬럼의 값들만 모은 `Illuminate\Support\Collection` 인스턴스를 얻으려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예시에서는 사용자 타이틀의 컬렉션을 가져옵니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인자를 지정하면, 컬렉션에서 해당 컬럼을 키로 사용하여 결과를 반환할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청크 단위 처리

수천 개의 데이터베이스 레코드를 한 번에 다뤄야 한다면, `DB` 파사드가 제공하는 `chunk` 메서드 사용을 고려해보세요. 이 메서드는 한 번에 소량의 결과 청크만 조회하여 처리용 클로저에 전달합니다. 예를 들어, `users` 테이블 전체를 100개씩 청크로 나눠 조회하려면 다음과 같이 합니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리를 중단할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 단위로 레코드를 처리하는 도중에 데이터베이스 레코드를 업데이트한다면, 예기치 않게 청크 결과가 변경될 수 있습니다. 청크 도중 조회한 레코드를 업데이트할 계획이라면 항상 `chunkById` 메서드 사용이 더 안전합니다. 이 메서드는 레코드의 기본 키(primary key)를 기준으로 결과를 자동으로 페이지네이션 처리합니다.

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

`chunkById`와 `lazyById` 메서드는 쿼리 실행 시 자체적으로 "where" 조건을 쿼리에 추가합니다. 따라서 자신만의 조건이 필요하다면 [논리적 그룹핑](#logical-grouping)을 위해 클로저 안에서 조건을 묶어주는 것이 좋습니다.

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
> 청크 콜백 안에서 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키 값이 변화한다면 쿼리 대상 청크에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 누락될 수 있으니 주의해야 합니다.

<a name="streaming-results-lazily"></a>
### 지연(lazy) 방식으로 결과 스트리밍

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 내부적으로 쿼리를 청크 단위로 실행합니다. 하지만 각 청크마다 콜백에 전달하는 대신, `lazy()` 메서드는 [LazyCollection](/docs/12.x/collections#lazy-collections) 인스턴스를 반환하므로 하나의 스트림처럼 결과에 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복 작업 중에 조회한 레코드를 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드 사용이 더 안전합니다. 이 메서드들은 레코드의 기본 키 기준으로 자동 페이지네이션을 처리합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중에 레코드를 업데이트하거나 삭제할 경우, 기본 키 또는 외래 키 값이 변경되면 쿼리 결과에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 다양한 집계 메서드를 제공합니다. 쿼리를 작성한 후 이 메서드 중 하나를 호출해서 집계값을 바로 구할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 조건절과 함께 조합하여 집계값 계산을 좀 더 세밀하게 제어할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

특정 조건에 일치하는 레코드가 있는지 확인할 때, `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

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
#### SELECT 절 지정하기

테이블의 모든 컬럼을 항상 선택할 필요는 없습니다. `select` 메서드를 사용해 쿼리에 사용할 SELECT 항목을 직접 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복 없는 결과만 강제로 반환할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고 기존 select 구문에 컬럼을 하나 더 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 사용

가끔 쿼리에 임의의 문자열을 직접 삽입해야 할 경우가 있습니다. 이럴 땐 `DB` 파사드의 `raw` 메서드로 원시 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> 원시 구문(raw statement)은 쿼리에 문자열 그대로 삽입됩니다. 따라서 SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### RAW 관련 메서드

`DB::raw` 메서드 대신, 원시 표현식을 쿼리 내 여러 부분에 삽입할 수 있는 다양한 메서드도 사용할 수 있습니다. **라라벨은 원시 표현식이 포함된 쿼리가 SQL 인젝션으로부터 반드시 안전함을 보장하지 않는다는 점에 유의하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메서드는 선택적으로 바인딩 값 배열을 두 번째 인자로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 원시 "where" 절을 삽입할 수 있게 해줍니다. 두 번째 인자로 선택적 바인딩 값 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw` 메서드를 사용하면 "having" 절에 사용할 원시 문자열을 지정할 수 있습니다. 이 메서드 역시 선택적으로 바인딩 값 배열을 두 번째 인자로 받습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드를 사용하면 "order by" 절에 사용할 원시 문자열을 지정할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드를 사용하면 `group by` 절에 사용할 원시 문자열을 직접 지정할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Joins)

<a name="inner-join-clause"></a>
#### INNER JOIN 구문

쿼리 빌더는 쿼리에 조인 절을 추가하는 기능을 제공합니다. 기본적인 "INNER JOIN"을 수행하려면 쿼리 빌더 인스턴스의 `join` 메서드를 사용하면 됩니다. 첫 번째 인자는 조인할 테이블명이고, 이후 인자들은 조인의 컬럼 제약 조건을 설정하는 데 사용됩니다. 한 쿼리 내에서 여러 테이블을 조인하는 것도 가능합니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### LEFT JOIN / RIGHT JOIN 구문

"INNER JOIN" 대신 "LEFT JOIN" 또는 "RIGHT JOIN"을 사용하고 싶다면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이 메서드들은 `join`과 똑같은 방식으로 사용합니다.

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

"Cross Join"을 수행하려면 `crossJoin` 메서드를 사용할 수 있습니다. Cross Join은 첫 번째 테이블과 조인 테이블의 데카르트 곱(모든 가능한 조합)을 만듭니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 구문

더 복잡한 조인 조건도 지정할 수 있습니다. 우선, `join` 메서드의 두 번째 인자로 클로저를 전달하세요. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받으며, 이 객체로 조인 조건을 세밀히 지정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인 조건에 "where" 절을 사용할 수도 있습니다. 조인된 두 컬럼이 아니라 컬럼 값과 고정 값 비교가 필요할 때 `JoinClause` 인스턴스의 `where` 및 `orWhere` 메서드를 사용하세요.

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 쿼리에 서브쿼리를 조인할 수 있습니다. 각 메서드는 세 가지 인자를 받습니다: 서브쿼리, 테이블 별칭, 그리고 연관 컬럼을 지정하는 클로저입니다. 아래 예에서는 각 사용자 레코드에 해당 사용자가 최근에 작성한 블로그 포스트의 `created_at` 타임스탬프가 포함되도록 결과를 가져옵니다.

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
> Lateral 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원됩니다.

`joinLateral`, `leftJoinLateral` 메서드를 사용해 서브쿼리와 함께 "Lateral Join"을 수행할 수 있습니다. 이 메서드는 두 가지 인자를 받으며: 서브쿼리와 테이블 별칭입니다. 조인 조건은 서브쿼리 내부의 `where` 절에 지정해야 합니다. Lateral 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

아래 예시는 사용자의 최근 블로그 포스트 3개도 함께 조회하는 쿼리입니다. 각 사용자는 최근 블로그 포스트 최대 3개만 결과로 가져옵니다. 조인 조건은 서브쿼리 내부의 `whereColumn` 절에 지정되어, 현재 사용자 행을 참조합니다.

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
## 유니언(Unions)

쿼리 빌더에는 두 개 이상의 쿼리를 "유니언"으로 합치는 편리한 메서드도 있습니다. 우선 첫 번째 쿼리를 만든 후, `union` 메서드를 사용해 더 많은 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드를 제공합니다. `unionAll`로 결합된 쿼리는 중복 결과가 제거되지 않습니다. `unionAll`의 사용 방법은 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 구문

<a name="where-clauses"></a>
### WHERE 구문

쿼리 빌더의 `where` 메서드로 쿼리에 "WHERE" 조건을 추가할 수 있습니다. 가장 단순하게는 세 개의 인자를 전달하는데, 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 모든 연산자 사용 가능), 세 번째는 컬럼 값과 비교할 대상 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼 값이 `100`이고 `age` 컬럼 값이 `35`보다 큰 사용자를 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

연산자가 `=`이면, 값만 두 번째 인자로 전달해도 라라벨이 연산자를 `=`로 자동 인식합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

앞서 언급한 것처럼, 데이터베이스에서 지원하는 아무 연산자나 사용할 수 있습니다.

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

조건 배열을 전달하여 여러 조건을 한 번에 지정할 수도 있습니다. 배열의 각 요소는 일반적으로 `where` 메서드에 전달하는 세 인자를 구성합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력값이 쿼리 내 참조되는 컬럼명을 결정하도록 해서는 절대 안 됩니다(예: "order by" 컬럼명 등).

> [!WARNING]
> MySQL과 MariaDB는 문자열과 숫자 비교 시 문자열을 자동으로 정수형으로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 0으로 바뀌기 때문에, 예기치 못한 결과가 발생할 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 행에 대해 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이런 문제를 방지하려면 쿼리 사용 전 각 값의 타입을 꼭 맞춰주세요.

<a name="or-where-clauses"></a>
### OR WHERE 구문

여러 번 `where` 메서드를 연달아 사용하면, 조건이 `and` 연산자로 연결됩니다. 하지만 `or` 연산자를 사용하려면 `orWhere` 메서드를 활용할 수 있습니다. `orWhere`는 `where`와 동일한 인자를 받습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호(())로 그룹핑된 "or" 조건이 필요하다면, 첫 번째 인자로 클로저를 넘길 수 있습니다.

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

위 예시는 아래와 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 스코프가 적용될 때 예기치 못한 동작을 피하려면 반드시 `orWhere` 호출을 그룹핑하는 것이 좋습니다.

<a name="where-not-clauses"></a>

### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정(negate)할 때 사용할 수 있습니다. 예를 들어, 아래 쿼리는 '할인(clearance) 판매 중이거나 가격이 10 미만인 상품'을 제외한 상품만을 조회합니다.

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

같은 쿼리 조건을 여러 컬럼에 한 번에 적용해야 할 때가 있습니다. 예를 들어, 여러 컬럼 중 하나라도 특정 값과 `LIKE`로 일치하는 모든 레코드를 조회하고 싶을 수 있습니다. 이 경우 `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL로 변환됩니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

이와 비슷하게, `whereAll` 메서드는 지정한 여러 컬럼 모두가 주어진 조건과 일치하는 레코드를 조회할 때 사용할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같은 SQL을 반환합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 여러 컬럼 모두가 특정 조건과 일치하지 않는 레코드를 조회할 때 사용합니다.

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

위 쿼리는 다음과 같은 SQL로 변환됩니다.

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

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스(현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼 쿼리도 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용합니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

`whereJsonContains`와 `whereJsonDoesntContain` 메서드를 사용해 JSON 배열 내 값을 조회할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

만약 MariaDB, MySQL, PostgreSQL 데이터베이스를 사용한다면, `whereJsonContains`와 `whereJsonDoesntContain`에 값 배열을 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한, `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용하여 JSON 키의 존재(또는 부재)를 기준으로 결과를 조회할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, `whereJsonLength` 메서드를 사용하면 JSON 배열의 길이를 기준으로 조회할 수 있습니다.

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

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가합니다. 이 메서드는 데이터베이스 종류에 상관없이 문자열 검색을 할 수 있으며, 대소문자 구분도 설정할 수 있습니다. 기본적으로 문자열 검색은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 사용하여 대소문자 구분 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 조건과 함께 LIKE 조건을 추가합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 "NOT LIKE" 절을 쿼리에 추가합니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`을 사용해 "or" 조건과 함께 NOT LIKE 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> 현재 SQL Server에서는 `whereLike`의 대소문자 구분 검색 옵션이 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 컬럼 값이 전달한 배열 안에 있는지 검증합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 컬럼 값이 주어진 배열 안에 없는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체를 넘길 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 다음과 같은 SQL 쿼리를 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 많은 개수의 정수 배열을 바인딩하여 쿼리에 추가해야 한다면, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 두 값 범위 밖에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 한 컬럼 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 한 컬럼 값이 같은 행의 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 지정한 컬럼의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 컬럼 값이 `NULL`이 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼 값을 날짜와 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 컬럼 값을 특정 월과 비교합니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼 값을 특정 일(day of the month)과 비교합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼 값을 특정 연도와 비교합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼 값을 특정 시간과 비교합니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture` 메서드는 컬럼 값이 과거/미래에 속하는지 확인합니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`와 `whereNowOrFuture` 메서드는 현재 일시를 포함하여 과거/미래 여부를 판단합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 각각 컬럼 값이 오늘, 오늘 이전, 오늘 이후인지 확인합니다.

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

마찬가지로, `whereTodayOrBefore`와 `whereTodayOrAfter`를 사용하면 오늘을 포함하여 이전/이후 여부를 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼 값이 같은지 확인합니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 `whereColumn`에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 비교를 배열로 전달할 수도 있으며, 이 조건들은 모두 `and`로 연결됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화(괄호 그룹핑)

여러 개의 "where" 절을 괄호로 묶어 원하는 논리 그룹을 만들어야 할 때가 있습니다. 특히 `orWhere` 메서드를 사용할 경우, 예기치 않은 쿼리 동작을 방지하기 위해 항상 괄호로 그룹을 만들어야 합니다. 이런 그룹을 만들기 위해서는 `where` 메서드에 클로저를 전달하면 됩니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위처럼 `where` 메서드에 클로저를 전달하면 쿼리 빌더는 괄호 그룹 생성을 시작합니다. 클로저에는 쿼리 빌더 인스턴스가 전달되며, 이 안에서 괄호로 묶고 싶은 조건을 정의할 수 있습니다. 위 쿼리는 다음과 같은 SQL로 변환됩니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프(global scope)가 적용된 경우에도 예기치 않은 동작을 방지하기 위해, 항상 `orWhere` 호출을 괄호로 그룹핑해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. 이 메서드는 클로저를 인수로 받아 쿼리 빌더 인스턴스를 전달하므로, "exists" 절 내부에 들어갈 쿼리를 쉽게 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체를 `whereExists`에 직접 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시는 다음과 같은 SQL 쿼리를 생성합니다.

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

때로는 서브쿼리 결과와 주어진 값을 비교하는 "where" 절이 필요할 때가 있습니다. 이런 경우, `where` 메서드에 클로저와 값을 함께 전달하면 됩니다. 아래 예시는 모든 사용자 중 최근 "membership"이 특정 타입인 사용자를 조회합니다.

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

또는, 컬럼 값을 서브쿼리 결과와 비교하고 싶을 때는 컬럼, 연산자, 클로저를 `where` 메서드에 순서대로 넘기면 됩니다. 아래 예시는 'amount'가 평균값보다 작은 수입 레코드를 모두 조회합니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문(Full Text) Where 절

> [!WARNING]
> 현재 전문(Full Text) Where 절은 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드는 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 생성된 컬럼에 대해 전문 검색 쿼리를 추가할 때 사용할 수 있습니다. 이 메서드들은 라라벨이 사용하는 데이터베이스 시스템에 맞는 적합한 SQL로 변환됩니다. 예를 들어, MariaDB나 MySQL을 사용하는 경우에는 자동으로 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹핑, Limit 및 Offset

<a name="ordering"></a>
### 정렬(주문)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 결과를 지정한 컬럼 기준으로 정렬할 때 사용합니다. 첫 번째 인수는 정렬할 컬럼명이고, 두 번째 인수는 정렬 방향을 나타내며 `asc`(오름차순) 또는 `desc`(내림차순) 중 하나입니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼을 기준으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본값이 오름차순이므로, 내림차순 정렬이 필요할 땐 두 번째 인수에 'desc'를 주거나, `orderByDesc` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

마지막으로, `->` 연산자를 사용해 JSON 컬럼 내부의 값을 기준으로도 정렬할 수 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>

#### `latest` 및 `oldest` 메서드

`latest` 및 `oldest` 메서드를 사용하면 결과를 날짜 기준으로 쉽게 정렬할 수 있습니다. 기본적으로 결과는 테이블의 `created_at` 컬럼을 기준으로 정렬됩니다. 정렬 기준이 되는 컬럼명을 직접 지정할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 이 메서드를 이용해 임의의 사용자를 조회할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 쿼리에 미리 적용된 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드에 컬럼명과 정렬 방식을 인수로 전달하면, 기존에 적용된 모든 "order by" 절을 제거한 뒤 원하는 정렬로 새롭게 지정할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해, `reorderDesc` 메서드를 사용하면 쿼리 결과를 내림차순으로 재정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹핑

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상할 수 있듯이, `groupBy` 및 `having` 메서드를 사용해 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드는 `where` 메서드와 유사한 시그니처를 가지고 있습니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

결과를 특정 범위 내로 필터링하려면 `havingBetween` 메서드를 사용할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인수를 전달하여 여러 컬럼 기준으로 그룹화할 수도 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 조건을 만들고 싶다면 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit와 Offset

`limit` 및 `offset` 메서드를 사용해 쿼리 결과에서 반환되는 결과의 수를 제한하거나, 쿼리 결과에서 특정 개수만큼 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절(Conditional Clauses)

특정 상황에서만 쿼리의 일부 절을 적용하고 싶을 때가 있습니다. 예를 들어, 들어오는 HTTP 요청에서 특정 입력 값이 존재할 때만 `where` 조건을 적용하고 싶을 수 있습니다. 이럴 때는 `when` 메서드를 사용하면 됩니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`로 평가될 때만 전달된 클로저를 실행합니다. 첫 번째 인수가 `false`라면 클로저는 실행되지 않습니다. 즉, 위 예시의 경우 요청에서 `role` 필드가 존재하고 `true`로 평가될 때만 클로저가 실행되어 where 조건이 추가됩니다.

또한, 세 번째 인수로 또 다른 클로저를 전달할 수도 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가될 때만 실행됩니다. 예를 들어 기본 정렬 방식을 설정할 때 이렇게 활용할 수 있습니다.

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

쿼리 빌더에서는 `insert` 메서드를 제공하여 데이터베이스 테이블에 레코드를 삽입할 수 있습니다. `insert` 메서드는 컬럼 이름과 값의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면, 배열의 배열을 전달하면 됩니다. 각 배열은 테이블에 삽입할 한 레코드를 의미합니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드를 삽입할 때 오류를 무시합니다. 이 메서드를 사용할 때는 중복 레코드 에러 등이 무시된다는 점과 데이터베이스 엔진에 따라 다른 유형의 에러도 무시될 수 있음을 알아야 합니다. 예를 들어 `insertOrIgnore`는 [MySQL의 strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 무시하게 됩니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 하위 쿼리를 사용하여 삽입할 데이터를 정한 뒤, 테이블에 새 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 오토 인크리먼트 ID

테이블에 오토 인크리먼트(id 자동 증가) 컬럼이 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입하고 그 ID를 바로 반환받을 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 때 `insertGetId` 메서드는 오토 인크리먼트 컬럼의 이름이 반드시 `id`라고 가정합니다. 다른 "시퀀스" 이름에서 ID를 받아오고 싶다면 해당 컬럼명을 두 번째 인수로 전달해야 합니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 새로운 값으로 업데이트합니다. 첫 번째 인수는 삽입 또는 업데이트할 값들, 두 번째 인수는 테이블 내에서 레코드를 고유하게 식별하는 컬럼(들), 세 번째 인수는 일치하는 레코드가 이미 존재한다면 업데이트할 컬럼들의 배열입니다.

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

위 예시에서 라라벨은 두 레코드를 삽입하려고 시도합니다. 만약 동일한 `departure`, `destination` 컬럼 값을 가진 레코드가 이미 존재하면, 해당 레코드의 `price` 컬럼만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수에 해당하는 컬럼이 반드시 "프라이머리" 또는 "유니크" 인덱스를 가져야 합니다. 또한 MariaDB와 MySQL 드라이버는 `upsert`의 두 번째 인수를 무시하고 테이블의 "프라이머리" 및 "유니크" 인덱스를 사용해 기존 레코드를 판별합니다.

<a name="update-statements"></a>
## Update 구문

데이터를 삽입하는 것 외에도 쿼리 빌더는 `update` 메서드를 통해 기존 레코드를 수정할 수도 있습니다. `update` 메서드는 업데이트할 컬럼명과 값이 쌍으로 구성된 배열을 인수로 받으며, 영향을 받은 행(row)의 수를 반환합니다. `where` 절과 함께 사용해 조건을 지정할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입(Update or Insert)

경우에 따라, 데이터베이스의 기존 레코드를 업데이트하거나, 일치하는 레코드가 없으면 새로 생성하고 싶을 수 있습니다. 이럴 때는 `updateOrInsert` 메서드를 활용할 수 있습니다. 이 메서드는 두 개의 인수를 받습니다. 첫 번째는 레코드를 조회할 조건(컬럼과 값 쌍의 배열), 두 번째는 업데이트할 컬럼과 값 쌍의 배열입니다.

`updateOrInsert` 메서드는 첫 번째 인수에 지정된 조건으로 데이터베이스에서 레코드를 찾고, 존재하면 두 번째 인수의 값으로 업데이트합니다. 해당 레코드를 찾을 수 없다면 두 인수의 속성을 합쳐서 새로운 레코드로 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

또한, `updateOrInsert` 메서드에 클로저를 전달해 일치하는 레코드의 존재 여부에 따라 삽입 또는 업데이트할 속성을 동적으로 조정할 수도 있습니다.

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

JSON 컬럼을 업데이트할 때는, 해당 JSON 객체 내의 키에 접근하려면 `->` 문법을 사용해야 합니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증분 및 감소(Incremnt and Decrement)

쿼리 빌더는 특정 컬럼의 값을 증가 또는 감소시키는 데 유용한 메서드를 제공합니다. 이 메서드들은 최소 한 개의 인수를 받으며, 이는 변경할 컬럼명입니다. 두 번째 인수로 증가/감소할 값을 지정할 수도 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 해당 연산과 동시에 추가로 업데이트할 컬럼도 지정할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach` 및 `decrementEach` 메서드를 이용해 여러 컬럼을 한 번에 증감시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문

쿼리 빌더의 `delete` 메서드를 통해 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행의 수를 반환합니다. `delete`를 호출하기 전에 "where" 절을 추가하여 삭제 범위를 제한할 수도 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 `select` 구문을 실행할 때 "비관적 잠금"을 위한 몇 가지 기능을 제공합니다. "공유 잠금(shared lock)"을 실행하려면 `sharedLock` 메서드를 사용할 수 있습니다. 공유 잠금은 선택된 행이 트랜잭션이 완료될 때까지 다른 트랜잭션에서 수정되지 않도록 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate` 메서드를 사용할 수도 있습니다. "FOR UPDATE" 잠금은 선택된 레코드가 다른 트랜잭션에 의해 수정되거나, 공유 잠금으로 선택되는 것을 막습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금을 사용할 때는 [트랜잭션](/docs/12.x/database#database-transactions)으로 감싸는 것이 권장됩니다. 이렇게 하면 전체 작업이 완료될 때까지 데이터가 변경되지 않도록 보장할 수 있습니다. 만약 작업 도중 실패하면, 트랜잭션이 롤백되며 잠금도 자동으로 해제됩니다.

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
## 재사용 가능한 쿼리 구성 요소

애플리케이션 전반에 반복해서 사용되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 사용해 로직을 재사용 가능한 객체로 추출할 수 있습니다. 예를 들어, 아래처럼 두 쿼리에서 동일한 목적의 필터링이 반복적으로 사용된다고 가정해 봅니다.

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

이러한 목적의 필터링 부분만 별도의 객체로 추출해 재사용할 수 있습니다.

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

그 다음, 쿼리 빌더의 `tap` 메서드로 이 객체의 로직을 쿼리에 적용할 수 있습니다.

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
#### Query Pipe

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 만약 쿼리를 실행하고 다른 값을 반환하는 객체로 추출하고 싶다면, 대신 `pipe` 메서드를 사용할 수 있습니다.

아래는 애플리케이션 곳곳에서 공통적으로 사용되는 [페이지네이션](/docs/12.x/pagination) 로직을 공유하기 위해 정의한 쿼리 객체 예시입니다. `DestinationFilter`가 쿼리 빌더에 조건만 적용하는 것과 달리, `Paginate` 객체는 쿼리를 실행해 paginator 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 활용해, 이 객체로 공통 페이지네이션 로직을 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하는 과정에서 `dd` 및 `dump` 메서드를 사용해 현재 쿼리의 바인딩 값과 SQL을 출력할 수 있습니다. `dd` 메서드는 디버그 정보를 보여준 뒤 요청을 종료합니다. 반면 `dump` 메서드는 디버그 정보만 출력하고, 요청 처리는 이어집니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드를 호출하면 쿼리의 SQL과 모든 파라미터 바인딩 값이 실제로 치환된 형태로 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```