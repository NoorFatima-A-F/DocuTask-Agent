import React, { useState, useEffect } from 'react';
import {
  Upload,
  FileText,
  Clock,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  Eye,
  Activity,
  Layers,
  Sparkles,
  Server,
  ArrowRight,
  ShieldCheck,
  Zap,
} from 'lucide-react';
import { validateFileMagicBytes, ValidationResult } from './utils/fileValidation';
import { DocumentJob } from './types/document';
import { JobService, generateSampleExtractedData } from './services/jobService';
import { HITLReviewer } from './components/HITLReviewer';

export function App() {
  const [activeTab, setActiveTab] = useState<'upload' | 'queue' | 'hitl' | 'analytics'>('upload');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadPhase, setUploadPhase] = useState<'idle' | 'uploading' | 'processing'>('idle');
  const [uploadProgress, setUploadProgress] = useState<number>(0);

  // Active Job List
  const [jobs, setJobs] = useState<DocumentJob[]>([
    {
      id: 'job-sample-1',
      document_id: 'doc-8849',
      document_name: 'Apex_Logistics_Invoice_BlurryScan.pdf',
      file_size: '2.40 MB',
      mime_type: 'application/pdf',
      status: 'COMPLETED',
      progress: 100,
      current_step: 'Completed — Human-in-the-Loop Sign-off Required',
      worker_name: 'AsyncWorker-1',
      created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
      updated_at: new Date().toISOString(),
      overall_confidence: 0.81,
      requires_hitl: true,
      extracted_data: generateSampleExtractedData('blurry_scan.pdf'),
    },
    {
      id: 'job-sample-2',
      document_id: 'doc-9921',
      document_name: 'Stripe_Monthly_Platform_Receipt.pdf',
      file_size: '1.15 MB',
      mime_type: 'application/pdf',
      status: 'COMPLETED',
      progress: 100,
      current_step: 'Completed — High Confidence Verified',
      worker_name: 'AsyncWorker-1',
      created_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
      updated_at: new Date().toISOString(),
      overall_confidence: 0.98,
      requires_hitl: false,
      extracted_data: generateSampleExtractedData('stripe_receipt.pdf'),
    },
  ]);

  const [reviewingJob, setReviewingJob] = useState<DocumentJob | null>(null);

  // Handle Drag & Drop / File Selection with Magic Byte Sniffing
  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    const result = await validateFileMagicBytes(file);
    setValidationResult(result);
  };

  const handleUploadAndProcess = async () => {
    if (!selectedFile || !validationResult?.isValid) return;

    setIsUploading(true);
    setUploadPhase('uploading');
    setUploadProgress(20);

    const newJob = await JobService.uploadAndSubmitDocument(selectedFile, (progress) => {
      setUploadProgress(progress);
    });

    setJobs((prev) => [newJob, ...prev]);
    setUploadPhase('processing');

    // Poll async pipeline
    JobService.pollJobProgress(newJob, (updatedJob) => {
      setJobs((prev) => prev.map((j) => (j.id === updatedJob.id ? updatedJob : j)));
      if (updatedJob.status === 'COMPLETED') {
        setIsUploading(false);
        setUploadPhase('idle');
        setSelectedFile(null);
        setValidationResult(null);
      }
    });

    // Switch to queue view to show asynchronous progress
    setActiveTab('queue');
  };

  const handleOpenReview = (job: DocumentJob) => {
    setReviewingJob(job);
    setActiveTab('hitl');
  };

  const pendingHitlCount = jobs.filter((j) => j.requires_hitl && j.status === 'COMPLETED').length;

  return (
    <div className="min-h-screen bg-[#070B14] text-slate-100 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      {/* Top Enterprise Navigation Header */}
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/25">
              <Layers className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-base tracking-tight text-white">DocuTask Agent</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 font-semibold">
                  v1.0.0 Enterprise
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Autonomous AI Document Processing &amp; HITL Pipeline</p>
            </div>
          </div>

          {/* Service Health Indicators & Docs Link */}
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-3 text-xs bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-xl">
              <span className="flex items-center space-x-1.5 text-emerald-400 font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span>FastAPI :8000</span>
              </span>
              <span className="text-slate-600">|</span>
              <span className="flex items-center space-x-1.5 text-blue-400 font-mono">
                <Server className="w-3.5 h-3.5" />
                <span>AsyncWorker-1</span>
              </span>
            </div>

            <a
              href="/api/v1/docs"
              target="_blank"
              rel="noreferrer"
              className="text-xs font-medium px-3.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center space-x-1.5 border border-slate-700/60"
            >
              <span>Swagger API Docs</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 py-6 flex-1 flex flex-col space-y-6 w-full">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 rounded-lg bg-blue-500/10 text-blue-400">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Processed Documents</p>
              <h4 className="text-xl font-bold text-white tracking-tight">1,432</h4>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Confidence Accuracy</p>
              <h4 className="text-xl font-bold text-white tracking-tight">96.8%</h4>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 rounded-lg bg-amber-500/10 text-amber-400">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Pending HITL Reviews</p>
              <h4 className="text-xl font-bold text-white tracking-tight">{pendingHitlCount}</h4>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center space-x-3.5">
            <div className="p-2.5 rounded-lg bg-purple-500/10 text-purple-400">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Median Pipeline Latency</p>
              <h4 className="text-xl font-bold text-white tracking-tight">1.82s</h4>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
          <button
            onClick={() => setActiveTab('upload')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-medium transition ${
              activeTab === 'upload'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span>Upload &amp; Ingest</span>
          </button>

          <button
            onClick={() => setActiveTab('queue')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-medium transition ${
              activeTab === 'queue'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>Live Job Queue ({jobs.length})</span>
          </button>

          <button
            onClick={() => {
              if (reviewingJob || jobs.length > 0) {
                if (!reviewingJob) setReviewingJob(jobs[0]);
                setActiveTab('hitl');
              }
            }}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-medium transition ${
              activeTab === 'hitl'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <Eye className="w-4 h-4" />
            <span>Side-by-Side HITL Reviewer</span>
            {pendingHitlCount > 0 && (
              <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-500 text-slate-950 font-bold">
                {pendingHitlCount}
              </span>
            )}
          </button>
        </div>

        {/* TAB 1: UPLOAD & INGESTION (With Client-Side Defensive Guards) */}
        {activeTab === 'upload' && (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 flex-1">
            <div className="md:col-span-8 flex flex-col space-y-4">
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault();
                  if (e.dataTransfer.files?.[0]) handleFileSelect(e.dataTransfer.files[0]);
                }}
                className={`flex-1 border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center text-center transition-all bg-slate-900/30 ${
                  validationResult?.isValid
                    ? 'border-emerald-500/50 bg-emerald-500/5'
                    : validationResult && !validationResult.isValid
                    ? 'border-red-500/50 bg-red-500/5'
                    : 'border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4 shadow-lg">
                  <Upload className="w-8 h-8" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">
                  Drag &amp; drop document binary (PDF, PNG, JPEG, TIFF)
                </h3>
                <p className="text-xs text-slate-400 mb-6 max-w-md">
                  Protected by Client-Side Magic Byte Sniffing &amp; 10MB memory guards before network egress.
                </p>

                <label className="cursor-pointer px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white transition border border-slate-700 shadow-md">
                  Browse Document
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.png,.jpg,.jpeg,.tiff"
                    onChange={(e) => {
                      if (e.target.files?.[0]) handleFileSelect(e.target.files[0]);
                    }}
                  />
                </label>
              </div>

              {/* Defensive Sniffing Validation Feedback Banner */}
              {validationResult && (
                <div
                  className={`p-4 rounded-xl border text-xs flex items-start space-x-3 transition-all ${
                    validationResult.isValid
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-red-500/10 border-red-500/30 text-red-300'
                  }`}
                >
                  {validationResult.isValid ? (
                    <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                  ) : (
                    <AlertTriangle className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold">
                        {validationResult.isValid
                          ? '✓ Client Validation Passed (Magic Bytes Verified)'
                          : '✗ Client Validation Failed'}
                      </span>
                      <span className="font-mono text-[11px] opacity-80">
                        {selectedFile?.name} ({validationResult.fileSizeFormatted})
                      </span>
                    </div>
                    <p className="mt-1 opacity-90">
                      {validationResult.isValid
                        ? `Detected MIME signature: ${validationResult.detectedMime}. Document complies with the 10 MB payload limit and is ready for Celery queuing.`
                        : validationResult.error}
                    </p>
                  </div>
                </div>
              )}

              {/* Upload Trigger Button */}
              {selectedFile && validationResult?.isValid && (
                <button
                  onClick={handleUploadAndProcess}
                  disabled={isUploading}
                  className="w-full py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-xl shadow-blue-600/25 transition flex items-center justify-center space-x-2"
                >
                  {isUploading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Submitting to Priority Queue...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      <span>Start Asynchronous Ingestion &amp; Gemini Extraction</span>
                    </>
                  )}
                </button>
              )}
            </div>

            {/* Right Instructions Panel */}
            <div className="md:col-span-4 p-6 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between space-y-6">
              <div>
                <h4 className="text-sm font-bold text-white mb-3 flex items-center space-x-2">
                  <ShieldCheck className="w-4 h-4 text-blue-400" />
                  <span>Enterprise Guardrails</span>
                </h4>
                <ul className="space-y-3 text-xs text-slate-300">
                  <li className="flex items-start space-x-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>
                      <strong className="text-white">Asynchronous Non-Blocking Queuing:</strong> Heavy OCR runs on background workers without HTTP timeout errors.
                    </span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>
                      <strong className="text-white">Magic Byte Sniffing:</strong> Real MIME signature verification on client prevents 415 media errors.
                    </span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>
                      <strong className="text-white">Human-in-the-Loop Threshold:</strong> Fields with confidence &lt; 0.85 automatically route to human review.
                    </span>
                  </li>
                </ul>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-[11px] text-slate-400">
                <span className="font-semibold text-slate-300 block mb-1">Architecture Note:</span>
                Frontend is decoupled from the backend and connects via OpenAPI v1 REST contracts.
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: LIVE ASYNCHRONOUS JOB QUEUE */}
        {activeTab === 'queue' && (
          <div className="space-y-4 flex-1">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-white">Live Distributed Job Queue</h3>
                <p className="text-xs text-slate-400">
                  Real-time status tracking via asynchronous polling and Celery state machines.
                </p>
              </div>
            </div>

            <div className="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/40">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-3.5">Document / Task ID</th>
                    <th className="p-3.5">Status &amp; Pipeline Step</th>
                    <th className="p-3.5">Confidence</th>
                    <th className="p-3.5">Worker</th>
                    <th className="p-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {jobs.map((job) => (
                    <tr key={job.id} className="hover:bg-slate-800/20 transition">
                      <td className="p-3.5">
                        <div className="flex items-center space-x-2.5">
                          <FileText className="w-4 h-4 text-blue-400 flex-shrink-0" />
                          <div>
                            <span className="font-semibold text-slate-200 block">{job.document_name}</span>
                            <span className="text-[10px] font-mono text-slate-500">ID: {job.id}</span>
                          </div>
                        </div>
                      </td>
                      <td className="p-3.5 max-w-xs">
                        <div className="space-y-1.5">
                          <div className="flex items-center space-x-2">
                            <span
                              className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                job.status === 'COMPLETED'
                                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                  : job.status === 'RUNNING'
                                  ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                                  : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                              }`}
                            >
                              {job.status}
                            </span>
                            <span className="text-[11px] text-slate-400 truncate">{job.current_step}</span>
                          </div>
                          {job.status === 'RUNNING' && (
                            <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                              <div
                                className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                                style={{ width: `${job.progress}%` }}
                              />
                            </div>
                          )}
                        </div>
                      </td>
                      <td className="p-3.5">
                        {job.overall_confidence ? (
                          <span
                            className={`text-xs font-mono font-bold px-2 py-1 rounded-lg ${
                              job.overall_confidence >= 0.85
                                ? 'bg-emerald-500/10 text-emerald-400'
                                : 'bg-amber-500/10 text-amber-400'
                            }`}
                          >
                            {(job.overall_confidence * 100).toFixed(0)}%
                          </span>
                        ) : (
                          <span className="text-slate-500 font-mono text-[11px]">Computing...</span>
                        )}
                      </td>
                      <td className="p-3.5 font-mono text-slate-400 text-[11px]">{job.worker_name || 'Worker-Pool'}</td>
                      <td className="p-3.5 text-right">
                        {job.status === 'COMPLETED' && (
                          <button
                            onClick={() => handleOpenReview(job)}
                            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center space-x-1.5 ml-auto ${
                              job.requires_hitl
                                ? 'bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-md shadow-amber-500/20 font-bold'
                                : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                            }`}
                          >
                            <Eye className="w-3.5 h-3.5" />
                            <span>{job.requires_hitl ? 'Review HITL' : 'View Extraction'}</span>
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 3: TWO-PANE SIDE-BY-SIDE HITL REVIEWER */}
        {activeTab === 'hitl' && reviewingJob && (
          <HITLReviewer
            job={reviewingJob}
            onBack={() => setActiveTab('queue')}
            onSave={(updatedJob) => {
              setJobs((prev) => prev.map((j) => (j.id === updatedJob.id ? updatedJob : j)));
              setReviewingJob(updatedJob);
            }}
          />
        )}
      </main>
    </div>
  );
}

export default App;
