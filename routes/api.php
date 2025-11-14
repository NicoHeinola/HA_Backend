<?php

use App\Http\Controllers\ActionRunnerController;
use App\Http\Middleware\APITokenAuthentication;
use Illuminate\Support\Facades\Route;

Route::middleware([APITokenAuthentication::class])->group(function ($route) {
    $route->post('action-runner/run-action', [ActionRunnerController::class, 'runAction']);
});
