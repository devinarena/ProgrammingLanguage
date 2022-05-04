
import sys
import os

def define_ast(output_dir: str, base_name: str, types: list) -> None:
    with open(os.path.join(output_dir, base_name + ".py"), "w") as f:
        f.write("import sys\n")
        f.write("import os\n")
        f.write("sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n")
        f.write("import token\n")
        f.write("\n")
        f.write("class Expr:\n")
        define_visitor(f, base_name, types)
        f.write("   def accept(self, visitor: object) -> object:\n")
        f.write("       pass\n")
        f.write("\n")

        for type in types:
            name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(f, name, fields)
        

def define_type(f: object, name: str, fields: str) -> None:
    f.write(f"class {name}(Expr):\n")
    f.write(f"    def __init__(self, {fields}):\n")
    for field in fields.split(","):
        f.write(f"        self.{field.strip()} = {field.strip()}\n")
    f.write("\n")
    f.write(f"    def accept(self, visitor: object) -> object:\n")
    f.write(f"        return visitor.visit_{name.lower()}(self)\n")
    f.write("\n")

def define_visitor(f: object, base_name: str, types: list) -> None:
    f.write("   class Visitor:\n")
    for type in types:
        type_name = type.split(":")[0].strip().lower()
        f.write(f"      def visit_{type_name}(self, {type_name}: object):\n")
        f.write(f"          pass\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 astgenerator.py <output_dir>")
        exit(1)
    
    if not os.path.exists(sys.argv[1]):
        os.mkdir(sys.argv[1])
    
    define_ast(sys.argv[1], "statement", [
        "Expression   : expression",
        "Output       : output",
    ])