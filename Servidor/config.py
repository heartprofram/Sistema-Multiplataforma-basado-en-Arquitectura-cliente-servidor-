import os

# Database
DATABASE_URL = "sqlite:///./sigep.db"

# Server
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
LOG_LEVEL = "info"

# GUI
THEME = "Light"
APP_TITLE = "SIGEP 2.0 - Sistema Integral"
APP_GEOMETRY = "1200x750"
REFRESH_INTERVAL_MS = 2000

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "server.log"
