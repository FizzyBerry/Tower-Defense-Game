import pytest

# functions being tested
from code import Menu, Scoreboard, Game, Tower,ShootingTower, SlowingTower

# checks if tower can be build
def test_Game_building_tower_succesfully(true=None):
    G = Game()
    tower = Tower
    result = G.buildTower(tower, (0,0))
    assert result == true

# checks buildTower with wrong parameters
def test_Game_buildinng_tower_on_unexisting_parameters():
    G = Game()
    tower = Tower
    result = G.buildTower(tower,(-1,-4))
    assert result == False

# checks if score is saved succesfully by removing it (in scoreboard nicknames are unique) (checking if nickname is unique will be implemented in method saveScore)
def test_Game_save_score():
    M = Menu()
    G = Game()
    S = Scoreboard()
    G.saveScore("nickname")
    M.showScoreboard()
    assert S.removeScore("nickname") == True

# checks deleting tower by checking money
def test_Game_delete_tower():
    G = Game
    tower = Tower
    moneyBefore = G.getMoney()
    moneyFromTower = G.buildTower(tower, (0,0))
    G.deleteTower()
    moneyAfter = G.getMoney()
    assert moneyAfter + moneyFromTower == moneyBefore

# checks upgrading tower
def test_Tower_upgrade():
    T = Tower()
    levelBefore = T.getLevel()
    T.upgrade()
    levelAfter = T.getLevel()
    assert levelAfter == levelBefore + 1