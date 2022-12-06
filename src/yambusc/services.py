from src.yambusc.model import (
    DataModel,
    DataClassUnpack,
    DATA_MODEL_KEY_CLASS_PAIRS,
)
from src.yambusc.reader import read_file
from src.yambusc.renderer import DiscreteInputWriter


def data_model_gen(structure: dict):
    for key, obj in DATA_MODEL_KEY_CLASS_PAIRS.items():
        instantiate = lambda d: DataClassUnpack.instantiate(obj, d)
        values = tuple(map(instantiate, structure[key]))
        yield key, values


def load_data_model(filename: str) -> DataModel:
    structure = read_file(filename)
    return DataModel(**dict(data_model_gen(structure)))


def write_headers(model: DataModel, writer: DiscreteInputWriter):
    inputs = map(lambda di: di.name, model.discrete_inputs)
    writer.render_header(inputs)
    writer.write("inc/discrete_inputs.h")


def write_sources(model: DataModel, writer: DiscreteInputWriter):
    inputs = tuple(map(lambda di: di.name, model.discrete_inputs))
    writer.render_source(inputs)
    writer.write("src/discrete_inputs.c")
