# vedio link-- https://www.youtube.com/watch?v=B1N3JkzmptU
import os
import wx
import wx.lib.dialogs
import wx.stc as stc

faces={ 'times':"Times New Roman",
	'mono':"Courier New",
	'helv':"Arial",
	'other':"Comic Sans MS",
	'size':10,
	'size2':8,}
class MainWindow(wx.Frame):
	
	def __init__(self,parent,title):
		self.leftMarginWidth=25
		self.dirname=''
		self.filename=''		
		self.linenumberenabled=True

		wx.Frame.__init__(self, parent, title=title, size=(800, 600))
		self.control=stc.StyledTextCtrl(self,style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
		self.control.CmdKeyAssign(ord('='),stc.STC_SCMOD_CTRL,stc.STC_CMD_ZOOMIN)
		self.control.CmdKeyAssign(ord('-'),stc.STC_SCMOD_CTRL,stc.STC_CMD_ZOOMOUT)
		
		self.control.SetViewWhiteSpace(False)
		self.control.SetMargins(5,0)
		self.control.SetMarginType(1,stc.STC_MARGIN_NUMBER)
		self.control.SetMarginWidth(1,self.leftMarginWidth)

		self.CreateStatusBar()
		self.StatusBar.SetBackgroundColour((220,220,220))

		filemenu=wx.Menu()
		menuNew=filemenu.Append(wx.ID_NEW,"&New","Create a new Document")
		menuOpen=filemenu.Append(wx.ID_OPEN,"&Open","Open an existing Document")
		menuSave=filemenu.Append(wx.ID_SAVE,"&Save","Save the current Document")
		menuSaveAs=filemenu.Append(wx.ID_SAVEAS,"&Save &As","Save a new Dcument")
		filemenu.AppendSeparator()
		menuClose=filemenu.Append(wx.ID_EXIT,"&Close","Close the application")
		editmenu=wx.Menu()
		menuundo=editmenu.Append(wx.ID_UNDO,"&Undo","Undo last action")
		menuredo=editmenu.Append(wx.ID_REDO,"&Redo","Redo last action")
		editmenu.AppendSeparator()
		menuSelectAll=editmenu.Append(wx.ID_SELECTALL,"&Select All","Select the entire Document")
		menucopy=editmenu.Append(wx.ID_COPY,"&Copy","Copy selected Text")
		menucut=editmenu.Append(wx.ID_CUT,"&CUT","Cut selected text")
		menupaste=editmenu.Append(wx.ID_PASTE,"&Paste","Paste text from cliborad")
		prefmenu=wx.Menu()
		menuLineNumbers=prefmenu.Append(wx.ID_ANY,"Toggle &Line Number","Show/Hide line numbers column")
		
		helpmenu=wx.Menu()
		menuHowTo=helpmenu.Append(wx.ID_ANY,"&How To...","Get help using the editor")
		helpmenu.AppendSeparator()
		menuAbout=helpmenu.Append(wx.ID_ABOUT,"&About","Read about the editor and its making")
		
		menuBar=wx.MenuBar()
		menuBar.Append(filemenu,"&File")
		menuBar.Append(editmenu,"&Edit")
		menuBar.Append(prefmenu,"&Preferences")
		menuBar.Append(helpmenu,"&Help")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU,self.OnNew,menuNew)
		self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
		self.Bind(wx.EVT_MENU,self.OnSave,menuSave)
		self.Bind(wx.EVT_MENU,self.OnSaveAs,menuSaveAs)
		self.Bind(wx.EVT_MENU,self.OnClose,menuClose)

		self.Bind(wx.EVT_MENU,self.OnUndo,menuundo)
		self.Bind(wx.EVT_MENU,self.OnRedo,menuredo)
		self.Bind(wx.EVT_MENU,self.OnSelectAll,menuSelectAll)
		self.Bind(wx.EVT_MENU,self.OnCopy,menucopy)
		self.Bind(wx.EVT_MENU,self.Oncut,menucut)
		self.Bind(wx.EVT_MENU,self.OnPaste,menupaste)

		self.Bind(wx.EVT_MENU,self.OntoggleLineNumber,menuLineNumbers)
		
		self.Bind(wx.EVT_MENU,self.OnHowTo,menuHowTo)

		self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)
	
		self.control.Bind(wx.EVT_KEY_UP,self.UpdateLineCol)
		self.control.Bind(wx.EVT_CHAR,self.OnCharEvent)
		self.Show()
		self.UpdateLineCol(self)

	def OnNew(self,e):
		self.filename=''
		self.control.SetValue("")
		
	def OnOpen(self,e):
		try:
			dlg=wx.FileDialog(self,"Choose a file",self.dirname,"","*.*",wx.FD_OPEN)
			if(dlg.ShowModal()==wx.ID_OK):
				self.filename=dlg.GetFilename()
				self.dirname=dlg.GetDirectory()
				f=open(os.path.join(self.dirname,self.filename),'r')
				self.control.SetValue(f.read())
				f.close()
			dlg.Destroy()
		except:
			dlg=wx.MessageDialog(self,"Coudtn't open the file","Error",wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()

	def OnSave(self,e):
		try:
			f=open(os.path.join(self.dirname,self.filename),'w')
			f.write(self.control.SetValue())
			f.close()
		except:
			try:
				dlg=wx.FileDialog(self,"Save file as",self.dirname,"Untitled","*.*",wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
				if(dlg.ShowModal()==wx.ID_OK):
					self.filename=dlg.GetFilename()
					self.dirname=dlg.GetDirectory()
					f=open(os.path.join(self.dirname,self.filename),'w')
					f.write(self.control.GetValue())
					f.close()
				dlg.Destroy()
			except:
				pass
	def OnSaveAs(self,e):
		try:
			dlg=wx.FileDialog(self,"Save file as",self.dirname,"Untitled","*.*",wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			if(dlg.ShowModal()==wx.ID_OK):
				self.filename=dlg.GetFilename()
				self.dirname=dlg.GetDirectory()
				f=open(os.path.join(self.dirname,self.filename),'w')
				f.write(self.control.GetValue())
				f.close()
			dlg.Destroy()
		except:
			pass

	def OnClose(self,e):
		self.Close(True)
	def OnUndo(self,e):
		self.control.Undo()
	def OnRedo(self,e):
		self.control.Redo()
	def OnSelectAll(self,e):
		self.control.SelectAll()
	def OnCopy(self,e):
		self.control.Copy()
	def Oncut(self,e):
		self.control.Cut()
	def OnPaste(self,e):
		self.control.Paste()
	def OntoggleLineNumber(self,e):
		if self.linenumberenabled:
			self.control.SetMarginWidth(1,0)
			self.linenumberenabled=False
		else:
			self.control.SetMarginWidth(1,self.leftMarginWidth)
			self.linenumberenabled=True
	def OnHowTo(self,e):
		dlg=wx.lib.dialogs.ScrolledMessageDialog(self,"This is how to .","How To",size=(400,400))
		dlg.ShowModal()
		dlg.Destroy()
	def OnAbout(self,e):
		dlg=wx.MessageDialog(self,"My advanced text Editor with python and wx","About",wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
				
	def UpdateLineCol(self,e):
		line=self.control.GetCurrentLine()+1
		col=self.control.GetColumn(self.control.GetCurrentPos())
		stat="Line %s,Column %s" % (line,col)
		self.StatusBar.SetStatusText(stat,0)
	def OnCharEvent(self,e):
		keycode=e.GetKeyCode()
		altdown=e.AltDown()
		if(keycode==14):
			self.OnNew(self)#ctrl+N
		elif(keycode==15):
			self.OnOpen(self)#ctrl+O		
		elif(keycode==19):
			self.OnSave(self)#ctrl+S
		elif(altdown and keycode==115):
			self.OnSaveAs(self)#Alt+S
		elif(keycode==23):
			self.OnClose(self)#ctrl+W
		elif keycode==340:
			self.OnHowTo(self)#F1
		elif keycode==341:
			self.OnAbout(self)#F2
		else:
			e.Skip()
app=wx.App()
frame=MainWindow(None,"Pythor")
app.MainLoop()
