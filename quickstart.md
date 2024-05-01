# Quickstart
## Installation
You can install skypy-api via pip:
`pip install skypy-api`
Or install the latest version from GitHub: https://github.com/FuchsCrafter/skypy/releases/latest
## Obtaining an API key
As a developer, you need an API key from Hypixel in order to use some features of their API. Obtaining one is pretty easy, you just need to register or log in at the [Hypixel developer dashboard](https://developer.hypixel.net/dashboard). For development, you can generate a development key, and for production, you need to register a permanent application on this dashboard.
## First steps
*Note: You can find more examples on the [example page](https://fuchscrafter.github.io/skypy/examples/)*
### Importing & Declaring the class
To import the module, use `import skypy`. Then, you need to declare a variable with the skypy-class. This object acts as the base for every other function of this module. You can do it like this:
```python
import skypy
skypyapi = skypy.skypy("API-KEY") # Replace API-KEY with your key
```
### Print the current bingo goals
You could then use this to get the current bingo goals:
```python
print(skypyapi.getCurrentBingo()["goals"])
```
And there you have it! This should print the current bingo goals to the python console.
### Full code
The full code should look like this: 
```python
import skypy
skypyapi = skypy.skypy("API-KEY") # Replace API-KEY with your key
print(skypyapi.getCurrentBingo()["goals"])
```
## More examples
You can find more examples on the [example page](https://fuchscrafter.github.io/skypy/examples/).

For Info on how to use the module, please take a look into the [wiki](https://github.com/FuchsCrafter/skypy/wiki).
