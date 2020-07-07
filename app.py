from flask import Flask, render_template, Response
from Camera import VideoCamera
import colorpicker

app = Flask(__name__)
'''
colorobj1 = colorpicker.color()
colorobj2 = colorpicker.color()
'''


@app.route('/')
def index():
	# rendering webpage
	return render_template('index.html', inpobj1 = True, inpobj2 = False, outshow = False)

@app.route('/click')
def click():
	# rendering webpage
	click.colorobj1 = detect.color
	return render_template('index.html', inpobj1 = False, inpobj2 = True, outshow = False)

@app.route('/showoutput')
def showoutput():
	# rendering webpage
	showoutput.colorobj2 = detect.color
	print(click.colorobj1)
	print(showoutput.colorobj2)
	return render_template('index.html', object1 = click.colorobj1, object2 = showoutput.colorobj2, inpobj1 = False, inpobj2 = False, outshow = True)
	

def detect(Camera):
	while True:
		frame = Camera.get_roi()
		detect.color = colorpicker.color()

		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')   

def gen(Camera):
	while True:
		frame = Camera.get_frame(click.colorobj1, showoutput.colorobj2)
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
	return Response(gen(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/color_detect')
def color_detect():
	return Response(detect(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')

			
