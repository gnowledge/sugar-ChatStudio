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
import math
import os
from gettext import gettext as _
import csv
from datetime import datetime
from operator import itemgetter
import time
import json
from sugar.graphics import style
from sugar.graphics.alert import NotifyAlert
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.alert import Alert
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.palette import Palette
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity import activity
from sugar.presence import presenceservice
from sugar.activity.widgets import ActivityButton, TitleEntry
from sugar.activity.widgets import StopButton, ShareButton, RadioMenuButton,ActivityToolbarButton
from random import randint,choice
from chat import smilies
from sugar.session import SessionManager
from sugar.graphics.toolcombobox import ToolComboBox
from chat.box import ChatBox
from sugar.graphics.icon import Icon
import time
import subprocess
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas


from chat.box import TextBox
logger = logging.getLogger('ChatStudioSelf-activity')
steps=0
SMILIES_COLUMNS = 5
snum=0
c1=0
chk=0
c2=0
scoretime=time.time()
flag=0
accuracy=0
cssw=0
no_of_mistake=0
lans=[]
luans=[]
gameComplete=False
dates=[]
timescores=[]
accscores=[]
ad=False
sb=False

class VisualScore(ToolButton):
    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'scorestats', **kwargs)
        self.props.tooltip = _('Score Stats')
        self.connect('clicked', self.draw_score_chart)


    def draw_score_chart(self,button):
	winScore = gtk.Window()
	winScore.connect("destroy", lambda x: gtk.main_quit())
	winScore.set_default_size(800,490)
	winScore.set_position(gtk.WIN_POS_CENTER)
	winScore.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
	winScore.set_title("Score Statistics")
	score_chart_fig = Figure(figsize=(5,4), dpi=100)
	plot_score_dgm = score_chart_fig.add_subplot(111)
	accuracy_list=[]
	dates_list=[]
	with open("scoreStatistics.csv", "r") as csvfile:
	 csv_content = csv.DictReader(csvfile,delimiter=',')
	 list_of_dict = []
	 for row in csv_content:
	  list_of_dict.append(row)
	for each_dict in list_of_dict[-10:]:
	 accuracy_list.append(int(each_dict["score"]))
	 date_det = each_dict["date_detail"].replace(" ","")
	 dates_list.append(date_det) 
	y_pos = np.arange(len(dates_list))	
	error = np.random.rand(len(dates_list))
	plot_score_dgm.barh(y_pos, accuracy_list, xerr=error, align='center', alpha=0.4)
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

    def draw_time_chart(self,button):
	winTime = gtk.Window()
	winTime.connect("destroy", lambda x: gtk.main_quit())
	winTime.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
	winTime.set_default_size(800,490)
	winTime.set_position(gtk.WIN_POS_CENTER)
	winTime.set_title("Time Statistics")
	time_chart_fig = Figure(figsize=(5,4), dpi=100)
	plot_time_dgm = time_chart_fig.add_subplot(111)
	game_time_list=[]
	dates_list=[]
	with open("scoreStatistics.csv", "rb") as csvfile:
	 csv_content = csv.DictReader(csvfile,delimiter=',')
	 list_of_dict = []
	 for row in csv_content:
	  list_of_dict.append(row)
	for each_dict in list_of_dict[-10:]:
	 game_time_list.append(float(each_dict["time_taken"]))
	 date_det = each_dict["date_detail"].replace(" ","")
	 dates_list.append(date_det) 
	y_pos = np.arange(len(dates_list))	
	error = np.random.rand(len(dates_list))
	plot_time_dgm.barh(y_pos, game_time_list, xerr=error, align='center', alpha=0.4)
	plot_time_dgm.set_yticks(y_pos)
	plot_time_dgm.set_yticklabels(dates_list)
	
	time_canvas = FigureCanvas(time_chart_fig)  # a gtk.DrawingArea
	winTime.add(time_canvas)
	winTime.show_all()
	gtk.main()

