import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scrape_product_details(url, driver: webdriver.Firefox, wait: WebDriverWait):
    # Navigate to the product page
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

    product_name = driver.find_element(By.CSS_SELECTOR, 'p.css-1rw23u7.enp2lf70').text
    product_name_long = driver.find_element(By.CSS_SELECTOR, 'p.css-qry54b.enp2lf70').text

    # Get the product description
    product_description = driver.find_element(By.CSS_SELECTOR, 'p.css-1cuz951.enp2lf70').text

    # Get the text of the third anchor element matching the specified CSS selector
    short_description = driver.find_elements(By.CSS_SELECTOR, 'a.css-19c7qaj.enp2lf70')[2].text

    # Get the text of the first matching anchor element with the specified CSS selector
    country = driver.find_element(By.CSS_SELECTOR, 'a.css-1bhjbql.enp2lf70').text

    # Find the first three elements matching the specified CSS selector and extract their 'aria-label' attribute
    taste_clocks = [element.get_attribute('aria-label') for element in driver.find_elements(By.CSS_SELECTOR, 'p.css-5frrl2.e78l9nd0')[:3]]

    # Grapes
    grapes = driver.find_element(By.CSS_SELECTOR, 'p.css-1l8wu88.enp2lf70').text
    
    # Write the product description to a text file
    with open('product_descriptions.txt', 'a') as f:
        f.write(product_name + ', ' + product_name_long + '\n')
        f.write(product_description + '\n')
        f.write('- ' + short_description.lower().capitalize() + '\n')  # Write the anchor text
        f.write('- ' + grapes.lower().capitalize() + '\n')  # Write the anchor text


       # Write the taste_clocks, prefixed with '- '
        for taste_clock in taste_clocks:
            f.write('- ' + taste_clock + '\n')

        f.write('- ' + country + '\n')  # Write the first anchor text

        f.write('---' + '\n')  # Write the separator

def scrape_product_links(url):
    # Set options for the driver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(executable_path='/Users/simon.shadman', options=options)
    wait = WebDriverWait(driver, 2)

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
        # Filter out only the ones with id starting with 'tile:'
        product_links = [tag.get_attribute('href') for tag in driver.find_elements(By.TAG_NAME, 'a') if tag.get_attribute('id').startswith('tile:')]

        i = 0
        # Fetch the details of all products
        for product_link in product_links:
            print('Iteration ' + str(i) + '. Processing ' + product_link + '...')
            scrape_product_details(product_link, driver, wait)
            i += 1

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser window
        driver.quit()

# The URL of the webpage
url = 'https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/glasflaska/?pris-fran=90&pris-till=150&sortiment=Fast%20sortiment_eller_Tillf%C3%A4lligt%20sortiment'

# Call the function
scrape_product_links(url)
