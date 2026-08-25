import pandas as pd


class RelevanceEvaluator:

    def __init__(self, data_path, threshold=2):

        self.products = pd.read_csv(data_path)
        self.threshold = threshold


    def calculate_score(self, product_a, product_b):

        score = 0

        if product_a["jenis"] == product_b["jenis"]:
            score += 1

        if product_a["kategori"] == product_b["kategori"]:
            score += 1

        if product_a["ram_gb"] == product_b["ram_gb"]:
            score += 1

        if product_a["storage_gb"] == product_b["storage_gb"]:
            score += 1

        return score


    def is_relevant(self, product_a, product_b):

        score = self.calculate_score(
            product_a,
            product_b
        )

        return score >= self.threshold