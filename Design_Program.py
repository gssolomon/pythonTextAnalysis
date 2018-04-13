# -*- coding: utf-8 -*-

#Created on Mon Jan  1 12:39:35 2018

#@author: glenn

#Name: Glenn Solomon
#Student Number: 040908930

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import os
import string

class Analysis:
    
    def __init__(self, infile):
        
        #Initialising all variables to count
        self.countWord = 0
        self.countOccurence = {} #to count occerences of words by help of dictionary's 'key'
        self.countChar = 0
        self.countWhite = 0
        self.percentageSpace = 0
        
        self.mainFunctioning(infile)
        
    def mainFunctioning(self,infile):
        try: #Opening the file in try block
            with open(infile) as f:
                lines = f.read().splitlines()
                
            for line in lines:
                self.countChar += len(line)
                self.countWhite += line.count(" ")
                words = line.split()
                self.countWord += len(words)
                
                for word in words:
                    trans = str.maketrans('','', string.punctuation)  #removes all punctuations if any
                    word = word.translate(trans)
                    word = word.lower() #converts to lower case
                    if word in self.countOccurence: #counting occurences
                        self.countOccurence[word] += 1
                    else:
                        self.countOccurence[word] = 1
                        
                self.percentageSpace = self.countWhite / self.countChar * 100
                
        except IOError as e:
            messagebox.showinfo("Failed to open file", "Error: %s" % (e))
            exit()
            
            
class GUIAnalysis:
    
    def __init__(self, top):
        self.inFile= ""
        self.labelFile = tk.Label(top, text = "Open file:", anchor = "e")
        self.labelFile.grid(row = 2, column = 1)
        self.entryFile = tk.Entry(top, validate = "focusout", validatecommand = self.callback)
        self.entryFile.grid(row = 2, column = 2)
        
        self.buttonBrowse = tk.Button(top, text = "Browse", command = self.browseOpen)
        self.buttonBrowse.grid(row = 2, column = 3)
        
        self.blankLabel = tk.Label(top, text = "\n")
        self.blankLabel.grid(row =3, column = 1, columnspan = 3)
        
        self.buttonBegin = tk.Button(top, text = "Start Analysis", command = lambda: self.beginProcess(top))
        self.buttonBegin.grid(row = 4, column = 1, columnspan = 3)
        
        self.blankLabel = tk.Label(top, text = "\n")
        self.blankLabel.grid(row = 5, column = 1, columnspan=3)
        
        self.buttonExit = tk.Button(top, text = "Exit", command = lambda: self.closeWindow(top))
        self.buttonExit.grid(row = 6, column = 1, columnspan = 3)
        
        
    def callback(self):
        self.inFile = self.entryFile.get()
        
    def browseOpen(self):
        currentDir = os.getcwd() #assigning current working directory
        tempFile = filedialog.askopenfilename(initialdir = currentDir, filetypes = (("Text Files", "*.txt"), ("All Files", "*.*"))) #which file to open
        
        if len(tempFile) > 0: #to display in entrybox the file-destination
            print("%s file chosen" %tempFile)
            
            self.inFile = tempFile
            self.entryFile.delete(0,tk.END)
            self.entryFile.insert(0,tempFile)
            
            
    def beginProcess(self, top):
        self.inFile = self.entryFile.get()
        if self.entryFile.get() == "": #if file not selected and 'Start Analysis' button is clicked
            self.browseOpen()
            
        if self.entryFile.get() == "":
            return
        
        callAnalysis = Analysis(self.inFile) #Analysis Class's object
        
        self.outFile = os.path.splitext(self.inFile)[0] + "_analysis.txt" #destination output file to be created
        
        try: #writing in output file in try block
            with open(self.outFile, "w") as f:
                f.write("Name of text: \t" + os.path.basename(self.inFile) + "\n")
                f.write("Total Non-Blank Character Count: \t" + str(callAnalysis.countChar) + "\n")
                f.write("Total Blank Character Count: \t" + str(callAnalysis.countWhite) + "\n")
                f.write("Percentage of Blank Characters: \t" + "{0:.3f}".format(round(callAnalysis.percentageSpace)) + "\n")
                f.write("Total Word Count: \t" + str(callAnalysis.countWord) + "\n")
                f.write("Word: Count:-\n")
                
                for key, value in callAnalysis.countOccurence.items():
                    f.write(key + ": " + str(value) + "\n \n")
                    
        except IOError as e:
            messagebox.showinfo("Failed to write to file", "Error: %s" % (e))
            exit()
            
        self.outputDisplay(top)
            
    def outputDisplay(self,top): #to display info on the widget
        
        callAnalysis = Analysis(self.inFile)
        
        displayOutput = "\n\nTotal number of words: " + str(callAnalysis.countWord) + "\n"
        displayOutput += "Total number of characters: " + str(callAnalysis.countChar) + "\n"
        displayOutput += "Total number of blank spaces: " + str(callAnalysis.countWhite) + "\n"
        displayOutput += "Percentage of blank spaces: " + "{0:.3f}".format(round(callAnalysis.percentageSpace)) + "\n"
        displayOutput += "\n\n More Info at: \n \n" + self.outFile
        
        self.dispLabel = tk.Label(top, text = displayOutput)
        self.dispLabel.grid(row = 7, column = 1, columnspan = 3, sticky = tk.W + tk.E)
        
    def closeWindow(self, top):
        top.destroy()
        

def main():
    root = tk.Tk()
    root.resizable(width = False, height = False)
    root.title("Text Analysis")
    begin = GUIAnalysis(root)
    root.mainloop()
    
if __name__=="__main__": main()