import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Iterable, Iterator, Optional, Union, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_PATH = "templates"


def extract_user_code(
    path: str, user_code_guard: str, set_get: str = "get"
) -> Iterable[str]:
    search_for = lambda w: f" * {w} {set_get}_{user_code_guard} code\n"
    with open(path, "r") as f:
        lines = list(l for l in f.readlines())
        start = lines.index(search_for("start")) + 2
        end = lines.index(search_for("end")) - 1
        return "".join(lines[start:end])


@dataclass
class ProjectContext:
    project_name: str


@dataclass
class ArrayContext(ProjectContext):
    access_type: str
    array_name: str
    table_n_macro: str
    names: Iterable[str]


@dataclass
class InterfaceContext(ProjectContext):
    getters: str
    setters: Optional[Union[str, int]] = 0


@dataclass
class GetterContext(ProjectContext):
    function_name: str
    user_code: str = None


@dataclass
class SourceContext:
    functions: Iterable[str]
    arrays: Iterable[str]
    interface: str
    table_name: str
    user_header_code: str
    create_code: str


class ReadArrayContext(ArrayContext):
    def __init__(
        self, project_name: str, table_n_macro: str, names: Iterable[str]
    ):
        self.project_name = project_name
        self.access_type = "read"
        self.array_name = "getters"
        self.table_n_macro = table_n_macro
        self.names = names


class WriteArrayContext(ArrayContext):
    def __init__(
        self, project_name: str, table_n_macro: str, names: Iterable[str]
    ):
        self.project_name = project_name
        self.access_type = "write"
        self.array_name = "setters"
        self.table_n_macro = table_n_macro
        self.names = names


class TableWriter(ABC):
    env: Environment
    TABLE_NAME: str
    TABLE_N_MACRO: str
    buffer: str

    class TemplatePath(str, Enum):
        HEADER = "header"
        SOURCE = "source"
        DATA_MODEL = "data_model"
        INTERFACE = "interface"
        GETTER = "getter"
        SETTER = "setter"
        ARRAY = "array"
        TEST = "test"
        TEST_GROUP = "test_group"

        def __str__(self) -> str:
            return str.__str__(self)

        def as_type(self, t: str) -> str:
            return f"{t}/{self}.{t}"

    def __init__(
        self,
        project_name: str,
        project_path: str = None,
        template_path: str = TEMPLATE_PATH,
    ):
        if project_path is None:
            project_path = project_name
        self.project_path = project_path
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(),
        )
        self.project_name = project_name
        self.buffer = ""
        self.n_functions = 0

    def _render_template(
        self, path: TemplatePath, file_type: str, template_vars: dict
    ):
        template = self.env.get_template(path.as_type(file_type))
        self.buffer = template.render(**template_vars)
        return self.buffer

    def render_header(self, *args, **kwargs):
        return self._render_template(
            self.TemplatePath.HEADER, "h", self.get_context(*args, **kwargs)
        )

    def render_array(self, context: ArrayContext):
        return self._render_template(
            self.TemplatePath.ARRAY, "c", asdict(context)
        )

    def render_interface(self, context: InterfaceContext):
        return self._render_template(
            self.TemplatePath.INTERFACE, "c", asdict(context)
        )

    def render_getter(self, context: GetterContext):
        return self._render_template(
            self.TemplatePath.GETTER, "c", asdict(context)
        )

    def get_context(self, *args, **kwargs) -> dict:
        functions = tuple(self._render_header(*args, **kwargs))
        return {
            "project_name": self.project_name.upper(),
            "header_name": self.TABLE_NAME.upper(),
            "table_name": self.TABLE_NAME.lower(),
            "table_size": self.n_functions,
            "functions": functions,
        }

    def source_context(
        self,
        functions: str,
        array_context: Tuple[ArrayContext, ...],
        interface_context: InterfaceContext,
        table_name: str,
        source_path: str,
    ) -> SourceContext:
        if os.path.exists(source_path):
            user_code = extract_user_code(source_path, "user")
            create_code = extract_user_code(source_path, "create")
        else:
            user_code = None
            create_code = None
        return SourceContext(
            functions=functions,
            arrays=tuple(map(lambda c: self.render_array(c), array_context)),
            interface=self.render_interface(context=interface_context),
            table_name=table_name,
            user_header_code=user_code,
            create_code=create_code,
        )

    def write(self, path: str, data: str = None):
        if data is None:
            data = self.buffer
        with open(os.path.join(self.project_path, path), "w") as f:
            f.write(data)

    @abstractmethod
    def _render_header(self, function_names: Iterable[str]):
        raise NotImplementedError

    def render_source(self, function_names: Iterable[str]):
        source_path = os.path.join(
            self.project_path, f"src/{self.TABLE_NAME}.c"
        )
        if os.path.exists(source_path):
            user_code = lambda n: extract_user_code(source_path, n)
        else:
            user_code = lambda n: None
        getter = lambda n: self.render_getter(
            GetterContext(self.project_name, n, user_code(n)),
        )

        functions = tuple(map(getter, function_names))
        context = self.source_context(
            functions=functions,
            array_context=(
                ReadArrayContext(
                    self.project_name,
                    self.TABLE_N_MACRO,
                    names=tuple(function_names),
                ),
            ),
            interface_context=InterfaceContext(self.project_name, "getters"),
            table_name=self.TABLE_NAME,
            source_path=source_path,
        )
        return self._render_template(
            self.TemplatePath.SOURCE, "c", asdict(context)
        )

    @abstractmethod
    def _render_source(self, function_names: Iterable):
        raise NotImplementedError

    def write_native_tests(self):
        pass

    def write_embedded_tests(self):
        pass


class DiscreteInputWriter(TableWriter):
    TABLE_NAME = "discrete_inputs"
    TABLE_N_MACRO = "N_DISCRETE_INPUTS"

    def _render(self, render_type: str, function_names: Iterable[str]):
        self.n_functions = 0
        for name in function_names:
            self.n_functions += 1
            path = render_type
            context = dict(function_name=name)
            yield self._render_template(path, "h", context)

    def _render_header(self, function_names: Iterable[str]) -> Iterator[str]:
        yield from self._render(self.TemplatePath.HEADER, function_names)

    def _render_source(self, function_names: Iterable[str]) -> Iterator[str]:
        yield from self._render(self.TemplatePath.GETTER, function_names)


class CoilWriter(TableWriter):
    TABLE_NAME = "coils"
    TABLE_N_MACRO = "N_COILS"

    def _render(self, render_type: str, function_names: Iterable[str]):
        self.n_functions = 0
        for name in function_names:
            self.n_functions += 1
            path = render_type
            context = dict(function_name=name)
            yield self._render_template(path, "h", context)

    def _render_header(self, function_names: Iterable[str]) -> Iterator[str]:
        yield from self._render(self.TemplatePath.HEADER, function_names)

    def _render_source(self, function_names: Iterable[str]) -> Iterator[str]:
        yield from self._render(self.TemplatePath.GETTER, function_names)
        yield from self._render(self.TemplatePath.SETTER, function_names)
