import sys
import subprocess
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/dbsync")
async def dbsync():
    """
    Sync the database models with the database using Alembic.
    """
    try:
        # Auto-generate migration script
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "sync"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Alembic Revision Output:", result.stdout)

        # Apply the migration
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Alembic Upgrade Output:", result.stdout)

        return {"message": "Database synchronized successfully!"}

    except subprocess.CalledProcessError as e:
        # Log the error output
        print("Subprocess Error:", e.stderr)

        # Provide a meaningful error response
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Alembic command failed",
                "command": e.cmd,
                "returncode": e.returncode,
                "stderr": e.stderr,
            },
        )

    except FileNotFoundError as e:
        # Handle the case where Alembic or Python executable is missing
        print("File Not Found Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Required executable not found",
                "message": str(e),
            },
        )

    except Exception as e:
        # Catch any unexpected errors
        print("Unexpected Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error": "An unexpected error occurred",
                "message": str(e),
            },
        )
