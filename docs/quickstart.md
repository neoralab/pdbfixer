# Quickstart

Follow this minimal workflow to clean a structure and add hydrogens.

## 1. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
```

## 2. Install PDBFixer
```bash
pip install pdbfixer-neoralab
```

## 3. Load and repair a structure
```python
from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer(filename="input.pdb")
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.0)

with open("fixed.pdb", "w") as handle:
    PDBFile.writeFile(fixer.topology, fixer.positions, handle)
```

## 4. Run locally packaged documentation
If you want to browse the refreshed manual locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then open the printed local URL (for example, http://127.0.0.1:8000/) in your browser.
