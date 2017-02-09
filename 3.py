import wx
import wx.media
import os
import time 
import threading
import webbrowser
import speech_recognition as sr
from espeak import espeak
from subprocess import check_output


EVT_ID_VALUE = wx.NewId()

class DataEvent(wx.PyEvent):
  def __init__(self, data):
    wx.PyEvent.__init__(self)
    self.SetEventType(EVT_ID_VALUE)
    self.data=data

class Main(wx.Frame):
        def __init__(self,parent,title):
                wx.Frame.__init__(self,None,title=title,size=(1500,1500))
                panel=wx.Panel(self)
                self.f=0.00
                self.flag=0
                self.mplay = wx.media.MediaCtrl(self,-1,"", wx.Point(0,0),wx.Size(1300,650)) #media constructor
                menubar=wx.MenuBar()#create a Menubar object mtlb upar wali line
          
                Mediamenu=wx.Menu()#create a menu object mtlb line ka first option
                Mediafirst=Mediamenu.Append(wx.ID_OPEN,'Open File','Open Media File')#first option ka pehla part
                Mediasecond=Mediamenu.Append(wx.ID_ANY,'Open Playlist','Open Your Playlist')
                Mediathird=Mediamenu.Append(wx.ID_ANY,'Open Disc','Open disc in system')
                Mediafourth=Mediamenu.Append(wx.ID_EXIT,'Quit','Quit Application')

                Playback=wx.Menu()
                Playfirst=Playback.Append(wx.ID_ANY,'Play','Play your Media File')
                Playsecond=Playback.Append(wx.ID_ANY,'Pause','Stop your Media File')
                Playthird=Playback.Append(wx.ID_ANY,'Stop','Play previous Media File')
                Playfourth=Playback.Append(wx.ID_ANY,'Next','Play next Media File')

                submenu=wx.Menu()#creating a submenu
                submenu1 = submenu.Append(wx.ID_ANY,"0.25")#creating 1 submenu
                submenu2 = submenu.Append(wx.ID_ANY,"0.50")#creating 2 submenu
                submenu3 = submenu.Append(wx.ID_ANY,"NORMAL")#creating 3 submenu
                submenu4 = submenu.Append(wx.ID_ANY,"1.25")#creating 4 submenu
                submenu5 = submenu.Append(wx.ID_ANY,"1.50")#creating 5 submenu
                submenu6=  submenu.Append(wx.ID_ANY,"2.0")#creating 6 submenu
                Playback.AppendMenu(wx.ID_ANY, "Speed", submenu)#submenu of Speed
        
                Sp=wx.Menu()
  
                Spfirst=Sp.Append(wx.ID_ANY,'Start Listening','Enable Listener')
                Spsecond=Sp.Append(wx.ID_ANY,'Stop Listening','Disable Listener')
                Spthird=Sp.Append(wx.ID_ANY,'Disable the voice','Disable the voice')

                Sub=wx.Menu()
                f=open("history.txt","r")
                s1=f.readline()
                s=[]
                while(s1!=""):
                	s.append(s1)
                	s1=f.readline()
                s1="<Empty>"
                s2="<Empty>"
                s3="<Empty>"
                s4="<Empty>"
                s5="<Empty>"	
                if len(s) >= 1:
                	s1=s[len(s)-1]
                if len(s) >= 2:
                	s2=s[len(s)-2]
                if len(s)>=3:	
                	s3=s[len(s)-3]
                if len(s)>=4 :
                	s4=s[len(s)-4]
                if len(s)>=5:	
                	s5=s[len(s)-5]	
                s11=""
                s12=""
                s13=""
                s14=""
                s15=""	
                for i in range(0,len(s1)):
                	if s1[i]=='/':
                		s11=""
                	else :
                		s11=s11+s1[i]
                for i in range(0,len(s2)):
                	if s2[i]=='/':
                		s12=""
                	else:
                		s12=s12+s2[i]
                for i in range(0,len(s3)):
                	if s3[i]=='/':
                		s13=""
                	else:
                		s13=s13+s3[i]
                for i in range(0,len(s4)):
                	if s4[i]=='/':
                		s14=""
                	else:
                		s14=s14+s4[i]
                for i in range(0,len(s5)):
                	if s5[i]=='/':
                		s15=""
                	else:
                		s15=s15+s5[i]
                self.s1=s11
                self.s2=s12
                self.s3=s13
                self.s4=s14
                self.s5=s15										
                Addsub=Sub.Append(wx.ID_ANY,s11,'history 1')
                history2=Sub.Append(wx.ID_ANY,s12,'history 2')
                history3=Sub.Append(wx.ID_ANY,s13,'history 3')
                history4=Sub.Append(wx.ID_ANY,s14,'history 4')
                history5=Sub.Append(wx.ID_ANY,s15,'history 5')
                f.close()
                menubar.Append(Mediamenu,'&Media')
                menubar.Append(Playback,'&Playback')
                menubar.Append(Sp,'&Speech')
                menubar.Append(Sub,'&History')
                
                Hel=wx.Menu()
                hel=Hel.Append(wx.ID_ANY,'Help','Help')
                About=Hel.Append(wx.ID_ANY,'About','About')

                menubar.Append(Hel,'&Help')

                self.SetMenuBar(menubar)
              #  self.CreateStatusBar()   #To create the bottom bar
               # self.StatusBar.SetBackgroundColour((220,220,220))

                
                pic=wx.Image("play.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button=wx.BitmapButton(self,-1,pic,pos=(600,675),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_pause,self.button)
                
                self.worker=None

                 #pause butoon

                pic1=wx.Image("pause.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button1=wx.BitmapButton(self,-1,pic1,pos=(600,675),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_pause,self.button1)
                self.button1.Hide()

                 #forward button
                   
                pic2=wx.Image("for.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button2=wx.BitmapButton(self,-1,pic2,pos=(640,675),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_forward,self.button2)
                

                #backward button
                   
                pic3=wx.Image("back.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button3=wx.BitmapButton(self,-1,pic3,pos=(560,675),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.on_backward,self.button3)
                

                #speech button
                pic4=wx.Image("speech.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.button4=wx.BitmapButton(self,-1,pic4,pos=(250,675),size=(40,40))
                self.Bind(wx.EVT_BUTTON,self.Onlisten,self.button4)
                
                
                  # create volume control
                self.volumeCtrl = wx.Slider(self,value=90,minValue=0,maxValue=100,pos=(1100,670),style = wx.SL_HORIZONTAL|wx.SL_LABELS,size=(100,50))
                self.volumeCtrl.Bind(wx.EVT_SLIDER,self.on_set_volume)
               
                

                #create track counter
                self.trackCounter = wx.StaticText(self, label="00:00",pos=(5,680))


                #set up playback timer
                self.playbackTimer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER,self.onTimer)
                #self.timer.Start(100)



                self.slider=wx.Slider(self,pos=(0,655),size=(1300,25),style = wx.SL_HORIZONTAL)
                #self.slider.SetRange(0,self.mplay.Length())
                #sliderSizer.Add(self.slider,1, wx.ALL|wx.EXPAND, 5)
                self.slider.Bind(wx.EVT_SLIDER, self.on_Seek)
                #self.slider.SetPageSize(5000)
                
                
                #mainSizer.Add(self.mplay,1,wx.ALL,5)
                self.mplay.GetBestSize()
                #self.SetSizer( mainSizer )

                
                self.Bind(wx.EVT_MENU,self.OnQuit,Mediafourth)
                self.Bind(wx.EVT_MENU,self.OnOpen,Mediafirst)
                self.Bind(wx.EVT_MENU,self.OnPlay,Playfirst)
                self.Bind(wx.EVT_MENU,self.OnPause,Playsecond)
                self.Bind(wx.EVT_MENU,self.OnStop,Playthird)
                self.Bind(wx.EVT_MENU,self.Onlisten,Spfirst)
                self.Bind(wx.EVT_MENU,self.Onclose,Spfirst)
                self.Bind(wx.EVT_MENU,self.Onvoice,Spthird)
                self.Bind(wx.EVT_MENU,self.SpeedChange,submenu1)
                self.Bind(wx.EVT_MENU,self.SpeedChange1,submenu2)
                self.Bind(wx.EVT_MENU,self.SpeedChange2,submenu3)
                self.Bind(wx.EVT_MENU,self.SpeedChange3,submenu4)
                self.Bind(wx.EVT_MENU,self.SpeedChange4,submenu5)
                self.Bind(wx.EVT_MENU,self.SpeedChange5,submenu6)
                self.Bind(wx.EVT_MENU,self.history_play1,Addsub)
                self.Bind(wx.EVT_MENU,self.history_play1,history2)
                self.Bind(wx.EVT_MENU,self.history_play1,history3)
                self.Bind(wx.EVT_MENU,self.history_play1,history4)
                self.Bind(wx.EVT_MENU,self.history_play1,history5)
                self.Show()

        def SpeedChange(self,evt):
                self.mplay.SetPlaybackRate(0.25)
                self.mplay.Play()

        def SpeedChange1(self,evt):
                self.mplay.SetPlaybackRate(0.50)
                self.mplay.Play()
        def SpeedChange2(self,evt):
                self.mplay.SetPlaybackRate(1.0)
                self.mplay.Play()
        def SpeedChange3(self,evt):
                self.mplay.SetPlaybackRate(1.25)
                self.mplay.Play()
        def SpeedChange4(self,evt):
                self.mplay.SetPlaybackRate(1.50)
                self.mplay.Play()
        def SpeedChange5(self,evt):
                self.mplay.SetPlaybackRate(2.0)
                self.mplay.Play()
                
        def OnQuit(self,evt):
                self.Close()
                self.Quit()

        def OnOpen(self,evt):
                dial=wx.FileDialog(self,"Choose a Media File",os.getcwd(),"","",wx.OPEN | wx.CHANGE_DIR)
                f=open("history.txt","a")
                if dial.ShowModal()== wx.ID_OK :
                        path=dial.GetPath()
                        print path
                        s1=""
                        l=len(path)
                        for i in range(0,l):
                        	if path[i]=='/':
                        		s1=""
                        	else :
                        		s1=s1+path[i]
                        f.write(path)
                        f.write("\n")
                        f.close()
                        if  self.mplay.Load(path):
                                folder, filen =os.path.split(path)   
                                #self.slider.SetRange(0,self.mplay.Length())
                                self.playbackTimer.Start(100)
                                self.mplay.Play()
                                self.slider.SetRange(0,self.mplay.Length())
                                self.button1.Show()
                                self.button.Hide()
                                #self.slider.SetRange(0,self.mplay.Length())
                #self.slider.SetRange(0,self.mplay.Length())             
                dial.Destroy() 
        
        def OnPlay(self,evt):
        		if self.flag==0:
        			speak=check_output(['espeak','Playing'])
        		self.mplay.Play()
        		self.slider.SetRange(0,self.mplay.Length())
        		self.button1.Show()
        		self.button.Hide()

        def OnPause(self,evt):
        		if self.flag==0:
        			speak=check_output(['espeak','Pausing'])
        		self.mplay.Pause()
        		self.slider.SetRange(0,self.mplay.Length())
        		self.button.Show()
        		self.button1.Hide()

        def OnStop(self,evt):
                self.mplay.Stop()
                self.button.Show()
                self.button1.Hide()
        def on_set_volume(self, event):
                self.currentVolume = self.volumeCtrl.GetValue()
                self.mplay.SetVolume((self.currentVolume)*.01)

        def on_mute(self,event):
        		self.f=self.volumeCtrl.GetValue()
        		self.mplay.SetVolume(0)

        def on_unmute(self,event):
        		self.mplay.SetVolume(self.f*.01)

        def Onlisten(self,evt):
    			if not self.worker:
      				self.worker = WorkerThread(self)
      				self.worker.start() 
      			elif self.worker:
      				self.worker.stop()
      				self.worker=None

        def Onclose(self,evt):
                print "hi"
                evt.Skip()


        def Onvoice(self,evt):
        		if self.flag==0:
        			self.flag=1
        		else:
        			self.flag=0


        def on_pause(self, event):
          if self.mplay.GetState()==wx.media.MEDIASTATE_PLAYING:
           if self.flag==0:	
           		speak=check_output(['espeak','Pausing']) 
           self.mplay.Pause()
           self.button.Show()
           self.button1.Hide()
          else:
          	if self.flag==0:
          		speak=check_output(['espeak','Playing'])
          	self.mplay.Play()
          	self.button.Hide()
          	self.button1.Show()
          	self.slider.SetRange(0,self.mplay.Length())

        def on_Seek(self, evt):
            offset=self.slider.GetValue()
            self.mplay.Seek(offset,0)


        def onTimer(self, evt):
            offset = self.mplay.Tell()
            self.slider.SetValue(offset)
            secsPlayed = time.strftime('%H:%M:%S', time.gmtime(offset*.001))
            self.trackCounter.SetLabel(secsPlayed)

        def on_forward(self,evt):
        	if self.flag==0:
        		speak=check_output(['espeak','Forwarding']) 
        	temp=self.mplay.Tell()
        	temp=temp+5000
        	if temp>self.mplay.Length():
        		temp=self.mplay.Length()
        	self.mplay.Seek(temp,0)

        def on_backward(self,evt):
        	if self.flag==0:
        		speak=check_output(['espeak','Backwarding']) 
        	temp=self.mplay.Tell()
        	temp=temp-5000
        	if temp<0:
        		temp=0
        	self.mplay.Seek(temp,0)

        def history_play1(self,evt):
        	f=open("history.txt","r")
        	s3=""
        	s3=f.readline()
        	while s3 != "":
        		s2=""
        		for i in range(0,len(s3)):
        			if s3[i]=="/":
        				s2=""
        			else:
        				s2+=s3[i]
        		if s2==self.s1:
        			print s2
        			if self.mplay.Load(s3):
        				print "fjfgj"
        				self.playbackTimer.Start(100)
                        self.mplay.Play()
                        #self.slider.SetRange(0,self.mplay.Length())
                        self.button1.Show()
                        self.button.Hide()
                        self.slider.SetRange(0,self.mplay.Length())
        		s3=f.readline()
        	f.close()					
        def _new_(self):
        	return self
#Thread for specch


class WorkerThread(threading.Thread):
  def __init__(self, notify_window):
    threading.Thread.__init__(self)
    self.counter = 0
    self._notify_window = notify_window
    self.abort = False 

  def run(self):
    while not self.abort:
    	new=None
    	r = sr.Recognizer()
        with sr.Microphone() as source:
        	print("Say something!")
        	audio = r.listen(source)
        try:
            e=0
            s=r.recognize_google(audio)
            print s
            if s=="hello media player":
            	if frame.flag==0:
            		speak=check_output(['espeak','hello how are you please tell me what can i do for you'])
            elif s=="play" or s=="play the audio" or s=="play the video":
            	if frame.flag==0:
                	speak=check_output(['espeak','Playing'])
                frame.mplay.Play()
            elif s=="stop" or s=="stock" or s=="top" or s=="stop the video" or s=="stop the audio" or s=="top the video":
            	if frame.flag==0:
                	speak=check_output(['espeak','Pausing'])
                frame.mplay.Pause()
            elif s=="open the media file" or s=="open" or s=="open the media" or s=="open a media file" or s=="open the mediafire":
                frame.OnOpen(e)
            elif s=="close the app":
            	if flag==0:
            		speak=check_output(['espeak','Good Bye see you again'])
                frame.OnQuit(e)
            elif s=="disable the sound":
            	frame.on_mute(e)
            elif s=="enable the sound":
            	frame.on_unmute(e)
            elif s=="increase the volume":
                frame.on_set_volume(e)
            elif s=="forward the video" or s=="forward the audio":
                frame.on_forward(e)
            elif s=="backward the video" or s=="backward the audio":
                frame.on_backward(e)
            elif s=="recommend me" or s=="remind me":
            	speak=check_output(['espeak',"what's on your mood"])
            	r1=sr.Recognizer()
            	with sr.Microphone() as source: 
            		audio2 = r1.listen(source)
            	s2=r1.recognize_google(audio2)
            	url="https://www.youtube.com/results?search_query=Most Popular "+s2
                webbrowser.open(url,new=new);
            else :
            	if frame.flag==0:
                	speak=check_output(['espeak','please try again']) 


        except sr.UnknownValueError:
            #speak=check_output(['espeak','Please try again']) 
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            #speak=check_output(['espeak','Please try again']) 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    	wx.PostEvent(self._notify_window, DataEvent(self.counter))
      	time.sleep(1)

  def stop(self):
      self.abort = True


if __name__ == "__main__":
	flag=0
	app=wx.App()
	frame=Main(None,"Interactive Media Player")
	app.MainLoop()
