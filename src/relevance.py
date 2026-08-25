import pandas as pd


class RelevanceEvaluator:

    def __init__(self, threshold=2):

        self.threshold = threshold


    def calculate_score(self, product_a, product_b):

        score = 0

        if product_a["jenis"] == product_b["jenis"]:
            score += 1

        if product_a["kategori"] == product_b["kategori"]:
            score += 1

        if (
            pd.notna(product_a["ram_gb"])
            and pd.notna(product_b["ram_gb"])
            and product_a["ram_gb"] == product_b["ram_gb"]
        ):
            score += 1

        if (
            pd.notna(product_a["storage_gb"])
            and pd.notna(product_b["storage_gb"])
            and product_a["storage_gb"] == product_b["storage_gb"]
        ):
            score += 1

        return score


    def is_relevant(self, product_a, product_b):

        score = self.calculate_score(
            product_a,
            product_b
        )

        return score >= self.threshold


    def get_reasons(self, product_a, product_b):

        reasons = []

        if product_a["jenis"] == product_b["jenis"]:
            reasons.append("Jenis sama")

        if product_a["kategori"] == product_b["kategori"]:
            reasons.append("Kategori sama")

        if (
            pd.notna(product_a["ram_gb"])
            and pd.notna(product_b["ram_gb"])
            and product_a["ram_gb"] == product_b["ram_gb"]
        ):
            reasons.append("RAM sama")

        if (
            pd.notna(product_a["storage_gb"])
            and pd.notna(product_b["storage_gb"])
            and product_a["storage_gb"] == product_b["storage_gb"]
        ):
            reasons.append("Storage sama")

        return reasons