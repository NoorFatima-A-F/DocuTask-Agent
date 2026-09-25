/**
 * Client-Side Defensive Guards: Magic Byte Sniffing & Payload Size Validation.
 * Validates actual binary signatures before network transmission to prevent 413/415 errors.
 */

export interface ValidationResult {
  isValid: boolean;
  detectedMime: string;
  fileSizeFormatted: string;
  error?: string;
  fileBytes?: Uint8Array;
}

export const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024; // 10MB limit

/**
 * Sniffs actual binary header magic numbers from file ArrayBuffer.
 */
export async function validateFileMagicBytes(file: File): Promise<ValidationResult> {
  const fileSizeFormatted = formatBytes(file.size);

  // 1. Client-Side Size Guard (<10MB)
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return {
      isValid: false,
      detectedMime: 'unknown',
      fileSizeFormatted,
      error: `Payload Size Exceeded (${fileSizeFormatted}). Platform limit is 10 MB. Please compress or crop the file.`,
    };
  }

  if (file.size === 0) {
    return {
      isValid: false,
      detectedMime: 'unknown',
      fileSizeFormatted,
      error: 'Empty file detected (0 Bytes). Please upload a valid document binary.',
    };
  }

  // 2. Read first 16 bytes for magic number sniffing
  try {
    const buffer = await file.slice(0, 16).arrayBuffer();
    const bytes = new Uint8Array(buffer);

    let detectedMime = 'unknown';

    // PDF Magic Bytes: %PDF (0x25 0x50 0x44 0x46)
    if (bytes[0] === 0x25 && bytes[1] === 0x50 && bytes[2] === 0x44 && bytes[3] === 0x46) {
      detectedMime = 'application/pdf';
    }
    // PNG Magic Bytes: 0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A
    else if (bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4E && bytes[3] === 0x47) {
      detectedMime = 'image/png';
    }
    // JPEG Magic Bytes: 0xFF 0xD8 0xFF
    else if (bytes[0] === 0xFF && bytes[1] === 0xD8 && bytes[2] === 0xFF) {
      detectedMime = 'image/jpeg';
    }
    // TIFF Magic Bytes: Little-endian 0x49 0x49 0x2A 0x00 or Big-endian 0x4D 0x4D 0x00 0x2A
    else if ((bytes[0] === 0x49 && bytes[1] === 0x49 && bytes[2] === 0x2A && bytes[3] === 0x00) ||
             (bytes[0] === 0x4D && bytes[1] === 0x4D && bytes[2] === 0x00 && bytes[3] === 0x2A)) {
      detectedMime = 'image/tiff';
    }

    if (detectedMime === 'unknown') {
      return {
        isValid: false,
        detectedMime: 'application/octet-stream',
        fileSizeFormatted,
        error: `Invalid file signature. File header magic bytes do not match supported document types (PDF, PNG, JPEG, TIFF).`,
      };
    }

    return {
      isValid: true,
      detectedMime,
      fileSizeFormatted,
      fileBytes: bytes,
    };
  } catch (err: any) {
    return {
      isValid: false,
      detectedMime: 'unknown',
      fileSizeFormatted,
      error: `Failed to inspect file binary: ${err.message || 'Unknown read error'}`,
    };
  }
}

export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}
