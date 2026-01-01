import pdbfixer
import openmm.app as app

def test_nonstandard(data_dir):
    """Test adding hydrogens to nonstandard residues."""
    fixer = pdbfixer.PDBFixer(filename=str(data_dir / "4JSV.pdb"))
    fixer.removeChains(chainIndices=[0, 1, 2])
    fixer.addMissingHydrogens()
    for residue in fixer.topology.residues():
        count = sum(1 for atom in residue.atoms() if atom.element.symbol == 'H')
        if residue.name == 'ADP':
            assert count == 15
        if residue.name in ('MG', 'MGF'):
            assert count == 0

def test_leaving_atoms(data_dir):
    """Test adding hydrogens to a nonstandard residue with leaving atoms."""
    fixer = pdbfixer.PDBFixer(filename=str(data_dir / "1BHL.pdb"))
    fixer.addMissingHydrogens()
    for residue in fixer.topology.residues():
        count = sum(1 for atom in residue.atoms() if atom.element.symbol == 'H')
        if residue.name == 'CAS':
            assert count == 10

def test_registered_template(data_dir):
    """Test adding hydrogens based on a template registered by the user."""
    fixer = pdbfixer.PDBFixer(filename=str(data_dir / "1BHL.pdb"))

    # Register a template for CAS from which a single hydrogen has been removed.

    pdb = app.PDBFile(str(data_dir / "CAS.pdb"))
    modeller = app.Modeller(pdb.topology, pdb.positions)
    modeller.delete([list(modeller.topology.atoms())[-1]])
    terminal = [atom.name in ('H2', 'OXT', 'HXT') for atom in modeller.topology.atoms()]
    fixer.registerTemplate(modeller.topology, modeller.positions, terminal)

    # See if the correct hydrogens get added.

    fixer.addMissingHydrogens()
    for residue in fixer.topology.residues():
        count = sum(1 for atom in residue.atoms() if atom.element.symbol == 'H')
        if residue.name == 'CAS':
            assert count == 9

def test_end_caps(data_dir):
    """Test adding hydrogens to a chain capped with ACE and NME."""
    fixer = pdbfixer.PDBFixer(filename=str(data_dir / "alanine-dipeptide.pdb"))
    fixer.addMissingHydrogens()
    forcefield = app.ForceField('amber14/protein.ff14SB.xml')
    forcefield.createSystem(fixer.topology)