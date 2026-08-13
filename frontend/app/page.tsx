"use client";

import { useEffect, useState } from "react";

type AnalysisResult = {
  url: string;
  scores: {
    overall: number;
    seo: number;
    content: number;
    technical: number;
    geo: number;
  };
  features: Record<string, any>;
  recommendations: {
    id: string;
    category: string;
    priority: string;
    impact: number;
    recommendation: string;
    evidence: Record<string, any>;
  }[];
  ai_analysis: {
    executive_summary: string;
    strengths: {
      area: string;
      finding: string;
      evidence: string;
    }[];
    weaknesses: {
      area: string;
      finding: string;
      evidence: string;
    }[];
    priorities: {
      rank: number;
      recommendation_id: string;
      action: string;
      why_it_matters: string;
    }[];
    geo_insight: string;
    next_steps: string[];
  };
};

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 1800);

    return () => clearTimeout(timer);
  }, []);

  const handleAnalyze = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      console.log("ANALYSIS RESULT:", data);

      setResult(data);
    } catch (error) {
      console.error("Analysis failed:", error);

      setError(
        "Unable to analyze this website. Make sure the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setResult(null);
    setError("");
    setUrl("");
  };

  /*
   * ---------------------------------------------------------
   * SPLASH SCREEN
   * ---------------------------------------------------------
   */

  if (showSplash) {
    return (
      <main className="flex min-h-screen items-center justify-center overflow-hidden bg-[#535dcc]">
        <div className="splash-logo-wrap">
          <img
            src="/mean-media-logo.png"
            alt="Mean Media"
            className="h-32 w-32 object-contain"
          />

          <div className="mt-8 text-center">
            <p className="text-xs font-medium uppercase tracking-[0.45em] text-black/50">
              Mean Media AI
            </p>
          </div>
        </div>

        <style jsx global>{`
          .splash-logo-wrap {
            animation:
              splashIn 0.7s ease-out forwards,
              logoBlink 1.2s steps(2, end) infinite;
          }

          @keyframes splashIn {
            0% {
              opacity: 0;
              transform: scale(0.75);
            }

            100% {
              opacity: 1;
              transform: scale(1);
            }
          }

          @keyframes logoBlink {
            0%,
            45% {
              opacity: 1;
            }

            50%,
            55% {
              opacity: 0.35;
            }

            60%,
            100% {
              opacity: 1;
            }
          }
        `}</style>
      </main>
    );
  }

  /*
   * ---------------------------------------------------------
   * ANALYSIS DASHBOARD
   * ---------------------------------------------------------
   */

  if (result) {
    return (
      <main className="min-h-screen overflow-hidden bg-[#050507] text-white">
        <BackgroundGrid />

        {/* NAVIGATION */}

        <nav className="relative z-20 border-b border-white/[0.08] bg-black/60 backdrop-blur-xl">
          <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
            <button
              onClick={resetAnalysis}
              className="group flex items-center gap-3"
            >
              <img
                src="/mean-media-logo.png"
                alt="Mean Media"
                className="h-9 w-9 rounded-lg object-contain transition-transform duration-300 group-hover:scale-110"
              />

              <div className="text-left">
                <div className="text-sm font-semibold tracking-tight">
                  Mean Media
                </div>

                <div className="text-[10px] uppercase tracking-[0.2em] text-[#6873e5]">
                  Intelligence
                </div>
              </div>
            </button>

            <div className="hidden items-center gap-3 sm:flex">
              <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs text-zinc-400">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6873e5]" />
                Analysis complete
              </div>
            </div>
          </div>
        </nav>

        {/* DASHBOARD */}

        <section className="relative z-10 mx-auto max-w-7xl px-6 py-10">
          {/* HEADER */}

          <div className="mb-10">
            <div className="mb-4 flex items-center gap-2 text-[10px] uppercase tracking-[0.3em] text-[#6873e5]">
              <span className="h-px w-8 bg-[#6873e5]" />
              Website intelligence report
            </div>

            <p className="text-sm text-zinc-500">
              Analysis for
            </p>

            <h1 className="mt-2 break-all text-2xl font-semibold tracking-tight sm:text-3xl">
              {result.url}
            </h1>
          </div>

          {/* SCORE GRID */}

          <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
            <ScoreCard
              title="Overall"
              score={result.scores.overall}
              primary
            />

            <ScoreCard
              title="SEO"
              score={result.scores.seo}
            />

            <ScoreCard
              title="Content"
              score={result.scores.content}
            />

            <ScoreCard
              title="Technical"
              score={result.scores.technical}
            />

            <ScoreCard
              title="GEO"
              score={result.scores.geo}
            />
          </div>

          {/* AI ANALYSIS */}

          {result.ai_analysis && (
            <section className="pixel-panel mt-6 overflow-hidden">
              <div className="border-b border-white/[0.08] px-6 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#5964d9] text-xs font-black text-black">
                    AI
                  </div>

                  <div>
                    <h2 className="font-semibold">
                      Mean Media Intelligence
                    </h2>

                    <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600">
                      AI interpretation layer
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-6">
                <p className="max-w-5xl text-base leading-8 text-zinc-300">
                  {result.ai_analysis.executive_summary}
                </p>
              </div>
            </section>
          )}

          {/* RECOMMENDATIONS */}

          <section className="mt-12">
            <SectionLabel number="01" title="Priority Recommendations" />

            <p className="mb-5 text-sm text-zinc-500">
              Improvements identified by the Mean Media analysis engine.
            </p>

            <div className="space-y-3">
              {result.recommendations.length === 0 ? (
                <div className="pixel-panel p-6 text-sm text-zinc-500">
                  No recommendations were generated.
                </div>
              ) : (
                result.recommendations.map((recommendation, index) => (
                  <RecommendationCard
                    key={recommendation.id || index}
                    recommendation={recommendation}
                    index={index}
                  />
                ))
              )}
            </div>
          </section>

          {/* STRENGTHS / WEAKNESSES */}

          {result.ai_analysis && (
            <div className="mt-12 grid gap-4 md:grid-cols-2">
              <InsightPanel
                title="Strengths"
                items={result.ai_analysis.strengths}
                positive
              />

              <InsightPanel
                title="Areas to Improve"
                items={result.ai_analysis.weaknesses}
              />
            </div>
          )}

          {/* GEO */}

          {result.ai_analysis?.geo_insight && (
            <section className="pixel-panel mt-4 p-6">
              <SectionLabel number="04" title="GEO Insight" />

              <p className="mt-5 max-w-4xl leading-8 text-zinc-400">
                {result.ai_analysis.geo_insight}
              </p>
            </section>
          )}

          {/* NEXT STEPS */}

          {result.ai_analysis?.next_steps?.length > 0 && (
            <section className="pixel-panel mt-4 p-6">
              <SectionLabel number="05" title="Next Steps" />

              <div className="mt-5 space-y-3">
                {result.ai_analysis.next_steps.map((step, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 border-b border-white/[0.05] pb-3 last:border-0"
                  >
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-[#5964d9]/10 text-xs font-semibold text-[#7d87ef]">
                      0{index + 1}
                    </span>

                    <p className="pt-1 text-sm leading-6 text-zinc-400">
                      {step}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* RESET */}

          <div className="flex justify-center py-16">
            <button
              onClick={resetAnalysis}
              className="group flex items-center gap-3 border border-white/10 bg-white/[0.03] px-6 py-3 text-sm transition-all hover:border-[#5964d9]/50 hover:bg-[#5964d9]/10"
            >
              <span className="transition-transform group-hover:-translate-x-1">
                ←
              </span>

              Analyze another website
            </button>
          </div>
        </section>
      </main>
    );
  }

  /*
   * ---------------------------------------------------------
   * LANDING PAGE
   * ---------------------------------------------------------
   */

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#050507] text-white">
      <BackgroundGrid />

      {/* NAV */}

      <nav className="relative z-20 border-b border-white/[0.07] bg-black/40 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <div className="flex items-center gap-3">
            <img
              src="/mean-media-logo.png"
              alt="Mean Media"
              className="h-9 w-9 rounded-lg object-contain"
            />

            <div>
              <div className="text-sm font-semibold">
                Mean Media
              </div>

              <div className="text-[9px] uppercase tracking-[0.25em] text-[#6873e5]">
                AI Intelligence
              </div>
            </div>
          </div>

          <div className="hidden items-center gap-6 text-xs text-zinc-500 sm:flex">
            <span className="hover:text-white transition">
              SEO
            </span>

            <span className="hover:text-white transition">
              CONTENT
            </span>

            <span className="hover:text-white transition">
              GEO
            </span>

            <span className="flex items-center gap-2 text-zinc-400">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6873e5]" />
              Engine online
            </span>
          </div>
        </div>
      </nav>

      {/* HERO */}

      <section className="relative z-10 mx-auto flex min-h-[calc(100vh-64px)] max-w-7xl flex-col items-center px-6 pt-16 text-center sm:pt-20">
        {/* EYEBROW */}

        <div className="mb-8 flex items-center gap-3 border border-[#5964d9]/20 bg-[#5964d9]/5 px-4 py-2 font-mono text-[10px] uppercase tracking-[0.3em] text-[#7e87ec]">
          <span className="h-1.5 w-1.5 animate-pulse bg-[#6873e5]" />

          AI-powered website intelligence

          <span className="text-zinc-700">
            v0.1
          </span>
        </div>

        {/* HEADLINE */}

        <h1 className="max-w-5xl text-5xl font-semibold leading-[0.95] tracking-[-0.05em] sm:text-7xl lg:text-8xl">
          Your website.
          <span className="block text-[#6873e5]">
            Decoded.
          </span>
        </h1>

        <p className="mt-7 max-w-2xl text-base leading-7 text-zinc-500 sm:text-lg">
          Mean Media analyzes how your website performs
          across search engines, content, technical health,
          and AI-powered discovery.
        </p>

        {/* INTERACTIVE WEBSITE */}

        <div className="relative mt-14 h-[260px] w-full max-w-4xl [perspective:1200px]">
          <div className="absolute inset-0 flex items-center justify-center">
            <PixelWebsite />
          </div>
        </div>

        {/* ANALYZER */}

        <div className="relative mt-4 w-full max-w-2xl">
          <div className="pixel-input-wrap">
            <div className="flex flex-col gap-2 p-2 sm:flex-row">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleAnalyze();
                  }
                }}
                placeholder="https://example.com"
                className="h-14 flex-1 bg-transparent px-4 text-sm text-white outline-none placeholder:text-zinc-700"
              />

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="group relative h-14 overflow-hidden bg-[#5964d9] px-7 text-sm font-semibold text-black transition-all hover:bg-[#7079e8] disabled:cursor-not-allowed disabled:opacity-50"
              >
                <span className="relative z-10">
                  {loading ? "SCANNING..." : "ANALYZE WEBSITE"}
                </span>

                <span className="absolute inset-0 -translate-x-full bg-white/20 transition-transform duration-500 group-hover:translate-x-0" />
              </button>
            </div>
          </div>

          {error && (
            <div className="mt-4 border border-red-500/20 bg-red-500/5 px-4 py-3 text-left text-xs text-red-400">
              {error}
            </div>
          )}

          <p className="mt-3 text-[10px] uppercase tracking-[0.2em] text-zinc-700">
            Enter any public website URL to begin analysis
          </p>
        </div>

        {/* FEATURE SYSTEM */}

        <div className="mt-20 grid w-full max-w-5xl grid-cols-2 gap-px overflow-hidden border border-white/[0.07] bg-white/[0.07] sm:grid-cols-4">
          <FeatureCard
            number="01"
            title="SEO"
            description="Search visibility"
          />

          <FeatureCard
            number="02"
            title="CONTENT"
            description="Content intelligence"
          />

          <FeatureCard
            number="03"
            title="TECHNICAL"
            description="Technical health"
          />

          <FeatureCard
            number="04"
            title="GEO"
            description="AI discoverability"
          />
        </div>

        {/* FOOTER LABEL */}

        <div className="flex w-full max-w-5xl justify-between py-10 font-mono text-[9px] uppercase tracking-[0.25em] text-zinc-800">
          <span>Mean Media AI</span>
          <span>Built for the AI web</span>
        </div>
      </section>

      <style jsx global>{`
        .pixel-panel {
          border: 1px solid rgba(255, 255, 255, 0.08);
          background:
            linear-gradient(
              135deg,
              rgba(255, 255, 255, 0.035),
              rgba(255, 255, 255, 0.012)
            );
          box-shadow:
            0 20px 80px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .pixel-input-wrap {
          border: 1px solid rgba(89, 100, 217, 0.3);
          background:
            linear-gradient(
              90deg,
              rgba(89, 100, 217, 0.05),
              rgba(255, 255, 255, 0.02)
            );
          box-shadow:
            0 0 0 1px rgba(89, 100, 217, 0.03),
            0 20px 70px rgba(0, 0, 0, 0.35);
        }

        .pixel-input-wrap:focus-within {
          border-color: rgba(104, 115, 229, 0.65);
          box-shadow:
            0 0 30px rgba(89, 100, 217, 0.12),
            0 20px 70px rgba(0, 0, 0, 0.35);
        }

        @keyframes pixelFloat {
          0%,
          100% {
            transform: rotateX(12deg) rotateY(-8deg) translateY(0);
          }

          50% {
            transform: rotateX(15deg) rotateY(-4deg) translateY(-10px);
          }
        }

        @keyframes scan {
          0% {
            transform: translateY(-100%);
          }

          100% {
            transform: translateY(100%);
          }
        }

        @keyframes pixelPulse {
          0%,
          100% {
            opacity: 0.35;
          }

          50% {
            opacity: 1;
          }
        }

        .pixel-website {
          animation: pixelFloat 7s ease-in-out infinite;
        }

        .pixel-scan {
          animation: scan 3s linear infinite;
        }

        .pixel-pulse {
          animation: pixelPulse 2s ease-in-out infinite;
        }
      `}</style>
    </main>
  );
}

