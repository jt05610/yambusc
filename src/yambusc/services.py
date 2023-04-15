import datetime
import getpass

from yambusc.model import (
    DataModel,
    DataClassUnpack,
    DATA_MODEL_KEY_CLASS_PAIRS, Meta,
)
from yambusc.reader import read_file
from yambusc.config import DEFAULT_PROJECT_DIR, DEFAULT_DEVICE_NAME, DATE_FMT
from yambusc.renderer import DataModelRenderer


def get_author() -> str:
    return getpass.getuser()


def meta_context(device: str = DEFAULT_DEVICE_NAME,
                 author: str = get_author()) -> Meta:
    _date = datetime.date.today()
    return Meta(
        device_name=device,
        author=author,
        date=_date.strftime(DATE_FMT),
        year=str(_date.year)
    )


def data_model_gen(structure: dict):
    for key, obj in DATA_MODEL_KEY_CLASS_PAIRS.items():
        if key == "meta":
            _date = datetime.datetime.strptime(structure["meta"]["date"],
                                               DATE_FMT)
            structure["meta"]["year"] = str(_date.year)
            values = DataClassUnpack.instantiate(obj, structure[key])
        else:
            instantiate = lambda d: DataClassUnpack.instantiate(obj, d)
            values = tuple(map(instantiate, structure[key]))
        yield key, values


def load_data_model(filename: str) -> DataModel:
    structure = read_file(filename)
    return DataModel(**dict(data_model_gen(structure)))


def generate_device(renderer: DataModelRenderer,
                    device_name: str = DEFAULT_DEVICE_NAME,
                    author: str = get_author()):
    context = meta_context(device_name, author)
    renderer.create_device(context)


def generate_ds(renderer: DataModelRenderer, ds_path: str,
                dest_path: str = DEFAULT_PROJECT_DIR):
    data_model = load_data_model(ds_path)
    renderer.data_model = data_model
    renderer.project_dir = dest_path
    renderer.render()
