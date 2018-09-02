# `vk-bot`

`vk-bot` is a Python 2/3 VK bot builder built with
[`vk-client`](https://github.com/Suenweek/vk-client).


## Install

```bash
pip install vk-bot
```

## Usage

```python
import vk_bot
import operator

# Create bot
bot = vk_bot.VkBot('YOUR_ACCESS_TOKEN')

OPS = {
    'add': operator.add,
    'sub': operator.sub,
    'mul': operator.mul,
    'div': operator.truediv
}

# Register commands
@bot.command(args={
    'op': {'choices': list(OPS)},
    'a': {'type': int},
    'b': {'type': int}
})
def calc(_, op, a, b):
    """Simple calculator."""
    try:
        return f'Result: {OPS[op](a, b)}'
    except ArithmeticError as e:
        return f'Error: {e}'

# Run
bot.run()
```
