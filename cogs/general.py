from os import link
import random
from cogs import utils
import discord
from discord.ext import commands, vbu, tasks
import math
import decimal
from PIL import Image
import requests
from io import BytesIO


class General(vbu.Cog):
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def pi(self, ctx: commands.Context, n: int):
        '''Calculates the first n digits of pi and returns them'''
        DIGITS = n

        if n < 1 or n > 1968:
            return await ctx.send("The max digits is 1968! please provide a number below that!")

        def pi_digits(x):
            """Generate x digits of Pi."""
            k, a, b, a1, b1 = 2, 4, 1, 12, 4
            while x > 0:
                p, q, k = k * k, 2 * k + 1, k + 1
                a, b, a1, b1 = a1, b1, p*a + q*a1, p*b + q*b1
                d, d1 = a/b, a1/b1
                while d == d1 and x > 0:
                    yield int(d)
                    x -= 1
                    a, a1 = 10*(a % b), 10*(a1 % b1)
                    d, d1 = a/b, a1/b1

        digits = [str(n) for n in list(pi_digits(DIGITS))]
        pi = "%s.%s" % (digits.pop(0), "".join(digits))
        return await ctx.send(f"Pi to the {n}th digit is **{pi}**!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def e(self, ctx: commands.Context, n: int):
        '''
        Calculates the first n digits of Euler's number and returns them (rounding the last digit)
        '''
        DIGITS = n

        if n < 1 or n > 1076:
            return await ctx.send("The max digits is 1076! please provide a number below that!")

        def factorial(n):
            factorials = [1]
            for i in range(1, n + 1):
                factorials.append(factorials[i - 1] * i)
            return factorials

        def compute_e(n):
            decimal.getcontext().prec = n + 1
            e = 2
            factorials = factorial(2 * n + 1)
            for i in range(1, n + 1):
                counter = 2 * i + 2
                denominator = factorials[2 * i + 1]
                e += decimal.Decimal(counter / denominator)
            return e

        e = (compute_e(DIGITS - 1))
        return await ctx.send(f"Eulers Number to the {n}th digit is **{e}**!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def fibonacci(self, ctx: commands.Context, n: int):
        '''
        Calculates the number in the Fibonacci sequence at the nth term and returns it
        '''
        DIGITS = n

        if n < 1 or n > 9333:
            return await ctx.send("The max term is 9333! please provide a number below that!")

        def compute_fibonacci(n):
            if n == 1:
                return 0
            term_1, term_2 = 0, 1
            count = 0
            while count < n-1:
                fib_num = term_1 + term_2
                term_1 = term_2
                term_2 = fib_num
                count += 1
            return term_1

        fib_num = compute_fibonacci(DIGITS)
        return await ctx.send(f"The Fibonacci Sequence to the {n}th term is **{fib_num}**!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def primefactors(self, ctx: commands.Context, n: int):
        '''
        Breaks n down to its prime factors and return them
        '''
        NUMBER = n
        if n > 1000000000000000:
            return await ctx.send("The max term is 1,000,000,000,000,000! please provide a number below that!")

        def prime_factors(n):
            i = 2
            factors = []
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
                    factors.append(str(i))
            if n > 1:
                factors.append(str(n))
            return factors

        fib_num = prime_factors(NUMBER)
        return await ctx.send(f"The prime factors of {n} are **{', '.join(fib_num)}**!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def primenumbers(self, ctx: commands.Context, start: int, end: int):
        '''
        Finds all prime numbers from start to end
        '''
        if start < 0 or end < 0 or end <= start or end > 2250:
            return await ctx.send("Please enter a start and end greater than 0, an end greater than your start, and an end less than 2,250")
        prime_numbers = []
        for i in range(start, end):
            if i == 1:
                prime_numbers.append(str(i))
            if i == 4:
                continue
            if i > 1:
                prime = True
                for x in range(2, i//2):
                    if i % x == 0:
                        prime = False
                        break
                if prime == True:
                    prime_numbers.append(str(i))
        return await ctx.send(f"The prime numbers from {start} to {end} are **{', '.join(prime_numbers)}**!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def cat_or_dog(self, ctx: commands.Context):
        '''
        Figures out if a picture is a cat or a dog
        '''
        response = requests.get(ctx.message.attachments[0].url)
        img = Image.open(BytesIO(response))


def setup(bot):
    bot.add_cog(General(bot))
