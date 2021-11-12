import runescape_text as runescape
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import tempfile
import os

PORT = os.environ["PORT"] if "PORT" in os.environ else 8777

ALLOWED_MODIFIERS = [
	"yellow",
	"white",
	"cyan",
	"red",
	"green",
	"purple",
	"flash1",
	"flash2",
	"flash3",
	"glow1",
	"glow2",
	"glow3",
	"none",
	"scroll",
	"slide",
	"wave",
	"wave2",
	"shake"
]

class RSHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse(self.path)
		if(parsed.path == "/"):
			self.send_response(200)
			self.end_headers()
			return
		if(parsed.path == "/convert"):
			query_components = parse_qs(parsed.query, keep_blank_values=True)
			if("text" not in query_components or query_components["text"]==""):
				self.send_response(401)
				self.end_headers()
				return
			modifiers = set(list(query_components.keys()))
			modifiers = list(filter(lambda x: x.lower() in ALLOWED_MODIFIERS, modifiers))

			fullstring = "{}{}{}".format(":".join(modifiers), ":" if len(modifiers)>0 else "", query_components["text"][0])
			img = runescape.parse_string(fullstring)

			fileobj = None
			if(len(img)==1):
				fileobj = tempfile.NamedTemporaryFile(suffix=".png",prefix="runescape-")
				filename = fileobj.name
				runescape.single_frame_save(img[0], file=fileobj.file)
				fileobj.file.flush()
				self.send_header("Content-Type", "image/png")
			else:
				fileobj = tempfile.NamedTemporaryFile(suffix=".gif",prefix="runescape-")
				filename = fileobj.name
				runescape.multi_frame_save(img, file=fileobj.file)
				fileobj.file.flush()
				self.send_header("Content-Type", "image/gif")
			fileobj.file.seek(0)

			self.send_response(200)
			self.end_headers()
			self.wfile.write(fileobj.read())
			return

class Server(socketserver.TCPServer):
	allow_reuse_address = True

with Server(("", PORT), RSHandler) as httpd:
	print("serving at port", PORT)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		# Clean-up server (close socket, etc.)
		print("CLOSING SERVER")
		httpd.server_close()