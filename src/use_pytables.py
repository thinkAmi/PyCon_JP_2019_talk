# PyCon JP 2019 サンプル
import io
import os
import pathlib
import random

import h5py
import tables
from PIL import Image
from tables import VLUnicodeAtom
from tables.nodes import filenode

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]
INPUT_DIR = BASE_DIR.joinpath('input')
OUTPUT_DIR = BASE_DIR.joinpath('output', 'pytables')


def create_data_at_root_dir():
    # ルートディレクトリに文字を置く
    filepath = OUTPUT_DIR.joinpath('root_dataset_by_pytables.hdf5')
    with tables.open_file(filepath, 'w') as f:
        dataset = f.create_vlarray('/', 'root_dataset', atom=VLUnicodeAtom())
        dataset.append('シナノゴールド')


def read_dataset():
    # h5pyで読んでみると
    filepath = OUTPUT_DIR.joinpath('root_dataset_by_pytables.hdf5')
    with h5py.File(filepath, mode='r') as f:
        dataset = f['root_dataset']
        print(dataset[0])  # => [12471 12490 12494 12468 12540 12523 12489]

    # pytablesで読んでみる
    filepath = OUTPUT_DIR.joinpath('root_dataset_by_pytables.hdf5')
    with tables.open_file(filepath, 'r') as f:
        node = f.get_node(where='/', name='root_dataset')
        print(node)  # => /root_dataset (VLArray(1,)) ''

        for row in node.iterrows():
            print(row)  # => シナノゴールド


def create_dataset_with_group():
    # グループを作って、階層構造にする
    filepath = OUTPUT_DIR.joinpath('group_data.hdf5')
    with tables.open_file(filepath, mode='w') as f:
        # ルートは同じ
        # whereは、末尾に `/` を付けないと、グループとして認識してくれない
        dataset = f.create_vlarray('/', 'root_dataset', atom=VLUnicodeAtom())
        dataset.append('シナノゴールド')

        # グループを作る
        g1 = f.create_group('/', 'apple')
        g1_dataset = f.create_vlarray(g1, 'g1_dataset', atom=VLUnicodeAtom())
        g1_dataset.append('りんご')

        # あるグループのサブグループも作れる
        g1_sub = f.create_group(g1, 'sub1')
        g1_sub_dataset = f.create_vlarray(g1_sub, 'g1_sub_dataset', atom=VLUnicodeAtom())
        g1_sub_dataset.append('秋映')
        g1_sub_dataset.append('シナノスイート')

        # g1と同階層のグループも作れる
        g2 = f.create_group('/', 'grape')
        g2_dataset = f.create_vlarray(g2, 'g2_dataset', atom=VLUnicodeAtom())
        g2_dataset.append('ぶどう')


def create_image_dataset():
    # 画像ファイルを入れ込む
    filepath = OUTPUT_DIR.joinpath('image_data.hdf5')
    with tables.open_file(filepath, mode='w') as f:
        image_path = INPUT_DIR.joinpath('shinanogold.png')

        filenode.save_to_filenode(f, filename=image_path, where='/', name='image_node')
        # nameを指定しないと、拡張子の `.` を `_` に変換したものがNode名になる
        filenode.save_to_filenode(f, filename=image_path, where='/')


def read_image_dataset():
    filepath = OUTPUT_DIR.joinpath('image_data.hdf5')
    with tables.open_file(filepath, mode='r') as f:
        node = f.get_node(where='/', name='image_node')
        print(node)  # => /image_node (EArray(5584,)) ''
        print(type(node.read()))  # => <class 'numpy.ndarray'>

        img = Image.open(io.BytesIO(node.read()))
        img.show()


def create_excel_dataset():
    # Excelファイルを入れ込む (画像の時と同じ方法)
    filepath = OUTPUT_DIR.joinpath('excel_data.hdf5')
    with tables.open_file(filepath, mode='w') as f:
        image_path = INPUT_DIR.joinpath('mybook.xlsx')
        filenode.save_to_filenode(f, filename=image_path, where='/', name='excel_node')


def read_excel_dataset():
    filepath = OUTPUT_DIR.joinpath('excel_data.hdf5')
    with tables.open_file(filepath, mode='r') as f:
        node = f.get_node(where='/', name='excel_node')

        excel_path = OUTPUT_DIR.joinpath('excel.xlsx')
        with excel_path.open('wb') as w:
            w.write(node.read())


