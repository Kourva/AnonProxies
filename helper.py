#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Standard imports
from typing import Union, ClassVar, NoReturn, Optional, List, Dict, Any
from datetime import datetime, timedelta


class User:
    """
    User class to get information about user
    """
    def __init__(self, user_data: ClassVar[Any]) -> NoReturn:
        """
        Initial function to get user's data from user object

        Parameters:
            user_data: typing.ClassVar[Any] = User object from telegram

        Returns:
            None: typing.NoReturn
        """
        self.id: int = user_data.id           # Chat ID
        self.fn: str = user_data.first_name   # First name
        self.ls: str = user_data.last_name    # Last name
        self.un: str = user_data.username     # Username

    @property
    def get_name(self) -> str:
        """
        Property function to print the user's name in possible way

        Returns:
            User detail (str): Possible name for user
        """
        return self.fn or self.ln or self.un or self.id


def convert_epoch(epoch_time: float) -> str:
    """
    Function to convert epoch time to one of these formats:
        - Just now
        - X minute ago
        - X hour ago
        - X day ago
        - X week ago

    Parameters:
        epoch_time: float = epoch time 

    Returns:
        output: str = Formatted time
    """

    # Convert epoch time to a date-time object
    date_time: ClassVar[Any] = datetime.utcfromtimestamp(epoch_time)

    # Calculate the time difference from the current time
    time_difference: ClassVar[Any] = datetime.utcnow() - date_time

    # Format the time difference as "x time ago"
    if time_difference.days > 7:
        return f"{time_difference.days // 7} weeks ago"
    elif time_difference.days > 0:
        return f"{time_difference.days} days ago"
    elif time_difference.seconds // 3600 > 0:
        return f"{time_difference.seconds // 3600} hours ago"
    elif time_difference.seconds // 60 > 0:
        return f"{time_difference.seconds // 60} minutes ago"
    else:
        return "just now"
