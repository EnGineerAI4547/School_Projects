# -*- coding: utf-8 -*-
"""A5_RL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bh0-Gi1nIz5FqeUzeaW1oGe-Gt1vPmIQ
"""

import numpy as np


class MDP:
	def __init__(self, T, R, discount):
		"""
		The constructor verifies that the inputs are valid and sets
		corresponding variables in a MDP object
		:param T: Transition function: |A| x |S| x |S'| array
		:param R: Reward function: |A| x |S| array
		:param discount: discount factor: scalar in [0,1)
		"""
		assert T.ndim == 3, "Invalid transition function: it should have 3 dimensions"
		self.nActions = T.shape[0]
		self.nStates = T.shape[1]
		assert T.shape == (self.nActions, self.nStates, self.nStates), "Invalid transition function: it has dimensionality " + repr(T.shape) + ", but it should be (nActions,nStates,nStates)"
		assert (abs(T.sum(2) - 1) < 1e-5).all(), "Invalid transition function: some transition probability does not equal 1"
		self.T = T
		assert R.ndim == 2, "Invalid reward function: it should have 2 dimensions"
		assert R.shape == (self.nActions, self.nStates), "Invalid reward function: it has dimensionality " + repr(R.shape) + ", but it should be (nActions,nStates)"
		self.R = R
		assert 0 <= discount < 1, "Invalid discount factor: it should be in [0,1)"
		self.discount = discount

		self.avail_actions = {}
		for s in range(self.nStates):
			self.avail_actions[s] = []
			for a in range(self.nActions):
				if np.max(T[a,s,:])>0: self.avail_actions[s].append(a)


	def isTerminal(self, state):
		return state == self.nStates-1

