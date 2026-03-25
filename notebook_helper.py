import argparse
import nbformat
import sys
import os

def load_notebook(path):
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)

def save_notebook(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Saved changes to {path}")

def list_cells(args):
    nb = load_notebook(args.path)
    print(f"Notebook: {args.path}")
    print(f"Total cells: {len(nb.cells)}")
    print("-" * 60)
    print(f"{'ID':<5} | {'Type':<10} | {'Content Preview'}")
    print("-" * 60)
    for i, cell in enumerate(nb.cells):
        source = cell.source.strip().split('\n')[0] if cell.source else "[Empty]"
        preview = (source[:40] + '...') if len(source) > 40 else source
        try:
            print(f"{i:<5} | {cell.cell_type:<10} | {preview}")
        except UnicodeEncodeError:
            print(f"{i:<5} | {cell.cell_type:<10} | [Content not displayable]")

def read_cell(args):
    nb = load_notebook(args.path)
    if not (0 <= args.index < len(nb.cells)):
        print(f"Error: Index {args.index} out of range (0-{len(nb.cells)-1})")
        sys.exit(1)
    
    cell = nb.cells[args.index]
    print(f"--- CELL {args.index} ({cell.cell_type}) ---")
    print("\n[SOURCE]:")
    print(cell.source)
    
    if cell.cell_type == 'code' and 'outputs' in cell:
        print("\n[OUTPUTS]:")
        for output in cell.outputs:
            if output.output_type == 'stream':
                print(output.text)
            elif output.output_type == 'execute_result' or output.output_type == 'display_data':
                print(f"[{output.output_type} data]")
            elif output.output_type == 'error':
                print(f"[Error: {output.ename}]")

def edit_cell(args):
    nb = load_notebook(args.path)
    if not (0 <= args.index < len(nb.cells)):
        print(f"Error: Index {args.index} out of range (0-{len(nb.cells)-1})")
        sys.exit(1)

    if args.source_file:
        with open(args.source_file, 'r', encoding='utf-8') as f:
            new_source = f.read()
    elif args.source_Text:
         new_source = args.source_Text
    else:
        print("Error: Must provide --source_file or --source_text")
        sys.exit(1)

    nb.cells[args.index].source = new_source
    save_notebook(nb, args.path)

def delete_cell(args):
    nb = load_notebook(args.path)
    if not (0 <= args.index < len(nb.cells)):
        print(f"Error: Index {args.index} out of range (0-{len(nb.cells)-1})")
        sys.exit(1)
    
    deleted_type = nb.cells[args.index].cell_type
    del nb.cells[args.index]
    print(f"Deleted cell {args.index} (type: {deleted_type})")
    save_notebook(nb, args.path)

def insert_cell(args):
    nb = load_notebook(args.path)
    if not (0 <= args.index <= len(nb.cells)):
        print(f"Error: Index {args.index} out of range (0-{len(nb.cells)})")
        sys.exit(1)

    if args.source_file:
        with open(args.source_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = ""

    if args.type == 'code':
        new_cell = nbformat.v4.new_code_cell(content)
    else:
        new_cell = nbformat.v4.new_markdown_cell(content)
    
    nb.cells.insert(args.index, new_cell)
    print(f"Inserted new {args.type} cell at index {args.index}")
    save_notebook(nb, args.path)

def set_type(args):
    nb = load_notebook(args.path)
    if not (0 <= args.index < len(nb.cells)):
        print(f"Error: Index {args.index} out of range (0-{len(nb.cells)-1})")
        sys.exit(1)
    
    cell = nb.cells[args.index]
    if args.type == cell.cell_type:
        print(f"Cell {args.index} is already {args.type}")
        return

    # Create new cell with same source but new type
    if args.type == 'code':
        new_cell = nbformat.v4.new_code_cell(cell.source)
    else:
        new_cell = nbformat.v4.new_markdown_cell(cell.source)
    
    nb.cells[args.index] = new_cell
    print(f"Changed cell {args.index} type to {args.type}")
    save_notebook(nb, args.path)

def main():
    parser = argparse.ArgumentParser(description="CLI tool to manipulate Jupyter Notebooks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    list_parser = subparsers.add_parser('list', help='List all cells')
    list_parser.add_argument('path', help='Path to .ipynb file')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read a specific cell')
    read_parser.add_argument('path', help='Path to .ipynb file')
    read_parser.add_argument('index', type=int, help='Cell index')

    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit a cell source')
    edit_parser.add_argument('path', help='Path to .ipynb file')
    edit_parser.add_argument('index', type=int, help='Cell index')
    group = edit_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source_file', help='File containing new source code')
    group.add_argument('--source_text', help='Direct text for source (use carefully with CLI)')

    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete a cell')
    del_parser.add_argument('path', help='Path to .ipynb file')
    del_parser.add_argument('index', type=int, help='Cell index')

    # Insert command
    ins_parser = subparsers.add_parser('insert', help='Insert a new cell')
    ins_parser.add_argument('path', help='Path to .ipynb file')
    ins_parser.add_argument('index', type=int, help='Index to insert at')
    ins_parser.add_argument('type', choices=['code', 'markdown'], help='Cell type')
    ins_parser.add_argument('--source_file', help='Initial content file')

    # Set Type command
    type_parser = subparsers.add_parser('set_type', help='Change cell type')
    type_parser.add_argument('path', help='Path to .ipynb file')
    type_parser.add_argument('index', type=int, help='Cell index')
    type_parser.add_argument('type', choices=['code', 'markdown'], help='New cell type')

    args = parser.parse_args()

    if args.command == 'list':
        list_cells(args)
    elif args.command == 'read':
        read_cell(args)
    elif args.command == 'edit':
        edit_cell(args)
    elif args.command == 'delete':
        delete_cell(args)
    elif args.command == 'insert':
        insert_cell(args)
    elif args.command == 'set_type':
        set_type(args)

if __name__ == "__main__":
    main()
