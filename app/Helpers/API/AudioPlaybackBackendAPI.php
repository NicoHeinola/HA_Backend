<?php

declare(strict_types=1);

namespace App\Helpers\API;

use GuzzleHttp\Client;

class AudioPlaybackBackendAPI
{
    protected string $audioPlaybackBackendHost;

    protected string $audioPlaybackBackendPort;

    protected string $audioPlaybackBackendToken;

    public function __construct()
    {
        $this->audioPlaybackBackendHost = config('services.audio_playback_backend.url');
        $this->audioPlaybackBackendPort = config('services.audio_playback_backend.port');
        $this->audioPlaybackBackendToken = config('services.audio_playback_backend.access_token');
    }

    public function playAudio(string $audioData): array
    {

        $client = new Client;

        $url = rtrim($this->audioPlaybackBackendHost, '/')
            .':'.$this->audioPlaybackBackendPort
            .'/audio-playback/play-audio';

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
        ]);

        // decode/return as above
        $body = (string) $response->getBody();
        $decoded = json_decode($body, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            return $decoded;
        }

        return ['status_code' => $response->getStatusCode(), 'response' => $body];

    }
}
