# 데이터베이스: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 청킹(Chunking)](#chunking-results)
    - [지연 스트리밍 결과](#streaming-results-lazily)
    - [집계](#aggregates)
- [SELECT 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
- [정렬, 그룹화, LIMIT, OFFSET](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [LIMIT & OFFSET](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 구문](#insert-statements)
    - [UPSERT 구문](#upserts)
- [UPDATE 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 & 감소](#increment-and-decrement)
- [DELETE 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행할 수 있는 편리하고 유연한 인터페이스를 제공합니다. 애플리케이션 내에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 작동합니다.

Laravel의 쿼리 빌더는 SQL 인젝션 공격으로부터 애플리케이션을 보호하기 위해 PDO 파라미터 바인딩을 사용합니다. 쿼리 빌더에 전달되는 문자열을 따로 정제하거나 이스케이프할 필요가 없습니다.

> {note} PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서, 사용자 입력을 쿼리의 컬럼명(특히 "order by" 컬럼 포함)으로 삼아서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드에서 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 해당 테이블에 대한 플루언트(유창한) 쿼리 빌더 인스턴스를 반환하며, 쿼리에 더 많은 제약 조건을 체이닝(chain)한 후 최종적으로 `get` 메서드를 사용하여 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 보여줍니다.
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

`get` 메서드는 각 결과가 PHP의 `stdClass` 객체인 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 컬럼의 값은 객체의 프로퍼티 방식으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> {tip} Laravel 컬렉션은 데이터 매핑과 집계를 위한 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대한 더 자세한 정보는 [컬렉션 문서](/docs/{{version}}/collections)를 참조하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회하기

테이블에서 단일 행만 조회하려는 경우, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

행 전체가 필요하지 않고, 한 컬럼의 값만 필요하다면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 해당 컬럼의 값을 바로 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 이용해 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값만 포함하는 `Illuminate\Support\Collection` 인스턴스를 조회하려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예제에서는 사용자 직책(타이틀) 컬렉션을 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인자를 전달하여, 결과 컬렉션이 사용할 키 컬럼을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청킹(Chunking)

수천 건 이상의 데이터베이스 레코드를 다뤄야 한다면, `DB` 파사드의 `chunk` 메서드 사용을 고려하세요. 이 메서드는 한 번에 작은 청크(chunk)만큼의 결과를 조회한 후, 각 청크를 클로저에 전달하여 처리합니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 나누어 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    foreach ($users as $user) {
        //
    }
});
```

클로저에서 `false`를 반환하면 이후 청크의 처리를 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중 레코드를 업데이트 하는 경우, 예상치 못한 방식으로 청크 결과가 변경될 수 있습니다. 청크 처리 중 조회된 레코드를 업데이트하려면 `chunkById` 메서드를 사용하는 것이 더 안전합니다. 이 메서드는 기본키 기준으로 결과를 자동 분할하여 처리합니다:

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

> {note} 청크 콜백 내에서 레코드를 업데이트하거나 삭제할 때는, 기본키 또는 외래키 변경이 청크 쿼리에 영향을 줄 수 있음을 유의하세요. 이는 일부 레코드가 청크 결과에서 제외될 수 있음을 의미합니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 결과

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 분할하여 실행합니다. 하지만 각 청크를 콜백으로 전달하는 대신, [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)를 반환합니다. 이를 통해 전체 결과를 하나의 스트림처럼 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

마찬가지로, 반복 중 조회된 레코드를 업데이트하려는 경우에는 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 더 안전합니다. 이 메서드들도 기본키를 기준으로 자동 분할 처리합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> {note} 레코드 반복 처리 중 업데이트/삭제 시에도, 기본키나 외래키의 변경은 쿼리 결과에 영향을 줄 수 있습니다.

<a name="aggregates"></a>
### 집계

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등의 집계 값을 쉽게 조회할 수 있는 다양한 메서드를 제공합니다. 아래 예제처럼 쿼리를 구성한 후 이 메서드를 호출하면 됩니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 메서드는 다른 절과 조합하여 집계 값을 정교하게 산출할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리 제약조건에 부합하는 레코드가 존재하는지 확인하려면 `count` 대신 `exists`, `doesntExist` 메서드를 사용할 수 있습니다:

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

항상 테이블의 모든 컬럼을 조회하고 싶지 않을 수 있습니다. `select` 메서드를 사용하면 쿼리의 SELECT 절을 커스텀 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복 없는 결과만 반환합니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 SELECT 절에 컬럼을 추가하려면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때때로 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. `DB` 파사드의 `raw` 메서드를 사용하면 raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> {note} Raw 구문은 쿼리에 문자열 그대로 삽입되므로, SQL 인젝션 취약성이 발생하지 않도록 각별히 주의하세요.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신, 쿼리의 특정 부분에 raw 표현식을 삽입하기 위한 다음과 같은 메서드들을 사용할 수 있습니다. **Laravel은 raw 표현식을 사용하는 쿼리가 SQL 인젝션 취약점으로부터 보호됨을 보장하지 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(...))`의 대체로 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 삽입할 수 있게 해줍니다. 이들 메서드 역시 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절의 값으로 raw 문자열을 사용할 수 있습니다. 이 메서드들 역시 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절의 값으로 raw 문자열을 사용할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절의 값으로 raw 문자열을 사용할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더 인스턴스의 `join` 메서드를 사용하면 기본적인 "inner join" 구문을 추가할 수 있습니다. 첫 번째 인자는 조인할 테이블 이름이며, 나머지 인자는 조인 절의 컬럼 제약을 지정합니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이들 메서드의 인수는 `join`과 동일합니다:

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

"cross join"을 수행하려면 `crossJoin` 메서드를 사용합니다. cross join은 두 테이블의 데카르트 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 조건도 지정할 수 있습니다. 시작하려면 `join`의 두 번째 인수에 클로저를 전달하세요. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아, "join" 절의 제약을 지정할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function ($join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(...);
    })
    ->get();
```

조인에서 "where" 절을 사용하고 싶으면 `JoinClause` 인스턴스에서 제공하는 `where`, `orWhere` 메서드를 사용하세요. 컬럼 간 비교가 아닌 값에 대한 비교를 수행합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하여 서브쿼리와 조인할 수 있습니다. 이 메서드들은 각각 서브쿼리, 테이블 별칭, 관련 컬럼을 정의하는 클로저를 인수로 받습니다. 아래 예시에서는 각 사용자 레코드에 사용자의 가장 최근 게시글의 `created_at` 타임스탬프도 함께 조회합니다:

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
## 유니온(UNION)

쿼리 빌더는 여러 쿼리를 "union"으로 합치는 편리한 방법도 제공합니다. 예를 들어, 초기 쿼리 작성 후 `union` 메서드로 추가 쿼리를 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에 중복된 결과까지 모두 합쳐주는 `unionAll`도 제공합니다. `unionAll`의 메서드 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용하여 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 사용방식은 세 개의 인수를 필요로 합니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 연산자라면 모두 가능), 세 번째는 비교 대상 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼 값이 100이고 `age` 컬럼 값이 35 초과인 사용자를 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

간편하게 `=` 비교를 할 때는 두 번째 인자만 값으로 주면 Laravel이 자동으로 `=` 연산자로 처리합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

다음과 같이 데이터베이스가 지원하는 연산자는 모두 사용할 수 있습니다:

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

여러 조건을 한 번에 배열로 전달할 수도 있습니다. 각 요소는 보통 `where`에서 사용하는 세 개의 인수 배열입니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> {note} PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리의 컬럼명("order by" 포함)을 결정하게 해서는 안 됩니다.

<a name="or-where-clauses"></a>
### OR WHERE 절

`where` 메서드를 체이닝 하면, 조건들이 `and`로 결합됩니다. 하지만 `or` 조건을 사용하려면, `orWhere` 메서드를 사용하세요. 인수는 `where`와 동일합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 그룹화된 "or" 조건이 필요하다면, `orWhere`의 첫 번째 인자로 클로저를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function($query) {
        $query->where('name', 'Abigail')
              ->where('votes', '>', 50);
    })
    ->get();
```

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> {note} 예상치 못한 동작을 방지하려면 `orWhere` 호출 시 항상 괄호로 그룹화하세요(글로벌 스코프 적용 시도 포함).

<a name="json-where-clauses"></a>
### JSON WHERE 절

Laravel은 MySQL 5.7+, PostgreSQL, SQL Server 2016, SQLite 3.9.0 ([JSON1 확장](https://www.sqlite.org/json1.html) 필요) 같은 JSON 컬럼 타입을 지원하는 데이터베이스의 JSON형 컬럼 쿼리도 지원합니다. `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 조회하려면 `whereJsonContains`를 사용할 수 있습니다. 이 기능은 SQLite에서는 지원되지 않습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MySQL이나 PostgreSQL을 사용할 경우, 값 배열을 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

JSON 배열의 길이에 따라 쿼리하려면 `whereJsonLength`를 사용하세요:

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

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
   ->whereBetween('votes', [1, 100])
   ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 두 값 밖에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 특정 컬럼 값이 주어진 배열에 포함되어 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼 값이 배열에 포함되어 있지 않은지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

> {note} 많은 수의 정수 바인딩 배열을 쿼리에 추가한다면 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아님을 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값을 날짜와 비교합니다:

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

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 같은지 비교합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 추가로 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 비교를 배열로 전달 가능하며, 조건은 모두 `and`로 결합됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화

여러 WHERE 절을 괄호로 그룹화해야 할 경우가 있습니다. 특히 `orWhere`를 사용할 때 예기치 않은 쿼리 동작을 방지하려면 항상 괄호로 묶는 것이 좋습니다. 이를 위해서는 `where` 메서드에 클로저를 전달하세요:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function ($query) {
        $query->where('votes', '>', 100)
              ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

클로저를 전달하면 쿼리 빌더는 제약조건 그룹을 시작합니다. 위 예시의 SQL은 다음과 같이 생성됩니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> {note} `orWhere`는 항상 그룹화하여 예기치 않은 동작을 피하세요(글로벌 스코프 적용 포함).

<a name="advanced-where-clauses"></a>
### 고급 WHERE 절

<a name="where-exists-clauses"></a>
### WHERE EXISTS 절

`whereExists` 메서드는 "where exists" SQL 절을 작동시킬 수 있게 해줍니다. 이 메서드는 쿼리 빌더 인스턴스를 받는 클로저를 인수로 받으며, 해당 쿼리가 EXISTS 절 내부에 들어갑니다:

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

서브쿼리 결과와 비교하는 WHERE 절이 필요한 경우, 클로저와 값을 `where`에 전달하면 됩니다. 예를 들어, 아래 쿼리는 특정 타입의 최근 "membership"이 있는 모든 사용자를 조회합니다:

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

또는, 컬럼을 서브쿼리와 비교하려면, 컬럼명·연산자·클로저 순으로 전달하세요. 아래 쿼리는 금액이 평균보다 작은 모든 소득 내역을 조회합니다:

```php
use App\Models\Income;

$incomes = Income::where('amount', '<', function ($query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, LIMIT, OFFSET

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 결과를 특정 컬럼으로 정렬합니다. 첫 번째 인수는 정렬할 컬럼, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼 정렬 시에는 `orderBy`를 여러 번 호출하세요:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` & `oldest` 메서드

`latest`, `oldest`는 날짜 기준으로 결과를 정렬합니다. 기본적으로 `created_at` 컬럼으로 정렬되며, 정렬할 컬럼명을 직접 줄 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드는 쿼리 결과를 무작위로 정렬합니다. 예를 들어, 무작위 사용자 한 명을 이렇게 조회할 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 해제

`reorder` 메서드는 기존의 모든 "order by" 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

또는, 새로운 정렬 조건을 적용하려면 컬럼명과 방향을 전달하세요:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` & `having` 메서드

`groupBy`와 `having` 메서드는 쿼리 결과 그룹화에 사용됩니다. `having`의 시그니처는 `where`와 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

특정 범위 내의 결과만 필터링하려면 `havingBetween` 메서드를 쓸 수 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼 그룹화 시에는 인자를 여러 개 전달하세요:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

보다 고급 Having 절이 필요하면 [`havingRaw`](#raw-methods)를 참고하세요.

<a name="limit-and-offset"></a>
### LIMIT & OFFSET

<a name="skip-take"></a>
#### `skip` & `take` 메서드

조회 결과 개수 제한, 결과 건너뛰기에는 `skip`, `take` 메서드를 사용하세요:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

또는, `limit`, `offset` 메서드를 사용할 수도 있습니다. 이는 각각 `take`, `skip`과 동등합니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

특정 조건에 따라 쿼리절을 적용하고 싶을 수 있습니다. 예를 들어, HTTP 요청에 특정 입력 값이 있을 때만 `where` 절을 적용하려면 `when` 메서드를 사용할 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function ($query, $role) {
        return $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 클로저를 실행합니다. `false`라면 실행하지 않습니다. 즉, 위 예시는 요청에 `role` 필드가 있고 `true`로 평가될 때 클로저가 적용됩니다.

세 번째 인자로 추가 클로저를 전달할 수도 있는데, 이는 첫 번째 인자가 `false`일 때만 실행됩니다. 아래 예시는 이를 활용해 기본 정렬을 지정합니다:

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
## INSERT 구문

쿼리 빌더는 테이블에 레코드를 추가하는 `insert` 메서드를 제공합니다. `insert`는 컬럼명과 값의 배열을 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드 삽입 시에는 배열의 배열을 전달하면 됩니다. 각 배열은 한 레코드를 나타냅니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드 삽입 중 오류를 무시합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

> {note} `insertOrIgnore`는 중복된 레코드를 무시하고, 데이터베이스 엔진에 따라 기타 오류도 무시할 수 있습니다. 예: `insertOrIgnore`는 [MySQL의 strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 무시합니다.

<a name="auto-incrementing-ids"></a>
#### 자동 증가(autoincrement) ID

테이블에 자동 증가 id가 있다면, `insertGetId` 메서드로 레코드를 추가하면서 새 id도 바로 받을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> {note} PostgreSQL에서는 자동 증가 컬럼 이름이 반드시 `id`로 설정되어야 합니다. 다른 시퀀스를 사용하려면 두 번째 인수로 컬럼명을 전달하십시오.

<a name="upserts"></a>
### UPSERT 구문

`upsert` 메서드는 존재하지 않는 레코드는 삽입(insert)하고, 이미 존재하는 레코드는 지정한 값으로 갱신(update)합니다. 첫 번째 인수는 삽입/업데이트할 값, 두 번째 인수는 테이블에서 레코드를 고유하게 식별하는 컬럼(들), 세 번째 인수는 중복 레코드가 있을 때 업데이트할 컬럼들입니다:

```php
DB::table('flights')->upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```

위 예제에서, 동일한 `departure`와 `destination` 조합이 이미 존재하면 `price` 컬럼만 업데이트합니다.

> {note} SQL Server를 제외한 모든 데이터베이스에서는 upsert 두 번째 인수(고유식별 컬럼)에 "primary" 또는 "unique" 인덱스가 필요합니다. 또한 MySQL 드라이버에서는 두 번째 인수를 무시하고 항상 테이블의 "primary", "unique" 인덱스를 사용합니다.

<a name="update-statements"></a>
## UPDATE 구문

레코드 추가 뿐 아니라 기존 레코드를 갱신하려면 `update` 메서드를 사용하세요. `insert`와 마찬가지로, 컬럼과 값 쌍의 배열을 전달합니다. 반환값은 영향을 받은 행의 수입니다. `where` 절로 업데이트 대상을 제한할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### UPDATE 또는 INSERT

일치하는 레코드는 갱신, 없으면 추가하고 싶을 때는 `updateOrInsert` 메서드를 사용합니다. 첫 번째 인자는 찾을 조건, 두 번째는 업데이트할 컬럼과 값 배열입니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼을 업데이트할 때는 `->` 문법을 사용해 JSON 객체의 특정 키를 갱신할 수 있습니다. 이 기능은 MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 컬럼 값 증가 & 감소

주어진 컬럼 값을 손쉽게 증가(Increase) 또는 감소(Decrease)시키는 메서드도 있습니다. 두 번째 인수로 증가/감소시킬 값(기본: 1)을 지정할 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

동시에 다른 컬럼도 함께 업데이트하려면 세 번째 인수로 컬럼/값 쌍 배열 전달:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

<a name="delete-statements"></a>
## DELETE 구문

쿼리 빌더의 `delete` 메서드로 테이블에서 레코드를 삭제할 수 있습니다. 반환값은 삭제된 행 수입니다. "where" 절을 추가해 일부만 삭제할 수도 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

테이블의 모든 레코드를 삭제하고 자동 증가 id를 0으로 초기화하고 싶으면 `truncate` 메서드를 사용하세요:

```php
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
#### 테이블 Truncate & PostgreSQL

PostgreSQL 데이터베이스에서 truncate 작업을 하면 `CASCADE` 동작이 적용되어, 연관된 외래키 테이블의 레코드까지 전부 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금

쿼리 빌더에는 "비관적 잠금(pessimistic locking)"을 위한 몇 가지 기능이 포함되어 있습니다. "shared lock" 선택 시 `sharedLock` 메서드를 사용하면 됩니다. 선택된 행은 트랜잭션이 커밋될 때까지 수정이 금지됩니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate`를 사용하면 "for update" 잠금을 사용할 수 있습니다. 이는 선택된 레코드를 수정하거나, 다른 공유 잠금으로 조회할 수 없게 만듭니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

<a name="debugging"></a>
## 디버깅

쿼리 작성 시 `dd` 및 `dump` 메서드를 사용하면 현재 쿼리 바인딩과 SQL을 덤프해줍니다. `dd`는 출력 후 실행을 중단하며, `dump`는 실행을 계속합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```
