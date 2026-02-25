import runpod
import os
from utils import JobInput
from engine import OllamaAnthropicEngine, OllamaEngine, OllamaOpenAiEngine

DEFAULT_MAX_CONCURRENCY = 8
max_concurrency = int(os.getenv("MAX_CONCURRENCY", DEFAULT_MAX_CONCURRENCY))

async def handler(job: any):
    # Just dump the whole input to the console and then return an {"ok": True} response
    print('Job:', job)

    job_input = JobInput(job["input"])
    if job_input.anthropic_input:
        engine = OllamaAnthropicEngine()
    elif job_input.openai_route:
        engine = OllamaOpenAiEngine()
    else:
        engine = OllamaEngine()

    job = engine.generate(job_input)  # Call generate with job_input

    async for batch in job:
        yield batch

# Original code from vllm runpod_wrapper.py
#async def handler(job):
#    job_input = JobInput(job["input"])
#    engine = OpenAIvLLMEngine if job_input.openai_route else vllm_engine
#    results_generator = engine.generate(job_input)
#    async for batch in results_generator:
#        yield batch

runpod.serverless.start(
    {
        "handler": handler,
        "concurrency_modifier": lambda x: max_concurrency,
        "return_aggregate_stream": True,
    }
)