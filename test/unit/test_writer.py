import pytest

from src.yambusc.renderer import *


def test_renderer(di_writer):
    writer = di_writer
    path = TableWriter.TemplatePath.GETTER
    name = "b"
    arguments = dict(function_name=name)
    result = writer._render_template(path, "c", arguments)
    assert result[: 13 + len(name)] == f"uint16_t\nget_{name}"


@pytest.fixture()
def read_array_context():
    return ReadArrayContext(
        project_name="testing",
        table_n_macro="N_DISCRETE_INPUTS",
        names=("a", "b", "c"),
    )


def test_write_array(di_writer, read_array_context):
    print(di_writer.render_array(context=read_array_context))


def test_render_interface(di_writer, read_array_context):
    interface_context = InterfaceContext(
        project_name=read_array_context.project_name,
        getters=read_array_context.array_name,
    )
    di_writer.render_interface(interface_context)


def test_extract_user_code(fake_project_path):
    path = os.path.join(fake_project_path, "src/fake.c")
    extract_user_code(path, "fake")


def test_render_getter_no_user_code(di_writer, fake_project_path):
    getter_context = GetterContext(
        project_name="testing",
        function_name="abc",
    )
    di_writer.render_getter(getter_context)


def test_render_getter_with_user_code(di_writer, fake_project_path):
    path = os.path.join(fake_project_path, "src/fake.c")
    getter_context = GetterContext(
        project_name="testing",
        function_name="fake",
        user_code=extract_user_code(path, "fake"),
    )
    di_writer.render_getter(getter_context)
