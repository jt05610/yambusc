import pytest

from src.yambusc.model import DataModel
from src.yambusc.reader import read_file
from src.yambusc.renderer import DiscreteInputWriter
from src.yambusc.services import load_data_model, data_model_gen

EXAMPLE_FILENAME = "../fake_project/example_data_structure.yaml"


@pytest.fixture()
def fake_project_path():
    return "../fake_project"


@pytest.fixture()
def template_path():
    return "../../src/templates"


@pytest.fixture()
def di_writer(template_path, fake_project_path):
    yield DiscreteInputWriter(
        project_name="testing",
        project_path=fake_project_path,
        template_path=template_path,
    )


@pytest.fixture
def structure() -> dict:
    yield read_file(EXAMPLE_FILENAME)


@pytest.fixture()
def data_model(structure):
    return DataModel(**dict(data_model_gen(structure)))
