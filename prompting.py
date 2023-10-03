import openai
import re
from dataclasses import dataclass
from string import Template
from api_secret import API_KEY
from tqdm import tqdm


openai.api_key = API_KEY

@dataclass 
class Options:
    temperature: float= 0.6 
    max_tokens: int=64
    model: str="text-davinci-003"
    n: int=3
    logprobs: int=5

class Question:
    def __init__(self, prompt:str ,name:str,  type: str ='Numerical', options: Options = Options()):
        self.prompt = prompt
        self.options = options
        self.name = name
        self.type = type
    
    def ask(self) -> str:
        response = openai.Completion.create(
        model=self.options.model,
        prompt=self.prompt,
        temperature=self.options.temperature,
        max_tokens=self.options.max_tokens,
        n = self.options.n
        )
        for i in range(0,len(response['choices'])):
            self.answer = response['choices'][i]['text']
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
    
    def extract_answer(self): 
        if self.type == 'Numerical':
           extracted_answer = re.findall(r'\d+', self.ask())
        elif self.type == 'Yes or No':
            extracted_answer =re.findall(r'yes|no', self.ask(), re.IGNORECASE)
        elif self.type == 'Now or Later':
            extracted_answer =re.findall(r'now|later', self.ask(), re.IGNORECASE)
        else:
            print('Please enter a valid question type')
        self.answer = extracted_answer[0]
        return extracted_answer[0] 

class UniqueQuestion(Question):
    def __init__(self, prompt: str, name: str,type: str='Numerical', options: Options = Options()):
        super().__init__(prompt, name, type,options)


class ScaleQuestion(Question):
    def __init__(self, prompt: str, name: str, amounts, type: str='Numerical', options: Options = Options()):
        super().__init__(prompt, name,type ,options)
        self.amounts = amounts
    def get_question_list(self) -> list: 
        tmp = Template(self.prompt)
        question_list = []
        for i in self.amounts:
            question_list.append(tmp.substitute(amount=i))
        self.prompt = question_list
        return question_list
    def ask(self):
        answers_list = []
        for prompts in self.get_question_list():
            answers_list.append(Question(prompt=prompts, name = self.name, options=self.options).ask())
        self.answer = answers_list
        return answers_list


# class SimpleQuestion(Question):
#     def __init__(self, prompt: str, options: Options = Options(n=1)):
#         super().__init__(prompt, options)
#     def write_answer(self):
#         yaml_file = open("answers.yaml", "a")
#         d = dict()
#         d["options"] = self.option.temperature
#         yaml_file.write(
#            f'''
# options : 
#     temperature : {self.option.temperature}
#     max_tokens : {self.option.max_tokens}
#     model : {self.option.model}
#     prompt : {self.prompt}
#            ''' 
            
#         )
#         yaml_file.write(
#             f'''
# question : 
#     name : 
#     answer : {self.ask().strip()} 
#             ''' 
#             )
#         yaml_file.close()

@dataclass
class Survey:
    questions: list[Question]  
    options: Options = Options(n=3)

    def run(self):
        results = []
        for i in tqdm(self.questions, desc='survey'):
            try: 
                i.get_answers(i.get_question_list())
            except Exception as e:
                i.ask()
            results.append(
                {
                    'question': i.name,
                    'prompt' : i.prompt, 
                    'answer': i.answer          #i.extract_answer(i.ask(), i.type)
                })
        return results


# with open('survey.yaml', 'r') as file:
#     survey = yaml.safe_load(file)
