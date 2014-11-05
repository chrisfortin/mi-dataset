#!/usr/bin/env python

"""
@package mi.dataset.driver.velpt_ab.dcl
@file mi-dataset/mi/dataset/driver/velpt_ab/dcl/velpt_ab_dcl_recovered_driver.py
@author Joe Padula
@brief Recovered driver for the velpt_ab_dcl instrument

Release notes:

Initial Release
"""

from mi.dataset.dataset_parser import DataSetDriverConfigKeys
from mi.dataset.dataset_driver import SimpleDatasetDriver
from mi.dataset.parser.velpt_ab_dcl import VelptAbDclParser, \
    VelptAbParticleClassKey
from mi.dataset.parser.velpt_ab_dcl_particles import VelptAbDiagnosticsDataParticleRecovered, \
    VelptAbInstrumentDataParticleRecovered, \
    VelptAbDiagnosticsHeaderParticleRecovered


def parse(basePythonCodePath, sourceFilePath, particleDataHdlrObj):
    """
    This is the method called by Uframe
    :param basePythonCodePath This is the file system location of mi-dataset
    :param sourceFilePath This is the full path and filename of the file to be parsed
    :param particleDataHdlrObj Java Object to consume the output of the parser
    :return particleDataHdlrObj
    """

    with open(sourceFilePath, 'rb') as stream_handle:

        # create and instance of the concrete driver class defined below
        driver = VelptAbDclRecoveredDriver(basePythonCodePath, stream_handle, particleDataHdlrObj)
        driver.processFileStream()

    return particleDataHdlrObj


class VelptAbDclRecoveredDriver(SimpleDatasetDriver):
    """
    The velpt_ab_dcl driver class extends the SimpleDatasetDriver.
    All this needs to do is create a concrete _build_parser method
    """

    def _build_parser(self, stream_handle):

        parser_config = {
            DataSetDriverConfigKeys.PARTICLE_MODULE: 'mi.dataset.parser.velpt_ab_dcl_particles',
            DataSetDriverConfigKeys.PARTICLE_CLASS: None,
            DataSetDriverConfigKeys.PARTICLE_CLASSES_DICT: {
                VelptAbParticleClassKey.METADATA_PARTICLE_CLASS: VelptAbDiagnosticsHeaderParticleRecovered,
                VelptAbParticleClassKey.DIAGNOSTICS_PARTICLE_CLASS: VelptAbDiagnosticsDataParticleRecovered,
                VelptAbParticleClassKey.INSTRUMENT_PARTICLE_CLASS: VelptAbInstrumentDataParticleRecovered
            }
        }

        parser = VelptAbDclParser(parser_config,
                                  stream_handle,
                                  lambda state, ingested: None,
                                  lambda data: None,
                                  self._exception_callback)

        return parser
