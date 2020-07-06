from typing import List, Tuple
import textwrap

import tcod

import color


class Message:
    def __init__(self, text: str, color: Tuple[int, int, int] = (0, 0, 0)):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.messages: List[Message] = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def add_message(
        self, message_text: str, message_color: Tuple[int, int, int] = color.white,
    ) -> None:
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message_text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message_color))

    def render(self, console: tcod.Console) -> None:
        y_offset: int = self.y

        for message in self.messages:
            console.print(x=self.x, y=y_offset, string=message.text, fg=message.color)
            y_offset += 1
