import os
import logging
import argparse
from pathlib import Path
import json

from project import analyze_project
from architecture import analyze_architecture
from user_story import analyze_user_story

import constants
    
BASEDIR = os.environ.get('GITHUB_WORKSPACE')
if not BASEDIR:
    print('GITHUB_WORKSPACE environment variable not set.')
    exit(1)

parser = argparse.ArgumentParser(
    prog='ai-tm.py',
    description='AI featured threat modeling and security review action',
    epilog='Experimental. Use on your own risk'
)
parser.add_argument("type", type=str, choices=['project', 'architecture', 'user-story'], help="Type of feature")
parser.add_argument("--provider", type=str, choices=['openai', 'openrouter'], help="Provider of LLM API", default="openai")
parser.add_argument("--inputs", type=str, help="json array of paths to input files", nargs='?')
parser.add_argument("--output", type=str, help="path to output file", nargs='?')
parser.add_argument("-ai", "--architecture-inputs", type=str, help="for user-story only: json array of paths to architecture files", nargs='?')
parser.add_argument("-atmi", "--architecture-threat-model-input", type=str, help="for user-story only: path to architecture threat model file", nargs='?')
parser.add_argument("--model", type=str, help="type of ChatGPT model, default: gpt-3.5-turbo", default="gpt-3.5-turbo")
parser.add_argument("--temperature", type=float, help="sampling temperature for a model, default 0", default=0)
parser.add_argument('-v', '--verbose', type=str, help="Turn on verbose messages", default="false")
parser.add_argument('-d', '--debug', type=str, help="Turn on debug messages", default="false")
parser.add_argument("-usos", "--user-story-output-suffix", type=str, help="for user-story only: suffix that will be added to input file name to create output file", default="_SECURITY")
parser.add_argument("-t", "--template-dir", type=str, help="path to template dir", default="./templates")

args = parser.parse_args()

if args.verbose == 'true':
    logging.basicConfig(level=logging.INFO)
    
if args.debug == 'true':
    logging.basicConfig(level=logging.DEBUG)
    
logging.debug(f'running for feature: {args.type}...')

if args.type == "project":
    if not args.inputs:
        inputs = [Path(BASEDIR).joinpath(constants.PROJECT_INPUT)]
    else:
        raw_input_paths = json.loads(args.inputs)
        inputs = [Path(BASEDIR).joinpath(p) for p in raw_input_paths]
    
    if not args.output:
        output = Path(BASEDIR).joinpath(constants.PROJECT_OUTPUT)
    else:
        output = Path(BASEDIR).joinpath(args.output)
    analyze_project(args, inputs, output)
    
if args.type == "architecture":
    if not args.inputs:
        inputs = [Path(BASEDIR).joinpath(constants.ARCHITECTURE_INPUT)]
    else:
        raw_input_paths = json.loads(args.inputs)
        inputs = [Path(BASEDIR).joinpath(p) for p in raw_input_paths]
    
    if not args.output:
        output = Path(BASEDIR).joinpath(constants.ARCHITECTURE_OUTPUT)
    else:
        output = Path(BASEDIR).joinpath(args.output)
    analyze_architecture(args, inputs, output)

if args.type == "user-story":
    if not args.inputs:
        parser.error("inputs cannot be empty for user-story")
    raw_input_paths = json.loads(args.inputs)
    
    inputs = [Path(BASEDIR).joinpath(p) for p in raw_input_paths]
    inputs = [i for i in inputs if i.exists()]
    
    logging.debug(f'inputs for process: {len(inputs)}')
    
    for i in inputs:
        if not args.output:
            filename, file_extension = os.path.splitext(str(i.resolve()))
            output = Path(filename + args.user_story_output_suffix + file_extension)
        else:
            parser.error("output is forbidden for user-story, it will be generated based on input")
        logging.debug(f'output set to: {output}')
    
        if not args.architecture_inputs:
            architecture_inputs = [Path(BASEDIR).joinpath(constants.ARCHITECTURE_INPUT)]
        else:
            architecture_raw_input_paths = json.loads(args.architecture_inputs)
            architecture_inputs = [Path(BASEDIR).joinpath(p) for p in architecture_raw_input_paths]
            
        if not args.architecture_threat_model_input:
            architecture_tm_input = Path(BASEDIR).joinpath(constants.ARCHITECTURE_OUTPUT)
        else:
            architecture_tm_input = Path(BASEDIR).joinpath(args.architecture_threat_model_input)
        
        analyze_user_story(args, i, architecture_inputs, architecture_tm_input, output)
        