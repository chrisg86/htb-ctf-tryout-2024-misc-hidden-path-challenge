# HTB CTF - Try Out - 2024 - Misc: Hidden Path challenge

> Legends speak of the infamous Kamara-Heto, a black-hat hacker of old who rose to fame as they brought entire countries to their knees. Opinions are divided over whether the fabled figure truly existed, but the success of the team surely lies in the hope that they did, for the location of the lost vault is only known to be held on what remains of the NSA's data centres. You have extracted the source code of a system check-up endpoint - can you find a way in? And was Kamara-Heto ever there?

## Overview
Upon spinning up the docker container, you retrieve a web link that exposes a web interface where you can select different system commands and the REST API returns the output through a index lookup. Seems like all we can send to the `/server_status` endpoint are choices, but upon further inspection of the code it seems there is another way.

When destructuring the body from the request, they use the following syntax which seems odd:
```js
const { choice,ㅤ} = req.body;
```

Why the trailing comma? Coinsidence? What if there was an invisible character that is interpreted as a legit variable name in javascript? Upon inspecting the character it indeed is the `U+3164` or "Hangul Filler"

The Unicode character U+3164 is ㅤ, which is known as Hangul Filler. It's a Korean character used as a placeholder, essentially representing an empty space. It's often employed in text tricks or to create visually blank nicknames. 

Then it quickly becomes clear that there is a hidden second key accepted from `req.body`, which we can exploit to inject custom commands, as it is also used on the last item inside the `commands` array.

```js
const commands = [
    'free -m',
    'uptime',
    'iostat',
    'mpstat',
    'netstat',
    'ps aux',ㅤ // <-- Here after the trailing comma
];
```

In order to execute it, we have to send the correct index into the array and some command that will fetch the flag for us:

```http
POST /server_status HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: http://<host>:<port>

choice=6&%E3%85%A4=cat%20flag.txt
```

Which equals `choice=6&ㅤ=cat flag.txt`

Let's script this in order to retrieve the flag.

## How to run
Run via `HOST=1.1.1.1 PORT=11111 uv run python main.py` and provide `HOST` and `PORT`:

```
HOST=1.1.1.1 PORT=11111 uv run python main.py
```

You can probably skip `uv` alltogether if you want and run with `python` directly.

## Dependencies

- `requests` for making HTTP requests
