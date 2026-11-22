
// Nand2Tetris Capstone - Part C: Box
// Draws a 16-pixel wide, 20-pixel high box.
// Box appears while a keyboard key is pressed.
// Box disappears when the key is released.
// Starting screen row: 84
// Starting screen address: 19072

(START)
    @KBD
    D=M
    @DRAW
    D;JGT
    @ERASE
    0;JMP

// Draw black box
(DRAW)
    @19072
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(DRAW_LOOP)
    @R13
    A=M
    M=-1

    @32
    D=A
    @R13
    M=D+M

    @R14
    MD=M-1
    @DRAW_LOOP
    D;JGT

    @START
    0;JMP

// Erase box
(ERASE)
    @19072
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(ERASE_LOOP)
    @R13
    A=M
    M=0

    @32
    D=A
    @R13
    M=D+M

    @R14
    MD=M-1
    @ERASE_LOOP
    D;JGT

    @START
    0;JMP
