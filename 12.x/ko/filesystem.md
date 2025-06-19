# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [스코프 지정 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 가져오기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 조회](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞/뒤에 내용 추가하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개 범위(가시성)](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

라라벨은 Frank de Jonge가 개발한 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일시스템 추상화를 제공합니다. 라라벨 Flysystem 통합 기능은 로컬 파일시스템, SFTP, Amazon S3 등 다양한 스토리지를 손쉽게 사용할 수 있도록 단순한 드라이버를 제공합니다. 더불어 API가 시스템마다 동일하게 동작하기 때문에, 로컬 개발 환경과 운영 서버에서 다양한 저장소 옵션을 매우 쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정

라라벨의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 여러분이 사용할 "디스크"들을 모두 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 의미합니다. 지원되는 각 드라이버에 대한 예시 설정이 이미 포함되어 있으니, 원하는 저장 방식이나 인증 정보를 바탕으로 설정을 변경하시면 됩니다.

`local` 드라이버는 라라벨 애플리케이션이 실행 중인 서버의 로컬 파일에 접근하며, `sftp` 저장소 드라이버는 SSH 키 기반 FTP 전송에 사용됩니다. `s3` 드라이버는 아마존 S3 클라우드 스토리지 서비스에 파일을 쓸 때 사용합니다.

> [!NOTE]
> 원하는 만큼 디스크를 설정할 수 있으며, 동일한 드라이버로 여러 디스크를 구성해도 됩니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때는 모든 파일 작업이 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 이루어집니다. 기본적으로 이 값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 따라서 아래 메서드는 `storage/app/private/example.txt` 파일에 데이터를 기록하게 됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 외부에서 접근 가능한 파일을 저장할 용도로 마련되어 있습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일은 `storage/app/public`에 저장됩니다.

`public` 디스크가 `local` 드라이버를 사용하고, 이 파일들을 웹 상에서 접근할 수 있도록 하려면, 소스 디렉터리 `storage/app/public`을 대상 디렉터리 `public/storage`에 심볼릭 링크로 연결해야 합니다.

이 심볼릭 링크를 생성하려면, 다음과 같이 아티즌 명령어 `storage:link`를 사용합니다.

