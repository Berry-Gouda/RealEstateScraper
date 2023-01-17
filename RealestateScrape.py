from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv



class Website:
    """
    class that contains information about website structure
    """
    def __init__(self, name: str, url : str, appendURL: str, linkRegex: str):
        self.name = name
        self.url = url
        self.appendURL = appendURL
        self.linkRegex = linkRegex






class Listing:
    """
    Common Class that contains the information about a Realestate Listing
    """

    def __init__(self, address: str, price: str, bed: str, bath: str, days_on_market: str, property_type: str,
     url: str, agent:str, agency:str):
        self.address = address
        self.price = price
        self.bed = bed
        self.bath = bath
        self.days_on_market = days_on_market
        self.property_type = property_type
        self.url = url
        self.agent = agent
        self.agency = agency
        self.fieldNames = ['Address', 'Price', 'Beds', 'Baths', 'Days Listed', 'Type', 'Agent', 'Agency', 'URL']

    def print(self):
        """
        Easy Printing Function Controls Output
        """
        print("Address:\t{}".format(self.address))
        print("Price:\t\t{}".format(self.price))
        print("Beds:\t\t{}".format(self.bed))
        print("Baths:\t\t{}".format(self.bath))
        print("Days Listed:\t{}".format(self.days_on_market))
        print("Type:\t\t{}".format(self.property_type))
        print("Agent:\t\t{}".format(self.agent))
        print("Agency:\t\t{}".format(self.agency))
        print("URL:\t\t{}".format(self.url))
        print()
        print()












class RealEstateDataHandler:

    def __init__(self):
        self.websites = [Website('Redfin', 'https://www.redfin.com/zipcode/', 'https://www.redfin.com', '^(/MA/).*')]
        self.zipCodes = []
        self.listings = []


    def WriteListingData(self):
        """
        Writes the results of the scrape to a csv file
        """
        file = open('Listings.csv', 'w', newline='')
        writer = csv.DictWriter(file, fieldnames=self.listings[0].fieldNames)
        writer.writeheader()
        for listing in self.listings:
            writer.writerow({'Address':listing.address, 'Price':listing.price, 'Beds':listing.bed, 'Baths':listing.bath, 'Days Listed':listing.days_on_market,
            'Type':listing.property_type, 'Agent':listing.agent, 'Agency':listing.agency,'URL': listing.url})

        file.close()

    

    def WriteZipCodes(self):
        """
        Writes the file for zipcodes
        """
        file = open('zipcodes.txt', 'w')
        file.writelines(self.zipCodes)
        file.close

    def LoadZipCodes(self):
        """
        Loads ZipCodes from the file zipcodes.txt
        """

        file = open('zipcodes.txt', 'r')
        self.zipCodes = file.read().splitlines()
        file.close()

    def EnterZipCodes(self):

        temp = ''
        print("\nEnter the zipcodes you would like to search")

        for s in input():
            print("We are in the input for loop")
            if s == ' ':
                self.zipCodes.append(temp)
                temp = ''
            else:
                temp += s

        self.zipCodes.append(temp)

        for code in self.zipCodes:
            print(code)

    def PrintListingData(self):
        """
        Debug Function to print the data that has been Scraped
        """
        for listing in self.listings:
            listing.print()

    def GatherData(self):
        global crawler

        print("Length of Zipcodes: " + str(len(self.zipCodes)))
        print("Length of Websites: " + str(len(self.websites)))

        for site in self.websites:
            for code in self.zipCodes:
                crawler.getListingLinks(site,code)

        self.listings = crawler.parseData()











class Menu:

    def PrintMenuOptions(self):
        """
        Prints the menu options
        """
        print("1:\tEnter Zipcodes")
        print("2:\tSave Zipcodes")
        print("3:\tLoad Zipcodes")
        print("4:\tCrawl")
        print("5:\tPrint Results")
        print("6:\tSave Results")
        print("7:\tExit")

    def MenuSelection(self, selection:str):
        """
        Handles calling the correct functions from menu selection
        """

        global dataHandler

        if selection == '1':
            dataHandler.EnterZipCodes()
        elif selection == '2':
            dataHandler.WriteZipCodes()
        elif selection == '3':
            dataHandler.LoadZipCodes()
        elif selection == '4':
            dataHandler.GatherData()
        elif selection == '5':
            dataHandler.PrintListingData()
        elif selection == '6':
            dataHandler.WriteListingData()
        elif selection == '7':
            return
        else:
            print("\nSelection not recognized, try again.")


class RealEstateCrawler:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.listingLinks = []

    def getListingLinks(self, site:Website, zipcode:str):
        """
        Gets a list of links for a specific ZipCode
        """

        #driver = webdriver.Chrome('chromdriver.exe')
        self.driver.minimize_window()
        self.driver.get(site.url+zipcode)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        reString = site.linkRegex + zipcode + '.*'

        links = bs.find_all('a', href=re.compile(reString))

        for listing in links:
            if not(site.appendURL+listing.attrs['href']) in self.listingLinks:
                self.listingLinks.append(site.appendURL + listing.attrs['href'])

        print(len(self.listingLinks))

    def parseData(self) -> list[Listing]:
        """
        Goes through the generated List of Links and processes pages to pull the information to 
        create a Listing Data Object 
        """

        rtnListings = []

        print(len(self.listingLinks))


        for listing in self.listingLinks:

            if "redfin" in listing:
                self.driver.minimize_window()
                self.driver.get(listing)
                bs = BeautifulSoup(self.driver.page_source, 'html.parser')

                details = bs.find_all('span', {'class': 'content text-right'})

                try:
                    agent_details = bs.find('div', {'class': 'agent-basic-details font-color-gray-dark'}).find_all('span')
                    agent = agent_details[1].get_text()
                    agency = agent_details[2].get_text()
                except:
                    agent = 'None'
                    agency = 'None'

                url = listing
                address = bs.find('div', {'data-rf-test-id':'abp-streetLine'}).get_text() + ' ' + bs.find('div', {'data-rf-test-id':'abp-cityStateZip'}).get_text()
                price = bs.find('div', {'data-rf-test-id': 'abp-price'}).find('div').get_text()
                bed = bs.find('div', {'data-rf-test-id': 'abp-beds'}).find('div').get_text()
                bath = bs.find('div', {'data-rf-test-id': 'abp-baths'}).find('div').get_text()
                time_on_market = details[1].get_text()
                type = details[2].get_text()

                tListing = Listing(address, price, bed, bath, time_on_market, type, url, agent, agency)

                rtnListings.append(tListing)

        return rtnListings




crawler = RealEstateCrawler()
dataHandler = RealEstateDataHandler()
menu = Menu()

selector = ''

while selector != '7':

    menu.PrintMenuOptions()
    selector = input()
    menu.MenuSelection(selector)












#Surface Level infromation to allow create ability to crawl multiple sites

#Zillow
#URL for zipcodes search examples
#https://www.zillow.com/homes/for_sale/02472_rb/
#https://www.zillow.com/watertown-ma-02472/
#URL Link example
#https://www.zillow.com/homedetails/51-Quirk-St-1-Watertown-MA-02472/2060389045_zpid/