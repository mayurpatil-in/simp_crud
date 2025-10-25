// src/api.ts
export interface Note {
  id: number;
  title: string;
  content?: string;
}

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchNotes(): Promise<Note[]> {
  const res = await fetch(`${API_BASE}/notes`);
  return res.json();
}

export async function createNote(note: { title: string; content?: string }) {
  const res = await fetch(`${API_BASE}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(note),
  });
  return res.json();
}

export async function deleteNote(id: number) {
  const res = await fetch(`${API_BASE}/notes/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
