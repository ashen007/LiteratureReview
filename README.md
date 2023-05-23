# LiteratureReview

scrapper for various science databases, supported databases are IEEE Xplore, Science Direct and
ACM. theses scrapping bots will retrieve link to each search results aka paper, title and some
other meta-data such as keywords and abstract, type of paper (conference, journal ect.) which
useful to do the systematic literature review process make easy.

_*If you find this work usefully, put a star on this repo ⭐*_

# Prerequisites

- python 3.9 or higher
- Chrome browser
- Chrome web driver which matches your Chrome version. download from [here](https://chromedriver.chromium.org/downloads/)

# How to use

1) go to the official site (advance search page), create a search query using their form,
   <P><h3>Science Direct</h3>
   <img height="300" src="demo\science direct adv search.jpg" width="600"/>
   <img height="300" src="demo\science direct adv search string.jpg" width="700"/></p>
   <P><h3>IEEE Xplore</h3>
   <img height="300" src="demo\ieee adv search string.jpg" width="700"/>
   <P><h3>ACM</h3>
   <img height="900" src="demo\acm adv search string.jpg" width="350"/></p>
2) copy that query text and use it to configure the tool
3) clone the repo (create virtual environment is recommended way) and complete the configuration
   can use a single bot or all the bots at one by one configuration.

```shell
git clone https://github.com/ashen007/LiteratureReview.git
```   
- all bots with single configuration

```json
{
  "BINARY_LOCATION": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "EXECUTABLE_PATH": "D:\\chromedriver.exe",
  "SCIDIR": {
    "search_term": "insert query string here",
    "link_file_save_to": "./temp/scidir_search_term.json",
    "abs_file_save_to": "./abs/scidir_search_term.json",
    "use_batches": true,
    "batch_size": 8,
    "keep_link_file": true
  },
    "ACM": {
    "search_term": "insert query string here",
    "link_file_save_to": "./temp/acm_search_term.json",
    "abs_file_save_to": "./abs/acm_search_term.json",
    "use_batches": true,
    "batch_size": 8,
    "keep_link_file": true
  },
    "IEEE": {
    "search_term": "insert query string here",
    "link_file_save_to": "./temp/ieee_search_term.json",
    "abs_file_save_to": "./abs/ieee_search_term.json",
    "use_batches": false,
    "batch_size": 8,
    "keep_link_file": true
  }
}      
```

- or can use one bot as well

```json
{
  "BINARY_LOCATION": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "EXECUTABLE_PATH": "D:\\chromedriver.exe",
  "SCIDIR": {
    "search_term": "insert query string here",
    "link_file_save_to": "./temp/scidir_search_term.json",
    "abs_file_save_to": "./abs/scidir_search_term.json",
    "use_batches": true,
    "batch_size": 8,
    "keep_link_file": true
  }
}
```

- config `BINARY_LOCATION`
    use a path to chrome.exe file location

- config `EXECUTABLE_PATH`
    use a path where you download and extract the Chrome web driver

4) install dependencies run the main.py

```shell
pip install -r ./requirements.txt
```

```shell
python main.py

```

5) that's it
6) save results into excel workbook, automatically saved into `./SLR.xlsx` file.
```python
   from src.utils import to_excel
   to_excel({"acm":'./abs/acm_search_term.json', "ieee": './abs/ieee_search_term.json', "science_direct": './abs/scidir_search_term.json'})
```
