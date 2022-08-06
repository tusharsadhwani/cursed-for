# cursed-for

Implementing C-style for loops in Python.

This was implemented because of a cursed idea I had one night, which I put on
[twitter](https://twitter.com/sadhlife/status/1497501076589019139):

![](https://user-images.githubusercontent.com/43412083/173145281-1a63ad93-56c0-4fd0-b8f1-78e7bf7005d6.png)

I wrote a [blog](TODO) on the approaches I went through to implement this.

The rough iterations that happened during the development are documented in the
[approach folder](./approach). It contains both the AST manipulation method, and
the "truly cursed" method.

## Installation

```text
pip install cursed-for
```

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
