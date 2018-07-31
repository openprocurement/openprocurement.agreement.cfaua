import os
import unittest
from openprocurement.agreement.core.tests.base import BaseAgreementWebTest
from openprocurement.agreement.cfaua.tests.base import TEST_AGREEMENT


class AgreementResourceTest(BaseAgreementWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = TEST_AGREEMENT
    def test_id(self):
        self.assertTrue(self.agreement_id)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AgreementResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')