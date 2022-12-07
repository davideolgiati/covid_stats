from .connectors.resilientHttpConnector import ResilientHttpConnector
import logging as log
import pandas as pd


class GithubDataService:
    def __init__(self, base_url, data_path):
        self.conn = ResilientHttpConnector(base_url, timeout=2)
        self.data_path = data_path
        log.debug(f"Set data path to {data_path}")
        self.data = None

    def set_data_path(self, data_path):
        self.data_path = data_path
        log.debug(f"Set data path to {data_path}")

    def retrieve_data(self):
        self.data = self.conn.get(self.data_path)
        log.info(f"Retrieved {len(self.data)} records")
        self.data = pd.DataFrame(self.data)
        self.data.set_index("data")

    def process_data(self):
        if self.data is None:
            log.warning("Can't process an empty Dataset")
        else:
            pd.set_option('display.precision', 3)

            columns = ["totale_positivi", "deceduti"]
            index = ["min", "max", "median", "mean"]
            stats = {k: index for k in columns}

            print("Totali da inizio pandemia a oggi divisi per regioni")
            print(self.data.groupby("denominazione_regione")[columns].sum())
            print("\n\nMedia da inizio pandemia a oggi divisi per regioni")
            print(self.data.groupby("denominazione_regione")[columns].mean())