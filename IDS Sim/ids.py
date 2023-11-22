import sys
import random
import math

data_counter = 0
stat_counter = 0

def main():
	if len(sys.argv) != 4:
		print("Invalid input\nUsage: python3 ids.py <EventsFile> <StatsFile> <Days>")
		return

	events_file = sys.argv[1]
	stats_file = sys.argv[2]
	days = int(sys.argv[3])

	e_dets,s_dets = input_engine(events_file,stats_file)
	if ((e_dets == False) or (s_dets == False)):
		print("Invalid data in files, please re run the program")
		sys.exit()
	baseline,baseline_data = sim_engine(e_dets, s_dets, days)
	baseline_stat = analysis_engine(baseline,days)
	alert_engine(e_dets)	
	
	
	
	
	
	
	
	
	
	
	
		

#===========================================================================================================================================
def sim_engine(e_dets,s_dets,days):
	baseline = []

	#e_dets will be for comparing the base line data
	#we start the simulation by generating some random numbers based on how many days there are assuming there is no negative numbers
	
	#to ensure data is more randomized, i will have 2 sets of randomly generated numbers one for discrete events and one for continuos events
	random_numbers_d = random.sample(range(10001),days)
	random_numbers_c = random.sample(range(10001),days)
	
	#average or random numbers
	average_d = calculate_avg(random_numbers_d)
	stand_dev_d = calculate_standard_dev(random_numbers_d)
	
	average_c = calculate_avg(random_numbers_c)
	stand_dev_c = calculate_standard_dev(random_numbers_c)
	
	#get z score for the individual random values
	z_score_1 = []
	z_score_2 = []
	for x in random_numbers_d:
		z = (x-average_d)/stand_dev_d
		z_score_1.append(z)
		
	for x in random_numbers_c:
		z = (x-average_c)/stand_dev_c
		z_score_2.append(z)
	
	#with the z-score i can come out with target values now
	#at this points we have confirmed that the number of events = number of stats which is just the length of the array
	for stat in s_dets:
		stat_name = stat[0]
		#check whether it is discrete or continuos
		for event in e_dets:
			if event[0] == stat_name:
				cont_or_dis = event[1]
				min_value = event[2]
				max_value = event[3]
			
		
		targets = [stat_name]
		for day in range(days):
			if cont_or_dis == 'D':
				#target is discrete, round it down
				target_raw = (z_score_1[day]*float(stat[2]))+float(stat[1])
				target = math.floor(target_raw)
				
				if((min_value == None) and (max_value)):
					if (target > int(max_value)):
						return False, False
				if((min_value) and (max_value == False)):
					if (target < int(min_value)):
						return False, False
				if((min_value) and (max_value)):
					if ((target > int(max_value)) and (target < int(min_value))):
						return False, False
			
			elif cont_or_dis == 'C':
				#target is continuos, 2dp
				target_raw = (z_score_2[day]*float(stat[2]))+float(stat[1])
				target = round(target_raw, 2)
				
				if((min_value == None) and (max_value)):
					if (target > float(max_value)):
						return False, False
				if((min_value) and (max_value == False)):
					if (target < float(min_value)):
						return False, False
				if((min_value) and (max_value)):
					if ((target > float(max_value)) and (target < int(min_value))):
						return False, False		
				
			targets.append(target)	
			
			
			
			
			
		baseline.append(targets)
	
	

				
		
		
		
		
		
		
	#for unique file names
	global data_counter
	data_counter+=1
	filename = f"baseline_data{data_counter}.txt"
	print(f"Simulated baseline data based on {days} days")
	print(f"Baseline data saved to {filename}")
	print("==============================================")
	
	#generate baseline_data.txt as a human readable file
	baseline_data = []
	with open(filename,"w") as file_out:
		for i in range(days):
			data_in = []
			current_day = i+1
			file_out.write(f"Day {current_day}\n")
			print(f"Day {current_day}")
			for event in baseline:
				event_name = event[0]
				numbers_only = event[1:]
				data_in.append(numbers_only[i])
				file_out.write(f"{event_name}: {numbers_only[i]}\n")
				print(f"{event_name}: {numbers_only[i]}")
			baseline_data.append(data_in)
			file_out.write("=================================\n")
			print("=================================")
		file_out.close()
	
	
	
	#baseline is the array list of all the generated base data
	#baseline_data is the data separated out by days, this will make it easier for the alert engine later
	return baseline,baseline_data
		

#===========================================================================================================================================
def analysis_engine(baseline,days):
	#i have the baseline data now, we can calculate base line statistics
	#doesnt really matter if i use baseline or baseline_data as they provide the same information, but by using baseline the data is already collated for me
	
	
	global stat_counter
	stat_counter+=1
	baseline_stat = []
	#calculating and outputing information into txt file and also in the commandlin
	print("\nSimulated statistic summary based on the simulated baseline data")
	filename = f"baseline_stat{stat_counter}.txt"
	
	print(f"Baseline statistic saved to {filename}")
	with open(filename,"w") as fileout:
		fileout.write(f"Simulated baseline stats based on {days} days\n")
		fileout.write("==============================================\n")
		for event in baseline:
			event_name = event[0]
			numbers_only = event[1:]
			mean = round(calculate_avg(numbers_only),2)
			std_dev = round(calculate_standard_dev(numbers_only),2)
			total_stat = [event_name,mean,std_dev]
			baseline_stat.append(total_stat)
			total_for_event = sum(numbers_only)
			
			fileout.write(f"Event Name: {event_name}, {numbers_only} \nTotal: {total_for_event}\nMean: {mean}, Standard Deviation: {std_dev}")
			fileout.write(f"\n===========================================\n")
			print(f"Event Name: {event_name}, {numbers_only} \nTotal: {total_for_event}\nMean: {mean}, Standard Deviation: {std_dev}")
			print("===========================================")
		fileout.close()
	
	
	
	
	
			
		
	print("Baseline simulated data and statistic generation completed")
	print("Open baseline_stat.txt and baseline_data.txt to view\n")
	
	return baseline_stat
	


	#===========================================================================================================================================
