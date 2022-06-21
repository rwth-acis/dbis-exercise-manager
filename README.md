# DBIS Exercise Manager

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