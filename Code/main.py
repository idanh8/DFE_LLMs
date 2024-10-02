from models import *
from secret_keys import *
from setup_params import *
from trials import Trial
import pandas as pd
import datetime
import pytz

def get_timestamp():
  gmt_plus_3 = pytz.timezone('Etc/GMT-3')
  now = datetime.datetime.now(gmt_plus_3)
  timestamp = now.strftime('%Y-%m-%d_%H-%M')
  return timestamp

if __name__ == "__main__":

    df = pd.read_csv('experiment_problems.csv')
    all_temps = True
    num_trials = 20
    last_id = 1156
    trial_idx = trial_params['idx'][3]
    model_name = model_params['model_history'][4][0]
    history = model_params['model_history'][4][1]
    temp = model_params['temperature'][2]

    results_df = pd.DataFrame()
    if all_temps:
        for temp in model_params['temperature']:
            print(f'--------------- Running 20 {model_name, history} Trials at Temperature {temp} ---------------')
            filename = f'trial_results_{model_name}_{history}_temp_{temp}_{get_timestamp()}.csv'
            for i in range(num_trials):
                model = GeminiModel(APIKeys.gemini_token.value, model_name, history, temp) if model_name == 'gemini-1.5-flash' else OpenAIModel(APIKeys.openai_token.value, model_name, history, temp)
                trial = Trial(i+last_id+1, df, model, num_rounds, trial_idx)
                trial_results = trial.run_trial()
                if len(trial_results) < 100:
                    break
                results_df = pd.concat([results_df, trial_results])
                print(f'\n Trial {i+1}/{num_trials} Complete!')
                results_df.to_csv(filename, index=False)
            last_id += 20
        fullname = f'trial_results_{model_name}_{history}_{get_timestamp()}.csv'
        results_df.to_csv(fullname, index=False)
    else:
        print(f'--------------- Running {num_trials} {model_name, history} Trials at Temperature {temp} ---------------')
        filename = f'trial_results_{model_name}_{history}_temp_{temp}_{get_timestamp()}.csv'
        for i in range(num_trials):
            model = GeminiModel(APIKeys.gemini_token.value, model_name, history, temp) if model_name == 'gemini-1.5-flash' else OpenAIModel(APIKeys.openai_token.value, model_name, history, temp)
            trial = Trial(i+last_id+1, df, model, num_rounds, trial_idx)
            trial_results = trial.run_trial()
            if len(trial_results) < 100:
                break
            results_df = pd.concat([results_df, trial_results])
            print(f'\n Trial {i+1}/{num_trials} Complete!')
            results_df.to_csv(filename, index=False)
