import os
import re
from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from yambusc.model import DataModel, TableEntry, Function, Meta
from yambusc.config import TEMPLATE_PATH, DEFAULT_PROJECT_DIR

name_pattern = re.compile('(.)([A-Z][a-z]+)')
camel_pattern = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name):
    name = name_pattern.sub(r'\1_\2', name)
    return camel_pattern.sub(r'\1_\2', name).lower()


class DataModelRenderer:
    def __init__(
            self,
            data_model: DataModel = None,
            template_path: str = TEMPLATE_PATH,
            project_dir: str = DEFAULT_PROJECT_DIR,
    ):
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.data_model = data_model
        self.project_dir = project_dir

    def map_function(self, table_name: str, entry: TableEntry) -> dict:
        path = self.table_path(table_name)
        function = Function(file_path=path, table_entry=entry)
        return function.__dict__()

    def render_table_source(self, table: str):
        template = self.env.get_template("c/source.c.jinja2")
        context = asdict(self.data_model.meta)
        table_obj = getattr(self.data_model, table)
        functions = tuple(
            map(lambda x: self.map_function(table, x), table_obj)
        )
        if table in ("discrete_inputs", "input_registers"):
            context["read_only"] = True
        else:
            context["read_only"] = False

        context["n_functions"] = len(functions)
        context["functions"] = functions
        context["table_name"] = table
        context["device_name_snake"] = camel_to_snake(self.data_model.meta.device_name)
        context["file_name"] = self.table_path(table, "c").split("/")[-1]
        return template.render(**context)

    def render_table_header(self, table: str):
        template = self.env.get_template("h/header.jinja2")
        context = asdict(self.data_model.meta)
        context["device_name"] = self.data_model.meta.device_name
        context["table_name"] = table
        context["file_name"] = self.table_path(table, "h").split("/")[-1]

        return template.render(**context)

    def table_path(self, table: str, ext: str = "c"):
        path = self.proj_dir("src")
        return os.path.join(path, f"{table}.{ext}")

    def proj_dir(self, which: str) -> str:
        return os.path.join(self.project_dir, which, "data_model")

    def ds_path(self):
        return os.path.join(self.project_dir, "data_structure.yaml")

    def render_tables(self):
        for table in vars(self.data_model).keys():
            if table != "meta":
                buffer = self.render_table_source(table)
                with open(self.table_path(table), "w") as f:
                    f.write(buffer)
                buffer = self.render_table_header(table)
                with open(self.table_path(table, "h"), "w") as f:
                    f.write(buffer)

    def render(self):
        self.make_tree()
        self.render_tables()
        self.render_device()
        self.render_device(True)

    def template_path(self, path: str):
        return path.strip(".jinja2"), self.env.get_template(path)

    def create_device(self, ctx: Meta):
        self.make_tree()

        paths = (
            "data_structure.yaml.jinja2",
            "CMakeLists.txt.jinja2",
        )

        templates = map(self.template_path, paths)
        for path, template in templates:
            write_path = os.path.join(self.project_dir, path)
            if not os.path.exists(write_path):
                with open(write_path, "w") as f:
                    f.write(template.render(asdict(ctx)))
    
    def update_device(self):
        paths = (
            "data_structure.yaml.jinja2",
            "CMakeLists.txt.jinja2",
        )

        templates = map(self.template_path, paths)
        for path, template in templates:
            write_path = os.path.join(self.project_dir, path)
            if not os.path.exists(write_path):
                with open(write_path, "w") as f:
                    f.write(template.render(asdict(ctx)))

    def make_tree(self):
        dirs = (
            self.project_dir,
            os.path.join(self.project_dir, "src"),
            self.proj_dir("src"),
            os.path.join(self.project_dir, "inc"),
            os.path.join(self.project_dir, "test"),
        )
        for sub_dir in dirs:
            if not os.path.exists(sub_dir):
                os.mkdir(sub_dir)

    def render_device(self, source: bool = False):
        snake = camel_to_snake(self.data_model.meta.device_name)
        path = lambda p, e: os.path.join(self.project_dir, f"{p}/{snake}.{e}")
        if source:
            dest_path = path("src", "c")
            template_path = "c/device.c.jinja2"
        else:
            dest_path = path("inc", "h")
            template_path = "h/device_header.jinja2"
        template = self.env.get_template(template_path)
        context = asdict(self.data_model.meta)
        tables = tuple(
            table for table in vars(self.data_model).keys() if table != "meta")
        context["tables"] = tables
        context["n_tables"] = len(tables)
        context["device_name_snake"] = snake
        context["file_name"] = dest_path.split("/")[-1]
        buffer = template.render(**context)
        if not os.path.exists(dest_path):
            with open(dest_path, "w") as f:
                f.write(buffer)
