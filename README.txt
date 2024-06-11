# Client-Server BWT Project

## Programming Language(s): Python

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

## Expected Outcome:
The server should:
-Handle client requests efficiently, avoiding waiting times wherever possible.
-Allow the user (server administrator) to run the server on an arbitrary host and port (e.g., by reading them from a configuration file instead of hard-coding them).

The client should:
-Allow the user to contact the server on an arbitrary host and port and with an arbitrary DNA (or BWT) query (by allowing the host and port, as well as the DNA sequence or the BWT, to be specified on the command line when the client is invoked).

## Testing with unittest:
The testing_project.py file contains unit tests for the server-client connection, the BWT functions, input validation, and integration testing of the BWT system. These tests ensure that the server and client functions correctly handle different types of input and commands.


## Execution Instructions

python3 Server_project.py

-This command activates the server to listen for client requests.

python3 Client_project.py --host 127.0.0.1 --port 8080 --command BWT

-You will be prompted to enter the sequence:

Please enter the data: ATGC

-This command sends a request to the server to perform the Burrows-Wheeler Transform on the DNA sequence "ATGC".

python3 Client_project.py --host 127.0.0.1 --port 8080 --command InverseBWT

-You will be prompted to enter the sequence:

Please enter the data: C$GTA

-This command sends a request to the server to perform the inverse Burrows-Wheeler Transform on the BWT sequence "CGTA$".

python3 -m unittest Testing_project.py

- This command test the correctness of the client and server 
implementation.


For further details on the implementation and usage of the system, refer to the source code of the `Server.py` and `Client.py` files.

