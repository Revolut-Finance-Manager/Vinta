import requests
import sys
import copy
import os

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
    "Austria": ".at",
    "Belgium": ".be",
    "Canada": ".ca",
    "Czech Republic": ".cz",
    "Germany": ".de",
    "Spain": ".es",
    "France": ".fr",
    "Hungary": ".hu",
    "Italy": ".it",
    "Lithuania": ".lt",
    "Luxembourg": ".lu",
    "Netherlands": ".nl",
    "Poland": ".pl",
    "Portugal": ".pt",
    "Sweden": ".se",
    "Slowakia": ".sk",
    "United Kingdom": ".co.uk",
    "United States": ".us"
}


# function to get all available urls from the website
def get_content(url):
    # get content from url
    r = requests.get(url)
    # return content
    return r.content

# def write_key_files(key, key_aux):
#         # if file does not exist, create it
#         if not os.path.exists(key + ".txt") and key == "mulher":
#             key_file = open(key + ".txt", "w")
#         else:
#             key_file = open(key + ".txt", "a")
#         key_file.write(key + ":\n")
#         while key_aux != {}:
#             for k in key_aux:
#                 key_file.write("\t" + k + "\n")
#                 if key_aux[key][k] != {}:
#                     key_aux = key_aux[key][k].keys()
#                     write_key_files(k, key_aux)
#                 else:
#                     key_aux = {}



# given an url like "/section1/section2/section3/section4"
# update the webmap dictionary so that each section is a key to the next section
def divide_url(url):
    # remove the first "/" from the url
    url = url[2:]
    # print(url)
    # split url by "/"
    sections = url.split("/")
    temp_dict = webmap
    prev_section = ""
    for i in range(len(sections)):
        key = sections[i]
        if '"' in key :
            key = key[:-1]
        if key == "www.vinted.pt" or key == "ttps:" or key == "images1.vinted.net":
            continue
        else: 
            if key not in temp_dict:
                if prev_section == "":
                    webmap[key] = {}
                    key_file = open("./Vinted Sections MD/" + sections[0] + ".md", "w")
                    key_file.write("- " + key + ":\n")
                else:
                    temp_dict[key] = {}
                    key_file = open("./Vinted Sections MD/" + sections[0] + ".md", "a")
                    key_file.write("\t"*i + "- " + key + "\n")
            prev_section = key
            temp_dict = temp_dict[key]



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
        

if __name__ == "__main__":
    # get country as argument
    country = sys.argv[1]
    main(country)