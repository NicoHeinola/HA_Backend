<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class APITokenAuthentication
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Get authorization token from request headers
        $apiToken = $request->header('Authorization');

        // Token is bearer so we need to strip the "Bearer " prefix
        if (str_starts_with($apiToken, 'Bearer ')) {
            $apiToken = substr($apiToken, 7);
        }

        // Compare it with the one in .env
        $ourAPIToken = config('auth.api_token');

        if ($apiToken !== $ourAPIToken) {
            return response()->json(['message' => 'Unauthorized'], Response::HTTP_UNAUTHORIZED);
        }

        return $next($request);
    }
}
