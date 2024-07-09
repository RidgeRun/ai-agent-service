#!/bin/bash

# This script has to be called from the root of the repository

if [[ $# -eq 0 ]] ; then
    echo "Usage: $0 <VERSION_NUMBER>"
    exit 0
fi

VERSION=${1}

# service-template a.b.c
sed -i "s/## AI Agent Microservice [[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+/## AI Agent Microservice ${VERSION}/g" README.md
#version="a.b.c"
sed -i "s/version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/version=\"${VERSION}\"/g" setup.py
# release = 'a.b.c'
sed -i "s/release = '[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+'/release = '${VERSION}'/g" docs/source/conf.py
# version: a.b.c
sed -i "s/version: [[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+/version: ${VERSION}/g" api/openapi.yaml
