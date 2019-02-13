from cffi import FFI
import os
from os import path
import errno
import subprocess
import glob

def absolute(*paths):
    op = os.path
    return op.realpath(op.abspath(op.join(op.dirname(__file__), *paths)))

base_dir = absolute(path.dirname(__file__))
build_temp = path.join(base_dir, 'build')

try:
  os.makedirs(build_temp)
except OSError as e:
  if e.errno != errno.EEXIST:
    raise



def has_system_lib():
    ffi = FFI()
    try:
        ffi.dlopen("progpow")
        return True
    except OSError:
        if 'LIB_DIR' in os.environ:
            for path in glob.glob(path.join(os.environ['LIB_DIR'], "*progpow*")):
                try:
                    FFI().dlopen(path)
                    return True
                except OSError:
                    pass
        return False

def has_local_lib():
  path.exists(path.join(base_dir, 'libprogpow.so'))

def build_clib():    
    c_lib_dir = path.join(base_dir, "c_lib")
    c_files, cpp_files = glob.glob(path.join(c_lib_dir, '*.c')), glob.glob(path.join(c_lib_dir, '*.cpp'))
    subprocess.check_call(["gcc", '-fPIC', '-c',] + c_files, cwd=build_temp)
    subprocess.check_call(["g++", '-fPIC', '-c'] + cpp_files, cwd=build_temp)
    subprocess.check_call(["g++", '-fPIC', '-shared'] + glob.glob(path.join(build_temp, '*.o')) + [ '-o', 'libprogpow.so'], cwd=build_temp)
    subprocess.check_call(["cp", 'libprogpow.so', base_dir], cwd=build_temp)


def install():
    place = None
    if 'LIB_DIR' in os.environ:
      lib_dir =os.environ['LIB_DIR'] 
      if len(lib_dir):
        place = lib_dir.split(";")[0]
    if not place:
      place = '/usr/local/lib/' #TODO win and mac
    subprocess.check_call(["cp", 'libprogpow.so', place], cwd=base_dir)

def ensure_local():
  if not has_local_lib():
    build_clib()

def ensure_system():
  if not has_system_lib():
    ensure_local()
    install()


