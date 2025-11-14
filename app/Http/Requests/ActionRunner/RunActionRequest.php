<?php

declare(strict_types=1);

namespace App\Http\Requests\ActionRunner;

use Illuminate\Foundation\Http\FormRequest;

class RunActionRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'action' => ['required', 'array'],
            'action.name' => ['required', 'string'],
            'action.params' => ['sometimes', 'array'],

            'ai_answer' => ['sometimes', 'string'],
        ];
    }
}
