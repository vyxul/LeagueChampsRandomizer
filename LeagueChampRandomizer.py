import random
import pandas as pd
import os
import json
import PIL.Image
import PIL.ImageTk
from typing import List, Set
from tkinter import *
from tkinter import ttk

class Champion():
    Name: str
    Categories: Set[str] = {}
    
    def __init__(self, Name: str):
        self.Name = Name
        
    def AddCategory(self, CategoryName: str):
        self.Categories.add(CategoryName)
        
    def RemoveCategory(self, CategoryName: str):
        self.Categories.remove(CategoryName)

# Aatrox = Chamption("Aatrox", "Champs/Images/", "Aatrox_Image.webp")
# Ahri = Chamption("Ahri")

# try:
#     img = Image.open(Aatrox.image_path + Aatrox.image_file)
#     img = img.rotate(180)
#     save_file_path = Aatrox.image_path + Aatrox.name + "_Reversed.jpeg"
#     img.save(save_file_path)

# except IOError:
#     print("fail")
#     pass

# print(Ahri.name)

# actual code
class CategoryToChampsStruct:
    CategoryName: str
    ChampsInCategory: List[str] = []
    
    def __init__(self, CategoryName: str, ChampsInCategory: List[str]) -> None:
        self.CategoryName = CategoryName
        self.ChampsInCategory = ChampsInCategory
        
def DisplayCategoryMenu(ChampDict: dict):
    for Key, Value in ChampDict.items():
        print(str(Key) + ". " + Value.CategoryName)

def GetUserChampCategory(ChampDict: dict) -> int:
    DisplayCategoryMenu(ChampDict)
    print("Enter the number of the category you want and press enter.")
    return int(input())

def GetRandomChampsFromCategory(ChampDict: dict, CategoryNumber: int, NumberOfChamps: int) -> List[str]:
    CategoryChampCount = len(ChampDict[CategoryNumber].ChampsInCategory)
    # print("CategoryChampCount = ", CategoryChampCount)
    
    # if the number of champs in the category is less than or equal to the specified random champ request
    if (CategoryChampCount <= NumberOfChamps):
        return ChampDict[CategoryNumber].ChampsInCategory
    
    # else, get the random champs from the pool
    RandomChamps = set()
    while len(RandomChamps) < NumberOfChamps:
        RandomChamps.add(random.choice(ChampDict[CategoryNumber].ChampsInCategory))
        
    RandomChampsList = list(RandomChamps)
    RandomChampsList.sort()
    return RandomChampsList
    
def PrintDict(ChampDict: dict):
    for Key, Value in ChampDict.items():
        print(str(Key) + ". " + Value.CategoryName + ": | ", end="")
        for Champ in Value.ChampsInCategory:
            print(Champ + " |", end=" ")
        
        print()

def SaveData(ChampCategoryDict: dict):
    FileName = "ChampCategoryData.json"
    FilePath = "Champs"
    
    if not os.path.exists(FilePath):
        os.makedirs(FilePath)
        print("Created Champs directory.")
        
    # ChampCategoryData_JSON = json.dumps(ChampCategoryDict, indent=4)
    # print(ChampCategoryData_JSON)
    
    with open(FilePath + "/" + FileName, "w") as OutFile:
        json.dump(ChampCategoryDict, OutFile)
    
def LoadData(ChampCategoryDataFile: str) -> dict:
    InFile = open(ChampCategoryDataFile)
    ChampCategoryData_JSON = json.load(InFile)
    return ChampCategoryData_JSON

# Meant to be used just for the first time, no categories on champs
def MakeInitialData() -> dict:
    ChampNameFile = "Champs/AllChampNames.txt"
    ChampNameFileExists = os.path.isfile(ChampNameFile)
    if not ChampNameFileExists:
        print("%s not found. Generate file using python GetLeagueChampInfo.py." %(ChampNameFile))
        return
    
    # Get dictionary ready
    ChampCategoryDict = {
        "Categories" : [],
        "Champions" : {}
    }
    
    # Get the champ info list
    ChampNameList: list[str] = []
    
    # Get Data from File
    ChampNameFile = open(ChampNameFile, "r")
    for line in ChampNameFile:
        ChampName = line.strip()
        ChampNameList.append(ChampName)
        
    # Convert Data into JSON format
    ChampionsDict = {}
    for ChampName in ChampNameList:
        CategoriesDict = {
            "Categories" : []
        }
        ChampionsDict.update({ChampName : CategoriesDict})
        
    ChampCategoryDict["Champions"] = ChampionsDict
    return ChampCategoryDict

