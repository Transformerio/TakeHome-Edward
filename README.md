**ToScrape Scraper -> CSV**

This code uses the AIOHTTP library so to expedite the scraping process as data is being scraped asynchronously compared to the synchronous python requests library.


https://user-images.githubusercontent.com/31602118/228300988-8fd05758-75fe-40b1-bd65-1d0967400d57.mov


Code Layout:

Helper Functions:
- WriteToCSV(filename, header, data)
    
    used to transfer parsed html code, that is put into a dict, into a csv file.
- FetchBookInfo(url, session)

    uses the session passed onto it and scrapes all the book information and returns a dict containing the desired information.
- FetchBookInfoWithGenre(url, session)
    
    same as FetchBookInfo(url, session) but adds in the genre for the special prompt.
- FetchAuthorInfo(url, session)
    
    similar to FetchBookInfo, this function uses the session passed onto it and scrapes all the author information and returns a dict containing the desired information.
    
Call Functions:
- FetchFiveStar() 
    
    Collects all the five fiction books' href values and passes it to FetchBookInfo and returns
    a list of all the books' information.
- FetchHistoricalFictionBooks()
    
    Collects all the historical fiction books' href values that has a price tag >$30.00 and passes it to FetchBookInfo and returns
    a list of all the books' information.
- FetchInspirationalQuotes()
    
    Collects all the quotes', that contain the inspiration tag, href values and passes it to FetchAuthorInfo and returns
    a list of all the books' and authors' information.
- FetchFriendshipQuotes()
    
    Collects all the authors', that wrote a quote containg the friendship tag, href values and passes it to FetchAuthorInfo and returns
    a list of all the authors' information.
- FetchAllGenres
    
    Collects all the books' href values and grouped it by genre, which then passes it to FetchBookInfoWithGenre and returns
    a list of all the books' information.
