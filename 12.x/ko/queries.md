# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청킹 처리하기](#chunking-results)
    - [결과를 게으르게 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [유니언(Union)](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 절](#where-any-all-none-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
    - [전문검색(Full Text) WHERE 절](#full-text-where-clauses)
- [정렬, 그룹핑, LIMIT과 OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [LIMIT과 OFFSET](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT문](#insert-statements)
    - [Upserts](#upserts)
- [UPDATE문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가/감소 처리](#increment-and-decrement)
- [DELETE문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅(Debugging)](#debugging)

<a name="introduction"></a>
## 소개

라라벨의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 유연하게 작성하고 실행할 수 있게 해주는 유용한 인터페이스를 제공합니다. 이 쿼리 빌더는 애플리케이션 내 대부분의 데이터베이스 작업을 수행할 수 있으며, 라라벨이 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

라라벨의 쿼리 빌더는 PDO의 파라미터 바인딩 기능을 사용하므로, SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호할 수 있습니다. 쿼리 빌더에 전달하는 문자열 인자를 별도로 정제하거나 이스케이프 처리할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자가 입력한 값을 쿼리 내 컬럼명(예: "order by" 컬럼)으로 사용하는 것은 절대 피해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 조회하기

쿼리를 시작하려면 `DB` 파사드가 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하며, 여기에 추가적으로 제약 조건을 체이닝한 뒤 마지막에 `get` 메서드를 사용하여 결과를 가져올 수 있습니다.

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

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체로 표현됩니다. 각 컬럼의 값은 객체의 속성처럼 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨의 컬렉션은 데이터를 매핑하거나 집계하는 데 매우 강력한 다양한 메서드를 제공합니다. 컬렉션에 대한 더 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회하기

데이터베이스 테이블에서 하나의 행만 조회하고 싶을 때는 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 원하는 행이 존재하지 않을 때 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면, `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException` 예외가 잡히지 않으면, 라라벨은 자동으로 클라이언트에 404 HTTP 응답을 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 하나의 값만 얻고 싶을 경우, `value` 메서드를 사용할 수 있습니다. 이 메서드는 해당 컬럼의 값만 바로 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 조회하고 싶을 때는 `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

하나의 컬럼 값들만 담은 `Illuminate\Support\Collection` 인스턴스를 받고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 아래 예시는 사용자의 직함(title)만 컬렉션으로 가져옵니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

조회할 컬렉션의 key로 사용할 컬럼을 두 번째 인자로 지정할 수도 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청킹 처리하기

수천 건의 데이터베이스 레코드를 다뤄야 한다면, `DB` 파사드가 제공하는 `chunk` 메서드 사용을 고려해보세요. 이 메서드는 한 번에 일정 크기의 결과 집합만 가져와서, 각 청크를 클로저로 전달해 처리하도록 해줍니다. 예를 들어, `users` 테이블 전체를 한 번에 100건씩 나누어 가져올 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청킹 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청킹 처리 중 결과를 업데이트하는 경우, 예상치 못한 결과가 발생할 수 있습니다. 청킹하면서 조회한 레코드를 업데이트할 계획이라면, 항상 `chunkById` 메서드를 사용하는 것이 안전합니다. 이 메서드는 자동으로 레코드의 기본키를 기준으로 페이지네이션하여 결과를 청킹합니다.

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

`chunkById`와 `lazyById` 메서드는 실행되는 쿼리에 자체적으로 "where" 조건을 추가하기 때문에, [논리 그룹화](#logical-grouping)가 필요한 경우 별도의 클로저로 그룹화하는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 수정하거나 삭제할 때, 기본키 또는 외래키 값이 변경되면 쿼리 결과에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청킹 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 게으르게 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백으로 넘기는 대신 [LazyCollection](/docs/12.x/collections#lazy-collections)으로 반환하여 전체 결과를 스트림처럼 다룰 수 있게 해줍니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

조회된 레코드를 반복(iterate)하며 업데이트할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드는 레코드의 기본키를 기준으로 자동으로 페이지네이션 처리합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 처리 중에 레코드를 수정(업데이트)하거나 삭제하는 경우, 기본키 또는 외래키 값이 변경되면 쿼리 결과에 영향을 줄 수 있으니 주의해야 합니다. 이로 인해 일부 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 함수도 제공합니다. 쿼리를 작성한 후 이 메서드들을 바로 호출할 수 있습니다.

```php
use Illuminate\Support\Facades.DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 함수 호출 전에 조건절을 추가하여 계산 대상을 세밀하게 지정할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리 제약 조건에 맞는 레코드가 존재하는지 판단할 때, `count` 메서드 대신 `exists` 혹은 `doesntExist` 메서드를 사용할 수도 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT문

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정하기

데이터베이스 테이블의 모든 컬럼을 선택하지 않고, 원하는 컬럼만 지정하고 싶다면 `select` 메서드를 사용할 수 있습니다. 이 메서드로 커스텀 SELECT 절을 명확하게 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리 결과에 중복이 있는 경우 중복 없이 반환합니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스를 가지고 있고, 여기에 컬럼을 추가로 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때로는 쿼리에 임의의 문자열을 넣어야 할 때가 있습니다. 이럴 때는 `DB` 파사드가 제공하는 `raw` 메서드를 활용해 Raw 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 바로 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 반드시 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 관련 메서드

`DB::raw`를 사용하는 대신 아래와 같은 메서드들을 이용해 쿼리의 여러 부분에 Raw 표현식을 삽입할 수 있습니다. **Raw 표현식이 사용된 쿼리는 라라벨이 SQL 인젝션 취약점으로부터 안전하다고 보증할 수 없으므로 각별히 주의해야 합니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인자로 바인딩 파라미터의 배열을 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 Raw "where" 절을 삽입할 때 사용합니다. 두 번째 인자로 바인딩 배열을 넘길 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드를 사용하면 "having" 절에 Raw 문자열을 직접 지정할 수 있습니다. 이 메서드들도 두 번째 인자로 바인딩 배열을 전달받습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 Raw 문자열을 사용할 때 쓸 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 Raw 문자열을 지정할 때 사용할 수 있습니다.

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

쿼리 빌더는 쿼리에 다양한 join 절도 추가할 수 있습니다. 기본적인 "inner join"을 수행하려면 쿼리 빌더 인스턴스의 `join` 메서드를 사용하세요. 첫 번째 인자는 조인할 테이블 이름이고, 나머지 인자들은 조인 조건(컬럼을 기준으로 매칭)을 지정합니다. 하나의 쿼리에서 여러 테이블을 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades.DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 절

"inner join" 대신 "left join" 또는 "right join"을 사용하고 싶다면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이 메서드들은 `join` 메서드와 사용법이 동일합니다.

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

"cross join"을 수행하고자 할 때는 `crossJoin` 메서드를 사용하면 됩니다. 크로스 조인은 두 테이블의 데카르트 곱(카티션 곱)을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

좀 더 복잡한 join 조건을 지정하고 싶을 때는, `join` 메서드의 두 번째 인자로 클로저를 넘기면 됩니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 "join" 절의 제약 조건을 세부적으로 설정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

join 조건에 "where" 절을 사용하고자 할 때는 `JoinClause` 인스턴스가 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이때는 두 컬럼을 비교하는 대신, 컬럼과 값을 비교합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 Join

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리와 서브쿼리를 조인할 수 있습니다. 각 메서드는 세 개의 인자를 받는데, 첫 번째는 서브쿼리, 두 번째는 해당 서브쿼리의 테이블 별칭(alias), 세 번째는 연관 컬럼을 지정하는 클로저입니다. 아래 예제에서는 각 사용자 레코드에 사용자의 가장 최근 포스팅의 `created_at` 값을 포함한 결과를 조회합니다.

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
#### Lateral Join

> [!WARNING]
> Lateral 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원됩니다.

`joinLateral`와 `leftJoinLateral` 메서드를 사용하면 서브쿼리와 함께 "lateral join"을 수행할 수 있습니다. 각 메서드는 두 개의 인자를 받는데, 첫 번째는 서브쿼리, 두 번째는 테이블 별칭입니다. 조인 조건은 해당 서브쿼리의 `where` 절 내에서 지정해야 하며, lateral 조인은 각 행마다 개별적으로 평가되어 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

다음 예시에서는 사용자 정보와 함께 각 사용자의 최근 블로그 포스트 3개씩 조회합니다. 각 사용자는 최대 3개의 행이 결과 집합에 나타날 수 있습니다(각 포스트마다 하나씩). 조인 조건은 서브쿼리 내부의 `whereColumn` 절에서 현재 사용자 행을 참조하여 지정합니다.

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
## 유니언(Union)

쿼리 빌더는 "union"을 활용해 둘 이상의 쿼리를 쉽게 합칠 수 있는 `union` 메서드도 제공합니다. 예를 들어, 초기 쿼리를 작성한 후 `union` 메서드로 추가 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드를 제공합니다. `unionAll`로 조합된 쿼리는 중복 결과가 제거되지 않으며, 메서드 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용하면 쿼리에 WHERE 조건을 추가할 수 있습니다. 가장 단순한 형태의 `where` 메서드는 세 개의 인자를 받습니다. 첫 번째 인자는 컬럼명, 두 번째는 데이터베이스에서 지원하는 연산자, 세 번째는 비교할 값입니다.

예를 들어, `votes` 컬럼이 `100` 이고 `age` 컬럼이 `35` 초과인 사용자를 조회하려면 아래와 같이 쿼리를 작성합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

만약 컬럼이 주어진 값과 `=`(같음)인지 확인만 하고 싶다면, 두 번째 인자로 값을 바로 전달할 수 있습니다. 라라벨은 자동으로 `=` 연산자를 사용합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

이미 언급한 것처럼, 데이터베이스가 지원하는 여러 연산자를 사용할 수도 있습니다.

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

조건을 여러 개 배열로 전달해서 한 번에 지정할 수도 있습니다. 배열의 각 요소는 `where` 메서드에서 일반적으로 전달하는 세 개의 인자를 순서대로 포함해야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자의 입력값이 쿼리의 컬럼명(특히 "order by" 컬럼)을 결정하게 해서는 절대 안 됩니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교에서 문자열을 자동으로 정수로 변환합니다. 이때 숫자가 아닌 문자열은 `0`으로 처리되어 예상치 않은 결과가 발생할 수 있습니다. 예를 들어, 테이블의 `secret` 컬럼에 값이 `aaa`인 행이 있고, `User::where('secret', 0)`을 실행하면 해당 행이 조회됩니다. 이러한 문제를 피하려면 쿼리 전에 모든 값을 반드시 적절한 타입으로 변환하세요.

<a name="or-where-clauses"></a>
### OR WHERE 절

쿼리 빌더의 `where` 메서드를 연속해서 체이닝 하면, 조건들은 `and` 연산자로 묶입니다. 하지만, `orWhere` 메서드를 사용하면 조건을 `or` 연산자로 추가할 수 있습니다. `orWhere`는 `where`와 동일한 인자를 받습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 묶인 `or` 조건 그룹이 필요하다면 첫 번째 인자로 클로저를 전달하면 됩니다.

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

위 예시는 다음과 같은 SQL이 생성됩니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예상치 못한 동작을 방지하려면 `orWhere` 조건은 항상 그룹화해서 사용하는 것이 좋습니다. (특히 글로벌 스코프가 적용되는 경우)

### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정(negate)하는 데 사용할 수 있습니다. 예를 들어, 아래 쿼리는 할인 중인 상품이나 가격이 10 미만인 상품을 제외합니다.

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

여러 컬럼에 동일한 쿼리 제약 조건을 적용해야 하는 경우가 있습니다. 예를 들어, 특정 컬럼 목록 중 하나라도 주어진 값과 `LIKE`로 일치하는 모든 레코드를 조회하고 싶을 수 있습니다. 이럴 때는 `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 아래와 같은 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

이와 유사하게, `whereAll` 메서드는 지정된 모든 컬럼이 주어진 조건과 일치하는 레코드를 조회할 때 사용할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같은 SQL이 생성됩니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정된 컬럼 중 어느 것도 주어진 조건과 일치하지 않는 레코드를 조회할 때 사용할 수 있습니다.

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

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼 쿼리도 지원합니다. 현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+가 이에 해당합니다. JSON 컬럼을 조회하려면 `->` 연산자를 사용하면 됩니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

`whereJsonContains` 메서드는 JSON 배열을 조건으로 조회할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

어플리케이션이 MariaDB, MySQL, PostgreSQL 데이터베이스를 사용하는 경우, 배열 형태로 여러 값을 `whereJsonContains`에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

`whereJsonLength` 메서드는 JSON 배열의 길이로 조회할 수 있도록 해줍니다.

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가적인 Where 절

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 조건을 쿼리에 추가할 수 있게 해줍니다. 이 메서드들은 데이터베이스에 상관없이 문자열 매칭 쿼리를 처리하며, 대소문자 구분 여부도 조정할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수로 대소문자를 구분하는 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 조건과 함께 LIKE 조건을 추가할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 "NOT LIKE" 조건을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`는 "or" 조건과 함께 NOT LIKE 조건을 쓸 수 있게 해줍니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike` 메서드의 대소문자 구분 검색 옵션은 SQL Server에서는 현재 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 특정 컬럼의 값이 지정한 배열에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 특정 컬럼의 값이 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인수로 쿼리 객체를 넘길 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 다음과 같은 SQL 문으로 변환됩니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 정수 배열을 바인딩해야 하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 이용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼의 값이 두 값 범위 바깥에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 컬럼의 값이 같은 테이블 행의 두 개 컬럼의 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 컬럼의 값이 같은 행의 두 컬럼 값 범위 바깥에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 해당 컬럼의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 해당 컬럼의 값이 `NULL`이 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼의 값을 특정 날짜와 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 컬럼의 값을 특정 월과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼의 값을 한 달 중 특정 일자와 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼의 값을 특정 연도와 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼의 값을 특정 시간과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture` 메서드는 컬럼의 값이 과거 또는 미래에 속하는지 체크할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast` 및 `whereNowOrFuture` 메서드는 현재 날짜 및 시간까지(즉, 현재 포함) 과거 또는 미래인지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 각각 컬럼의 값이 오늘, 오늘 이전, 오늘 이후인지 확인할 때 사용할 수 있습니다.

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

마찬가지로, `whereTodayOrBefore` 및 `whereTodayOrAfter` 메서드는 컬럼의 값이 오늘 이전(오늘 포함) 또는 오늘 이후(오늘 포함)인지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼의 값이 같은지 확인할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 `whereColumn` 메서드에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 조건 배열을 전달할 수도 있습니다. 이러한 조건들은 `and` 연산자로 묶입니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

여러 "where" 절을 괄호로 묶어 논리적으로 그룹화해야 하는 경우가 있습니다. 실제로는 `orWhere` 메서드를 사용할 때 항상 괄호로 묶는 것이, 예기치 않은 쿼리 동작을 방지하는 권장 방법입니다. 이를 위해 `where` 메서드에 클로저(익명 함수)를 전달하면 됩니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위에서 볼 수 있듯이, `where`에 클로저를 전달하면 쿼리 빌더가 괄호(())로 그룹을 시작하도록 지시합니다. 이 클로저는 쿼리 빌더 인스턴스를 받아서 괄호 그룹 내에 들어갈 제약 조건을 설정할 수 있습니다. 위 예제는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해서, 항상 `orWhere` 호출을 그룹으로 묶는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. 이 메서드는 클로저를 인수로 받고, 해당 클로저에서 쿼리 빌더 인스턴스를 활용하여 "exists" 절 내부에 들어갈 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 직접 `whereExists`에 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예제 모두 아래와 같은 SQL을 만들어냅니다.

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

서브쿼리 결과를 특정 값과 비교하는 "where" 절을 작성해야 할 때가 있습니다. 이럴 때는 `where` 메서드에 클로저와 값을 전달하여 구현할 수 있습니다. 아래 예시에서는 특정 타입의 최근 “membership”이 존재하는 모든 사용자를 조회합니다.

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

혹은 컬럼 값을 서브쿼리 결과와 비교하는 "where" 절을 만들 수도 있습니다. 이때는 컬럼명, 연산자, 클로저를 차례로 `where`에 넘기면 됩니다. 다음 예시는 amount가 평균보다 작은 모든 수입(income) 레코드를 조회합니다.

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
> 전문(Full Text) Where 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 설정된 컬럼에 대해 전문(Full Text) "where" 조건을 추가하는 데 사용할 수 있습니다. 이 메서드들은 라라벨이 사용하는 데이터베이스 시스템에 맞게 적절한 SQL로 변환됩니다. 예를 들어, MariaDB나 MySQL의 경우 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit 및 Offset

<a name="ordering"></a>
### 정렬(ORDER BY)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 결과 쿼리를 지정한 컬럼으로 정렬할 수 있도록 해줍니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(asc 또는 desc)입니다.

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

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 기준으로 간편하게 결과를 정렬합니다. 기본적으로는 테이블의 `created_at` 컬럼으로 정렬하지만, 다른 컬럼명을 지정하여 정렬할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 하나 조회하고 싶을 때 사용할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 쿼리에 적용된 모든 "order by" 조건을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 호출 시 컬럼과 정렬 방향을 지정하면, 기존에 적용된 모든 "order by" 조건을 제거하고 새로운 정렬을 적용합니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해, `reorderDesc` 메서드를 사용하여 쿼리 결과를 내림차순(desc)으로 재정렬할 수도 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>

### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상할 수 있듯이, `groupBy`와 `having` 메서드를 사용하면 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 시그니처는 `where` 메서드와 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하면 특정 범위 내의 결과만 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인수를 전달하면 여러 컬럼을 기준으로 그룹화할 수 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 구문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit과 Offset

쿼리 결과의 개수를 제한하거나, 쿼리 중 일부 결과를 건너뛰고 싶을 때 `limit`과 `offset` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 구문 사용

특정 조건에 따라 쿼리의 일부 절을 적용하고자 할 때가 있습니다. 예를 들어, HTTP 요청에 특정 입력값이 있을 때만 `where` 구문을 추가하고 싶을 수 있습니다. 이럴 때 `when` 메서드를 사용할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 주어진 클로저를 실행합니다. 첫 번째 인수가 `false`이면 클로저는 실행되지 않습니다. 따라서 위의 예시에서, `when`에 전달된 클로저는 요청에 `role` 필드가 존재하여, `true`로 평가될 때만 호출됩니다.

또한 `when` 메서드의 세 번째 인수로 또 다른 클로저를 전달할 수 있습니다. 이 경우 첫 번째 인수가 `false`일 때만 해당 클로저가 실행됩니다. 아래 예제는 쿼리의 기본 정렬 방식을 설정하는 방법을 보여줍니다.

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
## 데이터 삽입(Insert) 구문

쿼리 빌더는 레코드를 데이터베이스 테이블에 삽입할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 컬럼명과 값의 배열을 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열의 배열을 전달할 수 있습니다. 각 배열이 테이블에 삽입될 하나의 레코드를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드를 사용하면 데이터베이스에 레코드를 삽입하는 과정에서 오류가 발생해도 무시됩니다. 이 메서드를 사용할 때는 중복된 레코드에 대한 오류가 무시되며, 데이터베이스 엔진에 따라 다른 유형의 오류도 무시될 수 있음을 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리를 통해 삽입할 데이터를 결정하여 테이블에 새로운 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가(Auto-Incrementing) ID

테이블에 자동 증가하는 id 컬럼이 있다면, `insertGetId` 메서드를 사용하여 레코드를 삽입하고 곧바로 해당 ID를 가져올 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 경우, `insertGetId` 메서드는 자동 증가 컬럼의 이름이 반드시 `id`여야 합니다. 만약 다른 "시퀀스"에서 ID를 가져오기를 원한다면, `insertGetId` 두 번째 인수로 컬럼명을 전달하면 됩니다.

<a name="upserts"></a>
### Upsert(업서트)

`upsert` 메서드는 존재하지 않는 레코드는 새로 삽입(insert)하고, 이미 존재하는 레코드는 지정한 값으로 업데이트(update)합니다. 첫 번째 인수는 삽입 또는 업데이트할 값들의 배열이고, 두 번째 인수는 레코드를 고유하게 식별하는 컬럼(들)입니다. 세 번째 인수는 일치하는 레코드가 이미 데이터베이스에 존재할 경우 업데이트할 컬럼 리스트입니다.

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

위의 예제에서, 라라벨은 두 개의 레코드를 삽입하려 시도합니다. 만약 동일한 `departure`와 `destination` 컬럼 값을 가진 레코드가 이미 존재한다면, 해당 레코드의 `price` 컬럼만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드 두 번째 인수에 지정된 컬럼들이 반드시 "primary" 또는 "unique" 인덱스여야 합니다. 또한 MariaDB와 MySQL 드라이버는 이 두 번째 인수를 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스를 이용해 기존 레코드를 판별합니다.

<a name="update-statements"></a>
## 데이터 갱신(Update) 구문

레코드를 삽입하는 것 외에도, 쿼리 빌더를 통해 기존 레코드를 갱신할 수 있습니다. `update` 메서드는 `insert`와 마찬가지로, 갱신할 컬럼과 값 쌍의 배열을 받습니다. `update` 메서드는 영향을 받은(갱신된) 행의 수를 반환합니다. 또한 `where` 구문을 조합하여 갱신 쿼리를 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 갱신 또는 삽입(Update or Insert)

기존에 일치하는 레코드가 있으면 갱신하고, 없으면 새로 만들어야 할 때가 있습니다. 이 경우 `updateOrInsert` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 레코드 검색 조건 배열을, 두 번째 인수로 갱신할 컬럼과 값 쌍 배열을 받습니다.

`updateOrInsert` 메서드는 첫 번째 인수의 컬럼/값 쌍을 사용해 일치하는 레코드를 찾으려고 시도합니다. 레코드가 있으면 두 번째 인수의 값으로 갱신되고, 없으면 두 인수의 값을 합쳐 새 레코드로 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

또한 `updateOrInsert`에 클로저를 전달하여, 일치하는 레코드 존재 여부에 따라 데이터베이스에 갱신 또는 삽입할 속성을 커스터마이즈할 수 있습니다.

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
### JSON 컬럼 갱신

JSON 컬럼을 갱신할 때는 `->` 구문을 사용하여 JSON 객체 내부의 키를 지정해 갱신해야 합니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 값 증가 및 감소 (Increment / Decrement)

쿼리 빌더는 특정 컬럼 값의 증감 연산을 쉽게 할 수 있도록 편리한 메서드를 제공합니다. 두 방법 모두 적어도 변경할 컬럼명을 첫 번째 인수로 받으며, 두 번째 인수로 변경할 값을 지정할 수도 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

값을 증가(또는 감소)시키면서 동시에 다른 컬럼의 값도 한 번에 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach`와 `decrementEach` 메서드를 사용하면 여러 컬럼을 한 번에 증감시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## 데이터 삭제(Delete) 구문

쿼리 빌더의 `delete` 메서드를 사용해 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행의 수를 반환합니다. "where" 구문을 추가하여 삭제 기준을 제한할 수도 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더에는 `select` 구문을 실행할 때 "비관적 잠금"을 쉽게 적용할 수 있도록 도와주는 몇몇 메서드가 있습니다. "공유 잠금(shared lock)"으로 실행하려면 `sharedLock` 메서드를 사용하세요. 공유 잠금은 선택된 행이 트랜잭션이 완료될 때까지 수정되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate` 메서드를 사용할 수도 있습니다. "for update" 잠금은 선택된 레코드가 수정되거나, 다른 공유 잠금으로 조회되는 것을 차단합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금을 반드시 사용해야 하는 것은 아니지만, [트랜잭션](/docs/12.x/database#database-transactions) 내에서 감싸서 사용하는 것이 권장됩니다. 이렇게 하면, 전체 작업이 끝날 때까지 데이터가 데이터베이스에서 변경되지 않도록 보장해줍니다. 만약 수행 중 오류가 발생하면, 트랜잭션이 모든 변경사항을 자동으로 롤백하고 잠금도 해제합니다.

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

애플리케이션 곳곳에서 반복적으로 사용하는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 이용해 재사용 가능한 객체로 추출할 수 있습니다. 예를 들어, 애플리케이션에 다음과 같이 유사한 두 쿼리가 있다고 가정해봅시다.

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

이 때, 여러 쿼리에서 공통으로 사용되는 목적지(destination) 필터링 로직을 재사용 가능한 객체로 분리할 수 있습니다.

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

이제 `tap` 메서드를 사용하여 이 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더 자체를 반환합니다. 만약 쿼리를 실행해서 다른 값을 반환하는 객체를 분리하고 싶다면, 대신 `pipe` 메서드를 사용할 수 있습니다.

아래 예시는 전체 애플리케이션에서 공통적으로 사용되는 [페이지네이션](/docs/12.x/pagination) 로직을 포함한 쿼리 객체입니다. `DestinationFilter`는 쿼리 조건만 추가하는 반면, `Paginate` 객체는 쿼리를 실행하고 paginator 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용해 이 객체를 적용하여, 공통적인 페이지네이션 로직을 편리하게 사용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하는 도중 현재 쿼리 바인딩과 SQL을 출력하려면 `dd` 및 `dump` 메서드를 사용할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 뒤 요청의 실행을 중단합니다. `dump` 메서드는 정보를 출력하되, 요청의 실행을 계속 진행합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드는 쿼리의 SQL을 모든 파라미터 바인딩이 실제 값으로 치환된 상태로 출력해줍니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```