def build_mazeMDP():
	"""
	adopted from https://cs.uwaterloo.ca/~ppoupart/teaching/cs885-spring18/assignments/asst1/TestRLmaze.py
	Construct a simple maze MDP

	Grid world layout:

	---------------------
	|  0 |  1 |  2 |  3 |
	---------------------
	|  4 |  5 |  6 |  7 |
	---------------------
	|  8 |  9 | 10 | 11 |
	---------------------
	| 12 | 13 | 14 | 15 |
	---------------------

	Goal state: 15
	Bad state: 9
	End state: 16

	The end state is an absorbing state that the agent transitions
	to after visiting the goal state.

	There are 17 states in total (including the end state)
	and 4 actions (up, down, left, right).
	:return: mdp
	"""
	# Transition function: |A| x |S| x |S'| array
	T = np.zeros([4, 17, 17])
	a = 0.8;  # intended move
	b = 0.1;  # lateral move

	# up (a = 0)

	T[0, 0, 0] = a + b;
	T[0, 0, 1] = b;

	T[0, 1, 0] = b;
	T[0, 1, 1] = a;
	T[0, 1, 2] = b;

	T[0, 2, 1] = b;
	T[0, 2, 2] = a;
	T[0, 2, 3] = b;

	T[0, 3, 2] = b;
	T[0, 3, 3] = a + b;

	T[0, 4, 4] = b;
	T[0, 4, 0] = a;
	T[0, 4, 5] = b;

	T[0, 5, 4] = b;
	T[0, 5, 1] = a;
	T[0, 5, 6] = b;

	T[0, 6, 5] = b;
	T[0, 6, 2] = a;
	T[0, 6, 7] = b;

	T[0, 7, 6] = b;
	T[0, 7, 3] = a;
	T[0, 7, 7] = b;

	T[0, 8, 8] = b;
	T[0, 8, 4] = a;
	T[0, 8, 9] = b;

	T[0, 9, 8] = b;
	T[0, 9, 5] = a;
	T[0, 9, 10] = b;

	T[0, 10, 9] = b;
	T[0, 10, 6] = a;
	T[0, 10, 11] = b;

	T[0, 11, 10] = b;
	T[0, 11, 7] = a;
	T[0, 11, 11] = b;

	T[0, 12, 12] = b;
	T[0, 12, 8] = a;
	T[0, 12, 13] = b;

	T[0, 13, 12] = b;
	T[0, 13, 9] = a;
	T[0, 13, 14] = b;

	T[0, 14, 13] = b;
	T[0, 14, 10] = a;
	T[0, 14, 15] = b;

	T[0, 15, 16] = 1;
	T[0, 16, 16] = 1;

	# down (a = 1)

	T[1, 0, 0] = b;
	T[1, 0, 4] = a;
	T[1, 0, 1] = b;

	T[1, 1, 0] = b;
	T[1, 1, 5] = a;
	T[1, 1, 2] = b;

	T[1, 2, 1] = b;
	T[1, 2, 6] = a;
	T[1, 2, 3] = b;

	T[1, 3, 2] = b;
	T[1, 3, 7] = a;
	T[1, 3, 3] = b;

	T[1, 4, 4] = b;
	T[1, 4, 8] = a;
	T[1, 4, 5] = b;

	T[1, 5, 4] = b;
	T[1, 5, 9] = a;
	T[1, 5, 6] = b;

	T[1, 6, 5] = b;
	T[1, 6, 10] = a;
	T[1, 6, 7] = b;

	T[1, 7, 6] = b;
	T[1, 7, 11] = a;
	T[1, 7, 7] = b;

	T[1, 8, 8] = b;
	T[1, 8, 12] = a;
	T[1, 8, 9] = b;

	T[1, 9, 8] = b;
	T[1, 9, 13] = a;
	T[1, 9, 10] = b;

	T[1, 10, 9] = b;
	T[1, 10, 14] = a;
	T[1, 10, 11] = b;

	T[1, 11, 10] = b;
	T[1, 11, 15] = a;
	T[1, 11, 11] = b;

	T[1, 12, 12] = a + b;
	T[1, 12, 13] = b;

	T[1, 13, 12] = b;
	T[1, 13, 13] = a;
	T[1, 13, 14] = b;

	T[1, 14, 13] = b;
	T[1, 14, 14] = a;
	T[1, 14, 15] = b;

	T[1, 15, 16] = 1;
	T[1, 16, 16] = 1;

	# left (a = 2)

	T[2, 0, 0] = a + b;
	T[2, 0, 4] = b;

	T[2, 1, 1] = b;
	T[2, 1, 0] = a;
	T[2, 1, 5] = b;

	T[2, 2, 2] = b;
	T[2, 2, 1] = a;
	T[2, 2, 6] = b;

	T[2, 3, 3] = b;
	T[2, 3, 2] = a;
	T[2, 3, 7] = b;

	T[2, 4, 0] = b;
	T[2, 4, 4] = a;
	T[2, 4, 8] = b;

	T[2, 5, 1] = b;
	T[2, 5, 4] = a;
	T[2, 5, 9] = b;

	T[2, 6, 2] = b;
	T[2, 6, 5] = a;
	T[2, 6, 10] = b;

	T[2, 7, 3] = b;
	T[2, 7, 6] = a;
	T[2, 7, 11] = b;

	T[2, 8, 4] = b;
	T[2, 8, 8] = a;
	T[2, 8, 12] = b;

	T[2, 9, 5] = b;
	T[2, 9, 8] = a;
	T[2, 9, 13] = b;

	T[2, 10, 6] = b;
	T[2, 10, 9] = a;
	T[2, 10, 14] = b;

	T[2, 11, 7] = b;
	T[2, 11, 10] = a;
	T[2, 11, 15] = b;

	T[2, 12, 8] = b;
	T[2, 12, 12] = a + b;

	T[2, 13, 9] = b;
	T[2, 13, 12] = a;
	T[2, 13, 13] = b;

	T[2, 14, 10] = b;
	T[2, 14, 13] = a;
	T[2, 14, 14] = b;

	T[2, 15, 16] = 1;
	T[2, 16, 16] = 1;

	# right (a = 3)

	T[3, 0, 0] = b;
	T[3, 0, 1] = a;
	T[3, 0, 4] = b;

	T[3, 1, 1] = b;
	T[3, 1, 2] = a;
	T[3, 1, 5] = b;

	T[3, 2, 2] = b;
	T[3, 2, 3] = a;
	T[3, 2, 6] = b;

	T[3, 3, 3] = a + b;
	T[3, 3, 7] = b;

	T[3, 4, 0] = b;
	T[3, 4, 5] = a;
	T[3, 4, 8] = b;

	T[3, 5, 1] = b;
	T[3, 5, 6] = a;
	T[3, 5, 9] = b;

	T[3, 6, 2] = b;
	T[3, 6, 7] = a;
	T[3, 6, 10] = b;

	T[3, 7, 3] = b;
	T[3, 7, 7] = a;
	T[3, 7, 11] = b;

	T[3, 8, 4] = b;
	T[3, 8, 9] = a;
	T[3, 8, 12] = b;

	T[3, 9, 5] = b;
	T[3, 9, 10] = a;
	T[3, 9, 13] = b;

	T[3, 10, 6] = b;
	T[3, 10, 11] = a;
	T[3, 10, 14] = b;

	T[3, 11, 7] = b;
	T[3, 11, 11] = a;
	T[3, 11, 15] = b;

	T[3, 12, 8] = b;
	T[3, 12, 13] = a;
	T[3, 12, 12] = b;

	T[3, 13, 9] = b;
	T[3, 13, 14] = a;
	T[3, 13, 13] = b;

	T[3, 14, 10] = b;
	T[3, 14, 15] = a;
	T[3, 14, 14] = b;

	T[3, 15, 16] = 1;
	T[3, 16, 16] = 1;

	# Reward function: |A| x |S| array
	R = -1 * np.ones([4, 17]);

	# set rewards
	R[:, 15] = 100;  # goal state
	R[:, 9] = -70;  # bad state
	R[:, 5] = -70;  # bad state
	R[:, 16] = 0;  # end state

	# Discount factor: scalar in [0,1)
	discount = 0.95

	# MDP object
	mdp = MDP(T, R, discount)




	return mdp

