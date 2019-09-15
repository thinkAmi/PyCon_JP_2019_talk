# PyCon JP 2019 サンプル
import h5pyd

f = h5pyd.File("/nrel/wtk-us.h5", 'r')
one_value = f["windspeed_100m"][42, 42, 42]
print(one_value)
# => 9.1708145

# 参考
# https://ntrs.nasa.gov/search.jsp?R=20190027499
# https://earthdata.nasa.gov/esds/competitive-programs/access/hsds
# https://aws.amazon.com/jp/blogs/big-data/power-from-wind-open-data-on-aws/
# https://github.com/NREL/hsds-examples