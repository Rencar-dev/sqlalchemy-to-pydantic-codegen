from typing import Callable, Optional

from pydantic_sqlalchemy.models_collector import ModelsCollector

from pydantic_sqlalchemy.writers.common import ensure_file_module_path
from pydantic_sqlalchemy.writers.derivation_args.convert_file import collected_file_to_derivation_args_file
from pydantic_sqlalchemy.writers.derivation_args.convert_model import collected_model_to_derivation_args


def write_derivation_arg_files(
        collector: ModelsCollector,
        base_path: str = '__generated',
        exclude_relations: bool = False,
        postprocessor: Optional[Callable[[str], str]] = None
):
    for module_path, collected_file in collector.collected_files.items():
        tp_write_path = ensure_file_module_path(
            module_path=module_path,
            base_path=base_path,
        )
        with open(tp_write_path, 'w') as f:
            rendered = collected_file_to_derivation_args_file(
                collected_file=collected_file,
                base_module_path=base_path,
                exclude_relations=exclude_relations,
            ).render(indent_level=0, indent_chars="    ")
            if postprocessor is not None:
                rendered = postprocessor(rendered)
            f.write(rendered)

