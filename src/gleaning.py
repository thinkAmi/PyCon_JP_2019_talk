import hashlib
import pathlib

import h5py

import numpy as np

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]
INPUT_DIR = BASE_DIR.joinpath('input')
OUTPUT_DIR = BASE_DIR.joinpath('output', 'h5py')
TYPE_OF_BINARY = h5py.special_dtype(vlen=np.dtype('uint8'))

ORIGINAL_EXCEL_PATH = OUTPUT_DIR.joinpath('original.xlsx')
GLEANING_HDF5_PATH = OUTPUT_DIR.joinpath('gleaning.h5')

STATISTICS_3MB = OUTPUT_DIR.joinpath('statistics_kenporonbun-toukei201604.xlsx')
STATISTICS_LINE = OUTPUT_DIR.joinpath('statistics_nenpou09.xlsx')
STATISTICS_IMAGE = OUTPUT_DIR.joinpath('statistics_2017_1_02.xlsx')


def calculate_md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def compare_excel(from_path):
    print(f'{from_path.name} --------->')

    # 元ExcelのMD5を見る
    from_md5 = calculate_md5(from_path)
    print(f'from MD5: {from_md5}')

    dataset_name = f'excel_{from_path.stem}'

    # gzip圧縮して、ExcelをHDF5ファイルに入れる
    with h5py.File(GLEANING_HDF5_PATH, mode='a') as file:
        with from_path.open(mode='rb') as excel:
            excel_binary = excel.read()

        excel_data = np.frombuffer(excel_binary, dtype='uint8')
        ds_excel = file.create_dataset(
            dataset_name, excel_data.shape, dtype=TYPE_OF_BINARY, compression='gzip')
        ds_excel[0] = excel_data

    # 取り出して、MD5を見る
    with h5py.File(GLEANING_HDF5_PATH, mode='r') as file:
        dataset = file[dataset_name]
        export_path = from_path.parents[0].joinpath(f'{from_path.stem}_after{from_path.suffix}')
        with export_path.open('wb') as w:
            w.write(dataset[0])

    to_md5 = calculate_md5(export_path)
    print(f'to MD5  : {to_md5}')

    assert from_md5 == to_md5


if __name__ == '__main__':
    # きれいなHDF5ファイルを使うため、事前に削除しておく
    if GLEANING_HDF5_PATH.exists():
        GLEANING_HDF5_PATH.unlink()

    compare_excel(ORIGINAL_EXCEL_PATH)
    compare_excel(STATISTICS_3MB)
    compare_excel(STATISTICS_LINE)
    compare_excel(STATISTICS_IMAGE)
