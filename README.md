Tournament Results
===

## Description
Demonstrate Swiss-system tournament using vagrant VM and sql database.<br>
It is assumed that the number of players is even.

## Usage
1. Install Vagrant and VirtualBox. Use **vagrant up** and **vagrant ssh** command to launch the vagrant VM.
2. Move to /vagrant/tournament folder. Set up database by **psql -f filename** command. You can check the tournament.py works by running the test program as follows.  
```
$ psql -f tournament.sql # read commands from the file
$ python tournament_test.py # run the test file
```
3. You can access the database of this project using PostgreSQL. Use **psql** command as follows.
```
$ psql tournament # interactive terminal mode
```
4. You can also play around by adding main function to the end of tournament.py and run the file.
