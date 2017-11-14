import random
import numpy as np
import matplotlib.pyplot as plt

def main():
	choice = raw_input("Pick an experiment (1, 2, 3): ")
	if choice == '1':
		exp1()
	elif choice == '2':
		exp2()
	elif choice == '3':
		exp3()
	else:
		print "Wrong choice"
	

def plot(Q):
	pickup_states = ['(1,1)', '(1,2)', '(1,3)', '(1,4)', '(1,5)',
					 '(2,1)', '(2,2)', '(2,3)', '(2,4)', '(2,5)',
					 '(3,1)', '(3,2)', '(3,3)', '(3,4)', '(3,5)',
					 '(4,1)', '(4,2)', '(4,3)', '(4,4)', '(4,5)',
					 '(5,1)', '(5,2)', '(5,3)', '(5,4)', '(5,5)'
					 ]
	dropoff_states = ['(1,1)*', '(1,2)*', '(1,3)*', '(1,4)*', '(1,5)*',
					  '(2,1)*', '(2,2)*', '(2,3)*', '(2,4)*', '(2,5)*',
					  '(3,1)*', '(3,2)*', '(3,3)*', '(3,4)*', '(3,5)*',
					  '(4,1)*', '(4,2)*', '(4,3)*', '(4,4)*', '(4,5)*',
					  '(5,1)*', '(5,2)*', '(5,3)*', '(5,4)*', '(5,5)*'
					 ]
	
	
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	pickup_max_Q = []
	for i in pickup_states:		
		pickup_max_Q.append(max(Q[i].values()))
	
	data1 = np.array(pickup_max_Q)
	data1 = np.reshape(data1, (5,5))
	
	ax1.matshow(data1)
	for (i, j), z in np.ndenumerate(data1):
	    ax1.text(j, i, u'\u2190', ha='center', va='center',
	    	bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))

	#plt.figure()
	ax2 = fig.add_subplot(122)
	dropoff_max_Q = []
	for i in dropoff_states:
		dropoff_max_Q.append(max(Q[i].values()))
	data2 = np.array(dropoff_max_Q)
	data2 = np.reshape(data2, (5,5))

	ax2.matshow(data2)
	for (i, j), z in np.ndenumerate(data2):
	    ax2.text(j, i, '{:0.1f}'.format(z), ha='center', va='center',
	    	bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))

	plt.show()


def exp1():	

	alpha = 0.3
	gamma = 0.5
	# Experiment 1: 3000 pRandom then 3000 pGreedy
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	Q = {}
	init_Q(Q)
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(3000):		
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Random(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			
			max_Q = max(Q[next_state].values())
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*max_Q), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)			
			break
	
	# Print Q
	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]
			#fout.write(k, v)
	print "-------------------------------"
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(3000):
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Greedy(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			
			max_Q = max(Q[next_state].values())
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*max_Q), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)
			break

	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]

	plot(Q)

def exp2():	

	alpha = 0.3
	gamma = 0.5
	# Experiment 2: 200 pRandom then 5800 pExploit
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	Q = {}
	init_Q(Q)
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(200):		
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Random(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			
			max_Q = max(Q[next_state].values())
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*max_Q), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)			
			break

	# Print Q
	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]
			#fout.write(k, v)
	print "-------------------------------"
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(5800):
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Exploit(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			
			max_Q = max(Q[next_state].values())
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*max_Q), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)
			break

	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]


def exp3():	

	alpha = 0.3
	gamma = 0.5
	# Experiment 2: 200 pRandom then 5800 pExploit with SARSA for Q values
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	Q = {}
	init_Q(Q)
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(200):		
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Random(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			# SARSA formula
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*Q[current_state][action]), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)			
			break
	# Print Q
	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]
			#fout.write(k, v)
	print "-------------------------------"
	pickups = {'(1,1)': 4, '(3,3)': 4, '(4,1)': 4, '(5,5)': 4}
	dropoffs = {'(4,4)*': 0, '(5,1)*': 0}
	PD_world = {}
	init_PD_world(PD_world)
	current_state = '(1,5)'
	for i in range(5800):
		if dropoffs['(4,4)*'] < 8 or dropoffs['(5,1)*'] < 8:
			action = pick_action_Exploit(PD_world, current_state)
			next_state = PD_world[current_state][action]
			reward = -1
			if action == 'p':
				reward = 12
				pickups[current_state] -= 1
				if pickups[current_state] == 0:
					PD_world[current_state].pop('p') 
			elif action == 'd':
				reward = 12
				dropoffs[current_state] += 1
				if dropoffs[current_state] == 8:
					PD_world[current_state].pop('d')
			
			
			max_Q = max(Q[next_state].values())
			Q[current_state][action] = round((1 - alpha)*Q[current_state][action] + alpha*(reward + gamma*max_Q), 2)
			current_state = next_state
		else:
			print "Drop all off!" + str(i)
			break

	print pickups
	print dropoffs
	sorted_keys = sorted(Q.keys())
	for k in sorted_keys:
		print k,
		print Q[k]


