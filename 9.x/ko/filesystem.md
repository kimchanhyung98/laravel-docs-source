# 파일 저장소

- [소개](#introduction)
- [구성](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞뒤에 내용 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개/비공개 설정](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 작업할 수 있는 간단한 드라이버를 제공하며, API가 각 시스템마다 동일하여 로컬 개발 환경과 운영 서버 간에 파일 저장 방식을 간단하게 전환할 수 있습니다.

<a name="configuration"></a>
## 구성

Laravel의 파일시스템 구성 파일은 `config/filesystems.php`에 있습니다. 이 파일에서 모든 파일시스템 "디스크"를 구성할 수 있습니다. 각 디스크는 특정 저장 드라이버와 저장 위치를 나타내며, 구성 파일에는 각 지원 드라이버에 대한 예시 구성이 포함되어 있으므로 환경 및 자격 증명에 맞게 수정하면 됩니다.

`local` 드라이버는 Laravel이 실행 중인 서버의 로컬 파일을 제어하며, `s3` 드라이버는 Amazon S3 클라우드 저장소 서비스를 사용합니다.

> **참고**
> 원하는 만큼 디스크를 구성할 수 있으며, 동일한 드라이버를 여러 디스크에 사용할 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때 모든 파일 관련 작업은 `filesystems` 구성 파일에 정의된 `root` 디렉토리를 기준으로 상대 경로를 가집니다. 기본적으로 이 값은 `storage/app` 디렉토리로 설정됩니다. 따라서 아래 코드는 `storage/app/example.txt` 파일을 생성합니다.

    use Illuminate\Support\Facades\Storage;

    Storage::disk('local')->put('example.txt', 'Contents');

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 구성 파일에 포함된 `public` 디스크는 외부에 공개할 파일을 저장하기 위해 사용됩니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 `storage/app/public`에 파일을 저장합니다.

웹에서 해당 파일에 접근하려면, `public/storage`에서 `storage/app/public`으로의 심볼릭 링크를 생성해야 합니다. 이 폴더 구조를 활용하면, [Envoyer](https://envoyer.io)와 같이 무중단 배포 시스템에서 공개 파일을 쉽게 공유할 수 있습니다.

심볼릭 링크를 생성하려면 다음의 Artisan 명령어를 사용합니다:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 후, `asset` 헬퍼를 이용해 파일에 대한 URL을 만들 수 있습니다:

    echo asset('storage/file.txt');

`filesystems` 구성 파일 내에 추가적으로 심볼릭 링크를 지정할 수 있습니다. 설정된 모든 링크는 `storage:link` 명령 실행 시 생성됩니다:

    'links' => [
        public_path('storage') => storage_path('app/public'),
        public_path('images') => storage_path('app/images'),
    ],

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0"
```

S3 드라이버 관련 설정 정보는 `config/filesystems.php` 내에 있으며, 예시 설정 배열을 자유롭게 자신의 S3 정보 및 자격증명에 맞게 수정할 수 있습니다. 편의를 위해 AWS CLI와 동일한 환경 변수 네이밍 규칙을 사용합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer를 통해 Flysystem FTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 연동되지만, 기본 `filesystems.php` 구성 파일에는 예시가 포함되어 있지 않습니다. FTP를 설정하려면 아래 예시를 참고하여 구성하면 됩니다:

    'ftp' => [
        'driver' => 'ftp',
        'host' => env('FTP_HOST'),
        'username' => env('FTP_USERNAME'),
        'password' => env('FTP_PASSWORD'),

        // FTP의 선택적 설정...
        // 'port' => env('FTP_PORT', 21),
        // 'root' => env('FTP_ROOT'),
        // 'passive' => true,
        // 'ssl' => true,
        // 'timeout' => 30,
    ],

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 연동되지만, 기본 `filesystems.php` 구성 파일에는 예시가 포함되어 있지 않습니다. SFTP를 설정하려면 아래 예시를 참고하세요:

    'sftp' => [
        'driver' => 'sftp',
        'host' => env('SFTP_HOST'),

        // 기본 인증 정보
        'username' => env('SFTP_USERNAME'),
        'password' => env('SFTP_PASSWORD'),

        // 암호화된 SSH 키를 사용하는 인증 정보
        'privateKey' => env('SFTP_PRIVATE_KEY'),
        'passphrase' => env('SFTP_PASSPHRASE'),

        // SFTP의 선택적 설정...
        // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
        // 'maxTries' => 4,
        // 'passphrase' => env('SFTP_PASSPHRASE'),
        // 'port' => env('SFTP_PORT', 22),
        // 'root' => env('SFTP_ROOT', ''),
        // 'timeout' => 30,
        // 'useAgent' => true,
    ],

<a name="scoped-and-read-only-filesystems"></a>
### 스코프 및 읽기 전용 파일시스템

스코프 디스크를 이용하면 모든 경로에 자동으로 지정한 경로 프리픽스가 붙는 파일시스템을 정의할 수 있습니다. 스코프 파일시스템 디스크를 만들기 전에 Composer로 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 사용하여 기존 파일시스템 디스크의 경로에 프리픽스를 설정한 디스크를 만들 수 있습니다. 아래는 기존 `s3` 디스크를 특정 경로 프리픽스로 스코프하는 예시입니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크를 사용하면, 쓰기 작업이 불가능한 파일시스템 디스크를 만들 수 있습니다. `read-only` 설정을 사용하려면 Composer로 추가 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

그런 다음 디스크 설정 배열에 `read-only` 옵션을 추가하세요:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로 애플리케이션의 `filesystems` 구성 파일에는 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크를 사용해 Amazon S3와 상호작용할 수 있을 뿐만 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) 등 S3 호환 파일 저장 서비스를 사용할 수 있습니다.

일반적으로 해당 서비스의 자격증명에 맞춰 디스크의 설정 정보를 업데이트한 다음, `endpoint` 설정값을 변경하면 됩니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수로 지정합니다:

    'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),

<a name="minio"></a>
#### MinIO

MinIO 사용 시, Laravel의 Flysystem 통합이 적절한 URL을 생성할 수 있도록 아래와 같이 `AWS_URL` 환경 변수 값을 앱의 로컬 URL과 버킷명이 포함된 경로로 설정해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> **경고**  
> MinIO를 사용할 때 `temporaryUrl` 메서드를 통한 임시 저장소 URL 생성은 지원되지 않습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드는 구성된 모든 디스크와 상호작용할 수 있습니다. 예를 들어 `put` 메서드로 기본 디스크에 아바타를 저장할 수 있습니다. `disk` 메서드를 사용하지 않고 바로 `Storage` 파사드의 메서드를 호출하면, 기본 디스크에 해당 메서드가 전달됩니다.

    use Illuminate\Support\Facades\Storage;

    Storage::put('avatars/1', $content);

여러 디스크와 상호작용해야 한다면, `disk` 메서드로 특정 디스크를 지정할 수 있습니다:

    Storage::disk('s3')->put('avatars/1', $content);

<a name="on-demand-disks"></a>
### 온디맨드 디스크

실행 중에 임시로 직접 생성한 설정값으로 디스크를 만들고 싶을 때가 있습니다. `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하여 이를 실현할 수 있습니다:

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

`get` 메서드를 사용하여 파일의 내용을 가져올 수 있습니다. 파일의 원시 문자열 내용이 반환되며, 모든 파일 경로는 디스크의 "root" 위치를 기준으로 상대경로로 지정해야 합니다.

    $contents = Storage::get('file.jpg');

`exists` 메서드는 디스크에 파일이 존재하는지 확인할 때 사용합니다:

    if (Storage::disk('s3')->exists('file.jpg')) {
        // ...
    }

`missing` 메서드는 디스크에 파일이 없는지 확인할 때 사용합니다:

    if (Storage::disk('s3')->missing('file.jpg')) {
        // ...
    }

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 브라우저에서 지정한 경로의 파일을 바로 다운로드하도록 응답을 생성합니다. 두 번째 인자로 사용자에게 보일 파일명을, 세 번째 인자로 HTTP 헤더 배열을 전달할 수 있습니다:

    return Storage::download('file.jpg');

    return Storage::download('file.jpg', $name, $headers);

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 이용해 저장된 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용하는 경우 `/storage`가 앞에 붙은 상대 URL이 반환되며, `s3` 드라이버를 쓸 경우 완전한 원격 URL이 반환됩니다:

    use Illuminate\Support\Facades\Storage;

    $url = Storage::url('file.jpg');

`local` 드라이버 사용 시 공개적으로 접근 가능한 모든 파일은 반드시 `storage/app/public` 디렉토리에 있어야 합니다. 또한, [심볼릭 링크](#the-public-disk)를 `public/storage`에 만들어야 합니다.

> **경고**  
> `local` 드라이버에서 반환되는 `url` 값은 URL 인코딩되지 않습니다. 따라서 항상 유효한 URL을 만들 수 있는 파일명을 사용하는 것을 권장합니다.

<a name="temporary-urls"></a>
#### 임시 URL

`temporaryUrl` 메서드를 통해 `s3` 드라이버로 저장된 파일에 임시로 접근할 수 있는 URL을 생성할 수 있습니다. 이 메서드는 파일 경로와 만료 시각(`DateTime` 인스턴스)을 받습니다:

    use Illuminate\Support\Facades\Storage;

    $url = Storage::temporaryUrl(
        'file.jpg', now()->addMinutes(5)
    );

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정하고 싶다면, 세 번째 인수로 요청 파라미터 배열을 전달할 수 있습니다:

    $url = Storage::temporaryUrl(
        'file.jpg',
        now()->addMinutes(5),
        [
            'ResponseContentType' => 'application/octet-stream',
            'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
        ]
    );

특정 디스크에 대해 임시 URL 생성 방식을 커스터마이징 하고 싶다면 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 일반적으로 이 코드는 서비스 프로바이더의 `boot` 메서드 내에서 호출해야 합니다.

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Storage;
    use Illuminate\Support\Facades\URL;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            Storage::disk('local')->buildTemporaryUrlsUsing(function ($path, $expiration, $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            });
        }
    }

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드로 생성된 URL의 호스트를 미리 지정하고 싶다면, 디스크 구성 배열에 `url` 옵션을 추가하세요:

    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
    ],

<a name="file-metadata"></a>
### 파일 메타데이터

Laravel은 파일 읽기/쓰기 외에도 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일 크기(바이트)를 반환합니다:

    use Illuminate\Support\Facades\Storage;

    $size = Storage::size('file.jpg');

`lastModified` 메서드는 파일이 마지막으로 수정된 UNIX 타임스탬프를 반환합니다:

    $time = Storage::lastModified('file.jpg');

지정한 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

    $mime = Storage::mimeType('file.jpg')

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드는 파일의 경로를 반환합니다. `local` 드라이버 사용 시 절대 경로가 반환되고, `s3` 드라이버면 S3 버킷 내의 상대 경로가 반환됩니다:

    use Illuminate\Support\Facades\Storage;

    $path = Storage::path('file.jpg');

<a name="storing-files"></a>
## 파일 저장

`put` 메서드를 사용하여 파일 내용을 디스크에 저장할 수 있습니다. PHP `resource`도 지원하여 Flysystem의 스트림 기능도 사용할 수 있습니다. 모든 경로는 반드시 디스크의 "root" 위치를 기준으로 상대적인 경로여야 합니다:

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents);

    Storage::put('file.jpg', $resource);

