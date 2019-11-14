# Video habits

## Installation

First, make sure you have Python 3.6 or above installed. Then run:

```
pip3 install -r requirements.txt
```

### Scraping Canvas data

1. Go to `lib` directory and run `FLASK_APP=scrape.py flask run`
2. Go to `chrome://extensions` and enable "Developer mode" (top-right).
3. Click "Load unpacked" and select the "panopto-scraper" directory.
4. Go to [Panopto](https://stanford-pilot.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#isSharedWithMe=true) and click through to a listing of all your course videos.
5. Click the "V" icon in the top right of the browser.
6. Your data has now been populated and anonymized into the `data` directory of this repository.

### Analytics dashboard

1. Go to `lib` directory and run `FLASK_APP=dashboard.py flask run`
2. Go to [`http://localhost:5000`](http://localhost:5000).
