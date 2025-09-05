import sys
import tempfile
import shutil
from pathlib import Path as PathLib
from typing import Optional, Dict, Any

import fal
from pydantic import BaseModel, Field
from fal.toolkit import File
from fastapi import HTTPException


# important:
# - don't import stuff at the top level, especially pytorch.
# - if you need to import local modules, the easiest way is to clone the repo into the data directory and
#   dynamically import them into the system, using sys.path.insert(0, str(repo_path))
# - anything you download will be permanently cached, so before downloading anything, remember to check the data
#   directory to see if you've already downloaded something

# EXTREMELY IMPORTANT:
# - the data directory is shared between all apps, so be careful not to overwrite files from other apps,
#   so use the APP_DATA_DIR constant to access the data directory and make sure your app id is unique


APP_ID = "put-your-app-id-here"  # same id as in pyproject.toml
APP_DATA_DIR = f"/data/apps/{APP_ID}"
MACHINE_TYPE = "M"  # M is CPU; if you need a GPU, use "GPU-H100" or "GPU-A100"


class Input(BaseModel):
    some_string_prop: str = Field(description="Some string prop")
    some_numeric_prop: int = Field(default=1337, description="Some numeric prop")


class Output(BaseModel):
    some_output_prop: str = Field(description="Some output prop")
    another_output_prop: int = Field(description="Another output prop")


class FalApp(fal.App, name=APP_ID, keep_alive=0, min_concurrency=0, max_concurrency=10):
    machine_type = MACHINE_TYPE
    requirements = [
        # Add your dependencies here
        "Pillow",
    ]

    def setup(self):
        """Initialize the app"""

        print(f"Setting up {APP_ID}...")

        # Uncomment the lines below if you need to download models or clone repos into the data directory
        # self.base_dir = PathLib(APP_DATA_DIR)
        # self.base_dir.mkdir(parents=True, exist_ok=True)

        # do your setup here

        print("Setup complete!")

    @fal.endpoint("/")
    def process(self, request: Input) -> Output:
        """Process the input"""

        # Save any temporary files to this working directory:
        work_dir = tempfile.mkdtemp(prefix=f"{APP_ID}-")

        try:
            # do your processing here

            # then return the output
            return Output(
                some_output_prop=request.some_string_prop + " processed",
                another_output_prop=request.some_numeric_prop * 2,
            )

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            import traceback

            traceback.print_exc()
            sys.stdout.flush()

            raise e

        finally:
            if "work_dir" in locals() and PathLib(work_dir).exists():
                shutil.rmtree(work_dir, ignore_errors=True)


def raise_internal_server_error(
    message: str = "Internal server error occurred",
    details: Optional[Dict[str, Any]] = None,
):
    """Raises an HTTP 500 Internal Server Error with a custom message and optional details."""
    error_detail = {"message": message, "error_type": "internal_server_error"}
    if details:
        error_detail["details"] = details

    raise HTTPException(status_code=500, detail=error_detail)


def raise_validation_error(field: str, value: Any, message: str = "Validation failed"):
    """Raises an HTTP 422 Unprocessable Entity error for validation failures."""
    raise HTTPException(
        status_code=422,
        detail={
            "message": message,
            "error_type": "validation_error",
            "field": field,
            "value": value,
            "errors": [{"loc": [field], "msg": message, "type": "value_error"}],
        },
    )
