<?php

namespace App\Http\Requests\ActionRunner;

use Illuminate\Foundation\Http\FormRequest;

class RunActionRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'action' => ['required', 'array'],
            'action.name' => ['required', 'string'],
            'action.ai_answer' => ['sometimes', 'string'],
            'action.params' => ['sometimes', 'array'],
        ];
    }
}
