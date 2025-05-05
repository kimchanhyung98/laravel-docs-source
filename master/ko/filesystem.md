# 파일 스토리지

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [공용 디스크](#the-public-disk)
    - [드라이버 필수조건](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일 시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장하기](#storing-files)
    - [파일 앞/뒤로 쓰기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일 시스템 추상화를 제공합니다. Laravel Flysystem 통합은 로컬 파일 시스템, SFTP, Amazon S3와 작업하기 위한 간단한 드라이버를 제공합니다. 더 좋은 점은, 각 시스템의 API가 동일하기 때문에 로컬 개발 환경에서 프로덕션 서버로 스토리지 옵션을 손쉽게 전환할 수 있다는 점입니다.

<a name="configuration"></a>
## 설정

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치해 있습니다. 이 파일에서 모든 파일 시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 위치를 의미합니다. 지원되는 각 드라이버에 대한 예제 설정도 포함되어 있으므로, 원하는 저장소 환경과 자격 증명에 맞게 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행되는 서버에 로컬로 저장된 파일과 상호작용하고, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스에 파일을 저장할 때 사용됩니다.

> [!NOTE]
> 디스크는 원하는 만큼 추가할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 만들 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉토리 기준으로 상대적으로 동작합니다. 기본적으로 이 값은 `storage/app/private`로 설정되어 있습니다. 예를 들어, 다음 메서드는 `storage/app/private/example.txt`에 작성합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 공용 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 공개적으로 접근해야 하는 파일을 위해 설계되었습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public` 경로에 저장합니다.

`public` 디스크가 `local` 드라이버를 사용하면서, 이 파일들을 웹에서 접근할 수 있게 하려면 `storage/app/public` 원본 디렉터리에서 `public/storage` 대상 디렉터리로 심볼릭 링크를 만들어야 합니다:

심볼릭 링크를 생성하려면 다음의 Artisan 명령을 사용할 수 있습니다:

```shell
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 생성된 후에는 `asset` 헬퍼를 통해 URL을 만들 수 있습니다:

```php
echo asset('storage/file.txt');
```

`filesystems` 설정 파일에서 추가 심볼릭 링크도 설정할 수 있습니다. 설정된 모든 링크는 `storage:link` 명령 실행 시 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

설정된 심볼릭 링크를 제거하려면 `storage:unlink` 명령을 사용할 수 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 필수조건

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버 사용 전, Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 파일에 위치합니다. 일반적으로 S3 정보 및 자격 증명은 다음 환경변수를 사용하여 설정하며, 이는 `config/filesystems.php`에서 참조합니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 변수들은 AWS CLI에서 사용하는 명명 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전, Composer를 통해 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 작동하지만, 기본 설정 파일에 예제 설정은 포함되어 있지 않습니다. FTP 파일 시스템을 설정하려면 다음 예제를 참고하세요:

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // 선택 사항...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

마찬가지로, SFTP의 예제 설정은 기본 파일에 포함되어 있지 않습니다. 아래와 같이 설정할 수 있습니다:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 권한 설정...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // 선택 사항...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```

<a name="scoped-and-read-only-filesystems"></a>
### 스코프 및 읽기 전용 파일 시스템

스코프 디스크는 파일 시스템의 모든 경로에 지정한 프리픽스를 자동으로 붙여주는 방식입니다. 먼저 Composer로 Flysystem path prefixing 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 사용해 기존 파일 시스템 디스크의 경로에 프리픽스를 적용한 인스턴스를 만들 수 있습니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크를 만들려면 다음 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그리고 설정 배열에 `read-only` 옵션을 추가하세요:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템

애플리케이션의 기본 `filesystems` 설정 파일에는 `s3` 디스크 설정이 포함되어 있습니다. [Amazon S3](https://aws.amazon.com/s3/)뿐만 아니라 [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 호환 스토리지 서비스와도 연동 가능합니다.

서비스에 맞게 자격증명을 변경한 후에는, 일반적으로 `endpoint` 설정만 갱신하면 됩니다. 이는 보통 `AWS_ENDPOINT` 환경변수로 정의합니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO 사용 시, Laravel Flysystem이 올바른 URL을 생성하도록 `AWS_URL` 환경변수를 애플리케이션의 로컬 주소(버킷 이름 포함)로 맞춰야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> `endpoint` 값이 클라이언트에서 접근 가능하지 않으면 MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 파일 URL 생성이 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드는 설정한 어떤 디스크와도 상호작용할 수 있습니다. 예를 들어, 아바타를 기본 디스크에 저장하려면 다음처럼 사용할 수 있습니다. `disk` 메서드를 호출하지 않으면, 자동으로 기본 디스크가 사용됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크와 상호작용하는 경우, `disk` 메서드로 특정 디스크를 지정할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

런타임에 설정 파일에 없는 설정으로 디스크를 만들고 싶을 때, `Storage` 파사드의 `build` 메서드에 설정 배열을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 가져오기

`get` 메서드는 파일의 내용(문자열)을 가져올 때 사용합니다. 파일 경로는 디스크의 "root" 위치를 기준으로 상대경로로 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

JSON 파일을 가져오고 디코딩하려면 `json` 메서드를 사용할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 파일 존재 여부 확인에 사용합니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 없는지 확인합니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 브라우저에서 파일 다운로드를 강제하는 응답을 반환합니다. 두 번째 인수로 다운로드되는 파일명을 지정할 수 있으며, 세 번째 인수로 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드는 파일의 URL을 반환합니다. `local` 드라이버를 쓰는 경우 `/storage`가 경로 앞에 붙고, S3 드라이버를 쓰면 완전한 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버에서는 `storage/app/public`에 저장된 파일이 웹에서 공개적으로 접근 가능합니다. 그리고 [심볼릭 링크 생성](#the-public-disk)을 통해 `public/storage` 경로가 `storage/app/public`을 가리키도록 해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때 `url`의 반환값은 URL 인코딩되지 않습니다. 따라서, 항상 유효한 URL이 만들어지도록 올바른 파일명을 사용하시길 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

Storage 파사드로 생성된 URL의 호스트를 변경하려면 디스크 설정 배열의 `url` 옵션을 수정하세요:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a name="temporary-urls"></a>
### 임시 URL

`temporaryUrl` 메서드로 `local` 및 `s3` 드라이버를 사용하는 파일의 임시 URL을 생성할 수 있습니다. 만료 시각을 지정하는 `DateTime` 인스턴스를 전달해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

앱 개발을 일찍 시작해서 `local` 드라이버의 임시 URL 기능을 켜야 할 수도 있습니다. 이 경우, `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
#### S3 요청 파라미터

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, `temporaryUrl`의 세 번째 인자로 파라미터 배열을 전달하세요:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->addMinutes(5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a name="customizing-temporary-urls"></a>
#### 임시 URL 커스터마이징

특정 저장소 디스크에서 임시 URL 생성 방식을 커스터마이징하려면 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 지원하지 않는 디스크를 위한 커스텀 컨트롤러를 만들 때 유용합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 부트스트랩 애플리케이션 서비스.
     */
    public function boot(): void
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(
            function (string $path, DateTime $expiration, array $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            }
        );
    }
}
```

<a name="temporary-upload-urls"></a>
#### 임시 업로드 URL

> [!WARNING]
> 임시 업로드 URL 생성 기능은 `s3` 드라이버에서만 지원됩니다.

클라이언트 앱에서 직접 파일을 업로드할 수 있도록 임시 업로드 URL이 필요하다면, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 만료 시각(`DateTime`)을 받고, 업로드용 URL과 함께 넣어야 할 헤더를 포함하는 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 방법은 주로 Amazon S3와 같은 클라우드 스토리지에 직접 클라이언트에서 업로드해야 하는 서버리스 환경에서 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

Laravel은 파일의 읽기/쓰기에 더해, 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일의 바이트 크기를 가져옵니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 마지막 수정 시각의 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

지정한 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드는 파일의 경로를 반환합니다. `local` 드라이버는 절대경로, `s3` 드라이버는 버킷 내 상대경로를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장하기

`put` 메서드는 파일 내용을 디스크에 저장합니다. PHP `resource`를 전달할 수도 있어 Flysystem의 스트림 지원을 활용합니다. 경로는 디스크의 "root" 기준 상대경로여야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 저장 실패

`put`(또는 기타 "쓰기" 작업) 메서드가 파일 쓰기에 실패하면 `false`가 반환됩니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 저장하지 못함
}
```

원한다면, 디스크 설정 배열에 `throw` 옵션을 지정할 수 있습니다. 이 옵션이 `true`이면, `put`과 같은 "쓰기" 메서드가 실패시 `League\Flysystem\UnableToWriteFile` 예외를 발생시킵니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞/뒤로 쓰기

`prepend`와 `append` 메서드로 파일의 앞이나 끝에 내용을 쓸 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 새 위치에 복사하고, `move`는 파일을 새 위치(이름 변경 포함)로 이동합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 스트리밍 방식으로 저장하면 메모리 사용량이 크게 줄어듭니다. `putFile`과 `putFileAs` 메서드를 이용하면 `Illuminate\Http\File`이나 `Illuminate\Http\UploadedFile` 인스턴스를 자동으로 저장 경로에 스트리밍할 수 있습니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 자동으로 고유 파일명을 생성
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명 직접 지정
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드는 디렉토리만 지정하면 됩니다(파일명은 자동 생성). 확장자는 MIME 타입으로 결정되며, 반환값은 생성된 전체 파일 경로입니다. DB 등에 쉽게 저장할 수 있습니다.

`putFile`과 `putFileAs`는 저장 파일의 "가시성"을 지정하는 인수도 받을 수 있습니다. 예를 들어 S3 같은 클라우드 디스크에 파일을 공개로 저장하려면:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 앱에서 가장 흔한 저장 용도는 사진이나 문서 등 사용자 업로드 파일입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드로 손쉽게 파일을 저장할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자 아바타 수정
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

위 예제에서도 디렉토리만 지정하였으며, 파일명은 자동으로 생성됩니다. 확장자는 MIME 타입에서 결정되고, `store` 메서드는 전체 경로를 반환합니다.

동일한 작업을 `Storage` 파사드의 `putFile` 메서드로도 할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정

자동 파일명이 아닌 직접 파일명을 지정하려면 `storeAs` 메서드를 사용하세요(경로, 파일명[, 디스크]):

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs`로도 동일하게 구현할 수 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄 불가능한 문자 및 유효하지 않은 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 파일 경로를 미리 정제(sanitize)하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath`로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하려면 두 번째 인자로 디스크명을 전달하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드는 세 번째 인자로 디스크명을 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보

업로드된 파일의 원래 이름과 확장자를 얻으려면 `getClientOriginalName`과 `getClientOriginalExtension`을 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

그러나 이 두 메서드는 사용자가 파일명, 확장자를 악의적으로 변경 가능하기 때문에 보안상 안전하지 않습니다. 따라서 가능한 한 `hashName`과 `extension` 메서드 사용을 권장합니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유한 무작위 이름 생성
$extension = $file->extension(); // MIME 타입에 따라 확장자 결정
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel Flysystem 통합에서 "가시성"은 다양한 플랫폼에서 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private`으로 선언할 수 있습니다. `public`은 대체로 파일을 누구나 접근 가능하게 하겠다는 의미입니다. 예를 들어 S3 드라이버의 경우 public 파일의 URL을 얻을 수 있습니다.

파일 저장 시 가시성을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일이라면 `getVisibility`, `setVisibility` 메서드로 가시성 설정 및 조회가 가능합니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 파일과 연동할 때는 `storePublicly`, `storePubliclyAs`를 사용해 public 가시성으로 파일을 저장할 수 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 가시성

`local` 드라이버에서 [가시성](#file-visibility) `public`은 디렉토리 0755, 파일 0644 권한을 의미합니다. 파일 시스템의 설정 파일에서 권한을 커스터마이징할 수 있습니다:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app'),
    'permissions' => [
        'file' => [
            'public' => 0644,
            'private' => 0600,
        ],
        'dir' => [
            'public' => 0755,
            'private' => 0700,
        ],
    ],
    'throw' => false,
],
```

<a name="deleting-files"></a>
## 파일 삭제

`delete` 메서드는 단일 파일명 또는 파일명 배열을 받아 파일을 삭제합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면 디스크를 지정해 파일을 삭제할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 얻기

`files` 메서드는 지정한 디렉토리의 모든 파일을 배열로 반환합니다. 하위 디렉토리까지 모두 포함하려면 `allFiles`를 사용하세요:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 얻기

`directories` 메서드는 지정한 디렉토리 내 모든 하위 디렉토리 배열을 반환합니다. `allDirectories`로 전체 하위 디렉토리까지 목록을 얻을 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 지정한 디렉토리를(필요하면 하위 디렉토리 포함) 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

`deleteDirectory` 메서드로 디렉토리 및 그 안의 파일을 모두 삭제할 수 있습니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 임시 디스크를 쉽게 생성할 수 있으며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 기능과 결합하면 파일 업로드 테스트가 크게 쉬워집니다. 예시:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // 파일이 저장되었는지 확인
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 파일이 저장되지 않았는지 확인
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 지정 디렉토리 내 파일 개수 확인
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 디렉토리가 비어 있는지 확인
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded(): void
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // 파일이 저장되었는지 확인
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 파일이 저장되지 않았는지 확인
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 지정 디렉토리 내 파일 개수 확인
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 디렉토리가 비어 있는지 확인
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉토리 내 모든 파일을 삭제합니다. 파일을 보존하려면 `"persistentFake"` 메서드를 사용하면 됩니다. 파일 업로드 테스트에 관한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 섹션](/docs/{{version}}/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템

Laravel Flysystem 통합은 다양한 "드라이버"를 기본 지원하지만, Flysystem은 이외에도 다양한 스토리지 어댑터가 존재합니다. 추가 어댑터를 Laravel에서 사용하고 싶다면 커스텀 드라이버를 만들 수 있습니다.

먼저 Flysystem 어댑터를 설치해야 합니다. 예를 들어, Dropbox 어댑터를 추가하려면 다음을 실행하세요:

```shell
composer require spatie/flysystem-dropbox
```

그 다음, [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 드라이버를 등록할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Contracts\Foundation\Application;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 부트스트랩
     */
    public function boot(): void
    {
        Storage::extend('dropbox', function (Application $app, array $config) {
            $adapter = new DropboxAdapter(new DropboxClient(
                $config['authorization_token']
            ));

            return new FilesystemAdapter(
                new Filesystem($adapter, $config),
                $adapter,
                $config
            );
        });
    }
}
```

`extend` 메서드의 첫 번째 인자는 드라이버 명이고, 두 번째 인자는 `$app`, `$config`를 받는 클로저입니다. 반환값은 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스여야 합니다. `$config`에는 해당 디스크를 위한 `config/filesystems.php`의 값이 전달됩니다.

확장 서비스를 만들고 등록한 후, 이제 `config/filesystems.php`에서 `dropbox` 드라이버를 사용할 수 있습니다.