class RiskScore:
    @staticmethod
    def calculate(probability: float) -> float:
        if probability < 0:
            probability = 0

        if probability > 1:
            probability = 1

        return round(probability * 100, 2)
