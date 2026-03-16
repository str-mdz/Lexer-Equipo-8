
# Lexer Implementation – Compilers Project

## Description

This project implements a **Lexical Analyzer (Lexer)** developed in Python as part of the Compilers course.

A lexer is the first phase of the compilation process. It reads source code and converts a sequence of characters into meaningful units called **tokens**, such as keywords, identifiers, operators, punctuation symbols, constants and literals.

The implemented analyzer scans the input **character by character** and classifies lexemes according to predefined token categories.

The system can process code in two ways:
- Manual input through the terminal
- Reading source code from a text file

Additionally, the lexer detects **lexical errors**, such as unrecognized characters or unclosed strings.

---

## Theoretical Concepts

This implementation is based on fundamental concepts from **Formal Languages and Automata Theory**, including:

- Deterministic Finite Automata (DFA)
- Regular Expressions (RegEx)
- Symbol Tables
- Maximal Munch Principle

The lexer simulates DFA behavior through conditional transitions while scanning the source code.

---

## Project Structure

```
compilers-g5
│
├── src
│   └── lexer.py
│
├── test
│   ├── code1.txt
│   ├── code2.txt
│   ├── code3.txt
│   ├── code6.txt
│   ├── code7.txt
│   ├── code8.txt
│   ├── code9.txt
│   └── code10.txt
│
├── docs
│   └── report.pdf
│
└── README.md

```

## Documentation

The complete project report containing the theoretical framework, development process, results and conclusions can be found in the following document:

docs/report.pdf

---

## How to Run

Run the lexer with a test file:

python src/main.py test/code1.txt

The program also allows manual input through the terminal.

---

## Authors

320198687 320301238 321132927 321132477 321332086
Group 5  
Computer Engineering  
UNAM – Compilers Course  
Semester 2026-II

