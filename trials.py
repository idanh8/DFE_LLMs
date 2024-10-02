import numpy as np
import pandas as pd
from models import *
from tqdm import tqdm


class Trial:
  def __init__(self, trial_id: int, trials_df: pd.DataFrame, model: (GeminiModel | OpenAIModel), num_rounds: int = 100, trial_idx: (str | int) = 'random'):
    idx = np.random.randint(0, len(trials_df)) if trial_idx == 'random' else trial_idx
    row = trials_df.iloc[idx]
    self.num_rounds = num_rounds
    self.trial_id = trial_id
    self.prob_id = row['id']
    self.a1 = row['a1']
    self.pa1 = row['pa1']
    self.a2 = row['a2']
    self.b1 = row['b1']
    self.pb1 = row['pb1']
    self.b2 = row['b2']
    self.corrAB = row['corrAB']
    self.model = model
    self.round_num = 1
    self.rounds_details = {}

  def create_trial_dict(self):
    self.trial_dict = {'trial_id': self.trial_id, 'prob_id': self.prob_id, 'a1': self.a1, 'pa1': self.pa1, 'a2': self.a2, 'b1': self.b1, 'pb1': self.pb1, 'b2': self.b2, 'corrAB': self.corrAB}
    self.trial_dict.update(self.model.get_model_dict())
    return self.trial_dict

  def create_results_df(self):
    d = self.create_trial_dict()
    rows = []
    for round_number, round_info in self.rounds_details.items():
      row = {**d, 'round_number': round_number, **round_info,}
      rows.append(row)
    return pd.DataFrame(rows)

  def run_trial(self):
    for i in tqdm(range(self.num_rounds)):
      choice = self.model.get_response()
      if choice == None:
        break
      self.simulate_round(choice)
      self.model.set_history(self.rounds_details)
      self.model.set_prompt(self.rounds_details)
      self.round_num += 1
    return self.create_results_df()

  def simulate_round(self, choice: str):
    rand_a, rand_b = np.random.rand(), np.random.rand()
    if self.corrAB != 0:
      rand_b = rand_a if self.corrAB == 1 else 1 - rand_a
    if choice == 'A':
        outcome = self.a1 if rand_a < self.pa1 else self.a2
        alternative = self.b1 if rand_b < self.pb1 else self.b2
    else:
        outcome = self.b1 if rand_b < self.pb1 else self.b2
        alternative = self.a1 if rand_a < self.pa1 else self.a2
    self.rounds_details[self.round_num] = {'choice': choice,
                                              'outcome': outcome,
                                              'alternative': alternative}