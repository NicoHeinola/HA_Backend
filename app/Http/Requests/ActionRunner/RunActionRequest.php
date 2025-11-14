<?php

namespace App\Http\Requests\ActionRunner;

use Illuminate\Foundation\Http\FormRequest;

class RunActionRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'action' => ['required', 'array'],
        ];
    }
}
