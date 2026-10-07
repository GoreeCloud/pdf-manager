package stirling.software.SPDF.config;

import java.io.IOException;

import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Applies hardened browser response headers to the GoreeCloud-owned workbench surface.
 *
 * <p>The retained upstream application contains other specialized pages with their own browser
 * requirements. This filter intentionally scopes the strict policy to the GoreeCloud shell and its
 * assets rather than making an unverified claim that every retained route supports the same policy.
 */
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)
public class GoreeCloudWorkbenchSecurityHeadersFilter extends OncePerRequestFilter {

    private static final String CONTENT_SECURITY_POLICY =
            "default-src 'self'; "
                    + "script-src 'self'; "
                    + "style-src 'self'; "
                    + "img-src 'self' data: blob:; "
                    + "connect-src 'self'; "
                    + "font-src 'self'; "
                    + "object-src 'none'; "
                    + "base-uri 'self'; "
                    + "form-action 'self'; "
                    + "frame-ancestors 'self'";

    @Override
    protected void doFilterInternal(
            HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        if (isGoreeCloudWorkbenchRequest(request.getRequestURI())) {
            response.setHeader("Content-Security-Policy", CONTENT_SECURITY_POLICY);
            response.setHeader("X-Content-Type-Options", "nosniff");
            response.setHeader("X-Frame-Options", "SAMEORIGIN");
            response.setHeader("Referrer-Policy", "no-referrer");
            response.setHeader(
                    "Permissions-Policy",
                    "camera=(), microphone=(), geolocation=(), payment=(), usb=()");
            response.setHeader("Cross-Origin-Resource-Policy", "same-origin");
        }

        filterChain.doFilter(request, response);
    }

    static boolean isGoreeCloudWorkbenchRequest(String requestUri) {
        if (requestUri == null) {
            return false;
        }
        return requestUri.equals("/")
                || requestUri.equals("/index.html")
                || requestUri.startsWith("/goreecloud/");
    }
}
