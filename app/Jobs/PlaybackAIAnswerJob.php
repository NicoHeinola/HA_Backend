<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Helpers\API\AudioBackendAPI;
use App\Helpers\API\AudioPlaybackBackendAPI;
use Exception;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Log;

class PlaybackAIAnswerJob implements ShouldQueue
{
    use Queueable;

    protected string $aiAnswer;

    public function __construct(string $aiAnswer)
    {
        $this->aiAnswer = $aiAnswer;
    }

    public function handle(): void
    {
        Log::info('Playing AI answer: '.$this->aiAnswer);

        try {
            $audioBackendAPI = new AudioBackendAPI;
            $audioData = $audioBackendAPI->convertTextToSpeech($this->aiAnswer);

            // Make the audio more "human like"
            $audioData = $audioBackendAPI->speedUpAudio($audioData, 1.20);
        } catch (Exception $e) {
            Log::error('Error during TTS conversion: '.$e->getMessage());

            return;
        }

        if (!$audioData) {
            Log::warning('Failed to convert AI answer to speech.');

            return;
        }

        try {
            $audioPlaybackBackendAPI = new AudioPlaybackBackendAPI;
            $audioPlaybackBackendAPI->playAudio($audioData);
        } catch (Exception $e) {
            Log::error('Error during audio playback: '.$e->getMessage());

            return;
        }

        Log::info('AI answer playback completed.');

    }
}
