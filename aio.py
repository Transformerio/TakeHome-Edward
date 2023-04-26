import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup 
import csv

"""
This code is created by Edward Li
This code uses the AIOHTTP library so to expedite the scraping process as data is being scraped
    asynchronously compared to the synchronous python requests library.
BS4 is used to parse HTML code.
Regex is used to get specific text / content from BS4 or html

Layout:
Helper Functions:
- WriteToCSV(filename, header, data)
    used to transfer parsed html code, that is put into a dict, into a csv file.
- FetchBookInfo(url, session)
    uses the session passed onto it and scrapes all the book information and returns a dict containing 
    the desired information.
- FetchBookInfoWithGenre(url, session)
    same as FetchBookInfo(url, session) but adds in the genre for the special prompt.
- FetchAuthorInfo(url, session)
    similar to FetchBookInfo, this function uses the session passed onto it and scrapes all the author 
    information and returns a dict containing the desired information.


Call Functions:

- FetchFiveStar() 
    Answers Prompt 1
    Collects all the five fiction books' href values and passes it to FetchBookInfo and returns
    a list of all the books' information.

- FetchHistoricalFictionBooks()
    Answers Prompt 2
    Collects all the historical fiction books' href values that has a price tag >$30.00 and passes it to FetchBookInfo and returns
    a list of all the books' information.

- FetchInspirationalQuotes()
    Answers Prompt 3
    Collects all the quotes', that contain the inspiration tag, href values and passes it to FetchAuthorInfo and returns
    a list of all the books' and authors' information.

- FetchFriendshipQuotes()
    Answers Prompt 4
    Collects all the authors', that wrote a quote containg the friendship tag, href values and passes it to FetchAuthorInfo and returns
    a list of all the authors' information.

- FetchAllGenres
    Answers Prompt 5
    Collects all the books' href values and grouped it by genre, which then passes it to FetchBookInfoWithGenre and returns
    a list of all the books' information.
"""


async def FetchBookInfo(url, session) -> dict:
    async with session.get(url) as response:
        bookSoup = BeautifulSoup(await response.text(), 'html.parser')
        productmain_container = bookSoup.find_all('div', class_='col-sm-6 product_main')
        book_title = productmain_container[0].find('h1').text
        book_price = productmain_container[0].find('p', class_='price_color').text
        print('[FetchBookInfo] fetching {0}'.format(book_title))
        product_information_table = bookSoup.find('table', class_='table table-striped')
        product_details = {
            'Title': book_title,
            'Price': book_price,
            'UPC': None,
            'Product Type': None,
            'Price (excl. tax)': None,
            'Price (incl. tax)': None,
            'Tax': None,
            'Availability': None,
            'Number of reviews': None
        }
        for row in product_information_table.find_all('tr'):
            product_details[row.find('th').text] = row.find('td').text
        return product_details

async def FetchBookInfoWithGenre(genre, url, session) -> dict:
    async with session.get(url) as response:
        bookSoup = BeautifulSoup(await response.text(), 'html.parser')
        productmain_container = bookSoup.find_all('div', class_='col-sm-6 product_main')
        book_title = productmain_container[0].find('h1').text
        book_price = productmain_container[0].find('p', class_='price_color').text
        print('[FetchBookInfoWithGenre] fetching {0}'.format(book_title))
        product_information_table = bookSoup.find('table', class_='table table-striped')
        product_details = {
            'Genre': genre,
            'Title': book_title,
            'Price': book_price,
            'UPC': None,
            'Product Type': None,
            'Price (excl. tax)': None,
            'Price (incl. tax)': None,
            'Tax': None,
            'Availability': None,
            'Number of reviews': None
        }
        for row in product_information_table.find_all('tr'):
            product_details[row.find('th').text] = row.find('td').text
        return product_details

async def FetchAuthorInfo(author_name, url, session) -> dict:
    # author name has to be passed by param becuase toscrape has a typo in its author-title tag where start:<h3> end </h2> via Google Chrome
    # response.text() will report h3 including all the informatio in the author_container
    async with session.get(url) as response:
        authorSoup = BeautifulSoup(await response.text(), 'html.parser')
        author_container = authorSoup.find('div', class_='author-details')
        #author_name = author_container.findChil('h2', class_='author-title') decremented until toscrape fixes error
        author_dob = author_container.find('span', class_='author-born-date').text
        author_pob = author_container.find('span', class_='author-born-location').text
        author_desc = author_container.find('div', class_='author-description').text
        ##TODO: CHECK DESCRIPTION BECUASE CSV missing length
        print('[FetchAuthorInfo] fetching {0}'.format(len(author_desc.strip())))
        product_details = {
            'Author': author_name,
            'Date of Birth': author_dob,
            'Location of Birth': author_pob,
            'Description': author_desc.strip()
        }
        return product_details