def FilterCategories(ChampCategoryData: dict, CategoriesListbox: Listbox, ChampionListFrame: ttk.Frame):
    if CategoriesListbox.curselection():
        CategoryChoice = CategoriesListbox.selection_get()
        print("CategoryChoice = %s" %CategoryChoice)
        PopulateChampsFrame(ChampCategoryData,ChampionListFrame, CategoryChoice)
    # TODO: Filter Champ Panel list to show only champs in this category
    
def ResetCategories(CategoriesListbox: Listbox):
    CategoriesListbox.selection_clear(0, 'end')
    # TODO: Reset Champ Panel to show all champs

def SetupCategoriesListbox(ChampCategoryData: dict, CategoriesPanel: ttk.PanedWindow) -> Listbox:
    CategoriesListbox = Listbox(CategoriesPanel, justify="center")
    
    for Index, Category in enumerate(ChampCategoryData["Categories"]):
        CategoriesListbox.insert(Index, Category)
    
    return CategoriesListbox
      
def GetMatchingChamps(ChampCategoryData: dict, Category: str = "") -> dict:
    SpecificCategory: bool = True if Category != "" else False
    if not SpecificCategory:
        return ChampCategoryData["Champions"]
    
    MatchingChamps: dict = {}
    for Champion in ChampCategoryData["Champions"]:
        # print(Champion)
        ChampCategories = ChampCategoryData["Champions"][Champion]["Categories"]
        if Category in ChampCategories:
            MatchingChamps.update({Champion : {}})
            MatchingChamps[Champion].update({"Categories" : ChampCategories})
            
    return MatchingChamps

def GetChampImageFilePath(Champ: str):
    ChampNameSubstitue = Champ.replace(" ", "")
    ChampNameSubstitue = ChampNameSubstitue.replace("'", "")
    ImageFilePath = "Champs\Images\\"
    
    return ImageFilePath + ChampNameSubstitue + "_Image.jpg"
    

def PopulateChampsFrame(ChampCategoryData: dict, ChampionListFrame: ttk.Frame, Category: str = "test"):
    # destroy all the children in the widget
    for child in ChampionListFrame.winfo_children():
        child.destroy()
    
    # print(ChampCategoryData)
    MatchingChampList: dict = GetMatchingChamps(ChampCategoryData, Category)
    print(MatchingChampList)
    
    RowIndex = 0
    ColumnIndex = 0
    for Index, Champ in enumerate(MatchingChampList.keys()):
        MaxPerRow = 4
        RowIndex = int(Index / MaxPerRow)
        ColumnIndex = int(Index % MaxPerRow)
        
        ChampFrame = ttk.Frame(ChampionListFrame, width=100, height=120)
        ChampFrame.grid(row = RowIndex, column = ColumnIndex, padx=10, pady=10)
        
        ChampImageFilePath = GetChampImageFilePath(Champ)
        print("ChampImageFilePath = %s" %ChampImageFilePath)
        ChampImage = PIL.Image.open(ChampImageFilePath)
        ChampImage = ChampImage.resize((142, 155))
        ChampImageTk = PIL.ImageTk.PhotoImage(ChampImage)
        # some bs to keep the image alive
        global_image_list.append(ChampImageTk)
        
        ChampButton = ttk.Button(ChampFrame, image=ChampImageTk, text=Champ, compound="top", command= lambda ChampName=Champ: testButton(ChampName))
        ChampButton.pack(side="top")
        
def testButton(value: str):
    print("Button pressed. Value = %s" %value)
  
