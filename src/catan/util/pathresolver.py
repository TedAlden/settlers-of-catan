import pathlib

this_file = pathlib.Path(__file__).absolute()
src_dir = this_file.parent.parent.parent


def resolve_path(path):
    return src_dir.joinpath(path)
