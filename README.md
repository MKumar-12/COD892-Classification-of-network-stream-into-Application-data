# Network Traffic Analysis and Classification Using Transformers

This repository contains the codebase for a project focused on classifying network traffic and identifying applications using a Transformer-based model. 
The project was developed as part of the COD891 course at IIT Delhi under the supervision of Prof. Vireshwar Kumar and Prof. Tarun Mangla.

## Project Overview
In this project, we propose a Transformer-based approach to classify network traffic and identify applications from encrypted network streams. 
The Transformer model is currently trained and evaluated on the ISCX-VPN-NonVPN dataset. 

We're currently working on the process to set ground truth labels for network stream captured within our organization. We'll then re-evaluate our model for real-time network stream.

## Key Features

- **Transformer Model**: A novel application of the Transformer architecture to classify network traffic and identify applications.
- **Automatic Feature Extraction**: No need for manual feature extraction, reducing the likelihood of human error.
- **Performance on Encrypted Traffic**: The model shows high accuracy in handling encrypted traffic, making it suitable for modern network environments.

## Model Architectures
### Deep Packet - CNN
- **Layers**: Two convolutional layers followed by a pooling layer, fully connected layers, and a softmax classifier.
- **Overfitting Prevention**: Dropout technique applied in the fully connected layers.
- **Classifier**: Softmax.

### Deep Packet - SAE
- **Layers**: Five fully connected layers with varying numbers of neurons.
- **Overfitting Prevention**: Dropout technique applied after each layer.
- **Classifier**: Softmax with 17 neurons for application identification and 12 neurons for traffic characterization.

### Transformer
- **Architecture**: Standard Transformer model with modifications for network traffic classification.
- **Performance**:
  - Traffic Classification: 92.10% accuracy
  - Application Identification: 93.25% accuracy

## Results
The Transformer model achieved the following metrics:

| Task                        | Recall | Precision | F1-Score |
|-----------------------------|--------|-----------|----------|
| **Traffic Characterization** | 0.92   | 0.98      | 0.95     |
| **Application Identification** | 0.93   | 0.97      | 0.95     |

## Dataset
The model was trained and tested on the ISCX-VPN-NonVPN dataset, which contains a variety of network streams, including both VPN and non-VPN traffic.

## References
The project builds upon prior work in the field of network traffic analysis, including deep learning approaches like CNNs, LSTMs, and hybrid models. For more details, please refer to the references listed in the project presentation.

## Contributors
- **Sajal Verma** ([2023MCS2490@iitd.ac.in](mailto:2023MCS2490@iitd.ac.in))
- **Manish Kumar** ([2023MCS2497@iitd.ac.in](mailto:2023MCS2497@iitd.ac.in))
