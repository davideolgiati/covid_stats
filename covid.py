# Davide Olgiati 14/03/2020

import json
from services.GithubDataService import GithubDataService


def banner():
    with open("resources/banner.txt", "r") as fp:
        print("".join(fp.readlines()))


def main():
    with open("resources/config.json", "r") as fp:
        config = json.load(fp)

    data_engine = GithubDataService(config["github"]["base_url"],
                                    config["github"]["data_path"])

    data_engine.retrieve_data()

    data_engine.process_data()


if __name__ == "__main__":
    banner()
    main()
