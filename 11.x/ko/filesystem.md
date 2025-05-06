# 파일 스토리지

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일 시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞뒤에 붙여쓰기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge의 뛰어난 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem) 덕분에 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합은 로컬 파일 시스템, SFTP, Amazon S3와 쉽게 연동할 수 있는 드라이버를 제공합니다. 더 나아가, 각 시스템의 API가 동일하게 유지되기 때문에 로컬 개발 환경과 운영 서버 간에 스토리지 옵션을 손쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일 시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정한 스토리지 드라이버와 저장 위치를 나타냅니다. 설정 파일에는 지원되는 각 드라이버에 대한 예제가 포함되어 있으므로 자신의 스토리지 환경과 인증에 맞게 설정을 변경할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 동작하는 서버의 로컬 파일과 상호작용하고, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스를 사용하여 파일을 저장합니다.

> [!NOTE]  
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크를 구성할 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때는 모든 파일 작업이 `filesystems` 설정 파일에서 정의한 `root` 디렉터리를 기준으로 상대 경로로 이루어집니다. 기본적으로 이 값은 `storage/app/private`로 설정되어 있습니다. 따라서 다음 메서드는 `storage/app/private/example.txt`에 파일을 작성합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 외부에서 접근 가능한 파일을 위한 용도로 제공됩니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 파일을 `storage/app/public`에 저장합니다.

`public` 디스크가 `local` 드라이버를 사용하고, 웹에서 이 파일들을 접근 가능하게 하려면 소스 디렉터리 `storage/app/public`에서 대상 디렉터리 `public/storage`로 심볼릭 링크를 생성해야 합니다:

심볼릭 링크를 생성하려면 `storage:link` 아티즌 명령어를 사용하세요:

```shell
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 생성되었다면, `asset` 헬퍼로 파일의 URL을 만들 수 있습니다:

```php
echo asset('storage/file.txt');
```

추가적인 심볼릭 링크를 `filesystems` 설정 파일에서 구성할 수 있습니다. 설정된 각 링크는 `storage:link` 명령어를 실행할 때 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령어를 사용하면 구성된 심볼릭 링크를 제거할 수 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에 Composer 패키지 매니저로 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php`에 있습니다. 보통 다음과 같은 환경 변수를 사용하여 S3 정보 및 인증 정보를 설정하며, 이 환경 변수들은 `config/filesystems.php`에서 참조됩니다:

