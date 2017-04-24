from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import numpy as np
from tkinter import *
import tensorflow as tf

root = Tk()

input_display_title = LabelFrame(root, text="Network Inputs", bg="#191919", fg="white")
genome_stats_title = LabelFrame(root, text="Genome Stats", bg="#191919", fg="white")
log_display_title = LabelFrame(root, text="Logs", bg="#191919", fg="white")
game_stats_title = LabelFrame(root, text="Game Stats", bg="#191919", fg="white")

input_display_title.pack()
genome_stats_title.pack()
log_display_title.pack()
game_stats_title.pack()

input_display = Text(input_display_title, width=60, height=10, bg="#191919", fg="white", highlightbackground="#191919")
input_display.grid()
input_display.pack()

genome_stats = Text(genome_stats_title, width=60, height=6, bg="#191919", fg="white", highlightbackground="#191919")
genome_stats.grid()
genome_stats.pack()

log_display = Text(log_display_title, state="normal", wrap="none", width=400,
                   height=18, bg="#191919", fg="#A6E22E", highlightbackground="#191919")
log_display.grid()
log_display.pack()

game_stats = Text(game_stats_title, width=60, height=10, bg="#191919", fg="white", highlightbackground="#191919")
game_stats.grid()
game_stats.pack()

log_lines = 0
w = 400
h = 800
x = root.winfo_screenwidth()
y = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)


def writeToInput(array):
    """Writes to input_display"""
    input_display.delete(1.0, 'end')
    input_display.insert('end', "\t\t" + str(array[0][0]) + "\t" + str(array[0][4]) + "\t" +
                         str(array[0][8]) + "\t" + str(array[0][12]) + "\n\n\n")
    input_display.insert('end', "\t\t" + str(array[0][1]) + "\t" + str(array[0][5]) + "\t" +
                         str(array[0][9]) + "\t" + str(array[0][13]) + "\n\n\n")
    input_display.insert('end', "\t\t" + str(array[0][2]) + "\t" + str(array[0][6]) + "\t" +
                         str(array[0][10]) + "\t" + str(array[0][14]) + "\n\n\n")
    input_display.insert('end', "\t\t" + str(array[0][3]) + "\t" + str(array[0][7]) + "\t" +
                         str(array[0][11]) + "\t" + str(array[0][15]))
    root.update()


def writeToGenome_1(msg):
    """Writes to genome_stats for activation"""
    genome_stats.delete(1.0, 'end')
    if msg == '[0]':
        genome_stats.insert('end', "Activation: UP\n")
    if msg == '[1]':
        genome_stats.insert('end', "Activation: DOWN\n")
    if msg == '[2]':
        genome_stats.insert('end', "Activation: LEFT\n")
    if msg == '[3]':
        genome_stats.insert('end', "Activation: RIGHT\n")
    genome_stats.insert('end', "Output: \n")
    genome_stats.tag_add("movehl", "1.11", "2.0")
    genome_stats.tag_config("movehl", foreground="#66D9EF")


def writeToGenome_2(msg):
    """Writes to genome_stats for output"""
    genome_stats.insert('end', msg+"\n")
    genome_stats.tag_add("outputhl", "2.8", "end")
    genome_stats.tag_config("outputhl", foreground="#66D9EF")
    root.update()


def writeToLog(msg):
    """Writes to log_display"""
    global log_lines
    log_lines += 1
    if log_lines == 18:
        log_display.delete(1.0, 2.0)
        log_lines -= 1
    log_display.insert('end', msg)
    log_display.insert('end', '\n')
    root.update()


def writeToGame(msg):
    """Writes to game_stats"""
    game_stats.delete(1.0, 'end')
    game_stats.insert('end', "Fitness: " + str(msg) + "\n")
    game_stats.tag_add("fitnesshl", "1.8", "end")
    game_stats.tag_config("fitnesshl", foreground="#F92672")


