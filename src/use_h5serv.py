# PyCon JP 2019 サンプル

from pathlib import Path

import h5py
import requests

FILENAME = 'test'
URL_BASE = f'http://{FILENAME}.example.com:5000/'


# あらかじめ、所定のディレクトリに、HDF5ファイルを作成しておく
# デフォルトでは、h5servディレクトリの中にある、`data` ディレクトリが使われる
# 今回の例では、use_h5serv.pyと同階層に、h5servをgit cloneしてある
# 作成しない場合、TOCファイルの中にデータが保存される
# また、ローカルで動かす場合は、事前に /etc/hosts ファイルにドメイン部分(example.com)を記載する
p = Path(__file__).resolve().parents[0].joinpath('h5serv', 'data', f'{FILENAME}.h5')
with h5py.File(p, mode='w') as f:
    pass

# Datasetの型をPOST
str_type = {'charSet': 'H5T_CSET_UTF8',
            'class':   'H5T_STRING',
            'strPad':  'H5T_STR_NULLTERM',
            'length':  'H5T_VARIABLE'}
payload = {'type': str_type, 'shape': 1}

res1 = requests.post(
    URL_BASE + 'datasets',
    json=payload
).json()

print(res1)


# HDF REST APIに従い、Datasetの中身をPUT
url = URL_BASE + 'datasets/' + res1.get('id') + '/value'

res2 = requests.put(
    url,
    json={
        'value': 'ワールド'
    }
)

print('-' * 30)
print(res2)


# Datasetの中身をGETして、中身を確認
res3 = requests.get(
    URL_BASE + 'datasets/' + res1.get('id') + '/value'
).json()

print('-' * 30)
print(res3)
print(res3.get('value'))
