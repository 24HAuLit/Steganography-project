# Steganography Project

## Project Summary

This project is a cybersecurity application designed to demonstrate the dual nature of covert digital communication: Steganography (data concealment) and Steganalysis (forensic detection). Developed as a modern web-based tool using Python and Streamlit, the project provides a controlled environment for users to embed encrypted text within image files and immediately evaluate the security of that concealment using an automated AI Stego-Analyst. 

## Technical Methodology: The Encoding Engine

The core of the application is a manual implementation of Least Significant Bit (LSB) insertion. This technique targets the binary structure of digital images, specifically the Red, Green, and Blue (RGB) color channels. By modifying the final bit of these values (e.g., shifting a byte from 11111110 to 11111111), the engine can store 3 bits of data per pixel. Because the resulting change in color intensity is mathematically minimal (1/255), the modification is visually imperceptible to the human eye. To ensure data integrity, the system strictly utilizes lossless PNG containers, preventing the compression artifacts associated with JPEGs from corrupting the hidden payload.

## AI Stego-Analyst: Forensic Evaluation

This project will include an AI Stego-Analyst module. Rather than simply assuming a message is secure because it is invisible to human eyes, the application integrates pre-trained forensic libraries to perform automated steganalysis. This "Analyst" uses statistical models and machine learning algorithms to detect anomalies in pixel distribution and noise patterns. It provides a Detectability Score, informing the user of the probability that their hidden message could be uncovered by automated surveillance or forensic software. This component evaluates the "quality" of the hiding process, flagging instances where a payload is too large and creates detectable statistical signatures.