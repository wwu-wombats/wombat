$(function() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // G2G
        document.getElementById('files').addEventListener('change', handleFileSelect, false);
    } else {
        alert('File APIs are not supported in this browser.');
    }

    function handleFileSelect(evt) {
        var files = evt.target.files; // FileList object

        // files is a FileList of File objects. List some properties.
        var output = [];
        var request;
        for (var i = 0, f; f = files[i]; i++) {
            var encryptWorkerBlob = new Blob([document.querySelector('#encryptworker').textContent]);
            var reader = new FileReader(),
                encryptWorker = new Worker(window.URL.createObjectURL(encryptWorkerBlob)),
                filename = f.name,
                progressevents = 0,
                numprogresses = 0,
                encryptedPayload = [];
            encryptWorker.onmessage = function(e) {
                data = JSON.parse(e.data);
                // we need to make sure we don't write this out of order.
                encryptedPayload.push(data);
                if (numprogresses > 0) {
                    console.log(encryptedPayload);
                    var payload = ""
                        encryptedPayload = _.sortBy(encryptedPayload, function(peice) {
                            return peice.part;
                        });
                    _.each(encryptedPayload, function(peice) {
                        payload += peice.payload.ct;
                    });
                    $.post("http://67.201.205.18:8080/api/create/" + filename, {
                        payload: payload
                    }).done(function(e) {
                        console.log("done");
                        console.log(e);
                    }).fail(function(e, d) {
                        console.log("Failed");
                        console.log(e);
                        console.log(e);
                    }).always(function(e) {
                        console.log("totally done");
                        console.log(e);
                    });
                    request = $.ajax({
                        url: "",
                            type: "post",
                            data: { payload: payload },
                            contentType: 'application/json',
                            dataType: 'json',
                    });
                    request.done(function(response, textStatus, jqXHR){
                        console.log(response);
                        output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                            f.size, ' bytes, last modified: ',
                            f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                            '</li>');
                    });
                }
            }
            var JsonFormatter = {
                stringify: function (cipherParams) {
                    // create json object with ciphertext
                    var jsonObj = {
                        ct: cipherParams.ciphertext.toString(CryptoJS.enc.Base64)
                    };

                    // optionally add iv and salt
                    if (cipherParams.iv) {
                        jsonObj.iv = cipherParams.iv.toString();
                    }
                    if (cipherParams.salt) {
                        jsonObj.s = cipherParams.salt.toString();
                    }

                    // stringify json object
                    return JSON.stringify(jsonObj);
                },
                parse: function (jsonStr) {
                    // parse json string
                    var jsonObj = JSON.parse(jsonStr);

                    // extract ciphertext from json object, and create cipher params object
                    var cipherParams = CryptoJS.lib.CipherParams.create({
                        ciphertext: CryptoJS.enc.Base64.parse(jsonObj.ct)
                    });

                    // optionally extract iv and salt
                    if (jsonObj.iv) {
                        cipherParams.iv = CryptoJS.enc.Hex.parse(jsonObj.iv)
                    }
                    if (jsonObj.s) {
                        cipherParams.salt = CryptoJS.enc.Hex.parse(jsonObj.s)
                    }

                    return cipherParams;
                }
            };
            console.log(f);
            reader.onload = function() {
                numprogresses = progressevents;
            };
            reader.onprogress = (function(filepart) {
                return function(e) {
                    progressevents++;
                    console.log(progressevents + ' progress events have happened.');
                    console.log(e);
                    console.log(reader);
                    var text = reader.result;
                    var message = JSON.stringify({
                        part: progressevents,
                        payload: text,
                        title: filename
                    });
                    encryptWorker.postMessage(message);
                    // Now we've got some funny stuff with concurrency.
                    // potentially we'll have a bunch of stuff sent out
                    // and need to wait for all to come back from the worker
                    // before sending off to the api.
                };
            })();
            reader.readAsText(f);
        }
        document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
    }
});
