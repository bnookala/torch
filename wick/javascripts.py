SHOW_BIG_TEXT = """
(function () {
	var body = document.getElementsByTagName('body')[0];
	var flameIDNode = document.createElement('h1');
	var textNode = document.createTextNode('%(text)s');
	flameIDNode.setAttribute('style', 'z-index:9999999;position:absolute;width:100%%;height:100%%;top:0;left:0;margin-left:auto;margin-right:auto;color:red;font-size:300px;');
	flameIDNode.setAttribute('id', 'flame-enumerate-text');
	flameIDNode.appendChild(textNode);
	body.appendChild(flameIDNode);

	window.setTimeout(function () {
		body.removeChild(flameIDNode);
	}, 2000);
})();
"""
