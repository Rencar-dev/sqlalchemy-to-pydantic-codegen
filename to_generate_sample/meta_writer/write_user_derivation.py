# TO-BE-GENERATED part
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Literal, Dict, Optional

from pydantic_sqlalchemy.module_path_typ import ModulePathType
from to_generate_sample.meta_writer.common import (
    AttributeTransform,
    DerivationArgs,
    write_model_derivation,
)


@dataclass
class UserModelDerivationArgs(DerivationArgs):
    id: Optional[AttributeTransform]
    fullname: Optional[AttributeTransform]
    status: Optional[AttributeTransform]

    __sqlalchemy_fields = {
        'id': int,
        'fullname': str,
        'status': Enum(''),
    }





# Sample uses
write_model_derivation(
    base_path='',
    module_path=ModulePathType("__generated.dtos.user"),
    class_name="CreateUserArgs",
    derivation_args=UserModelDerivationArgs(
        id=AttributeTransform.OMIT_FIELD,
    ),
    default_attribute_transform=AttributeTransform.KEEP_FIELD_AS_IS
)

write_model_derivation(
    base_path='',
    module_path=ModulePathType("__generated.dtos.user"),
    class_name="GetUserSuccess",
    derivation_args=UserModelDerivationArgs(),
    default_attribute_transform=AttributeTransform.KEEP_FIELD_AS_IS
)
