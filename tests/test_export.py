from pathlib import Path
import subprocess

import pytest


@pytest.fixture
def example_project():
    return Path(__file__).resolve().parents[1] / "example"


def test_export_example(example_project):
    _ = subprocess.run(["pc", "init"], cwd=example_project, check=True)
    _ = subprocess.run(["pc", "export"], cwd=example_project, check=True)