def SetupGUI(ChampCategoryData: dict):
    # GUI stuff
    WindowWidth = 1024
    WindowHeight = 768
    WindowSize = str(WindowWidth) + "x" + str(WindowHeight)
    root = Tk()
    root.minsize(WindowWidth, WindowHeight)
    root.maxsize(WindowWidth, WindowHeight)
    root.geometry(WindowSize)
    root.update_idletasks()
    root.title("LOL Champ Randomizer")
    
    # Styles
    Style = ttk.Style()
    Style.configure("TFrame", background = "deep sky blue")
    Style.configure("TPanedwindow", background = "grey")
    Style.configure("InfoPanel.TPanedwindow", background="White")
    Style.configure("ChampionsPanel.TPanedwindow", background="blue")
    Style.configure("ChampionsListFrame.TFrame", background="deep sky blue")
    Style.configure("TButton", background = "grey")
    Style.configure("ChampImageBorder.TLabel", background = "black")
    Style.configure("ChampNameLabel.TLabel", background = "white")

    # Main areas of the window
    InfoPanel = ttk.PanedWindow(root, width = int(WindowWidth * 3 / 10), style = "InfoPanel.TPanedwindow")
    InfoPanel.pack(side = "left", fill = "y", padx=5, pady=5)
    ChampionsPanel = ttk.PanedWindow(root, style = "ChampionsPanel.TPanedwindow")
    ChampionsPanel.pack(fill = "both", expand= True, padx=5, pady=5)

    # InfoPanel Children
    CategoriesPanel = ttk.PanedWindow(InfoPanel, height = int(WindowHeight * 3 / 10))
    ChampionDetailsPanel = ttk.PanedWindow(InfoPanel)
    InfoPanel.add(CategoriesPanel)
    InfoPanel.add(ChampionDetailsPanel)

    # Category Filter Section
    CategoriesListbox = SetupCategoriesListbox(ChampCategoryData, CategoriesPanel)
    FilterButton = ttk.Button(CategoriesPanel, command= lambda: FilterCategories(ChampCategoryData, CategoriesListbox, ChampionsListFrame), text="Filter")
    ResetButton = ttk.Button(CategoriesPanel, command= lambda: ResetCategories(CategoriesListbox), text= "Reset")
    CategoriesListbox.pack(side="top", fill= "x")
    FilterButton.pack(fill= "x")
    ResetButton.pack(side="bottom", fill= "x")
    
    # ChampionsPanel Section
    ChampionsListFrame = ttk.Frame(ChampionsPanel, style="ChampionsListFrame.TFrame")
    ChampionsListFrame.pack(fill="both", expand=True, padx=5, pady=5)
    
    PopulateChampsFrame(ChampCategoryData, ChampionsListFrame)
    
    root.mainloop()
    
def main():
    #-- Get all the champ category data from excel sheet --#
    # data = pd.read_excel("ArenaChamps.xlsx")
    # print(data)
    
    # Get/Create Save Data
    ChampCategoryData: dict = {}
    ChampCategoryDataFile = "Champs/ChampCategoryData.json"
    ChampCategoryDataFileExists = os.path.isfile(ChampCategoryDataFile)
    
    if not ChampCategoryDataFileExists:
        print("No Save Data found, creating new data")
        ChampCategoryData = MakeInitialData()
        SaveData(ChampCategoryData)
        
    else:
        print("Save Data found")
        ChampCategoryData = LoadData(ChampCategoryDataFile)
        
    SetupGUI(ChampCategoryData)
    
        
    # ChampCount = len(ChampCategoryData["Champions"])
    # print(ChampCount)
    
    
        
    return

    ChampCategoriesDict = {}

    for CategoryNum, Category in enumerate(data.columns):
        # print("Category = ", Category)
        ChampsInCategory = set()
        
        for index in range(0, data[Category].count()):
            # print("\tindex = ", index, end = " | ")
            ChampsInCategory.add(data.at[index, Category])
            # print(data.at[index, Category])
            
        # print(ChampsInCategory)
        SortedChampsList = list(ChampsInCategory)
        SortedChampsList.sort()
        ChampCategoriesDict[CategoryNum] = CategoryToChampsStruct(Category, SortedChampsList)
                    
    PrintDict(ChampCategoriesDict)
    
    #-- Get user input --#
    CategoryChoice = GetUserChampCategory(ChampCategoriesDict)
    RandomChampsFromCategory = GetRandomChampsFromCategory(ChampCategoriesDict, CategoryChoice, 3)
    print(RandomChampsFromCategory)

global_image_list = []
if __name__=="__main__":
    main()