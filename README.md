[![CI Status](https://github.com/openmm/pdbfixer/actions/workflows/CI.yml/badge.svg)](https://github.com/openmm/pdbfixer/actions/workflows/CI.yml)
[![PyPI Version](https://img.shields.io/pypi/v/pdbfixer-neoralab.svg)](https://pypi.org/project/pdbfixer-neoralab/)
[![Conda Forge](https://img.shields.io/conda/vn/conda-forge/pdbfixer.svg?logo=anaconda)](https://anaconda.org/conda-forge/pdbfixer)
[![Python Versions](https://img.shields.io/pypi/pyversions/pdbfixer-neoralab.svg)](https://pypi.org/project/pdbfixer-neoralab/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-Manual-0d72bd.svg)](https://htmlpreview.github.io/?https://github.com/openmm/pdbfixer/blob/master/Manual.html)
[![Authors](https://img.shields.io/badge/authors-neoralab%20team-7c3aed.svg)](https://github.com/neoralab/pdbfixer/graphs/contributors)
[![Authors](https://img.shields.io/badge/authors-OpenMM%20team-7c3aed.svg)](https://github.com/openmm/pdbfixer/graphs/contributors)

PDBFixer
========

PDBFixer is an easy to use Python API for fixing problems in Protein Data Bank files in preparation for simulating them.  It can automatically fix the following problems:

- Add missing heavy atoms.
- Add missing hydrogen atoms.
- Build missing loops.
- Convert non-standard residues to their standard equivalents.
- Select a single position for atoms with multiple alternate positions listed.
- Delete unwanted chains from the model.
- Delete unwanted heterogens.
- Build a water box for explicit solvent simulations.

See our [manual](https://htmlpreview.github.io/?https://github.com/openmm/pdbfixer/blob/master/Manual.html)

## Improvements over the original OpenMM fork

- Published on PyPI as [`pdbfixer-neoralab`](https://pypi.org/project/pdbfixer-neoralab/) with support for Python 3.11 and newer.
- Modernized packaging via `pyproject.toml` and `versioningit`, keeping releases in sync with Git tags.
- Distributed purely as a Python API, removing the legacy web and command-line interfaces to focus on library usability.

## Installation

PDBFixer can be installed from PyPI using pip or uv as `pdbfixer-neoralab` (requires Python 3.11 or newer):

```
pip install pdbfixer-neoralab
```

```
uv pip install pdbfixer-neoralab
```

Conda and mamba packages are also available:

```
conda install -c conda-forge pdbfixer
```

Alternatively you can install from source, as described in the manual.

### Versioning

PDBFixer uses [versioningit](https://versioningit.readthedocs.io/) to derive
its version from Git tags. Building from a source checkout therefore requires
either a cloned repository with Git metadata or a source distribution that
already includes the generated version. When no tag information is available,
the default version reported is `0+unknown`. To see the version that will be
used for a build, run:

```
python -m versioningit
```

## Usage

PDBFixer is now distributed purely as a Python API. The historical web and command-line interfaces have been removed in favour of direct use from Python code.

```python
from pdbfixer import PDBFixer

fixer = PDBFixer(filename="input.pdb")
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.0)
```
