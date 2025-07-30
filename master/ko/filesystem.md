# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 가져오기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞뒤에 내용 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 개발한 훌륭한 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem) 덕분에 강력한 파일시스템 추상화를 제공합니다. Laravel Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3를 다루기 위한 간단한 드라이버를 제공합니다. 더 좋은 점은, 로컬 개발 환경과 프로덕션 서버 간에 이러한 저장 옵션들을 API가 동일하게 유지되므로 매우 쉽게 전환할 수 있다는 것입니다.

<a name="configuration"></a>
## 설정

Laravel의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일 내에서 모든 파일시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 저장 드라이버와 저장 위치를 나타냅니다. 설정 파일에는 지원하는 각 드라이버에 대한 예제 설정이 포함되어 있으므로 저장 환경 및 자격 증명에 맞게 자유롭게 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행되는 서버에 로컬로 저장된 파일과 상호 작용하며, `s3` 드라이버는 Amazon의 S3 클라우드 저장소 서비스에 쓰기 위해 사용됩니다.

> [!NOTE]
> 원하는 만큼 디스크를 구성할 수 있으며, 같은 드라이버를 사용하는 여러 디스크를 가질 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 경우 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 상대 경로가 적용됩니다. 기본값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 따라서 다음 메서드는 `storage/app/private/example.txt`에 파일을 작성합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 위한 용도로 만들어졌습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public`에 저장합니다.

만약 `public` 디스크가 `local` 드라이버를 사용하고 있고, 웹에서 이 파일들을 접근 가능하도록 하려면, `storage/app/public` 소스 디렉토리에서 타겟 디렉토리인 `public/storage`로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크는 `storage:link` Artisan 명령어를 통해 생성할 수 있습니다:

```shell
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 구성되면, `asset` 헬퍼를 사용해 파일에 대한 URL을 생성할 수 있습니다:

```php
echo asset('storage/file.txt');
```

추가 심볼릭 링크를 `filesystems` 설정 파일에 구성할 수 있습니다. 구성한 각 링크는 `storage:link` 명령어 실행 시 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령어를 사용하여 구성된 심볼릭 링크를 제거할 수도 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하려면 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

`config/filesystems.php` 파일에 S3 디스크 설정 배열이 포함되어 있습니다. 일반적으로 `config/filesystems.php`가 참조하는 다음 환경 변수를 통해 S3 정보와 자격 증명을 설정합니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수들은 AWS CLI에서 사용하는 명명 규칙과 일치하여 편리합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer를 통해 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem FTP 통합은 매우 잘 작동하지만, 기본 `config/filesystems.php` 파일에 샘플 설정은 포함되어 있지 않습니다. FTP 파일시스템을 설정해야 할 경우, 아래 설정 예를 참고하세요:

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

SFTP 드라이버를 사용하려면 Composer를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem SFTP 통합도 매우 잘 작동하지만, 기본 설정 파일에 샘플 설정은 포함되어 있지 않습니다. SFTP 파일시스템을 설정하려면 다음 예제를 참고하세요:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // 암호화 비밀번호가 있는 SSH 키 기반 인증 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일/디렉토리 권한 설정...
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
### 스코프 및 읽기 전용 파일시스템

