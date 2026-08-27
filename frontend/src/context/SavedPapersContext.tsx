import {createContext,useContext,useEffect,useState,} from "react";
import type { Paper } from "../types/paper";
import {getSavedPapers,savePaperForUser,removeSavedPaper,} from "../services/api";
import { useAuth } from "../auth/Authcontext";


type SavedPapersContextType = {

    savedPapers: Paper[];

    savePaper: (paper: Paper) => Promise<void>;

    removePaper: (arxiv_id: string) => Promise<void>;

    isPaperSaved: (arxiv_id: string) => boolean;

};


const SavedPapersContext =
    createContext<SavedPapersContextType | null>(null);


type SavedPapersProviderProps = {

    children: React.ReactNode;

};


export function SavedPapersProvider({
    children,
}: SavedPapersProviderProps) {

    const { isAuthenticated } = useAuth();

    const [savedPapers, setSavedPapers] =
        useState<Paper[]>([]);

    useEffect(() => {

        if (!isAuthenticated) {
            setSavedPapers([]);
            return;
        }

        async function loadSavedPapers() {

            try {

                const papers =
                    await getSavedPapers();

                setSavedPapers(papers);

            } catch (error) {

                console.error(
                    "Failed to load saved papers:",
                    error
                );

            }

        }

        loadSavedPapers();

    }, [isAuthenticated]);


    const savePaper = async (paper: Paper) => {

        if (
            savedPapers.some(
                (p) =>
                    p.arxiv_id === paper.arxiv_id
            )
        ) {
            return;
        }

        try {

            await savePaperForUser(
                paper.arxiv_id
            );

            setSavedPapers((current) => [
                ...current,
                paper,
            ]);

        } catch (error) {

            console.error(
                "Failed to save paper:",
                error
            );

            throw error;

        }

    };


    const removePaper = async (
        arxiv_id: string
    ) => {

        try {

            await removeSavedPaper(
                arxiv_id
            );

            setSavedPapers((current) =>
                current.filter(
                    (paper) =>
                        paper.arxiv_id !== arxiv_id
                )
            );

        } catch (error) {

            console.error(
                "Failed to remove saved paper:",
                error
            );

            throw error;

        }

    };


    const isPaperSaved = (
        arxiv_id: string
    ) =>
        savedPapers.some(
            (paper) =>
                paper.arxiv_id === arxiv_id
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

    const context =
        useContext(SavedPapersContext);

    if (!context) {

        throw new Error(
            "useSavedPapers must be used inside SavedPapersProvider"
        );

    }

    return context;

}