"""3D anisotropic diffusion filter code.

This script is taken from stackoverflow user ali_m:
[1] http://stackoverflow.com/questions/10802611/anisotropic-diffusion-2d-images
[2] http://pastebin.com/sBsPX4Y7

"""

import numpy as np
import warnings


def anisodiff3(stack, niter=1, kappa=50, gamma=0.1, step=(1., 1., 1.),
               option=1, ploton=False):
        """3D anisotropic diffusion.

        Parameters
        ----------
        stack : 3d numpy array
            Input stack/image/volume/data.
        niter : int
            Number of iterations
        kappa : float
            Conduction coefficient (20-100?). Controls conduction as a
            function of gradient.  If kappa is low small intensity
            gradients are able to block conduction and hence diffusion
            across step edges.  A large value reduces the influence of
            intensity gradients on conduction.
        gamma : float
            Controls speed of diffusion (you usually want it at a
            maximum of 0.25 for stability).
        step : tuple
            The distance between adjacent pixels in (z,y,x). Step is
            used to scale the gradients in case the spacing between
            adjacent pixels differs in the x,y and/or z axes.
        option : int, 1 or 2
            1 favours high contrast edges over low contrast ones
            (Perona & Malik [1] diffusion equation No 1).
            2 favours wide regions over smaller ones
            (Perona & Malik [1] diffusion equation No 2).
        ploton : bool
            if True, the middle z-plane will be plotted on every
            iteration/

        Returns
        -------
        stackout : 3d numpy array
            Diffused stack/image/volume/data.

        Reference
        ---------
        [1] P. Perona and J. Malik.
            Scale-space and edge detection using ansotropic diffusion.
            IEEE Transactions on Pattern Analysis and Machine
            Intelligence, 12(7):629-639, July 1990.

        Notes
        -----
        Original MATLAB code by Peter Kovesi
        School of Computer Science & Software Engineering,
        The University of Western Australia
        <http://www.csse.uwa.edu.au>

        Translated to Python and optimised by Alistair Muldal
        Department of Pharmacology, University of Oxford
        <alistair.muldal@pharm.ox.ac.uk>

        June 2000  original version.
        March 2002 corrected diffusion equation No 2.
        July 2012 translated to Python
        January 2017 docstring reorganization.

        """
        # ...you could always diffuse each color channel independently if you
        # really want
        if stack.ndim == 4:
                warnings.warn("Only grayscale stacks allowed, converting to 3D \
                              matrix")
                stack = stack.mean(3)

        # initialize output array
        stack = stack.astype('float32')
        stackout = stack.copy()

        # initialize some internal variables
        deltaS = np.zeros_like(stackout)
        deltaE = deltaS.copy()
        deltaD = deltaS.copy()
        NS = deltaS.copy()
        EW = deltaS.copy()
        UD = deltaS.copy()
        gS = np.ones_like(stackout)
        gE = gS.copy()
        gD = gS.copy()

        # create the plot figure, if requested
        if ploton:
            import pylab as pl

            showplane = stack.shape[0]//2

            fig = pl.figure(figsize=(20, 5.5), num="Anisotropic diffusion")
            ax1, ax2 = fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)

            ax1.imshow(stack[showplane, ...].squeeze(),
                       interpolation='nearest')
            ih = ax2.imshow(stackout[showplane, ...].squeeze(),
                            interpolation='nearest', animated=True)
            ax1.set_title("Original stack (Z = %i)" % showplane)
            ax2.set_title("Iteration 0")

            fig.canvas.draw()

        for ii in xrange(niter):

                # calculate the diffs
                deltaD[:-1, :, :] = np.diff(stackout, axis=0)
                deltaS[:, :-1, :] = np.diff(stackout, axis=1)
                deltaE[:, :, :-1] = np.diff(stackout, axis=2)

                # conduction gradients (only need to compute one per dim!)
                if option == 1:
                        gD = np.exp(-(deltaD/kappa)**2.)/step[0]
                        gS = np.exp(-(deltaS/kappa)**2.)/step[1]
                        gE = np.exp(-(deltaE/kappa)**2.)/step[2]
                elif option == 2:
                        gD = 1./(1.+(deltaD/kappa)**2.)/step[0]
                        gS = 1./(1.+(deltaS/kappa)**2.)/step[1]
                        gE = 1./(1.+(deltaE/kappa)**2.)/step[2]

                # update matrices
                D = gD*deltaD
                E = gE*deltaE
                S = gS*deltaS

                # subtract a copy that has been shifted 'Up/North/West' by one
                # pixel. don't as questions. just do it. trust me.
                UD[:] = D
                NS[:] = S
                EW[:] = E
                UD[1:, :, :] -= D[:-1, :, :]
                NS[:, 1:, :] -= S[:, :-1, :]
                EW[:, :, 1:] -= E[:, :, :-1]

                # update the image
                stackout += gamma*(UD+NS+EW)

                if ploton:
                        iterstring = "Iteration %i" % (ii+1)
                        ih.set_data(stackout[showplane, ...].squeeze())
                        ax2.set_title(iterstring)
                        fig.canvas.draw()
                        # sleep(0.01)

        return stackout
