#vedio link-https://www.youtube.com/watch?v=SeJKd98WdR0

from Tkinter import Tk,StringVar,Entry
from Tkinter import Button

class calc:
	
	def __init__(self):
		self.error=False
		window=Tk()
		window.title("Python Calculator")
		window.configure(background='yellow')
		self.string=StringVar()
		entry=Entry(window,textvariable=self.string,font="Helvetica 17 bold")
		entry.grid(row=0,column=0,columnspan=6)
		entry.bind('<KeyPress>',self.keyPress)
		entry.focus()

		values=["7","8","9","/","clear","<-","4","5","6","*","(",")","1","2","3","-","=","0",".","%","+"]
		row=1
		col=0
		i=0
		for txt in values:
			px=10
			py=10

			if(i==6):
				row=2
				col=0
			if(i==12):
				row=3
				col=0
			if(i==17):
				row=4
				col=0
						
			if(txt=="="):
				btn=Button(window,height=2,width=4,padx=23,pady=23,text=txt,command=lambda txt=txt:self.equals())
				btn.grid(row=row,column=col,columnspan=2,rowspan=2,padx=1,pady=1)
			elif(txt=="clear"):
				btn=Button(window,height=1,width=2,padx=px,pady=py,text=txt,command=lambda txt=txt:self.cleartxt())
				btn.grid(row=row,column=col,padx=1,pady=1)
			elif(txt=="<-"):
				btn=Button(window,height=1,width=2,padx=px,pady=py,text=txt,command=lambda txt=txt:self.delete())
				btn.grid(row=row,column=col,padx=1,pady=1)
			else:
				btn=Button(window,height=1,width=2,padx=px,pady=py,text=txt,command=lambda txt=txt:self.addchar(txt))
				btn.grid(row=row,column=col,padx=1,pady=1)

			
			col+=1
			i+=1
		window.mainloop()
	def keyPress(self,event):
		
		allowedvalues=["KP_0","KP_1","KP_2","KP_3","KP_4","KP_5","KP_6","KP_7","KP_8","KP_9","7","8","9","KP_Divide","slash","4","5","6","KP_Multiply","parenleft","parenright","1","2","3","KP_Subtract","minus","equal","0","period","percent","KP_Add","plus","BackSpace","asterick","Right","Left","KP_Decimal"]

		if not self.error:

			if event.keysym in ("Return","KP_Enter"):
				self.equals()
			elif event.keysym not in allowedvalues:
				return 'break'
		else:
			return 'break'

	def cleartxt(self):
		
		self.string.set("")
		self.error=False
	def equals(self):
		result=""
		try:
			result=eval(self.string.get())
			
		except:
			self.error=True
			result="ERROR"
		self.string.set(result)

	def addchar(self,char):
		if not self.error:
			self.string.set(self.string.get()+(str(char)))
	

	def delete(self):
		if not self.error:
			self.string.set(self.string.get()[0:-1])


calc()

