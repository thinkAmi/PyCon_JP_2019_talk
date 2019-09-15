# PyCon JP 2019 サンプル
import io
import os
import pathlib
import random

import h5py
import numpy as np
from PIL import Image

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]
INPUT_DIR = BASE_DIR.joinpath('input')
OUTPUT_DIR = BASE_DIR.joinpath('output', 'h5py')


def print_callback(name, obj):
    # コールバック関数
    print(f'name: {name}, type: {type(obj)}')


output = OUTPUT_DIR.joinpath('use_h5py.h5')
with h5py.File(output, mode='w') as file:

    # Group作成
    group = file.create_group('apple')

    # Groupの中にDataset作成
    # 文字列
    ds_str = group.create_dataset(
        # h5py 2.9までは、 dtype=h5py.special_dtype(vlen=str)
        name='name', shape=(1,), dtype=h5py.string_dtype())
    ds_str[0] = 'シナノゴールド'

    # 画像
    # 画像を読み込み
    image_path = INPUT_DIR.joinpath('shinanogold.png')
    with image_path.open(mode='rb') as img:
        image_binary = img.read()

    # NumPy配列化
    image_data = np.frombuffer(image_binary, dtype='uint8')

    # バイナリの型定義
    TYPE_OF_BINARY = h5py.special_dtype(vlen=np.dtype('uint8'))
    # 画像を設定
    ds_img = group.create_dataset(
        'image', image_data.shape, dtype=TYPE_OF_BINARY)
    ds_img[0] = image_data

    # Excel
    excel_path = INPUT_DIR.joinpath('mybook.xlsx')
    with excel_path.open(mode='rb') as excel:
        excel_binary = excel.read()

    excel_data = np.frombuffer(excel_binary, dtype='uint8')

    ds_excel = group.create_dataset(
        'spec', excel_data.shape, dtype=TYPE_OF_BINARY)
    ds_excel[0] = excel_data

    # Attribute
    # Groupにattributeを追加
    group.attrs['title'] = 'りんご情報'

    # Datasetにattributeを追加
    ds_str.attrs['color'] = '黄色系'

# データの読込
with h5py.File(output, mode='r') as file:
    # Dataset (文字列)
    rds_str = file['apple/name']
    print(rds_str[0])  # => シナノゴールド

    # Dataset (画像)
    rds_img = file['apple/image']
    # 参考 https://github.com/h5py/h5py/issues/745#issuecomment-339451940
    Image.open(io.BytesIO(rds_img[0])).show()

    # Dataset (Excel)
    dataset = file['apple/spec']

    excel_path = OUTPUT_DIR.joinpath('spec.xlsx')
    with excel_path.open('wb') as w:
        w.write(dataset[0])

    # 拡張子"xlsx"に関連付けされたアプリで開く
    os.system(f'open {excel_path}')  # Macの場合

    # データの検索
    # visititemsを使って、attributeに"title"を持つものを列挙しprint
    file.visititems(print_callback)
    # =>
    # name: apple, type: <class 'h5py._hl.group.Group'>
    # name: apple/excel, type: <class 'h5py._hl.dataset.Dataset'>
    # name: apple/image, type: <class 'h5py._hl.dataset.Dataset'>
    # name: apple/name, type: <class 'h5py._hl.dataset.Dataset'>


# ファイルの圧縮
# 準備
big_size_path = INPUT_DIR.joinpath('big.bin')
if not big_size_path.exists():
    data = bytearray(random.getrandbits(8) for _ in range(10 * 1000 * 1000))

    with big_size_path.open(mode='wb') as file:
        file.write(data)

print(f'{str(os.path.getsize(big_size_path)).rjust(10)} [original]')
# => 10000000 [original] (約10MB)

with big_size_path.open(mode='rb') as big_size:
    big_size_binary = big_size.read()
big_size_data = np.frombuffer(big_size_binary, dtype='uint8')

# h5py：HDF5ファイルに入れる & 無圧縮
uncompression_file_path = OUTPUT_DIR.joinpath(
    'big_size_data_without_compression.h5')
with h5py.File(uncompression_file_path, mode='w') as file:
    uncompression = file.create_dataset(
        'big_size_data', big_size_data.shape, dtype=TYPE_OF_BINARY)
    uncompression[0] = big_size_data

print(f'{str(os.path.getsize(uncompression_file_path)).rjust(10)}'
      f' [uncompress]')
# => 170002080 [uncompress] (約170MB)

# HDF5ファイルに入れる & gzipで圧縮
compression_file_path = OUTPUT_DIR.joinpath(
    'big_size_data_with_compression.h5')
with h5py.File(compression_file_path, mode='w') as file:
    compression = file.create_dataset(
        'big_size_data', big_size_data.shape, dtype=TYPE_OF_BINARY,
        compression='gzip')
    compression[0] = big_size_data

print(f'{str(os.path.getsize(compression_file_path)).rjust(10)}'
      f' [compress]')
# => 10003716 [compress] (約10MB)