/*
 * ---------------------------------------------------------
 * PIXEL WEBSITE HERO
 * ---------------------------------------------------------
 */

function PixelWebsite() {
  const pixels = Array.from({ length: 48 });

  return (
    <div className="pixel-website group relative w-[90%] max-w-3xl cursor-crosshair">
      {/* WEBSITE FRAME */}

      <div className="relative overflow-hidden border border-[#5964d9]/30 bg-[#0a0b10] shadow-[0_30px_100px_rgba(0,0,0,0.6)]">
        {/* TOP BAR */}

        <div className="flex h-8 items-center justify-between border-b border-white/[0.08] px-4">
          <div className="flex gap-1.5">
            <span className="h-2 w-2 rounded-full bg-zinc-700" />
            <span className="h-2 w-2 rounded-full bg-zinc-700" />
            <span className="h-2 w-2 rounded-full bg-zinc-700" />
          </div>

          <div className="h-1.5 w-32 bg-white/[0.05]" />
        </div>

        {/* PIXEL CONTENT */}

        <div className="relative grid grid-cols-12 gap-1 p-5">
          {pixels.map((_, index) => {
            const active =
              index % 7 === 0 ||
              index % 11 === 0 ||
              index === 20 ||
              index === 21 ||
              index === 32;

            return (
              <div
                key={index}
                className={`aspect-square transition-all duration-500 ${
                  active
                    ? "bg-[#5964d9]/70 group-hover:bg-[#7c85ef]"
                    : "bg-white/[0.025] group-hover:bg-white/[0.045]"
                }`}
              />
            );
          })}

          {/* MOCK WEBSITE */}

          <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
            <div className="w-[55%] text-left">
              <div className="mb-3 h-2 w-16 bg-[#5964d9]" />

              <div className="h-4 w-full bg-white/[0.12]" />

              <div className="mt-2 h-4 w-[75%] bg-white/[0.08]" />

              <div className="mt-6 grid grid-cols-3 gap-2">
                <div className="h-10 border border-white/[0.08] bg-white/[0.025]" />
                <div className="h-10 border border-white/[0.08] bg-white/[0.025]" />
                <div className="h-10 border border-white/[0.08] bg-white/[0.025]" />
              </div>
            </div>
          </div>

          {/* SCAN LINE */}

          <div className="pixel-scan pointer-events-none absolute left-0 right-0 top-0 h-12 bg-gradient-to-b from-transparent via-[#5964d9]/20 to-transparent" />
        </div>

        {/* HOVER SCORE */}

        <div className="pointer-events-none absolute inset-0 flex items-center justify-center opacity-0 transition-all duration-500 group-hover:opacity-100">
          <div className="scale-75 border border-[#6873e5]/50 bg-black/80 px-8 py-5 text-center shadow-[0_0_60px_rgba(89,100,217,0.25)] backdrop-blur-md transition-transform duration-500 group-hover:scale-100">
            <div className="text-[9px] uppercase tracking-[0.35em] text-[#6873e5]">
              Website Score
            </div>

            <div className="mt-1 text-6xl font-semibold tracking-[-0.06em]">
              82
            </div>

            <div className="mt-1 text-[9px] uppercase tracking-[0.25em] text-zinc-600">
              hover to inspect
            </div>
          </div>
        </div>
      </div>

      {/* FLOATING LABELS */}

      <div className="absolute -left-3 top-8 hidden border border-white/[0.08] bg-black/80 px-3 py-2 text-[9px] uppercase tracking-[0.2em] text-zinc-500 backdrop-blur-md sm:block">
        SEO
      </div>

      <div className="absolute -right-3 bottom-10 hidden border border-white/[0.08] bg-black/80 px-3 py-2 text-[9px] uppercase tracking-[0.2em] text-zinc-500 backdrop-blur-md sm:block">
        GEO
      </div>

      <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 border border-[#5964d9]/20 bg-black px-4 py-2 text-[9px] uppercase tracking-[0.3em] text-[#6873e5]">
        scan your website →
      </div>
    </div>
  );
}

/*
 * ---------------------------------------------------------
 * BACKGROUND
 * ---------------------------------------------------------
 */

function BackgroundGrid() {
  return (
    <>
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(89,100,217,0.13),transparent_40%)]" />

      <div
        className="pointer-events-none absolute inset-0 opacity-[0.035]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.7) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.7) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />

      <div className="pointer-events-none absolute left-1/2 top-[25%] h-[400px] w-[400px] -translate-x-1/2 rounded-full bg-[#5964d9]/5 blur-[120px]" />
    </>
  );
}

