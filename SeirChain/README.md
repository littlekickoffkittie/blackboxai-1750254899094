# Crysilis Compiler

This project is a compiler for the Crysilis (.cry) fractal-oriented programming language designed for SeirChain.

## Language Features

- Fractal-native data types: Triad, FractalArray, SierpinskiTree
- Built-in parallel execution primitives: fractal_spawn, triad_parallel
- Self-similar recursive constructs: fractal_recursion
- Ternary logic operators: true, false, uncertain
- Immutable-by-default variables with explicit mutability
- Pattern matching for fractal structures

## Core Keywords

triad, fractal, parallel, consensus, immutable, mutable, route, anchor

## Built-in Types

TriadHash, FractalCoord, ConsensusProof, WAC, NetworkPath

## Implementation Language

Python

## Project Structure

- lexer.py: Lexer implementation for tokenizing .cry files
- parser.py: Parser implementation for building AST
- ast.py: AST node definitions
- semantic.py: Semantic analysis and type checking
- codegen.py: Code generation or interpretation
- cli.py: Command line interface for compiling/running .cry files
- examples/: Example .cry source files
- tests/: Unit and integration tests

## Next Steps

- Implement lexer, parser, semantic analyzer, and code generator
- Add example source files demonstrating language features
- Add tests and documentation
