import os
from dataclasses import dataclass, fields
from enum import Enum
from typing import Tuple, Optional


@dataclass
class TableEntry:
    name: str
    read_only = True


@dataclass
class DiscreteInput(TableEntry):
    pass


@dataclass
class Coil(TableEntry):
    read_only = False


@dataclass
class InputRegister(TableEntry):
    pass


@dataclass
class HoldingRegister(TableEntry):
    read_only = False


@dataclass(frozen=True)
class Meta:
    device_name: str
    author: str
    date: str
    year: str


@dataclass
class DataModel:
    meta: Meta
    discrete_inputs: Optional[Tuple[DiscreteInput, ...]]
    coils: Optional[Tuple[Coil, ...]]
    input_registers: Optional[Tuple[InputRegister, ...]]
    holding_registers: Optional[Tuple[HoldingRegister, ...]]
    _current = 0

    def _tables(self):
        return (
            self.discrete_inputs,
            self.coils,
            self.input_registers,
            self.holding_registers,
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self._current > 3:
            raise StopIteration
        else:
            table = self._tables()[self._current]
            self._current += 1
            return table


class DataClassUnpack:
    classFieldCache = {}

    @classmethod
    def instantiate(cls, classToInstantiate, argDict: dict):
        if classToInstantiate not in cls.classFieldCache:
            cls.classFieldCache[classToInstantiate] = {
                f.name for f in fields(classToInstantiate) if f.init
            }

        field_set = cls.classFieldCache[classToInstantiate]
        filtered_arg_dict = {
            k: v for k, v in argDict.items() if k in field_set
        }

        return classToInstantiate(**filtered_arg_dict)


class EnumBase(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class SectionType(EnumBase):
    INCLUDE = "include"
    STRUCT = "struct"
    MACRO = "macro"
    CREATE = "create"


@dataclass(frozen=True)
class CodeSection:
    path: str
    name: Optional[str] = None

    def start_section_guard(self, which: str) -> str:
        return f"    /* {which} {self.name} code */\n"

    def __str__(self):
        if os.path.exists(self.path):
            search_for = lambda w: self.start_section_guard(w)
            with open(self.path, "r") as f:
                lines = list(l for l in f.readlines())
                start = lines.index(search_for("start")) + 1
                end = lines.index(search_for("end")) - 1
                result = "".join(lines[start:end])
        else:
            result = ""
        return result


class Function:
    name: str
    read_only: bool
    read_code: CodeSection
    write_code: Optional[CodeSection]

    def __init__(self, file_path: str, table_entry: TableEntry):
        self.name = table_entry.name
        self.read_only = table_entry.read_only
        self.read_code = CodeSection(path=file_path, name=f"read_{self.name}")
        if not self.read_only:
            self.write_code = CodeSection(
                path=file_path, name=f"write_{self.name}"
            )
        else:
            self.write_code = ""

    def __dict__(self):
        return dict(
            name=self.name,
            read_code=str(self.read_code),
            write_code=str(self.write_code),
        )


DATA_MODEL_KEY_CLASS_PAIRS = {
    "meta": Meta,
    "discrete_inputs": DiscreteInput,
    "coils": Coil,
    "input_registers": InputRegister,
    "holding_registers": HoldingRegister,
}
