import os


def normalize_path(real_path: str, desired_path_from_file: str) -> str:
    """
    Normalize a path given a real path and a desired path from the file

    :param real_path: Path provided using os.path.realpath(__file__)
    :param desired_path_from_file: Path to the desired file from the current file
    :return: the normalized path
    """
    current_script_path = os.path.dirname(real_path)
    combined_path = os.path.join(current_script_path, desired_path_from_file)
    fixed_path = os.path.normpath(combined_path)

    if not os.path.isfile(fixed_path):
        raise FileNotFoundError(f"File {fixed_path} not found")

    return fixed_path

