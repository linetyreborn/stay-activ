from flask import Flask, render_template, redirect, url_for, request
import pyautogui
import time
import logging
import win32api
import os
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

def move_mouse():
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x, current_y - 1, duration=0.1)
    pyautogui.moveTo(current_x, current_y + 1, duration=0.1)

def press_shift():
    pyautogui.keyDown('shift')
    pyautogui.keyUp('shift')

def is_locked():
    return bool(win32api.LockWorkStation())

last_position = pyautogui.position()
is_paused = False
last_active_time = time.time()

logging.info('Script is active.')

@app.route('/')
def index():
    return render_template('index.html', is_paused=is_paused)

@app.route('/toggle', methods=['POST'])
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    logging.info('Script is %s.', 'paused' if is_paused else 'active')
    return redirect(url_for('index'))

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    try:
        shutdown_server()
        os.kill(os.getpid(), signal.SIGINT)
        return 'Server shutting down...'
    except RuntimeError:
        os.kill(os.getpid(), signal.SIGINT)
        return 'Unable to shutdown server', 500

if __name__ == '__main__':
    app.run()
    while True:
        if not is_paused:
            current_position = pyautogui.position()
            if current_position == last_position:
                inactive_time = time.time() - last_active_time
                if inactive_time >= 15:
                    move_mouse()
                    press_shift()  # Pressing Shift key to keep the PC awake
                else:
                    logging.info('Inactive for %.1f seconds.', inactive_time)
            else:
                last_position = current_position
                last_active_time = time.time()
        time.sleep(1)