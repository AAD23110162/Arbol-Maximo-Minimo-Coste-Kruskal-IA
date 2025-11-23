# Arbol-Maximo-Minimo-Coste-Kruskal-IA
**Autor:** Alejandro Aguirre Díaz.  
**Descripción:** Este repositorio contiene un simulador del algoritmo Árbol de Máximo y Mínimo coste (Kruskal) programado en Python.  
**Última modificación:** Martes 25 de noviembre del 2025.  

## ¿Qué es?
Kruskal es un algoritmo voraz (greedy) para construir árboles generadores (spanning trees) en grafos conexos y ponderados. Existen dos variantes comunes:

- Árbol de mínimo coste (Minimum Spanning Tree, MST): selecciona aristas de menor peso primero.
- Árbol de máximo coste: selecciona aristas de mayor peso primero (equivalente a invertir el orden de selección).

Funcionamiento básico:

- Ordena todas las aristas por peso (ascendente para mínimo, descendente para máximo).
- Recorre las aristas en ese orden y añade una arista si conecta dos componentes diferentes (evita ciclos) usando una estructura Union-Find (disjoint-set).

Complejidad: ordenar las aristas domina el coste: O(E log E) (frecuentemente descrito como O(E log V)). Las operaciones de Union-Find son casi constantes amortizadas (≈ O(α(V))).

Propiedades clave: es un algoritmo determinista, voraz y produce una solución óptima para el MST.

## ¿Para qué sirve?
Kruskal se usa para obtener una forma óptima y económica de conectar todos los vértices de un grafo. Aplicaciones prácticas:

- Diseño de redes (telecomunicaciones, redes eléctricas): minimizar coste de cableado o enlaces.
- Reducción de costes en infraestructuras: carreteras, tendidos, tuberías.
- Clustering en aprendizaje automático: construir árboles de unión para separar grupos (single-linkage clustering).
- Compresión y segmentación de imágenes: detectar regiones conectadas con coste mínimo/óptimo.
- Algoritmos aproximados: componente en heurísticas para el problema del viajante (TSP) y otros problemas NP-hard.

## ¿Cómo se implementa en el mundo?
En la industria y en la investigación se implementa de forma práctica y escalable:

- Herramientas de planificación de redes usan Kruskal para proponer topologías de bajo coste y luego aplican restricciones reales (capacidad, redundancia) encima del MST.
- Sistemas GIS y planificación urbana: cálculo de mallas de conexión óptimas entre puntos de interés.
- En telecomunicaciones y distribución eléctrica se combina con análisis de confiabilidad: se obtiene un diseño de coste mínimo y luego se introducen redundancias según criterios de disponibilidad.
- En software se implementa con estructuras eficientes: listas de aristas, ordenación por peso y Union-Find con compresión de caminos y unión por rango.

Implementaciones comunes: bibliotecas como `NetworkX` (Python), funciones en C++/Java optimizadas para grandes grafos, y motores geoespaciales integrados en herramientas de planificación.

## ¿Cómo lo implementarías en tu vida?
En ideas prácticas y ejercicios personales como:

- Proyectos personales: construir un visualizador/simulador en Python que genere grafos aleatorios y muestre MST y árbol máximo (por ejemplo usando `matplotlib` o `pyvis`).
- Optimizar conexiones domésticas: planificar la colocación y cableado de routers/extensores minimizando cable o coste.
- Planificación de rutas de instalación: decidir el orden y las conexiones más baratas entre puntos de trabajo (obras, instalaciones).
- Aprendizaje y enseñanza: crear presentaciones interactivas que muestren cómo Union-Find evita ciclos.

Pequeños pasos: implementar Kruskal desde cero, luego comparar con `networkx.minimum_spanning_tree` para verificar resultados.

## ¿Cómo lo implementarías en tu trabajo o tu trabajo de ensueño?

- Integrarlo en herramientas de planificación y optimización para clientes, p. ej. módulos que propongan topologías iniciales de baja inversión para redes o logística.
- Automatizar análisis de coste-beneficio: generar MSTs como punto de partida y luego evaluar variantes con redundancia y restricciones operativas.
- Crear dashboards y simuladores interactivos para equipos no técnicos que muestren impacto económico de distintas topologías.
- Usarlo como caso de estudio en equipos de Data Science/Research para clustering de datos o preprocesamiento de grafos grandes.

