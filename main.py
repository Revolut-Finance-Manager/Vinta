import requests
import sys

# dictionary country name to country code url
# webmap should have the following structure:
# it is a dictionary of lists of dictionaries
# where for each key we have a list of dictionaries
# where each dictionary is an option than comes after the key
# if the option is a leaf, then the value of the dictionary is ""
# {
#   "section1": {
#     "option1": {"option1":""}, ... }, "option2":{}}, ... 
#   },
#    "section2": { ... }
#   }
webmap = {}
country_code = {
    "United States": ".us",
    "United Kingdom": ".co.uk",
    "Portugal": ".pt",
    "Germany": ".de",
    "Spain": ".es"
}
# function to get all available urls from the website
def get_content(url):
    # get content from url
    r = requests.get(url)
    # return content
    return r.content

    
# given an url like "/section1/section2/section3/section4"
# update the webmap dictionary so that each section is a key to the next section
def divide_url(url):
    # remove the first "/" from the url
    url = url[2:]
    # print(url)
    # split url by "/"
    sections = url.split("/")
    #print(sections)
    temp_dict = webmap
    prev_section = ""
    for i in range(len(sections)):
        key = sections[i]
        if key not in temp_dict:
            if prev_section == "":
                webmap[key] = {}
            else:
                temp_dict[key] = {}
        prev_section = key
        #print(prev_section)
        #print(webmap)
        temp_dict = temp_dict[key]
        #print(temp_dict)




    


def main(country):
    url = "https://vinted" + country_code[country]
    content = str(get_content(url))
    # get ids values from content after {"id": and before ,"
    # ids = [x.split(',')[0] for x in content.split('{"id":')]
    # split content by {"id":, then get "title": 
    # and split by "," to get the title
    urls = [x.split('"url":')[1].split(',')[0] for x in content.split('{"id":') if '"url":' in x]
    # update webmap dictionary
    for url in urls:
        try:
            divide_url(url)
        except:
            continue
    # remove key from webmap if it is empty
    
    import copy
    # print webmap dictionary
    # print the keys in webmap 
    # for each key in webmap, print the keys in the value
    temp = copy.deepcopy(webmap)
    for key in temp.keys():
        if key == "www.vinted.pt" or key == "ttps:" or key == "images1.vinted.net":
            del webmap[key]
        else:
            print(key)
            print(webmap[key].keys())
    print(webmap)
    # create a dictionary with the id as key and the title as value
    file = open("vinted" + country_code[country] + ".html", "w")
    file.write(str(content))
    file.close()

if __name__ == "__main__":
    # get country as argument
    country = sys.argv[1]
    main(country)