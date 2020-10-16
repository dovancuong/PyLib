import os,shutil,glob
class FileAccess:
	def __init__(self,fileName):
		self.fileName=fileName

	def OverWriteFile(self,*argv): # write array
		try:
			with open(self.fileName, 'w') as filetowrite:
				for line in argv:
					filetowrite.write(str(line)+'\n')
			print('Write file Success')
			return 'Completed'
		except OSError as ex:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			return 'Error:'+str(e.strerror)

	def WriteAppendFile(self, *argv): # append array
		try:
			with open(self.fileName, "a") as f:
				for line in argv:
					f.write(line+"\n")
			print('Append file success')
			return 'Completed'
		except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			return 'Error: '+str(e.strerror)

	def ReadFile(self):
		try:
			with open(self.fileName, 'r') as filehandle:
				places = [current_place.rstrip() for current_place in filehandle.readlines()]
			print('Read file success')
			print(str(places))
			return places
		except OSError as e:
			print ("Error:read file %s - %s." % (e.filename, e.strerror))
			return "Error: "+str(e.strerror)

	def DeleteFile(self):
		try:
			os.remove(self.fileName)
			print('Delete file success')
			return 'Completed'
		except OSError as e:  ## if failed, report it back to the user ##
			print ("Error: %s - %s." % (e.filename, e.strerror))
			return 'Error:'+str(e.strerror)

	def CheckFileExist(self):
		return os.path.isfile(self.fileName) 

	def CopyFile(self, newPath):
		newFile=os.path.join(newPath,os.path.basename(self.fileName)) # create new file from new path
		try:
			shutil.copy(self.fileName,newFile)
			print('Copy file success')
			return 'Completed'
		except OSError as e:
			pprint ("Error: %s - %s." % (e.filename, e.strerror))
			return "Error: "+str(e.strerror)

	def RenameFile(self, newName):
		try:
			os.rename(self.fileName, newName)
			os.path.dirname(os.path.join(os.path.abspath(self.fileName), newName)) # redefine fileName
			print('Rename file success')
			return'Completed'
		except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			return 'Error:'+str(e.strerror)

	def MoveFile(self,newPath):
		try:
			newFile=os.path.join(newPath,os.path.basename(self.fileName)) 
			print('new file:',newFile)
			shutil.move(self.fileName, newFile)
		except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
			return 'Error:'+str(e.strerror)

class  FolderAccess:
	def __init__(self, folderPath):
		self.folderPath=folderPath

	def CreateFolder(self):
		if not os.path.exists(self.folderPath):
			try:
				os.makedirs(self.folderPath)
				print('Create Folder Success')
				return 'Completed'
			except OSError as e:
				print ("Error: %s - %s." % (e.filename, e.strerror))
				return 'Error:'+str(e.strerror)
		else:
			print('Create folder exist')
			return'Completed'

	def CheckFolderExist(self):
		return os.path.exists(self.folderPath)

	def GetFolderFiles(self, fileType): # get list of files in root, fileType=None for all file type
		files=[]
		for file in os.listdir(self.folderPath):
			filePath=os.path.join(self.folderPath, file)
			if os.path.isfile(filePath):
				if fileType is not None:
					if fileType in filePath: # file filter
 						files.append(filePath)
				else: # get all file type
					files.append(filePath)
		print(str(files))
		return files

	def GetAllFolderFiles(self,fileType): # search all file in root folder & child folder
		files = []
		# r=root, d=directories, f = files
		for r, d, f in os.walk(self.folderPath):
			for file in f:
				if fileType is not None:
					if fileType in file: # use file filter
						files.append(os.path.join(r, file))
				else: # get all file
					files.append(os.path.join(r, file))
		print(str(files))
		return files


	def RenameFolder(self, newFolder):
		pass

	def DeleteFolder(self,folderPath):
		try:
			shutil.rmtree(folderPath)
		except OSError as e:
			print ("Error: %s - %s." % (e.filename, e.strerror))
	def MoveFolder(self,newFolder):
		pass



def TestFile():
	f=FileAccess('test1.txt')
	f.OverWriteFile('line1','line2','line3')
	print(str(f.CheckFileExist()))
	f.WriteAppendFile('add1','add2','add3')
	#f.CopyFile('New folder')
	f.RenameFile('new.txt')
	
	#f.MoveFile('New folder')
	#f.DeleteFile()

def TestFolder():
	f=FolderAccess('data')
	f.CreateFolder()
	f.GetAllFolderFiles('.py')
	f.DeleteFolder('123')


if __name__=='__main__':
	TestFolder()
