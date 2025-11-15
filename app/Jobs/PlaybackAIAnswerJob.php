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
        Log::info('Playing AI answer.');

        try {
            $audioBackendAPI = new AudioBackendAPI;
            $audioData = $audioBackendAPI->convertTextToSpeech($this->aiAnswer);

            if (!$audioData) {
                Log::warning('Failed to convert AI answer to speech.');

                return;
            }

            // Make the audio more "human like"
            $audioData = $audioBackendAPI->speedUpAudio($audioData, 1.20);

            $audioPlaybackBackendAPI = new AudioPlaybackBackendAPI;
            $audioPlaybackBackendAPI->playAudio($audioData);
        } catch (Exception $e) {
            Log::error('Error during AI answer playback: '.$e->getMessage());
        }
    }
}
