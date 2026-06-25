from train import train
from predict import predict


class MLPipeline:

    def train_model(self, ticker):
        return train(ticker)

    def predict_signal(self, ticker):
        return predict(ticker)
