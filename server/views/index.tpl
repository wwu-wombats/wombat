<html>
<head>
    <title>Webfs</title>
</head>
<body>
    <div id="urls">
      <a href="/">index</a> <a href="/logout">logout</a>
    </div>
    <h2>Welcome to Wombat</h2>
    <p>Welcome {{current_user.username}}, your role is: {{current_user.role}}</p>

    <input type="file" id="files" name="files[]" multiple>
    <output id="list"><ul></ul></output>

    <script src="/js/libs/jquery-2.1.0.min.js"></script>
    <script src="/js/libs/aes.js"></script>
    <script src="/js/libs/underscore-min.js"></script>
    <script src="/js/webfs.js"></script>

    <script id="encryptworker" type="javascript/worker">
        importScripts("js/libs/aes.js");
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
        //importScripts("libs/aes.js");
        self.onmessage = function(e) {
            var recv = JSON.parse(e.data);
            var encrypted = CryptoJS.AES.encrypt(recv.payload, "secretkey", { format: JsonFormatter });
            var data = JSON.stringify({title: recv.title, part: recv.part, payload: JSON.parse(encrypted.toString())});
            self.postMessage(data);
        }
    </script>
    <script id="decryptworker" type="javascript/worker">
        importScripts("libs/aes.js");
        self.onmessage = function(e) {
        }
    </script>
</body>
</html>
