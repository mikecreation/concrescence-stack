#!/usr/bin/env python3
"""
Concrescence Stack: Minimal Reproducible Example
Author: Michael Zot
Date: 2025-05-29
"""

import numpy as np
import networkx as nx
from scipy import stats
from typing import Tuple, List
import argparse

class NoeticDetector:
    """Detect noëtic events using three-signal test."""
    def __init__(self, tau_u: float = 0.95, tau_delta: float = 0.95):
        self.tau_u = tau_u
        self.tau_delta = tau_delta
        self.baseline_stats = None
    def calibrate_baseline(self, null_data: np.ndarray, n_bootstrap: int = 1000):
        uncertainties = []
        deltas = []
        for _ in range(n_bootstrap):
            shuffled = np.random.permutation(null_data)
            u = np.var(shuffled)
            delta = abs(u - np.var(shuffled[1:]))
            uncertainties.append(u)
            deltas.append(delta)
        self.u_threshold = np.percentile(uncertainties, 100 * self.tau_u)
        self.delta_threshold = np.percentile(deltas, 100 * self.tau_delta)
    def detect_event(self, u_t: float, u_prev: float, phi_change: float, delta_window: float = 1.0) -> bool:
        if self.baseline_stats is None:
            raise ValueError("Must calibrate baseline first")
        signal_1 = u_t > self.u_threshold
        signal_2 = abs(u_t - u_prev) > self.delta_threshold
        signal_3 = phi_change > 0
        return signal_1 and signal_2 and signal_3

def event_gravity_index(G: nx.Graph, node: int) -> float:
    if not G.has_node(node):
        return 0.0
    reachable = nx.single_source_shortest_path_length(G, node)
    return len(reachable) / G.number_of_nodes()

def percolation_experiment(G: nx.Graph, p_values: List[float], trials: int = 100) -> List[Tuple[float, float, float]]:
    results = []
    for p in p_values:
        egis = []
        bcs = []
        for trial in range(trials):
            H = nx.Graph()
            H.add_nodes_from(G.nodes())
            for u, v in G.edges():
                if np.random.random() < p:
                    H.add_edge(u, v)
            if H.number_of_edges() == 0:
                continue
            bc_dict = nx.betweenness_centrality(H)
            for node in H.nodes():
                egi = event_gravity_index(H, node)
                bc = bc_dict[node]
                egis.append(egi)
                bcs.append(bc)
        if len(egis) > 0:
            correlation = stats.pearsonr(egis, bcs)[0]
            results.append((p, correlation, len(egis)))
    return results

def main():
    parser = argparse.ArgumentParser(description='Concrescence Stack Demo')
    parser.add_argument('--nodes', type=int, default=100, help='Number of nodes')
    parser.add_argument('--trials', type=int, default=50, help='Trials per p-value')
    parser.add_argument('--output', type=str, help='Output CSV file')
    args = parser.parse_args()
    G = nx.erdos_renyi_graph(args.nodes, 0.1)
    p_values = np.linspace(0.0, 1.0, 21)
    results = percolation_experiment(G, p_values, args.trials)
    print("p_value,correlation,n_samples")
    for p, corr, n in results:
        print(f"{p:.3f},{corr:.3f},{n}")
    if args.output:
        with open(args.output, 'w') as f:
            f.write("p_value,correlation,n_samples\n")
            for p, corr, n in results:
                f.write(f"{p:.3f},{corr:.3f},{n}\n")

if __name__ == '__main__':
    main()
