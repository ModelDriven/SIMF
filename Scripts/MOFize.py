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
	name = None
	fixedname = ""
	spacer = "  ";
	legal = string.letters+string.digits
	log("In doUML level "+str(level))
	try :
		name = uml.getName()
		for i in range(level) :
			spacer = spacer + ".. "
		if (name and name>"") :
			log(spacer+name)
	except : # End of thing with name
		return 0 # don't do anything for unnamed element

	#log ("Check association1 "+str(level))	
	log (uml)
		
	# Remove non MOF element - unnammed association

	# if (isinstance(uml, com.nomagic.uml2.ext.magicdraw.classes.mdkernel.impl.AssociationImpl)) : <<doesn't work <<
	#log ("Check association2 "+str(level))	
	if (not(name) or name==""):
		try : # Association without name
			dontcare = uml.isDerived() # Odd way to check if association - only remove unnamed associations
			log(spacer+uml.getOwningPackage().getName()+" --------remove un-named association-----------")
			deleteme.append(uml)
			return 2
		except :
			dontcare = True

			
		try : #Property without name - only needed for association ends
			aname = ""
			try :
				aname = uml.eContainer().getName()
			except :
				aname = "null" #DOn't know how this would happen
			aname = "_unnamed_"+aname
			log(aname+"-----------------Add property name------------- ")
			uml.setName(aname)
		except :
			return 1
			
	#check for instance specification
	try :
		dontcare = uml.hasSlot() #check if instance spec
		log(spacer+uml.getOwningPackage().getName()+" --------remove instance specification-----------")
		deleteme.append(uml)
	except :
		dontcare = True
	
	log ("Make MOF Name "+str(level))	
	# Make MOF name
	if (name and name>"") :
		squished = False
		name2 = name.replace("Conceptual", "MOF")
		name2 = name2.replace("conceptual", "MOF")
		for c in name2 :
			#if (c==" "):
			if (legal.find(c)<0) :
				squished= True ##  Suppress non name characters
			else :
				if squished :
					c = c.capitalize() # Do camel case
				fixedname += c
				squished = False
				
		if (name!=fixedname) :
			log(spacer+fixedname+ " --------- Made Camel Case ---------")	
			uml.setName(fixedname) # set the new value

			log ("Propigate URI "+str(level))	
	
	# Propigate nested URI
	try :
		uri = uml.getURI()
		if ((not uri) or uri=="") :
			# Get URI from owner
			owneruri = uml.getOwningPackage().getURI()
			if ((owneruri) and owneruri>"") :
				newuri = owneruri
				if (owneruri[-1:]!="/") :
					newuri += "/"
				newuri += fixedname
				log(spacer+newuri+ "--------- Appended URI ---------")	
				uml.setURI(newuri) # Set the new value
		else : #Change URI to conceptual
			newuri = uri.replace("Conceptual", "MOF")
			newuri = newuri.replace("conceptual", "MOF")
			if (uri!=newuri) :
				uml.setURI(newuri)
				
	except : #Only for things that have a URI
		uri = ""
		## No URI
	
	#iterate thru the model	
	if (uml.hasOwnedElement()):
		# Visit all children
		for e in uml.getOwnedElement().iterator():	
			if e.isEditable() : ## Only visit placed we can edit
				doUML(e, level+1) # Visit editable elements	
				
	return 1

project = Application.getInstance().getProject()
model = project.getModel()
log("MOFize Model="+model.getName())
com.nomagic.magicdraw.openapi.uml.SessionManager.getInstance().createSession("MOFize model")
#log("-------- created session-----------")


try :
	doUML(model, 0)

	# delete things that need deleting at end, otherwise iterators are messed up
	man = com.nomagic.magicdraw.openapi.uml.ModelElementsManager.getInstance()
	for uml in deleteme :
		log("Remove "+str(uml))
		man.removeElement(uml)


finally :
	com.nomagic.magicdraw.openapi.uml.SessionManager.getInstance().closeSession()
#log("-------- closes session-----------")