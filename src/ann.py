from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error # Install error metrics 
from sklearn.linear_model import LinearRegression # Install linear regression model
from sklearn.neural_network import MLPRegressor # Install ANN model 
from sklearn.preprocessing import StandardScaler # to scale for ann

def func(x_data,y,split):
    print(len(x_data))
    print(len(y))
    X_train = x_data[:split]
    X_test = x_data[split:]
    y_train = y[:split]
    y_test = y[split:]
    print(f"y_test : {y_test}")
    print(f"X_test : {X_test}")
    MLP = MLPRegressor(random_state=1, max_iter=1000, hidden_layer_sizes = (100,), activation = 'identity',learning_rate = 'adaptive').fit(X_train, y_train)
    MLP_pred = MLP.predict(X_test)
    MLP_MSE = mean_squared_error(y_test, MLP_pred)
    MLP_R2 = MLP.score(X_test, y_test)

    print('Muli-layer Perceptron R2 Test: {}'.format(MLP_R2))
    print('Multi-layer Perceptron MSE: {}'.format(MLP_MSE))
    plt.plot([i for i in range(len(y_test))],y_test)
    plt.plot([i for i in range(len(y_test))],MLP_pred)
    plt.show()

    return MLP_pred

if __name__ == "__main__":
    x = [2*i for i in range(1000)]
    y = [2*i for i in range(10,1001)]
    x_data = [x[i:i+10] for i in range(0,991)]
    print(len(x_data))
    print(len(y))
    #X_train, X_test, y_train, y_test = train_test_split(x_data, y,random_state=1)
    split = 750
    X_train = x_data[:split]
    X_test = x_data[split:]
    y_train = y[:split]
    y_test = y[split:]
    print(f"y_test : {y_test}")
    print(f"X_test : {X_test}")
    MLP = MLPRegressor(random_state=1, max_iter=1000, hidden_layer_sizes = (100,), activation = 'identity',learning_rate = 'adaptive').fit(X_train, y_train)
    MLP_pred = MLP.predict(X_test)
    MLP_MSE = mean_squared_error(y_test, MLP_pred)
    MLP_R2 = MLP.score(X_test, y_test)

    print('Muli-layer Perceptron R2 Test: {}'.format(MLP_R2))
    print('Multi-layer Perceptron MSE: {}'.format(MLP_MSE))
    plt.plot([i for i in range(len(y_test))],y_test)
    plt.plot([i for i in range(len(y_test))],MLP_pred)
    plt.show()

    #prediction = func(x_data,y)
    #print(prediction)