# Contracts (계약)

- [소개](#introduction)
    - [Contracts와 Facades 비교](#contracts-vs-facades)
- [Contracts를 사용해야 할 때](#when-to-use-contracts)
- [Contracts 사용 방법](#how-to-use-contracts)
- [Contract 참고표](#contract-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "contracts"는 프레임워크가 제공하는 핵심 서비스들을 정의하는 인터페이스 모음입니다. 예를 들어, `Illuminate\Contracts\Queue\Queue` contract는 작업 큐잉에 필요한 메서드들을 정의하며, `Illuminate\Contracts\Mail\Mailer` contract는 이메일 전송에 필요한 메서드들을 정의합니다.

각 contract는 프레임워크가 제공하는 해당 구현체와 연결되어 있습니다. 예를 들어, Laravel은 다양한 드라이버를 지원하는 큐(queue) 구현체와 Symfony Mailer 기반의 메일러 구현체를 제공합니다.

모든 Laravel contracts는 [별도의 GitHub 저장소](https://github.com/illuminate/contracts)에 위치해 있습니다. 이를 통해 사용 가능한 모든 contracts를 쉽게 참조할 수 있으며, Laravel 서비스와 연동하는 패키지를 개발할 때 단일의 분리된 패키지로 활용할 수 있습니다.

<a name="contracts-vs-facades"></a>
### Contracts와 Facades 비교

Laravel의 [facades](/docs/master/facades)와 헬퍼 함수는 타입 힌트나 서비스 컨테이너에서 contract를 직접 해석하지 않아도 Laravel 서비스를 쉽게 사용할 수 있는 방법을 제공합니다. 대부분의 경우, 각 facade는 이에 상응하는 contract를 가지고 있습니다.

facade는 클래스 생성자에서 명시적으로 주입받을 필요가 없지만, contract는 클래스의 의존성을 명확히 정의할 수 있도록 허용합니다. 따라서 일부 개발자들은 의존성을 명확히 정의하는 방식으로 contract를 선호하는 반면, 다른 개발자들은 facade의 편리함을 더 선호합니다. **일반적으로 대부분의 애플리케이션은 개발 과정에서 facade를 문제없이 사용할 수 있습니다.**

<a name="when-to-use-contracts"></a>
## Contracts를 사용해야 할 때

contract를 사용할지 facade를 사용할지는 개인 혹은 개발팀의 선호도에 따라 다릅니다. contract와 facade 모두 강력하고 충분히 테스트된 Laravel 애플리케이션을 만드는 데 사용할 수 있습니다. 또한 contract와 facade는 상호 배타적이지 않습니다. 애플리케이션의 일부는 facade를, 다른 일부는 contract를 사용할 수 있습니다. 클래스 책임이 명확하게 구분되어 있다면 contract와 facade 간에 실질적인 차이를 거의 느끼지 못할 것입니다.

대부분의 애플리케이션은 개발 중에 facade를 문제없이 사용할 수 있습니다. 만약 여러 PHP 프레임워크와 연동하는 패키지를 만든다면, `illuminate/contracts` 패키지를 사용해 Laravel 서비스와의 통합을 정의하고, 패키지의 `composer.json`에 Laravel의 구체적 구현체들을 직접 포함하지 않아도 됩니다.

<a name="how-to-use-contracts"></a>
## Contracts 사용 방법

그렇다면 contract의 구현체는 어떻게 얻을 수 있을까요? 매우 간단합니다.

Laravel의 많은 클래스 타입은 [서비스 컨테이너](/docs/master/container)를 통해 해석됩니다. 여기에는 컨트롤러, 이벤트 리스너, 미들웨어, 큐 대기 작업, 라우트 클로저 등이 포함됩니다. 따라서 contract 구현체를 얻으려면, 해당 클래스 생성자의 매개변수에 인터페이스를 타입 힌트로 지정하기만 하면 됩니다.

예를 들어, 이 이벤트 리스너 코드를 살펴보세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderWasPlaced;
use App\Models\User;
use Illuminate\Contracts\Redis\Factory;

class CacheOrderInformation
{
    /**
     * Create a new event handler instance.
     */
    public function __construct(
        protected Factory $redis,
    ) {}

    /**
     * Handle the event.
     */
    public function handle(OrderWasPlaced $event): void
    {
        // ...
    }
}
```

이 이벤트 리스너가 해석될 때, 서비스 컨테이너는 생성자에 명시된 타입 힌트를 읽어 적절한 값을 자동으로 주입합니다. 서비스 컨테이너에서 객체를 등록하는 방법에 대해서는 [문서](/docs/master/container)를 참고하세요.

<a name="contract-reference"></a>
## Contract 참고표

아래 표는 모든 Laravel contracts와 이와 해당하는 facade를 빠르게 참고할 수 있도록 정리한 내용입니다:

<div class="overflow-auto">

| Contract | 참고할 수 있는 Facade |
| --- | --- |
| [Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/master/Auth/Access/Authorizable.php) | &nbsp; |
| [Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/master/Auth/Access/Gate.php) | `Gate` |
| [Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/master/Auth/Authenticatable.php) | &nbsp; |
| [Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/master/Auth/CanResetPassword.php) | &nbsp; |
| [Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/master/Auth/Factory.php) | `Auth` |
| [Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/master/Auth/Guard.php) | `Auth::guard()` |
| [Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/master/Auth/PasswordBroker.php) | `Password::broker()` |
| [Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/master/Auth/PasswordBrokerFactory.php) | `Password` |
| [Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/master/Auth/StatefulGuard.php) | &nbsp; |
| [Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/master/Auth/SupportsBasicAuth.php) | &nbsp; |
| [Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/master/Auth/UserProvider.php) | &nbsp; |
| [Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/master/Broadcasting/Broadcaster.php) | `Broadcast::connection()` |
| [Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/master/Broadcasting/Factory.php) | `Broadcast` |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/master/Broadcasting/ShouldBroadcast.php) | &nbsp; |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/master/Broadcasting/ShouldBroadcastNow.php) | &nbsp; |
| [Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/master/Bus/Dispatcher.php) | `Bus` |
| [Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/master/Bus/QueueingDispatcher.php) | `Bus::dispatchToQueue()` |
| [Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/master/Cache/Factory.php) | `Cache` |
| [Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/master/Cache/Lock.php) | &nbsp; |
| [Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/master/Cache/LockProvider.php) | &nbsp; |
| [Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/master/Cache/Repository.php) | `Cache::driver()` |
| [Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/master/Cache/Store.php) | &nbsp; |
| [Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/master/Config/Repository.php) | `Config` |
| [Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/master/Console/Application.php) | &nbsp; |
| [Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/master/Console/Kernel.php) | `Artisan` |
| [Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/master/Container/Container.php) | `App` |
| [Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/master/Cookie/Factory.php) | `Cookie` |
| [Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/master/Cookie/QueueingFactory.php) | `Cookie::queue()` |
| [Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/master/Database/ModelIdentifier.php) | &nbsp; |
| [Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/master/Debug/ExceptionHandler.php) | &nbsp; |
| [Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/master/Encryption/Encrypter.php) | `Crypt` |
| [Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/master/Events/Dispatcher.php) | `Event` |
| [Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/master/Filesystem/Cloud.php) | `Storage::cloud()` |
| [Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/master/Filesystem/Factory.php) | `Storage` |
| [Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/master/Filesystem/Filesystem.php) | `Storage::disk()` |
| [Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/master/Foundation/Application.php) | `App` |
| [Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/master/Hashing/Hasher.php) | `Hash` |
| [Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/master/Http/Kernel.php) | &nbsp; |
| [Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/master/Mail/Mailable.php) | &nbsp; |
| [Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/master/Mail/Mailer.php) | `Mail` |
| [Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/master/Mail/MailQueue.php) | `Mail::queue()` |
| [Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/master/Notifications/Dispatcher.php) | `Notification`|
| [Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/master/Notifications/Factory.php) | `Notification` |
| [Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/master/Pagination/LengthAwarePaginator.php) | &nbsp; |
| [Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/master/Pagination/Paginator.php) | &nbsp; |
| [Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/master/Pipeline/Hub.php) | &nbsp; |
| [Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/master/Pipeline/Pipeline.php) | `Pipeline` |
| [Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/master/Queue/EntityResolver.php) | &nbsp; |
| [Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/master/Queue/Factory.php) | `Queue` |
| [Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/master/Queue/Job.php) | &nbsp; |
| [Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/master/Queue/Monitor.php) | `Queue` |
| [Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/master/Queue/Queue.php) | `Queue::connection()` |
| [Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/master/Queue/QueueableCollection.php) | &nbsp; |
| [Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/master/Queue/QueueableEntity.php) | &nbsp; |
| [Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/master/Queue/ShouldQueue.php) | &nbsp; |
| [Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/master/Redis/Factory.php) | `Redis` |
| [Illuminate\Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/master/Routing/BindingRegistrar.php) | `Route` |
| [Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/master/Routing/Registrar.php) | `Route` |
| [Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/master/Routing/ResponseFactory.php) | `Response` |
| [Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/master/Routing/UrlGenerator.php) | `URL` |
| [Illuminate\Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/master/Routing/UrlRoutable.php) | &nbsp; |
| [Illuminate\Contracts\Session\Session](https://github.com/illuminate/contracts/blob/master/Session/Session.php) | `Session::driver()` |
| [Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/master/Support/Arrayable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/master/Support/Htmlable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/master/Support/Jsonable.php) | &nbsp; |
| [Illuminate\Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/master/Support/MessageBag.php) | &nbsp; |
| [Illuminate\Contracts\Support\MessageProvider](https://github.com/illuminate/contracts/blob/master/Support/MessageProvider.php) | &nbsp; |
| [Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/master/Support/Renderable.php) | &nbsp; |
| [Illuminate\Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/master/Support/Responsable.php) | &nbsp; |
| [Illuminate\Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/master/Translation/Loader.php) | &nbsp; |
| [Illuminate\Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/master/Translation/Translator.php) | `Lang` |
| [Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/master/Validation/Factory.php) | `Validator` |
| [Illuminate\Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/master/Validation/ValidatesWhenResolved.php) | &nbsp; |
| [Illuminate\Contracts\Validation\ValidationRule](https://github.com/illuminate/contracts/blob/master/Validation/ValidationRule.php) | &nbsp; |
| [Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/master/Validation/Validator.php) | `Validator::make()` |
| [Illuminate\Contracts\View\Engine](https://github.com/illuminate/contracts/blob/master/View/Engine.php) | &nbsp; |
| [Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/master/View/Factory.php) | `View` |
| [Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/master/View/View.php) | `View::make()` |

</div>