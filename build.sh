#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# strip the platform-injected script tag and any stray html wrappers
sed '/sites.super.myninja.ai/d' src/body.html > /tmp/body.clean
sed '/sites.super.myninja.ai/d' src/app.html  > /tmp/app.clean

cat > index.html <<'HEAD'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#04060c">
<title>Global Pilgrim — Autonomous Financial Engine</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 2 4 6v6c0 5 3.4 8.4 8 10 4.6-1.6 8-5 8-10V6l-8-4Z' fill='none' stroke='%23e8c65a' stroke-width='1.6'/></svg>">
<style>
HEAD

cat src/styles.css >> index.html

cat >> index.html <<'MID'
</style>
</head>
<body>
MID

cat /tmp/body.clean >> index.html
cat /tmp/app.clean  >> index.html

cat >> index.html <<'JS'
<script>
JS

cat src/core.js src/ui.js src/engines.js >> index.html

cat >> index.html <<'END'
</script>
</body>
</html>
END

# syntax check the javascript payload
cat src/core.js src/ui.js src/engines.js > /tmp/bundle.js
node --check /tmp/bundle.js
echo "index.html built: $(wc -c < index.html) bytes"
