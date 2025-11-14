<?php

namespace App\Jobs;

use App\Helpers\WiZ\WiZLightHelper;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Log;

class RunActionJob implements ShouldQueue
{
    use Queueable;

    protected array $action;

    public function __construct(array $action)
    {
        $this->action = $action;
    }

    private function handleTurnOnLights(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];

        $wizHelper = new WiZLightHelper(
            config('services.home_assistant.url'),
            config('services.home_assistant.access_token')
        );

        foreach ($entityIds as $entityId) {
            $wizHelper->turnOn($entityId);
        }
    }

    private function handleTurnOffLights(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];

        $wizHelper = new WiZLightHelper(
            config('services.home_assistant.url'),
            config('services.home_assistant.access_token')
        );

        foreach ($entityIds as $entityId) {
            $wizHelper->turnOff($entityId);
        }
    }

    public function handle(): void
    {
        $actionName = $this->action['name'] ?? null;
        if (! $actionName) {
            Log::warning('Action name is missing.');

            return;
        }

        switch ($actionName) {
            case 'lights.turn_on':
                $this->handleTurnOnLights();
                break;

            case 'lights.turn_off':
                $this->handleTurnOffLights();
                break;

                // Add more cases for different actions as needed

            default:
                Log::warning("Unknown action: {$actionName}");
                break;
        }
    }
}
