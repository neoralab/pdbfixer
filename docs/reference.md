# Reference

The `pdbfixer` package exposes a single main class, `PDBFixer`, plus helper functions and types. The class methods in `src/pdbfixer/pdbfixer.py` implement repair operations for PDB and PDBx/mmCIF structures.

## Class: `PDBFixer`

### Constructor
`PDBFixer(filename=None, pdbfile=None, pdbxfile=None, url=None, pdbid=None, platform=None)`

- Accepts one source argument (file path, file object, URL, or PDB ID). Formats are autodetected where possible.
- Optional `platform` lets you pass an `openmm.Platform` to control compute resources.

### Inspection helpers
- `missingResidues`, `missingAtoms`, `missingTerminals`: populated by the corresponding `find*` methods.
- `nonstandardResidues`: populated by `findNonstandardResidues()` to map residues to replacements.

### Core mutation and repair methods
- `findMissingResidues()` / `findMissingAtoms()` / `addMissingAtoms()`
- `findNonstandardResidues()` / `replaceNonstandardResidues()`
- `addMissingHydrogens(pH=7.0)`
- `addMissingResidues()` to build missing segments after inspection
- `applyMutations(["ALA-123-TYR"], chain_id="A")` to mutate residues by chain ID and residue number
- `removeChains(chainIndices=None, chainIds=None)`
- `removeHeterogens(keepWater=True)`
- `addSolvent(...)` to solvate with optional ions and padding

### Template utilities
- `registerTemplate(topology, positions, terminal=None)`: register a template for a nonstandard residue.
- `downloadTemplate(name)`: fetch a Chemical Component Dictionary entry and register it if found.

### I/O helpers
- `guess_file_format_from_text(text, filename="")` and `normalize_file_format()` normalize input formats when reading from strings.
- `normalize_box_shape(box_shape)` standardizes solvent box shape inputs.

### Saving
Persist the repaired structure with `openmm.app.PDBFile.writeFile(fixer.topology, fixer.positions, handle)`.

Refer to the source docstrings for argument defaults and return types. The MkDocs pages in this site provide narrative explanations of each routine.
