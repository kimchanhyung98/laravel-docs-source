# 데이터베이스: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 청크 단위로 가져오기](#chunking-results)
    - [게으르게 결과 스트리밍하기](#streaming-results-lazily)
    - [집계](#aggregates)
- [SELECT 문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [Or WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [서브쿼리 WHERE 절](#subquery-where-clauses)
    - [전문 검색 WHERE 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit & Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [UPDATE 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 & 감소](#increment-and-decrement)
- [DELETE 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 손쉽게 작성하고 실행할 수 있는 간결하고 직관적인 인터페이스를 제공합니다. 이 빌더를 이용해 애플리케이션의 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 쿼리 빌더의 바인딩에 전달되는 문자열을 별도로 정제하거나 필터링할 필요가 없습니다.

> **경고**  
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자가 입력한 데이터가 쿼리 내에서 참조하는 컬럼명을 지정할 수 있도록 허용해서는 안 됩니다. "order by" 컬럼도 포함됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드에서 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정된 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하므로, 쿼리에 제한 조건을 추가하고 마지막으로 `get` 메서드를 사용하여 쿼리 결과를 조회할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\DB;

    class UserController extends Controller
    {
        /**
         * 애플리케이션의 모든 사용자 목록 표시
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $users = DB::table('users')->get();

            return view('user.index', ['users' => $users]);
        }
    }

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체로 반환됩니다. 각 컬럼의 값은 객체의 프로퍼티 형태로 접근할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->get();

    foreach ($users as $user) {
        echo $user->name;
    }

> **참고**  
> Laravel의 컬렉션에는 데이터 매핑 및 리듀싱을 위한 매우 강력한 다양한 메서드가 있습니다. 자세한 정보는 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회하기

데이터베이스 테이블에서 단일 행만 조회해야 하는 경우, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

    $user = DB::table('users')->where('name', 'John')->first();

    return $user->email;

전체 행이 필요 없는 경우, `value` 메서드를 사용하여 단일 컬럼 값만 바로 추출할 수 있습니다:

    $email = DB::table('users')->where('name', 'John')->value('email');

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

    $user = DB::table('users')->find(3);

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값들만 담은 `Illuminate\Support\Collection`을 받고자 한다면, `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 모든 사용자의 타이틀 컬렉션을 조회할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    $titles = DB::table('users')->pluck('title');

    foreach ($titles as $title) {
        echo $title;
    }

`pluck` 메서드의 두 번째 인수로 반환되는 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다:

    $titles = DB::table('users')->pluck('title', 'name');

    foreach ($titles as $name => $title) {
        echo $title;
    }

<a name="chunking-results"></a>
### 결과 청크 단위로 가져오기

수천 건의 데이터베이스 레코드를 다루어야 한다면, `DB` 파사드에서 제공하는 `chunk` 메서드 사용을 고려하세요. 이 메서드는 한 번에 소량의 결과만 조회하여 각 청크를 클로저에 전달합니다. 예를 들어, `users` 테이블 전체를 100개씩 청크 단위로 조회할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        foreach ($users as $user) {
            //
        }
    });

클로저에서 `false`를 반환하면 더 이상의 청크 처리가 중단됩니다:

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        // 레코드를 처리...

        return false;
    });

청크 처리 중에 데이터베이스 레코드를 업데이트하면 결과가 예기치 않게 바뀔 수 있습니다. 청크 처리 도중 레코드를 업데이트하려면 `chunkById` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드는 기본키를 기준으로 자동으로 결과를 페이지네이션해줍니다:

    DB::table('users')->where('active', false)
        ->chunkById(100, function ($users) {
            foreach ($users as $user) {
                DB::table('users')
                    ->where('id', $user->id)
                    ->update(['active' => true]);
            }
        });

> **경고**  
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제하는 경우, 기본키/외래키의 변경사항이 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 결과에 포함되지 않을 수도 있습니다.

<a name="streaming-results-lazily"></a>
### 게으르게 결과 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행합니다. 하지만 각 청크를 콜백에 전달하는 대신, `lazy()`는 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)를 반환해 결과를 한 번에 하나씩 스트림처럼 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

마찬가지로, 반복 중에 레코드를 업데이트할 계획이 있다면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이러한 메서드는 자동으로 레코드의 기본키를 기준으로 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> **경고**  
> 이터레이션 중 레코드를 업데이트 또는 삭제하면, 기본키나 외래키 변경사항이 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 결과에 포함되지 않을 수도 있습니다.

<a name="aggregates"></a>
### 집계

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 여러 집계 메서드를 제공합니다.  쿼리 작성 후 해당 메서드를 호출하면 됩니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->count();

    $price = DB::table('orders')->max('price');

물론, 집계함수와 다른 절을 조합하여 세밀하게 제어할 수도 있습니다:

    $price = DB::table('orders')
                    ->where('finalized', 1)
                    ->avg('price');

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리 제약 조건에 해당하는 레코드의 존재 여부만 판단할 경우, `count` 대신 `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다:

    if (DB::table('orders')->where('finalized', 1)->exists()) {
        // ...
    }

    if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
        // ...
    }

<a name="select-statements"></a>
## SELECT 문

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정하기

테이블의 모든 컬럼을 조회하고 싶지 않을 때는 `select` 메서드를 사용하여 SELECT 절을 지정할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->select('name', 'email as user_email')
                ->get();

`distinct` 메서드는 쿼리에서 중복을 제거합니다:

    $users = DB::table('users')->distinct()->get();

이미 쿼리 빌더 인스턴스를 갖고 있고, 기존 SELECT 절에 컬럼을 추가하려면 `addSelect` 메서드를 사용할 수 있습니다:

    $query = DB::table('users')->select('name');

    $users = $query->addSelect('age')->get();

<a name="raw-expressions"></a>
## Raw 표현식

때때로 쿼리에 임의의 문자열을 삽입해야 할 수도 있습니다. 이럴 때는 `DB` 파사드의 `raw` 메서드를 사용해 Raw 문자열 표현식을 만들 수 있습니다:

    $users = DB::table('users')
                 ->select(DB::raw('count(*) as user_count, status'))
                 ->where('status', '<>', 1)
                 ->groupBy('status')
                 ->get();

> **경고**  
> Raw 구문은 쿼리에 문자열로 그대로 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 대신 아래 메서드들을 사용해 쿼리의 다양한 부분에 Raw 표현식을 삽입할 수도 있습니다.  
**Raw 표현식이 포함된 쿼리는 SQL 인젝션 취약점으로부터 보호된다고 보장할 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(/* ... */))` 대신 사용됩니다. 두 번째 인수로 바인딩 배열을 선택적으로 받을 수 있습니다:

    $orders = DB::table('orders')
                    ->selectRaw('price * ? as price_with_tax', [1.0825])
                    ->get();

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw`는 Raw "where" 절을 삽입하는 데 사용합니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

    $orders = DB::table('orders')
                    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                    ->get();

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw`는 HAVING 절에 Raw 문자열을 전달하는 데 사용합니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

    $orders = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > ?', [2500])
                    ->get();

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw`는 ORDER BY 절에 Raw 문자열을 전달하는 데 사용합니다:

    $orders = DB::table('orders')
                    ->orderByRaw('updated_at - created_at DESC')
                    ->get();

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw`는 GROUP BY 절에 Raw 문자열을 사용할 때 사용합니다:

    $orders = DB::table('orders')
                    ->select('city', 'state')
                    ->groupByRaw('city, state')
                    ->get();

<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### Inner Join (내부 조인) 절

쿼리 빌더는 쿼리에 조인 절을 추가하는 데 사용할 수 있습니다. 기본적인 "inner join"을 하려면 쿼리 빌더 인스턴스의 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블명이고, 나머지는 조인 조건입니다. 여러 테이블을 한 번에 조인할 수도 있습니다:

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->join('contacts', 'users.id', '=', 'contacts.user_id')
                ->join('orders', 'users.id', '=', 'orders.user_id')
                ->select('users.*', 'contacts.phone', 'orders.price')
                ->get();

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 절

"inner join" 대신 "left join" 또는 "right join"을 하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 서명은 `join`과 동일합니다:

    $users = DB::table('users')
                ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

    $users = DB::table('users')
                ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

<a name="cross-join-clause"></a>
#### Cross Join 절

`crossJoin` 메서드를 사용하여 "교차 조인"을 수행할 수 있습니다. 교차 조인은 두 테이블의 카티션 곱을 생성합니다:

    $sizes = DB::table('sizes')
                ->crossJoin('colors')
                ->get();

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 절을 지정할 수도 있습니다. `join`의 두 번째 인수로 클로저를 전달하면, 이 클로저에 `Illuminate\Database\Query\JoinClause` 인스턴스가 주어지고, 이를 이용해 여러 조건을 정의할 수 있습니다:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
            })
            ->get();

조인에 WHERE 절을 쓰고 싶다면, `JoinClause`의 `where` 및 `orWhere` 메서드를 사용하세요. 이 메서드들은 두 컬럼이 아니라, 컬럼과 값 비교로 동작합니다:

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')
                     ->where('contacts.user_id', '>', 5);
            })
            ->get();

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리를 서브쿼리와 조인할 수 있습니다. 각각의 메서드는 세 개의 인자를 받습니다: 서브쿼리, 테이블 별칭, 그리고 조인 조건을 정의하는 클로저입니다. 다음 예시에서는 각 사용자 레코드에 사용자의 마지막 게시글 작성 시각을 포함한 사용자 컬렉션을 조회합니다:

    $latestPosts = DB::table('posts')
                       ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                       ->where('is_published', true)
                       ->groupBy('user_id');

    $users = DB::table('users')
            ->joinSub($latestPosts, 'latest_posts', function ($join) {
                $join->on('users.id', '=', 'latest_posts.user_id');
            })->get();

<a name="unions"></a>
## 유니온(Unions)

쿼리 빌더는 여러 개의 쿼리를 "유니온"으로 합치는 메서드를 제공합니다. 예를 들어, 초기 쿼리를 만든 뒤 `union` 메서드를 호출해 추가 쿼리들과 유니온할 수 있습니다:

    use Illuminate\Support\Facades\DB;

    $first = DB::table('users')
                ->whereNull('first_name');

    $users = DB::table('users')
                ->whereNull('last_name')
                ->union($first)
                ->get();

`union` 외에, `unionAll` 메서드도 제공합니다. `unionAll`을 사용한 쿼리는 중복 결과를 제거하지 않습니다. `unionAll`의 사용법도 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용해 WHERE 절을 추가할 수 있습니다. 가장 기본적인 형태는 세 개의 인수를 필요로 합니다: 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 컬럼이 100이고, `age`가 35보다 큰 사용자만 조회합니다:

    $users = DB::table('users')
                    ->where('votes', '=', 100)
                    ->where('age', '>', 35)
                    ->get();

편의상 컬럼이 특정 값과 같음을 비교하려면 값만 두 번째 인수로 전달하세요. 이 경우 Laravel은 `=` 연산자를 자동으로 사용합니다:

    $users = DB::table('users')->where('votes', 100)->get();

데이터베이스가 지원하는 어떤 연산자도 사용할 수 있습니다:

    $users = DB::table('users')
                    ->where('votes', '>=', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('votes', '<>', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('name', 'like', 'T%')
                    ->get();

복수의 조건 배열을 `where`에 전달할 수도 있습니다. 각 원소는 세 개의 인수를 담은 서브 배열입니다:

    $users = DB::table('users')->where([
        ['status', '=', '1'],
        ['subscribed', '<>', '1'],
    ])->get();

> **경고**  
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 쿼리에서 참조하는 컬럼명을 사용자 입력으로 지정해서는 안 됩니다. "order by" 컬럼 역시 포함됩니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 여러 번 체이닝시 `AND` 연산자로 묶입니다. 하지만 `orWhere` 메서드를 사용하면 조건을 `OR` 연산자로 연결할 수 있습니다. 사용법은 `where`와 같습니다:

    $users = DB::table('users')
                        ->where('votes', '>', 100)
                        ->orWhere('name', 'John')
                        ->get();

괄호 안에 "or" 조건을 감싸고 싶다면, 첫 번째 인수로 클로저를 전달하세요:

    $users = DB::table('users')
                ->where('votes', '>', 100)
                ->orWhere(function($query) {
                    $query->where('name', 'Abigail')
                          ->where('votes', '>', 50);
                })
                ->get();

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> **경고**  
> 전역 스코프가 적용될 때 예상외의 동작을 방지하려면 항상 `orWhere` 호출을 그룹핑하세요.

<a name="where-not-clauses"></a>
### WHERE NOT 절

`whereNot` 및 `orWhereNot` 메서드는 조건 그룹을 부정(NOT)할 때 사용합니다. 예를 들어, 다음 쿼리는 할인 중이거나 10 미만 가격을 가진 상품을 제외합니다:

    $products = DB::table('products')
                    ->whereNot(function ($query) {
                        $query->where('clearance', true)
                              ->orWhere('price', '<', 10);
                    })
                    ->get();

<a name="json-where-clauses"></a>
### JSON WHERE 절

Laravel은 JSON 컬럼을 지원하는 데이터베이스(MySQL 5.7+, PostgreSQL, SQL Server 2016, SQLite 3.39.0+[JSON1 익스텐션](https://www.sqlite.org/json1.html))에 대해 JSON 컬럼 쿼리를 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용하세요:

    $users = DB::table('users')
                    ->where('preferences->dining->meal', 'salad')
                    ->get();

`whereJsonContains`로 JSON 배열 쿼리도 지원합니다. 이 기능은 SQLite 3.38.0 미만에서 지원되지 않습니다:

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', 'en')
                    ->get();

MySQL 또는 PostgreSQL 사용시 배열을 전달할 수도 있습니다:

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', ['en', 'de'])
                    ->get();

`whereJsonLength`로 JSON 배열의 길이 조건 쿼리도 가능합니다:

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', 0)
                    ->get();

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', '>', 1)
                    ->get();

<a name="additional-where-clauses"></a>
### 추가 WHERE 절

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼값이 두 값 사이에 있는지를 확인합니다:

    $users = DB::table('users')
               ->whereBetween('votes', [1, 100])
               ->get();

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼값이 두 값 범위 외에 있는지를 확인합니다:

    $users = DB::table('users')
                        ->whereNotBetween('votes', [1, 100])
                        ->get();

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 한 컬럼이 같은 행 내 두 컬럼값 사이에 있는지 검사합니다:

    $patients = DB::table('patients')
                           ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                           ->get();

`whereNotBetweenColumns`는 반대로 두 컬럼값 범위 바깥에 있는지 검사합니다:

    $patients = DB::table('patients')
                           ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                           ->get();

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼값이 배열에 포함되어 있음을 확인합니다:

    $users = DB::table('users')
                        ->whereIn('id', [1, 2, 3])
                        ->get();

`whereNotIn`은 컬럼값이 배열에 포함되지 않았음을 확인합니다:

    $users = DB::table('users')
                        ->whereNotIn('id', [1, 2, 3])
                        ->get();

또한, 쿼리 빌더 객체를 두 번째 인수로 전달할 수도 있습니다:

    $activeUsers = DB::table('users')->select('id')->where('is_active', 1);

    $users = DB::table('comments')
                        ->whereIn('user_id', $activeUsers)
                        ->get();

위 예시는 다음 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> **경고**  
> 아주 큰 정수 배열을 바인딩해서 쿼리하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용하면 메모리 사용을 크게 줄일 수 있습니다.

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인지 확인합니다:

    $users = DB::table('users')
                    ->whereNull('updated_at')
                    ->get();

`whereNotNull`은 컬럼 값이 `NULL`이 아님을 확인합니다:

    $users = DB::table('users')
                    ->whereNotNull('updated_at')
                    ->get();

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값과 특정 날짜를 비교할 때 사용합니다:

    $users = DB::table('users')
                    ->whereDate('created_at', '2016-12-31')
                    ->get();

`whereMonth`는 특정 월과 비교합니다:

    $users = DB::table('users')
                    ->whereMonth('created_at', '12')
                    ->get();

`whereDay`는 특정 일과 비교합니다:

    $users = DB::table('users')
                    ->whereDay('created_at', '31')
                    ->get();

`whereYear`는 특정 연도와 비교합니다:

    $users = DB::table('users')
                    ->whereYear('created_at', '2016')
                    ->get();

`whereTime`은 특정 시간과 비교합니다:

    $users = DB::table('users')
                    ->whereTime('created_at', '=', '11:20:45')
                    ->get();

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼 값이 같은지 확인합니다:

    $users = DB::table('users')
                    ->whereColumn('first_name', 'last_name')
                    ->get();

비교 연산자도 전달할 수 있습니다:

    $users = DB::table('users')
                    ->whereColumn('updated_at', '>', 'created_at')
                    ->get();

또한, 컬럼 비교 배열을 전달해 여러 조건을 `AND`로 조합할 수 있습니다:

    $users = DB::table('users')
                    ->whereColumn([
                        ['first_name', '=', 'last_name'],
                        ['updated_at', '>', 'created_at'],
                    ])->get();

<a name="logical-grouping"></a>
### 논리 그룹화

여러 개의 WHERE 절을 괄호로 그룹화해야 할 때가 있습니다. 사실, 전역 스코프 적용 시 예상치 못한 쿼리 결과를 방지하려면 `orWhere`는 항상 괄호로 감싸 그룹화하는 것이 좋습니다. 이를 위해 `where`에 클로저를 전달하세요:

    $users = DB::table('users')
               ->where('name', '=', 'John')
               ->where(function ($query) {
                   $query->where('votes', '>', 100)
                         ->orWhere('title', '=', 'Admin');
               })
               ->get();

이렇게 하면 전달된 클로저 내부의 조건들이 괄호로 감싸집니다. 위 쿼리는 다음과 같습니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> **경고**  
> 전역 스코프 적용시 우발적인 쿼리 오류를 방지하려면 항상 `orWhere`를 그룹으로 묶으세요.

<a name="advanced-where-clauses"></a>
### 고급 WHERE 절

<a name="where-exists-clauses"></a>
### WHERE EXISTS 절

`whereExists`는 SQL의 "where exists" 절을 작성할 수 있게 합니다. 클로저에 쿼리 빌더 인스턴스를 받아 "exists" 절 안에 들어갈 서브쿼리를 정의할 수 있습니다:

    $users = DB::table('users')
               ->whereExists(function ($query) {
                   $query->select(DB::raw(1))
                         ->from('orders')
                         ->whereColumn('orders.user_id', 'users.id');
               })
               ->get();

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

종종 서브쿼리의 결과와 특정 값을 비교하는 WHERE 절이 필요할 수 있습니다. 이때는 클로저와 값을 `where`에 전달하면 됩니다. 다음 쿼리는 주어진 타입의 최근 멤버쉽을 가진 모든 사용자를 찾습니다:

    use App\Models\User;

    $users = User::where(function ($query) {
        $query->select('type')
            ->from('membership')
            ->whereColumn('membership.user_id', 'users.id')
            ->orderByDesc('membership.start_date')
            ->limit(1);
    }, 'Pro')->get();

또는 컬럼을 서브쿼리 결과와 비교할 수도 있습니다. 컬럼, 연산자, 클로저를 순서대로 전달합니다. 아래는 모든 수입 레코드 중 금액이 평균보다 작은 것을 조회하는 예시입니다:

    use App\Models\Income;

    $incomes = Income::where('amount', '<', function ($query) {
        $query->selectRaw('avg(i.amount)')->from('incomes as i');
    })->get();

<a name="full-text-where-clauses"></a>
### 전문 검색(Full Text) WHERE 절

> **경고**  
> Full Text WHERE 절은 현재 MySQL 및 PostgreSQL에서만 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드는 [Full Text 인덱스](/docs/{{version}}/migrations#available-index-types)가 생성된 컬럼에 대해 전문 검색 WHERE 절을 추가합니다. 이 메서드는 데이터베이스에 맞는 SQL로 변환됩니다. 예를 들어 MySQL은 MATCH AGAINST 절을 생성합니다:

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드로 결과를 특정 컬럼 기준으로 정렬할 수 있습니다. 첫 인수는 정렬 컬럼, 두 번째 인수는 `asc` 또는 `desc`로 정렬 방향을 지정합니다:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

여러 컬럼으로 정렬하려면 `orderBy`를 여러 번 호출하세요:

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->orderBy('email', 'asc')
                    ->get();

<a name="latest-oldest"></a>
#### `latest` & `oldest` 메서드

`latest`와 `oldest`는 결과를 `created_at` 컬럼(또는 지정한 컬럼) 기준으로 손쉽게 정렬할 수 있습니다:

    $user = DB::table('users')
                    ->latest()
                    ->first();

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드는 결과를 무작위로 정렬합니다. 예를 들어, 임의의 사용자를 뽑으려면:

    $randomUser = DB::table('users')
                    ->inRandomOrder()
                    ->first();

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 쿼리에 적용된 모든 "order by"를 제거합니다:

    $query = DB::table('users')->orderBy('name');

    $unorderedUsers = $query->reorder()->get();

또한, 컬럼과 방향을 추가해 신규 정렬로 바꿀 수도 있습니다:

    $query = DB::table('users')->orderBy('name');

    $usersOrderedByEmail = $query->reorder('email', 'desc')->get();

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` & `having` 메서드

예상대로, `groupBy`와 `having`은 쿼리 결과를 그룹화할 때 사용합니다. `having`의 시그니처는 `where`와 유사합니다:

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

`havingBetween`으로 결과를 특정 범위 내로 필터링할 수도 있습니다:

    $report = DB::table('orders')
                    ->selectRaw('count(id) as number_of_orders, customer_id')
                    ->groupBy('customer_id')
                    ->havingBetween('number_of_orders', [5, 15])
                    ->get();

여러 컬럼으로 그룹화하려면 `groupBy`에 여러 인수를 전달하세요:

    $users = DB::table('users')
                    ->groupBy('first_name', 'status')
                    ->having('account_id', '>', 100)
                    ->get();

더 복잡한 `having` 구성을 위해서는 [`havingRaw`](#raw-methods)를 사용하세요.

<a name="limit-and-offset"></a>
### LIMIT & OFFSET

<a name="skip-take"></a>
#### `skip` & `take` 메서드

`skip`과 `take`로 쿼리 결과의 개수를 제한하거나, 앞의 결과들을 건너뛸 수 있습니다:

    $users = DB::table('users')->skip(10)->take(5)->get();

또는 `limit`과 `offset`을 사용할 수도 있습니다. 각각 `take`, `skip`과 동일하게 동작합니다:

    $users = DB::table('users')
                    ->offset(10)
                    ->limit(5)
                    ->get();

<a name="conditional-clauses"></a>
## 조건부 절

특정 조건에 따라 쿼리 절이 적용되게 하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에 특정 입력값이 있을 때만 WHERE 조건을 추가하고 싶다면, `when` 메서드를 사용하세요:

    $role = $request->input('role');

    $users = DB::table('users')
                    ->when($role, function ($query, $role) {
                        $query->where('role_id', $role);
                    })
                    ->get();

`when` 메서드는 첫 번째 인수가 `true`일 때에만 주어진 클로저를 실행합니다. 만약 첫 번째 인수가 `false`라면 클로저는 실행되지 않습니다. 즉, 위 예시에서 요청에 `role` 필드가 존재하고, 그 값이 true로 평가될 때에만 해당 클로저가 호출됩니다.

또한, 세 번째 인수로 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가될 때에만 실행됩니다. 예를 들어 기본 정렬을 다르게 설정할 수 있습니다:

    $sortByVotes = $request->input('sort_by_votes');

    $users = DB::table('users')
                    ->when($sortByVotes, function ($query, $sortByVotes) {
                        $query->orderBy('votes');
                    }, function ($query) {
                        $query->orderBy('name');
                    })
                    ->get();

<a name="insert-statements"></a>
## INSERT 문

쿼리 빌더는 `insert` 메서드로 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 값의 배열을 받습니다:

    DB::table('users')->insert([
        'email' => 'kayla@example.com',
        'votes' => 0
    ]);

배열의 배열을 전달해 여러 레코드를 한 번에 삽입할 수도 있습니다:

    DB::table('users')->insert([
        ['email' => 'picard@example.com', 'votes' => 0],
        ['email' => 'janeway@example.com', 'votes' => 0],
    ]);

`insertOrIgnore` 메서드는 삽입 중 에러가 발생해도 무시합니다. 이 메서드를 사용할 때는 중복 레코드 에러가 무시될 뿐 아니라, 데이터베이스 엔진에 따라 다른 종류의 에러도 무시될 수 있음을 유의하세요. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다:

    DB::table('users')->insertOrIgnore([
        ['id' => 1, 'email' => 'sisko@example.com'],
        ['id' => 2, 'email' => 'archer@example.com'],
    ]);

`insertUsing` 메서드는 서브쿼리를 이용해 삽입할 데이터를 결정하여 레코드를 추가합니다:

    DB::table('pruned_users')->insertUsing([
        'id', 'name', 'email', 'email_verified_at'
    ], DB::table('users')->select(
        'id', 'name', 'email', 'email_verified_at'
    )->where('updated_at', '<=', now()->subMonth()));

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있을 때는 `insertGetId`를 사용하면 레코드 삽입 후 ID를 반환받을 수 있습니다:

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

> **경고**  
> PostgreSQL에서 `insertGetId`는 자동 증가 컬럼의 이름이 `id`라고 가정합니다. 만약 다른 "sequence"에서 ID를 받아야 한다면, 컬럼명을 두 번째 인수로 전달하세요.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 존재하는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인수는 삽입/업데이트할 값 배열, 두 번째는 해당 테이블에서 레코드를 고유하게 식별하는 컬럼(들), 세 번째는 이미 존재하는 레코드에서 업데이트할 컬럼 배열입니다:

    DB::table('flights')->upsert(
        [
            ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
            ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
        ],
        ['departure', 'destination'],
        ['price']
    );

위 예시에서는 `departure`와 `destination` 컬럼 값이 같은 레코드가 이미 있으면 `price`만 업데이트하고, 그렇지 않으면 새 레코드를 삽입합니다.

> **경고**  
> SQL Server를 제외한 데이터베이스는 `upsert` 두 번째 인수의 컬럼들이 "primary" 또는 "unique" 인덱스로 지정되어 있어야 합니다. 그리고 MySQL 드라이버는 항상 테이블의 "primary" 및 "unique" 인덱스만을 사용합니다.

<a name="update-statements"></a>
## UPDATE 문

쿼리 빌더는 레코드 삽입 외에도, `update` 메서드로 기존 레코드 값을 업데이트할 수 있습니다. `update` 역시 컬럼명-값 쌍의 배열을 받으며, 반환값은 영향 받은 행의 수입니다. `where` 절로 업데이트 대상을 한정해야 합니다:

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['votes' => 1]);

<a name="update-or-insert"></a>
#### Update Or Insert

특정 조건에 맞는 기존 레코드가 있으면 업데이트하고, 없으면 삽입하려면 `updateOrInsert`를 사용하세요. 두 인수를 받으며, 첫 번째는 레코드 탐색 조건, 두 번째는 업데이트할 컬럼-값 배열입니다.

첫 인수에 해당하는 레코드가 있으면 두 번째 인수를 적용해 업데이트, 없으면 두 인수 정보를 조합해 새 레코드를 삽입합니다:

    DB::table('users')
        ->updateOrInsert(
            ['email' => 'john@example.com', 'name' => 'John'],
            ['votes' => '2']
        );

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼을 업데이트할 때는 `->` 문법을 이용해 객체 내 키를 지정해 값만 바꿀 수 있습니다. 이 기능은 MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다:

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['options->enabled' => true]);

<a name="increment-and-decrement"></a>
### 증가 & 감소

쿼리 빌더에는 지정 컬럼 값을 증가 또는 감소시키는 편리한 메서드도 있습니다. 최소 한 개의 인수가 필요하며, 두 번째 인수로 증가/감소치를 지정할 수 있습니다:

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

필요하다면 증가/감소와 동시에 다른 컬럼을 수정할 수도 있습니다:

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

또한, `incrementEach`와 `decrementEach`로 여러 컬럼을 동시에 증/감할 수도 있습니다:

    DB::table('users')->incrementEach([
        'votes' => 5,
        'balance' => 100,
    ]);

<a name="delete-statements"></a>
## DELETE 문

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제할 때 사용합니다. 반환값은 영향 받은 행의 수이며, `where`로 대상 레코드를 제한할 수 있습니다:

    $deleted = DB::table('users')->delete();

    $deleted = DB::table('users')->where('votes', '>', 100)->delete();

테이블의 모든 데이터를 삭제하고, AUTO_INCREMENT 값을 0으로 초기화하려면 `truncate`를 사용하세요:

    DB::table('users')->truncate();

<a name="table-truncation-and-postgresql"></a>
#### 테이블 잘라내기(truncate) & PostgreSQL

PostgreSQL 데이터베이스에서 truncate를 사용할 때는 `CASCADE`가 적용됩니다. 즉, 외래키로 연결된 타 테이블의 관련 레코드들도 모두 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 SELECT 실행 시 "비관적 잠금"을 돕는 기능도 내장되어 있습니다. "공유 잠금(shared lock)"을 사용하려면 `sharedLock`을 호출하세요. 공유 잠금을 사용하면 트랜잭션이 커밋될 때까지 선택된 행을 수정할 수 없습니다:

    DB::table('users')
            ->where('votes', '>', 100)
            ->sharedLock()
            ->get();

"for update" 잠금을 적용하려면 `lockForUpdate`를 사용하세요. 이는 선택된 레코드가 수정되거나 다른 공유 잠금으로 선택되는 것을 방지합니다:

    DB::table('users')
            ->where('votes', '>', 100)
            ->lockForUpdate()
            ->get();

<a name="debugging"></a>
## 디버깅

쿼리 빌더를 작성하는 와중에 `dd`와 `dump` 메서드로 현재 쿼리 바인딩과 SQL을 확인할 수 있습니다. `dd`는 디버그 정보를 표시하고 요청 실행을 중단하며, `dump`는 디버그 정보를 표시하고 요청은 계속 실행됩니다:

    DB::table('users')->where('votes', '>', 100)->dd();

    DB::table('users')->where('votes', '>', 100)->dump();
