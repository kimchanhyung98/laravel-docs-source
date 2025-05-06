# 릴리즈 노트

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 10](#laravel-10)

<a name="versioning-scheme"></a>
## 버전 관리 정책

Laravel과 기타 공식 패키지들은 [시맨틱 버전 관리](https://semver.org)를 따릅니다. 주요 프레임워크 릴리즈는 매년(약 1분기)에 한 번 출시되며, 마이너 및 패치 릴리즈는 매주 출시될 수 있습니다. 마이너와 패치 릴리즈에는 **절대로** 하위 호환성이 깨지는 변경 사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 컴포넌트를 참조할 때는, Laravel의 주요 릴리즈가 하위 호환성에 영향을 줄 수 있으므로 항상 `^10.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. 하지만 저희는 항상 하루 이내에 새로운 주요 릴리즈로 업데이트할 수 있도록 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인자(Arguments)

[명명된 인자](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. 필요하다면 Laravel 코드베이스 개선을 위해 함수 인자의 이름이 변경될 수 있습니다. 따라서 Laravel 메서드 호출 시 명명된 인자를 사용할 때는, 향후 인자명이 변경될 수 있음을 주의해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 Laravel 릴리즈에 대해 버그 수정은 18개월간, 보안 수정은 2년간 제공됩니다. Lumen 등 모든 추가 라이브러리의 경우, 최신 주요 버전만 버그 수정을 받습니다. 또한 Laravel에서 지원하는 데이터베이스 버전도 반드시 [공식 문서](/docs/{{version}}/database#introduction)에서 확인하세요.

<div class="overflow-auto">

| 버전 | PHP (*) | 릴리즈 | 버그 수정 지원 종료 | 보안 수정 지원 종료 |
| --- | --- | --- | --- | --- |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.3 | 2024년 3월 12일 | 2025년 8월 5일 | 2026년 2월 3일 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 수정만 지원</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-10"></a>
## Laravel 10

잘 아시다시피, Laravel은 8 버전부터 연 1회의 릴리즈 사이클로 전환하였습니다. 이전에는 주요 버전이 매 6개월마다 발표되었습니다. 이러한 전환은 커뮤니티의 유지보수 부담을 줄이고, 대규모 변경 없이 더 뛰어난 기능을 도입하도록 개발팀에 도전을 주기 위함입니다. 그 결과, Laravel 9에서도 하위 호환성을 깨지 않으면서 다양한 강력한 기능을 제공하였습니다.

따라서 앞으로의 "주요" 릴리즈는 주로 상위 종속성 업그레이드와 같은 "유지보수" 작업을 위해 사용될 가능성이 높으며, 이는 본 릴리즈 노트에서도 확인할 수 있습니다.

Laravel 10은 애플리케이션 스켈레톤의 모든 메소드와 프레임워크 전반에 걸친 모든 스텁 파일에 인자 및 반환 타입(타입힌트)을 도입하여 9.x의 개선 사항을 이어갑니다. 또한 외부 프로세스 실행 및 상호작용을 위한 새로운 개발자 친화적 추상 계층도 추가되었습니다. 더불어, 애플리케이션의 "기능 플래그"를 관리하는 훌륭한 방식인 Laravel Pennant가 처음으로 도입되었습니다.

<a name="php-8"></a>
### PHP 8.1

Laravel 10.x는 최소 PHP 8.1 버전이 필요합니다.

<a name="types"></a>
### 타입

_애플리케이션 스켈레톤과 스텁 타입힌트는 [Nuno Maduro](https://github.com/nunomaduro)님이 기여하였습니다._

Laravel은 초기 릴리즈부터 당시 PHP가 제공하는 모든 타입힌트 기능을 사용했습니다. 하지만 이후 PHP에는 추가적인 기본 타입힌트, 반환 타입, 유니온 타입 등 많은 새로운 기능이 도입되었습니다.

Laravel 10.x에서는 애플리케이션 스켈레톤과 프레임워크에서 사용하는 모든 스텁 파일을 전면적으로 업데이트하여, 모든 메소드 시그니처에 인자 및 반환 타입힌트가 적용되었습니다. 이와 함께 불필요한 "DocBlock" 타입 정보가 삭제되었습니다.

이 변경은 기존 애플리케이션과 완전한 하위 호환성을 보장합니다. 따라서 기존에 타입힌트가 없는 애플리케이션도 정상적으로 동작합니다.

<a name="laravel-pennant"></a>
### Laravel Pennant

_Laravel Pennant는 [Tim MacDonald](https://github.com/timacdonald)님이 개발하였습니다._

새로운 공식 패키지인 Laravel Pennant가 출시되었습니다. Pennant는 애플리케이션의 기능 플래그를 가볍고 간결하게 관리할 수 있게 해줍니다. 기본적으로 인메모리 `array` 드라이버와 영구 저장을 위한 `database` 드라이버가 제공됩니다.

기능은 `Feature::define` 메서드로 쉽게 정의할 수 있습니다:

```php
use Laravel\Pennant\Feature;
use Illuminate\Support\Lottery;

Feature::define('new-onboarding-flow', function () {
    return Lottery::odds(1, 10);
});
```

기능이 정의되면, 현재 사용자가 해당 기능에 접근 가능한지 손쉽게 확인할 수 있습니다:

```php
if (Feature::active('new-onboarding-flow')) {
    // ...
}
```

또한, 편의를 위해 Blade 지시어도 지원합니다:

```blade
@feature('new-onboarding-flow')
    <div>
        <!-- ... -->
    </div>
@endfeature
```

Pennant는 이 외에도 다양한 고급 기능과 API를 제공합니다. 더 자세한 내용은 [Pennant 공식 문서](/docs/{{version}}/pennant)를 참고하세요.

<a name="process"></a>
### 프로세스 상호작용

_프로세스 추상 계층은 [Nuno Maduro](https://github.com/nunomaduro)와 [Taylor Otwell](https://github.com/taylorotwell)님이 기여하였습니다._

Laravel 10.x에서는 새로운 `Process` 파사드를 통해 외부 프로세스 실행 및 상호작용을 위한 훌륭한 추상 계층이 도입되었습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

여러 프로세스를 풀(pool)로 동시에 실행하고 관리할 수도 있습니다:

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->command('cat first.txt');
    $pool->command('cat second.txt');
    $pool->command('cat third.txt');
});

return $first->output();
```

또한 프로세스 실행을 가짜로 만들 수도 있어, 테스트 시 매우 편리합니다:

```php
Process::fake();

// ...

Process::assertRan('ls -la');
```

프로세스와의 상호작용에 대한 자세한 내용은 [프로세스 공식 문서](/docs/{{version}}/processes)를 확인하세요.

<a name="test-profiling"></a>
### 테스트 프로파일링

_테스트 프로파일링 기능은 [Nuno Maduro](https://github.com/nunomaduro)님이 기여하였습니다._

Artisan의 `test` 명령에 새로운 `--profile` 옵션이 추가되어, 애플리케이션에서 가장 느린 테스트를 쉽게 찾을 수 있습니다:

```shell
php artisan test --profile
```

가장 느린 테스트는 CLI 출력에 바로 표시됩니다:

<p align="center">
    <img width="100%" src="https://user-images.githubusercontent.com/5457236/217328439-d8d983ec-d0fc-4cde-93d9-ae5bccf5df14.png"/>
</p>

<a name="pest-scaffolding"></a>
### Pest 스캐폴딩

이제 신규 Laravel 프로젝트에서 Pest 테스트 스캐폴딩을 기본적으로 선택할 수 있습니다. 이 기능을 사용하려면 Laravel 인스톨러로 새 애플리케이션을 생성할 때 `--pest` 플래그를 지정하세요:

```shell
laravel new example-application --pest
```

<a name="generator-cli-prompts"></a>
### 생성기 CLI 프롬프트

_생성기 CLI 프롬프트 기능은 [Jess Archer](https://github.com/jessarcher)님이 기여하였습니다._

프레임워크의 개발자 경험 향상을 위해 모든 내장 `make` 명령은 더 이상 인자를 필수로 입력받지 않습니다. 입력 없이 명령을 실행하면, 필요한 인자에 대해 프롬프트가 표시됩니다:

```shell
php artisan make:controller
```

<a name="horizon-telescope-facelift"></a>
### Horizon / Telescope UI 개선

[Horizon](/docs/{{version}}/horizon)과 [Telescope](/docs/{{version}}/telescope)는 타이포그래피, 여백, 디자인 등이 개선되어 한층 더 세련되고 현대적인 모습으로 업데이트되었습니다:

<img src="https://laravel.com/img/docs/horizon-example.png">
