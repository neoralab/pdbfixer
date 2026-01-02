from pathlib import Path

import pdbfixer
import pytest


@pytest.fixture(scope="session")
def data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture
def villin_factory(data_dir):
    def _create():
        return pdbfixer.PDBFixer(filename=str(data_dir / "test.pdb"))

    return _create


@pytest.fixture
def dipeptide_factory(data_dir):
    def _create():
        return pdbfixer.PDBFixer(filename=str(data_dir / "alanine-dipeptide.pdb"))

    return _create


@pytest.fixture
def jsv_content(data_dir):
    return (data_dir / "4JSV.pdb").read_text()
