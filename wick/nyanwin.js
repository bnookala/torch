var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js';
script.onload = function() {
    window.darwinStart = function() {
        var darwin = jQuery('<div style="width:100px; height:100px; background: pink; position: fixed; top: 10px; left: 0; z-index:999999;"></div>');
        $('body').append(darwin);
        darwin.animate({'left': $('body').width()}, 4000, null, function() {
            jQuery.get(window.nyanwinDoneUrl);
        });
    };
    window.darwinStart();
};
document.getElementsByTagName('head')[0].appendChild(script);
