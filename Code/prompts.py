from enum import Enum

class Prompts(Enum):
    initial =  "The current experiment includes many trials. Your task, in each trial, is to select one of two options, A or B. Each selection will be followed by the presentation of both choice’s payoffs. Your payoff for the trial is the payoff of the selection you made. To begin, please select A or B. Respond only with the letter 'A' or 'B', indicating your choice"
    initial_a = "The current experiment includes many trials. Your task, in each trial, is to select one of two options, A or B. Each selection will be followed by the presentation of both choice’s payoffs. Your payoff for the trial is the payoff of the selection you made."
    initial_b = "To begin, please select A or B. Respond only with the letter 'A' or 'B', indicating your choice."
    cont = "Please make a new selection, responding only with the letter 'A' or 'B', indicating your choice."
    hist_dict = "The following summarizes the past rounds, where 'choice' is what you chose, 'outcome' is what you recieved, and 'alternative' is what you would have recieved, had you chosen the other option. The numbers represent which round this occured in."
    hist_chat = "The following is the chat history of the past rounds, where keys called 'User' indicate the chat prompts, and those entitled 'Agent' indicate your past choices in this trial."
