Tournament Results
===

## Description
Demonstrate Swiss-system tournament using vagrant VM and sql database.
It is assumed that the number of players is even.

## Usage
1. Install Vagrant and VirtualBox. Use **vagrant up** and **vagrant ssh** command to launch the vagrant VM.
2. Move to /vagrant/tournament folder. You can check the tournament.py works by running the test program as follows.  
```
$ python tournament_test.py
```
3. You can access the database of this project using PostgreSQL. Use **psql** command as follows.
```
$ psql tournament
```
4. You can also play around by adding main function to the end of tournament.py and run the file.
