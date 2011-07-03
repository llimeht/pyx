#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
# Copyright (C) 2011 Michael Schindler <m-schindler@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
from math import atan2, pi, radians
import sys; sys.path[:0] = ["../.."]
from pyx import canvas, unit, deco, trafo
from pyx import path as pathmodule
from pyx.mpost import *
from pyx.mpost import _mp_endpoint, _mp_explicit, _mp_given, _mp_curl, _mp_open, knot_pt, _knot_len, _mp_make_choices

# internal tests: check that the reimplementation of mp_make_choices is correct:
# tested with the output of a mpost binary (modified to output the knot parameters)

def curve1(): # <<<
    """The open curve of Fig.3 on page 6 of mpman.pdf
    draw z0..z1..z2..z3..z4"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    p.next = knot_pt(60, 40, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(40, 90, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(10, 70, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(30, 50, _mp_curl, 1.0, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots
    refpoints = [
      ((None, None), (0, 0), (26.764633, -1.8454285)),
      ((51.409393, 14.584412), (60, 40), (67.098755, 61.001877)),
      ((59.762527, 84.57518), (40, 90), (25.357147, 94.01947)),
      ((10.480637, 84.502197), (10, 70), (9.628952, 58.804214)),
      ((18.804214, 49.628952), (30, 50), (None, None))]
    return knots, refpoints
# >>>
def curve2(): # <<<
    """The closed curve of Fig.4a on page 6 of mpman.pdf
    draw z0...z1...z2...z3...z4...cycle"""
    p = knot_pt(0, 0, _mp_open, None, 1, _mp_open, None, 1)
    knots = p
    p.next = knot_pt(60, 40, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(40, 90, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(10, 70, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(30, 50, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knots
    refpoints = [
      ((-4.105545, 21.238037), (0, 0), (5.187561, -26.835297)),
      ((60.360733, -18.40036), (60, 40), (59.877136, 59.889008)),
      ((57.338959, 81.642029), (40, 90), (22.399872, 98.483871)),
      ((4.7240448, 84.463684), (10, 70), (13.386368, 60.716507)),
      ((26.355911, 59.135101), (30, 50), (39.194092, 26.951981))]
    return knots, refpoints
# >>>
def curve3(): # <<<
    """The open curve of Fig.6 on page 8 of mpman.pdf
    draw z0..z1{up}..z2{left}..z3..z4"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    # XXX: given angle is copied over from one side to the other:
    p.next = knot_pt(60, 40, _mp_given, 0.5*pi, 1, _mp_given, 0.5*pi, 1)
    p = p.next
    p.next = knot_pt(40, 90, _mp_given, pi, 1, _mp_given, pi, 1)
    p = p.next
    p.next = knot_pt(10, 70, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(30, 50, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots
    refpoints = [
      ((None, None), (0, 0), (28.543137, -11.892975)),
      ((60, 9.0782776), (60, 40), (60, 63.263458)),
      ((60.129883, 90), (40, 90), (25.690277, 90)),
      ((11.52742, 83.230453), (10, 70), (8.666214, 58.446793)),
      ((18.446793, 48.666214), (30, 50), (None, None))]
    return knots, refpoints
# >>>
def curve4(a): # <<<
    """Some of the curves of Figs. 7 and 8 on page 8 of mpman.pdf
    beginfig(7)
    for a=-9 upto 7:
      draw (0,0){dir 45}..{dir 10a}(6cm,0);
    endfor
    endfig;"""
    if a == -90:
        refpoints = [((None, None), (0, 0), (72.980957, 72.980957)),
                     ((170.0787, 61.772141), (170.0787, 0), (None, None))]
    elif a == 0:
        refpoints = [((None, None), (0, 0), (44.36261, 44.36261)),
                     ((110.4153, 0), (170.0787, 0), (None, None))]
    elif a == 70:
        refpoints = [((None, None), (0, 0), (41.195404, 41.195404)),
                     ((138.80974, -85.909775), (170.0787, 0), (None, None))]
    else:
        refpoints = None

    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_given, 0.25*pi, 1)
    knots = p
    p.next = knot_pt(170.078740157, 0, _mp_given, radians(a), 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots
    return knots, refpoints
# >>>
def curve5(): # <<<
    """The right curve of Fig. 9 on page 9 of mpman.pdf
    draw z0{up}...z1{right}...z2{down}"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_given, 0.5*pi, -1)
    knots = p
    p.next = knot_pt(100, 20, _mp_given, 0, -1, _mp_given, 0, -1)
    p = p.next
    p.next = knot_pt(200, 0, _mp_given, -0.5*pi, -1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (0, 19.995117)),
      ((56.625137, 20), (100, 20), (143.37486, 20)),
      ((200, 19.995117), (200, 0), (None, None))]
    return knots, refpoints
# >>>
def curve6a(): # <<<
    """The first curve of Fig.10 on page 9 of mpman.pdf
    draw z0..z1..tension 1 and 1..z2..z3;"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    p.next = knot_pt(50, 50, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(150, 50, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(200, 0, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (10.747421, 21.688171)),
      ((28.311829, 39.252579), (50, 50), (81.50528, 65.612213)),
      ((118.49472, 65.612213), (150, 50), (171.68817, 39.252579)),
      ((189.25258, 21.688171), (200, 0), (None, None))]
    return knots, refpoints
# >>>
def curve6b(): # <<<
    """The first curve of Fig.10 on page 9 of mpman.pdf
    draw z0..z1..tension 1.3 and 1.3..z2..z3;"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    p.next = knot_pt(50, 50, _mp_open, None, 1, _mp_open, None, 1.3)
    p = p.next
    p.next = knot_pt(150, 50, _mp_open, None, 1.3, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(200, 0, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (7.0810547, 24.08403)),
      ((25.91597, 42.918945), (50, 50), (75.109573, 57.382568)),
      ((124.89043, 57.382568), (150, 50), (174.08403, 42.918945)),
      ((192.91895, 24.08403), (200, 0), (None, None))]
    return knots, refpoints
# >>>
def curve6c(): # <<<
    """The first curve of Fig.10 on page 9 of mpman.pdf
    draw z0..z1..tension 2.5 and 1..z2..z3;"""
    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    p.next = knot_pt(50, 50, _mp_open, None, 1, _mp_open, None, 2.5)
    p = p.next
    p.next = knot_pt(150, 50, _mp_open, None, 1, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(200, 0, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (5.4299469, 25.023956)),
      ((24.976044, 44.570053), (50, 50), (63.245346, 52.8741)),
      ((117.57947, 59.957458), (150, 50), (173.92447, 42.651978)),
      ((192.65198, 23.924469), (200, 0), (None, None))]
    return knots, refpoints
# >>>
def curve7(): # <<<
    """The first curve of Fig.10 on page 9 of mpman.pdf
    draw z0..z1..tension atleast 1..{curl 2}z2..z3{-1,-2}..tension 3 and 4..z4..controls z45 and z54..z5;"""

    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1) # z0
    knots = p
    p.next = knot_pt(50, 50, _mp_open, None, 1, _mp_open, None, -1) # z1
    p = p.next
    # XXX: curl value is copied over from one side to the other:
    p.next = knot_pt(80, 0, _mp_curl, 2, -1, _mp_curl, 2, 1) # z2
    p = p.next
    p.next = knot_pt(0, -20, _mp_given, atan2(-2, -1), 1, _mp_given, atan2(-2, -1), 3) # z3
    p = p.next
    p.next = knot_pt(50, -20, _mp_open, None, 4, _mp_explicit, -10, -50) # z4
    p = p.next
    p.next = knot_pt(150, 0, _mp_explicit, 100, 50, _mp_endpoint, None, None) # z5
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (-2.2696381, 28.501495)),
      ((21.498505, 52.269638), (50, 50), (78.324738, 47.744446)),
      ((94.584061, 19.255417), (80, 0), (57.765503, 24.445801)),
      ((16.6745, 13.348999), (0, -20), (-11.100037, -42.200073)),
      ((80.924652, -4.537674), (50, -20), (-10, -50)),
      ((100, 50), (150, 0), (None, None))]
    return knots, refpoints
# >>>
def curve8a(): # <<<
    """Testing degenerate points
    draw (0,0)..(100,50)..(100,50)..{curl 1}(200,0)..(100,-50)..(100,-50)..(0,0)"""

    p = knot_pt(0.0, 0.0, _mp_endpoint, None, None, _mp_curl, 1.0, 1.0)
    knots = p
    p.next = knot_pt(100.0, 50.0, _mp_open, None, 1, _mp_open, None, 1.0)
    p = p.next
    p.next = knot_pt(100.0, 50.0, _mp_open, None, 1, _mp_open, None, 1.0)
    p = p.next
    p.next = knot_pt(200.0, 0.0, _mp_curl, 1, 1, _mp_curl, 1, 1)
    p = p.next
    p.next = knot_pt(100.0, -50.0, _mp_open, None, 1, _mp_open, None, 1.0)
    p = p.next
    p.next = knot_pt(100.0, -50.0, _mp_open, None, 1, _mp_open, None, 1.0)
    p = p.next
    p.next = knot_pt(0.0, 0.0, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (33.333328, 16.666672)),
      ((66.666672, 33.333328), (100, 50), (100, 50)),
      ((100, 50), (100, 50), (133.33333, 33.333328)),
      ((166.66667, 16.666672), (200, 0), (166.66667, -16.666672)),
      ((133.33333, -33.333328), (100, -50), (100, -50)),
      ((100, -50), (100, -50), (66.666672, -33.333328)),
      ((33.333328, -16.666672), (0, 0), (None, None))]
    return knots, refpoints
# >>>
def curve8b(): # <<<
    """Testing degenerate points
    draw (0,0)..tension 2 and 3..(100,50)..tension 3 and 4..(100,50)..tension 4 and 2..{curl 1}(200,0)..tension 2 and 3..(100,-50)..tension 3 and 4..(100,-50)..tension 4 and 2..(0,0)"""

    p = knot_pt(0.0, 0.0, _mp_endpoint, None, None, _mp_curl, 1, 2)
    knots = p
    p.next = knot_pt(100.0, 50.0, _mp_open, None, 3, _mp_open, None, 3)
    p = p.next
    p.next = knot_pt(100.0, 50.0, _mp_open, None, 4, _mp_open, None, 4)
    p = p.next
    p.next = knot_pt(200.0, 0.0, _mp_curl, 1, 2, _mp_curl, 1, 2)
    p = p.next
    p.next = knot_pt(100.0, -50.0, _mp_open, None, 3, _mp_open, None, 3)
    p = p.next
    p.next = knot_pt(100.0, -50.0, _mp_open, None, 4, _mp_open, None, 4)
    p = p.next
    p.next = knot_pt(0.0, 0.0, _mp_curl, 1, 2, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    refpoints = [
      ((None, None), (0, 0), (16.666672, 8.3333282)),
      ((88.888885, 44.444443), (100, 50), (100, 50)),
      ((100, 50), (100, 50), (108.33333, 45.833328)),
      ((183.33333, 8.3333282), (200, 0), (183.33333, -8.3333282)),
      ((111.11111, -44.444443), (100, -50), (100, -50)),
      ((100, -50), (100, -50), (91.666672, -45.833328)),
      ((16.666672, -8.3333282), (0, 0), (None, None))]
    return knots, refpoints
# >>>
def curve9(): # <<<
    """Testing all parts of the code"""

    p = knot_pt(0, 0, _mp_endpoint, None, None, _mp_curl, 1, 1)
    knots = p
    p.next = knot_pt(50, 10, _mp_open, None, 1, _mp_explicit, 50, 10)
    p = p.next
    p.next = knot_pt(100, 0, _mp_explicit, 100, 0, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(150, 50, _mp_explicit, 149, 49, _mp_open, None, 1)
    p = p.next
    p.next = knot_pt(200.0, 0.0, _mp_curl, 1, 1, _mp_endpoint, None, None)
    p = p.next
    p.next = knots

    # we cannot reproduce this case
    refpoints = None
    return knots, refpoints
# >>>
def curve10(): # <<<
    """Testing all parts of the code: test the "else" in item 364
    draw z0..tension 1 and 2..{curl 2}z1..z2..z3..z4..cycle"""
    p = knot_pt(0, 0, _mp_open, None, -1, _mp_open, None, 1) # z0
    knots = p
    # XXX the curl will be copied over to the other side:
    # (but not the tension)
    p.next = knot_pt(60, 40, _mp_curl, 2, 2, _mp_open, None, -1) # z1
    p = p.next
    p.next = knot_pt(40, 90, _mp_open, None, -1, _mp_open, None, -1) # z2
    p = p.next
    p.next = knot_pt(10, 70, _mp_open, None, -1, _mp_open, None, -1) # z3
    p = p.next
    p.next = knot_pt(30, 50, _mp_open, None, -1, _mp_open, None, -1) # z4
    p = p.next
    p.next = knots

    # cannot exactly reproduce this curve using the "draw" statement
    refpoints = None
    #refpoints = [
    #  ((-10.217102, 22.887161), (0, 0), (23.535339, -52.721085)),
    #  ((79.806778, 18.998856), (60, 40), (74.813919, 56.094757)),
    #  ((64.052994, 82.80397), (40, 90), (21.924515, 95.407715)),
    #  ((5.5131836, 83.409958), (10, 70), (13.155396, 60.569336)),
    #  ((26.596268, 59.288879), (30, 50), (38.089523, 27.923462))]
    return knots, refpoints
# >>>

def myprint(knots): # <<<
    str = repr(knots)
    p = knots.next
    while not p is knots:
        str += " "
        str += repr(p)
        p = p.next
    return str
# >>>
def mypath(knots): # <<<
    p = pathmodule.path(pathmodule.moveto_pt(knots.x, knots.y))
    cx, cy = knots.rx, knots.ry
    prev = knots
    k = knots.next
    while not k is knots:
        p.append(pathmodule.curveto_pt(cx, cy, k.lx, k.ly, k.x, k.y))
        cx, cy = k.rx, k.ry
        prev = k
        k = k.next
    if knots.ltype is _mp_explicit:
        p.append(pathmodule.curveto_pt(prev.rx, prev.ry, knots.lx, knots.ly, knots.x, knots.y))
        p.append(pathmodule.closepath())
    return p
# >>>
def check(knots, refpoints, eps=1.0e-3, rel=1.0e-5): # <<<
    if refpoints is None:
        return
    assert _knot_len(knots) == len(refpoints)
    p = knots
    for i, (left, coord, right) in enumerate(refpoints):
        if left[0] is not None:
            assert abs(left[0]-p.lx) < rel*(abs(left[0])+eps)
            assert abs(left[1]-p.ly) < rel*(abs(left[1])+eps)
        assert abs(coord[0]-p.x) < rel*(abs(coord[0])+eps)
        assert abs(coord[1]-p.y) < rel*(abs(coord[1])+eps)
        if right[0] is not None:
            assert abs(right[0]-p.rx) < rel*(abs(right[0])+eps)
            assert abs(right[1]-p.ry) < rel*(abs(right[1])+eps)
        p = p.next
# >>>
def checkone(knots, refpoints): # <<<
    print myprint(knots)
    _mp_make_choices(knots)
    print myprint(knots)

    c = canvas.canvas()
    c.stroke(mypath(knots), [deco.shownormpath(), deco.earrow.normal])
    c.writePDFfile(bboxenlarge=unit.t_cm)
    c.writeEPSfile(bboxenlarge=unit.t_cm)

    check(knots, refpoints)
# >>>
def checkall(): # <<<
    c = None
    for knots, refpoints in [curve1(), curve2(), curve3(),
                             curve4(-90), curve4(0), curve4(70), curve5(),
                             curve6a(), curve6b(), curve6c(), curve7(),
                             curve8a(), curve8b(), curve9(), curve10()]:
        #print myprint(knots)
        _mp_make_choices(knots)
        #print myprint(knots)

        cc = canvas.canvas()
        cc.stroke(mypath(knots), [deco.shownormpath(), deco.earrow.normal])
        if c is None:
            c = canvas.canvas()
            c.insert(cc)
        else:
            c.insert(cc, [trafo.translate(0, c.bbox().bottom() - cc.bbox().top()-0.5)])

        check(knots, refpoints)
    c.writePDFfile()
    c.writeEPSfile()
# >>>

# test of the user interface:

def interface(): # <<<
    c = None

    for p in [
      path(beginknot(0,0), curve(), knot(6,4), curve(), knot(4,9), curve(), knot(1,7), curve(), endknot(3,5)),
      path(beginknot(0,0), curve(), endknot(6,4), beginknot(4,9), curve(), knot(1,7), curve(), endknot(3,5)),
      path(knot(0,0), curve(), knot(6,4), curve(), knot(4,9), curve(), knot(1,7), curve(), knot(3,5), curve()),
      path(knot(0,0), curve(), knot(6,4), curve(), endknot(4,9), beginknot(1,7), curve(), knot(3,5), curve()),
      path(knot(0,0), curve(), knot(6,4), curve(), knot(4,9), line(), knot(1,7), curve(), knot(3,5), curve()),
      # XXX the internal mp_make_choices treats this as closed, but the last curve is not plotted:
      path(knot(0,0), curve(), knot(6,4), curve(), knot(4,9), line(), knot(1,7), curve(), knot(3,5)),
    ]:
        cc = canvas.canvas()
        cc.stroke(p, [deco.shownormpath(), deco.earrow.normal])
        if c is None:
            c = cc
        else:
            c.insert(cc, [trafo.translate(c.bbox().right() - cc.bbox().left() + 0.5, 0)])
    c.writePDFfile()
    c.writeEPSfile()
# >>>


if __name__ == "__main__":
    #checkone(*curve10())
    checkall()
    interface()

# vim:foldmethod=marker:foldmarker=<<<,>>>
