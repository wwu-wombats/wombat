/api
====
Get the status of the API

::returns: { status: 'code', time: 'timestamp' }

/api/create/<file>
==================
Post data to this route to upload a file
{'payload': data }

/api/move
=========
Post two paths to this route to mave a to b
Post json {'src':'sourcepath', 'dest': 'destpath' }

/api/delete
==================
Post a path to the server for deletion
post json {'payload': "name of file to delete"}

/api/modify
===========
Post a modified file, remove old.

/api/download/<file>
====================
File: is the name of a file as it is stored on the filesystem
it can have some number of path segments infront eg. /api/download/test/test.txt

::returns: a file

/api/list/[<directory>]
=======================
Directory: a subdirectory that you want the contents of

::returns: json object of the form

.. code::

    {
        items: [{
            name: "filename",
            t: "file"
        }, {
            name: "dirname"
            t: "dir"
        }]
    }

/api/tree
=========

::returns: json object of the form 

.. code::

    {
        items: [{
            name: "filename",
            t: "file",
            items: "",
        }, {
            name: "dirname",
            t: "dir",
            items: [{
                 name: "filename",
                 t: "file",
                 items: "",
            }]
        }]
    }
