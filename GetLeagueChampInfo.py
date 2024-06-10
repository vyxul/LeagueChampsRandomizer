from typing import List
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import requests
import os

# This script is for scraping champ names and pictures from Riot website (https://www.leagueoflegends.com/en-us/champions/)
# Has no use for the champ randomizer besides getting champ data initially
class LeagueChampScraper:
    def __init__(self) -> None:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options= options)
        self.wait = WebDriverWait(self.driver, 3)
        
    def Get_Info(self, url) -> List[Tuple[str, str]]:
        self.driver.get(url)
        champ_name_elements = self.driver.find_elements(By.XPATH, "//div[@data-testid='card-title']")
        champ_image_elements = self.driver.find_elements(By.XPATH, "//img[@data-testid='mediaImage']")
        
        # Testing just to make sure that correct number of elements found
        # nameCount = len(champ_name_elements)
        # imageCount = len(champ_image_elements)
        # print("nameCount=%s, imageCount=%s" %(nameCount, imageCount))
        
        ChampNames = list()
        ChampImgUrls = list()
        
        for ChampNameElement in champ_name_elements:
            ChampNames.append(ChampNameElement.text)
            
        for ChampImageElement in champ_image_elements:
            ChampImgUrls.append(ChampImageElement.get_attribute("src"))
            
        return list(zip(ChampNames, ChampImgUrls))

def PrintZip(list: List[Tuple[str, str]]):
    for item in list:
        print(item)
        
def DownloadImages(ChampInfoList: List[Tuple[str, str]], ImageSaveLocation: str):
    DirectoryExists = os.path.exists(ImageSaveLocation)
    # print("DirectoryExists=%s" %(str(DirectoryExists)))
    
    if not DirectoryExists:
        return
    
    ImageCount = 0
    
    for ChampInfo in ChampInfoList:
        ChampName = ChampInfo[0]
        # Get ChampName ready to save as a file (No spaces or apostrophes)
        ChampNameSubstitue = ChampName.replace(" ", "")
        ChampNameSubstitue = ChampNameSubstitue.replace("'", "")
        
        ImageFileName = ImageSaveLocation + "/" + ChampNameSubstitue + "_Image.jpg"
        
        # Download image from url
        ImageData = requests.get(ChampInfo[1]).content
        with open(ImageFileName, "wb") as handler:
            handler.write(ImageData)
            ImageCount += 1
            
    print("Success, %s images downloaded to %s" %(ImageCount, ImageSaveLocation))
        
def SaveChampNames(ChampInfoList: List[Tuple[str, str]], FileSaveLocation: str):
    DirectoryExists = os.path.exists(FileSaveLocation)
    
    if not DirectoryExists:
        print("Doesn't exist")
        return
    
    ChampCount = 0
    
    FileName = "AllChampNames.txt"
    with open(FileSaveLocation + "/" + FileName, "w+") as file:
        for ChampInfo in ChampInfoList:
            file.write("%s\n" %(ChampInfo[0]))
            ChampCount += 1
    
    file.close()
    
    print("Success, %s champion names saved to %s" %(ChampCount, FileSaveLocation + FileName))

def main():
    url = "https://www.leagueoflegends.com/en-us/champions/"
    ImageSaveLocation = "Champs\Images"
    ChampListSaveLocation = "Champs"
    scraper = LeagueChampScraper();
    ChampInfoList = scraper.Get_Info(url)
    # PrintZip(ChampInfo)
    #DownloadImages(ChampInfoList, ImageSaveLocation)
    SaveChampNames(ChampInfoList, ChampListSaveLocation)
    
    
    
if __name__=="__main__":
    main()