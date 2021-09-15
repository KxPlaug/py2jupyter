import os
import json
from typing import Dict, Any, NoReturn
import uuid
import argparse


def fill_cell(filename: str, content: str) -> str:
    cell_template = {
        "cell_type": "code",
        "execution_count": None,
        "id": str(uuid.uuid4()),
        "metadata": {},
        "outputs": [],
        "source": []
    }
    file_name = f"#--*{filename}*--\n"
    cell_template['source'].append(file_name + content)
    return cell_template


def append_file_content(file_path: str, template_file: Dict[str, Any]) -> Dict[str, Any]:
    file = open(file_path, 'r',encoding='utf-8')
    file_content = "".join(file.readlines())
    cell_content = fill_cell(os.path.basename(file_path), file_content)
    template_file['cells'].append(cell_content)
    return template_file


def load_template_content(template_path: str) -> Dict[str, Any]:
    template_file = json.load(open(template_path, 'r'))
    return template_file


def main(dir_path: str, file_name: str, template_path='Template.json') -> NoReturn:
    py_file_paths = list()
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            if name.endswith('.py'):
                py_file_paths.append(os.path.join(root, name))
    template = load_template_content(template_path)
    for py_file_path in py_file_paths:
        template = append_file_content(py_file_path, template)
    f = open(f'{file_name}.ipynb', 'w')
    json.dump(template, f)
    f.close()
    return


if __name__ == '__main__':
    template_path = 'Template.json'
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-d', '--dir_path', type=str, required=True)
    parser.add_argument('-f', '--file_name', type=str, required=False, default='default')
    args = parser.parse_args()
    main(args.dir_path, args.file_name)