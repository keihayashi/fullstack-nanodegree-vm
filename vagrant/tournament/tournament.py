#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
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
    cur_num = countPlayers()
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players values (%s, %s)", (cur_num + 1, name))
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
    DB = connect()
    c = DB.cursor()
    c.execute(
    "select p.player_id as id, p.player_name as name, count(case when m.winner_id = p.player_id then 1 end) as wins, count(m.match_id) as matches" +
    " from players as p, matches as m" +
    " where p.player_id = m.winner_id or p.player_id = m.loser_id" +
    " group by p.player_id order by wins desc")
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
    DB = connect()
    c = DB.cursor()
    c.execute("select count(match_id) from matches")
    match_num = c.fetchone()[0]
    c.execute("insert into matches values (%s,%s,%s)", (match_num + 1, winner, loser))
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


if __name__ == '__main__':
    playerStandings()
#
# select p.player_id as id, p.player_name as name, count(case when m.winner_id = p.player_id then 1 end) as wins, count(m.match_id) as matches
# from players as p, matches as m
# where p.player_id = m.winner_id or p.player_id = m.loser_id
# group by p.player_id order by wins desc;
