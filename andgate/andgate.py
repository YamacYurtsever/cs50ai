import random

# Define problem

# Collect and prepare data
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [0, 0, 0, 1]

# Choose a neural network architecture --> Feedforward

# Define input and output layers
input_size = 2
output_size = 1

# Specify hidden layers

# Initialize weights and biases
W = [random.random() for i in range(input_size)]
b = random.random()

# Tune hyperparameters
learning_rate = 0.01
epochs = 10000

# Choose activation functions --> logistic sigmoid
def sigmoid(wdotx):
    return 1 / (1 + 2.7**(-wdotx))

# Choose a loss function --> L2
def L2(actual, predicted):
    return (actual - predicted)**2

# Choose an optimization algorithm --> Gradient Descent

# Train the neural network
for epoch in range(epochs):
    total_error = 0

    # Update weights and bias for each data point
    for i in range(len(X)):
        # Forward pass
        wdotx = b
        for j in range(input_size):
            wdotx += W[j] * X[i][j]
        predicted = sigmoid(wdotx)

        # Compute the error
        actual = Y[i]
        total_error += L2(actual, predicted)

        # Backward pass (Gradient Descent)
        for j in range(input_size):
            W[j] += learning_rate * (actual - predicted) * predicted * (1 - predicted) * X[i][j]
        b += learning_rate * (actual - predicted) * predicted * (1 - predicted)

print('Final Weights:', W)
print('Final Bias:', b)

# Evaluate on test data
test_input = [[0, 0], [0, 1], [1, 0], [1, 1]]

predicted_output = []
for i in range(len(test_input)):
    wdotx = b
    for j in range(input_size):
        wdotx += W[j] * test_input[i][j]
    predicted_output.append(round(sigmoid(wdotx)))

print('Predicted Output:', predicted_output)

# Deploy Model