<a name="failed-writes"></a>
#### 저장 실패 시

`put`(또는 기타 쓰기 연산) 메서드가 파일을 저장할 수 없으면, `false`가 반환됩니다:

    if (! Storage::put('file.jpg', $contents)) {
        // 파일 저장에 실패했을 때...
    }

원한다면 디스크 구성 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션을 `true`로 설정하면, `put` 등 "쓰기" 메서드에서 저장에 실패할 시 `League\Flysystem\UnableToWriteFile` 예외가 발생합니다:

    'public' => [
        'driver' => 'local',
        // ...
        'throw' => true,
    ],

<a name="prepending-appending-to-files"></a>
### 파일 앞뒤에 내용 추가

`prepend`와 `append` 메서드로 파일의 시작 혹은 끝에 내용을 쓸 수 있습니다:

    Storage::prepend('file.log', 'Prepended Text');

    Storage::append('file.log', 'Appended Text');

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 새 위치로 복사하고, `move` 메서드는 이름 변경 또는 다른 위치로 이동할 때 사용합니다:

    Storage::copy('old/file.jpg', 'new/file.jpg');

    Storage::move('old/file.jpg', 'new/file.jpg');

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장소로 스트리밍하면 메모리 사용량이 크게 줄어듭니다. Laravel에서 자동으로 스트리밍 저장을 처리하게 하려면 `putFile` 혹은 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 지정 디렉토리에 파일을 자동으로 스트리밍합니다:

    use Illuminate\Http\File;
    use Illuminate\Support\Facades\Storage;

    // 파일명에 고유한 ID를 자동 생성...
    $path = Storage::putFile('photos', new File('/path/to/photo'));

    // 파일명을 직접 지정...
    $path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');

