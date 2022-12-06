from src.yambusc.services import *


def test_load_data_model(structure):
    DataModel(**dict(data_model_gen(structure)))


def test_write_headers(data_model, di_writer):
    write_headers(data_model, di_writer)


def test_write_sources(data_model, di_writer):
    write_sources(data_model, di_writer)
