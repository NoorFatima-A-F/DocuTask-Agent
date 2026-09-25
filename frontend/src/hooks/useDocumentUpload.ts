/**
 * Document Ingestion & Job Submission Orchestration Hook
 * Manages client-side defensive validation, multipart upload, and async job dispatch.
 */

import { useState } from 'react';
import { documentsApi } from '../api/documents';
import { jobsApi } from '../api/jobs';
import { validateDocumentFile } from '../utils/fileValidation';
import { UploadResponse } from '../types/document';
import { JobSubmitResponse } from '../types/job';

export interface IngestionState {
  isUploading: boolean;
  validationError: string | null;
  uploadProgress: number;
  uploadedDocument: UploadResponse | null;
  submittedJob: JobSubmitResponse | null;
}

export function useDocumentUpload(onSuccess?: (jobId: string, documentId: string) => void) {
  const [state, setState] = useState<IngestionState>({
    isUploading: false,
    validationError: null,
    uploadProgress: 0,
    uploadedDocument: null,
    submittedJob: null,
  });

  const uploadAndProcess = async (file: File) => {
    setState((prev) => ({
      ...prev,
      isUploading: true,
      validationError: null,
      uploadProgress: 15,
    }));

    try {
      // 1. Client-Side Defensive Guard (Magic Bytes & 15MB Check)
      const validation = await validateDocumentFile(file);
      if (!validation.isValid) {
        setState((prev) => ({
          ...prev,
          isUploading: false,
          validationError: validation.error || 'File validation failed',
          uploadProgress: 0,
        }));
        return;
      }

      setState((prev) => ({ ...prev, uploadProgress: 40 }));

      // 2. Dispatch POST /api/v1/documents/upload
      const uploadResult = await documentsApi.upload(file);
      setState((prev) => ({
        ...prev,
        uploadedDocument: uploadResult,
        uploadProgress: 75,
      }));

      // 3. Dispatch POST /api/v1/jobs/submit (<100ms) with priority HIGH
      const jobResult = await jobsApi.submit({
        document_id: uploadResult.id,
        document_hash: uploadResult.file_hash || validation.sha256Hex || 'sha256_placeholder',
        document_type: 'invoice',
        priority: 'HIGH',
      });

      setState((prev) => ({
        ...prev,
        isUploading: false,
        submittedJob: jobResult,
        uploadProgress: 100,
      }));

      // 4. Trigger navigation callback to Pipeline Monitor
      if (onSuccess) {
        onSuccess(jobResult.job_id, uploadResult.id);
      }
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : 'Network error occurred during document ingestion';
      setState((prev) => ({
        ...prev,
        isUploading: false,
        validationError: message,
        uploadProgress: 0,
      }));
    }
  };

  const reset = () => {
    setState({
      isUploading: false,
      validationError: null,
      uploadProgress: 0,
      uploadedDocument: null,
      submittedJob: null,
    });
  };

  return {
    ...state,
    uploadAndProcess,
    reset,
  };
}
