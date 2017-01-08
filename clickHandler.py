import socket, traceback, win32api, win32con, time, os, turtle, re 
from win32api import GetSystemMetrics

host = '192.168.137.1'
port = 5959

horz = float(1366)
vert = float(768)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

print("Success binding")


############################################################
#						Turtle stuff					   #
############################################################
      # Create our favorite turtle

def rDevice():
	print("Reading")
	message, address = s.recvfrom(8192)
	messageString = message.decode("utf-8")
	return messageString

#gyro 1 y rotation, gyro3 z rotation
def read():
	message, address = s.recvfrom(8192)
	messageString = message.decode("utf-8")
	rotateList = re.findall(r"([\d|\-|\.|E]+)", messageString)
	return rotateList


# The next four functions are our "event handlers".
counter = [0]
#Used for calibration
xCList = []
yCList = []
zCList = []
def h1():
	readOut = read()
	xCList.append(float(readOut[0]))
	yCList.append(float(readOut[1]))
	zCList.append(float(readOut[2]))
	print(xCList)
	print(yCList)
	print(zCList)
	counter[0] += 1
	if (counter[0] == 4):
		counter[0]=0
		move()

def click(x,y):
    win32api.SetCursorPos((x,y))

def move():

	top = ((yCList[0]+yCList[2])/2)
	bottom = ((yCList[1]+yCList[3])/2)

	left = ((xCList[0]+xCList[1])/2)
	right = ((xCList[2]+xCList[3])/2)

	x_d = abs(right-left)
	y_D = abs(top-bottom)

	while 1:
		currentPos = read()
		for i in range(len(currentPos)):
			currentPos[i]=float(currentPos[i])

		print(currentPos)
		d_x = min(abs(currentPos[0]-left), 2-abs(currentPos[0]-left))
		d_y = min(abs(currentPos[1]-top), 2-abs(currentPos[1]-top))

		# if (xDistance > 1):
		# 	xDistance = 1 - xDistance % 1
		# if (yDistance > 1):
		# 	yDistance = 1 - yDistance % 1
		# if (posxDistance > 1):
		# 	posxDistance = 1 - posxDistance % 1
		# if (posyDistance > 1):
		# 	posyDistance = 1 - posyDistance %

		x = int(d_x/x_d*horz)

		y = int(d_y/y_D*vert)

		#print("X: " + str(x) + " Y: " + str(y))

		if currentPos[3]:
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

		elif currentPos[4]:
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
		else:
			win32api.SetCursorPos((x,y))
while 1:
	recentRead = read()
	for i in range(len(recentRead)):
		recentRead[i]=float(recentRead[i])
	print(recentRead)
	if (recentRead[4]):
		h1()
		time.sleep(1)