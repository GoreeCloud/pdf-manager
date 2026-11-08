package stirling.software.SPDF.config;

import java.io.IOException;
import java.util.Properties;
import java.util.UUID;

import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import stirling.software.common.model.ApplicationProperties;
import stirling.software.common.util.GeneralUtils;

@Component
@Slf4j
@Order(Ordered.HIGHEST_PRECEDENCE + 1)
@RequiredArgsConstructor
public class InitialSetup {

    private final ApplicationProperties applicationProperties;

    private static boolean isNewServer = false;

    @PostConstruct
    public void init() throws IOException {
        initUUIDKey();
        initSecretKey();
        initLegalUrls();
        initSetAppVersion();
        GeneralUtils.extractPipeline();
    }

    public void initUUIDKey() throws IOException {
        String uuid = applicationProperties.getAutomaticallyGenerated().getUUID();
        if (!GeneralUtils.isValidUUID(uuid)) {
            // Generating a random UUID as the secret key
            uuid = UUID.randomUUID().toString();
            GeneralUtils.saveKeyToSettings("AutomaticallyGenerated.UUID", uuid);
            applicationProperties.getAutomaticallyGenerated().setUUID(uuid);
        }
    }

    public void initSecretKey() throws IOException {
        String secretKey = applicationProperties.getAutomaticallyGenerated().getKey();
        if (!GeneralUtils.isValidUUID(secretKey)) {
            // Generating a random UUID as the secret key
            secretKey = UUID.randomUUID().toString();
            GeneralUtils.saveKeyToSettings("AutomaticallyGenerated.key", secretKey);
            applicationProperties.getAutomaticallyGenerated().setKey(secretKey);
        }
    }

    public void initLegalUrls() {
        // The original upstream policy URLs do not describe this derivative.
        // Legal policies must be published and explicitly configured by the operator.
        // Missing URLs remain missing: never silently write another publisher's policies.
        String termsUrl = applicationProperties.getLegal().getTermsAndConditions();
        String privacyUrl = applicationProperties.getLegal().getPrivacyPolicy();
        if (termsUrl == null || termsUrl.isBlank()
                || privacyUrl == null || privacyUrl.isBlank()) {
            log.warn("GoreeCloud PDF Manager legal policy URLs are unconfigured; "
                    + "publish verified local service policies before release");
        }
    }

    public void initSetAppVersion() throws IOException {
        // Check if this is a new server before setting the version
        String existingVersion = applicationProperties.getAutomaticallyGenerated().getAppVersion();
        isNewServer =
                existingVersion == null
                        || existingVersion.isEmpty()
                        || "0.0.0".equals(existingVersion);

        String appVersion = "0.0.0";
        Resource resource = new ClassPathResource("version.properties");
        Properties props = new Properties();
        try {
            props.load(resource.getInputStream());
            appVersion = props.getProperty("version");
        } catch (Exception e) {
        }
        GeneralUtils.saveKeyToSettings("AutomaticallyGenerated.appVersion", appVersion);
        applicationProperties.getAutomaticallyGenerated().setAppVersion(appVersion);
        applicationProperties.getAutomaticallyGenerated().setIsNewServer(isNewServer);
    }

    public static boolean isNewServer() {
        return isNewServer;
    }
}
