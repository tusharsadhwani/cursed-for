# cursed-for

Implementing C-style for loops in the Python REPL.

This was implemented because of a cursed idea I had one night, which I put on
[twitter](https://twitter.com/sadhlife/status/1497501076589019139):

![](https://user-images.githubusercontent.com/43412083/173145281-1a63ad93-56c0-4fd0-b8f1-78e7bf7005d6.png)

I wrote a [blog](TODO) on the approaches I went through to implement this.

The rough iterations that happened during the development are documented in the
[approach folder](./approach).

## Installation

```text
pip install cursed-for
```

## Usage

Note that this only really works in a REPL. If you try to import `cursed_for`
outside of a REPL, it will start a REPL anyway.

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
