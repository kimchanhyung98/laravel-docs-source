# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호와 해시 일치 여부 검증](#verifying-that-a-password-matches-a-hash)
    - [비밀번호 재해싱 필요 여부 판단](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/11.x/facades)는 사용자 비밀번호를 저장하기 위한 안전한 Bcrypt 및 Argon2 해싱을 제공합니다. 만약 [Laravel 애플리케이션 스타터 키트](/docs/11.x/starter-kits)를 사용한다면, 기본적으로 가입과 인증에 Bcrypt가 사용됩니다.

Bcrypt는 해싱 작업의 난이도(작업 계수, work factor)를 조정할 수 있어서, 하드웨어 성능이 향상됨에 따라 해시 생성에 필요한 시간을 늘릴 수 있기 때문에 비밀번호 해싱에 적합한 선택입니다. 비밀번호를 해싱할 때는 속도가 느린 것이 오히려 좋습니다. 해싱 알고리즘이 비밀번호 해싱에 오래 걸릴수록, 악의적인 사용자가 가능한 모든 문자열 해시값을 담은 ‘무지개 테이블(rainbow tables)’을 생성하여 브루트포스 공격을 시도하는 데 더 많은 시간이 필요하기 때문입니다.

<a name="configuration"></a>
## 설정

기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 하지만 [`argon`](https://en.wikipedia.org/wiki/Argon2) 및 [`argon2id`](https://en.wikipedia.org/wiki/Argon2)와 같은 다른 해싱 드라이버도 지원합니다.

애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 그러나 Laravel의 모든 해싱 드라이버 옵션을 직접 설정하려면, `config:publish` Artisan 명령어를 사용해 `hashing` 설정 파일 전체를 퍼블리시하는 것이 좋습니다:

```bash
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자의 비밀번호를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        // 새 비밀번호 길이 유효성 검증...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션으로 작업 계수를 제어할 수 있습니다. 그러나 Laravel에서 기본으로 제공하는 작업 계수는 대부분의 애플리케이션에서 적절하게 작동합니다:

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션으로 작업 계수를 조절할 수 있습니다. 하지만 Laravel에서 기본으로 관리하는 값들은 대부분의 애플리케이션에 적합합니다:

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]  
> 이러한 옵션에 대한 자세한 내용은 [PHP 공식 문서의 Argon 해싱 관련 부분](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호와 해시 일치 여부 검증

`Hash` 파사드가 제공하는 `check` 메서드를 사용하면, 주어진 평문 문자열이 어떤 해시와 일치하는지 검증할 수 있습니다:

```
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호 재해싱 필요 여부 판단

`Hash` 파사드의 `needsRehash` 메서드는, 비밀번호 해싱 시 사용된 작업 계수가 변경되었는지 검사할 수 있습니다. 일부 애플리케이션은 인증 과정 중에 이 검사를 수행해 재해싱을 합니다:

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증

해시 알고리즘 조작을 방지하기 위해, Laravel의 `Hash::check` 메서드는 먼저 주어진 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 확인합니다. 만약 알고리즘이 다르면 `RuntimeException` 예외가 발생합니다.

대부분 애플리케이션에서는 해싱 알고리즘이 변경되지 않는 것이 일반적이며, 다른 알고리즘이 발견되는 것은 악의적인 공격 신호일 수 있기 때문에 이 동작이 기대됩니다. 다만, 애플리케이션에서 해싱 알고리즘을 점진적으로 변경하는 등 다중 알고리즘을 지원해야 한다면, `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```