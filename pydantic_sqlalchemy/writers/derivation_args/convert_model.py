from typing import List

from sqlalchemy import Enum as SQLAlchemyEnum, ColumnDefault

from pydantic_sqlalchemy.extract_from_sqlalchemy import ExtractedField, GeneratedImportReference, ExtractedModel
from pydantic_sqlalchemy.module_path_typ import get_mangled_module_path_as_name
from pydantic_sqlalchemy.utils.trim_indent import TrimIndent


def stringify_field_type(extracted_field: ExtractedField):
    field = extracted_field.typ
    typ_str = ''
    if isinstance(field, GeneratedImportReference):
        typ_str = f"{get_mangled_module_path_as_name(field.module_path)}.{field.name}DerivationTemplate"
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


def collected_model_to_derivation_args(
        model: ExtractedModel,
        import_statements: List[str],
        exclude_relations: bool = False,
):
    field_types = [
        f"'{name}': {stringify_field_type(extracted_field)},"
        for name, extracted_field in model.fields.items()
        if not (
            exclude_relations and isinstance(extracted_field.typ, GeneratedImportReference)
        )
    ]
    field_derivation_args = [
        f"{name}: Optional[BaseFieldOption] = None,"
        for name, extracted_field in model.fields.items()
        if not (
            exclude_relations and isinstance(extracted_field.typ, GeneratedImportReference)
        )
    ]
    return [
        "",
        "@dataclass",
        f"class {model.ref.name}DerivationTemplate(DerivationTemplate):",
        TrimIndent(field_derivation_args),
        TrimIndent([
            '',
            '@classmethod',
            'def get_field_types(cls):',
            TrimIndent(import_statements),
            TrimIndent([
                'return {',
                TrimIndent(field_types),
                '}',
            ]),
        ]),
    ]
