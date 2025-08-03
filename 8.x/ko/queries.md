# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 문](#select-statements)
- [원시 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [유니언(Union)](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬(Ordering)](#ordering)
    - [그룹화(Grouping)](#grouping)
    - [제한 및 오프셋(Limit & Offset)](#limit-and-offset)
- [조건절(Conditional Clauses)](#conditional-clauses)
- [INSERT 문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [UPDATE 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소(Increment & Decrement)](#increment-and-decrement)
- [DELETE 문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [디버깅(Debugging)](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 손쉽고 유창한 방식으로 생성하고 실행할 수 있는 인터페이스를 제공합니다. 이 빌더는 애플리케이션 내의 대부분의 데이터베이스 작업에 사용될 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

Laravel 쿼리 빌더는 PDO의 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 바인딩에 넘겨지는 문자열을 별도로 정제하거나 필터링할 필요가 없습니다.

> [!NOTE]
> PDO는 컬럼 이름에 대한 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조할 컬럼 이름(예: "order by" 컬럼)을 사용자 입력에 의해 결정되지 않도록 해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드가 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 특정 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하며, 이를 통해 쿼리에 조건을 연결한 후 최종적으로 `get` 메서드를 사용하여 결과를 가져올 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 결과의 각 행은 PHP의 `stdClass` 객체입니다. 컬럼 값은 객체의 속성으로 바로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!TIP]
> Laravel 컬렉션은 데이터를 매핑 및 축소하기 위한 강력한 메서드들을 제공합니다. 컬렉션에 대한 자세한 정보는 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 또는 단일 컬럼 조회하기

데이터베이스 테이블에서 단일 행만 필요하다면, `DB` 파사드의 `first` 메서드를 사용하세요. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

전체 행이 필요하지 않고 특정 컬럼 값 하나만 필요하다면, `value` 메서드를 사용하여 직접 컬럼 값을 추출할 수 있습니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기반으로 단일 행을 조회할 때는 `find` 메서드를 이용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 단일 컬럼 값 리스트 조회하기

단일 컬럼의 값들로 이루어진 `Illuminate\Support\Collection` 인스턴스를 받고 싶으면 `pluck` 메서드를 사용하세요. 아래 예제에서는 사용자들의 직함(titles)을 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 키로 사용할 컬럼명을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기 (Chunking Results)

수천 건의 데이터베이스 레코드를 처리해야 한다면, `DB` 파사드가 제공하는 `chunk` 메서드를 사용하는 것을 고려하세요. 이 메서드는 일정 개수씩 결과를 나누어 가져와 각 청크를 클로저에 전달해 처리할 수 있게 합니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 나누어 처리하는 예제입니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    foreach ($users as $user) {
        //
    }
});
```

클로저에서 `false`를 반환하면 이후 청크에 대한 처리가 중지됩니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중 데이터베이스 레코드를 업데이트 할 계획이라면, 예상치 못한 결과가 발생할 수 있습니다. 이런 경우에는 `chunkById` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키(primary key)를 기준으로 자동 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function ($users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

> [!NOTE]
> 청크 콜백 안에서 레코드 업데이트나 삭제 시 기본 키나 외래 키의 변경 때문에 청크 쿼리에 영향을 줄 수 있으며, 이로 인해 일부 레코드가 청크 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 수행합니다. 그러나 각 청크를 콜백으로 넘기는 대신, `lazy()`는 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)을 반환하여 전체 결과를 하나의 스트림처럼 다룰 수 있게 합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

마찬가지로, 처리 중인 레코드를 업데이트할 계획이라면, 기본 키를 기준으로 자동 페이지네이션하는 `lazyById` 또는 `lazyByIdDesc` 메서드 사용을 권장합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!NOTE]
> 레코드를 처리하며 업데이트하거나 삭제할 경우, 기본 키나 외래 키 값 변경이 쿼리에 영향을 줄 수 있으며, 일부 레코드가 결과에 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 같은 다양한 집계 함수를 제공합니다. 쿼리 생성 후 이들 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 조건들과 결합해 집계 값을 세밀하게 계산할 수도 있습니다:

```php
$price = DB::table('orders')
                ->where('finalized', 1)
                ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리에 맞는 레코드가 있는지 확인할 때 `count` 대신 `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT 문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정하기

항상 테이블의 모든 컬럼을 선택하고 싶진 않을 수 있습니다. `select` 메서드를 사용하면 쿼리에 원하는 컬럼만 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->select('name', 'email as user_email')
            ->get();
```

`distinct` 메서드는 중복된 결과를 제거하도록 쿼리를 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스를 가지고 있고, 기존 선택 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 (Raw Expressions)

때때로 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 이럴 때 `DB` 파사드의 `raw` 메서드를 사용하여 원시 문자열 표현식을 생성할 수 있습니다:

```php
$users = DB::table('users')
             ->select(DB::raw('count(*) as user_count, status'))
             ->where('status', '<>', 1)
             ->groupBy('status')
             ->get();
```

> [!NOTE]
> 원시 문장은 쿼리에 문자열로 직접 삽입되기 때문에, SQL 인젝션 취약점을 만들지 않도록 특히 주의해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드 (Raw Methods)

`DB::raw` 메서드 대신 다음 메서드들을 사용해 쿼리의 여러 부분에 원시 표현식을 삽입할 수 있습니다. **단, 원시 표현식을 사용하는 쿼리가 SQL 인젝션으로부터 안전하다고 Laravel이 보장하지는 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(...))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
                ->selectRaw('price * ? as price_with_tax', [1.0825])
                ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw` / `orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 원시 "where" 절을 주입하는 데 사용됩니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 받습니다:

```php
$orders = DB::table('orders')
                ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw` / `orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드로 "having" 절에 원시 문자열을 지정할 수 있습니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 받습니다:

```php
$orders = DB::table('orders')
                ->select('department', DB::raw('SUM(price) as total_sales'))
                ->groupBy('department')
                ->havingRaw('SUM(price) > ?', [2500])
                ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 원시 문자열을 지정할 수 있습니다:

```php
$orders = DB::table('orders')
                ->orderByRaw('updated_at - created_at DESC')
                ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 원시 문자열을 지정할 수 있습니다:

```php
$orders = DB::table('orders')
                ->select('city', 'state')
                ->groupByRaw('city, state')
                ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 (Inner Join 절)

쿼리 빌더는 조인 절을 추가하는 데도 사용됩니다. 기본적인 "inner join"을 하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. `join` 메서드의 첫 번째 인자는 조인할 테이블명이고, 나머지 인자는 조인 조건의 컬럼 제약을 지정합니다. 하나의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->join('contacts', 'users.id', '=', 'contacts.user_id')
            ->join('orders', 'users.id', '=', 'orders.user_id')
            ->select('users.*', 'contacts.phone', 'orders.price')
            ->get();
```

<a name="left-join-right-join-clause"></a>
#### 왼쪽/오른쪽 조인 (Left Join / Right Join 절)

"inner join" 대신 "left join" 또는 "right join"을 수행하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이 메서드들의 시그니처는 `join` 메서드와 같습니다:

```php
$users = DB::table('users')
            ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();

$users = DB::table('users')
            ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 (Cross Join 절)

`crossJoin` 메서드는 "cross join"을 수행합니다. 크로스 조인은 첫 번째 테이블과 조인된 테이블 사이의 데카르트 곱(cartesian product)을 생성합니다:

```php
$sizes = DB::table('sizes')
            ->crossJoin('colors')
            ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 절을 구성하려면, `join` 메서드 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 인자로 받아 "join" 절에 조건을 지정할 수 있도록 합니다:

```php
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')->orOn(...);
        })
        ->get();
```

조인에서 "where" 절을 사용하려면 `JoinClause` 인스턴스가 제공하는 `where` 및 `orWhere` 메서드를 사용하면 됩니다. 이 메서드들은 두 컬럼 간 비교 대신 컬럼과 값 간 비교를 합니다:

```php
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')
                 ->where('contacts.user_id', '>', 5);
        })
        ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리를 서브쿼리에 조인할 수 있습니다. 각 메서드는 세 개의 인자를 받는데, 서브쿼리, 서브쿼리의 테이블 별칭(alias), 그리고 조인 컬럼을 정의하는 클로저입니다. 다음 예제는 각 사용자에 대해 가장 최근에 게시한 블로그 글의 `created_at` 타임스탬프도 함께 조회합니다:

```php
$latestPosts = DB::table('posts')
                   ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                   ->where('is_published', true)
                   ->groupBy('user_id');

$users = DB::table('users')
        ->joinSub($latestPosts, 'latest_posts', function ($join) {
            $join->on('users.id', '=', 'latest_posts.user_id');
        })->get();
```

<a name="unions"></a>
## 유니언 (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 유니언하여 합치는 `union` 메서드도 제공합니다. 예를 들어, 하나의 초기 쿼리를 만들고, `union` 메서드로 다른 쿼리와 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
            ->whereNull('first_name');

$users = DB::table('users')
            ->whereNull('last_name')
            ->union($first)
            ->get();
```

`union` 메서드 외에, 중복 결과를 제거하지 않는 `unionAll` 메서드도 있습니다. `unionAll`의 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용해 쿼리에 WHERE 조건을 추가할 수 있습니다. 가장 단순한 형태는 세 개의 인자를 받는데, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, `votes` 컬럼 값이 100이고, `age` 컬럼 값이 35보다 큰 사용자들을 조회하는 쿼리입니다:

```php
$users = DB::table('users')
                ->where('votes', '=', 100)
                ->where('age', '>', 35)
                ->get();
```

편의를 위해 `=` 연산자를 사용하려면 연산자 인자를 생략하고 값만 두 번째 인자로 넘길 수 있습니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

위에서 말한 대로, 데이터베이스가 지원하는 모든 연산자를 사용할 수 있습니다:

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

`where` 메서드에 조건 배열을 넘길 수도 있습니다. 배열의 각 요소는 `where` 메서드에 통상 전달하는 세 가지 인자를 담은 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!NOTE]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 쿼리에서 참조할 컬럼명(예: order by 컬럼)을 사용자 입력에 의존하지 않도록 해야 합니다.

<a name="or-where-clauses"></a>
### OR WHERE 절

`where` 메서드를 연결해서 호출하면 조건들은 `and` 연산자로 연결됩니다. 그러나 `orWhere` 메서드를 사용하면 `or` 연산자로 조건을 연결할 수 있습니다. `orWhere`는 `where`와 동일한 인자를 받습니다:

```php
$users = DB::table('users')
                    ->where('votes', '>', 100)
                    ->orWhere('name', 'John')
                    ->get();
```

`orWhere` 조건을 괄호로 묶어 그룹핑하려면, 클로저를 첫 번째 인자로 넘기면 됩니다:

```php
$users = DB::table('users')
            ->where('votes', '>', 100)
            ->orWhere(function($query) {
                $query->where('name', 'Abigail')
                      ->where('votes', '>', 50);
            })
            ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!NOTE]
