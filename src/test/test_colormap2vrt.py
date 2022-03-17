#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Tests for colormap2vrt.py
#

import sys
import unittest2 as unittest
import xmlrunner
from optparse import OptionParser
import os
import filecmp
import shutil
from oe_test_utils import run_command


SCRIPT_PATH = "/usr/bin/colormap2vrt.py"
OUTPUT_DIR = "./colormap2vrt_test_data/results"
COLORMAPS_DIR = "./colormap2vrt_test_data/colormaps"
VRT_IN_DIR = "./colormap2vrt_test_data/vrt_in"
VRT_OUT_DIR = "./colormap2vrt_test_data/vrt_out"

class TestColormap2VRT(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        os.mkdir(OUTPUT_DIR)

    # Tests using colormap2vrt.py to merge a colormap with a VRT file.
    # Passes if the generated VRT file matches the VRT file that was expected to be generated.
    def test_colormap2vrt(self):
        colormap = os.path.join(COLORMAPS_DIR, "MODIS_Aqua_Chlorophyll_A.xml")
        merge_filename = os.path.join(VRT_IN_DIR, "OBPG_20151202___mrfgen_20220310.212107.743826_137_resample.vrt")
        out_filename = "OBPG_20151202___mrfgen_20220310.212107.743826_137_resample_newcolormap.vrt"
        out_filepath = os.path.join(OUTPUT_DIR, out_filename)
        expected_filepath = os.path.join(VRT_OUT_DIR, out_filename)
        fail_str = "The contents of the .vrt file generated by colormap2vrt.py does not match the expected .vrt file."
        
        cmd = "python3 {0} -c {1} -o {2} -m {3}".format(SCRIPT_PATH, colormap, out_filepath, merge_filename)
        run_command(cmd)

        self.assertTrue(filecmp.cmp(out_filepath, expected_filepath), fail_str)
    
    # Tests using colormap2vrt.py to merge a colormap with a VRT file.
    # Passes if the generated VRT file matches the VRT file that was expected to be generated.
    def test_colormap2vrt_transparent(self):
        colormap = os.path.join(COLORMAPS_DIR, "MODIS_Combined_Flood.xml")
        merge_filename = os.path.join(VRT_IN_DIR, "Flood_webmerc_20190925___mrfgen_20220315.170501.279643_16_resample.vrt")
        out_filename = "Flood_webmerc_20190925___mrfgen_20220315.170501.279643_16_resample_newcolormap.vrt"
        out_filepath = os.path.join(OUTPUT_DIR, out_filename)
        expected_filepath = os.path.join(VRT_OUT_DIR, out_filename)
        fail_str = "The contents of the .vrt file generated by colormap2vrt.py does not match the expected .vrt file."
        
        cmd = "python3 {0} -c {1} -o {2} -m {3} -t".format(SCRIPT_PATH, colormap, out_filepath, merge_filename)
        run_command(cmd)

        self.assertTrue(filecmp.cmp(out_filepath, expected_filepath), fail_str)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(OUTPUT_DIR)
        
if __name__ == '__main__':
    # Parse options before running tests
    parser = OptionParser()
    parser.add_option(
        '-o',
        '--output',
        action='store',
        type='string',
        dest='outfile',
        default='test_colormap2vrt_results.xml',
        help='Specify XML output file (default is test_colormap2vrt_results.xml')
    parser.add_option(
        '-s',
        '--start_server',
        action='store_true',
        dest='start_server',
        help='Load test configuration into Apache and quit (for debugging)')
    (options, args) = parser.parse_args()

    # --start_server option runs the test Apache setup, then quits.
    if options.start_server:
        TestColormap2VRT.setUpClass()
        sys.exit(
            'Apache has been loaded with the test configuration. No tests run.'
        )

    # Have to delete the arguments as they confuse unittest
    del sys.argv[1:]

    with open(options.outfile, 'wb') as f:
        print('\nStoring test results in "{0}"'.format(options.outfile))
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=f))
