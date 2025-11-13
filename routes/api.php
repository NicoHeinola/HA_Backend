<?php

use App\Http\Controllers\ActionRunnerController;
use Illuminate\Support\Facades\Route;

Route::post('action-runner/run-action', [ActionRunnerController::class, 'runAction']);
