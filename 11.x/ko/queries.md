# 데이터베이스: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과 청크 처리](#chunking-results)
    - [지연 스트리밍 결과](#streaming-results-lazily)
    - [집계](#aggregates)
- [Select 문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [Union](#unions)
- [기본 Where 구문](#basic-where-clauses)
    - [Where 구문](#where-clauses)
    - [Or Where 구문](#or-where-clauses)
    - [Where Not 구문](#where-not-clauses)
    - [Where Any / All / None 구문](#where-any-all-none-clauses)
    - [JSON Where 구문](#json-where-clauses)
    - [추가 Where 구문](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 구문](#advanced-where-clauses)
    - [Where Exists 구문](#where-exists-clauses)
    - [서브쿼리 Where 구문](#subquery-where-clauses)
    - [전문 검색(Full Text) Where 구문](#full-text-where-clauses)
- [정렬, 그룹화, Limit, Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 구문](#conditional-clauses)
- [Insert 문](#insert-statements)
    - [Upsert](#upserts)
- [Update 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성 및 실행하는 데 편리하고 유연한(플루언트) 인터페이스를 제공합니다. 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

Laravel 쿼리 빌더는 SQL 인젝션 공격으로부터 애플리케이션을 보호하기 위해 PDO 파라미터 바인딩을 사용합니다. 쿼리 빌더에 전달된 문자열을 바인딩 시 추가적인 정제나 세척은 필요하지 않습니다.

> [!WARNING]  
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명(예: "order by" 컬럼 포함)을 사용자 입력에 따라 동적으로 지정하지 않도록 해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` 파사드의 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대해 플루언트 쿼리 빌더 인스턴스를 반환하며, 여기에 다양한 제약 조건을 체이닝하고 마지막에 `get` 메서드를 사용해서 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 전체 사용자 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 객체를 반환하며, 각각의 결과는 PHP의 `stdClass` 객체 인스턴스입니다. 각 컬럼의 값은 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑, 축소 등 매우 강력한 메서드를 다양하게 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회

데이터베이스에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키길 원한다면 `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException`이 처리되지 않으면 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 하나의 컬럼 값만 추출하려면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 컬럼의 값을 바로 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 리스트 조회

특정 컬럼의 값 목록을 `Illuminate\Support\Collection` 인스턴스로 받고 싶을 때는 `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 사용자들의 제목 값을 컬렉션으로 조회하려면:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 컬렉션의 키로 사용할 컬럼을 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

수천 개의 데이터베이스 레코드를 다뤄야 하는 경우 `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 한 번에 소량의 결과(청크)를 가져와, 각 청크를 클로저에 전달하여 처리할 수 있습니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 청크로 조회하려면:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하여 추가 청크 처리를 중단할 수도 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중 레코드를 업데이트하는 경우, 청크 결과가 예기치 않게 변경될 수 있습니다. 레코드 조회와 동시에 업데이트할 계획이라면 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 레코드의 기본 키(Primary Key) 기준으로 자동으로 결과를 페이지네이션합니다:

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

`chunkById`, `lazyById` 메서드는 쿼리에 자체적인 "where" 조건을 추가하므로, [논리 그룹화](#logical-grouping)와 마찬가지로 사용자 조건을 클로저 내에서 그룹화하는 것이 좋습니다:

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
> 청크 콜백 내에서 레코드를 업데이트 또는 삭제하는 경우, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 결과

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행합니다. 하지만 각 청크를 콜백에 넘기는 대신, `lazy()` 메서드는 결과를 단일 스트림처럼 다룰 수 있는 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로 조회된 레코드를 반복하며 동시에 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드들은 레코드의 기본 키 기준으로 자동 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 레코드를 반복하며 업데이트 또는 삭제하는 경우, 기본 키 또는 외래 키가 변경되면 쿼리 결과에 영향을 줄 수 있습니다. 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계값을 조회하는 메서드를 제공합니다. 쿼리를 작성한 후 언제든지 해당 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

또한, 원하는 집계를 구체화하기 위해 조건문과 결합할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리 조건에 맞는 레코드의 존재 여부만 확인하려면 `count` 대신 `exists`, `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 문

<a name="specifying-a-select-clause"></a>
#### Select 구문 지정

항상 테이블의 모든 컬럼을 선택할 필요는 없습니다. `select` 메서드를 사용하여 쿼리의 select 구문을 커스터마이징할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 쿼리 결과에서 중복을 제거합니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 빌더 인스턴스를 가지고 있고, select 구문에 컬럼을 추가하고 싶을 때 `addSelect` 메서드를 사용할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때로는 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 그럴 땐 `DB` 파사드의 `raw` 메서드를 사용하여 raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 삽입되므로 SQL 인젝션 취약점이 생기지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있는 다음 메서드들을 사용할 수 있습니다. **Raw 표현식을 사용할 경우 Laravel은 SQL 인젝션으로부터 완전한 보호를 보장할 수 없음을 기억하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(...))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 선택적으로 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리에 raw "where" 구문을 주입할 수 있습니다. 마찬가지로, 선택적으로 바인딩 배열을 두 번째 인수로 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw` 메서드는 "having" 구문의 값을 raw 문자열로 지정할 수 있게 해줍니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 구문의 값을 raw 문자열로 지정할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 구문의 값을 raw 문자열로 지정할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### Inner Join 구문

쿼리 빌더를 사용하면 쿼리에 조인 구문을 추가할 수 있습니다. 기본 "inner join"을 하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용합니다. 첫 번째 인수는 조인할 테이블명, 나머지 인수는 조인 조건입니다. 단일 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 하고 싶다면 `leftJoin`, `rightJoin` 메서드를 사용하세요. 시그니처는 `join`과 동일합니다:

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

"cross join"을 하려면 `crossJoin` 메서드를 사용할 수 있습니다. Cross join은 첫 번째 테이블과 조인 테이블 사이의 데카르트 곱을 만듭니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 구문

더 복잡한 조인 구문도 지정할 수 있습니다. `join` 메서드의 두 번째 인수로 클로저를 넘겨주면, 해당 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 전달받아, 조인 조건을 세밀하게 지정할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 구문을 사용하려면 `JoinClause` 인스턴스에서 제공하는 `where`, `orWhere` 메서드를 사용할 수 있습니다. 이 메서드들은 컬럼끼리 비교하는 대신 값을 비교합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 통해 서브쿼리를 조인할 수 있습니다. 각각의 메서드는 세 개의 인수를 받으며, 서브쿼리, 테이블 별칭, 관련 컬럼을 정의하는 클로저입니다. 아래 예제에서는 각 사용자 레코드에 최근 작성한 블로그 게시글의 `created_at` 타임스탬프를 포함하는 컬렉션을 조회합니다:

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

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하여 서브쿼리와 "lateral join"을 수행할 수 있습니다. 각 메서드는 서브쿼리와 테이블 별칭을 인수로 받고, 조인 조건은 제공된 서브쿼리의 `where` 구문 내부에서 지정해야 합니다. Lateral join은 각 행마다 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

아래는 각 사용자의 최근 블로그 게시물 3개를 가져오는 예시입니다. 각 사용자는 최대 3개의 게시글 행으로 결과가 나올 수 있습니다. 조인 조건은 서브쿼리 내에서 `whereColumn`로 지정합니다:

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
## Union

쿼리 빌더는 여러 쿼리를 "union"으로 결합하는 편리한 메서드도 제공합니다. 예를 들어, 초기 쿼리를 생성한 후 `union` 메서드로 추가 쿼리와 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도 `unionAll` 메서드가 제공되며, 중복 결과가 제거되지 않습니다. 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 구문

<a name="where-clauses"></a>
### Where 구문

쿼리 빌더의 `where` 메서드로 쿼리에 "where" 조건을 추가할 수 있습니다. 가장 기본적인 사용법은 세 개의 인수를 받습니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스가 지원하는 연산자), 세 번째는 비교할 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼 값이 100이고 `age` 값이 35보다 큰 사용자를 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

좀 더 간단하게, `=` 비교는 두 번째 인수 없이도 가능합니다. Laravel은 자동으로 `=` 연산자로 간주합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

데이터베이스에서 지원하는 연산자는 모두 사용할 수 있습니다:

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

여러 조건을 한번에 배열로 넘길 수도 있습니다. 배열의 각 요소는 보통의 `where` 메서드에 전달하는 세 개의 인자를 가지는 배열입니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]  
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 사용자 입력이 쿼리의 컬럼명, 특히 "order by" 컬럼에 직접적으로 반영되지 않게 해야 합니다.

> [!WARNING]
> MySQL 및 MariaDB는 문자열-숫자 비교에서 문자열을 자동으로 정수로 변환합니다. 이 과정에서 비숫자 문자열은 `0`으로 변환되어 예상과 다른 결과가 나올 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 행에서 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이를 방지하려면 쿼리에 값을 사용할 때 항상 올바른 타입으로 캐스팅하세요.

<a name="or-where-clauses"></a>
### Or Where 구문

`where` 메서드를 체이닝하면 기본적으로 `and` 연산자로 연결됩니다. `or` 연산자로 연결하려면 `orWhere` 메서드를 사용하세요. 인수는 `where`와 동일합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 그룹핑된 "or" 조건이 필요할 땐, 첫 번째 인수로 클로저를 넘길 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```

위 예제는 아래와 같은 SQL을 만듭니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]  
> `orWhere`는 항상 그룹화하여 예기치 않은 동작(특히 글로벌 스코프 적용 구문에서)을 방지해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 구문

`whereNot` 및 `orWhereNot` 메서드는 특정 쿼리 제약 조건 그룹을 부정할 때 사용합니다. 예를 들어, 다음 쿼리는 클리어런스 상품 또는 가격이 10 미만인 상품을 제외합니다:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### Where Any / All / None 구문

동일한 쿼리 제약 조건을 여러 컬럼에 적용해야 할 때가 있습니다. 예를 들어, 지정된 컬럼리스트 중 어떤 컬럼이라도 특정 값과 `LIKE`되는 레코드를 조회하고 싶다면 `whereAny` 메서드를 사용할 수 있습니다:

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

비슷하게, `whereAll` 메서드는 주어진 모든 컬럼이 조건을 만족하는 경우를 조회합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음 SQL을 만듭니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 컬럼들 중 어느 것도 조건을 만족하지 않는 레코드를 조회합니다:

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

위 쿼리는 다음 SQL을 만듭니다:

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
### JSON Where 구문

Laravel은 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+ 등 JSON 컬럼을 지원하는 데이터베이스에서 JSON 컬럼 검색도 지원합니다. JSON 컬럼을 쿼리할 때는 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

`whereJsonContains`로 JSON 배열을 검색할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL에서는 값 배열로도 쿼리할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

JSON 배열의 길이로 쿼리하려면 `whereJsonLength`를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가 Where 구문

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드는 패턴 매칭(LIKE) 검색 쿼리를 추가하는 방법을 제공합니다. 이 메서드들은 데이터베이스에 상관없이 대소문자 구분 등 세부 옵션을 조절하며, 기본적으로 대소문자 구분 없이 검색합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수로 대소문자 구분도 가능합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`로 LIKE 조건과 함께 "or" 구문을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`로 "NOT LIKE" 조건을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`도 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> SQL Server에서는 `whereLike`의 대소문자 구분 검색 옵션을 지원하지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 주어진 배열에 포함될 때만 레코드를 조회합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼 값이 주어진 배열에 포함되지 않을 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체를 넘길 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 코드는 다음 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대규모 정수 배열을 바인딩하려면, 메모리 사용을 줄이기 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용할 것을 권장합니다.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 있을 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 밖에 있을 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 컬럼 값이 같은 행의 두 컬럼 값 사이에 있을 때만 조회합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 컬럼 값이 두 컬럼 값 밖에 있을 때만 조회합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 해당 컬럼 값이 `NULL`일 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 해당 컬럼 값이 `NULL`이 아닐 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값을 특정 날짜와 비교합니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 특정 월과 비교합니다:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 특정 일과 비교합니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 특정 연도와 비교합니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 특정 시간과 비교합니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`, `whereFuture` 메서드는 컬럼 값이 과거 또는 미래인지 여부를 판단합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture`는 현재 날짜와 시간을 포함하여 과거 또는 미래인 경우를 판단합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 컬럼 값이 오늘, 오늘 이전, 오늘 이후인 경우를 판단합니다:

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

마찬가지로, `whereTodayOrBefore`, `whereTodayOrAfter`는 오늘까지 또는 오늘 이후인 경우를 판단합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼 값이 같을 때만 조회합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자도 쓸 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

`whereColumn`에 컬럼 비교 배열도 전달할 수 있습니다. 이 조건들은 `and`로 연결됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

쿼리의 논리적 그룹화를 위해 여러 "where" 구문을 괄호로 묶어야 하는 경우가 있습니다. 특히 `orWhere`는 항상 괄호로 그룹화하여 예기치 않은 동작을 방지해야 합니다. 이를 위해 `where`에 클로저를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위와 같이 클로저를 전달하면 쿼리 빌더는 괄호로 감싸진 제약 조건 그룹으로 인식합니다. 위 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> `orWhere`는 항상 그룹화하여 예기치 않은 쿼리 동작을 방지해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 구문

<a name="where-exists-clauses"></a>
### Where Exists 구문

`whereExists` 메서드를 사용하면 "where exists" SQL 구문을 작성할 수 있습니다. 이 메서드는 클로저를 인수로 받아 그 안에서 "exists" 절에 들어갈 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체도 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시는 아래와 같은 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 구문

때로는 서브쿼리 결과와 값을 비교하여 "where" 조건을 작성해야 할 때가 있습니다. 이 경우 `where`에 클로저와 값을 전달하면 됩니다. 예를 들어, 최근 "membership"이 특정 타입인 사용자를 모두 조회하려면:

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

혹은 서브쿼리 결과를 컬럼과 비교해야 할 때는, 컬럼, 연산자, 클로저를 `where`에 넘깁니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색(Full Text) Where 구문

> [!WARNING]
> 전문 검색 Where 구문은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드는 [전문 검색 인덱스](/docs/{{version}}/migrations#available-index-types)가 생성된 컬럼에 대해 전문 검색 "where" 구문을 추가합니다. Laravel은 이 구문을 알맞은 SQL로 변환합니다. 예를 들어, MariaDB나 MySQL에서는 `MATCH AGAINST` 구문이 생성됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit, Offset

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 지정한 컬럼으로 정렬할 수 있습니다. 첫 번째 인수는 정렬할 컬럼, 두 번째는 정렬 방향(`asc` 혹은 `desc`)입니다:

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

`latest`, `oldest` 메서드를 사용하면 시간 기준으로 쉽게 정렬할 수 있습니다. 기본적으로 `created_at`컬럼 기준이며, 다른 컬럼을 지정할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드는 결과를 무작위로 정렬합니다. 예를 들어 임의의 사용자를 가져올 때 사용됩니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 쿼리에 적용된 모든 "order by" 구문을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder`에 컬럼과 방향을 넘기면 기존 정렬을 모두 제거하고 새 정렬만 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy`, `having` 메서드

`groupBy`, `having` 메서드로 결과를 그룹화할 수 있습니다. `having`은 `where`와 비슷한 형태로 사용합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드로 결과를 특정 범위로 필터링할 수 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼으로 그룹핑하려면 `groupBy`에 여러 인수를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 고급 `having` 작성법은 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

<a name="skip-take"></a>
#### `skip`, `take` 메서드

`skip`, `take` 메서드를 사용하면 결과 건수를 제한하거나, 결과의 일부를 건너뛸 수 있습니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

또는 `limit`, `offset` 메서드를 사용할 수도 있습니다. 기능은 `take`, `skip`과 동일합니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 구문

특정 조건일 때만 쿼리 구문을 추가하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에 입력값이 있을 때만 `where` 구문을 적용하고 싶다면 `when` 메서드를 사용할 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 클로저를 실행합니다. 위 예시에서 `role`이 있을 때만 클로저가 실행됩니다.

세 번째 인수로 클로저를 추가로 전달하면, 첫 번째 인수가 `false`일 때 그 클로저가 실행됩니다. 이를 활용해 기본 정렬을 지정할 수도 있습니다:

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
## Insert 문

쿼리 빌더의 `insert` 메서드는 레코드를 데이터베이스 테이블에 삽입할 때 사용합니다. `insert`는 컬럼명-값 배열을 인수로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

한 번에 여러 레코드를 추가하려면 배열 배열을 전달하면 됩니다. 각 배열은 하나의 레코드입니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드를 삽입할 때 오류가 나도 무시합니다. 이 메서드를 사용할 때는 중복 레코드 오류 뿐 아니라, 데이터베이스 엔진에 따라 다른 오류들도 무시될 수 있음을 인지하세요. 예를 들어, `insertOrIgnore`는 [MySQL 스트릭트 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리로 삽입할 데이터를 결정하여 레코드를 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 컬럼이 있다면, 레코드를 삽입하고 ID를 반환받으려면 `insertGetId`를 사용하세요:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 auto increment 컬럼명이 `id`여야 `insertGetId`가 정상 동작합니다. 다른 시퀀스에서 ID를 반환받으려면 두 번째 인수로 컬럼명을 지정하세요.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입, 이미 기록된 레코드는 새로운 값으로 갱신합니다. 첫 번째 인수는 삽입/업데이트할 값이고, 두 번째는 레코드를 고유하게 식별하는 컬럼 리스트, 세 번째는 일치하는 레코드가 있을 경우 업데이트할 컬럼 리스트입니다:

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

위 예시에서, `departure`와 `destination` 컬럼 값이 같은 레코드가 있으면 해당 레코드의 `price` 컬럼이 갱신됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert`의 두 번째 인수(고유 키)는 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. MariaDB/MySQL 드라이버들은 두 번째 인수를 무시하고 기본적으로 "primary"/"unique" 인덱스를 사용합니다.

<a name="update-statements"></a>
## Update 문

쿼리 빌더는 레코드 삽입뿐만 아니라, `update` 메서드로 기존 레코드도 변경할 수 있습니다. `update`는 업데이트할 컬럼-값 배열을 인수로 받으며, 영향을 받은 행 개수를 반환합니다. 조건을 `where`로 제약할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

일치하는 레코드가 있으면 업데이트, 없으면 새로 삽입하는 경우 `updateOrInsert`를 사용합니다. 이 메서드는 두 개의 배열 인수를 받으며, 첫 번째는 검색 조건, 두 번째는 업데이트할 값입니다.

`updateOrInsert`는 첫 번째 배열로 레코드를 찾고, 있으면 두 번째 배열로 업데이트, 없으면 두 배열을 머지해 새 레코드로 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

일치 레코드 존재 여부에 따라 업데이트/삽입 속성을 클로저로 커스터마이즈할 수도 있습니다:

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

JSON 컬럼을 업데이트할 때는 `->` 문법을 사용하여 JSON 오브젝트의 특정 키를 업데이트합니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원합니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 지정한 컬럼값을 증가/감소시키는 편리한 메서드들도 제공합니다. 두 메서드 모두 첫 번째 인수로 수정할 컬럼명을 받고, 두 번째 인수로 증가/감소 할 값을 지정할 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증가/감소와 함께 다른 컬럼도 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

`incrementEach`, `decrementEach`로 여러 컬럼을 한 번에 값만큼 증가/감소시킬 수 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 문

쿼리 빌더의 `delete` 메서드로 테이블에서 레코드를 삭제할 수 있습니다. 삭제된 행의 수가 반환됩니다. "where" 구문으로 삭제 조건을 제약할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금

쿼리 빌더는 select 문을 실행할 때 "비관적 잠금"을 지원하는 여러 기능도 제공합니다. "공유 잠금(shared lock)"을 실행하려면 `sharedLock`을 호출하세요. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행이 변경되지 않도록 보장합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

`lockForUpdate`는 "for update" 잠금으로, 선택된 행이 변경되거나 다른 공유 잠금 select에 선택되지 않도록 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비록 필수는 아니지만, 비관적 잠금은 [트랜잭션](/docs/{{version}}/database#database-transactions) 내에서 사용하는 것이 권장됩니다. 이렇게 하면 전체 작업이 완료될 때까지 조회 데이터가 변경되지 않습니다. 실패 시 트랜잭션이 롤백되고, 잠금도 자동 해제됩니다:

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

<a name="debugging"></a>
## 디버깅

쿼리 빌더를 작성하면서 `dd` 및 `dump` 메서드를 사용하여 현재 쿼리 바인딩 및 SQL을 출력할 수 있습니다. `dd`는 디버그 정보를 출력하고 즉시 요청을 중지하며, `dump`는 디버그 정보를 출력하되 요청을 계속 실행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql` 메서드는 쿼리의 모든 파라미터가 치환된 SQL을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
