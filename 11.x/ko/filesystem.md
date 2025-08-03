# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 선행 조건](#driver-prerequisites)
    - [범위 지정 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 가져오기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장하기](#storing-files)
    - [파일에 앞/뒤로 내용 추가하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 Frank de Jonge가 만든 멋진 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem)을 활용해 강력한 파일시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 같은 다양한 드라이버에 대해 간단한 드라이버를 제공합니다. 더욱 좋은 점은, 각 시스템별 API가 동일하므로 로컬 개발 환경과 운영 서버 간에 저장 방식 전환이 매우 간단하다는 것입니다.

<a name="configuration"></a>
## 설정 (Configuration)

Laravel의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 저장 드라이버와 저장 위치를 나타냅니다. 설정 파일에는 지원되는 드라이버별 예제 설정이 포함되어 있으므로, 이를 참고하여 저장 선호도와 자격 증명에 맞게 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버의 로컬 파일에 접근하며, `s3` 드라이버는 Amazon S3 클라우드 저장소에 쓰는 데 사용됩니다.

> [!NOTE]  
> 원하시는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 구성할 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버 (The Local Driver)

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉토리를 기준으로 합니다. 기본값은 `storage/app/private` 디렉토리로 설정되어 있습니다. 따라서 다음 코드는 `storage/app/private/example.txt` 파일에 쓸 것입니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크 (The Public Disk)

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 웹에서 공개적으로 접근 가능한 파일용으로 설계되었습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public`에 저장합니다.

만약 `public` 디스크가 `local` 드라이버를 사용할 때, 이 파일들을 웹에서 접근 가능하게 하려면 `storage/app/public` 디렉토리에서 `public/storage`로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크는 `storage:link` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan storage:link
```

파일 저장 후 심볼릭 링크가 생성되면, `asset` 헬퍼를 이용해 파일 URL을 만들 수 있습니다:

```
echo asset('storage/file.txt');
```

`filesystems` 설정 파일에서 추가적인 심볼릭 링크를 정의할 수도 있으며, `storage:link` 명령어 실행 시 이 링크들도 생성됩니다:

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

심볼릭 링크를 제거하고 싶다면 `storage:unlink` 명령어를 사용하세요:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 선행 조건 (Driver Prerequisites)

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정 (S3 Driver Configuration)

S3 드라이버를 사용하기 전에, Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php`에 위치합니다. 보통은 아래 환경 변수들에 자격 증명을 설정하며, 설정 파일에서 이 변수를 참조합니다:

```
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이들 환경 변수는 AWS CLI와 동일한 명명 규칙을 사용해 일관성을 유지합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정 (FTP Driver Configuration)

FTP 드라이버 사용 전, Composer로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel Flysystem은 FTP와 잘 동작하지만, 기본 `config/filesystems.php`에는 예제 설정이 포함되어 있지 않습니다. FTP 파일시스템을 설정하려면 다음 예시를 참고하세요:

```
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
#### SFTP 드라이버 설정 (SFTP Driver Configuration)

SFTP 드라이버를 사용하기 전에, Composer로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

SFTP 또한 Laravel Flysystem과 잘 통합되지만, 기본 `config/filesystems.php`에는 예제 설정이 없습니다. 아래 예시를 참고해 설정할 수 있습니다:

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 인증 및 암호 설정...
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
### 범위 지정 및 읽기 전용 파일시스템 (Scoped and Read-Only Filesystems)

범위 지정된(Scoped) 디스크는 모든 경로가 자동으로 특정 경로 접두어와 합쳐지는 파일시스템을 정의할 수 있게 합니다. 범위 지정 디스크를 만들기 전에, Composer를 통해 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일시스템 디스크 중 하나를 범위 지정하려면 `scoped` 드라이버를 사용하는 디스크를 정의하세요. 예를 들어, 기존 `s3` 디스크에 특정 경로 접두어를 지정하는 디스크는 다음과 같습니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

읽기 전용(read-only) 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 정의합니다. 사용 전, Composer를 통해 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그 다음, 디스크 설정 배열에 `read-only` 옵션을 포함시킬 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템 (Amazon S3 Compatible Filesystems)

기본적으로 애플리케이션의 `filesystems` 설정 파일에 `s3` 디스크 구성이 포함되어 있습니다. 이를 통해 [Amazon S3](https://aws.amazon.com/s3/) 뿐만 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/)와 같은 S3 호환 서비스도 사용할 수 있습니다.

대부분 경우, 해당 서비스의 자격 증명으로 디스크 구성 정보를 업데이트한 뒤, `endpoint` 설정 값만 서비스 주소에 맞도록 바꾸면 됩니다. 보통 이 값은 `AWS_ENDPOINT` 환경 변수로 정의됩니다:

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

Laravel Flysystem 통합이 MinIO를 사용할 때 올바른 URL을 생성하기 위해서는, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과, 버킷 이름이 포함된 경로로 설정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]  
> MinIO 사용 시, 클라이언트가 `endpoint`에 접근할 수 없다면 `temporaryUrl` 메서드를 통한 임시 저장 URL 생성이 작동하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 가져오기 (Obtaining Disk Instances)

`Storage` 파사드를 사용하면 구성된 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하려면 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 호출하지 않고 `Storage`에 직접 메서드를 호출하면 기본 디스크로 자동 전달됩니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션에서 여러 디스크를 다루는 경우, `Storage`의 `disk` 메서드를 사용해 특정 디스크의 파일에 접근하세요:

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크 (On-Demand Disks)

실행 시점에 애플리케이션 `filesystems` 설정 파일에 없는 설정으로 디스크를 만들고자 할 때 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 가져오기 (Retrieving Files)

`get` 메서드를 사용하면 파일 내용을 가져올 수 있습니다. 이 메서드는 파일의 원시 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```
$contents = Storage::get('file.jpg');
```

파일이 JSON 데이터를 포함한다면 `json` 메서드를 사용해 파일을 읽고 내용을 디코드할 수 있습니다:

```
$orders = Storage::json('orders.json');
```

`exists` 메서드로 디스크에 파일이 존재하는지 확인할 수 있습니다:

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 없는지 확인합니다:

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드 (Downloading Files)

`download` 메서드는 주어진 경로의 파일을 사용자 브라우저가 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인수로는 다운로드 시 보이는 파일명을 지정할 수 있고, 세 번째 인수로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL (File URLs)

`url` 메서드를 이용하면 특정 파일의 URL을 가져올 수 있습니다. `local` 드라이버 사용 시, 보통 `/storage`를 경로 앞에 붙여 상대적인 파일 URL을 반환합니다. `s3` 드라이버 사용 시에는 완전한 원격 URL이 반환됩니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 쓸 때, 공개적으로 접근 가능한 모든 파일은 `storage/app/public` 디렉토리에 위치해야 하며, [심볼릭 링크](#the-public-disk)로 `public/storage`에 연결되어야 합니다.

> [!WARNING]  
> `local` 드라이버 사용 시 `url` 메서드 반환값은 URL 인코딩이 되어 있지 않습니다. 따라서 항상 유효한 URL이 될 수 있도록 파일명(경로)을 저장할 때 주의하세요.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징 (URL Host Customization)

`Storage` 파사드를 통해 생성되는 URL의 호스트를 수정하려면, 디스크 설정 배열에 `url` 옵션을 추가하거나 변경하세요:

```
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a name="temporary-urls"></a>
### 임시 URL (Temporary URLs)

`temporaryUrl` 메서드를 사용하면 `local` 및 `s3` 드라이버로 저장된 파일에 대해 만료 시간이 설정된 임시 URL을 생성할 수 있습니다. 경로 및 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받습니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 사용 활성화 (Enabling Local Temporary URLs)

`local` 드라이버에 임시 URL 지원이 추가되기 전에 개발을 시작했다면, 임시 URL을 활성화하려면 `config/filesystems.php` 내 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
#### S3 요청 파라미터 (S3 Request Parameters)

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 넘겨야 할 경우, `temporaryUrl` 메서드의 세 번째 인수로 배열을 전달할 수 있습니다:

```
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
#### 임시 URL 커스터마이징 (Customizing Temporary URLs)

특정 저장 디스크의 임시 URL 생성 방식을 커스터마이징하려면 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 일반적으로 지원하지 않는 디스크의 파일 다운로드 컨트롤러를 만들 때 유용합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
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
#### 임시 업로드 URL (Temporary Upload URLs)

> [!WARNING]  
> 임시 업로드 URL 생성 기능은 `s3` 드라이버만 지원합니다.

클라이언트 애플리케이션이 파일을 직접 클라우드 저장소에 업로드할 수 있도록 임시 업로드 URL을 생성하려면, `temporaryUploadUrl` 메서드를 사용하세요. 경로와 만료 시간을 인수로 받으며, URL과 업로드 요청에 포함할 헤더 배열을 포함한 연관 배열을 반환합니다:

```
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 기능은 서버리스 환경에서 Amazon S3 같은 클라우드 스토리에 클라이언트가 직접 파일을 업로드해야 하는 경우에 매우 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터 (File Metadata)

읽기 및 쓰기 외에도, Laravel은 파일 자체에 대한 정보 제공도 지원합니다. 예를 들어, `size` 메서드는 파일의 바이트 단위 크기를 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 마지막 수정 시점의 UNIX 타임스탬프를 반환합니다:

```
$time = Storage::lastModified('file.jpg');
```

`mimeType` 메서드는 파일의 MIME 타입을 얻을 수 있습니다:

```
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로 (File Paths)

`path` 메서드로 파일 경로를 얻을 수 있습니다. `local` 드라이버 사용 시 절대 경로가 반환되며, `s3` 드라이버 사용 시 버킷 내 상대 경로가 반환됩니다:

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장하기 (Storing Files)

`put` 메서드는 디스크에 파일 내용을 저장할 때 사용합니다. PHP `resource`를 전달할 수도 있으며, 이 경우 Flysystem이 내부적으로 스트림 지원을 활용합니다. 모든 경로는 디스크에 설정된 "root" 위치를 기준으로 지정합니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 실패한 쓰기 (Failed Writes)

`put` 등 쓰기 작업이 실패하면 `false`가 반환됩니다:

```
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 쓸 수 없었습니다...
}
```

원한다면, 파일시스템 디스크 설정 배열에 `throw` 옵션을 `true`로 정의할 수 있습니다. 이 경우 `put` 같은 쓰기 메서드가 실패하면 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

```
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일에 앞/뒤로 내용 추가하기 (Prepending and Appending To Files)

