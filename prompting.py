import openai
import yaml 
from dataclasses import dataclass
# import json
from api_secret import API_KEY

openai.api_key = API_KEY

@dataclass 
class Option:
    temperature: float= 0.6 
    max_tokens: int=64
    model: str="text-davinci-003"
    n: int=1
    logprobs: int=5

class Question:
    def __init__(self,prompt:str ,option: Option = Option()):
        self.prompt = prompt
        self.option = option
    def ask(self) -> str:
        response = openai.Completion.create(
        model=self.option.model,
        prompt=self.prompt,
        temperature=self.option.temperature,
        max_tokens=self.option.max_tokens,
        n = self.option.n
        )
        for i in range(0,len(response['choices'])):
            return response['choices'][i]['text']
    def get_logprob(self):
        response = openai.Completion.create(
        model=self.option.model,
        prompt=self.prompt,
        temperature=self.option.temperature,
        max_tokens=self.option.max_tokens,
        logprobs = self.option.logprobs
        )

        return response['choices'][0]['logprobs']['top_logprobs']

# class SimpleQuestion(Question):

@dataclass
class Survey:
    option: Option = Option()


with open('survey.yaml', 'r') as file:
    survey = yaml.safe_load(file)
