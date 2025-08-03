# 릴리즈 노트 (Release Notes)

- [버전 관리 방식](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 10](#laravel-10)

<a name="versioning-scheme"></a>
## 버전 관리 방식 (Versioning Scheme)

Laravel과 기타 Laravel 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 메이저 프레임워크 릴리즈는 매년(대략 1분기)에 한 번씩 출시되며, 마이너 및 패치 릴리즈는 주 단위로 자주 출시될 수 있습니다. 마이너 및 패치 릴리즈에는 **절대로** 호환성을 깨는 변경 사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 구성 요소를 참조할 때는 항상 `^10.0`과 같은 버전 제한(version constraint)을 사용하는 것이 좋습니다. 메이저 릴리즈에는 호환성을 깨는 변경이 포함되기 때문입니다. 하지만 저희는 새로운 메이저 버전으로 하루 이내에 업그레이드할 수 있도록 항상 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수 (Named Arguments)

[명명된 인수](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 이전 버전 호환 가이드라인의 적용 대상이 아닙니다. 코드베이스 개선을 위해 필요에 따라 함수 인수명을 변경할 수 있습니다. 따라서 Laravel 메서드를 호출할 때 명명된 인수를 사용할 경우 향후 파라미터 이름이 변경될 수 있다는 점을 염두에 두고 신중히 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈는 버그 수정이 18개월간, 보안 수정이 2년간 제공됩니다. Lumen을 포함한 추가 라이브러리들은 최신 메이저 릴리즈만 버그 수정 지원 대상에 포함됩니다. 또한, Laravel에서 지원하는 데이터베이스 버전도 확인해 주세요. [데이터베이스 지원](https://laravel.com/docs/10.x/database#introduction)

<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 종료 | 보안 수정 종료 |
| --- | --- | --- | --- | --- |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료 (End of life)</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 수정만 지원 (Security fixes only)</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-10"></a>
## Laravel 10

알고 계시듯이, Laravel은 8 버전부터 연 1회 출시 체계로 전환했습니다. 예전에는 메이저 버전을 6개월마다 출시했었습니다. 이 전환은 커뮤니티의 유지보수 부담을 줄이고 개발팀이 호환성을 깨뜨리지 않으면서도 뛰어나고 강력한 새 기능을 출시하는 데 집중할 수 있도록 하기 위한 목적입니다. 따라서 Laravel 9에서는 하위 호환성을 깨뜨리지 않고도 여러 견고한 기능을 소개했습니다.

그 결과 이번 릴리즈 노트에서 보시듯, 앞으로 메이저 릴리즈는 상위 종속성 업그레이드 같은 “유지보수” 작업에 주로 활용될 가능성이 높습니다.

Laravel 10은 Laravel 9.x에서 진행된 개선을 이어갑니다. 프레임워크 내 모든 애플리케이션 스켈레톤 메서드 및 클래스 생성에 사용되는 스텁(stub) 파일에 인수 및 반환 타입을 도입했으며, 외부 프로세스를 시작하고 상호작용하기 위한 개발자 친화적인 추상화 레이어가 새로 추가되었습니다. 또한, Laravel Pennant라는 새로운 기능 플래그(feature flags) 관리 패키지가 포함되었습니다.

<a name="php-8"></a>
### PHP 8.1

Laravel 10.x는 PHP 8.1 이상 버전을 요구합니다.

<a name="types"></a>
### 타입 (Types)

_애플리케이션 스켈레톤과 스텁 타입 힌트는 [Nuno Maduro](https://github.com/nunomaduro)님께서 기여했습니다._

Laravel 초기 버전은 당시 PHP가 제공하던 타입 힌팅 기능을 모두 사용했습니다. 하지만 이후 몇 년 동안 추가적인 원시 타입 힌팅, 반환 타입, 유니언 타입 등 여러 새 기능이 도입되었습니다.

Laravel 10.x는 애플리케이션 스켈레톤과 프레임워크 내에서 사용하는 모든 스텁 파일을 최신화하여 모든 메서드 시그니처에 인수 및 반환 타입을 도입했습니다. 동시에 불필요한 doc 블록의 타입 힌트 정보는 삭제했습니다.

이 변경은 기존 애플리케이션과 완전한 하위 호환성을 가집니다. 따라서 기존 앱에 타입 힌트가 없어도 정상 동작합니다.

<a name="laravel-pennant"></a>
### Laravel Pennant

_Laravel Pennant는 [Tim MacDonald](https://github.com/timacdonald)님이 개발했습니다._

새로운 공식 패키지인 Laravel Pennant가 릴리즈되었습니다. Pennant는 애플리케이션 내 기능 플래그를 관리하는 가볍고 간결한 방법을 제공합니다. 기본적으로 Pennant는 메모리 내 array 드라이버와 지속 저장용 데이터베이스 드라이버를 포함합니다.

기능 플래그는 `Feature::define` 메서드로 쉽게 정의할 수 있습니다:

```php
use Laravel\Pennant\Feature;
use Illuminate\Support\Lottery;

Feature::define('new-onboarding-flow', function () {
    return Lottery::odds(1, 10);
});
```

기능을 정의한 뒤에는 현재 사용자가 해당 기능에 접근 가능한지 간단히 확인할 수 있습니다:

```php
if (Feature::active('new-onboarding-flow')) {
    // ...
}
```

물론 편리함을 위해 Blade 디렉티브도 함께 제공됩니다:

```blade
@feature('new-onboarding-flow')
    <div>
        <!-- ... -->
    </div>
@endfeature
```

Pennant는 이외에도 다양한 고급 기능과 API를 제공합니다. 자세한 내용은 [Pennant 공식 문서](/docs/10.x/pennant)를 참고하세요.

<a name="process"></a>
### 프로세스 상호작용 (Process Interaction)

_프로세스 추상화 레이어는 [Nuno Maduro](https://github.com/nunomaduro)님과 [Taylor Otwell](https://github.com/taylorotwell)님이 기여했습니다._

Laravel 10.x에서는 외부 프로세스를 시작하고 상호작용하기 위한 아름다운 추상화 레이어가 새로 도입되었습니다. `Process` 파사드를 사용해 다음처럼 간단히 외부 명령을 실행할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

동시 실행이 필요한 경우 프로세스 풀(pool)도 지원하여 여러 프로세스를 편리하게 관리할 수 있습니다:

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

또한 테스트 편의를 위해 프로세스 실행을 가짜(faked) 처리할 수도 있습니다:

```php
Process::fake();

// ...

Process::assertRan('ls -la');
```

프로세스 상호작용에 대한 더 자세한 내용은 [프로세스 공식 문서](/docs/10.x/processes)를 참고하세요.

<a name="test-profiling"></a>
### 테스트 프로파일링 (Test Profiling)

_테스트 프로파일링 기능은 [Nuno Maduro](https://github.com/nunomaduro)님이 기여했습니다._

Artisan `test` 명령어에 `--profile` 옵션이 새로 추가되어, 애플리케이션에서 가장 느린 테스트를 쉽게 확인할 수 있습니다:

```shell
php artisan test --profile
```

CLI 출력 결과에 가장 오래 걸린 테스트들이 직접 표시되어 편리합니다:

<p align="center">
```
<img width="100%" src="https://user-images.githubusercontent.com/5457236/217328439-d8d983ec-d0fc-4cde-93d9-ae5bccf5df14.png"/>
```
</p>

<a name="pest-scaffolding"></a>
### Pest 테스트 스캐폴딩 (Pest Scaffolding)

신규 Laravel 프로젝트를 기본적으로 Pest 테스트 스캐폴딩과 함께 생성할 수 있습니다. Laravel 인스톨러 실행 시 `--pest` 플래그를 추가하면 됩니다:

```shell
laravel new example-application --pest
```

<a name="generator-cli-prompts"></a>
### 생성기 CLI 프롬프트 (Generator CLI Prompts)

_생성기 CLI 프롬프트 개선은 [Jess Archer](https://github.com/jessarcher)님이 기여했습니다._

프레임워크 개발자 경험 향상을 위해, Laravel에 내장된 모든 `make` 명령어는 기본적으로 필요한 인수 없이 실행할 수 있습니다. 인수가 부족하면 적절한 질문으로 프롬프트가 표시됩니다:

```shell
php artisan make:controller
```

<a name="horizon-telescope-facelift"></a>
### Horizon / Telescope 디자인 리뉴얼 (Horizon / Telescope Facelift)

[Horizon](/docs/10.x/horizon)과 [Telescope](/docs/10.x/telescope)가 더 깔끔하고 현대적인 디자인으로 업데이트되었습니다. 타이포그래피, 여백, 전반적인 레이아웃이 개선되었습니다:

<img src="https://laravel.com/img/docs/horizon-example.png" />