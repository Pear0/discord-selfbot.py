# discord-selfbot.py

This is my personal Discord self-bot. Feel free to host and use it yourself.

Currently it's only command is `>tex` which will take whatever comes after it and will compile it as a `latex` snippet.

For example, send the message `>tex $$\int_{a}^{b} x^2 dx$$` will trigger the selfbot to compile it and respond with:

![](examples/integral.png)

## Usage

To use this bot, you must create a file called `config.json` at the root level with the field `token` containing your self token.

```json
{
  "json": "token here"
}
```
