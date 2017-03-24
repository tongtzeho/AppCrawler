var system = require('system');
var url = system.args[1];
var page = require('webpage').create();
page.open(url);
page.onLoadFinished = phantom.exit;
page.onResourceReceived = function(j) {
	for (var i = 0; i < j.headers.length; i++) {
		if (j.headers[i].name == 'Location') {
			console.log(j.headers[i].value);
		}
	}
	f.close();
};