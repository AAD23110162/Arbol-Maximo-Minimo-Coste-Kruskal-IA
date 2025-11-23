"""
Programa: Simulador Arbol-Máximo-Mínimo-Coste-Kruskal-IA

Descripción:
    Simulador y demostración del algoritmo de Kruskal para obtener
    árboles generadores mínimos o máximos en un grafo ponderado.

    Modos de uso:
        - Demo (seleccionar 1): usa el grafo de ejemplo en `graphs/example_graph.json`.
            Muestra la lista de nodos disponibles y permite al usuario indicar
            un nodo de inicio y un nodo de fin (opcionales). Después ejecuta
            Kruskal en modo mínimo y muestra la ejecución paso a paso en terminal.

        - Interactiva (seleccionar 2): permite al usuario especificar la ruta
            a un JSON de grafo, elegir si quiere modo paso a paso y si desea
            el árbol de máximo o mínimo coste. Ejecuta Kruskal mostrando pasos.

    Formato esperados del JSON:
        {
            "nodes": [1,2,3],            opcional, si falta se infiere
            "edges": [[u,v,w], ...]     o lista de diccionarios {"u":..,"v":..,"w":..}
        }

Autor: Alejandro Aguirre Díaz

"""
import json
import sys
from typing import List, Tuple, Any

class UnionFind:
    # Estructura Union-Find (disjoint set) para gestionar componentes
    # durante la ejecución de Kruskal. Soporta búsqueda con compresión
    # de rutas y unión por rango (rank) para mantener árboles planos.
    def __init__(self, elements: List[Any]):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x):
        # Búsqueda con compresión de rutas: acercamos el nodo a su raíz
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y) -> bool:
        # Une dos componentes si son distintas. Devuelve True si se unieron.
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        # Unión por rango: conectar la raíz de menor rango a la de mayor
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

    def components(self):
        """Devuelve un dict root -> [nodos] representando las componentes actuales."""
        # Recorre todos los elementos y agrupa por raíz para obtener
        # la lista de componentes actuales (útil para mostrar progreso).
        comps = {}
        for e in list(self.parent.keys()):
            r = self.find(e)
            comps.setdefault(r, []).append(e)
        return comps


