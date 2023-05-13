from requests_html import HTMLSession

def scrape_product_links(url):
    # Create an HTML Session object
    session = HTMLSession()

    # Define the cookie
    cookies = {'systembolaget.age': '{%22state%22:{%22verified%22:true}%2C%22version%22:0}'}

    try:
        # Send a GET request to the webpage
        response = session.get(url, cookies=cookies)
        # Raise an exception if the GET request was unsuccessful
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
    else:
        # Render the page and wait for 2 seconds to allow JS scripts to load
        response.html.render(sleep=20, cookies=[{'name':'systembolaget.age', 'value': '{%22state%22:{%22verified%22:true}%2C%22version%22:0}', 'domain': '.systembolaget.se'}])

        # Find all the anchor tags in the HTML
        # Filter out only the ones with id starting with 'title:'
        product_links = [tag.attrs['href'] for tag in response.html.find('a')]

        # Write the links to a text file
        with open('product_links.txt', 'w') as f:
            for link in product_links:
                f.write(link + '\n')

# The URL of the webpage
url = 'https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/glasflaska/?pris-fran=90&pris-till=150&sortiment=Fast%20sortiment_eller_Tillf%C3%A4lligt%20sortiment'

# Call the function
scrape_product_links(url)
