import { useEffect, useState } from "react";
import { fetchNotes, createNote, deleteNote } from "./api";
import type { Note } from "./api"; // <--- type-only import

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // Load notes on mount
  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    const data = await fetchNotes();
    setNotes(data);
  }

  async function handleCreate() {
    if (!title) return;
    await createNote({ title, content });
    setTitle("");
    setContent("");
    loadNotes();
  }

  async function handleDelete(id: number) {
    await deleteNote(id);
    loadNotes();
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>My Notes CRUD App</h1>

      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button onClick={handleCreate}>Add Note</button>
      </div>

      <ul>
        {notes.map((note) => (
          <li key={note.id}>
            <strong>{note.title}</strong>: {note.content}{" "}
            <button onClick={() => handleDelete(note.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
