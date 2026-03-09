import uvicorn
import sys
from pathlib import Path

# Ensure the backend directory is in the path
sys.path.insert(0, str(Path(__file__).parent))

from server import app

if __name__ == "__main__":
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
