# 파일 스토리지

- [소개](#introduction)
- [구성](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일에 내용 앞뒤로 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개 범위](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지 덕분에 강력한 파일시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 작업할 수 있는 간단한 드라이버를 제공합니다. 더욱 좋은 점은 각 시스템의 API가 동일하게 유지되므로, 로컬 개발 환경과 프로덕션 서버 간의 스토리지 옵션 전환이 매우 쉽다는 것입니다.

<a name="configuration"></a>
## 구성

Laravel의 파일시스템 구성 파일은 `config/filesystems.php`에 위치합니다. 이 파일 안에서 모든 파일시스템 "디스크"를 구성할 수 있습니다. 각각의 디스크는 특정 스토리지 드라이버와 스토리지 위치를 나타냅니다. 각 드라이버별로 예제 구성도 포함되어 있으므로, 자신의 스토리지 선호도와 자격 증명에 맞게 설정을 수정하면 됩니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버에 저장된 파일과 상호작용하고, `s3` 드라이버는 Amazon S3 클라우드 스토리지 서비스에 기록할 때 사용합니다.

> [!NOTE]
> 원하는 만큼 많은 디스크를 구성할 수 있으며, 같은 드라이버를 사용하는 여러 디스크도 생성할 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 구성 파일에서 정의한 `root` 디렉토리를 기준으로 상대적으로 동작합니다. 기본적으로 이 값은 `storage/app/private` 디렉토리로 설정되어 있습니다. 따라서 아래 메서드는 `storage/app/private/example.txt`에 기록하게 됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 구성 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일용입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public` 디렉토리에 저장합니다.

만약 퍼블릭 디스크가 `local` 드라이버를 사용하고 있고, 이 파일들을 웹에서 접근 가능하게 만들고 싶다면, 소스 디렉토리 `storage/app/public`에서 대상 디렉토리 `public/storage`로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크를 생성하려면 `storage:link` 아티즌 명령어를 사용합니다.

```shell
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 만들어지면, `asset` 헬퍼를 사용해 파일의 URL을 생성할 수 있습니다.

```php
echo asset('storage/file.txt');
```

추가 심볼릭 링크는 `filesystems` 구성 파일에서 설정할 수 있습니다. 설정된 각 링크는 `storage:link` 명령을 실행할 때 생성됩니다.

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령은 설정된 심볼릭 링크들을 해제할 때 사용할 수 있습니다.

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 구성

S3 드라이버를 사용하기 전에 Composer 패키지 관리자를 통해 Flysystem S3 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 구성 배열은 `config/filesystems.php` 에 있습니다. 일반적으로 아래 환경변수를 통해 S3 정보와 자격증명을 설정하며, 이는 `config/filesystems.php` 파일에서 참조됩니다.

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

편의를 위해 이 환경변수들은 AWS CLI와 동일한 네이밍 규칙을 따릅니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 구성

FTP 드라이버를 사용하기 전에 Composer 패키지 관리자를 통해 Flysystem FTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와도 잘 작동합니다. 하지만, 프레임워크의 기본 `config/filesystems.php` 에는 샘플 구성이 포함되어 있지 않습니다. FTP 파일시스템을 구성하려면 아래 예제 구성을 사용할 수 있습니다.

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
#### SFTP 드라이버 구성

SFTP 드라이버를 사용하기 전에 Composer 패키지 관리자를 통해 Flysystem SFTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 작동합니다. 하지만, 프레임워크의 기본 `config/filesystems.php` 에는 샘플 구성이 포함되어 있지 않습니다. SFTP 파일시스템을 구성하려면 아래 예제 구성을 사용할 수 있습니다.

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // 암호화 비밀번호를 사용하는 SSH 키 기반 인증 설정
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일/디렉토리 권한 설정
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // 선택적 SFTP 설정
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

스코프 디스크를 활용하면 모든 경로가 지정한 경로 접두사로 자동으로 시작되는 파일시스템을 정의할 수 있습니다. 스코프 파일시스템 디스크를 생성하기 전에 Composer 패키지 관리자를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 활용하여 기존 파일시스템 디스크의 경로 스코프 인스턴스를 만들 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 스코프하여, 이후 스코프 디스크를 사용하는 모든 파일 작업에서 해당 접두사를 활용합니다.

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

읽기 전용("read-only") 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 만듭니다. `read-only` 옵션을 사용하려면 Composer 패키지 관리자를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

그 다음, 디스크 구성 배열 내에 `read-only` 옵션을 포함할 수 있습니다.

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로, 애플리케이션의 `filesystems` 구성 파일에는 `s3` 디스크에 대한 구성 예제가 있습니다. 이 디스크를 [Amazon S3](https://aws.amazon.com/s3/) 뿐만 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/)와 같은 S3 호환 파일 저장소 서비스와 상호작용하는 데도 사용할 수 있습니다.

보통 사용할 서비스의 자격 증명으로 디스크 설정을 변경한 후, `endpoint` 구성 옵션의 값을 업데이트하기만 하면 됩니다. 이 값은 일반적으로 `AWS_ENDPOINT` 환경 변수로 정의합니다.

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO 사용 시 Laravel의 Flysystem 통합이 올바른 URL을 생성하려면, 애플리케이션의 로컬 URL과 버킷 이름을 포함하여 `AWS_URL` 환경 변수를 정의해야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> 클라이언트가 `endpoint`에 접근할 수 없다면 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성이 MinIO에서 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드를 사용하여 구성된 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 사용해 기본 디스크에 아바타를 저장할 수 있습니다. `Storage` 파사드에서 `disk` 메서드를 먼저 호출하지 않고 직접 메서드를 호출하면, 해당 메서드는 자동으로 기본 디스크에 전달됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션이 여러 디스크를 사용할 경우, `Storage` 파사드의 `disk` 메서드를 통해 특정 디스크에 파일 작업을 할 수 있습니다.

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

애플리케이션의 `filesystems` 구성 파일에 정의되어 있지 않은 설정으로 런타임에 디스크를 생성하려는 경우, `Storage` 파사드의 `build` 메서드에 구성 배열을 전달할 수 있습니다.

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

`get` 메서드를 사용해 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 원시 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 상대 경로로 지정해야 합니다.

```php
$contents = Storage::get('file.jpg');
```

가져오는 파일이 JSON인 경우, `json` 메서드를 사용해 파일을 가져오고 그 내용을 디코드할 수 있습니다.

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 디스크에 파일이 존재하는지 확인하는 데 사용할 수 있습니다.

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 디스크에 파일이 없는지 확인하는 데 사용할 수 있습니다.

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자의 브라우저가 다운로드하도록 응답을 생성합니다. 두 번째 인수로 파일명을 지정하면, 다운로드 받을 때 보이는 파일명이 결정됩니다. 마지막으로 HTTP 헤더 배열을 세 번째 인수로 전달할 수 있습니다.

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용해 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용하면, 대개 이 메서드는 `/storage`를 경로 앞에 붙여 반환하며, 상대 URL을 반환합니다. `s3` 드라이버를 사용할 경우, 완전한 원격 URL이 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 사용 시, 공개적으로 접근 가능한 모든 파일은 `storage/app/public`에 있어야 합니다. 또한 [`public/storage`에 심볼릭 링크를 만들어야](#the-public-disk) 합니다.

> [!WARNING]
> `local` 드라이버 사용 시, `url`의 반환값은 URL 인코딩되지 않습니다. 따라서 파일명을 항상 valid URL이 될 수 있게 지정하는 것을 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드를 통해 생성되는 URL의 호스트를 수정하고 싶다면, 디스크 구성 배열의 `url` 옵션을 추가 및 변경할 수 있습니다.

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

`temporaryUrl` 메서드를 이용해 `local`과 `s3` 드라이버로 저장된 파일에 대한 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 만료 시간을 지정하는 `DateTime` 인스턴스를 입력받습니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

임시 URL 지원이 도입되기 전에 개발을 시작한 프로젝트라면, 로컬 임시 URL을 직접 활성화해야 할 수도 있습니다. `config/filesystems.php` 구성 파일의 `local` 디스크 배열에 `serve` 옵션을 추가하세요.

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

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, `temporaryUrl` 메서드의 세 번째 인수로 파라미터 배열을 전달할 수 있습니다.

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

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이징하려면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크로 저장된 파일을 다운로드할 수 있도록 컨트롤러를 사용하는 경우에 유용합니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드에서 호출되어야 합니다.

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

클라이언트 사이드 애플리케이션에서 파일을 직접 업로드하기 위한 임시 URL이 필요하다면, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 만료 시간을 입력받으며, 업로드 URL과 업로드 요청에 포함해야 할 헤더로 구성된 연관 배열을 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 메서드는 주로 서버리스 환경에서 클라이언트 사이드 애플리케이션이 Amazon S3와 같은 클라우드 스토리지에 직접 파일을 업로드해야 하는 경우에 사용됩니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 외에도, Laravel은 파일 자체에 대한 정보도 제공할 수 있습니다. 예를 들어, `size` 메서드는 파일의 크기를 바이트 단위로 가져옵니다.

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 UNIX 타임스탬프를 반환합니다.

```php
$time = Storage::lastModified('file.jpg');
```

`mimeType` 메서드로 지정한 파일의 MIME 타입을 확인할 수 있습니다.

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용해 단일 파일의 경로를 가져올 수 있습니다. `local` 드라이버를 사용하는 경우 파일의 절대 경로를 반환하며, `s3` 드라이버의 경우 S3 버킷 내의 상대 경로를 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드를 사용해 디스크에 파일 내용을 저장할 수 있습니다. 또한, PHP `resource`를 `put` 메서드에 전달하면 Flysystem의 스트림 기능을 사용하게 됩니다. 모든 파일 경로는 디스크별로 설정한 "root" 위치를 기준으로 지정해야 합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 쓰기 실패

`put` 메서드(혹은 다른 "쓰기" 작업)로 파일 저장에 실패하면, `false`가 반환됩니다.

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일이 저장되지 않았습니다...
}
```

원한다면, 파일시스템 디스크 구성 배열에 `throw` 옵션을 지정할 수 있습니다. 이 옵션을 `true`로 설정하면, `put` 같은 "쓰기" 메서드 실패 시 `League\Flysystem\UnableToWriteFile` 예외가 발생합니다.

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일에 내용 앞뒤로 추가

`prepend`와 `append` 메서드를 사용해 파일 앞 또는 뒤에 데이터를 쓸 수 있습니다.

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 새로운 위치로 복사하고, `move` 메서드는 기존 파일을 새 위치로 이름을 바꾸거나 이동할 때 사용합니다.

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 스토리지에 스트리밍하면 메모리 사용량이 크게 줄어듭니다. Laravel이 자동으로 파일 스트리밍을 관리하게 하려면 `putFile` 또는 `putFileAs` 메서드를 사용하세요. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 자동으로 파일을 원하는 위치에 스트리밍합니다.

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 고유 ID 자동 생성
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 지정한 파일명으로 저장
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드는 디렉토리명만 지정하면 파일명은 고유 ID로 자동 생성됩니다. 파일의 확장자는 MIME 타입을 검사하여 결정됩니다. 반환값으로 전체 파일 경로(생성된 파일명 포함)를 돌려줘서 데이터베이스에 저장할 수 있습니다.

`putFile`과 `putFileAs` 메서드는 저장할 파일의 "공개 범위(visibility)"도 인수로 받을 수 있습니다. Amazon S3 등 클라우드 디스크에 파일을 공개적으로 저장하고 URL로 접근하도록 하고 싶다면 이 기능이 유용합니다.

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 가장 흔한 파일 저장 예시는 사용자가 업로드하는 사진이나 문서 등의 파일 저장입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 사용해 손쉽게 업로드 파일을 저장할 수 있습니다. 파일을 저장할 경로를 인수로 넘깁니다.

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

이 예시에서 볼 수 있듯이, 디렉토리명만 지정하면 파일명은 자동으로 고유 ID로 생성됩니다. 파일의 확장자는 MIME 타입을 검사하여 결정됩니다. 경로(파일명 포함)는 반환값으로 전달되어 데이터베이스에 저장할 수 있습니다.

위와 동일하게 `Storage` 파사드의 `putFile` 메서드를 활용해서도 같은 작업을 할 수 있습니다.

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정

파일명을 자동으로 할당받고 싶지 않은 경우, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, (선택) 디스크명을 인수로 받습니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

마찬가지로 `Storage` 파사드의 `putFileAs`를 사용할 수 있습니다.

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 출력 불가(unprintable) 또는 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 파일 경로를 Laravel 파일 저장 메서드에 전달하기 전에 직접 정제(sanitize)할 필요가 있습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath`로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

업로드 파일의 `store` 메서드는 기본적으로 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 두 번째 인수로 디스크명을 전달합니다.

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용할 땐 세 번째 인수로 디스크명을 전달하세요.

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드된 파일 정보

업로드된 파일의 원래 이름과 확장자를 가져오려면 `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용하세요.

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만, 이 메서드들은 사용자가 악의적으로 변경할 수 있으므로 안전하지 않습니다. 보다 안전하게 이름과 확장자를 얻으려면 `hashName`과 `extension` 메서드를 권장합니다.

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 랜덤한 이름 생성
$extension = $file->extension(); // MIME 타입에 따라 파일 확장자 결정
```

<a name="file-visibility"></a>
### 파일 공개 범위(Visibility)

Laravel의 Flysystem 통합에서 "visibility(공개 범위)"는 여러 플랫폼에 걸친 파일 권한의 추상화 개념입니다. 파일은 `public` 또는 `private`로 선언할 수 있습니다. `public`로 선언하면 파일이 보통 다른 이들에게 접근 가능하다는 뜻입니다. 예를 들어, S3 드라이버를 사용할 경우, `public` 파일의 URL을 받아올 수 있습니다.

파일을 쓸 때 `put` 메서드를 통해 공개 범위를 설정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 공개 범위는 `getVisibility`, `setVisibility` 메서드로 얻거나 변경할 수 있습니다.

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일과 상호작용할 때, `storePublicly`와 `storePubliclyAs` 메서드를 사용해 `public` 공개 범위로 업로드할 수 있습니다.

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 공개 범위

`local` 드라이버를 사용할 때, `public` [공개 범위](#file-visibility)는 디렉토리에는 `0755`, 파일에는 `0644` 권한을 의미합니다. 이 권한 매핑은 애플리케이션의 `filesystems` 구성 파일에서 수정할 수 있습니다.

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

`delete` 메서드는 단일 파일명 또는 파일명의 배열을 인수로 받아 파일을 삭제합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면 파일을 삭제할 디스크도 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 특정 디렉토리 내 모든 파일의 배열을 반환합니다. 하위 디렉토리까지 포함해 모든 파일 목록을 가져오려면 `allFiles` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 가져오기

`directories` 메서드는 특정 디렉토리 내의 모든 디렉토리의 배열을 반환합니다. `allDirectories` 메서드를 통해 하위 디렉토리까지 전체 목록을 가져올 수 있습니다.

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 필요하다면 하위 디렉토리까지 포함하여 지정한 디렉토리를 생성합니다.

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

마지막으로, `deleteDirectory` 메서드를 사용해 디렉토리와 그 안의 모든 파일을 제거할 수 있습니다.

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 쉽게 임시 디스크를 생성할 수 있도록 해줍니다. 이는 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합해 파일 업로드 테스트를 매우 단순화합니다. 예:

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

    // 파일이 저장되었는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉토리의 파일 개수가 예상과 일치하는지 확인...
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

        // 파일이 저장되었는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉토리의 파일 개수가 예상과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉토리가 비어있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로, `fake` 메서드는 임시 디렉토리 내의 모든 파일을 삭제합니다. 파일을 유지하고 싶다면 "persistentFake" 메서드를 사용하세요. 파일 업로드 테스트에 대해 더 알고 싶다면 [HTTP 테스트 문서의 파일 업로드 관련 내용](/docs/{{version}}/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 익스텐션](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 여러 "드라이버"를 기본으로 지원합니다. 하지만 Flysystem 자체는 더 많은 스토리지 시스템용 어댑터가 있습니다. 이들 어댑터 중 하나를 Laravel 애플리케이션에서 사용하고 싶을 경우 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 아래와 같이 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가합니다.

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나의 `boot` 메서드 내에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용하세요.

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름이고, 두 번째 인수는 `$app`과 `$config` 변수를 받는 클로저입니다. 이 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 지정한 디스크의 `config/filesystems.php` 구성 값이 들어 있습니다.

확장 서비스 프로바이더를 생성 및 등록한 후에는, `config/filesystems.php`에서 `dropbox` 드라이버를 자유롭게 사용할 수 있습니다.