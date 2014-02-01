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
    var reader = new FileReader(),
        filename = f.name;
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
    reader.onload = (function(theFile) {
        return function (e) {
            var text = reader.result;
            var encrypted = CryptoJS.AES.encrypt(text, "asdf", { format: JsonFormatter });
            console.log(encrypted);
            var data = JSON.stringify({title: theFile.name, payload: encrypted + ""});
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
    })(f);
    reader.readAsText(f);
  }
  document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}
