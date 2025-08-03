# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 확인하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호를 다시 해싱할 필요가 있는지 판단하기](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Hash` [파사드](/docs/master/facades)는 사용자 비밀번호를 저장할 때 안전한 Bcrypt 및 Argon2 해싱을 제공합니다. 만약 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하고 있다면, 기본적으로 등록과 인증에 Bcrypt가 사용됩니다.

Bcrypt는 해시를 생성하는 데 걸리는 시간이 조절 가능한 "작업 계수(work factor)"를 갖고 있어 하드웨어 성능이 향상됨에 따라 해시 생성 시간을 늘릴 수 있어 비밀번호 해싱에 적합합니다. 해싱 시 느린 속도가 오히려 장점입니다. 알고리즘이 비밀번호 하나를 해싱하는 데 오래 걸릴수록 악의적인 사용자가 무차별 대입 공격에 사용할 수 있는 모든 가능한 문자열 해시값의 "레인보우 테이블"을 생성하는 데 더 오랜 시간이 걸립니다.

<a name="configuration"></a>
## 설정 (Configuration)

기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 그러나 [`argon`](https://en.wikipedia.org/wiki/Argon2)과 [`argon2id`](https://en.wikipedia.org/wiki/Argon2) 같은 다른 여러 해싱 드라이버도 지원합니다.

애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수를 통해 지정할 수 있습니다. 만약 Laravel의 모든 해싱 드라이버 옵션을 커스터마이징하려면, `config:publish` Artisan 명령어로 전체 `hashing` 설정 파일을 퍼블리시 해야 합니다:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="hashing-passwords"></a>
### 비밀번호 해싱 (Hashing Passwords)

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자의 비밀번호를 업데이트 합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        // 새 비밀번호 길이 유효성 검사...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드는 `rounds` 옵션으로 작업 계수를 조절할 수 있지만, Laravel이 기본으로 제공하는 작업 계수는 대부분의 애플리케이션에서 적절합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드는 `memory`, `time`, `threads` 옵션으로 작업 계수를 조절할 수 있지만, Laravel에서 기본으로 설정한 값들은 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이 옵션들에 관한 자세한 내용은 [PHP 공식 문서의 Argon 해싱 함수 설명](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 확인하기 (Verifying That a Password Matches a Hash)

`Hash` 파사드의 `check` 메서드를 사용하면 주어진 평문 문자열이 특정 해시와 일치하는지 확인할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 다시 해싱할 필요가 있는지 판단하기 (Determining if a Password Needs to be Rehashed)

`Hash` 파사드의 `needsRehash` 메서드는 비밀번호 해시 생성 시 사용된 작업 계수가 변경되었는지 확인합니다. 일부 애플리케이션은 인증 과정 중에 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증 (Hash Algorithm Verification)

해시 알고리즘 조작을 방지하기 위해, Laravel의 `Hash::check` 메서드는 주어진 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 먼저 확인합니다. 만약 알고리즘이 다르면 `RuntimeException` 예외가 발생합니다.

대부분의 애플리케이션에서는 해싱 알고리즘이 변경될 것으로 예상하지 않으며, 다른 알고리즘 사용은 악의적인 공격의 징후일 수 있으므로 이 동작이 정상입니다. 하지만, 하나의 애플리케이션에서 알고리즘을 변경하는 등 여러 해싱 알고리즘을 동시에 지원해야 한다면, `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```