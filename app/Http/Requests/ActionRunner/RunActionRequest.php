<?php

declare(strict_types=1);

namespace App\Http\Requests\ActionRunner;

use Illuminate\Foundation\Http\FormRequest;

class RunActionRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'action' => ['required', 'string'],
            'params' => ['sometimes', 'nullable', 'array'],
        ];
    }
}
