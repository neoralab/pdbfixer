# Configuration

PDBFixer does not require a global configuration file or environment variables. Most behavior is controlled directly through `PDBFixer` constructor arguments and method parameters.

## Environment variables
No environment variables are consumed by the library. If you rely on proxy settings for downloads, configure them at the system level (for example, `HTTP_PROXY`/`HTTPS_PROXY`).

## Runtime parameters
- **Input source**: choose one of `filename`, `pdbfile`, `pdbxfile`, `url`, or `pdbid` when creating `PDBFixer`.
- **Hydrogenation pH**: pass `pH` to `addMissingHydrogens()`.
- **Solvent box shape and ions**: provide `boxSize`, `padding`, `positiveIon`, `negativeIon`, and `ionicStrength` to `addSolvent()`.
- **Template resolution**: supply custom templates with `registerTemplate()` or allow downloads via `downloadTemplate()`.

## Configuration files
No repository-level configuration files are required beyond the Python package itself. If you use OpenMM platform selection, pass an `openmm.Platform` instance to the `PDBFixer` constructor.