def WriteToCSV(filename, header, data):
    '''
    - data must be an array of dicts
    - elements must not contain nested dicts
    - data keys = header
    '''
    
    with open(filename + '.csv', 'w') as csvfile:
        print('[WriteToCSV] {0}.csv has been opened and is currently being written ...'.format(filename))
        csvwriter = csv.DictWriter(csvfile, fieldnames = header)
        csvwriter.writeheader()
        csvwriter.writerows(data)
        print('[WriteToCSV] {0}.csv has successfully been written to.'.format(filename))


async def FetchFiveStar():
    fivestar_href_List = []
    headers = [
        'Title', 
        'Price', 
        'UPC',
        'Product Type', 
        'Price (excl. tax)', 
        'Price (incl. tax)', 
        'Tax', 
        'Availability', 
        'Number of reviews'
    ]
    async with aiohttp.ClientSession('http://books.toscrape.com/') as session:
        tasks = []
        book_href = []
        init_soup = ...
        async with session.get('/catalogue/page-1.html') as resp:
            init_soup = BeautifulSoup(await resp.text(), 'html.parser')
        page_range = init_soup.find_all('li', class_='current')[0].text.strip()
        page_max = re.search(r'(?<=of ).*', page_range)[0]
        for i in range(1, int(page_max) + 1):
            async with session.get('/catalogue/page-{0}.html'.format(i)) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                for book in soup.find_all('p', class_='star-rating Five'):
                    book_parent_container = book.parent
                    book_href.append('/catalogue/{0}'.format(book_parent_container.find('h3').find('a')['href']))
        for href in book_href:
            task = asyncio.ensure_future(FetchBookInfo(href, session))
            tasks.append(task)

            #responses = await asyncio.gather(*tasks)
            fivestar_href_List = await asyncio.gather(*tasks)


    await session.close()
    return headers, fivestar_href_List
    
async def FetchHistoricalFictionBooks():
    fivestar_href_List = []
    headers = [
        'Title', 
        'Price', 
        'UPC',
        'Product Type', 
        'Price (excl. tax)', 
        'Price (incl. tax)', 
        'Tax', 
        'Availability', 
        'Number of reviews'
    ]
    async with aiohttp.ClientSession('http://books.toscrape.com/') as session:
        tasks = []
        book_href = []
        init_soup = ...
        async with session.get('/catalogue/category/books/historical-fiction_4/page-1.html') as resp:
            init_soup = BeautifulSoup(await resp.text(), 'html.parser')
        page_range = init_soup.find_all('li', class_='current')[0].text.strip()
        page_max = re.search(r'(?<=of ).*', page_range)[0]
        for i in range(1, int(page_max) + 1):
            async with session.get('/catalogue/category/books/historical-fiction_4/page-{0}.html'.format(i)) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                page_range = soup.find_all('li', class_='current')[0].text.strip()
                page_current = re.search(r'Page (.*?) of', page_range).group(1)
                for price in soup.find_all('p', class_='price_color'):
                    if (float(str(price.text)[1:]) > 30.00):
                        book_parent_container = price.parent.parent
                        book_href.append('/catalogue/category/books/historical-fiction_4/{0}'.format(book_parent_container.find('h3').find('a')['href']))
        for href in book_href:
            task = asyncio.ensure_future(FetchBookInfo(href, session))
            tasks.append(task)

            #responses = await asyncio.gather(*tasks)
            fivestar_href_List = await asyncio.gather(*tasks)

    await session.close()
    return headers, fivestar_href_List

async def FetchInspirationalQuotes():
    quote_details = []
    header = [
        'Quote',
        'Author'
    ]
    async with aiohttp.ClientSession('https://quotes.toscrape.com/') as session:
        for i in range(1, 3):
            async with session.get('/tag/inspirational/page/{0}/'.format(i)) as resp:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                tags_parent = soup.find_all('div', class_='quote')
                for item in tags_parent:
                    print('[FetchBookInfo] fetching {0}'.format(item.find('span', class_='text').text))
                    quote_details.append(
                        {
                        'Quote': item.find('span', class_='text').text,
                        'Author': item.find('small', class_='author').text
                        }
                    )

    await session.close()
    return header, quote_details
    
