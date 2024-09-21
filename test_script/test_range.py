import requests

url = "http://127.0.0.1:5000/download/files/Hello_World!!!.txt"
headers = {
    "Range": "bytes=0-8"
}

response = requests.get(url, headers=headers)

file_range = response.headers.get("Content-Range").split("/")[-1]
print(f"File range: {file_range}")

string = b""
parties = int(file_range) / 10
parties = type(parties) == float and int(parties) + 1 or int(parties)


start = 0
for i in range(parties):
    end = start + 10
    end = end > int(file_range) and int(file_range) or end
    headers = {
        "Range": f"bytes={start}-{end}"
    }
    response = requests.get(url, headers=headers)
    string += response.content
    start = end

print(string.decode("utf-8"))