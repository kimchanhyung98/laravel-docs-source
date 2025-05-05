# 데이터베이스: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 분할(Chunking)](#chunking-results)
    - [지연 스트리밍(Streaming Results Lazily)](#streaming-results-lazily)
    - [집계 함수(Aggregates)](#aggregates)
- [SELECT 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Joins)](#joins)
- [UNION](#unions)
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
    - [전문검색(Full Text) WHERE 구문](#full-text-where-clauses)
- [정렬, 그룹화, LIMIT 및 OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 구문](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [Upsert](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 편리하게 생성하고 실행할 수 있도록 유창한 인터페이스를 제공합니다. 이 빌더는 어플리케이션의 대부분 데이터베이스 조작 작업에 사용할 수 있으며 Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 쿼리 빌더에 전달되는 문자열을 별도로 정제하거나 필터링할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 사용자의 입력값이 쿼리에서 참조되는 컬럼명(예:"order by" 컬럼)에 직접적으로 사용되지 않도록 해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 검색

`DB` 파사드의 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하며, 여러 제약 조건을 체이닝할 수 있고 마지막으로 `get` 메서드를 사용해 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 어플리케이션의 모든 사용자를 나열합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과가 담긴 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체입니다. 각 컬럼 값은 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑, 축소 등의 매우 강력한 메서드들을 제공합니다. 자세한 정보는 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회

데이터베이스 테이블에서 단 하나의 행만 필요하다면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

특정 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException`이 잡히지 않으면 404 HTTP 응답이 자동으로 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없다면 `value` 메서드를 사용해 단일 컬럼 값을 바로 추출할 수 있습니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

단일 컬럼 값을 담은 `Illuminate\Support\Collection` 인스턴스를 얻으려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예시는 사용자 타이틀의 컬렉션을 가져옵니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

결과 컬렉션이 사용할 키 컬럼을 두 번째 인자로 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 분할(Chunking)

수천 개의 데이터 레코드를 다뤄야 한다면 `DB` 파사드의 `chunk` 메서드 사용을 고려해보세요. 이 메서드는 한번에 소량의 결과만을 조회하고 각 청크마다 콜백에 전달하여 처리합니다. 예를 들어, 전체 `users` 테이블을 100건씩 분할해서 가져올 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

콜백에서 `false`를 반환하면 이후 청크 처리를 멈출 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크로 결과를 순회하는 동안 데이터를 업데이트한다면, 예상치 못한 결과가 발생할 수 있습니다. 이러한 경우에는 `chunkById` 메서드를 사용하세요. 이 메서드는 기본 키 기준으로 자동으로 페이지네이션합니다:

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

`chunkById` 및 `lazyById` 메서드는 쿼리 실행 시 자체적으로 "where" 조건을 추가하므로, 직접 조건을 지정할 때는 [논리 그룹화](#logical-grouping)를 참고해 그룹화하는 것이 좋습니다:

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
> 청크 콜백 내부에서 기본키 또는 외래키 값을 변경하는 update 또는 delete 작업은 쿼리 결과에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍(Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행합니다. 하지만, 각 청크를 콜백으로 전달하는 대신 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections) 형태로 전체 결과를 스트림처럼 다룰 수 있게 해줍니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 순회 과정에서 데이터를 수정할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드들은 자동으로 기본 키 기준으로 페이지네이션을 수행합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 순회 과정에서 기본키 또는 외래키 값을 수정/삭제하는 경우, 쿼리 결과에 영향이 있을 수 있으니 주의하세요.

<a name="aggregates"></a>
### 집계 함수(Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 메서드를 제공합니다. 쿼리 생성 후 이 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 메서드에 추가 조건을 결합해서 계산 방식을 세밀하게 조정할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리의 조건에 맞는 레코드가 존재하는지만 확인하려면, `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다:

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

항상 모든 컬럼을 선택하지 않고, 원하는 컬럼만 골라서 조회하려면 `select` 메서드를 사용하면 됩니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복을 제외한 결과를 받을 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스를 가지고 있다면 `addSelect` 메서드를 통해 SELECT 컬럼을 추가할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때때로 쿼리에 문자열 표현식을 직접 삽입해야 할 때는 `DB` 파사드의 `raw` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 주입되므로 반드시 SQL 인젝션 보안에 유의하세요.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 대신 아래의 메서드를 활용하여 쿼리의 여러 부분에 Raw 표현식을 삽입할 수 있습니다. **Raw 표현식이 사용된 쿼리는 SQL 인젝션으로부터 항상 안전하다고 보장할 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))`를 대체할 수 있습니다. 두 번째 인자로 바인딩 배열이 추가로 들어갈 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 Raw "where" 절을 삽입할 수 있습니다. 두 번째 인자로 바인딩 배열이 들어갑니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw`는 "having" 절에 Raw 문자열을 추가할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw`는 "order by" 절에 Raw 문자열을 사용할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw`는 "group by" 절에 Raw 문자열을 사용할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Joins)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더는 join 절을 추가하여 쿼리를 조인할 수 있습니다. 기본 "inner join"은 `join` 메서드를 통해 수행합니다. 첫 번째 인자는 조인할 테이블 명, 이후 인자들은 조인 컬럼 조건입니다. 한 쿼리에서 다수의 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하면 됩니다. 메서드 사용법은 `join`과 동일합니다:

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

"cross join"을 수행하려면 `crossJoin` 메서드를 사용하세요. cross join은 지정된 두 테이블 간의 데카르트 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 조건을 만들고 싶을 경우, 두 번째 인자로 클로저를 `join`에 전달하면 됩니다. 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받으며, 조인 조건을 자유롭게 지정할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 절이 필요하다면 JoinClause의 `where`나 `orWhere` 메서드를 사용할 수 있습니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드로 서브쿼리와 조인할 수 있습니다. 이 메서드는 서브쿼리, 테이블 별칭, 컬럼 관련 조건을 받습니다. 예를 들어, 각 user 레코드에 가장 최근 발행된 블로그 글의 `created_at` 날짜를 함께 조회할 수 있습니다:

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
> Lateral Join은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하여 서브쿼리와 "lateral join"을 수행할 수 있습니다. 두 인자를 받으며, 조인 조건은 서브쿼리의 `where` 절에 지정합니다. Lateral join은 각 행마다 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

예시: 각 사용자의 최근 블로그 글 3개까지 모두 함께 조회할 때:

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

여러 쿼리를 "union"으로 결합할 수 있습니다. 예를 들어, 초기 쿼리를 만들어 두고 `union` 메서드로 추가 쿼리와 합칩니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

기본 `union` 외에 `unionAll` 메서드도 제공됩니다. `unionAll`을 사용할 경우 중복 결과가 제거되지 않습니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 구문

<a name="where-clauses"></a>
### WHERE 구문

쿼리 빌더의 `where` 메서드로 "where" 조건을 추가할 수 있습니다. 기본적으로 세 개의 인자를 받으며, 첫째는 컬럼명, 둘째는 연산자, 셋째는 비교할 값입니다.

예: `votes`가 100이고 `age`가 35보다 큰 유저 조회

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

컬럼이 `=`일 때는 값만 두 번째 인자로 넘겨도 됩니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

다양한 연산자를 지원합니다:

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

아래처럼 배열로 다수의 조건을 넘길 수도 있습니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 쿼리에 참조되는 컬럼명(특히 "order by" 컬럼)에 사용자 입력값이 직접 사용되지 않도록 주의하세요.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교 시 자동 타입캐스팅을 하므로, 예기치 않은 결과가 나올 수 있습니다. 컬럼값을 쿼리에 넣기 전에 원하는 타입으로 변환하세요.

<a name="or-where-clauses"></a>
### OR WHERE 구문

`where` 메서드를 체이닝하면 `AND` 연산으로 연결됩니다. `orWhere` 메서드를 사용하면 OR 조건으로 연결할 수 있습니다. 사용법은 `where`와 동일합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

OR 조건을 괄호로 묶어 그룹화하고 싶다면, 첫 번째 인자로 클로저를 전달하세요:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```

위의 예시는 아래와 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예상치 못한 동작을 방지하려면 `orWhere`는 항상 그룹핑해서 사용하세요.

<a name="where-not-clauses"></a>
### WHERE NOT 구문

`whereNot`과 `orWhereNot` 메서드로 특정 조건 그룹을 부정할 수 있습니다. 예: 할인 중이거나 가격이 10 미만인 상품 제외

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

여러 컬럼에 동일한 조건을 적용하고 싶을 때 사용합니다.

**whereAny**: 지정된 컬럼 중 하나라도 조건에 만족하는 레코드 조회

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

위 쿼리는 다음 SQL로 변환됩니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

**whereAll**: 모든 컬럼이 조건을 만족하는 레코드 조회

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

해당 SQL:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

**whereNone**: 모든 컬럼이 조건에 부합하지 않는 레코드 조회

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

해당 SQL:

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

Laravel은 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+의 JSON 컬럼 타입 쿼리를 지원합니다. JSON 컬럼을 조회하려면 `->` 연산자를 사용합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열 쿼리는 `whereJsonContains`로 합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL에서는 배열을 인자로 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
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
### 추가 WHERE 구문

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike`는 문자열 패턴 검색(LIKE)을 위한 구문입니다. 기본적으로 대소문자를 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 true로 전달하면 대소문자를 구분합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`은 OR + LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`은 NOT LIKE 조건을, `orWhereNotLike`는 OR + NOT LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 민감 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 배열 내에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 포함되지 않아야 함을 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

서브쿼리를 두 번째 인자로 넘길 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 쿼리는 다음 SQL로 변환됩니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 매우 큰 정수 배열을 바인딩할 때에는 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용하면 메모리 사용량을 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값의 범위를 벗어나는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

같은 테이블 행의 두 컬럼 값 사이인지 확인하고 싶을 때 `whereBetweenColumns`를 사용합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

범위 밖인지 확인하려면 `whereNotBetweenColumns`를 사용하세요.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

컬럼 값이 NULL인지 확인:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

NULL이 아닌지 확인:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜/월/일/연도/시간 별 비교 쿼리:

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

특정 컬럼 값이 과거/미래/오늘/오늘 이전/오늘 이후인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
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

$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

두 컬럼 값이 같은지 비교:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자 지정도 가능:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 조건 배열도 지원:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화

종종 여러 "where" 절을 괄호로 묶어 그룹화할 필요가 있습니다. 특히 `orWhere`를 이용할 때에는 항상 그룹화를 해주는 것이 좋습니다. 클로저를 첫 번째 인자로 전달하면 됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 예상치 못한 동작을 방지하려면, `orWhere`는 항상 그룹화해서 사용하세요.

<a name="advanced-where-clauses"></a>
## 고급 WHERE 구문

<a name="where-exists-clauses"></a>
### WHERE EXISTS 구문

`whereExists` 메서드는 "where exists" SQL 절을 작성합니다. 클로저를 인자로 받아, "exists" 내부 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 쿼리 객체 자체를 넘길 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 방법 모두 아래 SQL을 생성합니다:

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

서브쿼리 결과와 값을 비교하는 WHERE 조건도 만들 수 있습니다.

예: `membership`의 최근 `type`이 특정 값인 사용자 찾기

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

다른 예: 컬럼 값이 서브쿼리 결과와 비교되는 경우

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문검색(Full Text) WHERE 구문

> [!WARNING]
> 전문검색 WHERE 구문은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드로 전체 텍스트 인덱스를 가진 컬럼의 전문 검색 WHERE 조건을 추가할 수 있습니다. 데이터베이스 종류에 따라 적절한 SQL로 변환됩니다. (MariaDB, MySQL이면 `MATCH AGAINST` 등이 사용됨)

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, LIMIT 및 OFFSET

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy`는 지정한 컬럼 순서로 결과를 정렬합니다. 첫 번째 인자는 컬럼명, 두 번째 인자는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 여러번 호출하세요:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest`로 날짜를 기준으로 손쉽게 정렬할 수 있습니다. 기본은 `created_at` 컬럼이지만, 정렬할 컬럼을 지정할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder`로 쿼리 결과를 무작위로 정렬할 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder`로 기존 정렬을 모두 제거할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

또한 `reorder`에 컬럼과 정렬 방향을 지정하면 새로 정렬됩니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having`으로 쿼리 결과를 그룹화하고 필터링할 수 있습니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween`으로 범위 내 결과만 필터링할 수도 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

두 개 이상의 컬럼으로 그룹화도 가능합니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

고급 `having` 구문 작성은 [`havingRaw`](#raw-methods)를 참고하세요.

<a name="limit-and-offset"></a>
### LIMIT 및 OFFSET

<a name="skip-take"></a>
#### `skip` 및 `take` 메서드

`skip`, `take`로 결과를 건너뛰고 제한할 수 있습니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

또는 `limit`, `offset`도 사용할 수 있습니다(기능은 동일):

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 구문

특정 조건이 참일 때만 쿼리 절을 적용하고 싶을 때는 `when` 메서드를 사용하세요:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 참일 때만 두 번째 인자로 전달된 클로저를 실행합니다. 추가로, 세 번째 인자에 다른 클로저를 넣으면 조건이 거짓일 때 실행됩니다; 예를 들어 정렬 기본값 지정:

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
## INSERT 구문

쿼리 빌더는 `insert` 메서드로 레코드를 테이블에 삽입할 수 있습니다. 컬럼과 값의 배열을 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드 삽입도 가능합니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 중 오류(예: 중복 키)를 무시합니다. 이 때 MySQL의 strict 모드도 우회됩니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드로 서브쿼리 결과를 이용해 삽입할 수도 있습니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id가 있다면, `insertGetId`로 레코드를 삽입하고 바로 id 값을 얻을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId`가 `id` 컬럼이 자동 증가 컬럼일 것으로 기대합니다. 다른 시퀀스를 사용할 경우 컬럼명을 두 번째 인자로 전달해야 합니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입, 이미 존재하는 레코드는 업데이트하는 작업을 합니다. 첫 번째 인자: 삽입/업데이트 데이터, 두 번째 인자: 레코드를 유일하게 식별하는 컬럼, 세 번째 인자: 일치할 경우 업데이트할 컬럼 목록

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

위 예시에서, 같은 출발지/목적지의 레코드가 이미 존재하면 `price`만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서 upsert의 두 번째 인자(고유 컬럼)는 반드시 Primary 또는 Unique 인덱스가 있어야 합니다. MariaDB, MySQL에서는 이 인자와 무관하게 항상 테이블의 Primary/Unique 인덱스로 판단합니다.

<a name="update-statements"></a>
## UPDATE 구문

레코드 수정에는 `update` 메서드를 사용합니다. 바꿀 컬럼/값 쌍의 배열을 인자로 받으며, 반환값은 적용된 행의 개수입니다. `where`로 범위를 제한할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### UPDATE 또는 INSERT

존재하면 업데이트, 없으면 삽입하는 기능은 `updateOrInsert` 메서드로 제공합니다. 첫 번째 인자에 조건, 두 번째 인자에 변경값을 넣으면 됩니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

클로저를 전달해 더 커스터마이즈된 프로세스도 가능합니다:

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

JSON 컬럼의 값을 업데이트하려면 `->` 문법을 사용하세요. 지원: MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

특정 컬럼 값을 증가/감소시키려면 `increment`/`decrement` 메서드를 사용하세요. 첫 번째 인자는 컬럼명, 두 번째 인자로 증감 수치를 넘길 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증감과 동시에 다른 컬럼 값도 변경하고 싶다면:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

여러 컬럼을 한 번에 증감하려면 `incrementEach`/`decrementEach`를 사용하세요:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## DELETE 구문

쿼리 빌더의 `delete` 메서드는 레코드를 삭제합니다. 반환값은 삭제된 행 수입니다. `delete` 전에 "where" 절을 붙여 범위를 지정할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더에는 SELECT 구문에 비관적 잠금을 적용하기 위한 기능이 있습니다. "공유 잠금(shared lock)"을 사용하려면 `sharedLock` 메서드를 사용하세요. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행이 수정되는 것을 방지합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 "for update" 잠금(`lockForUpdate`)을 사용하면 선택된 레코드가 수정되거나 다른 공유 잠금으로 선택되는 것을 방지할 수 있습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 [트랜잭션](/docs/{{version}}/database#database-transactions) 내에서 사용하는 것이 권장됩니다. 이렇게 하면 실패 시 자동 롤백 및 잠금 해제가 보장됩니다:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate();
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

<a name="debugging"></a>
## 디버깅

쿼리 작성 중 `dd`, `dump` 메서드로 쿼리 바인딩 및 SQL을 출력해 디버깅할 수 있습니다. `dd`는 정보 출력 후 실행을 멈추고, `dump`는 출력 후 실행을 계속합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql`은 파라미터 바인딩까지 적절히 치환된 순수 SQL을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
