<?php

namespace App\Http\Controllers;

use App\Http\Requests\ActionRunner\RunActionRequest;
use App\Jobs\RunActionJob;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Log;

class ActionRunnerController extends Controller
{
    public function runAction(RunActionRequest $request)
    {
        $data = $request->validated();

        RunActionJob::dispatch($data['action']);

        Log::info('Dispatched RunActionJob', $data['action']);

        return Response::HTTP_OK;
    }
}