```
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수들의 명명 규칙은 AWS CLI와 동일하므로 편리합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 작동하지만, 프레임워크의 기본 `config/filesystems.php`에는 샘플 설정이 포함되어 있지 않습니다. FTP 파일 시스템을 구성해야 한다면 아래 예시를 참고하여 설정할 수 있습니다:

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // 선택적 FTP 설정...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 작동하지만, 프레임워크의 기본 설정 파일에 샘플 설정이 포함되어 있지 않습니다. SFTP 파일 시스템을 구성해야 한다면 아래 예시를 참고하여 설정하세요:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 및 암호 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일/디렉터리 권한 설정...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // 선택적 SFTP 설정...
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

스코프 디스크는 모든 경로가 자동으로 지정한 경로 접두어로 시작하는 파일 시스템을 정의할 수 있습니다. 스코프 파일 시스템 디스크를 만들기 전에 Composer로 별도의 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일 시스템 디스크 중 아무 것이나 `scoped` 드라이버를 사용하여 경로 스코프 인스턴스를 만들 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 스코프하여 사용할 수 있습니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용(read-only)" 디스크는 쓰기 작업이 허용되지 않는 파일 시스템 디스크를 만들 수 있습니다. `read-only` 옵션을 사용하기 전에 아래와 같이 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그리고 나서, 디스크 설정 배열 중 하나 또는 그 이상에 `read-only` 옵션을 추가할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템

애플리케이션의 `filesystems` 설정 파일에는 기본적으로 `s3` 디스크의 설정이 포함되어 있습니다. [Amazon S3](https://aws.amazon.com/s3/)와 상호작용하는 데 사용할 수 있을 뿐만 아니라 [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 호환 파일 저장 서비스와도 연동할 수 있습니다.

사용하려는 서비스에 맞게 디스크의 인증 정보를 변경한 후에는 주로 `endpoint` 설정 값을 환경 변수 `AWS_ENDPOINT`로 지정해주면 됩니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하게 하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷 이름을 포함하도록 지정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]  
> 클라이언트에서 `endpoint`에 접근할 수 없으면 MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성이 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드는 설정된 디스크 중 아무 것이나와 상호작용할 때 사용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장할 때 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 먼저 호출하지 않고 `Storage` 파사드에서 메서드를 호출하면, 메서드는 자동으로 기본 디스크에서 실행됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

앱이 여러 디스크와 상호작용해야 한다면 `disk` 메서드로 특정 디스크를 지정해 사용할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

애플리케이션의 `filesystems` 설정 파일에 없는 설정을 사용해 런타임에 즉석에서 디스크 인스턴스를 만들고 싶을 때가 있을 수 있습니다. 이럴 땐 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다:

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

`get` 메서드는 파일의 내용을 가져오는 데 사용할 수 있습니다. 이 메서드는 파일의 원시 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치에 대한 상대 경로로 지정해야 함을 기억하세요:

```php
$contents = Storage::get('file.jpg');
```

가져오는 파일이 JSON을 포함한다면, `json` 메서드로 파일을 가져오고 내용을 디코드할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

파일이 디스크에 존재하는지 확인하려면 `exists` 메서드를 사용할 수 있습니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

디스크에 파일이 없는지 확인하려면 `missing` 메서드를 사용할 수 있습니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저에 지정된 경로의 파일을 다운로드하도록 응답을 생성할 수 있습니다. 두 번째 인자로 파일 이름을 전달해 다운로드될 파일의 이름을 지정할 수 있습니다. 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용하면 주어진 파일에 대한 URL을 가져올 수 있습니다. `local` 드라이버 사용 시 보통 `/storage`를 경로에 덧붙이는 상대 URL을 반환하고, `s3` 드라이버 사용 시 원격의 전체 URL을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 사용 시, 외부에서 접근 가능한 모든 파일은 `storage/app/public` 디렉터리에 있어야 하며, [심볼릭 링크를 생성](#the-public-disk)하여 `public/storage`가 `storage/app/public`을 가리키도록 해야 합니다.

> [!WARNING]  
> `local` 드라이버 사용 시 `url`의 반환값은 URL 인코딩되지 않습니다. 그러므로 파일명을 항상 URL로 사용할 수 있도록 저장하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드를 통해 생성된 URL의 호스트를 변경하고 싶다면, 디스크 설정 배열에 `url` 옵션을 추가하거나 수정하세요:

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

`temporaryUrl` 메서드를 사용해 `local`과 `s3` 드라이버로 저장된 파일에 대한 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

애플리케이션 개발을 임시 URL 도입 이전에 시작했다면 `local` 드라이버에서 임시 URL을 활성화해야 할 수 있습니다. 이를 위해 `config/filesystems.php`에서 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요:

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

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면 `temporaryUrl` 메서드의 세 번째 인자로 파라미터 배열을 전달할 수 있습니다:

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
#### 임시 URL 커스터마이즈

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이즈하고 싶다면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크의 파일 다운로드를 위해 별도 컨트롤러를 둘 때 사용할 수 있습니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
     * 애플리케이션 서비스 부트스트랩.
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
> 임시 업로드 URL 생성을 지원하는 드라이버는 `s3`뿐입니다.

클라이언트 애플리케이션에서 파일을 직접 업로드할 수 있는 임시 URL이 필요하다면, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 만료 시점을 받아 업로드 URL과 업로드 시 포함할 헤더를 담은 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 방식은 Amazon S3와 같은 클라우드 스토리지로 직접 파일 업로드가 필요한 서버리스 환경에서 주로 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 이외에도, Laravel은 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드로 파일 크기(바이트 단위)를 알 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 마지막 수정 시간의 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

지정한 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용해 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버 사용 시 파일의 절대 경로, `s3` 드라이버 사용 시 S3 버킷 내의 상대 경로가 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 파일 내용을 디스크에 저장하는 데 사용할 수 있습니다. PHP `resource`를 `put`에 전달해 Flysystem의 스트림 지원을 활용할 수도 있습니다. 경로는 항상 디스크의 설정된 "root" 위치에 대한 상대 경로여야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 저장 실패

`put` 같은 "쓰기" 메서드가 파일 저장에 실패하면 `false`를 반환합니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 쓸 수 없습니다...
}
```

원한다면 파일 시스템 디스크 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션을 `true`로 설정하면 "쓰기" 메서드는 실패 시 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞뒤에 붙여쓰기