def pick_action_Random(PD_world, current_state):
	if 'p' in PD_world[current_state]:
		return 'p'
	elif 'd' in PD_world[current_state]:
		return 'd'
	else:
		action = random.choice(list(PD_world[current_state].keys()))
		return action


def pick_action_Greedy(PD_world, current_state):
	if 'p' in PD_world[current_state]:
		return 'p'
	elif 'd' in PD_world[current_state]:
		return 'd'
	else:
		max_Q = max(PD_world[current_state].values())
		actions_has_same_maxQ = []
		for key in PD_world[current_state]:
			if PD_world[current_state][key] == max_Q:
				actions_has_same_maxQ.extend(key)
		action = random.choice(actions_has_same_maxQ)
		return action


def pick_action_Exploit(PD_world, current_state):
	if 'p' in PD_world[current_state]:
		return 'p'
	elif 'd' in PD_world[current_state]:
		return 'd'
	else:
		max_Q = max(PD_world[current_state].values())
		actions_has_same_maxQ = []
		for key in PD_world[current_state]:
			if PD_world[current_state][key] == max_Q:
				actions_has_same_maxQ.extend(key)
		if random.randint(0,100) < 85:
			action = random.choice(actions_has_same_maxQ)
			return action
		else:
			action = random.choice(list(PD_world[current_state].keys()))
			return action


def init_PD_world(PD_world):
	PD_world['(1,1)'] = {'e': '(1,2)', 's': '(2,1)', 'p': '(1,1)*'}	
	PD_world['(1,2)'] = {'w': '(1,1)', 'e': '(1,2)', 's': '(2,2)'}	
	PD_world['(1,3)'] = {'w': '(1,2)', 'e': '(1,4)', 's': '(2,3)'}
	PD_world['(1,4)'] = {'w': '(1,3)', 'e': '(1,5)', 's': '(2,4)'}
	PD_world['(1,5)'] = {'w': '(1,4)', 's': '(2,5)'}
	PD_world['(2,1)'] = {'n': '(1,1)', 'e': '(2,2)', 's': '(3,1)'}
	PD_world['(2,2)'] = {'w': '(2,1)', 'n': '(1,2)', 'e': '(2,3)', 's': '(3,2)'}
	PD_world['(2,3)'] = {'w': '(2,2)', 'n': '(1,3)', 'e': '(2,4)', 's': '(3,3)'}
	PD_world['(2,4)'] = {'w': '(2,3)', 'n': '(1,4)', 'e': '(2,5)', 's': '(3,4)'}
	PD_world['(2,5)'] = {'w': '(2,4)', 'n': '(1,5)', 's': '(3,5)'}
	PD_world['(3,1)'] = {'n': '(2,1)', 'e': '(3,2)', 's': '(4,1)'}
	PD_world['(3,2)'] = {'w': '(3,1)', 'n': '(2,2)', 'e': '(3,3)', 's': '(4,2)'}
	PD_world['(3,3)'] = {'w': '(3,2)', 'n': '(2,3)', 'e': '(3,4)', 's': '(4,3)', 'p': '(3,3)*'}
	PD_world['(3,4)'] = {'w': '(3,3)', 'n': '(2,4)', 'e': '(3,5)', 's': '(4,4)'}
	PD_world['(3,5)'] = {'w': '(3,4)', 'n': '(2,5)', 's': '(4,5)'}
	PD_world['(4,1)'] = {'n': '(3,1)', 'e': '(4,2)', 's': '(5,1)', 'p': '(4,1)*'}
	PD_world['(4,2)'] = {'w': '(4,1)', 'n': '(3,2)', 'e': '(4,3)', 's': '(5,2)'}
	PD_world['(4,3)'] = {'w': '(4,2)', 'n': '(3,3)', 'e': '(4,4)', 's': '(5,3)'}
	PD_world['(4,4)'] = {'w': '(4,3)', 'n': '(3,4)', 'e': '(4,5)', 's': '(5,4)'}
	PD_world['(4,5)'] = {'w': '(4,4)', 'n': '(3,5)', 's': '(5,5)'}
	PD_world['(5,1)'] = {'n': '(4,1)', 'e': '(5,2)'}
	PD_world['(5,2)'] = {'w': '(5,1)', 'n': '(4,2)', 'e': '(5,3)'}
	PD_world['(5,3)'] = {'w': '(5,2)', 'n': '(4,3)', 'e': '(5,4)'}
	PD_world['(5,4)'] = {'w': '(5,3)', 'n': '(4,4)', 'e': '(5,5)'}
	PD_world['(5,5)'] = {'w': '(5,4)', 'n': '(4,5)', 'p': '(5,5)*'}

	PD_world['(1,1)*'] = {'e': '(1,2)*', 's': '(2,1)*'}
	PD_world['(1,2)*'] = {'w': '(1,1)*', 'e': '(1,2)*', 's': '(2,2)*'}
	PD_world['(1,3)*'] = {'w': '(1,2)*', 'e': '(1,4)*', 's': '(2,3)*'}
	PD_world['(1,4)*'] = {'w': '(1,3)*', 'e': '(1,5)*', 's': '(2,4)*'}
	PD_world['(1,5)*'] = {'w': '(1,4)*', 's': '(2,5)*'}
	PD_world['(2,1)*'] = {'n': '(1,1)*', 'e': '(2,2)*', 's': '(3,1)*'}
	PD_world['(2,2)*'] = {'w': '(2,1)*', 'n': '(1,2)*', 'e': '(2,3)*', 's': '(3,2)*'}
	PD_world['(2,3)*'] = {'w': '(2,2)*', 'n': '(1,3)*', 'e': '(2,4)*', 's': '(3,3)*'}
	PD_world['(2,4)*'] = {'w': '(2,3)*', 'n': '(1,4)*', 'e': '(2,5)*', 's': '(3,4)*'}
	PD_world['(2,5)*'] = {'w': '(2,4)*', 'n': '(1,5)*', 's': '(3,5)*'}
	PD_world['(3,1)*'] = {'n': '(2,1)*', 'e': '(3,2)*', 's': '(4,1)*'}
	PD_world['(3,2)*'] = {'w': '(3,1)*', 'n': '(2,2)*', 'e': '(3,3)*', 's': '(4,2)*'}
	PD_world['(3,3)*'] = {'w': '(3,2)*', 'n': '(2,3)*', 'e': '(3,4)*', 's': '(4,3)*'}
	PD_world['(3,4)*'] = {'w': '(3,3)*', 'n': '(2,4)*', 'e': '(3,5)*', 's': '(4,4)*'}
	PD_world['(3,5)*'] = {'w': '(3,4)*', 'n': '(2,5)*', 's': '(4,5)*'}
	PD_world['(4,1)*'] = {'n': '(3,1)*', 'e': '(4,2)*', 's': '(5,1)*'}
	PD_world['(4,2)*'] = {'w': '(4,1)*', 'n': '(3,2)*', 'e': '(4,3)*', 's': '(5,2)*'}
	PD_world['(4,3)*'] = {'w': '(4,2)*', 'n': '(3,3)*', 'e': '(4,4)*', 's': '(5,3)*'}
	PD_world['(4,4)*'] = {'w': '(4,3)*', 'n': '(3,4)*', 'e': '(4,5)*', 's': '(5,4)*', 'd': '(4,4)'}
	PD_world['(4,5)*'] = {'w': '(4,4)*', 'n': '(3,5)*', 's': '(5,5)*'}
	PD_world['(5,1)*'] = {'n': '(4,1)*', 'e': '(5,2)*', 'd': '(5,1)'}
	PD_world['(5,2)*'] = {'w': '(5,1)*', 'n': '(4,2)*', 'e': '(5,3)*'}
	PD_world['(5,3)*'] = {'w': '(5,2)*', 'n': '(4,3)*', 'e': '(5,4)*'}
	PD_world['(5,4)*'] = {'w': '(5,3)*', 'n': '(4,4)*', 'e': '(5,5)*'}
	PD_world['(5,5)*'] = {'w': '(5,4)*', 'n': '(4,5)*'}	

