/api 
====
Get the status of the API

::returns: { status: 'code', time: 'timestamp' }

/api/upload
===========
Post data to this route to upload a file

/api/download/<file>
====================
File: is the name of a file as it is stored on the filesystem
it can have some number of path segments infront eg. /api/download/test/test.txt

::returns: a file

/api/list/[<directory>]
=======================
Directory: a subdirectory that you want the contents of

::returns: json array of the form { items: ['1', '2', ...] }

