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
    
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/arch_threat_model_tpl.txt", 
        input_variables=["text", "dataflow"])
    
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
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/arch_data_flows_tpl.txt", 
        input_variables=["text"])

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