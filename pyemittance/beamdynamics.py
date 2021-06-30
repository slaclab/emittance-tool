"""
This module shall contain only beam dynamics calculations,
for example transfer matrix computations and reconstructions
of beam properties from measured values.
No SwissFEL or PSI specific imports, so that you don't have to
run on a special machine in order to use this file
"""

import os
import itertools
import numpy as np
import scipy
from scipy.constants import m_e, e, c
import matplotlib.pyplot as plt
#import colorsys

# Using this try/except, this file can be used when this module is executed directly or when it is imported
try:
    from . import EmittanceToolConfig
    from .linearFit import LinearFit

    from .tilt import TiltAnalyzer
    from . import myplotstyle as ms
    from .gaussfit import GaussFit
except (SystemError, ImportError):
    import EmittanceToolConfig
    from linearFit import LinearFit
    from tilt import TiltAnalyzer
    import myplotstyle as ms
    from gaussfit import GaussFit

mEl_eV = m_e/e*c**2

class EmittanceError(Exception):
    pass

def transferMatrixDrift66(Ld):
    Md1 = [[1, Ld, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 0, 1, Ld, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1]]

    return np.array(Md1, dtype=float)

def transferMatrixQuad66(Lq, kini):
    # Using complex numbers, this method is valid for positive as well as negative k values
    sin, cos, sqrt = scipy.sin, scipy.cos, scipy.sqrt # numpy trigonometric functions do not work

    kinix = kini
    kiniy = -kini
    phi10x = Lq * sqrt(kinix)
    phi10y = Lq * sqrt(kiniy)
    if kinix == 0:
        Mq10 = transferMatrixDrift66(Lq)
    else:
        Mq10 = [[cos(phi10x), sin(phi10x) / sqrt(kinix), 0, 0, 0, 0],
            [-sqrt(kinix) * sin(phi10x), cos(phi10x), 0, 0, 0, 0],
            [0, 0, cos(phi10y), sin(phi10y) / sqrt(kiniy), 0, 0],
            [0, 0, -sin(phi10y) * sqrt(kiniy), cos(phi10y), 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]]

    Mq10 = np.array(Mq10, dtype=complex)
    assert np.all(np.imag(Mq10) == 0)
    return np.real(Mq10)

def calc_emittance(xx, xpxp, xxxp):
    em_sq = xx*xpxp - xxxp**2
    if em_sq > 0:
        return np.sqrt(em_sq)
    else:
        raise EmittanceError(xx, xpxp, xxxp, em_sq)

def calc_gammaBeta(energy_eV, E0=mEl_eV):
    return np.sqrt(energy_eV * (energy_eV + 2 * E0)) / E0

def calc_gamma_rel(energy_eV, E0=mEl_eV):
    return energy_eV/E0

def calc_mismatch(beta0, alpha0, beta, alpha):
    if beta == 0.:
        return 0.
    gamma0 = (1+alpha0**2)/beta0
    gamma = (1+alpha**2)/beta
    return 0.5 * (beta*gamma0 - 2*alpha*alpha0 + gamma*beta0)

def calc_misplacement(x, xp, beta, alpha, emittance):
    if beta == 0 or emittance == 0:
        return np.zeros_like(x)
    gamma = (1+alpha**2)/beta
    a = (beta*xp**2 + 2*alpha*x*xp + gamma*x**2)/emittance
    return a

def calc_phase_advance(r11, r12, beta0, alpha0):
    gamma0 = (1+alpha0**2)/beta0
    beta1 = r11**2 * beta0 - 2*r11*r12*alpha0 + r12**2 * gamma0
    sin_mu = r12 / np.sqrt(beta1 * beta0)
    cos_mu = r11 * np.sqrt(beta0/beta1) - alpha0 * sin_mu
    mu = np.arctan2(sin_mu, cos_mu)
    return mu / np.pi * 180

def calcProjEmittanceLinear(R11, R12, betaD, alphaD, beamsizes, beamsizes_err, rel_gammaBeta):

    R11sq = R11**2
    R12sq = R12**2
    R11R12 = R11*R12
    sig_sq = beamsizes**2
    err_sq = 2*beamsizes*beamsizes_err

    A = np.array([R11sq, 2*R11R12, R12sq]).T
    y = sig_sq
    w = 1/err_sq**2

    # Request from Eduard on 2020-12-01: Ignore points with 0 beamsize
    if np.sum(beamsizes != 0) >= 3:
        w[beamsizes==0] = 0

    try:
        sol_analytic = LinearFit(A, y, w)
    except:
        print('A.shape, y.shape, w.shape, R11.shape')
        print(A.shape, y.shape, w.shape, R11.shape)
        raise

    # y_solution corresponds to squared beam sizes
    mom_xx, mom_xxp, mom_xpxp = sol_analytic.solution

    try:
        eps = calc_emittance(mom_xx, mom_xpxp, mom_xxp)
        beta = mom_xx / eps
        alpha = -mom_xxp / eps
        gamma = mom_xpxp / eps
        eps_gradient = 1./(2*eps) * np.array([[mom_xpxp, -2*mom_xxp, mom_xx]]).T
        delta_eps = sol_analytic.error_propagation(eps_gradient)
        reconstruction = np.real(scipy.sqrt(sol_analytic.y_solution))
    except EmittanceError:
        eps, beta, alpha, gamma, delta_eps = [0.,]*5
        reconstruction = np.zeros_like(beamsizes)

    gammaD = (1+alphaD**2)/betaD
    y_design = np.array([betaD, -alphaD, gammaD])*eps
    design = np.sqrt(np.dot(A, y_design))
    mismatch = calc_mismatch(betaD, alphaD, beta, alpha)
    phase_design = calc_phase_advance(R11, R12, betaD, alphaD)

    if beta == 0:
        phase_meas = np.zeros_like(R11)
    else:
        phase_meas = calc_phase_advance(R11, R12, beta, alpha)

    emittance_dict = {
            'emittance': eps,
            'normalized_emittance': eps*rel_gammaBeta,
            'normalized_emittance_err': delta_eps*rel_gammaBeta,
            'emittance_err': delta_eps,
            'mismatch': mismatch,
            'beta': beta,
            'alpha': alpha,
            'gamma': gamma,
            'beta0': betaD,
            'alpha0': alphaD,
            'gamma0': gammaD,
            'reconstruction': reconstruction,
            'popt': sol_analytic.solution,
            'pcov': sol_analytic.covariance_matrix,
            'beamsizes': beamsizes,
            'beamsizes_err': beamsizes_err,
            'design': design,
            'R11': R11,
            'R12': R12,
            'phase_meas': phase_meas,
            'phase_design': phase_design,
            }
    return emittance_dict

