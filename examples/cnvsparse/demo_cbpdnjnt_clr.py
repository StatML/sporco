#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. BSD 3-clause License.
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""Usage example: cbpdn.ConvBPDNJoint (colour images, greyscale dictionary)"""

from __future__ import print_function
from builtins import input
from builtins import range

import numpy as np

from sporco import util
from sporco import plot
from sporco.admm import cbpdn
import sporco.metric as sm


# Load demo image
img = util.ExampleImages().image('standard', 'barbara.png', scaled=True,
                                 zoom=0.5)[27:283,55:311]


# Highpass filter test image
npd = 16
fltlmbd = 10
sl, sh = util.tikhonov_filter(img, fltlmbd, npd)


# Load dictionary
D = util.convdicts()['G:8x8x64']


# Set up ConvBPDNJoint options
lmbda = 1e-2
mu = 1e-2
opt = cbpdn.ConvBPDNJoint.Options({'Verbose' : True, 'MaxMainIter' : 200,
                    'LinSolveCheck' : True, 'RelStopTol' : 5e-3,
                    'AuxVarObj' : False})


# Initialise and run ConvBPDN object
b = cbpdn.ConvBPDNJoint(D, sh, lmbda, mu, opt, dimK=0)
X = b.solve()
print("ConvBPDNJoint solve time: %.2fs" % b.timer.elapsed('solve'))


# Reconstruct representation
shr = b.reconstruct().squeeze()
imgr = sl + shr
print("     reconstruction PSNR: %.2fdB\n" % sm.psnr(img, imgr))


# Display representation and reconstructed image
fig1 = plot.figure(1, figsize=(14,14))
plot.subplot(2,2,1)
plot.imview(sl, fgrf=fig1, title='Lowpass component')
plot.subplot(2,2,2)
plot.imview(np.sum(abs(X), axis=b.cri.axisM).squeeze(), fgrf=fig1,
            fltscl=True, title='Main representation')
plot.subplot(2,2,3)
plot.imview(imgr, fgrf=fig1, title='Reconstructed image')
plot.subplot(2,2,4)
plot.imview(imgr - img, fgrf=fig1, fltscl=True,
            title='Reconstruction difference')
fig1.show()


# Plot functional value, residuals, and rho
its = b.getitstat()
fig2 = plot.figure(2, figsize=(21,7))
plot.subplot(1,3,1)
plot.plot(its.ObjFun, fgrf=fig2, xlbl='Iterations', ylbl='Functional')
plot.subplot(1,3,2)
plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T, fgrf=fig2,
          ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['Primal', 'Dual'])
plot.subplot(1,3,3)
plot.plot(its.Rho, fgrf=fig2, xlbl='Iterations', ylbl='Penalty Parameter')
fig2.show()


# Wait for enter on keyboard
input()
