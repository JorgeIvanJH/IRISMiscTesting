/**
 * AWS Bedrock bearer-token provider for Pi.
 *
 * Problem this solves:
 *   Pi's built-in `amazon-bedrock` provider authenticates via the env var
 *   AWS_BEARER_TOKEN_BEDROCK, which users normally must `export` in their
 *   shell before starting Pi.  This extension reads that token from
 *   ~/.pi/agent/auth.json instead, so no shell export is required.
 *
 * How it works:
 *   1. Reads ~/.pi/agent/auth.json and extracts auth["aws-bedrock"].apiKey.
 *   2. Sets process.env.AWS_BEARER_TOKEN_BEDROCK to that value.
 *      Pi's built-in auth check (getEnvApiKey) reads that variable, so all
 *      built-in amazon-bedrock models appear as available.
 *      Pi's built-in Bedrock streaming code (streamBedrock) also reads that
 *      variable and sends it as "Authorization: Bearer" on every request.
 *   3. That's it.  No custom streaming implementation, no model list to
 *      maintain — everything comes from Pi's built-in amazon-bedrock provider.
 *
 * The factory is synchronous: there is no network call at startup (unlike the
 * Plaza extension).  Pi still awaits sync factories before startup continues,
 * so any error here surfaces as a hard startup failure with a clear message.
 *
 * Auth file shape (~/.pi/agent/auth.json):
 *   {
 *     "aws-bedrock": {
 *       "apiKey": "<your-bearer-token>"
 *     }
 *   }
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

// ─── Constants ────────────────────────────────────────────────────────────────

const AUTH_KEY = "aws-bedrock";
const ENV_VAR = "AWS_BEARER_TOKEN_BEDROCK";
const AUTH_PATH = join(homedir(), ".pi", "agent", "auth.json");

// ─── Auth helper ─────────────────────────────────────────────────────────────

/**
 * Read and validate the bearer token from ~/.pi/agent/auth.json.
 * Returns the raw token string on success; throws with an actionable message
 * on any failure.
 */
function readBearerToken(): string {
  if (!existsSync(AUTH_PATH)) {
    throw new Error(
      `[${AUTH_KEY}] Auth file not found: ${AUTH_PATH}\n` +
        `Create it with the following content:\n` +
        `  {\n` +
        `    "${AUTH_KEY}": {\n` +
        `      "apiKey": "<your-bedrock-bearer-token>"\n` +
        `    }\n` +
        `  }`,
    );
  }

  let raw: string;
  try {
    raw = readFileSync(AUTH_PATH, "utf-8");
  } catch (err) {
    throw new Error(
      `[${AUTH_KEY}] Could not read ${AUTH_PATH}: ` +
        `${err instanceof Error ? err.message : String(err)}`,
    );
  }

  let auth: unknown;
  try {
    auth = JSON.parse(raw);
  } catch {
    throw new Error(
      `[${AUTH_KEY}] ${AUTH_PATH} contains invalid JSON. ` +
        `Fix the file so it is valid JSON, e.g.:\n` +
        `  { "${AUTH_KEY}": { "apiKey": "<your-bedrock-bearer-token>" } }`,
    );
  }

  const section = (auth as Record<string, unknown>)?.[AUTH_KEY];
  if (typeof section !== "object" || section === null) {
    throw new Error(
      `[${AUTH_KEY}] Missing "${AUTH_KEY}" key in ${AUTH_PATH}.\n` +
        `Expected: { "${AUTH_KEY}": { "apiKey": "..." } }`,
    );
  }

  const token = (section as Record<string, unknown>).apiKey;
  if (typeof token !== "string" || token.trim() === "") {
    throw new Error(
      `[${AUTH_KEY}] "apiKey" under "${AUTH_KEY}" in ${AUTH_PATH} is missing or empty.\n` +
        `Expected: { "${AUTH_KEY}": { "apiKey": "your-non-empty-token" } }`,
    );
  }

  return token;
}

// ─── Extension factory ────────────────────────────────────────────────────────

/**
 * Synchronous factory — Pi awaits it before startup continues.
 *
 * The only job here is to set AWS_BEARER_TOKEN_BEDROCK from auth.json.
 * Pi's built-in amazon-bedrock provider:
 *   - uses that env var in its auth check, so models appear as available.
 *   - passes it as "Authorization: Bearer" on every Converse API call.
 * No registerProvider() call is needed; the built-in model list is unchanged.
 */
export default function (_pi: ExtensionAPI) {
  // If the token is already present in the environment (user exported it
  // manually), respect that and skip auth.json — don't override their shell.
  if (process.env[ENV_VAR]) {
    return;
  }

  // Read the token from auth.json and inject it into the process environment.
  // This is functionally equivalent to `export AWS_BEARER_TOKEN_BEDROCK=<token>`
  // but sourced from auth.json rather than the shell.
  const token = readBearerToken();
  process.env[ENV_VAR] = token;
}
