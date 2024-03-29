# Scrape Me

The Scrape Me project is made so you can learn web scraping without overloading any external website.

## Run it with Docker

```
docker pull codingforentrepreneurs/scrape-me:latest
docker run -p 8101:8101 --env PORT=8101 codingforentrepreneurs/scrape-me:latest
```

## Run with Python 3.10+

### Installation

```bash
mkdir -p ~/practice
cd ~/practice
git clone https://github.com/codingforentrepreneurs/Scrape-Me
cd Scrape-Me
```

Create an environment and activate it (mac/linux)
```
python3 -m venv venv
source venv/bin/activate
```

Create an environment and activate it (windows)
```
C:Python312\python.exe -m venv venv
venv\Scripts\activate
```

Install the requirements
```
pip install -r requirements.txt
```
> The `Waitress` package is used over Gunicorn so everyone can run the application easily (especially Windows users).


### Usage

```python
python app.py
```
This will run a Python-based web server with a default port at 8101.

or
```python
python app.py 8001
```
or
```python
PORT=8002 python app.py
```


### HTML

Each template within the `html_templates` directory corresponds to a URL path:

For example:

- `html_templates/index.html` corresponds to `http://localhost:8101/`
- `html_templates/soup.html` corresponds to `http://localhost:8101/soup/`
- `html_templates/timestamp/index.html` corresponds to `http://localhost:8101/timestamp/`

Assuming the Scrape Me server is running on `http://localhost:8101/`, you can run commands like:


```
curl http://localhost:8101/
curl http://localhost:8101/soup/
curl http://localhost:8101/timestamp/
```

If you installed Python requests (which is optional), you can then run requests like:

```
import requests
r = requests.get('http://localhost:8101/')
r.text
```


### Single Page Django App

This repo also serves as a practical example of creating a single-page Django application. In this case, Django will automatically serve HTML documents (with support for the Django Template Engine) and automatically create url paths for each HTML document.

To learn more about building single-page Django applications, watch https://www.youtube.com/watch?v=F91BTQnxV6w

Waitress is used over Gunicorn to allow Windows users to run the application easily.


## Contributing
If you'd like to contribute, please fork the repository create a feature, and submit a pull request.

The goal is to make local and dynamic web server so it's easier to practice web scraping without getting blocked or creating issues with public websites. 