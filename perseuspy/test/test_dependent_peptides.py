from unittest import TestCase, main
from os import path
from perseuspy.dependent_peptides import *
import perseuspy.io.maxquant as mqio
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
      <FileParam Type="BaseLibS.Param.FileParam, BaseLibS, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" Name="Raw files table">
	<Value>{rawFilesTable}</Value>
      </FileParam>
    </ParameterGroup>
  </Parameters>
""".format(allPeptides=path.join(TEST_DIR, 'allPeptides.txt.sample'), rawFilesTable=path.join(TEST_DIR, 'rawFilesTable.txt.sample')))

outfile = StringIO()

class TestDependentPeptides(TestCase):

    def test_reading_raw_files_table(self):
        df = mqio.read_rawFilesTable(path.join(TEST_DIR, 'rawFilesTable.txt.sample'))        
        self.assertEqual(9, len(df.columns))

    def test_reading_raw_files_table_should_fail_on_experimental_design_table(self):
        with self.assertRaises(ValueError):
            df = mqio.read_rawFilesTable(path.join(TEST_DIR, 'experimentalDesignTemplate.txt.sample'))

    def test_running_dependent_peptides_from_parameters(self):
        run_dependent_peptides_from_parameters(paramfile, outfile)
        outfile.seek(0)
        lines = outfile.readlines()
        types = lines[1]
        self.assertIn('E', types.strip().replace('#!{Type}', '').split('\t'))
        self.assertEqual(687, len(lines))

if __name__ == "__main__":
    main()
