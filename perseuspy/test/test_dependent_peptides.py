from unittest import TestCase
from os import path
from perseuspy.dependent_peptides import *
from perseuspy.parameters import *
from io import StringIO

TEST_DIR = path.dirname(__file__)
import numpy as np

paramfile = StringIO("""
  <Parameters>
    <ParameterGroup Name="" CollapsedDefault="false">
      <FileParam Type="BaseLibS.Param.FileParam, BaseLibS, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" Name="allPeptides.txt">
	<Value>{allPeptides}</Value>
      </FileParam>
      <FileParam Type="BaseLibS.Param.FileParam, BaseLibS, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" Name="experimentalDesign.txt">
	<Value>{experimentalDesign}</Value>
      </FileParam>
    </ParameterGroup>
  </Parameters>
""".format(allPeptides=path.join(TEST_DIR, 'allPeptides.txt.sample'), experimentalDesign=path.join(TEST_DIR, 'experimentalDesign.txt.sample')))

outfile = StringIO()

class TestDependentPeptides(TestCase):

    def test_running_dependent_peptides_from_parameters(self):
        run_dependent_peptides_from_parameters(paramfile, outfile)
        outfile.seek(0)
        lines = outfile.readlines()
        types = lines[1]
        self.assertIn('E', types.strip().replace('#!{Type}', '').split('\t'))
        self.assertEqual(687, len(lines))
