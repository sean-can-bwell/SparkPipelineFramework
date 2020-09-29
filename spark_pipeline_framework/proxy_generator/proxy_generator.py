from os import walk, path, listdir
from re import search
from shutil import rmtree
from typing import Match, Optional, List


class ProxyGenerator:
    @staticmethod
    def remove_empty_dirs(folder: str) -> None:
        def is_path_empty(directory: str):
            for dir_tuple in walk(directory):
                if [
                    file for file in dir_tuple[2] if not (file.startswith(('__', '.')) or file.endswith('.pyc'))
                ]:
                    return False
            return True

        for path_tuple in walk(folder):
            # noinspection SpellCheckingInspection
            if path_tuple[0].endswith('__pycache__'):
                pass
            else:
                current_path: str = path.join(folder, path_tuple[0])
                if is_path_empty(current_path):
                    try:
                        rmtree(current_path)
                    except FileNotFoundError:
                        pass
                    else:
                        print(f'Removed {current_path}')

    @staticmethod
    def generate_proxies(folder: str) -> None:
        all_objects_in_path: List[str] = listdir(folder)
        non_special_objects: List[str] = [
            file for file in all_objects_in_path if not file.startswith(('_', '.'))
        ]
        # noinspection SpellCheckingInspection
        folders: List[str] = [
            subfolder for subfolder in non_special_objects if
            '.' not in subfolder and len(listdir(path.join(folder, subfolder))) != 0
        ]
        files: List[str] = [
            file for file in all_objects_in_path if '.' in file and not file.startswith('_')
        ]
        transformer_file_indicators = ('.sql', '.csv', '.py')
        path_contains_transformer: bool = len(
            [file for file in files if file.endswith(transformer_file_indicators)]) > 0

        if path_contains_transformer:
            for file in files:
                if file.endswith(transformer_file_indicators):
                    search_result: Optional[Match[str]] = search(r'/library/', folder)
                    if search_result:
                        transformer_reader_file_name = folder[search_result.end():].replace('/', '_')
                        ProxyGenerator.write_transformer(
                            file_name=transformer_reader_file_name,
                            folder=folder
                        )

        # now recursively generate proxies
        # noinspection SpellCheckingInspection
        for subfolder in folders:
            ProxyGenerator.generate_proxies(path.join(folder, subfolder))

    @staticmethod
    def write_transformer(file_name: str, folder: str) -> None:
        transformer_reader_class_name = ''.join([s.title() for s in file_name.split('_')])
        transformer_reader_string = f"""
from typing import Optional
from spark_pipeline_framework.proxy_generator.proxy_base import ProxyBase
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.utilities.attr_dict import AttrDict
from os import path


# This file was auto-generated by generate_proxies(). It enables auto-complete in PyCharm. Do not edit manually!
class {transformer_reader_class_name}(ProxyBase):
    def __init__(self,
                 parameters: AttrDict,
                 progress_logger: Optional[ProgressLogger] = None,
                 verify_count_remains_same: bool = False
                 ) -> None:
        location: str = path.dirname(path.abspath(__file__))
        super().__init__(
            parameters=parameters,
            location=location,
            progress_logger=progress_logger,
            verify_count_remains_same=verify_count_remains_same
        )
    """
        transformer_proxy_file_name: str = path.join(folder, file_name + '.py')
        if not path.exists(transformer_proxy_file_name):
            with open(transformer_proxy_file_name, 'w+') as file:
                print(f"Creating {transformer_proxy_file_name}")
                file.write(transformer_reader_string)
