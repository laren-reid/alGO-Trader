from train import train
from predict import predict


class MLPipeline:

    def train_model(self, dataframe):

        return train(dataframe)

    def predict_signal(self, dataframe):

        return predict(dataframe)
