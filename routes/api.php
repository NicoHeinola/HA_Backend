<?php

declare(strict_types=1);

use App\Http\Controllers\ActionRunnerController;
use App\Http\Controllers\AIPlaybackController;
use App\Http\Middleware\APITokenAuthentication;
use Illuminate\Support\Facades\Route;

Route::middleware([APITokenAuthentication::class])->group(function ($route) {
    $route->post('action-runner/run-action', [ActionRunnerController::class, 'runAction']);
    $route->post('/ai/playback', [AIPlaybackController::class, 'playback']);
});
