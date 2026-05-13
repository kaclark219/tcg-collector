function withExtensionCandidate(url: string, extension: "png" | "webp"): string {
  const trimmed = url.trim().replace(/^['"]|['"]$/g, "").replace(/\/+$/g, "");

  if (!trimmed.includes("assets.tcgdex.net")) {
    return trimmed;
  }

  if (/\.(png|jpg|jpeg|webp)$/i.test(trimmed)) {
    return trimmed.replace(/\.(png|jpg|jpeg|webp)$/i, `.${extension}`);
  }

  return `${trimmed}/high.${extension}`;
}

export function normalizeTcgdexImageUrl(imageUrl?: string): string | undefined {
  if (!imageUrl) {
    return undefined;
  }

  return withExtensionCandidate(imageUrl, "png");
}

export function buildTcgdexImageCandidates(imageUrl?: string): string[] {
  if (!imageUrl) {
    return [];
  }

  const trimmed = imageUrl.trim().replace(/^['"]|['"]$/g, "").replace(/\/+$/g, "");
  const candidates = [trimmed];

  if (trimmed.includes("assets.tcgdex.net")) {
    candidates.push(withExtensionCandidate(trimmed, "png"));
    candidates.push(withExtensionCandidate(trimmed, "webp"));
  }

  return [...new Set(candidates)];
}