class scoreWindow:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	#self.window.set_size_request(800, 200)
	self.window.set_resizable(False)
	self.window.set_title("Score card")
	self.window.set_position(gtk.WIN_POS_CENTER)
	self.vb=gtk.VBox()

	line=''#Declare an empty string 
	self.go=gtk.Label("Game Over\n")
        self.lalign = gtk.Alignment(0, 0, 0, 0)
        self.label_result = gtk.Label("  Rank\tAccuracy\t\tStart\t\tAdd\t\tMistakes\t\t\tSteps\t\tTime\t\tMode")

        self.lalign.add(self.label_result)

	self.vb.pack_start(self.go, False, False, 0)
        self.vb.pack_start(self.lalign, False, False, 0)
	self.hb1=gtk.HBox()
	self.tv = gtk.TextView()
	self.tv.modify_text(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
	self.tv.set_editable(0)
	self.tv.set_cursor_visible(0)
	self.tv.set_left_margin(30)
        textbuffer = self.tv.get_buffer()
        self.tv.show()
	global gameComplete
	if (cssw==0):
	 self.readscores(textbuffer,line)
	elif (cssw==1):
	 if (gameComplete):
	  self.readscores1(textbuffer,line)

	 else:
	  line='Incomplete Game'
          textbuffer.set_text(line)
	 global cssw
	 cssw=0
	elif (cssw==2):
	 if (gameComplete):
	  self.readscores2(textbuffer,line)
	 else:
	  line='Incomplete Game'
          textbuffer.set_text(line)
	 global cssw
	 cssw=0
	self.hb1.pack_start(self.tv, fill=False)
	self.hb2=gtk.HBox()
	self.b1=gtk.Button("Check Last Game answer")

	self.b2=gtk.Button("Last Game Score")
	self.b1.connect("clicked", self.chkans_card,self.window)
	self.b2.connect("clicked", self.last_game_score,self.window)
	self.hb2.pack_start(self.b1, fill=False)
	self.hb2.pack_start(self.b2, fill=False)

	self.vb.pack_start(self.hb1, fill=False)
	self.vb.pack_start(self.hb2, fill=False)
	color = gtk.gdk.color_parse('#FF8300')
        self.window.modify_bg(gtk.STATE_NORMAL, color)
	self.window.add(self.vb)
	self.window.show_all()


    def readscores(self,textbuffer,line):
	 if not (os.stat("score_card1.txt").st_size==0): #when file not empty
          with open("score_card1.txt", "r") as infile:
	   for i in range(0,10): #displays only top 10 lines of the file
	     line+='\n'+str(i+1)+'\t'+infile.readline()
          textbuffer.set_text(line)

    def readscores2(self,textbuffer,line):
	 global luans
	 global lans
	 a=len(lans)
	 b=len(luans)
	 i,j=0,0
	 line+='Your Answer \t <------->\t Correct Answer\n'
	 while i < a and j<b:
	  line+=str(luans[i])+' \t\t\t <------->\t\t'+str(lans[j])+'\n'
	  i+=1
	  j+=1
         textbuffer.set_text(line)

    def readscores1(self,textbuffer,line):
	  line+='   '+str(accuracy)+'\t\t\t  '+str(c1)+'\t\t\t  '+str(c2)+'\t\t    '+str(no_of_mistake)+ \
	        '\t\t\t\t  '+str(steps)+'\t\t\t'+'%.1f' % scoretime+'\t\t\t'
	  if ad:
	   line+='Addition\n'
	  elif sb:
	   line+='Subtraction\n'
          textbuffer.set_text(line)

    def chkans_card(self,button,window):
	window.destroy()
	global cssw
	cssw=2
	scoreWindow()
	
    def last_game_score(self,button,window):
	window.destroy()
	global cssw
	cssw=1
	scoreWindow()


class ScoreButton(ToolButton):
    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'score_card', **kwargs)
        self.props.tooltip = _('Score Card')
        self.connect('clicked', self.__show_score_win, activity)

    def __show_score_win(self, button, activity):
	scoreWindow()

