# PyCon JP 2019 サンプル

import pathlib
import hashlib

import h5py

# ファイルで使う場合
# BASE_DIR = pathlib.Path(__file__).resolve().parents[0]

# REPLで使う場合
BASE_DIR = pathlib.Path.cwd()

# MD5を見て、同一ファイルを確認 (ファイルで使う場合は、'output' と 'h5py' をjoinpath()する)
input_hdf5 = BASE_DIR.joinpath('cross_platform.h5')
input_md5 = BASE_DIR.joinpath('cross_platform_md5.txt')
assert input_md5.read_text() == hashlib.md5(input_hdf5.read_bytes()).hexdigest()

with h5py.File(input_hdf5, mode='r') as f:
    dataset = f['hello']
    print(dataset[0])  # => ワールド
