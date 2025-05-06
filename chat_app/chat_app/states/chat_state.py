import asyncio
import os
from typing import List, TypedDict

import reflex as rx


class Message(TypedDict):
    text: str
    is_ai: bool


class ChatState(rx.State):
    messages: List[Message] = []
    typing: bool = False
    has_openai_key: bool = "OPENAI_API_KEY" in os.environ

    @rx.event
    def clear_messages(self):
        """Clears all chat messages and resets typing status."""
        self.typing = False
        self.messages = []

    @rx.event
    def send_message(self, form_data: dict):
        """Adds a user message and triggers AI response generation."""
        if self.typing:
            return
        message = form_data["message"].strip()
        if message:
            self.messages.append({"text": message, "is_ai": False})
            self.messages.append({"text": "", "is_ai": True})
            self.typing = True
            yield ChatState.generate_response

    @rx.event(background=True)
    async def generate_response(self):
        """Generates a response (mock or OpenAI)."""
        if not self.has_openai_key:
            await asyncio.sleep(1)
            response = "This is a mock response as the OPENAI_API_KEY is not set. Please set the environment variable to use the actual LLM."
            current_text = ""
            async with self:
                if not self.messages:
                    self.typing = False
                    return
            for char in response:
                if not self.typing:
                    break
                current_text += char
                async with self:
                    if self.messages:
                        self.messages[-1]["text"] = current_text
                await asyncio.sleep(0.02)
            async with self:
                self.typing = False
        else:
            from openai import OpenAI

            client = OpenAI()
            api_messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant.",
                }
            ]
            async with self:
                messages_to_send = self.messages[:-1]
            for msg in messages_to_send:
                role = "assistant" if msg["is_ai"] else "user"
                api_messages.append({"role": role, "content": msg["text"]})
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    stream=True,
                )
                current_text = ""
                async with self:
                    if not self.messages:
                        self.typing = False
                        return
                for chunk in stream:
                    if not self.typing:
                        break
                    if chunk.choices[0].delta.content is not None:
                        current_text += chunk.choices[0].delta.content
                        async with self:
                            if self.messages:
                                self.messages[-1]["text"] = current_text
            except Exception as e:
                async with self:
                    if self.messages:
                        self.messages[-1]["text"] = f"Error: {e!s}"

            finally:
                async with self:
                    self.typing = False
