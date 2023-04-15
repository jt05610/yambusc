import os.path

import pytest

from src.yambusc.model import DataModel
from src.yambusc.reader import read_file
from src.yambusc.services import load_data_model, data_model_gen
from yambusc.renderer import DataModelRenderer

EXAMPLE_FILENAME = "data_structure.yaml"


@pytest.fixture()
def fake_project_path():
    return "test/fake_project"


@pytest.fixture()
def template_path():
    return "src/templates"


@pytest.fixture()
def fake_ds_path(fake_project_path):
    return os.path.join(fake_project_path, EXAMPLE_FILENAME)


@pytest.fixture
def structure(fake_ds_path) -> dict:
    yield read_file(fake_ds_path)


@pytest.fixture()
def data_model(structure):
    return DataModel(**dict(data_model_gen(structure)))


@pytest.fixture()
def fake_device_renderer(template_path, fake_project_path):
    return DataModelRenderer(
        template_path= template_path,
        project_dir=fake_project_path
    )
