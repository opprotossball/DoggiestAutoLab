import time
import threading
from pynput.mouse import Button, Controller
import json
from utils import *

class AutoLab(threading.Thread):
    
    def __init__(self, settings):
        super(AutoLab, self).__init__()
        self.button = Button.left
        self.running = False
        self.settings = settings
        self.program_running = True
        self.mouse = Controller()
        self.next_to_optimize = None
        self.params = {p: (settings[p][1] - settings[p][0]) / 2 for p in settings['optimization_order']}
        self.simulation = 0
        self.averages = []
        self.bests = []
        self.worsts = []

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def optimize(self):
        param = self.next_to_optimize
        l = self.settings[param][0]
        r = self.settings[param][1]
        lmid = l + ((r - l) / 3)
        rmid = r - ((r - l) / 3)

        self.params[param] = lmid
        bl, wl, al = self.simulate()
        lval = bl

        self.params[param] = rmid
        br, wr, ar = self.simulate()
        rval = br

        # selects value with beter best score
        if lval < rval:
            self.settings[param][1] = rmid
            self.bests.append(bl)
            self.worsts.append(wl)
            self.averages.append(al)
        else:
            self.bests.append(br)
            self.worsts.append(wr)
            self.averages.append(ar)    
            if lval > rval:
                self.settings[param][0] = lmid
            else:
                self.settings[param][0] = lmid
                self.settings[param][1] = rmid
        self.params[param] = (self.settings[param][1] - self.settings[param][0]) / 2
        print(f'Optimized {param}. New value: {self.params[param]}')

    def simulate(self):
        print(f'Starting simulation {self.simulation}')
        self.write_parameters()
        self.mouse.click(self.button)
        time.sleep(self.settings['execution_time'])
        best_list, worst_list, avg_list = self.log_result(f'log{self.simulation}.txt')
        self.simulation += 1
        return best_list[-1], worst_list[-1], avg_list[-1]

    def log_result(self, fname):
        best_list, worst_list, avg_list = parse(self.settings['result_path'])
        with open(self.settings['result_path'], 'r') as f:
            result = f.read()
        with open(self.settings['log_path'] + fname, 'w') as f:
            json.dump(self.params, f, indent=4)
            f.write('\n\n\n')
            f.write(result)
        open(self.settings['result_path'], 'w').close()
        return best_list, worst_list, avg_list

    def write_parameters(self):
        with open(self.settings['config_path'], 'r') as f:
            lines = f.readlines()
        updated_lines = []
        for line in lines:
            key = line.split('=')[0]
            if key in self.params:
                if key == 'osobniki' or key == 'pokolenia':
                    updated_lines.append(f'{key}={int(self.params[key])}\n')
                else:
                    updated_lines.append(f'{key}={self.params[key]:.6f}\n')
            else:
                updated_lines.append(line)
        with open(self.settings['config_path'], 'w') as f:
            f.writelines(updated_lines)

    def run(self):
        print('Autolab will start in 7 seconds. Place cursor on optimalization button.')
        time.sleep(7)
        print('Auto Lab started')
        while self.simulation < self.settings['iterations']:
            self.next_to_optimize = self.settings['optimization_order'][int((self.simulation / 2) % len(self.settings['optimization_order']))] 
            self.optimize()
        print('Optimizaion ended. Best parameters:')
        print(json.dumps(self.params, indent=4))
        plot(self.bests, self.worsts, self.averages, x_label='Numer symulacji')
