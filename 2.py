import wx
import MplayerCtrl as mpc
import wx.media
import wx.lib.buttons as buttons
import os
import time
#include <wx/mediactrl.h>

class Main(wx.Frame):
    def __init__(self,parent,title):
            
        wx.Frame.__init__(self,None,title=title,size=(800,600))
        
        self.currentVolume = 50
        panel=wx.Panel(self)
        self.SetBackgroundColour("purple")
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sliderSizer = wx.BoxSizer(wx.HORIZONTAL)

        #adding button
        self.mpc = mpc.MplayerCtrl(self,-1,u'C:\\Users\\shubham\\Downloads\\MPlayer-generic-r37875+gce466d0\\MPlayer-generic-r37875+gce466d0\\mplayer.exe',u'C:\\Users\\shubham\\Desktop\\wxpython\\hello.mp4',size=(800,450))
        self.slider=wx.Slider(self,pos=(0,455),size=(800,25))
        sliderSizer.Add(self.slider,1, wx.ALL|wx.EXPAND, 5)

        #play button
        pic=wx.Image("play.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button=wx.BitmapButton(self,-1,pic,pos=(400,500),size=(50,50))
        self.Bind(wx.EVT_BUTTON,self.on_pause,self.button)
        self.button.SetDefault()
        #print self.mpc.playing
        self.button.Hide()

        #pause butoon

        pic1=wx.Image("pause.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button1=wx.BitmapButton(self,-1,pic1,pos=(400,500),size=(50,50))
        self.Bind(wx.EVT_BUTTON,self.on_pause,self.button1)
        self.button1.SetDefault()
        #if wx.media.MEDIASTATE_PAUSED:
           #self.button1.Hide()

        # create volume control
        self.volumeCtrl = wx.Slider(self,pos=(600,500))
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER,self.on_set_volume)

        #create track counter
        self.trackCounter = wx.StaticText(self, label="00:00",pos=(5,480))
        sliderSizer.Add(self.trackCounter,1, wx.ALL|wx.CENTER, 5)

        # set up playback timer
        self.playbackTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update_playback)

        self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
        self.Bind(mpc.EVT_MEDIA_FINISHED, self.on_media_finished)
        self.Bind(mpc.EVT_PROCESS_STARTED, self.on_process_started)
        self.Bind(mpc.EVT_PROCESS_STOPPED, self.on_process_stopped)

        self.playbackTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update_playback) 
    
       
        self.Bind(wx.EVT_CLOSE,self.closewindow)
        self.Show()
        self.Center()
        
    def closewindow(self,event):
        self.Destroy()
        self.mpc.Quit()
  
    def on_media_started(self, event):
        print 'Media started!'
 
   
    def on_media_finished(self, event):
        print 'Media finished!'
        self.playbackTimer.Stop()
    def on_pause(self, event):
        #self.mpc.Pause()
        if self.mpc.keep_pause is True:
           print "hello"
           self.mpc.Pause()
           self.button.Show()
           self.button1.Hide()
        else :
            self.mpc.Pause()
            self.button.Hide()
            self.button1.Show()
            
        #if self.playbackTimer.IsRunning():
          # print "pausing..."
           #self.mpc.Pause()
           #Self.mpc.Pause()
           #self.playbackTimer.Stop()
        #else:
         #print "unpausing..."
             #wx.media.MEDIASTATE_PLAYING
             #self.playbackTimer.Start()
 
    
    def on_process_started(self, event):
        print 'Process started!'
 
    
    def on_process_stopped(self, event):
        print 'Process stopped!'
 
    
    def on_set_volume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        self.mpc.SetProperty("volume", self.currentVolume)
 
    
    def on_stop(self, event):
        """"""
        print "stopping..."
        self.mpc.Stop()
        self.playbackTimer.Stop()

    def on_play(self,event):
              wx.media.MEDIASTATE_PLAYING
              #self.playbackTimer.Start()
    def on_update_playback(self, event):
        """
        Updates playback slider and track counter
        """
        
        try:
            offset = self.mpc.GetTimePos()
        except:
            return
        print offset
        mod_off = str(offset)[-1]
        if mod_off == '0':
            print "mod_off"
            offset = int(offset)
            self.slider.SetValue(offset)
            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed)
app=wx.App()
#frame=Main(None,-1,"Media Player",u'C:\\Users\\shubham\\Downloads\\MPlayer-generic-r37875+gce466d0\\MPlayer-generic-r37875+gce466d0\\mplayer.exe',u'C:\\Users\\shubham\\Desktop\\wxpython\\hello.mp4')
frame=Main(None,"Media Player")
app.MainLoop()