```shell
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 생성되면, `asset` 헬퍼를 사용해 해당 파일의 URL을 만들 수 있습니다.

```php
echo asset('storage/file.txt');
```

추가적인 심볼릭 링크도 `filesystems` 설정 파일에 구성할 수 있습니다. 설정된 링크들은 `storage:link` 명령어를 실행할 때마다 함께 생성됩니다.

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령어는 설정된 심볼릭 링크를 삭제할 때 사용할 수 있습니다.

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하려면 Composer 패키지 매니저로 Flysystem S3 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 설정 파일에 위치합니다. 보통 아래와 같은 환경 변수를 활용해 인증 정보를 지정하며, 이 값들은 `config/filesystems.php`에서도 참조합니다.

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수들은 AWS CLI에서 사용하는 네이밍 규칙과 동일하므로, 더욱 편리하게 작업할 수 있습니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하려면 Composer로 Flysystem FTP 패키지를 먼저 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

라라벨의 Flysystem 통합 기능은 FTP로도 잘 동작하지만, 프레임워크의 기본 `config/filesystems.php`에는 별도의 샘플 설정이 포함되어 있지 않습니다. FTP 파일시스템을 설정하려면 아래의 예시 구성을 참고하여 사용하실 수 있습니다.

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // Optional FTP Settings...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하려면 Composer로 Flysystem SFTP 패키지를 사전에 설치해야 합니다.

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

라라벨의 Flysystem 통합은 SFTP와도 잘 동작합니다. 단, 프레임워크 기본 `config/filesystems.php`에는 SFTP 샘플 설정이 포함되어 있지 않습니다. SFTP 파일시스템 활용이 필요한 경우 아래와 같은 설정 예제를 참고하실 수 있습니다.

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key-based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // Settings for file / directory permissions...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // Optional SFTP Settings...
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
### 스코프 지정 및 읽기 전용 파일시스템

스코프 지정(Scoped) 디스크를 사용하면, 특정 경로 프리픽스가 자동으로 앞에 붙는 파일시스템을 정의할 수 있습니다. 스코프 파일시스템 디스크를 만들려면 Composer로 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

이미 존재하는 파일시스템 디스크의 경로에 스코프를 지정하려면 `scoped` 드라이버를 사용해 디스크를 추가로 정의할 수 있습니다. 예를 들어, 기존의 `s3` 디스크에 특정 경로 프리픽스를 지정하는 디스크를 만들면, 해당 디스크로 파일 작업을 할 때마다 지정된 프리픽스가 자동으로 적용됩니다.

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 만들 수 있도록 해줍니다. `read-only` 설정 옵션을 사용하려면 Composer로 별도의 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

그 후, 디스크 설정 배열에 `read-only` 옵션을 포함하여 지정할 수 있습니다.

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

애플리케이션의 기본 `filesystems` 설정 파일에는 이미 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크를 [Amazon S3](https://aws.amazon.com/s3/)와 함께 사용할 수 있을 뿐 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/)와 같은 S3 호환 파일 스토리지 서비스와도 연동할 수 있습니다.

보통, 해당 서비스에 맞게 인증 정보(자격 증명)를 업데이트 한 뒤에는, `endpoint` 설정 값만 변경해주시면 됩니다. 이 값은 주로 `AWS_ENDPOINT` 환경 변수에서 정의합니다.

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO를 사용할 때 라라벨 Flysystem이 올바른 URL을 생성할 수 있도록 하려면, `AWS_URL` 환경 변수의 값을 애플리케이션의 로컬 URL과 버킷 이름이 포함된 경로로 설정해야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> `endpoint`가 클라이언트에서 접근 불가능한 경우에는, MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성이 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 가져오기

`Storage` 파사드를 사용하면 모든 설정된 디스크와 쉽게 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 이용해 기본 디스크에 아바타를 저장할 수 있습니다. 만약 `Storage` 파사드에서 먼저 `disk` 메서드를 호출하지 않고 바로 메서드를 호출하면, 해당 메서드는 자동으로 기본 디스크에 전달됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션이 여러 디스크를 사용하는 경우, `Storage` 파사드의 `disk` 메서드를 사용해 특정 디스크에서 파일 작업을 할 수 있습니다.

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

경우에 따라 애플리케이션의 `filesystems` 설정 파일에 디스크 구성이 존재하지 않더라도, 런타임에 임의의 설정으로 디스크를 생성하고 싶을 수 있습니다. 이럴 때는 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 조회

`get` 메서드를 사용해 파일의 내용을 불러올 수 있습니다. 해당 메서드는 파일의 원시 문자열 데이터를 반환합니다. 모든 파일 경로는 디스크의 "root" 경로 기준으로 상대 경로로 지정해야 한다는 점을 기억하세요.

```php
$contents = Storage::get('file.jpg');
```

만약 조회하려는 파일의 내용이 JSON이라면, `json` 메서드를 사용해 파일을 불러오고, 내용을 디코딩할 수 있습니다.

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 디스크에 해당 파일이 존재하는지 확인할 때 사용합니다.

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 존재하지 않는지 확인할 때 사용할 수 있습니다.

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정한 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. `download` 메서드는 두 번째 인수로 파일명을 지정할 수 있으며, 이는 사용자가 파일을 다운로드할 때 보게 되는 이름입니다. 마지막으로, HTTP 헤더 배열을 세 번째 인수로 전달할 수 있습니다.

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용해 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용할 경우, 일반적으로 `/storage` 경로가 앞에 붙은 상대 경로의 URL이 반환됩니다. 반면, `s3` 드라이버를 사용하면 완전히 경로가 지정된 원격 URL이 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 때는 공개적으로 접근해야 하는 모든 파일을 `storage/app/public` 디렉터리에 두어야 합니다. 또한, `public/storage`에 [심볼릭 링크를 생성](#the-public-disk)하여 `storage/app/public` 디렉터리를 가리키도록 해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때 `url` 메서드의 반환값은 URL 인코딩이 적용되지 않은 상태입니다. 따라서 항상, 올바른 URL이 생성될 수 있도록 파일명을 저장하는 것을 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드를 통해 생성되는 URL의 호스트를 변경하고 싶다면, 디스크 설정 배열에 `url` 옵션을 추가하거나 수정하면 됩니다.

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

`temporaryUrl` 메서드를 사용하면 `local`, `s3` 드라이버로 저장된 파일에 임시로 접근할 수 있는 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시간을 지정하는 `DateTime` 인스턴스를 받습니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

애플리케이션 개발을 기존에 시작했고, `local` 드라이버에서 임시 URL을 지원하기 전에 작업을 했던 경우, 로컬 임시 URL 기능을 직접 활성화해야 할 수도 있습니다. 이를 위해선 `config/filesystems.php` 파일의 `local` 디스크 설정 배열에 `serve` 옵션을 추가해주면 됩니다.

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

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요한 경우, `temporaryUrl` 메서드의 세 번째 인수로 파라미터 배열을 전달할 수 있습니다.

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

특정 스토리지 디스크에서 임시 URL 생성 방식을 직접 커스터마이징하고 싶다면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크의 파일을 다운로드할 수 있도록 컨트롤러에서 임시 접근을 제공해야 하는 상황에 유용합니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드 안에서 호출합니다.

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
     * Bootstrap any application services.
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
> 임시 업로드 URL 생성을 지원하는 드라이버는 `s3` 뿐입니다.

클라이언트 애플리케이션에서 직접 파일 업로드가 가능하도록 임시 업로드 URL을 생성해야 하는 경우, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 업로드 경로와 URL 만료 시간(`DateTime` 인스턴스)을 입력받으며, 업로드에 사용될 URL과 반드시 함께 전송해야 하는 헤더를 포함한 연관 배열을 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 방법은 주로 서버리스 환경에서 Amazon S3와 같은 클라우드 스토리지로 클라이언트에서 직접 파일을 업로드해야 하는 상황에 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 외에도, 라라벨은 파일 자체에 대한 정보 조회도 지원합니다. 예를 들어, `size` 메서드는 파일 크기를 바이트 단위로 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 시점의 UNIX 타임스탬프를 반환합니다.

```php
$time = Storage::lastModified('file.jpg');
```

지정 파일의 MIME 타입은 `mimeType` 메서드로 알아낼 수 있습니다.

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드는 파일의 전체 경로(path)를 반환합니다. `local` 드라이버를 사용할 경우 이 메서드는 파일의 절대 경로를, `s3` 드라이버를 사용할 경우 버킷 내 파일의 상대 경로를 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드를 사용하면 디스크에 파일 내용을 저장할 수 있습니다. 또한, Flysystem의 스트림 지원 기능을 활용해, PHP `resource`를 `put` 메서드에 전달하는 것도 가능합니다. 모든 파일 경로는 디스크 설정에서 지정한 "root" 기준의 상대 경로임을 기억하세요.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 파일 쓰기 실패

`put` 등 "쓰기" 동작이 정상적으로 파일을 디스크에 저장하지 못하면, `false`를 반환합니다.

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 기록할 수 없습니다...
}
```

