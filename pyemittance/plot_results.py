import numpy as np
import matplotlib.pyplot as plt
import colorsys

import beamdynamics

import myplotstyle as ms

def plotMisplacement(emit_data):
    misplacement_dict = emit_data['Meta_data']['misplacement']

    dimension = misplacement_dict['orientation']

    subplot = ms.subplot_factory(2,2)
    plt.figure(figsize=(15, 10))
    plt.suptitle('Slice misplacement', fontsize=16)
    sp_ctr = 1


    sp_x0 = subplot(sp_ctr, title='Reconstructed %s0' % dimension, sciy=True, xlabel='Slice position', ylabel='%s [m]' % dimension, scix=True)
    sp_ctr += 1
    sp_xp0 = subplot(sp_ctr, title='Reconstructed %sP0' % dimension, sciy=True, xlabel='Slice position', ylabel='%s\'' % dimension, scix=True)
    sp_ctr += 1
    sp_a = subplot(sp_ctr, title='Misplacement parameter', xlabel='Slice position', ylabel='A', scix=True)
    sp_ctr += 1
    sp_current = subplot(sp_ctr, title='Current', sciy=True, xlabel='Slice position', ylabel='Currennt (arb. units)', scix=True)
    sp_ctr += 1

    xx_slice = misplacement_dict['mean_sliceZ'].mean(axis=(0,1))
    xx_slice_err = misplacement_dict['mean_sliceZ'].std(axis=(0,1))

    x0 = misplacement_dict['x0_slice']
    x0_err = misplacement_dict['x0_slice_err']
    xp0 = misplacement_dict['xp0_slice']
    xp0_err = misplacement_dict['xp0_slice_err']
    a_proj = misplacement_dict['misplacement_proj']
    a_ref = misplacement_dict['misplacement_ref']

    mean_current = misplacement_dict['current_slice_mean']
    std_current = misplacement_dict['current_slice_std']

    sp_x0.errorbar(xx_slice, x0, xerr=xx_slice_err, yerr=x0_err, marker='.')
    sp_xp0.errorbar(xx_slice, xp0, xerr=xx_slice_err, yerr=xp0_err, marker='.')
    sp_a.errorbar(xx_slice, a_proj, xerr=xx_slice_err, marker='.', label='Proj')
    sp_a.errorbar(xx_slice, a_ref, xerr=xx_slice_err, marker='.', label='Design')
    sp_current.errorbar(xx_slice, mean_current, xerr=xx_slice_err, yerr=std_current, marker='.')

    sp_a.legend(title='Optics reference')

