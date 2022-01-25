import asyncio
from glance.cli import cmd
from glance.cli import parser

asyncio.run(cmd.run_with_args(parser.parse_args()))