원한다면, 파일시스템 디스크의 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 지정되면, `put`과 같은 "쓰기" 메서드가 실패했을 때 `League\Flysystem\UnableToWriteFile` 예외를 던집니다.

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞/뒤에 내용 추가하기

`prepend`와 `append` 메서드를 사용하면, 파일의 맨 앞이나 맨 뒤에 내용을 추가할 수 있습니다.

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 새 위치로 복사할 때 사용하며, `move` 메서드는 기존 파일의 이름을 변경하거나 다른 위치로 옮길 때 사용합니다.

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장소로 스트리밍하면 메모리 사용을 크게 줄일 수 있습니다. 라라벨이 특정 파일을 자동으로 스트림 전송하도록 하려면, `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받고, 지정한 위치로 파일을 자동 스트리밍합니다.

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명으로 자동 고유 ID를 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 직접 명시...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드와 관련해 주의해야 할 점이 몇 가지 있습니다. 파일명 대신 디렉터리명만 지정했는데, 기본적으로 `putFile`은 고유 ID를 생성해서 파일 이름으로 사용합니다. 파일의 확장자는 MIME 타입을 검사해 자동으로 결정됩니다. 그리고 메서드가 반환하는 값은 실제 저장된 파일 경로(생성된 파일명 포함)입니다. 이 경로를 데이터베이스에 저장해두면 활용에 용이합니다.

`putFile`, `putFileAs` 메서드에는 저장 파일의 "공개 여부"(visibility)를 설정하는 인수를 추가로 넣을 수 있습니다. 클라우드 디스크(Amazon S3 등)에 파일을 저장하면서 공개 URL로 접근 가능하게 하고 싶을 때 특히 유용합니다.

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 파일 저장의 가장 흔한 사용 사례 중 하나는, 사진이나 문서 등 사용자가 업로드한 파일 저장입니다. 라라벨에서는 업로드 파일 인스턴스의 `store` 메서드를 호출하면, 매우 간편하게 파일을 저장할 수 있습니다. 업로드된 파일을 저장할 경로를 지정해 `store` 메서드를 호출하세요.

```php
<?php

