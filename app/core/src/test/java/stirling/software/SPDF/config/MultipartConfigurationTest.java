package stirling.software.SPDF.config;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.mock.env.MockEnvironment;

import jakarta.servlet.MultipartConfigElement;

import stirling.software.SPDF.controller.web.UploadLimitService;

/** Independent multipart file and total request bounds: fail closed on invalid values. */
class MultipartConfigurationTest {
    private UploadLimitService uploadLimitService;
    private MockEnvironment environment;
    private MultipartConfiguration configuration;

    @BeforeEach
    void setUp() {
        uploadLimitService = mock(UploadLimitService.class);
        environment = new MockEnvironment();
        configuration = new MultipartConfiguration(uploadLimitService, environment);
    }

    @Test
    @DisplayName("safe default file and request bounds are independent")
    void usesBoundedDefaults() {
        MultipartConfigElement element = configuration.multipartConfigElement();
        assertThat(element.getMaxFileSize()).isEqualTo(128L * 1024 * 1024);
        assertThat(element.getMaxRequestSize()).isEqualTo(256L * 1024 * 1024);
    }

    @Test
    @DisplayName("inherited settings.yml fileUploadLimit changes per-file but not request limit")
    void usesLegacyPerFileLimitOnly() {
        when(uploadLimitService.getUploadLimit()).thenReturn(50L * 1024 * 1024);
        MultipartConfigElement element = configuration.multipartConfigElement();
        assertThat(element.getMaxFileSize()).isEqualTo(50L * 1024 * 1024);
        assertThat(element.getMaxRequestSize()).isEqualTo(256L * 1024 * 1024);
    }

    @Test
    @DisplayName("two dedicated env overrides win over legacy and stay separate")
    void dedicatedOverridesRemainIndependent() {
        when(uploadLimitService.getUploadLimit()).thenReturn(400L * 1024 * 1024);
        environment.withProperty("SPRING_SERVLET_MULTIPART_MAX_FILE_SIZE", "32KB");
        environment.withProperty("SPRING_SERVLET_MULTIPART_MAX_REQUEST_SIZE", "64KB");
        MultipartConfigElement element = configuration.multipartConfigElement();
        assertThat(element.getMaxFileSize()).isEqualTo(32L * 1024);
        assertThat(element.getMaxRequestSize()).isEqualTo(64L * 1024);
    }

    @Test
    @DisplayName("ordinary resolved Spring properties still configure independently")
    void springPropertiesAreRespected() {
        environment.withProperty("spring.servlet.multipart.max-file-size", "10MB");
        environment.withProperty("spring.servlet.multipart.max-request-size", "20MB");
        MultipartConfigElement element = configuration.multipartConfigElement();
        assertThat(element.getMaxFileSize()).isEqualTo(10L * 1024 * 1024);
        assertThat(element.getMaxRequestSize()).isEqualTo(20L * 1024 * 1024);
    }

    @Test
    @DisplayName("request budget is a final bound even if legacy file setting is larger")
    void fileLimitClampedToRequest() {
        when(uploadLimitService.getUploadLimit()).thenReturn(500L * 1024 * 1024);
        MultipartConfigElement element = configuration.multipartConfigElement();
        assertThat(element.getMaxFileSize()).isEqualTo(256L * 1024 * 1024);
        assertThat(element.getMaxRequestSize()).isEqualTo(256L * 1024 * 1024);
    }

    @Test
    @DisplayName("invalid explicit per-file limit fails startup, never expands budget")
    void invalidFileLimitFailsClosed() {
        environment.withProperty("SPRING_SERVLET_MULTIPART_MAX_FILE_SIZE", "a lot");
        assertThatThrownBy(configuration::multipartConfigElement)
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("SPRING_SERVLET_MULTIPART_MAX_FILE_SIZE");
    }

    @Test
    @DisplayName("zero aggregate request limit is rejected before request handling")
    void zeroTotalLimitFailsClosed() {
        environment.withProperty("SPRING_SERVLET_MULTIPART_MAX_REQUEST_SIZE", "0MB");
        assertThatThrownBy(configuration::multipartConfigElement)
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("SPRING_SERVLET_MULTIPART_MAX_REQUEST_SIZE");
    }

    @Test
    @DisplayName("bad resolved Spring property fails closed when env override absent")
    void invalidResolvedSpringPropertyFailsClosed() {
        environment.withProperty("spring.servlet.multipart.max-request-size", "-1MB");
        assertThatThrownBy(configuration::multipartConfigElement)
                .isInstanceOf(IllegalStateException.class);
    }
}
