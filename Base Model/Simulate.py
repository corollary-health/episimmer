import random
import copy
import numpy as np
import ReadFile

class Simulate():
	def __init__(self,config_obj,agents_filename,model):
		self.agents_filename=agents_filename
		self.model=model
		self.config_obj=config_obj

	def onStartSimulation(self):
		#Initialize agents
		self.agents_obj=ReadFile.ReadAgents(self.agents_filename,self.config_obj)

		#Intitialize state list
		self.state_list={}
		self.state_history={}
		for state in self.model.individual_state_types:
			self.state_list[state]=[]
			self.state_history[state]=[]

		#Starting Prevalence as described by config.txt
		for agent in self.agents_obj.agents.values():
			r=random.random()
			if r<self.config_obj.starting_exposed_percentage:
				agent.state='Exposed'

		#Update State list
		for agent in self.agents_obj.agents.values():
			self.state_list[agent.state].append(agent.index)

		#Store state list
		self.store_state()

	def onStartDay(self,filename):
		for agent in self.agents_obj.agents.values():
			agent.new_day()

		ReadFile.ReadInteractions(filename,self.config_obj,self.agents_obj)

	def handleDayForAllAgents(self):
		#Too ensure concurrency we update agent.next_state in method handleDayAsAgent
		#After every agent has updated next_state we update states of all agents in method handleDay() 

		for agent in self.agents_obj.agents.values():
			self.handleDayAsAgent(agent)

		for agent in self.agents_obj.agents.values():
			self.convert_state(agent)

	def handleDayAsAgent(self,agent):
		#Too ensure concurrency we update agent.next_state in method handleDayAsAgent
		#After every agent has updated next_state we update states of all agents in method handleDay()

		#Finding next_state
		agent.set_next_state(self.model.find_next_state(agent,self.agents_obj.agents)) 

	def endDay(self):
		self.store_state()

	def endSimulation(self):
		return self.state_history

	def store_state(self):
		for state in self.state_history.keys():
			self.state_history[state].append(len(self.state_list[state]))

	def convert_state(self,agent):
		self.state_list[agent.state].remove(agent.index)
		agent.update_state()
		self.state_list[agent.state].append(agent.index)