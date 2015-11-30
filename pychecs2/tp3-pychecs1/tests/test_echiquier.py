# -*- coding: utf-8 -*-
"""Exemples de tests unitaires pour l'échiquier. Aucun test n'est à remettre, mais vous êtes fortement conseillés de
vous en programmer pour valider vos programmes.

"""
from pychecs.echiquier import Echiquier
from pychecs.piece import Dame, Roi, Fou, Cavalier, Tour, Pion


# Création d'un échiquier avec un dictionnaire de pièces, pour les tests plus bas.
echiquier = Echiquier()
echiquier.dictionnaire_pieces = {
    'd1': Dame('blanc'),
    'c5': Roi('blanc'),
    'f1': Fou('blanc'),
    'e3': Cavalier('blanc'),
    'g2': Tour('blanc'),
    'h2': Pion('blanc'),
    'b7': Pion('noir'),
    'd6': Dame('noir'),
    'e8': Roi('noir'),
    'f7': Fou('noir'),
    'g6': Cavalier('noir'),
    'h8': Tour('noir'),
}

def test_recuperer_piece_a_position():
    assert echiquier.recuperer_piece_a_position('d2') == None
    assert isinstance(echiquier.recuperer_piece_a_position('d1'),Dame)
    assert isinstance(echiquier.recuperer_piece_a_position('c5'),Roi)
    assert isinstance(echiquier.recuperer_piece_a_position('f1'),Fou)
    assert not isinstance(echiquier.recuperer_piece_a_position('d1'),Fou)
    assert not isinstance(echiquier.recuperer_piece_a_position('c5'),Fou)
    assert not isinstance(echiquier.recuperer_piece_a_position('h7'),Fou)

def test_couleur_piece_a_position():
    assert echiquier.couleur_piece_a_position('d1')=='blanc'
    assert echiquier.couleur_piece_a_position('c5')=='blanc'
    assert echiquier.couleur_piece_a_position('g6')=='noir'
    assert echiquier.couleur_piece_a_position('e8')=='noir'

def test_position_est_valide():
    assert echiquier.position_est_valide('a1')
    assert echiquier.position_est_valide('e7')
    assert echiquier.position_est_valide('h8')
    assert echiquier.position_est_valide('f4')
    assert not echiquier.position_est_valide('i1')
    assert not echiquier.position_est_valide('a10')
    assert not echiquier.position_est_valide('j9')
    assert not echiquier.position_est_valide('a0')

def test_colonnes_entre():
    # Exemples de tests pour colonnes_entre.
    assert echiquier.colonnes_entre('a', 'a') == []
    assert echiquier.colonnes_entre('a', 'b') == []
    assert echiquier.colonnes_entre('a', 'c') == ['b']
    assert echiquier.colonnes_entre('a', 'h') == ['b', 'c', 'd', 'e', 'f', 'g']
    assert echiquier.colonnes_entre('c', 'b') == []
    assert echiquier.colonnes_entre('d', 'b') == ['c']
    assert echiquier.colonnes_entre('g', 'd') == ['f', 'e']


def test_chemin_libre_entre_positions():
    # Exemples de tests pour chemin_libre_entre_positions.
    assert echiquier.chemin_libre_entre_positions('d6', 'g6')
    assert not echiquier.chemin_libre_entre_positions('h6', 'd6')
    assert echiquier.chemin_libre_entre_positions('e8', 'e3')
    assert not echiquier.chemin_libre_entre_positions('e8', 'e2')
    assert echiquier.chemin_libre_entre_positions('c2', 'e4')
    assert not echiquier.chemin_libre_entre_positions('c7', 'e5')

def test_deplacement_est_valide():
    assert echiquier.deplacement_est_valide('c5','d5')
    assert echiquier.deplacement_est_valide('c5','c4')
    assert echiquier.deplacement_est_valide('c5','b5')
    assert echiquier.deplacement_est_valide('c5','d5')
    assert echiquier.deplacement_est_valide('c5','b6')
    assert echiquier.deplacement_est_valide('c5','b4')
    assert echiquier.deplacement_est_valide('c5','d6')
    assert echiquier.deplacement_est_valide('c5','d4')
    assert not echiquier.deplacement_est_valide('d1','f1')
    assert not echiquier.deplacement_est_valide('h2','h1')
    assert not echiquier.deplacement_est_valide('g6','a2')
    assert not echiquier.deplacement_est_valide('h8','h9')


if __name__ == '__main__':
    # Exécution des tests unitaires. Pour les intéressés, sachez qu'il existe des outils pour trouver
    # et exécuter automatiquement tous les tests unitaires d'un projet, notamment l'outil py.test.
    print(echiquier)
    test_deplacement_est_valide()
    test_position_est_valide()
    test_couleur_piece_a_position()
    test_colonnes_entre()
    test_recuperer_piece_a_position()
    test_chemin_libre_entre_positions()