`prepend` 와 `append` 메서드는 각각 파일의 시작 부분과 끝 부분에 내용을 덧붙일 때 사용합니다:

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동 (Copying and Moving Files)

`copy` 메서드는 기존 파일을 디스크 내 새 위치로 복사하고, `move` 메서드는 파일 이름 변경 또는 파일을 새 위치로 이동할 때 사용합니다:

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍 (Automatic Streaming)

파일을 저장소로 스트리밍하면 메모리 사용량이 크게 줄어듭니다. 지정한 파일을 자동으로 스트리밍하려면 `putFile` 또는 `putFileAs` 메서드를 사용하세요. `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 인수로 받아 파일을 스트리밍으로 저장합니다:

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 자동으로 고유 ID를 파일명으로 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 수동 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드를 사용할 때 주의할 점이 몇 가지 있습니다. 파일명을 지정하지 않고 디렉토리만 넘겼기 때문에 기본적으로 고유 ID가 파일명으로 자동 생성됩니다. 파일 확장자는 파일 MIME 타입을 검사하여 결정됩니다. 반환값은 저장된 파일 경로로, 여기에 생성된 파일명까지 포함해 데이터베이스에 저장할 수 있습니다.

또한, `putFile`과 `putFileAs`는 저장 파일의 "가시성"을 지정하는 인수를 받을 수 있습니다. Amazon S3와 같은 클라우드 디스크에서 공개 URL로 접근 가능하게 만들 때 유용합니다:

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드 (File Uploads)

웹 애플리케이션에서 가장 일반적인 파일 저장 사례 중 하나는 사용자가 업로드한 사진이나 문서 저장입니다. Laravel은 업로드된 파일 인스턴스의 `store` 메서드를 통해 이를 매우 쉽게 처리할 수 있습니다. 업로드 파일을 저장하고자 하는 경로를 인수로 전달하세요:

```
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

