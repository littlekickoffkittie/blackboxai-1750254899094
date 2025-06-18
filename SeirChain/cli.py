import sys
from lexer import Lexer
from parser import Parser
from stdlib.triad_matrix import Triad
from stdlib.triad_store import TriadStore
from stdlib.pof_consensus import ProofOfFractalConsensus

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <source-file.cry>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        with open(source_file, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"File not found: {source_file}")
        sys.exit(1)

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    print("Parsing successful. AST:")
    print(ast)

    # Example usage of Triad and TriadStore
    triad_id = b"example_triad_id_1234"
    triad = Triad(id=triad_id)
    triad_store = TriadStore(db_path="triad_db")
    # Note: put_triad is async, so in real code we would await it or run in event loop
    # Here just a placeholder call
    # await triad_store.put_triad(triad)

    # Example usage of ProofOfFractalConsensus
    pof = ProofOfFractalConsensus()
    puzzle = pof.generate_puzzle(triad_id, (0,0,0))
    print(f"Generated PoF puzzle with difficulty: {puzzle.difficulty_target}")

if __name__ == "__main__":
    main()
