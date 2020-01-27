import pytest

import owslib
from owslib.etree import etree
from owslib.wfs import WebFeatureService


WFS_SERVICE_URL = 'https://www.dov.vlaanderen.be/geoserver/gw_meetnetten/wfs'

# @pytest.fixture
# def mp_wfs_getfeature_200(monkeypatch):
#     """Monkeypatch the call to the remote GetFeature request of WFS
#     version 2.0.0.

#     Parameters
#     ----------
#     monkeypatch : pytest.fixture
#         PyTest monkeypatch fixture.

#     """
#     def read(*args, **kwargs):
#         with open('tests/resources/wfs_dov_getfeature_200.xml', 'r') as f:
#             data = f.read()
#             if type(data) is not bytes:
#                 data = data.encode('utf-8')
#             data = etree.fromstring(data)
#         return data

#     monkeypatch.setattr(
#         owslib.feature.common.WFSCapabilitiesReader, 'read', read)

# TO ADD: monkeypatch the openURL methode om ne te gaan of daar de juiste inpurs zijn ingegaan.

@pytest.fixture
def mp_get_base_url(monkeypatch):
    """Monkeypatch the call to the base_url WFS version 2.0.0.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def _get_base_url(*args, **kwargs):
        return 'https://www.dov.vlaanderen.be/geoserver/wfs/'

    monkeypatch.setattr(
        owslib.feature.WebFeatureService_, '_get_base_url', _get_base_url)


class TestOffline(object):
    def test_wfs_200_getfeature_(self, mp_get_base_url):
        """Test the post data

        Test whether the method is available and returns a valid
        Post message.
        """
        with open('tests/resources/wfs_dov_getcapabilities_200.xml',
                  'r') as f:
            data = f.read()
        wfs = WebFeatureService(url='http://localhost/not_applicable',
                                version='2.0.0',
                                xml=data)
        data = wfs.getPOSTGetFeatureRequest(
                typename=['dov-pub:Boringen'],
                maxfeatures=2
            )

        query_data = b'<wfs20:GetFeature xmlns:wfs20="http://www.opengis.net/wfs/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" count="2" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0.0/wfs.xsd"><wfs20:Query typeNames="dov-pub:Boringen" /></wfs20:GetFeature>'

        assert data == query_data


# class TestOnline(object):
#     @pytest.mark.online
#     @pytest.mark.skipif(not service_ok(WFS_SERVICE_URL),
#                         reason="WFS service is unreachable")
#     @pytest.mark.parametrize("wfs_version", ["2.0.0"])
#     def test_wfs_remotemd_parse_single(self, wfs_version):
#         """Test the remote metadata parsing for WFS.

#         Tests parsing the remote metadata for a single layer.

#         Test whether the method is available and returns remote metadata.

#         """
#         wfs = WebFeatureService(url=WFS_SERVICE_URL,
#                                 version=wfs_version,
#                                 parse_remote_metadata=False)

#         assert 'gw_meetnetten:meetnetten' in wfs.contents
#         layer = wfs.contents['gw_meetnetten:meetnetten']
#         layer.parse_remote_metadata()

#         mdrecords = layer.get_metadata()
#         assert type(mdrecords) is list
#         assert len(mdrecords) > 0

#         for m in mdrecords:
#             assert type(m) is owslib.iso.MD_Metadata