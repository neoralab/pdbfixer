"""Unit tests for CCD parsing utilities."""

from io import StringIO

import openmm as mm
from openmm.app.internal.pdbx.reader.PdbxReader import PdbxReader

from pdbfixer.ccd_definitions import BondOrder, CCDResidueDefinition

CCD_EXAMPLE = """
data_TEST
#
_chem_comp.id TEST
#
loop_
_chem_comp_atom.comp_id
_chem_comp_atom.atom_id
_chem_comp_atom.type_symbol
_chem_comp_atom.pdbx_leaving_atom_flag
_chem_comp_atom.pdbx_model_Cartn_x_ideal
_chem_comp_atom.pdbx_model_Cartn_y_ideal
_chem_comp_atom.pdbx_model_Cartn_z_ideal
_chem_comp_atom.charge
_chem_comp_atom.pdbx_aromatic_flag
TEST C1 C N 0.0 0.1 0.2 1 Y
TEST N1 N Y 0.3 0.4 0.5 0 N
#
loop_
_chem_comp_bond.comp_id
_chem_comp_bond.atom_id_1
_chem_comp_bond.atom_id_2
_chem_comp_bond.value_order
_chem_comp_bond.pdbx_aromatic_flag
TEST C1 N1 SING N
TEST N1 C1 DOUB Y
#
"""


def test_ccd_residue_definition_from_reader_validates_ccd_data():
    """CCD definitions should be parsed into validated models."""

    reader = PdbxReader(StringIO(CCD_EXAMPLE))
    residue_definition = CCDResidueDefinition.from_reader(reader)

    assert residue_definition is not None
    assert residue_definition.residue_name == "TEST"

    first_atom = residue_definition.atoms[0]
    assert first_atom.atom_name == "C1"
    assert first_atom.symbol == "C"
    assert first_atom.leaving is False
    assert isinstance(first_atom.coords, mm.Vec3)

    first_bond = residue_definition.bonds[0]
    assert first_bond.order is BondOrder.SINGLE
    assert first_bond.aromatic is False