class Controller:
    def __init__(self):
        """Builds chromedriver"""
        #Note for Github users: The filepath to the chromedriver must be changed to run this code
        self.path_to_chromedriver = '/Users/devinkim/Desktop/chromedriver'
        self.browser = webdriver.Chrome(executable_path=self.path_to_chromedriver)
        self.url = 'https://gabrielecirulli.github.io/2048/'

    def loadPage(self):
        """Sets up window"""
        self.browser.get(self.url)
        #self.browser.set_window_position(0, 0)
        #self.browser.set_window_size(878, 800)
        time.sleep(2)
        element = self.browser.find_element_by_class_name('notice-close-button')
        element.click()
        self.browser.execute_script("document.body.style.zoom='75%'")

        # writeToLog("Starting Process")

        main = self.browser.find_element_by_xpath('/html/body')
        main.send_keys(Keys.COMMAND, Keys.SUBTRACT)
        main.send_keys(Keys.COMMAND, Keys.SUBTRACT)
        time.sleep(1)

    def main(self):
        """Runs main NN program"""
        main = self.browser.find_element_by_xpath('/html/body')
        bot_01 = Bot("Genome 01")
        bot_02 = Bot("Genome 02")
        bot_03 = Bot("Genome 03")
        bot_04 = Bot("Genome 04")
        bot_05 = Bot("Genome 05")
        bot_06 = Bot("Genome 06")
        bot_07 = Bot("Genome 07")
        bot_08 = Bot("Genome 08")
        bot_09 = Bot("Genome 09")
        bot_10 = Bot("Genome 10")
        generation = [bot_01, bot_02, bot_03, bot_04, bot_05, bot_06, bot_07, bot_08, bot_09, bot_10]
        for gen in range(50):
            writeToLog('Executing generation '+str(gen))
            for x in range(10):
                game_state = True
                for y in range(10):
                # while game_state == True:
                    bot_x = generation[x]
                    # Takes care of score addition bug
                    score = self.browser.find_element_by_class_name('score-container').text
                    if '+' in score:
                        score = score[:score.index('+') - 1]
                    writeToGame(score)

                    tiles = self.loadTiles()
                    move = bot_x.run_neural_network(tiles)
                    if move == [0]:
                        main.send_keys(Keys.ARROW_UP)
                    if move == [1]:
                        main.send_keys(Keys.ARROW_DOWN)
                    if move == [2]:
                        main.send_keys(Keys.ARROW_LEFT)
                    if move == [3]:
                        main.send_keys(Keys.ARROW_RIGHT)
                    time.sleep(0.1)

                    msg = self.browser.find_element_by_class_name('game-message')
                    if 'Game over!' in msg.text:
                        game_state = False
                writeToLog(bot_x.get_name() + ' completed. Fitness: ' + score)
                bot_x.crossover_model(bot_10)
                bot_x.mutate_model()
                # Set up for next bot run
                self.browser.execute_script("document.body.style.zoom='100%'")
                new_game = self.browser.find_element_by_class_name('restart-button')
                new_game.click()
                self.browser.execute_script("document.body.style.zoom='75%'")
                time.sleep(1)

        self.browser.close()

    def loadTiles(self):
        """Reads in tiles from browser"""
        start = time.time()
        tiles = self.browser.find_elements_by_class_name('tile')
        tilearray = [[0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0]]
        for tile in tiles:
            value = int(tile.text)
            string = tile.get_attribute('class')
            startpos = string.index('position')
            row = int(string[startpos + 9])
            col = int(string[startpos + 11])
            index = 4 * (row - 1) + (col - 1)

            if value > tilearray[0][index]:
                tilearray[0][index] = value#math.log(value, 2)*100
        writeToInput(tilearray)
        # tilestate = tf.Variable(tf.constant(tilearray, dtype=tf.float32))
        end = time.time()
        lag = float(end - start)
        # writeToLog("Loading tiles:" + str(lag))
        return tilearray


