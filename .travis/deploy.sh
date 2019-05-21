#!/bin/bash

set -e -x

echo "deploy"

# remove left over files from previous steps
rm -rf build dist
mkdir dist

#python setup.py bdist_wheel
#rm dist/* build/*
# On linux we want to build `manylinux1` wheels. See:
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
	docker run --rm -v $(pwd):/io ${WHEELBUILDER_IMAGE} /io/.travis/build-linux-wheels.sh
else
	# Only build wheels for the non experimental bundled version
	if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
		python -m pip install wheel
		python setup.py bdist_wheel sdist
	fi
fi

ls -l dist

python -m pip install twine

# Ignore non-existing files in globs
shopt -s nullglob

twine upload --skip-existing dist/progpow*.{whl,gz} -u "${PYPI_USERNAME}" -p "${PYPI_PASSWORD}"

set +e +x