def plotProjEmittance(emit_data):

    location = emit_data['Input']['Measurement location']
    measurement_type = emit_data['Input']['Measurement type']
    energy_eV = emit_data['Input']['energy_eV']
    dimension = emit_data['Input']['Dimension']
    rel_gammaBeta = beamdynamics.calc_gammaBeta(energy_eV)
    meta_data = emit_data['Meta_data']

    fig = plt.figure(figsize=(15, 10))
    fig.subplots_adjust(hspace=0.3)
    plt.suptitle('%s: energy %i MeV' % (location, energy_eV/1e6), fontsize=16)

    dim_str_dict = {
            'X': 'Horizontal',
            'Y': 'Vertical',
            }
    to_analyze = []

    if 'proj_emittance_X' in meta_data:
        to_analyze.append('X')
    if 'proj_emittance_Y' in meta_data:
        to_analyze.append('Y')

    if not to_analyze:
        raise ValueError('Nothing to plot')

    for dim_ctr, dim in enumerate(to_analyze):
        dim_str = dim_str_dict[dim]
        dict_ = meta_data['proj_emittance_'+dim]
        sig = dict_['beamsizes']
        err = dict_['beamsizes_err']
        sigR = dict_['reconstruction']
        M = dict_['mismatch']
        design_beamsize = dict_['design']
        emit = dict_['emittance']
        nemit = emit*rel_gammaBeta
        R11, R12 = dict_['R11'], dict_['R12']
        phase_design = dict_['phase_design']
        phase_meas = dict_['phase_meas']
        betaM, alphaM = dict_['beta'], dict_['alpha']
        betaD, alphaD = dict_['beta0'], dict_['alpha0']

        mat = np.array([R11**2, 2*R11*R12, R12**2]).T
        design_beam = np.array([dict_['beta0'], -dict_['alpha0'], dict_['gamma0']])*emit
        design_beamsize = np.sqrt(np.dot(mat, design_beam))

        sp = plt.subplot(2, 2, 2*dim_ctr+1)
        sp.grid(True)

        if np.all(phase_meas == 0):
            x_plot = phase_design
            x_label = 'Design phase advance (deg)'
        else:
            x_plot = phase_meas
            x_label = 'Reconstructed phase advance (deg)'

        sp.errorbar(x_plot, sig*1e6, fmt='bo-', yerr=err*1e6, label='Measurement')
        sp.plot(x_plot, sigR*1e6, 'r*-', label='Reconstruction')

        if measurement_type != 'Slice (multi-quad)' or dim == dimension:
            sp.plot(x_plot, design_beamsize*1e6, marker='x', ls='None', color='g', label='Design')
        sp.set_xlabel(x_label)
        sp.set_ylabel('%s beam size ($\mu$m)' % dim_str)
        sp.set_title('%s: Emittance = %.2f nm, Mismatch = %.2f' % (dim, nemit*1e9, M))
        sp.legend(loc='best')

        # Ellipse plot
        pi = np.pi
        n_points = int(1e2)

        def phase_space_ellipse(emittance, beta, alpha, n_points):

            # - parametrize an ellipse using emittance, beta, alpha
            # - evaluate this parametrization for n_points

            gamma = (1 + alpha**2)/beta

            if gamma == beta:
                tan_2phi = 0
            else:
                tan_2phi = 2*alpha / (gamma - beta)
            phi = np.arctan(tan_2phi)/2

            # Find out length of ellipse axes
            x_sq = emittance/gamma
            y_sq = emittance/beta
            sin_sq, cos_sq = np.sin(phi)**2, np.cos(phi)**2
            b4 = (-sin_sq * x_sq + cos_sq * y_sq) / (cos_sq * x_sq - sin_sq * y_sq) * emittance**2
            b = b4**(1/4)
            a = emit/b

            # Straight ellipse
            t = np.linspace(0, 2*pi, n_points)
            x = a * np.cos(t)
            y = b * np.sin(t)

            # Rotate it
            x2 = np.cos(phi) * x - np.sin(phi) * y
            y2 = np.cos(phi) * y + np.sin(phi) * x

            return x2, y2

        sp = plt.subplot(2, 2, dim_ctr*2+2)
        sp.grid(True)

        if emit != 0:
            x, y = phase_space_ellipse(emit, betaM, alphaM, n_points)
            sp.plot(x*1e6, y*1e6, lw=3)
            x, y = phase_space_ellipse(emit, betaD, alphaD, n_points)
            sp.plot(x*1e6, y*1e6, lw=3, ls='--')

        beamsizes = dict_['beamsizes']
        R11 = dict_['R11']
        R12 = dict_['R12']

        xlim = np.array(sp.get_xlim())*1.5
        ylim = np.array(sp.get_ylim())*1.5


        for ctr, (beamsize, r11, r12, er, muM, muD) in enumerate(zip(beamsizes, R11, R12, err, phase_meas, phase_design)):
            color = colorsys.hsv_to_rgb(ctr/len(R11), .9, 1.)
            if r12 != 0:
                const = beamsize/r12
                grad = -r11/r12
                xx_plot = xlim
                yy_plot = const + grad*xx_plot
                error = er/r12
                sp.fill_between(xx_plot*1e6, (yy_plot-error)*1e6, (yy_plot+error)*1e6, alpha=0.5, color=color)
            else:
                xx_plot = np.array([beamsize, beamsize])
                yy_plot = ylim
                error = er
                sp.fill_betweenx(yy_plot*1e6, (xx_plot-error)*1e6, (xx_plot+error)*1e6, alpha=0.5, color=color)

            sp.plot(xx_plot*1e6, yy_plot*1e6, label="{:.0f}° ({:.0f}°)".format(muM, muD), color=color)

        sp.set_title('%s Phase space' % dim_str)
        sp.set_xlabel('%s ($\mu$m)' % (dim))
        sp.set_ylabel("%s ($\mu$rad)" % (dim))
        sp.set_xlim(*xlim)
        sp.set_ylim(*ylim)

        # Make sure the ellipse fits to beta, gamma
        #if emit != 0:
        #    xmax, ymax = np.sqrt(emit*betaM), np.sqrt(emit*(1+alphaM**2)/betaM)
        #    sp.axhline(ymax*1e6, color='red', ls='--')
        #    sp.axvline(xmax*1e6, color='green', ls='--')

        sp.legend(title='$\Delta \mu$: M (D)', bbox_to_anchor=(1,.4))

def plotSliceEmittance(emit_dict):

    dimension = emit_dict['Input']['Dimension']
    meta_data = emit_dict['Meta_data']
    slice_data = meta_data['slice_emittance_'+dimension]
    core_data = meta_data['slice_emittance_'+dimension+'_core']
    number_of_slices = emit_dict['Input']['Number of slices']
    n_measurements = emit_dict['Input']['QuadK'].shape[1]
    index_core = core_data['index_core']

    nemitS = slice_data['normalized_emittance']
    nemitC = core_data['normalized_emittance']
    nemitX = meta_data['proj_emittance_X']['normalized_emittance']
    nemitY = meta_data['proj_emittance_Y']['normalized_emittance']
    MS = slice_data['mismatch']
    currSlice = slice_data['current']
    MC = core_data['mismatch']
    sigC = core_data['beamsizes']
    errC = core_data['beamsizes_err']
    sigRC = core_data['reconstruction']

    slice_index_array = np.arange(number_of_slices)
    meas_index_array = np.arange(n_measurements)

    plt.figure(figsize=(15, 12))
    plt.suptitle('Slice measurement in %s' % (dimension), fontsize=16)
    sp = sp_em = plt.subplot(2,2,1)
    sp.grid(True)
    sp.plot(slice_index_array, nemitS*1e9, 'k*-', label='Emittance')
    sp.set_xlabel('Slice index')
    sp.set_ylabel('Horizontal emittance (nm)')
    sp.set_title('Core Emittance%s = %.2f nm, Projected EmittanceX = %.2f nm, Projected EmittanceY = %.2f nm' % (dimension, (nemitC * 1e9), (nemitX*1e9), (nemitY*1e9)))
    sp.set_xlim(-0.5, number_of_slices-0.5)
    sp.axvline(index_core, color='black', ls='--', lw=1, label='Core slice')
    sp.legend(loc='best')

    sp = sp_mm = plt.subplot(2,2,2, sharex=sp_em)
    sp.grid(True)
    sp.plot(slice_index_array, MS, 'k*-', label='Mismatch')
    sp.set_xlabel('Slice index')
    sp.set_ylabel('Horizontal mismatch')

    MM = meta_data['proj_emittance_'+dimension]['mismatch']

    sp.set_title('Core Mismatch%s = %.2f, Projected Mismatch%s = %.2f' % (dimension, MC, dimension, MM))
    sp.axvline(index_core, color='black', ls='--', lw=1, label='Core slice')
    sp.legend(loc='best')

    sp = plt.subplot(2,2,3)
    sp.grid(True)
    sp.set_title('Measured and reconstructed beam size for the core slice')
    sp.errorbar(meas_index_array, sigC*1e6, fmt='bo-', yerr=errC*1e6,label='Measurement')
    sp.plot(meas_index_array, sigRC*1e6, 'r*-', label='Reconstruction')
    sp.set_xlabel('Measurement index')
    sp.set_ylabel('Horizontal beam size (um)')
    sp.legend(loc='best')

    sp_mis = None
    if 'misplacement' in meta_data:
        misplacement_dict = meta_data['misplacement']
        sp = sp_mis = plt.subplot(2,2,4, sharex=sp_em)
        sp.set_title('Slice misplacement')
        sp.set_xlabel('Slice index')
        sp.set_ylabel('$A_s$')
        sp.grid(True)
        sp.axvline(index_core, color='black', ls='--', lw=1, label='Core slice')
        misplacement = misplacement_dict['misplacement_proj']
        try:
            sp.plot(slice_index_array, misplacement)
        except:
            print('slice_index_array, misplacement')
            print(slice_index_array, misplacement)
            raise

    for sp in sp_mm, sp_em, sp_mis:
        if sp is None:
            continue
        sp2 = sp.twinx()
        ms.sciy()
        sp2.plot(slice_index_array, currSlice, ls='--')
        sp2.set_ylabel('Current (arb. units)')

