#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Powerfull proxy scraper bot
# Scrapes & Sends proxies to Telegram Topics
# By KourvA (github.com/Kourva/AnonProxies)


# Standard imports
import os
import random
import time
import json
from typing import Union, ClassVar, NoReturn, Optional, List, Dict, Any

# Third-party imports
import telebot

# Internal imports
from proxy import ProxyEngine
from helper import User, convert_epoch


# Initialize the bot
with open("src/credential.json", "r") as token:
    try:
        # Load json credential from file
        credential: Dict[str, Union[str, int]] = json.load(token)

        # Initialize admin id
        admin: int = credential["Admin"]

        # Initialize Telegram Topic id and it's threads ids
        topic: str = credential["Topic"]
        vless_thread_id: int = credential["Vless"]
        vmess_thread_id: int = credential["Vmess"]
        socks5_thread_id: int = credential["Socks5"]
        trojan_thread_id: int = credential["Trojan"]
        mtproto_thread_id: int = credential["Mtproto"]
        shadowsocks_thread_id: int = credential["ShadowSocks"]

        # Initialize the bot and get bot detail
        bot: ClassVar[Any] = telebot.TeleBot(credential["Token"])
        me: ClassVar[Any] = bot.get_me()

        # Print working message
        print(f"\33[1;36m::\33[m {me.first_name} is running with id {me.id}")

    except Exception as error:
        raise SystemExit(f"Error while initializing bot!\nFull log:\n\n{error}")


# Start command handler
@bot.message_handler(func=lambda x:x.text in ["bot", "ping"] and str(x.chat.id) in [admin, topic])
def start_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Start command handler to handle start | bot | ping commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Send typing action to user
    bot.send_chat_action(
        chat_id=message.chat.id, 
        action="typing"
    )
    # Send message to user (reply)
    bot.reply_to(
        message=message, 
        text=f"Hi Developer. I'm Online"
    )


# Help command handler
@bot.message_handler(func=lambda x:x.text in ["help", "usage"] and str(x.chat.id) in [admin, topic])
def help_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Help command handler to handle start | usage commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Send typing action to user
    bot.send_chat_action(
        chet_id=message.chat.id,
        action="typing"
    )
    # Send message to user (reply)
    bot.reply_to(
        message=message, 
        text=(
            "Here is some commands:\n"
            "update: Update proxy database\n"
            "start | bot | ping: Ping the bot\n"
            "vl | vless: Get Vless proxy\n"
            "vm | vmess: Get Vmess proxy\n"
            "tr | trojan: Get Trojan proxy\n"
            "ss | shadowsocks: Get ShadowSocks proxy\n"
            "mt | mtproto: Get MTproto proxy\n"
            "s5 | socks5: Get Socks5 proxy\n"
        )
    )


# Update command handler
@bot.message_handler(func=lambda x:x.text in ["update", "updatedb"] and str(x.chat.id) in [admin, topic])
def update_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Update command handler to handle update | updatedb commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Updating database... This can takes up to 1 minute!"
    )

    # Get last update date in epoch time and format it
    last_update: str = convert_epoch(
        os.path.getmtime("src/data.txt")
    )

    # Initialize Proxy Engine
    engine: ClassVar[Any] = ProxyEngine()

    # Update database
    if engine.proxy_fetcher():
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=prompt.message_id,
            text=f"Databases updated!\nPrevious update: {last_update}"
        )


# Vless command handler
@bot.message_handler(func=lambda x:x.text in ["vl", "vless"] and str(x.chat.id) in [admin, topic])
def vless_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Vless command handler to handle vl | vless commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = vless_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading vless proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.proxy_parser()

    # Get vless proxies & shuffle them
    vless_proxies: List[str] = engine.result["vless"]
    random.shuffle(vless_proxies)

    # Send proxies in 5 pairs in total 100 proxies
    try:
        for i in range(0, len(vless_proxies[:100]), 5):
            # Get pair proxies from list
            proxy_list: List[str] = vless_proxies[i:i+5]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Send paired proxies to Topic -> vless thread            
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of Vless proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2"
            )

            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading vless proxies... Done"
        )
                

# Vmess command handler
@bot.message_handler(func=lambda x:x.text in ["vm", "vmess"] and str(x.chat.id) in [admin, topic])
def vmess_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Vmess command handler to handle vm | vmess commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = vmess_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading vless proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.proxy_parser()

    # Get vmess proxies & shuffle them
    vmess_proxies: List[str] = engine.result["vmess"]
    random.shuffle(vmess_proxies)

    try:
        # Send proxies in 5 pairs in total 100 proxies
        for i in range(0, len(vmess_proxies[:100]), 5):
            # Get pair proxies from list
            proxy_list: List[str] = vmess_proxies[i:i+5]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Send paired proxies to Topic -> vmess thread
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of Vmess proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2"
            )

            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading vmess proxies... Done"
        )