def print_policy(policy):
	print("=== policy ===")
	row, col = [4,4]
	policy = policy[:row*col].reshape([row,col])
	arrows = ['\u2191','\u2193','\u2190','\u2192']
	for i in range(row):
		string = ""
		for j in range(col):
			icon = arrows[int(policy[i, j])]
			if i==0 and j==0:
				# icon = '\x1b[0;30;47m' + icon + '\x1b[0m'
				icon = icon
			elif i==3 and j==3:
				icon = '\x1b[0;30;43m' + icon + '\x1b[0m'
			elif i==2 and j==1:
				icon = '\x1b[0;30;41m' + icon + '\x1b[0m'
			elif i==1 and j==1:
				icon = '\x1b[0;30;41m' + icon + '\x1b[0m'
			string += icon
		print(string)

def print_state_value(V):
	print("========= state value func ========")
	row, col = [4,4]
	last=V[16]
	V = V[:row*col].reshape([row,col])
	arrows = ['\u2191','\u2193','\u2190','\u2192']
	for i in range(row):
		string = "| "
		for j in range(col):
			value = str("{:.2f}".format(V[i, j]))
			if i==0 and j==0:
				# icon = '\x1b[0;30;47m' + icon + '\x1b[0m'
				value = value
			elif i==3 and j==3:
				value = '\x1b[0;30;43m' + value + '\x1b[0m'
			elif i==2 and j==1:
				value = '\x1b[0;30;41m' + value + '\x1b[0m'+ " "
			elif i==1 and j==1:
				value = '\x1b[0;30;41m' + value + '\x1b[0m'
			string += value
			string += " | "
		print("----------------------------------")
		print(string)
	print("----------------------------------")

import numpy as np