/*
 * ---------------------------------------------------------
 * SECTION LABEL
 * ---------------------------------------------------------
 */

function SectionLabel({
  number,
  title,
}: {
  number: string;
  title: string;
}) {
  return (
    <div className="flex items-center gap-3">
      <span className="font-mono text-[10px] text-[#6873e5]">
        [{number}]
      </span>

      <h2 className="text-xl font-semibold tracking-tight">
        {title}
      </h2>
    </div>
  );
}

/*
 * ---------------------------------------------------------
 * SCORE CARD
 * ---------------------------------------------------------
 */

function ScoreCard({
  title,
  score,
  primary = false,
}: {
  title: string;
  score: number;
  primary?: boolean;
}) {
  const rounded = Math.round(score);

  return (
    <div
      className={`group relative overflow-hidden border p-5 transition-all duration-300 ${
        primary
          ? "border-[#5964d9]/40 bg-[#5964d9]/10 hover:border-[#6873e5]"
          : "border-white/[0.08] bg-white/[0.025] hover:border-white/20"
      }`}
    >
      <div className="flex items-center justify-between">
        <p className="text-[10px] uppercase tracking-[0.25em] text-zinc-500">
          {title}
        </p>

        {primary && (
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#6873e5]" />
        )}
      </div>

      <div className="mt-4 flex items-end gap-1">
        <span className="text-4xl font-semibold tracking-[-0.05em]">
          {rounded}
        </span>

        <span className="mb-1 text-xs text-zinc-700">
          /100
        </span>
      </div>

      <div className="mt-5 h-1 bg-white/[0.06]">
        <div
          className="h-full bg-[#6873e5] transition-all duration-1000"
          style={{
            width: `${Math.min(Math.max(score, 0), 100)}%`,
          }}
        />
      </div>
    </div>
  );
}

