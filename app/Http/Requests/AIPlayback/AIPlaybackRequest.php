<?php

declare(strict_types=1);

namespace App\Http\Requests\AIPlayback;

use Illuminate\Foundation\Http\FormRequest;

class AIPlaybackRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'ai_answer' => 'required|string',
        ];
    }
}
