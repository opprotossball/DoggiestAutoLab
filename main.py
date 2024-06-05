from pynput.mouse import Button, Controller 
from pynput.keyboard import Listener, KeyCode 
from AutoLab import AutoLab
import json

if __name__ == '__main__':
	start_stop_key = KeyCode(char='r') 
	stop_key = KeyCode(char='t') 

	settings_path = 'settings.json'
	with open(settings_path) as f:
		settings = json.load(f)
	
	auto_lab = AutoLab(settings) 
	auto_lab.start() 
