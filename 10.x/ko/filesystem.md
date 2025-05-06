# 파일 스토리지

- [소개](#introduction)
- [구성](#configuration)
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
    - [파일에 데이터 추가 및 선행하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개 범위(가시성)](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합 기능으로 로컬 파일 시스템, SFTP, Amazon S3와 쉽게 작업할 수 있는 드라이버가 제공됩니다. 더 나아가, 각 시스템에 대해 API가 동일하게 유지되기 때문에 로컬 개발 환경과 프로덕션 서버 간에 이러한 스토리지 옵션을 간편하게 전환할 수 있습니다.

<a name="configuration"></a>
## 구성

Laravel의 파일 시스템 구성 파일은 `config/filesystems.php`에 위치합니다. 이 파일 내에서 모든 파일 시스템 “디스크”를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 나타냅니다. 지원되는 각 드라이버에 대한 예시 설정이 포함되어 있으므로, 필요한 환경에 맞게 파일을 수정하여 사용할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버에 저장된 파일과 상호작용하며, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스에 파일을 기록하는 데 사용됩니다.

> [!NOTE]  
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 개의 디스크도 설정할 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 구성 파일에 정의된 `root` 디렉터리를 기준으로 상대적으로 동작합니다. 기본값은 `storage/app` 디렉터리로 설정되어 있습니다. 따라서, 다음 코드는 `storage/app/example.txt` 파일에 저장합니다.

    use Illuminate\Support\Facades\Storage;

    Storage::disk('local')->put('example.txt', 'Contents');

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 구성 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 위해 사용됩니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public`에 저장합니다.

이 파일들을 웹에서 접근 가능하게 하려면, `public/storage`에서 `storage/app/public`으로의 심볼릭 링크를 생성해야 합니다. 이 폴더 구조를 사용하면 무정지 배포 시스템(예: [Envoyer](https://envoyer.io))으로 배포 시 공개 파일을 한 디렉터리에서 쉽게 관리할 수 있습니다.

심볼릭 링크를 생성하려면 `storage:link` 아티즌(Artisan) 명령어를 사용하세요:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 후, `asset` 헬퍼를 사용하여 파일의 URL을 만들 수 있습니다:

    echo asset('storage/file.txt');

또한, 추가 심볼릭 링크 경로를 `filesystems` 구성 파일에 설정할 수 있습니다. 모든 링크는 `storage:link` 명령 실행 시 생성됩니다:

    'links' => [
        public_path('storage') => storage_path('app/public'),
        public_path('images') => storage_path('app/images'),
    ],

`storage:unlink` 명령어로 설정된 심볼릭 링크를 삭제할 수 있습니다:

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

S3 드라이버의 설정 정보는 `config/filesystems.php` 파일에 있습니다. S3 드라이버에 대한 예시 배열이 포함되어 있으므로, 자신의 S3 정보와 자격증명으로 수정해서 사용하시면 됩니다. 편의를 위해 이 환경 변수들은 AWS CLI에서 사용하는 네이밍 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer 패키지 매니저로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와도 잘 작동합니다. 하지만, 기본 `filesystems.php` 파일에는 샘플 설정이 포함되어 있지 않습니다. FTP 파일 시스템을 설정하려면 아래 예시 설정을 사용하세요:

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

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer 패키지 매니저로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 작동합니다. 하지만, 기본 `filesystems.php` 파일에는 샘플 설정이 포함되어 있지 않습니다. SFTP 파일 시스템을 설정하려면 아래 예시 설정을 사용하세요:

    'sftp' => [
        'driver' => 'sftp',
        'host' => env('SFTP_HOST'),

        // 기본 인증 설정...
        'username' => env('SFTP_USERNAME'),
        'password' => env('SFTP_PASSWORD'),

        // 암호화 비밀번호를 이용한 SSH 키 기반 인증 설정...
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

<a name="scoped-and-read-only-filesystems"></a>
### 스코프 및 읽기 전용 파일 시스템

스코프 디스크를 이용하면 모든 경로를 지정된 경로 프리픽스(접두어)로 자동으로 시작하는 파일 시스템을 정의할 수 있습니다. 스코프 파일 시스템 디스크를 만들려면 Composer로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 사용하는 디스크를 정의하여 기존 파일 시스템 디스크의 경로 스코프 인스턴스를 만들 수 있습니다. 예를 들어, 기존 `s3` 디스크에 특정 경로 프리픽스를 두고, 스코프 디스크를 통해 모든 파일 작업 시 프리픽스를 자동으로 적용할 수 있습니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크로는 파일의 쓰기 작업을 제한할 수 있습니다. `read-only` 설정 옵션을 사용하려면, Composer로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

이후, 디스크 설정 배열에 `read-only` 옵션을 추가하면 됩니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 구성이 포함되어 있습니다. Amazon S3와의 연동뿐 아니라 [MinIO](https://github.com/minio/minio)나 [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/)와 같은 S3 호환 파일 스토리지 서비스와도 연동할 수 있습니다.

대체로 사용하려는 서비스에 맞추어 디스크의 인증 정보를 변경한 뒤 `endpoint` 설정 값만 바꿔주면 됩니다. 이 값은 주로 `AWS_ENDPOINT` 환경 변수를 통해 정의합니다:

    'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),

<a name="minio"></a>
#### MinIO

MinIO를 사용할 때 Laravel의 Flysystem 연동이 올바른 URL을 생성하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷명을 포함한 경로로 지정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]  
> MinIO를 사용할 경우, `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성이 지원되지 않습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드를 사용하여 구성된 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 통해 기본 디스크에 아바타 이미지를 저장할 수 있습니다. `Storage` 파사드에서 `disk` 메서드를 호출하지 않으면 기본 디스크로 작업이 전달됩니다:

    use Illuminate\Support\Facades\Storage;

    Storage::put('avatars/1', $content);

여러 디스크를 사용하는 경우, `Storage` 파사드의 `disk` 메서드를 이용해 특정 디스크에 파일을 저장할 수 있습니다:

    Storage::disk('s3')->put('avatars/1', $content);

<a name="on-demand-disks"></a>
### 온디맨드 디스크

간혹 애플리케이션의 `filesystems` 설정 파일에 등록하지 않은 특정 설정으로 런타임에 디스크를 생성해야 할 수 있습니다. 이 때, 설정 배열을 `Storage` 파사드의 `build` 메서드에 전달하여 바로 디스크 인스턴스를 만들 수 있습니다:

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

`get` 메서드를 사용해 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 원시 문자열 데이터를 반환합니다. 모든 파일 경로는 디스크의 “root” 위치를 기준으로 상대적으로 지정해야 합니다:

    $contents = Storage::get('file.jpg');

파일이 JSON 형식이라면, `json` 메서드를 사용하여 파일을 가져오고 내용을 디코드할 수 있습니다:

    $orders = Storage::json('orders.json');

`exists` 메서드는 디스크에 파일이 존재하는지 확인합니다:

    if (Storage::disk('s3')->exists('file.jpg')) {
        // ...
    }

`missing` 메서드는 디스크에서 파일이 없는지 확인할 수 있습니다:

    if (Storage::disk('s3')->missing('file.jpg')) {
        // ...
    }

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저에서 해당 경로에 있는 파일을 강제로 다운로드하도록 응답을 생성합니다. 이 메서드는 두 번째 인수로 파일 이름을 받아 사용자가 파일을 다운로드할 때 보여지는 이름을 지정할 수 있습니다. 마지막 인수로 HTTP 헤더의 배열도 전달할 수 있습니다:

    return Storage::download('file.jpg');

    return Storage::download('file.jpg', $name, $headers);

<a name="file-urls"></a>
### 파일 URL

특정 파일에 대한 URL을 가져오려면 `url` 메서드를 사용할 수 있습니다. `local` 드라이버를 사용하는 경우, `/storage`를 앞에 붙여 상대 URL을 반환합니다. `s3` 드라이버의 경우, 완전히 자격이 부여된 원격 URL이 반환됩니다:

    use Illuminate\Support\Facades\Storage;

    $url = Storage::url('file.jpg');

`local` 드라이버를 사용할 때, 공개 파일은 반드시 `storage/app/public` 디렉터리에 저장되어야 합니다. 또한, [심볼릭 링크를 생성](#the-public-disk)하여 `public/storage`가 `storage/app/public`을 가리키도록 해야 합니다.

> [!WARNING]  
> `local` 드라이버의 경우, `url` 반환 값은 URL 인코딩되지 않습니다. 따라서, 항상 유효한 URL을 생성할 수 있는 파일명을 사용하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드를 사용해 생성되는 URL의 호스트를 미리 지정하려면 디스크 구성 배열에 `url` 옵션을 추가할 수 있습니다:

    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
    ],

<a name="temporary-urls"></a>
### 임시 URL

`s3` 드라이버로 저장된 파일에 대해 `temporaryUrl` 메서드를 사용해 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL의 만료 시점을 지정하는 `DateTime` 인스턴스를 받습니다:

    use Illuminate\Support\Facades\Storage;

    $url = Storage::temporaryUrl(
        'file.jpg', now()->addMinutes(5)
    );

[S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, 세 번째 인수로 파라미터 배열을 지정할 수 있습니다:

    $url = Storage::temporaryUrl(
        'file.jpg',
        now()->addMinutes(5),
        [
            'ResponseContentType' => 'application/octet-stream',
            'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
        ]
    );

특정 디스크에서 임시 URL 생성 방식을 커스터마이징 하려면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 기본적으로 지원하지 않는 디스크로 저장된 파일을 다운로드하는 컨트롤러가 있다면 유용합니다. 대개 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

    <?php

    namespace App\Providers;

    use DateTime;
    use Illuminate\Support\Facades\Storage;
    use Illuminate\Support\Facades\URL;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
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

<a name="temporary-upload-urls"></a>
#### 임시 업로드 URL

> [!WARNING]  
> 임시 업로드 URL 생성 기능은 `s3` 드라이버에서만 지원됩니다.

클라이언트 측 애플리케이션에서 직접 파일을 업로드할 수 있는 임시 URL을 생성하려면, `temporaryUploadUrl` 메서드를 사용하세요. 이 메서드는 경로와 만료 시점을 받으며, 업로드 URL과 업로드 요청 시 포함되어야 할 헤더가 들어있는 연관 배열을 반환합니다:

    use Illuminate\Support\Facades\Storage;

    ['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
        'file.jpg', now()->addMinutes(5)
    );

이 기능은 Amazon S3 등 클라우드 스토리지 시스템에 클라이언트에서 직접 업로드해야 하는 서버리스 환경에서 유용하게 사용할 수 있습니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 외에도, Laravel은 파일 자체에 대한 정보를 제공합니다. 예를 들어, `size` 메서드로 파일 크기(바이트 단위)를 가져올 수 있습니다:

    use Illuminate\Support\Facades\Storage;

    $size = Storage::size('file.jpg');

`lastModified` 메서드는 파일이 마지막 수정된 시간의 UNIX 타임스탬프를 반환합니다:

    $time = Storage::lastModified('file.jpg');

지정된 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

    $mime = Storage::mimeType('file.jpg');

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드로 해당 파일의 경로를 얻을 수 있습니다. `local` 드라이버 사용 시 파일의 절대 경로를, `s3` 드라이버 사용 시 S3 버킷 내 상대 경로를 반환합니다:

    use Illuminate\Support\Facades\Storage;

    $path = Storage::path('file.jpg');

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 디스크상에 파일 내용을 저장하는 데 사용합니다. 또한, PHP `resource`를 `put` 메서드에 넘기면 Flysystem의 스트림 기능을 사용할 수 있습니다. 모든 파일 경로는 디스크의 “root” 위치 기준으로 상대적으로 지정해야 합니다:

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents);

    Storage::put('file.jpg', $resource);

<a name="failed-writes"></a>
#### 저장 실패 처리

`put`(또는 다른 “쓰기” 연산) 메서드가 파일을 디스크에 쓰지 못할 경우 `false`를 반환합니다:

    if (! Storage::put('file.jpg', $contents)) {
        // 파일을 저장할 수 없습니다...
    }

원한다면, 파일 시스템 디스크의 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 설정되면, `put` 등 “쓰기” 메서드가 실패 시 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

    'public' => [
        'driver' => 'local',
        // ...
        'throw' => true,
    ],

<a name="prepending-appending-to-files"></a>
### 파일에 데이터 추가 및 선행하기

`prepend`와 `append` 메서드를 사용하여 파일 앞 또는 뒤에 데이터를 작성할 수 있습니다:

    Storage::prepend('file.log', 'Prepended Text');

    Storage::append('file.log', 'Appended Text');

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 새 위치로 복사하며, `move` 메서드는 기존 파일을 새 위치로 이름 변경 또는 이동합니다:

    Storage::copy('old/file.jpg', 'new/file.jpg');

    Storage::move('old/file.jpg', 'new/file.jpg');

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장소로 스트림 전송하면 메모리 사용을 크게 절약할 수 있습니다. Laravel이 자동으로 파일을 지정된 저장 위치로 스트리밍하도록 하려면, `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 파일을 자동으로 원하는 위치로 스트림합니다:

    use Illuminate\Http\File;
    use Illuminate\Support\Facades\Storage;

    // 파일 이름을 고유하게 생성...
    $path = Storage::putFile('photos', new File('/path/to/photo'));

    // 파일 이름을 명시적으로 지정...
    $path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');

`putFile` 메서드는 디렉터리 이름만 명시하고 파일 이름은 저장 시 자동으로 고유 ID를 생성합니다. 파일 확장자는 MIME 타입을 통해 결정되며, 저장된 전체 경로(`파일명 포함`)가 반환됩니다. 

`putFile`, `putFileAs` 메서드는 저장 파일의 “가시성”을 지정하는 인수도 받을 수 있습니다. Amazon S3와 같이 파일을 공개적으로 접근시켜야 할 때 유용합니다:

    Storage::putFile('photos', new File('/path/to/photo'), 'public');

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션의 일반적인 파일 저장 사례는 사용자 업로드(사진, 문서 등)입니다. Laravel은 `store` 메서드로 업로드 파일을 아주 쉽게 저장할 수 있게 해줍니다. 저장할 경로를 지정해 `store` 메서드를 호출하세요:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserAvatarController extends Controller
    {
        /**
         * 사용자 아바타 업데이트
         */
        public function update(Request $request): string
        {
            $path = $request->file('avatar')->store('avatars');

            return $path;
        }
    }

이 예시에서 디렉터리명만 지정하고 파일명은 따로 지정하지 않았습니다. `store` 메서드는 기본적으로 파일명에 고유 식별자를 생성하며, 파일 확장자는 MIME 타입에 따라 결정됩니다. 반환된 경로(파일명 포함)는 데이터베이스 등에 저장해둘 수 있습니다.

동일한 작업을 `Storage` 파사드의 `putFile`로도 할 수 있습니다:

    $path = Storage::putFile('avatars', $request->file('avatar'));

<a name="specifying-a-file-name"></a>
#### 파일 이름 지정

저장 시 파일 이름이 자동 지정되는 것을 원하지 않을 경우, `storeAs` 메서드를 사용하세요. `storeAs`는 경로, 파일명, (선택) 디스크명을 받습니다:

    $path = $request->file('avatar')->storeAs(
        'avatars', $request->user()->id
    );

`Storage` 파사드의 `putFileAs`로도 동일한 작업을 할 수 있습니다:

    $path = Storage::putFileAs(
        'avatars', $request->file('avatar'), $request->user()->id
    );

> [!WARNING]  
> 인쇄 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서, Laravel 파일 저장 메서드에 전달하기 전 파일 경로를 정제(정상화)하시는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath`로 표준화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 업로드 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크에 저장하려면 두 번째 인수로 디스크명을 전달하세요:

    $path = $request->file('avatar')->store(
        'avatars/'.$request->user()->id, 's3'
    );

`storeAs` 메서드를 사용하는 경우, 세 번째 인수로 디스크명을 넘길 수 있습니다:

    $path = $request->file('avatar')->storeAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보

업로드한 파일의 원본 이름과 확장자를 얻으려면 `getClientOriginalName`, `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

    $file = $request->file('avatar');

    $name = $file->getClientOriginalName();
    $extension = $file->getClientOriginalExtension();

단, 이 두 메서드는 파일명과 확장자를 악의적으로 변경할 수 있으므로 안전하지 않습니다. 보안상 `hashName`과 `extension` 메서드로 무작위 이름 및 MIME 타입 기반 확장자를 얻는 것이 더 안전합니다:

    $file = $request->file('avatar');

    $name = $file->hashName(); // 고유 무작위 이름 생성...
    $extension = $file->extension(); // MIME 타입 기반 확장자 확인...

<a name="file-visibility"></a>
### 파일 공개 범위(가시성)

Laravel Flysystem 통합에서 “가시성”(visibility)은 여러 플랫폼에서의 파일 권한을 추상화한 기능입니다. 파일은 `public` 또는 `private`로 선언될 수 있습니다. `public`로 선언 시, 파일이 타인에 의해 접근 가능함을 의미하며, S3 드라이버와 함께 사용할 때 `public` 파일의 URL을 얻을 수 있습니다.

파일 작성 시 `put` 메서드에서 가시성을 지정할 수 있습니다:

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents, 'public');

저장된 파일의 가시성도 `getVisibility`, `setVisibility` 메서드로 확인/설정할 수 있습니다:

    $visibility = Storage::getVisibility('file.jpg');

    Storage::setVisibility('file.jpg', 'public');

업로드 파일을 공개로 저장하려면 `storePublicly`, `storePubliclyAs` 메서드도 사용할 수 있습니다:

    $path = $request->file('avatar')->storePublicly('avatars', 's3');

    $path = $request->file('avatar')->storePubliclyAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 공개 범위(가시성)

`local` 드라이버 기준, `public` [가시성](#file-visibility)은 디렉터리에 `0755`, 파일에 `0644` 권한을 부여합니다. 이 매핑은 `filesystems` 설정 파일에서 변경할 수 있습니다:

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
    ],

<a name="deleting-files"></a>
## 파일 삭제

`delete` 메서드는 단일 파일명 또는 파일명 배열을 받아 파일을 삭제합니다:

    use Illuminate\Support\Facades\Storage;

    Storage::delete('file.jpg');

    Storage::delete(['file.jpg', 'file2.jpg']);

필요하다면 삭제할 파일이 있는 디스크도 지정할 수 있습니다:

    use Illuminate\Support\Facades\Storage;

    Storage::disk('s3')->delete('path/file.jpg');

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 지정된 디렉터리의 모든 파일 배열을 반환합니다. 하위 디렉터리까지 포함한 전체 파일 목록을 원한다면 `allFiles` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Storage;

    $files = Storage::files($directory);

    $files = Storage::allFiles($directory);

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 디렉터리 가져오기

`directories` 메서드는 지정된 디렉터리 내의 모든 디렉터리 배열을 반환합니다. 하위 디렉터리까지 모두 포함한 디렉터리 목록은 `allDirectories` 메서드를 사용하세요:

    $directories = Storage::directories($directory);

    $directories = Storage::allDirectories($directory);

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 필요한 하위 디렉터리를 포함해 지정된 디렉터리를 생성합니다:

    Storage::makeDirectory($directory);

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

마지막으로, `deleteDirectory` 메서드는 디렉터리 및 그 안 모든 파일을 삭제합니다:

    Storage::deleteDirectory($directory);

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 가짜 디스크를 쉽게 생성할 수 있게 해주며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 함께 파일 업로드 테스트를 매우 단순화합니다. 예시:

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

            // 한 개 이상 파일이 저장되었는지 검증...
            Storage::disk('photos')->assertExists('photo1.jpg');
            Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

            // 한 개 이상 파일이 저장되지 않았는지 검증...
            Storage::disk('photos')->assertMissing('missing.jpg');
            Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

            // 지정 디렉터리가 비어있는지 검증...
            Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
        }
    }

기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 파일을 보존하려면 `persistentFake` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대해 더 자세하게 알고 싶다면 [HTTP 테스트 문서의 파일 업로드 문서](/docs/{{version}}/http-tests#testing-file-uploads)를 참고하세요.

> [!WARNING]  
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)을 필요로 합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템

Laravel의 Flysystem 통합은 여러 “드라이버”를 기본적으로 지원하지만, Flysystem은 여기에 제한되지 않고 다양한 저장소 어댑터를 지원합니다. 이 추가 어댑터를 Laravel에서 사용하려면 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예시로, 커뮤니티에서 관리하는 Dropbox 어댑터를 설치해보겠습니다:

```shell
composer require spatie/flysystem-dropbox
```

그 다음, [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 드라이버를 등록하세요. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

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
         * 애플리케이션 서비스 등록
         */
        public function register(): void
        {
            // ...
        }

        /**
         * 애플리케이션 서비스 부트스트랩
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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이고, 두 번째 인자는 `$app`과 `$config`를 받는 클로저입니다. 이 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 지정한 디스크의 `config/filesystems.php` 값이 들어있습니다.

확장 서비스 프로바이더를 만들고 등록한 후, `config/filesystems.php` 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.