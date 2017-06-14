# Wing Commander Prophecy controls
#
# implements a nice deadzone
#
# Assumes vJoy is joystick 0, hard joystick is joystick 1
#

if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	rotationDeadzone = 0.4
	joystickDeadzone = 0.1
	sliderSign = -1
	rotationSign = -1
	maxButtons = 16
	hardScale = 16384.0
	povRecognize = 6467
	virtual = vJoy[0]
	virtual.setAnalogPov(0, povRecognize)
	virtual.x = 0
	virtual.y = 0
	hard = None	
else:
	if hard is None:
		found_vJoy = False
		hardIndex = -1
		
		for i in range(16):
			try:
				if joystick[i].pov[0] == povRecognize:
					found_vJoy = True
				else:
					hardIndex = i
				if hardIndex >= 0 and found_vJoy:
					hard = joystick[hardIndex]
					hard.setRange(-int(hardScale),int(hardScale))
					break
			except:
				pass
				
		if hard is None:
			virtual.setAnalogPov(0, povRecognize)
			virtual.x = 0
			virtual.y = 0
		else:
			virtual.setAnalogPov(0, -1)

				
def scale(x):
	return int(x*virtual.axisMax)

def processDeadzone(x, zone):
	if abs(x) <= zone:
		return 0.
	else:
		sign = 1 if x > 0 else -1
		return sign * (abs(x)-zone) / (1.-zone)

if hard is not None:
	diagnostics.watch(hard.x)
	virtual.x = scale(processDeadzone( hard.x/hardScale, joystickDeadzone) )
	virtual.y = scale(processDeadzone( hard.y/hardScale, joystickDeadzone) )
	virtual.slider = scale(hard.sliders[0]/hardScale)
	virtual.rz = scale(processDeadzone(hard.zRotation / hardScale, rotationDeadzone)*rotationSign)
	
	for i in range(maxButtons):
		if i == 1:
			keyboard.setKey(Key.Return, hard.getPressed(i))
		elif i == 2:
			keyboard.setKey(Key.T, hard.getPressed(i))
		elif i == 3:
			keyboard.setKey(Key.R, hard.getPressed(i))
		elif i == 10:
			keyboard.setKey(Key.P, hard.getDown(i))
		elif i == 11:
			keyboard.setKey(Key.S, hard.getDown(i))
		elif i == 8:
			keyboard.setKey(Key.Grave, hard.getPressed(i))
		elif i == 9:
			keyboard.setKey(Key.Y, hard.getPressed(i))
		elif i == 4:
			keyboard.setKey(Key.M, hard.getPressed(i))
		elif i == 5:
			keyboard.setKey(Key.G, hard.getPressed(i))
		elif i == 7:
			keyboard.setKey(Key.E, hard.getPressed(i))
		else:
			virtual.setButton(i, hard.getDown(i))
	
	vJoy[0].setAnalogPov(0,hard.pov[0])