# Trojan command handler
@bot.message_handler(func=lambda x:x.text in ["tr", "trojan"] and str(x.chat.id) in [admin, topic])
def trojan_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Trojan command handler to handle tr | trojan commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = trojan_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading trojan proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.proxy_parser()

    # Get trojan proxies & shuffle them
    trojan_proxies = engine.result["trojan"]
    random.shuffle(trojan_proxies)

    try:
        # Send proxies in 5 pairs in total 100 proxies
        for i in range(0, len(trojan_proxies[:100]), 5):
            # Get pair proxies from list
            proxy_list: List[str] = trojan_proxies[i:i+5]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Send paired proxies to Topic -> trojan thread
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of Trojan proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2"
            )
            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading trojan proxies... Done"
        )


# Shadow Socks command handler
@bot.message_handler(func=lambda x:x.text in ["ss", "shadowsocks"] and str(x.chat.id) in [admin, topic])
def shadowsocks_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    ShadowSocks command handler to handle ss | shadowsocks commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = shadowsocks_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading shadowsocks proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.proxy_parser()

    # Get shadowsocks proxies & shuffle them
    ss_proxies = engine.result["shadowsocks"]
    random.shuffle(ss_proxies)

    try:
        # Send proxies in 5 pairs in total 100 proxies
        for i in range(0, len(ss_proxies[:100]), 5):
            # Get pair proxies from list
            proxy_list: List[str] = ss_proxies[i:i+5]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Send paired proxies to Topic -> shadow socks thread
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of Shadow Socks proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2"
            )

            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading shadowsocks proxies... Done"
        )


# Socks5 command handler
@bot.message_handler(func=lambda x:x.text in ["s5", "socks5"] and str(x.chat.id) in [admin, topic])
def socks5_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Socks5 command handler to handle s5 | socks5 commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = socks5_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading socks5 proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.fetch_socks_5()

    # Get socks5 proxies & shuffle them
    socks_proxies = engine.result["socks5"]
    random.shuffle(socks_proxies)

    try:
        # Send proxies in 10 pairs in total 100 proxies
        for i in range(0, len(socks_proxies[:100]), 10):
            # Get pair proxies from list
            proxy_list: List[str] = socks_proxies[i:i+10]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Make keyboard inline button for each
            buttons: Dict[str, Dict[str, str]] = {}
            for index, value in enumerate(proxy_list, start=1):
                buttons[f"⁀➴ Proxy {index}"] = {"url": f"t.me/socks?server={value.split(':')[0]}&port={value.split(':')[1]}"}

            # Initialize buttons (10 buttons in 2 rows)
            Markups = telebot.util.quick_markup(buttons, row_width=2)

            # Send paired proxies to Topic -> socks5 thread
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of Socks5 proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2",
                reply_markup=Markups
            )

            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading socks5 proxies... Done"
        )


# MtProto command handler
@bot.message_handler(func=lambda x:x.text in ["mt", "mtproto"] and str(x.chat.id) in [admin, topic])
def mtproto_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    MTProto command handler to handle mt | mtproto commands in 
    bot's chat or topic

    Parameters:
        message: typing.ClassVar[Any] = Message object from telegram

    Returns:
        None: typing.NoReturn
    """

    # Get target chat-id & income chat-id & message-thread-id
    chat: str = message.chat.id
    target_chat_id: str = topic
    target_message_thread_id: int = mtproto_thread_id

    # Send waiting prompt
    prompt: ClassVar[Any] = bot.reply_to(
        message=message, 
        text="Uploading mtproto proxies... Please be patient"
    )

    # Initialize Proxy Engine and fetch proxies
    engine: ClassVar[Any] = ProxyEngine()
    engine.fetch_mtproto()

    # Get mtproto proxies & shuffle them
    mtproto_proxies = engine.result["mtproto"]
    random.shuffle(mtproto_proxies)

    try:
        # Send proxies in 10 pairs in total 100 proxies
        for i in range(0, len(mtproto_proxies[:100]), 10):
            # Get pair proxies from list
            proxy_list: List[str] = mtproto_proxies[i:i+10]

            # Add new line to them. just for making them readable
            proxies: str = '\n\n'.join(proxy_list)

            # Make keyboard inline button for each
            buttons: Dict[str, Dict[str, str]] = {}
            for index, value in enumerate(proxy_list, start=1):
                buttons[f"⁀➴ Proxy {index}"] = {"url": value}

            # Initialize buttons (10 buttons in 2 rows)
            Markups = telebot.util.quick_markup(buttons, row_width=2)

            # Send paired proxies to Topic -> shadow socks thread
            bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=target_message_thread_id,
                text=f"જ⁀➴ List of MtProto proxies \(**Copy and Paste**\)\n\n```plaintext\n{proxies}```",
                parse_mode="MarkdownV2",
                reply_markup=Markups
            )

            # Sleep 1 second between them to avoid flood limit from telegram
            time.sleep(1)

    except IndexError:
        # Pass index error and break the loop
        pass

    finally:
        # Edit prompt message
        bot.edit_message_text(
            chat_id=chat,
            message_id=prompt.message_id,
            text=f"Uploading mtproto proxies... Done"
        )

if __name__ == "__main__":
    try:
        # Run the bot on polling mode
        bot.infinity_polling(
            skip_pending=True
        )

    except KeyboardInterrupt:
        # Exit the bot on keyboard interrupt
        raise SystemExit(f"\33[1;31m::\33[m Interrupted by user.")
