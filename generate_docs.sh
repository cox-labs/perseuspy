#!/bin/bash
sphinx-apidoc -f -o docs perseuspy perseuspy/test/*
cd docs && make html