def calcTilt(R11, R12, xy, xy_err):
    A = np.array([R11, R12]).T
    y = xy
    w = 1./xy_err**2

    fit = LinearFit(A, y, w)
    tilt, tiltp = fit.solution
    tilt_err, tiltp_err = fit.solution_errors

    tilt_dict = {
            'tilt': tilt,
            'tiltp': tiltp,
            'tilt_err': tilt_err,
            'tiltp_err': tiltp_err,
            'reconstruction': fit.y_solution,
            'xy': xy,
            'xy_err': xy_err,
            'chi2': fit.chi_squared,
            'red_chi2': fit.red_chi_squared,
            }
    return tilt_dict

def analyzePyscanResult(Emit_data):
    Input = Emit_data['Input']
    location = Input['Measurement location']
    type_ = Input['Measurement type']
    dimension = Input['Dimension']
    energy_eV = Input['energy_eV']
    k_steps = Input['Phase advance step']
    measurement_device = Input['Measurement device']
    tilt_options = Input['tilt_options']
    use_wire_scanner = measurement_device in (EmittanceToolConfig.wire_scanner, EmittanceToolConfig.ws_bdserver)
    use_slices = type_ in ('Slice (multi-quad)', 'Slice (single-quad)',)
    instance_config_update = Input['instance_config_update']
    number_of_slices = instance_config_update['image_slices']['number_of_slices']

    # Backward compatibility with older saved data
    if 'R11' in Input:
        optics = (Input['R11'], Input['R12'], Input['R33'], Input['R34'], Input['QuadK'])
    else:
        optics = None

    analyzer = SFEmittanceMeasurementAnalyzer(location, type_, dimension, energy_eV, k_steps, '', use_wire_scanner, optics=optics)

    # Backward compatibility with older saved data
    for key in 'QuadK', 'R11', 'R12', 'R33', 'R34':
        if key not in Input:
            Input[key] = getattr(analyzer, key)

    if use_wire_scanner:
        raise NotImplementedError
    else:
        analyzer.analyzePyscanResult(Emit_data['Raw_data'], Emit_data['Magnet_data'], use_slices, number_of_slices, tilt_options, show_camera_data=False)

    meta_data = analyzer.meta_data
    return meta_data

