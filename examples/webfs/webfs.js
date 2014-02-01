function init() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // G2G
        document.getElementById('files').addEventListener('change', handleFileSelect, false);
    } else {
        alert('File APIs are not supported in this browser.');
    }
}


function handleFileSelect(evt) {
  var files = evt.target.files; // FileList object

  // files is a FileList of File objects. List some properties.
  var output = [];
  var request;
  for (var i = 0, f; f = files[i]; i++) {
    output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                f.size, ' bytes, last modified: ',
                f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                '</li>');
    var encryptWorkerBlob = new Blob([document.querySelector('#encryptworker').textContent]);
    var reader = new FileReader(),
        encryptWorker = new Worker(window.URL.createObjectURL(encryptWorkerBlob)),
        filename = f.name;
    var fsize = f.size;
    var slicesize = 1024;
    encryptWorker.onmessage = function(e) {
        console.log("Received: " + e.data);
    }
    console.log(f);
    /*reader.onload = (function(filepart) {
        return function (e) {
            console.log(e);
            console.log(reader);
            var text = reader.result;
            var encrypted = CryptoJS.AES.encrypt(text, "secretkey", { format: JsonFormatter });
            var data = JSON.stringify({title: filepart.name, payload: encrypted + ""});
            destencrypted.push(data);
            console.log(Object.keys(reader));
            request = $.ajax({
                url: "/upload",
                type: "post",
                data: data,
                contentType: 'application/json',
                dataType: 'json',
            });
            request.done(function(response, textStatus, jqXHR){
                console.log("Done.");
            });
        };
    })();*/
    reader.onprogress = (function(filepart) {
        return function (e) {
            console.log(e);
            console.log(reader);
            var text = reader.result;
            encryptWorker.postMessage(text);
            /*request = $.ajax({
                url: "/upload",
                type: "post",
                data: data,
                contentType: 'application/json',
                dataType: 'json',
            });
            request.done(function(response, textStatus, jqXHR){
                console.log("Done.");
            });*/
        };
    })();
    reader.readAsText(f);
  }
  document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}
