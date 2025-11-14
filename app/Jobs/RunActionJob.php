<?php

declare(strict_types=1);

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

    public function handle(): void
    {
        $actionName = $this->action['name'] ?? null;
        if (!$actionName) {
            Log::warning('Action name is missing.');

            return;
        }

        Log::info("Executing action: {$actionName}");

        switch ($actionName) {
            case 'lights.turn_on':
                $this->handleTurnOnLights();
                break;
            case 'lights.turn_off':
                $this->handleTurnOffLights();
                break;
            case 'lights.toggle':
                $this->handleToggleLights();
                break;
            case 'lights.set_rgb_color':
                $this->handleSetRgbColor();
                break;
            case 'lights.set_brightness':
                $this->handleSetBrightness();
                break;
            default:
                Log::warning("Unknown action: {$actionName}");
                break;
        }
    }

    private function getWiZHelper(): WiZLightHelper
    {
        return new WiZLightHelper(
            config('services.home_assistant.url'),
            config('services.home_assistant.access_token')
        );
    }

    private function handleTurnOnLights(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];
        $wizHelper = $this->getWiZHelper();

        if (empty($entityIds)) {
            $entityIds = $wizHelper->getAllAvailableLights();
        }

        foreach ($entityIds as $entityId) {
            $wizHelper->turnOn($entityId);
        }
    }

    private function handleTurnOffLights(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];
        $wizHelper = $this->getWiZHelper();

        if (empty($entityIds)) {
            Log::info('No entity IDs provided, fetching all available lights.');
            $entityIds = $wizHelper->getAllAvailableLights();
        }

        foreach ($entityIds as $entityId) {
            $wizHelper->turnOff($entityId);
        }
    }

    private function handleToggleLights(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];
        $wizHelper = $this->getWiZHelper();

        if (empty($entityIds)) {
            $entityIds = $wizHelper->getAllAvailableLights();
        }

        foreach ($entityIds as $entityId) {
            $wizHelper->toggle($entityId);
        }
    }

    private function handleSetRgbColor(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];
        $r = $params['r'] ?? null;
        $g = $params['g'] ?? null;
        $b = $params['b'] ?? null;

        if ($r === null || $g === null || $b === null) {
            Log::warning('RGB values are missing for setRgbColor action.');

            return;
        }

        $wizHelper = $this->getWiZHelper();

        if (empty($entityIds)) {
            $entityIds = $wizHelper->getAllAvailableLights();
        }

        foreach ($entityIds as $entityId) {
            $wizHelper->setRgbColor($entityId, $r, $g, $b);
        }
    }

    private function handleSetBrightness(): void
    {
        $params = $this->action['params'] ?? [];
        $entityIds = $params['entity_ids'] ?? [];
        $brightness = $params['brightness'] ?? null;

        if ($brightness === null) {
            Log::warning('Brightness value is missing for setBrightness action.');

            return;
        }

        $wizHelper = $this->getWiZHelper();
        if (empty($entityIds)) {
            $entityIds = $wizHelper->getAllAvailableLights();
        }

        foreach ($entityIds as $entityId) {
            $wizHelper->setBrightness($entityId, (int) $brightness);
        }
    }
}
