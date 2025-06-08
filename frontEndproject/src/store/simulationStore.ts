import { create } from 'zustand';
import { SimulationActions, SimulationState } from '../types';

// stage flow (very basic for now)
const stages = [
  { name: 'ANALYSIS', duration: 3600 },
  { name: 'STRUCTURING', duration: 3600 },
  { name: 'PRESENTATION', duration: 1800 },
  { name: 'NEGOTIATION', duration: 1800 },
];

const calculateValuation = (state: SimulationState): number => {
  const ebitda = Number(state.ebitda.value) || 0;
  const multiple = Number(state.multiple.value) || 0;
  const factorScore = Number(state.factorScore.value) || 1;
  const interestRate = Number(state.interestRate.value) || 0;
  
  const baseValuation = ebitda * multiple * factorScore;
  
  const interestImpact = 1 - (interestRate / 100);
  
  return baseValuation * interestImpact;
};

const checkAgreement = (state: SimulationState): boolean => {
  const fields = ['ebitda', 'interestRate', 'multiple', 'factorScore', 'companyName', 'description'] as const;
  return fields.every(field => {
    const value = state[field];
    return typeof value === 'object' && 'status' in value && value.status === 'OK';
  });
};

const getCurrentStage = (elapsedTime: number): { current: string; next: string; nextDuration: string } => {
  let time = 0;
  for (let i = 0; i < stages.length; i++) {
    time += stages[i].duration;
    if (elapsedTime < time) {
      const next = stages[i + 1];
      return {
        current: stages[i].name,
        next: next ? next.name : 'COMPLETE',
        nextDuration: next ? `${Math.floor(next.duration / 3600)} hr` : ''
      };
    }
  }
  return { current: 'COMPLETE', next: '', nextDuration: '' };
}

export const useSimulationStore = create<SimulationState & SimulationActions>((set, get) => ({
  ebitda: { value: 0, status: 'TBD' },
  interestRate: { value: 0, status: 'TBD' },
  multiple: { value: 0, status: 'TBD' },
  factorScore: { value: 1, status: 'TBD' },
  companyName: { value: '', status: 'TBD' },
  description: { value: '', status: 'TBD' },
  currentTeam: 'team1',
  elapsedTime: 0,
  currentStage: 'ANALYSIS',
  nextStage: 'STRUCTURING',
  nextStageDuration: '1 hour',
  videoModalOpen: false,
  textModalOpen: false,
  valuation: 0,
  isAgreed: false,

  updateField: (field, value) => {
    const state = get();
    const updated = { ...state[field], value };
    const newState = { ...state, [field]: updated };
    newState.valuation = calculateValuation(newState);
    set(newState);
  },

  toggleFieldStatus: (field) => {
    const state = get();
    const nextStatus = state[field].status === 'TBD' ? 'OK' : 'TBD';
    const updated = { ...state[field], status: nextStatus };
    const isAgreed = checkAgreement({ ...state, [field]: updated });
    set({ [field]: updated, isAgreed });
  },

  setTeam: (team) => set({ currentTeam: team }),

  incrementTime: () => {
    const state = get();
    const newElapsed = state.elapsedTime + 1;
    const { current, next, nextDuration } = getCurrentStage(newElapsed);
    set({
      elapsedTime: newElapsed,
      currentStage: current,
      nextStage: next,
      nextStageDuration: nextDuration
    });
  },

  setVideoModalOpen: (open) => set({ videoModalOpen: open }),
  setTextModalOpen: (open) => set({ textModalOpen: open })
}));