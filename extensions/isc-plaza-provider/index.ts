/**
 * InterSystems Plaza custom provider for Pi.
 *
 * This is an async factory so Pi awaits it before startup continues.
 * That means:
 *   - Models are discoverable via `pi --list-models` immediately.
 *   - The provider is ready before `session_start` fires.
 *   - Any startup error surfaces as a hard failure with a clear message.
 *
 * Auth flow (no OAuth):
 *   Read ~/.pi/agent/auth.json → auth["isc-plaza"].apiKey → Bearer token.
 *   The raw key string is passed to registerProvider() as a literal value
 *   (not an env-var name), so Pi uses it directly for every inference request.
 *
 * Model discovery:
 *   Call GET /models with the Bearer token, parse the OpenAI-compatible
 *   { data: [{ id }] } response, and register every model that has a
 *   non-empty string id.
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

// ─── Constants ────────────────────────────────────────────────────────────────

const PROVIDER_ID = "isc-plaza";
const PROVIDER_NAME = "InterSystems Plaza";
const BASE_URL = "https://plaza.iscinternal.com/genai/v1";
const AUTH_PATH = join(homedir(), ".pi", "agent", "auth.json");

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** Read and validate the API key from ~/.pi/agent/auth.json. */
function readApiKey(): string {
  if (!existsSync(AUTH_PATH)) {
    throw new Error(
      `[${PROVIDER_ID}] Auth file not found: ${AUTH_PATH}\n` +
        `Create it with the following content:\n` +
        `  {\n` +
        `    "${PROVIDER_ID}": {\n` +
        `      "apiKey": "<your-plaza-api-key>"\n` +
        `    }\n` +
        `  }`,
    );
  }

  let raw: string;
  try {
    raw = readFileSync(AUTH_PATH, "utf-8");
  } catch (err) {
    throw new Error(
      `[${PROVIDER_ID}] Could not read ${AUTH_PATH}: ${err instanceof Error ? err.message : String(err)}`,
    );
  }

  let auth: unknown;
  try {
    auth = JSON.parse(raw);
  } catch {
    throw new Error(
      `[${PROVIDER_ID}] ${AUTH_PATH} contains invalid JSON. ` +
        `Fix the file so it is valid JSON, e.g.:\n` +
        `  { "${PROVIDER_ID}": { "apiKey": "<your-plaza-api-key>" } }`,
    );
  }

  const apiKey = (auth as Record<string, unknown>)?.[PROVIDER_ID];
  if (typeof apiKey !== "object" || apiKey === null) {
    throw new Error(
      `[${PROVIDER_ID}] Missing "${PROVIDER_ID}" key in ${AUTH_PATH}.\n` +
        `Expected: { "${PROVIDER_ID}": { "apiKey": "..." } }`,
    );
  }

  const key = (apiKey as Record<string, unknown>).apiKey;
  if (typeof key !== "string" || key.trim() === "") {
    throw new Error(
      `[${PROVIDER_ID}] "apiKey" under "${PROVIDER_ID}" in ${AUTH_PATH} is missing or empty.\n` +
        `Expected: { "${PROVIDER_ID}": { "apiKey": "your-non-empty-key" } }`,
    );
  }

  return key;
}

/** Fetch the list of available models from the Plaza /models endpoint. */
async function fetchModels(apiKey: string): Promise<{ id: string }[]> {
  const url = `${BASE_URL}/models`;

  let response: Response;
  try {
    response = await fetch(url, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
  } catch (err) {
    throw new Error(
      `[${PROVIDER_ID}] Network error calling GET ${url}: ` +
        `${err instanceof Error ? err.message : String(err)}\n` +
        `Check that plaza.iscinternal.com is reachable from this machine.`,
    );
  }

  if (!response.ok) {
    throw new Error(
      `[${PROVIDER_ID}] GET ${url} failed with HTTP ${response.status} ${response.statusText}.\n` +
        `Verify that your apiKey in ${AUTH_PATH} is correct and has not expired.`,
    );
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new Error(
      `[${PROVIDER_ID}] GET ${url} returned a non-JSON body. ` +
        `The endpoint may be temporarily unavailable.`,
    );
  }

  const data = (payload as Record<string, unknown>)?.data;
  if (!Array.isArray(data)) {
    throw new Error(
      `[${PROVIDER_ID}] GET ${url} response is missing a "data" array. ` +
        `Received: ${JSON.stringify(payload).slice(0, 200)}`,
    );
  }

  // Keep only entries with a non-empty string id.
  const models = (data as unknown[]).filter(
    (entry): entry is { id: string } =>
      typeof (entry as Record<string, unknown>)?.id === "string" &&
      ((entry as Record<string, unknown>).id as string).trim() !== "",
  );

  if (models.length === 0) {
    throw new Error(
      `[${PROVIDER_ID}] GET ${url} returned no usable model ids. ` +
        `Ensure your Plaza account has access to at least one model.`,
    );
  }

  return models;
}

// ─── Extension factory ────────────────────────────────────────────────────────

/**
 * Async factory: Pi awaits this before startup continues.
 * Reads auth, discovers models, then registers the provider.
 */
export default async function (pi: ExtensionAPI) {
  // Step 1 – read and validate the API key from auth.json.
  const apiKey = readApiKey();

  // Step 2 – discover the available models at startup time.
  const discovered = await fetchModels(apiKey);

  // Step 3 – convert each discovered model id into a Pi model definition.
  const models = discovered.map((m) => ({
    id: m.id,
    // Use the raw id as the display name; Plaza ids are already descriptive
    // (e.g. "Qwen/Qwen3.5-35B-A3B-FP8").
    name: m.id,
    reasoning: false,
    input: ["text"] as ("text" | "image")[],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128000,
    maxTokens: 4096,
    // Compatibility flags for OpenAI-compatible endpoints.
    compat: {
      supportsUsageInStreaming: true,
      maxTokensField: "max_tokens" as const,
    },
  }));

  // Step 4 – register the provider with Pi.
  // `apiKey` is the literal key string (not an env-var name); Pi's
  // openai-completions implementation sends it as "Authorization: Bearer".
  pi.registerProvider(PROVIDER_ID, {
    name: PROVIDER_NAME,
    baseUrl: BASE_URL,
    apiKey,
    api: "openai-completions",
    models,
  });
}
