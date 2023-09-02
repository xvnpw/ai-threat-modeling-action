from architecture import DataFlowAnalyzer
from llms import LLMWrapper
from langchain.llms.base import LLM

from langchain.llms.fake import FakeListLLM
from langchain.docstore.document import Document

import mock

class FakeLLMWrapper(LLMWrapper):
    def __init__(self, response):
        self.response = response
        
    def create(self) -> LLM:
        llm = FakeListLLM(responses=self.response)
        return llm
        

class TestArchitecture:
    def test_exclude_external_persons(self):
        responses = ["""{
   "data_flows":[
      {
         "data_flow":"Data flow 1: Client -> API Gateway",
         "source_of_data_flow":"Client",
         "destination_of_data_flow":"API Gateway",
         "external_person":false
      },
      {
         "data_flow":"Data flow 5: Meal Planner application -> API Gateway",
         "source_of_data_flow":"Meal Planner application",
         "destination_of_data_flow":"API Gateway",
         "external_person":true
      }
   ]
}"""]
        fake_llm_wrapper = FakeLLMWrapper(responses)
        
        args = mock.Mock()
        args.temperature=0
        args.model = "fake"
        args.template_dir = "./templates/"
        
        docs_all = [Document(page_content="test")]
        
        data_flow_analyzer = DataFlowAnalyzer(fake_llm_wrapper)
        data_flow_names = data_flow_analyzer.list_data_flow_for_architecture(args, docs_all)
        
        assert(len(data_flow_names) == 1)
        assert(data_flow_names[0] == "Data flow 1: Client -> API Gateway")
