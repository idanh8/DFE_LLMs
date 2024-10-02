from prompts import Prompts
import google.generativeai as genai
from openai import OpenAI
import numpy as np
import pandas as pd
import time 
import re

class OpenAIModel:
  def __init__(self, api_key: str, model_name: str = 'gpt-4o-mini',  provide_history: str = 'all', temp: float = 1):
    self.client = OpenAI(api_key=api_key)
    self.model_name = model_name
    self.temp = temp
    self.history_provided = provide_history
    self.messages = [{"role": "system", "content": Prompts.initial_a.value},
                   {"role": "user", "content": Prompts.initial_b.value}]
    self.history = {}

  def set_history(self, round_details: dict):
    if self.history_provided == 'all':
      self.history = round_details

  def set_prompt(self, round_details: dict):
    round_num = max(round_details.keys())
    prev_round = round_details[round_num]
    prev_alt = 'B' if prev_round['choice'] == 'A' else 'A'
    if self.history_provided == 'chat':
      self.messages.append({"role": "assistant", "content": prev_round['choice']})
      self.messages.append({"role": "user", "content": f"You selected {prev_round['choice']} and recieved a payoff of {prev_round['outcome']}. Had you selected {prev_alt}, you would have recieved {prev_round['alternative']}." + Prompts.cont.value})
    else:
      self.messages = [{"role": "system", "content": Prompts.initial_a.value},
                        {"role": "user", "content": f"You selected {prev_round['choice']} and recieved a payoff of {prev_round['outcome']}. Had you selected {prev_alt}, you would have recieved {prev_round['alternative']}." + Prompts.hist_dict.value + f"{self.history}. The current round number is {round_num}:" + Prompts.cont.value}]

  def get_response(self):
    retries = 0
    while retries < 7:
      try:
        response = self.client.chat.completions.create(model=self.model_name, messages=self.messages, temperature = self.temp)
        r = re.sub(r'\s+', '', response.choices[0].message.content)
        if r == 'A' or r == 'B':
          return r
        else:
          print('retrying call')
          self.messages.append({"role": "assistant", "content": r})
          self.messages.append({"role": "user", "content": "Your previous response was invalid. Please ensure your choice is a single character, either 'A' or 'B', and nothing more."})
          continue
      except Exception as e:
        print(f"An error occurred: {e}")

      time.sleep(0.5 * (2 * retries))
      retries += 1

    print("Max retries exceeded. API call failed.")
    return None


  def get_model_dict(self):
    return {'model_name': self.model_name, 'history_provided': self.history_provided, 'temperature': self.temp}

class GeminiModel:
  def __init__(self, api_key: str, model_name: str = 'gemini-1.5-flash',  provide_history: (str | None) = None, temp: float = 1):
    genai.configure(api_key=api_key)
    self.model_name = model_name
    self.temp = temp
    self.generation_config = {"temperature": self.temp, "top_p": 0.95, "top_k": 64, "max_output_tokens": 8192, "response_mime_type": "text/plain"}
    self.model = genai.GenerativeModel(model_name = self.model_name, generation_config=self.generation_config)
    self.history_provided = provide_history
    self.messages = [{"role": "user", "parts": Prompts.initial.value}] if self.history_provided == 'chat' else Prompts.initial.value
    self.history = {} if self.history_provided else self.model.start_chat(history=[])

  def generate_response(self):
    return self.model.generate_content(self.messages) if self.history_provided else self.history.send_message(self.messages)

  def set_prompt(self, round_details: dict):
    round_num = max(round_details.keys())
    prev_round = round_details[round_num]
    prev_alt = 'B' if prev_round['choice'] == 'A' else 'A'
    if self.history_provided == 'all':
      self.messages = f"You selected {prev_round['choice']} and recieved a payoff of {prev_round['outcome']}. Had you selected {prev_alt}, you would have recieved {prev_round['alternative']}." + Prompts.hist_dict.value + f"{self.history}. The current round number is {round_num}:" + Prompts.cont.value
    elif self.history_provided == 'chat':
     self.messages.append({"role": "model", "parts": [prev_round['choice']]})
     self.messages.append({"role": "user", "parts": [f"You selected {prev_round['choice']} and recieved a payoff of {prev_round['outcome']}. Had you selected {prev_alt}, you would have recieved {prev_round['alternative']}." + Prompts.cont.value]})
    else:
      self.messages = f"You selected {prev_round['choice']} and recieved a payoff of {prev_round['outcome']}. Had you selected {prev_alt}, you would have recieved {prev_round['alternative']}." + Prompts.cont.value

  def set_history(self, round_details: dict):
    if self.history_provided == 'all':
        self.history = round_details

  def get_response(self):
    retries = 0
    while retries < 7:
      try:
        response = self.generate_response()
        r = re.sub(r'\s+', '', response.text)
        if r == 'A' or r == 'B':
          return r
        else:
          self.prompt = "Your previous response was invalid. Please ensure your choice is a single character, either 'A' or 'B', and nothing more." + self.prompt
          print('retrying call')
          continue
      except Exception as e:
        print(f"An error occurred: {e}")

      time.sleep(0.5 * (2 * retries))
      retries += 1

    print("Max retries exceeded. API call failed.")
    return None

  def get_model_dict(self):
    return {'model_name': self.model_name, 'history_provided': self.history_provided, 'temperature': self.temp}
