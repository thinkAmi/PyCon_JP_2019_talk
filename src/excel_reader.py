import hashlib
import pathlib

import h5py

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]
OUTPUT_DIR = BASE_DIR.joinpath('output', 'h5py')
ORIGINAL_EXCEL_PATH = OUTPUT_DIR.joinpath('original.xlsx')
GLEANING_HDF5_PATH = OUTPUT_DIR.joinpath('gleaning.h5')

STATISTICS_3MB = OUTPUT_DIR.joinpath('statistics_kenporonbun-toukei201604.xlsx')
STATISTICS_LINE = OUTPUT_DIR.joinpath('statistics_nenpou09.xlsx')
STATISTICS_IMAGE = OUTPUT_DIR.joinpath('statistics_2017_1_02.xlsx')


def calculate_md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def print_md5(path):

    dataset_name = f'excel_{path.stem}'
    with h5py.File(GLEANING_HDF5_PATH, mode='r') as file:
        dataset = file[dataset_name]
        export_path = path.parents[0].joinpath(f'{path.stem}_reader{path.suffix}')
        with export_path.open('wb') as w:
            w.write(dataset[0])

    to_md5 = calculate_md5(export_path)
    print(f'{path.name} MD5  : {to_md5}')


if __name__ == '__main__':
    print_md5(ORIGINAL_EXCEL_PATH)
    print_md5(STATISTICS_3MB)
    print_md5(STATISTICS_LINE)
    print_md5(STATISTICS_IMAGE)
