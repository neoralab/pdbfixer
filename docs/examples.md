# Examples

## Mutate a residue and save
```python
from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer(pdbid="1CRN")
fixer.applyMutations(["ALA-25-LYS"], chain_id="A")  # chain A, residue 25 from Ala to Lys
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.4)

with open("1crn_mutated.pdb", "w") as handle:
    PDBFile.writeFile(fixer.topology, fixer.positions, handle)
```

## Remove heterogens but keep water
```python
from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer(pdbid="4J7F")
fixer.removeHeterogens(keepWater=True)
fixer.addMissingHydrogens(pH=7.0)

with open("4j7f_no_ligands.pdb", "w") as handle:
    PDBFile.writeFile(fixer.topology, fixer.positions, handle)
```

## Solvate with ions
```python
from pdbfixer import PDBFixer
from openmm.app import PDBFile
import openmm.unit as unit

fixer = PDBFixer(pdbid="1VII")
fixer.addMissingHydrogens(pH=7.0)
fixer.addSolvent(
    padding=1.0*unit.nanometer,
    ionicStrength=0.1*unit.molar,
    positiveIon="Na+",
    negativeIon="Cl-",
)

with open("1vii_solvated.pdb", "w") as handle:
    PDBFile.writeFile(fixer.topology, fixer.positions, handle)
```

## Register a custom residue template
```python
from pdbfixer import PDBFixer
from openmm.app import Topology, PDBFile
import openmm.unit as unit
import numpy as np

# Build a minimal topology for a custom residue named ABC
custom_top = Topology()
chain = custom_top.addChain()
residue = custom_top.addResidue("ABC", chain)
atom_a = custom_top.addAtom("C1", None, residue)
atom_b = custom_top.addAtom("C2", None, residue)
positions = [
    unit.Quantity(np.array([0.0, 0.0, 0.0]), unit.nanometer),
    unit.Quantity(np.array([0.2, 0.0, 0.0]), unit.nanometer),
]

fixer = PDBFixer(pdbid="1VII")
fixer.registerTemplate(custom_top, positions)
# You can now mutate or add residues using the ABC template
```
