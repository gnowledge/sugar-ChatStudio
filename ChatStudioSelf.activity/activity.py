# Copyright 2007-2008 One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import logging
import json
import os
from gettext import gettext as _
import csv
from datetime import datetime
import time
from sugar.graphics import style
from sugar.graphics.alert import NotifyAlert
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.alert import Alert
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity import activity
from sugar.presence import presenceservice
from sugar.activity.widgets import StopButton, ActivityToolbarButton
from random import randint, choice
from chat.box import ChatBox
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

logger = logging.getLogger('ChatStudioSelf-activity')
steps = 0
accuracy = 0
no_of_mistake = 0
global_first_num = 0
global_second_num = 0
redirect_opt = 0
list_of_comp_ans = []
list_of_user_ans = []
gameComplete = False
addition_mode = False
subtraction_mode = False
scoretime = time.time()


class VisualScore(ToolButton):
    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'scorestats', **kwargs)
        self.props.tooltip = _('Score Stats')
        self.connect('clicked', self.draw_score_chart)

    def draw_score_chart(self, button):
	winScore = gtk.Window()
	winScore.connect("destroy", lambda x: gtk.main_quit())
	winScore.set_default_size(800, 490)
	winScore.set_position(gtk.WIN_POS_CENTER)
	winScore.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
	winScore.set_title("Score Statistics")
	score_chart_fig = Figure(figsize=(5, 4), dpi=100)
	plot_score_dgm = score_chart_fig.add_subplot(111)
	accuracy_list = []
	dates_list = []
	with open("scoreStatistics.csv", "r") as csvfile:
	 csv_content = csv.DictReader(csvfile, delimiter=',')
	 list_of_dict = []
	 for row in csv_content:
	  list_of_dict.append(row)
	for each_dict in list_of_dict[-10:]:
	 accuracy_list.append(int(each_dict["score"]))
	 date_det = each_dict["date_detail"].replace(" ", "")
	 dates_list.append(date_det)
	y_pos = np.arange(len(dates_list))
	error = np.random.rand(len(dates_list))
	plot_score_dgm.barh(y_pos, accuracy_list, xerr=error, color = 'b', align='center')
	plot_score_dgm.set_yticks(y_pos)
	plot_score_dgm.set_yticklabels(dates_list)
	score_canvas = FigureCanvas(score_chart_fig)  # a gtk.DrawingArea
	winScore.add(score_canvas)
	winScore.show_all()
	gtk.main()


class VisualTime(ToolButton):
    def __init__(self, activity, **kwargs):

        ToolButton.__init__(self, 'timestats', **kwargs)
        self.props.tooltip = _('Time Stats')
        self.connect('clicked', self.draw_time_chart)

    def draw_time_chart(self, button):
	winTime = gtk.Window()
	winTime.connect("destroy", lambda x: gtk.main_quit())
	winTime.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
	winTime.set_default_size(800, 490)
	winTime.set_position(gtk.WIN_POS_CENTER)
	winTime.set_title("Time Statistics")
	time_chart_fig = Figure(figsize=(5, 4), dpi=100)
	plot_time_dgm = time_chart_fig.add_subplot(111)
	game_time_list = []
	dates_list = []
	with open("scoreStatistics.csv", "rb") as csvfile:
	 csv_content = csv.DictReader(csvfile, delimiter=',')
	 list_of_dict = []
	 for row in csv_content:
	  list_of_dict.append(row)
	for each_dict in list_of_dict[-10:]:
	 game_time_list.append(float(each_dict["time_taken"]))
	 date_det = each_dict["date_detail"].replace(" ", "")
	 dates_list.append(date_det)
	y_pos = np.arange(len(dates_list))
	error = np.random.rand(len(dates_list))
	plot_time_dgm.barh(y_pos, game_time_list, xerr=error, color = 'g', align='center')
	plot_time_dgm.set_yticks(y_pos)
	plot_time_dgm.set_yticklabels(dates_list)
	time_canvas = FigureCanvas(time_chart_fig)  # a gtk.DrawingArea
	winTime.add(time_canvas)
	winTime.show_all()
	gtk.main()


