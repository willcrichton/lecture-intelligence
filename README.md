# Lecture Intelligence

A tool for scraping and analyzing lecture video viewing data from Panopto.

## Setup

First, make sure you have Python 3.6 or above installed. Then run:

```
git clone https://github.com/willcrichton/lecture-intelligence
cd lecture-intelligence
pip3 install -r requirements.txt
cd lib
FLASK_APP=server flask run
```

Keep the server running in a terminal tab while proceeding to the next steps.

### Scraping Panopto data

For this step, you will need to use Google Chrome.

1. Go to `chrome://extensions` and enable "Developer mode" (top-right).
2. Click "Load unpacked" (top-left) and select the "panopto-scraper" directory in this repository.
3. Go to [Panopto](https://stanford-pilot.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#isSharedWithMe=true). Find a video from the course you want to analyze, and click the course link in the thumb nail, e.g. "Fall 2019 - Programming Languages".
4. Click the "V" icon in the top right of the browser.
5. Your data has now been populated and anonymized into the `data` directory of this repository.

### Analytics dashboard

Go to [`http://localhost:5000`](http://localhost:5000). Your results await!
