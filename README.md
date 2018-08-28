# `vk-bot`

`vk-bot` is a Python 2/3 VK bot builder. 


## Install

```bash
pip install vk-bot
```

## Usage

```python
import vk_bot
import operator

bot = vk_bot.VkBot('YOUR_ACCESS_TOKEN')

OPS = {
    'add': operator.add,
    'sub': operator.sub,
    'mul': operator.mul,
    'div': operator.truediv
}

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
```
