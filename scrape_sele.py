import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def scrape_product_links(url):
    # Set options for the driver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(executable_path='/Users/simon.shadman', options=options)

    try:
        # Navigate to the webpage
        driver.get(url)

        # Set the cookie
        cookie = {'name' : 'systembolaget.age', 'value' : '{%22state%22:{%22verified%22:true}%2C%22version%22:0}', 'domain':'.systembolaget.se'}
        driver.add_cookie(cookie)

        # Refresh the page after setting the cookie
        driver.refresh()
        time.sleep(5)

        # Find all the anchor tags in the HTML
        # Filter out only the ones with id starting with 'title:'
        product_links = [tag.get_attribute('href') for tag in driver.find_elements(By.TAG_NAME, 'a') if tag.get_attribute('id').startswith('tile:')]

        # Write the links to a text file
        with open('product_links.txt', 'w') as f:
            for link in product_links:
                f.write(link + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser window
        driver.quit()

# The URL of the webpage
url = 'https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/glasflaska/?pris-fran=90&pris-till=150&sortiment=Fast%20sortiment_eller_Tillf%C3%A4lligt%20sortiment'

# Call the function
scrape_product_links(url)