/*
 * ---------------------------------------------------------
 * FEATURE CARD
 * ---------------------------------------------------------
 */

function FeatureCard({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="group bg-[#08090d] p-5 text-left transition-all hover:bg-[#0d0f16]">
      <div className="flex items-center justify-between">
        <span className="font-mono text-[9px] text-zinc-700">
          / {number}
        </span>

        <span className="h-1.5 w-1.5 bg-[#5964d9]/50 transition group-hover:bg-[#6873e5]" />
      </div>

      <h3 className="mt-8 text-sm font-semibold tracking-tight">
        {title}
      </h3>

      <p className="mt-1 text-xs text-zinc-600">
        {description}
      </p>
    </div>
  );
}

/*
 * ---------------------------------------------------------
 * RECOMMENDATION CARD
 * ---------------------------------------------------------
 */

function RecommendationCard({
  recommendation,
  index,
}: {
  recommendation: AnalysisResult["recommendations"][number];
  index: number;
}) {
  const priority = recommendation.priority?.toUpperCase();

  return (
    <div className="group pixel-panel relative overflow-hidden p-5 transition-all duration-300 hover:border-[#5964d9]/40">
      <div className="absolute bottom-0 left-0 top-0 w-px bg-[#5964d9] opacity-0 transition group-hover:opacity-100" />

      <div className="flex gap-4">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center border border-white/[0.08] bg-white/[0.03] font-mono text-xs text-zinc-500">
          0{index + 1}
        </div>

        <div className="flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[9px] font-medium uppercase tracking-[0.25em] text-[#6873e5]">
              {recommendation.category}
            </span>

            <span className="border border-white/[0.08] px-2 py-0.5 text-[9px] uppercase tracking-wider text-zinc-500">
              {priority}
            </span>
          </div>

          <h3 className="mt-2 text-sm font-medium text-zinc-200">
            {recommendation.recommendation}
          </h3>

          <div className="mt-4 flex items-center gap-3">
            <div className="h-1 w-24 bg-white/[0.06]">
              <div
                className="h-full bg-[#5964d9]"
                style={{
                  width: `${Math.min(
                    recommendation.impact * 10,
                    100
                  )}%`,
                }}
              />
            </div>

            <span className="text-[9px] uppercase tracking-wider text-zinc-600">
              Impact {recommendation.impact}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

/*
 * ---------------------------------------------------------
 * INSIGHT PANEL
 * ---------------------------------------------------------
 */

function InsightPanel({
  title,
  items,
  positive = false,
}: {
  title: string;
  items: {
    area: string;
    finding: string;
    evidence: string;
  }[];
  positive?: boolean;
}) {
  return (
    <section className="pixel-panel p-6">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">
          {title}
        </h2>

        <span
          className={`h-2 w-2 ${
            positive ? "bg-[#6873e5]" : "bg-orange-400"
          }`}
        />
      </div>

      <div className="mt-6 space-y-5">
        {items?.length ? (
          items.map((item, index) => (
            <div
              key={index}
              className="border-b border-white/[0.05] pb-4 last:border-0"
            >
              <div className="text-[9px] uppercase tracking-[0.25em] text-zinc-600">
                {item.area}
              </div>

              <p className="mt-2 text-sm leading-6 text-zinc-400">
                {item.finding}
              </p>
            </div>
          ))
        ) : (
          <p className="text-sm text-zinc-600">
            No insights returned.
          </p>
        )}
      </div>
    </section>
  );
}