def kruskal(nodes: List[Any], edges: List[Tuple[Any, Any, float]], maximize: bool = False, verbose: bool = True, step_mode: bool = False):
    """Ejecuta Kruskal (mínimo por defecto) y muestra pasos si verbose=True.

    edges: lista de tuplas (u, v, weight)
    maximize: si True calcula el árbol de máximo coste
    """
    # Mensaje inicial describiendo el modo (máximo/minimo)
    if verbose:
        typ = "Máximo" if maximize else "Mínimo"
        print(f"Ejecutando Kruskal ({typ}) sobre grafo con {len(nodes)} nodos y {len(edges)} aristas\n")

    # Ordenar aristas por peso; reverse=True para obtener árbol de máximo coste
    edges_sorted = sorted(edges, key=lambda e: e[2], reverse=maximize)

    # Mostrar la lista de aristas ordenadas (útil para seguir la ejecución)
    if verbose:
        print("Aristas ordenadas (u, v, peso):")
        for i, e in enumerate(edges_sorted, 1):
            print(f"  {i:>2}. {e}")
        print("")

    # Inicializar estructura de componentes, árbol parcial y variables
    uf = UnionFind(nodes)
    mst = []
    total_weight = 0.0
    step = 0

    for u, v, w in edges_sorted:
        # Procesar la siguiente arista en orden
        step += 1
        ru = uf.find(u)
        rv = uf.find(v)
        if verbose:
            print(f"Paso {step}: considerar arista ({u}, {v}, {w}) -> raíces: {ru}, {rv}")

        # Si las raíces son distintas, añadir la arista al MST/MAST
        if ru != rv:
            uf.union(ru, rv)
            mst.append((u, v, w))
            total_weight += w
            if verbose:
                print(f"  => Añadida. Peso acumulado: {total_weight}\n")
        else:
            # Si pertenecen a la misma componente, se omite porque formaría ciclo
            if verbose:
                print("  => Omitida (crearía ciclo)\n")

        # Mostrar componentes actuales y el árbol parcial construido hasta ahora
        if verbose:
            comps = uf.components()
            comp_summary = ", ".join(f"{r}:{{{','.join(map(str,sorted(ns)))}}}" for r, ns in comps.items())
            print(f"  Componentes actuales ({len(comps)}): {comp_summary}")
            if mst:
                mst_list = ", ".join(f"({a},{b}:{w})" for a, b, w in mst)
                print(f"  Árbol parcial: {mst_list}")
            else:
                print("  Árbol parcial: (vacío)")

        # Si estamos en modo paso a paso, esperar interacción del usuario
        if step_mode:
            try:
                cont = input("Presiona Enter para siguiente paso (o 'q' para salir): ")
            except EOFError:
                cont = ''
            if cont.strip().lower() == 'q':
                if verbose:
                    print("Simulación interrumpida por el usuario.\n")
                break
            print("")

    # Comprobar si se conectaron todos los nodos (grafo conexo)
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
    import os

    def choose_node(prompt: str, nodes: List[Any]):
        s = input(prompt).strip()
        if s == '':
            return None
        # Buscar coincidencia por representación en cadena
        for n in nodes:
            if str(n) == s:
                return n
        print("Nodo no encontrado. Intenta de nuevo.")
        return choose_node(prompt, nodes)

    print("Elige modo:\n  1) Demo (grafo de ejemplo)\n  2) Interactiva")
    modo = input("Introduce 1 o 2: ").strip()
    if modo == '1':
        # Demo: usar el grafo de ejemplo incluido
        default_path = os.path.join(os.path.dirname(__file__), 'graphs', 'example_graph.json')
        if not os.path.exists(default_path):
            print(f"Archivo de ejemplo no encontrado: {default_path}")
            sys.exit(1)
        nodes, edges = load_graph_from_json(default_path)
        print("\nNodos disponibles:", ", ".join(map(str, sorted(nodes))))
        start = choose_node("Introduce nodo de inicio (presiona Enter para omitir): ", nodes)
        end = choose_node("Introduce nodo de fin (presiona Enter para omitir): ", nodes)
        if start is None:
            print("Nodo inicio: (omitido)")
        else:
            print(f"Nodo inicio seleccionado: {start}")
        if end is None:
            print("Nodo fin: (omitido)")
        else:
            print(f"Nodo fin seleccionado: {end}")
        print("\nIniciando demo (Kruskal mínimo) sobre grafo de ejemplo...\n")
        mst, total = kruskal(nodes, edges, maximize=False, verbose=True, step_mode=False)
    else:
        # Interactiva: pedir ruta y opciones
        path = input("Ruta al JSON del grafo (presiona Enter para usar ejemplo): ").strip()
        if path == '':
            path = os.path.join(os.path.dirname(__file__), 'graphs', 'example_graph.json')
        if not os.path.exists(path):
            print(f"Archivo no encontrado: {path}")
            sys.exit(1)
        nodes, edges = load_graph_from_json(path)
        # Preguntar si modo paso a paso
        step_ans = input("¿Modo paso a paso? (s/N): ").strip().lower()
        step_mode = step_ans == 's' or step_ans == 'si'
        max_ans = input("¿Calcular árbol de máximo coste? (s/N): ").strip().lower()
        maximize = max_ans == 's' or max_ans == 'si'
        print("\nEjecutando Kruskal...\n")
        mst, total = kruskal(nodes, edges, maximize=maximize, verbose=True, step_mode=step_mode)

    print('\nResultado final:')
    for u, v, w in mst:
        print(f"  - ({u}, {v}) peso {w}")
    print(f"Peso total: {total}")
