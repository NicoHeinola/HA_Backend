<?php

declare(strict_types=1);

namespace App\Helpers\API;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;

/**
 * Home Assistant API integration base class
 */
class HomeAssistantAPI
{
    protected string $haUrl;

    protected string $accessToken;

    protected Client $client;

    /**
     * HomeAssistantAPI constructor.
     */
    public function __construct(string $haUrl, string $accessToken)
    {
        $this->haUrl = rtrim($haUrl, '/');
        $this->accessToken = $accessToken;
        $this->client = new Client;
    }

    /**
     * Get the authorization header for requests.
     */
    protected function getAuthorizationHeader(): array
    {
        return [
            'Authorization' => 'Bearer '.$this->accessToken,
        ];
    }

    /**
     * Call a Home Assistant service.
     *
     * @param  string  $domain  Service domain (e.g., "light", "media_player").
     * @param  string  $service  Service name (e.g., "turn_on", "play_media").
     * @param  array  $payload  JSON payload to send with the request.
     * @param  array  $extraHeaders  Additional headers to include in the request.
     * @return \Psr\HttpMessage\ResponseInterface|null
     *
     * @throws GuzzleException
     */
    protected function callService(string $domain, string $service, array $payload = [], array $extraHeaders = [])
    {
        $headers = array_merge(
            $this->getAuthorizationHeader(),
            ['Content-Type' => 'application/json'],
            $extraHeaders
        );

        $url = $this->haUrl."/api/services/{$domain}/{$service}";

        $response = $this->client->post($url, [
            'json' => $payload,
            'headers' => $headers,
        ]);

        return $response;
    }
}