def plotTilt(emit_dict):

    dimension = emit_dict['Input']['Dimension']
    n_measurements = emit_dict['Input']['QuadK'].shape[1]
    tilt_options = emit_dict['Input']['tilt_options']
    second_order_tilt = tilt_options['order'] >= 2
    tilt1_dict = emit_dict['Meta_data']['tilt']
    tilt2_dict = emit_dict['Meta_data']['tilt2']

    plt.figure(figsize=(14, 10))
    plt.suptitle('Tilt measurement in %s' % (dimension), fontsize=16)

    sp_ctr = 1

    orders = [(1,tilt1_dict)]
    if second_order_tilt:
        orders.append((2, tilt2_dict))

    for order, tilt_dict in orders:

        tilt, tilt_err, tiltp, tiltp_err = tilt_dict['tilt'], tilt_dict['tilt_err'], tilt_dict['tiltp'], tilt_dict['tiltp_err']
        xy, xy_err = tilt_dict['xy'], tilt_dict['xy_err']
        tilt_reconstruction = tilt_dict['reconstruction']

        if order == 1:
            mu_str, mup_str = r'$\mu$', r"$\mu'$"
        elif order == 2:
            mu_str, mup_str = r'$\mu_2$', r"$\mu_2'$"
        else:
            raise ValueError('Only orders 1 and 2 are supported. Is: %s' % order)

        sp = plt.subplot(2,2,sp_ctr)
        sp_ctr += 1
        sp.grid(True)
        sp.set_title('%.2e$\pm$ %.2e %s %.2e $\pm$ %.2e %s' % (tilt, tilt_err, mu_str, tiltp, tiltp_err, mup_str))
        sp.set_xlabel('Scan index')
        sp.set_ylabel('Tilt at Screen [au]')
        sp.ticklabel_format(style='sci', scilimits=(0,0),axis='y')

        index_array = np.arange(n_measurements) + 1
        sp.errorbar(index_array, xy, yerr=xy_err)
        sp.plot(index_array, tilt_reconstruction, marker='o', ls='None')
        sp.set_xlim(0.5, n_measurements+0.5)

        sp = plt.subplot(2,2,sp_ctr)
        sp_ctr += 1
        sp.grid(True)
        sp.set_title("%s, %s phase space" % (mu_str, mup_str))
        sp.set_xlabel(mu_str)
        sp.set_ylabel(mup_str)
        sp.ticklabel_format(style='sci', scilimits=(0,0),axis='y')
        sp.ticklabel_format(style='sci', scilimits=(0,0),axis='x')

        xx_min = min(xy.min(), tilt)
        xx_max = max(xy.max(), tilt)
        xx_size0 = xx_max - xx_min
        xx_vec = np.array([tilt - xx_size0/2*0.3, tilt + xx_size0/2*0.3])

        if dimension == 'X':
            rmat11, rmat12 = emit_dict['Input']['R11'], emit_dict['Input']['R12']
        elif dimension == 'Y':
            rmat11, rmat12 = emit_dict['Input']['R33'], emit_dict['Input']['R34']

        for ctr, (r11, r12, tilt1, tilt1_err) in enumerate(zip(rmat11, rmat12, xy, xy_err)):
            color = colorsys.hsv_to_rgb(ctr/len(rmat11), .9, 1.)
            if r12 == 0:
                sp.axvline(tilt1, color=color)
            else:
                a = tilt1/r12
                b = -r11/r12
                a_err = tilt1_err/r12
                yy = a+b*xx_vec
                sp.plot(xx_vec, yy, label='%i' % ctr, color=color)
                sp.fill_between(xx_vec, yy-a_err, yy+a_err, alpha=0.5, color=color)
        sp.axvline(tilt, color='black', ls='--')
        sp.axhline(tiltp, color='black', ls='--')

def plot_all(emit_dict, plot_tilt=True, plot_misplacement=True, noshow=False):
    meta_data = emit_dict['Meta_data']
    if 'proj_emittance_X' in meta_data or 'proj_emittance_Y' in meta_data:
        plotProjEmittance(emit_dict)
    if 'slice_emittance_X' in meta_data or 'slice_emittance_Y' in meta_data:
        plotSliceEmittance(emit_dict)
    if 'tilt' in meta_data and plot_tilt:
        plotTilt(emit_dict)
    if 'misplacement' in meta_data and plot_misplacement:
        plotMisplacement(emit_dict)

    if not noshow:
        plt.show()