class Bot:
    def __init__(self, msg):
        """Sets up neural network"""
        self.name = str(msg)
        self.n_inputs = 16
        self.n_nodes_hl1 = 10
        self.n_nodes_hl2 = 10
        self.n_nodes_hl3 = 10
        self.n_classes = 4
        self.mutate_chance = 0.03

        self.hidden_layer_1 = {'weights': np.random.random((self.n_inputs, self.n_nodes_hl1)),
                               'biases': np.random.random(self.n_nodes_hl1)}
        self.hidden_layer_2 = {'weights': np.random.random((self.n_nodes_hl1, self.n_nodes_hl2)),
                               'biases': np.random.random(self.n_nodes_hl2)}
        self.hidden_layer_3 = {'weights': np.random.random((self.n_nodes_hl2, self.n_nodes_hl3)),
                               'biases': np.random.random(self.n_nodes_hl3)}
        self.output_layer = {'weights': np.random.random((self.n_nodes_hl3, self.n_classes)),
                               'biases': np.random.random(self.n_classes)}

        # self.hidden_1_layer = {'weights': tf.Variable(tf.random_normal([16, n_nodes_hl1])),
        #                        'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
        # self.hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
        #                        'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
        # self.hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
        #                        'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
        # self.output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
        #                      'biases': tf.Variable(tf.random_normal([n_classes]))}

        writeToLog(self.name + " initialized")

    def get_name(self):
        return self.name

    def crossover_model(self, other):
        for value_a, value_b in zip(self.hidden_layer_1['weights'], other.hidden_layer_1['weights']):
            print("Value a:", value_a, "Value b:", value_b)


    def mutate_model(self):
        """Mutate Genome"""

        #Mutate layer 1
        for value in self.hidden_layer_1['weights']:
            for i in value:
                if self.mutate_chance >= np.random.random():
                    i = np.random.random()
        for value in self.hidden_layer_1['biases']:
                if self.mutate_chance >= np.random.random():
                    value = np.random.random()

        #Mutate layer 2
        for value in self.hidden_layer_2['weights']:
            for i in value:
                if self.mutate_chance >= np.random.random():
                    i = np.random.random()
        for value in self.hidden_layer_2['biases']:
            if self.mutate_chance >= np.random.random():
                value = np.random.random()

        #Mutate layer 3
        for value in self.hidden_layer_3['weights']:
            for i in value:
                if self.mutate_chance >= np.random.random():
                    i = np.random.random()
        for value in self.hidden_layer_3['biases']:
            if self.mutate_chance >= np.random.random():
                value = np.random.random()

        #Mutate output layer
        for value in self.output_layer['weights']:
            for i in value:
                if self.mutate_chance >= np.random.random():
                    i = np.random.random()
        for value in self.output_layer['biases']:
            if self.mutate_chance >= np.random.random():
                value = np.random.random()

    def neural_network_model(self, data):
        """Performs neural network operations"""
        l1 = np.add(np.dot(data, self.hidden_layer_1['weights']), self.hidden_layer_1['biases'])
        l1 = np.maximum(l1, 0)

        l2 = np.add(np.dot(l1, self.hidden_layer_2['weights']), self.hidden_layer_2['biases'])
        l2 = np.maximum(l2, 0)

        l3 = np.add(np.dot(l2, self.hidden_layer_3['weights']), self.hidden_layer_3['biases'])
        l3 = np.maximum(l3, 0)

        output = np.dot(l3, self.output_layer['weights']) + self.output_layer['biases']
        output = np.maximum(output, 0)
        return output

        # l1 = tf.add(tf.matmul(data, self.hidden_1_layer['weights']), self.hidden_1_layer['biases'])
        # l1 = tf.nn.relu(l1)
        #
        # l2 = tf.add(tf.matmul(l1, self.hidden_2_layer['weights']), self.hidden_2_layer['biases'])
        # l2 = tf.nn.relu(l2)
        #
        # l3 = tf.add(tf.matmul(l2, self.hidden_3_layer['weights']), self.hidden_3_layer['biases'])
        # l3 = tf.nn.relu(l3)
        #
        # output = tf.matmul(l3, self.output_layer['weights']) + self.output_layer['biases']
        # return output

    def run_neural_network(self, x):
        """Returns output from neural network fed inputs"""
        start = time.time()
        keypress = self.neural_network_model(x)


        end = time.time()
        lag = float(end - start)
        writeToGenome_1(str(np.argmax(keypress, 1)))
        writeToGenome_2("UP: "+str(keypress[0][0]))
        writeToGenome_2("DOWN: "+str(keypress[0][1]))
        writeToGenome_2("LEFT: "+str(keypress[0][2]))
        writeToGenome_2("RIGHT: "+str(keypress[0][3]))
        # writeToLog("Returning data: " + str(lag))
        return np.argmax(keypress, 1)


        # with tf.Session() as sess:
        #     start = time.time()
        #     sess.run(tf.initialize_all_variables())
        #     end = time.time()
        #     lag = float(end - start)
        #     writeToLog("Returning data: " + str(lag))
        #     writeToGenome_1(str(sess.run(tf.argmax(keypress, 1))))
        #     writeToGenome_2(str(sess.run(keypress)))
        #     return sess.run(tf.argmax(keypress, 1))


program = Controller()
program.loadPage()
program.main()
