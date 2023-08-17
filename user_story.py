from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema.messages import AIMessage
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

import logging
from pathlib import Path

def analyze_user_story(args, input: Path, architecture_inputs: [Path], architecture_tm_input: Path, output: Path):
    logging.info("user story content generation started...")
    logging.debug(f"loading user story from: {input}...")
    logging.debug(f"loading architecture from: {architecture_inputs}...")
    logging.debug(f"loading architecture threat model from: {architecture_tm_input}...")
    
    user_story_loader = TextLoader(str(input.resolve()))
    user_story_doc = user_story_loader.load()
    
    architecture_loaders = [TextLoader(str(i.resolve())) for i in architecture_inputs]
    architecture_docs = [loader.load() for loader in architecture_loaders]
    architecture_docs_all = (elem for iterable in architecture_docs for elem in iterable)
    
    architecture_tm_loader = TextLoader(str(architecture_tm_input.resolve()))
    architecture_tm_doc = architecture_tm_loader.load()
    
    components_for_user_story = _list_components_for_user_story(args, user_story_doc)
        
    chat_prompt_template = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_intro_tpl.yaml")),
        AIMessage(content="""Sure, I understand your instructions. Please provide me with the user story, 
                architecture description, and architecture threat model documents in markdown format one 
                by one, and I'll be ready to analyze them and provide you with the most important security-related 
                acceptance criteria for the user story.""", additional_kwargs={}),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_doc_tpl.yaml")),
        AIMessage(content="""Thank you for providing the user story. Please proceed to provide me with 
                  the "Architecture Description" document in markdown format, and I'll analyze it next. 
                  Once I have all the relevant information, I'll be able to list the most important security-related 
                  acceptance criteria for the user story.""", additional_kwargs={}),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_arch_doc_tpl.yaml")),
        AIMessage(content="""Thank you for providing the "Architecture Description" document. Please 
                  proceed to provide me with the "Architecture Threat Model" document in markdown format, 
                  and I'll analyze it next. Once I have all the relevant information, I'll be able to list 
                  the most important security-related acceptance criteria for the user story.""", additional_kwargs={}),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_arch_tm_doc_tpl.yaml")),
    ])

    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    llm = ChatOpenAI(temperature=args.temperature, model_name=args.model)
    llm_chain = LLMChain(llm=llm, prompt=chat_prompt_template)
    
    with get_openai_callback() as cb:
        architecture_docs_loaded = "\n\n".join([str(d.page_content) for d in architecture_docs_all])
        
        ret = llm_chain.run(user_story_doc=str(user_story_doc[0].page_content), 
            components=components_for_user_story,
            arch_doc=architecture_docs_loaded,
            arch_tm_doc=str(architecture_tm_doc[0].page_content))
        logging.debug(cb)
    
    logging.info("finished waiting on chatgpt response")
    
    f = open(str(output.resolve()), "w")
    f.write("# (AI Generated) Security Related Acceptance Criteria\n")
    f.write(ret)
    f.close()
    logging.info("response written to file")
    
def _list_components_for_user_story(args, user_story_doc) -> str:
    # Define prompt
    prompt_template = """You are solution architect. I will provide you User Story and you will list all 
architecture containers, services or applications included in architecture. Answer only with list, 
each entry in one line and nothing more.

User Story:
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
        ret = stuff_chain.run(user_story_doc)
        logging.debug(cb)
    parsedOutput = ret.strip().split("\n")
    logging.info("finished waiting on chatgpt response - components")
    logging.debug(f"got following components: {parsedOutput}")
           
    return ret