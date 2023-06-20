import openai
# import yaml 
from dataclasses import dataclass
# import json
from api_secret import API_KEY
# from prompting import Options
# from prompting import Option

openai.api_key = API_KEY

@dataclass 
class Options:
    temperature: float= 0.6 
    max_tokens: int=64
    model: str="text-davinci-003"
    n: int=1
    logprobs: int=5

class Question:
    def __init__(self, prompt:str ,name:str, options: Options = Options()):
        self.prompt = prompt
        self.options = options
        self.name = name
    
    def ask(self) -> str:
        response = openai.Completion.create(
        model=self.options.model,
        prompt=self.prompt,
        temperature=self.options.temperature,
        max_tokens=self.options.max_tokens,
        n = self.options.n
        )
        for i in range(0,len(response['choices'])):
            return response['choices'][i]['text']
    def get_logprob(self):
        response = openai.Completion.create(
        model=self.options.model,
        prompt=self.prompt,
        temperature=self.options.temperature,
        max_tokens=self.options.max_tokens,
        logprobs = self.options.logprobs
        )

        return response['choices'][0]['logprobs']['top_logprobs']

class UniqueQuestion(Question):
    def __init__(self, prompt: str, name: str, options: Options = Options()):
        super().__init__(prompt, name, options)

class ScaleQuestion(Question):
    def __init__(self, prompt: str, name: str, options: Options = Options()):
        super().__init__(prompt, name, options)
    
class SimpleQuestion(Question):
    def __init__(self, prompt: str, options: Options = Options(n=1)):
        super().__init__(prompt, options)
    def write_answer(self):
        yaml_file = open("answers.yaml", "a")
        d = dict()
        d["options"] = self.option.temperature
        yaml_file.write(
           f'''
options : 
    temperature : {self.option.temperature}
    max_tokens : {self.option.max_tokens}
    model : {self.option.model}
    prompt : {self.prompt}
           ''' 
            
        )
        yaml_file.write(
            f'''
question : 
    name : 
    answer : {self.ask().strip()} 
            ''' 
            )
        yaml_file.close()

@dataclass
class Survey:
    questions: list[Question]  
    options: Options = Options()

    def run(self):
        results = []
        for i in self.questions:
            results.append(
                {
                    'question': i.name,
                    'prompt' : i.prompt, 
                    'answer': i.ask()
                })
        return results


# with open('survey.yaml', 'r') as file:
#     survey = yaml.safe_load(file)
