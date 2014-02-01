(function run() {
    var $uploadform = $('#upload');

    $uploadform.on('submit', function(e) {
        e.preventDefault()
        var files = $('#input').get(0).files;

        var reader = FileReader();

        reader.readAsBinaryString(files[0]);

        console.log(files);
    });


})()