class DynamicProgramming:
	def __init__(self, MDP):
		self.R = MDP.R
		self.T = MDP.T
		self.discount = MDP.discount
		self.nStates = MDP.nStates
		self.nActions = MDP.nActions







	def valueIteration(self, initialV, nIterations=np.inf, tolerance=0.01):
		'''Value iteration procedure
		V <-- max_a R^a + gamma T^a V

		Inputs:
		initialV -- Initial value function: array of |S| entries
		nIterations -- limit on the # of iterations: scalar (default: infinity)
		tolerance -- threshold on ||V^n-V^n+1||_inf: scalar (default: 0.01)

		Outputs:
		policy -- Policy: array of |S| entries
		V -- Value function: array of |S| entries
		iterId -- # of iterations performed: scalar
		epsilon -- ||V^n-V^n+1||_inf: scalar'''

		V = np.zeros(self.nStates)
		iterId = 0
		epsilon = tolerance + 1e-9

		while iterId < nIterations and epsilon > tolerance:
			iterId += 1
			epsilon = 0
			for s in range(self.nStates):
				old_value_s = V[s]
				action_values_s = self.Q_helper(V, s) # evaluate Q(s,a) for all a
				V[s] = np.max(action_values_s)
				if epsilon < np.abs(V[s] - old_value_s):
					epsilon = np.abs(V[s] - old_value_s)

		policy = np.zeros(self.nStates, dtype=int)
		for s in range(self.nStates):
			action_values_s = self.Q_helper(V, s)
			policy[s] = np.argmax(action_values_s)

		return [policy, V, iterId, epsilon]

	def Q_helper(self, V, s):
		'''
		Input:  s -- state
		Output: action_values -- Q(s, a) for all actions a
		'''
		action_values = np.zeros(self.nActions)
		for a in range(self.nActions):
			for next_state in range(self.nStates):
				action_values[a] += self.T[a, s, next_state] * V[next_state]
			action_values[a] = self.discount * action_values[a] + self.R[a, s]
		return action_values










	def policyIteration_v1(self, initialPolicy, nIterations=np.inf):
		'''Policy iteration procedure: alternate between policy
		evaluation (solve V^pi = R^pi + gamma T^pi V^pi) and policy
		improvement (pi <-- argmax_a R^a + gamma T^a V^pi).

		Inputs:
		initialPolicy -- Initial policy: array of |S| entries
		nIterations -- limit on # of iterations: scalar (default: inf)
		# tolerance -- threshold on ||V^n-V^n+1||_inf: scalar (default: 0.01)

		Outputs:
		policy -- Policy: array of |S| entries
		V -- Value function: array of |S| entries
		iterId -- # of iterations peformed by modified policy iteration: scalar'''

		policy = np.zeros(dp.nStates, dtype=int)
		iterId = 0

		while iterId < nIterations:
			iterId += 1

			# policy evaluation
			V = self.evaluatePolicy_SolvingSystemOfLinearEqs(policy)

			# policy improvement
			policy_prev = np.copy(policy)
			policy = self.extractPolicy(V)

			# until pi is stable
			if (np.all(np.equal(policy, policy_prev))):
				break

		return [policy, V, iterId]

	def evaluatePolicy_SolvingSystemOfLinearEqs(self, policy):
		'''Evaluate a policy by solving a system of linear equations
		V^pi = R^pi + gamma T^pi V^pi

		Input:
		policy -- Policy: array of |S| entries

		Ouput:
		V -- Value function: array of |S| entries'''

		# Calculate (I-A), b
		I = np.identity(self.nStates)
		A = np.zeros((self.nStates, self.nStates))
		b = np.zeros(self.nStates)
		for s in range(self.nStates):
			a = policy[s]
			b[s] = self.R[a,s]
			A[s, :] = self.T[a, s, :]
		A = I - self.discount * A

		# Solving (I-A)x = b
		V = np.linalg.solve(A, b)

		return V

	def extractPolicy(self, V):
		'''Procedure to extract a policy from a value function
		pi <-- argmax_a R^a + gamma T^a V

		Inputs:
		V -- Value function: array of |S| entries

		Output:
		policy -- Policy: array of |S| entries'''

		policy = np.zeros(self.nStates, dtype=int)
		for s in range(self.nStates):
			action_values_s = self.Q_helper(V, s)
			policy[s] = np.argmax(action_values_s)

		return policy

	print("before converge, policy evaluation requires", " steps")


	def policyIteration_v2(self, initialPolicy, initialV, nPolicyEvalIterations=2,
						   nIterations=np.inf, tolerance=0.01):
		'''Modified policy iteration procedure: alternate between
		partial policy evaluation (repeat a few times V^pi <-- R^pi + gamma T^pi V^pi)
		and policy improvement (pi <-- argmax_a R^a + gamma T^a V^pi)

		Inputs:
		initialPolicy -- Initial policy: array of |S| entries
		initialV -- Initial value function: array of |S| entries
		nPolicyEvalIterations -- limit on # of iterations to be performed in each partial policy evaluation: scalar (default: 5)
		nIterations -- limit on # of iterations to be performed in modified policy iteration: scalar (default: inf)
		tolerance -- threshold on ||V^n-V^n+1||_inf: scalar (default: 0.01)

		Outputs:
		policy -- Policy: array of |S| entries
		V -- Value function: array of |S| entries
		iterId -- # of iterations peformed by modified policy iteration: scalar
		epsilon -- ||V^n-V^n+1||_inf: scalar'''
		policy = np.zeros(dp.nStates, dtype=int)
		V = np.zeros(dp.nStates)
		iterId = 0
		epsilon = 0

		while iterId < nIterations:
			iterId += 1

			# policy evaluation
			V, eval_iter, epsilon = self.evaluatePolicy_IterativeUpdate(policy,V,
																		nPolicyEvalIterations,
																		tolerance)
			# policy improvement
			policy_prev = np.copy(policy)
			policy = self.extractPolicy(V)

			# policy stable
			if (np.all(np.equal(policy, policy_prev))):
				break

		return [policy, V, iterId, epsilon]

	def evaluatePolicy_IterativeUpdate(self, policy, initialV, nIterations, tolerance):
		'''Partial policy evaluation:
		Repeat V^pi <-- R^pi + gamma T^pi V^pi

		Inputs:
		policy -- Policy: array of |S| entries
		initialV -- Initial value function: array of |S| entries
		nIterations -- limit on the # of iterations: scalar (default: infinity)

		Outputs:
		V -- Value function: array of |S| entries
		iterId -- # of iterations performed: scalar
		epsilon -- ||V^n-V^n+1||_inf: scalar'''
		V = initialV
		iterId = 0
		epsilon = tolerance + 1e-9
		while iterId < nIterations and epsilon > tolerance:
			iterId += 1
			epsilon = 0
			for s in range(self.nStates):
				old_value_s = V[s]

				# V(s) = Q(s, pi(s))
				a = policy[s]
				new_value_s = 0
				for next_state in range(self.nStates):
					new_value_s += self.T[a, s, next_state] * V[next_state]
          
				V[s] = self.R[a, s] + self.discount * new_value_s

				if epsilon < np.abs(V[s] - old_value_s):
					epsilon = np.abs(V[s] - old_value_s)
     


		return V, iterId, epsilon







