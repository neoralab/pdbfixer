# Usage

PDBFixer is a Python API. Create a `PDBFixer` instance by pointing to a local file, an mmCIF file, a URL, or a PDB identifier, then apply the repair routines you need.

## Loading structures
```python
from pdbfixer import PDBFixer

# Local PDB
fixer = PDBFixer(filename="input.pdb")

# mmCIF file object
with open("input.cif") as handle:
    fixer = PDBFixer(pdbxfile=handle)

# Remote download
fixer = PDBFixer(url="https://files.rcsb.org/download/1VII.pdb")

# RCSB ID shortcut
fixer = PDBFixer(pdbid="1VII")
```

Only one source argument should be provided at a time. The class automatically detects PDB vs. PDBx/mmCIF content when possible.

## Common repairs

- **Find and patch gaps**: `fixer.findMissingResidues()` populates `fixer.missingResidues`, and `fixer.findMissingAtoms()` populates `fixer.missingAtoms`. Call `fixer.addMissingAtoms()` to build the missing atoms once you have reviewed the results.
- **Resolve nonstandard residues**: `fixer.findNonstandardResidues()` fills `fixer.nonstandardResidues` with suggested substitutions. Apply them with `fixer.replaceNonstandardResidues()`.
- **Hydrogenation**: `fixer.addMissingHydrogens(pH=7.0)` adds hydrogens based on the provided pH.
- **Mutations**: `fixer.applyMutations(["ALA-123-TYR"], chain_id="A")` mutates residues by chain ID and residue number using three-letter codes.
- **Remove content**: use `fixer.removeChains(chainIndices=[...], chainIds=[...])` or `fixer.removeHeterogens(keepWater=True)` to strip unwanted pieces.
- **Solvation**: `fixer.addSolvent(boxSize=unit.Vector3(...), positiveIon='Na+', negativeIon='Cl-', ionicStrength=0.1*unit.molar, padding=1.0*unit.nanometer)` builds a solvent box with optional ions.

## Saving results
```python
from openmm.app import PDBFile

with open("fixed.pdb", "w") as handle:
    PDBFile.writeFile(fixer.topology, fixer.positions, handle)
```

The `PDBFile` writer supports gzip-compressed outputs if you provide a `.gz` filename.

## Using templates and CCD downloads
- Register a nonstandard residue template with `fixer.registerTemplate(topology, positions, terminal=None)` when you want to add or mutate residues not shipped in the built-in templates.
- Automatically download a template from the Chemical Component Dictionary with `fixer.downloadTemplate("ABC")`. Downloads are cached per `PDBFixer` instance.

## Legacy manual
A legacy single-page reference remains available as [`Manual.html`](../Manual.html) if you prefer a printable resource.