`prepend`와 `append` 메서드를 사용해 파일의 앞이나 뒤에 내용을 쓸 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 다른 위치로 복사하며, `move` 메서드는 파일 이름을 변경하거나 다른 위치로 이동할 때 사용합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장소로 스트리밍하면 메모리 사용량이 크게 줄어듭니다. Laravel이 지정한 파일을 자동으로 스트리밍해 저장하도록 하려면, `putFile` 또는 `putFileAs` 메서드를 사용하세요. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 지정한 위치로 파일을 스트리밍 저장합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 대해 자동으로 고유 ID 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 수동 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile`의 주요 특징은 디렉터리명만 지정하고 파일명을 지정하지 않아도 된다는 점입니다. 기본적으로 이 메서드는 파일명으로 고유 ID(UUID 등)를 생성하며, 파일 확장자는 MIME 타입을 참조해 결정됩니다. 반환값은 전체 경로이므로 DB에 저장하기에 적합합니다.

`putFile`, `putFileAs` 모두 저장된 파일의 "가시성"도 지정할 수 있습니다. 이는 S3와 같은 클라우드 디스크라면 URL로 접근을 허용할 때 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 가장 흔한 파일 저장 사례는 사용자 업로드 파일(사진, 문서 등) 저장입니다. Laravel은 업로드된 파일의 인스턴스에 `store` 메서드를 호출하는 것만으로 매우 쉽게 파일을 저장할 수 있습니다. 원하는 저장 경로를 `store`에 넘겨 저장할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자 아바타를 업데이트합니다.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

위 예시에서 디렉터리명만 지정하고 파일명은 지정하지 않은 것에 유의하세요. 기본적으로 `store` 메서드는 파일명에 고유 ID를 생성하며, 파일 확장자는 MIME 타입을 참조해서 결정합니다. `store` 메서드는 전체 경로를 반환하므로 DB에 저장하기 좋습니다.

또는 동일한 파일 저장 작업을 `Storage` 파사드의 `putFile` 메서드로도 수행할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정

파일명 자동 부여를 원하지 않는 경우, `storeAs` 메서드를 사용하여 경로, 파일명, (선택적으로) 디스크명을 인자로 넘길 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs` 메서드로도 동일하게 처리할 수 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]  
> 인쇄 불가능한 문자, 잘못된 유니코드 문자는 파일 경로에서 자동 제거됩니다. 따라서 파일 경로를 Laravel 파일 스토리지 메서드에 전달하기 전에 미리 정제해주길 권장합니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath`로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 업로드 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하려면 두 번째 인자로 디스크명을 지정하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드의 경우 세 번째 인자로 디스크명을 넘기면 됩니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드 파일의 기타 정보

업로드한 파일의 원래 이름과 확장자를 얻고 싶다면, `getClientOriginalName`과 `getClientOriginalExtension`을 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 악의적인 사용자가 파일 이름이나 확장자를 변조할 수 있기 때문에 안전하지 않으므로, `hashName` 및 `extension` 메서드를 사용하는 것이 더 좋습니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유한 무작위 이름 생성
$extension = $file->extension(); // MIME 타입 기반으로 확장자 결정
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성"은 여러 플랫폼에서의 파일 권한을 추상화한 개념입니다. 파일은 `public`(공개) 또는 `private`(비공개)로 선언할 수 있습니다. 파일이 `public`으로 선언되면 일반적으로 외부에서 접근 가능함을 의미합니다. 예를 들어, S3 드라이버에서는 `public` 파일에 대해 URL을 가져올 수 있습니다.

파일을 쓸 때 `put` 메서드로 가시성을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility`, `setVisibility` 메서드로 조회/설정할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 파일을 다룰 때는 `storePublicly`, `storePubliclyAs` 메서드로 `public` 가시성으로 저장할 수 있습니다:

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

`local` 드라이버에서 `public` [가시성](#file-visibility)은 디렉터리에 `0755`, 파일에 `0644` 권한 부여로 매핑됩니다. 이 권한 값은 앱의 `filesystems` 설정 파일에서 수정할 수 있습니다:

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

`delete` 메서드는 삭제할 파일 이름을 하나 또는 파일 이름 배열로 받을 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면 파일을 삭제할 디스크도 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉터리 내 모든 파일의 배열을 반환합니다. 하위 디렉터리까지 포함한 전체 파일 목록을 가져오려면 `allFiles` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 디렉터리 가져오기

`directories` 메서드는 지정한 디렉터리 내 모든 하위 디렉터리를 배열로 반환합니다. 하위디렉터리까지 모두 포함한 목록은 `allDirectories`로 가져올 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 필요하다면 하위 디렉터리를 포함하여 지정한 디렉터리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

`deleteDirectory` 메서드를 사용하면 디렉터리와 그 안의 모든 파일을 삭제할 수 있습니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드를 사용하면 임시 디스크를 손쉽게 생성할 수 있고, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 기능과 결합하면 파일 업로드 테스트가 매우 간단합니다. 예시:

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

    // 파일 하나 이상이 저장되었는지 확인
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 파일 하나 이상이 저장되지 않았는지 확인
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉터리의 파일 수가 기대치와 일치하는지 확인
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 특정 디렉터리가 비어있는지 확인
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

        // 파일 하나 이상이 저장되었는지 확인
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 파일 하나 이상이 저장되지 않았는지 확인
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리의 파일 수가 기대치와 일치하는지 확인
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉터리가 비어있는지 확인
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 파일을 남기고 싶다면 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대해 더 알아보려면 [HTTP 테스트 문서의 파일 업로드 관련 내용](/docs/{{version}}/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]  
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템

Laravel의 Flysystem 통합은 여러 "드라이버"를 기본 지원하지만, Flysystem은 여기에 한정되지 않고 다양한 추가 스토리지 시스템을 위한 어댑터도 있습니다. 이런 추가 어댑터를 사용하고 싶다면 커스텀 드라이버를 직접 만들 수 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가해봅니다:

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록하세요. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

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
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 두 번째는 `$app`과 `$config` 변수(설정 배열)를 받는 클로저입니다. 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config`는 `config/filesystems.php`에 정의한 디스크 설정 값을 포함합니다.

확장 서비스 프로바이더를 만들고 등록했다면 이제 `config/filesystems.php`에서 `dropbox` 드라이버를 사용할 수 있습니다.