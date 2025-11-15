import json
from typing import List, Tuple, Any


class UnionFind:
    def __init__(self, elements: List[Any]):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y) -> bool:
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal(nodes: List[Any], edges: List[Tuple[Any, Any, float]], maximize: bool = False, verbose: bool = True):
    """Ejecuta Kruskal (mínimo por defecto) y muestra pasos si verbose=True.

    edges: lista de tuplas (u, v, weight)
    maximize: si True calcula el árbol de máximo coste
    """
    if verbose:
        typ = "Máximo" if maximize else "Mínimo"
        print(f"Ejecutando Kruskal ({typ}) sobre grafo con {len(nodes)} nodos y {len(edges)} aristas\n")

    # Ordenar aristas
    edges_sorted = sorted(edges, key=lambda e: e[2], reverse=maximize)

    if verbose:
        print("Aristas ordenadas (u, v, peso):")
        for i, e in enumerate(edges_sorted, 1):
            print(f"  {i:>2}. {e}")
        print("")

    uf = UnionFind(nodes)
    mst = []
    total_weight = 0.0
    step = 0

    for u, v, w in edges_sorted:
        step += 1
        ru = uf.find(u)
        rv = uf.find(v)
        if verbose:
            print(f"Paso {step}: considerar arista ({u}, {v}, {w}) -> raíces: {ru}, {rv}")
        if ru != rv:
            uf.union(ru, rv)
            mst.append((u, v, w))
            total_weight += w
            if verbose:
                print(f"  => Añadida. Peso acumulado: {total_weight}\n")
        else:
            if verbose:
                print("  => Omitida (crearía ciclo)\n")

    # Comprobar si se conectaron todos los nodos (grafo conexo)
    roots = set(uf.find(n) for n in nodes)
    if verbose:
        if len(roots) == 1:
            print("Árbol generador obtenido (grafo conexo).\n")
        else:
            print(f"Grafo no conexo: {len(roots)} componentes separadas. Se obtuvo un bosque mínimo parcial.\n")

    return mst, total_weight


def load_graph_from_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    nodes = data.get('nodes')
    edges = data.get('edges', [])
    # Normalizar formatos: permitir aristas como [u, v, w] o diccionarios {"u":..}
    normalized_edges = []
    for e in edges:
        if isinstance(e, list) or isinstance(e, tuple):
            u, v, w = e
        elif isinstance(e, dict):
            u = e.get('u')
            v = e.get('v')
            w = e.get('w') or e.get('weight')
        else:
            raise ValueError(f"Formato de arista no reconocido: {e}")
        normalized_edges.append((u, v, float(w)))

    if nodes is None:
        # inferir nodos de aristas
        node_set = set()
        for u, v, _ in normalized_edges:
            node_set.add(u)
            node_set.add(v)
        nodes = list(node_set)

    return list(nodes), normalized_edges


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simulador Kruskal (paso a paso)')
    parser.add_argument('json', help='Ruta a archivo JSON con el grafo')
    parser.add_argument('--max', action='store_true', help='Calcular árbol de máximo coste')
    args = parser.parse_args()
    nodes, edges = load_graph_from_json(args.json)
    mst, total = kruskal(nodes, edges, maximize=args.max, verbose=True)
    print('Resultado final:')
    for u, v, w in mst:
        print(f"  - ({u}, {v}) peso {w}")
    print(f"Peso total: {total}")
