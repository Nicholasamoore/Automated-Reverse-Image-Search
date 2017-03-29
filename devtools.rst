==================
Development Tools
==================

Sphinx
=======
* Used to write this lab report
* Handy for grouping together multiple .rst files into an easily readable and navigable webpage

Git/Github
===========
* Source control software
* Used to allow multiple team members to contribute to the project without creating conflicts
* Allows for backup and retreival of project files
* Creates easily accessable repository hosted off-site (Github)  

Python - read.py
=================
The first revision of read.py received a string as an argument using argv[1] (The filename of the text file provided by Mike's code), opened the file, and displayed the text. Initially, we tried using the gitpython module to push our transcribed text files to the group project repo but it didn't work properly inside the docker container.

The latest revision of read.py receives the transcribed text as a string in argv[1] through the read() function. It uses the datetime, os (getcwd), and os.path (dirname, abspath) modules. The current timestamp is placed into the filename of the text document, that file is created in the proper directory, and then the transcription is written to the text file. We are hoping to use the functionality of an SSH key and bash scripting to push straight to the project repo instead of using the gitpython module.

Key components:

* datetime.today().now().time() - returns a current timestamp.
* getcwd - returns the current working directory.
* abspath() - returns a normalized absolutized version of the pathname provided.
* dirname(abspath) - returns the directory name of pathname abspath.

