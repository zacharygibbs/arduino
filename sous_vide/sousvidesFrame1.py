"""
This was created with Boa Constructor and is meant to provide a user interface to viewing the incoming Sous Vide Data
"""

#Boa:Frame:Frame1

import wx
from matplotlib.figure import Figure
import copy
import pickle

#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib import use
use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_wx import _load_bitmap, bind
from pylab import setp
#import numpy.random
#Boa:Frame:Frame1
import sys
sys.path.append('../')
import numpy as np
import wx
import zach
import os.path
from os import getcwd
import os
import subprocess
import pdb
#import matplotlib.animation as animation

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(6)]

[wxID_FRAME1TIMER1] = [wx.NewId() for _init_utils in range(1)]

class Frame1(wx.Frame):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_FRAME1TIMER1, owner=self)
        self.Bind(wx.EVT_TIMER, self.Timer1update, id=wxID_FRAME1TIMER1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(712, 124), size=wx.Size(802, 583),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self._init_utils()
        self.SetClientSize(wx.Size(786, 544))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(176, 40), size=wx.Size(424, 192),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2', parent=self,
              pos=wx.Point(176, 296), size=wx.Size(424, 192),
              style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='Start Plotting',
              name='button1', parent=self, pos=wx.Point(104, 512),
              size=wx.Size(75, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label='Stop Plotting',
              name='button2', parent=self, pos=wx.Point(208, 512),
              size=wx.Size(75, 23), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='p - black\ni-red\nd-blue\nval-green', name='staticText1',
              parent=self, pos=wx.Point(64, 352), size=wx.Size(47, 128),
              style=0)

    def init_plot(self):
            self.dpi = 100
            figdim=6,1.5#(4.5,3.0)
            self.figure = Figure(figdim, dpi=self.dpi)
            self.canvas = FigCanvas(self.panel1, -1, self.figure)
            self.axes = self.figure.add_subplot(111)
            self.axes.set_axis_bgcolor('white')
            setp(self.axes.get_xticklabels(), fontsize=6)
            setp(self.axes.get_yticklabels(), fontsize=6)
            
            self.toolbar = NavigationToolbar(self.canvas)#Toolbar(self.canvas)
            #self.toolbar.Realize()
            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
            self.vbox.Add(self.toolbar, 0, wx.EXPAND|wx.BOTTOM)
            self.panel1.SetSizer(self.vbox)
            self.vbox.Fit(self.panel1)
#            cid = self.figure.canvas.mpl_connect('button_press_event', self.onfigureclick)
            
        
            self.figure2 = Figure(figdim, dpi=self.dpi)
            self.canvas2 = FigCanvas(self.panel2, -1, self.figure2)
            self.axes2 = self.figure2.add_subplot(111)
            self.axes2.set_axis_bgcolor('white')
            setp(self.axes2.get_xticklabels(), fontsize=6)
            setp(self.axes2.get_yticklabels(), fontsize=6)
            
            self.toolbar2 = NavigationToolbar(self.canvas2)#Toolbar(self.canvas)
            
            #self.toolbar.Realize()
            self.vbox2 = wx.BoxSizer(wx.VERTICAL)
            self.vbox2.Add(self.canvas2, 1, wx.LEFT | wx.TOP | wx.GROW)
            self.vbox2.Add(self.toolbar2, 0, wx.EXPAND|wx.BOTTOM)
            self.panel2.SetSizer(self.vbox2)
            self.vbox2.Fit(self.panel2)
#            cid = self.figure.canvas.mpl_connect('button_press_event', self.onfigureclick)
    def __init__(self, parent):
        self._init_ctrls(parent)
        self.init_plot()
        self._init_utils()

    def OnButton1Button(self, event):
        self.timer1.Start(2000)
        print 'made it HHEHHEHEHRE'

    def OnButton2Button(self, event):
        self.timer1.Stop()
    def Timer1update(self, event):
        
        #print "success"
        cur_time, cur_temp, cur_sp, cur_p, cur_i, cur_d, cur_val= pickle.load(open('sous_videslog.pickle','r'))
        
        self.axes.plot(cur_time, cur_temp, 'k.-')
        self.axes.plot(cur_time, cur_sp, 'r.-')
        self.axes2.plot(cur_time, cur_p, 'k.-')
        self.axes2.plot(cur_time, cur_i, 'r.-')
        self.axes2.plot(cur_time, cur_d, 'b.-')
        self.axes2.plot([0, cur_time[-1]], [0, 0], 'k--', lw=1)
        self.axes2.plot(cur_time, cur_val, 'g.-')
        self.canvas.draw()
        #self.canvas.refresh()
        self.canvas2.draw()


        
class BoaApp(wx.App):
    def OnInit(self):
        self.main = create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True
        
def main(file = ''):
    application = BoaApp(0)
    application.MainLoop()    
        

if __name__ == '__main__':
    if len(sys.argv)>1:
        file = sys.argv[1]
    else:
        file = ''
    if file=="pickle":
        main(file)
    else:
        #execfile('sous_vides.py')
        try:
            pee=subprocess.Popen(['python','sous_vides.py'], shell=True)
            main(file)
        except:
            pass
        finally:
            pee.kill()
