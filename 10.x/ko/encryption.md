# 암호화 (Encryption)

- [소개](#introduction)
- [설정](#configuration)
- [암호화 도구 사용하기](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 AES-256과 AES-128 암호화를 이용하여 OpenSSL 기반으로 텍스트를 간편하게 암호화 및 복호화할 수 있는 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)로 서명되어, 암호화된 값이 변조되거나 수정되지 못하도록 보호합니다.

<a name="configuration"></a>
## 설정

Laravel의 암호화 도구를 사용하기 전에 `config/app.php` 설정 파일 내 `key` 옵션을 반드시 설정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에 의해 지정됩니다. `php artisan key:generate` 명령어를 사용하여 이 환경 변수 값을 생성하는 것을 권장합니다. 이 명령은 PHP의 안전한 랜덤 바이트 생성기를 사용하여 애플리케이션에 강력한 암호화 키를 생성합니다. 일반적으로 `APP_KEY` 환경 변수 값은 [Laravel 설치 가이드](/docs/10.x/installation) 과정에서 자동 생성됩니다.

<a name="using-the-encrypter"></a>
## 암호화 도구 사용하기

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`Crypt` 파사드가 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 암호화된 모든 값은 OpenSSL과 AES-256-CBC 암호화 방식으로 처리됩니다. 또한 모든 암호화 데이터는 메시지 인증 코드(MAC)로 서명되어, 악의적인 사용자가 값을 변조한 경우 복호화를 자동으로 차단합니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a name="decrypting-a-value"></a>
#### 값 복호화하기

`Crypt` 파사드가 제공하는 `decryptString` 메서드를 사용해 값을 복호화할 수 있습니다. 만약 메시지 인증 코드가 유효하지 않거나 올바르게 복호화할 수 없는 경우, `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

```
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```