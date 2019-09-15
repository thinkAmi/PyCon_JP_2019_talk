# PyCon JP 2019 サンプル

import pathlib
import hashlib

import h5py

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]

output = BASE_DIR.joinpath('output', 'h5py', 'cross_platform.h5')
with h5py.File(output, mode='w') as file:
    dataset = file.create_dataset(
        name='hello', shape=(1,), dtype=h5py.string_dtype())
    dataset[0] = 'ワールド'

# ファイルのMD5を出力しておく
output_md5 = BASE_DIR.joinpath('output', 'h5py', 'cross_platform_md5.txt')
output_md5.write_text(hashlib.md5(output.read_bytes()).hexdigest())

