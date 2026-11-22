Nand2Tetris Capstone Project 
# NAND2TETRIS CAPSTONE PROJECT

## Student Details

- **Student Name:** Aman Kumar
- **Roll Number:** 2501010284
- **Course:** B.Tech CSE Core
- **Subject:** Nand to Tetris
- **Department:** SOET
- **Submission Date:** 22-11-2026

---

## 1. Project Overview

This capstone project is based on the Nand2Tetris computer system. It demonstrates the construction of hardware components, the development of a Hack Assembler, and the implementation of a graphical Box program using Hack Assembly language.

The project is divided into three main parts:

- **Part A:** Hardware Construction
- **Part B:** Hack Assembler
- **Part C:** Box Drawing Program

## 2. Technologies and Tools Used

- Hardware Description Language (HDL)
- Python
- Hack Assembly Language
- Nand2Tetris Web IDE
- CPU Emulator
- Visual Studio Code
- Windows PowerShell

## 3. Project Structure

Nand2Tetris-Capstone/

- Part-A-Hardware/
  - Add.hack
  - CPU.hdl
  - Memory.hdl
  - Computer.hdl
  - Test and comparison files

- Part-B-Assembler/
  - assembler.py
  - examples/
    - Add.asm
    - Add.hack
    - Max.asm
    - Max.hack
  - tests/

- Part-C-Box/
  - Box.asm
  - Box.hack
  - symbols.txt

- Tests/
- Screenshots/
- Report/
- README.txt

## 4. Part A – Hardware Construction

The first part focuses on the construction and testing of the main hardware components of the Hack computer.

Components covered:

- CPU
- Memory
- Computer

The components were implemented and tested using the Nand2Tetris Hardware Simulator.

## 5. Part B – Hack Assembler

A Hack Assembler was developed using Python.

The assembler converts Hack Assembly language instructions into 16-bit binary machine instructions.

### Main Features

- Reads `.asm` assembly files.
- Processes A-instructions and C-instructions.
- Handles labels and symbols.
- Generates `.hack` machine-code files.
- Generates a symbol table.

### How to Run

Open the project folder in VS Code and run the following commands in the terminal:

**For Add.asm:**

python Part-B-Assembler/assembler.py Part-B-Assembler/examples/Add.asm

**For Max.asm:**

python Part-B-Assembler/assembler.py Part-B-Assembler/examples/Max.asm

The assembler generates the corresponding `.hack` machine-code file.

## 6. Part C – Box Drawing Program

The third part implements a Box drawing program using Hack Assembly language.

### Features

- Draws a black rectangular box on the screen.
- Displays the box when a keyboard key is pressed.
- Erases the box when the key is released.
- Uses screen memory addresses to control the display.

### Box Specifications

- Width: 16 pixels
- Height: 20 pixels
- Starting screen address: 19072
- Screen row: 84

The program was assembled using the Python Hack Assembler and executed using the Nand2Tetris CPU Emulator.

## 7. Testing and Validation

The project includes testing and validation evidence for all three parts.

- Hardware components were tested using the Hardware Simulator.
- The assembler was tested using Add.asm and Max.asm.
- Machine-code formatting was validated.
- The Box program was executed using the CPU Emulator.
- Keyboard interaction was tested to verify drawing and erasing behavior.

Screenshots of the implementation and testing results are available in the Screenshots folder.

## 8. Limitations

- The assembler currently supports the Hack Assembly instruction set implemented in this project.
- The Box program draws a fixed-size rectangle at a fixed screen position.
- The project is intended for educational and demonstration purposes.

## 9. Conclusion

This capstone project demonstrates the fundamental concepts of computer architecture, hardware construction, assembly language, and machine-code generation.

It provides practical experience in understanding how hardware components work together and how assembly instructions are translated into machine code and executed by a computer system.

---

**Project:** Nand2Tetris Capstone  
**Submitted by:** Aman Kumar