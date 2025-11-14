<?php

namespace App\Helpers\WiZ;

use App\Helpers\HomeAssistantAPI;

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

        // You can add logic here to actually toggle based on state
        // For now, just print and return true
        // error_log('STATE RESPONSE: ' . print_r($lightState, true));
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
}
