"""
File: mk-deepseek-response.py
Author: Chuncheng Zhang
Date: 2025-07-08
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-07-08 ------------------------
# Requirements and constants
from ollama import Client, ChatResponse
from rich import print, inspect


# %% ---- 2025-07-08 ------------------------
# Function and class
FIXED_PROMPT = '''
请用400字的markdown形式进行回复，
格式要求是从二级标题开始。
'''


class MyOllama:
    host = 'http://172.18.116.140:11434'
    model_name = 'deepseek-r1:32b'
    msg_template = {'role': 'user', 'content': f'{FIXED_PROMPT}:'}

    def mk_msg(self, content: str):
        msg = {}
        msg.update(self.msg_template)
        msg['content'] += content
        return msg


# %% ---- 2025-07-08 ------------------------
# Play ground
content = '今年天气热，给一些防暑降温的建议。'
mo = MyOllama()

client = Client(host=mo.host)
response: ChatResponse = client.chat(
    model=mo.model_name,
    messages=[mo.mk_msg(content)]
)
inspect(response)
print(response['message'])
print(response['message']['content'])
print(response['message']['content'], file=open(
    './asset/doc/ai.md', 'w', encoding='utf-8'))


# %% ---- 2025-07-08 ------------------------
# Pending


# %% ---- 2025-07-08 ------------------------
# Pending
