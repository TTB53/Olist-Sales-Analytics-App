import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

import pandas as pd
import math
import numpy as np
from joblib import dump


class ForecastingModel:

    def prep_dataframe_for_ml_models(self, df, col_of_interest):

        # place targets at the end of the dataframe.
        if type(col_of_interest) is list:
            cols = list(df.columns.values)
            for col in col_of_interest:
                cols.pop(cols.index(col))
                df = df[cols + [col]]
        else:
            cols = list(df.columns.values)
            cols.pop(cols.index(col_of_interest))
            df = df[cols + [col_of_interest]]

    def encode_categorical_feature(self, df, col, encoder="target"):
        from sklearn.preprocessing import OneHotEncoder, LabelEncoder
        # creating encoding for categorical features Label Encoder can be used for
        # Ordinal Categorical Features

        if type(col) is list:
            for c in col:
                if encoder is "label":
                    encoder = LabelEncoder()
                    df[c] = encoder.fit_transform(df[c])
                    print(c, "\\", df[c])
                    # return df
                elif encoder is "target":
                    # df["{}_t_encoding".format(c)] = df[c]
                    encodings = df.groupby(c)["won_target"].mean().reset_index()
                    encodings.rename(columns={c: c, "won_target": "{}_encoded".format(c)}, inplace=True)
                    print(c, "\\", encodings)
                    df = df.merge(encodings, how="left", on=c)
                    df = df.drop(c, axis=1)
                    # return df
                else:
                    encoder = OneHotEncoder()
                    # reshape the 1-D country array to 2-D as fit_transform expects 2-D and finally fit the object
                    X = encoder.fit_transform(df[c].values.reshape(-1, 1)).toarray()
                    # To add this back into the original dataframe
                    dfOneHot = pd.DataFrame(X, columns=["{}_".format(c) + str(int(i)) for i in range(df.shape[1])])
                    df = pd.concat([df, dfOneHot], axis=1)
                    # dropping the country column
                    df = df.drop([c], axis=1)
                    # printing to verify
                    print(df.head())
            print("Encoded DF\n", df.head(15), "\n", df.tail(15))
            return df

        else:
            if encoder is "label":
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col])
                print(df[col])
                return df
            elif encoder is "target":
                encodings = df.groupby(col)["{}_t_encoding".format(col)].mean().reset_index()
                print(encodings)
                df = df.merge(encodings, how="left", on=col)
                df = df.drop(col, axis=1, inplace=True)
                return df
            else:
                encoder = OneHotEncoder()
                # reshape the 1-D country array to 2-D as fit_transform expects 2-D and finally fit the object
                X = encoder.fit_transform(df[col].values.reshape(-1, 1)).toarray()
                # To add this back into the original dataframe
                dfOneHot = pd.DataFrame(X, columns=["{}_".format(col) + str(int(i)) for i in range(df.shape[1])])
                df = pd.concat([df, dfOneHot], axis=1)
                # dropping the country column
                df = df.drop([col], axis=1)
                # printing to verify
                print(df.head())

                return df

    def save_model(self, model, filename, save_path):
        path = save_path + "/" + filename + '.joblib'
        print(filename, " save location: \n", path)
        dump(model, path)

    def linear_regression(self, df, x_col, y_col,
                          pred_1, pred_2, pred_3,
                          debug=True, save=True,
                          scale=True, scaler=1,
                          filename='lr_model',
                          save_path='./ml/models'):
        # Creating the Linear Regression Model
        model = LinearRegression(fit_intercept=True)

        # Converting Timestamp and Datetime features to numeric.
        print(type(df[x_col][0]))
        if type(df[x_col][0]) == pd._libs.tslib.Timestamp or type(df[x_col][0]) == "Datetime" or isinstance(
                df[x_col][0],
                pd._libs.tslibs.timestamps.Timestamp):
            df[x_col] = pd.to_numeric(pd.to_datetime(df[x_col]))
            x = np.array(df[x_col]).reshape(-1, 1)
        else:
            x = np.array(df[x_col]).reshape(-1, 1)

        y = np.array(df[y_col]).reshape(-1, 1)

        # Splitting and training the model
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

        if scale is True:
            if scaler == 0:
                df = StandardScaler().fit_transform(df)
            else:
                df = MinMaxScaler().fit_transform(df)

        model = model.fit(X_train, y_train)

        pred_1 = pd.to_numeric(pd.to_datetime([pred_1]))
        pred_1 = np.array(pred_1).reshape(-1, 1)

        pred_2 = pd.to_numeric(pd.to_datetime(pred_2))
        pred_2 = np.array(pred_2).reshape(-1, 1)

        pred_3 = pd.to_numeric(pd.to_datetime([pred_3]))
        pred_3 = np.array(pred_3).reshape(-1, 1)

        if debug:
            print(
                """
                The Models Coefficent of Determination:  {}\n
                Intercept : {}\n
                Slope     : {}\n
                Prediction Value 1: {}\n
                Prediction Value 2: {}\n
                Prediction Value 3: {}
                """.format(
                    model.score(X_test, y_test),
                    model.intercept_,
                    model.coef_,
                    model.predict(pred_1),
                    model.predict(pred_2),
                    model.predict(pred_3)
                )
            )

        if save:
            self.save_model(model=model, filename=filename, save_path=save_path)

        return model

    def knn_regression(self, X, y, save, filename, save_path):
        prediction1 = [[.162875, 0, 0, 0]]
        prediction2 = [[.162875, 1, 1, 1]]
        prediction3 = [[.532725, 1, 0, 0]]

        neigh = KNeighborsRegressor()
        neigh.fit(X, y)
        neighbors = neigh.kneighbors_graph(prediction1)
        print("Prediction 1 Neighbors\n", neighbors.toarray())
        print("Prediction 1\n", neigh.predict(prediction1))
        print("Prediction 2\n", neigh.predict(prediction2))
        print("Prediction 3\n", neigh.predict(prediction3))
        # print("Score\n", neigh.score([prediction3, prediction2, prediction1], [1, 1, 0]))
        if save:
            self.save_model(model=neigh, filename=filename, save_path=save_path)
        return neigh
