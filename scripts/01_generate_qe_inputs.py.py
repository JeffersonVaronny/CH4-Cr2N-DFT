import os
from pathlib import Path

# carpeta raíz del proyecto
base_dir = Path(__file__).resolve().parent.parent

# rutas importantes
configs_dir = base_dir / "structures" / "generated"                       # carpeta con los .xyz
template_file = base_dir / "qe_inputs" / "templates" / "pw_template.in"
generated = base_dir / "qe_inputs" / "generated"         # donde se guardan los .in nuevos
generated.mkdir(parents=True, exist_ok=True)



assert configs_dir.exists(), "No existe carpeta xyz"
assert template_file.exists(), "No existe template"

if configs_dir.exists() and template_file.exists():
    print("------Rutas de entrada/salida------")
    print("Base dir:", base_dir)
    print("XYZ folder:", configs_dir)
    print("Template:", template_file)
    print("Output:", generated)
    print("----------------------------------")

# -------- FUNCIONES --------

def read_xyz(file_path):
    """Lee un archivo xyz y devuelve lista de líneas 'Elemento x y z'"""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    atom_lines = lines[2:]  # saltar N_atoms y comentario
    atom_lines = [line.strip() for line in atom_lines if line.strip()]

    return atom_lines

def replace_name(template, name):
    return template.replace("name", name)

def replace_tem(template, name):
    return template.replace("tmp/outdir", f"tmp/{name}")

def replace_atomic_positions(template, new_positions):
    """Reemplaza el bloque ATOMIC_POSITIONS en el template"""

    lines = template.splitlines()

    new_lines = []
    inside_block = False

    for line in lines:
        if line.strip().startswith("ATOMIC_POSITIONS"):
            inside_block = True
            new_lines.append("ATOMIC_POSITIONS angstrom")

            # insertar nuevas posiciones
            for atom in new_positions:
                new_lines.append(atom)

            continue

        # detectar fin del bloque (cuando aparece otra sección)
        if inside_block:
            if line.strip() == "" or line.startswith(("K_POINTS", "CELL_PARAMETERS", "ATOMIC_SPECIES", "&")):
                inside_block = False
                new_lines.append(line)
            # saltar líneas viejas
            continue

        new_lines.append(line)

    return "\n".join(new_lines)


# -------- MAIN --------

# leer template
with open(template_file, 'r') as f:
    template_content = f.read()

#template = template_file.read_text()
# recorrer xyz
for xyz_file in configs_dir.glob("*.xyz"):
        xyz_path = os.path.join(configs_dir, xyz_file)
        name = xyz_file.stem # nombre sin extensión
        atoms = read_xyz(xyz_path)

        new_input = replace_atomic_positions(template_content, atoms)
        new_input = replace_name(new_input, name)
        new_input = replace_tem(new_input, name)
        #content = template

        #content = replace_atomic_positions(content, atomic_positions)
        # nombre de salida
        output_name = f"pw-{name}.in"
        output_path = os.path.join(generated, output_name)

        with open(output_path, 'w') as f:
            f.write(new_input)
        
        tmp_dir = base_dir / "tmp" / name
        tmp_dir.mkdir(parents=True, exist_ok=True)

        print(f"Generado: {output_name}")
print("Dir pws generados:", generated)