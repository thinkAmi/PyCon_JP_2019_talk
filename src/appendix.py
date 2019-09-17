# 圧縮したデータの読込
import h5py
import os
import pathlib
import numpy as np


BASE_DIR = pathlib.Path(__file__).resolve().parents[0]
INPUT_DIR = BASE_DIR.joinpath('input')
OUTPUT_DIR = BASE_DIR.joinpath('output', 'h5py')
TYPE_OF_BINARY = h5py.special_dtype(vlen=np.dtype('uint8'))


def create_excel(filename, is_compression=False):

    with h5py.File(filename, mode='w') as file:
        excel_path_for_read = INPUT_DIR.joinpath('mybook.xlsx')
        with excel_path_for_read.open(mode='rb') as excel:
            excel_binary = excel.read()

        excel_data = np.frombuffer(excel_binary, dtype='uint8')

        params = {
            'dtype': TYPE_OF_BINARY
        }

        # ロスレスな圧縮形式は gzip の他に、lzf・szipがある
        # また、独自の圧縮フィルターも指定できる
        # http://docs.h5py.org/en/stable/high/dataset.html#lossless-compression-filters
        if is_compression:
            params['compression'] = 'gzip'

        ds_excel = file.create_dataset(
            'spec', excel_data.shape, **params
        )
        ds_excel[0] = excel_data

        print(f'{os.path.getsize(filename)} [compress: {is_compression}]')


def open_excel(h5_path, excel_path):
    with h5py.File(h5_path, mode='r') as file:
        dataset = file['spec']
        with excel_path.open('wb') as w:
            w.write(dataset[0])

    # 拡張子"xlsx"に関連付けされたアプリで開く
    os.system(f'open {excel_path}')  # Macの場合


def use_visititems():
    def create_dataset(target, value):
        ds_str = target.create_dataset(
            name='apple', shape=(1,), dtype=h5py.string_dtype())
        ds_str[0] = value

    def visit_items_callback(name, obj):
        v = 'Group' if isinstance(obj, h5py.Group) else obj[0]

        print(f'name: {name}, type: {type(obj)}, value: {v}')

    # groupをネストして使ってみる
    output = OUTPUT_DIR.joinpath('visititems.h5')
    with h5py.File(output, mode='w') as file:
        # 1階層目にGroup2つとDataset
        child_group = file.create_group('child')
        create_dataset(file, 'つがる')
        file.create_group('foo')

        # 2階層目にGroupとDataset
        grandchild_group = child_group.create_group('grandchild')
        create_dataset(child_group, 'シナノレッド')

        # 3階層目にDataset
        create_dataset(grandchild_group, 'シナノリップ')

    # visititemsを使ってみる
    with h5py.File(output, mode='r') as file:
        # fileオブジェクトに対して実行
        file.visititems(visit_items_callback)
        print('-' * 40)
        # =>
        # name: apple, type: <class 'h5py._hl.dataset.Dataset'>, value: つがる
        # name: child, type: <class 'h5py._hl.group.Group'>, value: Group
        # name: child/apple, type: <class 'h5py._hl.dataset.Dataset'>, value: シナノレッド
        # name: child/grandchild, type: <class 'h5py._hl.group.Group'>, value: Group
        # name: child/grandchild/apple, type: <class 'h5py._hl.dataset.Dataset'>, value: シナノリップ
        # name: foo, type: <class 'h5py._hl.group.Group'>, value: Group

        # 2階層目に対して実行
        child_group = file['child']
        child_group.visititems(visit_items_callback)
        print('-' * 40)
        # =>
        # name: apple, type: <class 'h5py._hl.dataset.Dataset'>, value: シナノレッド
        # name: grandchild, type: <class 'h5py._hl.group.Group'>, value: Group
        # name: grandchild/apple, type: <class 'h5py._hl.dataset.Dataset'>, value: シナノリップ

        # 3階層目に対して実行
        grandchild_group = file['child/grandchild']
        grandchild_group.visititems(visit_items_callback)
        # => name: apple, type: <class 'h5py._hl.dataset.Dataset'>, value: シナノリップ


if __name__ == '__main__':
    # Datasetが圧縮されていても、開く時は何も気にしなくて良い
    normal = OUTPUT_DIR.joinpath('normal_excel.h5')
    create_excel(normal, is_compression=False)
    normal_excel = OUTPUT_DIR.joinpath('normal.xlsx')
    open_excel(normal, normal_excel)

    compression = OUTPUT_DIR.joinpath('compression_excel.h5')
    create_excel(compression, is_compression=True)
    compression_excel = OUTPUT_DIR.joinpath('compression.xlsx')
    open_excel(compression, compression_excel)

    # h5servはロックがかかる
    # https://github.com/HDFGroup/h5serv/issues/127

    # visititems()メソッドをネストしたグループにも使ってみる
    use_visititems()