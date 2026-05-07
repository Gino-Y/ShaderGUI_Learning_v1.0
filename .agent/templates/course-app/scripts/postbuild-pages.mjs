import { copyFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const distDir = join(process.cwd(), "dist");

copyFileSync(join(distDir, "index.html"), join(distDir, "404.html"));
writeFileSync(join(distDir, ".nojekyll"), "");

