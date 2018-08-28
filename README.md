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
@bot.command(
    name='calc',
    args_defs=[
        [('op',), {'choices': list(OPS)}],
        [('a',), {'type': int}],
        [('b',), {'type': int}]
    ]
)
def calc(msg, ns):
    try:
        rv = f'Result: {OPS[ns.op](ns.a, ns.b)}'
    except ArithmeticError as e:
        rv = f'Error: {e}'

    bot.vk.Message.send(
        peer=msg.sender,
        message=rv
    )

# Run
bot.run()
```
