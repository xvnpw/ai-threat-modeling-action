from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

import logging
from pathlib import Path

def analyze_project(args, inputs: [Path], output: Path):
    logging.info("project content generation started...")
    logging.debug(f"loading files: {inputs}...")
    
    loaders = [TextLoader(str(i.resolve())) for i in inputs]
    docs = [loader.load() for loader in loaders]
    docs_all = (elem for iterable in docs for elem in iterable)
    
    # Define prompt
    prompt_template = """Instruction:
- You are an security architect.
- Your task is to analyze project description and create high level security and privacy requirements
- Project description will be in markdown format
- Format output as markdown
- Response with at least 10 high level security and privacy requirements formatted as markdown and nothing else
- I will provide you example of requirement

Example of requirement:
### 1. Authentication and Authorization
- **Requirement**: Implement strong authentication mechanisms for all users, applications, and APIs accessing AI Nutrition-Pro.
- **Description**: Utilize secure authentication protocols such as OAuth 2.0 or JWT to authenticate and authorize tenants, dietitians, and other users. Different levels of access should be granted based on roles and responsibilities.

Project description:
"{text}"
"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    llm = ChatOpenAI(temperature=args.temperature, model_name=args.model)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )

    with get_openai_callback() as cb:
        ret = stuff_chain.run(docs_all)
        logging.debug(cb)
    logging.info("finished waiting on chatgpt response")
    
    f = open(str(output.resolve()), "w")
    f.write("# (AI Generated) High Level Security and Privacy Requirements\n\n")
    f.write(ret)
    f.close()
    logging.info("response written to file")