"""Utilities for working with Chemical Component Dictionary (CCD) records."""

from __future__ import annotations

from enum import Enum
from typing import Optional

import openmm as mm
from openmm.app.internal.pdbx.reader.PdbxReader import PdbxReader
from pydantic import BaseModel, ConfigDict, Field, field_validator

# CCD download endpoint for residue definitions.
CCD_DOWNLOAD_URL: str = "https://files.rcsb.org/ligands/download/{residue}.cif"


class BondOrder(str, Enum):
    """Enumerated bond orders reported by the CCD."""

    SINGLE = "SING"
    DOUBLE = "DOUB"
    TRIPLE = "TRIP"
    QUADRUPLE = "QUAD"
    AROMATIC = "AROM"
    DELOCALIZED = "DELO"
    PI = "PI"
    POLY = "POLY"


class CCDAtomDefinition(BaseModel):
    """Validated description of an atom within a CCD residue."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, populate_by_name=True)

    atom_name: str = Field(alias="atomName")
    symbol: str
    leaving: bool
    coords: mm.Vec3
    charge: int = 0
    aromatic: bool = False

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        """Normalize chemical symbols to uppercase for consistency."""

        return value.upper()


class CCDBondDefinition(BaseModel):
    """Validated description of a bond within a CCD residue."""

    model_config = ConfigDict(frozen=True)

    atom1: str
    atom2: str
    order: BondOrder
    aromatic: bool = False


class CCDResidueDefinition(BaseModel):
    """Validated Chemical Component Dictionary residue definition."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    residue_name: str = Field(alias="residueName")
    atoms: list[CCDAtomDefinition]
    bonds: list[CCDBondDefinition]

    @classmethod
    def from_reader(cls, reader: PdbxReader) -> Optional["CCDResidueDefinition"]:
        """Create a CCD residue definition by parsing a CIF reader.

        Args:
            reader: PdbxReader instance positioned at the start of a CCD record.

        Returns:
            CCDResidueDefinition instance when atoms are present, otherwise ``None``
            if the CCD file does not contain atomic data.
        """

        data = []
        reader.read(data)
        block = data[0]

        residue_name = block.getObj("chem_comp").getValue("id")

        atom_data = block.getObj("chem_comp_atom")
        if atom_data is None:
            # The file doesn't contain any atoms, so report that no definition is available.
            return None

        atom_name_col = atom_data.getAttributeIndex("atom_id")
        symbol_col = atom_data.getAttributeIndex("type_symbol")
        leaving_col = atom_data.getAttributeIndex("pdbx_leaving_atom_flag")
        x_col = atom_data.getAttributeIndex("pdbx_model_Cartn_x_ideal")
        y_col = atom_data.getAttributeIndex("pdbx_model_Cartn_y_ideal")
        z_col = atom_data.getAttributeIndex("pdbx_model_Cartn_z_ideal")
        charge_col = atom_data.getAttributeIndex("charge")
        aromatic_col = atom_data.getAttributeIndex("pdbx_aromatic_flag")

        atoms = [
            CCDAtomDefinition(
                atomName=row[atom_name_col],
                symbol=row[symbol_col],
                leaving=row[leaving_col] == "Y",
                coords=mm.Vec3(float(row[x_col]), float(row[y_col]), float(row[z_col])) * 0.1,
                charge=row[charge_col] if row[charge_col] != "?" else 0,
                aromatic=row[aromatic_col] == "Y",
            )
            for row in atom_data.getRowList()
        ]

        bond_data = block.getObj("chem_comp_bond")
        if bond_data is not None:
            atom1_col = bond_data.getAttributeIndex("atom_id_1")
            atom2_col = bond_data.getAttributeIndex("atom_id_2")
            order_col = bond_data.getAttributeIndex("value_order")
            aromatic_col = bond_data.getAttributeIndex("pdbx_aromatic_flag")
            bonds = [
                CCDBondDefinition(
                    atom1=row[atom1_col],
                    atom2=row[atom2_col],
                    order=BondOrder(row[order_col]),
                    aromatic=row[aromatic_col] == "Y",
                )
                for row in bond_data.getRowList()
            ]
        else:
            bonds = []

        return cls(residue_name=residue_name, atoms=atoms, bonds=bonds)
