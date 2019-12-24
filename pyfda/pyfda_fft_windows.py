# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Store the available fft windows and their properties
"""
import logging
logger = logging.getLogger(__name__)

import importlib
import numpy as np
import scipy.signal as sig
import scipy


windows =\
    {'Boxcar':
        {'fn_name':'boxcar', 
         'info':
             ("<span>Rectangular (a.k.a. 'Boxcar') window, well suited for coherent signals, i.e. "
              " where the window length is an integer number of the signal's period.</span>"),
        'props':{
            'enbw':1,
            'cgain':1,
            'bw':1
            }
         },
    'Barthann':
        {'fn_name':'scipy.signal.windows.barthann',
         'info':
             ("<span>A modified Bartlett-Hann Window."
              "</span>")},
    'Bartlett':
        {'fn_name':'bartlett',
         'info':'<span>The Bartlett window is very similar to a triangular window, '
             'except that the end points are at zero. Its side lobes fall off with '
             '12 dB/oct., the side lobe suppression is xx dB.'
             '<br /><br />Its Fourier transform is the product of two (periodic) sinc functions.<span>'},
    'Blackman':
        {'fn_name':'blackman'},
    'Blackmanharris':
        {'fn_name':'blackmanharris',
         'info':
             ("<span>The minimum 4-term Blackman-Harris window gives an excellent "
              "constant side-lobe suppression of more than 90 dB while keeping a "
              "reasonably narrow main lobe.</span>")
             },
    'Blackmanharris_7':
        {'fn_name':'pyfda.pyfda_fft_windows.blackmanharris7',
         'info':
             ("<span>The 7-term Blackman-Harris window with excellent side-"
              "lobe suppression.</span>")
             },
    'Bohman':
        {'fn_name':'bohman'},
    'Dolph-Chebychev':
        {'fn_name':'chebwin',
         'par':[{
            'name':'a', 'name_tex':r'$a$',
            'val':80, 'min':45, 'max':300, 
            'tooltip':"<span>Side lobe attenuation in dB.</span>"}],
         'info':
             ("<span>This window optimizes for the narrowest main lobe width for "
              "a given order <i>M</i> and sidelobe equiripple attenuation <i>a</i>, "
              "using Chebychev polynomials.</span>"),
        },
    'Cosine':
        {'info':
             ('<span>The window is half a cosine period, shifted by pi/2. '
              'For that reason it is also known as "half-cosine" or "sine" window.</span>'),
             },
    'Flattop':
         {'win_fn_name':'flattop'},
    'General Gaussian':
        {'fn_name':'general_gaussian',
         'par':[{
            'name':'p','name_tex':r'$p$',
            'val':1.5, 'min':0, 'max':20,
             'tooltip':"<span>Shape parameter p</span>"
             },
             {
            'name':'&sigma;','name_tex':r'$\sigma$',
            'val':5, 'min':0, 'max':100,
             'tooltip':"<span>Standard deviation &sigma;</span>"}
             ],
         'info':
             ("<span>General Gaussian window, <i>p</i> = 1 yields a Gaussian window, "
              "<i>p</i> = 0.5 yields the shape of a Laplace distribution."
              "</span>"),
         },
    'Gauss':
        {'fn_name':'gaussian',
         'par':[{
             'name':'&sigma;', 'name_tex':r'$\sigma$',
             'val':5,'min':0, 'max':100,
             'tooltip':"<span>Standard deviation &sigma;</span>"}],
         'info':
             ("<span>Gaussian window "
              "</span>")
         },
    'Hamming':
        {'fn_name':'hamming',
         'info':
             ("<span>The Hamming Window has been optimized for suppression of "
              "the first side lobe. Compared to the Hann window, this comes at "
              "the cost of a worse (constant) level of higher side lobes."
              "<br />Mathematically, it is a two-term raised cosine window with "
              "non-zero endpoints (DC-offset).</span>")
         },
    'Hann':
        {'fn_name':'hann',
        'info':'<span>The Hann (or, falsely, "Hanning") window is smooth at the '
          'edges. In the frequency domain this corresponds to side-lobes falling '
          'off with a rate of 18 dB/oct or 30 dB/dec. The first sidelobe is quite '
          'high (-32 dB). It is a good compromise for many applications, especially '
          'when higher frequency components need to be suppressed.'
          '<br />Mathematically, it is the most simple two-term raised cosine '
          'or squared sine window.</span>'},
    'Kaiser':
        {'fn_name':'kaiser',
         'par':[{
                'name':'&beta;', 'name_tex':r'$\beta$',
                'val':10, 'min':0, 'max':30,
                'tooltip':
                    ("<span>Shape parameter; lower values reduce  main lobe width, "
                     "higher values reduce side lobe level, typ. in the range "
                     "5 ... 20.</span>")}],
         'info':
             ("<span>The Kaiser window is a very good approximation to the "
              "Digital Prolate Spheroidal Sequence (DPSS), or Slepian window, "
              "which maximizes the energy in the main lobe of the window relative "
              "to the total energy.</span>")
        },
    'Nuttall':{},
    'Parzen':{
        'info':
            ('<span>The Parzen window is a 4th order B-spline window whose side-'
             'lobes fall off with -24 dB/oct.'
             '<br/ >&nbsp;<br />'
             'It can be constructed by convolving '
             'a rectangular window four times (or multiplying its frequency response '
             'four times).'
             '<br />See also: Boxcar and Triangular / Bartlett windows.</span>')},
    'Rectangular':{'fn_name':'boxcar'},
    'Slepian':
        {'fn_name':'slepian',
         'par':[{
             'name':'BW', 'name_tex':r'$BW$',
             'val':0.3, 'min':0, 'max':100,
             'tooltip':"<span>Bandwidth</span>"}],
         'info':
             ("<span>Used to maximize the energy concentration in the main lobe. "
              " Also called the digital prolate spheroidal sequence (DPSS)."
              "<br/ >See also: Kaiser window."
              "</span>")
         },
    'Triangular':{'fn_name':'triang'},
    'Ultraspherical':
        {'fn_name':'pyfda.pyfda_fft_windows.ultraspherical',
         'par':[{
            'name':'&alpha;','name_tex':r'$\alpha$',
            'val':0.5, 'min':-0.5, 'max':10,
             'tooltip':"<span>Shape parameter &alpha; or &mu;</span>"
             },
             {
            'name':'x0','name_tex':r'$x_0$',
            'val':1, 'min':-10, 'max':10,
             'tooltip':"<span>Amplitude</span>"}
             ],
         'info':
             ("<span>Ultraspherical or Gegenbauer window, <i>p</i> = 1 yields a Gaussian window, "
              "<i>p</i> = 0.5 yields the shape of a Laplace distribution."
              "</span>"),
             }
    }
def get_window_names():
    """
    Extract window names (= keys) from the windows dict and return and a list
    with all the names (strings).
    """
    win_name_list = []
    for d in windows:
        win_name_list.append(d)
    
    return sorted(win_name_list)
        

def calc_window_function(win_dict, win_name, N=32, sym=True):
    """
    Generate a window function.

    Parameters
    ----------
    win_dict : dict
        The dict where the window functions are stored.
    win_name : str
        Name of the window, this will be looked for in scipy.signal.windows.
    N : int, optional
        Number of data points. The default is 32.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter design. 
        When False, generates a periodic window, for use in spectral analysis.
    Returns
    -------
    win_fnct : ndarray
        The window function 
    """
    
    par = []
    info = ""
    
    if win_name not in windows:
        logger.warning("Unknown window name {}, using rectangular window instead.".format(win_name))
        win_name = "Boxcar"
    d = windows[win_name]
    if 'fn_name' not in d:
        fn_name = win_name.lower()
    else:
        fn_name = d['fn_name']

    if 'par' in d:
        par = d['par']
        n_par = len(par)
    else:
        par = []
        n_par = 0
        
    if 'info' in d:
        info = d['info']
        
    #--------------------------------------
    # get attribute fn_name from submodule (default: sig.windows) and
    # return the desired window function:
    mod_fnct = fn_name.split('.') # try to split fully qualified name
    fnct = mod_fnct[-1]
    if len(mod_fnct) == 1: 
        # only one element, no modules given -> use scipy.signal.windows
        win_fnct = getattr(sig.windows, fnct, None)
    else:
        # remove the leftmost part starting with the last '.'
        mod_name = fn_name[:fn_name.rfind(".")] 
        mod = importlib.import_module(mod_name)  
        win_fnct = getattr(mod, fnct, None)
    
    if not win_fnct:
        logger.error("No window function {0} in scipy.signal.windows, using rectangular window instead!"\
                     .format(fn_name))
        fn_name  = "boxcar"
        win_fnct = getattr(scipy, fn_name, None)
        
    win_dict.update({'name':win_name, 'fnct':fn_name, 'info':info, 
                     'par':par, 'n_par':n_par, 'win_len':N})

    if n_par == 0:
        return win_fnct(N,sym=sym)
    elif n_par == 1:
        return win_fnct(N, par[0]['val'], sym=sym)
    elif n_par == 2:
        return win_fnct(N, par[0]['val'], par[1]['val'], sym=sym)        
    else:
        logger.error("{0:d} parameters is not supported for windows at the moment!".format(n_par))


def blackmanharris7(N, sym):
    a = [0.27105140069342,
         -0.43329793923448,
         0.21812299954311,
         -0.06592544638803,
         0.01081174209837,
         -0.00077658482522,
         0.00001388721735]
    if sym:
        L = N-1
    else:
        L = N  
    x = np.arange(N) * 2 * np.pi / L
    blk = a[0]
    for k in range(1,7):
        blk += a[k] * np.cos(k*x)
    return blk

def ultraspherical(N, alpha = 0.5, x_0 = 1, sym=True):

    if sym:
        L = N-1
    else:
        L = N  
    #x = np.arange(N) * np.pi / (N)
    
    geg_ev = scipy.special.eval_gegenbauer
    w0= geg_ev(N, alpha, x_0)
    w=np.zeros(N)
    # a = 2
    # for n in range(5 + 1):
    #     x = np.linspace(-1.1, 1.1, 5001)
    #     y = eval_gegenbauer(n, a, x)
    #     plt.plot(x, y, label=r'$C_{%i}^{(2)}$' % n, zorder=-n)
    #     plt.ylim((-10,10))
    
    for n in range(0,N):
        w[n] = w0
        for k in range(1,N//2+1):
            w[n] += geg_ev(N, alpha, x_0 * np.cos(k*np.pi/(N+1))) * np.cos(2*n*np.pi*k/(N+1))
    #     rtn +=  np.cos(x*k)
    
    #w = geg_ev(N-1, alpha, x_0 * np.cos(x))
    #logger.error(W[0].dtype, len(W))
    #W = np.abs(fft.ifft(w))
    #logger.error(type(w[0].dtype), len(w))
    return w


class UserWindows(object):
    def __init__(self, parent):
        super(UserWindows, self).__init__(parent)
 
        
# =======
# see also:
# https://www.electronicdesign.com/technologies/analog/article/21798689/choose-the-right-fft-window-function-when-evaluating-precision-adcs 
# https://github.com/capitanov/blackman_harris_win
# https://en.m.wikipedia.org/wiki/Window_function


