import pytest

from src.yambusc.renderer import *


def test_render_tables(template_path, data_model, fake_project_path):
    renderer = DataModelRenderer(data_model, template_path, fake_project_path)
    renderer.render_tables()


def test_render_device(fake_device_renderer, data_model):
    fake_device_renderer.data_model = data_model
    fake_device_renderer.render_device()
    fake_device_renderer.render_device(True)


def test_camel_to_snake():
    name = "PressureSensor"
    expected = "pressure_sensor"
    actual = camel_to_snake(name)
    assert actual == expected


def test_template(template_path):
    env = Environment(
        loader=FileSystemLoader("src/templates"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(f"c/source.c.jinja2")
    context = dict(
        author="me",
        date="date",
        year="2022",
        device_name="Injector",
        includes=("data_model", "primary_table"),
        functions=(
            dict(
                name="a",
                read_code="",
                write_code="",
            ),
            dict(
                name="b",
                read_code="",
                write_code="",
            ),
        ),
        read_only=False,
        table_name="coils",
        n_tables=2,
    )
    rendered = template.render(**context)
    print(rendered)
