<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Helpers\API\WiZ\WiZLightHelper;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Log;

class RunActionJob implements ShouldQueue
{
    use Queueable;

    protected array $actionName;

    protected array $actionParams;

    public function __construct(array $actionName, array $actionParams = [])
    {
        $this->actionName = $actionName;
        $this->actionParams = $actionParams;
    }

    public function handle(): void
    {
        $actionName = $this->actionName['name'] ?? '';

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
        $entityIds = $this->actionParams['entity_ids'] ?? [];
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

        $entityIds = $this->actionParams['entity_ids'] ?? [];
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

        $entityIds = $this->actionParams['entity_ids'] ?? [];
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

        $entityIds = $this->actionParams['entity_ids'] ?? [];
        $r = $this->actionParams['r'] ?? null;
        $g = $this->actionParams['g'] ?? null;
        $b = $this->actionParams['b'] ?? null;

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

        $entityIds = $this->actionParams['entity_ids'] ?? [];
        $brightness = $this->actionParams['brightness'] ?? null;

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
