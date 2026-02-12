#!/bin/bash
set -e

REPO_URL="https://github.com/CREAsTIVE/regru-set-ip.git"
INSTALL_DIR="/opt/regru-set-ip"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="regru-set-ip"
LINK_PATH="/usr/local/bin/$SCRIPT_NAME"

echo "Installing regru-set-ip from $REPO_URL"

# Check for git and python3
command -v git >/dev/null 2>&1 || { echo "Error: git is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required"; exit 1; }

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo "Directory $INSTALL_DIR already exists. Pulling latest changes..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository to $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create virtual environment
echo "Creating Python virtual environment..."
cd "$INSTALL_DIR"

python3 -m venv venv
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

sudo tee "$WRAPPER_PATH" > /dev/null <<EOF
#!/bin/bash
exec "$VENV_DIR/bin/python" "$PYTHON_SCRIPT" "\$@"
EOF

sudo chmod +x "$WRAPPER_PATH"

echo ""
echo "Installation complete!"
echo "You can now run 'regru-set-ip' from anywhere."
echo "Configuration file: $INSTALL_DIR/.env"