package stirling.software.SPDF.config;

import org.springframework.boot.servlet.MultipartConfigFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
import org.springframework.core.env.Environment;
import org.springframework.util.unit.DataSize;

import jakarta.servlet.MultipartConfigElement;

import lombok.extern.slf4j.Slf4j;

import stirling.software.SPDF.controller.web.UploadLimitService;

/**
 * Multipart upload bounds for the core preview.
 *
 * <p>The explicit Spring per-file and aggregate limits are independent. The
 * imported implementation assigned the same limit to both and silently
 * reverted to 2,000 MB, defeating application.properties defaults. The
 * legacy fileUploadLimit from settings.yml remains supported as a per-file
 * override when a dedicated Spring file-limit environment variable is absent.
 */
@Configuration
@Slf4j
public class MultipartConfiguration {
    private static final String FILE_OVERRIDE = "SPRING_SERVLET_MULTIPART_MAX_FILE_SIZE";
    private static final String REQUEST_OVERRIDE = "SPRING_SERVLET_MULTIPART_MAX_REQUEST_SIZE";
    private static final String DEFAULT_FILE_LIMIT = "128MB";
    private static final String DEFAULT_REQUEST_LIMIT = "256MB";

    private final UploadLimitService uploadLimitService;
    private final Environment environment;

    public MultipartConfiguration(UploadLimitService uploadLimitService, Environment environment) {
        this.uploadLimitService = uploadLimitService;
        this.environment = environment;
    }

    private static long positiveSize(String value, String source) {
        try {
            long bytes = DataSize.parse(value.trim()).toBytes();
            if (bytes > 0) {
                return bytes;
            }
        } catch (RuntimeException e) {
            throw new IllegalStateException("Invalid positive multipart size in " + source, e);
        }
        throw new IllegalStateException("Multipart size must be positive in " + source);
    }

    @Bean
    @DependsOn("applicationProperties")
    public MultipartConfigElement multipartConfigElement() {
        String fileOverride = environment.getProperty(FILE_OVERRIDE);
        String requestOverride = environment.getProperty(REQUEST_OVERRIDE);

        long fileBytes;
        if (fileOverride != null && !fileOverride.isBlank()) {
            fileBytes = positiveSize(fileOverride, FILE_OVERRIDE);
        } else {
            long legacyFileBytes = uploadLimitService.getUploadLimit();
            if (legacyFileBytes > 0) {
                fileBytes = legacyFileBytes;
            } else {
                fileBytes = positiveSize(
                        environment.getProperty(
                                "spring.servlet.multipart.max-file-size", DEFAULT_FILE_LIMIT),
                        "spring.servlet.multipart.max-file-size");
            }
        }

        long requestBytes = requestOverride != null && !requestOverride.isBlank()
                ? positiveSize(requestOverride, REQUEST_OVERRIDE)
                : positiveSize(
                        environment.getProperty(
                                "spring.servlet.multipart.max-request-size", DEFAULT_REQUEST_LIMIT),
                        "spring.servlet.multipart.max-request-size");

        // A larger per-file allowance than the aggregate request allowance
        // cannot actually be used; enforce and report the effective bound.
        if (fileBytes > requestBytes) {
            log.warn("Multipart per-file limit exceeds total-request limit; clamping to aggregate");
            fileBytes = requestBytes;
        }

        MultipartConfigFactory factory = new MultipartConfigFactory();
        factory.setMaxFileSize(DataSize.ofBytes(fileBytes));
        factory.setMaxRequestSize(DataSize.ofBytes(requestBytes));
        log.info("Effective multipart limits: {} bytes/file, {} bytes/request", fileBytes, requestBytes);
        return factory.createMultipartConfig();
    }
}
