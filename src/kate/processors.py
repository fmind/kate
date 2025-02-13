"""Additional processors for Pipecat pipelines."""

# %% IMPORTS

import importlib.resources

from PIL import Image
from pipecat.frames import frames
from pipecat.processors import frame_processor

from kate import images

# %% ASSETS

ASSET_FILES = importlib.resources.files(images)

# %% PROCESSORS


class TalkingAnimationProcessor(frame_processor.FrameProcessor):
    """Manages the bot's visual animation states."""

    CACHED_SPRITES: dict[str, frames.OutputImageRawFrame] = {}

    def __init__(self):
        super().__init__()
        self.sprites = []
        self.is_talking = False
        for traversable in ASSET_FILES.iterdir():
            path = str(traversable)  # cast
            if path not in self.CACHED_SPRITES:
                with Image.open(fp=path) as image:
                    self.CACHED_SPRITES[path] = frames.OutputImageRawFrame(
                        image=image.tobytes(), size=image.size, format=image.format
                    )
            self.sprites.append(self.CACHED_SPRITES[path])
        # create a smooth animation (reverse)
        self.sprites.extend(self.sprites[::-1])
        # static frame for when bot is listening
        self.quiet_frame = self.sprites[0]  # first
        # animation sequence for when bot is talking
        self.talking_frame = frames.SpriteFrame(images=self.sprites)

    async def process_frame(self, frame: frames.Frame, direction: frame_processor.FrameDirection):
        """Process incoming frames and update animation state."""
        await super().process_frame(frame, direction)
        # switch to talking animation when bot starts speaking
        if isinstance(frame, frames.BotStartedSpeakingFrame):
            if not self.is_talking:
                await self.push_frame(frame=self.talking_frame)
                self.is_talking = True
        # return to static frame when bot stops speaking
        elif isinstance(frame, frames.BotStoppedSpeakingFrame):
            await self.push_frame(frame=self.quiet_frame)
            self.is_talking = False
        await self.push_frame(frame=frame, direction=direction)
