<div align="center">
    <h3><b>ᨒ AnonProxies ᨒ</b></h3>
    <p>˗ˏˋ Proxy scraper bot to Scrape and send proxies to Telegram topics automatically ˎˊ˗</p>
</div>

<br>

# ⿻ About AnonProxies
There are many [proxy collectors](https://github.com/search?q=proxy%20collectors&type=repositories) and scrapers on GitHub that scrape proxies from Telegram channels or other sources. It is a good idea to have a Telegram bot that can collect all of them for you and post them in a group. As you may know, Telegram has [Topics](https://telegram.org/blog/topics-in-groups-collectible-usernames#topics-in-groups), which means you can create sub-topics such as one for vless proxy and another for trojan.

<img align="right" src="https://github.com/Kourva/AnonProxies/assets/118578799/306e986c-7c63-42b2-917d-14fa80c60416" width=350>

This bot collects all proxies from different sources and sends them to your chosen topic. All you need to do is give the bot a few commands to tell it what to do. You can open `src/services.json` to see which sources are being used by the bot (you can also use their tools).

The bot will send proxies in pairs of 10 to make it easy to copy and paste proxies into apps like V2ray-Ng. Additionally, some proxies like Mtproto and Socks5 have inline buttons to connect to them directly within Telegram.

I hope you find this project useful! If you do, I kindly invite you to show your support by starring the project. Your encouragement means a lot to me. Thank you!

Let's begin the installation process...


# ⿻ Installation
1. **Clone repository**:
    ```bash
    git clone https://github.com/Kourva/AnonProxies
    ```
2. **Navigate to Anon Proxies**:
    ```bash
    cd AnonProxies
    ```
3. **Make Virtual Environment**:
    ```bash
    virtualenv venv && source venv/bin/activate
    ```
5. **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

# ⿻ Configuration
Navigate to `src/credintial.json` and fill required values:
```json
{
    "Token": "1234567890:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Admin": "1234567890",
    "Topic": "-1001234567890",
    "Vless":1, 
    "Vmess":2,
    "Trojan":3,
    "Socks5":4,
    "Mtproto":5,
    "ShadowSocks":6
}
```
> Get the token from [bot father](https://t.me/botfather)<br>
> Put your Chat-ID in Admin section<br>
> Put your Topic group's chat-ID in topic section (Google it if you don't know how)<br>
> Put your topic's thread id in other sections. if your topic section X url is this: `t.me/your_topic/12` (**12 is thread id for section X**)

# ⿻ Running bot
After configuration, run bot using python:
```bash
python bot.py
```
You can also use proxychains and run it with tor or any other proxy:
```bash
proxychians -q python bot.py
```

# ⿻ Any idea or Issue ?
You can submit your ideas and issues in [issue section](https://github.com/Kourva/AnonProxies/issues). This project is licensed under the [**MIT License**](https://opensource.org/license/mit/). You are welcome to access the code, use it, and make modifications, all in accordance with the terms of the MIT License.
