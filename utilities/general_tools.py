import os
import re


def get_dir_files_names(dir_name: str) -> list:
    """
    Returns list of all files (excluding temporary files) in given directory. Off course *NIX only!
    :param dir_name:
    :return:
    """
    raw_list = os.listdir(dir_name)
    names_pat = re.compile(r'(.+)\.[^.]*')
    temp_path = re.compile(r'^\.~.+')
    return [names_pat.match(name).group(1) for name in raw_list if not temp_path.match(name)]
