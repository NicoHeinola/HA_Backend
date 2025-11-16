<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Http\Requests\AIPlaybackRequest;
use App\Jobs\PlaybackAIAnswerJob;
use Illuminate\Http\JsonResponse;

class AIPlaybackController extends Controller
{
    public function playback(AIPlaybackRequest $request): JsonResponse
    {
        $aiAnswer = $request->input('ai_answer');
        dispatch(new PlaybackAIAnswerJob($aiAnswer));

        return response()->json(['status' => 'Playback job dispatched.']);
    }
}
