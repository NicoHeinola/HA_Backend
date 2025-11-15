<?php

declare(strict_types=1);

namespace App\Helpers\API;

use GuzzleHttp\Client;

class AudioPlaybackBackendAPI
{
    protected string $audioPlaybackBackendUrl;

    protected string $audioPlaybackBackendToken;

    public function __construct()
    {
        $this->audioPlaybackBackendUrl = rtrim(config('services.audio_playback_backend.url'), '/');
        $this->audioPlaybackBackendToken = config('services.audio_playback_backend.access_token');
    }

    public function playAudio(string $audioData): array
    {

        $client = new Client(['timeout' => 3]);
        $url = $this->audioPlaybackBackendUrl.'/audio-playback/play-audio';
        $response = $client->post($url, [
            'headers' => [
                'Authorization' => 'Bearer '.$this->audioPlaybackBackendToken,
                'Accept' => 'application/json',
            ],
            'multipart' => [
                [
                    'name' => 'file',
                    'contents' => $audioData,
                    'filename' => 'speech',
                ],
            ],
            'http_errors' => false,
        ], );

        // decode/return as above
        $body = (string) $response->getBody();
        $decoded = json_decode($body, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            return $decoded;
        }

        return ['status_code' => $response->getStatusCode(), 'response' => $body];

    }
}
