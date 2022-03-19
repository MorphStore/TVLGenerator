import argparse
import logging
from pathlib import Path

from core.tvlgenerator import TVLGenerator


def existing_path(path_str: str):
    p = Path(path_str).resolve()
    outpath = Path(p).relative_to(Path(".").resolve())
    if p.exists():
        if p.is_dir():
            return str(outpath)
        raise argparse.ArgumentError(f"{p} is already present but not a directory.")
    p.mkdir(parents=True)
    return str(outpath)

if __name__ == '__main__':
    logging.basicConfig(#filename="tvlgen.log",
                        format='[%(asctime)s %(levelname)-8s %(name)s::%(decorated_funcName)s (%(decorated_filename)s)]: %(message)s',
                        datefmt='%d.%m.%Y %I:%M:%S %p',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description="TVL Generator")
    parser.add_argument(
        '-o', '--outpath',
        default="./generated/",
        type=existing_path,
        help='Relative or absolut path where TVL should be generated into.',
        dest='outpath')
    parser.add_argument(
        '-t', '--targets',
        default=None,
        nargs='*',
        dest='targets'
    )
    parser.add_argument(
        '-d', '--datapath',
        default="./primitive_data/",
        type=existing_path,
        help='Relative or absolut path where TVL primitive and extension files are located.',
        dest='datapath')
    args = parser.parse_args()
    generator = TVLGenerator(
        Path(args.outpath),
        Path("config/data/templates"),
        Path("config/data/tvl_generator_schema.yaml"),
        Path(args.datapath),
        Path("static_files")
    )
    generator.import_data()
    generator.create_generated_files(args.targets)
    generator.create_static_files()
    
