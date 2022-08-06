# cursed-for

Implementing C-style for loops in Python:

```python
for (i = 0; i < 10; i += 3):
    print(i)
```

## Installation

```text
pip install cursed-for
```

## Usage

Add the following `# coding` comment at the top of the file in which you wish to
curse:

```python
# coding: cursed_for
```

Then write the cursed for-loops as needed. Check [this file][ex] for an example.

## But why?

This was implemented because of a cursed idea I had one night, which I put on
[twitter](https://twitter.com/sadhlife/status/1497501076589019139):

<p align="center">
  <img src="https://user-images.githubusercontent.com/43412083/173145281-1a63ad93-56c0-4fd0-b8f1-78e7bf7005d6.png" width="500">
</p>

And although this worked, I really didn't like the look of it. But using the
methods I used, I was confined to Python's syntax, which really doesn't support
the kind of things I'd have liked to do. But then I stumbled upon a [couple][2]
[packages][3] which gave me exactly the tools I needed to commit this atrocity.

I wrote a [blog](TODO) on the approaches I went through to implement this.

The rough iterations that happened during the development are documented in the
[approach folder](./approach). It contains both the AST manipulation method, and
the "truly cursed" method.

## The "old way" usage

Note that this only really works in a REPL. To start it, run [cursedfor.py][1]
in the terminal. It's a single file, you can get it by just downloading the one
file if you want to.

```pycon
>>> from cursed_for import _for, var
>>> with _for(i := var(0), i < 10, i += 2):
...     print(i)
0
2
4
6
8
```

[1]: ./approach/ast_manipulation/cursedfor.py
[2]: https://pypi.org/p/cstyle
[3]: https://github.com/asottile/future-fstrings
[ex]: approach/the_truly_cursed_way/test_v3.py
