<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;

class ActionRunnerController extends Controller
{
    public function runAction(Request $request)
    {
        return Response::HTTP_OK;
    }
}
