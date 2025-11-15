import argparse
from kruskal import load_graph_from_json, kruskal


def main():
    parser = argparse.ArgumentParser(description='Ejecuta el simulador Kruskal paso a paso')
    parser.add_argument('json', help='Ruta al archivo JSON que describe el grafo')
    parser.add_argument('--max', action='store_true', help='Calcular árbol de máximo coste en lugar del mínimo')
    args = parser.parse_args()

    nodes, edges = load_graph_from_json(args.json)
    mst, total = kruskal(nodes, edges, maximize=args.max, verbose=True)

    print('\nResumen final:')
    if mst:
        for u, v, w in mst:
            print(f"  - ({u}, {v}) peso {w}")
        print(f"Peso total: {total}")
    else:
        print('No se seleccionaron aristas.')


if __name__ == '__main__':
    main()
