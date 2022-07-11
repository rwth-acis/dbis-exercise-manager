# DBIS Exercise Manager

[![pypi](https://img.shields.io/pypi/pyversions/dbis-exc-manager)](https://pypi.org/project/dbis-exc-manager/)
[![PyPI Status](https://img.shields.io/pypi/v/dbis-exc-manager)](https://pypi.python.org/pypi/dbis-exc-manager/)
[![Github Actions Build](https://github.com/rwth-acis/dbis-exercise-manager/workflows/Build/badge.svg?branch=main)](https://github.com/rwth-acis/dbis-exercise-manager/actions?query=workflow%3ABuild+branch%3Amain)
[![GitHub issues](https://img.shields.io/github/issues/rwth-acis/dbis-exercise-manager.svg)](https://github.com/rwth-acis/dbis-exercise-manager/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/rwth-acis/dbis-exercise-manager.svg)](https://github.com/rwth-acis/dbis-exercise-manager/issues/?q=is%3Aissue+is%3Aclosed)

This class manages the state of the exercises.
Example for arguments:
ÜB 1, Aufgabe 2.3 a), 2 Punkte 
* exc = 1
* task = 2
* subtask = 3a)
* points = 2

Example usage:
``` python
exc = Exercise( 1 )
task1 = Task( exc, task = 1, subtask = "2 a)", points = 2 )
```