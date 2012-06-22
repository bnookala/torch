SHOW_BIG_TEXT = """
(function () {
	var body = document.getElementsByTagName('body')[0];
	var flameIDNode = document.createElement('h1');
	var textNode = document.createTextNode('%(text)s');
	flameIDNode.setAttribute('style', 'position:fixed;top:0;left:0;z-index:9999999;height:100%%;text-align:center;margin: 0 auto;color:purple;font-size:200px;');
	flameIDNode.setAttribute('id', 'flame-enumerate-text');
	flameIDNode.appendChild(textNode);
	body.appendChild(flameIDNode);

	window.setTimeout(function () {
		body.removeChild(flameIDNode);
	}, 5000);
})();
"""
