# import required modules
from bs4 import BeautifulSoup
import requests

baseUrl = "https://en.wikipedia.org"
moviesHomePageUrl = "https://en.wikipedia.org/wiki/Lists_of_Hindi_films"


def crawl(moviesHomePageUrl): 
    # get URL
    moviesHomePage = requests.get(moviesHomePageUrl)
 
    # scrape webpage
    homePageSoup = BeautifulSoup(moviesHomePage.content, 'html.parser')

    # find tags
    yearlyMoviesPageUrls = homePageSoup.find(class_="mw-parser-output").find_all("li")
    for yearlyMoviesPageUrl in yearlyMoviesPageUrls:
        yearlyMoviePage = requests.get(baseUrl + yearlyMoviesPageUrl.next.get("href"))
        yearlyMoviePageSoup = BeautifulSoup(yearlyMoviePage.content, 'html.parser')
        movieUrlTables = yearlyMoviePageSoup.find_all(class_="wikitable")
        for movieTeble in movieUrlTables:
            movieRows = movieTeble.find_all("tr")
            for movieRow in movieRows:
                columns = movieRow.find_all("td")
                if(columns is not None and len(columns) > 0):
                    for column in columns:
                        urls = column.find_all('a')
                        if(urls is not None and len(urls) > 0):
                            moviePage = requests.get(baseUrl + urls[0]['href'])
                            moviePageSoup = BeautifulSoup(moviePage.content, 'html.parser')
                            paras = moviePageSoup.find_all("p")
                            for para in paras:
                                print(para.get_text())

                            print(urls[0]['href'])
                            break

  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    crawl(moviesHomePageUrl)