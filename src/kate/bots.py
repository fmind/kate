"""Bots that handle live user interactions."""

# %% IMPORTS

import abc
import os

from loguru import logger
from pipecat.frames import frames
from pipecat.pipeline import pipeline, runner, task
from pipecat.processors.frameworks import rtvi
from pipecat.services.gemini_multimodal_live import gemini
from pipecat.transports.services import daily

from kate import processors, tools

# %% CONFIGS

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.0-flash-exp")
MODEL_VOICE_ID = os.getenv("MODEL_VOICE_ID", "Aoede")  # Aoede, Charon, Fenrir, Kore, Puck

# %% BOTS


class Bot(abc.ABC):
    """Base class for bots."""

    @abc.abstractmethod
    async def run(self):
        """Run the bot."""
        pass


class OTLBot(Bot):
    """Bot for Open Textbook Library."""

    NAME = "Kate"
    TOOLS = [
        tools.search_website_information_schema,
    ]
    FUNCTIONS = {
        tools.search_website_information.__name__: tools.search_website_information,
    }
    TEMPERATURE = 0.7
    WELCOME_CONTENT = "Start by introducing yourself"
    SYSTEM_INSTRUCTIONS = f"""
    You are {NAME}, a friendly and knowledgeable online librarian for the Open Textbook Library website. Help users find textbooks for their needs and answer their questions. Use the "search_website_information" tool when needed to gather more information about the available textbooks and website FAQ.
    """

    def __init__(self, room_url: str, token: str):
        logger.info(f"Initialize bot: {self.NAME}")
        # processors
        self.transport = daily.DailyTransport(
            token=token,
            room_url=room_url,
            bot_name=self.NAME,
            params=daily.DailyParams(
                audio_in_enabled=True,
                audio_in_sample_rate=16000,
                audio_out_enabled=True,
                audio_out_sample_rate=24000,
                camera_out_enabled=True,
                camera_out_height=1024,
                camera_out_width=1024,
            ),
        )
        self.llm_service = gemini.GeminiMultimodalLiveLLMService(
            api_key=GOOGLE_API_KEY,
            model=MODEL_NAME,
            voice_id=MODEL_VOICE_ID,
            transcribe_user_audio=True,
            transcribe_model_audio=True,
            system_instruction=self.SYSTEM_INSTRUCTIONS,
            params=gemini.InputParams(
                temperature=self.TEMPERATURE,
            ),
            tools=self.TOOLS,
        )
        for function_name, function in self.FUNCTIONS.items():
            self.llm_service.register_function(function_name=function_name, callback=function)
        messages = (
            [{"role": "user", "content": self.WELCOME_CONTENT}] if self.WELCOME_CONTENT else []
        )
        self.llm_context = gemini.GeminiMultimodalLiveContext(
            messages=messages,
            tools=self.TOOLS,
        )
        self.context_aggregator = self.llm_service.create_context_aggregator(
            context=self.llm_context
        )
        self.talking_animation = processors.TalkingAnimationProcessor()
        self.rtvi_speaking = rtvi.RTVISpeakingProcessor()
        self.rtvi_user_transcription = rtvi.RTVIUserTranscriptionProcessor()
        self.rtvi_bot_transcription = rtvi.RTVIBotTranscriptionProcessor()
        self.rtvi_metrics = rtvi.RTVIMetricsProcessor()
        self.rtvi_config = rtvi.RTVIConfig(config=[])
        self.rtvi_processor = rtvi.RTVIProcessor(config=self.rtvi_config)
        # pipeline
        self.params = task.PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
            enable_usage_metrics=True,
        )
        self.pipeline = pipeline.Pipeline(
            processors=[
                self.transport.input(),
                self.rtvi_processor,
                self.context_aggregator.user(),
                self.llm_service,
                self.rtvi_speaking,
                self.rtvi_user_transcription,
                self.rtvi_bot_transcription,
                self.talking_animation,
                self.rtvi_metrics,
                self.transport.output(),
                self.context_aggregator.assistant(),
            ]
        )
        self.pipeline_task = task.PipelineTask(
            pipeline=self.pipeline,
            params=self.params,
        )
        self.pipeline_runner = runner.PipelineRunner(name=self.NAME)

    async def run(self):
        """Run the bot."""
        logger.info(f"Run bot: {self.NAME}")

        # event handlers
        @self.rtvi_processor.event_handler("on_client_ready")
        async def on_client_ready(rtvi_processor):
            await rtvi_processor.set_bot_ready()

        @self.transport.event_handler("on_first_participant_joined")
        async def on_first_participant_joined(transport, participant):
            await transport.capture_participant_transcription(participant_id=participant["id"])
            await self.pipeline_task.queue_frames(
                frames=[self.context_aggregator.user().get_context_frame()]
            )

        @self.transport.event_handler("on_participant_left")
        async def on_participant_left(transport, participant, reason):
            await self.pipeline_task.queue_frame(frame=frames.EndFrame())

        # runner
        await self.pipeline_task.queue_frame(frame=self.talking_animation.quiet_frame)
        await self.pipeline_runner.run(task=self.pipeline_task)
        logger.info(f"Bot running: {self.NAME}")
