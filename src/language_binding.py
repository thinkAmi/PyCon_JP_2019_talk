# PyCon JP 2019 サンプル

import pathlib

import h5py

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]

output = BASE_DIR.joinpath('output', 'h5py', 'binding.h5')
with h5py.File(output, mode='w') as file:
    dataset = file.create_dataset(
        name='hello', shape=(1,), dtype=h5py.string_dtype())
    dataset[0] = 'ワールド'
