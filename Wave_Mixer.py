#!/usr/bin/env python
import wave
import struct
import gtk
import pyaudio
from sys import byteorder
from array import array
import os
import sys
import signal

files=['','','']
modified_files=['1.wav','2.wav','3.wav']


class mixer:

    def __init__(self):

        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL) 
        self.window.set_position(gtk.WIN_POS_CENTER) 
        self.window.set_size_request(750,650) 
        self.window.set_title("Wave Mixer") 
        self.window.connect("destroy", lambda w: gtk.main_quit())

        
        self.play1=0
        self.play2=0
        self.play3=0
    

        self.pid1=0
        self.pid2=0
        self.pid3=0
        self.pid4=0
        self.pid5=0
        self.pid6=0

        
        self.fixed=gtk.Fixed() 
        self.window.add(self.fixed) 
        self.fixed.show()



        self.filechooserbutton11= gtk.FileChooserButton("Wave1", None)
        self.filechooserbutton11.set_size_request(150,40)
        fil = gtk.FileFilter()
        fil.add_pattern("*.wav")
        self.filechooserbutton11.add_filter(fil)
        self.fixed.put(self.filechooserbutton11,40,50)
        self.filechooserbutton11.connect("file-set",self.get_file,1)

        self.lable1=gtk.Label("Amplitude")
        self.fixed.put(self.lable1,40,120)

        self.scale=gtk.HScale() 
        self.scale.set_range(0,5) 
        self.scale.set_increments(0.1, 1) 
        self.scale.set_digits(1) 
        self.scale.set_value(1) 
        self.scale.set_size_request(160, 45) 
        self.fixed.put(self.scale,40,140)
     
        self.lable2=gtk.Label("Time Shift")
        self.fixed.put(self.lable2,40,200)

        self.scale2=gtk.HScale() 
        self.scale2.set_range(-1,1) 
        self.scale2.set_increments(0.1, 1) 
        self.scale2.set_digits(1) 
        self.scale2.set_size_request(160, 45) 
        self.fixed.put(self.scale2,40,220)

        self.lable3=gtk.Label("Time Scaling")
        self.fixed.put(self.lable3,40,280)

        self.scale3=gtk.HScale() 
        self.scale3.set_range(0,10) 
        self.scale3.set_increments(0.125, 1) 
        self.scale3.set_digits(3) 
        self.scale3.set_size_request(160, 45) 
        self.fixed.put(self.scale3,40,300)

        self.check1=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check1,40,370)
        self.l1=gtk.Label("Time Reversal")
        self.fixed.put(self.l1,70,372)

        self.check2=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check2,40,400)
        self.l2=gtk.Label("Select for Modulation")
        self.fixed.put(self.l2,70,402)

        self.check3=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check3,40,430)
        self.l3=gtk.Label("Select for Mixing")
        self.fixed.put(self.l3,70,432)


        self.progressbar1=gtk.ProgressBar(adjustment=None)
        self.fixed.put(self.progressbar1,60,480)

        self.button11=gtk.Button("Play") 
        self.button11.connect("clicked",self.play,1)
        self.fixed.put(self.button11,50,510)


        self.button12=gtk.Button("Pause") 
        self.button12.connect("clicked",self.pause,1)
        self.fixed.put(self.button12,110,510)

        self.button20=gtk.Button("Stop") 
        self.button20.connect("clicked",self.stop,1)
        self.fixed.put(self.button20,180,510)

        self.text=gtk.Entry(12)
        self.fixed.put(self.text,60,565)

        self.text=gtk.HScale() 
        self.text.set_range(0,30) 
        self.text.set_increments(0.5, 1) 
        self.text.set_digits(1) 
        self.text.set_size_request(160, 45) 
        self.fixed.put(self.text,80,555)

        self.inp=gtk.Label("Time")
        self.fixed.put(self.inp,30,570)


        self.window.show()
        self.filechooserbutton11.show()
        self.scale.show()
        self.lable1.show()
        self.scale2.show()
        self.lable2.show()
        self.scale3.show()
        self.lable3.show()
        self.check1.show()
        self.l1.show()
        self.check2.show()
        self.l2.show()
        self.check3.show()
        self.l3.show()
        self.progressbar1.show()
        self.button11.show()
        self.button12.show()
        self.button20.show()
        self.text.show()
        self.inp.show()



        self.filechooserbutton22= gtk.FileChooserButton("Wave2", None)
        self.filechooserbutton22.set_size_request(150,40)
        self.filechooserbutton22.add_filter(fil)
        self.fixed.put(self.filechooserbutton22,280,50)
        self.filechooserbutton22.connect("file-set",self.get_file,2)

        self.lable21=gtk.Label("Amplitude")
        self.fixed.put(self.lable21,280,120)

        self.scale21=gtk.HScale() 
        self.scale21.set_range(0,5) 
        self.scale21.set_increments(0.1, 1) 
        self.scale21.set_digits(1) 
        self.scale21.set_value(1) 
        self.scale21.set_size_request(160, 45) 
        self.fixed.put(self.scale21,280,140)
     

        self.lable22=gtk.Label("Time Shift")
        self.fixed.put(self.lable22,280,200)

        self.scale22=gtk.HScale() 
        self.scale22.set_range(-1,1) 
        self.scale22.set_increments(0.1, 1) 
        self.scale22.set_digits(1) 
        self.scale22.set_size_request(160, 45) 
        self.fixed.put(self.scale22,280,220)

        self.lable23=gtk.Label("Time Scaling")
        self.fixed.put(self.lable23,280,280)

        self.scale23=gtk.HScale() 
        self.scale23.set_range(0,10) 
        self.scale23.set_increments(0.125, 1) 
        self.scale23.set_digits(3) 
        self.scale23.set_size_request(160, 45) 
        self.fixed.put(self.scale23,280,300)

        self.check21=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check21,280,370)
        self.l21=gtk.Label("Time Reversal")
        self.fixed.put(self.l21,310,372)

        self.check22=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check22,280,400)
        self.l22=gtk.Label("Select for Modulation")
        self.fixed.put(self.l22,310,402)

        self.check23=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check23,280,430)
        self.l23=gtk.Label("Select for Mixing")
        self.fixed.put(self.l23,310,432)

        self.progressbar2=gtk.ProgressBar(adjustment=None)
        self.fixed.put(self.progressbar2,300,480)

        self.button21=gtk.Button("Play") 
        self.button21.connect("clicked",self.play,2)
        self.fixed.put(self.button21,290,510)

        self.button22=gtk.Button("Pause") 
        self.button22.connect("clicked",self.pause,2)
        self.fixed.put(self.button22,350,510)

        self.button30=gtk.Button("Stop") 
        self.button30.connect("clicked",self.stop,2)
        self.fixed.put(self.button30,420,510)


        self.filechooserbutton22.show()
        self.scale21.show()
        self.lable21.show()
        self.scale22.show()
        self.lable22.show()
        self.scale23.show()
        self.lable23.show()
        self.check21.show()
        self.l21.show()
        self.check22.show()
        self.l22.show()
        self.check23.show()
        self.l23.show()
        self.progressbar2.show()
        self.button21.show()
        self.button22.show()
        self.button30.show()


        self.filechooserbutton33= gtk.FileChooserButton("Wave3", None)
        self.filechooserbutton33.set_size_request(150,40)
        self.filechooserbutton33.add_filter(fil)
        self.fixed.put(self.filechooserbutton33,520,50)
        self.filechooserbutton33.connect("file-set",self.get_file,3)

        self.lable31=gtk.Label("Amplitude")
        self.fixed.put(self.lable31,520,120)

        self.scale31=gtk.HScale() 
        self.scale31.set_range(0,5) 
        self.scale31.set_increments(0.1, 1) 
        self.scale31.set_digits(1) 
        self.scale31.set_value(1) 
        self.scale31.set_size_request(160, 45) 
        self.fixed.put(self.scale31,520,140)
        
        self.lable32=gtk.Label("Time Shift")
        self.fixed.put(self.lable32,520,200)

        self.scale32=gtk.HScale() 
        self.scale32.set_range(-1,1) 
        self.scale32.set_increments(0.1, 1) 
        self.scale32.set_digits(1) 
        self.scale32.set_size_request(160, 45) 
        self.fixed.put(self.scale32,520,220)

        self.lable33=gtk.Label("Time Scaling")
        self.fixed.put(self.lable33,520,280)

        self.scale33=gtk.HScale() 
        self.scale33.set_range(0,10) 
        self.scale33.set_increments(0.125, 1) 
        self.scale33.set_digits(3) 
        self.scale33.set_size_request(160, 45) 
        self.fixed.put(self.scale33,520,300)

        self.check31=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check31,520,370)
        self.l31=gtk.Label("Time Reversal")
        self.fixed.put(self.l31,550,372)

        self.check32=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check32,520,400)
        self.l32=gtk.Label("Select for Modulation")
        self.fixed.put(self.l32,552,402)

        self.check33=gtk.CheckButton(label=None, use_underline=True)
        self.fixed.put(self.check33,520,430)
        self.l33=gtk.Label("Select for Mixing")
        self.fixed.put(self.l33,550,432)

        self.progressbar3=gtk.ProgressBar(adjustment=None)
        self.fixed.put(self.progressbar3,540,480)

        self.button31=gtk.Button("Play") 
        self.button31.connect("clicked",self.play,3)
        self.fixed.put(self.button31,530,510)

        self.button32=gtk.Button("Pause") 
        self.button32.connect("clicked",self.pause,3)
        self.fixed.put(self.button32,590,510)

        self.button40=gtk.Button("Stop") 
        self.button40.connect("clicked",self.stop,3)
        self.fixed.put(self.button40,660,510)


        self.filechooserbutton33.show()
        self.scale31.show()
        self.lable31.show()
        self.scale32.show()
        self.lable32.show()
        self.scale33.show()
        self.lable33.show()
        self.check31.show()
        self.l31.show()
        self.check32.show()
        self.l32.show()
        self.check33.show()
        self.l33.show() 
        self.progressbar3.show()
        self.button31.show()
        self.button32.show()
        self.button40.show()



        self.progressbar4=gtk.ProgressBar(adjustment=None)
        self.fixed.put(self.progressbar4,305,580)
        self.button4=gtk.Button("Modulate and Play") 
        self.button4.connect("clicked",self.do_modulate)
        self.fixed.put(self.button4,310,605)
       

        self.progressbar5=gtk.ProgressBar(adjustment=None)
        self.fixed.put(self.progressbar5,540,580)
        self.button5=gtk.Button("Mix and Play") 
        self.button5.connect("clicked",self.do_mix)
        self.fixed.put(self.button5,570,605)
        

        self.button6=gtk.Button("Record") 
        self.button6.connect("clicked",self.record_it)
        self.fixed.put(self.button6,130,605)

        self.button7=gtk.Button("Play") 
        self.button7.connect("clicked",self.play_myrec)
        self.fixed.put(self.button7,200,605)


        self.progressbar4.show()
        self.progressbar5.show()
        self.button4.show()
        self.button5.show()
        self.button6.show()
       
        

    def get_file(self,widget,value):
        if value==1:
            files[0]=widget.get_filename()
        if value==2:
            files[1]=widget.get_filename()
        if value==3:
            files[2]=widget.get_filename()

    
    def destroy(self,widget,data=None):
        gtk.main_quit()

    def do_modulate(self,widget,data=None):
    	x=self.check2.get_active()
    	y=self.check22.get_active()
    	z=self.check32.get_active()

    	if x==True or y==True or z==True:
	    	m=9999999999
	    	final=[]

	    	if x==True:
	    		self.change(self,1)
	    		wav = wave.open (modified_files[0], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out1 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=min(m,len(out1))
		
	    	if y==True:
	    		self.change(self,2)
	    		wav = wave.open (modified_files[1], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out2 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=min(m,len(out2))

			
	    	if z==True:
	    		self.change(self,3)
	    		wav = wave.open (modified_files[2], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out3 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=min(m,len(out3))

		

		for i in xrange(m):
			val=1
			if x==True:
				if i<len(out1):
					val*=out1[i]
			if y==True:
				if i<len(out2):
					val*=out2[i]
			if z==True:
				if i<len(out3):
					val*=out3[i]
			if val>32767:
				val=32767
			if val<-32767:
				val=-32767
			final.append(val)


		output = struct.pack("%ih" % len(final), *final)
		wav1 = wave.open("modulated_file.wav", "wb")
		nf=len(final)/nchannels	
		wav1.setparams((nchannels, sampwidth, framerate, nf, comptype, compname))

		wav1.writeframesraw(output)	
		wav1.close()

            
                self.pid5=os.fork()
                if self.pid5==0:
                    		CHUNK=1024
                    	    	wf=wave.open("modulated_file.wav",'rb')
                    	      	p=pyaudio.PyAudio()
                    	        
                    		stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

                    		data = wf.readframes(CHUNK)

                    		while data != '':
                    		   	stream.write(data)
                    	    		data = wf.readframes(CHUNK)

                    		stream.stop_stream()
                    		stream.close()
                    		p.terminate()
                            	exit(0)

    def do_mix(self,widget,data=None):
    	x=self.check3.get_active()
    	y=self.check23.get_active()
    	z=self.check33.get_active()

    	if x==True or y==True or z==True:
	    	m=0
	    	final=[]

	    	if x==True:
	    		self.change(self,1)
	    		wav = wave.open (modified_files[0], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out1 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=max(m,len(out1))
			
	    	if y==True:
	    		self.change(self,2)
	    		wav = wave.open (modified_files[1], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out2 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=max(m,len(out2))

	    	if z==True:
	    		self.change(self,3)
	    		wav = wave.open (modified_files[2], "rb")
			(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
			frames = wav.readframes (nframes * nchannels)
			out3 = struct.unpack("%ih" % nframes * nchannels, frames)
			m=max(m,len(out3))

		

		for i in xrange(m):
			val=0
			if x==True:
				if i<len(out1):
					val+=out1[i]
			if y==True:
				if i<len(out2):
					val+=out2[i]
			if z==True:
				if i<len(out3):
					val+=out3[i]
			if val>32767:
				val=32767
			if val<-32767:
				val=-32767
			final.append(val)

		
		output = struct.pack("%ih" % len(final), *final)
		wav1 = wave.open("mixed_file.wav", "wb")
		nf=len(final)/nchannels	
		wav1.setparams((nchannels, sampwidth, framerate, nf, comptype, compname))

		wav1.writeframes(output)	
		wav1.close()

                self.pid4=os.fork()
                if self.pid4==0:
                              
                
                        CHUNK=1024
                        wtf=wave.open("mixed_file.wav",'rb')
                        p=pyaudio.PyAudio()
                        
                        stream=p.open(format=p.get_format_from_width(wtf.getsampwidth()),channels=wtf.getnchannels(),rate=wtf.getframerate(),output=True)

                        data = wtf.readframes(CHUNK)

                        while data != '':
                                stream.write(data)
                                data = wtf.readframes(CHUNK)

                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        exit(0)
                
                            
        	


    def play(self,widget,value):
        if value==1:
            if self.play1==2:
                os.kill(self.pid1,signal.SIGCONT)
                self.play1=1
            else:
                self.pid1=os.fork()
                if self.pid1==0:
                   	 self.play1=1
                 	 CHUNK=1024
            	      	 self.change(self,value)
            	      	 wf=wave.open(modified_files[0],'rb')
            	    
            		 p=pyaudio.PyAudio()
            	        
            		 stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

            		 data = wf.readframes(CHUNK)

            		 while data != '':
            	    		stream.write(data)
            	  		data = wf.readframes(CHUNK)

            		 stream.stop_stream()
            		 stream.close()
            		 p.terminate()
                     	 exit(0)

        if value==2:
            if self.play2==2:
                os.kill(self.pid2,signal.SIGCONT)
                self.play2=1
            else:
                self.pid2=os.fork()
                if self.pid2==0:
                     self.play2=1
                     CHUNK=1024
                     self.change(self,value)
                     wf=wave.open(modified_files[value-1],'rb')
                    
                     p=pyaudio.PyAudio()
                        
                     stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

                     data = wf.readframes(CHUNK)

                     while data != '':
                            stream.write(data)
                       	    data = wf.readframes(CHUNK)

                     stream.stop_stream()
                     stream.close()
                     p.terminate()
                     exit(0)

        if value==3:
            if self.play3==2:
                os.kill(self.pid3,signal.SIGCONT)
                self.play3=1
            else:
                self.pid3=os.fork()
                if self.pid3==0:
                     self.play3=1
                     CHUNK=1024
                     self.change(self,value)
                     wf=wave.open(modified_files[value-1],'rb')
                    
                     p=pyaudio.PyAudio()
                        
                     stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

                     data = wf.readframes(CHUNK)

                     while data != '':
                            stream.write(data)
                            data = wf.readframes(CHUNK)

                     stream.stop_stream()
                     stream.close()
                     p.terminate()
                     exit(0)

       
        

    def play_myrec(self,widget):
                pid6=os.fork()
                if pid6==0:
                    CHUNK=1024
                    
                    wtf=wave.open('rec.wav','rb')
                        
                    pp=pyaudio.PyAudio()
                            
                    stream=pp.open(format=pp.get_format_from_width(wtf.getsampwidth()),channels=wtf.getnchannels(),rate=wtf.getframerate(),output=True)

                    data = wtf.readframes(CHUNK)

                    while data != '':
                            stream.write(data)
                            data = wtf.readframes(CHUNK)

                    stream.stop_stream()
                    stream.close()
                    pp.terminate()
                    exit(0)

    def pause(self,widget,value):
        if value==1:
            os.kill(self.pid1,signal.SIGSTOP)
            self.play1=2

        if value==2:
            os.kill(self.pid2,signal.SIGSTOP)
            self.play2=2

        if value==3:
            os.kill(self.pid3,signal.SIGSTOP)
            self.play3=2

    def stop(self,widget,value):
        if value==1:
            os.kill(self.pid1,9)

        if value==2:
            os.kill(self.pid2,9)

        if value==3:
            os.kill(self.pid3,9)

    
    def change(self,widget,value):
    	path=files[value-1]
    	if len(path)!=0:
	    	if value==1:
	    		x=self.scale.get_value()
	    		y=self.scale2.get_value()
	    		z=self.scale3.get_value()
	    		w=self.check1.get_active()
	    	if value==2:
	    		x=self.scale21.get_value()
	    		y=self.scale22.get_value()
	    		z=self.scale23.get_value()
	    		w=self.check21.get_active()
	    	if value==3:
	    		x=self.scale31.get_value()
	    		y=self.scale32.get_value()
	    		z=self.scale33.get_value()
	    		w=self.check31.get_active()
		
	    	wav = wave.open (path, "rb")
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
		frames = wav.readframes (nframes * nchannels)

		if sampwidth==1:
			fmt="%iB" % nframes*nchannels
		else:
			fmt="%ih" % nframes*nchannels

		out = struct.unpack(fmt, frames)
		nf=nframes
		a=[]
		if x>0:
			for i in xrange(len(out)):
				if out[i]*x>32767:
					a.append(32767)
				elif out[i]*x<-32767:
					a.append(-32767)
				else:
					a.append(out[i]*x)
		else:
			for i in xrange(len(out)):
				a.append(out[i])

		print int(int(y)*nchannels*framerate)
		print int(y*nchannels*framerate)
	

		b=[]
		if y!=0:
			if y>0:
				for i in xrange(int(y*nchannels*framerate)):
					b.append(0)
				for i in xrange(len(out)):
					b.append(out[i])
			else:
				y=abs(y)
				for i in xrange(int(y*nchannels*framerate),len(out)):
					b.append(out[i])
			nf=len(b)/nchannels
		else:
			for i in xrange(len(a)):
				b.append(a[i])

		c=[]
		if w==True:
			c=b[::-1]
		else:
			for i in xrange(len(b)):
				c.append(b[i])

		d=[]
		new_odd=[]
		new_even=[]
		if z!=0:
			if nchannels==1:
				i=0
				N=len(c)
				while i*z<N:
					d.append(c[int(i*z)])
					i+=1
			else:
				for i in xrange(len(c)):
					if i%2==0:
						new_even.append(c[i])
					else:
						new_odd.append(c[i])
				N=len(new_odd)
				i=0
				while i*z<N:
					d.append(new_even[int(i*z)])
					d.append(new_odd[int(i*z)])
					i+=1
		else:
			for i in xrange(len(c)):
				d.append(c[i]);
			
		
		if sampwidth==1:
			fmt="%iB" % len(d)
		else:
			fmt="%ih" % len(d)

		output = struct.pack(fmt, *d)
		wav1 = wave.open(modified_files[value-1], "wb")
		wav1.setparams((nchannels, sampwidth, framerate, nf, comptype, compname))

		wav1.writeframesraw(output)
		wav1.close()

    def do_record(self,widget):
	myobject=rec()
        myobject.record_to_file('demo.wav')
        print "done"

    def record_it(self,widget):
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS =float(self.text.get_value())
            
            if sys.platform == 'darwin':
                CHANNELS = 1

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

            print("* recording")

            frames = []
            x=int(RATE / CHUNK * RECORD_SECONDS)

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            #   self.pgbar_2.set_fraction(i*1.0/x)
                data = stream.read(CHUNK)
                frames.append(data)

            print("* done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open('rec.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    def file_selected(self, widget):
        print "Selected filepath: %s" % widget.get_filename()

mixer()
gtk.main()