class scoreWindow:
    def __init__(self):
        self.scorewindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.scorewindow.set_resizable(False)
	self.scorewindow.set_title("Score card")
	self.scorewindow.set_position(gtk.WIN_POS_CENTER)
	self.vbox_as_parent = gtk.VBox()
	self.hbox_for_text_content = gtk.HBox()
	self.hbox_for_btns = gtk.HBox()
	self.text_content = gtk.TextView()
	line = ''  # Declare an empty string
	self.gameover_msg = gtk.Label("Game Over\n")
        self.lalign = gtk.Alignment(0, 0, 0, 0)
        self.top_label = gtk.Label("Rank\tAccuracy\t\tStart\t\tAdd\t\tMistakes\t\t\tSteps\t\tTime\t\tMode")
	self.text_content.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
	self.text_content.set_editable(0)
	self.text_content.set_cursor_visible(0)
	self.text_content.set_left_margin(30)
        textbuffer = self.text_content.get_buffer()
        self.text_content.show()
	global gameComplete
	if (redirect_opt == 0):
	 self.recent_ten_scores(textbuffer, line)
	elif (redirect_opt == 1):
	 if (gameComplete):
	  self.last_game_score_stats(textbuffer, line)
	 else:
	  line = 'Incomplete Game'
          textbuffer.set_text(line)
	 global redirect_opt
	 redirect_opt = 0
	elif (redirect_opt == 2):
	 if (gameComplete):
	  self.last_game_ans_list(textbuffer, line)
	  self.top_label = gtk.Label("Compare Answers")
	
	 else:
	  line = 'Incomplete Game'
          textbuffer.set_text(line)
	 global redirect_opt
	 redirect_opt = 0

	self.hbox_for_text_content.pack_start(self.text_content, fill=False)
	self.last_game_compare_ans_btn = gtk.Button("Check Last Game answer")
	self.last_game_score_btn = gtk.Button("Last Game Score")
	self.last_game_compare_ans_btn.connect("clicked", self.last_game_compare_ans_card, self.scorewindow)
	self.last_game_score_btn.connect("clicked", self.last_game_score_card, self.scorewindow)
	self.hbox_for_btns.pack_start(self.last_game_compare_ans_btn, fill=False)
	self.hbox_for_btns.pack_start(self.last_game_score_btn, fill=False)
        self.lalign.add(self.top_label)
	self.vbox_as_parent.pack_start(self.gameover_msg, False, False, 0)
        self.vbox_as_parent.pack_start(self.lalign, False, False, 0)
	self.vbox_as_parent.pack_start(self.hbox_for_text_content, fill=False)
	self.vbox_as_parent.pack_start(self.hbox_for_btns, fill=False)
	color = gtk.gdk.color_parse('#FF8300')
        self.scorewindow.modify_bg(gtk.STATE_NORMAL, color)
	self.scorewindow.add(self.vbox_as_parent)
	self.scorewindow.show_all()

    def recent_ten_scores(self,textbuffer,line):
	 if not (os.stat("sorted_score_card.txt").st_size == 0):  # when file not empty
          with open("sorted_score_card.txt", "r") as infile:
	   for i in range(0, 10):  # displays only top 10 lines of the file
	     line += '\n' + str(i + 1) + '\t' + infile.readline()
          textbuffer.set_text(line)

    def last_game_ans_list(self, textbuffer, line):
	 global list_of_user_ans
	 global list_of_comp_ans
	 a = len(list_of_comp_ans)
	 b = len(list_of_user_ans)
	 i, j = 0, 0
	 line += 'Your Answer \t <------->\t Correct Answer\n'
	 while i < a and j < b:
	  line += str(list_of_user_ans[i])+\
	  ' \t\t\t <------->\t\t' + str(list_of_comp_ans[j]) + '\n'
	  i += 1
	  j += 1
         textbuffer.set_text(line)

    def last_game_score_stats(self, textbuffer, line):
	  line += '   ' + str(accuracy) + '\t\t\t  ' +\
	   str(global_first_num) + '\t\t\t  ' + \
	   str(global_second_num) + '\t\t    ' +\
	   str(no_of_mistake) + '\t\t\t\t  ' + \
	   str(steps) + '\t\t\t' + '%.1f' % scoretime + '\t\t\t'
	  if addition_mode:
	   line += 'Addition\n'
	  elif subtraction_mode:
	   line += 'Subtraction\n'
          textbuffer.set_text(line)

    def last_game_compare_ans_card(self, button, window):
	window.destroy()
	global redirect_opt
	redirect_opt = 2
	scoreWindow()

    def last_game_score_card(self, button, window):
	window.destroy()
	global redirect_opt
	redirect_opt = 1
	scoreWindow()


