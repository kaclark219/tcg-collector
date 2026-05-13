import { useEffect, useState } from "react";
import { CandidateMatchCard } from "@/components/CandidateMatchCard";
import { ScreenLayout } from "@/screens/shared";
import { mockCards } from "@/data/mockData";
import { confirmScanCandidate, getScanSession } from "@/services/scanApi";
import { ScanSession } from "@/types";

type ScanResultScreenProps = {
  scanId: string;
};

export function ScanResultScreen({ scanId }: ScanResultScreenProps) {
  const [session, setSession] = useState<ScanSession | null>(null);

  useEffect(() => {
    getScanSession(scanId).then(setSession);
  }, [scanId]);

  return (
    <ScreenLayout
      title="Scan Results"
      subtitle="Candidates are shown for user confirmation before anything is saved."
    >
      {session?.candidates.map((candidate) => (
        <CandidateMatchCard
          key={candidate.id}
          candidate={candidate}
          card={mockCards.find((card) => card.id === candidate.cardId)}
          onConfirm={() => {
            void confirmScanCandidate(scanId, candidate.id);
          }}
        />
      ))}
    </ScreenLayout>
  );
}