class NotifyAlert1(Alert):
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
	self.a=0
	global accuracy
	accuracy=0
	global luans
	del luans[:]
	self.a1=0
	self.a2=0
	self.xsum=50
	self.sum1=0
	self.diff1=0
	self.xx=0
	self.mode_of_game={}
	self.op_mode=""
	self.game_metadata = False

	global lans
	del lans[:]
	self.attempts=1
	self.hard_difficulty_level="Easy"
	self.initialize=0
	self.create_toolbar()


        pservice = presenceservice.get_instance()
        self.owner = pservice.get_owner()
        # Chat is room or one to one:
        self._chat_is_room = False
        #self._alert1(_('\t\tStart : '+str(self.a1)+ '\n\t\tAdd\t: '+str(self.a2)), _(''))

    def create_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.toolbar.insert(ActivityToolbarButton(self), -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	scoreButton=ScoreButton(self)
	toolbar_box.toolbar.insert(scoreButton,-1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	self._modes = ToolComboBox()
        self._modelist = ['Select Mode','+ Add', '- Subtract']
       	for i, f in enumerate(self._modelist):
         self._modes.combo.append_item(i, f) 
       	self.modes_handle_id = self._modes.combo.connect("changed",self._changemodes_toolbar)
        toolbar_box.toolbar.insert(self._modes, -1)

        self._modes.combo.set_active(0)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	scorestats=VisualScore(self)
	toolbar_box.toolbar.insert(scorestats,-1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

	timestats=VisualTime(self)
	toolbar_box.toolbar.insert(timestats,-1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        toolbar_box.toolbar.insert(separator, -1)

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)

	stopButton=StopButton(self)
	toolbar_box.toolbar.insert(stopButton,-1)
        toolbar_box.show_all()

    def _changemodes_toolbar(self, combo):
        self.x = combo.get_active()
	global c1
	global c2
	if (self.x == 1):
	 c1=randint(5,9)
	 c2=randint(5,9)
	 combo.set_sensitive(False)
	 self.a1=c1
	 self.a2=c2
	 self.sum1=self.a1+self.a2
	 self.op_mode="Addition"
	 global ad
	 ad=True
	 self.showalert()

 	elif (self.x==2):
	 c1=randint(50,55)
	 c2=randint(5,9)
	 combo.set_sensitive(False)
	 self.a1=c1
	 self.a2=c2
	 self.diff1=self.a1-self.a2
	 self.op_mode="Subtraction"
	 global sb
	 sb=True
	 self.showalert()

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

    def _alert1(self, title, text=None):
        alert = NotifyAlert1()
        alert.props.title = title
        alert.props.msg = text
        self.add_alert(alert)
        alert.connect('response', self.ng)
        alert.show()

    def ng(self, alert, response_id):
	global steps
 	global no_of_mistake
	global accuracy
	global lans
	global luans
	global gameComplete
	steps=0
 	accuracy=0.0
	no_of_mistake=0
	self.initialize==0
	gameComplete=False
	del lans[:]	
	del luans[:]
	global scoretime
    	scoretime = time.time()
        self.remalert(alert)
	global c1
	global c2
	self.xx=1
	self.chatbox.rem()	
	
	if (response_id==1): #Cancel--> New Game
	 self.hard_difficulty_level="Easy"
	 if ad:
	  c1=randint(5,9)	
	  c2=randint(5,9)
	  self.xsum=50
	 elif sb:
	  c1=randint(50,59)	
	  c2=randint(5,9)
	  self.xsum=50

	elif (response_id==2): #OK--> Change Numbers Dialog
	 self.hard_difficulty_level="Changed_Numbers"

	 messagedialog = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK,\
	 message_format="Enter Numbers")
	 action_area = messagedialog.get_content_area()
	 lbl1=gtk.Label("Start")
	 entry1 = gtk.Entry()
         entry1.set_size_request(int(gtk.gdk.screen_width() / 25),-1)
	 if ad:
	  lbl2=gtk.Label("+ Add")
	 elif sb:
	  lbl2=gtk.Label("- Subtract")
	 entry2 = gtk.Entry()
         entry2.set_size_request(int(gtk.gdk.screen_width() / 25),-1)

	 action_area.pack_start(lbl1)
	 action_area.pack_start(entry1)
	 action_area.pack_start(lbl2)
	 action_area.pack_start(entry2)
	 messagedialog.show_all()
	 ark=messagedialog.run()

         if ark == gtk.RESPONSE_OK:
	  try:
       	   c1 = int(entry1.get_text())
	   c2 = int(entry2.get_text())
	   if sb:
	    if (c2>c1):
		#raise BadNum("Num2 canot be greater than Num1")
		raise Exception
	  except Exception:
	   if ad:
	    c1=randint(5,9)
	    c2=randint(5,9)
	   elif sb:
	    c1=randint(50,59)
	    c2=randint(5,9)

	 messagedialog.destroy()
	 self.xsum=50

	elif(response_id==3):
	 self.hard_difficulty_level="Easy"
	 easylistStartNum=[50,52,54,55,56,51]
	 l1=[6,9,3,2]
	 l2=[5,10,2]
	 l3=[7,8]
	 if ad:
	  c1=randint(1,9)	
	  c2=c1
	 elif sb:
	  c1=choice(easylistStartNum)	
	  if (c1==50):
	   c2=choice(l2)
	  elif (c1==51):
	   c2=3
	  elif (c1==52):
	   c2=2
	  elif (c1==54):
	   c2=choice(l1)
	  elif (c1==55):
	   c2=5
	  elif (c1==56):
	   c2=choice(l3)
 	 self.xsum=50

	elif(response_id==4):
	 self.hard_difficulty_level="Medium"
	 l11=[51,52,53,54,56,57,58,59]
	 if ad:
	  c1=randint(2,9)
	  c2=randint(2,9)
	  if (c1==c2):
	   c2=randint(2,9)
	 elif sb:
	  c1=choice(l11)
	  c2=randint(2,9)
	 if (c1==c2):
	   c2=randint(2,9)
	 self.xsum=50
	 
	elif(response_id==5):
	 self.hard_difficulty_level="Hard"
	 if ad:
	  c1=randint(5,10)	
	  c2=randint(5,10)
	 elif sb:
	  c1=randint(100,105)	
	  c2=randint(5,9)
	 self.xsum=100

	self.a1=c1
	self.a2=c2
	if ad:
	 self.sum1=self.a1+self.a2
	if sb:
	 self.diff1=self.a1-self.a2
		
	global lans
	lans.append(self.sum1)
	self.showalert()

    def remalert(self,alert):
	self.remove_alert(alert)

    def showalert(self):
	self.chatbox.rem()		
	if ad:		
         self._alert1(_('\t\tStart : '+str(c1)+ '\n\t\t+ Add\t: '+str(c2)), _(''))
	if sb:
         self._alert1(_('\t\tStart : '+str(c1)+ '\n\t\t- Subtract\t: '+str(c2)), _(''))


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

	strr="Please enter a number."

	self.chatbox._scroll_auto = True
        text = entry.props.text
	logger.debug('Entry: %s' % text)
 	global scoretime
	global accuracy
	global gameComplete
	global lans
	global luans
	if text.isdigit():
	 if ad:
	  while (self.sum1<=self.xsum):
   	   self.chatbox.add_text(self.owner, text)
       	   entry.props.text = ''
	   luans.append(int(text))
	   lans.append(self.sum1)
   	   self.chatbox.add_text1(self.owner,str(self.sum1))
	   self.connect(self.entry_ans_check_auto(text))
	   if (self.initialize==0):
    	    scoretime = time.time()
	    self.initialize=1
	  self.calAccuracy(no_of_mistake,steps)
	  scoretime= time.time() - scoretime
	  self.msg_displ(accuracy,scoretime)
	  gameComplete=True
	  self.game_metadata = True
	  self.write_data_for_visual()
	  self.write_score()
	  self.sort_score_file()
	  self.initialize+=1
	  entry.props.text = ''
	 elif sb:
	  while (self.diff1>0):
   	   self.chatbox.add_text(self.owner, text)
       	   entry.props.text = ''
	   luans.append(text)
	   lans.append(self.diff1)
   	   self.chatbox.add_text1(self.owner,str(self.diff1))
	   self.connect(self.entry_ans_check_auto(text))
	   if (self.initialize==0):
    	    scoretime = time.time()
	    self.initialize=1
	  self.calAccuracy(no_of_mistake,steps)
	  scoretime= time.time() - scoretime

	  self.msg_displ(accuracy,scoretime)
	  
	  gameComplete=True
	  self.write_data_for_visual()
	  self.write_score()
	  self.sort_score_file()
	  self.initialize+=1
	  entry.props.text = ''
	 entry.props.text = ''
	else:
	   self.chatbox.add_text(self.owner, strr)
        entry.props.text = ''

    def calAccuracy(self,mist,stps):
	  global accuracy
	  accuracy=((stps-mist)/float(stps))*100
	  accuracy=int(accuracy*100)/100.0
	  accuracy=int(round(accuracy,0))

    def msg_displ(self,ac,st):
	  lbl1=gtk.Label()
	  lbl2=gtk.Label()
	  strdialog=''
	  scoreimg = gtk.Image()
	  if (accuracy==100):
	   strdialog="Congratulations..!!"
	   lbl1.set_text("Perfect Score")
	   lbl2.set_text("Accuracy: "+str(accuracy)+"\nTime: "+str('%.1f' % scoretime))
	   scoreimg.set_from_file ("100AC.png") 
	  elif (accuracy<100 and accuracy>=85):
	   strdialog="Congratulations..!!"
	   lbl1.set_text("Great Score")
	   lbl2.set_text("Accuracy: "+str(accuracy)+"\nTime: "+str('%.1f' % scoretime))
	   scoreimg.set_from_file ("85_100AC.png")
	  elif (accuracy<85 and accuracy>=60):
	   strdialog="Congratulations..!!"
	   lbl1.set_text("Well Played")
	   lbl2.set_text("Accuracy: "+str(accuracy)+"\nTime: "+str('%.1f' % scoretime))
	   scoreimg.set_from_file ("60_85AC.png")
	  elif (accuracy==0):
	   strdialog="Game Over..!!"
	   lbl1.set_text("Better Luck Next Time")
	   lbl2.set_text("Accuracy: "+str(accuracy)+"\nTime: "+str('%.1f' % scoretime))
	   scoreimg.set_from_file ("AC_0.svg") 
	  else:
	   strdialog="Game Over..!!"
	   lbl1.set_text("Play Once More..")
	   lbl2.set_text("Accuracy: "+str(accuracy)+"\nTime: "+str('%.1f' % scoretime))
	   scoreimg.set_from_file ("60AC.png")

	  messagedialog = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK,message_format=strdialog)
	  messagedialog.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse('#00FFFF'))
	  
   	  messagedialog.set_image (scoreimg)
	  action_area = messagedialog.get_content_area()

	  action_area.pack_start(lbl1)
	  action_area.pack_start(lbl2)
	  messagedialog.show_all()
	  messagedialog.run()
	  messagedialog.destroy()

    def write_data_for_visual(self):
	global accuracy
	x=time.strftime("%d/%m %I:%M")
	a=round(scoretime,3)
	with open("scoreStatistics.csv","a+") as f:
	 f.write(x)
	 f.write(",")
	 f.write('%i'%accuracy)
	 f.write(",")
	 f.write(str(self.a1))
	 f.write(",")
	 f.write(str(self.a2))
	 f.write(",")
	 f.write(str(self.op_mode))
	 f.write(",")
	 f.write(str(steps))
 	 f.write(",")
	 f.write(str(no_of_mistake))
	 f.write(",")
	 f.write(str(a))
	 f.write(",")
	 f.write(str(round((a/steps),3)))
	 f.write(",")
	 f.write(self.hard_difficulty_level)
	 f.write("\n")

    def write_score(self):
	if ad:
	 line1='Addition'
	elif sb:
	 line1='Subtraction'
     	l= [[accuracy,self.a1,self.a2,no_of_mistake,steps,'%.1f' % scoretime,line1]]

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
	with open('score_card1.txt', 'w') as fout:
		for el in lines:
        		fout.write('{0}\t\t\t\t\n'.format('\t\t\t'.join(el)))
    #for addition
    def entry_ans_check_auto(self,ans):
	 global steps
 	 global no_of_mistake
	 global accuracy
	 global lans
	 global luans
	 if ad:
	  v = self.sum1
	 elif sb:
	  v = self.diff1
	 steps+=1
	 if (v ==int(ans)):
	   accuracy+=10
	 else:
  	   no_of_mistake+=1
	 if ad:
	  self.sum1=self.sum1+self.a2
	 elif sb:	
	  self.diff1=self.diff1-self.a2
  	 self.connect(self.entry_ans_check_auto(self.connect(self.entry_activate_cb())))    

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
 	 self.mode_of_game["Player"] = str(self.owner.props.nick)
 	 self.mode_of_game["Played At"] = str(datetime.now())
	 self.mode_of_game["Start_Num: "] = self.a1
	 self.mode_of_game["Second_num"] = self.a2
	 self.mode_of_game["Mistakes"] = no_of_mistake
	 self.mode_of_game["Mode_of_game"] = self.op_mode
	 self.mode_of_game["Steps"] = steps
	 self.mode_of_game["Accuracy"] = accuracy
	 self.mode_of_game["Correct_Ans"] = json.dumps(lans)
	 self.mode_of_game["User_Ans"] = json.dumps(luans)
	 self.mode_of_game["Time_taken"] = round(scoretime,3)
	 self.mode_of_game["Avg_response_time"] = round((scoretime/steps),3)
	 self.mode_of_game["Difficulty_Level"] = str(self.hard_difficulty_level)
         self.metadata['Game_Details'] = json.dumps(self.mode_of_game, indent=4)

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