if __name__ == '__main__':
	mdp = build_mazeMDP()
	dp = DynamicProgramming(mdp)
	# Test value iteration
	print("##### DP1: value iteration #####\n")
	[policy, V, nIterations, epsilon] = dp.valueIteration(initialV=np.zeros(dp.nStates), tolerance=0.01)
	print_policy(policy)
	print("\n")
	print('policy converged at iteration', nIterations)
	print('V(s) epsilon after converge', epsilon)
	print("\n")
	print_state_value(V)
	print('\n')
	# Test policy iteration v1
	print("##### DP2: policy iteration v1 #####\n")
	[policy, V, nIterations] = dp.policyIteration_v1(np.zeros(dp.nStates, dtype=int))
	print_policy(policy)
	print("\n")
	print('policy converged at iteration', nIterations)
	print("\n")
	print_state_value(V)
	print('\n')
	# Test policy iteration v2
	print("##### DP3: policy iteration v2 #####\n")
	for p in range(1, 11):
		[policy, V, nIterations, epsilon] = dp.policyIteration_v2(np.zeros(dp.nStates, dtype=int), np.zeros(dp.nStates), nPolicyEvalIterations=p, tolerance=0.01)
		print("nIteration=",p)
		print_policy(policy)
		print("\n")
		print('policy converged at iteration', nIterations)
		print('V(s) epsilon after converge', epsilon)
		print("\n")
		print_state_value(V)

