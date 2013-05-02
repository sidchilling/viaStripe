from brubeck.request_handling import WebMessageHandler, render

import json

class JSONRendering(WebMessageHandler):
    def render(self):
	self.headers['Content-Type'] = 'application/json'
	self.headers['P3P'] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
	body = json.dumps(self.body)
	response = render(body, self.status_code, self.status_msg,
		self.headers)
	return response
