import inspect
from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class BaseFieldOption:
    pass


@dataclass
class OmitField(BaseFieldOption):
    pass


@dataclass
class KeepFieldAsIs(BaseFieldOption):
    pass

# TODO: requires a lot more work...
# @dataclass
# class MakeFieldRequired(BaseFieldOption):
#     pass


@dataclass
class MakeFieldOptional(BaseFieldOption):
    pass


@dataclass
class DerivationTemplate:
    def get_field_types(self) -> Dict[str, Type]:
        return {}


def get_default_applied_to_template(
    template: DerivationTemplate,
    default_field_option: BaseFieldOption,
):
    return {
        key: default_field_option if value == (None,) else value
        for key, value in template.__dict__.items()
    }


def get_filtered_fields(
    template: DerivationTemplate,
    default_field_option: BaseFieldOption,
):

    options = get_default_applied_to_template(
        template=template,
        default_field_option=default_field_option,
    )

    field_types = template.get_field_types()
    return {
        key: value
        for key, value in field_types.items()
        if not isinstance(options.get(key), OmitField)
        and options.get(key) is not OmitField
    }