#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not set up connection to the database.")

def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("truncate table matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("select count(player_id) from players")
    ans = c.fetchone()
    DB.commit()
    DB.close()
    return ans[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    c.execute("insert into players values (default, %s)", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute("select * from standings order by wins desc")
    ans = c.fetchall()
    DB.commit()
    DB.close()
    return ans

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    c.execute("insert into matches values (default,%s,%s)", (winner, loser))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB, c = connect()
    c.execute(
    """select standing1.id as id1, standing1.name as name1,
     standing2.id as id2, standing2.name as name2
     from standings as standing1,
     standings as standing2
     where standing1.id < standing2.id and
     standing1.wins = standing2.wins and
     (select count(*) as c from matches as m
     where (m.winner_id = standing1.id and
     m.loser_id = standing2.id) or (m.winner_id = standing2.id and
     m.loser_id = standing1.id)) = 0""")
    pairings = c.fetchall()
    DB.commit()
    DB.close()
    del_pair = []
    players_dict = {}

    for i in range(len(pairings)):
        if pairings[i][0] in players_dict or pairings[i][2] in players_dict:
            del_pair.append(i)
        else:
            players_dict[pairings[i][0]] = 1
            players_dict[pairings[i][2]] = 1

    for i in reversed(del_pair):
        del pairings[i]

    return pairings
