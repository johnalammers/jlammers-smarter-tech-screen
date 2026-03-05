# John Lammers Tech Screen for Smarter

GitHub repo: https://github.com/johnalammers-realityforge/jlammers-smarter-tech-screen

## Environment and Technology Choices
Developed with Python 3.12.
Uses pytest for unit tests.
The commands that follow presume python is in your system path.

## Setup
From the command line, in the project root directory,run:
`pip install pytest`

## Run Tests
From the command line, in the project root directory, run: 
`python -m pytest`

## Example

```python
from sorter import sort

stack = sort(100, 100, 100, 10)
print(stack)  # SPECIAL
```

## A Note on Invalid Values
The spec did not cover invalid values: dimensions or mass <= 0. 
I'm raising a ValueError in my implementation. This would be 
something to run by the team calling this function to ensure 
that it's handled well upstream. I'm making the tentative 
assumption that we want the option to distinguish between a
"normal" REJECT and one due to a bug in the caller or a 
hardware failure in our measuring devices. We certainly don't 
want to place a package with invalid dimensions or weight on 
the STANDARD stack.