import numpy as np
import matplotlib.pyplot as plt

class ReinforcementLearning:
	def __init__(self, mdp, sampleReward):
		"""
		Constructor for the RL class

		:param mdp: Markov decision process (T, R, discount)
		:param sampleReward: Function to sample rewards (e.g., bernoulli, Gaussian). This function takes one argument:
		the mean of the distribution and returns a sample from the distribution.
		"""

		self.mdp = mdp
		self.sampleReward = sampleReward

	def sampleRewardAndNextState(self,state,action):
		'''Procedure to sample a reward and the next state
		reward ~ Pr(r)
		nextState ~ Pr(s'|s,a)

		Inputs:
		state -- current state
		action -- action to be executed

		Outputs:
		reward -- sampled reward
		nextState -- sampled next state
		'''

		reward = self.sampleReward(self.mdp.R[action,state])
		cumProb = np.cumsum(self.mdp.T[action,state,:])
		nextState = np.where(cumProb >= np.random.rand(1))[0][0]
		return reward,nextState

	def OffPolicyTD(self, nEpisodes, epsilon=0.0):
		'''
		Off-policy TD (Q-learning) algorithm

		Inputs:
		nEpisodes -- # of episodes (one episode consists of a trajectory of nSteps that starts in s0
		epsilon -- probability with which an action is chosen at random

		Outputs:
		Q -- final Q function (|A|x|S| array)
		policy -- final policy
		'''
		alpha = 0.1
		Q = np.zeros([self.mdp.nActions, self.mdp.nStates])
		cum_rewards = np.zeros(nEpisodes)
		for episode in range(nEpisodes):
			state = np.random.randint(self.mdp.nStates-1) # initial state
			step = 0
			done = False
			while not done:

				# Choose action At from St using e-greedy policy dirived from Q
				if np.random.uniform(0, 1) < epsilon:
					action = np.random.randint(self.mdp.nActions)  # Explore
				else:
					action = np.argmax(Q[:,state])  # Exploit

				# Take action At, Observe Rt+1, St+1
				reward, next_state = self.sampleRewardAndNextState(state, action)

				# Update Q[St, At] <- Q[St, At] + alpha[Rt+1 + gamma * max_a Q[St+1, a] - Q[St, At]]
				td_target = reward + self.mdp.discount * np.max(Q[:, next_state])
				td_delta = td_target - Q[action, state]
				Q[action, state] += alpha * td_delta

				# St <- St+1
				state = next_state
				step += 1
				cum_rewards[episode] += reward # Calculate cumulative reward for plotting

				# done if reach terminal state
				if state == 16:
					done = True

		policy = np.zeros(self.mdp.nStates, int)
		for s in range(self.mdp.nStates):
			policy[s] = np.argmax(Q[:, s])

		return [Q, policy, cum_rewards]

	def OffPolicyMC(self, nEpisodes, epsilon=0.0):
		'''
		Off-policy MC algorithm with epsilon-soft behavior policy

		Inputs:
		nEpisodes -- # of episodes (one episode consists of a trajectory of nSteps that starts in s0
		epsilon -- probability with which an action is chosen at random

		Outputs:
		Q -- final Q function (|A|x|S| array)
		policy -- final policy
		'''

		def epsilon_soft(epsilon): # Choose At from St using e-greedy policy dirived from Q
			def func(Q, state):
				if np.random.uniform(0, 1) < epsilon:
					action = np.random.randint(self.mdp.nActions)  # Explore
				else:
					action = np.argmax(Q[:, state])  # Exploit
				if np.argmax(Q[:,state]) != action:  b_AtSt = epsilon / self.mdp.nActions
				else:   b_AtSt = 1 - epsilon + epsilon/self.mdp.nActions
				return action, b_AtSt
			return func

		Q = np.zeros([self.mdp.nActions,self.mdp.nStates])
		C = np.zeros([self.mdp.nActions, self.mdp.nStates])
		target_policy   = lambda q: np.argmax(q)
		behavior_policy = epsilon_soft(epsilon)
		cum_rewards = np.zeros(nEpisodes)

		for episode in range(nEpisodes):

			#### Generate an episode using behavior policy ###
			trajectory = []
			state = np.random.randint(self.mdp.nStates-1)
			for t in range(100):
				action, b_AtSt = behavior_policy(Q, state) # using the epsilon_soft policy wrt Q
				reward, next_state = self.sampleRewardAndNextState(state, action)
				trajectory.append((state, action, b_AtSt, reward))
				state = next_state
				if state == 16:
					break

			#### For each step in the episode, backward ###
			G = 0
			W = 1
			for t in range(len(trajectory))[::-1]:
				state, action, b_AtSt, reward = trajectory[t]

				# Update the total reward from step t to the end
				G = self.mdp.discount * G + reward

				# Update weighted importance sampling formula denominator
				C[action, state] += W

				# Update the action-value function
				Q[action, state] += ( W / C[action, state]) * (G - Q[action, state])

				# If At is not the action taken by target policy, we can break
				if action != np.argmax(Q[:, state]):
					break

				# action probability b(At|St) was already stored in the trajectory
				W = W * 1. / b_AtSt

			#### Cumulative reward #####
			for t in range(len(trajectory)):
				_, _, _, reward = trajectory[t]
				cum_rewards[episode] += reward

		policy = np.zeros(self.mdp.nStates, int)
		for s in range(self.mdp.nStates):
			policy[s] = np.argmax(Q[:, s])

		return [Q,policy,cum_rewards]



