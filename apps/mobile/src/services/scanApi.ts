import { mockScanSession } from "@/data/mockData";
import { apiRequest } from "@/services/apiClient";
import { ScanSession } from "@/types";

export async function simulateScan(): Promise<ScanSession> {
  try {
    return await apiRequest<ScanSession>("/scan", {
      method: "POST",
      body: { mode: "mock" },
    });
  } catch {
    return mockScanSession;
  }
}

export async function getScanSession(scanId: string): Promise<ScanSession> {
  try {
    return await apiRequest<ScanSession>(`/scan/${scanId}`);
  } catch {
    return { ...mockScanSession, id: scanId };
  }
}

export async function confirmScanCandidate(
  scanId: string,
  candidateId: string,
): Promise<{ success: boolean }> {
  try {
    return await apiRequest<{ success: boolean }>(`/scan/${scanId}/confirm`, {
      method: "POST",
      body: { candidateId },
    });
  } catch {
    return { success: true };
  }
}

