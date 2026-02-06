"""
Backwards-compatible entrypoint.

The refactored implementation lives in `app/main.py`.
"""

from app.main import main, process_claim  # noqa: F401

if __name__ == "__main__":
    main()
