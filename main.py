from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS configuration
origins = [
    "*",  # Adjust this to your frontend URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Link(BaseModel):
    from_node: str
    to_node: str
    cost: int

class Graph(BaseModel):
    nodes: List[str]
    links: List[Link]

def is_valid(v, pos, path, graph):
    if graph[path[pos - 1]][v] == 0:
        return False
    if v in path:
        return False
    return True

def hamiltonian_util(graph, path, pos):
    if pos == len(graph):
        return graph[path[pos - 1]][path[0]] == 1

    for v in range(1, len(graph)):
        if is_valid(v, pos, path, graph):
            path[pos] = v

            if hamiltonian_util(graph, path, pos + 1):
                return True

            path[pos] = -1  # Backtrack

    return False

def find_hamiltonian_cycle(nodes, links):
    graph = [[0] * len(nodes) for _ in range(len(nodes))]

    for link in links:
        from_index = nodes.index(link.from_node)
        to_index = nodes.index(link.to_node)
        graph[from_index][to_index] = 1
        graph[to_index][from_index] = 1  # Undirected graph

    path = [-1] * len(nodes)
    path[0] = 0  # Start from the first vertex

    if not hamiltonian_util(graph, path, 1):
        return []

    return [nodes[i] for i in path]

@app.post("/find-hamilton")
async def find_hamilton(graph: Graph):
    nodes = graph.nodes
    links = graph.links

    if len(nodes) < 3:
        return {"cycle": []}  # Not enough nodes for a Hamiltonian cycle

    cycle = find_hamiltonian_cycle(nodes, links)
    return {"cycle": cycle}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
