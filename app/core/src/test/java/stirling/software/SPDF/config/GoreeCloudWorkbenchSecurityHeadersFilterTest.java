package stirling.software.SPDF.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

class GoreeCloudWorkbenchSecurityHeadersFilterTest {

    private final GoreeCloudWorkbenchSecurityHeadersFilter filter =
            new GoreeCloudWorkbenchSecurityHeadersFilter();

    @Test
    void workbenchRootGetsStrictBrowserHeaders() throws Exception {
        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        String csp = response.getHeader("Content-Security-Policy");
        assertTrue(csp.contains("default-src 'self'"));
        assertTrue(csp.contains("frame-ancestors 'self'"));
        assertEquals("nosniff", response.getHeader("X-Content-Type-Options"));
        assertEquals("SAMEORIGIN", response.getHeader("X-Frame-Options"));
        assertEquals("no-referrer", response.getHeader("Referrer-Policy"));
        assertEquals("same-origin", response.getHeader("Cross-Origin-Resource-Policy"));
    }

    @Test
    void goreeCloudAssetsGetStrictBrowserHeaders() throws Exception {
        MockHttpServletRequest request =
                new MockHttpServletRequest("GET", "/goreecloud/pdf-manager.js");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertTrue(response.containsHeader("Content-Security-Policy"));
    }

    @Test
    void unrelatedRetainedRoutesAreNotGivenWorkbenchCsp() throws Exception {
        MockHttpServletRequest request =
                new MockHttpServletRequest("GET", "/mobile-scanner");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertNull(response.getHeader("Content-Security-Policy"));
    }
}
