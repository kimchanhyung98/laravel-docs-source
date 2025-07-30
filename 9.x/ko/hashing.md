# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱하기](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 검증하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호를 재해싱해야 하는지 확인하기](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/9.x/facades)는 사용자 비밀번호를 저장하기 위한 보안이 강화된 Bcrypt와 Argon2 해싱을 제공합니다. 만약 [Laravel 애플리케이션 스타터 키트](/docs/9.x/starter-kits) 중 하나를 사용하고 있다면, 기본적으로 회원가입과 인증에 Bcrypt가 사용됩니다.

Bcrypt는 해싱할 때 "작업 부하(work factor)"를 조정할 수 있어, 하드웨어 성능이 향상됨에 따라 해시 생성에 걸리는 시간을 늘릴 수 있기 때문에 비밀번호 해싱에 적합한 방식입니다. 비밀번호 해싱에 있어서 느린 속도는 오히려 장점입니다. 해시를 생성하는 데 시간이 오래 걸릴수록 악의적인 사용자가 가능한 모든 문자열 해시값의 '레인보우 테이블'을 생성하는 데 더 많은 시간이 필요하므로, 무차별 대입 공격에 대한 방어 효과가 커집니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 구성됩니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2)(Argon2i 및 Argon2id 변형)입니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱하기

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자 비밀번호를 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // 새 비밀번호 길이 유효성 검증...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 부하 조정하기

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 통해 작업 부하를 조절할 수 있지만, Laravel이 기본적으로 관리하는 작업 부하는 대부분의 애플리케이션에 적합합니다:

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 부하 조정하기

Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션을 통해 작업 부하를 조절할 수 있지만, Laravel이 기본으로 설정해 둔 값이 대부분의 애플리케이션에 적합합니다:

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이러한 옵션에 대한 자세한 내용은 [PHP 공식 문서의 Argon 해싱 관련 내용](https://secure.php.net/manual/en/function.password-hash.php)을 참고하시기 바랍니다.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 검증하기

`Hash` 파사드에서 제공하는 `check` 메서드를 사용하면, 주어진 평문 문자열이 특정 해시와 일치하는지 검증할 수 있습니다:

```
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 재해싱해야 하는지 확인하기

`Hash` 파사드의 `needsRehash` 메서드를 사용하면, 비밀번호가 해싱된 이후 해싱 작업 부하가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션은 인증 과정에서 이 검사를 수행하기도 합니다:

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```