namespace App\Http\Controllers;

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

이 예시에서 주의해야 할 점이 몇 가지 있습니다. 먼저, 디렉터리 이름만 지정했고 파일명을 따로 지정하지 않았다는 점입니다. 기본적으로 `store` 메서드는 고유 ID를 파일명으로 자동 생성합니다. 파일의 확장자는 MIME 타입에 따라 자동으로 판별됩니다. 반환되는 파일 경로(생성된 파일명 포함)는 데이터베이스 등에 저장해 두고 활용할 수 있습니다.

위와 동일한 파일 저장 작업은 `Storage` 파사드의 `putFile` 메서드를 호출해도 수행할 수 있습니다.

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>

#### 파일명 지정하기

저장되는 파일의 이름이 자동으로 지정되는 것을 원하지 않는 경우, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로(path), 파일명(filename), 그리고 (선택적으로) 디스크 이름을 인수로 받습니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

위 예제와 동일한 파일 저장 작업을 `Storage` 파사드의 `putFileAs` 메서드를 사용하여 수행할 수도 있습니다.

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 라라벨의 파일 스토리지 메서드에 파일 경로를 전달하기 전에 파일 경로를 직접 정제(정상화)하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 사용해 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하고 싶다면, `store` 메서드의 두 번째 인수로 디스크 이름을 전달하면 됩니다.

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용하는 경우에는, 세 번째 인수로 디스크 이름을 넘겨주면 됩니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 그 외 업로드 파일 정보

업로드한 파일의 원래 이름과 확장자를 얻고 싶다면, `getClientOriginalName`와 `getClientOriginalExtension` 메서드를 사용할 수 있습니다.

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만, `getClientOriginalName`와 `getClientOriginalExtension` 메서드는 파일 이름과 확장자가 악의적인 사용자에 의해 조작될 수 있으므로 안전하지 않다는 점에 유의해야 합니다. 따라서, 일반적으로 업로드된 파일 이름과 확장자를 구할 때는 `hashName`과 `extension` 메서드를 사용하는 것이 더 안전합니다.

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 임의의 이름을 생성합니다...
$extension = $file->extension(); // 파일의 MIME 타입을 기반으로 확장자를 결정합니다...
```

<a name="file-visibility"></a>
### 파일 가시성(visibility)

라라벨의 Flysystem 통합에서 "가시성(visibility)"은 여러 플랫폼에서 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private`로 지정할 수 있습니다. 파일이 `public`으로 선언되면, 일반적으로 다른 사용자도 접근 가능함을 의미합니다. 예를 들어 S3 드라이버를 사용할 경우, `public` 파일의 URL을 조회할 수 있습니다.

