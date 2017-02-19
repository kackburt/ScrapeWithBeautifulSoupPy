from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re


def get_soup(site_url):
    site_html = urlopen(site_url).read()
    site_soup = BeautifulSoup(site_html)
    return site_soup


def main():

    csv_file = open("pareddata.csv", "w")

    url = 'https://scrapebook22.appspot.com/'

    soup = get_soup(url)

    print
    print "PRINTING PERSON LINKS"
    print

    # only print links which have 'person' in their reference
    for link in soup.findAll("a"):
        # link.attrs gives a list, each entry is a tuple of 2 values, attribute and value.
        # trick to make it more easy to access: turn it into a dictionary
        if 'person' in link['href']:
            person_url = "https://scrapebook22.appspot.com" + link["href"]
            person_soup = get_soup(person_url)
            # we know the Email is in a span, however there might be many spans on the website.
            # fortunately, we can add additonal information about the span we try to find, e.g. the attributes:
            # we know, our span has the attribute: class = "email", so we can insert that in our find() function
            email = person_soup.find("span", attrs={"class": "email"}).string
            gender = person_soup.find("span", attrs={"data-gender": True}).string
            city = person_soup.find("span", attrs={"data-city": True}).string
            age = person_soup.findAll(text=re.compile('Age:(.*)', re.IGNORECASE))
            findage = re.search(r'\d+', str(age))
            #rightage = str(age).replace("[u'Age: ","",1)

            csv_file.write(str(findage.group()) + ";" + gender + ";" + city + ";" + email + "\n")
            print str(findage.group()) + ";" + gender + ";" + city + ";" + email

    csv_file.close()

    print("Parsing done. Goodbye!")

if __name__ == '__main__':
    main()
