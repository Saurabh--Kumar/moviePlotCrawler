# import required modules
from bs4 import BeautifulSoup
import requests
import os
import concurrent.futures


chunkSize = 10
baseUrl = "https://en.wikipedia.org"
moviesDirectory = "./MoviesDetails/"

# moviesHomePageUrl is an index page which contains link to yearly movie pages.
# with each yearly page havinf links to movie pages of the movies releases in that year.
moviesHomePageUrl = "https://en.wikipedia.org/wiki/Lists_of_Hindi_films"

def saveToFile(movieText, movieFilePath):

    directory = os.path.dirname(movieFilePath)
    os.makedirs(directory, exist_ok=True)

    
    with open(movieFilePath, 'w') as f:
        f.write(movieText)


def saveMovie(paras, movieName):
    movieDetailsText = ""
    for para in paras:
        movieDetailsText = movieDetailsText + para.get_text() + "\n"

    
    saveToFile(movieDetailsText, moviesDirectory + movieName + ".txt")


def scrapMovieDetails(moviePageUrl: str):
    moviePage = requests.get(moviePageUrl)
    moviePageSoup = BeautifulSoup(moviePage.content, 'html.parser')
    paras = moviePageSoup.find_all("p")
    movieName = moviePageUrl.split("/")[-1]
    saveMovie(paras, movieName)



# each table has movies releases in that quarter of the year
def crawlMoviesFromEachQuarter(quarterlyMovieTable):
    movieRows = quarterlyMovieTable.find_all("tr")
    for movieRow in movieRows:
        columns = movieRow.find_all("td")
        if(columns is not None and len(columns) > 0):
            for column in columns:
                urls = column.find_all('a')
                if(urls is not None and len(urls) > 0):
                    scrapMovieDetails(baseUrl +urls[0]['href'])
                    print(urls[0]['href'])
                    break



def crawlYearlyMoviePage(yearlyMoviesPageUrl: str):
    yearlyMoviePage = requests.get(baseUrl + yearlyMoviesPageUrl.next.get("href"))
    yearlyMoviePageSoup = BeautifulSoup(yearlyMoviePage.content, 'html.parser')
    movieUrlTables = yearlyMoviePageSoup.find_all(class_="wikitable")
    # each page has one table for each quarter. Each table has a list of movies released that year
    for movieTable in movieUrlTables:
        crawlMoviesFromEachQuarter(movieTable)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def crawl(moviesHomePageUrl: str): 
    # get URL
    moviesHomePage = requests.get(moviesHomePageUrl)
 
    # scrape webpage
    homePageSoup = BeautifulSoup(moviesHomePage.content, 'html.parser')

    # find tags
    yearlyMoviesPageUrlList = homePageSoup.find(class_="mw-parser-output").find_all("li")
    yearlyMoviesPageUrlListChunks = chunks(yearlyMoviesPageUrlList, chunkSize)
    for yearlyMoviesPageUrlListChunk in yearlyMoviesPageUrlListChunks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunkSize) as executor:
            # Submit file writing tasks to the thread pool
            futures = [executor.submit(crawlYearlyMoviePage, yearlyMoviesPageUrl) for yearlyMoviesPageUrl in yearlyMoviesPageUrlListChunk]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

  
if __name__=="__main__":
    crawl(moviesHomePageUrl)