파일을 저장할 때 `put` 메서드에 가시성을 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility`와 `setVisibility` 메서드로 조회하거나 변경할 수 있습니다.

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 된 파일의 경우, `storePublicly`와 `storePubliclyAs` 메서드를 사용하면 파일을 `public` 가시성으로 저장할 수 있습니다.

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

`local` 드라이버를 사용할 때, `public` [가시성](#file-visibility)은 디렉터리에 대해서는 `0755`, 파일에 대해서는 `0644` 권한으로 매핑됩니다. 이 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 수정할 수 있습니다.

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
## 파일 삭제하기

`delete` 메서드는 하나의 파일 이름 또는 여러 파일의 배열을 받아 삭제할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면, 파일을 삭제할 디스크를 지정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내부의 모든 파일 가져오기

`files` 메서드는 지정한 디렉터리 내의 모든 파일을 배열로 반환합니다. 하위 디렉터리까지 포함하여 모든 파일 목록을 가져오고 싶다면, `allFiles` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내부의 모든 디렉터리 가져오기

`directories` 메서드는 지정한 디렉터리 내의 모든 하위 디렉터리의 목록을 배열로 반환합니다. 하위 디렉터리까지 모두 포함하려면 `allDirectories` 메서드를 사용합니다.

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성하기

`makeDirectory` 메서드는 필요하다면 하위 디렉터리까지 포함하여 지정한 디렉터리를 생성합니다.

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제하기

마지막으로, `deleteDirectory` 메서드를 사용하면 디렉터리와 그 안의 모든 파일을 삭제할 수 있습니다.

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드를 사용하면 가짜 디스크를 쉽게 생성할 수 있습니다. 이 기능과 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티를 결합하면 파일 업로드 테스트를 훨씬 간단하게 작성할 수 있습니다. 예시:

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

    // 하나 또는 여러 파일이 저장되었는지 검증합니다...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 하나 또는 여러 파일이 저장되지 않았는지 검증합니다...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 해당 디렉터리 내 파일 개수가 기대한 값과 일치하는지 검증합니다...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 해당 디렉터리가 비어 있는지 검증합니다...
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

        // 하나 또는 여러 파일이 저장되었는지 검증합니다...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 하나 또는 여러 파일이 저장되지 않았는지 검증합니다...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 해당 디렉터리 내 파일 개수가 기대한 값과 일치하는지 검증합니다...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 해당 디렉터리가 비어 있는지 검증합니다...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로, `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 만약 이 파일들을 유지하고 싶다면 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 더 자세한 정보는 [HTTP 테스트 문서의 파일 업로드 부분](/docs/12.x/http-tests#testing-file-uploads)을 참고하시기 바랍니다.

> [!WARNING]
> `image` 메서드를 사용하려면 [GD 확장 모듈](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템

라라벨의 Flysystem 통합은 여러 "드라이버"를 기본으로 지원하지만, Flysystem은 이에 제한되지 않고 다양한 외부 스토리지 시스템용 어댑터가 존재합니다. 만약 이 추가 어댑터 중 하나를 라라벨 애플리케이션에서 사용하고 싶다면 커스텀 드라이버를 직접 정의할 수 있습니다.

커스텀 파일 시스템을 정의하려면 먼저 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 유지관리하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다.

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나에서 `boot` 메서드 안에 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다.

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
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름이고, 두 번째 인수는 `$app`(애플리케이션 인스턴스)와 `$config`를 전달받는 클로저입니다. 이 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 지정한 디스크에 대해 `config/filesystems.php`에서 정의한 값들이 들어 있습니다.

이제 확장 서비스 프로바이더를 생성 및 등록했다면, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.