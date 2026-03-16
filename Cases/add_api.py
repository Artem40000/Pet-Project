from requests import post


url = "http://localhost:8000/api/add/"
data = {
    "pOne": "-",
    "pTwo": "-",
    "Url": "-",
}


response = post(url, data=data)