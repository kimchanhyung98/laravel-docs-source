# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 검증하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호를 다시 해싱해야 하는지 확인하기](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자 비밀번호 저장을 위해 안전한 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하는 경우 기본적으로 등록과 인증에 Bcrypt가 사용됩니다.

Bcrypt는 "작업 비용(work factor)"을 조절할 수 있기 때문에 비밀번호 해싱에 탁월한 선택입니다. 작업 비용이란 해시 생성에 걸리는 시간으로, 하드웨어 성능이 향상됨에 따라 이 시간을 늘릴 수 있습니다. 비밀번호 해싱에서는 느린 연산이 더 안전합니다. 해시 생성에 시간이 오래 걸릴수록, 악의적인 사용자가 무차별 대입 공격을 위해 가능한 모든 문자열 해시 값을 미리 계산하는 이른바 "레인보우 테이블"을 만드는 데 더 많은 시간이 소요됩니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 지정할 수 있습니다. 현재 지원하는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i와 Argon2id 변형 포함)가 있습니다.

> [!NOTE]
> Argon2i 드라이버는 PHP 7.2.0 이상, Argon2id 드라이버는 PHP 7.3.0 이상이 필요합니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

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
     * 사용자의 비밀번호를 업데이트합니다.
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
#### Bcrypt 작업 비용 조절

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드의 `rounds` 옵션으로 작업 비용을 조절할 수 있습니다. 다만 Laravel이 기본으로 관리하는 작업 비용은 대부분의 애플리케이션에서 적절합니다:

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 비용 조절

Argon2 알고리즘을 사용하는 경우, `make` 메서드의 `memory`, `time`, `threads` 옵션으로 작업 비용을 조절할 수 있습니다. 기본값 또한 Laravel이 관리하는 값으로 대부분의 애플리케이션에 적합합니다:

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!TIP]
> 이러한 옵션들에 관한 자세한 내용은 [PHP 공식 문서의 Argon 해싱 관련 부분](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 검증하기

`Hash` 파사드의 `check` 메서드를 사용하면 평문 비밀번호가 특정 해시와 일치하는지 검증할 수 있습니다:

```
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 다시 해싱해야 하는지 확인하기

`Hash` 파사드의 `needsRehash` 메서드는 비밀번호를 해싱할 때 사용된 작업 비용이 변경되었는지 확인하는 데 사용합니다. 일부 애플리케이션은 인증 과정에서 이 검사를 수행하기도 합니다:

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```