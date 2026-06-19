#!/bin/bash
set -e

iris session IRIS <<'EOF'

Write "STARTING IRIS CONFIGURATION...",!


Write "IRIS CONFIGURATION COMPLETED.",!
halt
EOF