> 글로벌 스코프가 적용될 때 예상치 못한 동작을 방지하려면 `orWhere` 호출을 항상 그룹핑해야 합니다.

<a name="json-where-clauses"></a>
### JSON WHERE 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼을 쿼리할 수 있습니다. 현재 MySQL 5.7+, PostgreSQL, SQL Server 2016 이상, SQLite 3.9.0 이상([JSON1 확장](https://www.sqlite.org/json1.html) 필요)를 지원합니다. JSON 컬럼 쿼리는 `->` 연산자를 사용합니다:

```php
$users = DB::table('users')
                ->where('preferences->dining->meal', 'salad')
                ->get();
```

`whereJsonContains` 메서드는 JSON 배열 내에 특정 값이 포함되어 있는지 검사합니다. 단, SQLite에서는 지원되지 않습니다:

```php
$users = DB::table('users')
                ->whereJsonContains('options->languages', 'en')
                ->get();
```

MySQL 또는 PostgreSQL을 사용할 경우, 배열 형태로 여러 값을 전달해도 됩니다:

```php
$users = DB::table('users')
                ->whereJsonContains('options->languages', ['en', 'de'])
                ->get();
```

`whereJsonLength` 메서드는 JSON 배열 길이를 기준으로 쿼리할 수 있습니다:

