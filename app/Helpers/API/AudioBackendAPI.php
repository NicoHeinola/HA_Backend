<?php

declare(strict_types=1);

namespace App\Helpers\API;

use GuzzleHttp\Client;

class AudioBackendAPI
{
    protected string $audioBackendUrl;

    protected string $audioBackendToken;

    public function __construct()
    {
        $this->audioBackendUrl = rtrim(config('services.audio_backend.url'), '/');
        $this->audioBackendToken = config('services.audio_backend.access_token');
    }

    public function convertTextToSpeech(string $text): ?string
    {
        $headers = [
            'Authorization' => 'Bearer '.$this->audioBackendToken,
            'Content-Type' => 'application/json',
            'Accept' => 'application/octet-stream',
        ];

        $payload = [
            'message' => $text,
        ];

        $client = new Client;
        $url = $this->audioBackendUrl.'/text-to-speech';
        $response = $client->post($url, [
            'headers' => $headers,
            'json' => $payload,
        ]);

        if ($response->getStatusCode() !== 200) {
            return null;
        }

        return $response->getBody()->getContents();
    }
}
