<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Log;

class RunActionJob implements ShouldQueue
{
    use Queueable;

    protected array $action;

    public function __construct(array $action)
    {
        $this->action = $action;
    }

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Running action', $this->action);
    }
}