예시에서 주목할 점은 디렉토리 명만 지정했고 파일명은 지정하지 않았다는 것입니다. `store` 메서드는 기본적으로 고유 ID를 파일명으로 생성하며, 확장자는 파일 MIME 타입으로 판단됩니다. 반환값인 저장 경로 및 파일명은 데이터베이스에 저장할 수 있습니다.

또한, `Storage` 파사드의 `putFile` 메서드로 동일한 동작을 할 수도 있습니다:

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정하기 (Specifying a File Name)

자동 파일명이 아닌 직접 지정하려면, 경로, 파일명, (옵션) 디스크를 인수로 받는 `storeAs` 메서드를 사용합니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs` 메서드로도 동일한 작업을 할 수 있습니다:

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]  
> 인쇄 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동 삭제됩니다. 따라서 Laravel 파일 저장 메서드에 넘기기 전에 경로를 반드시 정제(sanitize)하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기 (Specifying a Disk)

기본적으로 파일 업로드의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 두 번째 인수로 디스크 이름을 전달하세요:

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드는 세 번째 인수로 디스크 이름을 받습니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보 (Other Uploaded File Information)

업로드한 원본 이름과 확장자를 얻으려면 `getClientOriginalName` 및 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 악의적인 사용자에 의해 조작될 가능성이 있어 안전하지 않습니다. 보통은 `hashName`과 `extension` 메서드를 통해 고유한 이름과 MIME 타입 기반 확장자를 얻는 것이 더 안전합니다:

```
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 무작위 이름 생성
$extension = $file->extension(); // 파일 MIME 타입에 기반한 확장자 판별
```

<a name="file-visibility"></a>
### 파일 가시성 (File Visibility)

Laravel의 Flysystem 통합에서 "가시성"은 다양한 플랫폼 간 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private` 중 하나로 선언할 수 있습니다. `public`으로 선언하면 일반적으로 타인이 접근할 수 있음을 의미합니다. 예를 들어, S3 드라이버에서는 `public` 파일의 URL을 얻을 수 있습니다.

