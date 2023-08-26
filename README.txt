DISCLAIMER!:
    **UNCOMMENT BUY/SELL SECTION AT YOUR OWN RISK!**
    It WILL spend your entire brokerage balance if it thinks there is a good opportunity.
    The logic behind this is not developed enough yet.
    I am halting development on this side of the project until I have trained my neural network in pytorch to my satisfaction.

About the project:
    This project is a Crypto Bot for use with Robinhood.
    It is very early in development and I don't suggest that anyone use it in its current state. - Reread the disclaimer.

How it works:
    - The bot logs into robinhood with account details provided in settings.py.
    - Bot gets historicals from monthly average. Gets hourly average every 15 seconds.
        - Compares the two values and assigns a weight.
            - Below 1.0 is seen as a 'good' price.
        - If hourly weight and monthly weight together are < 2:
            - A limit buy will be placed.
        - If limit sell goes above the purchase price:
            - A limit sell is immediately placed.

Requirements:
    - Python 3.11
    - robin-stocks

Notes:
    This is being actively worked on. Currently I am working on pytorch implementation and building a neural network for price analysis.
    Extensive neural training needs to be done. I've tabled a few things that really need to be worked on before this is used on a real account.
    Some account information doesn't update properly within the while loop. The bot doesn't understand pending trades at present.

License:

MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Note from the Author:
Thanks for reading! - Zak