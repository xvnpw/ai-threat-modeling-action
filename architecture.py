from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

import logging
from pathlib import Path

def analyze_architecture(args, inputs: Path, output: Path):
    logging.info("analyze of architecture started...")
    logging.debug(f"loading file: {inputs}...")
    
    loaders = [TextLoader(str(i.resolve())) for i in inputs]
    docs = [loader.load() for loader in loaders]
    docs_all = [elem for iterable in docs for elem in iterable]
    
    data_flows = _list_data_flow_for_architecture(args, docs_all)
    
    prompt_template = """Instruction:
- You are an security architect
- I will provide you Architecture description
- Perform threat modelling using STRIDE per component technique for data flow
- I will provide you data flow in structure: Data flow 1: Component A -> Component B
- You should answer only in table and nothing more
- Architecture description will be in markdown format
- Format output as markdown

Output of threat modelling should be in table as in example:
### Data flow 1: Component A -> Component B
| Threat Id | Component name | Threat Name | STRIDE category | Mitigations | Risk severity |
| --- | --- | --- | --- | --- | --- |
| 1 | Component A | Attacker is able to spoof client using leaked API key | Spoofing | Invalidation of API keys. Usage of request signing technique | Critical |

Architecture description:
"{text}"

Data flow:
"{dataflow}"
"""
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text", "dataflow"]
    )
    
    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    llm = ChatOpenAI(temperature=args.temperature, model_name=args.model)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    
    f = open(str(output.resolve()), "w")
    f.write("# (AI Generated) Architecture Threat Model\n\n")
    
    for idx, df in enumerate(data_flows):
        with get_openai_callback() as cb:
            ret = stuff_chain.run(input_documents=docs_all, dataflow=df)
            logging.debug(cb)
        logging.info(f"({idx+1} of {len(data_flows)}) finished waiting on chatgpt response")
        f.write(ret)
        f.write("\n\n")
        
    f.close()
    logging.info("response written to file")
    
def _list_data_flow_for_architecture(args, docs_all) -> str:
    # Define prompt
    prompt_template = """Instruction:
- You are an security architect
- List data flows for all components that are internal and important for security of system
- You should not include any persons in data flows
- You should answer only in list and nothing more. Each data flow should be in separated line
- Architecture description will be in markdown format

Example:
Data flow 1: Client -> API Gateway 
Data flow 2: API Gateway -> API Application
Data flow 3: API Application -> API Database

Architecture description:
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
    parsedOutput = ret.strip().split("\n")
    logging.info("finished waiting on chatgpt response - data flows")
    logging.debug(f"got following data flows: {parsedOutput}")
    
    return parsedOutput