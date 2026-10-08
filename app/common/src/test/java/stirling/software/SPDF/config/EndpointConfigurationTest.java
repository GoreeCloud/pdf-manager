package stirling.software.SPDF.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import org.junit.jupiter.api.Test;

class EndpointConfigurationTest {

    @Test
    void endpointKeyForUriExtractsSimpleKebab() {
        assertEquals(
                "remove-pages",
                EndpointConfiguration.endpointKeyForUri("/api/v1/general/remove-pages"));
        assertEquals(
                "compress-pdf",
                EndpointConfiguration.endpointKeyForUri("/api/v1/misc/compress-pdf"));
        assertEquals(
                "add-watermark",
                EndpointConfiguration.endpointKeyForUri("/api/v1/security/add-watermark"));
        assertEquals(
                "remove-image-pdf",
                EndpointConfiguration.endpointKeyForUri("/api/v1/general/remove-image-pdf"));
    }

    @Test
    void endpointKeyForUriComposesConvertEndpoints() {
        assertEquals(
                "pdf-to-img", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/pdf/img"));
        assertEquals(
                "pdf-to-word", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/pdf/word"));
        assertEquals(
                "pdf-to-xlsx", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/pdf/xlsx"));
        assertEquals(
                "pdf-to-epub", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/pdf/epub"));
        assertEquals(
                "img-to-pdf", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/img/pdf"));
        assertEquals(
                "file-to-pdf", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/file/pdf"));
        assertEquals(
                "html-to-pdf", EndpointConfiguration.endpointKeyForUri("/api/v1/convert/html/pdf"));
    }

    @Test
    void endpointKeyForUriReturnsNullForNonApiPaths() {
        assertNull(EndpointConfiguration.endpointKeyForUri(null));
        assertNull(EndpointConfiguration.endpointKeyForUri("/some-page"));
        assertNull(EndpointConfiguration.endpointKeyForUri("/api/v1/general"));
    }
}
