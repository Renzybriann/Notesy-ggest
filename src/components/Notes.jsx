import React, { useState, useEffect } from 'react';
import { getNotes, createNote, deleteNote } from '../api';

const Notes = () => {
  const [notes, setNotes] = useState([]);
  const [newNoteContent, setNewNoteContent] = useState('');
  const [showSubtasks, setShowSubtasks] = useState({});

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const fetchedNotes = await getNotes();
        setNotes(fetchedNotes);
      } catch (error) {
        console.error('Error fetching notes:', error);
      }
    };
    fetchNotes();
  }, []);

  const handleCreateNote = async () => {
    if (newNoteContent.trim()) {
      try {
        const createdNote = await createNote(newNoteContent);
        setNotes([...notes, createdNote]);
        setNewNoteContent('');
      } catch (error) {
        console.error('Error creating note:', error);
      }
    }
  };

  const handleDeleteNote = async (noteId) => {
    try {
      await deleteNote(noteId);
      setNotes(notes.filter((note, index) => index !== noteId));
    } catch (error) {
      console.error('Error deleting note:', error);
    }
  };

  const toggleSubtasks = (index) => {
    setShowSubtasks((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-semibold text-center mb-6">Notesy-ggest</h1>

      <div className="mb-4">
        <textarea
          value={newNoteContent}
          onChange={(e) => setNewNoteContent(e.target.value)}
          placeholder="Write a new note"
          className="w-full p-4 border-0 rounded-lg focus:ring-2 focus:ring-blue-500 rainbow-border"
        ></textarea>

        <button
          onClick={handleCreateNote}
          className="mt-4 w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-200"
        >
          Create Note
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {notes.map((note, index) => (
          <div key={index} className="relative bg-white shadow-md rounded-lg p-6 border border-gray-200">
            <h3 className="text-base font-medium text-gray-800 mb-2">{note.content}</h3>

            <div className="flex items-center justify-between mt-4">
              {note.subtasks && note.subtasks.length > 0 && (
                <div className="relative">
                  <button
                    onClick={() => toggleSubtasks(index)}
                    className="text-sm text-blue-600 font-medium hover:underline focus:outline-none"
                  >
                    {showSubtasks[index] ? 'Hide Subtasks' : 'View Subtasks'}
                  </button>

                  {showSubtasks[index] && (
                    <div className="absolute z-10 top-8 left-0 w-80 bg-white border border-gray-300 rounded-lg shadow-lg p-4 text-sm text-gray-700">
                      <h4 className="font-semibold mb-2">Subtasks</h4>
                      <ul className="list-disc ml-5 space-y-1">
                        {note.subtasks.slice(0, 4).map((subtask, subIndex) => (
                          <li key={subIndex}>{subtask.replace(/\*\*/g, '')}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              <button
                onClick={() => handleDeleteNote(index)}
                className="text-sm text-red-500 font-medium hover:underline"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Notes;
