"""Internal typing utilities for pdbfixer."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pdbfixer.ccd_definitions import CCDResidueDefinition


class FileFormat(Enum):
    """Supported structure file formats."""

    PDB = "pdb"
    PDBX = "pdbx"

    @classmethod
    def from_value(cls, value: str) -> "FileFormat":
        normalized = value.lower()
        for member in cls:
            if normalized == member.value:
                return member
        raise ValueError(f"Unsupported file format: {value}")


class BoxShape(Enum):
    """Supported solvent box shapes."""

    CUBE = "cube"
    DODECAHEDRON = "dodecahedron"
    OCTAHEDRON = "octahedron"

    @classmethod
    def from_value(cls, value: str) -> "BoxShape":
        normalized = value.lower()
        for member in cls:
            if normalized == member.value:
                return member
        raise ValueError(f"Unsupported box shape: {value}")


@dataclass(frozen=True, slots=True)
class CCDCacheEntry:
    residue_name: str
    definition: Optional[CCDResidueDefinition]
    available: bool


@dataclass(frozen=True, slots=True)
class PDBFixerInput:
    filename: Optional[str] = None
    pdbfile: Optional[object] = None
    pdbxfile: Optional[object] = None
    url: Optional[str] = None
    pdbid: Optional[str] = None

    def selected_source(self) -> tuple[str, object]:
        specified = [
            source
            for source in (
                ("filename", self.filename),
                ("pdbfile", self.pdbfile),
                ("pdbxfile", self.pdbxfile),
                ("url", self.url),
                ("pdbid", self.pdbid),
            )
            if source[1]
        ]
        if len(specified) != 1:
            raise ValueError("Exactly one option [filename, pdbfile, pdbxfile, url, pdbid] must be specified.")
        return specified[0]
