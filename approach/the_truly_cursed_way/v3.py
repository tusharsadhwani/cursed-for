from __future__ import annotations

import codecs
from encodings import utf_8
import re

beginning_with_for_regex = re.compile(r'^\s*for\b')
for_in_regex = re.compile(r'^\s*for\b.+?\bin\b')
indent_regex = re.compile(r'^\s*')
cursed_for_regex = re.compile(r'^\s*for\s*\((.*?);(.*?);(.*?)\):(.*)$')

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

        initializer_stmt = f'{indent_spaces}{initializer.strip()}' 
        increment_stmt = f'{body_indent_level}{increment.strip()}'

        condition = condition.strip()
        if condition == '':
            while_stmt = f'{indent_spaces}while True:'
        else:
            while_stmt = f'{indent_spaces}while {condition}:'

        new_source.append(initializer_stmt)
        new_source.append(while_stmt)
        new_source.extend(new_block_lines)
        new_source.append(increment_stmt)

    return new_source

def transform_cursed_for(source: str) -> str:
    lines = source.splitlines()
    new_lines = _transform_cursed_for(lines)
    return '\n'.join(new_lines)


def cursed_for_decode(source_bytes: bytes | memoryview) -> tuple[str, int]:
    source = bytes(source_bytes).decode('utf-8')
    modified_source = transform_cursed_for(source)
    return modified_source, len(source_bytes)

def cursed_for_loop_decoder(encoding: str) -> codecs.CodecInfo | None:
    if encoding not in ('cursed_for', 'cursed-for'):
        return None
    
    return codecs.CodecInfo(
        name=encoding,
        encode=utf_8.encode,
        decode=cursed_for_decode,
    )

codecs.register(cursed_for_loop_decoder)

import test_v3
test_v3.main()
