#=
language_binding:
- Julia version: 
- Author: thinkAmi
- Date: 2019-09-17
=#

using HDF5

h5open("output/h5py/binding.h5", "r") do f
    dataset = read(f, "hello")
    print(dataset[1])  # Juliaのindexは1始まり
    # => ワールド
end
