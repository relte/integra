#!/bin/sh

rm -rf build/* dist/*
pyinstaller run.spec
./dist/integra/integra init
tar -zcvf ./dist/integra-$1.tar.gz ./dist/integra
