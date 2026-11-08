package stirling.software.SPDF.controller.api;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;

import stirling.software.SPDF.model.api.general.MergePdfsRequest;
import stirling.software.common.model.ApplicationProperties;
import stirling.software.common.service.CustomPDFDocumentFactory;
import stirling.software.common.service.PdfMetadataService;
import stirling.software.common.util.ExceptionUtils.PdfCorruptedException;
import stirling.software.common.util.TempFileManager;
import stirling.software.common.util.TempFileRegistry;

/**
 * Real PDF prevalidation regression: invalid client files must never continue
 * into native merging or surface as generic HTTP 500 failures.
 */
class MalformedPdfMergeTest {
    private MergeController controller;

    @BeforeEach
    void setUp() {
        var pdfDocumentFactory =
                new CustomPDFDocumentFactory(mock(PdfMetadataService.class));
        var tempFileManager =
                new TempFileManager(new TempFileRegistry(), new ApplicationProperties());
        controller = new MergeController(pdfDocumentFactory, tempFileManager);
    }

    private static MockMultipartFile validPdf() throws IOException {
        try (var document = new PDDocument(); var out = new ByteArrayOutputStream()) {
            document.addPage(new PDPage());
            document.save(out);
            return new MockMultipartFile(
                    "fileInput", "valid-synthetic.pdf", MediaType.APPLICATION_PDF_VALUE, out.toByteArray());
        }
    }

    private static MergePdfsRequest request(MockMultipartFile... files) {
        var req = new MergePdfsRequest();
        req.setFileInput(files);
        req.setSortType("orderProvided");
        req.setRemoveCertSign(false);
        req.setGenerateToc(false);
        return req;
    }

    @Test
    void truncatedPdfIsRejectedWithTypedCorruptedFileException() throws Exception {
        var truncated = new MockMultipartFile(
                "fileInput",
                "truncated-synthetic.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "%PDF-1.4\n% generated truncated fixture without any PDF objects\n"
                        .getBytes(StandardCharsets.US_ASCII));
        assertThatThrownBy(() -> controller.mergePdfs(request(validPdf(), truncated), null))
                .isInstanceOf(PdfCorruptedException.class);
    }

    @Test
    void completelyEmptyPdfIsRejectedWithTypedCorruptedFileException() {
        var empty = new MockMultipartFile(
                "fileInput", "empty-synthetic.pdf", MediaType.APPLICATION_PDF_VALUE, new byte[0]);
        assertThatThrownBy(() -> controller.mergePdfs(request(empty), null))
                .isInstanceOf(PdfCorruptedException.class);
    }
}
