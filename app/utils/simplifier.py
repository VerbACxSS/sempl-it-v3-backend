import os
import re
from typing import List

from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.models.SimplificationResponse import SimplificationProgress
from app.utils import loader

class AbstractSimplifier:
    def __init__(self, prev_step: str, step: str, prompt_name: str):
        self.prev_step = prev_step
        self.step = step
        self.prompt_name = prompt_name

        self.sempl_it = ChatOpenAI(base_url=os.getenv("SEMPL_IT_ENDPOINT", "http://localhost:40010/v1"),
                                   api_key=SecretStr(os.getenv("SEMPL_IT_API_KEY", "")),
                                   model=self.step,
                                   max_tokens=4095,
                                   temperature=0.1, top_p=0.2,
                                   frequency_penalty=0.0, presence_penalty=0.0)

    def simplify(self, _progress: SimplificationProgress):
        print(f"Running {self.step} simplification")

        text_to_simplify = _progress[self.prev_step]
        prompt = self.prompt(text_to_simplify)

        text_simplified = self.sempl_it.invoke(prompt).content

        _progress.update({self.step: self.postprocess_output(text_simplified)})
        return _progress

    def prompt(self, text: str) -> List[BaseMessage]:
        system_prompt = f"/no_think\n{loader.load_prompt(self.prompt_name)}"

        return [
            SystemMessage(system_prompt),
            HumanMessage(self.process_user_input(text))
        ]

    def process_user_input(self, user_input: str) -> str:
        return user_input

    def postprocess_output(self, output: str) -> str:
        output = output.replace('**', '')
        output = re.sub(r"<think>.*?</think>\n\n", "", output, flags=re.DOTALL)
        return '\n'.join([x.rstrip() for x in output.split('\n')])


class Proofreader(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="original", step="proofreading" , prompt_name="1_proofreading")


class LexNormalizer(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="proofreading", step="lex", prompt_name="2_lex")


class ConnectivesSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="lex", step="connectives", prompt_name="3_connectives")
        self.connectives = loader.load_connectives()

    def process_user_input(self, user_input: str) -> str:
        connectives_found = []
        for conn in self.connectives:
            results = [m.group() for m in re.finditer(conn, user_input, re.IGNORECASE)]
            connectives_found.extend(results)

        output = "## Testo\n" + user_input + "\n\n## Connettivi\n"
        if len(connectives_found) == 0:
            output += "[Nessuno]"
        else:
            for c in connectives_found:
                output += f"- {c}\n"
        return output

class ExpressionsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="connectives", step="expressions", prompt_name="4_expressions")

class SentenceSplitter(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="expressions", step="sentence_splitter", prompt_name="5_sentence_splitter")

class NominalizationsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="sentence_splitter", step="nominalizations", prompt_name="6_nominalizations")

class VerbsSimplifier(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="nominalizations", step="verbs", prompt_name="7_verbs")

class SentenceReorganizer(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="verbs", step="sentence_reorganizer", prompt_name="8_sentence_reorganizer")

class Explainer(AbstractSimplifier):
    def __init__(self):
        super().__init__(prev_step="sentence_reorganizer", step="explain", prompt_name="9_explain")