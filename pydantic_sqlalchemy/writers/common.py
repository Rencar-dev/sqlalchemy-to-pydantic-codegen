import os

from pydantic_sqlalchemy.module_path_typ import ModulePathType, get_child_modules_path, to_fs_path


def ensure_file_module_path(
        module_path: ModulePathType,
        base_path: str = '__generated',
):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    child_module_paths = get_child_modules_path(module_path)
    for child_module_path in child_module_paths:
        to_generate_folder = to_fs_path(
            module_path=child_module_path,
            base_path=base_path,
        )
        to_generate_file = os.path.join(to_generate_folder, '__init__.py')
        if not os.path.exists(to_generate_folder):
            os.mkdir(to_generate_folder)
        if not os.path.exists(to_generate_file):
            with open(to_generate_file, 'w') as f:
                f.write('')
    # TODO not a good practice...
    last = child_module_paths[-1]
    return os.path.join(
        to_fs_path(module_path, base_path=base_path),
        '__init__.py',
    )
