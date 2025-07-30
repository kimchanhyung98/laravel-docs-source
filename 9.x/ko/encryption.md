# 암호화 (Encryption)

- [소개](#introduction)
- [설정](#configuration)
- [Encrypter 사용법](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 OpenSSL을 사용하여 AES-256 및 AES-128 암호화를 통해 텍스트를 암호화하고 복호화하는 간단하고 편리한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)로 서명되어 암호화된 후에는 기본 값이 수정되거나 변조되지 않도록 보호합니다.

<a name="configuration"></a>
## 설정

Laravel의 Encrypter를 사용하기 전에 `config/app.php` 설정 파일에서 `key` 구성 옵션을 반드시 설정해야 합니다. 이 구성 값은 `APP_KEY` 환경 변수에 의해 결정됩니다. `php artisan key:generate` 명령어를 사용해 이 변수 값을 생성하는 것이 좋습니다. 이 명령어는 PHP의 안전한 난수 생성기를 사용하여 애플리케이션에 대해 암호학적으로 안전한 키를 생성해 줍니다. 일반적으로 `APP_KEY` 환경 변수 값은 [Laravel 설치](/docs/9.x/installation) 과정에서 자동으로 생성됩니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용법

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 모든 암호화된 값은 OpenSSL과 AES-256-CBC 암호화 방식을 사용해 암호화됩니다. 또한 모든 암호화된 값은 메시지 인증 코드(MAC)로 서명되어 있습니다. 이 인증 코드는 악의적인 사용자가 값을 변조했을 경우 이를 감지하고 복호화를 방지합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * 사용자의 DigitalOcean API 토큰을 저장합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function storeSecret(Request $request)
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();
    }
}
```

<a name="decrypting-a-value"></a>
#### 값 복호화하기

`Crypt` 파사드에서 제공하는 `decryptString` 메서드를 통해 암호화된 값을 복호화할 수 있습니다. 만약 메시지 인증 코드가 유효하지 않거나 값이 정상적으로 복호화될 수 없으면 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다.

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    //
}
```