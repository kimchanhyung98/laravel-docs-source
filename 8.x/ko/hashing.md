# 해싱

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호와 해시가 일치하는지 확인하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호가 다시 해싱이 필요한지 확인하기](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 사용하는 경우 등록 및 인증에 기본적으로 Bcrypt가 사용됩니다.

Bcrypt는 "작업 인자(work factor)"를 조정할 수 있기 때문에 비밀번호 해싱에 훌륭한 선택입니다. 즉, 하드웨어 성능이 향상됨에 따라 해시 생성에 소요되는 시간을 증가시킬 수 있습니다. 비밀번호를 해싱할 때는 느릴수록 좋습니다. 알고리즘이 비밀번호를 해싱하는 데 오래 걸릴수록, 악의적인 사용자가 모든 가능한 문자열 해시 값을 미리 계산하여 생성하는 "레인보우 테이블" 공격이나 무차별 대입(brute force) 공격을 수행하는 데 더 오랜 시간이 필요하기 때문입니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 지정합니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i, Argon2id 변종)입니다.

> {note} Argon2i 드라이버는 PHP 7.2.0 이상이 필요하며, Argon2id 드라이버는 PHP 7.3.0 이상이 필요합니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

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
            // 새로운 비밀번호의 길이 유효성 검사...

            $request->user()->fill([
                'password' => Hash::make($request->newPassword)
            ])->save();
        }
    }

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 인자 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 이용해 알고리즘의 작업 인자를 조절할 수 있습니다. 대부분의 애플리케이션에서는 Laravel이 기본적으로 관리하는 작업 인자가 적절합니다:

    $hashed = Hash::make('password', [
        'rounds' => 12,
    ]);

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 인자 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션을 이용해 작업 인자를 조절할 수 있습니다. 대부분의 애플리케이션에서는 Laravel이 기본적으로 관리하는 값이 적절합니다:

    $hashed = Hash::make('password', [
        'memory' => 1024,
        'time' => 2,
        'threads' => 2,
    ]);

> {tip} 이러한 옵션에 대한 자세한 내용은 [공식 PHP Argon 해싱 관련 문서](https://secure.php.net/manual/en/function.password-hash.php)를 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호와 해시가 일치하는지 확인하기

`Hash` 파사드에서 제공되는 `check` 메서드를 사용하면 주어진 일반 문자열이 해당 해시와 일치하는지 확인할 수 있습니다:

    if (Hash::check('plain-text', $hashedPassword)) {
        // 비밀번호가 일치합니다...
    }

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호가 다시 해싱이 필요한지 확인하기

`Hash` 파사드에서 제공하는 `needsRehash` 메서드를 사용하면, 비밀번호가 해싱된 이후 해싱 알고리즘의 작업 인자가 변경되었는지를 확인할 수 있습니다. 일부 애플리케이션은 인증 과정에서 이 검사를 수행하기도 합니다:

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }