# MST-Delivery-Route-Optimization

## Overview
This program simulates a delivery route optimizer based on Minimum Spanning Tree (MST) algorithms. It features an interactive online shopping interface combined with a graphing tool that helps users plan delivery routes efficiently.

---

## Features

* **Online Shopping Display:**
  Users can browse and purchase items through a simple shopping interface.
  After shopping, the program displays the total amount spent.

* **Map Selection:**
  Users can choose from three different map backgrounds, each representing a different delivery area.

* **Interactive Graphing Map:**
  The selected map acts as a background where users can select nodes (delivery points) — limited to the number of items purchased.
  Users manually draw edges between nodes and input the weights (distances or costs).

* **Minimum Spanning Tree Calculation:**
  Using the input graph, the program computes the Minimum Spanning Tree to optimize the delivery route, minimizing total travel cost.

---

## How to Use

1. Run the program.
2. Shop for items using the online shopping display.
3. View your total spending amount.
4. Choose one of the three available maps.
5. On the graphing map, select up to the number of nodes equal to items purchased.
6. Draw edges between nodes and input their weights when prompted.
7. The program calculates and displays the MST for your delivery route.

---

## Requirements

* Python 3.x
* Required libraries : pygame

---

## Notes

* Ensure weights (edge costs) are numeric and reflect realistic distances or delivery costs for accurate MST calculation.
* This is a user-interactive program combining GUI elements with graph algorithms.

---


