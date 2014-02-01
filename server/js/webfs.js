$(function() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // G2G
        document.getElementById('files').addEventListener('change', handleFileSelect, false);
    } else {
        alert('File APIs are not supported in this browser.');
    }
    var Templates = window.Templates;
    var encryptWorkerBlob = new Blob([document.querySelector('#encryptworker').textContent]);
    var decryptWorkerBlob = new Blob([document.querySelector('#decryptworker').textContent]);
    var SECRETKEY = "secretkey";

    // Read hash from url to get location.
    var hashre = /^#\/(.*)$/;
    function getHash() {
        var re = hashre.exec(window.location.hash);
        if (re) {
            return re[1] || '';
        } else {
            return '';
        }
    }
    var inithash = getHash();

    function loadDir() {
        // list files
        $.get("/api/list/" + getHash(), function(data) {
            $('#list').html(Templates.list(_.extend(data, { path: getHash() })));
            $('#list li.item.dir').click(function(e) {
                paths = getHash().split('/');
                paths.push($.trim($(this).text()));
                paths = _.without(paths, "", "#", undefined);
                console.log(paths.join('/'));
                window.location.hash = '/' + paths.join('/');
                loadDir();
            });
            $('#list li.item.file').click(function(e) {
                downloadFile(getHash() + '/' + $.trim($(this).text()), $.trim($(this).text()));
            });
            $('#list li.item.up').click(function(e) {
                path = window.location.hash.split('/');
                console.log(path);
                path.pop();
                console.log(path);
                window.location.hash = path.join('/');
                loadDir();
            });
        }, "json");
    }


    switch (getHash()) {
        default:
            loadDir();
    }

    function handleFileSelect(evt) {
        var files = evt.target.files; // FileList object
        var $outputlist = $('#uploaded ul');

        // files is a FileList of File objects. List some properties.
        var output = [];
        var request;
        for (var i = 0, f; f = files[i]; i++) {(
            // use a closure here, so each file (and reader) has it's own namespace
            function() {
                var reader = new FileReader(),
                    encryptWorker = new Worker(window.URL.createObjectURL(encryptWorkerBlob)),
                    filename = f.name,
                    filetype = f.type,
                    filesize = f.size,
                    filedate = f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                    progressevents = 0,
                    numprogresses = 0;
                //var encryptedPayload = new Array();
                var encryptedPayload = "";
                console.log("processing " + filename);
                console.log(encryptedPayload);
                encryptWorker.onmessage = function(e) {
                    console.log(e);
                    console.log(filename);
                    console.log(encryptedPayload);
                    var data = JSON.parse(e.data);
                    // we need to make sure we don't write this out of order.
                    //encryptedPayload.push(data);
                    encryptedPayload += data.payload;
                    if (numprogresses > 0) {
                        /*console.log(encryptedPayload);
                        var payload = "",
                            encryptedPayload = _.sortBy(encryptedPayload, function(peice) {
                                return peice.part;
                            });
                        _.each(encryptedPayload, function(peice) {
                            payload += peice.payload.ct;
                        });*/
                        var payload = encryptedPayload;
                        var sendrequest = $.ajax({
                            type: 'post',
                            url: "/api/create/" + filename,
                            dataType: 'json',
                            contentType: 'application/json',
                            data: JSON.stringify({payload: payload}),
                        });
                        sendrequest.always(function(e) {
                            console.log("done");
                            console.log(e);
                            if (e.status == 200) {
                                $outputlist.append([
                                    '<li><strong>', escape(filename), '</strong> (',
                                    filetype || 'n/a', ') - ', filesize,
                                    ' bytes, last modified: ', filedate, '</li>'
                                ].join(''));
                            } else {
                                alert("File upload failed!")
                            }
                        });
                    }
                }
                console.log(f);
                reader.onload = function(e) {
                    console.log("Loaded all of " + filename);
                    numprogresses = progressevents;
                };
                reader.onprogress = (function(filepart) {
                    return function(e) {
                        progressevents++;
                        var text = reader.result;
                        var message = JSON.stringify({
                            part: progressevents,
                            payload: text,
                            title: filename,
                            secretkey: SECRETKEY
                        });
                        encryptWorker.postMessage(message);
                        // Now we've got some funny stuff with concurrency.
                        // potentially we'll have a bunch of stuff sent out
                        // and need to wait for all to come back from the worker
                        // before sending off to the api.
                    };
                })();
                reader.readAsText(f);
            })()
        }
    }
    function downloadFile(filepath, filename) {
        console.log(filepath);
        $.get("/api/download/" + filepath, function(data) {
            var decryptWorker = new Worker(window.URL.createObjectURL(decryptWorkerBlob));
            decryptWorker.onmessage = function(e) {
                var recv = JSON.parse(e.data);
                console.log(recv);

                var file = new Blob([recv.payload], {
                    name: filename,
                    type: "image/png"
                });
                window.open(window.URL.createObjectURL(file));

                /*window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;

                window.requestFileSystem(window.TEMPORARY, 1024*1024, function(fs) {
                    fs.root.getFile(filename, {create: true}, function(fileEntry) {
                        fileEntry.createWriter(function(fileWriter) {
                            var blob = new Blob([recv.payload]);

                            fileWriter.addEventListener("writeend", function() {
                                // navigate to file, will download
                                //location.href = fileEntry.toURL();
                            }, false);

                            fileWriter.write(blob);
                        }, function() {});
                    }, function() {});
                }, function() {});*/
            }
            decryptWorker.postMessage(JSON.stringify({
                payload: data.payload,
                secretkey: SECRETKEY
            }));
        });
    }
});
