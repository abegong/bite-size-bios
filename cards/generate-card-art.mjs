#!/usr/bin/env node
// Generate employee-card character art with the OpenAI Images API.
//
// Reads a roster of employees, pairs each employee's reference photos with a
// shared set of style-reference images, and asks the OpenAI Images API to
// produce card art that matches the style while preserving the employee's
// likeness. Run with --dry-run to inspect every request before spending API
// credits.

import { existsSync } from "node:fs";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";
import { parse as parseToml } from "smol-toml";

const API_URL = "https://api.openai.com/v1/images";
const DEFAULT_MODEL = "gpt-image-2";
const DEFAULT_SIZE = "1024x1024";
const DEFAULT_QUALITY = "high";
const DEFAULT_FORMAT = "png";
const IMAGE_MIME_TYPES = new Map([
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".webp", "image/webp"],
]);
const RETRYABLE_STATUS = new Set([429, 500, 502, 503, 504]);
const MAX_ATTEMPTS = 4;

const DEFAULT_STYLE = `Stylized character-portrait illustration with clean shapes, confident line
work, and a simple flat background. Friendly and professional, readable at
small card size.`;

const SUBJECT_REFERENCE_PARAGRAPH = (which, name) =>
  `The ${which} attached image(s) are reference photos of ${name}. Use them only
to capture likeness: facial structure, hair, skin tone, glasses or facial
hair, and overall build. Make the final image an original illustration, not
a photographic copy of any single reference.`;

const STYLE_REFERENCE_PARAGRAPH = (which) =>
  `The ${which} attached image(s) are style references from the existing card
set. Match their artistic style, rendering technique, palette, background
treatment, and level of detail exactly, so the new card feels like part of
the same set. Do not borrow faces, identity, or clothing from the style
references.`;

const AVOID_PARAGRAPH = `Avoid: text, captions, name tags, logos, watermarks, frames, extra people,
distorted anatomy, busy background.`;

const cardsRoot = path.dirname(fileURLToPath(import.meta.url));

function fail(message) {
  console.error(message);
  process.exit(1);
}

async function loadRoster(rosterPath) {
  if (!existsSync(rosterPath)) {
    fail(`Roster file not found: ${rosterPath}`);
  }
  return parseToml(await readFile(rosterPath, "utf-8"));
}

async function discoverImages(directory) {
  let entries;
  try {
    entries = await readdir(directory, { withFileTypes: true });
  } catch {
    return [];
  }
  return entries
    .filter(
      (entry) =>
        entry.isFile() && IMAGE_MIME_TYPES.has(path.extname(entry.name).toLowerCase()),
    )
    .map((entry) => path.join(directory, entry.name))
    .sort();
}

async function employeeReferences(employee) {
  if (employee.references?.length) {
    return employee.references.map((item) => path.join(cardsRoot, item));
  }
  return discoverImages(path.join(cardsRoot, "employees", employee.slug));
}

