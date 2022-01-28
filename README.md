# pygame_skript
A Latex [script](./00 skript.pdf) with executable examples about Pygame for my students.

# Intention
This script started as a help for my IT students at the TBS1 in Bochum, Germany. It is a short introduction to the main features of Pygame. You're welcome to help me out by correcting the text or source code or by adding new chapters. Why german? Because my students are german and learning programming is in their own language hard enough. 

Ralf Adams, 04.01.2022

# Structure
## Pygame Source Code
At least for each Pygame feature one source code is stored in the ./src/ directory. The next level is divided in two directories. `00 Einführung` contains for each chapter of the introduction part of the script one corresponding directory. They are ordered like the chapters of the script. Each directory like `src\00 Einführung\04 Bewegung` contains complete projects. If you add your code, please follow this systematic. `01 Spiele` contains examples games. Each game project is stored in one directory and should be independend of the other game directories. By beginning there is only one empty game directory `src\01 Spiele\01 Bubbles`.

## Latex Files
I've choosen Latex (LuaLatex) -- my favourite typesetting system. This gives me the chance to be independent of the actual *in* office product. Inside the Latex files all examples and concepts of Pygame are explained. The bitmap pictures are stored in `./pics`. To construct own figures use TikZ and PGF, please.

