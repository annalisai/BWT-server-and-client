# Client-Server BWT Project

## Overview

This project implements a client-server application that performs the Burrows-Wheeler Transform (BWT) and its inverse on given DNA sequences. The client sends a command and data to the server, which processes the request and returns the result to the client. It is divided into two main files:

## Project Structure

- **Client_project.py**: Contains the client implementation.
- **Server_project.py**: Contains the server implementation.
- **Test_project.py**: Contains unit tests for the client-server system and BWT functions.

## Brief Description: 
Implement a server (along with a corresponding client) that accepts a DNA sequence and returns its Burrows Wheeler Transform (BWT). It should also accept a BWT and return the corresponding original DNA sequence.

## Project Scope
The aim of the project is to demonstrate the implementation of a client-server system for BWT, allowing users to send strings to the server for transformation and receive the result.

## Requirements

- Python 3.x

## Installation and Setup
To get started with the project, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/annalisai/BWT-server-and-client
   ```

2. Navigate to the project directory:
   ```
   cd BWT-server-and-client
   ```

3. Start the server:
   ```
   python3 Server_project.py
   ```

## Usage

To perform the Burrows-Wheeler Transform on a DNA sequence:
```
python3 Client_project.py --host 127.0.0.1 --port 8080 --command BWT
```
You will be prompted to enter the sequence: 
```
Please enter the data: ATGC
```

To perform the inverse Burrows-Wheeler Transform on a BWT sequence:
```
python3 Client_project.py --host 127.0.0.1 --port 8080 --command InverseBWT
```
You will be prompted to enter the sequence: 
```
Please enter the data: C$GTA
```

## Testing with unittest

The testing_project.py file contains unit tests for the server-client connection, the BWT functions, input validation, and integration testing of the BWT system. These tests ensure that the server and client functions correctly handle different types of input and commands.

To run the tests:
```
python3 -m unittest Testing_project.py
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
