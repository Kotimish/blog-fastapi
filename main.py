import asyncio

from scripts.seed_db import init_data


def main():
    asyncio.run(init_data())


if __name__ == "__main__":
    main()
