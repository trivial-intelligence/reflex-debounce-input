from pathlib import Path
import shutil
import subprocess
import sys
from unittest import mock

import reflex.config
import pytest

import reflex_debounce_input


@pytest.fixture
def example_project(tmp_path):
    project_dir = Path(__file__).resolve().parents[1] / "example"
    tmp_project_dir = tmp_path / "example"
    shutil.copytree(project_dir, tmp_project_dir)
    return tmp_project_dir


@pytest.fixture(params=[True, False], ids=["pin_deps", "no_deps"])
def pin_deps(request, example_project):
    if request.param:
        new_config = []
        for config_line in (
            (example_project / "rxconfig.py").read_text().splitlines(True)
        ):
            new_config.append(
                config_line.replace(
                    "frontend_packages=[]",
                    "frontend_packages=['react-debounce-input@3.3.0']",
                )
            )
        (example_project / "rxconfig.py").write_text("".join(new_config))
    return request.param


def test_export_example(example_project, pin_deps):
    _ = subprocess.run(["reflex", "init"], cwd=example_project, check=True)
    # hack to ensure frontend packages get generated pynecone-io/pynecone#814
    _ = subprocess.run(
        [
            sys.executable,
            "-c",
            "import reflex_debounce_input; "
            "from reflex.utils.prerequisites import install_frontend_packages as f; f('.web')",
        ],
        cwd=example_project,
        check=True,
    )
    _ = subprocess.run(["reflex", "export"], cwd=example_project, check=True)
    assert (example_project / "frontend.zip").exists()
    assert (example_project / "backend.zip").exists()


@pytest.mark.parametrize(
    ("frontend_packages", "exp_frontend_packages"),
    [
        ([], ["react-debounce-input"]),
        (["react-debounce-input"], ["react-debounce-input"]),
        (["react-debounce-input@3.3.0"], ["react-debounce-input@3.3.0"]),
        (
            ["foo", "react-debounce-input@3.3.0", "bar"],
            ["foo", "react-debounce-input@3.3.0", "bar"],
        ),
        (["foo", "bar"], ["foo", "bar", "react-debounce-input"]),
    ],
)
def test_ensure_frontend_package(monkeypatch, frontend_packages, exp_frontend_packages):
    config = reflex.config.get_config()
    config.frontend_packages = frontend_packages
    monkeypatch.setattr(reflex.config, "get_config", mock.Mock(return_value=config))
    reflex_debounce_input.ensure_frontend_package()
    assert config.frontend_packages == exp_frontend_packages
