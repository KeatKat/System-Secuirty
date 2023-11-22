import hashlib
#check through the rbt for the corresponding hash value
#if it searches through the table and no hash value matches
#apply reduction function so that i can reference off the whole table
def check_rbt(hash_in):
	for hashes in rbt:
		split_line = hashes.split("--")
		hash_value = split_line[1]
		if hash_in == hash_value:
			return True
	return(reduction(hash_in))
	
#checking the entire table for corresponding reduction value then return hash to check against rbt again
def check_whole(red_value):
	for item in whole_table:
		split_item = item.split("--")
		number = split_item[0]
		if red_value == int(number):
			hash_value = split_item[2]
			return hash_value


def check_password(rbt_hash):
	#filter out only correct hash matches
	correct_hash_rbt = []
	for password in rbt:
		split_line = password.split("--")
		hash_value = split_line[1]
		if hash_value == rbt_hash:
			correct_hash_rbt.append(password)
				
	#for each password reduce until hash matches
	for password in correct_hash_rbt:
		split_line = password.split("--")
		keyword = split_line[0]#the word itself
		hashed_pw = hashing(keyword)#hash of the word
		if(hashed_pw == original_hash):
			return keyword
		
		for i in range(5):
			hashed_keyword = hashing(keyword)
			if hashed_keyword == original_hash:
				return keyword
			else:
				red_value = reduction(hashed_keyword)
				keyword = whole_table[red_value-1].split("--")[1]
				
		#if the code reaches here there is probably a collision but technically the word can still be found since the rainbow table will cover all bases, so it is likely one of the rainbow table words is the target hash
	for password in rbt:
		split_pass = password.split("--")
		key_word = split_pass[0]
		hashed_keyword = hashing(key_word)
		
		if hashed_keyword == original_hash:
			return key_word
		
		
#reduction function
def reduction(hashed_pw):
	#convert hexa to long int
	long_integer = int(hashed_pw, 16)
	r = long_integer%pw_count +1
	return r

#hash function
def hashing(password):	
	md5_hash = hashlib.md5()
	md5_hash.update(password.encode('utf-8'))
	return md5_hash.hexdigest()


#rainbow table read in
rbt=[]
with open("rainbow_table.txt","r") as file_in:
	for lines in file_in:	
		rbt.append(lines.strip())
	file_in.close()
#whole table read in
whole_table = []
with open("whole_table.txt") as file_in:
	for lines in file_in:
		whole_table.append(lines.strip())#get rid of \n
	file_in.close()
#password count is the same as the whole table count
pw_count = len(whole_table)


hash_in = input("Enter hash value to search: " )
original_hash = hash_in
#checking goes in 5 iterations

found = False
for i in range(5):
	hash_check = check_rbt(hash_in)
	if hash_check is True:
		best = check_password(hash_in)
		print(best)
		found = True
		break
	else:
		hash_in = check_whole(hash_check)

if found == False:
	print("Invalid hash entered")

