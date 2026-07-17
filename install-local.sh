#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
ICON_ROOT="$HOME/.local/share/icons/hicolor"
VEILSHOT_DATA_DIR="$HOME/.local/share/veilshot"
LAUNCHER="$BIN_DIR/veilshot"
DESKTOP_FILE="$APP_DIR/veilshot.desktop"
AUTOSTART_FILE="$AUTOSTART_DIR/veilshot-tray.desktop"
APP_ICON_SOURCE="$PROJECT_DIR/src/veilshot/assets/veilshot.svg"
TRAY_ICON_SOURCE="$PROJECT_DIR/src/veilshot/assets/veilshot-tray-22.png"
TRAY_LOG="${XDG_RUNTIME_DIR:-/tmp}/veilshot-tray.log"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Missing $VENV_DIR. First run: ./setup.sh" >&2
  exit 1
fi

for file in \
  "$APP_ICON_SOURCE" \
  "$TRAY_ICON_SOURCE" \
  "$PROJECT_DIR/packaging/veilshot.desktop.in" \
  "$PROJECT_DIR/packaging/veilshot-tray.desktop.in"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
done

mkdir -p \
  "$BIN_DIR" \
  "$APP_DIR" \
  "$AUTOSTART_DIR" \
  "$ICON_ROOT/scalable/apps" \
  "$ICON_ROOT/48x48/apps" \
  "$ICON_ROOT/128x128/apps" \
  "$ICON_ROOT/256x256/apps" \
  "$VEILSHOT_DATA_DIR"

cat > "$LAUNCHER" <<LAUNCHER
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" -m veilshot "\$@"
LAUNCHER
chmod +x "$LAUNCHER"

install -m 0644 "$APP_ICON_SOURCE" "$ICON_ROOT/scalable/apps/veilshot.svg"
install -m 0644 "$PROJECT_DIR/src/veilshot/assets/veilshot-48.png" "$ICON_ROOT/48x48/apps/veilshot.png"
install -m 0644 "$PROJECT_DIR/src/veilshot/assets/veilshot-128.png" "$ICON_ROOT/128x128/apps/veilshot.png"
install -m 0644 "$PROJECT_DIR/src/veilshot/assets/veilshot-256.png" "$ICON_ROOT/256x256/apps/veilshot.png"
install -m 0644 "$TRAY_ICON_SOURCE" "$VEILSHOT_DATA_DIR/veilshot-tray.png"

sed "s|@VEILSHOT_LAUNCHER@|$LAUNCHER|g" \
  "$PROJECT_DIR/packaging/veilshot.desktop.in" > "$DESKTOP_FILE"
chmod 0644 "$DESKTOP_FILE"

sed "s|@VEILSHOT_LAUNCHER@|$LAUNCHER|g" \
  "$PROJECT_DIR/packaging/veilshot-tray.desktop.in" > "$AUTOSTART_FILE"
chmod 0644 "$AUTOSTART_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -t "$ICON_ROOT" >/dev/null 2>&1 || true
fi

# Stop an older tray instance, then start the installed one.
pkill -f "$VENV_DIR/bin/python -m veilshot --tray" 2>/dev/null || true
: > "$TRAY_LOG"
nohup "$LAUNCHER" --tray >"$TRAY_LOG" 2>&1 &
TRAY_PID=$!
sleep 1

VERSION="$($LAUNCHER --version 2>/dev/null || true)"
echo "Installed Veilshot version: ${VERSION:-unknown}"
echo "Installed launcher: $LAUNCHER"
echo "Installed application entry: $DESKTOP_FILE"
echo "Installed autostart entry: $AUTOSTART_FILE"
echo "Installed app icons under: $ICON_ROOT"

if kill -0 "$TRAY_PID" 2>/dev/null; then
  echo "Tray process started (PID $TRAY_PID)."
else
  echo "WARNING: tray process exited. Diagnostic log:" >&2
  if [[ -s "$TRAY_LOG" ]]; then
    cat "$TRAY_LOG" >&2
  else
    echo "  $TRAY_LOG is empty" >&2
  fi
fi

echo "Global screenshot shortcut command: $LAUNCHER"
echo "Application-menu launch command: $LAUNCHER --tray"