class ScoreButton(ToolButton):
    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'score_card', **kwargs)
        self.props.tooltip = _('Score Card')
        self.connect('clicked', self.__show_score_win, activity)

    def __show_score_win(self, button, activity):
	scoreWindow()


class GameToolbar(Alert):
    def __init__(self, **kwargs):
	Alert.__init__(self, **kwargs)
        self.add_button(1, _('New\nGame'), icon=None)
        self.add_button(2, _(' Change \n Numbers '), icon=None)
        self.add_button(3, _('Easy'), icon=None)
        self.add_button(4, _('Medium'), icon=None)
        self.add_button(5, _('Hard'), icon=None)

# pylint: disable-msg=W0223
class ChatStudioSelf(activity.Activity):

    def __init__(self, handle):
        self.chatbox = ChatBox()
        super(ChatStudioSelf, self).__init__(handle)
        self.entry = None
        root = self.make_root()
        self.set_canvas(root)
        root.show_all()
        self.entry.grab_focus()
	global accuracy
	accuracy = 0
	self.local_first_num = 0
	self.local_second_num = 0
	self.limit_num = 50
	self.calculated_sum = 0
	self.calculated_diff = 0
	self.second_attempt_flag = False
	self.metadata_dict = {}
	self.mode_of_game = ""
	self.game_metadata = False
	self.difficulty_level = "Easy"
	self.first_come_check = 0
	self.create_toolbar()
        pservice = presenceservice.get_instance()
        self.owner = pservice.get_owner()
        # Chat is room or one to one:
        self._chat_is_room = False

    def create_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.toolbar.insert(ActivityToolbarButton(self), -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	scoreButton = ScoreButton(self)
	toolbar_box.toolbar.insert(scoreButton, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	self._modes = ToolComboBox()
        self._modelist = ['Select Mode', '+ Add', '- Subtract']
       	for i, f in enumerate(self._modelist):
         self._modes.combo.append_item(i, f) 
       	self.modes_handle_id = self._modes.combo.connect("changed", self._change_modes_toolbar)
        toolbar_box.toolbar.insert(self._modes, -1)
        self._modes.combo.set_active(0)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	scorestats = VisualScore(self)
	toolbar_box.toolbar.insert(scorestats, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	timestats = VisualTime(self)
	toolbar_box.toolbar.insert(timestats, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)

	stopButton = StopButton(self)
	toolbar_box.toolbar.insert(stopButton, -1)
        toolbar_box.show_all()

    def _change_modes_toolbar(self, combo):
        response_id_of_modes_toolbar = combo.get_active()
	global global_first_num
	global global_second_num
	if (response_id_of_modes_toolbar == 1):
	 global_first_num = randint(5, 9)
	 global_second_num = randint(5, 9)
	 combo.set_sensitive(False)
	 self.local_first_num = global_first_num
	 self.local_second_num = global_second_num
	 self.calculated_sum = self.local_first_num + self.local_second_num
	 self.mode_of_game = "Addition"
	 global addition_mode
	 addition_mode = True
	 self.show_game_toolbar()

 	elif (response_id_of_modes_toolbar == 2):
	 global_first_num = randint(50, 55)
	 global_second_num = randint(5, 9)
	 combo.set_sensitive(False)
	 self.local_first_num = global_first_num
	 self.local_second_num = global_second_num
	 self.calculated_diff = self.local_first_num - self.local_second_num
	 self.mode_of_game = "Subtraction"
	 global subtraction_mode
	 subtraction_mode = True
	 self.show_game_toolbar()

    def _setup(self):
        self.entry.set_sensitive(True)
        self.entry.grab_focus()

    def _alert(self, title, text=None):
        alert = NotifyAlert(timeout=5)
        alert.props.title = title
        alert.props.msg = text
        self.add_alert(alert)
        alert.connect('response', self._alert_cancel_cb)
        alert.show()

    def _alert_cancel_cb(self, alert, response_id):
        self.remove_alert(alert)

    def game_tools(self, title, text=None):
        game_opts = GameToolbar()
        game_opts.props.title = title
        game_opts.props.msg = text
        self.add_alert(game_opts)
        game_opts.connect('response', self.new_game)
        game_opts.show()

    def new_game(self, game_opt_tools, response_id):
	global steps
 	global no_of_mistake
	global accuracy
	global list_of_comp_ans
	global list_of_user_ans
	global gameComplete
	steps = 0
 	accuracy = 0.0
	no_of_mistake = 0
	self.first_come_check = 0
	gameComplete = False
	self.second_attempt_flag = False
	self.entry.set_sensitive(True)
        self.entry.grab_focus()
	del list_of_comp_ans[:]
	del list_of_user_ans[:]
	global scoretime
    	scoretime = time.time()
        self.remove_game_toolbar(game_opt_tools)
	global global_first_num
	global global_second_num
	self.chatbox.rem()
	if (response_id == 1):  # Cancel--> New Game
	 self.difficulty_level = "Easy"
	 if addition_mode:
	  global_first_num = randint(5, 9)
	  global_second_num = randint(5, 9)
	  self.limit_num = 50
	 elif subtraction_mode:
	  global_first_num = randint(50, 59)
	  global_second_num = randint(5, 9)
	  self.limit_num = 50

	elif (response_id == 2):  # OK--> Change Numbers Dialog
	 self.difficulty_level = "Changed_Numbers"

	 messagedialog = gtk.MessageDialog(parent=None, flags=0,\
	  type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK,\
	 message_format="Enter Numbers")
	 action_area = messagedialog.get_content_area()
	 start_lbl = gtk.Label("Start")
	 input_first_num_txtbox = gtk.Entry()
         input_first_num_txtbox.set_size_request(int(gtk.gdk.screen_width() / 25), -1)
	 if addition_mode:
	  mode_lbl = gtk.Label("+ Add")
	 elif subtraction_mode:
	  mode_lbl = gtk.Label("- Subtract")
	 input_second_num_txtbox = gtk.Entry()
         input_second_num_txtbox.set_size_request(int(gtk.gdk.screen_width() / 25), -1)

	 action_area.pack_start(start_lbl)
	 action_area.pack_start(input_first_num_txtbox)
	 action_area.pack_start(mode_lbl)
	 action_area.pack_start(input_second_num_txtbox)
	 messagedialog.show_all()
	 changed_num_resp = messagedialog.run()

         if changed_num_resp == gtk.RESPONSE_OK:
	  try:
       	   global_first_num = int(input_first_num_txtbox.get_text())
	   global_second_num = int(input_second_num_txtbox.get_text())
	   if subtraction_mode:
	    if (global_second_num > global_first_num):
		# raise BadNum("Num2 canot be greater than Num1")
		raise Exception
	  except Exception:
	   if addition_mode:
	    global_first_num = randint(5, 9)
	    global_second_num = randint(5, 9)
	   elif subtraction_mode:
	    global_first_num = randint(50, 59)
	    global_second_num = randint(5, 9)

	 messagedialog.destroy()
	 self.limit_num = 50

	elif(response_id == 3):
	 self.difficulty_level = "Easy"
	 easylistStartNum = [50, 52, 54, 55, 56, 51]
	 l1 = [6, 9, 3, 2]
	 l2 = [5, 10, 2]
	 l3 = [7, 8]
	 if addition_mode:
	  global_first_num = randint(1, 9)
	  global_second_num = global_first_num
	 elif subtraction_mode:
	  global_first_num = choice(easylistStartNum)
	  if (global_first_num == 50):
	   global_second_num = choice(l2)
	  elif (global_first_num == 51):
	   global_second_num = 3
	  elif (global_first_num == 52):
	   global_second_num = 2
	  elif (global_first_num == 54):
	   global_second_num = choice(l1)
	  elif (global_first_num == 55):
	   global_second_num = 5
	  elif (global_first_num == 56):
	   global_second_num = choice(l3)
 	 self.limit_num = 50

	elif(response_id == 4):
	 self.difficulty_level = "Medium"
	 l11 = [51, 52, 53, 54, 56, 57, 58, 59]
	 if addition_mode:
	  global_first_num = randint(2, 9)
	  global_second_num = randint(2, 9)
	  if (global_first_num == global_second_num):
	   global_second_num = randint(2, 9)
	 elif subtraction_mode:
	  global_first_num = choice(l11)
	  global_second_num = randint(2, 9)
	 if (global_first_num == global_second_num):
	   global_second_num = randint(2, 9)
	 self.limit_num = 50
	 
	elif(response_id == 5):
	 self.difficulty_level = "Hard"
	 if addition_mode:
	  global_first_num = randint(5, 10)
	  global_second_num = randint(5, 10)
	 elif subtraction_mode:
	  global_first_num = randint(100, 105)
	  global_second_num = randint(5, 9)
	 self.limit_num = 100

	self.local_first_num = global_first_num
	self.local_second_num = global_second_num
	global list_of_comp_ans
	if addition_mode:
	 self.calculated_sum = self.local_first_num + self.local_second_num
	 list_of_comp_ans.append(self.calculated_sum)

	if subtraction_mode:
	 self.calculated_diff = self.local_first_num - self.local_second_num
	 list_of_comp_ans.append(self.calculated_diff)
		
	self.show_game_toolbar()

    def remove_game_toolbar(self, alert):
	self.remove_alert(alert)

    def show_game_toolbar(self):
	self.chatbox.rem()
	if addition_mode:
         self.game_tools(_('\t\tStart : ' + \
         	str(global_first_num) + '\n\t\t+ Add\t: ' +\
         	str(global_second_num)), _(''))
	if subtraction_mode:
         self.game_tools(_('\t\tStart : ' + \
         	str(global_first_num) + '\n\t\t- Subtract\t: ' + \
         	str(global_second_num)), _(''))


    def make_root(self):
        entry = gtk.Entry()
        entry.modify_bg(gtk.STATE_INSENSITIVE, style.COLOR_WHITE.get_gdk_color())
        entry.modify_base(gtk.STATE_INSENSITIVE, style.COLOR_WHITE.get_gdk_color())
        entry.set_sensitive(True)
        entry.connect('activate', self.entry_activate_cb)
	entry.connect('key-press-event', self.entry_key_press_cb)
        self.entry = entry
        hbox = gtk.HBox()
        hbox.add(entry)
        box = gtk.VBox(homogeneous=False)
        box.pack_start(self.chatbox)
        box.pack_start(hbox, expand=False)
        return box


    def entry_key_press_cb(self, widget, event):
        """Check for scrolling keys.
        Check if the user pressed Page Up, Page Down, Home or End and
        scroll the window according the pressed key.
        """
        vadj = self.chatbox.get_vadjustment()
        if event.keyval == gtk.keysyms.Page_Down:
            value = vadj.get_value() + vadj.page_size
            if value > vadj.upper - vadj.page_size:
                value = vadj.upper - vadj.page_size
            vadj.set_value(value)
        elif event.keyval == gtk.keysyms.Page_Up:
            vadj.set_value(vadj.get_value() - vadj.page_size)
        elif event.keyval == gtk.keysyms.Home and \
             event.state & gtk.gdk.CONTROL_MASK:
            vadj.set_value(vadj.lower)
        elif event.keyval == gtk.keysyms.End and \
             event.state & gtk.gdk.CONTROL_MASK:
            vadj.set_value(vadj.upper - vadj.page_size)

    def entry_activate_cb(self, entry):
	msg_for_NaN = "Please enter a number."
	self.chatbox._scroll_auto = True
        text = entry.props.text
	logger.debug('Entry: %s' % text)
 	global scoretime
	global accuracy
	global gameComplete
	global list_of_comp_ans
	global list_of_user_ans
	if text.isdigit():
	 if addition_mode:
	  while (self.calculated_sum <= self.limit_num):
   	   self.chatbox.add_text(self.owner, text)
       	   entry.props.text = ''
	   list_of_user_ans.append(int(text))
	   list_of_comp_ans.append(self.calculated_sum)
   	   self.chatbox.add_text1(self.owner, str(self.calculated_sum))
	   self.connect(self.input_ans_check(text))
	   if (self.first_come_check == 0):
    	    scoretime = time.time()
	    self.first_come_check = 1
	 elif subtraction_mode:
	  while (self.calculated_diff > 0):
   	   self.chatbox.add_text(self.owner, text)
       	   entry.props.text = ''
	   list_of_user_ans.append(text)
	   list_of_comp_ans.append(self.calculated_diff)
   	   self.chatbox.add_text1(self.owner, str(self.calculated_diff))
	   self.connect(self.input_ans_check(text))
	   if (self.first_come_check == 0):
    	    scoretime = time.time()
	    self.first_come_check = 1
	 self.calc_accuracy(no_of_mistake, steps)
	 scoretime = time.time() - scoretime
	 self.game_finish()
	 gameComplete = True
	 self.game_metadata = True
	 self.write_to_csv()
	 self.write_to_scorecard()
	 self.sort_score_file()
	 self.first_come_check += 1
	 entry.props.text = ''
   	 self.chatbox.add_text1(self.owner, "Game Over")
	 self.entry.set_sensitive(False)
	else:
	   self.chatbox.add_text(self.owner, msg_for_NaN)
        entry.props.text = ''

    def calc_accuracy(self, mistakes_arg, steps_arg):
	  global accuracy
	  accuracy = ((steps_arg - mistakes_arg) / float(steps_arg)) * 100
	  accuracy = int(accuracy * 100) / 100.0
	  accuracy = int(round(accuracy, 0))

    def game_finish(self):
	  top_lbl_in_dialog = ''
	  game_reply = gtk.Label()
	  game_details = gtk.Label()
	  img_on_game_finish = gtk.Image()
	  if (accuracy == 100):
	   top_lbl_in_dialog = "Congratulations..!!"
	   game_reply.set_text("Perfect Score")
	   game_details.set_text("Accuracy: " + str(accuracy) + \
	   	"\nTime: " + str('%.1f' % scoretime))
	   img_on_game_finish.set_from_file("100AC.png")
	  elif (accuracy < 100 and accuracy >= 85):
	   top_lbl_in_dialog = "Congratulations..!!"
	   game_reply.set_text("Great Score")
	   game_details.set_text("Accuracy: " + str(accuracy) + \
	   	"\nTime: " + str('%.1f' % scoretime))
	   img_on_game_finish.set_from_file("85_100AC.png")
	  elif (accuracy < 85 and accuracy >= 60):
	   top_lbl_in_dialog = "Congratulations..!!"
	   game_reply.set_text("Well Played")
	   game_details.set_text("Accuracy: " + str(accuracy) + \
	   	"\nTime: " + str('%.1f' % scoretime))
	   img_on_game_finish.set_from_file("60_85AC.png")
	  elif (accuracy == 0):
	   top_lbl_in_dialog = "Game Over..!!"
	   game_reply.set_text("Better Luck Next Time")
	   game_details.set_text("Accuracy: " + str(accuracy) + \
	   	"\nTime: " + str('%.1f' % scoretime))
	   img_on_game_finish.set_from_file("AC_0.svg")
	  else:
	   top_lbl_in_dialog = "Game Over..!!"
	   game_reply.set_text("Play Once More..")
	   game_details.set_text("Accuracy: " + str(accuracy) + \
	   	"\nTime: " + str('%.1f' % scoretime))
	   img_on_game_finish.set_from_file("60AC.png")

	  messagedialog = gtk.MessageDialog(parent=None, \
	  	flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, \
	  	buttons=gtk.BUTTONS_OK,message_format=top_lbl_in_dialog)
	  
	  messagedialog.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00FFFF'))
	  
   	  messagedialog.set_image(img_on_game_finish)
	  action_area = messagedialog.get_content_area()

	  action_area.pack_start(game_reply)
	  action_area.pack_start(game_details)
	  messagedialog.show_all()
	  messagedialog.run()
	  messagedialog.destroy()

    def write_to_csv(self):
	global accuracy
	time_of_write = time.strftime("%d/%m %I:%M")
	game_time = round(scoretime, 3)
	with open("scoreStatistics.csv", "a+") as f:
	 f.write(time_of_write + "," + '%i' %accuracy + "," + \
	 	str(self.local_first_num) + "," + \
	 	str(self.local_second_num) + "," + \
	 	str(self.mode_of_game) + "," + str(steps))
 	 f.write("," + str(no_of_mistake) + "," + \
 	 	str(game_time) + "," + str(round((game_time / steps), 3)) \
 	 	+ "," + self.difficulty_level + "\n")

    def write_to_scorecard(self):
	if addition_mode:
	 line1 = 'Addition'
	elif subtraction_mode:
	 line1 = 'Subtraction'
     	l = [[accuracy, self.local_first_num, \
     	self.local_second_num, no_of_mistake, \
     	steps, '%.1f' % scoretime, line1]]

	with open('score_card.txt', 'a+') as f:
	 for row in l:
	    for column in row:
	        f.write('%s\t\t\t\t' % column)
	    f.write('\n')
	 f.close()
	

    def sort_score_file(self):
	with open('score_card.txt') as fin:
    		lines = [line.split() for line in fin]
	lines.sort(key=lambda x:int(x[0]), reverse=True)
	with open('sorted_score_card.txt', 'w') as fout:
		for el in lines:
        		fout.write('{0}\t\t\t\t\n'.format('\t\t\t'.join(el)))

    #for evaluation for user ans
    def input_ans_check(self, ans):
	 global steps
 	 global no_of_mistake
	 global accuracy
	 global list_of_comp_ans
	 global list_of_user_ans
	 if addition_mode:
	  v = self.calculated_sum
	 elif subtraction_mode:
	  v = self.calculated_diff
	 steps += 1
	 if (v == int(ans)):
	   accuracy += 10
	   if self.second_attempt_flag:
	    self.second_attempt_flag = False
	 else:
  	   no_of_mistake += 1
	   if self.second_attempt_flag:
	    self.second_attempt_flag = False
	   else:
	    self.second_attempt_flag = True
	 if addition_mode and not self.second_attempt_flag:
	  self.calculated_sum = self.calculated_sum + self.local_second_num
	  self.second_attempt_flag = False
	 elif subtraction_mode and not self.second_attempt_flag:
	  self.calculated_diff = self.calculated_diff - self.local_second_num
	  self.second_attempt_flag = False
  	 self.connect(self.input_ans_check(self.connect(self.entry_activate_cb())))

    def write_file(self, file_path):

        """Store chat log in Journal.

        Handling the Journal is provided by Activity - we only need
        to define this method.
        """
        logger.debug('write_file: writing %s' % file_path)
        self.chatbox.add_log_timestamp()
        f = open(file_path, 'w')
        try:
            f.write(self.chatbox.get_log())
        finally:
            f.close()
	  
        self.metadata['mime_type'] = 'text/plain'

	if self.game_metadata:
         self.metadata['Steps'] = steps
         self.metadata['Accuracy'] = accuracy
 	 self.metadata_dict["Player"] = str(self.owner.props.nick)
 	 self.metadata_dict["Played At"] = str(datetime.now())
	 self.metadata_dict["Start_Num: "] = self.local_first_num
	 self.metadata_dict["Second_num"] = self.local_second_num
	 self.metadata_dict["Mistakes"] = no_of_mistake
	 self.metadata_dict["Mode_of_game"] = self.mode_of_game
	 self.metadata_dict["Steps"] = steps
	 self.metadata_dict["Accuracy"] = accuracy
	 self.metadata_dict["Correct_Ans"] = json.dumps(list_of_comp_ans)
	 self.metadata_dict["User_Ans"] = json.dumps(list_of_user_ans)
	 self.metadata_dict["Time_taken"] = round(scoretime, 3)
	 self.metadata_dict["Avg_response_time"] = round((scoretime / steps), 3)
	 self.metadata_dict["Difficulty_Level"] = str(self.difficulty_level)
         self.metadata['Game_Details'] = json.dumps(self.metadata_dict, indent=4)

    def read_file(self, file_path):
        """Load a chat log from the Journal.

        Handling the Journal is provided by Activity - we only need
        to define this method.
        """
        logger.debug('read_file: reading %s' % file_path)
        log = open(file_path).readlines()
        last_line_was_timestamp = False
        for line in log:
            if line.endswith('\t\t\n'):
                if last_line_was_timestamp is False:
                    timestamp = line.strip().split('\t')[0]
                    self.chatbox.add_separator(timestamp)
                    last_line_was_timestamp = True
            else:
                timestamp, nick, color, status, text = line.strip().split('\t')
                status_message = bool(int(status))
                self.chatbox.add_text({'nick': nick, 'color': color},
                              text, status_message)
                last_line_was_timestamp = False
