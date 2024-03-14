# flake8: noqa: E501
import json
import os
import pandas as pd
import csv
from typing import List, Optional, Tuple, Union
import string

import requests

from lagent.actions.base_action import BaseAction
from lagent.schema import ActionReturn, ActionStatusCode
from lagent.actions.parser import BaseParser, JsonParser


class Amap(BaseAction):
    """AMap plugin for looking up map information."""
    def __init__(self,
                key: Optional[str] = None,
                description: Optional[dict] = None,
                k: int = 10,
                search_type: str = 'search',
                name: Optional[str] = None,
                enable: bool = True,
                disable_description: Optional[str] = None) -> None:
        super().__init__(description, name, enable, disable_description)
        key = '60657a274bd05b79436aed700319947d'
        self.key = key
        self.search_type = search_type
        self.k = k
        self.base_url = 'https://restapi.amap.com/v3/staticmap'
    
    def run(self, query: str) -> ActionReturn:
        """Return the search response.

        Args:
            query (str): The search content.

        Returns:
            ActionReturn: The action return.
        """
        tool_return = ActionReturn(url=None, args=None, type=self.name)
        status_code, response = self.map(
            query)
        #convert search results to ToolReturn format
        if status_code == -1:
            tool_return.errmsg = response
            tool_return.state = ActionStatusCode.HTTP_ERROR
        elif status_code == 200:
            tool_return.result = response
            tool_return.state = ActionStatusCode.SUCCESS
        else:
            tool_return.errmsg = str(status_code)
            tool_return.state = ActionStatusCode.API_ERROR
        return tool_return

    def map(self, long_text: str) -> dict:
        csv_filename = '/root/code/lagent/lagent/actions/Shanghai.csv'
        with open(csv_filename, 'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            df = pd.DataFrame({})
            for field_info in csv_reader:
                if field_info[0] in long_text:
                    df=df._append({'name': field_info[0], 'lon': float(field_info[1]), 'lat': float(field_info[2])}, ignore_index=True)
        markers = []
        letters = string.ascii_uppercase
        for index, row in df.iterrows():
            marker_letter = letters[index]
            markers.append(f"mid,0xFF0000,{marker_letter}:{row['lon']},{row['lat']}")
        
        parameters = {
            'zoom': '9',
            'size': '516*516',
            'markers': '|'.join(markers),  # 将所有标记组合在一起
            'key': self.key
        }
        response = requests.get('https://restapi.amap.com/v3/staticmap', params=parameters)
        return response.status_code, response.url



        