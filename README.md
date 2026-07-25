### 🚀 LunarLander-DQN: From-Scratch Deep Reinforcement Learning

**Overview**  
A completely custom, from-scratch implementation of a Deep Q-Network (DQN) agent designed to safely land a spacecraft in the `LunarLander-v2` environment. This project strictly avoids high-level reinforcement learning libraries (such as Ray RLlib or StableBaselines) to provide a transparent, fundamental build of the DQN architecture and its core mathematical mechanics.

**Key Features**

* **Pure Algorithm Implementation**: Features a custom-built Neural Network policy, an Experience Replay buffer to break data correlation, and a periodically updated Target Network to ensure stable training.


* **Hyperparameter Robustness**: Carefully tuned parameters (learning rate, discount factor, replay buffer capacity, and episode-level epsilon decay) selected to support algorithmic stability and avoid premature collapse of exploration during training.
* **Vanilla DQN, by design**: The project implements a clean, transparent Deep Q-Network (experience replay + target network). Advanced variants such as Double DQN and Dueling DQN are documented in the references as possible extensions, but are intentionally not implemented here so that the core DQN mechanism remains the primary, defensible build.
* **Zero External RL Dependencies**: Built entirely using foundational tools like PyTorch and NumPy, proving a deep understanding of Q-value estimation and backpropagation.

**References & Architecture Foundations**
The neural network architecture and training logic are heavily inspired by the foundational DeepMind papers:

* *Playing Atari with Deep Reinforcement Learning* (Mnih et al., 2013) - Introducing the initial DQN architecture and Experience Replay.


* *Human-level control through deep reinforcement learning* (Mnih et al., 2015) - Introducing the Target Network concept for enhanced training stability.