`putFile` 메서드는 디렉토리명만 있고 파일명은 명시하지 않은 것이 특징입니다. 기본적으로 고유한 ID가 파일명으로 생성되며, 확장자는 MIME 타입으로 결정됩니다. 반환 값은 경로(파일명 포함)이므로 DB에 저장할 때 활용할 수 있습니다.

또한 `putFile`과 `putFileAs`에 저장 파일의 "visibility"를 지정할 수도 있습니다. 클라우드 디스크(Amazon S3 등)에 파일을 공개할 때 유용합니다:

    Storage::putFile('photos', new File('/path/to/photo'), 'public');

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 파일 저장의 대표적인 예시는 사용자가 업로드한 사진이나 문서 저장입니다. Laravel에서는 업로드 파일 인스턴스의 `store` 메서드만으로 손쉽게 파일을 저장할 수 있습니다:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserAvatarController extends Controller
    {
        /**
         * 사용자의 아바타를 업데이트합니다.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function update(Request $request)
        {
            $path = $request->file('avatar')->store('avatars');

            return $path;
        }
    }

위 예시에서도 디렉토리만 지정했지 파일명은 명시하지 않았습니다. 기본적으로 `store` 메서드는 고유한 ID로 파일명을 생성하며, 확장자는 파일의 MIME 타입을 기반으로 자동 결정됩니다. 저장 경로(파일명 포함)가 반환되므로 DB에 기록할 수 있습니다.

동일 작업을 `Storage` 파사드의 `putFile` 메서드를 통해 진행할 수도 있습니다:

    $path = Storage::putFile('avatars', $request->file('avatar'));

<a name="specifying-a-file-name"></a>
#### 파일명 지정

저장되는 파일명 자동 지정이 싫다면, `storeAs` 메서드를 사용하세요. 경로, 파일명, (선택적으로) 디스크 이름을 인수로 받습니다:

    $path = $request->file('avatar')->storeAs(
        'avatars', $request->user()->id
    );

`Storage` 파사드의 `putFileAs`도 동일한 역할을 합니다:

    $path = Storage::putFileAs(
        'avatars', $request->file('avatar'), $request->user()->id
    );

> **경고**  
> 인쇄 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 경로를 반드시 정제(sanitize)하여 저장하도록 하세요. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

업로드 파일의 `store` 메서드는 기본적으로 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 두 번째 인수로 디스크 이름을 전달하세요:

    $path = $request->file('avatar')->store(
        'avatars/'.$request->user()->id, 's3'
    );

`storeAs`의 경우, 세 번째 인수로 디스크 이름을 넘기면 됩니다:

    $path = $request->file('avatar')->storeAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보

업로드 파일의 원본 이름과 확장자를 가져오려면 `getClientOriginalName`과 `getClientOriginalExtension`을 사용할 수 있습니다:

    $file = $request->file('avatar');

    $name = $file->getClientOriginalName();
    $extension = $file->getClientOriginalExtension();

하지만 이 두 메서드는 사용자 조작(악의적인 사용자)이 가능하여 안전하지 않습니다. 따라서 보통 고유한 이름은 `hashName`, 확장자는 `extension` 메서드를 사용하는 것이 더 안전합니다:

    $file = $request->file('avatar');

    $name = $file->hashName(); // 고유한 랜덤 이름 생성
    $extension = $file->extension(); // MIME 타입 기준 확장자 결정

<a name="file-visibility"></a>
### 파일 공개/비공개 설정

Laravel의 Flysystem 통합에서 "visibility"란 여러 플랫폼에서의 파일 권한 개념을 추상화한 것입니다. 파일은 `public`(공개), `private`(비공개)로 선언할 수 있습니다. 예를 들어 S3 드라이버에서 `public` 파일은 URL로 조회가 가능합니다.

파일을 저장하며 visibility를 설정하려면:

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents, 'public');

이미 저장된 파일의 경우에는 `getVisibility` 및 `setVisibility` 메서드로 값을 조회/설정할 수 있습니다:

    $visibility = Storage::getVisibility('file.jpg');

    Storage::setVisibility('file.jpg', 'public');

업로드 파일 처리 시 `storePublicly`, `storePubliclyAs`로 `public` visibility 저장이 가능합니다:

    $path = $request->file('avatar')->storePublicly('avatars', 's3');

    $path = $request->file('avatar')->storePubliclyAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="local-files-and-visibility"></a>
#### 로컬 파일 & 퍼미션

`local` 드라이버를 사용하면, `public` [visibility](#file-visibility)는 디렉토리에는 `0755`, 파일에는 `0644` 권한을 의미합니다. 이 매핑은 `filesystems` 구성 파일에서 수정 가능합니다:

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

`delete` 메서드는 하나의 파일명 또는 파일명 배열을 받아 해당 파일을 삭제합니다:

    use Illuminate\Support\Facades\Storage;

    Storage::delete('file.jpg');

    Storage::delete(['file.jpg', 'file2.jpg']);

필요하다면 삭제할 디스크를 명시적으로 지정할 수도 있습니다:

    use Illuminate\Support\Facades\Storage;

    Storage::disk('s3')->delete('path/file.jpg');

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉토리 내의 모든 파일 배열을 반환합니다. 하위 폴더까지 전부 포함하려면 `allFiles` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Storage;

    $files = Storage::files($directory);

    $files = Storage::allFiles($directory);

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 가져오기

`directories` 메서드는 지정한 디렉토리의 하위 디렉토리 목록을 반환합니다. 하위 디렉토리의 하위까지 모두 가져오고 싶다면 `allDirectories`를 사용하세요:

    $directories = Storage::directories($directory);

    $directories = Storage::allDirectories($directory);

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 지정한 디렉토리를, 필요한 하위 디렉토리까지 포함하여 생성합니다:

    Storage::makeDirectory($directory);

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

마지막으로, `deleteDirectory` 메서드를 사용하여 디렉토리와 그 안의 모든 파일을 삭제할 수 있습니다:

    Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 여러 "드라이버"를 기본 제공합니다. 그러나 Flysystem은 여기에 제한되지 않으며 다양한 외부 스토리지 시스템용 어댑터와 함께 사용할 수 있습니다. 추가 어댑터를 Laravel에서 사용하려면 커스텀 드라이버를 직접 정의할 수 있습니다.

커스텀 파일시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 설치합니다:

```shell
composer require spatie/flysystem-dropbox
```

그 후 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

    <?php

    namespace App\Providers;

    use Illuminate\Filesystem\FilesystemAdapter;
    use Illuminate\Support\Facades\Storage;
    use Illuminate\Support\ServiceProvider;
    use League\Flysystem\Filesystem;
    use Spatie\Dropbox\Client as DropboxClient;
    use Spatie\FlysystemDropbox\DropboxAdapter;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스를 등록합니다.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 애플리케이션 서비스를 부트스트랩합니다.
         *
         * @return void
         */
        public function boot()
        {
            Storage::extend('dropbox', function ($app, $config) {
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

`extend` 메서드의 첫 번째 인수는 드라이버 이름, 두 번째는 `$app` 및 `$config` 변수를 받는 클로저입니다. 이 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config`는 지정한 디스크의 `config/filesystems.php`의 값을 포함합니다.

확장 서비스 프로바이더를 생성하고 등록했다면, `config/filesystems.php`에서 `dropbox` 드라이버를 사용할 수 있습니다.