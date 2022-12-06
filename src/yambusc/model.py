from dataclasses import dataclass, fields
from typing import Tuple, Optional


@dataclass
class TableEntry:
    pass


@dataclass
class DiscreteInput(TableEntry):
    name: str
    port: str
    pin: str


@dataclass
class Coil(TableEntry):
    name: str


@dataclass
class InputRegister(TableEntry):
    name: str


@dataclass
class HoldingRegister(TableEntry):
    name: str


@dataclass
class DataModel:
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


DATA_MODEL_KEY_CLASS_PAIRS = {
    "discrete_inputs": DiscreteInput,
    "coils": Coil,
    "input_registers": InputRegister,
    "holding_registers": HoldingRegister,
}