def compress_big_file():
    # 10MBくらいのバイナリファイルを作成し、圧縮効果を見る
    big_size_path = INPUT_DIR.joinpath('big.bin')
    if not big_size_path.exists():
        data = bytearray(random.getrandbits(8) for _ in range(10 * 1000 * 1000))

        with big_size_path.open(mode='wb') as f:
            f.write(data)

    print(f'original file: {os.path.getsize(big_size_path)}')  # => 10000000

    # HDF5ファイルに入れる & filter設定なし
    uncompression_file_path = OUTPUT_DIR.joinpath('big_size_data_without_compression.hdf5')
    with tables.open_file(uncompression_file_path, mode='w') as f:
        filenode.save_to_filenode(f, filename=big_size_path, where='/', name='big_size_data')

    print(f'uncompression file: {os.path.getsize(uncompression_file_path)}')  # => 10039272

    # # HDF5ファイルに入れる & filter 'lzo' を使用
    compression_file_path = OUTPUT_DIR.joinpath('big_size_data_with_compression.hdf5')
    with tables.open_file(compression_file_path, mode='w') as f:
        filters = tables.Filters(complib='lzo')
        filenode.save_to_filenode(f, filename=big_size_path, where='/', name='big_size_data',
                                  filters=filters)

    print(f'compression file: {os.path.getsize(compression_file_path)}')  # => 10039272
    # => すでに圧縮済とわかった


def set_attributes():
    attribute_file_path = OUTPUT_DIR.joinpath('attributes.hdf5')
    with tables.open_file(attribute_file_path, mode='w') as f:
        dataset = f.create_vlarray('/', 'dataset_attribute', atom=VLUnicodeAtom())
        dataset.append('datasetのattribute')
        dataset.set_attr('title', 'datasetのタイトル')

        group = f.create_group('/', 'group_attribute')
        print(dir(group))

        # "_" はじまりの属性なので、アクセスしてよいかが不明
        group._v_attrs['title'] = 'groupのタイトル'


def read_attributes():
    attribute_file_path = OUTPUT_DIR.joinpath('attributes.hdf5')
    with tables.open_file(attribute_file_path, mode='r') as f:
        dataset_node = f.get_node(where='/', name='dataset_attribute')
        if hasattr(dataset_node.attrs, 'title'):
            print(dataset_node.attrs.title)  # => datasetのタイトル

        group_node = f.get_node(where='/', name='group_attribute')
        # http://www.pytables.org/_modules/tables/attributeset.html
        print(group_node._v_attrs)  # => /group_attribute._v_attrs (AttributeSet), 4 attributes
        if hasattr(group_node._v_attrs, 'title'):
            print(group_node._v_attrs.title)  # => groupのタイトル
            print(group_node._v_attrs._v_attrnamesuser)  # => ['title']


def traverse():
    # list_nodes(), walk_groups(), walk_nodes() の違い
    group_path = OUTPUT_DIR.joinpath('group_data.hdf5')
    with tables.open_file(group_path, mode='r') as f:
        for n in f.list_nodes(where='/'):
            print(n)
            """
            /apple (Group) ''
            /grape (Group) ''
            /root_dataset (VLArray(1,)) ''
            """

        print('-' * 30)

        for n in f.walk_groups(where='/'):
            print(n)
            """
            / (RootGroup) ''
            /apple (Group) ''
            /grape (Group) ''
            /apple/sub1 (Group) ''
            """

        print('-' * 30)

        for n in f.walk_nodes(where='/'):
            print(n)
            """
            / (RootGroup) ''
            /apple (Group) ''
            /grape (Group) ''
            /root_dataset (VLArray(1,)) ''
            /apple/g1_dataset (VLArray(1,)) ''
            /apple/sub1 (Group) ''
            /grape/g2_dataset (VLArray(1,)) ''
            /apple/sub1/g1_sub_dataset (VLArray(2,)) ''
            """

        print('=' * 30)

    # attributeの検索
    attribute_path = OUTPUT_DIR.joinpath('attributes.hdf5')
    with tables.open_file(attribute_path, mode='r') as f:
        # walk_nodesを使って、attributeに"title"を持つ元を列挙しprint
        for n in f.walk_nodes(where='/'):
            if isinstance(n, (tables.Group, tables.group.RootGroup)):
                # group系の場合は、attrsがないので、_v_attrsから探す
                if 'title' in n._v_attrs._v_attrnamesuser:
                    print(f'title: {n._v_attrs.title}, Group: {n}')
                    # => title: groupのタイトル, Group: /group_attribute (Group) ''

            elif hasattr(n.attrs, 'title'):
                print(f'title: {n.attrs.title}, Object: {n}')
                # => title: datasetのタイトル, Object: /dataset_attribute (VLArray(1,)) ''


if __name__ == '__main__':
    # 必要なディレクトリはあらかじめ作っておく
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Dataset
    # ルートにdatasetを追加
    create_data_at_root_dir()
    # グループにdatasetを追加
    create_dataset_with_group()
    # datasetの読込
    read_dataset()

    # 画像
    # HDF5ファイルにdatasetとして追加
    create_image_dataset()
    # HDF5ファイルのdatasetから画像を復元
    read_image_dataset()

    # Excel
    # HDF5ファイルにdatasetとして追加
    create_excel_dataset()
    # HDF5ファイルのdatasetからExcelを復元
    read_excel_dataset()

    # HDF5ファイルの圧縮
    compress_big_file()

    # Attribute
    # dataset/groupへの追加
    set_attributes()
    # dataset/groupからの読込
    read_attributes()

    # オブジェクトの検索
    traverse()

