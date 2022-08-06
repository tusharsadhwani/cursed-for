from __future__ import annotations

import codecs
from encodings import utf_8
import re

beginning_with_for_regex = re.compile(r'^\s*for\b')
for_in_regex = re.compile(r'^\s*for\b.+?\bin\b')
indent_regex = re.compile(r'^\s*')
cursed_for_regex = re.compile(r'^\s*for\s*\((.+?);(.+?);(.+?)\):(.*)$')

def transform_cursed_for(source: str) -> str:
    new_source = []
    lines = source.splitlines(keepends=True)

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
        for_indent_level = indent_regex.match(line).group()

        if index >= len(lines):
            raise SyntaxError("Unexpected for-statement at end of file")

        next_line = lines[index]
        index += 1

        body_indent_level = indent_regex.match(next_line).group()

        for_body_lines = [next_line]

        while index < len(lines):
            next_line = lines[index]
            if not next_line.startswith(body_indent_level):
                break

            for_body_lines.append(next_line)
            index += 1
        
        initializer_stmt = f'{for_indent_level}{initializer.strip()}\n' 
        while_stmt = f'{for_indent_level}while {condition.strip()}:\n'
        increment_stmt = f'{body_indent_level}{increment.strip()}\n'

        new_source.extend(initializer_stmt)
        new_source.extend(while_stmt)
        new_source.extend(for_body_lines)
        new_source.extend(increment_stmt)

    return ''.join(new_source)



def cursed_for_decode(source_bytes: bytes | memoryview) -> tuple[str, int]:
    source = bytes(source_bytes).decode('utf-8')
    modified_source = transform_cursed_for(source)
    print(modified_source)
    print('***')
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

import test_v1
test_v1.main()
