<?php

declare(strict_types=1);

namespace App\Helpers\API\WiZ;

use App\Helpers\API\HomeAssistantAPI;
use Illuminate\Support\Facades\Log;

class WiZLightHelper extends HomeAssistantAPI
{
    /**
     * Turn off a Wiz light.
     */
    public function turnOff(string $entityId)
    {
        return $this->callService('light', 'turn_off', [
            'entity_id' => 'light.'.$entityId,
        ]);
    }

    /**
     * Turn on a Wiz light.
     */
    public function turnOn(string $entityId)
    {
        return $this->callService('light', 'turn_on', [
            'entity_id' => 'light.'.$entityId,
        ]);
    }

    /**
     * Toggle a Wiz light.
     */
    public function toggle(string $entityId): bool
    {
        $lightState = $this->getLightState($entityId);

        if (!$lightState || !isset($lightState['state'])) {
            Log::warning('Unable to retrieve light state for toggle.', ['entity_id' => $entityId]);

            return false;
        }

        if ($lightState['state'] === 'on') {
            $this->turnOff($entityId);
        } else {
            $this->turnOn($entityId);
        }

        return true;
    }

    /**
     * Set the RGB color of a Wiz light.
     */
    public function setRgbColor(string $entityId, int $r, int $g, int $b)
    {
        $payload = [
            'entity_id' => 'light.'.$entityId,
            'rgb_color' => [$r, $g, $b],
        ];

        return $this->callService('light', 'turn_on', $payload);
    }

    /**
     * Set the brightness of a Wiz light.
     */
    public function setBrightness(string $entityId, int $brightness)
    {
        $payload = [
            'entity_id' => 'light.'.$entityId,
            'brightness' => $brightness,
        ];

        return $this->callService('light', 'turn_on', $payload);
    }

    /**
     * Get the current state of a Wiz light.
     */
    public function getLightState(string $entityId): ?array
    {
        $headers = $this->getAuthorizationHeader();
        $url = $this->haUrl.'/api/states/light.'.$entityId;
        $response = $this->client->get($url, [
            'headers' => $headers,
        ]);

        if ($response->getStatusCode() === 200) {
            return json_decode($response->getBody()->getContents(), true);
        }

        return null;
    }

    public function getAllAvailableLights(): array
    {
        $headers = $this->getAuthorizationHeader();
        $url = $this->haUrl.'/api/states';
        $response = $this->client->get($url, [
            'headers' => $headers,
        ]);

        if ($response->getStatusCode() !== 200) {
            return [];
        }

        $states = json_decode($response->getBody()->getContents(), true);
        $lights = [];
        foreach ($states as $state) {
            $stateEntityId = $state['entity_id'] ?? '';

            // Remove light. prefix
            if (mb_strpos($stateEntityId, 'light.') !== 0) {
                continue;
            }
            $stateEntityId = str_replace('light.', '', $stateEntityId);

            $lights[] = $stateEntityId;
        }

        return $lights;
    }
}
