# Installation

PDBFixer is distributed as the `pdbfixer-neoralab` package for Python 3.11 and newer. You can install it from PyPI, uv, or conda-forge, or work directly from a cloned repository.

## Prerequisites
- Python 3.11+
- A C++ toolchain and OpenMM runtime dependencies as required by your platform (see the [OpenMM installation guide](https://openmm.org)).
- Optional: Git, if installing from source.

## Install from PyPI
```bash
pip install pdbfixer-neoralab
```

## Install with uv
```bash
uv pip install pdbfixer-neoralab
```

## Install from conda-forge
```bash
conda install -c conda-forge pdbfixer
```

## Install from source
```bash
git clone https://github.com/neoralab/pdbfixer.git
cd pdbfixer
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -e .
```

The source install respects optional extras. For development and testing, install with tests enabled:

```bash
pip install -e ".[tests]"
```

## Documentation dependencies
To build or serve the MkDocs site locally, install the documentation extra defined in `pyproject.toml`:

```bash
pip install -e ".[docs]"
```

Then run `mkdocs serve` from the repository root and open the printed local URL.