if __name__ == '__main__':
	mdp = build_mazeMDP()
	rl = ReinforcementLearning(mdp, np.random.normal)
	f, axa = plt.subplots(2, 1)

	# Test Q-learning
	run_times = 200
	num_episodes = 1500
	x_axis = range(num_episodes)
	avg_rewards = {}
	for epsilon in [0.05, 0.1, 0.3, 0.5]:
		avg_rewards[epsilon] = np.zeros(num_episodes)
		for run in range(run_times):
			[Q, policy, y_axis] = rl.OffPolicyTD(nEpisodes=num_episodes, epsilon=epsilon)
			# print_policy(policy)
			avg_rewards[epsilon] += y_axis
		avg_rewards[epsilon] /= run_times
		axa[1].plot(x_axis[:num_episodes], avg_rewards[epsilon][:num_episodes], label="epsilon="+str(epsilon))
	axa[1].legend(loc='lower right', prop={'size': 9})
	axa[1].set_xlabel("Episodes")
	axa[1].set_ylabel("Avg Cumulative rewards")
	axa[1].set_title("Off-policy TD Control")


	# Test Off-Policy MC
	run_times = 1
	num_episodes = 200000
	x_axis = range(num_episodes)
	avg_rewards = np.zeros(num_episodes)
	for run in range(run_times):
		[Q, policy, y_axis] = rl.OffPolicyMC(nEpisodes=num_episodes, epsilon=1)
		print_policy(policy)
		avg_rewards += y_axis
	avg_rewards /= run_times
	axa[0].plot(x_axis[:num_episodes], avg_rewards[:num_episodes])
	axa[0].set_xlabel("Episodes")
	axa[0].set_ylabel("Avg Cumulative rewards")
	axa[0].set_title("Off-policy MC Control")


	plt.show()