# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 덩어리로 가져오기](#chunking-results)
    - [결과를 지연 스트리밍으로 가져오기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 절](#where-any-all-none-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리적 그룹핑](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
    - [전체 텍스트 WHERE 절](#full-text-where-clauses)
- [정렬, 그룹핑, LIMIT & OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [LIMIT & OFFSET](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 문](#insert-statements)
    - [Upserts](#upserts)
- [UPDATE 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [DELETE 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 만들고 실행할 수 있는 편리하고 유연한 인터페이스를 제공합니다. 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 때 사용할 수 있으며, 라라벨이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

라라벨 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 애플리케이션을 SQL 인젝션 공격으로부터 보호합니다. 쿼리 빌더에 전달하는 문자열 바인딩을 따로 정제하거나 필터링할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명(예: "order by" 컬럼 포함)에 사용자 입력값이 직접 전달되도록 절대로 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드에서 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 지정된 테이블을 위한 플루언트 쿼리 빌더 인스턴스를 반환하여, 쿼리에 다양한 조건을 체이닝하고 마지막에 `get` 메서드로 최종 결과를 조회할 수 있습니다.

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

`get` 메서드는 쿼리 결과가 담긴 `Illuminate\Support\Collection` 인스턴스를 반환하며, 결과 각각은 PHP의 `stdClass` 객체입니다. 각 컬럼의 값은 객체의 속성으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨 컬렉션은 데이터 매핑과 집계에 매우 강력한 다양한 메서드를 제공합니다. 라라벨 컬렉션에 대해 더 알고 싶다면 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 또는 컬럼 조회하기

데이터베이스 테이블에서 한 행만 조회하면 되는 경우, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

쿼리 결과가 없을 때 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 잡히지 않으면, 자동으로 404 HTTP 응답이 클라이언트에 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아닌, 특정 컬럼의 값만 필요하다면 `value` 메서드로 원하는 컬럼의 값을 바로 추출할 수 있습니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 찾으려면 `find` 메서드를 사용하면 됩니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값들만 포함하는 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 아래는 사용자들의 title 목록을 컬렉션으로 가져오는 예시입니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인수로 컬렉션의 키로 사용할 컬럼명을 지정할 수도 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 덩어리로 가져오기

수천 개의 데이터베이스 레코드를 다뤄야 한다면, `DB` 파사드에서 제공하는 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 한 번에 작은 조각씩 가져와서, 각 덩어리를 콜백(클로저)에 전달하여 처리하도록 해줍니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 나눠서 처리할 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가로 남은 덩어리의 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

결과를 `chunk`로 나누어 처리하면서 동시에 레코드를 업데이트한다면, 쿼리 결과가 예기치 않게 바뀔 수 있습니다. 이렇게 레코드를 갱신하는 경우에는 반드시 `chunkById` 메서드를 사용하는 것이 안전합니다. 이 메서드는 해당 레코드의 기본키를 기준으로 자동으로 결과를 페이지네이션합니다.

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

`chunkById`와 `lazyById` 메서드는 쿼리에 자동으로 자체 "where" 조건을 추가하므로, 직접 추가하는 조건들은 [논리적으로 그룹핑](#logical-grouping)하여 사용하는 것이 좋습니다.

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
> chunk 콜백 내에서 레코드를 업데이트하거나 삭제할 때, 기본키나 외래키가 변경되면 chunk 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 덩어리 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍으로 가져오기

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 쿼리를 일정 크기로 나누어 실행하지만, 각 덩어리를 콜백에 넘기는 대신 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환해 하나의 스트림처럼 결과를 다룰 수 있게 합니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복하면서 조회한 결과로 레코드를 갱신할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 더 안전합니다. 이 메서드는 레코드의 기본키를 기준으로 자동으로 결과를 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복처리 중에 레코드를 업데이트하거나 삭제하면, 기본키 또는 외래키 변경으로 인해 chunk 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 다양한 집계 함수 메서드를 제공합니다. 쿼리를 만든 후에 해당 집계 메서드를 바로 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 값을 더욱 정밀하게 계산하려면 다른 조건절과 함께 사용할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

조회 조건에 맞는 레코드의 유무를 단순히 확인할 때는 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT 문

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정하기

데이터베이스 테이블의 모든 컬럼을 다 조회하지 않고 일부만 선택하고 싶다면, `select` 메서드로 쿼리의 "SELECT" 절을 직접 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리가 중복 없는 결과만 반환하도록 할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고 여기에 컬럼을 추가하고 싶을 때는, `addSelect` 메서드를 사용하면 됩니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

특정 쿼리에 임의의 문자열을 삽입해야 할 때, `DB` 파사드에서 제공하는 `raw` 메서드로 Raw 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 문장은 쿼리에 문자열로 그대로 삽입되므로, SQL 인젝션 취약점이 생기지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신, 다양한 쿼리 부분에 Raw 표현식을 삽입할 수 있는 아래 메서드들을 사용할 수 있습니다. **Raw 표현식을 사용하는 쿼리는 라라벨이 SQL 인젝션으로부터 안전함을 보장할 수 없다는 점을 꼭 유념하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))`와 같은 역할을 하며, 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 Raw "where" 절을 삽입하는 데 사용할 수 있으며, 두 번째 인수로 바인딩 배열을 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절의 값으로 Raw 문자열을 전달할 때 사용할 수 있습니다. 이 메서드들 역시 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 Raw 문자열을 전달할 때 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 Raw 문자열을 사용할 때 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### INNER JOIN 절

쿼리 빌더로 쿼리에 조인 절을 추가할 수도 있습니다. 기본적인 "INNER JOIN"을 하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용합니다. 첫 번째 인수는 조인할 테이블명, 이후 인수는 조인을 위한 컬럼 조건을 지정합니다. 한 쿼리 내에서 여러 테이블을 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### LEFT JOIN / RIGHT JOIN 절

"INNER JOIN" 대신 "LEFT JOIN"이나 "RIGHT JOIN"을 하려면, `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 메서드 시그니처는 `join`과 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### CROSS JOIN 절

"CROSS JOIN"을 수행하려면 `crossJoin` 메서드를 사용합니다. Cross Join은 첫 번째 테이블과 조인하는 테이블 간의 데카르트 곱을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 JOIN 절

더 복잡한 조인 조건을 지정하려면, `join` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 "join" 절의 조건을 세밀하게 정의할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 절을 사용하려면, `JoinClause` 인스턴스의 `where`와 `orWhere` 메서드를 사용할 수 있습니다. 이 경우에는 두 컬럼 비교가 아니라, 컬럼과 값을 비교합니다.

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드로 서브쿼리를 조인할 수 있습니다. 각각의 메서드는 세 가지 인수(서브쿼리, 테이블 별칭, 연관 컬럼을 정의하는 클로저)를 받습니다. 아래 예시는 각 사용자 레코드에 해당 사용자의 최근 게시글 생성일을 포함하는 결과를 가져오는 예입니다.

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
> Lateral 조인은 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서만 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용해 "lateral join"을 서브쿼리와 수행할 수 있습니다. 각각의 메서드는 서브쿼리와 별칭 두 개의 인수를 받으며, 조인 조건은 서브쿼리 내의 `where` 절에 지정해야 합니다. Lateral 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

예를 들어, 각 사용자의 최근 블로그 포스트 3개와 함께 사용자 목록을 조회하는 쿼리는 아래와 같습니다. 각 사용자는 최대 3개의 최근 게시글(행)을 가질 수 있습니다. 조인 조건은 서브쿼리 내부에서 `whereColumn` 절로 지정합니다.

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
## 유니온

쿼리 빌더는 여러 쿼리를 "유니온"으로 결합하는 편리한 방법도 제공합니다. 처음에 쿼리를 만들고, 그 쿼리를 `union` 메서드로 다른 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도, 쿼리 결과의 중복을 제거하지 않는 `unionAll` 메서드도 지원합니다. `unionAll`의 사용법은 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드로 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 `where` 호출에는 세 개의 인수가 필요합니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스가 지원하는 모든 연산자 사용 가능), 세 번째는 컬럼의 값과 비교할 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼이 `100`이고, `age` 컬럼이 `35`보다 큰 사용자만 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

만약 특정값이 `=`인지 검증하고 싶고, 연산자를 직접 지정하고 싶지 않다면, 두 번째 인수로 값을 전달하면 라라벨이 자동으로 `=` 연산자를 적용합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

앞서 언급했듯이, 데이터베이스 시스템이 지원하면 어떤 연산자든 사용할 수 있습니다.

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

여러 조건을 한 번에 배열로 전달하여 `where` 메서드에 전부 적용할 수도 있습니다. 배열의 각 요소는 세 개의 인수를 가진 배열이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명(예: "order by" 컬럼 포함)에 사용자 입력값이 직접 전달되도록 절대로 허용해서는 안 됩니다.

> [!WARNING]
> MySQL과 MariaDB에서는 문자열-숫자 비교에서 문자열이 자동으로 정수로 타입캐스팅됩니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되기 때문에, 의도하지 않은 결과가 발생할 수 있습니다. 예를 들어, 테이블의 `secret` 컬럼 값이 `aaa`인 경우, `User::where('secret', 0)`을 실행하면 해당 행이 조회됩니다. 이를 방지하려면 모든 값이 쿼리에 사용되기 전에 적절한 타입으로 변환되어 있는지 확인하세요.

<a name="or-where-clauses"></a>
### OR WHERE 절

`where` 메서드를 체이닝하면 조건이 모두 `and` 연산자로 연결됩니다. 하지만 `or` 조건으로 연결하고 싶다면 `orWhere` 메서드를 사용할 수 있습니다. `orWhere`의 인수는 `where`와 동일합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 묶인 `or` 조건을 만들고 싶다면, 첫 번째 인수로 클로저를 전달할 수 있습니다.

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
> `orWhere` 호출 시, 전역 스코프가 적용되는 경우 예기치 않은 동작을 막기 위해 항상 괄호로 그룹핑하는 것이 좋습니다.

<a name="where-not-clauses"></a>

### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정(negate)할 때 사용할 수 있습니다. 예를 들어, 아래 쿼리는 특가 상품이거나 가격이 10 미만인 상품을 제외합니다.

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

여러 컬럼에 동일한 조건을 적용해야 할 때가 있습니다. 예를 들어, 주어진 컬럼 목록 중 하나라도 특정 값과 `LIKE` 연산을 만족하는 모든 레코드를 조회하고 싶을 수 있습니다. 이럴 때는 `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

마찬가지로, `whereAll` 메서드는 주어진 컬럼 모두가 특정 조건을 만족하는 레코드를 조회할 때 사용할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 컬럼들 중 어느 것도 조건을 만족하지 않는 레코드를 조회할 때 사용할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL을 생성합니다.

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼에 대한 쿼리도 지원합니다. 현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+에서 지원합니다. JSON 컬럼을 조회하려면 `->` 연산자를 사용하세요.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

`whereJsonContains`를 사용해서 JSON 배열을 조회할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL 데이터베이스를 사용하는 경우, `whereJsonContains` 메서드에 여러 값의 배열을 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

JSON 배열의 길이로 조회하려면 `whereJsonLength` 메서드를 사용할 수 있습니다.

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

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가할 수 있도록 해줍니다. 이 메서드들은 데이터베이스 종류에 상관없이 문자열 매칭 쿼리를 작성할 수 있고, 대소문자 구분을 설정할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 사용하여 대소문자를 구분하는 검색을 할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 LIKE 조건으로 "or" 절을 추가합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 "NOT LIKE" 절을 쿼리에 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`를 사용하면 NOT LIKE 조건을 가진 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 컬럼 값이 주어진 배열에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 주어진 컬럼 값이 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인자로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 아래와 같은 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 정수 배열을 바인딩해야 하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 두 값의 범위 밖에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 한 컬럼의 값이 동일한 행의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 한 컬럼의 값이 동일한 행의 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 주어진 컬럼 값이 `NULL`인지 확인합니다.

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

`whereDate` 메서드는 컬럼의 값이 특정 날짜와 같은지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 컬럼의 값이 특정 월(month)에 해당하는지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼의 값이 날짜의 특정 일(day)과 같은지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼의 값이 특정 연도(year)에 해당하는지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼의 값이 특정 시간(time)과 같은지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture` 메서드는 컬럼 값이 과거인지, 미래인지 판별할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast` 및 `whereNowOrFuture` 메서드는 컬럼 값이 과거나 미래인지(현재 날짜/시간도 포함) 판별할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 각각 컬럼 값이 오늘/오늘 이전/오늘 이후인지 판단할 때 사용할 수 있습니다.

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

마찬가지로, `whereTodayOrBefore` 및 `whereTodayOrAfter` 메서드는 컬럼 값이 오늘 이전인지, 오늘 이후인지(오늘을 포함) 판단할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼의 값이 같은지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

`whereColumn` 메서드에 비교 연산자를 함께 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 비교를 배열로 전달해 여러 조건을 한 번에 만들 수 있으며, 이 조건들은 `and`로 연결됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화

여러 `where` 절을 괄호로 묶어서 논리적으로 그룹핑해야 할 때가 있습니다. 실제로, `orWhere` 메서드를 사용할 때는 원하지 않는 쿼리 동작을 방지하기 위해 보통 괄호 그룹을 반드시 사용하는 것이 좋습니다. 이를 위해 `where` 메서드에 클로저를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

이처럼, `where` 메서드에 클로저를 전달하면 쿼리 빌더는 그룹 제약조건을 시작하게 됩니다. 이 클로저는 쿼리 빌더 인스턴스를 받아, 괄호로 묶을 조건들을 설정할 수 있습니다. 위 예시는 다음과 같은 SQL을 만듭니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용될 때 원치 않는 동작을 피하기 위해 항상 `orWhere` 호출을 그룹핑해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. 이 메서드는 클로저를 인수로 받아, 클로저에 쿼리 빌더 인스턴스를 전달하여 "exists" 절 안에 들어갈 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체를 그대로 `whereExists`에 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시는 모두 다음과 같은 SQL을 생성합니다.

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

때로는 서브쿼리 결과를 특정 값과 비교하는 "where" 절을 만들어야 할 때가 있습니다. 이럴 때는 `where` 메서드에 클로저와 비교 값을 함께 전달하면 됩니다. 예를 들어 아래 쿼리는 지정 타입의 최근 "membership"이 있는 모든 사용자를 조회합니다.

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

또는, 컬럼 값을 서브쿼리 결과와 비교해야 할 수도 있습니다. 이 경우, `where` 메서드에 컬럼, 연산자, 클로저를 전달하면 됩니다. 아래는 수입 내역(amount)이 평균보다 작은 모든 income 레코드를 조회하는 예시입니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문(Full Text) 검색 Where 절

> [!WARNING]
> 전문 검색(where full text) 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드를 사용하면 [전체텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 지정된 컬럼에 대해 전문 검색 Where 절을 추가할 수 있습니다. 이 메서드들은 라라벨이 내부적으로 데이터베이스 시스템에 맞는 SQL로 변환합니다. MariaDB나 MySQL을 사용할 경우 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit, Offset

<a name="ordering"></a>
### 정렬(Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 지정 컬럼 기준으로 정렬할 수 있게 해줍니다. 첫 번째 인수는 정렬할 컬럼명을, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)을 지정합니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향 지정은 생략 가능하며, 지정하지 않으면 기본값으로 오름차순(asc)입니다. 만약 내림차순(desc)으로 정렬하려면 두 번째 인자를 지정하거나 `orderByDesc`를 사용할 수도 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest`, `oldest` 메서드

`latest`, `oldest` 메서드를 이용하면 날짜를 기준으로 손쉽게 정렬할 수 있습니다. 기본적으로 테이블의 `created_at` 컬럼을 기준으로 정렬합니다. 별도의 정렬 기준 컬럼명을 지정할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬(Random Ordering)

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의의 사용자 한 명을 조회할 때 사용할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>

#### 기존 정렬 제거하기

`reorder` 메서드는 쿼리에 미리 적용되어 있던 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드 호출 시 컬럼명과 정렬 방향을 전달하면, 기존의 모든 "order by" 절을 제거하고 완전히 새로운 정렬 기준을 적용할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해, `reorderDesc` 메서드를 사용하면 쿼리 결과를 내림차순으로 바로 정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화(Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상하셨겠지만, `groupBy`와 `having` 메서드를 사용하여 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 시그니처는 `where` 메서드와 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하면 특정 구간 내의 결과만 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인자를 전달하면, 여러 컬럼을 기준으로 그룹화할 수도 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

보다 복잡한 `having` 문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

`limit` 및 `offset` 메서드를 사용하여 쿼리 결과의 반환 개수를 제한하거나, 지정한 개수만큼 결과를 건너뛰도록 할 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 사용하기

특정 조건에 따라 쿼리 절을 적용하고 싶을 때가 있습니다. 예를 들어, 입력값이 HTTP 요청에 존재할 때만 `where` 절을 추가하고 싶을 수 있습니다. 이런 경우 `when` 메서드를 사용하면 가능합니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 전달값이 `true`일 때만 주어진 클로저를 실행합니다. 첫 번째 인자가 `false`면 클로저는 실행되지 않습니다. 위 예제에서 `when` 메서드에 전달된 클로저는 들어오는 요청의 `role` 필드가 존재하며 그 값이 true로 평가될 때만 호출됩니다.

`when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인자가 `false`로 평가될 때만 실행됩니다. 아래 예제에서는 이 기능을 활용해 쿼리의 기본 정렬방식을 조건적으로 설정합니다.

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

쿼리 빌더에서는 레코드를 데이터베이스 테이블에 삽입할 때 사용할 수 있는 `insert` 메서드를 제공합니다. `insert` 메서드는 컬럼명과 값의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

배열의 배열을 전달해 여러 레코드를 한 번에 삽입할 수도 있습니다. 각 배열이 삽입될 하나의 레코드를 의미합니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드를 사용하면 레코드를 삽입할 때 에러를 무시합니다. 이 메서드를 사용할 때는 중복 레코드 관련 에러뿐만 아니라, 데이터베이스 엔진에 따라 기타 에러도 무시될 수 있음을 주의해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리의 결과를 이용해 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블이 auto-increment(자동 증가) id 컬럼을 가지고 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입하고 그 id 값을 즉시 받아올 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 때 `insertGetId` 메서드는 자동 증가 컬럼명이 반드시 `id`라고 가정합니다. 만약 다른 "시퀀스"에서 id를 가져오고 싶다면, 컬럼명을 두 번째 파라미터로 전달할 수 있습니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 업데이트해줍니다. 첫 번째 인자는 삽입 또는 업데이트할 값 배열이고, 두 번째 인자에는 레코드의 고유성을 결정할 컬럼명을 넘깁니다. 세 번째 인자에는 중복 레코드가 있을 때 업데이트할 컬럼 목록을 배열로 전달합니다.

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

위 예제에서는 두 개의 레코드를 삽입하려고 시도합니다. 만약 동일한 `departure` 및 `destination` 값을 가진 레코드가 이미 존재한다면, 해당 레코드의 `price` 컬럼만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는, `upsert` 메서드의 두 번째 인자인 컬럼들이 "primary" 또는 "unique" 인덱스를 가져야 합니다. 추가로, MariaDB와 MySQL 드라이버는 두 번째 인자를 무시하고, 항상 테이블의 "primary"와 "unique" 인덱스를 활용해 기존 레코드의 존재 여부를 판단합니다.

<a name="update-statements"></a>
## Update 구문

데이터베이스에 레코드를 삽입하는 것뿐 아니라, 쿼리 빌더를 사용해 이미 존재하는 레코드도 `update` 메서드로 업데이트할 수 있습니다. `update` 메서드 역시 업데이트할 컬럼과 값을 배열로 전달합니다. 이 메서드는 영향을 받은 행의 개수를 반환합니다. 업데이트 쿼리에는 `where` 절로 대상 레코드를 제한할 수도 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 조건부 Update 또는 Insert

때로는 데이터베이스에 해당하는 레코드가 존재하면 업데이트, 존재하지 않으면 새로 생성해야 할 때가 있습니다. 이 경우 `updateOrInsert` 메서드를 사용하면 됩니다. 이 메서드는 2개의 인자를 받습니다. 첫 번째는 찾고자 하는 조건의 컬럼-값 배열, 두 번째는 업데이트할 컬럼-값 배열입니다.

`updateOrInsert` 메서드는 첫 번째 인자에 해당하는 조건으로 레코드를 검색합니다. 해당 레코드가 있으면 두 번째 인자의 값으로 업데이트하고, 없으면 두 인자를 합친 속성으로 새 레코드를 생성합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

레코드 존재 여부에 따라 데이터베이스에 저장될 속성을 클로저로 세밀하게 커스터마이즈할 수도 있습니다.

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

JSON 컬럼을 업데이트할 때는 `->` 문법을 이용해 JSON 객체 내의 특정 키를 업데이트할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가/감소 (Increment & Decrement)

쿼리 빌더에서는 지정한 컬럼의 값을 쉽게 증가시키거나 감소시킬 수 있는 편리한 메서드를 제공합니다. 이 두 메서드는 적어도 한 개 이상의 인자를 받으며, 반드시 조작할 컬럼명을 명시해야 합니다. 두 번째 인자를 지정하면 얼마만큼 증가(감소)시킬지 수치를 전달할 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면 증가/감소와 동시에 추가로 다른 컬럼도 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach`와 `decrementEach` 메서드를 사용해 여러 컬럼을 한 번에 증가시키거나 감소시킬 수 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문

쿼리 빌더의 `delete` 메서드를 사용하여 테이블에서 레코드를 삭제할 수 있습니다. `delete`는 영향을 받은 행의 수를 반환합니다. 삭제 작업을 위해 `delete` 메서드 호출 전에 "where" 절을 추가해 대상을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더에서는 `select` 실행 시 "비관적 잠금"을 지원하는 몇 가지 메서드를 제공합니다. "공유 잠금(shared lock)"을 실행하려면 `sharedLock` 메서드를 사용하면 됩니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행의 변경을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate` 메서드를 사용할 수도 있습니다. "for update" 잠금은 선택된 레코드가 공유 잠금으로 선택되거나 변경되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

필수 사항은 아니지만, 비관적 잠금은 [트랜잭션](/docs/12.x/database#database-transactions) 안에서 활용하는 것이 권장됩니다. 이렇게 하면 전체 작업이 완료될 때까지 데이터베이스의 데이터가 변경되지 않고 유지됩니다. 만약 실패 발생 시 트랜잭션은 모든 변경 사항을 자동으로 롤백하고, 잠금도 해제됩니다.

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

애플리케이션 전반에 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 사용해 해당 로직을 재사용 가능한 객체로 분리할 수 있습니다. 예를 들어, 아래처럼 서로 다른 두 쿼리에서 동일한 목적의 필터링이 사용되고 있다고 가정해보겠습니다.

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

공통적으로 사용되는 목적지(destination) 필터링 부분을 재사용 가능한 객체로 추출할 수 있습니다.

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

이제 쿼리 빌더의 `tap` 메서드를 사용해, 해당 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더 자체를 반환합니다. 만약 쿼리를 실행해서 다른 결과 값을 반환하는 오브젝트로 추출하고 싶다면 `pipe` 메서드를 사용할 수 있습니다.

다음 예제처럼, 애플리케이션 전역에서 공통적으로 사용하는 [페이지네이션](/docs/12.x/pagination) 로직을 갖는 쿼리 오브젝트가 있다고 가정해보겠습니다. `DestinationFilter`와 달리, `Paginate` 객체는 쿼리 조건을 쿼리에 더하는 것이 아니라 쿼리를 실행해서 페이지네이터 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용해, 위 객체를 통해 공용 페이지네이션 로직을 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅(Debugging)

쿼리를 작성하는 도중, `dd`와 `dump` 메서드를 사용해 현재 쿼리의 바인딩과 SQL을 즉시 출력할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 후 즉시 요청 처리를 중지하고, `dump` 메서드는 출력만 하며 요청 처리를 계속합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드를 사용하면, 쿼리의 SQL 문에 모든 파라미터 바인딩이 실제 값으로 치환된 형태를 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```