/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { MessageSquare, Send, Book, Upload, Trash2, ChevronRight, AlertCircle, CheckCircle2 } from 'lucide-react';

interface Source {
  content: string;
  metadata: {
    source: string;
  };
}

interface QueryResponse {
  answer: string;
  sources: Source[];
  query_rewrite?: string;
  retry_count: number;
}

export default function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [url, setUrl] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<string | null>(null);

  const handleQuery = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse(null);
    setError(null);
    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error('Failed to fetch answer');
      const data = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    if (!url.trim()) return;
    setIngesting(true);
    setIngestStatus(null);
    try {
      const res = await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls: [url] }),
      });
      if (!res.ok) throw new Error('Ingestion failed');
      const data = await res.json();
      setIngestStatus(`Success! Created ${data.num_chunks} chunks.`);
      setUrl('');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIngesting(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 font-sans text-neutral-900 selection:bg-neutral-200">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-black text-white">
              <Book size={18} />
            </div>
            <h1 className="text-xl font-semibold tracking-tight">DocuMind AI</h1>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium text-neutral-500">
             <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-green-500"></span> System Live</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-12">
        {/* Ingestion Section */}
        <section className="mb-12 rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-neutral-400">
            <Upload size={16} /> Knowledge Base Ingestion
          </h2>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Paste documentation URL here (e.g. https://docs.langchain.com/...)"
              className="flex-1 rounded-xl border border-neutral-200 px-4 py-2 text-sm outline-none transition-all focus:border-black focus:ring-2 focus:ring-neutral-200"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button
              onClick={handleIngest}
              disabled={ingesting}
              className="flex items-center gap-2 rounded-xl bg-black px-6 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {ingesting ? 'Ingesting...' : 'Ingest'}
            </button>
          </div>
          <AnimatePresence>
            {ingestStatus && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mt-4 flex items-center gap-2 text-sm text-green-600"
              >
                <CheckCircle2 size={16} /> {ingestStatus}
              </motion.div>
            )}
          </AnimatePresence>
        </section>

        {/* Query Section */}
        <div className="mb-8">
          <div className="relative">
            <textarea
              rows={3}
              placeholder="Ask anything about the documentation..."
              className="w-full resize-none rounded-2xl border-2 border-neutral-200 bg-white p-5 pr-16 text-lg outline-none transition-all focus:border-black"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleQuery())}
            />
            <button
              onClick={handleQuery}
              disabled={loading}
              className="absolute right-4 bottom-4 flex h-10 w-10 items-center justify-center rounded-xl bg-black text-white transition-transform active:scale-95 disabled:opacity-50"
            >
              {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }}><Send size={18} /></motion.div> : <Send size={18} />}
            </button>
          </div>
        </div>

        {/* Response Section */}
        <AnimatePresence mode="wait">
          {error && (
            <motion.div
              layout
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700"
            >
              <AlertCircle className="mt-0.5 shrink-0" size={18} />
              <p className="text-sm">{error}</p>
            </motion.div>
          )}

          {response && (
            <motion.div
              layout
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="rounded-2xl border border-neutral-200 bg-white p-8 shadow-sm">
                <div className="mb-4 flex items-center justify-between">
                  <span className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-neutral-400">
                    <MessageSquare size={14} /> AI Assistant Response
                  </span>
                  {response.retry_count > 0 && (
                    <span className="rounded-full bg-orange-50 px-2 py-1 text-[10px] font-bold text-orange-600">
                      RECOVERY LOOP: {response.retry_count} RETRIES
                    </span>
                  )}
                </div>
                <div className="prose prose-neutral max-w-none text-neutral-800 leading-relaxed">
                  {response.answer}
                </div>
              </div>

              {response.sources.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-widest text-neutral-400">Retrieved Sources</h3>
                  <div className="grid gap-4 sm:grid-cols-2">
                    {response.sources.map((source, i) => (
                      <motion.div
                        key={i}
                        whileHover={{ y: -2 }}
                        className="rounded-xl border border-neutral-200 bg-white p-4 text-sm transition-shadow hover:shadow-md"
                      >
                         <div className="mb-2 flex items-center justify-between font-medium text-neutral-500">
                            <span>Source {i + 1}</span>
                            <span className="truncate max-w-[150px] text-[10px]">{source.metadata.source}</span>
                         </div>
                         <p className="line-clamp-4 text-xs leading-relaxed text-neutral-600 italic">
                            "{source.content}"
                         </p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="mt-24 border-t border-neutral-200 py-12">
        <div className="mx-auto max-w-5xl px-4 text-center text-sm text-neutral-400">
          Built with LangGraph, FastAPI, and ChromaDB • © 2026 DocuMind AI
        </div>
      </footer>
    </div>
  );
}
