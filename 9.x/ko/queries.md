# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 청크 단위로 처리하기](#chunking-results)
    - [느리게 결과를 스트리밍하기](#streaming-results-lazily)
    - [집계 함수들](#aggregates)
- [SELECT 문](#select-statements)
- [RAW 표현식](#raw-expressions)
- [조인](#joins)
- [유니언](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
    - [전문 검색 FULL TEXT WHERE 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한 & 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한 & 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [UPDATE 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 & 감소](#increment-and-decrement)
- [DELETE 문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 편리하고 유연한 인터페이스를 제공하여 데이터베이스 쿼리를 생성하고 실행할 수 있게 도와줍니다. 애플리케이션 내 대부분의 데이터베이스 작업에 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 쿼리 바인딩으로 전달되는 문자열을 별도로 정리하거나 세척할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼 이름에 대한 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조하는 컬럼 이름(예: `order by` 컬럼)을 결정하도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드의 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. 이 메서드는 지정한 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하며, 이어서 제약 조건을 체이닝하고 `get` 메서드로 최종 결과를 조회할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 목록으로 보여줍니다.
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

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 이 컬렉션의 각 결과는 PHP의 `stdClass` 객체입니다. 개별 컬럼 값은 객체의 속성으로 접근할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터를 매핑하거나 축약하는 매우 강력한 메서드를 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/9.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 또는 단일 컬럼 값 조회하기

데이터베이스 테이블에서 단일 행만 필요할 때는 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

전체 행 대신 특정 컬럼 값만 추출하려면 `value` 메서드를 사용하세요. 이 메서드는 해당 컬럼의 값을 직접 반환합니다:

```
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용할 수 있습니다:

```
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

특정 컬럼의 값들만 모은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면 `pluck` 메서드를 사용하세요. 예를 들어, 사용자들의 타이틀 목록을 조회하는 방법은 다음과 같습니다:

```
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

또한, 두 번째 인수를 지정하여 결과 컬렉션의 키로 사용할 컬럼을 정의할 수 있습니다:

```
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청크 단위로 처리하기 (Chunking Results)

수천 개의 데이터 레코드를 다뤄야 할 때는 `DB` 파사드의 `chunk` 메서드 사용을 고려하세요. 이 메서드는 한 번에 적은 양의 결과만 불러와 클로저에 전달하여 처리할 수 있게 합니다. 예를 들어 `users` 테이블 전체를 100개씩 나누어 처리하려면 다음과 같이 합니다:

```
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    foreach ($users as $user) {
        //
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리를 중단할 수 있습니다:

```
DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    // 레코드 처리...

    return false;
});
```

청크 단위로 처리하면서 데이터 레코드를 업데이트할 경우, 결과가 예상치 못하게 변할 수 있습니다. 만약 청크 처리 중 값을 변경할 계획이라면 대신 `chunkById` 메서드를 사용하는 것이 안전합니다. 이 메서드는 기본 키를 기준으로 자동으로 페이지네이션합니다:

```
DB::table('users')->where('active', false)
    ->chunkById(100, function ($users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

> [!WARNING]
> 청크 콜백 내에서 레코드를 업데이트하거나 삭제할 때 기본 키(primary key) 또는 외래 키(foreign key)가 변경되면 청크 쿼리에 영향을 주어 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 느리게 결과를 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [`chunk` 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백에 넘기지 않고 [`LazyCollection`](/docs/9.x/collections#lazy-collections) 인스턴스를 반환합니다. 이를 이용해 결과를 하나의 스트림처럼 처리할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

역시 청크 처리 중 값을 갱신할 경우, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드들은 기본 키를 기준으로 자동 페이징을 수행합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 순회하며 레코드 업데이트 또는 삭제 시 기본 키나 외래 키가 변할 경우 쿼리에 영향을 주어 일부 결과가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수들 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 함수도 지원합니다. 이 메서드들은 쿼리를 구성한 후 호출할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 조건절과 결합해 집계값 계산을 조정할 수도 있습니다:

```
$price = DB::table('orders')
                ->where('finalized', 1)
                ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 데이터 존재 여부 확인하기

`count` 대신 `exists` 및 `doesntExist` 메서드를 사용하여 조건에 맞는 데이터가 존재하는지 쉽게 판단할 수 있습니다:

```
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

항상 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용해 원하는 "select" 절을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->select('name', 'email as user_email')
            ->get();
```

`distinct` 메서드는 결과를 중복 없이 반환하도록 강제합니다:

```
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있을 때, 기존 select 절에 컬럼을 추가하려면 `addSelect` 메서드를 사용하세요:

```
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## RAW 표현식 (Raw Expressions)

쿼리에 임의의 문자열을 삽입해야 할 경우 `DB` 파사드가 제공하는 `raw` 메서드를 사용해 RAW 표현식을 만들 수 있습니다:

```
$users = DB::table('users')
             ->select(DB::raw('count(*) as user_count, status'))
             ->where('status', '<>', 1)
             ->groupBy('status')
             ->get();
```

> [!WARNING]
> RAW 문은 쿼리 문자열에 직접 삽입되므로, SQL 인젝션 취약점 발생에 매우 주의해야 합니다.

<a name="raw-methods"></a>
### RAW 메서드들

`DB::raw` 대신 다음 메서드들을 사용해 쿼리의 여러 부분에 RAW 표현식을 직접 삽입할 수 있습니다. **다만 RAW 표현식을 사용하는 쿼리는 Laravel이 SQL 인젝션 방지 보장을 제공하지 않음을 기억하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용 가능하며, 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```
$orders = DB::table('orders')
                ->selectRaw('price * ? as price_with_tax', [1.0825])
                ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 와 `orWhereRaw` 메서드는 쿼리에 RAW "where" 절을 삽입할 때 사용하며, 둘 다 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```
$orders = DB::table('orders')
                ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 와 `orHavingRaw` 메서드는 RAW "having" 절을 넣을 때 사용됩니다. 이들 역시 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```
$orders = DB::table('orders')
                ->select('department', DB::raw('SUM(price) as total_sales'))
                ->groupBy('department')
                ->havingRaw('SUM(price) > ?', [2500])
                ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 RAW "order by" 절에 문자열을 직접 지정할 때 사용합니다:

```
$orders = DB::table('orders')
                ->orderByRaw('updated_at - created_at DESC')
                ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 RAW `group by` 절에 문자열을 전달할 때 사용됩니다:

```
$orders = DB::table('orders')
                ->select('city', 'state')
                ->groupByRaw('city, state')
                ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 (Inner Join) 절

쿼리 빌더로 조인 절을 추가할 수 있습니다. 기본 내부 조인을 하려면 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블명이며, 이후 인수로 조인할 컬럼 조건을 지정합니다. 여러 테이블을 한 쿼리에 조인할 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->join('contacts', 'users.id', '=', 'contacts.user_id')
            ->join('orders', 'users.id', '=', 'orders.user_id')
            ->select('users.*', 'contacts.phone', 'orders.price')
            ->get();
```

<a name="left-join-right-join-clause"></a>
#### LEFT 조인 / RIGHT 조인 절

내부 조인 대신 "left join"이나 "right join"을 하고 싶으면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 인수 구조는 `join`과 같습니다:

```
$users = DB::table('users')
            ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();

$users = DB::table('users')
            ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
            ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 절

`crossJoin` 메서드를 사용하면 두 테이블 간 데카르트 곱(cartesian product) 형태인 "cross join"을 수행할 수 있습니다:

```
$sizes = DB::table('sizes')
            ->crossJoin('colors')
            ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 조건을 지정하려면 `join` 메서드에 두 번째 인수로 클로저를 전달하세요. 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받으며, `join` 절에 대한 제약 조건을 정의할 수 있습니다:

```
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
        })
        ->get();
```

조인에 "where" 절을 포함시키려면 `JoinClause` 인스턴스의 `where` 와 `orWhere` 메서드를 사용하세요. 이 메서드들은 컬럼끼리 비교하는 대신, 컬럼과 값을 비교합니다:

```
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')
                 ->where('contacts.user_id', '>', 5);
        })
        ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인 (Subquery Joins)

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리를 서브쿼리와 조인할 수 있습니다. 각 메서드는 3개의 인수를 받습니다: 서브쿼리, 서브쿼리의 테이블 별칭, 그리고 관련 컬럼 정의를 위한 클로저입니다. 다음 예시는 각 사용자 데이터에 가장 최근 게시한 블로그 글의 `created_at` 타임스탬프를 포함시킵니다:

```
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

쿼리 빌더는 두 개 이상의 쿼리를 "union"하는 편리한 메서드를 제공합니다. 예를 들어, 초기 쿼리를 만들고 `union` 메서드로 추가 쿼리와 합칠 수 있습니다:

```
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
            ->whereNull('first_name');

$users = DB::table('users')
            ->whereNull('last_name')
            ->union($first)
            ->get();
```

`union` 외에 `unionAll` 메서드도 존재합니다. `unionAll`은 중복 결과를 제거하지 않고 모든 결과를 합칩니다. 사용법은 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드는 "where" 절을 추가할 때 사용합니다. 기본 형태는 세 개의 인수를 받습니다. 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, `votes` 컬럼이 `100`이고 `age` 컬럼이 35 초과인 사용자를 조회하는 쿼리는 다음과 같습니다:

```
$users = DB::table('users')
                ->where('votes', '=', 100)
                ->where('age', '>', 35)
                ->get();
```

간편하게, `=` 연산자인 경우 두 번째 인자에 값을 바로 전달할 수 있습니다:

```
$users = DB::table('users')->where('votes', 100)->get();
```

지원하는 모든 데이터베이스 연산자를 사용할 수 있습니다:

```
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

`where` 메서드에 조건 배열을 넘겨 여러 조건을 동시에 지정할 수도 있습니다. 배열 각 요소는 다시 `where`에 전달할 세 인자 배열이어야 합니다:

```
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리의 컬럼명(예: order by 컬럼)을 결정하도록 절대 허용하지 마세요.

<a name="or-where-clauses"></a>
### OR WHERE 절

기본적으로 `where` 메서드 호출들은 `and` 연산자로 연결됩니다. 그러나 `orWhere` 메서드를 사용하면 `or` 연산자로 절을 추가할 수 있습니다. `orWhere`도 `where`와 동일한 인자를 받습니다:

```
$users = DB::table('users')
                    ->where('votes', '>', 100)
                    ->orWhere('name', 'John')
                    ->get();
```

OR 조건을 괄호로 묶어 그룹화해야 할 경우, 첫 번째 인수로 클로저를 전달할 수 있습니다:

```
$users = DB::table('users')
            ->where('votes', '>', 100)
            ->orWhere(function($query) {
                $query->where('name', 'Abigail')
                      ->where('votes', '>', 50);
            })
            ->get();
```

위 예제가 생성할 SQL은 다음과 같습니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하려면 `orWhere` 호출은 반드시 그룹화해서 사용하세요.

<a name="where-not-clauses"></a>
### WHERE NOT 절

`whereNot` 및 `orWhereNot` 메서드를 사용하면 특정 쿼리 조건을 부정할 수 있습니다. 예를 들어, 깔끔하게 처리되지 않은(clerance) 상품이거나 가격이 10 미만인 상품을 제외하려면 다음과 같이 작성합니다:

```
$products = DB::table('products')
                ->whereNot(function ($query) {
                    $query->where('clearance', true)
                          ->orWhere('price', '<', 10);
                })
                ->get();
```

<a name="json-where-clauses"></a>
### JSON WHERE 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼을 조회하는 기능을 제공합니다. 현재 MySQL 5.7+, PostgreSQL, SQL Server 2016, SQLite 3.39.0 이상([JSON1 확장 기능](https://www.sqlite.org/json1.html))에서 지원됩니다. JSON 컬럼 조회 시 `->` 연산자를 사용하세요:

```
$users = DB::table('users')
                ->where('preferences->dining->meal', 'salad')
                ->get();
```

`whereJsonContains` 메서드로 JSON 배열에 특정 값이 포함되어 있는지 조회할 수 있습니다. 이 기능은 SQLite 3.38.0 미만에서는 지원하지 않습니다:

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', 'en')
                ->get();
```

MySQL 또는 PostgreSQL을 사용하는 경우, 배열을 전달해 여러 값 포함 여부도 확인할 수 있습니다:

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', ['en', 'de'])
                ->get();
```

`whereJsonLength` 메서드로 JSON 배열의 길이로 조회할 수도 있습니다:

```
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

`whereBetween` 메서드는 컬럼 값이 특정 범위 안에 포함되는지 확인합니다:

```
$users = DB::table('users')
           ->whereBetween('votes', [1, 100])
           ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 특정 범위를 벗어나 있는지 확인합니다:

```
$users = DB::table('users')
                    ->whereNotBetween('votes', [1, 100])
                    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 같은 행의 두 컬럼 값 사이에 특정 컬럼 값이 속하는지 검사합니다:

```
$patients = DB::table('patients')
                       ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

`whereNotBetweenColumns` 메서드는 해당 컬럼 값이 두 컬럼 값 사이에 있지 않은지 검사합니다:

```
$patients = DB::table('patients')
                       ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 컬럼 값이 주어진 배열 중 하나에 포함되는지 확인합니다:

```
$users = DB::table('users')
                    ->whereIn('id', [1, 2, 3])
                    ->get();
```

`whereNotIn` 메서드는 컬럼 값이 주어진 배열에 포함되지 않는지 확인합니다:

```
$users = DB::table('users')
                    ->whereNotIn('id', [1, 2, 3])
                    ->get();
```

두 번째 인수로 서브쿼리 객체를 넘길 수도 있습니다:

```
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
                    ->whereIn('user_id', $activeUsers)
                    ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 많은 정수 바인딩 배열을 쿼리에 추가할 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 주어진 컬럼 값이 `NULL` 인지 확인합니다:

```
$users = DB::table('users')
                ->whereNull('updated_at')
                ->get();
```

`whereNotNull` 메서드는 컬럼 값이 `NULL`이 아닌지 확인합니다:

```
$users = DB::table('users')
                ->whereNotNull('updated_at')
                ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜 혹은 시간대로 컬럼 값을 비교할 때 각 메서드를 사용하세요:

```
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

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼이 같은지 비교합니다:

```
$users = DB::table('users')
                ->whereColumn('first_name', 'last_name')
                ->get();
```

비교 연산자도 전달할 수 있습니다:

```
$users = DB::table('users')
                ->whereColumn('updated_at', '>', 'created_at')
                ->get();
```

배열을 전달해 여러 컬럼 비교 조건을 `and`로 연결할 수도 있습니다:

```
$users = DB::table('users')
                ->whereColumn([
                    ['first_name', '=', 'last_name'],
                    ['updated_at', '>', 'created_at'],
                ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

여러 WHERE 절을 논리적으로 묶어 괄호로 감싸야 할 때 클로저를 `where`에 전달해 그룹화할 수 있습니다. 특히 `orWhere` 호출은 의도치 않은 쿼리 결과를 막기 위해 기본적으로 항상 그룹화해야 합니다:

```
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

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하려면 `orWhere` 호출은 반드시 그룹화해서 사용하세요.

<a name="advanced-where-clauses"></a>
### 고급 WHERE 절

<a name="where-exists-clauses"></a>
### WHERE EXISTS 절

`whereExists` 메서드는 SQL의 "where exists" 절을 작성할 때 사용합니다. 클로저에 쿼리 빌더 인스턴스를 전달하며, 이 안에서 "exists" 절 내 서브쿼리를 정의할 수 있습니다:

```
$users = DB::table('users')
           ->whereExists(function ($query) {
               $query->select(DB::raw(1))
                     ->from('orders')
                     ->whereColumn('orders.user_id', 'users.id');
           })
           ->get();
```

생성되는 SQL은 다음과 같습니다:

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

서브쿼리 결과와 값을 비교하는 where 절을 구성하려면 `where` 메서드에 클로저와 값을 함께 전달하세요. 예를 들어, 최근 회원권이 특정 타입인 유저를 조회하려면:

```
use App\Models\User;

$users = User::where(function ($query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

컬럼과 서브쿼리 결과를 비교하려면 컬럼명, 연산자, 클로저를 `where`에 전달합니다. 예를 들어 평균보다 적은 소득을 조회하려면:

```
use App\Models\Income;

$incomes = Income::where('amount', '<', function ($query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색 FULL TEXT WHERE 절

> [!WARNING]
> 전문 검색 WHERE 절은 현재 MySQL과 PostgreSQL만 지원합니다.

`whereFullText` 와 `orWhereFullText` 메서드는 [전문 검색 인덱스](/docs/9.x/migrations#available-index-types)가 생성된 컬럼에 대해 전문 검색 WHERE 절을 쉽게 작성할 수 있게 해줍니다. Laravel은 데이터베이스에 맞는 적절한 SQL을 생성합니다. 예를 들어 MySQL의 경우 `MATCH AGAINST` 구문이 생성됩니다:

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 & 오프셋 (Ordering, Grouping, Limit & Offset)

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 특정 컬럼 기준으로 정렬할 때 사용합니다. 첫 번째 인수는 정렬할 컬럼명이며, 두 번째 인수는 정렬 방향으로 `asc` 또는 `desc`를 지정합니다:

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->get();
```

여러 컬럼 기준으로 정렬하려면 `orderBy`를 여러 번 호출하세요:

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->orderBy('email', 'asc')
                ->get();
```

<a name="latest-oldest"></a>
#### `latest` & `oldest` 메서드

`latest` 와 `oldest` 메서드는 기본적으로 `created_at` 컬럼을 기준으로 날짜 역순/오름차순 정렬을 쉽게 할 수 있습니다. 물론 정렬할 컬럼을 직접 지정할 수도 있습니다:

```
$user = DB::table('users')
                ->latest()
                ->first();
```

<a name="random-ordering"></a>
#### 임의 순서 정렬하기

`inRandomOrder` 메서드로 쿼리 결과를 랜덤하게 정렬할 수 있습니다. 예를 들어 무작위 사용자 한 명을 가져올 때 사용합니다:

```
$randomUser = DB::table('users')
                ->inRandomOrder()
                ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거하기

`reorder` 메서드는 기존에 적용된 모든 `order by` 절을 제거합니다:

```
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드에 정렬할 컬럼과 방향을 전달하면 기존 정렬 조건을 제거한 뒤 새로 지정한 정렬 조건을 적용합니다:

```
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` & `having` 메서드

`groupBy` 와 `having` 메서드로 결과를 특정 컬럼별로 그룹화할 수 있습니다. `having` 메서드는 `where` 메서드와 유사한 시그니처를 갖습니다:

```
$users = DB::table('users')
                ->groupBy('account_id')
                ->having('account_id', '>', 100)
                ->get();
```

`havingBetween` 메서드는 범위 내 조건으로 필터링할 때 사용합니다:

```
$report = DB::table('orders')
                ->selectRaw('count(id) as number_of_orders, customer_id')
                ->groupBy('customer_id')
                ->havingBetween('number_of_orders', [5, 15])
                ->get();
```

여러 컬럼별로 그룹화하려면 여러 인수를 `groupBy` 메서드에 전달하세요:

```
$users = DB::table('users')
                ->groupBy('first_name', 'status')
                ->having('account_id', '>', 100)
                ->get();
```

더 복잡한 `having` 조건은 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 제한 & 오프셋

<a name="skip-take"></a>
#### `skip` & `take` 메서드

`skip`과 `take` 메서드로 결과 개수를 제한하거나 특정 개수를 건너뛸 수 있습니다:

```
$users = DB::table('users')->skip(10)->take(5)->get();
```

기능상 동일한 `limit` 과 `offset` 메서드도 사용할 수 있습니다:

```
$users = DB::table('users')
                ->offset(10)
                ->limit(5)
                ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

특정 조건에 따라 쿼리 절을 적용하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에 특정 값이 있는 경우에만 WHERE 절을 추가하고 싶다면 `when` 메서드를 사용하세요:

```
$role = $request->input('role');

$users = DB::table('users')
                ->when($role, function ($query, $role) {
                    $query->where('role_id', $role);
                })
                ->get();
```

`when` 메서드는 첫 번째 인수가 참일 때만 클로저를 실행합니다. 만약 거짓이면 클로저가 실행되지 않습니다. 위 예에서는 요청에 `role` 필드가 존재하고 참 값일 때만 조건절이 추가됩니다.

세 번째 인수로 다른 클로저를 전달할 수 있는데, 이는 첫 번째 인수가 거짓일 때 실행됩니다. 이를 활용해 기본 정렬 방식을 설정할 수 있습니다:

```
$sortByVotes = $request->input('sort_by_votes');

$users = DB::table('users')
                ->when($sortByVotes, function ($query, $sortByVotes) {
                    $query->orderBy('votes');
                }, function ($query) {
                    $query->orderBy('name');
                })
                ->get();
```

<a name="insert-statements"></a>
## INSERT 문 (Insert Statements)

쿼리 빌더의 `insert` 메서드는 레코드를 데이터베이스에 삽입할 때 사용합니다. 이 메서드는 컬럼명과 값의 배열을 받습니다:

```
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면, 배열의 배열 형태로 전달하세요:

```
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 도중 오류가 생겨도 무시합니다. 중복 레코드 오류나 일부 다른 오류도 무시할 수 있으니, 데이터베이스 엔진 특성을 잘 이해한 뒤 사용하세요. 예를 들어 MySQL strict 모드를 우회합니다:

```
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리를 통해 삽입할 데이터를 지정할 수 있습니다:

```
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있을 경우, `insertGetId` 메서드를 활용해 레코드 삽입 후 그 ID를 즉시 가져올 수 있습니다:

```
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL 사용 시 `insertGetId`는 기본적으로 자동 증가 컬럼명이 `id`라고 가정합니다. 다른 시퀀스에서 ID를 얻어오려면 두 번째 인자로 컬럼명을 명시해야 합니다.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 컬럼을 업데이트합니다. 첫 번째 인자는 삽입하거나 업데이트할 값 배열, 두 번째 인자는 레코드를 고유하게 식별할 컬럼들, 세 번째 인자는 업데이트할 컬럼 배열입니다:

```
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

위 예제에서 `departure`와 `destination` 값이 동일한 레코드가 있으면 `price`만 업데이트되고, 없으면 레코드를 새로 삽입합니다.

> [!WARNING]
> SQL Server 제외, 모든 데이터베이스는 `upsert` 두 번째 인자의 컬럼들에 대해 "primary" 또는 "unique" 인덱스가 있어야 합니다. MySQL 드라이버는 `upsert`의 두 번째 인자 대신 테이블의 "primary" 및 "unique" 인덱스를 자동으로 사용합니다.

<a name="update-statements"></a>
## UPDATE 문 (Update Statements)

레코드를 갱신할 때는 `update` 메서드를 사용합니다. `insert`와 마찬가지로 컬럼명과 값의 배열을 인수로 받으며, 영향을 받은 행 수를 반환합니다. `where` 절을 사용해 갱신 범위를 제한할 수 있습니다:

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update Or Insert

이미 존재하는 레코드를 업데이트하거나 없으면 새로 삽입하려면 `updateOrInsert` 메서드를 사용하세요. 첫 번째 인수는 조건 배열, 두 번째 인수는 업데이트할 컬럼과 값입니다:

```
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

해당 이메일과 이름을 가진 레코드가 있으면 `votes`를 2로 업데이트하고, 없으면 각 조건과 업데이트 값을 병합해 새 레코드를 삽입합니다.

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼의 특정 키를 업데이트하려면 `->` 구문을 키에 포함시켜 지정하세요. 이 기능은 MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다:

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 & 감소 (Increment & Decrement)

쿼리 빌더는 특정 컬럼 값을 증가 또는 감소시키는 편리한 메서드도 제공합니다. 최소 인수는 변경할 컬럼명이며, 두 번째 인수로 증가/감소할 수를 지정할 수 있습니다:

```
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하면 증가/감소 작업을 하면서 다른 컬럼도 함께 업데이트할 수 있습니다:

```
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한 `incrementEach` 와 `decrementEach` 메서드로 여러 컬럼을 한꺼번에 증감할 수도 있습니다:

```
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## DELETE 문 (Delete Statements)

`delete` 메서드로 테이블에서 레코드를 삭제할 수 있습니다. 삭제된 행 수를 반환하며, `where` 절을 추가해 삭제 대상을 제한할 수 있습니다:

```
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

테이블을 완전히 비우고(모든 레코드 제거 및 자동 증가 ID 초기화) 싶다면 `truncate` 메서드를 사용하세요:

```
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
#### 테이블 초기화와 PostgreSQL

PostgreSQL에서 `truncate`를 실행할 때는 `CASCADE` 동작이 적용되어, 관련된 외래 키가 참조하는 다른 테이블의 레코드들도 함께 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문에서 "비관적 잠금"을 실현하는 메서드를 제공합니다. "공유 잠금"을 위해 `sharedLock` 메서드를 호출하면, 트랜잭션 커밋 전까지 해당 행들이 수정되지 못합니다:

```
DB::table('users')
        ->where('votes', '>', 100)
        ->sharedLock()
        ->get();
```

또는 `lockForUpdate` 메서드를 사용해 "for update" 잠금을 걸 수 있습니다. 이 잠금은 선택한 레코드를 수정하거나 다른 공유 잠금으로 선택하는 것도 막습니다:

```
DB::table('users')
        ->where('votes', '>', 100)
        ->lockForUpdate()
        ->get();
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 빌드하는 도중 `dd` 혹은 `dump` 메서드를 사용해 현재 쿼리 바인딩과 SQL을 확인할 수 있습니다. `dd`는 디버그 정보를 출력 후 요청 실행을 중지하고, `dump`는 정보만 출력 후 요청을 계속 실행합니다:

```
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```