Además, en un rol de ingeniería se puede extender la implementación básica con: soporte para grafos no conexos, pesos dinámicos, costes multi-criterio y visualizaciones en tiempo real.

---

## Glosario técnico

- **Árbol generador (Spanning Tree):** Subgrafo que conecta todos los nodos sin ciclos y con exactamente V-1 aristas.
- **Árbol generador máximo:** Árbol generador con peso total máximo (equivalente a ordenar aristas en orden descendente y aplicar Kruskal).
- **Árbol generador mínimo (MST):** Árbol generador cuyo peso total (suma de pesos de aristas) es mínimo posible.
- **Arista (Edge):** Conexión entre dos nodos; puede ser ponderada (tener un peso).
- **Arista dirigida (directed edge):** definición y diferencias con aristas no dirigidas; representación y consecuencias para árboles generadores.
- **Bosque (Forest):** Conjunto de árboles disjuntos; aparece cuando el grafo original no es conexo y se generan varios árboles generadores parciales.
- **Caminos simples, ciclos y corte mínimo (cut):** definiciones formales y relación con MSTs.
- **Ciclo (Cycle):** Camino cerrado donde se vuelve al nodo inicial; los algoritmos de MST deben evitar crear ciclos.
- **Componente conexa (Connected component):** Conjunto de nodos donde existe un camino entre cualquier par de nodos dentro del conjunto.
- **Compresión de rutas (Path compression):** Técnica en Union-Find que hace que las búsquedas futuras sean más rápidas apuntando directamente a la raíz.
- **Conexo / No conexo:** Un grafo es conexo si existe un camino entre cualquier par de nodos; si no, es no conexo y Kruskal produce un bosque.
- **E (aristas) y V (vértices):** Símbolos habituales para el número de aristas y vértices de un grafo.
- **Embeddings de grafos (graph embeddings):** representaciones vectoriales, usos en ML y ejemplos prácticos.
- **Entrada JSON:** Formato usado en este repositorio para describir grafos; puede incluir `nodes` y `edges` (listas o diccionarios).
- **Grafo (Graph):** Estructura compuesta por vértices (nodos) y aristas (edges). Se denota habitualmente G=(V,E).
- **Heurística:** Técnica práctica que guía la búsqueda de soluciones (no siempre garantiza optimalidad) —en Kruskal la heurística es ordenar por peso.
- **Hipergráfos:** generalización de aristas que conectan más de dos vértices.
- **Isomorfismo de grafos:** definición formal y técnicas de verificación.
- **Kruskal:** Algoritmo voraz que construye un MST ordenando aristas por peso y añadiéndolas si unen componentes diferentes.
- **Matriz de adyacencia, matriz de incidencia y matriz Laplaciana:** definiciones, propiedades y usos algorítmicos.
- **Multigrafo y pseudografo:** aristas paralelas, lazos, y cómo afectan algoritmos de MST.
- **Notación O (Complejidad temporal):** Forma de expresar cómo escala el tiempo de ejecución en función del tamaño de entrada; por ejemplo O(E log E) para Kruskal por la ordenación.
- **Nodo / Vértice (Node / Vertex):** Elemento fundamental del grafo que representa un punto o entidad.
- **Peso (Weight / Cost):** Valor numérico asociado a una arista que representa coste, distancia o capacidad.
- **Peso total:** Suma de los pesos de las aristas seleccionadas en un árbol generador.
- **Single-linkage (clustering):** Método de agrupamiento que usa la distancia mínima entre elementos; se puede relacionar con MSTs para construir dendrogramas.
- **Unión por rango / por tamaño (Union by rank/size):** Heurística para unir árboles más pequeños debajo de los más grandes para mantener baja la altura.
- **Union-Find (Disjoint Set Union, DSU):** Estructura de datos que mantiene particiones de elementos en conjuntos disjuntos, soportando operaciones `find` (buscar raíz) y `union` (unir conjuntos).
- **Voraz (Greedy):** Estrategia algorítmica que toma la mejor decisión local en cada paso con la esperanza de alcanzar una solución global óptima.