def alert_engine(e_dets):
	s_dets = []
	#weightage is basedp on the event_details file so i have that as a parameter so that i can extract the weightages
	
	total_weightage = 0
	ind_weightage = []
	for events in e_dets:
		total_weightage += int(events[4])
		ind_weightage.append(events[4])
	threshold = total_weightage*2
	while(True):
	#outer for loop in range or days, inner for loop takes baseline
		input_line = input("Please enter a new stats.txt file followed by the number of days\nOr enter 'exit' to quit simulation\n")
		
		if(input_line == "exit"):
			print("Simulation ended")
			break
		
		values = input_line.split()
		
		#check that both parameters are satisfied
		if(len(values)) == 2:
			new_file = values[0]
			new_days = int(values[1])
			
			with open(new_file,"r") as file_in:
			
				#we do some validation again, ensurin that the number of stats is the same as the number of events
				num_stats = int(file_in.readline().strip())
				if(num_stats == len(e_dets)):
					for line in file_in:
						components = line.strip().split(':')
						
						event_name = components[0]
						mean = components[1]
						standard_dev = components[2]
						
						s_dets.append([event_name,mean,standard_dev])
				
			#now that i have my event and statistic details i can once again call on my simulator engine to generate the baseline for me
			baseline,baseline_data = sim_engine(e_dets,s_dets,new_days)
			#and then into my analysis engine
			baseline_stat = analysis_engine(baseline,new_days)
			
			#the information i need to use will be baseline_data, baseline_stat and the threshold
			num_of_events = len(e_dets)
			anomaly_found = False
			for i in range(new_days):
				daily_counter = 0
				for j in range(num_of_events):
					#formula to get the daily counter for the live data
					#abs(abs(live mean - target)/live sd)*weight
					stat_only = baseline_stat[j][1:]
					
					
					#convert all to float first
					target = float(baseline_data[i][j])
					mean = float(stat_only[0])
					std_dev = float(stat_only[1])
					weight = float(ind_weightage[j])
					
					formula = (abs(mean-target)/std_dev)*weight
					
					daily_counter += formula
					
				#catch those daily counters that are above the weight threshold
				if daily_counter > float(threshold):
					anomaly_found = True
					print(f"Day {i+1}")
					print(f"Threshold = {threshold}")
					print(f"Current Score = {daily_counter}")
					print(f"===============================")
			
			if anomaly_found == False:
				print(f"No anomalies found for the {new_days} days simulation\n")				
					
				
				
				
					
					
				
				
			
			
			
			
			
		
		else:
			print("Invalid input please try again\n")
			
			
				
				
			


#===========================================================================================================================================
def input_engine(events, stats):
	#firstly check that the number of events and number of stats match, if it doesnt, reject the file
	
	events_in = open(events,'r')
	num_events = events_in.readline().strip()
	
	stats_in = open(stats, 'r')
	num_stats = stats_in.readline().strip()
	
	
	event_details = []
	stat_details = []
	#checking that the given number of events matches the given number of stats
	if num_stats == num_events:
		#we handle the events file first
		#first line is already taken out
		event_count = 0
		for line in events_in:
			event_count +=1
			components = line.strip().split(':')
			
			event_name = components[0] 
			event_type = components[1] 
			min_value = components[2] if components[2] else None
			max_value = components[3] if components[3] else None
			weight = components[4]
			
			if ((len(event_name) == 0) or (event_type not in ['C','D']) or (len(weight) == 0)):
				return False,False
			event_details.append([event_name,event_type,min_value,max_value,weight])
		
		#handling the stats file
		stat_count = 0
		for line in stats_in:
			stat_count +=1
			components = line.strip().split(':')
			
			event_name = components[0]
			mean = components[1]
			standard_dev = components[2]
			if ((len(event_name) == 0)):
				return False,False
			stat_details.append([event_name,mean,standard_dev])
		
		#double checking that the counts are synced up
		if ((event_count != int(num_events)) or (stat_count != int(num_stats)) or (event_count != stat_count)):
			print("Numbers of given events or number of given stats do not match the number of actual events or stats")
			return False,False
		
		
		#print out the information that i have read in
		print("Read in of events.txt and stats.txt successful")
		print("\n")
		
		#print out event.txt
		for event in event_details:
			print(f"Event Name: {event[0]},{event[1]},Min: {event[2]}, Max: {event[3]}, Weight: {event[4]}")
		print("\n")
		#print out stats.txt
		for stat in stat_details:
			print(f"Event Name: {stat[0]}, Mean: {stat[1]}, Standard Deviation: {stat[2]}")
		print("\n")
		
		#other inconsistencies
		#1 checking that the order of the events are the same in events.txt and stats.txt
		
		#4 checking the name of the event matches the event name in the stats file
		
		
		
		return event_details, stat_details
			
		
		
		
	else:
		print("Number of events and number of statistics do not match")
		return False, False

#===========================================================================================================================================
#math functions
#average function
def calculate_avg(numbers):
	return sum(numbers)/len(numbers)
	
#sd function
def calculate_standard_dev(numbers):
	mean = calculate_avg(numbers)
	sum_squared_diff = 0
	for x in numbers:
		sum_squared_diff += (x-mean)**2
	variance = sum_squared_diff/len(numbers)
	
	standard_dev = math.sqrt(variance)
	return standard_dev









if __name__ == "__main__":
	main()
