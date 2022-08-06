# cursed-for

Adding C-style for loops to Python, because you can.

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

This was made because of a cursed idea I had one night, which I put on
[twitter](https://twitter.com/sadhlife/status/1497501076589019139):

<p align="center">
  <img src="https://user-images.githubusercontent.com/43412083/173145281-1a63ad93-56c0-4fd0-b8f1-78e7bf7005d6.png" width="500">
</p>

And although this worked, I didn't like the look of it. But using the methods I
used, I was confined by Python's syntax, which really doesn't support the kind
of things I'd have liked to do. But then I stumbled upon a [couple][1] of
[packages][2] which gave me exactly the tools I needed to commit this atrocity.

## OK, but how is this possible?

I wrote a [blog][blog] on the approaches I went through to implement this.

The rough iterations that happened during the development are documented in the
[approach folder][3]. It contains both the AST manipulation method, and
the "truly cursed" method.

## The "old way" usage

The first version (as shown in the original tweet) is also present in the
repository, for archival purposes.

Note that this only really works in a REPL. To start it, run [cursedfor.py][4]
in the terminal. It's a single file, you can get it by just downloading the one
file if you want to.

```pycon
>>> with _for(i := 0, i < 10, i += 2):
...     print(i)
0
2
4
6
8
```

[1]: https://pypi.org/p/cstyle
[2]: https://github.com/asottile/future-fstrings
[3]: https://github.com/tusharsadhwani/cursed-for/approach
[4]: https://github.com/tusharsadhwani/cursed-for/approach/ast_manipulation/cursedfor.py
[ex]: https://github.com/tusharsadhwani/cursed-for/approach/the_truly_cursed_way/test_v3.py
[blog]: https://sadh.life/post/cursed-for
