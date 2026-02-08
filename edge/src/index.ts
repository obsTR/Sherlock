export interface Env {
	BACKEND_URL: string;
	API_KEY: string;
}

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
		const url = new URL(request.url);

		// 1. Handle CORS Preflight
		if (request.method === "OPTIONS") {
			return new Response(null, {
				headers: {
					"Access-Control-Allow-Origin": "*",
					"Access-Control-Allow-Methods": "GET, POST, OPTIONS",
					"Access-Control-Allow-Headers": "Content-Type, X-API-KEY",
				},
			});
		}

		// 2. Authentication Check
		// We expect an 'X-API-KEY' header
		const apiKey = request.headers.get("X-API-KEY");
		const validApiKey = env.API_KEY || "dev-secret-key"; // Fallback for dev

		if (!apiKey || apiKey !== validApiKey) {
			return new Response(JSON.stringify({ error: "Unauthorized: Invalid or missing API Key" }), {
				status: 401,
				headers: { "Content-Type": "application/json" },
			});
		}

		// 3. Request Forwarding (Proxy)
		// We forward the request to the Python Backend
		try {
			// Construct the target URL
			// Example: request path "/api/v1/analyze" -> backend "/api/v1/analyze"
			const targetUrl = `${env.BACKEND_URL}${url.pathname}${url.search}`;

			// Create a new request to send to the backend
			// We clone the body and headers
			const newRequest = new Request(targetUrl, {
				method: request.method,
				headers: request.headers,
				body: request.body,
			});

			// Fetch from the backend
			const response = await fetch(newRequest);

			// Return the response to the client
			// We can inspect or log the response here if needed
			return response;

		} catch (e: any) {
			return new Response(JSON.stringify({ error: `Gateway Error: ${e.message}` }), {
				status: 502,
				headers: { "Content-Type": "application/json" },
			});
		}
	},
};