async def FetchFriendshipQuotes():
    author_detail_list = []
    author_href = []
    header = [
        'Author',
        'Date of Birth',
        'Location of Birth',
        'Description'
    ]
    tasks = []
    async with aiohttp.ClientSession('https://quotes.toscrape.com/') as session:   
        async with session.get('/tag/friendship/page/{0}/'.format(1)) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            tags_parent = soup.find_all('div', class_='quote')
            for quote in tags_parent:
                author_href.append(
                    [
                        quote.find('small', class_='author').text,
                        quote.find_all('span')[1].find('a')['href'] #in form /author/[author name]
                    ]) 
            for href in author_href:
                task = asyncio.ensure_future(FetchAuthorInfo(href[0], href[1], session))
                tasks.append(task)
                
                author_detail_list = await asyncio.gather(*tasks)
    await session.close()
    return header, author_detail_list
    
async def FetchAllGenres():
    headers = [
        'Genre',
        'Title', 
        'Price', 
        'UPC',
        'Product Type', 
        'Price (excl. tax)', 
        'Price (incl. tax)', 
        'Tax', 
        'Availability', 
        'Number of reviews'
    ]
    tasks = []
    genre_href_list = []
    init_soup = ...
    genre_book_info_list = []
    tasks = []
    async with aiohttp.ClientSession(base_url = 'http://books.toscrape.com/') as session:    
        async with session.get('/index.html') as resp:
            init_soup = BeautifulSoup(await resp.text(), 'html.parser')
            genre_list_container = init_soup.find('ul', class_='nav nav-list').find('ul')
            for genre_container in genre_list_container.find_all('li'):
                genre_href_list.append( [
                    genre_container.find('a').text.strip(), 
                    '/' + genre_container.find('a')['href']]
                )
                #print('/' + genre_container.find('a')['href'])

        for href in genre_href_list:
            #print(str(href[1])[:(len(href[1]) - 10) ] + 'page')
            async with session.get(href[1]) as resp:
                c_soup = BeautifulSoup(await resp.text(), 'html.parser')
                # if multiple pages exists
                if (c_soup.find('li', class_='current') != None):   
                    page_range = c_soup.find_all('li', class_='current')[0].text.strip()
                    page_max = re.search(r'(?<=of ).*', page_range)[0]
                    #print(page_max)
                    for i in range(1, int(page_max) + 1):
                        async with session.get(str(href[1])[:(len(href[1]) - 10) ] + 'page-{0}.html'.format(i)) as resp:
                            c_soup = BeautifulSoup(await resp.text(), 'html.parser')
                            for book_container in c_soup.find_all('h3'):
                                h = book_container.find('a')['href']
                                if ('../../../' in h):
                                    h = '/catalogue' + h[8:]
                                #print('----------------------------------------' + h)
                                task = asyncio.ensure_future(FetchBookInfoWithGenre(href[0], h, session))
                                tasks.append(task)
                else:
                    for book_container in c_soup.find_all('h3'):
                        h = book_container.find('a')['href']
                        if ('../../../' in h):
                            h = '/catalogue' + h[8:]
                        #print(h)
                        task = asyncio.ensure_future(FetchBookInfoWithGenre(href[0], h, session))
                        tasks.append(task)

        genre_book_info_list = await asyncio.gather(*tasks)

    await session.close()
    return headers, genre_book_info_list

async def main():
    #prompt 1
    result_book_five_star = await FetchFiveStar()
    WriteToCSV('book_five_star_books', result_book_five_star[0], result_book_five_star[1])

    #prompt 2
    result_book_historical_fiction = await FetchHistoricalFictionBooks()
    WriteToCSV('book_historical_fiction', result_book_historical_fiction[0], result_book_historical_fiction[1])
    
    #prompt 3
    result_quote_inspirational = await FetchInspirationalQuotes()
    WriteToCSV('quote_inspirational', result_quote_inspirational[0], result_quote_inspirational[1])

    #prompt 4
    result_quote_friendship_author = await FetchFriendshipQuotes()
    WriteToCSV('quote_friendship_author', result_quote_friendship_author[0], result_quote_friendship_author[1])

    #prompt 5
    result_book_by_genre = await FetchAllGenres()
    WriteToCSV('book_by_genre', result_book_by_genre[0], result_book_by_genre[1])

asyncio.get_event_loop().run_until_complete(main())
