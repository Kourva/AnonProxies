#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Standard imports
import base64
import json
import re
from typing import Union, NoReturn, Optional, List, Dict, Any

# Third-party imports
import requests


class ProxyEngine:
    """
    Proxy Engine class to work with proxies
    """
    def __init__(self) -> NoReturn:
        """
        Initial method to set result variable

        Returns:
            None: typing.NoReturn
        """
        self.result: Dict[str, List[str]] = {
            "vmess": [],
            "vless": [],
            "trojan": [],
            "shadowsocks": [],
            "mtproto": [],
            "socks5": []
        }

    def base64_decoder(self, data: str) -> Union[str, NoReturn]:
        """
        Decoder method to decode base-64 encoded data

        Parameters:
            data: str = base-64 encoded data

        Returns:
            Union[str, NoRetun] = Decoded string or None in failure
        """
        try:
            # Decode data
            return base64.b64decode(data).decode("utf-8")

        except Exception as error:
            # Exit in failure
            raise SystemExit(f"Issue in decoding Data using base-64 method\nFull log:\n\n{error}!")

    def source_loader(self) -> Dict[str, Union[None, str]]:
        """
        Source loader method to get list of proxy sources

        Returns:
            Sources: Dict[str, Union[None, str]] = All sources
        """
        try:
            # Load services
            with open("src/services.json", "r") as data:
                return json.load(data)

        except FileNotFoundError:
            # Exit in file not found error
            raise SystemExit(f"No service file found in src/services.json!")

        except Exception as error:
            # Exit on failure
            raise SystemExit(f"Issue in loading source data\nFull log:\n\n{error}!")

    def proxy_loader(self) -> str:
        """
        Proxy loader method to get all saved proxies

        Returns:
            Proxies: str = All Proxies
        """
        try:
            # Load proxies
            with open("src/data.txt", "r") as data:
                return data.read()

        except FileNotFoundError:
            # Exit in file not found error
            raise SystemExit(f"No data file found in src/data.txt!")

        except Exception as error:
            # Exit on failure
            raise SystemExit(f"Issue in loading proxy data\nFull log:\n\n{error}!")

    def proxy_fetcher(self) -> bool:
        """
        Proxy fetcher method to get proxies from services

        Returns:
            bool = True on success and False on failure
        """
        try:
            # Make temporary variable to store data
            temp_data: str = ""

            # Loop through sources and get data
            for item in self.source_loader():
                # Print current state on terminal
                print(f"Getting sources -> {': '.join(item['source'].split('/')[3:5])}")

                # Open session and make request to target
                with requests.Session() as sesstion:
                    response: ClassVar[Any] = sesstion.get(url=item['source']).text

                    if item['encryption']:
                        temp_data += self.base64_decoder(response)
                    else:
                        temp_data += response

            # Save the proxies into file
            with open("src/data.txt", "w") as data:
                data.write(temp_data)
                print("\33[1;36m::\33[m Result saved in src/data.txt successfully!")

            # Return true on success
            return True

        except Exception as error:
            # Return false and print error message on failure
            print(f"Issue in fetching proxies\nFull log:\n\n{error}!")
            return False

    def proxy_parser(self) -> NoReturn:
        """
        Proxy parser method to parse proxies and update main database (self.result)

        Returns:
            None: typing.NoReturn
        """
        # Fetch proxies
        proxies: str = self.proxy_loader()

        # Update main result 
        self.result["vless"] += re.findall(r"vless://.*", proxies)
        self.result["vmess"] += re.findall(r"vmess://.*", proxies)
        self.result["trojan"] += re.findall(r"trojan://.*", proxies)
        self.result["shadowsocks"] += re.findall(r"ss://.*", proxies)

    def fetch_socks_5(self) -> NoReturn:
        """
        Fetch socks-5 method to fetch socks-5 proxies and update main database (self.result)

        Returns:
            None: typing.NoReturn
        """
        # URL to request
        url: str = "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"

        # Open a session and send request to url
        with requests.Session() as sesstion:
            response: List[str] = requests.get(url=url).text.split("\n")

            # Add proxies to main result
            self.result["socks5"] = list(map(lambda x:x.split("\r")[0], response))

    def fetch_mtproto(self) -> NoReturn:
        """
        Fetch MTProto method to fetch MTProto proxies and update main database (self.result)

        Returns:
            None: typing.NoReturn
        """
        # URL to request
        url: str = "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json"

        # Open a session and send request to url
        with requests.Session() as sesstion:
            response: List[Dict[str, Union[str, int]]] = requests.get(url=url).json()

            # Add proxies to main database
            # Using map function to pick host, port, secret from json data and change them to sting
            self.result["mtproto"] = list(
                map(
                    lambda x: f"tg://proxy?server={x['host']}&port={x['port']}&secret={x['secret']}", 
                    response
                )
            )
