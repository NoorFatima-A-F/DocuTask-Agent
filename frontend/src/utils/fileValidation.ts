/**
 * Client-Side Defensive Guards & Binary Sniffing
 * Validates payload size (<=15 MB) and authenticates magic byte signatures
 * prior to any network dispatch.
 */

import { DocumentValidationResult } from '../types/document';

export const MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024; // 15 Megabytes

const MAGIC_SIGNATURES: Record<string, { bytes: number[]; offset?: number; mime: string }> = {
  pdf: {
    bytes: [0x25, 0x50, 0x44, 0x46], // %PDF
    mime: 'application/pdf',
  },
  png: {
    bytes: [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A], // PNG magic header
    mime: 'image/png',
  },
  jpeg: {
    bytes: [0xFF, 0xD8, 0xFF], // JPEG SOI marker
    mime: 'image/jpeg',
  },
  tiff_le: {
    bytes: [0x49, 0x49, 0x2A, 0x00], // II*. (Little Endian)
    mime: 'image/tiff',
  },
  tiff_be: {
    bytes: [0x4D, 0x4D, 0x00, 0x2A], // MM.* (Big Endian)
    mime: 'image/tiff',
  },
};

/**
 * Computes SHA-256 hex string of File for duplicate detection and idempotency.
 */
export async function calculateSHA256(file: File): Promise<string> {
  const arrayBuffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Validates file binary header against known file signatures.
 */
export async function validateDocumentFile(file: File): Promise<DocumentValidationResult> {
  // 1. Enforce payload size boundary (<15MB)
  if (file.size > MAX_FILE_SIZE_BYTES) {
    const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
    return {
      isValid: false,
      error: `File payload exceeds maximum boundary of 15MB (Current: ${sizeMb}MB). Rejected at client perimeter.`,
      sizeBytes: file.size,
    };
  }

  if (file.size === 0) {
    return {
      isValid: false,
      error: 'Cannot process empty (0 bytes) document payload.',
      sizeBytes: 0,
    };
  }

  // 2. Read first 16 bytes for magic byte sniffing
  const slice = file.slice(0, 16);
  const buffer = await slice.arrayBuffer();
  const headerBytes = new Uint8Array(buffer);

  let detectedMime: string | undefined = undefined;

  for (const sig of Object.values(MAGIC_SIGNATURES)) {
    const isMatch = sig.bytes.every((byte, idx) => headerBytes[idx] === byte);
    if (isMatch) {
      detectedMime = sig.mime;
      break;
    }
  }

  if (!detectedMime) {
    return {
      isValid: false,
      error: 'Unrecognized or corrupted binary signature. Supported document formats: PDF, TIFF, PNG, JPEG.',
      sizeBytes: file.size,
    };
  }

  // 3. Compute client-side SHA-256
  const sha256Hex = await calculateSHA256(file);

  return {
    isValid: true,
    detectedMimeType: detectedMime,
    sizeBytes: file.size,
    sha256Hex,
  };
}