```php
$users = DB::table('users')
                ->whereJsonLength('options->languages', 0)
                ->get();

$users = DB::table('users')
                ->whereJsonLength('options->languages', '>', 1)
                ->get();
```

<a name="additional-where-clauses"></a>
### 추가 WHERE 절

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 지정한 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
           ->whereBetween('votes', [1, 100])
           ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 지정한 두 값 범위 밖에 있는지 확인합니다:

```php
$users = DB::table('users')
                    ->whereNotBetween('votes', [1, 100])
                    ->get();
```

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 지정된 배열에 포함되어 있는지 확인합니다:

```php
$users = DB::table('users')
                    ->whereIn('id', [1, 2, 3])
                    ->get();
```

`whereNotIn`은 컬럼 값이 지정된 배열에 포함되어 있지 않은지 확인합니다:

```php
$users = DB::table('users')
                    ->whereNotIn('id', [1, 2, 3])
                    ->get();
```

> [!NOTE]
> 큰 배열로 정수 바인딩을 추가할 때는 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용해 메모리 사용량을 크게 줄일 수 있습니다.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 지정한 컬럼 값이 `NULL`인지 검사합니다:

```php
$users = DB::table('users')
                ->whereNull('updated_at')
                ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아닌지 검사합니다:

```php
$users = DB::table('users')
                ->whereNotNull('updated_at')
                ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼의 값을 특정 날짜와 비교할 때 사용합니다:

```php
$users = DB::table('users')
                ->whereDate('created_at', '2016-12-31')
                ->get();
```

`whereMonth`는 컬럼 값을 특정 월과 비교합니다:

```php
$users = DB::table('users')
                ->whereMonth('created_at', '12')
                ->get();
```

`whereDay`는 컬럼 값을 특정 일자와 비교합니다:

```php
$users = DB::table('users')
                ->whereDay('created_at', '31')
                ->get();
```

`whereYear`는 컬럼 값을 특정 연도와 비교합니다:

```php
$users = DB::table('users')
                ->whereYear('created_at', '2016')
                ->get();
```

`whereTime`은 컬럼 값을 특정 시간과 비교합니다:

```php
$users = DB::table('users')
                ->whereTime('created_at', '=', '11:20:45')
                ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼 값이 같은지 검증합니다:

```php
$users = DB::table('users')
                ->whereColumn('first_name', 'last_name')
                ->get();
```

비교 연산자를 직접 전달할 수도 있습니다:

```php
$users = DB::table('users')
                ->whereColumn('updated_at', '>', 'created_at')
                ->get();
```

컬럼 비교 배열을 전달하면 조건들은 `and` 연산자로 연결됩니다:

```php
$users = DB::table('users')
                ->whereColumn([
                    ['first_name', '=', 'last_name'],
                    ['updated_at', '>', 'created_at'],
                ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화 (Logical Grouping)

때로는 여러 WHERE 절을 괄호로 묶어 논리적으로 그룹화해야 할 때가 있습니다. 특히 `orWhere`를 사용할 때는 예기치 않은 쿼리 동작을 피하기 위해 항상 그룹핑하는 게 좋습니다. 이를 위해 `where` 메서드에 클로저를 전달하면 됩니다:

```php
$users = DB::table('users')
           ->where('name', '=', 'John')
           ->where(function ($query) {
               $query->where('votes', '>', 100)
                     ->orWhere('title', '=', 'Admin');
           })
           ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!NOTE]
> 글로벌 스코프 적용 시 예상치 못한 동작을 막기 위해 `orWhere` 호출을 항상 그룹핑하세요.

<a name="advanced-where-clauses"></a>
### 고급 WHERE 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### WHERE EXISTS 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있게 합니다. 이 메서드는 클로저를 인자로 받으며, 클로저는 query builder 인스턴스를 받아 "exists" 절 내부에 들어갈 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
           ->whereExists(function ($query) {
               $query->select(DB::raw(1))
                     ->from('orders')
                     ->whereColumn('orders.user_id', 'users.id');
           })
           ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 WHERE 절

때때로 서브쿼리 결과와 값을 비교하는 "where" 절을 작성할 필요가 있습니다. 이때 `where` 메서드에 클로저와 비교할 값을 넘기면 됩니다. 예를 들어, 특정 타입의 최근 멤버십이 있는 모든 사용자를 조회하는 예:

```php
use App\Models\User;

$users = User::where(function ($query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

또는 컬럼과 서브쿼리 결과를 비교할 수도 있습니다. 이때는 컬럼, 연산자, 클로저를 인자로 넘깁니다. 아래는 평균보다 적은 금액의 모든 수입 기록을 조회하는 예입니다:

```php
use App\Models\Income;

$incomes = Income::where('amount', '<', function ($query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋 (Ordering, Grouping, Limit & Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 지정한 컬럼으로 정렬합니다. 첫 인자는 정렬할 컬럼명, 두 번째 인자는 정렬 방향으로 `asc` 또는 `desc` 중 하나입니다:

```php
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->orderBy('email', 'asc')
                ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 컬럼 기준 정렬을 편하게 해줍니다. 기본값은 `created_at` 컬럼이며, 컬럼명을 지정할 수도 있습니다:

```php
$user = DB::table('users')
                ->latest()
                ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드는 쿼리 결과를 무작위로 정렬합니다. 예를 들어, 무작위 사용자를 가져올 때 사용할 수 있습니다:

```php
$randomUser = DB::table('users')
                ->inRandomOrder()
                ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거

`reorder` 메서드는 이전에 지정했던 모든 `order by` 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder`가 컬럼명과 방향 인자를 받을 경우, 기존의 모든 `order by` 절을 제거하고 완전히 새로 정렬 조건을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having` 메서드는 쿼리 결과를 그룹화할 때 사용합니다. `having` 메서드의 시그니처는 `where` 메서드와 유사합니다:

```php
$users = DB::table('users')
                ->groupBy('account_id')
                ->having('account_id', '>', 100)
                ->get();
```

`havingBetween` 메서드를 사용해 범위 내 조건을 지정할 수도 있습니다:

```php
$report = DB::table('orders')
                ->selectRaw('count(id) as number_of_orders, customer_id')
                ->groupBy('customer_id')
                ->havingBetween('number_of_orders', [5, 15])
                ->get();
```

`groupBy`는 여러 컬럼을 인수로 받아 그룹화할 수 있습니다:

```php
$users = DB::table('users')
                ->groupBy('first_name', 'status')
                ->having('account_id', '>', 100)
                ->get();
```

더 복잡한 `having` 절을 만들려면 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 제한 및 오프셋 (Limit & Offset)

<a name="skip-take"></a>
#### `skip` 및 `take` 메서드

`skip`과 `take` 메서드를 통해 결과 개수를 제한하거나 건너뛸 수 있습니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

또는 `limit`과 `offset` 메서드를 사용해도 되며, 기능적으로 `take`와 `skip`과 같습니다:

```php
$users = DB::table('users')
                ->offset(10)
                ->limit(5)
                ->get();
```

<a name="conditional-clauses"></a>
## 조건절 (Conditional Clauses)

때때로 특정 조건이 충족될 때만 쿼리 절을 적용하고 싶을 수 있습니다. 예를 들어, HTTP 요청에 특정 입력값이 있을 때만 `where` 절을 추가하려는 경우가 그렇습니다. 이럴 때는 `when` 메서드를 사용하세요:

```php
$role = $request->input('role');

$users = DB::table('users')
                ->when($role, function ($query, $role) {
                    return $query->where('role_id', $role);
                })
                ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 두 번째 인자로 주어진 클로저를 실행합니다. `false`면 클로저가 실행되지 않습니다. 위 예제로 보면, `role` 입력값이 있고 참으로 평가되어야 클로저가 실행됩니다.

세 번째 인수로 또 다른 클로저를 넘길 수 있으며, 이는 첫 번째 인자가 `false`일 경우에만 실행됩니다. 예시로, 기본 정렬 방식을 조건에 따라 다르게 지정하는 예제입니다:

```php
$sortByVotes = $request->input('sort_by_votes');

$users = DB::table('users')
                ->when($sortByVotes, function ($query, $sortByVotes) {
                    return $query->orderBy('votes');
                }, function ($query) {
                    return $query->orderBy('name');
                })
                ->get();
```

<a name="insert-statements"></a>
## INSERT 문 (Insert Statements)

쿼리 빌더는 `insert` 메서드를 제공하며, 이를 통해 데이터를 테이블에 삽입할 수 있습니다. `insert` 메서드는 컬럼과 값이 담긴 배열을 인자로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

한 번에 여러 레코드를 삽입하려면 배열의 배열을 넘기면 됩니다. 각 배열이 하나의 레코드를 나타냅니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 중 에러가 발생해도 무시합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

> [!NOTE]
> `insertOrIgnore`는 중복 레코드를 무시하며, 데이터베이스 엔진에 따라 다른 타입의 에러도 무시할 수 있습니다. 예를 들어, MySQL에서는 [엄격 모드(strict mode)](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다.

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입 후 바로 ID 값을 가져올 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!NOTE]
> PostgreSQL에서는 `insertGetId` 메서드가 자동 증가 컬럼 이름이 `id`일 것으로 기대합니다. 다른 시퀀스에서 ID를 가져오려면 두 번째 인자로 컬럼명을 넘길 수 있습니다.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 컬럼을 업데이트합니다. 첫 번째 인자는 삽입 혹은 업데이트할 값들, 두 번째 인자는 해당 테이블 내에서 유일한 레코드를 식별하는 컬럼들, 세 번째 인자는 업데이트할 컬럼 목록입니다:

```php
DB::table('flights')->upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

위 예제는 `departure`와 `destination` 컬럼 조합이 같은 레코드가 이미 있다면 해당 레코드의 `price` 컬럼만 업데이트합니다. 없다면 새로운 레코드를 삽입합니다.

> [!NOTE]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 두 번째 인자의 컬럼들이 "primary" 또는 "unique" 인덱스로 설정되어 있어야 합니다. MySQL 드라이버는 두 번째 인자를 무시하고 테이블의 모든 "primary" 및 "unique" 인덱스를 기준으로 중복 여부를 판단합니다.

<a name="update-statements"></a>
## UPDATE 문 (Update Statements)

쿼리 빌더는 기존 레코드도 `update` 메서드로 수정할 수 있습니다. `update`는 컬럼명과 값이 담긴 배열을 받으며, 영향을 받은 행 수를 반환합니다. `where` 절로 수정을 제한할 수 있습니다:

```php
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입 (Update Or Insert)

존재하는 레코드는 수정하고, 없으면 새로 만들고 싶을 때 `updateOrInsert` 메서드를 사용합니다. 인자로 비교 조건과 업데이트할 컬럼·값 배열을 받습니다.

`updateOrInsert`는 첫 번째 인자를 기준으로 데이터베이스에서 레코드를 탐색합니다. 있으면 두 번째 인자로 수정을 하고, 없으면 두 인자를 병합해 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼을 업데이트할 때는 `->` 문법을 써서 JSON 객체 내 적절한 키를 지정해야 합니다. 이 기능은 MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 (Increment & Decrement)

쿼리 빌더는 컬럼 값을 증가 혹은 감소시키는 편리한 메서드를 제공합니다. 첫 번째 인자는 수정할 컬럼명이 반드시 필요합니다. 두 번째 인자로는 증감값을 지정할 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

동시에 다른 컬럼을 업데이트할 수도 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

<a name="delete-statements"></a>
## DELETE 문 (Delete Statements)

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제합니다. 영향 받은 행 수를 반환하며, 삭제 전에 `where` 절로 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

전체 테이블을 비우고 자동 증가 ID도 초기화하려면 `truncate` 메서드를 사용하세요:

```php
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
#### 테이블 비우기와 PostgreSQL

PostgreSQL에서 테이블을 비우면 `CASCADE` 동작이 적용되어 관련된 외래 키 레코드들도 함께 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문에 "비관적 잠금" 기능을 제공합니다. "공유 잠금(shared lock)"을 걸려면 `sharedLock` 메서드를 호출하세요. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행의 수정을 막습니다:

```php
DB::table('users')
        ->where('votes', '>', 100)
        ->sharedLock()
        ->get();
```

또는 `lockForUpdate` 메서드를 쓸 수 있는데, 이 잠금은 선택된 레코드가 수정되거나 다른 공유 잠금으로 조회되는 것을 방지합니다:

```php
DB::table('users')
        ->where('votes', '>', 100)
        ->lockForUpdate()
        ->get();
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리 만드는 도중 현재 쿼리 바인딩과 SQL을 출력하려면 `dd` 또는 `dump` 메서드를 사용할 수 있습니다. `dd`는 출력 후 요청 실행을 중단하고, `dump`는 출력 후 계속 실행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```