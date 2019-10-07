#!/bin/sh

rm -rf build/* dist/*
pyinstaller run.spec
./dist/integra/integra init
