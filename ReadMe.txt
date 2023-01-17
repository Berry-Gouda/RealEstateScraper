Title: Real Estate Listing Scraper

Motivation: 

This project was developed due to the inefficiencies of searching sites like redfin when truly searching for a new property over many different zip codes. Compared to their current design which is aimed at casual browsing.

Build Status: Works as intended.

Use Cases:

The current use cases for this scraper are currently limited to simplifying the searching of data across many zip codes. It saves time allowing you view the listings in a clear and concise way with the high level information for the listing. 

Product Description: 

This scraper takes a list of zip codes that you provide and searches redfin for all listings those zip codes. Before parsing the data in those links, it will make sure there are no duplicates, this can happen if multiple zip codes for one town exist along with some low inventory density locations having a bit of bleed into surrounding zip codes to fill out search results.

This project uses selenium along with the chromium web driver to bypass redfin’s defense against automated page requests. It also uses Beautiful Soup to help us parse the data that we are pulling.

How to install and run the project:

Following these instructions will allow you to run this project with no code modifications.
1. Download and extract the directory to your desired location.
2. Use pip to install the required libraries. If you need to install PIP please visit this link
		Windows 		MacOS			LinuxSelenium	pip3 install selenium	pip3 install selenium	$sudo pip install seleniumBeautiful Soup	pip3 install bs4	pip3 install bs4	$sudo pip install bs4
3. Install the chromium driver.
	a. Using this driver and ensuring that it is installed on path allows you to not make any code modifications.

4. To run the program type the following into the command line.
	a. \RealEstate Scraper\python RealestateScrape.py



How to use the Project:

* When started for the first time you will need to enter the 5-digit zip codes you would like to search.
	o You can add them directly to the txt file in the directory or type them in by selecting the menu option.
	o You can then save these zip codes to a file to save time in future crawls.
* The Website class stores the information related to appending and checking url’s for validity and duplicates.

* The Listing Class is a data object that stores all of the information that is scraped from the web. This class also contains a helper function to print out the data to the console.

* The RealEstateDataHandler class manages the loading and saving of files, along with storing the data that is parsed during operation.

* The Crawler class makes the page requests and parses the data. It does the work in the following order.
	o Gathers all listing url’s from zip code searches.
	o Removes duplicates
	o Parses the data from each page in the list of url’s

* The Data that is parsed follows:
	o Address
	o Price
	o Beds
	o Baths
	o Days on Market
	o Property Type
	o The Listing Agent and Agency
	o Direct URL
* To Change the data that is parsed and output you will need a general knowledge of html and the way that webpages are structured. Along with modifying the 3 of the 4 classes in the program.
	o Listing Class:
		* Update the fieldNames variable with new data field.
		* Initialize new data in the constructor.
		* Update the print helper function to account for new data.
	o Data Handler Class:
		* Update the WriteListingData function to include the new data in the writerow call.
	o Crawler Class:
		* Update the ParseData function to retrieve the information that you would like based on the page html.	


* To use a different webdriver please visit the following link for detailed instructions on getting your WebDriver of choice of installed.
	o Updating the Crawler Class will also be necessary.

Trouble Shooting:

* 403 errors.
	o Make sure webdriver is working properly
* No data being output.
	o Make sure your zip codes are being loaded properly
	o Check to make sure your zip codes are correct
* None types do not have the function .get_text().
	o Check the webpage to see if they have updated the html code behind the site.

Upcoming Features:

* Restructuring of Website Class and Crawler Class to handle different websites to search for data.
* More User feed back on errors and current status of the program.
* Restructure of the DataHandler class to include the following.
	o Option to save more than one Listing csv files.
	o Ability to load multiple Listing csv files into memory.
* Creation of a math class that can help analyze data including but not limited to:
	o Average Listing Price
	o Difference in Average listing price between dates
	o Difference in Number of listings per property type
	o Average time on market

Contributors:
	* Roger Silvestri

License: Public Domain


