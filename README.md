# Decisions-From-Experience Trials in LLM Agents

This repository contains the code associated with the research project **Decisions-From-Experience Trials in LLM Agents**.

## Repository Structure

- **Code**: Contains all relevant Python files for running the experiments.
- **Data**: Includes necessary datasets, such as `experiment_problems.csv` for conducting trials and `all_trial_results_2024_09_28.csv` for generating analysis results.
- **Notebooks**: Contains Jupyter notebooks for running and analyzing experiments.

## How to Run the Code

### Requirements
- You will need to install the following Python packages:
  - `google.generativeai`
  - `openai`
- Ensure you have valid API keys for both Google and OpenAI. These keys should be stored in an `enum` class called `APIKeys` within a Python file named `secret_keys.py`.

### Setup

1. **Configure Experiment Parameters**: 
   - Use the `experiment_problems.csv` file located in the `Data` folder.
   - Adjust the `setup_params` in the Python files to suit the trials you would like to run.

2. **Run Trials**:
   - For running trials in a notebook format, open the `Agent_trials.ipynb` notebook in the `Notebooks` folder.
   - To generate results, use the `Analysis.ipynb` notebook. It requires the `all_trial_results_2024_09_28.csv` file from the `Data` folder.

## Notes

- Ensure your environment is properly set up with the required libraries and API keys before running the trials.
- The `secret_keys.py` file should be created manually, and it should not be pushed to the repository for security reasons.

## Contact

For any questions or further information about this research, feel free to reach out - idanhorowitz@campus.technion.ac.il 😃

