from langchain.document_loaders import TextLoader
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.output_parsers import PydanticOutputParser

import logging
from pathlib import Path

from typing import List
from pydantic import BaseModel, Field

class AcceptanceCriteria(BaseModel):
    id: str = Field(description="Id of acceptance criteria, eg. AC1, AC2, AC3")
    acceptance_criteria: str = Field(description="Value of acceptance criteria. Very specific and detailed, eg: The API for payments (`/api/process`) must enforce proper input validation to prevent injection attacks.")
    explanation: str = Field(description="Expiation why acceptance criteria is included for particular component for this user story")

class ComponentAcceptanceCriteriaList(BaseModel):
    component_name: str = Field(description="Name of component, example: Service A, API Gateway, Database B, Microservice X, Queue Z")
    acceptance_criteria_list: List[AcceptanceCriteria] = Field(description="List of acceptance criteria for this particular component for user story")

class AcceptanceCriteriaList(BaseModel):
    components: List[ComponentAcceptanceCriteriaList] = Field(description="List of components with acceptance criteria for user story")

class Component(BaseModel):
    component_name: str = Field(description="Name of component, example: Service A, API Gateway, Database B, Microservice X, Queue Z")
    component_scope: str = Field(description="Explanation why component is included in scope of this user story")
    
class ComponentList(BaseModel):
    components: List[Component] = Field(description="List of components that are internal and important for security of system. List don't include persons and external components.")

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
        AIMessagePromptTemplate.from_template_file(template_file=f"{args.template_dir}/user_story_ai_confirmation_step1_tpl.txt", input_variables=[]),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_doc_tpl.yaml")),
        AIMessagePromptTemplate.from_template_file(template_file=f"{args.template_dir}/user_story_ai_confirmation_step2_tpl.txt", input_variables=[]),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_arch_doc_tpl.yaml")),
        AIMessagePromptTemplate.from_template_file(template_file=f"{args.template_dir}/user_story_ai_confirmation_step3_tpl.txt", input_variables=[]),
        HumanMessagePromptTemplate(prompt=load_prompt(f"{args.template_dir}/user_story_arch_tm_doc_tpl.yaml")),
    ])

    parser = PydanticOutputParser(pydantic_object=AcceptanceCriteriaList)

    # Define LLM chain
    logging.debug(f'using temperature={args.temperature} and model={args.model}')
    llm = ChatOpenAI(temperature=args.temperature, model_name=args.model)
    llm_chain = LLMChain(llm=llm, prompt=chat_prompt_template)
    
    with get_openai_callback() as cb:
        architecture_docs_loaded = "\n\n".join([str(d.page_content) for d in architecture_docs_all])
        
        ret = llm_chain.run(user_story_doc=str(user_story_doc[0].page_content), 
            components="\n".join(components_for_user_story),
            arch_doc=architecture_docs_loaded,
            arch_tm_doc=str(architecture_tm_doc[0].page_content),
            format_instructions=parser.get_format_instructions())
        logging.debug(cb)
    
    logging.info("finished waiting on chatgpt response")
    
    gen_components_all = parser.parse(ret)
    
    _processJsonToMarkdownAndSave(gen_components_all.components, output)
    
def _processJsonToMarkdownAndSave(gen_components_all : List[ComponentAcceptanceCriteriaList], output):
    with open(str(output.resolve()), "w") as f:
        f.write("# (AI Generated) Security Related Acceptance Criteria\n")
        
        for component in gen_components_all:
            f.write(f"**{component.component_name}**\n")
            
            for ac in component.acceptance_criteria_list:
                f.write(f'- **{ac.id}:** {ac.acceptance_criteria}\n')
            
            f.write("\n")
    f.close()
    logging.info("response written to file")            
    
def _list_components_for_user_story(args, user_story_doc) -> str:
    parser = PydanticOutputParser(pydantic_object=ComponentList)
    
    # Define prompt
    prompt = PromptTemplate.from_file(template_file=f"{args.template_dir}/user_story_arch_components_tpl.txt", 
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()})

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
    gen_components = parser.parse(ret)
    logging.info("finished waiting on chatgpt response - components")
    logging.debug(f"got following components: {gen_components}")
    
    gen_components = [c.component_name for c in gen_components.components]
           
    return gen_components