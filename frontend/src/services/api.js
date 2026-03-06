/**
 * Founder Copilot — API Service
 * Handles all communication with the FastAPI backend.
 */

const API_BASE = '/api';

/**
 * Generic API call helper
 */
async function apiCall(endpoint, body) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Generate a Startup Plan
 */
export async function generateStartupPlan(idea, model = 'pro') {
  return apiCall('/generate/startup-plan', { idea, model });
}

/**
 * Generate Technical Architecture
 */
export async function generateTechArchitecture(productDescription, model = 'pro') {
  return apiCall('/generate/tech-architecture', {
    product_description: productDescription,
    model,
  });
}

/**
 * Generate GitHub Issues
 */
export async function generateGitHubIssues(
  productName,
  productDescription,
  techStack = 'To be determined',
  model = 'pro'
) {
  return apiCall('/generate/github-issues', {
    product_name: productName,
    product_description: productDescription,
    tech_stack: techStack,
    model,
  });
}

/**
 * Generate Pitch Deck
 */
export async function generatePitchDeck(idea, productDescription = '', model = 'pro') {
  return apiCall('/generate/pitch-deck', {
    idea,
    product_description: productDescription,
    model,
  });
}

/**
 * Auto-detect feature and generate
 */
export async function autoGenerate(message, model = 'pro', context = null) {
  return apiCall('/generate/auto', { message, model, context });
}

/**
 * Stream generation (SSE)
 */
export async function streamGenerate(feature, message, model = 'pro', onChunk) {
  const response = await fetch(`${API_BASE}/generate/stream/${feature}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, model }),
  });

  if (!response.ok) {
    throw new Error(`Stream error: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') return;
        try {
          const parsed = JSON.parse(data);
          if (parsed.text) onChunk(parsed.text);
          if (parsed.error) throw new Error(parsed.error);
        } catch (e) {
          if (e.message !== 'Unexpected end of JSON input') {
            // Ignore incomplete JSON
          }
        }
      }
    }
  }
}

/**
 * Health check
 */
export async function healthCheck() {
  const response = await fetch('/health');
  return response.json();
}
