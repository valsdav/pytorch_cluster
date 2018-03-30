import os.path as osp
import shutil
import subprocess

import torch
from torch.utils.ffi import create_extension

if osp.exists('build'):
    shutil.rmtree('build')

files = ['serial', 'grid']

headers = ['torch_cluster/src/{}_cpu.h'.format(f) for f in files]
headers += ['aten/TH/THGreedy.h', 'aten/TH/THGrid.h']
sources = ['torch_cluster/src/{}_cpu.c'.format(f) for f in files]
sources += ['aten/TH/THGreedy.c', 'aten/TH/THGrid.c']
include_dirs = ['torch_cluster/src', 'aten/TH']
define_macros = []
extra_objects = []
with_cuda = False

if torch.cuda.is_available():
    subprocess.call(['./build.sh', osp.dirname(torch.__file__)])

    headers += ['torch_cluster/src/{}_cuda.h'.format(f) for f in files]
    sources += ['torch_cluster/src/{}_cuda.c'.format(f) for f in files]
    include_dirs += ['torch_cluster/kernel']
    define_macros += [('WITH_CUDA', None)]
    extra_objects += ['torch_cluster/build/{}.so'.format(f) for f in files]
    with_cuda = True

ffi = create_extension(
    name='torch_cluster._ext.ffi',
    package=True,
    headers=headers,
    sources=sources,
    include_dirs=include_dirs,
    define_macros=define_macros,
    extra_objects=extra_objects,
    with_cuda=with_cuda,
    relative_to=__file__)

if __name__ == '__main__':
    ffi.build()
