from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

# Ruta al archivo JSON
POKEMONS_FILE = 'pokemons.json'

# Funciones auxiliares para manipular el archivo JSON
def load_pokemons():
    if os.path.exists(POKEMONS_FILE):
        with open(POKEMONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_pokemons(pokemons):
    with open(POKEMONS_FILE, 'w') as f:
        json.dump(pokemons, f, indent=4)

# Cargar los datos iniciales
pokemons = load_pokemons()
pokemon_id_counter = max([p['id'] for p in pokemons], default=0) + 1

# Rutas

# Obtener todos los Pokémon
@app.route('/pokemons', methods=['GET'])
def get_pokemons():
    return jsonify(pokemons), 200

# Crear un nuevo Pokémon
@app.route('/pokemons', methods=['POST'])
def create_pokemon():
    global pokemon_id_counter
    data = request.get_json()

    # Validar los campos obligatorios
    required_fields = ['nombre', 'imagen', 'caracteristicas', 'habilidades', 'tipo', 'habitat']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"El campo {field} es obligatorio")

    pokemon = {
        'id': pokemon_id_counter,
        'nombre': data['nombre'],
        'imagen': data['imagen'],
        'caracteristicas': {
            'peso': data['caracteristicas'].get('peso'),
            'altura': data['caracteristicas'].get('altura'),
            'fuerza': data['caracteristicas'].get('fuerza'),
            'edad': data['caracteristicas'].get('edad')
        },
        'habilidades': data['habilidades'],
        'tipo': data['tipo'],
        'habitat': data['habitat']
    }
    pokemons.append(pokemon)
    pokemon_id_counter += 1

    save_pokemons(pokemons)

    return jsonify(pokemon), 201

# Obtener un Pokémon específico por ID
@app.route('/pokemons/<int:id>', methods=['GET'])
def get_pokemon(id):
    pokemon = next((p for p in pokemons if p['id'] == id), None)
    if pokemon is None:
        abort(404, description="Pokémon no encontrado")
    return jsonify(pokemon), 200

# Actualizar un Pokémon por ID
@app.route('/pokemons/<int:id>', methods=['PUT'])
def update_pokemon(id):
    pokemon = next((p for p in pokemons if p['id'] == id), None)
    if pokemon is None:
        abort(404, description="Pokémon no encontrado")

    data = request.get_json()

    # Actualizar los atributos
    pokemon['nombre'] = data.get('nombre', pokemon['nombre'])
    pokemon['imagen'] = data.get('imagen', pokemon['imagen'])
    if 'caracteristicas' in data:
        pokemon['caracteristicas']['peso'] = data['caracteristicas'].get('peso', pokemon['caracteristicas']['peso'])
        pokemon['caracteristicas']['altura'] = data['caracteristicas'].get('altura', pokemon['caracteristicas']['altura'])
        pokemon['caracteristicas']['fuerza'] = data['caracteristicas'].get('fuerza', pokemon['caracteristicas']['fuerza'])
        pokemon['caracteristicas']['edad'] = data['caracteristicas'].get('edad', pokemon['caracteristicas']['edad'])
    pokemon['habilidades'] = data.get('habilidades', pokemon['habilidades'])
    pokemon['tipo'] = data.get('tipo', pokemon['tipo'])
    pokemon['habitat'] = data.get('habitat', pokemon['habitat'])

    save_pokemons(pokemons)

    return jsonify(pokemon), 200

# Eliminar un Pokémon por ID
@app.route('/pokemons/<int:id>', methods=['DELETE'])
def delete_pokemon(id):
    global pokemons
    pokemon = next((p for p in pokemons if p['id'] == id), None)
    if pokemon is None:
        abort(404, description="Pokémon no encontrado")

    pokemons = [p for p in pokemons if p['id'] != id]
    save_pokemons(pokemons)
    return '', 204

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
