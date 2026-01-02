# Troubleshooting

## Download failures for CCD definitions
If `downloadTemplate()` returns `False`, verify internet connectivity and that the residue name exists in the PDB Chemical Component Dictionary. Proxy settings must be configured via your environment or system network settings.

## No atoms found
`PDBFixer` raises an exception if the loaded structure has zero atoms. Confirm the input file path or URL and that you are passing the correct source argument.

## Missing templates for nonstandard residues
If `findNonstandardResidues()` suggests replacements that lack templates, register your own via `registerTemplate()` or allow downloads with `downloadTemplate()`.

## Slow solvation
`addSolvent()` can be compute-intensive for large systems. Consider running with an explicit `openmm.Platform` tuned for your hardware or increasing padding only as needed.

## Reporting issues
If you encounter problems, please file an issue or open a pull request with reproduction steps. Include the input structure and the sequence of PDBFixer calls you executed.
