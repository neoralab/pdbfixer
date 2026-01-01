[![CI Status](https://github.com/openmm/pdbfixer/actions/workflows/CI.yml/badge.svg)](https://github.com/openmm/pdbfixer/actions/workflows/CI.yml)
[![PyPI Version](https://img.shields.io/pypi/v/pdbfixer.svg)](https://pypi.org/project/pdbfixer/)
[![Conda Forge](https://img.shields.io/conda/vn/conda-forge/pdbfixer.svg?logo=anaconda)](https://anaconda.org/conda-forge/pdbfixer)
[![Python Versions](https://img.shields.io/pypi/pyversions/pdbfixer.svg)](https://pypi.org/project/pdbfixer/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-Manual-0d72bd.svg)](https://htmlpreview.github.io/?https://github.com/openmm/pdbfixer/blob/master/Manual.html)
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

## Installation

PDBFixer can be installed from PyPI using pip or uv (requires Python 3.13 or newer):

```
pip install pdbfixer
```

```
uv pip install pdbfixer
```

Conda and mamba packages are also available:

```
conda install -c conda-forge pdbfixer
```

Alternatively you can install from source, as described in the manual.

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
