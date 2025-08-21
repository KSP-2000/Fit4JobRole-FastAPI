import React, { useState } from "react";
import axios from "axios";

export default function FileUploadForm() {
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [file, setFile] = useState(null);
  const [backendData, setBackendData] = useState([]);
  const [loading, setLoading] = useState(false);

  const LoadingSpinner = () => {
      return (
        <div className="flex flex-col items-center justify-center h-64 space-y-4">
          {/* Animated spinner */}
          <div className="w-16 h-16 border-4 border-blue-500 border-dashed rounded-full animate-spin"></div>
          <p className="text-gray-600 font-medium">Fetching jobs for you...</p>
        </div>
      );
    };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("role", role);
    formData.append("location", location);
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const normalizedData = Array.isArray(res.data) ? res.data : [res.data];
      setBackendData(normalizedData);
    } catch (err) {
      console.error("Upload failed:", err);
    }

    setLoading(false);
  };

  // Small helper to normalize skills (array or comma-separated string)
  const toArray = (val) => {
    if (Array.isArray(val)) return val;
    if (typeof val === "string") return val.split(",").map(s => s.trim()).filter(Boolean);
    return [];
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Page container */}
      <div className="mx-auto max-w-[var(--page-max-w)] px-4 py-10">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-5xl font-bold tracking-tight text-slate-800">
           <span className="text-blue-600">⚡</span>Fit4JobRole
          </h1>
          <p className="text-slate-500">
            Upload your resume, set role & location – match your skills with jobs.
          </p>
        </header>

        {/* Form Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <form onSubmit={handleSubmit} className="grid gap-5 md:grid-cols-2">
            {/* Role */}
            <div className="flex flex-col">
              <label className="mb-1 text-sm font-medium text-slate-700">Role</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
                placeholder="e.g. Frontend Developer"
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 placeholder:text-slate-400 outline-none focus:border-transparent focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Location */}
            <div className="flex flex-col">
              <label className="mb-1 text-sm font-medium text-slate-700">Location</label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
                placeholder="e.g. Bangalore"
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 placeholder:text-slate-400 outline-none focus:border-transparent focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* File picker – full width on md */}
            <div className="md:col-span-2">
              <label className="mb-1 block text-sm font-medium text-slate-700">Resume (PDF or DOCX)</label>

              {/* Label-as-button pattern (more stylish than raw input) */}
              <label className="flex w-full cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 px-6 py-8 text-center transition hover:border-blue-400 hover:bg-blue-50">
                <span className="text-sm text-slate-600">
                  {file ? (
                    <span className="font-medium text-slate-800">{file.name}</span>
                  ) : (
                    "Click to choose a file or drop it here"
                  )}
                </span>
                <span className="text-xs text-slate-400">Max 10 MB</span>
                <input
                  type="file"
                  className="sr-only"
                  onChange={(e) => setFile(e.target.files[0])}
                  required
                />
              </label>
            </div>

            {/* Submit button (right aligned on md) */}
            <div className="md:col-span-2 flex items-center justify-center">
              <button
                type="submit"
                className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-2.5 text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={!file}
              >
                Upload & Match
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        { loading ? LoadingSpinner() : ( backendData.length > 0 && (
          <section className="mt-10">
            <div className="mb-4 flex items-baseline justify-between">
              <h2 className="text-2xl font-semibold text-slate-800">Matched Jobs</h2>
              <span className="text-sm text-slate-500">{backendData.length} results</span>
            </div>

            {/* Responsive grid: 1 col on mobile, 2 on md, 3 on lg */}
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {backendData.map((item, idx) => {
                const matched = toArray(item.matched_skills);
                const missing = toArray(item.missing_skills);
                const pct = Number(item.match_percentage ?? 0);
                let color = "red-500";
                if (pct > 60) color = "green-500";
                else if (pct >= 30) color = "yellow-500";

                const colorMap = {
                  "green-500": "#22c55e",
                  "yellow-500": "#eab308",
                  "red-500": "#ef4444",
                };

                return (
                  <article
                    key={idx}
                    className="relative group rounded-2xl border border-slate-200 bg-white p-5 pr-24 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                  >
                    {/* Title → clickable */}
                    <a
                      href={item.job_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block text-lg font-semibold text-slate-800 decoration-blue-500 underline-offset-4 transition group-hover:text-blue-700 group-hover:underline"
                      title="Open job link"
                    >
                      {item.title || "Untitled Role"}
                    </a>

                    {/* Sub details */}
                    <div className="mt-1 text-sm text-slate-500">
                      <span className="mr-3">📍 {item.location || "—"}</span>
                      <span>🏢 {item.company_name || "—"}</span>
                    </div>

                    {/* Salary */}
                    {item.salary && (
                      <div className="mt-2 text-sm font-medium text-emerald-700">
                        💸 {item.salary}
                      </div>
                    )}

                    {/* Match progress */}
                    <div className="absolute top-2 right-2">
                      <div className="relative flex items-center justify-center w-20 h-20">
                        <div
                          className="absolute inset-0 rounded-full"
                          style={{
                            background: `conic-gradient(${colorMap[color]} ${pct}%, #e5e7eb ${pct}%)`,
                          }}
                        ></div>
                        <div className="absolute inset-2 bg-white rounded-full flex items-center justify-center">
                          <span className="text-sm font-bold">{pct}%</span>
                        </div>
                      </div>
                    </div>               

                    {/* Matched Skills */}
                    {matched.length > 0 && (
                      <div className="mt-4">
                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Matched Skills
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {matched.map((s, i) => (
                            <span
                              key={i}
                              className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700 ring-1 ring-inset ring-emerald-200"
                            >
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Missing Skills */}
                    {missing.length > 0 && (
                      <div className="mt-3">
                        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Missing Skills
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {missing.map((s, i) => (
                            <span
                              key={i}
                              className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-700 ring-1 ring-inset ring-amber-200"
                            >
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Footer: apply link */}
                    <div className="mt-5">
                      <a
                        href={item.job_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:border-blue-300 hover:text-blue-700"
                      >
                        Open Job ↗
                      </a>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        ) ) }
      </div>
    </div>
  );
}

