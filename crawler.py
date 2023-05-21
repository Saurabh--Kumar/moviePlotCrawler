# import required modules
from bs4 import BeautifulSoup
import requests

baseUrl = "https://en.wikipedia.org"

# moviesHomePageUrl is an index page which contains link to yearly movie pages.
# with each yearly page havinf links to movie pages of the movies releases in that year.
moviesHomePageUrl = "https://en.wikipedia.org/wiki/Lists_of_Hindi_films"

def crawlYearlyMoviePage(yearlyMoviesPageUrl):
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


def crawl(moviesHomePageUrl): 
    # get URL
    moviesHomePage = requests.get(moviesHomePageUrl)
 
    # scrape webpage
    homePageSoup = BeautifulSoup(moviesHomePage.content, 'html.parser')

    # find tags
    yearlyMoviesPageUrlList = homePageSoup.find(class_="mw-parser-output").find_all("li")
    for yearlyMoviesPageUrl in yearlyMoviesPageUrlList:
        crawlYearlyMoviePage(yearlyMoviesPageUrl)

  
if __name__=="__main__":
    crawl(moviesHomePageUrl)