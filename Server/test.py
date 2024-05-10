import requests

url = 'https://minecraft-analysis-422617.oa.r.appspot.com/download'
params = {
    'videoPath': 'data/10.0/cheeky-cornflower-setter-02e496ce4abb-20220421-093149.mp4'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    with open('download.zip', 'wb') as f:
        f.write(response.content)
    print('Download successful.')
else:
    print('Error:', response.status_code)
