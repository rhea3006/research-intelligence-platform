import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";
import type { Paper } from "../types/paper";

type WorkspaceContextType = {
    workspacePapers: Paper[];
    addPaper: (paper: Paper) => void;
    removePaper: (arxiv_id: string) => void;
    clearWorkspace: () => void;
    isPaperSelected: (arxiv_id: string) => boolean;
};

const WorkspaceContext =
    createContext<WorkspaceContextType | null>(null);

type WorkspaceProviderProps = {
    children: React.ReactNode;
};

export function WorkspaceProvider({
    children,
}: WorkspaceProviderProps) {

    const [workspacePapers, setWorkspacePapers] =
        useState<Paper[]>([]);

    useEffect(() => {
        const papers = localStorage.getItem("workspacePapers");

        if (papers) {
            setWorkspacePapers(JSON.parse(papers));
        }
    }, []);

    const addPaper = (paper: Paper) => {
        if (
            workspacePapers.some(
                (p) => p.arxiv_id === paper.arxiv_id
            )
        ) {
            return;
        }

        const updated = [...workspacePapers, paper];

        setWorkspacePapers(updated);

        localStorage.setItem(
            "workspacePapers",
            JSON.stringify(updated)
        );
    };

    const removePaper = (arxiv_id: string) => {
        const updated = workspacePapers.filter(
            (paper) => paper.arxiv_id !== arxiv_id
        );

        setWorkspacePapers(updated);

        localStorage.setItem(
            "workspacePapers",
            JSON.stringify(updated)
        );
    };

    const clearWorkspace = () => {
        setWorkspacePapers([]);
        localStorage.removeItem("workspacePapers");
    };

    const isPaperSelected = (arxiv_id: string) =>
        workspacePapers.some(
            (paper) => paper.arxiv_id === arxiv_id
        );

    return (
        <WorkspaceContext.Provider
            value={{
                workspacePapers,
                addPaper,
                removePaper,
                clearWorkspace,
                isPaperSelected,
            }}
        >
            {children}
        </WorkspaceContext.Provider>
    );
}

export function useWorkspace() {
    const context = useContext(WorkspaceContext);

    if (!context) {
        throw new Error(
            "useWorkspace must be used inside WorkspaceProvider"
        );
    }

    return context;
}

