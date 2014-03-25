import requests
from bs4 import BeautifulSoup

# Temporarily Get User Credentials, you'll probably want to pass these some other way

username = raw_input("Enter GSA Advantage Username: ")
password = raw_input("Enter GSA Advantage Password: ")
cart_number = raw_input("Enter the Cart Number you wish to display: ")

# Set some other things, like the login url for GSA Advantage
gsa_login_url = "https://www.gsaadvantage.gov/advantage/main/login.do"
gsa_login_post_url = "https://www.gsaadvantage.gov/advantage/main/login_in.do"
gsa_retrieve_cart_url = "https://www.gsaadvantage.gov/advantage/parkcart/retrieve_parkcart.do"


# We'll use requests to login and get to the cart page
s = requests.Session()

# Quick script to get the token of the session so that we can login
def token_get(s):
  page = s.get(gsa_login_url).text
  soup = BeautifulSoup(page)
  #print soup.title
  token_tag = soup.find('input', attrs={'name':'org.apache.struts.taglib.html.TOKEN', 'type':'hidden'})
  return token_tag['value']

# Setting the payload for the login
login_payload = {
  "userName": username,
  "password": password,
  "mapName": "",
  "map": "forgotPassword",
  "addressMap": "false",
  "productOID": "",
  "org.apache.struts.taglib.html.TOKEN": token_get(s),
}

# We'll login now
s.post(gsa_login_post_url, data=login_payload)


# We'll now get the content of the cart
cart_payload = {
  'cartNumber': cart_number,
  'cartPassword': "",
  'retrieveCart': "true"
}

cart_page = s.post(gsa_retrieve_cart_url, data=cart_payload).text
soup = BeautifulSoup(cart_page)
product_table = soup.find('table', attrs={'class':'sectionpanel4'}).find('table', attrs={'class':'greybox'}).find_all('tr')

for row in product_table:
  if row.find('th'):
    # We're going to skip if this is a table header because it doesn't contain product info
    pass
  else:
    product_name = row.find_all('td')[1].string
    product_url = row.find('a')['href']
    product_num = row.find('a').string

    # We'll just print out some info here
    print "Product Name: %s" % product_name
    print "Product URL: %s" % product_url
    print "Product Number: %s" % product_num
