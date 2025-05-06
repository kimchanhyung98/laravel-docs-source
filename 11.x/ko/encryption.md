# 암호화

- [소개](#introduction)
- [설정](#configuration)
    - [암호화 키의 무중단 교체](#gracefully-rotating-encryption-keys)
- [Encrypter 사용하기](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 OpenSSL을 이용해 AES-256 및 AES-128 방식을 통해 텍스트를 암호화하고 복호화할 수 있는 간단하고 편리한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)로 서명되어, 암호화된 이후로 그 값이 변경되거나 변조될 수 없습니다.

<a name="configuration"></a>
## 설정

Laravel의 Encrypter를 사용하기 전에, `config/app.php` 설정 파일에서 `key` 설정 옵션을 지정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에 의해 결정됩니다. `php artisan key:generate` 명령어를 사용하여 이 변수의 값을 생성하는 것이 권장됩니다. 이 명령어는 PHP의 보안 랜덤 바이트 생성기를 이용해, 애플리케이션에 암호학적으로 안전한 키를 생성합니다. 일반적으로, [Laravel 설치](/docs/{{version}}/installation) 시 `APP_KEY` 환경 변수의 값이 자동으로 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
### 암호화 키의 무중단 교체

애플리케이션의 암호화 키를 변경하면, 인증된 모든 사용자 세션이 로그아웃됩니다. 이는 세션 쿠키를 포함한 모든 쿠키가 Laravel에 의해 암호화되기 때문입니다. 또한, 이전에 암호화 키로 암호화된 데이터를 더 이상 복호화할 수 없게 됩니다.

이 문제를 완화하기 위해 Laravel은 애플리케이션의 `APP_PREVIOUS_KEYS` 환경 변수에 이전 암호화 키들을 나열할 수 있도록 지원합니다. 이 변수에는 이전에 사용한 모든 암호화 키를 쉼표(,)로 구분하여 넣을 수 있습니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

이 환경 변수를 설정하면, Laravel은 항상 "현재" 암호화 키를 사용해 값을 암호화합니다. 하지만 값을 복호화할 때는, 먼저 현재 키로 복호화를 시도하고, 실패하는 경우 이전 키 목록을 차례로 시도하여 값의 복호화를 시도합니다.

이와 같은 점진적 복호화 방식 덕분에, 암호화 키가 변경되어도 사용자는 애플리케이션을 중단 없이 계속 사용할 수 있습니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용하기

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 모든 값은 OpenSSL과 AES-256-CBC 암호 알고리즘을 이용해 암호화됩니다. 또한, 암호화된 값은 모두 메시지 인증 코드(MAC)로 서명됩니다. 이 통합된 메시지 인증 코드는 악의적인 사용자가 값을 변조했을 경우 복호화를 막아줍니다:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Crypt;

    class DigitalOceanTokenController extends Controller
    {
        /**
         * 사용자를 위해 DigitalOcean API 토큰을 저장합니다.
         */
        public function store(Request $request): RedirectResponse
        {
            $request->user()->fill([
                'token' => Crypt::encryptString($request->token),
            ])->save();

            return redirect('/secrets');
        }
    }

<a name="decrypting-a-value"></a>
#### 값 복호화하기

`Crypt` 파사드의 `decryptString` 메서드를 이용해 암호화된 값을 복호화할 수 있습니다. 만약 메시지 인증 코드가 유효하지 않아서 값을 정상적으로 복호화할 수 없을 경우, `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

    use Illuminate\Contracts\Encryption\DecryptException;
    use Illuminate\Support\Facades\Crypt;

    try {
        $decrypted = Crypt::decryptString($encryptedValue);
    } catch (DecryptException $e) {
        // ...
    }
