from typing import Callable, Optional

from pydantic_sqlalchemy.extract_from_sqlalchemy import ExtractedModel, GeneratedImportReference, ExtractedField
from pydantic_sqlalchemy.models_collector import ModelsCollector, CollectedFile
from pydantic_sqlalchemy.module_path_typ import (
    get_mangled_module_path_as_name,
)
from pydantic_sqlalchemy.utils.trim_indent import TrimIndent
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
    ColumnDefault,
)

from pydantic_sqlalchemy.writers.common import ensure_file_module_path


def stringify_field_type(extracted_field: ExtractedField):
    field = extracted_field.typ
    typ_str = ''
    if isinstance(field, GeneratedImportReference):
        typ_str = f"{get_mangled_module_path_as_name(field.module_path)}.{field.name}"
    elif isinstance(field, SQLAlchemyEnum):
        enums_to_strings = [
            f"'{e}'" for e in field.enums
        ]
        typ_str = f"Literal[{', '.join(enums_to_strings)}]"
    else:
        typ_str = f"{field.__name__}"

    if extracted_field.is_array:
        return f"List[{typ_str}]"
    if extracted_field.is_nullable:
        return f"Optional[{typ_str}]"
    return typ_str


def stringify_field_default(default_val):
    if default_val == Ellipsis:
        return '...'
    if isinstance(default_val, ColumnDefault):
        if default_val.is_callable:
            # FIXME: what to do on 'utcnow' for created_at, updated_at ?
            return None
        if type(default_val.arg) == str:
            return f"'{default_val.arg}'"
        return f"{default_val.arg}"
    return str(default_val)


def collected_model_to_pydantic_model(
        model: ExtractedModel
):
    fields = [
        f"{name}: {stringify_field_type(extracted_field)} = {stringify_field_default(extracted_field.default)}"
        for name, extracted_field in model.fields.items()
    ]
    return [
        ""
        f"class {model.ref.name}(BaseModel):",
        TrimIndent(fields)
    ]


def collected_file_to_pydantic_file(
        collected_file: CollectedFile,
        base_module_path: str = '__generated',
) -> TrimIndent:
    header_part = [
        f"""from __future__ import annotations
        |from datetime import datetime
        |from typing import TYPE_CHECKING, Optional, List, Dict, Literal
        |from pydantic import BaseModel
        |if TYPE_CHECKING:""",
        TrimIndent(["..."]),
        TrimIndent([
            f"import {base_module_path}.{_i.module_path} as {get_mangled_module_path_as_name(_i.module_path)}"
            for _i in collected_file.imports
        ]),
        "",
        "",
    ]
    models_parts = [
        collected_model_to_pydantic_model(model)
        for model in collected_file.models
    ]
    to_return = header_part[:]
    for model_part in models_parts:
        to_return = to_return + model_part
    return TrimIndent(to_return)


def write_pydantic_models(
        collector: ModelsCollector,
        base_path: str = '__generated',
        postprocessor: Optional[Callable[[str], str]] = None
):
    for module_path, collected_file in collector.collected_files.items():
        tp_write_path = ensure_file_module_path(
            module_path=module_path,
            base_path=base_path,
        )
        with open(tp_write_path, 'w') as f:
            rendered = collected_file_to_pydantic_file(
                collected_file=collected_file,
                base_module_path=base_path,

            ).render(indent_level=0, indent_chars="    ")
            if postprocessor is not None:
                rendered = postprocessor(rendered)
            f.write(rendered)
