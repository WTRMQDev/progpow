#!/bin/bash

set -e
set -x

# Install a system package required by our library
yum install -y pkg-config libffi libffi-devel

# The whole auto* stack in CentOS is too old - see https://github.com/pypa/manylinux/issues/71
#wget -q https://ftp.gnu.org/gnu/autoconf/autoconf-latest.tar.gz && tar zxf autoconf-latest.tar.gz && cd autoconf* && ./configure > /dev/null && make install > /dev/null && cd ..
#wget -q https://ftp.gnu.org/gnu/automake/automake-1.15.tar.gz && tar zxf automake-*.tar.gz && cd automake* && ./configure > /dev/null && make install > /dev/null && cd ..
#wget -q https://ftp.gnu.org/gnu/libtool/libtool-2.4.5.tar.gz && tar zxf libtool-*.tar.gz && cd libtool* && ./configure > /dev/null && make install > /dev/null && cd ..

# Compile wheels
cp -r /io /local
mkdir wheelhouse
cd /local
rm libprogpow*.so _libprogpow0_9_*.o _libprogpow0_9_*.c
for PYBIN in /opt/python/*/bin; do
	if [[ ${PYBIN} != *"cp26"* && ${PYBIN} != *"cp27"* ]]; then
        ${PYBIN}/pip install cffi
	${PYBIN}/python setup.py bdist_wheel
        mv dist/progpow*.whl /wheelhouse
    fi
done

# Adjust wheel tags
cd /
mkdir out
for whl in wheelhouse/progpow*.whl; do
    auditwheel show $whl;
    auditwheel repair $whl --plat manylinux2010_x86_64 -w out
done

cp out/*.whl /io/dist