파일 작성 시 `put` 메서드의 세 번째 인수로 가시성을 설정할 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility`와 `setVisibility` 메서드를 통해 가져오거나 수정할 수 있습니다:

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일을 다룰 때는 `storePublicly`와 `storePubliclyAs` 메서드를 사용해 `public` 가시성으로 저장할 수 있습니다:

```
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 가시성 (Local Files and Visibility)

`local` 드라이버 사용 시, `public` 가시성은 디렉토리에 `0755` 권한, 파일에 `0644` 권한으로 매핑됩니다. 권한 매핑은 애플리케이션 `filesystems` 설정 파일에서 수정 가능합니다:

```
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
## 파일 삭제 (Deleting Files)

`delete` 메서드는 하나 또는 여러 파일명을 배열로 받아 파일을 삭제합니다:

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하면 삭제할 파일이 있는 디스크를 지정할 수도 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리 (Directories)

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉토리 내 모든 파일의 배열을 반환합니다. 하위 디렉토리까지 모든 파일을 가져오려면 `allFiles` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 가져오기

`directories` 메서드는 지정한 디렉토리 내 모든 디렉토리의 배열을 반환합니다. 하위 디렉토리까지 모든 디렉토리를 가져오려면 `allDirectories` 메서드를 사용하세요:

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성하기

`makeDirectory` 메서드는 지정한 디렉토리를 생성하며, 필요한 하위 디렉토리까지 함께 만듭니다:

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제하기

`deleteDirectory` 메서드는 디렉토리와 그 안의 모든 파일을 삭제합니다:

```
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트 (Testing)

`Storage` 파사드의 `fake` 메서드는 임시 디스크를 쉽게 생성해 주며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합하여 파일 업로드 테스트를 크게 간소화합니다. 예:

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

    // 파일들이 저장되었는지 단언...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 저장되지 않은 파일 단언...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 지정 디렉토리 내 파일 개수가 예상과 일치하는지 단언...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 지정 디렉토리가 비어있는지 단언...
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

        // 파일들이 저장되었는지 단언...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 저장되지 않은 파일 단언...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 지정 디렉토리 내 파일 개수가 예상과 일치하는지 단언...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 지정 디렉토리가 비어있는지 단언...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉토리에 저장된 모든 파일을 삭제합니다. 파일을 유지하려면 `persistentFake` 메서드를 사용하세요. 파일 업로드 테스트 관련 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 항목](/docs/11.x/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]  
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템 (Custom Filesystems)

Laravel의 Flysystem 통합은 여러 "드라이버"를 기본 지원하지만, Flysystem은 훨씬 다양한 저장소 어댑터를 지원합니다. 따라서 추가 어댑터를 Laravel에 사용하고 싶다면, 커스텀 드라이버를 생성할 수 있습니다.

커스텀 파일시스템 정의를 위해서는 Flysystem 어댑터가 필요합니다. 예를 들어, 스포티(Spatie)가 유지 관리하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다:

```shell
composer require spatie/flysystem-dropbox
```

다음으로 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드에서 `Storage` 파사드의 `extend` 메서드를 사용해 드라이버를 등록합니다:

```
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

`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 두 번째는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config` 변수는 `config/filesystems.php`에서 해당 디스크에 관한 설정값을 포함합니다.

확장 서비스 프로바이더를 생성하고 등록한 후에는, `config/filesystems.php`에서 `dropbox` 드라이버를 사용할 수 있습니다.