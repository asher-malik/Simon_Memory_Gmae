import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

window = ttk.Window()
window.geometry('620x620')
window.resizable(False, False)


global computer_turn, player_turn
computer_turn = False
player_turn = False

VERY_LIGHT_GREEN = '#4edc92'
VERY_LIGHT_ORANGE = "#ffe18d"
VERY_LIGHT_RED = "#ffb9b6"
VERY_LIGHT_GREY = "#d2d8e0"

style = ttk.Style()
style.configure('ButtonFrame.TFrame', background='black')
style.configure('Custom.TButton', font=('Open Sans', 16, 'bold'))
style.configure('Custom.TLabel', font=('Open Sans', 16, 'bold'))

style.configure('First.TButton', **style.configure('success.TButton'))
style.map('First.TButton', background=[('pressed', VERY_LIGHT_GREEN)])

style.configure('Second.TButton', **style.configure('warning.TButton'))
style.map('Second.TButton', background=[('pressed', VERY_LIGHT_ORANGE)])

style.configure('Third.TButton', **style.configure('danger.TButton'))
style.map('Third.TButton', background=[('pressed', VERY_LIGHT_RED)])

style.configure('Forth.TButton', **style.configure('secondary.TButton'))
style.map('Forth.TButton', background=[('pressed', VERY_LIGHT_GREY)])


class Game:
    def __init__(self, topframe, buttonframe, bottomframe):
        self.topframe = topframe
        self.buttonframe = buttonframe
        self.bottomframe = bottomframe

        self.extra_pick = 0
        self.topframe.game_button.configure(command=self.pressed_game_button)

        self.buttonframe.first_button.configure(command=lambda: self.button_click(0))
        self.buttonframe.second_button.configure(command=lambda: self.button_click(1))
        self.buttonframe.third_button.configure(command=lambda: self.button_click(2))
        self.buttonframe.forth_button.configure(command=lambda: self.button_click(3))

        self.answer = []
        self.guess = []

    def pressed_game_button(self):
        global computer_turn
        if self.topframe.game_button.cget('text') != 'Playing!' or self.topframe.game_button.cget('text') != 'correct' or self.topframe.game_button.cget('text') != 'Wrong!':
            self.topframe.game_button.configure(text='Playing!')
            computer_turn = True

            self.pick_buttons()

    def button_click(self, num):
        global player_turn, computer_turn
        if player_turn:
            self.guess.append(num)
            print(self.guess)
            if len(self.guess) == len(self.answer):
                player_turn = False
                if self.guess == self.answer:
                    self.topframe.game_button.configure(text='correct')
                    self.topframe.score += 10
                    self.topframe.score_label.configure(text=f'Score: {self.topframe.score}')
                    window.update_idletasks()
                    window.after(1000)
                    self.topframe.game_button.configure(text='Playing!')
                    computer_turn = True
                    self.pick_buttons()
                else:
                    self.topframe.score = 0
                    self.topframe.game_button.configure(text='Wrong!')
                    window.update_idletasks()
                    self.topframe.score_label.configure(text=f'Score: {self.topframe.score}')
                    window.after(1000)
                    self.topframe.game_button.configure(text='New Game')
                    self.guess = []
                    self.answer = []
                    self.extra_pick = 0

    def number_pick(self, index, delay):
        if computer_turn:
            if index == 0:
                style.configure('First.TButton', background=VERY_LIGHT_GREEN)
                window.update_idletasks()
                window.after(delay)
                self.answer.append(index)
                style.configure('First.TButton', **style.configure('success.TButton'))
                window.update_idletasks()
            elif index == 1:
                style.configure('Second.TButton', background=VERY_LIGHT_ORANGE)
                window.update_idletasks()
                window.after(delay)
                self.answer.append(index)
                style.configure('Second.TButton', **style.configure('warning.TButton'))
                window.update_idletasks()
            elif index == 2:
                style.configure('Third.TButton', background=VERY_LIGHT_RED)
                window.update_idletasks()
                window.after(delay)
                self.answer.append(index)
                style.configure('Third.TButton', **style.configure('danger.TButton'))
                window.update_idletasks()
            elif index == 3:
                style.configure('Forth.TButton', background=VERY_LIGHT_GREY)
                window.update_idletasks()
                window.after(delay)
                self.answer.append(index)
                style.configure('Forth.TButton', **style.configure('secondary.TButton'))
                window.update_idletasks()

    def pick_buttons(self):
        global player_turn, computer_turn
        if self.bottomframe.difficulty_var.get() == 'easy':
            for _ in range(1+self.extra_pick):
                i = random.randint(0, 3)
                self.number_pick(i, 1000)
                print(self.answer)
            player_turn = True
            computer_turn = False
            self.extra_pick += 1
        elif self.bottomframe.difficulty_var.get() == 'medium':
            for _ in range(1+self.extra_pick):
                i = random.randint(0, 3)
                self.number_pick(i, 500)
            player_turn = True
            computer_turn = False
            self.extra_pick += 1
        elif self.bottomframe.difficulty_var.get() == 'hard':
            for _ in range(1+self.extra_pick):
                i = random.randint(0, 3)
                self.number_pick(i, 200)
            player_turn = True
            computer_turn = False
            self.extra_pick += 1


