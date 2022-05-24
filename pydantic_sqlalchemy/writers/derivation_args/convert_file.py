from pydantic_sqlalchemy.models_collector import CollectedFile
from pydantic_sqlalchemy.module_path_typ import get_mangled_module_path_as_name
from pydantic_sqlalchemy.utils.trim_indent import TrimIndent
from pydantic_sqlalchemy.writers.derivation_args.convert_model import collected_model_to_derivation_args


def collected_file_to_derivation_args_file(
        collected_file: CollectedFile,
        base_module_path: str = '__generated',
        exclude_relations: bool = False,
) -> TrimIndent:
    import_statements = [
            f"import {base_module_path}.{_i.module_path} as {get_mangled_module_path_as_name(_i.module_path)}"
            for _i in collected_file.imports
        ]
    header_part = [
        f"""from __future__ import annotations
        |from pydantic_sqlalchemy.writers.derivation_args.markers import (
        |   BaseFieldOption, DerivationTemplate,
        |)
        |from decimal import Decimal
        |from datetime import datetime
        |from typing import TYPE_CHECKING, Optional, List, Dict, Literal
        |from dataclasses import dataclass
        |from pydantic import BaseModel
        |if TYPE_CHECKING:""",
        TrimIndent(["..."]),
        TrimIndent(import_statements),
        "",
        "",
    ]
    models_parts = [
        collected_model_to_derivation_args(
            model=model,
            import_statements=import_statements,
            exclude_relations=exclude_relations,
        )
        for model in collected_file.models
    ]
    to_return = header_part[:]
    for model_part in models_parts:
        to_return = to_return + model_part
    return TrimIndent(to_return)