스코프 디스크는 모든 경로가 자동으로 지정한 경로 접두사로 시작하도록 정의할 수 있습니다. 스코프 파일시스템 디스크를 생성하기 전에 Composer를 통해 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일시스템 디스크를 스코프 처리하려면 `scoped` 드라이버를 사용하는 디스크를 정의하면 됩니다. 예를 들어, 기존의 `s3` 디스크를 특정 경로 접두사로 제한하는 디스크를 생성할 수 있습니다. 그러면 이 스코프 디스크를 사용하는 모든 파일 작업은 지정된 접두사를 사용합니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 만들 수 있습니다. `read-only` 옵션을 사용하기 전에 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그런 다음 디스크 설정 배열에 `read-only` 옵션을 추가할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로, 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 설정이 포함되어 있습니다. 이 디스크는 [Amazon S3](https://aws.amazon.com/s3/) 작업뿐만 아니라 [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/)와 같은 S3 호환 스토리지 서비스와도 연동에 사용할 수 있습니다.

일반적으로, 디스크 자격 증명을 사용하려는 서비스에 맞게 업데이트한 후에는 `endpoint` 설정 옵션만 변경하면 됩니다. 이 옵션은 보통 `AWS_ENDPOINT` 환경 변수로 정의됩니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하도록 하려면, 애플리케이션의 로컬 URL과 버킷 이름이 URL 경로에 포함되도록 `AWS_URL` 환경 변수를 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> `temporaryUrl` 메서드를 이용한 임시 저장 URL 생성은 클라이언트가 `endpoint`에 접근할 수 없으면 MinIO 사용 시 제대로 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 가져오기

`Storage` 파사드를 사용하여 구성한 모든 디스크와 상호 작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하려면 `put` 메서드를 사용할 수 있습니다. 먼저 `disk` 메서드를 호출하지 않고 `Storage` 파사드에 직접 메서드를 호출하면 기본 디스크에 자동으로 전달됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션이 여러 디스크를 다룰 경우, `Storage` 파사드의 `disk` 메서드를 사용하여 특정 디스크의 파일을 다룰 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

때로는 `filesystems` 설정 파일에 실제로 존재하지 않는 설정을 이용해 런타임에 디스크를 생성하고 싶을 수 있습니다. 이럴 때는 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달할 수 있습니다:

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

`get` 메서드는 파일 내용을 가져오는 데 쓰입니다. 이 메서드는 파일의 원본 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

만약 가져오는 파일이 JSON일 경우, `json` 메서드를 이용해 파일을 디코드하여 바로 가져올 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 디스크에 파일이 존재하는지 확인할 때 사용합니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 디스크에 없는지 확인할 때 사용합니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정한 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인수로 다운로드 시 사용자에게 보일 파일명을 지정할 수 있고, 세 번째 인수로는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드는 주어진 파일에 대한 URL을 생성합니다. `local` 드라이버를 사용하는 경우, 보통 `/storage`가 경로 앞에 붙고 상대 URL을 반환합니다. `s3` 드라이버를 사용할 땐 완전한 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 사용 시, 공개 접근이 필요한 모든 파일은 `storage/app/public`에 위치해야 하며, [심볼릭 링크](#the-public-disk)로 `public/storage`가 이 디렉터리를 가리키도록 해야 합니다.

> [!WARNING]
> `local` 드라이버에서 `url` 메서드의 반환값은 URL 인코딩되지 않습니다. 따라서 URL이 올바른 형식이 되도록 파일명을 설정하는 것을 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드를 통해 생성되는 URL의 호스트를 변경하고 싶다면, 디스크 설정 배열에 `url` 옵션을 추가하거나 변경할 수 있습니다:

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

`temporaryUrl` 메서드를 사용하면 `local` 및 `s3` 드라이버를 사용하는 파일에 대해 만료 시간이 있는 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

`local` 드라이버에서 임시 URL 지원이 도입되기 전에 개발을 시작했다면, 로컬 임시 URL을 활성화해야 할 수 있습니다. 이를 위해 `config/filesystems.php`에서 `local` 디스크 설정에 `serve` 옵션을 추가하세요:

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

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, `temporaryUrl` 메서드의 세 번째 인수로 요청 파라미터 배열을 전달할 수 있습니다:

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

특정 스토리지 디스크의 임시 URL 생성 방식을 커스터마이징해야 할 경우 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 기본적으로 임시 URL을 지원하지 않는 디스크를 사용하지만, 컨트롤러에서 해당 파일 다운로드를 허용하고 싶을 때 유용합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
> 임시 업로드 URL 생성 기능은 `s3` 드라이버만 지원합니다.

클라이언트 애플리케이션에서 직접 파일을 업로드할 수 있도록 임시 URL을 생성해야 할 경우, `temporaryUploadUrl` 메서드를 사용하세요. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받습니다. 반환값은 업로드 URL과 업로드 요청에 포함할 헤더를 포함한 연관 배열이며, 구조 분해 할당이 가능합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 기능은 클라우드 저장소(Amazon S3 등)에 클라이언트 측에서 직접 업로드할 때 주로 사용됩니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일 읽기 및 쓰기 외에 Laravel은 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일 크기를 바이트 단위로 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 변경된 시점을 UNIX 타임스탬프로 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

`mimeType` 메서드를 사용하면 특정 파일의 MIME 타입을 얻을 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 통해 특정 파일의 절대 경로를 가져올 수 있습니다. `local` 드라이버 사용 시는 절대 경로를, `s3` 드라이버 사용 시는 S3 버킷 내 상대 경로를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 디스크에 파일 내용을 저장할 때 사용합니다. PHP `resource`를 넘겨줄 수도 있는데, 이 경우 Flysystem의 스트림 지원이 활용됩니다. 모든 파일 경로는 디스크의 "root" 위치에 대해 상대 경로로 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 쓰기 실패

`put` 메서드(또는 다른 쓰기 작업)가 디스크에 파일을 쓸 수 없으면 `false`를 반환합니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 쓸 수 없습니다...
}
```

원한다면 파일시스템 디스크 설정 배열에 `throw` 옵션을 `true`로 설정할 수 있습니다. 이 경우 `put` 같은 쓰기 메서드가 실패하면 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞뒤에 내용 추가

`prepend` 및 `append` 메서드를 사용하여 파일의 앞이나 뒤에 내용을 추가할 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 새로운 위치에 복사하고, `move` 메서드는 기존 파일의 이름을 변경하거나 다른 위치로 이동할 때 사용합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장할 때 메모리 사용을 크게 줄이려면 스트리밍 방식이 유리합니다. `putFile` 혹은 `putFileAs` 메서드를 이용하면 Laravel이 자동으로 파일을 스트리밍하여 저장합니다. 이 메서드들은 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 인수로 받습니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 고유 ID를 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 직접 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드에 디렉터리 이름만 지정한 이유는, 기본적으로 고유 ID를 생성해 파일명으로 사용하기 때문입니다. 파일 확장자는 파일의 MIME 타입을 확인해 결정됩니다. `putFile` 메서드는 저장된 파일 경로(생성된 파일명 포함)를 반환하므로, 데이터베이스 등에 저장해 둘 수 있습니다.

`putFile`과 `putFileAs` 메서드는 저장 시 "visibility" (가시성) 설정을 위한 인수도 받습니다. 예를 들어 클라우드 디스크(S3 등)에 파일을 공개용으로 저장하고 싶을 때 사용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서는 사용자 업로드 파일(사진, 문서 등)을 저장하는 것이 흔한 작업입니다. Laravel은 업로드된 파일 인스턴스의 `store` 메서드를 통해 손쉽게 저장할 수 있게 합니다. `store` 메서드에 저장할 경로를 지정하세요:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자의 아바타를 업데이트합니다.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

중요한 점은 디렉터리 이름만 지정했고, 파일명은 지정하지 않았다는 것입니다. 기본적으로 `store` 메서드는 고유 ID를 파일명으로 생성하며, 파일 확장자는 MIME 타입 분석으로 결정합니다. 반환되는 경로에는 생성된 파일명이 포함되므로 필요시 데이터베이스에 저장할 수 있습니다.

위 예제처럼 `Storage` 파사드의 `putFile` 메서드를 사용해 동일 작업을 수행할 수도 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정하기

자동 생성된 파일명이 아닌 원하는 파일명을 지정하려면, `storeAs` 메서드를 사용하세요. 이 메서드는 경로, 파일명, (선택적) 디스크명을 인수로 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs` 메서드로 동일 작업을 할 수도 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 출력 불가능한 문자와 유효하지 않은 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 파일 경로를 Laravel 파일 저장 메서드에 전달하기 전에 별도로 정리하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

업로드된 파일의 `store` 메서드는 기본적으로 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 `store` 메서드에 두 번째 인수로 디스크 이름을 전달하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드는 세 번째 인수로 디스크 이름을 받을 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드된 파일의 기타 정보

업로드된 파일의 원본 이름과 확장자를 가져오려면 `getClientOriginalName` 및 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 악의적인 사용자가 변경할 수 있으므로 안전하지 않은 것으로 간주됩니다. 따라서 보통은 `hashName`과 `extension` 메서드로 파일명과 확장자를 가져오는 것을 권장합니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 무작위 이름 생성...
$extension = $file->extension(); // MIME 타입에 기반한 확장자 결정...
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel Flysystem 통합에서 "가시성(visibility)"은 여러 플랫폼의 파일 권한을 추상화한 것입니다. 파일은 `public` 또는 `private`으로 선언할 수 있고, `public` 파일은 보통 더 넓게 접근할 수 있게 됩니다. 예를 들면 S3 드라이버에서 `public` 파일은 URL을 받아 접근할 수 있습니다.

`put` 메서드에서 파일을 쓸 때 가시성을 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일도 `getVisibility`와 `setVisibility` 메서드로 가시성을 조회하거나 변경할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일과 상호작용할 때는 `storePublicly`와 `storePubliclyAs` 메서드로 공개 가시성을 지정해 저장할 수 있습니다:

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

`local` 드라이버에서 `public` 가시성은 디렉터리에 대해 `0755` 권한, 파일에 대해 `0644` 권한으로 매핑됩니다. 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 조정할 수 있습니다:

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

`delete` 메서드는 삭제할 단일 파일명 또는 파일명 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요시, 삭제할 디스크를 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 특정 디렉토리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉토리 내 모든 파일 배열을 반환합니다. 하위 디렉토리를 포함해 모든 파일을 가져오려면 `allFiles` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 특정 디렉토리 내 모든 서브디렉토리 가져오기

`directories` 메서드는 지정한 디렉토리 내 모든 하위 디렉토리 배열을 반환합니다. `allDirectories` 메서드를 사용하면 하위 디렉토리까지 모두 포함된 목록을 가져올 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 지정한 디렉토리와 필요한 모든 하위 디렉토리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

`deleteDirectory` 메서드는 디렉토리와 그 안의 모든 파일을 삭제합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 임시 디스크를 쉽게 생성합니다. 이 기능은 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합하여 파일 업로드 테스트를 크게 단순화합니다. 예를 들어:

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

    // 하나 이상의 파일이 저장됐는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 하나 이상의 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉토리 파일 개수가 기대값과 일치하는지 확인...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 특정 디렉토리가 비어있는지 확인...
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

        // 하나 이상의 파일이 저장됐는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 하나 이상의 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉토리 파일 개수가 기대값과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉토리가 비어있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉토리 내 모든 파일을 삭제합니다. 파일을 유지하려면 대신 `persistentFake` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 관한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 관련 부분](/docs/master/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)을 필요로 합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 기본적으로 여러 "드라이버"를 지원하지만, Flysystem은 이 밖에도 다양한 저장 시스템에 대한 어댑터를 제공합니다. 추가 어댑터를 사용하려면 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어 커뮤니티 유지 관리되는 Dropbox 어댑터를 프로젝트에 추가해봅시다:

```shell
composer require spatie/flysystem-dropbox
```

다음으로, 애플리케이션의 [서비스 프로바이더](/docs/master/providers) 중 하나의 `boot` 메서드에서 이 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 두 번째 인수는 `$app`과 `$config` 변수를 인수로 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config` 변수는 `config/filesystems.php`에 정의된 지정 디스크의 설정 값을 포함합니다.

확장 서비스 프로바이더를 생성 및 등록한 뒤에는 `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.