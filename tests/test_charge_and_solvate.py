import openmm.unit


def test_add_solvent_to_local_structure(dipeptide_factory):
    fixer = dipeptide_factory()
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(pH=7.0)

    fixer.addSolvent(
        padding=1.0 * openmm.unit.nanometer,
        ionicStrength=0.0 * openmm.unit.molar,
        boxShape="cube",
    )

    box_vectors = fixer.topology.getPeriodicBoxVectors()
    assert box_vectors is not None

    water_residues = [res for res in fixer.topology.residues() if res.name.upper() in {"HOH", "WAT"}]
    assert len(water_residues) > 0

    ions = [res for res in fixer.topology.residues() if res.name.upper() in {"NA", "CL"}]
    assert len(ions) == 0
