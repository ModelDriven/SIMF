#
# Python script (Macro) to be run inside of Magicdraw to MOFize a conceptual model.
# - camelCase all names
# - removed un-named associations (SIMF Restructons)
# - add nested package URIs
# - Replace term "Conceptual" with "MOF"
#
# Changes are logged as it modified the model in place.
#
# Put in a Magicdraw python macro.
#
#
from java.io import File
from java.lang import Integer
from java.lang import System

from com.nomagic.magicdraw.core import Application
from com.nomagic.magicdraw.core import Project
from com.nomagic.magicdraw.core.project import ProjectsManager
from com.nomagic.magicdraw.core.project import ProjectDescriptorsFactory

from com.nomagic.magicdraw.uml import BaseElement
from com.nomagic.uml2.ext.jmi.helpers import StereotypesHelper
import sys
import string

def log(something): 
	Application.getInstance().getGUILog().log(str(something))
	
#import com.nomagic.uml2
#import com.nomagic.magicdraw.openapi.uml
import com.nomagic.magicdraw.openapi.uml

#global array
deleteme = []

	
	
def doUML(uml, level):


	#log ("Check association1 "+str(level))	

	#log(uml)
	try :
		ends = uml.getMemberEnd()
		# Only get here is association
		for end in ends:
			try :
				log("TRY End: "+end.getName())
				opposite = end.getOpposite()
				log("Opposite="+opposite.getName())
				domain = opposite.getType()
				log("Set end to: "+domain.getName())
				end.setOwner(domain)
				log("CHANGED END: "+end.getName())
			except :
				dontcare = True
	except :
		dontcare = True
		
	
	#iterate thru the model	
	if (uml.hasOwnedElement()):
		# Visit all children
		for e in uml.getOwnedElement().iterator():	
			if e.isEditable() : ## Only visit placed we can edit
				doUML(e, level+1) # Visit editable elements	
				
	return 1

project = Application.getInstance().getProject()
model = project.getModel()
log("Make owned ends="+model.getName())
com.nomagic.magicdraw.openapi.uml.SessionManager.getInstance().createSession("MOFize model")
#log("-------- created session-----------")


try :
	doUML(model, 0)


finally :
	com.nomagic.magicdraw.openapi.uml.SessionManager.getInstance().closeSession()
#log("-------- closes session-----------")