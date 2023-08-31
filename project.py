from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.callbacks import get_openai_callback
from llms import LLMWrapper

import logging
from pathlib import Path

def analyze_project(args, inputs: [Path], output: Path):
    logging.info("project content generation started...")
    logging.debug(f"loading files: {inputs}...")
    
    loaders = [TextLoader(str(i.resolve())) for i in inputs]
    docs = [loader.load() for loader in loaders]
    docs_all = (elem for iterable in docs for elem in iterable)
    
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/project_tpl.txt", 
        input_variables=["text"])

    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    llm = LLMWrapper(args).create()
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