"""External tools available to the bot."""

# %% IMPORTS

import os
import typing as T

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from loguru import logger
from pipecat.frames import frames
from pipecat.services.gemini_multimodal_live import gemini

# %% CONFIGS

GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", None)
GOOGLE_SEARCH_ENGINE = os.getenv("GOOGLE_SEARCH_ENGINE", None)
GOOGLE_SEARCH_LANG = os.getenv("GOOGLE_SEARCH_LANG", "en")
GOOGLE_SEARCH_LOCATION = os.getenv("GOOGLE_SEARCH_LOCATION", "global")
GOOGLE_SEARCH_MODEL = os.getenv("GOOGLE_SEARCH_MODEL", "gemini-1.5-flash-002/answer_gen/v1")

# %% TOOLS


async def search_website_information(
    function_name: str,
    tool_call_id: str,
    args: dict[str, T.Any],
    llm: gemini.GeminiMultimodalLiveLLMService,
    context: gemini.GeminiMultimodalLiveContext,
    result_callback: T.Callable,
) -> None:
    """Search accurate information on the company website."""
    try:
        logger.info(f"[TOOL:{tool_call_id}] Search Website Information: {function_name}({args})")
        client_options = (
            ClientOptions(api_endpoint=f"{GOOGLE_SEARCH_LOCATION}-discoveryengine.googleapis.com")
            if GOOGLE_SEARCH_LOCATION != "global"
            else None
        )
        search_client = discoveryengine.ConversationalSearchServiceAsyncClient(
            client_options=client_options,
        )
        serving_config = f"projects/{GOOGLE_PROJECT_ID}/locations/{GOOGLE_SEARCH_LOCATION}/collections/default_collection/engines/{GOOGLE_SEARCH_ENGINE}/servingConfigs/default_serving_config"
        model_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
            model_version=GOOGLE_SEARCH_MODEL,
        )
        prompt_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
            preamble="Provide a detailed summary",
        )
        answer_generation_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
            model_spec=model_spec,
            prompt_spec=prompt_spec,
            include_citations=False,
            answer_language_code=GOOGLE_SEARCH_LANG,
        )
        query = discoveryengine.Query(text=args["query"])
        request = discoveryengine.AnswerQueryRequest(
            query=query,
            serving_config=serving_config,
            answer_generation_spec=answer_generation_spec,
        )
        response = await search_client.answer_query(request=request)
        answer = response.answer.answer_text  # also contains search results
        logger.info(f"[TOOL:{tool_call_id}] Search Website Answer: {answer}")
        result_callback_properties = frames.FunctionCallResultProperties(run_llm=True)
        await result_callback(answer, properties=result_callback_properties)
        # # send the answer of the search engine to the user interface
        # await llm.push_frame(frames.LLMFullResponseStartFrame())
        # await llm.push_frame(frames.TextFrame(text=answer))
        # await llm.push_frame(frames.LLMFullResponseEndFrame())
        # # ask the model to answer the user question right now
        # event = events.ClientContentMessage.model_validate(
        #     {
        #         "clientContent": {
        #             "turns": [
        #                 {
        #                     "role": "user",
        #                     "parts": [
        #                         {"text": "Summarize the information you found for my question"}
        #                     ],
        #                 }
        #             ],
        #             "turnComplete": True,
        #         }
        #     }
        # )
        # await asyncio.sleep(delay=1.0)
        # await llm.send_client_event(event)
    except Exception as error:
        logger.error(f"[TOOL:{tool_call_id}] Search Website Error: {str(error)}")
        await llm.push_frame(frames.ErrorFrame(str(error)))


# %% SCHEMAS

search_website_information_schema = {
    "function_declarations": [
        {
            "name": search_website_information.__name__,
            "description": search_website_information.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query formulated as a question",
                    },
                },
                "required": ["query"],
            },
        },
    ]
}
