#!/usr/bin/env bash
set -euo pipefail
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Errore: python3 non disponibile' >&2
  exit 1
fi
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/readylinux/app"
BIN_DIR="$HOME/.local/bin"
mkdir -p -- "$APP_DIR" "$BIN_DIR"
install -m 644 -- "$SCRIPT_DIR/readylinux.py" "$APP_DIR/readylinux.py"
install -m 644 -- "$SCRIPT_DIR/ai_local.py" "$APP_DIR/ai_local.py"
install -m 644 -- "$SCRIPT_DIR/vibe.py" "$APP_DIR/vibe.py"
cat > "$BIN_DIR/readylinux" <<EOF
#!/usr/bin/env bash
exec python3 "${APP_DIR}/readylinux.py" "\$@"
EOF
chmod 755 "$BIN_DIR/readylinux"
echo "Installato: $BIN_DIR/readylinux"
echo 'Avvio: ~/.local/bin/readylinux'
echo 'IA locale opzionale: bash setup-ai-cpu.sh (richiede rete solo per installazione)'
echo 'Nessuna modifica a boot, login o servizi di sistema.'
