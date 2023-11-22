To allow the file to be executed via ./rainbow Passwords.txt

we have to allow the file to be executable. we can do this by entering  "chmod +x rainbow.py" into the command prompt for the corresponding folder the file is in
after this, you can run the file as "./rainbow.py Passwords.txt" or whatever password.txt file you have. Or u can just run it as "python3 rainbow.py Passwords.txt"

The file produces 2 outputs, the rainbow table and the entire table for referencing.

Once you are ready to do the search, run the searchhash.py as "python3 searchhash.py" and enter the hash that you want to find the pre-image from then click enter.

The search collision is handled simply through a search of the words in the rainbow table. Since every word should be covered by the rainbow table, if in the event where a scenario occurs that is similar to the last few slides in the rainbow table powerpoint slides, the word can still be found.



The reduction is done similarly to the example. Where i take the hashdigest, convert it into an integer and proceed to MOD it against the size of the password file then add 1.
