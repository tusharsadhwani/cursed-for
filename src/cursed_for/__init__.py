"""cursed-for: Import this to use C-style for loops the in Python REPL."""
from __future__ import annotations

import codecs
import encodings
import io
import re
import sys

utf_8 = encodings.search_function("utf8")

beginning_with_for_regex = re.compile(r"^\s*for\b")
for_in_regex = re.compile(r"^\s*for\b.+?\bin\b")
indent_regex = re.compile(r"^\s*")
cursed_for_regex = re.compile(r"^\s*for\s*\((.*?);(.*?);(.*?)\):(.*)$")


def _transform_cursed_for(lines: list[str]) -> list[str]:
    new_source = []
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1

        if not beginning_with_for_regex.match(line):
            new_source.append(line)
            continue

        if for_in_regex.match(line):
            raise SyntaxError("Cannot use for-in loops in a cursed file!")

        match = cursed_for_regex.match(line)
        if match is None:
            raise SyntaxError(
                "Invalid for-syntax, use `for (initializer; condition; increment):`"
            )

        initializer, condition, increment = match[1], match[2], match[3]
        indent_spaces = indent_regex.match(line).group()

        if index >= len(lines):
            raise SyntaxError("Unexpected for-statement at end of file")

        next_line = lines[index]
        index += 1

        body_indent_level = indent_regex.match(next_line).group()

        block_lines = [next_line]
        while index < len(lines):
            next_line = lines[index]
            if not next_line.startswith(body_indent_level):
                break

            block_lines.append(next_line)
            index += 1

        new_block_lines = _transform_cursed_for(block_lines)

        initializer_stmt = f"{indent_spaces}{initializer.strip()}\n"
        increment_stmt = f"{body_indent_level}{increment.strip()}\n"

        condition = condition.strip()
        if condition == "":
            while_stmt = f"{indent_spaces}while True:\n"
        else:
            while_stmt = f"{indent_spaces}while {condition}:\n"

        new_source.extend(initializer_stmt)
        new_source.extend(while_stmt)
        new_source.extend(new_block_lines)
        new_source.extend(increment_stmt)

    return new_source


def transform_cursed_for(source: str) -> str:
    lines = source.splitlines(keepends=True)
    new_lines = _transform_cursed_for(lines)
    return "".join(new_lines)


def cursed_for_decode(
    source_bytes: bytes | memoryview,
    errors: str = "strict",
) -> tuple[str, int]:
    source = bytes(source_bytes).decode("utf-8", errors=errors)
    modified_source = transform_cursed_for(source)
    return modified_source, len(source_bytes)


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    """Copied from future-fstrings."""

    def _buffer_decode(self, input: bytes, errors: str, final: bool) -> tuple[str, int]:
        if final:
            return cursed_for_decode(input, errors)
        else:
            return "", 0


class StreamReader(utf_8.streamreader, object):
    """
    decode is deferred to support better error messages.

    Copied from future-fstrings.
    """

    _stream = None
    _decoded = False

    @property
    def stream(self):
        if not self._decoded:
            text, _ = cursed_for_decode(self._stream.read())
            self._stream = io.BytesIO(text.encode("utf-8"))
            self._decoded = True
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream
        self._decoded = False


def cursed_for_loop_decoder(encoding: str) -> codecs.CodecInfo | None:
    if encoding not in ("cursed_for", "cursed-for"):
        return None

    return codecs.CodecInfo(
        name=encoding,
        encode=utf_8.encode,
        decode=cursed_for_decode,
        incrementalencoder=utf_8.incrementalencoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=utf_8.streamwriter,
    )


def register():
    codecs.register(cursed_for_loop_decoder)


def cli():
    if len(sys.argv) >= 3:
        print("Syntax: cursed-for-decode [filename.py]")
        sys.exit(1)

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, "rb") as file:
            code = file.read()
    else:
        code = sys.stdin.buffer.read()

    print(code.decode("cursed_for"))
