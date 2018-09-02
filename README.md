# `vk-bot`

`vk-bot` is a Python 2/3 VK bot builder built with
[`vk-client`](https://github.com/Suenweek/vk-client).


## Install

```bash
pip install vk-bot
```

## Usage

#### Create bot
```python
import vk_bot

bot = vk_bot.VkBot('YOUR_ACCESS_TOKEN')
```

#### Register cmd handlers
```python
@bot.command(pass_msg=True)
def whoami(msg):
    """Print effective user name."""
    return f'{msg.sender.first_name} {msg.sender.last_name}'
```

#### More involved cmd handler
```python
import operator

OPS = {
    'add': operator.add,
    'sub': operator.sub,
    'mul': operator.mul,
    'div': operator.truediv
}

@bot.command(args={
    'op': {'choices': list(OPS)},
    'a': {'type': int},
    'b': {'type': int}
})
def calc(op, a, b):
    """Simple calculator."""
    try:
        return f'Result: {OPS[op](a, b)}'
    except ArithmeticError as e:
        return f'Error: {e}'
```

#### Run bot
```python
# Run
bot.run()
```
