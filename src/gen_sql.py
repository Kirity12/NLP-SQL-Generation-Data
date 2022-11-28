#!/usr/bin/env python3
import sys
import time
import logging
import os
from typing import Dict
from collections import deque
import json
from pathlib import Path
PARENT_DIR = Path(__file__, '../..').resolve()
sys.path.append(str(PARENT_DIR))
sys.path.append(r'C:\Users\sganugap\Documents\Kirity Projects\sql_generation-c39846c9d76f296857017c3d7cf9ffb958a4c6ec\src\lib')

import hydra
import openai
openai.api_key = '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'

from omegaconf import OmegaConf
from openai.error import RateLimitError

from src.config import (
    APIConfig, ExperimentConfig, GenerationConfig,
    get_output_dir, get_exp_time
)

from lib.create_few_shot_prompt import generate_prompts
from lib.write_output import OutputManager

logger = logging.getLogger("myLogger")

def generate_sql(api_cfg: APIConfig, gen_cfg: GenerationConfig,  db_prompts: Dict[str, Dict[str, str]]):
    data_output_dir = PARENT_DIR / gen_cfg.data_output_dir
    output_queue = deque()
    api_cfg = OmegaConf.to_container(api_cfg)
    
    # Create output manager object to write output to disk
    output_dir = get_output_dir()
    gpt_response_dir = output_dir / "gpt_input_output"
    gpt_response_dir.mkdir()

    exp_time = get_exp_time()
    output_manager = OutputManager(
        exp_time=exp_time,
        exp_output_dir=gpt_response_dir,
        data_output_dir=data_output_dir
    )

    for i, dd in enumerate(db_prompts):
        output_queue.append({(dd['databases'], 'pair', i): 
            {
                'question': dd['qustions'],
                'query': dd['predicted_answer'],
                'prompt': dd['pompt'],
                'difficulty_of_few_shot': dd['difficulty']
            }
        })

    seconds_spent = output_manager.write_output(output_queue)
    logger.debug(f'Spent: {seconds_spent} seconds writing output')

def parse_response(response: Dict[str, str], sql_prefix: str) -> Dict[str, str]:
    output = response['choices'][0]['text']
    question, query = output.split(sql_prefix)
    return {'output': output, 'question': question, 'query': query}

@hydra.main(config_path="configs", config_name="gpt", version_base="1.2")
def main(cfg: ExperimentConfig):
    logger.info(OmegaConf.to_yaml(cfg))

    with open(r'C:\Users\sganugap\Documents\Kirity Projects\sql_generation-c39846c9d76f296857017c3d7cf9ffb958a4c6ec\few_shot_prompts\grouped_questions.json') as f:
        questions = json.load(f)
    
    prompts = []
    for example in os.listdir(r'C:\Users\sganugap\Documents\Kirity Projects\sql_generation-c39846c9d76f296857017c3d7cf9ffb958a4c6ec\predicted_prompt2'):

        if 'example' in example:
            pqth = os.path.join(r'C:\Users\sganugap\Documents\Kirity Projects\sql_generation-c39846c9d76f296857017c3d7cf9ffb958a4c6ec\predicted_prompt2', example)

            with open(pqth) as f:
                d = json.load(f)
            
            question = questions[d['databases']]

            for difficulty, ques in question.items():

                i=0

                for q in ques :

                    if q['question'] == d['qustions']:

                        d['difficulty'] = difficulty
                        i=1

                        break  
                if i==1:
                    break

            prompts.append(d)
                

            

    
    generate_sql(cfg.api_cfg, cfg.generation_cfg, prompts)

if __name__ == '__main__':
    main()