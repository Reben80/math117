#!/usr/bin/env node
/** Build-time KaTeX: HTML only (no MathML), so slide players never show a second broken math layer. */
const katex = require("katex");
const display = process.argv[2] === "1";
let latex = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  latex += chunk;
});
process.stdin.on("end", () => {
  process.stdout.write(
    katex.renderToString(latex, {
      throwOnError: true,
      displayMode: display,
      strict: "ignore",
      output: "html",
      trust: false,
    })
  );
});