function buildPrompt(employee, style, subjectCount, styleCount) {
  if (employee.prompt) {
    return String(employee.prompt).trim();
  }

  const name = employee.name || employee.slug;
  const roleClause = employee.role ? `, ${employee.role},` : "";

  const paragraphs = [
    `Create a square character portrait of ${name}${roleClause} for an employee trading card.`,
  ];

  if (subjectCount) {
    const which = styleCount ? `first ${subjectCount}` : "attached";
    paragraphs.push(SUBJECT_REFERENCE_PARAGRAPH(which, name));
  }
  if (styleCount) {
    const which = subjectCount ? `remaining ${styleCount}` : "attached";
    paragraphs.push(STYLE_REFERENCE_PARAGRAPH(which));
  }

  paragraphs.push(`Style: ${style.trim()}`);

  const background = styleCount
    ? "simple background consistent with the style references"
    : "simple flat background";
  paragraphs.push(
    "Composition: centered head-and-shoulders bust portrait, square crop, " +
      "face clearly readable at card-thumbnail size, generous margin around " +
      `the head, ${background}.`,
  );

  if (employee.notes) {
    paragraphs.push(`Subject details: ${employee.notes}`);
  }

  paragraphs.push(AVOID_PARAGRAPH);
  return paragraphs.join("\n\n");
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function performRequest(url, options) {
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    let response;
    try {
      response = await fetch(url, options);
    } catch (error) {
      if (attempt < MAX_ATTEMPTS) {
        const delay = 2 ** attempt;
        console.error(
          `  Network error (${error.cause?.code ?? error.message}); retrying in ` +
            `${delay}s (attempt ${attempt}/${MAX_ATTEMPTS})`,
        );
        await sleep(delay * 1000);
        continue;
      }
      fail(`OpenAI API request failed: ${error.message}`);
    }

    if (response.ok) {
      return response.json();
    }
    const details = await response.text();
    if (RETRYABLE_STATUS.has(response.status) && attempt < MAX_ATTEMPTS) {
      const delay = 2 ** attempt;
      console.error(
        `  OpenAI returned ${response.status}; retrying in ${delay}s ` +
          `(attempt ${attempt}/${MAX_ATTEMPTS})`,
      );
      await sleep(delay * 1000);
      continue;
    }
    fail(`OpenAI API request failed: ${response.status} ${response.statusText}\n${details}`);
  }
  fail("OpenAI API request failed after retries.");
}

async function callImagesApi(apiKey, prompt, images, settings) {
  const fields = {
    model: settings.model,
    prompt,
    size: settings.size,
    quality: settings.quality,
    output_format: settings.outputFormat,
    background: "opaque",
  };

  let url;
  let body;
  const headers = { Authorization: `Bearer ${apiKey}` };

  if (images.length) {
    url = `${API_URL}/edits`;
    body = new FormData();
    for (const [name, value] of Object.entries(fields)) {
      body.append(name, value);
    }
    for (const imagePath of images) {
      const mime = IMAGE_MIME_TYPES.get(path.extname(imagePath).toLowerCase());
      const blob = new Blob([await readFile(imagePath)], { type: mime });
      body.append("image[]", blob, path.basename(imagePath));
    }
  } else {
    url = `${API_URL}/generations`;
    body = JSON.stringify(fields);
    headers["Content-Type"] = "application/json";
  }

  const response = await performRequest(url, { method: "POST", headers, body });

  const b64 = response?.data?.[0]?.b64_json;
  if (typeof b64 !== "string") {
    fail("OpenAI response did not include data[0].b64_json.");
  }
  return Buffer.from(b64, "base64");
}

function outputPaths(artDir, slug, outputFormat, variants) {
  const ext = outputFormat === "jpeg" ? "jpg" : outputFormat;
  if (variants === 1) {
    return [path.join(artDir, `${slug}.${ext}`)];
  }
  return Array.from({ length: variants }, (_, index) =>
    path.join(artDir, `${slug}-v${index + 1}.${ext}`),
  );
}

const relativeToRoot = (filePath) =>
  filePath.startsWith(cardsRoot + path.sep)
    ? path.relative(cardsRoot, filePath)
    : filePath;

async function updateManifest(manifestPath, slug, entry) {
  let manifest = {};
  if (existsSync(manifestPath)) {
    manifest = JSON.parse(await readFile(manifestPath, "utf-8"));
  }
  (manifest[slug] ??= []).push(entry);
  await mkdir(path.dirname(manifestPath), { recursive: true });
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
}

function parseCliArgs() {
  const { values } = parseArgs({
    options: {
      roster: { type: "string" },
      only: { type: "string", multiple: true, default: [] },
      force: { type: "boolean", default: false },
      variants: { type: "string", default: "1" },
      "dry-run": { type: "boolean", default: false },
      help: { type: "boolean", default: false },
    },
  });
  if (values.help) {
    console.log(`Usage: node generate-card-art.mjs [options]

Options:
  --roster PATH   Path to the roster TOML file (default: cards/roster.toml).
  --only SLUG     Generate art only for this employee slug. Repeat for several.
  --force         Regenerate art even when the output file already exists.
  --variants N    Number of variants to generate per employee (default: 1).
  --dry-run       Print the planned requests without calling the OpenAI API.`);
    process.exit(0);
  }
  const variants = Number.parseInt(values.variants, 10);
  if (!Number.isInteger(variants) || variants < 1) {
    fail(`--variants must be a positive integer, got: ${values.variants}`);
  }
  return { ...values, variants, dryRun: values["dry-run"] };
}