def init_Q(Q):
	Q['(1,1)'] = {'e': 0.0, 's': 0.0, 'p': 0.0}	
	Q['(1,2)'] = {'w': 0.0, 'e': 0.0, 's': 0.0}	
	Q['(1,3)'] = {'w': 0.0, 'e': 0.0, 's': 0.0}
	Q['(1,4)'] = {'w': 0.0, 'e': 0.0, 's': 0.0}
	Q['(1,5)'] = {'w': 0.0, 's': 0.0}
	Q['(2,1)'] = {'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,2)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,3)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,4)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,5)'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(3,1)'] = {'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,2)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,3)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0, 'p': 0.0}
	Q['(3,4)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,5)'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(4,1)'] = {'n': 0.0, 'e': 0.0, 's': 0.0, 'p': 0.0}
	Q['(4,2)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,3)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,4)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,5)'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(5,1)'] = {'n': 0.0, 'e': 0.0}
	Q['(5,2)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,3)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,4)'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,5)'] = {'w': 0.0, 'n': 0.0, 'p': 0.0}

	Q['(1,1)*'] = {'e': 0.0, 's': 0.0}
	Q['(1,2)*'] = {'w': 0.0, 'e': 0.0, 's': 0.0}
	Q['(1,3)*'] = {'w': 0.0, 'e': 0.0, 's': 0.0}
	Q['(1,4)*'] = {'w': 0.0, 'e': 0.0, 's': 0.0}
	Q['(1,5)*'] = {'w': 0.0, 's': 0.0}
	Q['(2,1)*'] = {'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,2)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,3)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,4)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(2,5)*'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(3,1)*'] = {'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,2)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,3)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,4)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(3,5)*'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(4,1)*'] = {'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,2)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,3)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0}
	Q['(4,4)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0, 's': 0.0, 'd': 0.0}
	Q['(4,5)*'] = {'w': 0.0, 'n': 0.0, 's': 0.0}
	Q['(5,1)*'] = {'n': 0.0, 'e': 0.0, 'd': 0.0}
	Q['(5,2)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,3)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,4)*'] = {'w': 0.0, 'n': 0.0, 'e': 0.0}
	Q['(5,5)*'] = {'w': 0.0, 'n': 0.0}	

main()