class SFEmittanceMeasurementAnalyzer:
    """
    Emittance measurement analysis and preparation.
    """

    use_new_tilt_method = True
    # can be 'coupling' or 'coupling_slope'
    tilt_key = 'coupling_slope'

    add_err_projected = 0.05
    add_err_slice = 0.05
    add_err_tilt = 0.01

    def __init__(self, location, measurement_type, dimension='X', energy_eV=1., k_steps=1, id_string='', use_wire_scanner=False, optics=None):
        self.location = location
        self.measurement_type = measurement_type
        self.dimension = dimension
        self.energy_eV = energy_eV # Should also work when energy is not specified
        self.rel_gamma = calc_gamma_rel(energy_eV)
        self.rel_gammaBeta = calc_gammaBeta(energy_eV)
        self.dict_key = dict_key = location + '/' + measurement_type
        self.k_steps = k_steps
        self.measurementQuads = EmittanceToolConfig.MeasurementQuads[dict_key]
        self.quadDefaults = EmittanceToolConfig.defaultKValues[dict_key]
        if id_string and id_string[-1] != ' ':
            id_string += ' '
        self.id_string = id_string

        # Only important for symetric single quad scans
        if dict_key in EmittanceToolConfig.Lq_dict:
            self.Lq = EmittanceToolConfig.Lq_dict[dict_key]
            if use_wire_scanner:
                self.mu = EmittanceToolConfig.ws_muVec_dict[dict_key]
                self.Ld = EmittanceToolConfig.Ld_dict_WS[dict_key]
            else:
                self.mu = EmittanceToolConfig.muVec_dict[dict_key]
                self.Ld = EmittanceToolConfig.Ld_dict[dict_key]
            self.betaX0 = EmittanceToolConfig.bxD[dict_key]

        self.betaX0 = EmittanceToolConfig.bxD[location + '/' + measurement_type]
        self.alphaX0 = EmittanceToolConfig.axD[location + '/' + measurement_type]
        self.betaY0 = EmittanceToolConfig.byD[location + '/' + measurement_type]
        self.alphaY0 = EmittanceToolConfig.ayD[location + '/' + measurement_type]

        # Sets self.R11 and energy etc.
        if optics is None:
            if self.measurement_type in EmittanceToolConfig.single_quad_measurement_types:
                self.getTransferMatrixSymSingleQuad()
            elif self.measurement_type in EmittanceToolConfig.multi_quad_measurement_types:
                self.getTransferMatrixFile()
            else:
                raise ValueError('Measurement type %s not understood ' % self.measurement_type)
        else:
            self.R11, self.R12, self.R33, self.R34, self.QuadK, self.n_measurements = optics+(optics[-1].shape[1],)

        self.sfbd_epics_data = {}
        self.meta_data = {'sfbd_epics_data': self.sfbd_epics_data}

    def analyzeMisplacement(self, n_slices=21, n_sig=EmittanceToolConfig.default_misalignment_sig, orientation=None, show_camera_data=False, refX='mean_fit', refY='mean_fit', ref_beta_alpha=None, use_pyscan_center=False, show_reconstruction=False, tdc_voltage=None, magnet_data=None):
        """
        n_slices: Number of slices
        n_sig: Width of y_values that are taken into account for slicing
        orientation: 'X': slice along y ; 'Y': slice along x. Default: self.dimension
        show_camera_data: Debug option to show plots of the slicing
        refX, refY: slice number that is defined as centered. Acts as offset to all other slice means.
        For both refX and refY, the default is that the mean of a Gaussian fit is used as a reference.
        use_pyscan_center: Use the values from the pyscan slicing. If true: n_slicas and n_sig are irrelevant
        show_reconstruction: Another debug option to show the reconstruction of the tilt fit for individual slices
        tdc_voltage: Specify TDC voltage that was used for the measurement
        """

        if orientation is None:
            orientation = self.dimension
        assert orientation in ('X', 'Y')

        images = np.array(self.pyscan_result_dict['image'], np.int64)
        n_results, n_images, _, _ = images.shape

        if not use_pyscan_center:
            x_axis_arr = self.pyscan_result_dict['x_axis']*1e-6
            y_axis_arr = self.pyscan_result_dict['y_axis']*1e-6

        # Allocate arrays to be filled by subfunctions
        mean_sliceX = np.zeros([n_results, n_images, n_slices])
        mean_sliceY = np.zeros_like(mean_sliceX)
        current_arr = np.zeros_like(mean_sliceX)

        refX_arr = np.zeros([n_results, n_images])
        refY_arr = np.zeros_like(refX_arr)

        # I use subfunctions here to protect the namespace of the main function
        def pyscan():
            raw_data = self.pyscan_result_dict
            for n_result, n_image in itertools.product(range(n_results), range(n_images)):
                xx_slice = np.array([raw_data['slice_%i_center_x' % i][n_result, n_image] for i in range(n_slices)])*1e-6
                yy_slice = np.array([raw_data['slice_%i_center_y' % i][n_result, n_image] for i in range(n_slices)])*1e-6

                if refX == 'mean_fit':
                    # Due to the chaotic implementation of pyscan, the format of the saved data is not guaranteed.
                    # The try/except clauses handle this.
                    try:
                        gauss_x = raw_data['gr_x_fit_gauss_function_%i_%i' % (n_result, n_image)]
                        ref_x = raw_data['gr_x_axis_%i_%i' % (n_result, n_image)][gauss_x.argmax()].squeeze()*1e-6
                    except KeyError:
                        gauss_x = raw_data['gr_x_fit_gauss_function'][n_result, n_image]
                        ref_x = raw_data['gr_x_axis'][n_result, n_image][gauss_x.argmax()].squeeze()*1e-6
                else:
                    ref_x = xx_slice[refX]

                if refY == 'mean_fit':
                    try:
                        gauss_y = raw_data['gr_y_fit_gauss_function'][n_result, n_image]
                        ref_y = raw_data['gr_y_axis'][n_result, n_image][gauss_y.argmax()].squeeze()*1e-6
                    except KeyError:
                        gauss_y = raw_data['gr_y_fit_gauss_function_%i_%i' % (n_result, n_image)]
                        ref_y = raw_data['gr_y_axis_%i_%i' % (n_result, n_image)][gauss_y.argmax()].squeeze()*1e-6
                else:
                    ref_y = yy_slice[refY]

                xx_slice -= ref_x
                yy_slice -= ref_y

                refX_arr[n_result, n_image] = ref_x
                refY_arr[n_result, n_image] = ref_y
                mean_sliceX[n_result, n_image] = xx_slice
                mean_sliceY[n_result, n_image] = yy_slice
                current_arr[n_result, n_image, :] = np.array([raw_data['slice_%i_intensity' % i][n_result, n_image] for i in range(n_slices)])

        # Again use a function to protect the namespace
        def image_analysis():
            for n_result, n_image in itertools.product(range(n_results), range(n_images)):
                image = images[n_result, n_image]
                image -= image.min()
                y_axis = y_axis_arr[n_result, n_image]
                x_axis = x_axis_arr[n_result, n_image]

                gauss = GaussFit.fit_func

                projY = np.sum(image, axis=1)
                projX = np.sum(image, axis=0)

                gfY = GaussFit(y_axis, projY, sigma_00=None)
                gfX = GaussFit(x_axis, projX, sigma_00=None)

                if show_camera_data:
                    plt.figure()
                    plt.suptitle('%s debug %i %i' % (self.id_string, n_result, n_image))

                    subplot = ms.subplot_factory(2,2)
                    sp = subplot(1, title='Full y fit', xlabel='y [m]', ylabel='Intensity (arb. units')
                    sp.plot(y_axis, projY)
                    sp.axvline(gfY.mean, label='Y fit mean', color='red', ls='--')
                    sp.plot(y_axis, gauss(y_axis, *gfY.p0), label='Initial guess')
                    sp.plot(y_axis, gfY.reconstruction, label='Fit')
                    sp.legend()

                    sp = subplot(2, grid=False, title='Raw image')
                    sp.imshow(image, aspect='auto', extent=(x_axis[0], x_axis[-1], y_axis[-1], y_axis[0]))

                    sp1 = subplot(3, title='Slices 1')
                    sp2 = subplot(4, title='Slices 2')

                # Slicing
                y_max = min(gfY.mean + n_sig*gfY.sigma, y_axis.max())
                y_min = max(gfY.mean - n_sig*gfY.sigma, y_axis.min())
                index_max = int(np.argmin((y_axis - y_max)**2))
                index_min = int(np.argmin((y_axis - y_min)**2))
                slice_borders = np.array(np.linspace(index_min, index_max, n_slices+1), int)

                # Get properties (means, intensity) for each slice
                for n_slice in range(n_slices):
                    min_index = min(slice_borders[n_slice], slice_borders[n_slice+1])
                    max_index = max(slice_borders[n_slice], slice_borders[n_slice+1])

                    slice_image = image[min_index:max_index,:]
                    projX_slice = np.sum(slice_image, axis=0)
                    gf_slice = GaussFit(x_axis, projX_slice, sigma_00=None)
                    meanX_slice = gf_slice.mean
                    meanY_slice = (y_axis[min_index]+y_axis[max_index])/2

                    mean_sliceX[n_result, n_image, n_slice] = meanX_slice
                    mean_sliceY[n_result, n_image, n_slice] = meanY_slice
                    current_arr[n_result, n_image, n_slice] = np.sum(slice_image)

                    if show_camera_data:
                        sp.plot(meanX_slice, meanY_slice, marker='+', color='red')

                        if n_slice < n_slices/2:
                            sp_s = sp1
                        else:
                            sp_s = sp2
                        color = ms.colorprog(n_slice, n_slices/2+1)
                        sp_s.plot(x_axis, projX_slice, color=color)
                        sp_s.plot(x_axis, gf_slice.reconstruction, color=color, ls='--')
                        sp_s.axvline(gf_slice.mean, ls='--', color=color)

                # Obtain reference point
                if refX == 'mean_fit':
                    ref_x = gfX.mean
                else:
                    ref_x = mean_sliceX[n_result, n_image, refX]
                mean_sliceX[n_result, n_image] -= ref_x

                if refY == 'mean_fit':
                    ref_y = gfY.mean
                else:
                    ref_y = mean_sliceY[n_result, n_image, refY]
                mean_sliceY[n_result, n_image] -= ref_y

                refX_arr[n_result, n_image] = ref_x
                refY_arr[n_result, n_image] = ref_y

        # This function must work for both orientations, X or Y.
        # The correpsonding axes are simply being swapped in case the orientation is 'Y'
        if use_pyscan_center:
            if orientation == 'Y':
                refX_arr, refY_arr = refY_arr, refX_arr
                mean_sliceX, mean_sliceY = mean_sliceY, mean_sliceX
            pyscan()
        else:
            if orientation == 'Y':
                images = np.transpose(images, axes=(0,1,3,2))
                y_axis_arr, x_axis_arr = x_axis_arr, y_axis_arr
            image_analysis()

        mean_x = np.mean(mean_sliceX, axis=1)
        std_x = np.std(mean_sliceX, axis=1)+1e-10

        mean_current = np.mean(current_arr, axis=(0,1))
        std_current = np.std(current_arr, axis=(0,1))

        x0 = np.zeros(n_slices)
        xp0 = np.zeros(n_slices)
        x0_err, xp0_err = np.zeros_like(x0), np.zeros_like(xp0)
        reconstruction = np.zeros((n_results, n_slices))

        if show_reconstruction:
            plt.figure()
            plt.suptitle('%s Check reconstruction' % self.id_string)
            subplot = ms.subplot_factory(3, 3)
            n_slices_per_sp = 5
            sp_ctr = 1
            xx_rec = np.arange(n_results)

        for n_slice in range(n_slices):
            try:
                mean, std = mean_x[:,n_slice], std_x[:,n_slice]
                slice_tilt_dict = self.analyzeTilt(mean, std, self.add_err_tilt)
                x0[n_slice] = slice_tilt_dict['tilt']
                xp0[n_slice] = slice_tilt_dict['tiltp']
                x0_err[n_slice] = slice_tilt_dict['tilt_err']
                xp0_err[n_slice] = slice_tilt_dict['tiltp_err']
                reconstruction[:,n_slice] = slice_tilt_dict['reconstruction']
            except np.linalg.LinAlgError:
                print('LinAlgError occured for slice %i. Mean: %e Std: %e' % (n_slice, mean, std))
                x0[n_slice] = np.nan
                xp0[n_slice] = np.nan
                x0_err[n_slice] = np.nan
                xp0_err[n_slice] = np.nan
                reconstruction[:,n_slice] = np.nan

            if show_reconstruction:
                n_sp = n_slice % n_slices_per_sp
                color = ms.colorprog(n_sp, n_slices_per_sp)
                if n_sp == 0 and sp_ctr <= 9:
                    sp = subplot(sp_ctr, xlabel='Measurement index', ylabel='Slice position', sciy=True)
                    sp_ctr += 1
                sp.errorbar(xx_rec, mean_x[:, n_slice], yerr=std_x[:, n_slice], label=n_slice, color=color)
                sp.plot(xx_rec, slice_tilt_dict['reconstruction'], color=color, ls='--')
                sp.legend()

        # Calculate time domain from TDC properties
        mean_sliceZ = np.copy(mean_sliceY)
        try:
            if orientation == 'X':
                if tdc_voltage is None:
                    if magnet_data is None:
                        tdc_voltage = None
                    else:
                        other_names = list(magnet_data['Other'])
                        other_values = magnet_data['Other_values']
                        tdc_name = EmittanceToolConfig.tdc_dict[self.location]['pv']
                        index_tdc = other_names.index(tdc_name)
                        tdc_voltage = other_values[index_tdc]*1e6
                beta0 = EmittanceToolConfig.byD[self.location+'/'+self.measurement_type]
                alpha0 = EmittanceToolConfig.ayD[self.location+'/'+self.measurement_type]
                gamma0 = (1+alpha0**2)/beta0
                beta_screen = self.R33**2*beta0 - 2*self.R33*self.R34*alpha0 + self.R34**2*gamma0
                beta_tdc = EmittanceToolConfig.tdc_dict[self.location]['betaY_design']

                tdc_freq = EmittanceToolConfig.tdc_dict[self.location]['freq']
                k_rf = 2*np.pi*tdc_freq/c
                sin_phi = -1
                if tdc_voltage is None:
                    streaking_factor = np.ones(n_results)
                else:
                    streaking_factor = tdc_voltage/self.energy_eV*k_rf*np.sqrt(beta_tdc*beta_screen)*sin_phi

                for n_result in range(n_results):
                    mean_sliceZ[n_result] = mean_sliceY[n_result]/streaking_factor[n_result]
            elif orientation == 'Y':
                streaking_factor = np.ones(n_results)

        except KeyError:
            print('TDC voltage not saved. Streaking factor cannot be determined unless the voltage used is specified a a parameter to this function.')
            streaking_factor = np.ones(n_results)

        if orientation == 'X' and 'proj_emittance_X' in self.meta_data:
            _d = self.meta_data['proj_emittance_X']
            a_parameter_proj = calc_misplacement(x0, xp0, _d['beta'], _d['alpha'], _d['emittance'])
            if ref_beta_alpha is None:
                beta_ref = EmittanceToolConfig.bxD[self.location+'/'+self.measurement_type]
                alpha_ref = EmittanceToolConfig.axD[self.location+'/'+self.measurement_type]
            else:
                alpha_ref, beta_ref = ref_beta_alpha
            a_parameter_ref = calc_misplacement(x0, xp0, beta_ref, alpha_ref, _d['emittance'])
        elif orientation == 'Y' and 'proj_emittance_Y' in self.meta_data:
            _d = self.meta_data['proj_emittance_Y']
            a_parameter_proj = calc_misplacement(x0, xp0, _d['beta'], _d['alpha'], _d['emittance'])

            if ref_beta_alpha is None:
                beta_ref = EmittanceToolConfig.byD[self.location+'/'+self.measurement_type]
                alpha_ref = EmittanceToolConfig.ayD[self.location+'/'+self.measurement_type]
            else:
                alpha_ref, beta_ref = ref_beta_alpha
            a_parameter_ref = calc_misplacement(x0, xp0, beta_ref, alpha_ref, _d['emittance'])
        else:
            a_parameter_proj = a_parameter_ref = np.zeros_like(x0)

        if (len(a_parameter_proj) == 1 and a_parameter_proj == 0) or \
                (len(a_parameter_ref) == 1 and a_parameter_ref == 0):
            raise ValueError

        misplacement_dict = {
                'x0_slice': x0,
                'xp0_slice': xp0,
                'x0_slice_err': x0_err,
                'xp0_slice_err': xp0_err,
                'current_slice_mean': mean_current,
                'current_slice_std': std_current,
                'current': current_arr,
                'mean_sliceX': mean_sliceX,
                'mean_sliceY': mean_sliceY,
                'mean_sliceZ': mean_sliceZ,
                'reconstructionX': reconstruction,
                'ref_sliceX': refX_arr,
                'ref_sliceY': refY_arr,
                'misplacement_ref': a_parameter_ref,
                'misplacement_proj': a_parameter_proj,
                'refX': refX,
                'refY': refY,
                'n_sig': n_sig,
                'orientation': orientation,
                }

        self.meta_data['misplacement'] = misplacement_dict
        return misplacement_dict

    def calcTiltFromMisplacement(self, misplacement_dict, order):
        z = np.mean(misplacement_dict['mean_sliceZ'], axis=(0,1))
        x = misplacement_dict['x0_slice']
        xp = misplacement_dict['xp0_slice']

        fit_mu = np.polyfit(z, x, order)
        fit_mup = np.polyfit(z, xp, order)
        return fit_mu, fit_mup

    def getTiltFromCameraData(self, images, x_axis_arr, y_axis_arr, tilt_options, show_camera_data=False):
        n_results, n_images, _, _ = images.shape

        tilt2_xy_list = np.zeros([n_results, n_images])
        tilt2_xy2_list = np.zeros([n_results, n_images])
        sp_ctr = 0
        for index, n_image in itertools.product(range(n_results), range(n_images)):
            image0 = images[index, n_image]
            x_axis0 = x_axis_arr[index, n_image]
            y_axis0 = y_axis_arr[index, n_image]
            # Transpose image and axis if necessary
            if self.dimension == 'X':
                image, x_axis, y_axis = image0.T, y_axis0, x_axis0
            elif self.dimension == 'Y':
                image, x_axis, y_axis = image0, x_axis0, y_axis0

            try:
                analyzer = TiltAnalyzer(image, 1, x_axis, y_axis)
                poly = analyzer.analyzeTilt(**tilt_options)
            except:
                print(image.shape)
                print(x_axis.shape)
                print(y_axis.shape)
                raise
            tilt2_xy_list[index, n_image] = poly[1]

            second_order_tilt = len(poly) >= 2

            if second_order_tilt:
                tilt2_xy2_list[index, n_image] = poly[2]

            if show_camera_data:
                sp_ctr = sp_ctr % 8 + 1
                if sp_ctr == 1:
                    plt.figure(figsize=(18,10))
                    plt.suptitle(tilt_options)
                sp = plt.subplot(2,4,sp_ctr)
                analyzer.plotImageAveraged(sp)
                analyzer.plotFit(sp, poly)
                sp.set_title(str(poly).split('\n')[-1])

        tilt2_xy = np.mean(tilt2_xy_list, axis=1)
        tilt2_xy_err = np.std(tilt2_xy_list, axis=1)

        output_dict = {
                1: (tilt2_xy, tilt2_xy_err),
                '1_list': tilt2_xy_list,
                }

        if second_order_tilt:
            tilt2_xy2 = np.mean(tilt2_xy2_list, axis=1)
            tilt2_xy2_err = np.std(tilt2_xy2_list, axis=1)

            output_dict[2] = (tilt2_xy2, tilt2_xy2_err)
            output_dict['2_list'] = tilt2_xy2_list

        return output_dict

    def analyzePyscanResult(self, pyscan_result_dict, magnet_data, use_slices, number_of_slices=0, tilt_options=EmittanceToolConfig.default_tilt_options, show_camera_data=False, analyzeMisplacement=True, screen_resolution=0):


        if tilt_options is None:
            tilt_options = {}

        #self.use_wire_scanner = False
        #self.use_profile_monitor = True
        result_dict = self.pyscan_result_dict = pyscan_result_dict

        # Beam sizes in micrometers!
        beamsizesX = np.mean(result_dict['gr_x_fit_standard_deviation'], axis=1)*1e-6
        beamsizesX_err = np.std(result_dict['gr_x_fit_standard_deviation'], axis=1)*1e-6
        beamsizesY = np.mean(result_dict['gr_y_fit_standard_deviation'], axis=1)*1e-6
        beamsizesY_err = np.std(result_dict['gr_y_fit_standard_deviation'], axis=1)*1e-6

        if screen_resolution != 0:
            beamsizesX = np.sqrt(beamsizesX**2 - screen_resolution**2)
            beamsizesY = np.sqrt(beamsizesY**2 - screen_resolution**2)

        self.analyzeProjectedEmittance(beamsizesX, beamsizesX_err, beamsizesY, beamsizesY_err, add_err=self.add_err_projected)

        n_results, n_images = result_dict['gr_x_fit_standard_deviation'].shape

        if use_slices:
            try:
                if self.dimension == 'X':
                    xy = np.mean(1/result_dict[self.tilt_key], axis=1)
                    xy_err = np.std(1/result_dict[self.tilt_key], axis=1)
                elif self.dimension == 'Y':
                    try:
                        xy = np.mean(result_dict[self.tilt_key], axis=1)
                        xy_err = np.std(result_dict[self.tilt_key], axis=1)
                    except:
                        print(result_dict.keys(), self.tilt_key, result_dict[self.tilt_key])
                else:
                    raise ValueError('Is:', self.dimension, 'must be X or Y')

            except KeyError:
                print('Coupling data not available :(')

            if self.use_new_tilt_method:
                image = np.array(result_dict['image'], np.int64)
                x_axis = result_dict['x_axis']
                y_axis = result_dict['y_axis']
                image_tilt_dict = self.getTiltFromCameraData(image, x_axis, y_axis, tilt_options, show_camera_data=show_camera_data)
                tilt_xy, tilt_xy_err = image_tilt_dict[1]
                if tilt_options['order'] >= 2:
                    tilt2_xy2, tilt2_xy2_err = image_tilt_dict[2]
            else:
                try:
                    if self.dimension == 'X':
                        xy = np.mean(1/result_dict[self.tilt_key], axis=1)
                        xy_err = np.std(1/result_dict[self.tilt_key], axis=1)
                    elif self.dimension == 'Y':
                        try:
                            xy = np.mean(result_dict[self.tilt_key], axis=1)
                        except:
                            print(result_dict.keys(), self.tilt_key, result_dict[self.tilt_key])
                            raise
                        xy_err = np.std(result_dict[self.tilt_key], axis=1)
                    else:
                        raise ValueError(self.dimension)

                except KeyError:
                    print('Coupling data not available :(')
                tilt_xy, tilt_xy_err = xy, xy_err

        if use_slices:
            sigRawSlice = np.zeros([n_images, n_results, number_of_slices])
            intRawSlice = np.zeros([n_images, n_results, number_of_slices])
            for i in range(number_of_slices):
                try:
                    sigRawSlice[:,:,i] = result_dict['slice_%i_standard_deviation' % i].T*1e-6
                    intRawSlice[:,:,i] = result_dict['slice_%i_intensity' % i].T
                except TypeError:
                    sigRawSlice[:,:,i] = np.nan
                    intRawSlice[:,:,i] = np.nan

            sigSlice = np.mean(sigRawSlice, axis=0)
            errSlice = np.std(sigRawSlice, axis=0)

            currSlice = np.mean(intRawSlice, axis=(0,1))
            errcurrSlice = np.std(np.mean(intRawSlice, axis=0), axis=0)

            try:
                self.analyzeSlice(sigSlice, errSlice, currSlice, errcurrSlice, add_err=self.add_err_slice)
            except Exception as e:
                print(e)
                print('Slice could not be analyzed')

            print('analyzing tilt')
            self.meta_data['tilt'] = self.analyzeTilt(tilt_xy, tilt_xy_err, add_err=self.add_err_tilt)

            if tilt_options['order'] >= 2:
                self.meta_data['tilt2'] = self.analyzeTilt(tilt2_xy2, tilt2_xy2_err, add_err=self.add_err_tilt)

            self.sigSlice = sigSlice
            self.errSlice = errSlice

            if analyzeMisplacement:
                self.analyzeMisplacement(number_of_slices, EmittanceToolConfig.default_misalignment_sig, magnet_data=magnet_data, show_camera_data=show_camera_data)

    def getTransferMatrixSymSingleQuad(self):
        R11, R12, R33, R34 = [], [], [], []

        # calculate k-values, considering steps in phase-advance
        kl = 1 / (np.tan(np.deg2rad(-self.mu)) * self.betaX0)
        kini = (kl / self.Lq)[::self.k_steps]
        self.QuadK = QuadK = np.zeros((len(self.quadDefaults), len(kini)))

        for index, (_, val) in enumerate(self.quadDefaults):
            if val is None:
                QuadK[index,:] = kini
            else:
                QuadK[index,:] = val

        # calculate transfer matrices
        Md1 = transferMatrixDrift66(self.Ld)

        for kini_i in kini:
            Mq10 = transferMatrixQuad66(self.Lq, kini_i)

            M = np.dot(Md1, Mq10)
            R11.append(M[0,0])
            R12.append(M[0,1])
            R33.append(M[2,2])
            R34.append(M[2,3])

        arr = lambda x: np.array(x, float)

        self.R11, self.R12, self.R33, self.R34 = arr(R11), arr(R12), arr(R33), arr(R34)
        self.n_measurements = len(kini)

        return self.R11, self.R12, self.R33, self.R34

    def getTransferMatrixFile(self):
        '''
        For txt files
        '''
        file_, mag_length = EmittanceToolConfig.files_constants_dict[self.dict_key]
        kini_file = file_ + {'X':'', 'Y':'Y'}[self.dimension] + '.txt'
        R_file = file_ + {'X':'', 'Y':'Y'}[self.dimension] + '_mat.txt'


        def _loadtxt(file_):
            path = os.path.join(os.path.dirname(__file__), file_)
            return np.loadtxt(path)

        kini0 = _loadtxt(kini_file) / mag_length
        R = _loadtxt(R_file)

        # considering steps in phase-advance
        k_steps = self.k_steps

        kini = kini0[::k_steps]
        QuadK = self.QuadK = np.zeros((len(self.measurementQuads), len(kini)))
        kiniT = kini.transpose()

        index_temp = 0
        for n_quad, (quadName, default) in enumerate(self.quadDefaults):
            if default == '__file__':
                QuadK[n_quad,:] = kiniT[index_temp,:]
                index_temp += 1
            else:
                QuadK[n_quad,:] = default

        self.R11 = R[0,::k_steps]
        self.R12 = R[1,::k_steps]
        self.R33 = R[2,::k_steps]
        self.R34 = R[3,::k_steps]

        self.n_measurements = len(kini)

        return self.R11, self.R12, self.R33, self.R34

    def analyzeProjectedEmittance(self, beamsizesX, beamsizesX_err, beamsizesY, beamsizesY_err, add_err):

        for dimension, beamsizes, beamsizes_err, r11, r12, beta0, alpha0 in [
                ('X', beamsizesX, beamsizesX_err, self.R11, self.R12, self.betaX0, self.alphaX0),
                ('Y', beamsizesY, beamsizesY_err, self.R33, self.R34, self.betaY0, self.alphaY0),
                ]:

            beamsizes_err = np.sqrt(beamsizes_err**2 + (beamsizes*add_err)**2)
            emittance_dict = d = calcProjEmittanceLinear(r11, r12, beta0, alpha0, beamsizes, beamsizes_err, self.rel_gammaBeta)

            self.meta_data['proj_emittance_'+dimension] = emittance_dict

            if not (self.measurement_type in EmittanceToolConfig.slice_measurement_types and dimension != self.dimension):
                self.sfbd_epics_data.update({
                    'EMITTANCE-'+dimension: d['emittance']*1e9,
                    'MISMATCH-'+dimension: d['mismatch'],
                    'BETA-'+dimension: d['beta'],
                    'ALPHA-'+dimension: d['alpha'],
                    })

    def analyzeSlice(self, sigSlice, sigSlice_err, currSlice, currSlice_err, add_err=0.05):
        """
        Provide slice emittane measurement results.
        Shape: n_results, number of slices.
        No data for different images, this has to be done before.
        """

        n_results, number_of_slices = sigSlice.shape
        sigSlice_err = np.sqrt(sigSlice_err**2 + (sigSlice*add_err)**2)

        if self.dimension == 'X':
            r11, r12 = self.R11, self.R12
            beta0, alpha0 = self.betaX0, self.alphaX0
        elif self.dimension == 'Y':
            r11, r12 = self.R33, self.R34
            beta0, alpha0 = self.betaY0, self.alphaY0
        gamma0 = (1+alpha0**2)/beta0

        emitS = np.zeros(number_of_slices)
        nemitS = np.zeros(number_of_slices)
        betaS = np.zeros(number_of_slices)
        alphaS = np.zeros(number_of_slices)
        gammaS = np.zeros(number_of_slices)
        MS = np.zeros(number_of_slices)
        sigR = np.zeros([number_of_slices, self.n_measurements])

        for i in range(number_of_slices):
            sliceEmittancedict = calcProjEmittanceLinear(r11, r12, beta0, alpha0, sigSlice[:,i], sigSlice_err[:,i], self.rel_gammaBeta)
            emitS[i] = sliceEmittancedict['emittance']
            nemitS[i] = sliceEmittancedict['emittance']*self.rel_gammaBeta
            betaS[i] = sliceEmittancedict['beta']
            alphaS[i] = sliceEmittancedict['alpha']
            gammaS[i] = sliceEmittancedict['gamma']
            MS[i] = sliceEmittancedict['mismatch']
            sigR[i,:] = sliceEmittancedict['reconstruction']

        # core parameters
        index_core = int(round(number_of_slices / 2))
        emitC = emitS[index_core]
        nemitC = nemitS[index_core]
        betaC = betaS[index_core]
        alphaC = alphaS[index_core]
        gammaC = gammaS[index_core]
        MC = MS[index_core]
        sigRC = sigR[index_core,:]
        sigC = sigSlice[:,index_core]
        errC = sigSlice_err[:,index_core]

        emittance_dict = {
            'emittance': emitS,
            'normalized_emittance': nemitS,
            'mismatch': MS,
            'beta': betaS,
            'alpha': alphaS,
            'gamma': gammaS,
            'beta0': beta0,
            'alpha0': alpha0,
            'gamma0': gamma0,
            'reconstruction': sigR,
            'beamsizes': sigSlice,
            'beamsizes_err': sigSlice_err,
            'R11': self.R11,
            'R12': self.R12,
            'current': currSlice,
            'current_err': currSlice_err,
            }

        emittance_dict_core = {
            'emittance': emitC,
            'normalized_emittance': nemitC,
            'mismatch': MC,
            'beta': betaC,
            'alpha': alphaC,
            'gamma': gammaC,
            'beta0': beta0,
            'alpha0': alpha0,
            'gamma0': gamma0,
            'reconstruction': sigRC,
            'beamsizes': sigC,
            'beamsizes_err': errC,
            'R11': self.R11,
            'R12': self.R12,
            'index_core': index_core,
            }

        self.meta_data['slice_emittance_%s' % self.dimension] = emittance_dict
        self.meta_data['slice_emittance_%s_core' % self.dimension] = emittance_dict_core
        self.sfbd_epics_data.update({
            'EMITTANCE-%s-SLICE' % self.dimension: nemitS*1e9,
            'MISMATCH-%s-SLICE' % self.dimension: MS,
            'BETA-%s-SLICE' % self.dimension: betaS,
            'ALPHA-%s-SLICE' % self.dimension: alphaS,
            })

    def analyzeTilt(self, xy, xy_err, add_err=0.):

        xy_err[xy_err == 0] = xy_err.max()
        xy_err2 = np.sqrt(xy_err**2 + (add_err*xy)**2)
        del xy_err

        if self.dimension == 'X':
            tilt_dict = calcTilt(self.R11, self.R12, xy, xy_err2)
        elif self.dimension == 'Y':
            tilt_dict = calcTilt(self.R33, self.R34, xy, xy_err2)

        self.meta_data['tilt'] = tilt_dict
        return tilt_dict