async function main() {
  const args = parseCliArgs();
  const rosterPath = args.roster
    ? path.resolve(args.roster)
    : path.join(cardsRoot, "roster.toml");
  const roster = await loadRoster(rosterPath);

  const defaults = roster.defaults ?? {};
  const settings = {
    model: String(defaults.model ?? DEFAULT_MODEL),
    size: String(defaults.size ?? DEFAULT_SIZE),
    quality: String(defaults.quality ?? DEFAULT_QUALITY),
    outputFormat: String(defaults.output_format ?? DEFAULT_FORMAT),
  };
  const style = String(defaults.style ?? DEFAULT_STYLE);
  const styleDir = path.join(
    cardsRoot,
    String(defaults.style_reference_dir ?? "style-references"),
  );
  const artDir = path.join(cardsRoot, String(defaults.output_dir ?? "art"));

  const styleReferences = await discoverImages(styleDir);

  let employees = roster.employees ?? [];
  if (!employees.length) {
    fail(`No [[employees]] entries found in ${rosterPath}.`);
  }

  if (args.only.length) {
    const known = new Set(employees.map((employee) => employee.slug));
    const missing = args.only.filter((slug) => !known.has(slug));
    if (missing.length) {
      fail(`Unknown slug(s) in --only: ${missing.join(", ")}`);
    }
    employees = employees.filter((employee) => args.only.includes(employee.slug));
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey && !args.dryRun) {
    fail("Set OPENAI_API_KEY before running this script.");
  }

  let generated = 0;
  let skipped = 0;
  for (const employee of employees) {
    const slug = String(employee.slug);
    const references = await employeeReferences(employee);
    for (const imagePath of [...references, ...styleReferences]) {
      if (!existsSync(imagePath)) {
        fail(`Reference image not found: ${imagePath}`);
      }
    }

    if (!references.length) {
      console.error(
        `warning: no reference photos found for ${slug} in ` +
          `${path.join(cardsRoot, "employees", slug)}; likeness will be invented`,
      );
    }

    const prompt = buildPrompt(employee, style, references.length, styleReferences.length);
    const images = [...references, ...styleReferences];
    const outputs = outputPaths(artDir, slug, settings.outputFormat, args.variants);

    for (const output of outputs) {
      if (existsSync(output) && !args.force) {
        console.log(`skip ${path.basename(output)} (exists; use --force to regenerate)`);
        skipped += 1;
        continue;
      }

      if (args.dryRun) {
        const endpoint = images.length ? "edits" : "generations";
        console.log(`--- ${slug} -> ${output}`);
        console.log(`endpoint: ${API_URL}/${endpoint}`);
        console.log(
          `model: ${settings.model}  size: ${settings.size}  quality: ${settings.quality}`,
        );
        console.log("subject references:");
        for (const imagePath of references) {
          console.log(`  - ${imagePath}`);
        }
        console.log("style references:");
        for (const imagePath of styleReferences) {
          console.log(`  - ${imagePath}`);
        }
        console.log("prompt:");
        console.log(prompt.replace(/^/gm, "  "));
        continue;
      }

      console.log(`generating ${path.basename(output)} ...`);
      const imageBytes = await callImagesApi(apiKey, prompt, images, settings);
      await mkdir(path.dirname(output), { recursive: true });
      await writeFile(output, imageBytes);
      generated += 1;
      console.log(`wrote ${output}`);

      await updateManifest(path.join(artDir, "manifest.json"), slug, {
        generated_at: new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00"),
        output: relativeToRoot(output),
        model: settings.model,
        size: settings.size,
        quality: settings.quality,
        subject_references: references.map(relativeToRoot),
        style_references: styleReferences.map(relativeToRoot),
        prompt,
      });
    }
  }

  if (!args.dryRun) {
    console.log(`done: ${generated} generated, ${skipped} skipped`);
  }
}

await main();
