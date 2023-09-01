from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.callbacks import get_openai_callback
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

from llms import LLMWrapper

from llms import LLMWrapper

import logging
from pathlib import Path

from typing import List
from pydantic import BaseModel, Field

class DataFlow(BaseModel):
    data_flow: str = Field(description="Name of data flow, e.g. Data flow 1: Client -> Component A, Data flow 2: Component A -> Component B")
    external_person: bool = Field(description="Flag that informs whether or not data flow contains external person.")
    
class DataFlowList(BaseModel):
    data_flows: List[DataFlow] = Field(description="List of data flows that are important for security of system.")

class Threat(BaseModel):
    threat_id: int = Field(description="id of threat")
    component_name: str = Field(description="Name of component, example: Service A, API Gateway, Database B, Microservice X, Queue Z")
    threat_name: str = Field(description="Name of threat. Should be detailed and specific, e.g. Attacker bypasses weak authentication and gains unauthorized access to Component A")
    stride_category: str = Field(description="STRIDE category (e.g. Spoofing)")
    applicability_explanation: str = Field(description="Explanation whether or not this threat is already mitigated in architecture")
    mitigation: str = Field(description="Mitigation that can be applied for this threat. Detailed and related to context")
    risk_severity: str = Field(description="Risk severity")
    
class ThreatList(BaseModel):
    data_flow: str = Field(description="Name of data flow, e.g. Data flow 1: Client -> Component A, Data flow 2: Component A -> Component B")
    threats: List[Threat] = Field(description="list of threats applicable for data flow")

def analyze_architecture(args, inputs: Path, output: Path):
    logging.info("analyze of architecture started...")
    logging.debug(f"loading file: {inputs}...")
    
    loaders = [TextLoader(str(i.resolve())) for i in inputs]
    docs = [loader.load() for loader in loaders]
    docs_all = [elem for iterable in docs for elem in iterable]
    
    data_flows = _list_data_flow_for_architecture(args, docs_all)
    
    parser = PydanticOutputParser(pydantic_object=ThreatList)
    
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/arch_threat_model_tpl.txt", 
        input_variables=["text", "dataflow"],
        partial_variables={"format_instructions": parser.get_format_instructions()})
    
    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    
    llm = LLMWrapper(args).create()
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
       
    gen_threats_all = []
    for idx, df in enumerate(data_flows):
        with get_openai_callback() as cb:
            ret = stuff_chain.run(input_documents=docs_all, dataflow=df)
            logging.debug(cb)
        logging.info(f"({idx+1} of {len(data_flows)}) finished waiting on chatgpt response")
        
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        gen_threats = fixing_parser.parse(ret)
        gen_threats_all.append(gen_threats)
        
    _processJsonToMarkdownAndSave(gen_threats_all, output)
    
def _list_data_flow_for_architecture(args, docs_all) -> str:
    parser = PydanticOutputParser(pydantic_object=DataFlowList)
    
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/arch_data_flows_tpl.txt", 
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()})

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
        
    fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    gen_data_flows = fixing_parser.parse(ret)
    logging.info("finished waiting on chatgpt response - data flows")
    logging.debug(f"got following data flows: {gen_data_flows}")
    
    gen_data_flows = [df.data_flow for df in gen_data_flows.data_flows]
    
    return gen_data_flows

def _processJsonToMarkdownAndSave(gen_threats_all : List[ThreatList], output):
    with open(str(output.resolve()), "w") as f:
        f.write("# (AI Generated) Architecture Threat Model\n\n")
        
        for dataflow in gen_threats_all:
            f.write(f'### {dataflow.data_flow}\n\n')
            
            f.write("| Threat Id | Component name | Threat Name | STRIDE category | Explanation | Mitigations | Risk severity |\n")
            f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
            
            for t in dataflow.threats:
                f.write(f'| {t.threat_id} | {t.component_name} | {t.threat_name} | {t.stride_category} | {t.applicability_explanation} | {t.mitigation} | {t.risk_severity} |\n')
                
            f.write("\n\n")
                
        f.close()
        logging.info("response written to file")