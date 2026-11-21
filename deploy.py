"""Copy the application to a local release and verify its output."""

import argparse
import contextlib
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import runpy
import shutil


def deploy(target):
    """Create a release outside the workspace and a downloadable archive."""
    project = Path(__file__).resolve().parent
    target = Path(target).expanduser().resolve()
    if target == project or project in target.parents:
        raise ValueError("Deployment must be outside the project workspace.")

    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(project / "app.py", target / "app.py")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        runpy.run_path(str(target / "app.py"), run_name="__main__")
    if output.getvalue() != "Hello, World from Ali Naji!\n":
        raise RuntimeError("The deployed application failed its smoke test.")

    metadata = {
        "application": "Ali Naji Lab 10 greeting",
        "build_number": os.environ.get("BUILD_NUMBER", "local"),
        "git_commit": os.environ.get("GIT_COMMIT", "local"),
        "deployed_at_utc": datetime.now(timezone.utc).isoformat(),
        "deployment_path": str(target),
        "smoke_test": "PASS",
        "output": output.getvalue().strip(),
    }
    metadata_text = json.dumps(metadata, indent=2) + "\n"
    (target / "release.json").write_text(metadata_text, encoding="utf-8")
    reports = project / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "deployment.json").write_text(metadata_text, encoding="utf-8")
    (reports / "deployment-smoke.txt").write_text(
        f"Deployment smoke test: PASS\n{output.getvalue()}", encoding="utf-8"
    )
    dist = project / "dist"
    dist.mkdir(exist_ok=True)
    shutil.make_archive(str(dist / "ali-naji-lab10"), "zip", target)
    print(f"Deployed application to: {target}")
    print("Deployment smoke test: PASS")
    print(output.getvalue(), end="")
    return metadata


def default_target():
    """Keep a Jenkins deployment separate from its disposable workspace."""
    workspace = Path(os.environ.get("WORKSPACE", __file__)).resolve()
    if "WORKSPACE" in os.environ:
        base = workspace.parent.parent / "deployments" / workspace.name
    else:
        base = Path(__file__).resolve().parent.parent / "deployments"
    release = "build-" + os.environ.get("BUILD_NUMBER", "local")
    return base / release


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=default_target())
    deploy(parser.parse_args().target)
