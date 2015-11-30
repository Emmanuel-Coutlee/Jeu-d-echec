# -*- coding: utf-8 -*-
"""Exemples de tests unitaires pour les pièces. Aucun test n'est à remettre, mais vous êtes fortement conseillés de
vous en programmer pour valider vos programmes.

"""
from pychecs.piece import Piece, Pion,Fou, Dame, Cavalier, Roi, Tour


def test_couleur():
    # Test de méthodes de la classe de base Pion.
    piece = Piece('noir', True)
    assert piece.est_noir()

    piece = Piece('blanc', False)
    assert piece.est_blanc()


def test_mouvements_pion():
    # Quelques tests de déplacements de pion blanc.
    pion = Pion('blanc')
    assert pion.peut_se_deplacer_vers('b2', 'b3')
    assert not pion.peut_se_deplacer_vers('b2', 'c3')
    assert not pion.peut_se_deplacer_vers('c2', 'c1')
    assert not pion.peut_se_deplacer_vers('c2', 'c2')

    # Quelques tests de déplacements de pion noir.
    pion = Pion('noir')
    assert not pion.peut_se_deplacer_vers('b2', 'b3')
    assert not pion.peut_se_deplacer_vers('b3', 'c2')
    assert pion.peut_se_deplacer_vers('c2', 'c1')

def test_mouvement_tour():
    tour = Tour('blanc')
    assert tour.peut_se_deplacer_vers('a1', 'a8')
    assert tour.peut_se_deplacer_vers('a1', 'h1')
    assert tour.peut_se_deplacer_vers('h8', 'h1')
    assert tour.peut_se_deplacer_vers('h8', 'a8')
    assert not tour.peut_se_deplacer_vers('a1', 'f5')
    assert not tour.peut_se_deplacer_vers('a1', 'c3')
    assert not tour.peut_se_deplacer_vers('a1', 'b3')
    assert not tour.peut_se_deplacer_vers('h8', 'g6')


def test_mouvements_fou():
    # Quelques tests de déplacements de pion blanc.
    fou = Fou('blanc')
    assert fou.peut_se_deplacer_vers('c1', 'a3')
    assert not fou.peut_se_deplacer_vers('c1', 'e5')
    assert not fou.peut_se_deplacer_vers('c1', 'd3')
    assert not fou.peut_se_deplacer_vers('c1', 'h2')

def test_mouvements_dame():
    # Quelques tests de déplacements de pion blanc.
    dame = Dame('blanc')
    assert dame.peut_se_deplacer_vers('d1', 'a4')
    assert dame.peut_se_deplacer_vers('d1', 'h5')
    assert dame.peut_se_deplacer_vers('d1', 'd8')
    assert dame.peut_se_deplacer_vers('d1', 'h1')
    assert not dame.peut_se_deplacer_vers('d1', 'e5')
    assert not dame.peut_se_deplacer_vers('d1', 'g3')
    assert not dame.peut_se_deplacer_vers('d1', 'h2')

def test_mouvements_cavalier():
    # Quelques tests de déplacements de pion blanc.
    cav = Cavalier('blanc')
    assert cav.peut_se_deplacer_vers('h3', 'g1')
    assert cav.peut_se_deplacer_vers('f3', 'g1')
    assert cav.peut_se_deplacer_vers('e2', 'g1')
    assert cav.peut_se_deplacer_vers('d2', 'b1')
    assert not cav.peut_se_deplacer_vers('g1', 'f2')
    assert not cav.peut_se_deplacer_vers('g1', 'g3')
    assert not cav.peut_se_deplacer_vers('g1', 'h2')
    assert not cav.peut_se_deplacer_vers('g1', 'e3')
    assert not cav.peut_se_deplacer_vers('g1', 'f4')



def test_mouvements_roi():
    # Quelques tests de déplacements de pion blanc.
    roi = Roi('blanc')
    assert roi.peut_se_deplacer_vers('e1', 'f1')
    assert roi.peut_se_deplacer_vers('e1', 'd1')
    assert roi.peut_se_deplacer_vers('e1', 'e2')
    assert roi.peut_se_deplacer_vers('e1', 'd2')
    assert roi.peut_se_deplacer_vers('e8', 'f7')
    assert roi.peut_se_deplacer_vers('e8', 'e7')
    assert not roi.peut_se_deplacer_vers('e1', 'e8')
    assert not roi.peut_se_deplacer_vers('e1', 'e3')
    assert not roi.peut_se_deplacer_vers('e1', 'h1')
    assert not roi.peut_se_deplacer_vers('e1', 'h3')
    assert not roi.peut_se_deplacer_vers('e1', 'a4')

def test_prises_pion():
    # Quelques tests de prises par un pion blanc.
    pion = Pion('blanc')
    assert pion.peut_faire_une_prise_vers('b2', 'c3')
    assert pion.peut_faire_une_prise_vers('b2', 'a3')
    assert not pion.peut_faire_une_prise_vers('b2', 'b3')
    assert not pion.peut_faire_une_prise_vers('c2', 'c1')
    assert not pion.peut_faire_une_prise_vers('c2', 'c2')
    assert not pion.peut_faire_une_prise_vers('c2', 'c3')
    assert not pion.peut_faire_une_prise_vers('c2', 'c4')

    # Quelques tests de prises par un pion noir.
    pion = Pion('noir')
    assert not pion.peut_faire_une_prise_vers('b2', 'c3')
    assert not pion.peut_faire_une_prise_vers('b2', 'a3')
    assert pion.peut_faire_une_prise_vers('b3', 'c2')
    assert not pion.peut_faire_une_prise_vers('c2', 'c1')


def test_mouvements_pion_deplacement_depart():
    # Quelques tests pour le mouvement initial d'un pion: il peut sauter 2 cases.
    pion = Pion('blanc')
    assert pion.peut_se_deplacer_vers('b2', 'b4')
    assert pion.peut_se_deplacer_vers('g2', 'g4')
    assert not pion.peut_se_deplacer_vers('b2', 'b5')
    assert not pion.peut_se_deplacer_vers('c3', 'c5')

    pion = Pion('noir')
    assert not pion.peut_se_deplacer_vers('b2', 'b4')
    assert pion.peut_se_deplacer_vers('b7', 'b5')
    assert pion.peut_se_deplacer_vers('h7', 'h5')
    assert not pion.peut_se_deplacer_vers('d7', 'd4')
    assert not pion.peut_se_deplacer_vers('d8', 'd6')




if __name__ == '__main__':
    # Exécution des tests unitaires. Pour les intéressés, sachez qu'il existe des outils pour trouver
    # et exécuter automatiquement tous les tests unitaires d'un projet, notamment l'outil py.test.
    test_mouvement_tour()
    test_mouvements_cavalier()
    test_mouvements_dame()
    test_mouvements_fou()
    test_couleur()
    test_mouvements_pion()
    test_prises_pion()
    test_mouvements_pion_deplacement_depart()
