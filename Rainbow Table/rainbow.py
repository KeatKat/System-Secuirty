#!/usr/bin/env python3
import sys
import hashlib

file_in = sys.argv[1]

#open and read the password file
passwords_in = open(file_in,'r')
passwords = passwords_in.read().split('\n')

#get rid of any empty strings
passwords = [item for item in passwords if item != ""]
#get number of passwords in the file
pw_count = len(passwords)

#hash function
def hashing(password):	
	md5_hash = hashlib.md5()
	md5_hash.update(password.encode('utf-8'))
	return md5_hash.hexdigest()
	
#reduction function
def reduction(hashed_pw):
	#convert hexa to long int
	long_integer = int(hashed_pw, 16)
	r = long_integer%pw_count +1
	return r

#function to combined everything, i initally wanted to do this so i just copied and pasted my old code
def hashing_cmb(pw_list):
	hashed_pw = []
	for item in pw_list:
		md5_hash = hashlib.md5()
		md5_hash.update(item.encode('utf-8'))
		hashed_pw.append(md5_hash.hexdigest())
	return hashed_pw
#applying reduction values to the hashed passwords
def reduction_cmb(hashed_pw):
	reduction_pw = []
	for item in hashed_pw:
		#convert hexa to long int
		long_integer = int(item, 16)
		r = long_integer%pw_count +1
		reduction_pw.append(r)
	return reduction_pw

#combining all 3 values delimited by a "--"
def combined_lines(passwords,hashed_pw,reduction_pw):
	combined_PHR = []
	for i in range(pw_count):
		combined = str(i+1) + "--" + str(passwords[i]) + "--" + str(hashed_pw[i]) + "--" + str(reduction_pw[i]) + "\n"
		combined_PHR.append(combined)
	return combined_PHR

#creating the table of all passwords, hashes and reduction value
hashed_cmb = hashing_cmb(passwords)
reduction_cmb = reduction_cmb(hashed_cmb)
combined_lines = combined_lines(passwords,hashed_cmb,reduction_cmb)
#saving the entire table into a file
with open("whole_table.txt", "w") as file:
	for item in combined_lines:
		file.write(item)
	file.close()








#creating the rainbow table
used_passwords = []
rb_table = []
file_out = "rainbow_table.txt"
for word in range(pw_count):
	if passwords[word] not in used_passwords:

		curr_pw = passwords[word]
		used_passwords.append(curr_pw)
		curr_hash = hashing(curr_pw)
		curr_red1= reduction(curr_hash) -1
		
		curr_pw2 = passwords[curr_red1]
		if curr_pw2 not in used_passwords:
			used_passwords.append(curr_pw2)
		curr_hash2 = hashing(curr_pw2)
		curr_red2 = reduction(curr_hash2) -1
		
		curr_pw3 = passwords[curr_red2]
		if curr_pw3 not in used_passwords:
			used_passwords.append(curr_pw3)
		curr_hash3 = hashing(curr_pw3)
		curr_red3 = reduction(curr_hash3) -1
		
		curr_pw4 = passwords[curr_red3]
		if curr_pw4 not in used_passwords:
			used_passwords.append(curr_pw4)
		curr_hash4 = hashing(curr_pw4)
		curr_red4 = reduction(curr_hash4) -1
		
		curr_pw5 = passwords[curr_red4]
		if curr_pw5 not in used_passwords:
			used_passwords.append(curr_pw5)
		curr_hash5 = hashing(curr_pw5)
		curr_red5 = reduction(curr_hash5) -1
		
		curr_pw6 = passwords[curr_red5]
		if curr_pw6 not in used_passwords:
			used_passwords.append(curr_pw6)
		curr_hash6 = hashing(curr_pw6)
		
		
		rb_table.append(curr_pw + "--" + curr_hash6 +"\n")
		
		
#sort the rainbow table according to the hashes and not the password
def sorting_key(item):
	return item.split("--")[1]

sorted_rb_table = sorted(rb_table, key=sorting_key)
#print(rb_table)
with open(file_out,"w") as file:
			for item in sorted_rb_table:
				file.write(item)
			file.close()
		

		
		
		
		
			
			
			
		
		
		
	
