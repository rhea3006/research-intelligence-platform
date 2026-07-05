import {createContext,useContext,useEffect,useState,} from "react";
import type { Paper } from "../types/paper";

type SavedPapersContextType = {
  savedPapers: Paper[];
  savePaper: (paper: Paper) => void;
  removePaper: (arxiv_id: string) => void;
  isPaperSaved: (arxiv_id: string) => boolean;
};

const SavedPapersContext =
  createContext<SavedPapersContextType | null>(null);

type SavedPapersProviderProps = {
  children: React.ReactNode;
};

export function SavedPapersProvider({children,}: SavedPapersProviderProps) {
  const [savedPapers, setSavedPapers] = useState<Paper[]>([]);

  useEffect(() => {
  const papers = localStorage.getItem("savedPapers");

  if (papers) {
    setSavedPapers(JSON.parse(papers));
  }
}, []);

const savePaper = (paper: Paper) => {
  if (
    savedPapers.some(
      (p) => p.arxiv_id === paper.arxiv_id
    )
  ) {
    return;
  }

  const updated = [...savedPapers, paper];

  setSavedPapers(updated);

  localStorage.setItem(
    "savedPapers",
    JSON.stringify(updated)
  );
};

const removePaper = (arxiv_id: string) => {
  const updated = savedPapers.filter(
    (paper) => paper.arxiv_id !== arxiv_id
  );

  setSavedPapers(updated);

  localStorage.setItem(
    "savedPapers",
    JSON.stringify(updated)
  );
};

const isPaperSaved = (arxiv_id: string) =>
  savedPapers.some(
    (paper) => paper.arxiv_id === arxiv_id
  );

  return (
    <SavedPapersContext.Provider
        value={{
        savedPapers,
        savePaper,
        removePaper,
        isPaperSaved,
        }}
    >
        {children}
    </SavedPapersContext.Provider>
    );
}

export function useSavedPapers() {
  const context = useContext(SavedPapersContext);

  if (!context) {
    throw new Error(
      "useSavedPapers must be used inside SavedPapersProvider"
    );
  }

  return context;
}
