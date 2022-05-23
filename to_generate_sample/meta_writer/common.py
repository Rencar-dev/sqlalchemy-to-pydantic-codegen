from enum import Enum, auto
from typing import Mapping

from pydantic_sqlalchemy.module_path_typ import ModulePathType


# marker-type
class DerivationArgs:
    pass


class AttributeTransform(Enum):
    TO_REQUIRED_FIELD = auto  # to required field
    TO_OPTIONAL_FIELD = auto  # to optional field
    KEEP_FIELD_AS_IS = auto  # don't transform
    OMIT_FIELD = auto  # remove attribute


def write_model_derivation(
        base_path: str,
        module_path: ModulePathType,
        class_name: str,
        derivation_args: DerivationArgs,
        default_attribute_transform: AttributeTransform
):
    pass