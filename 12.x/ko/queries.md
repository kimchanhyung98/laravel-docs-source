# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [합집합(Unions)](#unions)
- [기본 WHERE 조건](#basic-where-clauses)
    - [WHERE 조건](#where-clauses)
    - [OR WHERE 조건](#or-where-clauses)
    - [WHERE NOT 조건](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 조건](#where-any-all-none-clauses)
    - [JSON WHERE 조건](#json-where-clauses)
    - [추가 WHERE 조건](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 WHERE 조건](#advanced-where-clauses)
    - [WHERE EXISTS 조건](#where-exists-clauses)
    - [서브쿼리 WHERE 조건](#subquery-where-clauses)
    - [전체 텍스트 WHERE 조건](#full-text-where-clauses)
- [정렬, 그룹화, LIMIT, OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [LIMIT 및 OFFSET](#limit-and-offset)
- [조건부 구문](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [Upsert(UPSERT)](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소(Incremet/Decrement)](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅(Debugging)](#debugging)

<a name="introduction"></a>
## 소개

라라벨의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 유연하게 작성하고 실행할 수 있는 간편한 인터페이스를 제공합니다. 이 빌더를 사용하면 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, 라라벨이 지원하는 모든 데이터베이스 시스템에 완벽하게 작동합니다.

라라벨 쿼리 빌더는 PDO 파라미터 바인딩을 사용해 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더의 바인딩으로 전달되는 문자열은 별도의 정리(clean)나 필터링 작업이 필요하지 않습니다.

> [!WARNING]
> PDO는 컬럼 이름에 대한 바인딩을 지원하지 않습니다. 따라서 사용자 입력값이 쿼리에서 참조되는 컬럼 이름(특히 "order by"의 컬럼 등)을 직접 지정하게 해서는 절대 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드의 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 주어진 테이블에 대해 유연한 쿼리 빌더 인스턴스를 반환하므로, 여기에 연이어 다양한 조건을 추가하고, 마지막에 `get` 메서드로 결과를 조회할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 이 컬렉션의 각 결과는 PHP의 `stdClass` 객체로 반환됩니다. 각 컬럼의 값은 객체의 속성 방식으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨 컬렉션은 데이터 매핑, 집계 등에 매우 강력한 여러 메서드를 제공합니다. 라라벨 컬렉션에 대해 더 자세히 알아보고 싶다면 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회하기

데이터베이스 테이블에서 하나의 행만 조회하고 싶을 때는, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 아무 행도 결과로 나오지 않을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 만약 이 예외가 잡히지 않으면, 클라이언트에게 404 HTTP 응답이 자동으로 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

한 행 전체가 필요하지 않고, 특정 한 컬럼의 값만 추출하고 싶을 때는 `value` 메서드를 사용하세요. 이 메서드는 해당 컬럼의 값을 바로 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 이용해 한 행만 조회하려면 `find` 메서드를 사용하세요.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 특정 컬럼 값 목록 조회하기

특정 컬럼의 값만을 담은 `Illuminate\Support\Collection` 인스턴스를 얻으려면 `pluck` 메서드를 사용하십시오. 예를 들어, 사용자들의 직함만 모은 컬렉션을 조회할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

또한, `pluck` 메서드의 두 번째 인수로 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크로 처리하기

수천 개에 달하는 데이터베이스 레코드를 다루어야 할 경우, `DB` 파사드가 제공하는 `chunk` 메서드 사용을 고려할 수 있습니다. 이 메서드는 결과를 한 번에 소량씩(청크 단위로) 불러와서, 각 청크를 콜백 함수에 전달해 처리합니다. 예시로, `users` 테이블 전체를 100개씩 나누어 청크 단위로 조회해 보겠습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

콜백에서 `false`를 반환하면, 이후 추가 청크들은 처리하지 않고 중단할 수도 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 작업 중에 데이터베이스 레코드를 업데이트하는 경우, 청크 결과가 예기치 않게 변경될 수 있습니다. 청크 반복 중 레코드를 업데이트할 계획이라면, `$chunkById` 메서드 사용을 권장합니다. 이 메서드는 기본키(primary key)를 기준으로 자동으로 결과를 페이지네이션합니다.

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

`chunkById` 및 `lazyById` 메서드는 실행되는 쿼리에 자체적으로 "where" 조건을 추가하기 때문에, [논리적 그룹화](#logical-grouping)가 필요한 조건들은 클로저 내부에서 묶어주는 것이 좋습니다.

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
> 청크 콜백 내에서 기본키 또는 외래키(primary, foreign key)가 변경되는 경우, 이후 청크 쿼리의 결과에 영향을 줄 수 있으며, 일부 레코드가 빠질 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기

`lazy` 메서드 역시 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행합니다. 하지만, 각 청크를 콜백으로 전달하는 대신 `lazy()` 메서드는 [LazyCollection](/docs/12.x/collections#lazy-collections) 인스턴스를 반환하여, 결과 전체를 하나의 스트림처럼 사용할 수 있게 해줍니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복 도중에 조회한 레코드를 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드 사용이 더 좋습니다. 이 메서드들도 마찬가지로 기본키 기준으로 자동 페이지네이션을 적용합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 처리 중에 기본키나 외래키가 변경되는 경우, 이후 쿼리 결과에 영향을 주어 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 합계(`count`), 최대/최소(`max`/`min`), 평균(`avg`), 합계(`sum`)와 같은 다양한 집계 함수도 제공합니다. 쿼리 빌더로 쿼리를 작성한 뒤, 이 메서드들을 호출하면 집계 결과를 바로 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 이 집계 메서드들도 다양한 조건과 조합해 사용할 수 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

특정 조건에 맞는 레코드가 존재하는지 단순히 확인하고 싶다면, `count` 메서드 대신 `exists`와 `doesntExist` 메서드를 사용할 수 있습니다.

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

항상 테이블의 모든 컬럼을 조회하는 것이 아니라, 원하는 컬럼만 지정해 조회할 수도 있습니다. `select` 메서드를 이용하면 SELECT 절에 원하는 컬럼만 직접 명시할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

중복된 결과를 제거하여 반환하고 싶다면 `distinct` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 SELECT 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

쿼리에 임의의 문자열을 그대로 삽입해야 할 경우도 있습니다. 이럴 땐, `DB` 파사드가 제공하는 `raw` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 "문자열"로 직접 삽입되므로, SQL 인젝션 취약점이 생기지 않도록 주의가 필요합니다.

<a name="raw-methods"></a>
### Raw 메서드들

`DB::raw` 메서드를 사용하는 대신, 쿼리 빌더의 다양한 부분에 raw 표현을 삽입할 수 있는 아래 메서드들도 사용할 수 있습니다.  
**주의: 라라벨은 raw 표현식이 포함된 쿼리의 보안(특히 SQL 인젝션 방지)을 보장하지 않으므로, 각별한 주의가 필요합니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(...))` 대신 사용할 수 있습니다. 이 메서드는 두 번째 인수로 바인딩 배열도 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 삽입할 때 사용할 수 있습니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 지정할 수 있도록 해줍니다. 이들 역시 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 지정할 때 사용합니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 지정할 때 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Join)

<a name="inner-join-clause"></a>
#### Inner Join 구문

쿼리 빌더를 사용하여 쿼리에 조인 구문을 추가할 수도 있습니다. 기본적인 "inner join"을 하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인수에는 조인할 테이블명을, 나머지 인수에는 조인 조건을 지정합니다. 한 쿼리에서 여러 테이블도 조인할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 구문

"inner join" 대신 "left join"이나 "right join"을 원한다면, 각각 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이 메서드의 사용법은 `join` 메서드와 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Cross Join 구문

"cross join"을 수행하려면 `crossJoin` 메서드를 사용하면 됩니다. Cross join은 첫 번째 테이블과 조인된 테이블 사이의 데카르트 곱(cartesian product)을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 구문

더 복잡한 조인을 작성할 수도 있습니다. 시작할 땐, `join` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다. 이 클로저에는 `Illuminate\Database\Query\JoinClause` 인스턴스가 주어지며, 이 객체로 조인 조건을 세부적으로 지정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 절을 사용하고 싶을 때는, `JoinClause` 인스턴스가 제공하는 `where`, `orWhere` 메서드를 활용할 수 있습니다. 이 때는 두 컬럼 간 비교가 아니라, 컬럼과 값의 비교가 이루어집니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인(Subquery Join)

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리에 서브쿼리를 조인할 수 있습니다. 이 메서드들은 세 개의 인수를 받습니다: (1) 서브쿼리, (2) 테이블 별칭, (3) 관련 컬럼을 정의하는 클로저. 예시로, 각 사용자의 가장 최근 블로그 게시물의 작성일(`created_at`)을 함께 포함한 사용자 목록을 조회해보겠습니다.

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
> Lateral join은 현재 PostgreSQL, MySQL(8.0.14 이상), SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하면 서브쿼리와 "lateral join"을 수행할 수 있습니다. 이 메서드들은 서브쿼리와 그 별칭 두 가지 인수를 받습니다. 조인 조건은 서브쿼리 내부의 `where` 절에서 지정해야 하며, lateral join은 각 행에 대해 평가되어 서브쿼리 바깥의 컬럼도 참조할 수 있습니다.

예를 들어, 각 사용자와 해당 사용자의 가장 최근 블로그 게시물 3개를 함께 조회하도록 해보겠습니다. 한 사용자가 최대 3개의 게시물을 가져오게 되고, 조인 조건은 서브쿼리 내의 `whereColumn` 절에서 현재 사용자 행을 참조하여 지정됩니다.

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
## 합집합(Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "합집합(union)"으로 결합하는 메서드도 제공합니다. 예를 들어, 초기 쿼리를 만든 뒤, `union` 메서드로 더 많은 쿼리를 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드가 제공됩니다. `unionAll`로 결합하면 중복되는 결과도 모두 포함되어 반환됩니다. 두 메서드는 시그니처가 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 조건

<a name="where-clauses"></a>
### WHERE 조건

쿼리 빌더의 `where` 메서드를 사용해 "where" 조건을 쿼리에 추가할 수 있습니다. 가장 기본적인 형태는 세 개의 인수를 받으며, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 컬럼과 비교할 값입니다.

아래는 `votes` 컬럼이 100이고 `age` 컬럼이 35보다 큰 사용자만 조회하는 예제입니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의상, 컬럼값이 어떤 값과 `=`인지 확인하려면 연산자는 생략하고 값만 두 번째 인수로 넘겨도 됩니다. 라라벨이 자동으로 `=` 연산자를 사용합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

배열을 전달하면 여러 컬럼 조건도 간단히 조합할 수 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

앞서 언급했듯, 데이터베이스 시스템이 지원하는 모든 연산자를 사용할 수 있습니다.

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

조건의 목록을 배열로 넘길 수도 있습니다. 각 배열의 요소는 보통 `where` 메서드에 전달하는 세 개의 인자를 담은 배열입니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리의 컬럼명(특히 "order by" 등)을 지정할 수 있게 해서는 절대 안 됩니다.

> [!WARNING]
> MySQL 및 MariaDB에서는 문자열-숫자 비교 시 문자열을 자동으로 정수형으로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 모두 `0`으로 변환되어 예기치 않은 결과가 발생할 수 있습니다. 예를 들어, 테이블의 `secret` 컬럼에 값이 `'aaa'`라고 입력되어 있을 때 `User::where('secret', 0)` 쿼리를 실행하면 해당 행이 반환됩니다. 이러한 문제를 피하려면 쿼리에 사용하는 값의 타입을 항상 명확하게 맞춰주어야 합니다.

<a name="or-where-clauses"></a>
### OR WHERE 조건

여러 번 `where` 메서드를 체이닝하면 AND로 쿼리 조건이 결합됩니다. 하지만 `orWhere` 메서드를 사용하면, OR 연산자로 조건을 결합할 수 있습니다. `orWhere` 메서드의 사용법은 `where`와 동일합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 묶어서 OR 그룹 조건을 만들고 싶을 때는, 첫 번째 인자로 클로저를 넘기세요.

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

위의 예시는 다음과 같은 SQL로 변환됩니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 피하기 위해, 항상 `orWhere`는 그룹화해서 사용하는 것이 좋습니다.

<a name="where-not-clauses"></a>
### WHERE NOT 조건

`whereNot` 및 `orWhereNot` 메서드를 사용하면 쿼리 조건 그룹을 부정할 수 있습니다. 예를 들어, 아래 쿼리는 할인(clearance) 품목이거나 가격이 10 미만인 상품을 제외합니다.

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### WHERE ANY / ALL / NONE 조건

여러 컬럼에 동일한 조건을 한 번에 적용해야 할 때가 있습니다. 예를 들어, 주어진 컬럼 리스트 중 어느 하나라도 값이 특정 패턴에 `LIKE`되면 레코드를 조회하려면 `whereAny` 메서드를 사용할 수 있습니다.

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

마찬가지로, 여러 컬럼 모두가 특정 조건을 만족해야 할 때는 `whereAll` 메서드를 사용할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

이 쿼리는 다음과 같은 SQL이 생성됩니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

하나도 해당하지 않는 레코드만 조회하려면 `whereNone` 메서드를 사용할 수 있습니다.

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

이 쿼리는 아래와 같은 SQL로 변환됩니다.

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
### JSON WHERE 조건

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 타입 컬럼 쿼리도 지원합니다. (MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+ 등) JSON 컬럼을 쿼리할 때는 `->` 연산자를 사용합니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열 데이터에 대해 쿼리하려면, `whereJsonContains`와 `whereJsonDoesntContain` 메서드를 사용하세요.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용할 때는, `whereJsonContains`와 `whereJsonDoesntContain`에 배열을 전달하는 것도 가능합니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한, `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 활용하면 JSON 객체에 특정 키가 존재하는(혹은 존재하지 않는) 레코드를 조회할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이를 검색하고 싶다면 `whereJsonLength` 메서드를 사용할 수 있습니다.

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

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 조건을 쿼리에 추가할 수 있게 해줍니다. 이 메서드들은 데이터베이스에 독립적인 방식으로 문자열 매칭 쿼리를 수행하며, 대소문자 구분 여부도 설정할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 사용하여 대소문자를 구분하는 검색을 활성화할 수 있습니다.

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

`whereNotLike` 메서드는 "NOT LIKE" 조건을 쿼리에 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`를 사용하여 NOT LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 컬럼 값이 전달된 배열 안에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 컬럼의 값이 전달된 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

또한, `whereIn` 메서드의 두 번째 인자로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 수의 정수 바인딩 배열을 추가해야 하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지 확인합니다.

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

`whereBetweenColumns` 메서드는 같은 테이블 행의 두 컬럼 값 사이에 컬럼의 값이 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 컬럼 값이 같은 행의 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween` 메서드는 주어진 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween` 메서드는 값이 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 주어진 컬럼 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 해당 컬럼 값이 `NULL`이 아님을 확인합니다.

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

`whereMonth` 메서드는 컬럼 값을 특정 월과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼 값을 특정 일(day)과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼 값을 특정 연도와 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼 값을 특정 시간과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture` 메서드는 컬럼의 값이 과거인지, 미래인지 확인할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast` 및 `whereNowOrFuture` 메서드는 현재 날짜와 시간을 포함하여, 컬럼의 값이 과거 또는 미래에 해당하는지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 컬럼 값이 각각 오늘, 오늘 이전, 오늘 이후인지 확인할 때 사용합니다.

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

마찬가지로, `whereTodayOrBefore`, `whereTodayOrAfter` 메서드를 사용하면 오늘을 포함하여 오늘 이전 또는 이후의 값인지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 개의 컬럼 값이 서로 같은지 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

`whereColumn` 메서드에 비교 연산자를 전달하여 사용할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 개의 컬럼 비교 조건을 배열로 전달할 수도 있습니다. 이 조건들은 모두 `and`로 연결됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑

여러 개의 "where" 절을 괄호로 묶어서 논리적 그룹을 지정해야 할 때가 있습니다. 실제로, 예기치 않은 쿼리 결과를 방지하기 위해, `orWhere` 메서드를 사용할 때는 항상 괄호로 해당 조건들을 묶는 것이 좋습니다. 이를 위해서는 `where` 메서드에 클로저를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

이처럼, `where` 메서드에 클로저를 전달하면 쿼리 빌더는 하나의 제약 그룹(괄호 그룹)을 시작합니다. 이 클로저 내에서 그룹에 포함시킬 조건을 지정할 수 있습니다. 위의 예시는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용될 때 예기치 않은 동작을 방지하려면 `orWhere` 호출을 항상 그룹으로 묶어야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있게 해줍니다. 이 메서드는 클로저를 인수로 받아, 그 안에서 "exists" 절 안에 들어갈 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체를 `whereExists` 메서드에 바로 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예제는 다음과 같은 SQL을 생성합니다.

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

때로는 서브쿼리의 결과를 특정 값과 비교하는 "where" 절이 필요할 수 있습니다. 이럴 때는 `where` 메서드에 클로저와 비교할 값을 전달하면 됩니다. 예를 들어, 아래 쿼리는 주어진 타입의 최근 "membership"이 있는 모든 사용자를 가져옵니다.

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

또는, 컬럼 값을 서브쿼리 결과와 비교해야 할 수도 있습니다. 이럴 때는 컬럼, 연산자, 그리고 클로저를 `where` 메서드에 전달하면 됩니다. 아래 쿼리는 금액이 평균보다 작은 모든 수입 레코드를 가져옵니다.

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
> 전문(Full text) where 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드를 사용하면 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 있는 컬럼에 대해 전문 검색을 위한 "where" 조건을 추가할 수 있습니다. 이 메서드들은 라라벨이 사용하는 데이터베이스에 맞게 적절한 SQL로 변환됩니다. 예를 들어, MariaDB나 MySQL을 사용할 경우 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한, 오프셋

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 특정 컬럼 기준으로 정렬할 수 있게 해줍니다. 첫 번째 인자로 정렬할 컬럼명을, 두 번째 인자로 정렬 방향(`asc`, `desc`)을 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼을 기준으로 정렬하려면 `orderBy`를 여러 번 사용하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본적으로 오름차순(`asc`)입니다. 내림차순 정렬이 필요하면 두 번째 인자로 지정하거나, `orderByDesc`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한, `->` 연산자를 이용하면 JSON 컬럼 내부 값으로 정렬할 수도 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest` 및 `oldest` 메서드를 이용하면 쉽게 날짜 기준으로 정렬할 수 있습니다. 기본적으로는 테이블의 `created_at` 컬럼을 기준으로 정렬하며, 다른 컬럼명을 지정할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 랜덤하게 정렬할 수 있습니다. 예를 들어, 무작위 사용자 한 명을 조회하려면 다음처럼 사용할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 해제

`reorder` 메서드는 쿼리에 이전에 적용된 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드 호출 시 컬럼과 방향을 함께 지정하면, 기존 정렬을 지우고 새로운 정렬 기준을 적용합니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

좀 더 편리하게, `reorderDesc`를 사용하면 내림차순 정렬도 할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상하신 대로, `groupBy`와 `having` 메서드를 활용해 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 사용법은 `where`와 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하면, 특정 범위 내 결과만 걸러낼 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼을 기준으로 그룹화하려면 `groupBy`에 여러 인자를 전달하면 됩니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 발전된 having 구문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

`limit`과 `offset` 메서드를 사용하면 결과 레코드 수를 제한하거나, 쿼리 결과에서 특정 개수만큼 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

어떤 조건에 따라 쿼리의 일부 절을 적용하고 싶을 때가 있습니다. 예를 들어, 주어진 입력 값이 HTTP 요청에 있을 때만 `where` 조건을 추가하고 싶은 경우가 있습니다. 이럴 때는 `when` 메서드를 사용할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 주어진 클로저를 실행합니다. 만약 첫 번째 인자가 `false`라면 클로저는 무시됩니다. 즉, 위 예제에서는 요청에 `role` 필드가 있을 때만 해당 조건이 쿼리에 추가됩니다.

`when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수도 있습니다. 이 클로저는 첫 번째 인자가 `false`일 때만 실행됩니다. 아래 예시는 이런 기능을 활용해 기본 정렬 방식을 설정하는 방법을 보여줍니다.

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

쿼리 빌더는 `insert` 메서드를 제공하여 레코드를 데이터베이스 테이블에 삽입할 수 있습니다. `insert` 메서드는 컬럼명과 값의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 중첩 배열을 전달하면 됩니다. 각 배열이 테이블에 삽입될 레코드를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드를 사용하면 레코드 삽입 도중 오류가 발생해도 무시할 수 있습니다. 이 메서드를 사용할 경우, 중복 레코드 오류가 무시되며, 데이터베이스 엔진에 따라 다른 오류들도 무시될 수 있습니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드를 이용하면 서브쿼리 결과로 새 레코드를 테이블에 삽입할 수 있습니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id가 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입한 뒤 그 ID를 바로 반환받을 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId` 메서드가 자동 증가 컬럼명을 반드시 `id`로 기대합니다. 다른 "시퀀스"에서 ID를 반환받고 싶다면 두 번째 인자로 원하는 컬럼명을 전달하세요.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 새 값으로 갱신합니다. 첫 번째 인자는 삽입 또는 업데이트할 값들이고, 두 번째 인자에는 해당 테이블에서 레코드를 고유하게 식별할 컬럼(들)을 지정합니다. 마지막 세 번째 인자는 일치하는 레코드가 있을 경우 업데이트할 컬럼 이름의 배열입니다.

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

위 예제에서, 라라벨은 두 레코드를 삽입하려 시도합니다. 만약 `departure`와 `destination` 값이 같은 레코드가 이미 있다면, 해당 레코드의 `price` 컬럼값만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 두 번째 인자에 해당하는 컬럼들이 "primary" 또는 "unique" 인덱스를 가져야 합니다. 추가로, MariaDB와 MySQL에서는 두 번째 인자를 무시하고 항상 테이블의 "primary" 및 "unique" 인덱스를 사용해 기존 레코드 존재 여부를 판별합니다.

<a name="update-statements"></a>
## Update 구문

데이터베이스에 레코드를 삽입하는 것 외에도, 쿼리 빌더는 `update` 메서드를 사용해 기존 레코드를 갱신할 수 있습니다. `update` 메서드도 `insert`처럼, 갱신할 컬럼과 값의 배열을 전달합니다. 실행 결과로 영향을 받은 행(row)의 개수를 반환합니다. `where` 조건을 통해 update 범위를 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

기존 레코드를 갱신하고 싶지만 일치하는 레코드가 없으면 새 레코드를 삽입하는 경우에는 `updateOrInsert` 메서드를 사용하면 됩니다. 이 메서드는 첫 번째 인자에 검색할 조건(컬럼 및 값의 배열), 두 번째 인자에 갱신할 컬럼과 값의 배열을 전달합니다.

`updateOrInsert`는 첫 인자의 조건으로 레코드 탐색을 시도합니다. 레코드가 있으면 두 번째 인자의 값으로 갱신하고, 없으면 두 인자를 병합한 값으로 새 레코드를 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

`updateOrInsert` 메서드에 클로저를 전달하면, 일치하는 레코드 존재 여부에 따라 삽입 혹은 갱신할 속성을 동적으로 지정할 수 있습니다.

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
### JSON 컬럼의 갱신

JSON 컬럼을 갱신할 때는 `->` 문법을 사용해 해당 JSON 필드(키)를 직접 갱신할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 (Increment & Decrement)

쿼리 빌더는 특정 컬럼 값을 증가(`increment`) 또는 감소(`decrement`)시키는 간편한 메서드를 제공합니다. 두 메서드 모두 첫 인자로 갱신할 컬럼명을 받으며, 두 번째 인자로 증감할 수를 지정할 수 있습니다(생략 시 1).

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

추가로, 증감 작업과 동시에 다른 컬럼을 같이 갱신하고 싶다면 배열로 전달할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한 `incrementEach`, `decrementEach` 메서드를 사용하면 여러 컬럼을 한 번에 증감시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>

## 삭제(DELETE) 구문

쿼리 빌더의 `delete` 메서드를 사용해 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행(row)의 개수를 반환합니다. 삭제 구문에 조건을 추가하고 싶다면, `delete` 메서드를 호출하기 전에 "where" 절을 추가하면 됩니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 `select` 구문 실행 시 "비관적 잠금(pessimistic locking)"을 위한 여러 메서드도 제공합니다. "공유 잠금(shared lock)"을 걸고 싶다면, `sharedLock` 메서드를 사용하면 됩니다. 공유 잠금은 선택된 행이 트랜잭션이 커밋될 때까지 수정되지 않도록 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate` 메서드를 사용할 수도 있습니다. "FOR UPDATE" 잠금은 선택된 레코드가 수정되거나, 다른 트랜잭션에서 공유 잠금과 함께 선택되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

꼭 필수는 아니지만, 비관적 잠금을 사용할 때는 [트랜잭션](/docs/12.x/database#database-transactions) 안에 쿼리를 감싸는 것이 권장됩니다. 이렇게 하면 데이터가 전체 작업이 끝날 때까지 데이터베이스에서 변경되지 않으며, 실패가 발생하면 트랜잭션이 모든 변경사항을 롤백하고 잠금도 자동으로 해제합니다.

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

애플리케이션 전반에 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap`과 `pipe` 메서드를 활용해 재사용 가능한 객체로 로직을 추출할 수 있습니다. 예를 들어, 다음과 같은 서로 다른 두 쿼리가 존재한다고 가정해 보겠습니다.

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

여기서 공통적으로 사용되는 목적지 필터링 로직을 재사용 가능한 객체로 추출할 수 있습니다.

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

위와 같이 정의한 후, 쿼리 빌더의 `tap` 메서드를 사용해 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더를 반환합니다. 만약 쿼리를 실행해서 다른 값을 반환하는 객체로 로직을 추출하고 싶다면 `pipe` 메서드를 사용할 수 있습니다.

아래는 애플리케이션 전체에서 공통적으로 사용하는 [페이지네이션](/docs/12.x/pagination) 로직이 포함된 쿼리 객체 예시입니다. `DestinationFilter`가 쿼리 조건만 추가한 것과 달리, `Paginate` 객체는 쿼리를 실행하고 paginator 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용하여, 이 객체를 통해 공통 페이지네이션 로직을 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하면서 `dd` 및 `dump` 메서드를 사용해 현재의 쿼리 바인딩과 SQL을 출력할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 뒤 요청 실행을 멈추며, `dump` 메서드는 디버그 정보만 출력하고 요청을 계속 진행합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드를 사용하면 쿼리의 SQL 문장 전체와, 모든 파라미터 바인딩을 실제 값으로 대체한 결과를 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```