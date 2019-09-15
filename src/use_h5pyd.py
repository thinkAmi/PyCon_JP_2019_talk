# PyCon JP 2019 サンプル

from pathlib import Path

import h5py
import h5pyd

# URL_BASE = f'http://{SUB_DIR}.{FILENAME}.example.com:5000/'
FILENAME = 'h5pyd'
DIR = Path(__file__).resolve().parents[0].joinpath('h5serv', 'data')

p = DIR.joinpath(f'{FILENAME}.h5')
with h5py.File(p, mode='w') as f:
    pass

with h5pyd.File(f'{FILENAME}.example.com', mode='w',
                endpoint=f'http://localhost:5000') as file:

    ds_str = file.create_dataset(name='hello', data='world', dtype='S6')

    # byte型になるので、デコードしておく
    print(file['hello'].value.decode('utf-8'))
    # => hello
