---
title: Dynamic Pricing Environment
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
---
# Dynamic Pricing Optimization Environment

## Overview

This project simulates a real-world dynamic pricing system where an AI agent learns how to adjust prices over time.

In many businesses today, such as e-commerce, ride-sharing, or travel platforms, pricing is not fixed. It changes based on demand, competition, and availability. This environment recreates that scenario in a simple and structured way.

The goal is to provide a setup where an AI agent can make pricing decisions step-by-step and learn from the outcomes.

---

## What the Agent Does

At every step, the agent:
- observes the current market conditions
- decides a new price
- receives feedback (reward) based on how good the decision was

The objective of the agent is to maximize revenue while making reasonable pricing decisions.

---

## Environment Design

### Observation

The agent receives the following information:
- current price  
- demand level (0 to 1)  
- competitor price  
- remaining inventory  
- time step  
- last reward  

---

### Action

The agent performs one action:
- set a new price (float value)

---

### Reward

The reward is based on:
- revenue generated  
- efficiency of inventory usage  
- competitiveness of pricing  

All rewards are normalized between 0 and 1.

---

## Environment Behavior

- Higher prices can reduce demand  
- Lower prices increase demand but reduce profit per unit  
- Inventory decreases as items are sold  
- Competitor prices change over time in a deterministic manner  

Each episode ends when:
- inventory is depleted, or  
- maximum number of steps is reached  

---

## Tasks

The environment includes three difficulty levels:

### Easy
Focus on maximizing the number of units sold.

### Medium
Balance between sales volume and revenue.

### Hard
Optimize pricing while considering competition and long-term revenue.

---

## Evaluation

Each task is evaluated using a deterministic scoring method:

- Easy → based on total units sold  
- Medium → balance between revenue and sales  
- Hard → total revenue generated  

Scores are always between 0.0 and 1.0.

---

## Baseline Agent

A simple rule-based agent is used:

- increases price when demand is high  
- decreases price when demand is low  
- keeps price unchanged otherwise  

This ensures:
- reproducibility  
- consistent evaluation  
- no dependency on external APIs  

---

## How to Run

### Build the Docker image

```bash
docker build -t pricing-env .
```