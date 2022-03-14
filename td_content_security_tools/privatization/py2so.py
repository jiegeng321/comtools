import os
from pathlib import Path
from distutils.core import setup, Extension
from Cython.Build import cythonize
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--build_dir', type=str, default='build')
parser.add_argument('--source_dir', type=str, default='ai-logo-gen-dist')

args = parser.parse_args()

if __name__ == "__main__":
    build_dir = args.build_dir
    build_temp_dir = os.path.join(build_dir, 'temp')
    os.makedirs(build_temp_dir, exist_ok=True)
    path = Path(args.source_dir)
    python_scripts = [str(p) for p in path.rglob("*.py")]
    print("\n".join(python_scripts))
    exclude_files = [str(path / 'start.py')]
    print(*exclude_files, sep=',')
    extensions = []
    for s in python_scripts:
        moudle_name = os.path.splitext(
            s)[0].replace("/", ".").replace('-', '_')
        extensions.append(Extension(moudle_name, [s]))
    setup(ext_modules=cythonize(extensions,
          compiler_directives={'language_level': "3"},
          exclude=[__file__] + exclude_files),
          script_args=[
              "build_ext", '-b', build_dir, '-t', build_temp_dir])

    # clean
    shutil.rmtree(build_temp_dir)

    # remove temp c file
    for p in path.rglob("*.c"):
        os.remove(str(p))

    # copy asset
    asset_files = [p for p in path.rglob("*")
                   if str(p) not in python_scripts and not str(p).endswith('pyc')]

    print(f'copy asset file...')
    for asset in asset_files:
        if asset.is_file():
            rename_parts = []
            for p in asset.parts[:-1]:
                rename_parts.append(p.replace('-', '_'))
            output_name = f'{build_dir}/{os.path.join(*rename_parts)}/{asset.name}'
            output_dir = Path(output_name).parent
            os.makedirs(output_dir, exist_ok=True)
            shutil.copyfile(asset, output_name)

    print(f'copy program entrance and exclude file')
    # copy program entrance and other exclude file
    for f in exclude_files:
        try:
            shutil.copyfile(f, f'{build_dir}/{f.replace("-", "_")}')
        except Exception as e:
            print(e)
