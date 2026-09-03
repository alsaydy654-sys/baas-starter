import os
import subprocess
import sys


def test_required_environment_validation():
    env = os.environ.copy()
    for key in ("DATABASE_URL", "APP_ENV", "API_PORT", "FRONTEND_URL"):
        env.pop(key, None)
    result = subprocess.run([sys.executable, "-c", "import backend.server"], env=env, capture_output=True, text=True)
    assert result.returncode != 0