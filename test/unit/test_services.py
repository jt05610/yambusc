from src.yambusc.services import *


def test_load_data_model(structure):
    DataModel(**dict(data_model_gen(structure)))


def test_generate_ds(fake_device_renderer, fake_ds_path, fake_project_path):
    generate_ds(fake_device_renderer, fake_ds_path, fake_project_path)


def test_generate_device(fake_device_renderer):
    generate_device(fake_device_renderer)