class ButtonGame(ttk.Frame):
    def __init__(self, parent):
        super(ButtonGame, self).__init__(master=parent, style='ButtonFrame.TFrame')
        self.columnconfigure((0, 1), uniform='a', weight=1)
        self.rowconfigure((0, 1), uniform='b', weight=1)

        self.first_button = ttk.Button(master=self, text='', takefocus=False, style='First.TButton')
        self.first_button.grid(row=0, column=0, sticky='nesw', padx=15, pady=15)

        self.second_button = ttk.Button(master=self, text='', takefocus=False, style='Second.TButton')
        self.second_button.grid(row=0, column=1, sticky='nesw', padx=15, pady=15)

        self.third_button = ttk.Button(master=self, text='', takefocus=False, style='Third.TButton')
        self.third_button.grid(row=1, column=0, sticky='nesw', padx=15, pady=15)

        self.forth_button = ttk.Button(master=self, text='', takefocus=False, style='Forth.TButton')
        self.forth_button.grid(row=1, column=1, sticky='nesw', padx=15, pady=15)

        self.pack(expand=True, fill=BOTH, padx=30, pady=20)


class TopFrame(ttk.Frame):
    def __init__(self, parent):
        super(TopFrame, self).__init__(master=parent)

        self.score = 0

        self.columnconfigure((0, 1), uniform='a', weight=1)

        self.game_button = ttk.Button(self, bootstyle='dark', text='New Game', takefocus=False, style='Custom.TButton')
        self.game_button.configure(default='normal')
        self.game_button.grid(row=0, column=0, padx=60, pady=30)

        self.score_label = ttk.Label(self, bootstyle='dark', text=f'Score: {self.score}', style='Custom.TLabel')
        self.score_label.grid(row=0, column=1, pady=30, padx=(0, 70))

        self.pack(expand=False, fill=BOTH)

class BottomFrame(ttk.Frame):
    def __init__(self, parent):
        super(BottomFrame, self).__init__(master=parent)
        self.difficulty_var = ttk.StringVar(value='medium')

        self.columnconfigure((0, 1, 2, 3), uniform='c', weight=1)

        self.difficulty_label = ttk.Label(bootstyle='dark', master=self, text='Difficulty:')

        self.easy = ttk.Radiobutton(bootstyle='dark', text='easy', variable=self.difficulty_var, value='easy', master=self)
        self.medium = ttk.Radiobutton(bootstyle='dark', text='medium', variable=self.difficulty_var, value='medium', master=self)
        self.hard = ttk.Radiobutton(bootstyle='dark', text='hard', variable=self.difficulty_var, value='hard', master=self)

        self.difficulty_label.grid(row=0, column=0)
        self.easy.grid(row=0, column=1)
        self.medium.grid(row=0, column=2)
        self.hard.grid(row=0, column=3)

        self.pack(pady=10)



top_frame = TopFrame(window)
button_frame = ButtonGame(window)
bottom_frame = BottomFrame(window)

my_game = Game(topframe=top_frame, buttonframe=button_frame, bottomframe=bottom_frame)

window.mainloop()
